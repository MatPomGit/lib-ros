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
