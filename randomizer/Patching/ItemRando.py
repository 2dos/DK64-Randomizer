"""Apply item rando changes."""

from randomizer.Enums.Maps import Maps
from randomizer.Enums.Items import Items
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Settings import MicrohintsEnabled
from randomizer.Enums.Types import Types
from randomizer.Lists.Item import ItemList
from randomizer.Patching.Library.DataTypes import intf_to_float
from randomizer.Lists.EnemyTypes import enemy_location_list
from randomizer.Patching.Library.Generic import setItemReferenceName
from randomizer.Patching.Library.ItemRando import getModelFromItem, getItemPreviewText, getPropFromItem, getModelMask, getItemDBEntry, item_shop_text_mapping, BuyText
from randomizer.Patching.Library.Assets import getPointerLocation, TableNames
from randomizer.Patching.Library.ASM import getItemTableWriteAddress, populateOverlayOffsets, getSym, getROMAddress, Overlay
from randomizer.Patching.Patcher import LocalROM
from randomizer.CompileHints import getHelmProgItems, GetRegionIdOfLocation
import randomizer.ItemPool as ItemPool

TRAINING_LOCATIONS = (
    Locations.IslesSwimTrainingBarrel,
    Locations.IslesVinesTrainingBarrel,
    Locations.IslesOrangesTrainingBarrel,
    Locations.IslesBarrelsTrainingBarrel,
)
THEMATIC_TEXT = True

kong_flags = (385, 6, 70, 66, 117)

subitems = (Items.JunkOrange, Items.JunkAmmo, Items.JunkCrystal, Items.JunkMelon, Items.JunkFilm)
shop_owner_types = (Types.Cranky, Types.Funky, Types.Snide, Types.Candy)


class TextboxChange:
    """Class to store information which pertains to a change of textbox information."""

    def __init__(
        self,
        location,
        file_index,
        textbox_index,
        text_replace,
        default_type: Types,
        default_item: Items,
        replacement_text="|",
        force_pipe=False,
    ):
        """Initialize with given paremeters."""
        self.location = location
        self.file_index = file_index
        self.textbox_index = textbox_index
        self.text_replace = text_replace  # Text which is going to be replaced with replacement_text
        self.replacement_text = replacement_text
        self.force_pipe = force_pipe  # If True, don't replace with item name upon checking later. Instead, will be replaced in RDRAM dynamically
        self.default_type = default_type
        self.default_item = default_item


textboxes = [
    TextboxChange(Locations.AztecTinyBeetleRace, 14, 0, "GOLDEN BANANA", Types.Banana, Items.GoldenBanana, "\x04|\x04", True),
    TextboxChange(Locations.CavesLankyBeetleRace, 14, 0, "GOLDEN BANANA", Types.Banana, Items.GoldenBanana, "\x04|\x04", True),
    TextboxChange(Locations.JapesDiddyMinecarts, 16, 2, "GOLDEN BANANA", Types.Banana, Items.GoldenBanana),
    TextboxChange(Locations.JapesDiddyMinecarts, 16, 3, "BANANA", Types.Banana, Items.GoldenBanana),
    TextboxChange(Locations.JapesDiddyMinecarts, 16, 4, "BANANA", Types.Banana, Items.GoldenBanana),
    TextboxChange(Locations.ForestChunkyMinecarts, 16, 5, "GOLDEN BANANA", Types.Banana, Items.GoldenBanana),
    TextboxChange(Locations.ForestChunkyMinecarts, 16, 7, "BANANA", Types.Banana, Items.GoldenBanana),
    TextboxChange(Locations.CastleDonkeyMinecarts, 16, 8, "BE A WINNER", Types.Banana, Items.GoldenBanana, "WIN A |"),
    TextboxChange(Locations.CastleDonkeyMinecarts, 16, 9, "BANANA", Types.Banana, Items.GoldenBanana),
    TextboxChange(Locations.IslesDonkeyInstrumentPad, 16, 18, "ANOTHER BANANA", Types.Banana, Items.GoldenBanana, "SOMETHING"),
    TextboxChange(Locations.IslesDiddyInstrumentPad, 16, 18, "ANOTHER BANANA", Types.Banana, Items.GoldenBanana, "SOMETHING"),
    TextboxChange(Locations.IslesLankyInstrumentPad, 16, 18, "ANOTHER BANANA", Types.Banana, Items.GoldenBanana, "SOMETHING"),
    TextboxChange(Locations.IslesTinyInstrumentPad, 16, 18, "ANOTHER BANANA", Types.Banana, Items.GoldenBanana, "SOMETHING"),
    TextboxChange(Locations.IslesChunkyInstrumentPad, 16, 18, "ANOTHER BANANA", Types.Banana, Items.GoldenBanana, "SOMETHING"),
    TextboxChange(Locations.FactoryTinyCarRace, 17, 4, "GOLDEN BANANA", Types.Banana, Items.GoldenBanana),
    TextboxChange(
        Locations.GalleonTinyPearls,
        23,
        0,
        "PLEASE TRY AND GET THEM BACK",
        Types.Banana,
        Items.GoldenBanana,
        "IF YOU HELP ME FIND THEM, I WILL REWARD YOU WITH A |",
    ),
    TextboxChange(Locations.GalleonTinyPearls, 23, 1, "GOLDEN BANANA", Types.Banana, Items.GoldenBanana),
    TextboxChange(
        Locations.GalleonTinyPearls,
        23,
        2,
        "ALTOGETHER.",
        Types.Banana,
        Items.GoldenBanana,
        "ALTOGETHER. IF YOU FIND THEM ALL, YOU WILL RECEIVE A |",
    ),
    TextboxChange(Locations.AztecDiddyVultureRace, 15, 1, "PRIZE", Types.Banana, Items.GoldenBanana),
    TextboxChange(Locations.AztecDonkeyFreeLlama, 10, 1, "ALL THIS SAND", Types.Banana, Items.GoldenBanana, "THIS |"),
    TextboxChange(Locations.AztecDonkeyFreeLlama, 10, 2, "BANANA", Types.Banana, Items.GoldenBanana),
    TextboxChange(Locations.RarewareCoin, 8, 2, "RAREWARE COIN", Types.RarewareCoin, Items.RarewareCoin),  # Rareware Coin
    TextboxChange(Locations.RarewareCoin, 8, 34, "RAREWARE COIN", Types.RarewareCoin, Items.RarewareCoin),  # Rareware Coin
    TextboxChange(Locations.ForestLankyRabbitRace, 20, 1, "TROPHY", Types.Banana, Items.GoldenBanana, "| TROPHY"),
    TextboxChange(Locations.ForestLankyRabbitRace, 20, 2, "TROPHY", Types.Banana, Items.GoldenBanana, "| TROPHY"),
    TextboxChange(Locations.ForestLankyRabbitRace, 20, 3, "TROPHY", Types.Banana, Items.GoldenBanana, "| TROPHY"),
    TextboxChange(Locations.ForestChunkyApple, 22, 0, "BANANA", Types.Banana, Items.GoldenBanana),
    TextboxChange(Locations.ForestChunkyApple, 22, 1, "BANANA", Types.Banana, Items.GoldenBanana),
    TextboxChange(Locations.ForestChunkyApple, 22, 4, "BANANA", Types.Banana, Items.GoldenBanana),
    TextboxChange(Locations.GalleonDonkeySealRace, 28, 2, "CHEST O' GOLD", Types.Banana, Items.GoldenBanana),
    TextboxChange(Locations.RarewareBanana, 30, 0, "REWARD ANYONE", Types.Banana, Items.GoldenBanana, "REWARD ANYONE WITH A |"),
    TextboxChange(Locations.CavesLankyCastle, 33, 0, "HOW ABOUT IT", Types.Banana, Items.GoldenBanana, "HOW ABOUT A |"),
    TextboxChange(Locations.CastleTinyCarRace, 34, 4, "BANANA", Types.Banana, Items.GoldenBanana),
    TextboxChange(
        Locations.ForestDiddyOwlRace,
        21,
        0,
        "WHEN YOU CAN FLY",
        Types.Banana,
        Items.GoldenBanana,
        "WHEN YOU CAN FLY TO HAVE A CHANCE TO RECEIVE A |",
    ),
    TextboxChange(Locations.ForestTinySpiderBoss, 19, 32, "\x04GOLDEN BANANA\x04", Types.Banana, Items.GoldenBanana),
    TextboxChange(Locations.CavesChunky5DoorIgloo, 19, 34, "\x04GOLDEN BANANA\x04", Types.Banana, Items.GoldenBanana),
]

