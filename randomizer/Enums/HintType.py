"""Hint Type enum."""
from enum import IntEnum, auto


class HintType(IntEnum):
    """Hint type enum."""

    Joke = auto()
    KRoolOrder = auto()
    HelmOrder = auto()
    MoveLocation = auto()
    DirtPatch = auto()
    BLocker = auto()
    TroffNScoff = auto()
    KongLocation = auto()
    MedalsRequired = auto()
    Entrance = auto()
    RequiredKongHint = auto()
    RequiredKeyHint = auto()
    RequiredWinConditionHint = auto()
    RequiredHelmDoorHint = auto()
    FullShopWithItems = auto()
    WothLocation = auto()
    FoolishMove = auto()
    FoolishRegion = auto()
