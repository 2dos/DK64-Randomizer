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
MODEL_TO_EXPORT = 0x12
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
    with open(output_file, 'w') as obj_file:
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
                obj_file.write(f'f {tri[0]} {tri[1]} {tri[2]}\n')
            
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


with open(MODEL_FILE, "rb") as obj:
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
        verts.append({
            "coords": coords,
            "uv": uv_mapping,
            "rgba": rgba,
            "index": index
        })
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
            verts_loaded = verts[i_load_vert: i_load_vert_end]                                    
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
            mesh.append(Triangle(
                vert_cache[tri_buffer_positions[0]]["index"],
                vert_cache[tri_buffer_positions[1]]["index"],
                vert_cache[tri_buffer_positions[2]]["index"],
                bone_index,
                rgba
            ))
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
            mesh.append(Triangle(
                vert_cache[tri_buffer_positions[0]]["index"],
                vert_cache[tri_buffer_positions[1]]["index"],
                vert_cache[tri_buffer_positions[2]]["index"],
                bone_index,
                rgba
            ))
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
            mesh.append(Triangle(
                vert_cache[tri_buffer_positions[3]]["index"],
                vert_cache[tri_buffer_positions[4]]["index"],
                vert_cache[tri_buffer_positions[5]]["index"],
                bone_index,
                rgba
            ))
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
    print(verts)
    write_obj_file(mesh, verts, "test.obj")
    