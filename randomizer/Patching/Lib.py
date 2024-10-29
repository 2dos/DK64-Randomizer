"""Library functions for patching."""

from __future__ import annotations

import struct
from enum import IntEnum, auto
from typing import TYPE_CHECKING, Any, Dict, List, Tuple, Union

import js
import random
import zlib
import gzip
from randomizer.Enums.ScriptTypes import ScriptTypes
from randomizer.Patching.Patcher import ROM, LocalROM
from randomizer.Enums.Items import Items
from randomizer.Enums.Enemies import Enemies
from randomizer.Enums.Maps import Maps
from randomizer.Enums.Types import BarrierItems, Types
from randomizer.Enums.Settings import HardModeSelected, MiscChangesSelected, HelmDoorItem, IceTrapFrequency

if TYPE_CHECKING:
    from randomizer.Lists.MapsAndExits import Maps

icon_db = {
    0x0: "waterfall_tall",
    0x1: "waterfall_short",
    0x2: "water",
    0x3: "lava",
    0x4: "sparkles",
    0x5: "pop_explosion",
    0x6: "lava_explosion",
    0x7: "green_leaf?",
    0x8: "brown_smoke_explosion",
    0x9: "small_explosion",
    0xA: "solar_flare?",
    0xB: "splash",
    0xC: "bubble",
    0xD: "purple_sparkle",
    0xE: "yellow_sparkle",
    0xF: "green_sparkle",
    0x10: "purple_sparkle",
    0x11: "yellow_sparkle",
    0x12: "green_sparkle",
    0x13: "large_smoke_explosion",
    0x14: "pink_implosion",
    0x15: "brown_horizontal_spinning_plank",
    0x16: "birch_horizontal_spinning_plank",
    0x17: "brown_vertical_spinning_plank",
    0x18: "star_water_ripple",
    0x19: "circle_water_ripple",
    0x1A: "small_smoke_explosion",
    0x1B: "static_star",
    0x1C: "static_z",
    0x1D: "white_flare?",
    0x1E: "static_rain?",
    0x1F: "medium_smoke_explosion",
    0x20: "bouncing_melon",
    0x21: "vertical_rolling_melon",
    0x22: "red_flare?",
    0x23: "sparks",
    0x24: "peanut",
    0x25: "star_flare?",
    0x26: "peanut_shell",
    0x27: "small_explosion",
    0x28: "large_smoke_implosion",
    0x29: "blue_lazer",
    0x2A: "pineapple",
    0x2B: "fireball",
    0x2C: "orange",
    0x2D: "grape",
    0x2E: "grape_splatter",
    0x2F: "tnt_sparkle",
    0x30: "fire_explosion",
    0x31: "small_fireball",
    0x32: "diddy_coin",
    0x33: "chunky_coin",
    0x34: "lanky_coin",
    0x35: "dk_coin",
    0x36: "tiny_coin",
    0x37: "dk_coloured_banana",
    0x38: "film",
    0x39: "bouncing_orange",
    0x3A: "crystal_coconut",
    0x3B: "gb",
    0x3C: "banana_medal",
    0x3D: "diddy_coloured_banana",
    0x3E: "chunky_coloured_banana",
    0x3F: "lanky_coloured_banana",
    0x40: "dk_coloured_banana",
    0x41: "tiny_coloured_banana",
    0x42: "exploded_krash_barrel_enemy",
    0x43: "white_explosion_thing",
    0x44: "coconut",
    0x45: "coconut_shell",
    0x46: "spinning_watermelon_slice",
    0x47: "tooth",
    0x48: "ammo_crate",
    0x49: "race_coin",
    0x4A: "lanky_bp",
    0x4B: "cannonball",
    0x4C: "crystal_coconut",
    0x4D: "feather",
    0x4E: "guitar_gazump",
    0x4F: "bongo_blast",
    0x50: "saxophone",
    0x51: "triangle",
    0x52: "trombone",
    0x53: "waving_yellow_double_eighth_note",
    0x54: "waving_yellow_single_eighth_note",
    0x55: "waving_green_single_eighth_note",
    0x56: "waving_purple_double_eighth_note",
    0x57: "waving_red_double_eighth_note",
    0x58: "waving_red_single_eighth_note",
    0x59: "waving_white_double_eighth_note",
    0x5A: "diddy_bp",
    0x5B: "chunky_bp",
    0x5C: "dk_bp",
    0x5D: "tiny_bp",
    0x5E: "spinning_sparkle",
    0x5F: "static_rain?",
    0x60: "translucent_water",
    0x61: "unk61",
    0x62: "black_screen",
    0x63: "white_cloud",
    0x64: "thin_lazer",
    0x65: "blue_bubble",
    0x66: "white_faded_circle",
    0x67: "white_circle",
    0x68: "grape_particle?",
    0x69: "spinning_blue_sparkle",
    0x6A: "white_smoke_explosion",
    0x6B: "l-r_joystick",
    0x6C: "fire_wall",
    0x6D: "static_rain_bubble",
    0x6E: "a_button",
    0x6F: "b_button",
    0x70: "z_button",
    0x71: "c_down_button",
    0x72: "c_up_button",
    0x73: "c_left_button",
    0x74: "acid",
    0x75: "acid_explosion",
    0x76: "race_hoop",
    0x77: "acid_goop?",
    0x78: "unk78",
    0x79: "broken_bridge?",
    0x7A: "white_pole?",
    0x7B: "bridge_chip?",
    0x7C: "wooden_beam_with_rivets",
    0x7D: "chunky_bunch",
    0x7E: "diddy_bunch",
    0x7F: "lanky_bunch",
    0x80: "dk_bunch",
    0x81: "tiny_bunch",
    0x82: "chunky_balloon",
    0x83: "diddy_balloon",
    0x84: "dk_balloon",
    0x85: "lanky_balloon",
    0x86: "tiny_balloon",
    0x87: "r_button",
    0x88: "l_button",
    0x89: "fairy",
    0x8A: "boss_key",
    0x8B: "crown",
    0x8C: "rareware_coin",
    0x8D: "nintendo_coin",
    0x8E: "no_symbol",
    0x8F: "headphones",
    0x90: "opaque_blue_water",
    0x91: "start_button",
    0x92: "white_question_mark",
    0x93: "candy_face",
    0x94: "cranky_face",
    0x95: "snide_face",
    0x96: "funky_face",
    0x97: "left_arrow",
    0x98: "white_spark?",
    0x99: "black_boulder_chunk",
    0x9A: "green_boulder_chunk",
    0x9B: "wood_chip",
    0x9C: "snowflake/dandelion",
    0x9D: "static_water?",
    0x9E: "spinning_leaf",
    0x9F: "flashing_water?",
    0xA0: "rainbow_coin",
    0xA1: "shockwave_orange_particle",
    0xA2: "implosion?",
    0xA3: "rareware_employee_face",
    0xA4: "smoke",
    0xA5: "static_smoke?",
    0xA6: "barrel_bottom_chunk",
    0xA7: "scoff_face",
    0xA8: "multicoloured_bunch",
    0xA9: "dk_face",
    0xAA: "diddy_face",
    0xAB: "lanky_face",
    0xAC: "tiny_face",
    0xAD: "chunky_face",
    0xAE: "fairy_tick",
    0xAF: "wrinkly",
}


