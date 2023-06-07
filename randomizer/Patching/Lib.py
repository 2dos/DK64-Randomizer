"""Library functions for patching."""
import struct
from enum import IntEnum, auto

import js
from randomizer.Enums.ScriptTypes import ScriptTypes
from randomizer.Patching.Patcher import ROM, LocalROM

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


def float_to_hex(f):
    """Convert float to hex."""
    if f == 0:
        return "0x00000000"
    return hex(struct.unpack("<I", struct.pack("<f", f))[0])


def short_to_ushort(short):
    """Convert short to unsigned short format."""
    if short < 0:
        return short + 65536
    return short


def intf_to_float(intf):
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


def getNextFreeID(cont_map_id: int, ignore=[]):
    """Get next available Model 2 ID."""
    setup_table = js.pointer_addresses[9]["entries"][cont_map_id]["pointing_to"]
    LocalROM().seek(setup_table)
    model2_count = int.from_bytes(LocalROM().readBytes(4), "big")
    vacant_ids = list(range(0, 600))
    for item in range(model2_count):
        item_start = setup_table + 4 + (item * 0x30)
        LocalROM().seek(item_start + 0x2A)
        item_id = int.from_bytes(LocalROM().readBytes(2), "big")
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


def addNewScript(cont_map_id: int, item_ids: list, type: ScriptTypes):
    """Append a new script to the script database. Has to be just 1 execution and 1 endblock."""
    script_table = js.pointer_addresses[10]["entries"][cont_map_id]["pointing_to"]
    LocalROM().seek(script_table)
    script_count = int.from_bytes(LocalROM().readBytes(2), "big")
    good_scripts = []
    # Construct good pre-existing scripts
    file_offset = 2
    for script_item in range(script_count):
        LocalROM().seek(script_table + file_offset)
        script_start = script_table + file_offset
        script_id = int.from_bytes(LocalROM().readBytes(2), "big")
        block_count = int.from_bytes(LocalROM().readBytes(2), "big")
        file_offset += 6
        for block_item in range(block_count):
            LocalROM().seek(script_table + file_offset)
            cond_count = int.from_bytes(LocalROM().readBytes(2), "big")
            file_offset += 2 + (8 * cond_count)
            LocalROM().seek(script_table + file_offset)
            exec_count = int.from_bytes(LocalROM().readBytes(2), "big")
            file_offset += 2 + (8 * exec_count)
        script_end = script_table + file_offset
        if script_id not in item_ids:
            script_data = []
            LocalROM().seek(script_start)
            for x in range(int((script_end - script_start) / 2)):
                script_data.append(int.from_bytes(LocalROM().readBytes(2), "big"))
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
    LocalROM().seek(script_table)
    LocalROM().writeMultipleBytes(len(good_scripts), 2)
    for script in good_scripts:
        for x in script:
            LocalROM().writeMultipleBytes(x, 2)


def grabText(file_index: int) -> list:
    """Pull text from ROM with a particular file index."""
    file_start = js.pointer_addresses[12]["entries"][file_index]["pointing_to"]
    LocalROM().seek(file_start + 0)
    count = int.from_bytes(LocalROM().readBytes(1), "big")
    text = []
    text_data = []
    text_start = (count * 0xF) + 3
    data_start = 1
    for i in range(count):
        LocalROM().seek(file_start + data_start)
        section_1_count = int.from_bytes(LocalROM().readBytes(1), "big")
        section_2_count = int.from_bytes(LocalROM().readBytes(1), "big")
        section_3_count = int.from_bytes(LocalROM().readBytes(1), "big")
        LocalROM().seek(file_start + data_start + 5)
        start = int.from_bytes(LocalROM().readBytes(2), "big")
        size = int.from_bytes(LocalROM().readBytes(2), "big")
        block_start = 1
        blocks = []
        for k in range(section_1_count):
            LocalROM().seek(file_start + data_start + block_start)
            sec2ct = int.from_bytes(LocalROM().readBytes(1), "big")
            offset = 0
            if (sec2ct & 4) != 0:
                offset += 4
            text_blocks = []
            if (sec2ct & 1) == 0:
                if (sec2ct & 2) != 0:
                    LocalROM().seek(file_start + data_start + block_start + offset + 1)
                    sec3ct = int.from_bytes(LocalROM().readBytes(1), "big")
                    for j in range(sec3ct):
                        _block = block_start + 2 + offset + (4 * j) - 1
                        LocalROM().seek(file_start + data_start + _block)
                        _pos = int.from_bytes(LocalROM().readBytes(2), "big")
                        LocalROM().seek(file_start + data_start + _block)
                        _dat = int.from_bytes(LocalROM().readBytes(4), "big")
                        text_blocks.append({"type": "sprite", "position": _pos, "data": hex(_dat), "sprite": icon_db[(_dat >> 8) & 0xFF]})
                    added = block_start + 2 + offset + (4 * sec3ct) + 4
            else:
                LocalROM().seek(file_start + data_start + block_start + offset + 1)
                sec3ct = int.from_bytes(LocalROM().readBytes(1), "big")
                for j in range(sec3ct):
                    _block = block_start + 2 + offset + (8 * j) - 1
                    LocalROM().seek(file_start + data_start + _block + 3)
                    _start = int.from_bytes(LocalROM().readBytes(2), "big")
                    LocalROM().seek(file_start + data_start + _block + 5)
                    _size = int.from_bytes(LocalROM().readBytes(2), "big")
                    text_blocks.append({"type": "normal", "start": _start, "size": _size})
                added = block_start + 2 + offset + (8 * sec3ct) + 4
            # print(f"File {file_index}, Textbox {i}, section {k}")
            blocks.append({"block_start": hex(block_start + data_start), "section2count": sec2ct, "section3count": sec3ct, "offset": offset, "text": text_blocks})
            block_start = added
        LocalROM().seek(file_start + data_start)
        if added < data_start:
            info = b""
        else:
            info = LocalROM().readBytes(added - data_start)
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
                    end = start + item3["size"]
                    LocalROM().seek(file_start + start)
                    temp.append(LocalROM().readBytes(item3["size"]).decode())
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


