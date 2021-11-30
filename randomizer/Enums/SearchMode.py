"""Search mode enum."""
from enum import IntEnum, auto


class SearchMode(IntEnum):
    """Search mode enum."""

    GetReachable = auto()
    GeneratePlaythrough = auto()
    CheckBeatable = auto()
