"""Database of items, which will create some C code to reduce code maintainence issues when adding new item types to item rando."""

import json
from enum import IntEnum, auto
from BuildEnums import Kong, Song, Maps


class InGameItem:
    """Class to define an in-game item."""

    def __init__(self, *, name="", actor=0, model_two=0, scale=0.25, base=None, force_dance=True, boss_enabled=True, bounce=False, will_dance=True, is_null=False, is_custom=False):
        """Initialize with given parameters."""
        if base is not None and False:
            self.name = base.name
            self.actor = base.actor
            self.model_two = base.model_two
            self.scale = base.scale
            self.force_dance = base.force_dance
            self.boss_enabled = base.boss_enabled
            self.bounce = base.bounce
            self.will_dance = base.will_dance
            self.is_null = base.is_null
        self.name = name
        self.actor = actor
        self.model_two = model_two
        if is_custom:
            self.actor = self.actor + 345
        self.scale = scale
        self.force_dance = force_dance  # Force dance if in boss/crown
        self.boss_enabled = boss_enabled  # Can be a boss reward
        self.bounce = bounce  # Will bounce (excl sprites)
        self.will_dance = will_dance  # Produces dance animation upon grabbing it (if auto-dance skip off)
        self.is_null = is_null


class CollectableTypes(IntEnum):
    """Collectable Types Enum."""

    AmmoBox = -2
    Null = -1
    ColoredBanana = 0
    Coin = 1
    AmmoPellet = 2
    Orange = 4
    Crystal = 5
    Film = 6
    GoldenBanana = 8
    Medal = 10
    RaceCoin = 11
    Blueprint = 12


class Hitbox:
    """Class to store information regarding item hitboxes."""

    def __init__(self, y: int, radius: int, height: int):
        """Initialize with given parameters."""
        self.y = y
        self.radius = radius
        self.height = height


class ItemRandoDef:
    """Class to store information regarding item collision and spawning."""

    def __init__(self, object_id: int, item_type: CollectableTypes, kong: Kong = None, actor_equivalent: int = 0, hitbox: Hitbox = None, custom_actor: bool = False):
        """Initialize with given parameters."""
        self.object_id = object_id
        self.item_type = item_type
        self.kong = 0
        if kong is not None:
            self.kong = int(kong) + 2
        self.actor_equivalent = actor_equivalent
        self.hitbox = hitbox
        self.custom_actor = custom_actor
        if hitbox is None:
            self.hitbox = Hitbox(0, 0, 0)


class EnemyDropDef:
    """Class to store information regarding the drops an enemy makes."""

    def __init__(self, source_object: int, dropped_object: int, drop_music: Song, drop_count: int):
        """Initialize with given parameters."""
        self.source_object = source_object
        self.dropped_object = dropped_object
        self.drop_music = drop_music
        self.drop_count = drop_count


class CustomActors(IntEnum):
    """Custom Actors Enum."""

    NintendoCoin = 0
    RarewareCoin = auto()
    Null = auto()
    PotionDK = auto()
    PotionDiddy = auto()
    PotionLanky = auto()
    PotionTiny = auto()
    PotionChunky = auto()
    PotionAny = auto()
    KongDK = auto()
    KongDiddy = auto()
    KongLanky = auto()
    KongTiny = auto()
    KongChunky = auto()
    KongDisco = auto()
    KongKrusha = auto()
    Bean = auto()
    Pearl = auto()
    Fairy = auto()
    IceTrapBubble = auto()
    IceTrapReverse = auto()
    IceTrapSlow = auto()
    Medal = auto()
    JetpacItemOverlay = auto()
    CrankyItem = auto()
    FunkyItem = auto()
    CandyItem = auto()
    SnideItem = auto()
    ZingerFlamethrower = auto()
    Scarab = auto()
    HintItemDK = auto()
    KopDummy = auto()
    HintItemDiddy = auto()
    HintItemLanky = auto()
    HintItemTiny = auto()
    HintItemChunky = auto()


POTIONS = (
    CustomActors.PotionDK,
    CustomActors.PotionDiddy,
    CustomActors.PotionLanky,
    CustomActors.PotionTiny,
    CustomActors.PotionChunky,
    CustomActors.PotionAny,
)
KONGS = (
    CustomActors.KongDK,
    CustomActors.KongDiddy,
    CustomActors.KongLanky,
    CustomActors.KongTiny,
    CustomActors.KongChunky,
)
SHOPKEEPERS = (
    CustomActors.CrankyItem,
    CustomActors.FunkyItem,
    CustomActors.CandyItem,
    CustomActors.SnideItem,
)
TRAPS = (
    CustomActors.IceTrapBubble,
    CustomActors.IceTrapReverse,
    CustomActors.IceTrapSlow,
)


