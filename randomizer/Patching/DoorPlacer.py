"""Apply Door Locations."""

import js
from randomizer.Enums.DoorType import DoorType
from randomizer.Enums.ScriptTypes import ScriptTypes
from randomizer.Enums.Settings import MiscChangesSelected
from randomizer.Enums.Types import Types
from randomizer.Lists.DoorLocations import door_locations
from randomizer.Enums.Maps import Maps
from randomizer.Patching.Lib import IsItemSelected, addNewScript, float_to_hex, getNextFreeID, TableNames
from randomizer.Patching.Patcher import LocalROM

LEVEL_MAIN_MAPS = (Maps.JungleJapes, Maps.AngryAztec, Maps.FranticFactory, Maps.GloomyGalleon, Maps.FungiForest, Maps.CrystalCaves, Maps.CreepyCastle)

PORTAL_MAP_ID_PAIRING = {
    Maps.JungleJapes: 0x11B,
    Maps.AngryAztec: 0x1A0,
    Maps.FranticFactory: 0x1C2,
    Maps.GloomyGalleon: 0x57,
    Maps.FungiForest: 0x5C,
    Maps.CrystalCaves: 0x54,
    Maps.CreepyCastle: 0xB8,
}

PORTAL_MAP_EXIT_PAIRING = {
    Maps.JungleJapes: [0, 15],
    Maps.AngryAztec: [0],
    Maps.FranticFactory: [0],
    Maps.GloomyGalleon: [0],
    Maps.FungiForest: [0, 27],
    Maps.CrystalCaves: [0],
    Maps.CreepyCastle: [0, 21],
}


class FunctionData:
    """Function information regarding an instance script."""

    def __init__(self, conditions: list, executions: list):
        """Initialize with given parameters."""
        self.conditions = conditions.copy()
        self.executions = executions.copy()


class InstanceInstruction:
    """Information about an instruction regarding an instance script."""

    def __init__(self, function: int, parameters: list, inverted: bool = False):
        """Initialize with given parameters."""
        self.function = function
        self.parameters = parameters.copy()
        self.inverted = inverted