class MenuTextDim(IntEnum):
    """Definition of base size of image."""

    size_w32_h32 = auto()
    size_w32_h64 = auto()
    size_w64_h32 = auto()


class MenuTexture:
    """Class to store information regarding a texture compatible with the main menu background."""

    def __init__(self, name: str, dim: MenuTextDim, table: int = 25, weight: int = 100, is_color: bool = False):
        """Initialize with given parameters."""
        self.name = name
        self.dim = dim
        self.table = table
        self.weight = weight
        self.is_color = is_color


class CustomActors(IntEnum):
    """Custom Actors Enum."""

    NintendoCoin = 0x8000  # Starts at 0x8000
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
    HintItem = auto()
    KopDummy = auto()


compatible_background_textures = {
    0x47A: MenuTexture("Gold Tower Stack", MenuTextDim.size_w32_h64),
    0x9DD: MenuTexture("Book", MenuTextDim.size_w32_h64),
    0x5C8: MenuTexture("Bricks", MenuTextDim.size_w32_h64),
    0x76F: MenuTexture("Bricks", MenuTextDim.size_w32_h64),
    0xAAF: MenuTexture("Floodlights", MenuTextDim.size_w32_h64),
    0x33D: MenuTexture("Wooden Board", MenuTextDim.size_w32_h64),
    0x79C: MenuTexture("Grassy Brick", MenuTextDim.size_w32_h64),
    0x992: MenuTexture("Wooden Door", MenuTextDim.size_w32_h64),
    0x39B: MenuTexture("C Block", MenuTextDim.size_w32_h32, 25, 7),
    0x39C: MenuTexture("G Block", MenuTextDim.size_w32_h32, 25, 7),
    0x39D: MenuTexture("9 Block", MenuTextDim.size_w32_h32, 25, 7),
    0x39F: MenuTexture("R Block", MenuTextDim.size_w32_h32, 25, 7),
    0x3A0: MenuTexture("S Block", MenuTextDim.size_w32_h32, 25, 7),
    0x3A1: MenuTexture("1 Block", MenuTextDim.size_w32_h32, 25, 7),
    0x3A2: MenuTexture("F Block", MenuTextDim.size_w32_h32, 25, 7),
    0x3A3: MenuTexture("8 Block", MenuTextDim.size_w32_h32, 25, 7),
    0x3A4: MenuTexture("7 Block", MenuTextDim.size_w32_h32, 25, 7),
    0x3A5: MenuTexture("B Block", MenuTextDim.size_w32_h32, 25, 7),
    0x3A6: MenuTexture("4 Block", MenuTextDim.size_w32_h32, 25, 7),
    0x3A7: MenuTexture("N Block", MenuTextDim.size_w32_h32, 25, 7),
    0x3A8: MenuTexture("D Block", MenuTextDim.size_w32_h32, 25, 7),
    0x3A9: MenuTexture("Q Block", MenuTextDim.size_w32_h32, 25, 7),
    0x7B2: MenuTexture("Up Arrow", MenuTextDim.size_w32_h32, 25, 50),
    0x7B3: MenuTexture("Down Arrow", MenuTextDim.size_w32_h32, 25, 50),
    0xAC: MenuTexture("TNT", MenuTextDim.size_w32_h32),
    0x7CD: MenuTexture("Night Sign", MenuTextDim.size_w32_h32),
    0x3DE: MenuTexture("Color", MenuTextDim.size_w32_h32, 7, 50, True),
    0xF7: MenuTexture("Grass", MenuTextDim.size_w32_h32),
    0xA00: MenuTexture("Sand", MenuTextDim.size_w32_h32),
    0xA84: MenuTexture("Sand", MenuTextDim.size_w32_h32),
    0xB4D: MenuTexture("Leaf", MenuTextDim.size_w32_h32),
    0xB19: MenuTexture("Boxes", MenuTextDim.size_w32_h32),
    0xB24: MenuTexture("Pineapple Switch", MenuTextDim.size_w32_h32),
    0xB25: MenuTexture("Coconut Switch", MenuTextDim.size_w32_h32),
    0xB1E: MenuTexture("Peanut Switch", MenuTextDim.size_w32_h32),
    0xC80: MenuTexture("Feather Switch", MenuTextDim.size_w32_h32),
    0xC81: MenuTexture("Grape Switch", MenuTextDim.size_w32_h32),
    # 0xB27: MenuTexture("Boxes", MenuTextDim.size_w32_h32),
    0xCF1: MenuTexture("L Square", MenuTextDim.size_w32_h32),
    0xCF4: MenuTexture("R Square", MenuTextDim.size_w32_h32),
    0xE63: MenuTexture("Metallic Green", MenuTextDim.size_w32_h32),
    0x9F3: MenuTexture("Watery Blue", MenuTextDim.size_w32_h32),
    0x9F4: MenuTexture("Watery Yellow", MenuTextDim.size_w32_h32),
    0x83: MenuTexture("Beige Strips", MenuTextDim.size_w32_h32),
    0x788: MenuTexture("Beige Panels", MenuTextDim.size_w32_h32),
    0x789: MenuTexture("Blue Panels", MenuTextDim.size_w32_h32),
    0x792: MenuTexture("White Granite", MenuTextDim.size_w32_h32),
    0x1258: MenuTexture("Horizontal Metal Green", MenuTextDim.size_w32_h32),
    0x1260: MenuTexture("Red Light", MenuTextDim.size_w32_h32),
    0x1343: MenuTexture("Fluid Red", MenuTextDim.size_w32_h32),
    0x1344: MenuTexture("Fluid Green", MenuTextDim.size_w32_h32),
    0x1347: MenuTexture("Fluid Orange", MenuTextDim.size_w32_h32),
    0x1348: MenuTexture("Fluid Blue", MenuTextDim.size_w32_h32),
    0xCC: MenuTexture("Bathroom Wall", MenuTextDim.size_w32_h64),
    0xCD5: MenuTexture("Orange Barrel", MenuTextDim.size_w32_h64),
    0xCD6: MenuTexture("Green Barrel", MenuTextDim.size_w32_h64),
    0xCD7: MenuTexture("Purple Barrel", MenuTextDim.size_w32_h64),
    0xCD8: MenuTexture("Yellow Barrel", MenuTextDim.size_w32_h64),
    0xCD9: MenuTexture("Blue Barrel", MenuTextDim.size_w32_h64),
    0xCDA: MenuTexture("Red Barrel", MenuTextDim.size_w32_h64),
    0xE3A: MenuTexture("Light Fixing", MenuTextDim.size_w32_h64),
    0x8F5: MenuTexture("Metal Pillars", MenuTextDim.size_w32_h64),
    0x786: MenuTexture("Just Straight Dirt", MenuTextDim.size_w32_h64),
    0x1257: MenuTexture("Copper", MenuTextDim.size_w32_h64),
    # 0xC: MenuTexture("Shelf of Bananas", MenuTextDim.size_w64_h32),
    # 0xD: MenuTexture("Shelf of Books", MenuTextDim.size_w64_h32),
    # 0xE: MenuTexture("Shelf of Wine", MenuTextDim.size_w64_h32),
    0xA8F: MenuTexture("Grime Panels", MenuTextDim.size_w64_h32),
    0xA43: MenuTexture("Books", MenuTextDim.size_w64_h32),
    0xA53: MenuTexture("Dolphins", MenuTextDim.size_w64_h32),
    0xA70: MenuTexture("Way Out Sign", MenuTextDim.size_w64_h32),
    0xA72: MenuTexture("Banana Hoard Sign", MenuTextDim.size_w64_h32),
    0xA73: MenuTexture("Training Area Sign", MenuTextDim.size_w64_h32),
    0xA74: MenuTexture("Cranky's Lab Sign", MenuTextDim.size_w64_h32),
    # 0xA76: MenuTexture("DK's Sign", MenuTextDim.size_w64_h32),
    0xC14: MenuTexture("No Admittance Sign", MenuTextDim.size_w64_h32),
    0xC47: MenuTexture("Danger Sign", MenuTextDim.size_w64_h32),
    0xC64: MenuTexture("Accept Sign", MenuTextDim.size_w64_h32),
    0xCCF: MenuTexture("A Sign", MenuTextDim.size_w64_h32, 25, 7),
    0xCD0: MenuTexture("B Sign", MenuTextDim.size_w64_h32, 25, 7),
    0xCD1: MenuTexture("C Sign", MenuTextDim.size_w64_h32, 25, 7),
    0xCD2: MenuTexture("D Sign", MenuTextDim.size_w64_h32, 25, 7),
    0xCD3: MenuTexture("E Sign", MenuTextDim.size_w64_h32, 25, 7),
    0xCD4: MenuTexture("F Sign", MenuTextDim.size_w64_h32, 25, 7),
    0xD3C: MenuTexture("Blessed", MenuTextDim.size_w64_h32),  # Beans
    0x8DA: MenuTexture("Museum Sign", MenuTextDim.size_w64_h32),
    0x8DB: MenuTexture("Ballroom Sign", MenuTextDim.size_w64_h32),
    0x8DE: MenuTexture("Library Sign", MenuTextDim.size_w64_h32),
    0x9DA: MenuTexture("Library Wall", MenuTextDim.size_w64_h32),
    0x79A: MenuTexture("Minecart Tracks", MenuTextDim.size_w64_h32),
    0x339: MenuTexture("Piano Keys", MenuTextDim.size_w64_h32),
    0x398: MenuTexture("4 and B Blocks", MenuTextDim.size_w64_h32, 25, 7),
    0x399: MenuTexture("C and Z Blocks", MenuTextDim.size_w64_h32, 25, 7),
    0x902: MenuTexture("Carpet", MenuTextDim.size_w64_h32),
}