level_names = {
    Levels.JungleJapes: "Jungle Japes",
    Levels.AngryAztec: "Angry Aztec",
    Levels.FranticFactory: "Frantic Factory",
    Levels.GloomyGalleon: "Gloomy Galleon",
    Levels.FungiForest: "Fungi Forest",
    Levels.CrystalCaves: "Crystal Caves",
    Levels.CreepyCastle: "Creepy Castle",
    Levels.DKIsles: "DK Isles",
    Levels.HideoutHelm: "Hideout Helm",
}

kong_names = {
    Kongs.donkey: "Donkey Kong",
    Kongs.diddy: "Diddy",
    Kongs.lanky: "Lanky",
    Kongs.tiny: "Tiny",
    Kongs.chunky: "Chunky",
    Kongs.any: "Any Kong",
}


class ItemPatchingInfo:
    """Class to store information regarding how an item is patched into ROM."""

    def __init__(self, response_type: int, level: int = 0, kong: int = 0, audiovisual_medal: int = 0):
        """Initialize with given parameters."""
        self.response_type = response_type
        self.level = level
        self.kong = kong
        self.audiovisual_medal = audiovisual_medal


def getItemPatchingFromList(list_set: list, item: Items, type_str: str, throw_error: bool = True):
    """Get the move index from a list."""
    if item not in list_set:
        if throw_error:
            raise Exception(f"{type_str} Type provided, but invalid {type_str} item provided resulting in search mismatch")
        return None
    return list_set.index(item)