def getActorDefaultString(input) -> str:
    """Get the C attribute string for an actor definition."""
    dict_str = []
    if not isinstance(input, dict):
        return str(input)
    for k in input:
        val = input[k]
        if isinstance(val, list):
            val = "{" + ", ".join([str(x) for x in val]) + "}"
        dict_str.append(f".{k} = {val}")
    complete_internals = ", ".join(dict_str)
    return "{" + complete_internals + "}"


def initActor(actor_data: dict, actor_type: int, func: str, master_type: int, health: int, damage_given: int, init_interactions: int, base_actor: int) -> dict:
    """Initialize actor."""
    actor_data["actor_functions"][actor_type] = func
    actor_data["actor_master_types"][actor_type] = master_type
    actor_data["actor_health_damage"][actor_type] = {"init_health": health, "damage_applied": damage_given}
    actor_data["actor_interactions"][actor_type] = init_interactions
    actor_data["actor_extra_data_sizes"][actor_type] = actor_data["actor_extra_data_sizes"][base_actor]
    actor_data["actor_collisions"][actor_type] = actor_data["actor_collisions"][base_actor].copy()
    return actor_data


base_potion = InGameItem(scale=0.25, bounce=True)
base_kong = InGameItem(scale=0.25, bounce=True)
base_bp = InGameItem(scale=2, will_dance=False)
base_coin = InGameItem(scale=0.4, will_dance=False)

db = [
    InGameItem(name="Golden Banana", actor=45, model_two=0x74, scale=0.25, bounce=True),
    InGameItem(name="DK Blueprint", actor=78, model_two=0xDE, base=base_bp, scale=2),
    InGameItem(name="Diddy Blueprint", actor=75, model_two=0xE0, base=base_bp, scale=2),
    InGameItem(name="Lanky Blueprint", actor=77, model_two=0xE1, base=base_bp, scale=2),
    InGameItem(name="Tiny Blueprint", actor=79, model_two=0xDD, base=base_bp, scale=2),
    InGameItem(name="Chunky Blueprint", actor=76, model_two=0xDF, base=base_bp, scale=2),
    InGameItem(name="Nintendo Coin", actor=CustomActors.NintendoCoin, is_custom=True, model_two=0x48, base=base_coin, scale=0.4, bounce=True),
    InGameItem(name="Rareware Coin", actor=CustomActors.RarewareCoin, is_custom=True, model_two=0x28F, base=base_coin, scale=0.4, bounce=True),
    InGameItem(name="Boss Key", actor=72, model_two=0x13C, scale=0.17, bounce=True),
    InGameItem(name="Battle Crown", actor=86, model_two=0x18D, scale=0.25, bounce=True),
    InGameItem(name="Banana Medal", actor=CustomActors.Medal, is_custom=True, model_two=0x90, scale=0.22, bounce=True),
    InGameItem(name="DK Potion", actor=CustomActors.PotionDK, is_custom=True, model_two=0x5B, base=base_potion, bounce=True),
    InGameItem(name="Diddy Potion", actor=CustomActors.PotionDiddy, is_custom=True, model_two=0x1F2, base=base_potion, bounce=True),
    InGameItem(name="Lanky Potion", actor=CustomActors.PotionLanky, is_custom=True, model_two=0x59, base=base_potion, bounce=True),
    InGameItem(name="Tiny Potion", actor=CustomActors.PotionTiny, is_custom=True, model_two=0x1F3, base=base_potion, bounce=True),
    InGameItem(name="Chunky Potion", actor=CustomActors.PotionChunky, is_custom=True, model_two=0x1F5, base=base_potion, bounce=True),
    InGameItem(name="Any Potion", actor=CustomActors.PotionAny, is_custom=True, model_two=0x1F6, base=base_potion, bounce=True),
    InGameItem(name="No Item", actor=CustomActors.Null, is_custom=True, model_two=0x0, scale=0.25, force_dance=False, boss_enabled=False, is_null=True),
    InGameItem(name="DK Item", actor=CustomActors.KongDK, is_custom=True, model_two=0x257, base=base_kong, bounce=True),
    InGameItem(name="Diddy Item", actor=CustomActors.KongDiddy, is_custom=True, model_two=0x258, base=base_kong, bounce=True),
    InGameItem(name="Lanky Item", actor=CustomActors.KongLanky, is_custom=True, model_two=0x259, base=base_kong, bounce=True),
    InGameItem(name="Tiny Item", actor=CustomActors.KongTiny, is_custom=True, model_two=0x25A, base=base_kong, bounce=True),
    InGameItem(name="Chunky Item", actor=CustomActors.KongChunky, is_custom=True, model_two=0x25B, base=base_kong, bounce=True),
    InGameItem(name="Bean", actor=CustomActors.Bean, is_custom=True, model_two=0x198, scale=0.25, will_dance=False, bounce=True),
    InGameItem(name="Pearl", actor=CustomActors.Pearl, is_custom=True, model_two=0x1B4, scale=0.25, will_dance=False, bounce=True),
    InGameItem(name="Fairy", actor=CustomActors.Fairy, is_custom=True, model_two=0x25C, bounce=True, scale=0.25),
    InGameItem(name="Rainbow Coin", actor=140, model_two=0xB7, scale=0.25),
    InGameItem(name="Fake Item (Bubble)", actor=CustomActors.IceTrapBubble, is_custom=True, model_two=0x25D, bounce=True, scale=0.25),
    InGameItem(name="Fake Item (Reverse)", actor=CustomActors.IceTrapReverse, is_custom=True, model_two=0x264, bounce=True, scale=0.25),
    InGameItem(name="Fake Item (Slow)", actor=CustomActors.IceTrapSlow, is_custom=True, model_two=0x265, bounce=True, scale=0.25),
    InGameItem(name="Junk Item (Orange)", actor=0x34, model_two=0x56, will_dance=False, force_dance=False, scale=1),
    InGameItem(name="Junk Item (Melon)", actor=0x2F, model_two=0x25E, will_dance=False, force_dance=False, scale=0.25),
    InGameItem(name="Junk Item (Crystal)", actor=0x79, model_two=0x8E, will_dance=False, force_dance=False, scale=1),
    InGameItem(name="Junk Item (Ammo)", actor=0x33, model_two=0x8F, will_dance=False, force_dance=False, scale=1),
    InGameItem(name="Cranky Item", actor=CustomActors.CrankyItem, is_custom=True, model_two=0x25F, base=base_kong, bounce=True),
    InGameItem(name="Funky Item", actor=CustomActors.FunkyItem, is_custom=True, model_two=0x260, base=base_kong, bounce=True),
    InGameItem(name="Candy Item", actor=CustomActors.CandyItem, is_custom=True, model_two=0x261, base=base_kong, bounce=True),
    InGameItem(name="Snide Item", actor=CustomActors.SnideItem, is_custom=True, model_two=0x262, base=base_kong, bounce=True),
    InGameItem(name="Hint Item (DK)", actor=CustomActors.HintItemDK, is_custom=True, model_two=638, base=base_kong, bounce=True),
    InGameItem(name="Hint Item (Diddy)", actor=CustomActors.HintItemDiddy, is_custom=True, model_two=649, base=base_kong, bounce=True),
    InGameItem(name="Hint Item (Lanky)", actor=CustomActors.HintItemLanky, is_custom=True, model_two=650, base=base_kong, bounce=True),
    InGameItem(name="Hint Item (Tiny)", actor=CustomActors.HintItemTiny, is_custom=True, model_two=651, base=base_kong, bounce=True),
    InGameItem(name="Hint Item (Chunky)", actor=CustomActors.HintItemChunky, is_custom=True, model_two=652, base=base_kong, bounce=True),
]