class HelmDoorRandomInfo:
    """Store information regarding helm door random boundaries."""

    def __init__(self, min_bound: int, max_bound: int, selection_weight: float):
        """Initialize with given parameters."""
        self.min_bound = min_bound
        self.max_bound = max_bound
        self.selection_weight = selection_weight
        self.selected_amount = None

    def chooseAmount(self) -> int:
        """Choose amount for the helm door."""
        raw_float = random.triangular(self.min_bound, self.max_bound)
        self.selected_amount = round(raw_float)
        return self.selected_amount


class HelmDoorInfo:
    """Store information about helm door requirements."""

    def __init__(self, absolute_max: int, hard: HelmDoorRandomInfo = None, medium: HelmDoorRandomInfo = None, easy: HelmDoorRandomInfo = None):
        """Initialize with given parameters."""
        self.absolute_max = absolute_max
        self.hard = hard
        self.medium = medium
        self.easy = easy

    def getDifficultyInfo(self, difficulty: int) -> HelmDoorRandomInfo:
        """Get the random info pertaining to the difficulty."""
        if difficulty == 0:
            return self.easy
        if difficulty == 1:
            return self.medium
        if difficulty == 2:
            return self.hard
        return None


class PaletteFillType(IntEnum):
    """Palette Fill Type enum."""

    block = auto()
    patch = auto()
    sparkle = auto()
    checkered = auto()
    radial = auto()
    kong = auto()