def getItemPatchingData(item_type: Types, item: Items) -> ItemPatchingInfo:
    """Get the data associated with how an item is patched into ROM from various attributes."""
    simple_types = {
        Types.Banana: 3,
        Types.Fairy: 5,
        Types.Crown: 7,
        Types.Medal: 9,
        Types.Bean: 10,
        Types.Pearl: 11,
        Types.RainbowCoin: 12,
        Types.JunkItem: 18,
        Types.FillerBanana: 3,
        Types.FillerFairy: 5,
        Types.FillerCrown: 7,
        Types.FillerMedal: 9,
        Types.FillerPearl: 11,
    }
    if item_type in simple_types:
        return ItemPatchingInfo(simple_types[item_type])
    elif item_type == Types.NintendoCoin:
        return ItemPatchingInfo(8, 0, 0)
    elif item_type == Types.RarewareCoin:
        return ItemPatchingInfo(8, 0, 1)
    elif item_type == Types.Key:
        key_index = getItemPatchingFromList(ItemPool.Keys(), item, "Key")
        return ItemPatchingInfo(6, key_index)
    elif item_type == Types.FakeItem:
        idx_lst = [Items.IceTrapBubble, Items.IceTrapBubbleBean, Items.IceTrapBubbleKey]
        if item in idx_lst:
            return ItemPatchingInfo(13, 0, 1)
        idx_lst = [Items.IceTrapReverse, Items.IceTrapReverseBean, Items.IceTrapReverseKey]
        if item in idx_lst:
            return ItemPatchingInfo(13, 0, 2)
        idx_lst = [Items.IceTrapSlow, Items.IceTrapSlowBean, Items.IceTrapSlowKey]
        if item in idx_lst:
            return ItemPatchingInfo(13, 0, 3)
        idx_lst = [Items.IceTrapDisableA, Items.IceTrapDisableABean, Items.IceTrapDisableAKey]
        if item in idx_lst:
            return ItemPatchingInfo(13, 0, 5)
        idx_lst = [Items.IceTrapDisableB, Items.IceTrapDisableBBean, Items.IceTrapDisableBKey]
        if item in idx_lst:
            return ItemPatchingInfo(13, 0, 6)
        idx_lst = [Items.IceTrapDisableZ, Items.IceTrapDisableZBean, Items.IceTrapDisableZKey]
        if item in idx_lst:
            return ItemPatchingInfo(13, 0, 7)
        idx_lst = [Items.IceTrapDisableCU, Items.IceTrapDisableCUBean, Items.IceTrapDisableCUKey]
        if item in idx_lst:
            return ItemPatchingInfo(13, 0, 8)
        raise Exception("Ice Trap Type provided, but invalid Ice Trap item provided resulting in search mismatch")
    elif item_type == Types.Blueprint:
        bp_index = getItemPatchingFromList(ItemPool.Blueprints(), item, "BP")
        bp_level = int(bp_index / 5)
        bp_kong = bp_index % 5
        # Isles is first on that BP list, so shift it to last
        if bp_level == 0:
            bp_level = 7
        else:
            bp_level -= 1
        return ItemPatchingInfo(4, bp_level, bp_kong)
    elif item_type == Types.Kong:
        kong_lst = [Items.Donkey, Items.Diddy, Items.Lanky, Items.Tiny, Items.Chunky]
        kong_index = getItemPatchingFromList(kong_lst, item, "Kong")
        return ItemPatchingInfo(1, 0, kong_index)
    elif item_type in (Types.Hint, Types.ProgressiveHint):
        hint_index = getItemPatchingFromList(ItemPool.HintItems(), item, "Hint")
        hint_level = int(hint_index / 5)
        hint_kong = hint_index % 5
        return ItemPatchingInfo(19, hint_level, hint_kong)
    elif item_type in (Types.Shockwave, Types.Shop, Types.Climbing, Types.TrainingBarrel):
        # Special Moves
        idx_lst = [Items.BaboonBlast, Items.ChimpyCharge, Items.Orangstand, Items.MiniMonkey, Items.HunkyChunky]
        idx = getItemPatchingFromList(idx_lst, item, "Move", False)
        if idx is not None:
            return ItemPatchingInfo(2, 0, idx, 1)
        idx_lst = [Items.StrongKong, Items.RocketbarrelBoost, Items.BaboonBalloon, Items.PonyTailTwirl, Items.PrimatePunch]
        idx = getItemPatchingFromList(idx_lst, item, "Move", False)
        if idx is not None:
            return ItemPatchingInfo(2, 1, idx, 1)
        idx_lst = [Items.GorillaGrab, Items.SimianSpring, Items.OrangstandSprint, Items.Monkeyport, Items.GorillaGone]
        idx = getItemPatchingFromList(idx_lst, item, "Move", False)
        if idx is not None:
            return ItemPatchingInfo(2, 2, idx, 1)
        # Slam
        if item in [Items.ProgressiveSlam, Items.ProgressiveSlam2, Items.ProgressiveSlam3]:
            return ItemPatchingInfo(2, 3, 0, 1)
        # Gun
        idx_lst = [Items.Coconut, Items.Peanut, Items.Grape, Items.Feather, Items.Pineapple]
        idx = getItemPatchingFromList(idx_lst, item, "Move", False)
        if idx is not None:
            return ItemPatchingInfo(2, 4, idx, 2)
        # Homing/Sniper
        if item == Items.HomingAmmo:
            return ItemPatchingInfo(2, 5, 2)
        if item == Items.SniperSight:
            return ItemPatchingInfo(2, 6, 2)
        # Ammo Belt
        if item in (Items.ProgressiveAmmoBelt, Items.ProgressiveAmmoBelt2):
            return ItemPatchingInfo(2, 7, 2)
        # Instrument
        idx_lst = [Items.Bongos, Items.Guitar, Items.Trombone, Items.Saxophone, Items.Triangle]
        idx = getItemPatchingFromList(idx_lst, item, "Move", False)
        if idx is not None:
            return ItemPatchingInfo(2, 8, idx, 3)
        # Progressive Instrument Upgrades
        if item in (Items.ProgressiveInstrumentUpgrade, Items.ProgressiveInstrumentUpgrade2, Items.ProgressiveInstrumentUpgrade3):
            return ItemPatchingInfo(2, 9, 0, 3)
        # Misc flag moves
        idx_lst = [Items.Swim, Items.Oranges, Items.Barrels, Items.Vines, Items.Camera, Items.Shockwave]
        idx = getItemPatchingFromList(idx_lst, item, "Move", False)
        if idx is not None:
            visual_index = 1
            if item == Items.Camera:
                visual_index = 4
            elif item == Items.Shockwave:
                visual_index = 5
            return ItemPatchingInfo(2, 10, idx, visual_index)
        if item == Items.CameraAndShockwave:
            return ItemPatchingInfo(2, 10, 4, 4)
        # Climbing
        if item == Items.Climbing:
            return ItemPatchingInfo(2, 11, 0, 1)
        raise Exception("Could not find valid move")
    elif item is None or item == Items.NoItem:
        return ItemPatchingInfo(0)
    elif item_type in (Types.Cranky, Types.Funky, Types.Candy, Types.Snide):
        shopkeeper_lst = [Items.Cranky, Items.Funky, Items.Candy, Items.Snide]
        shopkeeper_index = getItemPatchingFromList(shopkeeper_lst, item, "Shopkeeper")
        return ItemPatchingInfo(20, 0, shopkeeper_index)
    raise Exception("Invalid item for patching")


def appendTextboxChange(spoiler, file_index: int, textbox_index: int, search: str, target: str):
    """Alter a specific textbox."""
    data = {"textbox_index": textbox_index, "mode": "replace", "search": search, "target": target}
    if file_index in spoiler.text_changes:
        spoiler.text_changes[file_index].append(data)
    else:
        spoiler.text_changes[file_index] = [data]


def writeBuyText(item: Items, address: int, ROM_COPY: LocalROM):
    """Write the buy text to the world based on the item."""
    ROM_COPY.seek(address)
    if item is None or item == Items.NoItem:
        ROM_COPY.writeMultipleBytes(0, 2)
        return
    data = item_shop_text_mapping.get(item, (0, 0))
    ROM_COPY.write(data[0])
    ROM_COPY.write(data[1] + BuyText.terminator)


NUMBERS_AS_WORDS = ["ZERO", "ONE", "TWO", "THREE", "FOUR", "FIVE"]

