"""Generate corrected Diddy and Lanky models."""

import os
import zlib
import math

from BuildEnums import TableNames, ExtraTextures
from BuildLib import ROMName, float_to_hex, intf_to_float, main_pointer_table_offset, barrel_skins, getBonusSkinOffset, INSTRUMENT_PADS

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

kong_models = [0, 0, 0, 0, 0]
DK_SCALE = 0.75
GENERIC_SCALE = 0.49
krusha_scaling = [
    # [x, y, z, xz, y]
    # DK
    [lambda x: x * DK_SCALE, lambda x: x * DK_SCALE, lambda x: x * GENERIC_SCALE, lambda x: x * DK_SCALE, lambda x: x * DK_SCALE],
    # Diddy
    [lambda x: (x * 1.043) - 41.146, lambda x: (x * 9.893) - 8.0, lambda x: x * GENERIC_SCALE, lambda x: (x * 1.103) - 14.759, lambda x: (x * 0.823) + 35.220],
    # Lanky
    [lambda x: (x * 0.841) - 17.231, lambda x: (x * 6.925) - 2.0, lambda x: x * GENERIC_SCALE, lambda x: (x * 0.680) - 18.412, lambda x: (x * 0.789) + 42.138],
    # Tiny
    [lambda x: (x * 0.632) + 7.590, lambda x: (x * 6.925) + 0.0, lambda x: x * GENERIC_SCALE, lambda x: (x * 1.567) - 21.676, lambda x: (x * 0.792) + 41.509],
    # Chunky
    [lambda x: x, lambda x: x, lambda x: x, lambda x: x, lambda x: x],
]

kong_pairing = [
    (3, None),  # DK
    (0, 1),  # Diddy
    (5, 6),  # Lanky
    (8, 9),  # Tiny
    (11, 12),  # Chunky
]

model_pairing = {
    1: (3, 3),  # DK
    2: (0, 1),  # Diddy
    3: (5, 6),  # Lanky
    4: (8, 9),  # Tiny
    5: (11, 12),  # Chunky
    6: (13, 0xEC),  # Disco
    7: (0xDA, 0xDA),  # Krusha
    8: (0x113, 0x113),  # K Rool Fight
    9: (0x114, 0x114),  # K Rool Cutscene
}

krusha_kong = -1

BARREL_BASE = 0xE3  # 0x75
BLOCKER_BASE = 0x64
DIRT_BASE = 0xDF

