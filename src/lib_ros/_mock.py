"""Deterministic in-process backend; no ROS installation required."""
from collections import deque
from threading import Condition
from time import monotonic
from .models import TopicDescriptor, RosError, RosUnavailable


class MockBackend:
    """Inject test messages with emit(); never communicates with ROS."""
    def __init__(self, topics=None, nodes=()):
        self._topics = {}
        for name, types in (topics or {}).items():
            self._topics[name] = (types,) if isinstance(types, str) else tuple(types)
        self._nodes = list(nodes)
        self._subscriptions = {}
        self._condition = Condition()
        self._closed = False

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
                    queue.append(message)
            self._condition.notify_all()

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