db2 = [
    # Colored Bananas
    ItemRandoDef(0x000D, CollectableTypes.ColoredBanana, Kong.DK),
    ItemRandoDef(0x000A, CollectableTypes.ColoredBanana, Kong.Diddy),
    ItemRandoDef(0x001F, CollectableTypes.ColoredBanana, Kong.Chunky),
    ItemRandoDef(0x001E, CollectableTypes.ColoredBanana, Kong.Lanky),
    ItemRandoDef(0x0016, CollectableTypes.ColoredBanana, Kong.Tiny),
    # Coins
    ItemRandoDef(0x0024, CollectableTypes.Coin, Kong.Diddy),
    ItemRandoDef(0x0023, CollectableTypes.Coin, Kong.Lanky, 0x35),
    ItemRandoDef(0x0027, CollectableTypes.Coin, Kong.Chunky),
    ItemRandoDef(0x001C, CollectableTypes.Coin, Kong.Tiny),
    ItemRandoDef(0x001D, CollectableTypes.Coin, Kong.DK),
    # Bunch
    ItemRandoDef(0x002B, CollectableTypes.ColoredBanana, Kong.DK),
    ItemRandoDef(0x0208, CollectableTypes.ColoredBanana, Kong.Diddy),
    ItemRandoDef(0x0206, CollectableTypes.ColoredBanana, Kong.Chunky, 0x6E),
    ItemRandoDef(0x0205, CollectableTypes.ColoredBanana, Kong.Lanky),
    ItemRandoDef(0x0207, CollectableTypes.ColoredBanana, Kong.Tiny),
    # Pellets
    ItemRandoDef(0x0091, CollectableTypes.AmmoPellet),  # Peanut
    ItemRandoDef(0x015D, CollectableTypes.AmmoPellet),  # Feather
    ItemRandoDef(0x015E, CollectableTypes.AmmoPellet),  # Grape
    ItemRandoDef(0x015F, CollectableTypes.AmmoPellet),  # Pineapple
    ItemRandoDef(0x0160, CollectableTypes.AmmoPellet),  # Coconut
    # Blueprint
    ItemRandoDef(0x00DE, CollectableTypes.Blueprint, Kong.DK, 0x4E, Hitbox(8, 4, 13)),
    ItemRandoDef(0x00E0, CollectableTypes.Blueprint, Kong.Diddy, 0x4B, Hitbox(8, 4, 13)),
    ItemRandoDef(0x00E1, CollectableTypes.Blueprint, Kong.Lanky, 0x4D, Hitbox(8, 4, 13)),
    ItemRandoDef(0x00DD, CollectableTypes.Blueprint, Kong.Tiny, 0x4F, Hitbox(8, 4, 13)),
    ItemRandoDef(0x00DF, CollectableTypes.Blueprint, Kong.Chunky, 0x4C, Hitbox(8, 4, 13)),
    # Multiplayer
    ItemRandoDef(0x01CF, CollectableTypes.Null, None, 0x78),  # Yellow CB Powerup
    ItemRandoDef(0x01D0, CollectableTypes.Null, None, 0x77),  # Blue CB Powerup
    ItemRandoDef(0x01D1, CollectableTypes.Null, None, 0x76),  # Coin Powerup
    ItemRandoDef(0x01D2, CollectableTypes.Coin, None, 0x7A),  # Coin Multiplayer
    # Potions
    ItemRandoDef(0x005B, CollectableTypes.Null, None, CustomActors.PotionDK, Hitbox(8, 4, 13), True),  # Potion DK
    ItemRandoDef(0x01F2, CollectableTypes.Null, None, CustomActors.PotionDiddy, Hitbox(8, 4, 13), True),  # Potion Diddy
    ItemRandoDef(0x0059, CollectableTypes.Null, None, CustomActors.PotionLanky, Hitbox(8, 4, 13), True),  # Potion Lanky
    ItemRandoDef(0x01F3, CollectableTypes.Null, None, CustomActors.PotionTiny, Hitbox(8, 4, 13), True),  # Potion Tiny
    ItemRandoDef(0x01F5, CollectableTypes.Null, None, CustomActors.PotionChunky, Hitbox(8, 4, 13), True),  # Potion Chunky
    ItemRandoDef(0x01F6, CollectableTypes.Null, None, CustomActors.PotionAny, Hitbox(8, 4, 13), True),  # Potion Any
    # Kongs
    ItemRandoDef(0x0257, CollectableTypes.Null, None, CustomActors.KongDK, Hitbox(8, 4, 13), True),  # DK
    ItemRandoDef(0x0258, CollectableTypes.Null, None, CustomActors.KongDiddy, Hitbox(8, 4, 13), True),  # Diddy
    ItemRandoDef(0x0259, CollectableTypes.Null, None, CustomActors.KongLanky, Hitbox(8, 4, 13), True),  # Lanky
    ItemRandoDef(0x025A, CollectableTypes.Null, None, CustomActors.KongTiny, Hitbox(8, 4, 13), True),  # Tiny
    ItemRandoDef(0x025B, CollectableTypes.Null, None, CustomActors.KongChunky, Hitbox(8, 4, 13), True),  # Chunky
    # Misc
    ItemRandoDef(0x00B7, CollectableTypes.Coin, None, 0x8C, Hitbox(8, 4, 13)),  # Rainbow Coin
    # Others
    ItemRandoDef(0x0074, CollectableTypes.GoldenBanana, None, 0x2D, Hitbox(8, 4, 13)),  # Golden Banana
    ItemRandoDef(0x0056, CollectableTypes.Orange, None, 0x34),  # Orange
    ItemRandoDef(0x008F, CollectableTypes.AmmoBox, None, 0x33),  # Ammo Crate
    ItemRandoDef(0x0011, CollectableTypes.AmmoBox),  # Homing Ammo Crate
    ItemRandoDef(0x008E, CollectableTypes.Crystal, None, 0x79),  # Crystal
    ItemRandoDef(0x0057, CollectableTypes.Null, None, 0x2F),  # Watermelon
    ItemRandoDef(0x025E, CollectableTypes.Null, None, 0, Hitbox(8, 4, 13)),  # Watermelon - Duplicate
    ItemRandoDef(0x0098, CollectableTypes.Film),  # Film
    ItemRandoDef(0x0090, CollectableTypes.Medal, None, CustomActors.Medal, Hitbox(8, 4, 13), True),  # Medal
    ItemRandoDef(0x00EC, CollectableTypes.RaceCoin, None, 0x36),  # Race Coin
    ItemRandoDef(0x013C, CollectableTypes.Null, None, 0x48, Hitbox(8, 4, 13)),  # Boss Key
    ItemRandoDef(0x018D, CollectableTypes.Null, None, 0x56, Hitbox(8, 4, 13)),  # Battle Crown
    ItemRandoDef(0x0288, CollectableTypes.GoldenBanana, None, 0x2D, Hitbox(8, 4, 13)),  # Rareware GB
    ItemRandoDef(0x0048, CollectableTypes.Null, None, CustomActors.NintendoCoin, Hitbox(8, 4, 13), True),  # Nintendo Coin
    ItemRandoDef(0x028F, CollectableTypes.Null, None, CustomActors.RarewareCoin, Hitbox(8, 4, 13), True),  # Rareware Coin
    ItemRandoDef(0x0198, CollectableTypes.Null, None, CustomActors.Bean, Hitbox(8, 4, 13), True),  # Bean
    ItemRandoDef(0x01B4, CollectableTypes.Null, None, CustomActors.Pearl, Hitbox(8, 4, 13), True),  # Pearl
    ItemRandoDef(0x025C, CollectableTypes.Null, None, CustomActors.Fairy, Hitbox(8, 4, 13), True),  # Fairy
    ItemRandoDef(0x025D, CollectableTypes.Null, None, CustomActors.IceTrapBubble, Hitbox(8, 4, 13), True),  # Fake Item
    ItemRandoDef(0x0264, CollectableTypes.Null, None, CustomActors.IceTrapReverse, Hitbox(8, 4, 13), True),  # Fake Item
    ItemRandoDef(0x0265, CollectableTypes.Null, None, CustomActors.IceTrapSlow, Hitbox(8, 4, 13), True),  # Fake Item
    ItemRandoDef(0x025F, CollectableTypes.Null, None, CustomActors.CrankyItem, Hitbox(8, 4, 13), True),  # Cranky
    ItemRandoDef(0x0260, CollectableTypes.Null, None, CustomActors.FunkyItem, Hitbox(8, 4, 13), True),  # Funky
    ItemRandoDef(0x0261, CollectableTypes.Null, None, CustomActors.CandyItem, Hitbox(8, 4, 13), True),  # Candy
    ItemRandoDef(0x0262, CollectableTypes.Null, None, CustomActors.SnideItem, Hitbox(8, 4, 13), True),  # Snide
    ItemRandoDef(0x027E, CollectableTypes.Null, None, CustomActors.HintItemDK, Hitbox(8, 4, 13), True),  # Hint
    ItemRandoDef(0x0289, CollectableTypes.Null, None, CustomActors.HintItemDiddy, Hitbox(8, 4, 13), True),  # Hint
    ItemRandoDef(0x028A, CollectableTypes.Null, None, CustomActors.HintItemLanky, Hitbox(8, 4, 13), True),  # Hint
    ItemRandoDef(0x028B, CollectableTypes.Null, None, CustomActors.HintItemTiny, Hitbox(8, 4, 13), True),  # Hint
    ItemRandoDef(0x028C, CollectableTypes.Null, None, CustomActors.HintItemChunky, Hitbox(8, 4, 13), True),  # Hint
]

