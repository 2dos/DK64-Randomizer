"""Library functions for patching."""
import struct
import js
from randomizer.Patching.Patcher import ROM
from randomizer.Enums.ScriptTypes import ScriptTypes


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


def getNextFreeID(cont_map_id: int, ignore=[]):
    """Get next available Model 2 ID."""
    setup_table = js.pointer_addresses[9]["entries"][cont_map_id]["pointing_to"]
    ROM().seek(setup_table)
    model2_count = int.from_bytes(ROM().readBytes(4), "big")
    vacant_ids = list(range(0, 600))
    for item in range(model2_count):
        item_start = setup_table + 4 + (item * 0x30)
        ROM().seek(item_start + 0x2A)
        item_id = int.from_bytes(ROM().readBytes(2), "big")
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
    ROM().seek(script_table)
    script_count = int.from_bytes(ROM().readBytes(2), "big")
    good_scripts = []
    # Construct good pre-existing scripts
    file_offset = 2
    for script_item in range(script_count):
        ROM().seek(script_table + file_offset)
        script_start = script_table + file_offset
        script_id = int.from_bytes(ROM().readBytes(2), "big")
        block_count = int.from_bytes(ROM().readBytes(2), "big")
        file_offset += 6
        for block_item in range(block_count):
            ROM().seek(script_table + file_offset)
            cond_count = int.from_bytes(ROM().readBytes(2), "big")
            file_offset += 2 + (8 * cond_count)
            ROM().seek(script_table + file_offset)
            exec_count = int.from_bytes(ROM().readBytes(2), "big")
            file_offset += 2 + (8 * exec_count)
        script_end = script_table + file_offset
        if script_id not in item_ids:
            script_data = []
            ROM().seek(script_start)
            for x in range(int((script_end - script_start) / 2)):
                script_data.append(int.from_bytes(ROM().readBytes(2), "big"))
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
    ROM().seek(script_table)
    ROM().writeMultipleBytes(len(good_scripts), 2)
    for script in good_scripts:
        for x in script:
            ROM().writeMultipleBytes(x, 2)
