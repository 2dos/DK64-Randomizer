"""Event enum."""
from enum import IntEnum, auto


class EnemySubtype(IntEnum):
    """Enemy Subtype enum."""

    GroundSimple = auto()
    GroundBeefy = auto()
    Air = auto()
    Water = auto()