HOLDABLE_LOCATION_INFO = {
    Locations.HoldableBoulderIslesNearAztec: {
        "map_id": Maps.Isles,
        "spawner_id": 12,
    },
    Locations.HoldableBoulderIslesNearCaves: {
        "map_id": Maps.Isles,
        "spawner_id": 13,
    },
    Locations.HoldableBoulderAztec: {
        "map_id": Maps.AngryAztec,
        "spawner_id": 4,
    },
    Locations.HoldableBoulderCavesSmall: {
        "map_id": Maps.CrystalCaves,
        "spawner_id": 0,
    },
    Locations.HoldableBoulderCavesLarge: {
        "map_id": Maps.CrystalCaves,
        "spawner_id": 1,
    },
    Locations.HoldableBoulderMuseum: {
        "map_id": Maps.CastleMuseum,
        "spawner_id": 0,
    },
    Locations.HoldableBoulderJapesLobby: {
        "map_id": Maps.JungleJapesLobby,
        "spawner_id": 2,
    },
    Locations.HoldableBoulderCastleLobby: {
        "map_id": Maps.CreepyCastleLobby,
        "spawner_id": 0,
    },
    Locations.HoldableBoulderCavesLobby: {
        "map_id": Maps.CrystalCavesLobby,
        "spawner_id": 5,
    },
    Locations.HoldableKegMillFrontNear: {
        "map_id": Maps.ForestMillFront,
        "spawner_id": 5,
    },
    Locations.HoldableKegMillFrontFar: {
        "map_id": Maps.ForestMillFront,
        "spawner_id": 7,
    },
    Locations.HoldableKegMillRear: {
        "map_id": Maps.ForestMillBack,
        "spawner_id": 4,
    },
    Locations.HoldableVaseCircle: {
        "map_id": Maps.AngryAztec,
        "spawner_id": 3,
    },
    Locations.HoldableVaseColon: {
        "map_id": Maps.AngryAztec,
        "spawner_id": 2,
    },
    Locations.HoldableVaseTriangle: {
        "map_id": Maps.AngryAztec,
        "spawner_id": 1,
    },
    Locations.HoldableVasePlus: {
        "map_id": Maps.AngryAztec,
        "spawner_id": 0,
    },
}


def alterTextboxRequirements(spoiler):
    """Alters various textboxes based on the requirement count changing."""
    pearl_req = spoiler.settings.mermaid_gb_pearls
    appendTextboxChange(spoiler, 23, 2, "FIVE MISSING PEARLS", f"{NUMBERS_AS_WORDS[pearl_req]} MISSING PEARL{'S' if pearl_req != 1 else ''}")
    all_text = ""
    if pearl_req == 5:
        all_text = "ALL "
    plea_including_pearl_count = f"PLEASE TRY AND GET {all_text}{NUMBERS_AS_WORDS[pearl_req]} OF THEM BACK"
    for x in textboxes:
        if x.location == Locations.GalleonTinyPearls and x.textbox_index == 0:
            x.text_replace = plea_including_pearl_count
            x.replacement_text = f"IF YOU HELP ME FIND {all_text}{NUMBERS_AS_WORDS[pearl_req]} OF THEM, I WILL REWARD YOU WITH A |"
    appendTextboxChange(spoiler, 23, 0, "PLEASE TRY AND GET THEM BACK", plea_including_pearl_count)
    fairy_req = spoiler.settings.rareware_gb_fairies
    if fairy_req != 20:
        appendTextboxChange(spoiler, 30, 0, "FIND THEM ALL", f"FIND {fairy_req} OF THEM")
        appendTextboxChange(spoiler, 40, 0, "RESCUED ALL THE BANANA FAIRIES", "RESCUED THE BANANA FAIRIES")
    appendTextboxChange(spoiler, 40, 4, "MUST GET FAIRIES", f"MUST GET {fairy_req} FAIRIES")


def pushItemMicrohints(spoiler):
    """Push hint for the micro-hints system."""
    helm_prog_items = getHelmProgItems(spoiler)
    hinted_items = [
        # Key = Item, Value = (Textbox index in text file 19, (all_accepted_settings))
        (helm_prog_items[0], 26, [MicrohintsEnabled.base, MicrohintsEnabled.all]),
        (helm_prog_items[1], 25, [MicrohintsEnabled.base, MicrohintsEnabled.all]),
        (Items.Bongos, 27, [MicrohintsEnabled.all]),
        (Items.Triangle, 28, [MicrohintsEnabled.all]),
        (Items.Saxophone, 29, [MicrohintsEnabled.all]),
        (Items.Trombone, 30, [MicrohintsEnabled.all]),
        (Items.Guitar, 31, [MicrohintsEnabled.all]),
        (Items.ProgressiveSlam, 33, [MicrohintsEnabled.base, MicrohintsEnabled.all]),
        (Items.Cranky, 35, [MicrohintsEnabled.off, MicrohintsEnabled.base, MicrohintsEnabled.all]),
        (Items.Funky, 36, [MicrohintsEnabled.off, MicrohintsEnabled.base, MicrohintsEnabled.all]),
        (Items.Candy, 37, [MicrohintsEnabled.off, MicrohintsEnabled.base, MicrohintsEnabled.all]),
        (Items.Snide, 38, [MicrohintsEnabled.off, MicrohintsEnabled.base, MicrohintsEnabled.all]),
    ]
    for item_hint, item_data in enumerate(hinted_items):
        if spoiler.settings.microhints_enabled in list(item_data[2]):
            if ItemList[item_data[0]].name in spoiler.microhints:
                data = {
                    "textbox_index": item_data[1],
                    "mode": "replace_whole",
                    "target": spoiler.microhints[ItemList[item_data[0]].name],
                }
                if 19 in spoiler.text_changes:
                    spoiler.text_changes[19].append(data)
                else:
                    spoiler.text_changes[19] = [data]

def writeNullShopSlot(ROM_COPY: LocalROM, location: int):
    """Write an empty shop slot."""
    ROM_COPY.seek(location)
    for _ in range(3):
        ROM_COPY.writeMultipleBytes(0, 2)


def writeShopData(ROM_COPY: LocalROM, location: int, ipd: ItemPatchingInfo, price: int):
    """Write shop data to slot."""
    if ipd is not None:
        ROM_COPY.seek(location)
        ROM_COPY.writeMultipleBytes(ipd.response_type, 1)
        ROM_COPY.writeMultipleBytes(ipd.level, 1)
        ROM_COPY.writeMultipleBytes(ipd.kong, 1)
        ROM_COPY.writeMultipleBytes(ipd.audiovisual_medal, 1)
    ROM_COPY.seek(location + 4)
    ROM_COPY.writeMultipleBytes(0, 1)  # Pad
    ROM_COPY.writeMultipleBytes(price, 1)