with open(ROMName, "rb") as rom:
    rom.seek(main_pointer_table_offset + (TableNames.ActorGeometry * 4))
    actor_table = main_pointer_table_offset + int.from_bytes(rom.read(4), "big")
    rom.seek(main_pointer_table_offset + (TableNames.ModelTwoGeometry * 4))
    modeltwo_table = main_pointer_table_offset + int.from_bytes(rom.read(4), "big")
    for model in modifications:
        idx = model["model_index"]
        rom.seek(actor_table + (idx * 4))
        model_start = main_pointer_table_offset + int.from_bytes(rom.read(4), "big")
        model_end = main_pointer_table_offset + int.from_bytes(rom.read(4), "big")
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
        model_start = main_pointer_table_offset + int.from_bytes(rom.read(4), "big")
        model_end = main_pointer_table_offset + int.from_bytes(rom.read(4), "big")
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
    # New Bonus Barrel
    rom.seek(actor_table + (BARREL_BASE << 2))
    model_start = main_pointer_table_offset + int.from_bytes(rom.read(4), "big")
    model_end = main_pointer_table_offset + int.from_bytes(rom.read(4), "big")
    model_size = model_end - model_start
    BASE_TEXTURE = 0xC
    rom.seek(model_start)
    with open(f"barrel_skin_base.bin", "wb") as fh:
        compress = rom.read(model_size)
        decompress = zlib.decompress(compress, (15 + 32))
        fh.write(decompress[:-4])
        fh.write((2).to_bytes(2, "big"))
        texture_count = len(barrel_skins)
        if BARREL_BASE == 0x75:
            texture_count += 1
        second_count = 1
        for x in range(2):
            fh.write(texture_count.to_bytes(2, "big"))
            fh.write((BASE_TEXTURE + x).to_bytes(2, "big"))
            fh.write(second_count.to_bytes(2, "big"))
            if BARREL_BASE == 0x75:
                base_texture = 0x128A - x
                fh.write(base_texture.to_bytes(2, "big"))
            for bi in range(len(barrel_skins)):
                fh.write((6026 + (2 * bi) + x).to_bytes(2, "big"))
        raw_size = fh.tell()
        offset = raw_size & 3
        if offset != 0:
            for x in range(4 - offset):
                fh.write((0).to_bytes(1, "big"))
    with open(f"barrel_skin_base.bin", "r+b") as fh:
        fh.seek(0x59C)
        if BARREL_BASE == 0xE3:
            fh.seek(0x13C4)
        fh.write(((BASE_TEXTURE + 1) << 24).to_bytes(4, "big"))  # 1289
        fh.seek(0x63C)
        if BARREL_BASE == 0xE3:
            fh.seek(0x1484)
        fh.write(((BASE_TEXTURE + 0) << 24).to_bytes(4, "big"))  # 128A
        if BARREL_BASE == 0xE3:
            vert_count = int((0xFC8 - 0x28) / 0x10)
            for i in range(vert_count):
                fh.seek(0x28 + (0x10 * i) + 2)
                y = int.from_bytes(fh.read(2), "big")
                if y > 32767:
                    y -= 65536
                ymag = abs(y)
                radius = 0
                if ymag == 72:
                    radius = 45
                elif ymag < 24:
                    radius = 60
                else:
                    diff = ymag - 24
                    diff_range = 72 - 24
                    radius_diff = int((diff / diff_range) * 15)
                    radius = 60 - radius_diff
                fh.seek(0x28 + (0x10 * i))
                x = int.from_bytes(fh.read(2), "big")
                fh.seek(0x28 + (0x10 * i) + 4)
                z = int.from_bytes(fh.read(2), "big")
                if x > 32767:
                    x -= 65536
                if z > 32767:
                    z -= 65536
                normal_radius = math.sqrt((x * x) + (z * z))
                if normal_radius > 10:
                    ratio = radius / normal_radius
                    x = int(x * ratio)
                    z = int(z * ratio)
                    if x < 0:
                        x += 65536
                    if z < 0:
                        z += 65536
                    fh.seek(0x28 + (0x10 * i))
                    fh.write(x.to_bytes(2, "big"))
                    fh.seek(0x28 + (0x10 * i) + 4)
                    fh.write(z.to_bytes(2, "big"))
            fh.seek(0x114C)
            fh.write(getBonusSkinOffset(ExtraTextures.BonusShell).to_bytes(4, "big"))
    # New B. Locker
    rom.seek(actor_table + (BLOCKER_BASE << 2))
    model_start = main_pointer_table_offset + int.from_bytes(rom.read(4), "big")
    model_end = main_pointer_table_offset + int.from_bytes(rom.read(4), "big")
    model_size = model_end - model_start
    BASE_TEXTURE = 0xF
    rom.seek(model_start)
    with open("blocker_base.bin", "wb") as fh:
        compress = rom.read(model_size)
        decompress = zlib.decompress(compress, (15 + 32))
        fh.write(decompress[:0x304C])  # Copy initial data
        number_array = [0x124B + x for x in range(10)]
        texture_arrays = [
            [0xDFB] + number_array,
            [0xDF8] + number_array,
            [0xDF3] + number_array,
            [
                0x1255,  # REQITEM_NONE
                getBonusSkinOffset(ExtraTextures.BLockerItemKong),  # REQITEM_KONG - TODO: Get image for this
                getBonusSkinOffset(ExtraTextures.BLockerItemMove),  # REQITEM_MOVE - TODO: Get image for this
                0x1255,  # REQITEM_GOLDENBANANA
                getBonusSkinOffset(ExtraTextures.BLockerItemBlueprint),  # REQITEM_BLUEPRINT - TODO: Get image for this, sprite image is 48x42 rather than 44x44
                getBonusSkinOffset(ExtraTextures.BLockerItemFairy),  # REQITEM_FAIRY - TODO: Get image for this, sprite image is RGBA32
                0x16F5,  # REQITEM_KEY
                0x1705,  # REQITEM_CROWN
                getBonusSkinOffset(ExtraTextures.BLockerItemCompanyCoin),  # REQITEM_COMPANYCOIN
                0x156D,  # REQITEM_MEDAL
                getBonusSkinOffset(ExtraTextures.BLockerItemBean),  # REQITEM_BEAN - TODO: Get image for this
                getBonusSkinOffset(ExtraTextures.BLockerItemPearl),  # REQITEM_PEARL - TODO: Get image for this
                getBonusSkinOffset(ExtraTextures.BLockerItemRainbowCoin),  # REQITEM_RAINBOWCOIN - TODO: Get image for this, sprite image is 48x42 rather than 44x44
                getBonusSkinOffset(ExtraTextures.BLockerItemIceTrap),  # REQITEM_ICETRAP - TODO: Get image for this
                getBonusSkinOffset(ExtraTextures.BLockerItemPercentage),  # REQITEM_GAMEPERCENTAGE - TODO: Get image for this
                getBonusSkinOffset(ExtraTextures.BLockerItemBalloon),  # REQITEM_COLOREDBANANA
            ],
        ]
        fh.write(len(texture_arrays).to_bytes(2, "big"))
        for arr_index, arr in enumerate(texture_arrays):
            fh.write(len(arr).to_bytes(2, "big"))
            key = 0xC + arr_index
            fh.write(key.to_bytes(2, "big"))
            fh.write((1).to_bytes(2, "big"))
            for item in arr:
                fh.write(item.to_bytes(2, "big"))
        raw_size = fh.tell()
        offset = raw_size & 3
        if offset != 0:
            for x in range(4 - offset):
                fh.write((0).to_bytes(1, "big"))
    with open("blocker_base.bin", "r+b") as fh:
        fh.seek(0x256C)
        fh.write(((BASE_TEXTURE + 0) << 24).to_bytes(4, "big"))
    # New Dirt Patch
    rom.seek(actor_table + (DIRT_BASE << 2))
    model_start = main_pointer_table_offset + int.from_bytes(rom.read(4), "big")
    model_end = main_pointer_table_offset + int.from_bytes(rom.read(4), "big")
    model_size = model_end - model_start
    BASE_TEXTURE = 0xC
    rom.seek(model_start)
    with open("dirt_base.bin", "wb") as fh:
        compress = rom.read(model_size)
        decompress = zlib.decompress(compress, (15 + 32))
        fh.write(decompress[:0xD84])  # Copy initial data
        dirt_reward_array = [x + 6026 + (2 * len(barrel_skins)) for x in range(len(barrel_skins))]
        texture_arrays = [[0x1379] + dirt_reward_array]
        fh.write(len(texture_arrays).to_bytes(2, "big"))
        for arr_index, arr in enumerate(texture_arrays):
            fh.write(len(arr).to_bytes(2, "big"))
            key = 0xC + arr_index
            fh.write(key.to_bytes(2, "big"))
            fh.write((1).to_bytes(2, "big"))
            for item in arr:
                fh.write(item.to_bytes(2, "big"))
        raw_size = fh.tell()
        offset = raw_size & 3
        if offset != 0:
            for x in range(4 - offset):
                fh.write((0).to_bytes(1, "big"))
    with open("dirt_base.bin", "r+b") as fh:
        fh.seek(0x5FC)
        fh.write(((BASE_TEXTURE + 0) << 24).to_bytes(4, "big"))

    # Fake Item - Model Two
    rom.seek(modeltwo_table + (0x74 << 2))
    model_start = main_pointer_table_offset + int.from_bytes(rom.read(4), "big")
    model_end = main_pointer_table_offset + int.from_bytes(rom.read(4), "big")
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
        fh.write(getBonusSkinOffset(ExtraTextures.FakeGBShine).to_bytes(4, "big"))
        fh.seek(0)
        data = fh.read()
    if os.path.exists("temp.bin"):
        os.remove("temp.bin")
    with open("fake_item.bin", "wb") as fh:
        fh.write(data)
    # Fake Item - Actor
    rom.seek(actor_table + (0x87 << 2))
    model_start = main_pointer_table_offset + int.from_bytes(rom.read(4), "big")
    model_end = main_pointer_table_offset + int.from_bytes(rom.read(4), "big")
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
        fh.write(getBonusSkinOffset(ExtraTextures.FakeGBShine).to_bytes(4, "big"))
        fh.seek(0)
        data = fh.read()
    if os.path.exists("temp.bin"):
        os.remove("temp.bin")
    with open("fake_item_actor.bin", "wb") as fh:
        fh.write(data)
    # Multiplayer Pad
    rom.seek(modeltwo_table + (0x214 << 2))
    model_start = main_pointer_table_offset + int.from_bytes(rom.read(4), "big")
    model_end = main_pointer_table_offset + int.from_bytes(rom.read(4), "big")
    model_size = model_end - model_start
    rom.seek(model_start)
    indic = int.from_bytes(rom.read(2), "big")
    rom.seek(model_start)
    data = rom.read(model_size)
    if indic == 0x1F8B:
        data = zlib.decompress(data, (15 + 32))
    with open("temp.bin", "wb") as fh:
        fh.write(data)
    # Beetle squishable enemy
    rom.seek(actor_table + (0x2D << 2))
    model_start = main_pointer_table_offset + int.from_bytes(rom.read(4), "big")
    model_end = main_pointer_table_offset + int.from_bytes(rom.read(4), "big")
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
        texture_alloc = {
            ExtraTextures.BeetleTex0: [0x2424, 0x26CC, 0x29D4, 0x2C64, 0x2F0C, 0x3214, 0x3414],
            ExtraTextures.BeetleTex1: [0x23A4, 0x2B84, 0x3534],
            ExtraTextures.BeetleTex2: [0x1DDC, 0x249C, 0x279C, 0x2AA4, 0x2CDC, 0x2FDC, 0x32E4],
            ExtraTextures.BeetleTex3: [0x2164, 0x2284],
            ExtraTextures.BeetleTex4: [0x1FA4, 0x2204, 0x232C],
            ExtraTextures.BeetleTex5: [0x204C, 0x2574, 0x287C, 0x2DB4, 0x30BC],
            ExtraTextures.BeetleTex6: [0x2624, 0x292C, 0x2E64, 0x316C],
        }
        for tex in texture_alloc:
            for write_loc in texture_alloc[tex]:
                fh.seek(write_loc)
                fh.write(getBonusSkinOffset(tex).to_bytes(4, "big"))
        fh.seek(0)
        data = fh.read()
    if os.path.exists("temp.bin"):
        os.remove("temp.bin")
    with open("scarab_actor.bin", "wb") as fh:
        fh.write(data)

    for obj_id in INSTRUMENT_PADS:
        file_name = INSTRUMENT_PADS[obj_id]
        rom.seek(modeltwo_table + (obj_id << 2))
        model_start = main_pointer_table_offset + int.from_bytes(rom.read(4), "big")
        model_end = main_pointer_table_offset + int.from_bytes(rom.read(4), "big")
        model_size = model_end - model_start
        rom.seek(model_start)
        indic = int.from_bytes(rom.read(2), "big")
        rom.seek(model_start)
        data = rom.read(model_size)
        if indic == 0x1F8B:
            data = zlib.decompress(data, (15 + 32))
        with open(f"{file_name}_pad.bin", "wb") as fh:
            fh.write(data)
        with open(f"{file_name}_pad.bin", "r+b") as fh:
            fh.seek(0x50)
            floor_start = int.from_bytes(fh.read(4), "big")
            fh.seek(floor_start)
            floor_count = int.from_bytes(fh.read(4), "big")
            for x in range(floor_count):
                tri_start = floor_start + 0x10 + (0x18 * x)
                fh.seek(tri_start + 0x15)
                fh.write((2).to_bytes(1, "big"))

    # Base tex:
    #
    # Top
    # 0xEC (0xDF9), 0x164 (0xDFA)
    #
    # Rim
    # 0x1CE (0xBB2), 0x274 (0xBB3)
    #
    # Number
    # 0x374 (0xDFB)