DK_PORTAL_NEW_PICKUP_RADIUS = 60
DK_PORTAL_SCRIPT = [
    FunctionData(
        [InstanceInstruction(1, [0, 0, 0])], [InstanceInstruction(22, [1, 0, 0]), InstanceInstruction(22, [2, 0, 0]), InstanceInstruction(20, [1, 160, 0]), InstanceInstruction(20, [2, 115, 0])]
    ),
    FunctionData(
        [
            InstanceInstruction(1, [0, 0, 0]),
        ],
        [
            InstanceInstruction(17, [1, 65535, 0]),
            InstanceInstruction(17, [2, 65535, 0]),
            InstanceInstruction(1, [1, 0, 0]),
        ],
    ),
    FunctionData(
        [
            InstanceInstruction(1, [1, 0, 0]),
            InstanceInstruction(19, [DK_PORTAL_NEW_PICKUP_RADIUS, 0, 0]),
            InstanceInstruction(35, [0, 0, 0], True),
        ],
        [
            InstanceInstruction(3, [0, 60, 0]),
            InstanceInstruction(7, [116, 0, 1]),
        ],
    ),
    FunctionData(
        [
            InstanceInstruction(1, [1, 0, 0]),
            InstanceInstruction(19, [DK_PORTAL_NEW_PICKUP_RADIUS, 0, 0]),
            InstanceInstruction(35, [0, 0, 0], True),
        ],
        [
            InstanceInstruction(110, [1, 0, 0]),
            InstanceInstruction(37, [29, 0, 15]),
            InstanceInstruction(25, [90, 0, 0]),
            InstanceInstruction(1, [100, 0, 0]),
        ],
    ),
    FunctionData(
        [
            InstanceInstruction(1, [100, 0, 0]),
            InstanceInstruction(4, [0, 0, 0]),
        ],
        [
            InstanceInstruction(1, [2, 0, 0]),
        ],
    ),
    FunctionData(
        [
            InstanceInstruction(1, [1, 0, 0]),
            InstanceInstruction(19, [DK_PORTAL_NEW_PICKUP_RADIUS, 0, 0], True),
        ],
        [
            InstanceInstruction(1, [2, 0, 0]),
        ],
    ),
    FunctionData(
        [
            InstanceInstruction(1, [1, 0, 0]),
            InstanceInstruction(35, [0, 0, 0]),
        ],
        [
            InstanceInstruction(1, [2, 0, 0]),
        ],
    ),
    FunctionData(
        [
            InstanceInstruction(1, [2, 0, 0]),
            InstanceInstruction(4, [0, 0, 0]),
        ],
        [
            InstanceInstruction(90, [60, 60, 60]),
            InstanceInstruction(61, [3, 0, 0]),
            InstanceInstruction(1, [3, 0, 0]),
        ],
    ),
    FunctionData(
        [
            InstanceInstruction(1, [3, 0, 0]),
            InstanceInstruction(16, [1, 1, 0]),
        ],
        [
            InstanceInstruction(3, [0, 40, 0]),
            InstanceInstruction(7, [116, 0, 0]),
            InstanceInstruction(110, [1, 0, 0]),
            InstanceInstruction(37, [30, 0, 15]),
        ],
    ),
    FunctionData(
        [
            InstanceInstruction(1, [3, 0, 0]),
            InstanceInstruction(16, [1, 1, 0]),
        ],
        [
            InstanceInstruction(25, [89, 0, 0]),
            InstanceInstruction(1, [4, 0, 0]),
        ],
    ),
    FunctionData(
        [
            InstanceInstruction(1, [4, 0, 0]),
            InstanceInstruction(4, [0, 0, 0]),
        ],
        [
            InstanceInstruction(141, [0, 0, 0]),
            InstanceInstruction(1, [5, 0, 0]),
        ],
    ),
]


def pushNewDKPortalScript(cont_map_id: Maps):
    """Write new dk portal script to ROM."""
    id_pairings = {
        Maps.JungleJapes: 0x11B,
        Maps.AngryAztec: 0x1A0,
        Maps.FranticFactory: 0x1C2,
        Maps.GloomyGalleon: 0x57,
        Maps.FungiForest: 0x5C,
        Maps.CrystalCaves: 0x54,
        Maps.CreepyCastle: 0xB8,
    }
    if cont_map_id not in id_pairings:
        raise Exception(f"Invalid map for pairing. Alert the devs (Map {cont_map_id})")
    obj_id = id_pairings[cont_map_id]
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
        if script_id != obj_id:
            script_data = []
            ROM_COPY.seek(script_start)
            for x in range(int((script_end - script_start) / 2)):
                script_data.append(int.from_bytes(ROM_COPY.readBytes(2), "big"))
            good_scripts.append(script_data)
    # Get new script data
    script_arr = [
        obj_id,
        len(DK_PORTAL_SCRIPT),
        0,
    ]
    for block in DK_PORTAL_SCRIPT:
        script_arr.append(len(block.conditions))
        for cond in block.conditions:
            func = cond.function
            if cond.inverted:
                func |= 0x8000
            script_arr.append(func)
            script_arr.extend(cond.parameters)
        script_arr.append(len(block.executions))
        for ex in block.executions:
            script_arr.append(ex.function)
            script_arr.extend(ex.parameters)
    good_scripts.append(script_arr)
    # Reconstruct File
    ROM_COPY.seek(script_table)
    ROM_COPY.writeMultipleBytes(len(good_scripts), 2)
    for script in good_scripts:
        for x in script:
            ROM_COPY.writeMultipleBytes(x, 2)


