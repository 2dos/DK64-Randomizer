import zlib

rom_file = "../rom/dk64.z64"
pointer_offset = 0x101C50

diddy_fix = """
    E7 00 00 00 00 00 00 00
    E3 00 0A 01 00 10 00 00
    FC 12 18 24 FF 33 FF FF
    D9 F9 FF FF 00 00 00 00
    D7 00 00 02 FF FF FF FF
    E7 00 00 00 00 00 00 00
    FD 10 00 00 0E 00 00 00
    E6 00 00 00 00 00 00 00
    F3 00 00 00 07 3F F1 00
    E7 00 00 00 00 00 00 00
    E3 00 10 01 00 00 00 00
    D9 FF FF FF 00 02 00 00
    DA 38 00 03 04 00 00 40
"""

lanky_fix = """
    E7 00 00 00 00 00 00 00
    E3 00 0A 01 00 10 00 00
    FC 12 18 24 FF 33 FF FF
    D9 F9 FF FF 00 00 00 00
    D7 00 00 02 FF FF FF FF
    E7 00 00 00 00 00 00 00
    FD 10 00 00 0D 00 00 00
    E6 00 00 00 00 00 00 00
    F3 00 00 00 07 3F F1 00
    E7 00 00 00 00 00 00 00
    E3 00 10 01 00 00 00 00
    D9 FF FF FF 00 02 00 00
    DA 38 00 03 04 00 03 C0
"""

lanky_fix2 = """
    FD 10 00 00 0D 00 00 00
"""

modifications = [
    {
        "model_index": 0,
        "model_file": "diddy_base.bin",
        "wipe": [[0x47D0,0x4878]],
        "add": [diddy_fix]
    },
    {
        "model_index": 1,
        "model_file": "diddy_ins.bin",
        "wipe": [[0x4598,0x4620]],
        "add": [diddy_fix]
    },
    {
        "model_index": 5,
        "model_file": "lanky_base.bin",
        "wipe": [[0x50D8,0x5188],[0x51D0,0x5238],[0x5418,0x5420],[0x56C8,0x56D0]],
        "add": [lanky_fix,lanky_fix,lanky_fix2,lanky_fix2]
    },
    {
        "model_index": 6,
        "model_file": "lanky_ins.bin",
        # "wipe": [],
        # "add": []
        # "wipe": [[0x6040,0x60E8],[0x5930,0x5990],[0x5BD8,0x5C30],[0x5E90,0x5EE8]],
        "wipe": [[0x6070,0x6078],[0x5948,0x5950],[0x5BE8,0x5BF0],[0x5EA0,0x5EA8]],
        "add": [lanky_fix2,lanky_fix2,lanky_fix2,lanky_fix2]
    }
]

with open(rom_file,"rb") as rom:
    rom.seek(pointer_offset + (5 * 4))
    actor_table = pointer_offset + int.from_bytes(rom.read(4),"big")
    for model in modifications:
        idx = model["model_index"]
        rom.seek(actor_table + (idx * 4))
        model_start = pointer_offset + int.from_bytes(rom.read(4),"big")
        model_end = pointer_offset + int.from_bytes(rom.read(4),"big")
        model_size = model_end - model_start
        rom.seek(model_start)
        with open(model["model_file"],"wb") as fh:
            compress = rom.read(model_size)
            decompress = zlib.decompress(compress, (15+32))
            fh.write(decompress)
        with open(model["model_file"],"r+b") as fh:
            sub_idx = 0
            for wipe in model["wipe"]:
                fh.seek(wipe[0])
                wipe_size = wipe[1] - wipe[0]
                wipe_lst = []
                for x in range(wipe_size):
                    wipe_lst.append(0)
                fh.write(bytearray(wipe_lst))
                fix_arr = model["add"][sub_idx].split("\n")
                fix_lst = []
                for f in fix_arr:
                    if not f == "":
                        for x in f.strip().split(" "):
                            fix_lst.append(int(f"0x{x}",16))
                fh.seek(wipe[0])
                fh.write(bytearray(fix_lst))
                sub_idx += 1