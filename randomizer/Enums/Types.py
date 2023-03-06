"""Location/item type enum."""
from enum import IntEnum, auto

from randomizer.Enums.Items import Items


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
    RainbowCoin = auto()
    FakeItem = auto()
    ToughBanana = auto()
    JunkItem = auto()
    Hint = auto()
    PreGivenMove = auto()


# If you make change to this selector, make sure to change the corresponding
# ItemRandoListSelected enum in randomizer.Enums.Settings.
ItemRandoSelector = [
    {"name": "Shops", "value": "shop", "tooltip": "Cranky, Funky, and Candy Moves are in the Pool and become possible locations for items.&#10;By selecting this, Cross-Kong purchases is forced on."},
    {"name": "Golden Bananas", "value": "banana", "tooltip": ""},
    {
        "name": "Tough Golden Bananas",
        "value": "toughbanana",
        "tooltip": "Tougher Golden Banana checks will be in the pool:&#10;- All 3 Minecart Rides&#10;- Both Beetle Races&#10;- Fungi and Caves Baboon Blasts&#10;- Rabbit, Owl, Vulture and Seal Races&#10;- Arcade Round 1&#10;- Rareware Golden Banana",
    },
    {"name": "Battle Crowns", "value": "crown", "tooltip": "Crowns are in the Pool and Battle Arenas become possible locations for items."},
    {"name": "Blueprints", "value": "blueprint", "tooltip": "Blueprints are in the Pool and Kasplats become possible locations for items."},
    {"name": "Keys", "value": "key", "tooltip": "Keys are in the Pool and Bosses become possible locations for items."},
    {"name": "Banana Medals", "value": "medal", "tooltip": "Medals are in the Pool and Collecting the required amount of Colored Bananas&#10;for a Banana Medal can reward items."},
    {"name": "Nintendo/Rareware Coins", "value": "coin", "tooltip": "Company Coins are in the Pool and DK Arcade/Jetpac become possible locations for items."},
    {"name": "Kongs", "value": "kong", "tooltip": "Kongs are in the Pool but are not replaced with an item currently."},
    {"name": "Fairies", "value": "fairy", "tooltip": "Fairies are in the Pool and Items in their place can be captured with a camera."},
    {"name": "Rainbow Coins", "value": "rainbowcoin", "tooltip": "Rainbow Coins are in the Pool and Dirt Patches become possible locations for items."},
    {"name": "Miscellaneous Items", "value": "beanpearl", "tooltip": "The 5 Pearls and the Bean are in the Pool&#10;Tiny's Anthill and Treasure Chest become possible locations for items."},
    {"name": "Ice Traps", "value": "fakeitem", "tooltip": "If you pick up a fake item it'll hurt and freeze you."},
    {"name": "Junk Items", "value": "junkitem", "tooltip": "Pointless items will fill no-item slots."},
]

KeySelector = [
    {"name": "Key 1", "value": Items.JungleJapesKey.name, "tooltip": ""},
    {"name": "Key 2", "value": Items.AngryAztecKey.name, "tooltip": ""},
    {"name": "Key 3", "value": Items.FranticFactoryKey.name, "tooltip": ""},
    {"name": "Key 4", "value": Items.GloomyGalleonKey.name, "tooltip": ""},
    {"name": "Key 5", "value": Items.FungiForestKey.name, "tooltip": ""},
    {"name": "Key 6", "value": Items.CrystalCavesKey.name, "tooltip": ""},
    {"name": "Key 7", "value": Items.CreepyCastleKey.name, "tooltip": ""},
    {"name": "Key 8", "value": Items.HideoutHelmKey.name, "tooltip": ""},
]