item_drops = [
    EnemyDropDef(0xB2, 0x2F, Song.MelonSliceDrop, 1),  # Beaver (Blue)
    EnemyDropDef(0xD4, 0x2F, Song.MelonSliceDrop, 2),  # Beaver (Gold)
    EnemyDropDef(0xCD, 0x2F, Song.MelonSliceDrop, 1),  # Green Klaptrap
    EnemyDropDef(0xD0, 0x34, Song.Silence, 3),  # Purple Klaptrap
    EnemyDropDef(0xD1, 0x33, Song.Silence, 1),  # Red Klaptrap
    EnemyDropDef(0x03, 0x35, Song.Silence, 3),  # Diddy
    EnemyDropDef(0xF1, 0x4E, Song.BlueprintDrop, 1),  # Kasplat (DK)
    EnemyDropDef(0xF2, 0x4B, Song.BlueprintDrop, 1),  # Kasplat (Diddy)
    EnemyDropDef(0xF3, 0x4D, Song.BlueprintDrop, 1),  # Kasplat (Lanky)
    EnemyDropDef(0xF4, 0x4F, Song.BlueprintDrop, 1),  # Kasplat (Tiny)
    EnemyDropDef(0xF5, 0x4C, Song.BlueprintDrop, 1),  # Kasplat (Chunky)
    EnemyDropDef(0xBB, 0x34, Song.Silence, 3),  # Klump
    EnemyDropDef(0xEE, 0x2F, Song.MelonSliceDrop, 1),  # Kremling
    EnemyDropDef(0xEB, 0x2F, Song.MelonSliceDrop, 2),  # Robo Kremling
    EnemyDropDef(0x123, 0x2F, Song.MelonSliceDrop, 2),  # Kosha
    EnemyDropDef(0xB7, 0x2F, Song.MelonSliceDrop, 1),  # Zinger
    EnemyDropDef(0xCE, 0x2F, Song.MelonSliceDrop, 1),  # Zinger
    EnemyDropDef(0x105, 0x2F, Song.MelonSliceDrop, 1),  # Robo-Zinger
    EnemyDropDef(0x11D, 0x2F, Song.MelonSliceDrop, 1),  # Bat
    EnemyDropDef(0x10F, 0x2F, Song.MelonSliceDrop, 1),  # Mr. Dice
    EnemyDropDef(0x10E, 0x2F, Song.MelonSliceDrop, 1),  # Sir Domino
    EnemyDropDef(0x10D, 0x2F, Song.MelonSliceDrop, 1),  # Mr. Dice
    EnemyDropDef(0xE0, 0x2F, Song.MelonSliceDrop, 1),  # Mushroom Man
    EnemyDropDef(0x106, 0x2F, Song.MelonSliceDrop, 1),  # Krossbones
    EnemyDropDef(0x121, 0x2F, Song.MelonSliceDrop, 1),  # Ghost
    EnemyDropDef(0xB6, 0x2F, Song.MelonSliceDrop, 1),  # Klobber
    EnemyDropDef(0xAF, 0x2F, Song.MelonSliceDrop, 1),  # Kaboom
    EnemyDropDef(0x103, 0x79, Song.Silence, 1),  # Guard
    EnemyDropDef(276, 0x34, Song.Silence, 2),  # Spiderling
    EnemyDropDef(273, 0x34, Song.Silence, 1),  # Fireball with Glasses
    EnemyDropDef(230, 0x2F, Song.MelonSliceDrop, 1),  # Ruler
    EnemyDropDef(340, 0x2F, Song.MelonSliceDrop, 1),  # Bug
    EnemyDropDef(345 + CustomActors.ZingerFlamethrower, 0x2F, Song.MelonSliceDrop, 2),  # Flamethrowing Zinger
    EnemyDropDef(345 + CustomActors.Scarab, 0x2F, Song.MelonSliceDrop, 1),  # Kiosk Bug Replica
]

