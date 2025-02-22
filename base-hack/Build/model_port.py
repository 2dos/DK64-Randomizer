"""Port models to actors and model two objects, based on inputs of vertices and a display list."""

import os
import zlib

from BuildClasses import ROMPointerFile
from BuildEnums import TableNames, ExtraTextures
from BuildLib import ROMName, intf_to_float, MODEL_DIRECTORY, getBonusSkinOffset

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
    with open(ROMName, "rb") as rom:
        model_f = ROMPointerFile(rom, TableNames.ModelTwoGeometry, base)
        rom.seek(model_f.start)
        data = rom.read(model_f.size)
        if model_f.compressed:
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
    with open(ROMName, "rb") as rom:
        model_f = ROMPointerFile(rom, TableNames.ActorGeometry, base)
        rom.seek(model_f.start)
        data = rom.read(model_f.size)
        if model_f.compressed:
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
                fh.seek(0)
                fg.write(fh.read(0x28))  # Head
                vtx_len = 0
                with open(vtx_file, "rb") as vtx:
                    vtx_data = vtx.read()
                    vtx_len = len(vtx_data)
                    fg.write(vtx_data)
                dl_len = 0
                with open(dl_file, "rb") as dl:
                    dl_data = dl.read()
                    dl_len = len(dl_data)
                    fg.write(dl_data)
                dl_end = fg.tell()
                fg.seek(4)
                dl_end_ptr = dl_end + init_ptr - 0x28
                fg.write(dl_end_ptr.to_bytes(4, "big"))
                diff = dl_end_ptr - init_dl_end_ptr
                fh.seek(8)
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
        with open(ROMName, "rb") as rom:
            model_f = ROMPointerFile(rom, TableNames.ActorGeometry, actor_index)
            rom.seek(model_f.start)
            data = rom.read(model_f.size)
            if model_f.compressed:
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


def portModelTwoToActor(model_two_index: int, input_file: str, output_file: str, base_file_index: int, vtx_bottom_is_zero: bool, scale: float):
    """Port Model Two object to an actor model."""
    if input_file == "":
        # Use Model Two Index
        with open(ROMName, "rb") as rom:
            model_f = ROMPointerFile(rom, TableNames.ModelTwoGeometry, model_two_index)
            rom.seek(model_f.start)
            data = rom.read(model_f.size)
            if model_f.compressed:
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
    # Read vert/dl data
    with open(temp_file, "r+b") as fh:
        fh.seek(0x40)
        dl_start_pointer = int.from_bytes(fh.read(4), "big")
        dl_end_pointer = int.from_bytes(fh.read(4), "big")
        dl_size = dl_end_pointer - dl_start_pointer
        dl_ins_count = int(dl_size / 8)
        vert_start_pointer = int.from_bytes(fh.read(4), "big")
        vert_end_pointer = int.from_bytes(fh.read(4), "big")
        vert_size = vert_end_pointer - vert_start_pointer
        vert_count = int(vert_size / 0x10)
        # Prune DL
        for d in range(dl_ins_count):
            fh.seek(dl_start_pointer + (8 * d))
            # Prune DL of bad instructions and segmented addresses
            instruction = int.from_bytes(fh.read(1), "big")
            if instruction == 1:
                # Change seg address header from 8 to 3
                fh.seek(dl_start_pointer + (d * 8) + 4)
                fh.write((3).to_bytes(1, "big"))
            elif instruction == 0xDA:
                # Remove instruction
                fh.seek(dl_start_pointer + (d * 8))
                fh.write((0).to_bytes(4, "big"))
                # # Change seg address header from 9 to 4
                # fh.seek(dl_start_pointer + (d * 8) + 3)
                # fh.write((3).to_bytes(1, "big"))
                # fh.write((4).to_bytes(1, "big"))
            elif instruction == 3:
                # Remove instruction
                fh.seek(dl_start_pointer + (d * 8))
                fh.write((0).to_bytes(4, "big"))
        # Fix Verts
        if vtx_bottom_is_zero:
            y_offset = None
            for v in range(vert_count):
                fh.seek(vert_start_pointer + (0x10 * v) + 2)
                raw = int.from_bytes(fh.read(2), "big")
                if raw > 0x7FFF:
                    raw -= 0x10000
                if y_offset is None or y_offset > raw:
                    y_offset = raw
            for v in range(vert_count):
                fh.seek(vert_start_pointer + (0x10 * v) + 2)
                raw = int.from_bytes(fh.read(2), "big")
                if raw > 0x7FFF:
                    raw -= 0x10000
                raw -= y_offset
                if raw < 0:
                    raw += 0x10000
                if raw < 0:
                    raw = 0
                elif raw > 0xFFFF:
                    raw = 0xFFFF
                fh.seek(vert_start_pointer + (0x10 * v) + 2)
                fh.write(raw.to_bytes(2, "big"))
        # Write data to temp files
        fh.seek(dl_start_pointer)
        dl_data = b"\xda\x38\x00\x03\x04\x00\x00\x00" + fh.read(dl_size)
        fh.seek(vert_start_pointer)
        vert_data = fh.read(vert_size)
    # Write
    with open("temp.vtx", "wb") as fh:
        fh.write(vert_data)
    with open("temp.dl", "wb") as fh:
        fh.write(dl_data)
    portalModel_Actor("temp.vtx", "temp.dl", output_file, base_file_index)
    for f in ("temp.vtx", "temp.dl", "temp.bin"):
        if os.path.exists(f):
            os.remove(f)


