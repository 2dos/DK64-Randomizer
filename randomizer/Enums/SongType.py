"""Enum for Song Types."""
from enum import IntEnum, auto


class SongType(IntEnum):
    """Enum data for what type of song you are playing.

    Args:
            IntEnum (int): Enum of the song.
    """

    System = auto()
    BGM = auto()
    Fanfare = auto()
    Ambient = auto()
    Event = auto()
