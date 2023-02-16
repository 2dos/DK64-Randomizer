"""Port models to actors and model two objects, based on inputs of vertices and a display list."""

import zlib
import os
from BuildLib import intf_to_float, main_pointer_table_offset

rom_file = "rom/dk64.z64"
temp_file = "temp.bin"
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
        rom.seek(main_pointer_table_offset + (m2_table * 4))
        table = main_pointer_table_offset + int.from_bytes(rom.read(4), "big")
        rom.seek(table + (base * 4))
        start = main_pointer_table_offset + (int.from_bytes(rom.read(4), "big") & 0x7FFFFFFF)
        finish = main_pointer_table_offset + (int.from_bytes(rom.read(4), "big") & 0x7FFFFFFF)
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
        rom.seek(main_pointer_table_offset + (ac_table * 4))
        table = main_pointer_table_offset + int.from_bytes(rom.read(4), "big")
        rom.seek(table + (base * 4))
        start = main_pointer_table_offset + (int.from_bytes(rom.read(4), "big") & 0x7FFFFFFF)
        finish = main_pointer_table_offset + (int.from_bytes(rom.read(4), "big") & 0x7FFFFFFF)
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


def portActorToModelTwo(actor_index: int, input_file: str, output_file: str, base_file_index: int, vtx_bottom_is_zero: bool, scale: float):
    """Port Actor to Model Two."""
    if input_file == "":
        # Use Actor Index
        with open(rom_file, "rb") as rom:
            rom.seek(main_pointer_table_offset + (ac_table * 4))
            table = main_pointer_table_offset + int.from_bytes(rom.read(4), "big")
            rom.seek(table + (actor_index * 4))
            start = main_pointer_table_offset + (int.from_bytes(rom.read(4), "big") & 0x7FFFFFFF)
            finish = main_pointer_table_offset + (int.from_bytes(rom.read(4), "big") & 0x7FFFFFFF)
            size = finish - start
            rom.seek(start)
            data = rom.read(size)
            rom.seek(start)
            indic = int.from_bytes(rom.read(2), "big")
            if indic == 0x1F8B:
                data = zlib.decompress(data, (15 + 32))
            with open(temp_file, "wb") as fh:
                fh.write(data)
    else:
        # Use provided input file
        with open(input_file, "rb") as fh:
            with open(temp_file, "wb") as fg:
                fg.write(fh.read())
    vert_data = b""
    dl_data = b""
    with open(temp_file, "r+b") as fh:
        offset = int.from_bytes(fh.read(4), "big")
        dl_end = (int.from_bytes(fh.read(4), "big") + 0x28) - offset
        bone_start = (int.from_bytes(fh.read(4), "big") + 0x28) - offset
        fh.seek(0x10)
        texturing_start = (int.from_bytes(fh.read(4), "big") + 0x28) - offset
        fh.seek(0x20)
        bone_count = int.from_bytes(fh.read(1), "big")
        fh.seek(dl_end)
        vert_end = (int.from_bytes(fh.read(4), "big") + 0x28) - offset
        vert_count = int((vert_end - 0x28) / 0x10)
        dl_count = int((dl_end - vert_end) / 8)
        vert_bones = []
        bone_offsets = []
        bone_master = [0] * bone_count
        bone_bases = []
        for b in range(bone_count):
            vert_bones.append([])  # Can't do [[]] * bone_count because of referencing errors
            bone_offsets.append([0, 0, 0])  # Same ^
            bone_bases.append([0, 0, 0])  # Same ^
        bone_index = 0
        used_verts = []
        # Grab Verts which are assigned to each bone
        for d in range(dl_count):
            ins_start = vert_end + (d * 8)
            fh.seek(ins_start)
            instruction = int.from_bytes(fh.read(1), "big")
            if instruction == 0xDA:
                fh.seek(ins_start + 6)
                bone_index = int(int.from_bytes(fh.read(2), "big") / 0x40)
            elif instruction == 1:
                fh.seek(ins_start + 1)
                loaded_vert_count = int.from_bytes(fh.read(2), "big") >> 4
                fh.seek(ins_start + 6)
                loaded_vert_start = int(int.from_bytes(fh.read(2), "big") / 0x10)
                for v in range(loaded_vert_count):
                    focused_vert = loaded_vert_start + v
                    if focused_vert not in used_verts:
                        used_verts.append(focused_vert)
                    # else:
                    #     print(f"{focused_vert} already used (Actor {actor_index})")
                    vert_bones[bone_index].append(focused_vert)
        # Grab Bones
        for b in range(bone_count):
            fh.seek(bone_start + (b * 0x10))
            base_bone = int.from_bytes(fh.read(1), "big")
            local_bone = int.from_bytes(fh.read(1), "big")
            master_bone = int.from_bytes(fh.read(1), "big")
            coords = [0, 0, 0]
            if base_bone != 0xFF:
                coords = bone_offsets[base_bone].copy()
            fh.seek(bone_start + (b * 0x10) + 4)
            for c in range(3):
                coords[c] += intf_to_float(int.from_bytes(fh.read(4), "big"))
            bone_offsets[local_bone] = coords.copy()
            bone_bases[master_bone] = coords.copy()
            bone_master[local_bone] = master_bone
        # Get bottom of model (vtx)
        bottom = 99999
        for v in range(vert_count):
            fh.seek(0x28 + (0x10 * v) + 2)
            val = int.from_bytes(fh.read(2), "big")
            if val > 32767:
                val -= 65536
            if bottom > val:
                bottom = val
        # Change verts to account for bones
        for bone_local_index, bone in enumerate(vert_bones):
            for vert in bone:
                fh.seek(0x28 + (vert * 0x10))
                coords = []
                for c in range(3):
                    val = int.from_bytes(fh.read(2), "big")
                    if val > 32767:
                        val -= 65536
                    val += bone_offsets[bone_local_index][c]
                    if vtx_bottom_is_zero and c == 1:
                        val -= bottom
                    val *= scale
                    if val < 0:
                        val += 65536
                    coords.append(int(val))
                fh.seek(0x28 + (vert * 0x10))
                for c in coords:
                    fh.write(c.to_bytes(2, "big"))
        # Get Dynamic Textures
        fh.seek(texturing_start)
        dyn_tex = {}
        dyn_tex_count = int.from_bytes(fh.read(2), "big")
        for d in range(dyn_tex_count):
            tex_count = int.from_bytes(fh.read(2), "big")
            header = int.from_bytes(fh.read(2), "big")
            layers = int.from_bytes(fh.read(2), "big")
            dyn_tex[header] = []
            for layer in range(layers):
                for tex in range(tex_count):
                    dyn_tex[header].append(int.from_bytes(fh.read(2), "big"))
        # Prune DL of bad instructions and segmented addresses
        for d in range(dl_count):
            fh.seek(vert_end + (d * 8))
            instruction = int.from_bytes(fh.read(1), "big")
            if instruction in (0xDA, 0xDE):
                # Wipe mtx transforms and end_dl stuff
                fh.seek(vert_end + (d * 8))
                fh.write((0).to_bytes(8, "big"))
            elif instruction == 1:
                # Change seg address header from 3 to 8
                fh.seek(vert_end + (d * 8) + 4)
                fh.write((8).to_bytes(1, "big"))
            elif instruction == 0xFD:
                # Handle Dynamic Texturing
                fh.seek(vert_end + (d * 8) + 4)
                seg = int.from_bytes(fh.read(1), "big")
                if seg in dyn_tex:
                    fh.seek(vert_end + (d * 8) + 4)
                    fh.write(dyn_tex[seg][0].to_bytes(4, "big"))
        # Get vert data and dl data for porting
        fh.seek(0x28)
        vert_data = fh.read(vert_end - 0x28)
        dl_data = fh.read(dl_end - vert_end)
    with open("temp.vtx", "wb") as fh:
        fh.write(vert_data)
    with open("temp.dl", "wb") as fh:
        fh.write(dl_data)
    portalModel_M2("temp.vtx", "temp.dl", 0, output_file, base_file_index)
    for f in ("temp.vtx", "temp.dl", "temp.bin"):
        if os.path.exists(f):
            os.remove(f)