def getHintKongFromFlag(flag: int) -> int:
    """Get the kong associated with a hint from it's flag."""
    return (flag - 0x384) % 5


def setItemInWorld(ROM_COPY: LocalROM, offset: int, base_flag: int, current_flag: int):
    """Write item to world array."""
    delta = current_flag - base_flag
    flag_offset = delta >> 3
    flag_shift = delta & 7
    ROM_COPY.seek(offset + flag_offset)
    raw = int.from_bytes(ROM_COPY.readBytes(1), "big")
    ROM_COPY.seek(offset + flag_offset)
    ROM_COPY.writeMultipleBytes(raw | (1 << flag_shift), 1)


def getActorIndex(item):
    """Get actor index from item."""
    item_type = item.new_item
    if item_type is None:
        item_type = Types.NoItem
    index = getItemDBEntry(item_type).index_getter(item.new_subitem, item.new_flag, item.shared)
    return getItemDBEntry(item_type).actor_index[index]


model_two_items = [
    0x74,  # GB
    0xDE,  # BP - DK
    0xE0,  # BP - Diddy
    0xE1,  # BP - Lanky
    0xDD,  # BP - Tiny
    0xDF,  # BP - Chunky
    0x48,  # Nintendo Coin
    0x28F,  # Rareware Coin
    0x13C,  # Key
    0x18D,  # Crown
    0x90,  # Medal
    0x288,  # Rareware GB
    0x198,  # Bean
    0x1B4,  # Pearls
]

POINTER_ROM_BONUSES = 0x1FF1200
POINTER_ROM_ENEMIES = 0x1FF9000
POINTER_ROM_IPDTABLE = 0x1FF2000