def remove_existing_indicators(spoiler):
    """Remove all existing indicators."""
    if not spoiler.settings.portal_numbers:
        ROM_COPY = LocalROM()
        for cont_map_id in range(216):
            setup_table = js.pointer_addresses[9]["entries"][cont_map_id]["pointing_to"]
            # Filter Setup
            ROM_COPY.seek(setup_table)
            model2_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
            retained_model2 = []
            for item in range(model2_count):
                item_start = setup_table + 4 + (item * 0x30)
                ROM_COPY.seek(item_start + 0x28)
                item_type = int.from_bytes(ROM_COPY.readBytes(2), "big")
                if cont_map_id == 0x2A or item_type != 0x2AB:
                    ROM_COPY.seek(item_start)
                    item_data = []
                    for x in range(int(0x30 / 4)):
                        item_data.append(int.from_bytes(ROM_COPY.readBytes(4), "big"))
                    retained_model2.append(item_data)
            mys_start = setup_table + 4 + (model2_count * 0x30)
            ROM_COPY.seek(mys_start)
            mys_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
            act_start = mys_start + 4 + (mys_count * 0x24)
            ROM_COPY.seek(act_start)
            act_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
            act_end = act_start + 4 + (act_count * 0x38)
            other_retained_data = []
            ROM_COPY.seek(mys_start)
            for x in range(int((act_end - mys_start) / 4)):
                other_retained_data.append(int.from_bytes(ROM_COPY.readBytes(4), "big"))
            # Reconstruct setup file
            ROM_COPY.seek(setup_table)
            ROM_COPY.writeMultipleBytes(len(retained_model2), 4)
            for item in retained_model2:
                for data in item:
                    ROM_COPY.writeMultipleBytes(data, 4)
            for data in other_retained_data:
                ROM_COPY.writeMultipleBytes(data, 4)


