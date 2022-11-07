"""Port models to actors and model two objects, based on inputs of vertices and a display list."""

import zlib
import os

rom_file = "rom/dk64.z64"
temp_file = "temp.bin"
ptr_offset = 0x101C50
m2_table = 4
ac_table = 5

# Conversions:
# Load vertices Seg Start:
# - Actor: 0x3
# - M2: 0x8
# G_MTX:
# - Actor: 0x4
# - M2: 0x9
# G_DL:
# - Actor: 0x5
# - M2: ?


class BoneVertex:
    """Store information relating to bone vertices in actors."""

    def __init__(self, start, count):
        """Initialize with given data."""
        self.start = start
        self.count = count


def portalModel_M2(vtx_file, dl_file, overlay_dl_file, model_name, base):
    """Convert model two model file from various source files."""
    with open(rom_file, "rb") as rom:
        rom.seek(ptr_offset + (m2_table * 4))
        table = ptr_offset + int.from_bytes(rom.read(4), "big")
        rom.seek(table + (base * 4))
        start = ptr_offset + (int.from_bytes(rom.read(4), "big") & 0x7FFFFFFF)
        finish = ptr_offset + (int.from_bytes(rom.read(4), "big") & 0x7FFFFFFF)
        size = finish - start
        rom.seek(start)
        data = rom.read(size)
        rom.seek(start)
        indic = int.from_bytes(rom.read(2), "big")
        if indic == 0x1F8B:
            data = zlib.decompress(data, (15 + 32))
        with open(temp_file, "wb") as fh:
            fh.write(data)
    with open(temp_file, "rb") as fh:
        with open(f"{model_name}_om2.bin", "wb") as fg:
            fh.seek(0x40)
            dl_start = int.from_bytes(fh.read(4), "big")
            fh.seek(0)
            head = fh.read(dl_start)
            fg.write(head)
            dl_data_length = 0
            with open(dl_file, "rb") as dl:
                dl_data = dl.read()
                dl_data_length = len(dl_data)
                fg.write(dl_data)
            dl_addon_length = 0
            if overlay_dl_file != 0:
                with open(overlay_dl_file, "rb") as dl:
                    dl_addon = dl.read()
                    dl_addon_length = len(dl_addon)
                    fg.write(dl_addon)
            else:
                dl_addon_length = 8
                fg.write((0xDF << 56).to_bytes(8, "big"))
            vtx_data_length = 0
            with open(vtx_file, "rb") as vtx:
                vtx_data = vtx.read()
                vtx_data_length = len(vtx_data)
                fg.write(vtx_data)
            fh.seek(0x4C)
            file_extra_data_start = int.from_bytes(fh.read(4), "big")
            fh.seek(file_extra_data_start)
            file_extra_data = fh.read()
            fg.write(file_extra_data)
            fg.seek(0x44)
            pointer = dl_start + dl_data_length
            fg.write(pointer.to_bytes(4, "big"))
            pointer += dl_addon_length
            fg.write(pointer.to_bytes(4, "big"))
            pointer += vtx_data_length
            fh.seek(0x4C)
            old = int.from_bytes(fh.read(4), "big")
            fg.write(pointer.to_bytes(4, "big"))
            diff = pointer - old
            iterations = int(((dl_start - 1) - 0x50) / 4)
            for i in range(iterations):
                old = int.from_bytes(fh.read(4), "big")
                fg.write((old + diff).to_bytes(4, "big"))
    if os.path.exists(temp_file):
        os.remove(temp_file)


