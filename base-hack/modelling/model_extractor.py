"""Model extractor for the purpose of custom models."""

# Process of making a compatible custom model (roadmap - maximum effort, maximum optimism)
# 1. Extract the file from DK64 -> obj and a list of textures in the game
# 2. Go into blender -> fix issues
# 3. .json file -> for each mesh, what part of the body that is
# 3b. -> The connection between x mesh index and y mesh index = this bone joint
# 3c. -> Texture indexes which are used
# 4. .obj / .json -> binary -> dk64
# 4b. -> Validation
# 5. Happy fun times, no crashing, no messages in #5.0-bug-reports
# 6. Happy Ballaam

from enum import IntEnum, auto
import zlib
import struct
import math


class TableNames(IntEnum):
    """Pointer Table Enum."""

    MusicMIDI = 0
    MapGeometry = auto()
    MapWalls = auto()
    MapFloors = auto()
    ModelTwoGeometry = auto()
    ActorGeometry = auto()
    Unknown6 = auto()
    TexturesUncompressed = auto()
    Cutscenes = auto()
    Setups = auto()
    InstanceScripts = auto()
    Animations = auto()
    Text = auto()
    Unknown13 = auto()
    TexturesHUD = auto()
    Paths = auto()
    Spawners = auto()
    DKTVInputs = auto()
    Triggers = auto()
    Unknown19 = auto()
    Unknown20 = auto()
    Autowalks = auto()
    Critters = auto()
    Exits = auto()
    RaceCheckpoints = auto()
    TexturesGeometry = auto()
    UncompressedFileSizes = auto()
    Unknown27 = auto()
    Unknown28 = auto()
    Unknown29 = auto()
    Unknown30 = auto()
    Unknown31 = auto()


class Triangle:
    def __init__(self, coord_set_0: int, coord_set_1: int, coord_set_2: int, mesh: int, rgba: tuple = None):
        self.coords = (coord_set_0, coord_set_1, coord_set_2)
        self.rgba = rgba
        self.mesh = mesh


class Color:
    def __init__(self, red: int, green: int, blue: int, alpha: int = 0xFF):
        self.red = red if red < 255 else 255
        self.green = green if green < 255 else 255
        self.blue = blue if blue < 255 else 255
        self.alpha = alpha if alpha < 255 else 255

    def asRatioString(self) -> str:
        channels = [self.red, self.green, self.blue, self.alpha]
        return " ".join([str(int(x / 25.5) / 10) for x in channels])


POINTER_OFFSET = 0x101C50
MODEL_TO_EXPORT = 0x48
# MODEL_TO_EXPORT = 5
MODEL_DATA_OFFSET = 0x28
MODEL_FILE = f"model_{hex(MODEL_TO_EXPORT)[2:]}.bin"


def getObjOffset(base_offset: int, targ_offset: int):
    """Get the read pointer for a file based on the dk64 obj offsets."""
    return MODEL_DATA_OFFSET + (targ_offset - base_offset)


def intf_to_float(intf):
    """Convert float as int format to float."""
    if intf == 0:
        return 0
    else:
        return struct.unpack("!f", bytes.fromhex("{:08X}".format(intf)))[0]


def getColorString(rgba: list[int]) -> str:
    return Color(rgba[0], rgba[1], rgba[2]).asRatioString()


def write_obj_file(triangles: list[Triangle], verts: list[dict], output_file: str):
    mesh_indexes = []
    with open(output_file, "w") as obj_file:
        for triangle in triangles:
            if triangle.mesh not in mesh_indexes:
                mesh_indexes.append(triangle.mesh)
        mesh_indexes.sort()
        mesh_triangles = {}
        for vert in verts:
            selected_vert = vert["coords"]
            obj_file.write(f'v {selected_vert[0]} {selected_vert[1]} {selected_vert[2]} {getColorString(vert["rgba"])}\n')
        for triangle in triangles:
            if triangle.mesh not in mesh_triangles:
                mesh_triangles[triangle.mesh] = []
            mesh_triangles[triangle.mesh].append((triangle.coords[0] + 1, triangle.coords[1] + 1, triangle.coords[2] + 1))

        for mesh_index in mesh_triangles:
            obj_file.write(f"o {mesh_index}\n")
            obj_file.write(f"g {mesh_index}\n")
            for tri in mesh_triangles[mesh_index]:
                obj_file.write(f"f {tri[0]} {tri[1]} {tri[2]}\n")


