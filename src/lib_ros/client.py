"""Synchronous client; application controls when callbacks run."""
from math import isfinite
from time import monotonic
from .models import RosError, RosTimeout


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
    """Read-only ROS session. Use from one application thread."""
    def __init__(self, *, node_name="lib_ros", namespace="/", domain_id=None,
                 backend=None):
        if domain_id is not None and (type(domain_id) is not int or domain_id < 0):
            raise ValueError("domain_id must be a non-negative integer")
        if backend is None:
            from ._native import NativeBackend
            backend = NativeBackend(node_name, namespace, domain_id)
        self._backend = backend
        self._closed = False
        self._spinning = False
        self._subscriptions = set()

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
        if not isinstance(topic, str) or not topic.startswith("/") or topic == "/":
            raise ValueError("use an absolute ROS topic name")
        if not callable(callback):
            raise TypeError("callback must be callable")
        cancel = self._backend.subscribe(topic, callback, message_type, _qos(qos))

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
                    raise RosTimeout(f"no message on {topic} before timeout")
                self.spin_once(remaining)
        return result[0]

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