def portalModel_Actor(vtx_file, dl_file, model_name, base):
    """Create actor file from various source files."""
    with open(rom_file, "rb") as rom:
        rom.seek(ptr_offset + (ac_table * 4))
        table = ptr_offset + int.from_bytes(rom.read(4), "big")
        rom.seek(table + (base * 4))
        start = ptr_offset + (int.from_bytes(rom.read(4), "big") & 0x7FFFFFFF)
        finish = ptr_offset + (int.from_bytes(rom.read(4), "big") & 0x7FFFFFFF)
        size = finish - start
        rom.seek(start)
        data = rom.read(size)
        rom.seek(start)
        indic = int.from_bytes(rom.read(2), "big")
        if indic == 0x1F8B:
            data = zlib.decompress(data, (15 + 32))
        with open(temp_file, "wb") as fh:
            fh.write(data)
    with open(temp_file, "rb") as fh:
        with open(f"{model_name}_om1.bin", "w+b") as fg:
            if dl_file is None:
                fg.write(fh.read())
                fg.seek(0x28)
                upscale = 10
                with open(vtx_file, "rb") as vtx:
                    vtx_data = vtx.read()
                    vtx_len = int(len(vtx_data) / 0x10)
                    fg.write(vtx_data)
                    vtx_end = fg.tell()
                    for vtx_item in range(vtx_len):
                        for c in range(3):
                            fg.seek((vtx_item * 0x10) + 0x28 + (2 * c))
                            c_v = int.from_bytes(fg.read(2), "big")
                            if c_v > 32767:
                                c_v -= 65536
                            c_v *= upscale
                            fg.seek((vtx_item * 0x10) + 0x28 + (2 * c))
                            if c_v < 0:
                                c_v += 65536
                            fg.write(c_v.to_bytes(2, "big"))
            else:
                fh.seek(0)
                init_ptr = int.from_bytes(fh.read(4), "big")
                init_dl_end_ptr = int.from_bytes(fh.read(4), "big")
                fg.write(fh.read(0x28))  # Head
                vtx_len = 0
                with open(vtx_file, "rb") as vtx:
                    vtx_data = vtx.read()
                    vtx_len = len(vtx_data)
                    fg.write(vtx_data)
                dl_len = 0
                with open(dl_file, "rb") as dl:
                    dl_data = dl.read()[0x30:]
                    dl_len = len(dl_data)
                    fg.write(dl_data)
                dl_end = fg.tell()
                fg.seek(4)
                dl_end_ptr = dl_end + init_ptr - 0x28
                fg.write(dl_end_ptr.to_bytes(4, "big"))
                diff = dl_end_ptr - init_dl_end_ptr
                for i in range(3):
                    old = int.from_bytes(fh.read(4), "big")
                    fg.write((old + diff).to_bytes(4, "big"))
                fg.seek(dl_end)
                fg.write((init_ptr + vtx_len).to_bytes(4, "big"))
                fh.seek(init_dl_end_ptr + 0x2C - init_ptr)
                fg.write(fh.read())
    if os.path.exists(temp_file):
        os.remove(temp_file)