dance_acceptable_items = [x for x in db if x.force_dance]
boss_enabled_items = [x for x in db if x.boss_enabled]
bounce_items = [x for x in db if x.bounce]
actor_drops = [x for x in db if x.actor is not None]
danceless_items = [x for x in db if not x.will_dance]
warning_text_data = [
    "This is a pre-generated file. Please don't directly modify this file as this will be overwritten upon next build.",
    "Visit build/item_dictionaries.py to modify this output.",
    "\nThanks,",
    "\tBallaam",
]
warning_text = "/*\n\t" + "\n\t".join(warning_text_data) + "\n*/\n"

with open("include/item_data.h", "w") as fh:
    fh.write(warning_text)
    fh.write(f"extern const short acceptable_items[{len(dance_acceptable_items)}];\n")
    fh.write(f"extern const item_conversion_info item_conversions[{len(boss_enabled_items)}];\n")
    fh.write(f"extern const unsigned short bounce_objects[{len(bounce_items)}];\n")
    fh.write(f"extern const unsigned short actor_drops[{len(actor_drops)}];\n")
    # fh.write(f"extern const unsigned short danceless_items[{len(danceless_items)}];\n")
    fh.write(f"extern const item_scale_info item_scales[{len(db)}];\n")
    fh.write(f"typedef enum new_custom_actors {{\n")
    for e in CustomActors:
        fh.write(f"\t/* 0x{'{:03X}'.format(e.value)} */ NEWACTOR_{e.name.upper()}, \n")
    fh.write("\t/* ----- */ NEWACTOR_TERMINATOR, \n")
    fh.write("} new_custom_actors;\n")
    fh.write(f"#define DROP_COUNT {len(item_drops) + 1}")