def createSpriteModelTwo(new_image: int, scaling: float, output_file: str):
    """Create a model two object based on a singular image."""
    with open(rom_file, "rb") as rom:
        rom.seek(main_pointer_table_offset + (m2_table * 4))
        table = main_pointer_table_offset + int.from_bytes(rom.read(4), "big")
        rom.seek(table + (436 * 4))
        start = main_pointer_table_offset + (int.from_bytes(rom.read(4), "big") & 0x7FFFFFFF)
        finish = main_pointer_table_offset + (int.from_bytes(rom.read(4), "big") & 0x7FFFFFFF)
        size = finish - start
        rom.seek(start)
        data = rom.read(size)
        rom.seek(start)
        indic = int.from_bytes(rom.read(2), "big")
        if indic == 0x1F8B:
            data = zlib.decompress(data, (15 + 32))
        with open(f"{output_file}_om2.bin", "wb") as fh:
            fh.write(data)
        with open(f"{output_file}_om2.bin", "r+b") as fh:
            fh.seek(0xEC)
            fh.write(new_image.to_bytes(4, "big"))
            for v in range(0x3E, 0x92):
                for c in range(3):
                    fh.seek((v * 0x10) + (c * 2))
                    val = int.from_bytes(fh.read(2), "big")
                    if val > 32767:
                        val -= 65536
                    val = int(val * scaling)
                    if val < 0:
                        val += 65536
                    fh.seek((v * 0x10) + (c * 2))
                    fh.write(val.to_bytes(2, "big"))