def portKongDL(base_file, new_file, base_vtx, new_vtx, dyn_textures, vtx_adjustments):
    """Port Kong DL to Model Two."""
    bone_slot = 0
    bone_vtx_lst = []
    bone_vtx = []
    vtx_load_count = 0
    current_vtx_start = 0
    loaded_vtx = [0] * 32
    with open(new_file, "w+b") as new:
        data = [
            0x01008010,
            0x08000710,
            0x03000000,
            0x0000000E,
        ]
        # for d in data:
        #     new.write(d.to_bytes(4, "big"))
        with open(base_file, "rb") as old:
            new.write(old.read())
        dl_count = int(new.tell() / 0x8)
        for func in range(dl_count):
            new.seek(func * 8)
            command_head = int.from_bytes(new.read(1), "big")
            new.seek(func * 8)
            if command_head == 0xDA:
                new.write((0).to_bytes(8, "big"))
            elif command_head == 0xFD:
                new.seek((func * 8) + 4)
                dyn_texture_head = int.from_bytes(new.read(1), "big")
                new.seek((func * 8) + 4)
                if dyn_texture_head in dyn_textures:
                    tex_idx = dyn_textures[dyn_texture_head]
                    new.write(tex_idx.to_bytes(4, "big"))
            elif command_head == 0x01:
                new.seek((func * 8) + 4)
                new.write((8).to_bytes(1, "big"))
                new.seek((func * 8) + 1)
                vtx_chunk_size = (int.from_bytes(new.read(2), "big") >> 4) & 0xFF
                vtx_buffer_load = int.from_bytes(new.read(1), "big") >> 1
                new.seek((func * 8) + 4)
                vtx_chunk_start = int.from_bytes(new.read(4), "big") & 0xFFFFFF
                print(f"{hex(int(vtx_chunk_start / 0x10))}: {hex(vtx_chunk_size)} | {hex(vtx_buffer_load)}")
                current_vtx_start = int(vtx_chunk_start / 0x10)
                vtx_write_start = vtx_buffer_load - vtx_chunk_size
                for i in range(vtx_chunk_size):
                    loaded_vtx[vtx_write_start + i] = int(vtx_chunk_start / 0x10) + i
            elif command_head in (5, 6, 7):
                # Draw Tri/2 Tris
                vtx_list = []
                sub_idx = []
                for i in range(7):
                    if i != 3:
                        if (command_head in (6, 7) and i > 3) or i < 3:
                            new.seek((func * 8) + 1 + i)
                            val = int.from_bytes(new.read(1), "big")
                            vtx_list.append(loaded_vtx[int(val / 2)])
                            sub_idx.append(int(val / 2))
                            vtx_load_count += 1
                print(sub_idx)
                bone_vtx.extend(vtx_list)
            elif command_head == 0xDE:
                new.write((0).to_bytes(8, "big"))
                bone_slot += 1
                bone_vtx_lst.append(bone_vtx)
                bone_vtx = []
                print("NEW BUCKET")
        bone_slot += 1
        bone_set = set(bone_vtx)
        unique_bones = list(bone_set)
        bone_vtx_lst.append(unique_bones)
    # print(len(bone_vtx_lst))
    # print(hex(vtx_load_count))
    print(bone_vtx_lst)
    with open(new_vtx, "w+b") as new:
        with open(base_vtx, "rb") as old:
            new.write(old.read())
        adjusted = []
        base_adj = []
        for adj_idx, adj_mtx in enumerate(vtx_adjustments):
            if adj_idx < len(bone_vtx_lst) and len(adj_mtx) == 3:
                if adj_idx == 0:
                    base_adj = list(adj_mtx)
                else:
                    bone_lst = bone_vtx_lst[adj_idx]
                    for vtx_index in bone_lst:
                        vtx_addr = vtx_index * 0x10
                        if vtx_index not in adjusted:
                            adjusted.append(vtx_index)
                            for c in range(3):
                                new.seek(vtx_addr + (c * 2))
                                val = int.from_bytes(new.read(2), "big")
                                if val > 0x7FFF:
                                    val -= 65536
                                val += list(adj_mtx)[c] + base_adj[c]
                                if val < 0:
                                    val += 65536
                                new.seek(vtx_addr + (c * 2))
                                new.write(val.to_bytes(2, "big"))
        for x in range(max(adjusted)):
            if x not in adjusted:
                vtx_group = -1
                for y_i, y in enumerate(bone_vtx_lst):
                    if x in y:
                        vtx_group = y_i
                print(f"{hex(x)}: {vtx_group}")


model_dir = "assets/Non-Code/models/"
# Coins
portalModel_M2(f"{model_dir}coin.vtx", f"{model_dir}nin_coin.dl", f"{model_dir}coin_overlay.dl", "nintendo_coin", 0x90)
portalModel_M2(f"{model_dir}coin.vtx", f"{model_dir}rw_coin.dl", f"{model_dir}coin_overlay.dl", "rareware_coin", 0x90)
# Potions - Model 2
portalModel_M2(f"{model_dir}potion_dk.vtx", f"{model_dir}potion.dl", 0, "potion_dk", 0x90)
portalModel_M2(f"{model_dir}potion_diddy.vtx", f"{model_dir}potion.dl", 0, "potion_diddy", 0x90)
portalModel_M2(f"{model_dir}potion_lanky.vtx", f"{model_dir}potion.dl", 0, "potion_lanky", 0x90)
portalModel_M2(f"{model_dir}potion_tiny.vtx", f"{model_dir}potion.dl", 0, "potion_tiny", 0x90)
portalModel_M2(f"{model_dir}potion_chunky.vtx", f"{model_dir}potion.dl", 0, "potion_chunky", 0x90)
portalModel_M2(f"{model_dir}potion_any.vtx", f"{model_dir}potion.dl", 0, "potion_any", 0x90)
# Potions - Actors (Ignore Chunky Model)
portalModel_Actor(f"{model_dir}potion_dk.vtx", None, "potion_dk", 0xB8)
portalModel_Actor(f"{model_dir}potion_diddy.vtx", None, "potion_diddy", 0xB8)
portalModel_Actor(f"{model_dir}potion_lanky.vtx", None, "potion_lanky", 0xB8)
portalModel_Actor(f"{model_dir}potion_tiny.vtx", None, "potion_tiny", 0xB8)
portalModel_Actor(f"{model_dir}potion_chunky.vtx", None, "potion_chunky", 0xB8)
portalModel_Actor(f"{model_dir}potion_any.vtx", None, "potion_any", 0xB8)
# Kongs