class Overlay(IntEnum):
    """Overlay enum."""

    Boot = 0
    Static = 1
    Menu = 2
    Multiplayer = 3
    Minecart = 4
    Race = 5
    Critter = 6
    Boss = 7
    Bonus = 8
    Arcade = 9
    Jetpac = 10
    Custom = 11  # Fake overlay used for patching


def float_to_hex(f: Union[float, int]) -> str:
    """Convert float to hex."""
    if f == 0:
        return "0x00000000"
    return hex(struct.unpack("<I", struct.pack("<f", f))[0])


def short_to_ushort(short: int) -> int:
    """Convert short to unsigned short format."""
    if short < 0:
        return short + 65536
    return short


def intf_to_float(intf: int) -> float:
    """Convert float as int format to float."""
    if intf == 0:
        return 0
    else:
        return struct.unpack("!f", bytes.fromhex("{:08X}".format(intf)))[0]


def ushort_to_short(ushort):
    """Convert unsigned short to signed short."""
    if ushort > 32767:
        return ushort - 65536
    return ushort


def int_to_list(num: int, size: int):
    """Convert an integer to a list."""
    arr = [0] * size
    for a in range(size):
        slot = (size - 1) - a
        val = num % 256
        num = int((num - val) / 256)
        arr[slot] = val
    return arr


def getNextFreeID(cont_map_id: Union[Maps, int], ignore: List[Union[Any, int]] = []) -> int:
    """Get next available Model 2 ID."""
    ROM_COPY = LocalROM()
    setup_table = js.pointer_addresses[9]["entries"][cont_map_id]["pointing_to"]
    ROM_COPY.seek(setup_table)
    model2_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
    vacant_ids = list(range(0, 600))
    for item in range(model2_count):
        item_start = setup_table + 4 + (item * 0x30)
        ROM_COPY.seek(item_start + 0x2A)
        item_id = int.from_bytes(ROM_COPY.readBytes(2), "big")
        if item_id in vacant_ids:
            vacant_ids.remove(item_id)
    for id in range(0x220, 0x225):
        if id in vacant_ids:
            vacant_ids.remove(id)
    for id in ignore:
        if id in vacant_ids:
            vacant_ids.remove(id)
    if len(vacant_ids) > 0:
        return min(vacant_ids)
    return 0  # Shouldn't ever hit this. This is a case if there's no vacant IDs in range [0,599]


def addNewScript(cont_map_id: Union[Maps, int], item_ids: List[int], type: ScriptTypes) -> None:
    """Append a new script to the script database. Has to be just 1 execution and 1 endblock."""
    ROM_COPY = LocalROM()
    script_table = js.pointer_addresses[10]["entries"][cont_map_id]["pointing_to"]
    ROM_COPY.seek(script_table)
    script_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
    good_scripts = []
    # Construct good pre-existing scripts
    file_offset = 2
    for script_item in range(script_count):
        ROM_COPY.seek(script_table + file_offset)
        script_start = script_table + file_offset
        script_id = int.from_bytes(ROM_COPY.readBytes(2), "big")
        block_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
        file_offset += 6
        for block_item in range(block_count):
            ROM_COPY.seek(script_table + file_offset)
            cond_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
            file_offset += 2 + (8 * cond_count)
            ROM_COPY.seek(script_table + file_offset)
            exec_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
            file_offset += 2 + (8 * exec_count)
        script_end = script_table + file_offset
        if script_id not in item_ids:
            script_data = []
            ROM_COPY.seek(script_start)
            for x in range(int((script_end - script_start) / 2)):
                script_data.append(int.from_bytes(ROM_COPY.readBytes(2), "big"))
            good_scripts.append(script_data)
    # Get new script data
    subscript_type = -100
    if type == ScriptTypes.Bananaport:
        subscript_type = -1
    elif type == ScriptTypes.Wrinkly:
        subscript_type = -2
    elif type == ScriptTypes.TnsPortal:
        subscript_type = -3
    elif type == ScriptTypes.TnsIndicator:
        subscript_type = -4
    elif type == ScriptTypes.CrownMain:
        subscript_type = -5
    elif type == ScriptTypes.CrownIsles2:
        subscript_type = -6
    elif type == ScriptTypes.MelonCrate:
        subscript_type = -13
    elif type == ScriptTypes.DeleteItem:
        subscript_type = -16
    for item_id in item_ids:
        script_arr = [
            item_id,
            1,  # Block Count
            0,  # Behav 9C, Not sure the purpose on this. 0 seems safe from prior knowledge
            0,  # Cond Count
            1,  # Exec Count
            7,  # Func Type (Run JALR)
            125,  # JALR Type (Points to our custom code)
            short_to_ushort(subscript_type),  # Subscript Type
            item_id,  # Item ID, for the purpose of our script to locate any required data
        ]
        good_scripts.append(script_arr)
    # Reconstruct File
    ROM_COPY.seek(script_table)
    ROM_COPY.writeMultipleBytes(len(good_scripts), 2)
    for script in good_scripts:
        for x in script:
            ROM_COPY.writeMultipleBytes(x, 2)