model_dir = "assets/models/"
# Coins
portalModel_M2(f"{model_dir}coin.vtx", f"{model_dir}nin_coin.dl", f"{model_dir}coin_overlay.dl", "nintendo_coin", 0x90)
portalModel_M2(f"{model_dir}coin.vtx", f"{model_dir}rw_coin.dl", f"{model_dir}coin_overlay.dl", "rareware_coin", 0x90)
portalModel_M2(f"{model_dir}coin.vtx", f"{model_dir}rainbow_coin.dl", f"{model_dir}coin_overlay.dl", "rainbow_coin", 0x90)
# Fairy
portActorToModelTwo(0x3C, "", "fairy", 0x90, True, 0.5)
# Melon
# portalModel_M2(f"{model_dir}melon.vtx", f"{model_dir}melon.dl", 0, "melon", 0x90)
createSpriteModelTwo(0x17B2, 0.6, "melon")
# Potions
for kong in ("dk", "diddy", "lanky", "tiny", "chunky", "any"):
    portalModel_M2(f"{model_dir}potion_{kong}.vtx", f"{model_dir}potion.dl", 0, f"potion_{kong}", 0x90)  # Potions - Model 2
    portalModel_Actor(f"{model_dir}potion_{kong}.vtx", None, f"potion_{kong}", 0xB8)  # Actors
# Kongs
portActorToModelTwo(3, "dk_base.bin", "kong_dk", 0x90, True, 0.5)
portActorToModelTwo(0, "diddy_base.bin", "kong_diddy", 0x90, True, 0.5)
portActorToModelTwo(5, "lanky_base.bin", "kong_lanky", 0x90, True, 0.5)
portActorToModelTwo(8, "tiny_base.bin", "kong_tiny", 0x90, True, 0.5)
portActorToModelTwo(0xB, "", "kong_chunky", 0x90, True, 0.5)
# portalModel_M2(f"{model_dir}dk_head.vtx", f"{model_dir}dk_head.dl", 0, "kong_dk", 0x90)
