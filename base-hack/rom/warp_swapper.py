"""Bananaport Swapper."""
bananaport_replacements = [
    {
        "containing_map": 0x14,
        "pads": [
            {
                "warp_index": 0,
                "warp_ids": [0x58, 0x99],
            },
            {
                "warp_index": 1,
                "warp_ids": [0x4E, 0x9A],
            },
        ],
    }
]

pad_types = [0x214, 0x213, 0x211, 0x212, 0x210]

with open("dk64-randomizer-base-dev.z64", "r+b") as fh:
    pad_vanilla = []
    for cont_map in bananaport_replacements:
        aztec_llama_setup = 0x22C331C
        # Pointer Table 9, use "containing_map" as a map index to grab setup start address
        fh.seek(aztec_llama_setup)
        model2_count = int.from_bytes(fh.read(4), "big")
        for x in range(model2_count):
            start = aztec_llama_setup + 4 + (x * 0x30)
            fh.seek(start + 0x28)
            obj_type = int.from_bytes(fh.read(2), "big")
            if obj_type in pad_types:
                pad_index = pad_types.index(obj_type)
                fh.seek(start + 0x2A)
                obj_id = int.from_bytes(fh.read(2), "big")
                fh.seek(start + 0)
                obj_x = int.from_bytes(fh.read(4), "big")
                fh.seek(start + 4)
                obj_y = int.from_bytes(fh.read(4), "big")
                fh.seek(start + 8)
                obj_z = int.from_bytes(fh.read(4), "big")
                fh.seek(start + 12)
                obj_scale = int.from_bytes(fh.read(4), "big")
                fh.seek(start + 0x18)
                obj_rotx = int.from_bytes(fh.read(4), "big")
                fh.seek(start + 0x1C)
                obj_roty = int.from_bytes(fh.read(4), "big")
                fh.seek(start + 0x20)
                obj_rotz = int.from_bytes(fh.read(4), "big")
                obj_index = x
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
    for x in bananaport_replacements:
        for y in x["pads"]:
            warp_idx = y["warp_index"]
            repl_ids = y["warp_ids"]
            source_counter = 0
            for repl in repl_ids:
                for vanilla_pad in pad_vanilla:
                    if vanilla_pad["_id"] == repl:
                        vanilla_idx = vanilla_pad["idx"]
                        start = aztec_llama_setup + (0x30 * vanilla_idx) + 4
                        ref_pad = {}
                        counter = 0
                        for vanilla_pad0 in pad_vanilla:
                            if vanilla_pad0["pad_index"] == warp_idx:
                                if counter == source_counter:
                                    ref_pad = vanilla_pad0
                                counter += 1
                        # print("Source Pad:")
                        # print(vanilla_pad)
                        # print("Reference Pad:")
                        # print(ref_pad)
                        fh.seek(start + 0x28)
                        fh.write(pad_types[vanilla_pad["pad_index"]].to_bytes(2, "big"))
                        fh.seek(start + 0)
                        fh.write(ref_pad["x"].to_bytes(4, "big"))
                        fh.seek(start + 4)
                        fh.write(ref_pad["y"].to_bytes(4, "big"))
                        fh.seek(start + 8)
                        fh.write(ref_pad["z"].to_bytes(4, "big"))
                        fh.seek(start + 12)
                        fh.write(ref_pad["scale"].to_bytes(4, "big"))
                        fh.seek(start + 0x18)
                        fh.write(ref_pad["rx"].to_bytes(4, "big"))
                        fh.seek(start + 0x1C)
                        fh.write(ref_pad["ry"].to_bytes(4, "big"))
                        fh.seek(start + 0x20)
                        fh.write(ref_pad["rz"].to_bytes(4, "big"))
                source_counter += 1