def grabText(file_index: int, cosmetic: bool = False) -> List[List[Dict[str, List[str]]]]:
    """Pull text from ROM with a particular file index."""
    if cosmetic:
        ROM_COPY = ROM()
    else:
        ROM_COPY = LocalROM()
    file_start = js.pointer_addresses[12]["entries"][file_index]["pointing_to"]
    ROM_COPY.seek(file_start + 0)
    count = int.from_bytes(ROM_COPY.readBytes(1), "big")
    text = []
    text_data = []
    text_start = (count * 0xF) + 3
    data_start = 1
    for i in range(count):
        ROM_COPY.seek(file_start + data_start)
        section_1_count = int.from_bytes(ROM_COPY.readBytes(1), "big")
        section_2_count = int.from_bytes(ROM_COPY.readBytes(1), "big")
        section_3_count = int.from_bytes(ROM_COPY.readBytes(1), "big")
        ROM_COPY.seek(file_start + data_start + 5)
        start = int.from_bytes(ROM_COPY.readBytes(2), "big")
        int.from_bytes(ROM_COPY.readBytes(2), "big")
        block_start = 1
        blocks = []
        for k in range(section_1_count):
            ROM_COPY.seek(file_start + data_start + block_start)
            sec2ct = int.from_bytes(ROM_COPY.readBytes(1), "big")
            offset = 0
            if (sec2ct & 4) != 0:
                offset += 4
            text_blocks = []
            if (sec2ct & 1) == 0:
                if (sec2ct & 2) != 0:
                    ROM_COPY.seek(file_start + data_start + block_start + offset + 1)
                    sec3ct = int.from_bytes(ROM_COPY.readBytes(1), "big")
                    for j in range(sec3ct):
                        _block = block_start + 2 + offset + (4 * j) - 1
                        ROM_COPY.seek(file_start + data_start + _block)
                        _pos = int.from_bytes(ROM_COPY.readBytes(2), "big")
                        ROM_COPY.seek(file_start + data_start + _block)
                        _dat = int.from_bytes(ROM_COPY.readBytes(4), "big")
                        text_blocks.append({"type": "sprite", "position": _pos, "data": hex(_dat), "sprite": icon_db[(_dat >> 8) & 0xFF]})
                    added = block_start + 2 + offset + (4 * sec3ct) + 4
            else:
                ROM_COPY.seek(file_start + data_start + block_start + offset + 1)
                sec3ct = int.from_bytes(ROM_COPY.readBytes(1), "big")
                for j in range(sec3ct):
                    _block = block_start + 2 + offset + (8 * j) - 1
                    ROM_COPY.seek(file_start + data_start + _block + 3)
                    _start = int.from_bytes(ROM_COPY.readBytes(2), "big")
                    ROM_COPY.seek(file_start + data_start + _block + 5)
                    _size = int.from_bytes(ROM_COPY.readBytes(2), "big")
                    text_blocks.append({"type": "normal", "start": _start, "size": _size})
                added = block_start + 2 + offset + (8 * sec3ct) + 4
            # print(f"File {file_index}, Textbox {i}, section {k}")
            blocks.append({"block_start": hex(block_start + data_start), "section2count": sec2ct, "section3count": sec3ct, "offset": offset, "text": text_blocks})
            block_start = added
        ROM_COPY.seek(file_start + data_start)
        if added < data_start:
            info = b""
        else:
            info = ROM_COPY.readBytes(added - data_start)
        text_data.append({"arr": info, "text": blocks, "section1count": section_1_count, "section2count": section_2_count, "section3count": section_3_count, "data_start": hex(data_start)})
        text_start += added - data_start
        data_start += block_start
    for item in text_data:
        text_block = []
        # print(item)
        for item2 in item["text"]:
            # print(item2)
            temp = []
            for item3 in item2["text"]:
                if item3["type"] == "normal":
                    start = item3["start"] + data_start + 2
                    # print(hex(start))
                    start + item3["size"]
                    ROM_COPY.seek(file_start + start)
                    temp.append(ROM_COPY.readBytes(item3["size"]).decode())
                elif item3["type"] == "sprite":
                    temp.append(item3["sprite"])
                    # print(fh.read(item3["size"]))
            text_block.append(temp)
        text.append(text_block)
    formatted_text = []
    for t in text:
        y = []
        for x in t:
            y.append({"text": x})
        formatted_text.append(y)
    return formatted_text


