"""Enum for Song Groups."""
from enum import IntEnum, auto


class SongGroup(IntEnum):
    """Enum data for what group of song you are playing.

    Args:
            IntEnum (int): Enum of the song.
    """

    Calm = auto()
    Bouncy = auto()
    Loud = auto()