def place_randomized_items(spoiler, original_flut: list, ROM_COPY: LocalROM):
    """Place randomized items into ROM."""
    sav = spoiler.settings.rom_data
    ROM_COPY.seek(sav + 0x1EC)
    ROM_COPY.writeMultipleBytes(0xF0, 1)
    spoiler.japes_rock_actor = 45
    spoiler.aztec_vulture_actor = 45
    FAST_START = spoiler.settings.fast_start_beginning_of_game
    if spoiler.settings.shuffle_items:
        ROM_COPY.seek(sav + 0x034)
        ROM_COPY.write(1)  # Item Rando Enabled
        item_data = spoiler.item_assignment

        map_items = {}
        bonus_table_offset = 0
        ipd_data = original_flut.copy()
        offset_dict = populateOverlayOffsets(ROM_COPY)
        pushItemMicrohints(spoiler)
        pregiven_shop_owners = None
        # Place first move, if fast start is off
        if not FAST_START:
            placed_item = spoiler.first_move_item
            write_space = spoiler.settings.move_location_data + (6 * 125)
            if placed_item is None:
                # Is Nothing
                writeNullShopSlot(ROM_COPY, write_space)
            else:
                prog_flags = {
                    Items.ProgressiveSlam: [0x3BC, 0x3BD, 0x3BE],
                    Items.ProgressiveAmmoBelt: [0x292, 0x293],
                    Items.ProgressiveInstrumentUpgrade: [0x294, 0x295, 0x296],
                }
                if placed_item in prog_flags:
                    item_flag = prog_flags[placed_item][0]
                else:
                    item_flag = ItemList[placed_item].rando_flag
                if item_flag is not None and item_flag & 0x8000:
                    # Is move
                    writeShopData(ROM_COPY, write_space, None, 0)  # What to do here?
                else:
                    # Is Flagged Item
                    writeShopData(ROM_COPY, write_space, None, 0)  # What to do here?
        # Go through bijection
        for item in item_data:
            if item.can_have_item:
                # Write placement
                item_properties = getItemPatchingData(item.new_item, item.new_subitem)
                if item.is_shop:
                    # Write in placement index
                    movespaceOffset = spoiler.settings.move_location_data
                    if item.location in TRAINING_LOCATIONS:
                        if not FAST_START:
                            # Add to bonus table
                            old_tflag = 0x182 + TRAINING_LOCATIONS.index(item.location)
                            ROM_COPY.seek(POINTER_ROM_BONUSES + (4 * bonus_table_offset))
                            ROM_COPY.writeMultipleBytes(old_tflag, 2)
                            ROM_COPY.writeMultipleBytes(getActorIndex(item), 2)
                            bonus_table_offset += 1
                            # Append to FLUT
                            data = [old_tflag]
                            if item.new_item is None:
                                data.append(0)
                            else:
                                data.append(item.new_flag)
                            ipd_data.append(data)
                    for placement in item.placement_index:
                        write_space = movespaceOffset + (6 * placement)
                        if item.new_item is None:
                            # Is Nothing
                            # First check if there is an item here
                            ROM_COPY.seek(write_space)
                            check = int.from_bytes(ROM_COPY.readBytes(1), "big")
                            if check == 0 or placement >= 120:  # No Item
                                writeNullShopSlot(ROM_COPY, write_space)
                        elif item.new_flag & 0x8000:
                            # Is Move
                            writeShopData(ROM_COPY, write_space, item_properties, item.price)
                        else:
                            # Is Flagged Item
                            price_var = 0
                            if isinstance(item.price, list):
                                price_var = 0
                            else:
                                price_var = item.price
                            writeShopData(ROM_COPY, write_space, item_properties, price_var)
                        if spoiler.settings.enable_shop_hints and placement < 120:
                            addr = getItemTableWriteAddress(ROM_COPY, Types.Shop, placement, offset_dict)
                            writeBuyText(item.new_subitem, addr, ROM_COPY)
                elif not item.reward_spot:
                    for map_id in item.placement_data:
                        if map_id not in map_items:
                            map_items[map_id] = []
                        if item.new_item is None:
                            map_items[map_id].append(
                                {
                                    "id": item.placement_data[map_id],
                                    "obj": Types.NoItem,
                                    "kong": 0,
                                    "flag": 0,
                                    "upscale": 1,
                                    "shared": False,
                                    "subitem": 0,
                                }
                            )
                        else:
                            numerator = getItemDBEntry(item.new_item).scale
                            denominator = getItemDBEntry(item.old_item).scale
                            upscale = numerator / denominator
                            map_items[map_id].append(
                                {
                                    "id": item.placement_data[map_id],
                                    "obj": item.new_item,
                                    "kong": item.new_kong,
                                    "flag": item.new_flag,
                                    "upscale": upscale,
                                    "shared": item.shared,
                                    "subitem": item.new_subitem,
                                }
                            )
                    if item.location == Locations.NintendoCoin:
                        spoiler.arcade_item_reward = item.new_subitem
                        arcade_rewards = (
                            Types.NoItem,  # Or Nintendo Coin
                            Types.Bean,
                            Types.Blueprint,
                            Types.Crown,
                            Types.Fairy,
                            Types.Banana,
                            Types.Key,
                            Types.Medal,
                            Types.Pearl,
                            Types.Shop,  # Handled in special case
                            Types.Shop,  # Handled in special case
                            Types.Shop,  # Handled in special case
                            Types.Shop,  # Handled in special case
                            Types.Shop,  # Handled in special case
                            Types.Shop,  # Handled in special case
                            Types.Kong,  # Handled in special case
                            Types.Kong,  # Handled in special case
                            Types.Kong,  # Handled in special case
                            Types.Kong,  # Handled in special case
                            Types.Kong,  # Handled in special case
                            Types.RainbowCoin,
                            Types.RarewareCoin,  # Flag check handled separately
                            Types.JunkItem,
                        )
                        arcade_reward_index = 0
                        if item.new_item == Types.Kong:
                            if item.new_flag in kong_flags:
                                arcade_reward_index = kong_flags.index(item.new_flag) + 15
                        elif item.new_item in (Types.Shop, Types.TrainingBarrel, Types.Shockwave, Types.Climbing):
                            if (item.new_flag & 0x8000) == 0:
                                slot = 5
                            else:
                                slot = (item.new_flag >> 12) & 7
                                if item.shared or slot > 5:
                                    slot = 5
                            arcade_reward_index = 9 + slot
                        elif item.new_item in arcade_rewards:
                            arcade_reward_index = arcade_rewards.index(item.new_item)
                        elif item.new_item == Types.FillerBanana:
                            arcade_reward_index = 5
                        elif item.new_item == Types.FillerCrown:
                            arcade_reward_index = 3
                        elif item.new_item == Types.FillerMedal:
                            arcade_reward_index = 7
                        elif item.new_item == Types.FillerFairy:
                            arcade_reward_index = 4
                        elif item.new_item == Types.FillerPearl:
                            arcade_reward_index = 8
                        ROM_COPY.seek(sav + 0x110)
                        ROM_COPY.write(arcade_reward_index)
                    elif item.location == Locations.RarewareCoin:
                        spoiler.jetpac_item_reward = item.new_subitem
                        jetpac_rewards = (
                            Types.NoItem,  # Or RW Coin
                            Types.Bean,
                            Types.Blueprint,
                            Types.Crown,
                            Types.Fairy,
                            Types.Banana,
                            Types.Key,
                            Types.Medal,
                            Types.Pearl,
                            Types.Shop,  # Shockwave/Training/Climbing handled separately
                            Types.Kong,
                            Types.RainbowCoin,
                            Types.NintendoCoin,  # Flag check handled separately
                            Types.JunkItem,
                        )
                        jetpac_reward_index = 0
                        if item.new_item in (Types.Shop, Types.TrainingBarrel, Types.Shockwave, Types.Climbing):
                            jetpac_reward_index = 9
                        elif item.new_item in jetpac_rewards:
                            jetpac_reward_index = jetpac_rewards.index(item.new_item)
                        elif item.new_item == Types.FillerBanana:
                            jetpac_reward_index = 5
                        elif item.new_item == Types.FillerPearl:
                            jetpac_reward_index = 8
                        elif item.new_item == Types.FillerCrown:
                            jetpac_reward_index = 3
                        elif item.new_item == Types.FillerMedal:
                            jetpac_reward_index = 7
                        elif item.new_item == Types.FillerFairy:
                            jetpac_reward_index = 4
                        ROM_COPY.seek(sav + 0x111)
                        ROM_COPY.write(jetpac_reward_index)
                    elif item.location in (Locations.ForestDonkeyBaboonBlast, Locations.CavesDonkeyBaboonBlast):
                        # Autocomplete bonus barrel fix
                        actor_index = getActorIndex(item)
                        ROM_COPY.seek(POINTER_ROM_BONUSES + (4 * bonus_table_offset))
                        ROM_COPY.writeMultipleBytes(item.old_flag, 2)
                        ROM_COPY.writeMultipleBytes(actor_index, 2)
                        bonus_table_offset += 1
                else:
                    if item.old_item != Types.Medal:
                        actor_index = getActorIndex(item)
                    if item.old_item == Types.Blueprint:
                        # Write to BP Table
                        # Just needs to store an array of actors spawned
                        addr = getItemTableWriteAddress(ROM_COPY, Types.Blueprint, item.old_flag - 469, offset_dict)
                        ROM_COPY.seek(addr)
                        ROM_COPY.writeMultipleBytes(actor_index, 2)
                    elif item.old_item == Types.Crown:
                        # Write to Crown Table
                        crown_flags = [0x261, 0x262, 0x263, 0x264, 0x265, 0x268, 0x269, 0x266, 0x26A, 0x267]
                        addr = getItemTableWriteAddress(ROM_COPY, Types.Crown, crown_flags.index(item.old_flag), offset_dict)
                        ROM_COPY.seek(addr)
                        ROM_COPY.writeMultipleBytes(actor_index, 2)
                    elif item.old_item == Types.Key:
                        key_flags = [26, 74, 138, 168, 236, 292, 317, 380]
                        addr = getItemTableWriteAddress(ROM_COPY, Types.Key, key_flags.index(item.old_flag), offset_dict)
                        ROM_COPY.seek(addr)
                        ROM_COPY.writeMultipleBytes(actor_index, 2)
                    elif item.old_item == Types.RainbowCoin:
                        index = item.location - Locations.RainbowCoin_Location00
                        if index < 16:
                            addr = getItemTableWriteAddress(ROM_COPY, Types.RainbowCoin, index, offset_dict)
                            ROM_COPY.seek(addr)
                            ROM_COPY.writeMultipleBytes(actor_index, 2)
                        else:
                            raise Exception("Dirt Patch Item Placement Error")
                    elif item.old_item == Types.CrateItem:
                        index = item.location - Locations.MelonCrate_Location00
                        if index < 13:
                            addr = getItemTableWriteAddress(ROM_COPY, Types.CrateItem, index, offset_dict)
                            ROM_COPY.seek(addr)
                            ROM_COPY.writeMultipleBytes(actor_index, 2)
                        else:
                            raise Exception("Melon Crate Item Placement Error")
                    elif item.old_item == Types.BoulderItem:
                        index = item.location - Locations.HoldableBoulderIslesNearAztec
                        if index < 16:
                            addr = getItemTableWriteAddress(ROM_COPY, Types.BoulderItem, index, offset_dict)
                            ROM_COPY.seek(addr)
                            ROM_COPY.writeMultipleBytes(actor_index, 2)
                            ROM_COPY.writeMultipleBytes(HOLDABLE_LOCATION_INFO[item.location]["map_id"], 2)
                            ROM_COPY.writeMultipleBytes(HOLDABLE_LOCATION_INFO[item.location]["spawner_id"], 2)
                        else:
                            raise Exception("Melon Crate Item Placement Error")
                    elif item.old_item == Types.Enemies:
                        index = item.location - Locations.JapesMainEnemy_Start
                        ROM_COPY.seek(POINTER_ROM_ENEMIES + (index * 4))
                        ROM_COPY.writeMultipleBytes(enemy_location_list[item.location].map, 1)
                        ROM_COPY.writeMultipleBytes(enemy_location_list[item.location].id, 1)
                        ROM_COPY.writeMultipleBytes(actor_index, 2)
                    elif item.old_item in (Types.Medal, Types.Hint):
                        offset = None
                        if item.old_item == Types.Medal:
                            offset = item.old_flag - 549
                            if item.old_flag >= 0x3C6 and item.old_flag < 0x3CB:  # Isles Medals
                                offset = 40 + (item.old_flag - 0x3C6)
                        elif item.old_item == Types.Hint:
                            offset = item.old_flag - 0x384
                        addr = getItemTableWriteAddress(ROM_COPY, item.old_item, offset, offset_dict)
                        ROM_COPY.seek(addr)
                        ROM_COPY.write(item_properties.response_type)
                        ROM_COPY.write(item_properties.level)
                        ROM_COPY.write(item_properties.kong)
                        ROM_COPY.write(item_properties.audiovisual_medal)
                    elif item.location == Locations.JapesChunkyBoulder:
                        # Write to Boulder Spawn Location
                        spoiler.japes_rock_actor = actor_index
                    elif item.location == Locations.AztecLankyVulture:
                        # Write to Vulture Spawn Location
                        spoiler.aztec_vulture_actor = actor_index
                    elif item.old_item == Types.Banana:
                        # Bonus GB Table
                        ROM_COPY.seek(POINTER_ROM_BONUSES + (4 * bonus_table_offset))
                        ROM_COPY.writeMultipleBytes(item.old_flag, 2)
                        ROM_COPY.writeMultipleBytes(actor_index, 2)
                        bonus_table_offset += 1
                    elif item.old_item == Types.Fairy:
                        # Fairy Item
                        model = getModelFromItem(item.new_subitem, item.new_item, item.new_flag, item.shared)
                        if model is not None:
                            addr = getItemTableWriteAddress(ROM_COPY, Types.Fairy, item.old_flag - 589, offset_dict)
                            ROM_COPY.seek(addr)
                            ROM_COPY.writeMultipleBytes(model, 2)
                            ROM_COPY.writeMultipleBytes(0, 2)
                            ROM_COPY.write(item_properties.response_type)
                            ROM_COPY.write(item_properties.level)
                            ROM_COPY.write(item_properties.kong)
                            ROM_COPY.write(item_properties.audiovisual_medal)
                    elif item.old_item == Types.Kong:
                        kong_idx = {
                            Locations.DiddyKong: 0,
                            Locations.LankyKong: 1,
                            Locations.TinyKong: 2,
                            Locations.ChunkyKong: 3,
                        }
                        if item.location in kong_idx:
                            model = getModelFromItem(item.new_subitem, item.new_item, item.new_flag, item.shared)
                            if model is not None:
                                idx = kong_idx[item.location]
                                has_no_textures = item.new_item in (
                                    Types.Candy,
                                    Types.Climbing,
                                    Types.Cranky,
                                    Types.Fairy,
                                    Types.FillerFairy,
                                    Types.Funky,
                                    Types.Shockwave,
                                    Types.Shop,
                                    Types.TrainingBarrel,
                                )
                                addr = getItemTableWriteAddress(ROM_COPY, Types.Kong, idx, offset_dict)
                                ROM_COPY.seek(addr)
                                ROM_COPY.writeMultipleBytes(model, 2)
                                ROM_COPY.writeMultipleBytes(has_no_textures, 1)
                                ROM_COPY.writeMultipleBytes(0, 1)
                                ROM_COPY.write(item_properties.response_type)
                                ROM_COPY.write(item_properties.level)
                                ROM_COPY.write(item_properties.kong)
                                ROM_COPY.write(item_properties.audiovisual_medal)
            if item.new_item == Types.Hint:
                offset = item.new_flag - 0x384
                tied_region = GetRegionIdOfLocation(spoiler, item.location)
                spoiler.tied_hint_regions[offset] = spoiler.RegionList[tied_region].hint_name
            helm_medals = (
                Locations.HelmDonkeyMedal,
                Locations.HelmDiddyMedal,
                Locations.HelmLankyMedal,
                Locations.HelmTinyMedal,
                Locations.HelmChunkyMedal,
            )
            placed_items = (
                # Anything that's pre-placed into the world or spawns an item that's grabbed physically by the player
                Types.Blueprint,
                Types.CrateItem,
                Types.BoulderItem,
                Types.Key,
                Types.RainbowCoin,
                Types.Banana,
                Types.NintendoCoin,
                Types.RarewareCoin,
                Types.Enemies,
                Types.Crown,
                Types.Pearl,
                Types.Bean,
            )
            items_needing_ipd = (
                Types.Blueprint,
                Types.Hint,
                Types.Key,
                Types.ProgressiveHint,
                Types.Shockwave,
                Types.Shop,
                Types.Climbing,
                Types.TrainingBarrel,
            )
            if item.old_item in placed_items or item.location in helm_medals:
                if item.new_item in items_needing_ipd:
                    # Write item placement data
                    ipd = getItemPatchingData(item.new_item, item.new_subitem)
                    ipd_data.append([item.old_flag, ipd.level, ipd.kong])
            ref_index = 0
            if item.new_subitem == Items.ProgressiveAmmoBelt:
                ref_index = item.new_flag - 0x292
            elif item.new_subitem == Items.ProgressiveInstrumentUpgrade:
                ref_index = item.new_flag - 0x294
            elif item.new_subitem == Items.ProgressiveSlam:
                ref_index = item.new_flag - 0x3BC
            setItemReferenceName(spoiler, item.new_subitem, ref_index, spoiler.LocationList[item.location].name, item.old_flag)
            # Handle pre-given shops, only ran into if shop owners are in the pool
            if item.old_item in shop_owner_types:
                if pregiven_shop_owners is None:
                    pregiven_shop_owners = []
                if item.new_item in shop_owner_types:
                    pregiven_shop_owners.append(item.new_item)
                elif item.new_item != Items.NoItem and item.new_item is not None:
                    raise Exception(f"Invalid item {item.new_subitem.name} placed in shopkeeper slot. This shouldn't happen.")
        # Patch pre-given shops
        if pregiven_shop_owners is not None:  # Shop owners in pool
            data = 0
            or_data = {
                Types.Cranky: 0x80,
                Types.Funky: 0x40,
                Types.Candy: 0x20,
                Types.Snide: 0x10,
            }
            for x in or_data:
                if x not in spoiler.settings.shuffled_location_types:
                    data |= or_data[x]
            for x in pregiven_shop_owners:
                data |= or_data[x]
            ROM_COPY.seek(sav + 0x1EC)
            ROM_COPY.writeMultipleBytes(data, 1)
        # Text stuff
        if spoiler.settings.item_reward_previews:
            for textbox in textboxes:
                new_item = textbox.default_type
                new_subitem = textbox.default_item
                flag = 379  # Rareware Coin flag for RW Coin textbox
                for item in item_data:
                    if textbox.location == item.location:
                        new_item = item.new_item
                        new_subitem = item.new_subitem
                        flag = item.new_flag
                replacement = textbox.replacement_text
                if not textbox.force_pipe:
                    reward_text = getItemPreviewText(new_item, textbox.location, THEMATIC_TEXT, getModelMask(new_subitem))
                    replacement = replacement.replace("|", reward_text)
                data = {
                    "textbox_index": textbox.textbox_index,
                    "mode": "replace",
                    "search": textbox.text_replace,
                    "target": replacement,
                }
                if textbox.file_index in spoiler.text_changes:
                    spoiler.text_changes[textbox.file_index].append(data)
                else:
                    spoiler.text_changes[textbox.file_index] = [data]
            beetle_data = {
                Locations.AztecTinyBeetleRace: "aztec_beetle",
                Locations.CavesLankyBeetleRace: "caves_beetle",
            }
            beetle_locations = list(beetle_data.keys())
            for item in item_data:
                if item.location in beetle_locations:
                    VERSION_STRING_START = getSym(beetle_data[item.location])
                    addr = getROMAddress(VERSION_STRING_START, Overlay.Custom, offset_dict)
                    item_text = getItemPreviewText(item.new_item, item.location, THEMATIC_TEXT, getModelMask(new_subitem))
                    ROM_COPY.seek(addr)
                    ROM_COPY.writeBytes(bytes(f"{item_text}\0", "ascii"))
            minor_item = "\x05FOR A FOOLISH GAME\x05"
            major_item = "\x04FOR SOMETHING YOU MIGHT NEED ON YOUR QUEST\x04"
            if 8 not in spoiler.text_changes:
                spoiler.text_changes[8] = []
            major_items = spoiler.majorItems
            new_item = Items.RarewareCoin
            for item in item_data:
                if item.location == Locations.RarewareCoin:
                    new_item = item.new_subitem
            placed_text = major_item if new_item in major_items else minor_item
            spoiler.text_changes[8].append({"textbox_index": 0, "mode": "replace", "search": "FOR MY AMAZING SURPRISE", "target": placed_text})

        # Terminate IPD
        ipd_data.append([0xFFFF, 0xFF, 0xFF])
        ROM_COPY.seek(POINTER_ROM_IPDTABLE)
        for ipd_info in sorted(ipd_data, key=lambda x: x[0]):
            ROM_COPY.writeMultipleBytes(ipd_info[0], 2)
            ROM_COPY.writeMultipleBytes(ipd_info[1], 1)
            ROM_COPY.writeMultipleBytes(ipd_info[2], 1)
        # Setup Changes
        for map_id in map_items:
            cont_map_setup_address = getPointerLocation(TableNames.Setups, map_id)
            ROM_COPY.seek(cont_map_setup_address)
            model2_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
            for item in range(model2_count):
                start = cont_map_setup_address + 4 + (item * 0x30)
                ROM_COPY.seek(start + 0x2A)
                item_id = int.from_bytes(ROM_COPY.readBytes(2), "big")
                for item_slot in map_items[map_id]:
                    if item_slot["id"] == item_id:
                        ROM_COPY.seek(start + 0x28)
                        old_item = int.from_bytes(ROM_COPY.readBytes(2), "big")
                        if old_item in model_two_items:
                            ROM_COPY.seek(start + 0x28)
                            item_obj_index = getPropFromItem(item_slot["subitem"], item_slot["obj"], item_slot["flag"], item_slot["shared"])
                            ROM_COPY.writeMultipleBytes(item_obj_index, 2)
                            # Scaling fix
                            ROM_COPY.seek(start + 0xC)
                            old_scale = intf_to_float(int.from_bytes(ROM_COPY.readBytes(4), "big"))
                            new_scale = old_scale * item_slot["upscale"]
                            ROM_COPY.seek(start + 0xC)
                            ROM_COPY.writeFloat(new_scale)
