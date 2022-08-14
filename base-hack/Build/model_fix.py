"""Generate corrected Diddy and Lanky models."""

import zlib

rom_file = "rom/dk64.z64"
pointer_offset = 0x101C50

diddy_fix = """
    E7 00 00 00 00 00 00 00
    FC 12 18 24 FF 33 FF FF
    D7 00 00 02 08 00 08 00
    FD 10 00 00 0E 00 00 00
    E6 00 00 00 00 00 00 00
    F3 00 00 00 07 3F F1 00
    E7 00 00 00 00 00 00 00
    E3 00 10 01 00 00 00 00
    D9 FF FF FF 00 04 00 00
    DA 38 00 03 04 00 00 40
"""

# lanky_fix = """
#     E7 00 00 00 00 00 00 00
#     E3 00 0A 01 00 10 00 00
#     FC 12 18 24 FF 33 FF FF
#     D9 F9 FF FF 00 00 00 00
#     D7 00 00 02 FF FF FF FF
#     E7 00 00 00 00 00 00 00
#     FD 10 00 00 0D 00 00 00
#     E6 00 00 00 00 00 00 00
#     F3 00 00 00 07 3F F1 00
#     E7 00 00 00 00 00 00 00
#     E3 00 10 01 00 00 00 00
#     D9 FF FF FF 00 02 00 00
#     DA 38 00 03 04 00 03 C0
# """

lanky_fix = """
    E7 00 00 00 00 00 00 00
    FC 12 18 24 FF 33 FF FF
    D7 00 00 02 08 00 08 00
    FD 10 00 00 0D 00 00 00
    E6 00 00 00 00 00 00 00
    F3 00 00 00 07 3F F1 00
    E7 00 00 00 00 00 00 00
    E3 00 10 01 00 00 00 00
    D9 FF FF FF 00 04 00 00
    DA 38 00 03 04 00 03 C0
"""

lanky_fix2 = """
    FD 10 00 00 0D 00 00 00
"""

lanky_fix3 = """
    FC 12 18 24 FF 33 FF FF
    D7 00 00 02 08 00 08 00
    FD 10 00 00 0D 00 00 00
    E6 00 00 00 00 00 00 00
    F3 00 00 00 07 3F F1 00
    E7 00 00 00 00 00 00 00
    E3 00 10 01 00 00 00 00
    D9 FF FF FF 00 04 00 00
"""

lanky_fix4 = """
    FC 12 18 24 FF 33 FF FF
"""

lanky_fix5 = """
    00 00 0E 69
"""

dk_adjustment = """
    17 7D
"""

tiny_adjustment = """
    17 7E
"""

modifications = [
    {"model_index": 0, "model_file": "diddy_base.bin", "wipe": [[0x47D0, 0x4878]], "add": [diddy_fix]},
    {"model_index": 1, "model_file": "diddy_ins.bin", "wipe": [[0x4598, 0x4620]], "add": [diddy_fix]},
    {"model_index": 5, "model_file": "lanky_base.bin", "wipe": [[0x5204, 0x5208], [0x541C, 0x5420], [0x56CC, 0x56D0]], "add": [lanky_fix5, lanky_fix5, lanky_fix5]},
    {
        "model_index": 6,
        "model_file": "lanky_ins.bin",
        "wipe": [[0x5BEC, 0x5BF0], [0x5EA4, 0x5EA8], [0x594C, 0x5950], [0x5FEC, 0x5FF0]],
        "add": [lanky_fix5, lanky_fix5, lanky_fix5, lanky_fix5],
    },
    {"model_index": 3, "model_file": "dk_base.bin", "wipe": [[0x61A2, 0x61A4]], "add": [dk_adjustment]},
    {"model_index": 8, "model_file": "tiny_base.bin", "wipe": [[0x63D4, 0x63D6]], "add": [tiny_adjustment]},
    {"model_index": 9, "model_file": "tiny_ins.bin", "wipe": [[0x679C, 0x679E]], "add": [tiny_adjustment]},
]

with open(rom_file, "rb") as rom:
    rom.seek(pointer_offset + (5 * 4))
    actor_table = pointer_offset + int.from_bytes(rom.read(4), "big")
    for model in modifications:
        idx = model["model_index"]
        rom.seek(actor_table + (idx * 4))
        model_start = pointer_offset + int.from_bytes(rom.read(4), "big")
        model_end = pointer_offset + int.from_bytes(rom.read(4), "big")
        model_size = model_end - model_start
        rom.seek(model_start)
        with open(model["model_file"], "wb") as fh:
            compress = rom.read(model_size)
            decompress = zlib.decompress(compress, (15 + 32))
            fh.write(decompress)
        with open(model["model_file"], "r+b") as fh:
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
                            fix_lst.append(int(f"0x{x}", 16))
                fh.seek(wipe[0])
                fh.write(bytearray(fix_lst))
                sub_idx += 1