def writeText(file_index: int, text: list):
    """Write the text to ROM."""
    text_start = js.pointer_addresses[12]["entries"][file_index]["pointing_to"]
    LocalROM().seek(text_start)
    LocalROM().writeBytes(bytearray([len(text)]))
    position = 0
    for textbox in text:
        LocalROM().writeBytes(len(textbox).to_bytes(1, "big"))
        for block in textbox:
            # Get Icon State
            icon_id = -1
            for string in block["text"]:
                if string in icon_db.values():
                    for icon in icon_db:
                        if icon_db[icon] == string:
                            icon_id = icon
            if icon_id > -1:
                LocalROM().writeBytes(bytearray([2, 1]))
                LocalROM().writeBytes(icon_id.to_bytes(2, "big"))
                LocalROM().writeBytes(bytearray([0, 0]))
            else:
                LocalROM().writeBytes(bytearray([1, len(block["text"])]))
                for string in block["text"]:
                    LocalROM().writeBytes(position.to_bytes(4, "big"))
                    LocalROM().writeBytes(len(string).to_bytes(2, "big"))
                    LocalROM().writeBytes(bytearray([0, 0]))
                    position += len(string)
            unk0 = 0
            if "unk0" in block:
                unk0 = block["unk0"]
            LocalROM().writeBytes(int(float_to_hex(unk0), 16).to_bytes(4, "big"))
    LocalROM().writeBytes(bytearray(position.to_bytes(2, "big")))
    for textbox in text:
        for block in textbox:
            is_icon = False
            for string in block["text"]:
                if string in icon_db.values():
                    is_icon = True
            if not is_icon:
                for string in block["text"]:
                    LocalROM().writeBytes(string.encode("ascii"))


def getObjectAddress(map: int, id: int, object_type: str) -> int:
    """Get address of object in setup."""
    setup_start = js.pointer_addresses[9]["entries"][map]["pointing_to"]
    LocalROM().seek(setup_start)
    model_2_count = int.from_bytes(LocalROM().readBytes(4), "big")
    if object_type == "modeltwo":
        for item in range(model_2_count):
            item_start = setup_start + 4 + (item * 0x30)
            LocalROM().seek(item_start + 0x2A)
            if int.from_bytes(LocalROM().readBytes(2), "big") == id:
                return item_start
    mystery_start = setup_start + 4 + (0x30 * model_2_count)
    LocalROM().seek(mystery_start)
    mystery_count = int.from_bytes(LocalROM().readBytes(4), "big")
    actor_start = mystery_start + 4 + (0x24 * mystery_count)
    LocalROM().seek(actor_start)
    actor_count = int.from_bytes(LocalROM().readBytes(4), "big")
    if object_type == "actor":
        for item in range(actor_count):
            item_start = actor_start + 4 + (item * 0x38)
            LocalROM().seek(item_start + 0x34)
            if int.from_bytes(LocalROM().readBytes(2), "big") == id:
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


class TextureFormat(IntEnum):
    """Texture Format Enum."""

    Null = auto()
    RGBA5551 = auto()
    RGBA32 = auto()
    I8 = auto()
    I4 = auto()
    IA8 = auto()
    IA4 = auto()


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
