"""Generate corrected Diddy and Lanky models."""

import zlib
import os
import struct
import gzip


def intf_to_float(intf):
    """Convert float as int format to float."""
    if intf == 0:
        return 0
    else:
        return struct.unpack("!f", bytes.fromhex("{:08X}".format(intf)))[0]


def float_to_hex(f):
    """Convert float to hex."""
    if f == 0:
        return "0x00000000"
    return hex(struct.unpack("<I", struct.pack("<f", f))[0])


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

krusha_adjustment_0 = """
    13 6B
"""

krusha_adjustment_1 = """
    13 66
"""

counter_adjustment_0 = """
    00 00
"""

counter_adjustment_1 = """
    02 16
"""

counter_adjustment_2 = """
    FD EA
"""

modifications = [
    {"model_index": 0, "model_file": "diddy_base.bin", "wipe": [[0x47D0, 0x4878]], "add": [diddy_fix]},
    {"model_index": 1, "model_file": "diddy_ins.bin", "wipe": [[0x4598, 0x4620]], "add": [diddy_fix]},
    {"model_index": 5, "model_file": "lanky_base.bin", "wipe": [[0x5204, 0x5208], [0x541C, 0x5420], [0x56CC, 0x56D0]], "add": [lanky_fix5, lanky_fix5, lanky_fix5]},
    {"model_index": 6, "model_file": "lanky_ins.bin", "wipe": [[0x5BEC, 0x5BF0], [0x5EA4, 0x5EA8], [0x594C, 0x5950], [0x5FEC, 0x5FF0]], "add": [lanky_fix5, lanky_fix5, lanky_fix5, lanky_fix5]},
    {"model_index": 3, "model_file": "dk_base.bin", "wipe": [[0x61A2, 0x61A4]], "add": [dk_adjustment]},
    {"model_index": 8, "model_file": "tiny_base.bin", "wipe": [[0x63D4, 0x63D6]], "add": [tiny_adjustment]},
    {"model_index": 9, "model_file": "tiny_ins.bin", "wipe": [[0x679C, 0x679E]], "add": [tiny_adjustment]},
    {
        "model_index": 0xDA,
        "model_file": "krusha_base.bin",
        "wipe": [[0x2E96, 0x2E98], [0x3A5E, 0x3A60], [0x3126, 0x3128], [0x354E, 0x3550], [0x37FE, 0x3800], [0x41E6, 0x41E8]],
        "add": [krusha_adjustment_0, krusha_adjustment_0, krusha_adjustment_1, krusha_adjustment_1, krusha_adjustment_1, krusha_adjustment_1],
    },
    {
        "model_index": 0xA3,
        "model_file": "counter.bin",
        "wipe": [[0x68, 0x6A], [0x78, 0x7A], [0x88, 0x8A], [0x98, 0x9A], [0xA8, 0xAA], [0xB8, 0xBA], [0xC8, 0xCA], [0xD8, 0xDA]],
        "add": [counter_adjustment_0, counter_adjustment_1, counter_adjustment_1, counter_adjustment_0, counter_adjustment_2, counter_adjustment_2, counter_adjustment_0, counter_adjustment_0],
    },
]

