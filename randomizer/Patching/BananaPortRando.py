"""Rando write bananaport locations."""

import js
from randomizer.Enums.Settings import BananaportRando, ShufflePortLocations
from randomizer.Lists.Warps import BananaportVanilla
from randomizer.Patching.Patcher import LocalROM
from randomizer.Enums.Maps import Maps
from randomizer.Lists.Warps import BananaportVanilla
from randomizer.Lists.CustomLocations import CustomLocations
from randomizer.Enums.Levels import Levels
from randomizer.Patching.Lib import float_to_hex


def randomize_bananaport(spoiler):
    """Rando write bananaport locations."""
    pad_types = [0x214, 0x213, 0x211, 0x212, 0x210]
    ROM_COPY = LocalROM()

    if spoiler.settings.bananaport_rando == BananaportRando.in_level:
        for cont_map in spoiler.bananaport_replacements:
            pad_vanilla = {}
            cont_map_id = int(cont_map["containing_map"])
            cont_map_setup_address = js.pointer_addresses[9]["entries"][cont_map_id]["pointing_to"]
            # Pointer Table 9, use "containing_map" as a map index to grab setup start address
            ROM_COPY.seek(cont_map_setup_address)
            model2_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
            for x in range(model2_count):
                start = cont_map_setup_address + 4 + (x * 0x30)
                ROM_COPY.seek(start + 0x28)
                obj_type = int.from_bytes(ROM_COPY.readBytes(2), "big")
                if obj_type in pad_types:
                    pad_types.index(obj_type)
                    ROM_COPY.seek(start + 0x2A)
                    obj_id = int.from_bytes(ROM_COPY.readBytes(2), "big")
                    ROM_COPY.seek(start + 0)
                    obj_x = int.from_bytes(ROM_COPY.readBytes(4), "big")
                    ROM_COPY.seek(start + 4)
                    obj_y = int.from_bytes(ROM_COPY.readBytes(4), "big")
                    ROM_COPY.seek(start + 8)
                    obj_z = int.from_bytes(ROM_COPY.readBytes(4), "big")
                    ROM_COPY.seek(start + 12)
                    obj_scale = int.from_bytes(ROM_COPY.readBytes(4), "big")
                    ROM_COPY.seek(start + 0x18)
                    obj_rotx = int.from_bytes(ROM_COPY.readBytes(4), "big")
                    ROM_COPY.seek(start + 0x1C)
                    obj_roty = int.from_bytes(ROM_COPY.readBytes(4), "big")
                    ROM_COPY.seek(start + 0x20)
                    obj_rotz = int.from_bytes(ROM_COPY.readBytes(4), "big")
                    banned = False
                    for warp in BananaportVanilla.values():
                        if warp.map_id == cont_map_id and warp.obj_id_vanilla == obj_id and warp.locked:
                            banned = True
                    if not banned:
                        pad_vanilla[obj_id] = {"x": obj_x, "y": obj_y, "z": obj_z, "scale": obj_scale, "rx": obj_rotx, "ry": obj_roty, "rz": obj_rotz, "idx": x}
            for y in cont_map["pads"]:
                warp_idx = y["warp_index"]
                for assortment_index, warp_id in enumerate(y["warp_ids"]):
                    # For each warp in pair, look up id it's using. Take the vanilla warps for that index, transplant the loc/rot/scale data to that id
                    # Search for the relevant vanilla ID for the selected warp index
                    pair_index = 0
                    pair_locked = []
                    vanilla_id = -1
                    for pad in BananaportVanilla.values():
                        if pad.map_id == cont_map_id and pad.vanilla_warp == warp_idx and vanilla_id == -1:
                            pair_locked.append(pad.locked)
                            if (assortment_index == pair_index and not pad.locked) or (
                                assortment_index == 0 and pair_index == 1 and pair_locked[0] and not pad.locked
                            ):  # Second condition checks if 1st warp in pair is locked, but second isn't
                                vanilla_id = pad.obj_id_vanilla
                            pair_index += 1
                    if vanilla_id != -1:  # Found associated Warp
                        if vanilla_id in pad_vanilla and warp_id in pad_vanilla:  # Search and reference warp in location dump
                            vanilla_idx = pad_vanilla[vanilla_id]["idx"]
                            start = cont_map_setup_address + (0x30 * vanilla_idx) + 4
                            ROM_COPY.seek(start)
                            ROM_COPY.writeMultipleBytes(pad_vanilla[warp_id]["x"], 4)
                            ROM_COPY.writeMultipleBytes(pad_vanilla[warp_id]["y"], 4)
                            ROM_COPY.writeMultipleBytes(pad_vanilla[warp_id]["z"], 4)
                            ROM_COPY.writeMultipleBytes(pad_vanilla[warp_id]["scale"], 4)
                            ROM_COPY.seek(start + 0x18)
                            ROM_COPY.writeMultipleBytes(pad_vanilla[warp_id]["rx"], 4)
                            ROM_COPY.writeMultipleBytes(pad_vanilla[warp_id]["ry"], 4)
                            ROM_COPY.writeMultipleBytes(pad_vanilla[warp_id]["rz"], 4)
                        else:
                            print("ERROR: ID not found in pad location dump")
                    else:
                        print("ERROR: Vanilla ID not found")
    elif spoiler.settings.bananaport_rando in (BananaportRando.crossmap_coupled, BananaportRando.crossmap_decoupled):
        data_start = 0x1FF0000
        visual_warp_changes = []
        maps_used = []
        for port_index, port_new in enumerate(spoiler.bananaport_replacements):
            ROM_COPY.seek(data_start + (port_index * 0xA))
            map_id = int.from_bytes(ROM_COPY.readBytes(1), "big")
            ROM_COPY.writeMultipleBytes(port_new[0], 1)
            obj_id = int.from_bytes(ROM_COPY.readBytes(2), "big")
            if map_id not in maps_used:
                maps_used.append(map_id)
            visual_warp_changes.append([map_id, obj_id, port_new[1]])
        for cont_map_id in maps_used:
            cont_map_setup_address = js.pointer_addresses[9]["entries"][cont_map_id]["pointing_to"]
            ROM_COPY.seek(cont_map_setup_address)
            model2_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
            for x in range(model2_count):
                start = cont_map_setup_address + 4 + (x * 0x30)
                ROM_COPY.seek(start + 0x2A)
                obj_id = int.from_bytes(ROM_COPY.readBytes(2), "big")
                for warp_change in visual_warp_changes:
                    if warp_change[0] == cont_map_id and warp_change[1] == obj_id:
                        ROM_COPY.seek(start + 0x28)
                        ROM_COPY.writeMultipleBytes(pad_types[warp_change[2]], 2)