def place_door_locations(spoiler):
    """Place Wrinkly Doors, and eventually T&S Doors."""
    enabled = False
    settings_enable = [
        spoiler.settings.wrinkly_location_rando,
        spoiler.settings.tns_location_rando,
        spoiler.settings.remove_wrinkly_puzzles,
        spoiler.settings.enable_progressive_hints,
        spoiler.settings.dk_portal_location_rando,
    ]
    for boolean in settings_enable:
        if boolean:
            enabled = True
    if enabled:
        ROM_COPY = LocalROM()
        wrinkly_doors = [0xF0, 0xF2, 0xEF, 0x67, 0xF1]
        # Also remove
        #   0x23C: Spinning Door (Az Lobby)
        #   0x18: Metal Pad (Az Lobby)
        #   0x23D: Wrinkly Wheel (Fungi Lobby)
        #   0x28: Lever (Fungi Lobby)
        #   0x35: Ice Block (Caves Lobby)
        #   0xCE: Grey Switch (Caves Lobby)
        dk_portal_locations = {
            Maps.JungleJapes: [0, 0, 0, 0],
            Maps.AngryAztec: [0, 0, 0, 0],
            Maps.FranticFactory: [0, 0, 0, 0],
            Maps.GloomyGalleon: [0, 0, 0, 0],
            Maps.FungiForest: [0, 0, 0, 0],
            Maps.CrystalCaves: [0, 0, 0, 0],
            Maps.CreepyCastle: [0, 0, 0, 0],
        }
        # Handle Setup
        for cont_map_id in range(216):
            setup_table = js.pointer_addresses[9]["entries"][cont_map_id]["pointing_to"]
            # Filter Setup
            ROM_COPY.seek(setup_table)
            model2_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
            retained_model2 = []
            for item in range(model2_count):
                item_start = setup_table + 4 + (item * 0x30)
                ROM_COPY.seek(item_start + 0x28)
                item_type = int.from_bytes(ROM_COPY.readBytes(2), "big")
                retain = True
                if spoiler.settings.wrinkly_location_rando or spoiler.settings.remove_wrinkly_puzzles or spoiler.settings.enable_progressive_hints:
                    if item_type in wrinkly_doors:
                        retain = False
                    if cont_map_id == Maps.AngryAztecLobby and item_type in (0x23C, 0x18):
                        retain = False
                    if cont_map_id == Maps.FungiForestLobby and item_type in (0x23D, 0x28):
                        retain = False
                    if cont_map_id == Maps.CrystalCavesLobby and item_type in (0x35, 0xCE):
                        retain = False
                if spoiler.settings.tns_location_rando:
                    if cont_map_id != 0x2A:
                        if item_type in (0x2AB, 0x2AC):
                            retain = False
                if spoiler.settings.dk_portal_location_rando:
                    if cont_map_id in LEVEL_MAIN_MAPS:
                        if item_type == 0x2AD:
                            retain = False
                if retain:
                    ROM_COPY.seek(item_start)
                    item_data = []
                    for x in range(int(0x30 / 4)):
                        item_data.append(int.from_bytes(ROM_COPY.readBytes(4), "big"))
                    retained_model2.append(item_data)
            mys_start = setup_table + 4 + (model2_count * 0x30)
            ROM_COPY.seek(mys_start)
            mys_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
            act_start = mys_start + 4 + (mys_count * 0x24)
            ROM_COPY.seek(act_start)
            act_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
            act_end = act_start + 4 + (act_count * 0x38)
            other_retained_data = []
            ROM_COPY.seek(mys_start)
            for x in range(int((act_end - mys_start) / 4)):
                other_retained_data.append(int.from_bytes(ROM_COPY.readBytes(4), "big"))
            # Construct placed wrinkly doors
            door_ids = []
            map_wrinkly_ids = []
            portal_indicator_ids = []
            portal_ids = []
            indicator_ids = []
            for level in spoiler.shuffled_door_data:
                for data in spoiler.shuffled_door_data[level]:
                    door = door_locations[level][data[0]]
                    door_type = data[1]
                    if door.map == cont_map_id:
                        if door_type == "wrinkly" and (
                            spoiler.settings.wrinkly_location_rando
                            or IsItemSelected(spoiler.settings.quality_of_life, spoiler.settings.misc_changes_selected, MiscChangesSelected.remove_wrinkly_puzzles)
                        ):
                            if (not spoiler.settings.enable_progressive_hints) or Types.Hint in spoiler.settings.shuffled_location_types:
                                kong = data[2]
                                item_data = []
                                for coord_index in range(3):
                                    item_data.append(int(float_to_hex(door.location[coord_index]), 16))  # x y z
                                default_scale = door.scale
                                if door.default_placed == DoorType.dk_portal:
                                    default_scale = 2
                                item_data.append(int(float_to_hex(default_scale), 16))  # Scale
                                item_data.append(0x5F0)
                                item_data.append(0x80121B00)
                                item_data.append(int(float_to_hex(door.rx), 16))  # rx
                                item_data.append(int(float_to_hex(door.location[3]), 16))  # ry
                                item_data.append(int(float_to_hex(door.rz), 16))  # rz
                                item_data.append(0)
                                id = getNextFreeID(cont_map_id, door_ids)
                                map_wrinkly_ids.append(id)
                                door_ids.append(id)
                                item_data.append((wrinkly_doors[kong] << 16) | id)
                                item_data.append(1 << 16)
                                retained_model2.append(item_data)
                        elif door_type == "tns" and spoiler.settings.tns_location_rando:
                            lim = 2
                            if not spoiler.settings.portal_numbers:
                                lim = 1
                            for k in range(lim):
                                item_data = []
                                for coord_index in range(3):
                                    if k == 1 and coord_index == 1:
                                        item_data.append(int(float_to_hex(door.location[coord_index] - 30), 16))  # y
                                    else:
                                        item_data.append(int(float_to_hex(door.location[coord_index]), 16))  # x y z
                                default_scale = door.scale
                                if door.default_placed == DoorType.dk_portal:
                                    default_scale = 2
                                item_data.append(int(float_to_hex([default_scale, 0.35 * default_scale][k]), 16))  # Scale
                                item_data.append(0xFFFEFEFF)
                                item_data.append(0x001BFFE1)
                                item_data.append(int(float_to_hex(door.rx), 16))  # rx
                                item_data.append(int(float_to_hex(door.location[3]), 16))  # ry
                                item_data.append(int(float_to_hex(door.rz), 16))  # rz
                                item_data.append(0)
                                id = getNextFreeID(cont_map_id, door_ids)
                                portal_indicator_ids.append(id)
                                door_ids.append(id)
                                if k == 0:
                                    portal_ids.append(id)
                                else:
                                    indicator_ids.append(id)
                                item_data.append(([0x2AC, 0x2AB][k] << 16) | id)
                                item_data.append(1 << 16)
                                retained_model2.append(item_data)
                        elif door_type == "dk_portal" and spoiler.settings.dk_portal_location_rando:
                            item_data = []
                            for coord_index in range(3):
                                item_data.append(int(float_to_hex(door.location[coord_index]), 16))  # x y z
                            for coord_index in range(4):
                                dk_portal_locations[cont_map_id][coord_index] = door.location[coord_index]
                            default_scale = 1
                            if door.default_placed != DoorType.dk_portal:
                                default_scale = door.scale / 2
                            item_data.append(int(float_to_hex(default_scale), 16))  # Scale
                            item_data.append(0xFFFFFEFF)
                            item_data.append(0x0101F03E)
                            item_data.append(int(float_to_hex(door.rx), 16))  # rx
                            item_data.append(int(float_to_hex(door.location[3]), 16))  # ry
                            item_data.append(int(float_to_hex(door.rz), 16))  # rz
                            item_data.append(0)
                            item_data.append((0x2AD << 16) | PORTAL_MAP_ID_PAIRING[cont_map_id])
                            item_data.append(1 << 16)
                            retained_model2.append(item_data)
            if len(map_wrinkly_ids) > 0:
                addNewScript(cont_map_id, map_wrinkly_ids, ScriptTypes.Wrinkly)
            if len(portal_ids) > 0:
                addNewScript(cont_map_id, portal_ids, ScriptTypes.TnsPortal)
            if len(indicator_ids) > 0:
                addNewScript(cont_map_id, indicator_ids, ScriptTypes.TnsIndicator)
            # Reconstruct setup file
            ROM_COPY.seek(setup_table)
            ROM_COPY.writeMultipleBytes(len(retained_model2), 4)
            for item in retained_model2:
                for data in item:
                    ROM_COPY.writeMultipleBytes(data, 4)
            for data in other_retained_data:
                ROM_COPY.writeMultipleBytes(data, 4)
        if spoiler.settings.dk_portal_location_rando:
            for portal_map in dk_portal_locations:
                pushNewDKPortalScript(portal_map)
                exit_start = js.pointer_addresses[TableNames.Exits]["entries"][portal_map]["pointing_to"]
                exits_to_alter = PORTAL_MAP_EXIT_PAIRING[portal_map]
                for exit_index in exits_to_alter:
                    ROM_COPY.seek(exit_start + (exit_index * 10))
                    for coord_index in range(3):
                        coord_value = dk_portal_locations[portal_map][coord_index]
                        coord_int = int(coord_value)
                        if coord_int < 0:
                            coord_int += 0x10000
                        ROM_COPY.writeMultipleBytes(coord_int, 2)
                    angle = int(255 * (dk_portal_locations[portal_map][3] / 360))
                    cam_raw_angle = dk_portal_locations[portal_map][3]
                    if cam_raw_angle >= 180:
                        cam_raw_angle -= 180
                    else:
                        cam_raw_angle += 180
                    cam_angle = int(255 * (cam_raw_angle / 360))
                    ROM_COPY.writeMultipleBytes(angle, 1)
                    ROM_COPY.writeMultipleBytes(cam_angle, 1)
