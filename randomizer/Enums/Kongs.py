"""Kong enum."""

from __future__ import annotations

from enum import IntEnum, auto
from typing import TYPE_CHECKING, List


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
