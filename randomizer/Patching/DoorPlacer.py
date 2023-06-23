"""Apply Door Locations."""
import random

import js
from randomizer.Enums.ScriptTypes import ScriptTypes
from randomizer.Enums.Settings import MiscChangesSelected
from randomizer.Lists.DoorLocations import door_locations
from randomizer.Lists.MapsAndExits import Maps
from randomizer.Patching.Lib import addNewScript, float_to_hex, getNextFreeID
from randomizer.Patching.Patcher import ROM, LocalROM


def remove_existing_indicators(spoiler):
    """Remove all existing indicators."""
    if not spoiler.settings.portal_numbers:
        for cont_map_id in range(216):
            setup_table = js.pointer_addresses[9]["entries"][cont_map_id]["pointing_to"]
            # Filter Setup
            LocalROM().seek(setup_table)
            model2_count = int.from_bytes(LocalROM().readBytes(4), "big")
            retained_model2 = []
            for item in range(model2_count):
                item_start = setup_table + 4 + (item * 0x30)
                LocalROM().seek(item_start + 0x28)
                item_type = int.from_bytes(LocalROM().readBytes(2), "big")
                if cont_map_id == 0x2A or item_type != 0x2AB:
                    LocalROM().seek(item_start)
                    item_data = []
                    for x in range(int(0x30 / 4)):
                        item_data.append(int.from_bytes(LocalROM().readBytes(4), "big"))
                    retained_model2.append(item_data)
            mys_start = setup_table + 4 + (model2_count * 0x30)
            LocalROM().seek(mys_start)
            mys_count = int.from_bytes(LocalROM().readBytes(4), "big")
            act_start = mys_start + 4 + (mys_count * 0x24)
            LocalROM().seek(act_start)
            act_count = int.from_bytes(LocalROM().readBytes(4), "big")
            act_end = act_start + 4 + (act_count * 0x38)
            other_retained_data = []
            LocalROM().seek(mys_start)
            for x in range(int((act_end - mys_start) / 4)):
                other_retained_data.append(int.from_bytes(LocalROM().readBytes(4), "big"))
            # Reconstruct setup file
            LocalROM().seek(setup_table)
            LocalROM().writeMultipleBytes(len(retained_model2), 4)
            for item in retained_model2:
                for data in item:
                    LocalROM().writeMultipleBytes(data, 4)
            for data in other_retained_data:
                LocalROM().writeMultipleBytes(data, 4)


def place_door_locations(spoiler):
    """Place Wrinkly Doors, and eventually T&S Doors."""
    if spoiler.settings.wrinkly_location_rando or spoiler.settings.tns_location_rando or spoiler.settings.remove_wrinkly_puzzles:
        wrinkly_doors = [0xF0, 0xF2, 0xEF, 0x67, 0xF1]
        # Also remove
        #   0x23C: Spinning Door (Az Lobby)
        #   0x18: Metal Pad (Az Lobby)
        #   0x23D: Wrinkly Wheel (Fungi Lobby)
        #   0x28: Lever (Fungi Lobby)
        #   0x35: Ice Block (Caves Lobby)
        #   0xCE: Grey Switch (Caves Lobby)
        # Handle Setup
        for cont_map_id in range(216):
            setup_table = js.pointer_addresses[9]["entries"][cont_map_id]["pointing_to"]
            # Filter Setup
            LocalROM().seek(setup_table)
            model2_count = int.from_bytes(LocalROM().readBytes(4), "big")
            retained_model2 = []
            for item in range(model2_count):
                item_start = setup_table + 4 + (item * 0x30)
                LocalROM().seek(item_start + 0x28)
                item_type = int.from_bytes(LocalROM().readBytes(2), "big")
                retain = True
                if spoiler.settings.wrinkly_location_rando or spoiler.settings.remove_wrinkly_puzzles:
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
                if retain:
                    LocalROM().seek(item_start)
                    item_data = []
                    for x in range(int(0x30 / 4)):
                        item_data.append(int.from_bytes(LocalROM().readBytes(4), "big"))
                    retained_model2.append(item_data)
            mys_start = setup_table + 4 + (model2_count * 0x30)
            LocalROM().seek(mys_start)
            mys_count = int.from_bytes(LocalROM().readBytes(4), "big")
            act_start = mys_start + 4 + (mys_count * 0x24)
            LocalROM().seek(act_start)
            act_count = int.from_bytes(LocalROM().readBytes(4), "big")
            act_end = act_start + 4 + (act_count * 0x38)
            other_retained_data = []
            LocalROM().seek(mys_start)
            for x in range(int((act_end - mys_start) / 4)):
                other_retained_data.append(int.from_bytes(LocalROM().readBytes(4), "big"))
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
                            or (MiscChangesSelected.remove_wrinkly_puzzles in spoiler.settings.misc_changes_selected or len(spoiler.settings.misc_changes_selected) == 0)
                        ):
                            kong = data[2]
                            item_data = []
                            for coord_index in range(3):
                                item_data.append(int(float_to_hex(door.location[coord_index]), 16))  # x y z
                            item_data.append(int(float_to_hex(door.scale), 16))  # Scale
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
                                item_data.append(int(float_to_hex([door.scale, 0.35][k]), 16))  # Scale
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
            if len(map_wrinkly_ids) > 0:
                addNewScript(cont_map_id, map_wrinkly_ids, ScriptTypes.Wrinkly)
            if len(portal_ids) > 0:
                addNewScript(cont_map_id, portal_ids, ScriptTypes.TnsPortal)
            if len(indicator_ids) > 0:
                addNewScript(cont_map_id, indicator_ids, ScriptTypes.TnsIndicator)
            # Reconstruct setup file
            LocalROM().seek(setup_table)
            LocalROM().writeMultipleBytes(len(retained_model2), 4)
            for item in retained_model2:
                for data in item:
                    LocalROM().writeMultipleBytes(data, 4)
            for data in other_retained_data:
                LocalROM().writeMultipleBytes(data, 4)
