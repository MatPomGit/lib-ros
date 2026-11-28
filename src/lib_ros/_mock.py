"""Deterministic in-process backend; no ROS installation required."""
from collections import deque
from threading import Condition
from time import monotonic, monotonic_ns, time_ns
from .models import TopicDescriptor, RosError, RosUnavailable, RosTimeout, ClockSnapshot, ActionResult


class MockBackend:
    """Inject test messages with emit(); never communicates with ROS."""
    name = 'mock'

    def __init__(self, topics=None, nodes=(), *, services=None, actions=None,
                 transforms=None, ros_clock=None):
        self._topics = {}
        for name, types in (topics or {}).items():
            self._topics[name] = (types,) if isinstance(types, str) else tuple(types)
        self._nodes = list(nodes)
        self._subscriptions = {}
        self._condition = Condition()
        self._closed = False
        self._services = dict(services or {})
        self._actions = dict(actions or {})
        self._transforms = dict(transforms or {})
        self._ros_clock = ros_clock
        self.local_drops = 0

    def topics(self):
        return [TopicDescriptor(name, tuple(sorted(types)))
                for name, types in sorted(self._topics.items())]

    def nodes(self):
        return sorted(self._nodes)

    def subscribe(self, topic, callback, message_type, qos):
        types = self._topics.get(topic, ())
        if message_type is None and len(types) != 1:
            raise RosUnavailable(f"topic {topic} not discovered or ambiguous; specify message_type")
        key = object()
        depth = 5 if qos == "sensor_data" else qos
        with self._condition:
            if self._closed:
                raise RosError("backend is closed")
            self._subscriptions[key] = (topic, callback, deque(maxlen=depth))

        def cancel():
            with self._condition:
                self._subscriptions.pop(key, None)
        return cancel

    def emit(self, topic, message):
        """Queue a message for current subscriptions; oldest dropped if full."""
        with self._condition:
            if self._closed:
                raise RosError("backend is closed")
            for name, _, queue in self._subscriptions.values():
                if name == topic:
                    if len(queue) == queue.maxlen:
                        self.local_drops += 1
                    queue.append(message)
            self._condition.notify_all()

    def ready(self):
        return not self._closed

    def publish(self, topic, message, qos):
        self.emit(topic, message)

    def services(self):
        return [TopicDescriptor(name, (entry[0],))
                for name, entry in sorted(self._services.items())]

    def call(self, name, request, service_type, timeout):
        if name not in self._services:
            raise RosTimeout(f"mock service unavailable: {name}")
        return self._services[name][1](request)

    def send_goal(self, name, goal, action_type, timeout):
        if name not in self._actions:
            raise RosTimeout(f"mock action unavailable: {name}")
        result = self._actions[name](goal)
        if not isinstance(result, ActionResult):
            raise TypeError("mock action must return ActionResult")
        return result

    def transform(self, target, source, stamp_ns, timeout):
        key = (target, source, stamp_ns)
        if key not in self._transforms:
            raise RosTimeout(f"mock transform unavailable: {target} <- {source}")
        return self._transforms[key]

    def clock(self):
        return ClockSnapshot(self._ros_clock() if self._ros_clock else time_ns(),
                             time_ns(), monotonic_ns(), self._ros_clock is not None)

    def spin_once(self, timeout):
        deadline = monotonic() + timeout
        with self._condition:
            while not self._closed:
                for _, callback, queue in self._subscriptions.values():
                    if queue:
                        message = queue.popleft()
                        break
                else:
                    remaining = deadline - monotonic()
                    if remaining <= 0:
                        return
                    self._condition.wait(remaining)
                    continue
                break
            else:
                return
        callback(message)

    def close(self):
        with self._condition:
            self._closed = True
            self._subscriptions.clear()
            self._condition.notify_all()
