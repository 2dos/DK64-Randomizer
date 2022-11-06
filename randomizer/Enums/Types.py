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


ItemRandoSelector = [
    {"name": "Shops", "value": "shop", "tooltip": ""},
    {"name": "Golden Bananas", "value": "banana", "tooltip": ""},
    {"name": "Battle Crowns", "value": "crown", "tooltip": ""},
    {"name": "Blueprints", "value": "blueprint", "tooltip": ""},
    {"name": "Keys", "value": "key", "tooltip": ""},
    {"name": "Banana Medals", "value": "medal", "tooltip": ""},
    {"name": "Nintendo/Rareware Coins", "value": "coin", "tooltip": ""},
]

KeySelector = [
    {"name": "Key 1", "value": "key1", "tooltip": ""},
    {"name": "Key 2", "value": "key2", "tooltip": ""},
    {"name": "Key 3", "value": "key3", "tooltip": ""},
    {"name": "Key 4", "value": "key4", "tooltip": ""},
    {"name": "Key 5", "value": "key5", "tooltip": ""},
    {"name": "Key 6", "value": "key6", "tooltip": ""},
    {"name": "Key 7", "value": "key7", "tooltip": ""},
    {"name": "Key 8", "value": "key8", "tooltip": ""},
]
