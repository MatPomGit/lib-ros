"""Public data types and errors."""
from dataclasses import dataclass


class RosError(RuntimeError):
    """ROS operation failed."""


class RosUnavailable(RosError):
    """Required runtime, topic or message type is unavailable."""


class RosTimeout(RosError):
    """Operation exceeded its timeout."""


@dataclass(frozen=True)
class TopicDescriptor:
    name: str
    types: tuple[str, ...]


class RosWriteDisabled(RosError):
    """Client was not explicitly enabled for outgoing operations."""


@dataclass(frozen=True)
class ClockSnapshot:
    ros_ns: int
    wall_ns: int
    monotonic_ns: int
    simulated: bool


@dataclass(frozen=True)
class ActionResult:
    status: int
    result: object


@dataclass(frozen=True)
class ConnectionHealth:
    backend: str
    ready: bool
    topic_count: int
    node_count: int
    subscriptions: int
    messages_received: int
    messages_published: int
    timeouts: int
    clock_regressions: int
    # Native DDS loss is unknown; mock reports local queue overflow only.
    local_drops: int | None