def createSpriteModelTwo(new_image: int, scaling: float, output_file: str):
    """Create a model two object based on a singular image."""
    with open(ROMName, "rb") as rom:
        model_f = ROMPointerFile(rom, TableNames.ModelTwoGeometry, 436)
        rom.seek(model_f.start)
        data = rom.read(model_f.size)
        if model_f.compressed:
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


def ripCollision(collision_source_model: int, output_model: int, output_file: str):
    """Rips collision from one file (collision_source_model), transplanting it onto a base of another model (output_model) which can be written to an output file."""
    with open(ROMName, "rb") as rom:
        source = ROMPointerFile(rom, TableNames.ActorGeometry, collision_source_model)
        base = ROMPointerFile(rom, TableNames.ActorGeometry, output_model)
        rom.seek(source.start)
        source_data = rom.read(source.size)
        if source.compressed:
            source_data = zlib.decompress(source_data, (15 + 32))
        rom.seek(base.start)
        base_data = rom.read(base.size)
        if base.compressed:
            base_data = zlib.decompress(base_data, (15 + 32))
        with open(f"{output_file}_om1.bin", "wb") as fh:
            fh.write(base_data)
        col_data = None
        col_size = None
        with open(f"{output_file}_om1.bin", "rb") as fh:
            ptr_start = int.from_bytes(fh.read(4), "big")
            fh.seek(0xC)
            col_start = (int.from_bytes(fh.read(4), "big") - ptr_start) + 0x28
            col_end = (int.from_bytes(fh.read(4), "big") - ptr_start) + 0x28
            col_size = col_end - col_start
            fh.seek(col_start)
            col_data = fh.read(col_size)
        with open(f"{output_file}_om1.bin", "wb") as fh:
            fh.write(source_data)
        head_data = None
        foot_data = None
        increase = None
        with open(f"{output_file}_om1.bin", "rb") as fh:
            ptr_start = int.from_bytes(fh.read(4), "big")
            fh.seek(0xC)
            col_start = (int.from_bytes(fh.read(4), "big") - ptr_start) + 0x28
            col_end = (int.from_bytes(fh.read(4), "big") - ptr_start) + 0x28
            fh.seek(0)
            head_data = fh.read(col_start)
            fh.seek(col_end)
            foot_data = fh.read()
            increase = col_size - (col_end - col_start)
        with open(f"{output_file}_om1.bin", "wb") as fh:
            fh.write(head_data)
            fh.write(col_data)
            fh.write(foot_data)
        with open(f"{output_file}_om1.bin", "r+b") as fh:
            fh.seek(0x10)
            old = int.from_bytes(fh.read(4), "big")
            fh.seek(0x10)
            fh.write((old + increase).to_bytes(4, "big"))


def createMelon():
    """Create melon model based off pearl."""
    with open(ROMName, "rb") as rom:
        with open("melon_3d_om2.bin", "wb") as fh:
            pearl = ROMPointerFile(rom, TableNames.ModelTwoGeometry, 0x1B4)
            rom.seek(pearl.start)
            pearl_data = rom.read(pearl.size)
            if pearl.compressed:
                pearl_data = zlib.decompress(pearl_data, (15 + 32))
            fh.write(pearl_data)
        with open("melon_3d_om2.bin", "r+b") as fh:
            fh.seek(0xEC)
            fh.write(getBonusSkinOffset(ExtraTextures.MelonSurface).to_bytes(4, "big"))


