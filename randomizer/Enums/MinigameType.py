"""Minigames enum."""
from enum import IntEnum, auto


class MinigameType(IntEnum):
    """Bonus minigame type enum."""

    NoGame = auto()
    BonusBarrel = auto()
    HelmBarrel = auto()
