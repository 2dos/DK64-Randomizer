"""Database of items, which will create some C code to reduce code maintainence issues when adding new item types to item rando."""

import json
from enum import IntEnum, auto
from BuildEnums import Kong, Song, Maps, CustomActors


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


class EnemyDropDef:
    """Class to store information regarding the drops an enemy makes."""

    def __init__(self, source_object: int, dropped_object: int, drop_music: Song, drop_count: int):
        """Initialize with given parameters."""
        self.source_object = source_object
        self.dropped_object = dropped_object
        self.drop_music = drop_music
        self.drop_count = drop_count


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
GUARDS = (
    CustomActors.GuardDisableA,
    CustomActors.GuardDisableZ,
    CustomActors.GuardGetOut,
    CustomActors.GuardTag,
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


class Item:
    """Class to store information pertaining to an item."""

    def __init__(
        self,
        name: str = "",
        actor: int = 0,
        model_two: int = 0,
        scale: float = 0.25,
        force_dance: bool = True,
        boss_enabled: bool = True,
        bounce: bool = False,
        will_dance: bool = True,
        is_null: bool = False,
        item_db: bool = True,
        item_type: CollectableTypes = CollectableTypes.Null,
        kong: Kong = None,
        hitbox: Hitbox = None,
        has_collision: bool = False,
    ):
        """Initialize with given parameters."""
        self.name = name
        self.actor = actor
        self.model_two = model_two
        self.scale = scale
        self.force_dance = force_dance
        self.bounce = bounce
        self.boss_enabled = boss_enabled
        self.will_dance = will_dance
        self.is_null = is_null
        self.item_db = item_db
        self.item_type = item_type
        self.kong = 0
        if kong is not None:
            self.kong = kong + 2
        if hitbox is None:
            self.hitbox = Hitbox(8, 4, 13)
        else:
            self.hitbox = hitbox
        self.has_collision = has_collision


item_database = [
    Item(name="Boss Key", actor=72, model_two=0x13C, scale=0.17, bounce=True, has_collision=True),
    Item(name="Battle Crown", actor=86, model_two=0x18D, scale=0.25, bounce=True, has_collision=True),
    Item(name="Banana Medal", actor=CustomActors.Medal, model_two=0x90, scale=0.22, bounce=True, has_collision=True, item_type=CollectableTypes.Medal),
    Item(name="No Item", actor=CustomActors.Null, model_two=0x0, scale=0.25, force_dance=False, boss_enabled=False, is_null=True),
    Item(name="Bean", actor=CustomActors.Bean, model_two=0x198, scale=0.25, will_dance=False, bounce=True, has_collision=True),
    Item(name="Pearl", actor=CustomActors.Pearl, model_two=0x1B4, scale=0.25, will_dance=False, bounce=True, has_collision=True),
    Item(name="Fairy", actor=CustomActors.Fairy, model_two=0x25C, bounce=True, scale=0.25, has_collision=True),
    Item(name="Rainbow Coin", actor=140, model_two=0xB7, scale=0.25, has_collision=True, item_type=CollectableTypes.Coin),
    Item(name="Archipelago Item", actor=CustomActors.ArchipelagoItem, model_two=0x291, bounce=True, has_collision=True),
    Item(name="Special Archipelago Item", actor=CustomActors.SpecialArchipelagoItem, model_two=0x292, bounce=True, has_collision=True),
    Item(name="Fools Archipelago Item", actor=CustomActors.FoolsArchipelagoItem, model_two=0x293, bounce=True, has_collision=True),
    Item(name="Trap Archipelago Item", actor=CustomActors.TrapArchipelagoItem, model_two=0x294, bounce=True, has_collision=True),
    Item(name="Race Coin", actor=0x36, model_two=0xEC, item_db=False, item_type=CollectableTypes.RaceCoin, has_collision=True, hitbox=Hitbox(0, 0, 0)),
    Item(name="Film", actor=0, model_two=0x98, item_db=False, item_type=CollectableTypes.Film, has_collision=True, hitbox=Hitbox(0, 0, 0)),
    # GBs
    Item(name="Golden Banana", actor=0x2D, model_two=0x74, scale=0.25, bounce=True, has_collision=True, item_type=CollectableTypes.GoldenBanana),
    Item(name="Rareware Banana", actor=0x2D, model_two=0x288, has_collision=True, item_type=CollectableTypes.GoldenBanana, item_db=False),
    # Blueprints
    Item(name="DK Blueprint", actor=78, model_two=0xDE, scale=2, has_collision=True, item_type=CollectableTypes.Blueprint, kong=Kong.DK),
    Item(name="Diddy Blueprint", actor=75, model_two=0xE0, scale=2, has_collision=True, item_type=CollectableTypes.Blueprint, kong=Kong.Diddy),
    Item(name="Lanky Blueprint", actor=77, model_two=0xE1, scale=2, has_collision=True, item_type=CollectableTypes.Blueprint, kong=Kong.Lanky),
    Item(name="Tiny Blueprint", actor=79, model_two=0xDD, scale=2, has_collision=True, item_type=CollectableTypes.Blueprint, kong=Kong.Tiny),
    Item(name="Chunky Blueprint", actor=76, model_two=0xDF, scale=2, has_collision=True, item_type=CollectableTypes.Blueprint, kong=Kong.Chunky),
    # Junk
    Item(name="Junk Item (Orange)", actor=0x34, model_two=0x56, will_dance=False, force_dance=False, scale=1, has_collision=True, item_type=CollectableTypes.Orange, hitbox=Hitbox(0, 0, 0)),
    Item(name="Junk Item (Melon)", actor=0x2F, model_two=0x25E, will_dance=False, force_dance=False, scale=0.25),
    Item(name="Junk Item (Crystal)", actor=0x79, model_two=0x8E, will_dance=False, force_dance=False, scale=1, has_collision=True, item_type=CollectableTypes.Crystal, hitbox=Hitbox(0, 0, 0)),
    Item(name="Junk Item (Ammo)", actor=0x33, model_two=0x8F, will_dance=False, force_dance=False, scale=1, has_collision=True, item_type=CollectableTypes.AmmoBox, hitbox=Hitbox(0, 0, 0)),
    Item(name="Homing Ammo", actor=0, model_two=0x11, item_db=False, has_collision=True, item_type=CollectableTypes.AmmoBox, hitbox=Hitbox(0, 0, 0)),
    Item(name="Melon (Collision 1)", actor=0x2F, model_two=0x57, item_db=False, has_collision=True, hitbox=Hitbox(0, 0, 0)),
    Item(name="Melon (Collision 2)", actor=0, model_two=0x25E, item_db=False, has_collision=True),
    # Company Coin
    Item(name="Nintendo Coin", actor=CustomActors.NintendoCoin, model_two=0x48, scale=0.4, bounce=True, has_collision=True),
    Item(name="Rareware Coin", actor=CustomActors.RarewareCoin, model_two=0x28F, scale=0.4, bounce=True, has_collision=True),
    # Potion
    Item(name="DK Potion", actor=CustomActors.PotionDK, model_two=0x5B, bounce=True, has_collision=True),
    Item(name="Diddy Potion", actor=CustomActors.PotionDiddy, model_two=0x1F2, bounce=True, has_collision=True),
    Item(name="Lanky Potion", actor=CustomActors.PotionLanky, model_two=0x59, bounce=True, has_collision=True),
    Item(name="Tiny Potion", actor=CustomActors.PotionTiny, model_two=0x1F3, bounce=True, has_collision=True),
    Item(name="Chunky Potion", actor=CustomActors.PotionChunky, model_two=0x1F5, bounce=True, has_collision=True),
    Item(name="Any Potion", actor=CustomActors.PotionAny, model_two=0x1F6, bounce=True, has_collision=True),
    # Kongs
    Item(name="DK Item", actor=CustomActors.KongDK, model_two=0x257, bounce=True, has_collision=True),
    Item(name="Diddy Item", actor=CustomActors.KongDiddy, model_two=0x258, bounce=True, has_collision=True),
    Item(name="Lanky Item", actor=CustomActors.KongLanky, model_two=0x259, bounce=True, has_collision=True),
    Item(name="Tiny Item", actor=CustomActors.KongTiny, model_two=0x25A, bounce=True, has_collision=True),
    Item(name="Chunky Item", actor=CustomActors.KongChunky, model_two=0x25B, bounce=True, has_collision=True),
    # Shopkeepers
    Item(name="Cranky Item", actor=CustomActors.CrankyItem, model_two=0x25F, bounce=True, has_collision=True),
    Item(name="Funky Item", actor=CustomActors.FunkyItem, model_two=0x260, bounce=True, has_collision=True),
    Item(name="Candy Item", actor=CustomActors.CandyItem, model_two=0x261, bounce=True, has_collision=True),
    Item(name="Snide Item", actor=CustomActors.SnideItem, model_two=0x262, bounce=True, has_collision=True),
    # Ice Traps
    Item(name="Fake Item (GB)", actor=CustomActors.IceTrapGB, model_two=0x25D, bounce=True, scale=0.25, has_collision=True),
    Item(name="Fake Item (Bean)", actor=CustomActors.IceTrapBean, model_two=0x264, bounce=True, scale=0.25, has_collision=True),
    Item(name="Fake Item (Key)", actor=CustomActors.IceTrapKey, model_two=0x265, bounce=True, scale=0.25, has_collision=True),
    Item(name="Fake Item (Fairy)", actor=CustomActors.IceTrapFairy, model_two=0x299, bounce=True, scale=0.25, has_collision=True),
    # Singles
    Item(name="DK Single", actor=0, model_two=0xD, item_db=False, has_collision=True, hitbox=Hitbox(0, 0, 0), item_type=CollectableTypes.ColoredBanana, kong=Kong.DK),
    Item(name="Diddy Single", actor=0, model_two=0xA, item_db=False, has_collision=True, hitbox=Hitbox(0, 0, 0), item_type=CollectableTypes.ColoredBanana, kong=Kong.Diddy),
    Item(name="Lanky Single", actor=0, model_two=0x1E, item_db=False, has_collision=True, hitbox=Hitbox(0, 0, 0), item_type=CollectableTypes.ColoredBanana, kong=Kong.Lanky),
    Item(name="Tiny Single", actor=0, model_two=0x16, item_db=False, has_collision=True, hitbox=Hitbox(0, 0, 0), item_type=CollectableTypes.ColoredBanana, kong=Kong.Tiny),
    Item(name="Chunky Single", actor=0, model_two=0x1F, item_db=False, has_collision=True, hitbox=Hitbox(0, 0, 0), item_type=CollectableTypes.ColoredBanana, kong=Kong.Chunky),
    # Coins
    Item(name="DK Coin", actor=0, model_two=0x1D, item_db=False, has_collision=True, hitbox=Hitbox(0, 0, 0), item_type=CollectableTypes.Coin, kong=Kong.DK),
    Item(name="Diddy Coin", actor=0, model_two=0x24, item_db=False, has_collision=True, hitbox=Hitbox(0, 0, 0), item_type=CollectableTypes.Coin, kong=Kong.Diddy),
    Item(name="Lanky Coin", actor=0x35, model_two=0x23, item_db=False, has_collision=True, hitbox=Hitbox(0, 0, 0), item_type=CollectableTypes.Coin, kong=Kong.Lanky),
    Item(name="Tiny Coin", actor=0, model_two=0x1C, item_db=False, has_collision=True, hitbox=Hitbox(0, 0, 0), item_type=CollectableTypes.Coin, kong=Kong.Tiny),
    Item(name="Chunky Coin", actor=0, model_two=0x27, item_db=False, has_collision=True, hitbox=Hitbox(0, 0, 0), item_type=CollectableTypes.Coin, kong=Kong.Chunky),
    # Bunch
    Item(name="DK Bunch", actor=0, model_two=0x2B, item_db=False, has_collision=True, hitbox=Hitbox(0, 0, 0), item_type=CollectableTypes.ColoredBanana, kong=Kong.DK),
    Item(name="Diddy Bunch", actor=0, model_two=0x208, item_db=False, has_collision=True, hitbox=Hitbox(0, 0, 0), item_type=CollectableTypes.ColoredBanana, kong=Kong.Diddy),
    Item(name="Lanky Bunch", actor=0, model_two=0x205, item_db=False, has_collision=True, hitbox=Hitbox(0, 0, 0), item_type=CollectableTypes.ColoredBanana, kong=Kong.Lanky),
    Item(name="Tiny Bunch", actor=0, model_two=0x207, item_db=False, has_collision=True, hitbox=Hitbox(0, 0, 0), item_type=CollectableTypes.ColoredBanana, kong=Kong.Tiny),
    Item(name="Chunky Bunch", actor=0x6E, model_two=0x206, item_db=False, has_collision=True, hitbox=Hitbox(0, 0, 0), item_type=CollectableTypes.ColoredBanana, kong=Kong.Chunky),
    # Pellets
    Item(name="Coconut", actor=0, model_two=0x160, item_db=False, has_collision=True, hitbox=Hitbox(0, 0, 0), item_type=CollectableTypes.AmmoPellet),
    Item(name="Peanut", actor=0, model_two=0x91, item_db=False, has_collision=True, hitbox=Hitbox(0, 0, 0), item_type=CollectableTypes.AmmoPellet, kong=Kong.Diddy),
    Item(name="Grape", actor=0, model_two=0x15E, item_db=False, has_collision=True, hitbox=Hitbox(0, 0, 0), item_type=CollectableTypes.AmmoPellet, kong=Kong.Lanky),
    Item(name="Feather", actor=0, model_two=0x15D, item_db=False, has_collision=True, hitbox=Hitbox(0, 0, 0), item_type=CollectableTypes.AmmoPellet, kong=Kong.Tiny),
    Item(name="Pineapple", actor=0, model_two=0x15F, item_db=False, has_collision=True, hitbox=Hitbox(0, 0, 0), item_type=CollectableTypes.AmmoPellet, kong=Kong.Chunky),
    # Hints
    Item(name="Hint Item (DK)", actor=CustomActors.HintItemDK, model_two=638, bounce=True, has_collision=True),
    Item(name="Hint Item (Diddy)", actor=CustomActors.HintItemDiddy, model_two=649, bounce=True, has_collision=True),
    Item(name="Hint Item (Lanky)", actor=CustomActors.HintItemLanky, model_two=650, bounce=True, has_collision=True),
    Item(name="Hint Item (Tiny)", actor=CustomActors.HintItemTiny, model_two=651, bounce=True, has_collision=True),
    Item(name="Hint Item (Chunky)", actor=CustomActors.HintItemChunky, model_two=652, bounce=True, has_collision=True),
    # Multiplayer
    Item(name="Yellow CB Powerup", actor=0x78, model_two=0x1CF, item_db=False, has_collision=True, hitbox=Hitbox(0, 0, 0)),
    Item(name="Blue CB Powerup", actor=0x77, model_two=0x1D0, item_db=False, has_collision=True, hitbox=Hitbox(0, 0, 0)),
    Item(name="Coin Powerup", actor=0x76, model_two=0x1D1, item_db=False, has_collision=True, hitbox=Hitbox(0, 0, 0)),
    Item(name="Coin Multiplayer", actor=0x7A, model_two=0x1D2, item_db=False, has_collision=True, hitbox=Hitbox(0, 0, 0)),
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
    EnemyDropDef(CustomActors.ZingerFlamethrower, 0x2F, Song.MelonSliceDrop, 2),  # Flamethrowing Zinger
    EnemyDropDef(CustomActors.Scarab, 0x2F, Song.MelonSliceDrop, 1),  # Kiosk Bug Replica
    EnemyDropDef(288, 0x34, Song.Silence, 1),
]

dance_acceptable_items = [x for x in item_database if x.item_db and x.force_dance]
boss_enabled_items = [x for x in item_database if x.item_db and x.boss_enabled]
bounce_items = [x for x in item_database if x.item_db and x.bounce]
actor_drops = [x for x in item_database if x.item_db and x.actor is not None]
danceless_items = [x for x in item_database if x.item_db and not x.will_dance]
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
    fh.write(f"extern const item_scale_info item_scales[{len([x for x in item_database if x.item_db])}];\n")
    fh.write(f"typedef enum new_custom_actors {{\n")
    for e in CustomActors:
        fh.write(f"\t/* 0x{'{:03X}'.format(e.value)} */ NEWACTOR_{e.name.upper()} = {hex(e.value)}, \n")
    fh.write("\t/* ----- */ NEWACTOR_TERMINATOR, \n")
    fh.write("} new_custom_actors;\n")
    fh.write(f"#define DROP_COUNT {len(item_drops) + 1}\n")

with open("src/lib_items.c", "w") as fh:
    fh.write('#include "../include/common.h"\n\n')
    fh.write(warning_text)
    fh.write("\nconst short acceptable_items[] = {" + ",".join([hex(x.model_two) for x in dance_acceptable_items]) + "};")
    fh.write("\nconst item_conversion_info item_conversions[] = {\n\t" + ",\n\t".join([f"{{.actor={x.actor}, .model_two={x.model_two}, .scale={x.scale:.2f}f}}" for x in boss_enabled_items]) + "\n};")
    fh.write("\nconst unsigned short bounce_objects[] = {" + ",".join([str(x.actor) for x in bounce_items]) + "};")
    fh.write("\nconst unsigned short actor_drops[] = {" + ",".join([str(x.actor) for x in actor_drops]) + "};")
    # fh.write("\nconst unsigned short danceless_items[] = {" + ",".join([str(x.actor) for x in danceless_items]) + "};")
    fh.write("\nconst item_scale_info item_scales[] = {\n\t" + ",\n\t".join([f"{{.type={x.model_two}, .scale={x.scale:.2f}f}}" for x in item_database if x.item_db]) + "\n};")
    fh.write(
        "\ncollision_info object_collisions[] = {\n\t"
        + ",\n\t".join(
            [
                f"{{.type={x.model_two}, .collectable_type={x.item_type}, .unk4=0.08f, .unk8=0.95f, .intended_actor={x.kong}, .actor_equivalent={x.actor}, .hitbox_y_center={x.hitbox.y}, .hitbox_radius={x.hitbox.radius}, .hitbox_height={x.hitbox.height}}}"
                for x in item_database
                if x.has_collision
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
                "actor_type": CustomActors.NintendoCoin,
                "model": 0x10B,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Nintendo Coin
            {
                "actor_type": CustomActors.RarewareCoin,
                "model": 0x10D,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Rareware Coin
            # Potions
            {
                "actor_type": CustomActors.PotionDK,
                "model": 0xEE,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # DK Potion
            {
                "actor_type": CustomActors.PotionDiddy,
                "model": 0xEF,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Diddy Potion
            {
                "actor_type": CustomActors.PotionLanky,
                "model": 0xF0,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Lanky Potion
            {
                "actor_type": CustomActors.PotionTiny,
                "model": 0xF1,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Tiny Potion
            {
                "actor_type": CustomActors.PotionChunky,
                "model": 0xF2,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Chunky Potion
            {
                "actor_type": CustomActors.PotionAny,
                "model": 0xF3,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Any Potion
            # Kongs
            {
                "actor_type": CustomActors.KongDK,
                "model": 0xFE,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # DK
            {
                "actor_type": CustomActors.KongDiddy,
                "model": 0xFF,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Diddy
            {
                "actor_type": CustomActors.KongLanky,
                "model": 0x100,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Lanky
            {
                "actor_type": CustomActors.KongTiny,
                "model": 0x101,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Tiny
            {
                "actor_type": CustomActors.KongChunky,
                "model": 0x102,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Chunky
            # Shop Owners
            {
                "actor_type": CustomActors.CrankyItem,
                "model": 0x10F,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Cranky
            {
                "actor_type": CustomActors.FunkyItem,
                "model": 0x110,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Funky
            {
                "actor_type": CustomActors.CandyItem,
                "model": 0x111,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Candy
            {
                "actor_type": CustomActors.SnideItem,
                "model": 0x112,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Snide
            # Misc
            {
                "actor_type": CustomActors.Bean,
                "model": 0x105,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Bean
            {
                "actor_type": CustomActors.Pearl,
                "model": 0x107,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Pearl
            {
                "actor_type": CustomActors.Fairy,
                "model": 0xFC,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Fairy
            {
                "actor_type": CustomActors.Null,
                "model": 0,
                "code": 0x80689F80,
                "unk10": 0x8068A10C,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Nothing
            {
                "actor_type": CustomActors.Medal,
                "model": 0x109,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Medal
            {
                "actor_type": CustomActors.IceTrapGB,
                "model": 0xFD,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Fake Item
            {
                "actor_type": CustomActors.IceTrapBean,
                "model": 0x126,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Fake Item
            {
                "actor_type": CustomActors.IceTrapKey,
                "model": 0x129,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Fake Item
            {
                "actor_type": CustomActors.IceTrapFairy,
                "model": 0x12C,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Fake Item
            {
                "actor_type": CustomActors.HintItemDK,
                "model": 0x11A,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Hint Item
            {
                "actor_type": CustomActors.HintItemDiddy,
                "model": 0x11C,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Hint Item
            {
                "actor_type": CustomActors.HintItemLanky,
                "model": 0x11E,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Hint Item
            {
                "actor_type": CustomActors.HintItemTiny,
                "model": 0x120,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Hint Item
            {
                "actor_type": CustomActors.HintItemChunky,
                "model": 0x122,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # Hint Item
            {
                "actor_type": CustomActors.ArchipelagoItem,
                "model": 0x124,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # AP Item
            {
                "actor_type": CustomActors.SpecialArchipelagoItem,
                "model": 0x133,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # AP Item
            {
                "actor_type": CustomActors.FoolsArchipelagoItem,
                "model": 0x135,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # AP Item
            {
                "actor_type": CustomActors.TrapArchipelagoItem,
                "model": 0x137,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # AP Item
            {
                "actor_type": CustomActors.SpreadCounter,
                "model": 0x139,
                "code": 0x80689F80,
                "unk10": 0x80689FEC,
                "unk4": [0, 0, 0, 0, 0x02, 0x26, 0, 0],
            },  # AP Item
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
    actor_data = initActor(actor_data, CustomActors.NintendoCoin, "&GoldenBananaCode", 2, 0, 1, 8, 45)
    actor_data = initActor(actor_data, CustomActors.RarewareCoin, "&GoldenBananaCode", 2, 0, 1, 8, 45)
    actor_data = initActor(actor_data, CustomActors.Null, "&NothingCode", 4, 0, 1, 8, 0)
    actor_data = initActor(actor_data, CustomActors.Medal, "&GoldenBananaCode", 2, 0, 1, 8, 45)
    for potion in POTIONS:
        actor_data = initActor(actor_data, potion, "&PotionCode", 2, 0, 1, 8, 45)
    for kong in KONGS:
        actor_data = initActor(actor_data, kong, "&KongDropCode", 2, 0, 1, 8, 45)
    for shopkeeper in SHOPKEEPERS:
        actor_data = initActor(actor_data, shopkeeper, "&shopOwnerItemCode", 2, 0, 1, 8, 45)
    actor_data = initActor(actor_data, CustomActors.IceTrapGB, "&FakeGBCode", 2, 0, 1, 8, 45)
    actor_data = initActor(actor_data, CustomActors.IceTrapBean, "&FakeGBCode", 2, 0, 1, 8, 45)
    actor_data = initActor(actor_data, CustomActors.IceTrapKey, "&FakeKeyCode", 2, 0, 1, 8, 45)
    actor_data = initActor(actor_data, CustomActors.IceTrapFairy, "&FakeFairyCode", 2, 0, 1, 8, 45)
    actor_data = initActor(actor_data, CustomActors.SpreadCounter, "&newCounterCode", 2, 0, 1, 8, 70)

    actor_data = initActor(actor_data, CustomActors.Bean, "&GoldenBananaCode", 2, 0, 1, 8, 45)
    actor_data = initActor(actor_data, CustomActors.Pearl, "&GoldenBananaCode", 2, 0, 1, 8, 45)
    actor_data = initActor(actor_data, CustomActors.Fairy, "&fairyDuplicateCode", 2, 0, 1, 8, 45)
    actor_data = initActor(actor_data, CustomActors.HintItemDK, "&GoldenBananaCode", 2, 0, 1, 8, 45)
    actor_data = initActor(actor_data, CustomActors.HintItemDiddy, "&GoldenBananaCode", 2, 0, 1, 8, 45)
    actor_data = initActor(actor_data, CustomActors.HintItemLanky, "&GoldenBananaCode", 2, 0, 1, 8, 45)
    actor_data = initActor(actor_data, CustomActors.HintItemTiny, "&GoldenBananaCode", 2, 0, 1, 8, 45)
    actor_data = initActor(actor_data, CustomActors.HintItemChunky, "&GoldenBananaCode", 2, 0, 1, 8, 45)
    actor_data = initActor(actor_data, CustomActors.ArchipelagoItem, "&GoldenBananaCode", 2, 0, 1, 8, 45)
    actor_data = initActor(actor_data, CustomActors.SpecialArchipelagoItem, "&GoldenBananaCode", 2, 0, 1, 8, 45)
    actor_data = initActor(actor_data, CustomActors.FoolsArchipelagoItem, "&GoldenBananaCode", 2, 0, 1, 8, 45)
    actor_data = initActor(actor_data, CustomActors.TrapArchipelagoItem, "&FakeGBCode", 2, 0, 1, 8, 45)
    actor_data = initActor(actor_data, CustomActors.JetpacItemOverlay, "&getNextMoveText", 3, 0, 0, 0x10, 324)
    actor_data = initActor(actor_data, CustomActors.ZingerFlamethrower, "(void*)0x806B4958", 2, 1, 0, 2, 183)
    actor_data = initActor(actor_data, CustomActors.Scarab, "&kioskBugCode", 2, 1, 0, 2, 183)
    actor_data = initActor(actor_data, CustomActors.SlipPeel, "&slipPeelCode", 2, 1, 0, 8, 0xDE)
    for actor in GUARDS:
        actor_data = initActor(actor_data, actor, "(void*)0x806AF688", 2, 3, 0, 2, 259)
        
    actor_data = initActor(actor_data, 141, "&charSpawnerItemCode", 2, 0, 1, 0x40, 197)
    actor_data["actor_collisions"][CustomActors.Scarab] = {
        "collision_info": 0x8074B240,
        "unk_4": 1,
    }
    actor_data = initActor(actor_data, CustomActors.KopDummy, "&dummyGuardCode", 2, 0, 1, 8, 45)
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
            {
                "map": Maps.GalleonSealRace,
                "model2_id": 0x3B,
                "flag_index": 0xA5,
                "intended_kong_actor": 0,
            },
            {
                "map": Maps.CastleCarRace,
                "model2_id": 0x1,
                "flag_index": 0x145,
                "intended_kong_actor": 0,
            },
        ]
    )
    for sym in data_types:
        fh.write(f"\n{data_types[sym]} {sym}[] = {{\n\t" + ",\n\t".join([getActorDefaultString(x) for x in actor_data[sym]]) + "\n};")
    with open("include/item_data.h", "a") as fg:
        fg.write(f"extern GBDictItem new_flag_mapping[{len(actor_data['new_flag_mapping'])}];\n")
        # File Size Calc (Just for base hack testing purposes)
        static_expansion = 0x100
        balloon_expansion = 150
        target_gb_bits = 7
        kong_var_size = 0xA1 + ((target_gb_bits - 3) * 8) + target_gb_bits + 14
        file_info_location = 0x320 + static_expansion + balloon_expansion + (5 * kong_var_size)
        fg.write(f"#define FILE_INFO_SIZE {hex(file_info_location)}\n")
        fg.write(f"#define GB_DICTIONARY_COUNT {len(actor_data['new_flag_mapping'])}\n")
