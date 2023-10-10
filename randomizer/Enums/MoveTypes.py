"""Move type enum."""
from enum import IntEnum, auto


class MoveTypes(IntEnum):
    """Move type enum."""

    Moves = 0
    Slam = auto()
    Guns = auto()
    AmmoBelt = auto()
    Instruments = auto()
    Flag = auto()
