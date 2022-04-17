"""Kong enum."""
from enum import IntEnum, auto


class Kongs(IntEnum):
    """Kong enum."""

    donkey = 0
    diddy = auto()
    lanky = auto()
    tiny = auto()
    chunky = auto()
    any = auto()


def GetKongs():
    """Return list of kongs without any."""
    return [Kongs.donkey, Kongs.diddy, Kongs.lanky, Kongs.tiny, Kongs.chunky]