with open(rom_file, "rb") as rom:
    rom.seek(pointer_offset + (5 * 4))
    actor_table = pointer_offset + int.from_bytes(rom.read(4), "big")
    rom.seek(pointer_offset + (4 * 4))
    modeltwo_table = pointer_offset + int.from_bytes(rom.read(4), "big")
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
            fh.seek(0)
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
    for bp_index in range(5):
        file_index = bp_index + 0xDD
        rom.seek(modeltwo_table + (file_index * 4))
        model_start = pointer_offset + int.from_bytes(rom.read(4), "big")
        model_end = pointer_offset + int.from_bytes(rom.read(4), "big")
        model_size = model_end - model_start
        rom.seek(model_start)
        with open(f"blueprint{bp_index}.bin", "wb") as fh:
            compress = rom.read(model_size)
            decompress = zlib.decompress(compress, (15 + 32))
            fh.write(decompress)
        with open(f"blueprint{bp_index}.bin", "r+b") as fh:
            fh.seek(0x48)
            vtx_start = int.from_bytes(fh.read(4), "big")
            vtx_end = int.from_bytes(fh.read(4), "big")
            vtx_count = int((vtx_end - vtx_start) / 0x10)
            for vtx_i in range(vtx_count):
                vtx_addr = vtx_start + (vtx_i * 0x10) + 2
                fh.seek(vtx_addr)
                bp_y = int.from_bytes(fh.read(2), "big")
                if bp_y > 0x7FFF:
                    bp_y -= 65536
                bp_y += 4
                if bp_y < 0:
                    bp_y += 65536
                fh.seek(vtx_addr)
                fh.write(bp_y.to_bytes(2, "big"))
    barrel_skins = (
        "dk",
        "diddy",
        "lanky",
        "tiny",
        "chunky",
        "bp",
        "nin_coin",
        "rw_coin",
        "key",
        "crown",
        "medal",
        "potion",
        "bean",
        "pearl",
        "fairy",
        "rainbow",
        "fakegb",
    )
    rom.seek(actor_table + (0x75 << 2))
    model_start = pointer_offset + int.from_bytes(rom.read(4), "big")
    model_end = pointer_offset + int.from_bytes(rom.read(4), "big")
    model_size = model_end - model_start
    for bi, b in enumerate(barrel_skins):
        rom.seek(model_start)
        with open(f"barrel_skin_{b}.bin", "wb") as fh:
            compress = rom.read(model_size)
            decompress = zlib.decompress(compress, (15 + 32))
            fh.write(decompress)
        with open(f"barrel_skin_{b}.bin", "r+b") as fh:
            fh.seek(0x59C)
            fh.write((6026 + (2 * bi) + 1).to_bytes(4, "big"))
            fh.seek(0x63C)
            fh.write((6026 + (2 * bi)).to_bytes(4, "big"))
    # Fake Item - Model Two
    rom.seek(modeltwo_table + (0x74 << 2))
    model_start = pointer_offset + int.from_bytes(rom.read(4), "big")
    model_end = pointer_offset + int.from_bytes(rom.read(4), "big")
    model_size = model_end - model_start
    rom.seek(model_start)
    indic = int.from_bytes(rom.read(2), "big")
    rom.seek(model_start)
    data = rom.read(model_size)
    if indic == 0x1F8B:
        data = zlib.decompress(data, (15 + 32))
    with open("temp.bin", "wb") as fh:
        fh.write(data)
    with open("temp.bin", "r+b") as fh:
        fh.seek(0xF4)
        fh.write((6060).to_bytes(4, "big"))
        fh.seek(0)
        data = fh.read()
    if os.path.exists("temp.bin"):
        os.remove("temp.bin")
    with open("fake_item.bin", "wb") as fh:
        fh.write(data)
    # Fake Item - Actor
    rom.seek(actor_table + (0x68 << 2))
    model_start = pointer_offset + int.from_bytes(rom.read(4), "big")
    model_end = pointer_offset + int.from_bytes(rom.read(4), "big")
    model_size = model_end - model_start
    rom.seek(model_start)
    indic = int.from_bytes(rom.read(2), "big")
    rom.seek(model_start)
    data = rom.read(model_size)
    if indic == 0x1F8B:
        data = zlib.decompress(data, (15 + 32))
    with open("temp.bin", "wb") as fh:
        fh.write(data)
    with open("temp.bin", "r+b") as fh:
        fh.seek(0xACC)
        fh.write((6060).to_bytes(4, "big"))
        fh.seek(0)
        data = fh.read()
    if os.path.exists("temp.bin"):
        os.remove("temp.bin")
    with open("fake_item_actor.bin", "wb") as fh:
        fh.write(data)