with open("src/lib_items.c", "w") as fh:
    fh.write('#include "../include/common.h"\n\n')
    fh.write(warning_text)
    fh.write("\nconst short acceptable_items[] = {" + ",".join([hex(x.model_two) for x in dance_acceptable_items]) + "};")
    fh.write("\nconst item_conversion_info item_conversions[] = {\n\t" + ",\n\t".join([f"{{.actor={x.actor}, .model_two={x.model_two}, .scale={x.scale:.2f}f}}" for x in boss_enabled_items]) + "\n};")
    fh.write("\nconst unsigned short bounce_objects[] = {" + ",".join([str(x.actor) for x in bounce_items]) + "};")
    fh.write("\nconst unsigned short actor_drops[] = {" + ",".join([str(x.actor) for x in actor_drops]) + "};")
    # fh.write("\nconst unsigned short danceless_items[] = {" + ",".join([str(x.actor) for x in danceless_items]) + "};")
    fh.write("\nconst item_scale_info item_scales[] = {\n\t" + ",\n\t".join([f"{{.type={x.model_two}, .scale={x.scale:.2f}f}}" for x in db]) + "\n};")
    fh.write(
        "\ncollision_info object_collisions[] = {\n\t"
        + ",\n\t".join(
            [
                f"{{.type={x.object_id}, .collectable_type={x.item_type}, .unk4=0.08f, .unk8=0.95f, .intended_actor={x.kong}, .actor_equivalent={f'{x.actor_equivalent} + CUSTOM_ACTORS_START' if x.custom_actor else x.actor_equivalent}, .hitbox_y_center={x.hitbox.y}, .hitbox_radius={x.hitbox.radius}, .hitbox_height={x.hitbox.height}}}"
                for x in db2
            ]
        )
        + "\n};"
    )
    fh.write(
        "\ndrop_item drops[] = {\n\t"
        + ",\n\t".join([f"{{.source_object={x.source_object}, .dropped_object={x.dropped_object}, .drop_music={x.drop_music}, .drop_count={x.drop_count}}}" for x in item_drops])
        + ",\n\t{.source_object=0, .dropped_object=0, .drop_music=0, .drop_count=0}, // Terminator\n};"
    )
    data_types = {
        "actor_defs": "actor_behaviour_def",
        "actor_master_types": "unsigned char",
        "actor_interactions": "short",
        "actor_health_damage": "health_damage_struct",
        "actor_collisions": "collision_data_struct",
        "actor_functions": "void*",
        "actor_extra_data_sizes": "short*",
        "new_flag_mapping": "GBDictItem",
    }
    actor_data = {}
    with open("actor_data.json", "r") as fg:
        actor_data = json.load(fg)
    actor_data["actor_defs"].extend(
        [
            {
                "actor_type": 345 + CustomActors.NintendoCoin,
                "model": 0x10B,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Nintendo Coin
            {
                "actor_type": 345 + CustomActors.RarewareCoin,
                "model": 0x10D,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Rareware Coin
            # Potions
            {
                "actor_type": 345 + CustomActors.PotionDK,
                "model": 0xEE,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # DK Potion
            {
                "actor_type": 345 + CustomActors.PotionDiddy,
                "model": 0xEF,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Diddy Potion
            {
                "actor_type": 345 + CustomActors.PotionLanky,
                "model": 0xF0,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Lanky Potion
            {
                "actor_type": 345 + CustomActors.PotionTiny,
                "model": 0xF1,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Tiny Potion
            {
                "actor_type": 345 + CustomActors.PotionChunky,
                "model": 0xF2,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Chunky Potion
            {
                "actor_type": 345 + CustomActors.PotionAny,
                "model": 0xF3,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Any Potion
            # Kongs
            {
                "actor_type": 345 + CustomActors.KongDK,
                "model": 0xFE,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # DK
            {
                "actor_type": 345 + CustomActors.KongDiddy,
                "model": 0xFF,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Diddy
            {
                "actor_type": 345 + CustomActors.KongLanky,
                "model": 0x100,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Lanky
            {
                "actor_type": 345 + CustomActors.KongTiny,
                "model": 0x101,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Tiny
            {
                "actor_type": 345 + CustomActors.KongChunky,
                "model": 0x102,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Chunky
            # Shop Owners
            {
                "actor_type": 345 + CustomActors.CrankyItem,
                "model": 0x10F,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Cranky
            {
                "actor_type": 345 + CustomActors.FunkyItem,
                "model": 0x110,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Funky
            {
                "actor_type": 345 + CustomActors.CandyItem,
                "model": 0x111,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Candy
            {
                "actor_type": 345 + CustomActors.SnideItem,
                "model": 0x112,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Snide
            # Misc
            {
                "actor_type": 345 + CustomActors.Bean,
                "model": 0x105,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Bean
            {
                "actor_type": 345 + CustomActors.Pearl,
                "model": 0x107,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Pearl
            {
                "actor_type": 345 + CustomActors.Fairy,
                "model": 0xFC,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Fairy
            {
                "actor_type": 345 + CustomActors.Null,
                "model": 0,
                "code": 0x80689F80,
                "unk10": 0x8068A10C,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Nothing
            {
                "actor_type": 345 + CustomActors.Medal,
                "model": 0x109,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Medal
            {
                "actor_type": 345 + CustomActors.IceTrapBubble,
                "model": 0xFD,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Fake Item
            {
                "actor_type": 345 + CustomActors.IceTrapReverse,
                "model": 0xFD,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Fake Item
            {
                "actor_type": 345 + CustomActors.IceTrapSlow,
                "model": 0xFD,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Fake Item
            {
                "actor_type": 345 + CustomActors.HintItemDK,
                "model": 0x11A,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Hint Item
            {
                "actor_type": 345 + CustomActors.HintItemDiddy,
                "model": 0x11C,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Hint Item
            {
                "actor_type": 345 + CustomActors.HintItemLanky,
                "model": 0x11E,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Hint Item
            {
                "actor_type": 345 + CustomActors.HintItemTiny,
                "model": 0x120,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Hint Item
            {
                "actor_type": 345 + CustomActors.HintItemChunky,
                "model": 0x122,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Hint Item
        ]
    )
    default_values = {
        "actor_master_types": 0,
        "actor_interactions": 0,
        "actor_health_damage": {
            "init_health": 0,
            "damage_applied": 0,
        },
        "actor_collisions": {
            "collision_info": 0,
            "unk_4": 0,
        },
        "actor_functions": 0,
        "actor_extra_data_sizes": 0,
    }
    for exp_prop in default_values:
        val = default_values[exp_prop]
        exp_lst = [val] * len(CustomActors)
        actor_data[exp_prop].extend(exp_lst)
    print(len(actor_data["actor_functions"]))
    actor_data["actor_functions"][70] = "&newCounterCode"
    actor_data["actor_functions"][184] = "&snideCodeHandler"
    actor_data["actor_functions"][189] = "&crankyCodeHandler"
    actor_data["actor_functions"][190] = "&funkyCodeHandler"
    actor_data["actor_functions"][191] = "&candyCodeHandler"
    actor_data["actor_functions"][324] = "&getNextMoveText"
    actor_data["actor_functions"][320] = "&getNextMoveText"
    actor_data["actor_functions"][107] = "&HelmBarrelCode"
    actor_data = initActor(actor_data, 345 + CustomActors.NintendoCoin, "&ninCoinCode", 2, 0, 1, 8, 45)
    actor_data = initActor(actor_data, 345 + CustomActors.RarewareCoin, "&rwCoinCode", 2, 0, 1, 8, 45)
    actor_data = initActor(actor_data, 345 + CustomActors.Null, "&NothingCode", 4, 0, 1, 8, 0)
    actor_data = initActor(actor_data, 345 + CustomActors.Medal, "&medalCode", 2, 0, 1, 8, 45)
    for potion in POTIONS:
        actor_data = initActor(actor_data, 345 + potion, "&PotionCode", 2, 0, 1, 8, 45)
    for kong in KONGS:
        actor_data = initActor(actor_data, 345 + kong, "&KongDropCode", 2, 0, 1, 8, 45)
    for shopkeeper in SHOPKEEPERS:
        actor_data = initActor(actor_data, 345 + shopkeeper, "&shopOwnerItemCode", 2, 0, 1, 8, 45)
    for trap in TRAPS:
        actor_data = initActor(actor_data, 345 + trap, "&FakeGBCode", 2, 0, 1, 8, 45)

    actor_data = initActor(actor_data, 345 + CustomActors.Bean, "&beanCode", 2, 0, 1, 8, 45)
    actor_data = initActor(actor_data, 345 + CustomActors.Pearl, "&pearlCode", 2, 0, 1, 8, 45)
    actor_data = initActor(actor_data, 345 + CustomActors.Fairy, "&fairyDuplicateCode", 2, 0, 1, 8, 45)
    actor_data = initActor(actor_data, 345 + CustomActors.HintItemDK, "&GoldenBananaCode", 2, 0, 1, 8, 45)
    actor_data = initActor(actor_data, 345 + CustomActors.HintItemDiddy, "&GoldenBananaCode", 2, 0, 1, 8, 45)
    actor_data = initActor(actor_data, 345 + CustomActors.HintItemLanky, "&GoldenBananaCode", 2, 0, 1, 8, 45)
    actor_data = initActor(actor_data, 345 + CustomActors.HintItemTiny, "&GoldenBananaCode", 2, 0, 1, 8, 45)
    actor_data = initActor(actor_data, 345 + CustomActors.HintItemChunky, "&GoldenBananaCode", 2, 0, 1, 8, 45)
    actor_data = initActor(actor_data, 345 + CustomActors.JetpacItemOverlay, "&getNextMoveText", 3, 0, 0, 0x10, 324)
    actor_data = initActor(actor_data, 345 + CustomActors.ZingerFlamethrower, "(void*)0x806B4958", 2, 1, 0, 2, 183)
    actor_data = initActor(actor_data, 345 + CustomActors.Scarab, "&kioskBugCode", 2, 1, 0, 2, 183)
    actor_data["actor_collisions"][345 + CustomActors.Scarab] = {
        "collision_info": 0x8074B240,
        "unk_4": 1,
    }
    actor_data = initActor(actor_data, 345 + CustomActors.KopDummy, "&dummyGuardCode", 2, 0, 1, 8, 45)
    # Flag Mapping
    for item in actor_data["new_flag_mapping"]:
        if item["map"] == Maps.Helm:
            if item["model2_id"] == 0x5E:
                item["flag_index"] = 0x24C
            elif item["model2_id"] == 0x61:
                item["flag_index"] = 0x249
    # Add new flag mappings
    pearl_lst = []
    for x in range(5):
        pearl_lst.append(
            {
                "map": Maps.GalleonTreasureChest,
                "model2_id": x,
                "flag_index": 0xBA + x,
                "intended_kong_actor": 0,
            }
        )
    actor_data["new_flag_mapping"].extend(pearl_lst)
    actor_data["new_flag_mapping"].extend(
        [
            {
                "map": Maps.FungiAntHill,
                "model2_id": 5,
                "flag_index": 0x300,
                "intended_kong_actor": 0,
            },
            {
                "map": Maps.Helm,
                "model2_id": 0x5A,
                "flag_index": 0x17C,
                "intended_kong_actor": 0,
            },
        ]
    )
    for sym in data_types:
        fh.write(f"\n{data_types[sym]} {sym}[] = {{\n\t" + ",\n\t".join([getActorDefaultString(x) for x in actor_data[sym]]) + "\n};")