def rotate(x, y, angle):
    theta = math.radians(-angle)

    cos_t = math.cos(theta)
    sin_t = math.sin(theta)

    x_new = x * cos_t - y * sin_t
    y_new = x * sin_t + y * cos_t

    return x_new, y_new


def float_to_hex(f):
    """Convert float to hex."""
    if f == 0:
        return "0x00000000"
    return hex(struct.unpack("<I", struct.pack("<f", f))[0])


main_pointer_table_offset = POINTER_OFFSET


def mergeModel(
    source_file: int,
    attribute_stealing: int,
    output_file: str,
    steal_bones: bool,
    steal_collision: bool,
    scale_forearms: float = None,
    t_to_a_pose: bool = False,
    left_arm_bones: list = [],
    right_arm_bones: list = [],
    rerigged_bones: dict = {},
):
    """Version 6 modification function test."""
    with open("dk64.z64", "rb") as rom:
        rom.seek(main_pointer_table_offset + (TableNames.ActorGeometry * 4))
        actor_table = main_pointer_table_offset + int.from_bytes(rom.read(4), "big")

        model_names = {"merge_source": source_file, "merge_attribute": attribute_stealing}
        for fn in model_names:
            rom.seek(actor_table + (model_names[fn] << 2))
            model_start = main_pointer_table_offset + int.from_bytes(rom.read(4), "big")
            model_end = main_pointer_table_offset + int.from_bytes(rom.read(4), "big")
            model_size = model_end - model_start
            rom.seek(model_start)
            model_data = zlib.decompress(rom.read(model_size), (15 + 32))
            with open(f"{fn}.bin", "wb") as fh:
                fh.write(model_data)
        col_size_increase = 0
        bone_size_increase = 0
        bone_start = 0
        bone_end = 0
        with open(output_file, "wb") as fh:
            with open("merge_source.bin", "rb") as fg:
                with open("merge_attribute.bin", "rb") as fk:
                    # Get Data From Source
                    source_head = int.from_bytes(fg.read(4), "big")
                    fg.seek(0x8)
                    bone_head = (int.from_bytes(fg.read(4), "big") - source_head) + 0x28
                    fg.seek(0xC)
                    collision_head = (int.from_bytes(fg.read(4), "big") - source_head) + 0x28
                    fg.seek(0x10)
                    color_head = (int.from_bytes(fg.read(4), "big") - source_head) + 0x28
                    fg.seek(color_head)
                    color_data = fg.read()
                    fg.seek(0)
                    vtx_dl_data = fg.read(bone_head)
                    original_bone_size = collision_head - bone_head
                    original_col_size = color_head - collision_head
                    fg.seek(bone_head)
                    bone_data = fg.read(original_bone_size)
                    fg.seek(collision_head)
                    collision_data = fg.read(original_col_size)
                    # Get Data from Attribute
                    attribute_head = int.from_bytes(fk.read(4), "big")
                    fk.seek(0x8)
                    attr_bone_head = (int.from_bytes(fk.read(4), "big") - attribute_head) + 0x28
                    fk.seek(0xC)
                    attr_collision_head = (int.from_bytes(fk.read(4), "big") - attribute_head) + 0x28
                    fk.seek(0x10)
                    attr_color_head = (int.from_bytes(fk.read(4), "big") - attribute_head) + 0x28
                    new_col_size = attr_color_head - attr_collision_head
                    new_bone_size = attr_collision_head - attr_bone_head
                    if steal_collision:
                        col_size_increase = new_col_size - original_col_size
                        fk.seek(attr_collision_head)
                        collision_data = fk.read(new_col_size)
                    if steal_bones:
                        bone_size_increase = new_bone_size - original_bone_size
                        fk.seek(attr_bone_head)
                        bone_data = fk.read(new_bone_size)
                    fk.seek(attr_bone_head)
                    fh.write(vtx_dl_data)
                    bone_start = fh.tell()
                    fh.write(bone_data)
                    bone_end = fh.tell()
                    fh.write(collision_data)
                    fh.write(color_data)
        with open(output_file, "r+b") as fh:
            if scale_forearms is not None:
                bone_data_count = int((bone_end - bone_start) / 0x10)
                for x in range(bone_data_count):
                    fh.seek(bone_start + (x * 0x10))
                    start_bone = int.from_bytes(fh.read(1), "big")
                    end_bone = int.from_bytes(fh.read(1), "big")
                    if (start_bone == left_arm_bones[0] and end_bone == left_arm_bones[1]) or (start_bone == right_arm_bones[0] and end_bone == right_arm_bones[1]):
                        fh.seek(bone_start + (x * 0x10) + 4)
                        dx = intf_to_float(int.from_bytes(fh.read(4), "big"))
                        dy = intf_to_float(int.from_bytes(fh.read(4), "big"))
                        dx *= scale_forearms
                        dy *= scale_forearms
                        fh.seek(bone_start + (x * 0x10) + 4)
                        fh.write(int(float_to_hex(dx), 16).to_bytes(4, "big"))
                        fh.write(int(float_to_hex(dy), 16).to_bytes(4, "big"))
            # Bone size increases
            fh.seek(0xC)
            original_pointer = int.from_bytes(fh.read(4), "big")
            original_pointer += bone_size_increase
            fh.seek(0xC)
            fh.write(original_pointer.to_bytes(4, "big"))
            fh.seek(0x10)
            original_pointer = int.from_bytes(fh.read(4), "big")
            original_pointer += col_size_increase + bone_size_increase
            fh.seek(0x10)
            fh.write(original_pointer.to_bytes(4, "big"))
            fh.seek(0x20)
            bone_count = int.from_bytes(fh.read(1), "big")
            if t_to_a_pose:
                # Discount shoulder bones
                arms = left_arm_bones[1:] + right_arm_bones[1:]
                fh.seek(0x0)
                head = int.from_bytes(fh.read(4), "big")
                fh.seek(0x8)
                collision_head = (int.from_bytes(fh.read(4), "big") - head) + 0x28
                collision_tail = (int.from_bytes(fh.read(4), "big") - head) + 0x28
                collision_count = int((collision_tail - collision_head) / 0x10)
                for x in range(collision_count):
                    fh.seek(collision_head + (x * 0x10) + 1)
                    connecting_bone = int.from_bytes(fh.read(1), "big")
                    if connecting_bone in arms:
                        fh.seek(collision_head + (x * 0x10) + 4)
                        dx = intf_to_float(int.from_bytes(fh.read(4), "big"))
                        dy = intf_to_float(int.from_bytes(fh.read(4), "big"))
                        if connecting_bone in left_arm_bones:
                            new_dx, new_dy = rotate(dx, dy, -70)
                        else:
                            new_dx, new_dy = rotate(dx, dy, 70)
                        fh.seek(collision_head + (x * 0x10) + 4)
                        fh.write(int(float_to_hex(new_dx), 16).to_bytes(4, "big"))
                        fh.write(int(float_to_hex(new_dy), 16).to_bytes(4, "big"))
                vert_rotation = left_arm_bones[:] + right_arm_bones[:]
                fh.seek(0x4)
                dl_end = (int.from_bytes(fh.read(4), "big") - head) + 0x28
                fh.seek(dl_end)
                dl_start = (int.from_bytes(fh.read(4), "big") - head) + 0x28
                dl_size = dl_end - dl_start
                dl_count = int(dl_size / 8)
                in_bone = False
                focused_bone = None
                vert_buffer = [None] * 32
                translated_verts = []
                translated_verts_opp = []
                untouched_verts = []
                ignored_verts = []
                ignored_rerigged_verts = {}
                rerigged_verts = {}
                rerigged_verts_flat = []
                vert_size = int((dl_start - 0x28) / 0x10)
                for x in range(vert_size):
                    untouched_verts.append(x * 0x10)
                for x in range(dl_count):
                    fh.seek(dl_start + (8 * x))
                    command = int.from_bytes(fh.read(1), "big")
                    if command == 0xDA:
                        fh.seek(dl_start + (8 * x) + 6)
                        bone = int(int.from_bytes(fh.read(2), "big") / 0x40)
                        for target_bone, joined_bones in rerigged_bones.items():
                            if bone in joined_bones:
                                fh.seek(dl_start + (8 * x) + 6)
                                val = target_bone * 0x40
                                fh.write(val.to_bytes(2, "big"))
                        in_bone = bone in vert_rotation
                        focused_bone = bone
                    elif command == 1:
                        fh.seek(dl_start + (8 * x) + 1)
                        load_count = int.from_bytes(fh.read(2), "big") >> 4
                        fh.seek(dl_start + (8 * x) + 3)
                        delay = int.from_bytes(fh.read(1), "big")
                        # vert_buffer_start = delay - (load_count * 2)
                        vert_buffer_start = (delay >> 1) - load_count
                        fh.seek(dl_start + (8 * x) + 5)
                        vert_start = int.from_bytes(fh.read(3), "big")
                        offset = 0
                        vert_cap = 0xFFFFFFFFF
                        i_load_vert = (vert_start + offset) >> 4
                        i_load_vert_end = min(i_load_vert + load_count, vert_cap)
                        range_count = (i_load_vert_end - i_load_vert) + 1
                        for yi in range(range_count):
                            if vert_buffer_start + yi < 32:
                                vert_buffer[vert_buffer_start + yi] = vert_start + (yi * 0x10)
                                offset = vert_start + (yi * 0x10) + 0x28
                                if offset == 0x2DE8:
                                    print("DUMP BONE", bone)
                                if in_bone:
                                    if focused_bone in left_arm_bones:
                                        if offset not in translated_verts:
                                            translated_verts.append(offset)
                                    else:
                                        if offset not in translated_verts_opp:
                                            translated_verts_opp.append(offset)
                                else:
                                    if offset not in ignored_verts:
                                        ignored_verts.append(offset)
                                for target_bone, joined_bones in rerigged_bones.items():
                                    if bone in joined_bones:
                                        if offset == 0x2DE8:
                                            print("Attempting to include", bone, joined_bones)
                                        if offset not in rerigged_verts_flat:
                                            rerigged_verts_flat.append(offset)
                                            if bone not in rerigged_verts:
                                                rerigged_verts[bone] = []
                                            rerigged_verts[bone].append(offset)
                                            if offset == 0x2E28:
                                                print(bone, rerigged_verts[bone])
                                    else:
                                        if offset == 0x2DE8:
                                            print("Attempting to exclude", bone)
                                        if target_bone not in ignored_rerigged_verts:
                                            ignored_rerigged_verts[target_bone] = []
                                        ignored_rerigged_verts[target_bone].append(offset)
                    elif command in (5, 6, 7):
                        continue
                vert_rotation_data = [
                    {"verts": translated_verts, "angle": -70},
                    {"verts": translated_verts_opp, "angle": 70},
                ]
                for vrd in vert_rotation_data:
                    for v in vrd["verts"]:
                        if v not in ignored_verts:
                            fh.seek(v)
                            x = int.from_bytes(fh.read(2), "big")
                            if x > 0x7FFF:
                                x -= 0x10000
                            y = int.from_bytes(fh.read(2), "big")
                            if y > 0x7FFF:
                                y -= 0x10000
                            nx, ny = rotate(x, y, vrd["angle"])
                            nx = int(nx)
                            ny = int(ny)
                            if nx < 0:
                                nx += 0x10000
                            if ny < 0:
                                ny += 0x10000
                            fh.seek(v)
                            fh.write(nx.to_bytes(2, "big"))
                            fh.write(ny.to_bytes(2, "big"))
            fh.seek(0x0)
            source_head = int.from_bytes(fh.read(4), "big")
            fh.seek(0x8)
            bone_head = (int.from_bytes(fh.read(4), "big") - source_head) + 0x28
            bone_offsets = []
            bone_master = [0] * bone_count
            bone_bases = []
            for b in range(bone_count):
                bone_offsets.append([0, 0, 0])  # Same ^
                bone_bases.append([0, 0, 0])  # Same ^
            for b in range(bone_count):
                fh.seek(bone_head + (b * 0x10))
                base_bone = int.from_bytes(fh.read(1), "big")
                local_bone = int.from_bytes(fh.read(1), "big")
                master_bone = int.from_bytes(fh.read(1), "big")
                coords = [0, 0, 0]
                if base_bone != 0xFF:
                    coords = bone_offsets[base_bone].copy()
                fh.seek(bone_head + (b * 0x10) + 4)
                for c in range(3):
                    coords[c] += intf_to_float(int.from_bytes(fh.read(4), "big"))
                bone_offsets[local_bone] = coords.copy()
                if master_bone < bone_count:
                    bone_bases[master_bone] = coords.copy()
                else:
                    print("Boney boy")
                    bone_bases.append(coords.copy())
                bone_master[local_bone] = master_bone
            for target_bone, joined_bones in rerigged_bones.items():
                for bn in joined_bones:
                    for v in rerigged_verts[bn]:
                        if target_bone not in ignored_rerigged_verts or v not in ignored_rerigged_verts[target_bone]:
                            print(f"Raising {hex(v)} - Bone {bn}")
                            for x in range(3):
                                fh.seek(v + (2 * x))
                                val = int.from_bytes(fh.read(2), "big")
                                if val > 0x7FFF:
                                    val -= 0x10000
                                val += bone_offsets[bn][x] - bone_offsets[target_bone][x]
                                fh.seek(v + (2 * x))
                                val = int(val)
                                if val < 0:
                                    val += 0x10000
                                fh.write(val.to_bytes(2, "big"))


