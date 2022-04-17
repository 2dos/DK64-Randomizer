"""Rando write bananaport locations."""
from imp import source_from_cache

import js
from randomizer.Lists.Warps import BananaportVanilla
from randomizer.Patching.Patcher import ROM
from randomizer.Spoiler import Spoiler


def randomize_bananaport(spoiler: Spoiler):
    """Rando write bananaport locations."""
    pad_types = [0x214, 0x213, 0x211, 0x212, 0x210]

    if spoiler.settings.bananaport_rando:
        for cont_map in spoiler.bananaport_replacements:
            pad_vanilla = []
            cont_map_id = int(cont_map["containing_map"])
            cont_map_setup_address = js.pointer_addresses[9]["entries"][cont_map_id]["pointing_to"]
            # Pointer Table 9, use "containing_map" as a map index to grab setup start address
            ROM().seek(cont_map_setup_address)
            model2_count = int.from_bytes(ROM().readBytes(4), "big")
            for x in range(model2_count):
                start = cont_map_setup_address + 4 + (x * 0x30)
                ROM().seek(start + 0x28)
                obj_type = int.from_bytes(ROM().readBytes(2), "big")
                if obj_type in pad_types:
                    pad_index = pad_types.index(obj_type)
                    ROM().seek(start + 0x2A)
                    obj_id = int.from_bytes(ROM().readBytes(2), "big")
                    ROM().seek(start + 0)
                    obj_x = int.from_bytes(ROM().readBytes(4), "big")
                    ROM().seek(start + 4)
                    obj_y = int.from_bytes(ROM().readBytes(4), "big")
                    ROM().seek(start + 8)
                    obj_z = int.from_bytes(ROM().readBytes(4), "big")
                    ROM().seek(start + 12)
                    obj_scale = int.from_bytes(ROM().readBytes(4), "big")
                    ROM().seek(start + 0x18)
                    obj_rotx = int.from_bytes(ROM().readBytes(4), "big")
                    ROM().seek(start + 0x1C)
                    obj_roty = int.from_bytes(ROM().readBytes(4), "big")
                    ROM().seek(start + 0x20)
                    obj_rotz = int.from_bytes(ROM().readBytes(4), "big")
                    obj_index = x
                    banned = False
                    for warp in BananaportVanilla.values():
                        if warp.map_id == cont_map_id and warp.obj_id_vanilla == obj_id and warp.locked:
                            banned = True
                    if not banned:
                        pad_vanilla.append(
                            {
                                "pad_index": pad_index,
                                "_id": obj_id,
                                "x": obj_x,
                                "y": obj_y,
                                "z": obj_z,
                                "scale": obj_scale,
                                "rx": obj_rotx,
                                "ry": obj_roty,
                                "rz": obj_rotz,
                                "idx": obj_index,
                            }
                        )
            for y in cont_map["pads"]:
                warp_idx = y["warp_index"]
                repl_ids = y["warp_ids"]
                source_counter = 0
                for repl in repl_ids:
                    for vanilla_pad in pad_vanilla:
                        if vanilla_pad["_id"] == repl:
                            vanilla_idx = vanilla_pad["idx"]
                            start = cont_map_setup_address + (0x30 * vanilla_idx) + 4
                            ref_pad = {}
                            counter = 0
                            for vanilla_pad0 in pad_vanilla:
                                if vanilla_pad0["pad_index"] == warp_idx:
                                    if counter == source_counter:
                                        ref_pad = vanilla_pad0
                                    counter += 1
                            ROM().seek(start + 0x28)
                            ROM().writeMultipleBytes(pad_types[vanilla_pad["pad_index"]], 2)
                            ROM().seek(start + 0)
                            ROM().writeMultipleBytes(ref_pad["x"], 4)
                            ROM().seek(start + 4)
                            ROM().writeMultipleBytes(ref_pad["y"], 4)
                            ROM().seek(start + 8)
                            ROM().writeMultipleBytes(ref_pad["z"], 4)
                            ROM().seek(start + 12)
                            ROM().writeMultipleBytes(ref_pad["scale"], 4)
                            ROM().seek(start + 0x18)
                            ROM().writeMultipleBytes(ref_pad["rx"], 4)
                            ROM().seek(start + 0x1C)
                            ROM().writeMultipleBytes(ref_pad["ry"], 4)
                            ROM().seek(start + 0x20)
                            ROM().writeMultipleBytes(ref_pad["rz"], 4)
                    source_counter += 1