def writeText(file_index: int, text: List[Union[List[Dict[str, List[str]]], Tuple[Dict[str, List[str]]]]], cosmetic: bool = False) -> None:
    """Write the text to ROM."""
    text_start = js.pointer_addresses[12]["entries"][file_index]["pointing_to"]
    if cosmetic:
        ROM_COPY = ROM()
    else:
        ROM_COPY = LocalROM()
    ROM_COPY.seek(text_start)
    ROM_COPY.writeBytes(bytearray([len(text)]))
    position = 0
    for textbox in text:
        ROM_COPY.writeBytes(len(textbox).to_bytes(1, "big"))
        for block in textbox:
            # Get Icon State
            icon_id = -1
            for string in block["text"]:
                if string in icon_db.values():
                    for icon in icon_db:
                        if icon_db[icon] == string:
                            icon_id = icon
            if icon_id > -1:
                ROM_COPY.writeBytes(bytearray([2, 1]))
                ROM_COPY.writeBytes(icon_id.to_bytes(2, "big"))
                ROM_COPY.writeBytes(bytearray([0, 0]))
            else:
                ROM_COPY.writeBytes(bytearray([1, len(block["text"])]))
                for string in block["text"]:
                    ROM_COPY.writeBytes(position.to_bytes(4, "big"))
                    ROM_COPY.writeBytes(len(string).to_bytes(2, "big"))
                    ROM_COPY.writeBytes(bytearray([0, 0]))
                    position += len(string)
            unk0 = 0
            if "unk0" in block:
                unk0 = block["unk0"]
            ROM_COPY.writeBytes(int(float_to_hex(unk0), 16).to_bytes(4, "big"))
    ROM_COPY.writeBytes(bytearray(position.to_bytes(2, "big")))
    for textbox in text:
        for block in textbox:
            is_icon = False
            for string in block["text"]:
                if string in icon_db.values():
                    is_icon = True
            if not is_icon:
                for string in block["text"]:
                    ROM_COPY.writeBytes(string.encode("ascii"))


def getObjectAddress(map: int, id: int, object_type: str) -> int:
    """Get address of object in setup."""
    setup_start = js.pointer_addresses[9]["entries"][map]["pointing_to"]
    ROM_COPY = LocalROM()
    ROM_COPY.seek(setup_start)
    model_2_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
    if object_type == "modeltwo":
        for item in range(model_2_count):
            item_start = setup_start + 4 + (item * 0x30)
            ROM_COPY.seek(item_start + 0x2A)
            if int.from_bytes(ROM_COPY.readBytes(2), "big") == id:
                return item_start
    mystery_start = setup_start + 4 + (0x30 * model_2_count)
    ROM_COPY.seek(mystery_start)
    mystery_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
    actor_start = mystery_start + 4 + (0x24 * mystery_count)
    ROM_COPY.seek(actor_start)
    actor_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
    if object_type == "actor":
        for item in range(actor_count):
            item_start = actor_start + 4 + (item * 0x38)
            ROM_COPY.seek(item_start + 0x34)
            if int.from_bytes(ROM_COPY.readBytes(2), "big") == id:
                return item_start
    return None


def getObjectAddressBrowser(map: int, id: int, object_type: str) -> int:
    """Get address of object in setup."""
    setup_start = js.pointer_addresses[9]["entries"][map]["pointing_to"]
    ROM().seek(setup_start)
    model_2_count = int.from_bytes(ROM().readBytes(4), "big")
    if object_type == "modeltwo":
        for item in range(model_2_count):
            item_start = setup_start + 4 + (item * 0x30)
            ROM().seek(item_start + 0x2A)
            if int.from_bytes(ROM().readBytes(2), "big") == id:
                return item_start
    mystery_start = setup_start + 4 + (0x30 * model_2_count)
    ROM().seek(mystery_start)
    mystery_count = int.from_bytes(ROM().readBytes(4), "big")
    actor_start = mystery_start + 4 + (0x24 * mystery_count)
    ROM().seek(actor_start)
    actor_count = int.from_bytes(ROM().readBytes(4), "big")
    if object_type == "actor":
        for item in range(actor_count):
            item_start = actor_start + 4 + (item * 0x38)
            ROM().seek(item_start + 0x34)
            if int.from_bytes(ROM().readBytes(2), "big") == id:
                return item_start
    return None


def IsItemSelected(bool_setting: bool, multiselector_setting: List[Union[MiscChangesSelected, Any]], check: Union[HardModeSelected, MiscChangesSelected]) -> bool:
    """Determine whether a multiselector setting is enabled."""
    if not bool_setting:
        return False
    if len(multiselector_setting) == 0:
        return True
    return check in multiselector_setting


class SpawnerChange:
    """Information regarding a spawner change."""

    def __init__(self, map: Maps, spawner_id: int):
        """Initialize with given variables."""
        self.map_target = map
        self.spawner_target = spawner_id
        self.new_enemy = None
        self.new_scale = None
        self.new_speed_0 = None
        self.new_speed_1 = None


