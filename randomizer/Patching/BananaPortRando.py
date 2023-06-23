"""Rando write bananaport locations."""
from imp import source_from_cache

import js
from randomizer.Enums.Settings import BananaportRando
from randomizer.Lists.Warps import BananaportVanilla
from randomizer.Patching.Patcher import ROM, LocalROM


def randomize_bananaport(spoiler):
    """Rando write bananaport locations."""
    pad_types = [0x214, 0x213, 0x211, 0x212, 0x210]

    if spoiler.settings.bananaport_rando == BananaportRando.in_level:
        for cont_map in spoiler.bananaport_replacements:
            pad_vanilla = {}
            cont_map_id = int(cont_map["containing_map"])
            cont_map_setup_address = js.pointer_addresses[9]["entries"][cont_map_id]["pointing_to"]
            # Pointer Table 9, use "containing_map" as a map index to grab setup start address
            LocalROM().seek(cont_map_setup_address)
            model2_count = int.from_bytes(LocalROM().readBytes(4), "big")
            for x in range(model2_count):
                start = cont_map_setup_address + 4 + (x * 0x30)
                LocalROM().seek(start + 0x28)
                obj_type = int.from_bytes(LocalROM().readBytes(2), "big")
                if obj_type in pad_types:
                    pad_index = pad_types.index(obj_type)
                    LocalROM().seek(start + 0x2A)
                    obj_id = int.from_bytes(LocalROM().readBytes(2), "big")
                    LocalROM().seek(start + 0)
                    obj_x = int.from_bytes(LocalROM().readBytes(4), "big")
                    LocalROM().seek(start + 4)
                    obj_y = int.from_bytes(LocalROM().readBytes(4), "big")
                    LocalROM().seek(start + 8)
                    obj_z = int.from_bytes(LocalROM().readBytes(4), "big")
                    LocalROM().seek(start + 12)
                    obj_scale = int.from_bytes(LocalROM().readBytes(4), "big")
                    LocalROM().seek(start + 0x18)
                    obj_rotx = int.from_bytes(LocalROM().readBytes(4), "big")
                    LocalROM().seek(start + 0x1C)
                    obj_roty = int.from_bytes(LocalROM().readBytes(4), "big")
                    LocalROM().seek(start + 0x20)
                    obj_rotz = int.from_bytes(LocalROM().readBytes(4), "big")
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
                            LocalROM().seek(start)
                            LocalROM().writeMultipleBytes(pad_vanilla[warp_id]["x"], 4)
                            LocalROM().writeMultipleBytes(pad_vanilla[warp_id]["y"], 4)
                            LocalROM().writeMultipleBytes(pad_vanilla[warp_id]["z"], 4)
                            LocalROM().writeMultipleBytes(pad_vanilla[warp_id]["scale"], 4)
                            LocalROM().seek(start + 0x18)
                            LocalROM().writeMultipleBytes(pad_vanilla[warp_id]["rx"], 4)
                            LocalROM().writeMultipleBytes(pad_vanilla[warp_id]["ry"], 4)
                            LocalROM().writeMultipleBytes(pad_vanilla[warp_id]["rz"], 4)
                        else:
                            print("ERROR: ID not found in pad location dump")
                    else:
                        print("ERROR: Vanilla ID not found")
    elif spoiler.settings.bananaport_rando in (BananaportRando.crossmap_coupled, BananaportRando.crossmap_decoupled):
        data_start = 0x1FF0000
        visual_warp_changes = []
        maps_used = []
        for port_index, port_new in enumerate(spoiler.bananaport_replacements):
            LocalROM().seek(data_start + (port_index * 0xA))
            map_id = int.from_bytes(LocalROM().readBytes(1), "big")
            LocalROM().writeMultipleBytes(port_new[0], 1)
            obj_id = int.from_bytes(LocalROM().readBytes(2), "big")
            if map_id not in maps_used:
                maps_used.append(map_id)
            visual_warp_changes.append([map_id, obj_id, port_new[1]])
        for cont_map_id in maps_used:
            cont_map_setup_address = js.pointer_addresses[9]["entries"][cont_map_id]["pointing_to"]
            LocalROM().seek(cont_map_setup_address)
            model2_count = int.from_bytes(LocalROM().readBytes(4), "big")
            for x in range(model2_count):
                start = cont_map_setup_address + 4 + (x * 0x30)
                LocalROM().seek(start + 0x2A)
                obj_id = int.from_bytes(LocalROM().readBytes(2), "big")
                for warp_change in visual_warp_changes:
                    if warp_change[0] == cont_map_id and warp_change[1] == obj_id:
                        LocalROM().seek(start + 0x28)
                        LocalROM().writeMultipleBytes(pad_types[warp_change[2]], 2)
