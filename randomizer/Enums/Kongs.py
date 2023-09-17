"""Kong enum."""
from enum import IntEnum, auto
from typing import List


class Kongs(IntEnum):
    """Kong enum."""

    donkey = 0
    diddy = auto()
    lanky = auto()
    tiny = auto()
    chunky = auto()
    any = auto()


def GetKongs() -> List[Kongs]:
    """Return list of kongs without any."""
    return [Kongs.donkey, Kongs.diddy, Kongs.lanky, Kongs.tiny, Kongs.chunky]