def applyCharacterSpawnerChanges(changes: list[SpawnerChange], fence_speed_factor: float = None):
    """Apply a series of changes to character spawners."""
    ROM_COPY = ROM()
    formatted_changes = {}
    id_changes_in_map = {}
    for change in changes:
        if change.map_target not in formatted_changes:
            formatted_changes[change.map_target] = {}
            id_changes_in_map[change.map_target] = []
        formatted_changes[change.map_target][change.spawner_target] = change
        id_changes_in_map[change.map_target].append(change.spawner_target)
    for map_id in formatted_changes:
        file_start = js.pointer_addresses[16]["entries"][map_id]["pointing_to"]
        ROM_COPY.seek(file_start)
        fence_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
        offset = 2
        used_fence_ids = []
        if fence_count > 0:
            for x in range(fence_count):
                fence = []
                fence_start = file_start + offset
                ROM_COPY.seek(file_start + offset)
                point_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
                offset += (point_count * 6) + 2
                ROM_COPY.seek(file_start + offset)
                point0_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
                if fence_speed_factor is not None:
                    for y in range(point0_count):
                        ROM_COPY.seek(file_start + offset + 2 + (y * 10) + 8)
                        old_value = int.from_bytes(ROM_COPY.readBytes(1), "big")
                        new_value = int(old_value * fence_speed_factor)
                        ROM_COPY.seek(file_start + offset + 2 + (y * 10) + 8)
                        ROM_COPY.write(new_value)
                offset += (point0_count * 10) + 6
                fence_finish = file_start + offset
                fence_size = fence_finish - fence_start
                ROM_COPY.seek(fence_finish - 4)
                used_fence_ids.append(int.from_bytes(ROM_COPY.readBytes(2), "big"))
                ROM_COPY.seek(fence_start)
                for y in range(int(fence_size / 2)):
                    fence.append(int.from_bytes(ROM_COPY.readBytes(2), "big"))
                ROM_COPY.seek(fence_finish)
        spawner_count_location = file_start + offset
        ROM_COPY.seek(spawner_count_location)
        spawner_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
        offset += 2
        for x in range(spawner_count):
            # Parse spawners
            ROM_COPY.seek(file_start + offset + 0x13)
            enemy_index = int.from_bytes(ROM_COPY.readBytes(1), "big")
            init_offset = offset
            if enemy_index in id_changes_in_map[map_id]:
                change_data = formatted_changes[map_id][enemy_index]
                if change_data.new_enemy is not None:
                    ROM_COPY.seek(file_start + init_offset)
                    ROM_COPY.write(change_data.new_enemy)
                if change_data.new_scale is not None:
                    ROM_COPY.seek(file_start + init_offset + 0xF)
                    ROM_COPY.write(change_data.new_scale)
                if change_data.new_speed_0 is not None:
                    ROM_COPY.seek(file_start + init_offset + 0xC)
                    ROM_COPY.write(change_data.new_speed_0)
                if change_data.new_speed_1 is not None:
                    ROM_COPY.seek(file_start + init_offset + 0xD)
                    ROM_COPY.write(change_data.new_speed_1)
            ROM_COPY.seek(file_start + offset + 0x11)
            extra_count = int.from_bytes(ROM_COPY.readBytes(1), "big")
            offset += 0x16 + (extra_count * 2)


def camelCaseToWords(string: str):
    """Convert camel case string to separated words."""
    words = [[string[0]]]

    for c in string[1:]:
        if words[-1][-1].islower() and c.isupper():
            words.append(list(c))
        else:
            words[-1].append(c)

    return " ".join(["".join(word) for word in words])


def getItemNumberString(count: int, item_type: Types) -> str:
    """Get a string which displays the number of items and the item name."""
    names = {
        Types.Banana: "Golden Banana",
        Types.BlueprintBanana: "Golden Banana",
        Types.Shop: "Move",
        Types.Blueprint: "Blueprint",
        Types.Fairy: "Fairy",
        Types.Key: "Key",
        Types.Crown: "Crown",
        Types.Coin: "Company Coin",
        Types.TrainingBarrel: "Move",
        Types.Climbing: "Move",
        Types.Kong: "Kong",
        Types.Medal: "Medal",
        Types.Shockwave: "Move",
        Types.Bean: "Bean",
        Types.Pearl: "Pearl",
        Types.RainbowCoin: "Rainbow Coin",
        Types.FakeItem: "Ice Trap",
        Types.ToughBanana: "Golden Banana",
        Types.JunkItem: "Junk Item",
        Types.Hint: "Hint",
        Types.PreGivenMove: "Move",
        Types.Climbing: "Move",
        Types.NintendoCoin: "Nintendo Coin",
        Types.RarewareCoin: "Rareware Coin",
        Types.Cranky: "Cranky",
        Types.Funky: "Funky",
        Types.Candy: "Candy",
        Types.Snide: "Snide",
        Types.IslesMedal: "Medal",
        Types.ProgressiveHint: "Hint",
    }
    name = names.get(item_type, item_type.name)
    if count != 1:
        name = f"{name}s"
        if item_type == Types.Fairy:
            name = "Fairies"
    return f"{count} {name}"


class TableNames(IntEnum):
    """Pointer Table Enum."""

    MusicMIDI = 0
    MapGeometry = auto()
    MapWalls = auto()
    MapFloors = auto()
    ModelTwoGeometry = auto()
    ActorGeometry = auto()
    Unknown6 = auto()
    TexturesUncompressed = auto()
    Cutscenes = auto()
    Setups = auto()
    InstanceScripts = auto()
    Animations = auto()
    Text = auto()
    Unknown13 = auto()
    TexturesHUD = auto()
    Paths = auto()
    Spawners = auto()
    DKTVInputs = auto()
    Triggers = auto()
    Unknown19 = auto()
    Unknown20 = auto()
    Autowalks = auto()
    Unknown22 = auto()
    Exits = auto()
    RaceCheckpoints = auto()
    TexturesGeometry = auto()
    UncompressedFileSizes = auto()
    Unknown27 = auto()
    Unknown28 = auto()
    Unknown29 = auto()
    Unknown30 = auto()
    Unknown31 = auto()


