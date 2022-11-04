"""Location/item type enum."""
from enum import IntEnum, auto


class Types(IntEnum):
    """Location/item type enum."""

    Banana = auto()
    BlueprintBanana = auto()
    Shop = auto()
    Blueprint = auto()
    Fairy = auto()
    Key = auto()
    Crown = auto()
    Coin = auto()
    TrainingBarrel = auto()
    Kong = auto()
    Medal = auto()
    Shockwave = auto()
    Constant = auto()
    NoItem = auto()
    Bean = auto()
    Pearl = auto()


ItemRandoSelector = [
    {"name": "Shops", "value": "shop", "tooltip": ""},
    {"name": "Golden Bananas", "value": "banana", "tooltip": ""},
    {"name": "Battle Crowns", "value": "crown", "tooltip": ""},
    {"name": "Blueprints", "value": "blueprint", "tooltip": ""},
    {"name": "Keys", "value": "key", "tooltip": ""},
    {"name": "Banana Medals", "value": "medal", "tooltip": ""},
    {"name": "Nintendo/Rareware Coins", "value": "coin", "tooltip": ""},
]