def loadNewModels():
    """Load new models."""
    with open(f"{MODEL_DIRECTORY}rainbow_coin.dl", "r+b") as fh:
        fh.seek(0x74)
        fh.write(getBonusSkinOffset(ExtraTextures.RainbowCoin0).to_bytes(4, "big"))
        fh.seek(0xEC)
        fh.write(getBonusSkinOffset(ExtraTextures.RainbowCoin1).to_bytes(4, "big"))
        fh.seek(0x154)
        fh.write(getBonusSkinOffset(ExtraTextures.RainbowCoin2).to_bytes(4, "big"))
        fh.seek(0x1FC)
        fh.write(getBonusSkinOffset(ExtraTextures.RainbowCoin2).to_bytes(4, "big"))
        fh.seek(0x2D4)
        fh.write(getBonusSkinOffset(ExtraTextures.RainbowCoin0).to_bytes(4, "big"))
        fh.seek(0x34C)
        fh.write(getBonusSkinOffset(ExtraTextures.RainbowCoin1).to_bytes(4, "big"))
    with open(f"{MODEL_DIRECTORY}melon.dl", "r+b") as fh:
        fh.seek(0x144)
        fh.write(getBonusSkinOffset(ExtraTextures.MelonSurface).to_bytes(4, "big"))
        fh.seek(0x164)
        fh.write(getBonusSkinOffset(ExtraTextures.MelonSurface).to_bytes(4, "big"))
        fh.seek(0x2EC)
        fh.write(getBonusSkinOffset(ExtraTextures.MelonSurface).to_bytes(4, "big"))
        fh.seek(0x30C)
        fh.write(getBonusSkinOffset(ExtraTextures.MelonSurface).to_bytes(4, "big"))
    # Coins
    portalModel_M2(f"{MODEL_DIRECTORY}coin.vtx", f"{MODEL_DIRECTORY}nin_coin.dl", f"{MODEL_DIRECTORY}coin_overlay.dl", "nintendo_coin", 0x90)
    portalModel_M2(f"{MODEL_DIRECTORY}coin.vtx", f"{MODEL_DIRECTORY}rw_coin.dl", f"{MODEL_DIRECTORY}coin_overlay.dl", "rareware_coin", 0x90)
    portalModel_M2(f"{MODEL_DIRECTORY}coin.vtx", f"{MODEL_DIRECTORY}rainbow_coin.dl", f"{MODEL_DIRECTORY}coin_overlay.dl", "rainbow_coin", 0x90)
    # Fairy
    portActorToModelTwo(0x3C, "", "fairy", 0x90, True, 0.5)
    # Melon
    # portalModel_M2(f"{MODEL_DIRECTORY}melon.vtx", f"{MODEL_DIRECTORY}melon.dl", 0, "melon", 0x90)
    createSpriteModelTwo(getBonusSkinOffset(ExtraTextures.MelonSurface), 0.6, "melon")
    # Potions
    for kong in ("dk", "diddy", "lanky", "tiny", "chunky", "any"):
        portalModel_M2(f"{MODEL_DIRECTORY}potion_{kong}.vtx", f"{MODEL_DIRECTORY}potion.dl", 0, f"potion_{kong}", 0x90)  # Potions - Model 2
        portalModel_Actor(f"{MODEL_DIRECTORY}potion_{kong}.vtx", None, f"potion_{kong}", 0xB8)  # Actors
        if kong != "any":
            portActorToModelTwo(0, f"hint_item_actor_{kong}.bin", f"question_mark_{kong}", 0x90, True, 0.5)
    # Kongs
    portActorToModelTwo(3, "dk_base.bin", "kong_dk", 0x90, True, 0.5)
    portActorToModelTwo(0, "", "kong_diddy", 0x90, True, 0.5)
    portActorToModelTwo(5, "lanky_base.bin", "kong_lanky", 0x90, True, 0.5)
    portActorToModelTwo(8, "tiny_base.bin", "kong_tiny", 0x90, True, 0.5)
    portActorToModelTwo(0xB, "", "kong_chunky", 0x90, True, 0.5)

    # portalModel_M2(f"{MODEL_DIRECTORY}dk_head.vtx", f"{MODEL_DIRECTORY}dk_head.dl", 0, "kong_dk", 0x90)
    # ripCollision(0x48, 0x67, "k_rool_cutscenes")
    # Misc
    portModelTwoToActor(0x198, "", "bean", 0x68, True, 1.0)
    portModelTwoToActor(0x1B4, "", "pearl", 0x68, True, 1.0)
    portModelTwoToActor(0x90, "", "medal", 0x68, True, 1.0)
    portModelTwoToActor(0, "nintendo_coin_om2.bin", "nintendo_coin", 0x68, True, 1.0)
    portModelTwoToActor(0, "rareware_coin_om2.bin", "rareware_coin", 0x68, True, 1.0)
    createMelon()
    portModelTwoToActor(0, "melon_3d_om2.bin", "melon_3d", 0x68, True, 1.0)
    portModelTwoToActor(694, "", "race_hoop", 0xC0, False, 1.0)
    # Shop Owners
    portActorToModelTwo(0x10, "", "cranky", 0x90, True, 0.5)
    portActorToModelTwo(0x11, "", "funky", 0x90, True, 0.5)
    portActorToModelTwo(0x12, "", "candy", 0x90, True, 0.5)
    portActorToModelTwo(0x1E, "", "snide", 0x90, True, 0.5)
    # portModelTwoToActor(0, "rainbow_coin_om2.bin", "rainbow_coin", 0x68, True, 1.0)