base = (0, 0, 10)

dk_jaw = (0, -16, 22)  # 03
dk_head = (0, 53, 54)  # 02
dk_tie = (0, 4, 55)  # 05
dk_arm_left0 = (42, 38, 26)  # 08
dk_arm_left1 = (5, -40, -1)  # 09
dk_arm_left2 = (0, -39, 10)  # 0A
dk_arm_right0 = (-42, 38, 26)  # 0D
dk_arm_right1 = (-5, -40, -1)  # 0E
dk_arm_right2 = (0, -39, 10)  # 0F
dk_leg_left0 = (15, -4, -1)  # 13
dk_leg_left1 = (6, -18, 4)  # 14
dk_leg_left2 = (1, -24, -1)  # 15
dk_leg_right0 = (-15, -4, -1)  # 16
dk_leg_right1 = (-6, -18, 4)  # 17
dk_leg_right2 = (-1, -24, -1)  # 18


# portKongDL(f"{model_dir}dk_copy.dl", f"{model_dir}dk.dl", f"{model_dir}dk_copy.vtx", f"{model_dir}dk.vtx", {
#     0xC: 0xE8E,
#     0xD: 0xE8C,
#     0xE: 0x177D
# }, [
#     (0, 0, -54),
#     tuple(map(lambda i, j: i + j, dk_head, dk_jaw)), # Jaw
#     dk_head, # Face Skin
#     dk_head, # Face Fur
#     base, # Tie Knot
#     base, # Torso
#     tuple(map(lambda i, j, k: i + j + k, dk_arm_left0, dk_arm_left1, dk_arm_left2)), # Left Hand
#     tuple(map(lambda i, j: i + j, dk_arm_left0, dk_arm_left1)), # Left Arm
#     tuple(map(lambda i, j, k: i + j + k, dk_arm_right0, dk_arm_right1, dk_arm_right2)), # Right Hand
#     tuple(map(lambda i, j: i + j, dk_arm_right0, dk_arm_right1)),
#     dk_arm_left0,
#     (330, -200, 0), # Right Arm
#     # tuple(map(lambda i, j: i + j, dk_arm_left0, dk_arm_left1)), # ?
#     # tuple(map(lambda i, j, k: i + j + k, dk_arm_left0, dk_arm_left1, dk_arm_left2)), # ?
#     # dk_arm_right0, # Right Leg
#     # tuple(map(lambda i, j: i + j, dk_arm_right0, dk_arm_right1)), # ?
#     # tuple(map(lambda i, j, k: i + j + k, dk_arm_right0, dk_arm_right1, dk_arm_right2)), # ?

#     # (78, 27, 80 ),
#     # (78, 27, 65 ),
#     # (125, 25, 55),
#     # (-1, 36, 62 ),
#     # (-1, 36, 55 ),
#     # (78, 27, 125),
#     # (-17, 1, 30 ),
#     # (-20, 1, 30 ),
#     # (78, 27, 125),
#     # (0, 200, 0  ),
#     # (78, 27, 0  ),
# ])
portalModel_M2(f"{model_dir}dk_head.vtx", f"{model_dir}dk_head.dl", 0, "kong_dk", 0x90)
# portalModel_Actor(f"{model_dir}coin.vtx", f"{model_dir}nin_coin.dl", "nintendo_coin", 0x66)