def move_bananaports(spoiler):
    """Move bananaports around in conjunction with custom bananaport location rando."""
    ROM_COPY = LocalROM()
    MAPS_WITH_WARPS = {
        Maps.JungleJapes: Levels.JungleJapes,
        Maps.AngryAztec: Levels.AngryAztec,
        Maps.FranticFactory: Levels.FranticFactory,
        Maps.GloomyGalleon: Levels.GloomyGalleon,
        Maps.FungiForest: Levels.FungiForest,
        Maps.CrystalCaves: Levels.CrystalCaves,
        Maps.CreepyCastle: Levels.CreepyCastle,
        Maps.Isles: Levels.DKIsles,
        Maps.AztecLlamaTemple: Levels.AngryAztec,
        Maps.CastleCrypt: Levels.CreepyCastle,
    }

    if spoiler.settings.bananaport_placement_rando != ShufflePortLocations.off:
        for cont_map_id in MAPS_WITH_WARPS:
            level_id = MAPS_WITH_WARPS[cont_map_id]
            setup_table = js.pointer_addresses[9]["entries"][cont_map_id]["pointing_to"]
            # exit_table = js.pointer_addresses[23]["entries"][cont_map_id]["pointing_to"]
            modification_table = []
            for warp_id in spoiler.warp_locations:
                if BananaportVanilla[warp_id].map_id == cont_map_id:
                    custom_location_id = spoiler.warp_locations[warp_id]
                    obj_id = BananaportVanilla[warp_id].obj_id_vanilla
                    modification_table.append(
                        {
                            "obj_id": obj_id,
                            "coords": CustomLocations[level_id][custom_location_id].coords,
                            "scale": min(CustomLocations[level_id][custom_location_id].max_size / (56 * 4), 0.25),  # Make 0.25 the max size
                            "rot_y": (CustomLocations[level_id][custom_location_id].rot_y / 4096) * 360,
                        }
                    )
                # exit_id =

            # Modify setup table
            obj_id_list = [x["obj_id"] for x in modification_table]
            ROM_COPY.seek(setup_table)
            model2_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
            for model2_item in range(model2_count):
                item_start = setup_table + 4 + (model2_item * 0x30)
                ROM_COPY.seek(item_start + 0x2A)
                item_id = int.from_bytes(ROM_COPY.readBytes(2), "big")
                if item_id in obj_id_list:
                    ROM_COPY.seek(item_start)
                    for k in modification_table:
                        if k["obj_id"] == item_id:
                            for c in k["coords"]:
                                ROM_COPY.writeMultipleBytes(int(float_to_hex(c), 16), 4)
                            ROM_COPY.writeMultipleBytes(int(float_to_hex(k["scale"]), 16), 4)
                            ROM_COPY.seek(item_start + 0x18)
                            ROM_COPY.writeMultipleBytes(0, 4)
                            ROM_COPY.writeMultipleBytes(int(float_to_hex(k["rot_y"]), 16), 4)
                            ROM_COPY.writeMultipleBytes(0, 4)
