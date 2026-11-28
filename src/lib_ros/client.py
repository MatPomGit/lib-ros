"""Synchronous client; application controls when callbacks run."""
from math import isfinite
from time import monotonic
from .models import RosError, RosTimeout, RosWriteDisabled, ConnectionHealth


def _timeout(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("timeout must be a non-negative finite number")
    if not isfinite(value) or value < 0:
        raise ValueError("timeout must be a non-negative finite number")
    return float(value)


def _qos(value):
    if type(value) is int and value > 0:
        return value
    if isinstance(value, str) and value == "sensor_data":
        return value
    raise ValueError("qos must be a positive queue depth or 'sensor_data'")


def _name(value):
    if not isinstance(value, str) or not value.startswith("/") or value == "/":
        raise ValueError("use an absolute ROS name")
    return value


class Subscription:
    """Explicit, idempotent cancellation handle."""
    def __init__(self, cancel):
        self._cancel = cancel

    def close(self):
        if self._cancel is not None:
            self._cancel()
            self._cancel = None

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()


class RosClient:
    """ROS session, read-only unless allow_writes=True. Single application thread."""
    def __init__(self, *, node_name="lib_ros", namespace="/", domain_id=None,
                 backend=None, allow_writes=False, use_sim_time=False):
        if type(allow_writes) is not bool or type(use_sim_time) is not bool:
            raise TypeError("allow_writes and use_sim_time must be bool")
        if domain_id is not None and (type(domain_id) is not int or domain_id < 0):
            raise ValueError("domain_id must be a non-negative integer")
        if backend is None:
            from ._native import NativeBackend
            backend = NativeBackend(node_name, namespace, domain_id, use_sim_time)
        self._backend = backend
        self._closed = False
        self._spinning = False
        self._subscriptions = set()
        self._allow_writes = allow_writes
        self._received = self._published = self._timeouts = self._clock_regressions = 0
        self._last_clock = None

    def __enter__(self):
        self._ensure_open()
        return self

    def __exit__(self, *exc):
        self.close()

    def _ensure_open(self):
        if self._closed:
            raise RosError("client is closed")

    def topics(self):
        self._ensure_open()
        return self._backend.topics()

    def nodes(self):
        self._ensure_open()
        return self._backend.nodes()

    def subscribe(self, topic, callback, *, message_type=None, qos=10):
        self._ensure_open()
        _name(topic)
        if not callable(callback):
            raise TypeError("callback must be callable")
        def receive(message):
            self._received += 1
            callback(message)

        cancel = self._backend.subscribe(topic, receive, message_type, _qos(qos))

        def remove():
            cancel()
            self._subscriptions.discard(handle)

        handle = Subscription(remove)
        self._subscriptions.add(handle)
        return handle

    def spin_once(self, timeout=0.1):
        self._ensure_open()
        if self._spinning:
            raise RosError("nested spin or read from a callback is not supported")
        timeout = _timeout(timeout)
        self._spinning = True
        try:
            self._backend.spin_once(timeout)
        finally:
            self._spinning = False
            if self._closed:
                self._dispose()

    def spin(self):
        """Run callbacks until closed or interrupted."""
        while not self._closed:
            self.spin_once()

    def read(self, topic, *, timeout=5.0, message_type=None, qos=10):
        """Return the next original message; never return stale cached data."""
        self._ensure_open()
        if self._spinning:
            raise RosError("nested spin or read from a callback is not supported")
        timeout = _timeout(timeout)
        deadline = monotonic() + timeout
        result = []
        with self.subscribe(topic, result.append, message_type=message_type, qos=qos):
            while not result:
                remaining = deadline - monotonic()
                if remaining <= 0:
                    self._timeouts += 1
                    raise RosTimeout(f"no message on {topic} before timeout")
                self.spin_once(remaining)
        return result[0]

    def _require_write(self):
        self._ensure_open()
        if not self._allow_writes:
            raise RosWriteDisabled("outgoing operations require allow_writes=True")

    def _blocking(self, operation, *args):
        self._ensure_open()
        if self._spinning:
            raise RosError("blocking operations are not supported inside callbacks")
        self._spinning = True
        try:
            return operation(*args)
        except RosTimeout:
            self._timeouts += 1
            raise
        finally:
            self._spinning = False
            if self._closed:
                self._dispose()

    def publish(self, topic, message, *, qos=10):
        self._require_write()
        self._backend.publish(_name(topic), message, _qos(qos))
        self._published += 1

    def services(self):
        self._ensure_open()
        return self._backend.services()

    def call(self, service, request, *, service_type, timeout=5.0):
        self._require_write()
        return self._blocking(self._backend.call, _name(service), request,
                              service_type, _timeout(timeout))

    def send_goal(self, action, goal, *, action_type, timeout=30.0):
        self._require_write()
        return self._blocking(self._backend.send_goal, _name(action), goal,
                              action_type, _timeout(timeout))

    def transform(self, target, source, *, stamp_ns=None, timeout=5.0):
        if any(not isinstance(s, str) or not s or s.startswith("/")
               for s in (target, source)):
            raise ValueError("frame names must be nonempty and have no leading slash")
        if stamp_ns is not None and (type(stamp_ns) is not int or stamp_ns <= 0):
            raise ValueError("stamp_ns must be positive or None for latest")
        return self._blocking(self._backend.transform, target, source,
                              stamp_ns, _timeout(timeout))

    def clock(self):
        self._ensure_open()
        snapshot = self._backend.clock()
        if self._last_clock is not None and snapshot.ros_ns < self._last_clock:
            self._clock_regressions += 1
        self._last_clock = snapshot.ros_ns
        return snapshot

    def health(self):
        self._ensure_open()
        return ConnectionHealth(
            self._backend.name, self._backend.ready(), len(self.topics()),
            len(self.nodes()), len(self._subscriptions), self._received,
            self._published, self._timeouts, self._clock_regressions,
            self._backend.local_drops,
        )

    def close(self):
        if self._closed:
            return
        self._closed = True
        if not self._spinning:
            self._dispose()

    def _dispose(self):
        try:
            for handle in tuple(self._subscriptions):
                handle.close()
        finally:
            self._backend.close()