def extractModel():
    with open("dk64.z64", "rb") as fh:
        fh.seek(POINTER_OFFSET + (TableNames.ActorGeometry << 2))
        actor_table = POINTER_OFFSET + int.from_bytes(fh.read(4), "big")
        fh.seek(actor_table + (MODEL_TO_EXPORT << 2))
        file_start = POINTER_OFFSET + int.from_bytes(fh.read(4), "big")
        file_end = POINTER_OFFSET + int.from_bytes(fh.read(4), "big")
        file_size = file_end - file_start
        fh.seek(file_start)
        data = fh.read(file_size)
        with open(MODEL_FILE, "wb") as fg:
            fg.write(zlib.decompress(data, (15 + 32)))


extractModel()
mergeModel(
    MODEL_TO_EXPORT,
    0xDA,
    f"{hex(MODEL_TO_EXPORT)[2:]}_APOSE.bin",
    False,
    True,
    1.377,
    True,
    [19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33],
    [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
    {
        # 1: [34, 35, 36, 37]
        1: [37]
    },
)

for filename in (MODEL_FILE, f"{hex(MODEL_TO_EXPORT)[2:]}_APOSE.bin"):
    print("---------------------")
    with open(filename, "rb") as obj:
        # Get file offsets
        file_offset = int.from_bytes(obj.read(4), "big")
        dl_end_offset = int.from_bytes(obj.read(4), "big")
        bone_start_offset = int.from_bytes(obj.read(4), "big")
        dl_end_pointer = getObjOffset(file_offset, dl_end_offset)
        bone_start_pointer = getObjOffset(file_offset, bone_start_offset)
        obj.seek(dl_end_pointer)
        vert_end_offset = int.from_bytes(obj.read(4), "big")
        vert_end_pointer = getObjOffset(file_offset, vert_end_offset)
        # Other info
        obj.seek(0x20)
        bone_count = int.from_bytes(obj.read(1), "big")
        print(bone_count)
        vert_bones = []
        bone_offsets = []
        bone_master = [0] * bone_count
        bone_bases = []
        for b in range(bone_count):
            vert_bones.append([])  # Can't do [[]] * bone_count because of referencing errors
            bone_offsets.append([0, 0, 0])  # Same ^
            bone_bases.append([0, 0, 0])  # Same ^
        # Get object verts
        vert_count = int((vert_end_pointer - MODEL_DATA_OFFSET) / 0x10)
        obj.seek(MODEL_DATA_OFFSET)
        verts = []
        bottom_y = 9999999
        for index in range(vert_count):
            coords = []
            for coord_index in range(3):
                value = int.from_bytes(obj.read(2), "big")
                if value > 0x7FFF:
                    value -= 0x10000  # Make it signed
                if coord_index == 1 and value < bottom_y:
                    bottom_y = value
                coords.append(value)
            uv_mapping = []
            for _ in range(3):
                value = int.from_bytes(obj.read(2), "big")
                if value > 0x7FFF:
                    value -= 0x10000  # Make it signed
                uv_mapping.append(value)
            rgba = []
            for _ in range(4):
                rgba.append(int.from_bytes(obj.read(1), "big"))
            verts.append({"coords": coords, "uv": uv_mapping, "rgba": rgba, "index": index})
        # Parse display list
        loaded_verts = []
        used_verts = []
        triangles = []
        vert_cache = [None] * 32
        dl_size = int((dl_end_pointer - vert_end_pointer) / 8)
        bone_index = 0
        mesh = []
        for index in range(dl_size):
            ins_start = vert_end_pointer + (index * 8)
            obj.seek(ins_start)
            i_hi = int.from_bytes(obj.read(4), "big")
            i_lo = int.from_bytes(obj.read(4), "big")
            obj.seek(ins_start)
            instruction = int.from_bytes(obj.read(1), "big")
            if instruction == 0xDA:
                obj.seek(ins_start + 6)
                bone_index = int(int.from_bytes(obj.read(2), "big") / 0x40)
            elif instruction == 1:
                obj.seek(ins_start + 1)
                loaded_vert_count = int.from_bytes(obj.read(2), "big") >> 4
                obj.seek(ins_start + 6)
                loaded_vert_start = int(int.from_bytes(obj.read(2), "big") / 0x10)
                for v in range(loaded_vert_count):
                    focused_vert = loaded_vert_start + v
                    if focused_vert not in used_verts:
                        used_verts.append(focused_vert)
                    vert_bones[bone_index].append(focused_vert)
                i_vert_count = (i_hi >> 12) & 0xFF
                i_vert_buffer_end = i_hi & 0xFF
                # i_vert_buffer_start = i_vert_buffer_end - (i_vert_count * 2)
                i_vert_buffer_start = (i_vert_buffer_end >> 1) - i_vert_count
                i_load_position = i_lo & 0xFFFFFF
                offset = 0
                vert_cap = 0xFFFFFFFFF
                # if self.pointer_table == 1:
                #     offset = vert_offsets[chunk_index]
                #     vert_cap = vert_caps[chunk_index] >> 4
                i_load_vert = (i_load_position + offset) >> 4
                i_load_vert_end = min(i_load_vert + i_vert_count, vert_cap)
                verts_loaded = verts[i_load_vert:i_load_vert_end]
                for yi, y in enumerate(verts_loaded):
                    # print(i_vert_buffer_start, yi, len(verts_loaded), i_vert_buffer_start + yi)
                    if i_vert_buffer_start + yi < 32:
                        vert_cache[i_vert_buffer_start + yi] = y
                    else:
                        print(hex(i_hi), hex(i_lo))
            elif instruction == 5:
                # G_TRI
                tri_buffer_positions = [
                    ((i_hi >> 16) & 0xFF) >> 1,
                    ((i_hi >> 8) & 0xFF) >> 1,
                    ((i_hi >> 0) & 0xFF) >> 1,
                ]
                rgba = None
                tbp_count = 0
                tbp_sum = [0, 0, 0, 0]
                for tbp in (0, 1, 2):
                    if vert_cache[tri_buffer_positions[tbp]]["rgba"] is not None:
                        tbp_count += 1
                        for ch in range(4):
                            tbp_sum[ch] += vert_cache[tri_buffer_positions[tbp]]["rgba"][ch]
                if tbp_count > 0:
                    rgba = tbp_sum.copy()
                    for ch in range(4):
                        rgba[ch] = int(rgba[ch] / tbp_count)
                mesh.append(Triangle(vert_cache[tri_buffer_positions[0]]["index"], vert_cache[tri_buffer_positions[1]]["index"], vert_cache[tri_buffer_positions[2]]["index"], bone_index, rgba))
            elif instruction in (6, 7):
                # G_TRI2 / # G_QUAD
                tri_buffer_positions = [
                    ((i_hi >> 16) & 0xFF) >> 1,
                    ((i_hi >> 8) & 0xFF) >> 1,
                    ((i_hi >> 0) & 0xFF) >> 1,
                    ((i_lo >> 16) & 0xFF) >> 1,
                    ((i_lo >> 8) & 0xFF) >> 1,
                    ((i_lo >> 0) & 0xFF) >> 1,
                ]
                rgba = None
                tbp_count = 0
                tbp_sum = [0, 0, 0, 0]
                for tbp in (0, 1, 2):
                    if vert_cache[tri_buffer_positions[tbp]]["rgba"] is not None:
                        tbp_count += 1
                        for ch in range(4):
                            tbp_sum[ch] += vert_cache[tri_buffer_positions[tbp]]["rgba"][ch]
                if tbp_count > 0:
                    rgba = tbp_sum.copy()
                    for ch in range(4):
                        rgba[ch] = int(rgba[ch] / tbp_count)
                mesh.append(Triangle(vert_cache[tri_buffer_positions[0]]["index"], vert_cache[tri_buffer_positions[1]]["index"], vert_cache[tri_buffer_positions[2]]["index"], bone_index, rgba))
                rgba = None
                tbp_count = 0
                tbp_sum = [0, 0, 0, 0]
                for tbp in (3, 4, 5):
                    if vert_cache[tri_buffer_positions[tbp]]["rgba"] is not None:
                        tbp_count += 1
                        for ch in range(4):
                            tbp_sum[ch] += vert_cache[tri_buffer_positions[tbp]]["rgba"][ch]
                if tbp_count > 0:
                    rgba = tbp_sum.copy()
                    for ch in range(4):
                        rgba[ch] = int(rgba[ch] / tbp_count)
                mesh.append(Triangle(vert_cache[tri_buffer_positions[3]]["index"], vert_cache[tri_buffer_positions[4]]["index"], vert_cache[tri_buffer_positions[5]]["index"], bone_index, rgba))
        # Parse bone offsets
        for b in range(bone_count):
            obj.seek(bone_start_pointer + (b * 0x10))
            base_bone = int.from_bytes(obj.read(1), "big")
            local_bone = int.from_bytes(obj.read(1), "big")
            master_bone = int.from_bytes(obj.read(1), "big")
            coords = [0, 0, 0]
            if base_bone != 0xFF:
                coords = bone_offsets[base_bone].copy()
            obj.seek(bone_start_pointer + (b * 0x10) + 4)
            for c in range(3):
                coords[c] += intf_to_float(int.from_bytes(obj.read(4), "big"))
            bone_offsets[local_bone] = coords.copy()
            if master_bone < bone_count:
                bone_bases[master_bone] = coords.copy()
            else:
                print("Boney boy")
                bone_bases.append(coords.copy())
            bone_master[local_bone] = master_bone
        for bone_local_index, bone in enumerate(vert_bones):
            for vert in bone:
                for c in range(3):
                    verts[vert]["coords"][c] += bone_offsets[bone_local_index][c]
        # print(verts)
        write_obj_file(mesh, verts, filename.replace(".bin", ".obj"))