def recalculatePointerJSON(ROM_COPY: ROM):
    """Recalculates the pointer tables."""
    TABLE_COUNT = 32
    POINTER_OFFSET = 0x101C50
    new_data = [None] * TABLE_COUNT
    for x in range(TABLE_COUNT):
        ROM_COPY.seek(POINTER_OFFSET + ((TABLE_COUNT + x) << 2))
        table_data = {"entries": []}
        count = int.from_bytes(ROM_COPY.readBytes(4), "big")
        ROM_COPY.seek(POINTER_OFFSET + (x << 2))
        head = POINTER_OFFSET + int.from_bytes(ROM_COPY.readBytes(4), "big")
        for y in range(count):
            ROM_COPY.seek(head + (y << 2))
            local_data = {
                "index": y,
                "pointing_to": POINTER_OFFSET + int.from_bytes(ROM_COPY.readBytes(4), "big"),
            }
            next_file = POINTER_OFFSET + int.from_bytes(ROM_COPY.readBytes(4), "big")
            local_data["compressed_size"] = next_file - local_data["pointing_to"]
            table_data["entries"].append(local_data)
        new_data[x] = table_data
    js.pointer_addresses = new_data


def setItemReferenceName(spoiler, item: Items, index: int, new_name: str):
    """Set new name for a location of an item."""
    if item == Items.CameraAndShockwave:
        setItemReferenceName(spoiler, Items.Camera, index, new_name)
        setItemReferenceName(spoiler, Items.Shockwave, index, new_name)
    else:
        for loc in spoiler.location_references:
            if loc.item == item:
                loc.setLocation(index, new_name)


def DoorItemToBarrierItem(item: HelmDoorItem, is_coin_door: bool = False, is_crown_door: bool = False) -> BarrierItems:
    """Convert helm door item enum to barrier item enum."""
    if item == HelmDoorItem.vanilla:
        if is_coin_door:
            return BarrierItems.CompanyCoin
        elif is_crown_door:
            return BarrierItems.Crown
    converter = {
        HelmDoorItem.opened: BarrierItems.Nothing,
        HelmDoorItem.req_bean: BarrierItems.Bean,
        HelmDoorItem.req_bp: BarrierItems.Blueprint,
        HelmDoorItem.req_companycoins: BarrierItems.CompanyCoin,
        HelmDoorItem.req_crown: BarrierItems.Crown,
        HelmDoorItem.req_fairy: BarrierItems.Fairy,
        HelmDoorItem.req_gb: BarrierItems.GoldenBanana,
        HelmDoorItem.req_key: BarrierItems.Key,
        HelmDoorItem.req_medal: BarrierItems.Medal,
        HelmDoorItem.req_pearl: BarrierItems.Pearl,
        HelmDoorItem.req_rainbowcoin: BarrierItems.RainbowCoin,
    }
    return converter.get(item, BarrierItems.Nothing)


def getRawFile(table_index: int, file_index: int, compressed: bool):
    """Get raw file from ROM."""
    file_start = js.pointer_addresses[table_index]["entries"][file_index]["pointing_to"]
    file_end = js.pointer_addresses[table_index]["entries"][file_index + 1]["pointing_to"]
    file_size = file_end - file_start
    try:
        LocalROM().seek(file_start)
        data = LocalROM().readBytes(file_size)
    except Exception:
        ROM().seek(file_start)
        data = ROM().readBytes(file_size)
    if compressed:
        data = zlib.decompress(data, (15 + 32))
    return data


def writeRawFile(table_index: int, file_index: int, compressed: bool, data: bytearray, ROM_COPY):
    """Write raw file from ROM."""
    file_start = js.pointer_addresses[table_index]["entries"][file_index]["pointing_to"]
    file_end = js.pointer_addresses[table_index]["entries"][file_index + 1]["pointing_to"]
    file_size = file_end - file_start
    write_data = bytes(data)
    if compressed:
        write_data = gzip.compress(bytes(data), compresslevel=9)
    if len(write_data) > file_size:
        raise Exception(f"Cannot write file {file_index} in table {table_index} to ROM as it's too big.")
    ROM_COPY.seek(file_start)
    ROM_COPY.writeBytes(write_data)


def getIceTrapCount(settings) -> int:
    """Get the amount of Ice Traps the game will attempt to place."""
    ice_trap_freqs = {
        IceTrapFrequency.rare: 4,
        IceTrapFrequency.mild: 10,
        IceTrapFrequency.common: 32,
        IceTrapFrequency.frequent: 64,
        IceTrapFrequency.pain: 100,
    }
    return ice_trap_freqs.get(settings.ice_trap_frequency, 16)


class Holidays(IntEnum):
    """Holiday Enum."""

    no_holiday = 0
    Christmas = auto()
    Halloween = auto()
    Anniv25 = auto()


def getHolidaySetting(settings):
    """Get the holiday setting."""
    is_offseason = False
    if is_offseason:
        return settings.holiday_setting_offseason
    return settings.holiday_setting


def getHoliday(settings):
    """Get the holiday experienced."""
    if getHolidaySetting(settings):
        return Holidays.Halloween
    return Holidays.no_holiday


plando_colors = {
    "\x04": [
        "orange",
        "woth",
        "keys",
        "donkey",
        "aztec",
        "freekongs",
        "dogadon1",
    ],
    "\x05": [
        "red",
        "foolish",
        "diddy",
        "helm",
    ],
    "\x06": [
        "blue",
        "lanky",
        "galleon",
        "pufftoss",
    ],
    "\x07": [
        "purple",
        "tiny",
        "forest",
        "fungi",
        "dogadon2",
    ],
    "\x08": [
        "lightgreen",
        "chunky",
        "japes",
        "dillo1",
    ],
    "\x09": [
        "magenta",
        "castle",
        "kutout",
    ],
    "\x0a": [
        "cyan",
        "caves",
        "fridge",
        "dillo2",
    ],
    "\x0b": [
        "rust",
        "isles",
        "training",
    ],
    "\x0c": [
        "paleblue",
        "allkongs",
        "factory",
        "madjack",
    ],
    "\x0d": [
        "green",
        "jetpac",
    ],
}
