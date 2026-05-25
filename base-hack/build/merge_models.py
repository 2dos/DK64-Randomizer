"""Library of functions used to merge two models together."""

from BuildLib import main_pointer_table_offset, intf_to_float, float_to_hex
from BuildEnums import TableNames
import zlib
import math


def rotate(x, y, angle):
    """Rotate an xy point around (0, 0) through an angle."""
    theta = math.radians(-angle)

    cos_t = math.cos(theta)
    sin_t = math.sin(theta)

    x_new = x * cos_t - y * sin_t
    y_new = x * sin_t + y * cos_t

    return x_new, y_new


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
    manual_rerig_inclusions: list = [],
):
    """Merge two models."""
    with open("rom/dk64.z64", "rb") as rom:
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
                                        if offset not in rerigged_verts_flat:
                                            rerigged_verts_flat.append(offset)
                                            if bone not in rerigged_verts:
                                                rerigged_verts[bone] = []
                                            rerigged_verts[bone].append(offset)
                                    elif offset not in manual_rerig_inclusions:
                                        if target_bone not in ignored_rerigged_verts:
                                            ignored_rerigged_verts[target_bone] = []
                                        ignored_rerigged_verts[target_bone].append(offset)
                    elif command in (5, 6, 7):
                        continue
                vert_rotation_data = [
                    {
                        "verts": translated_verts,
                        "angle": -70
                    },
                    {
                        "verts": translated_verts_opp,
                        "angle": 70
                    },
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
                            for x in range(3):
                                fh.seek(v + (2 * x))
                                val = int.from_bytes(fh.read(2), "big")
                                if val > 0x7FFF:
                                    val -= 0x10000
                                val += (bone_offsets[bn][x] - bone_offsets[target_bone][x])
                                fh.seek(v + (2 * x))
                                val = int(val)
                                if val < 0:
                                    val += 0x10000
                                fh.write(val.to_bytes(2, "big"))


mergeModel(
    0x48, 0xDA,
    "k_rool_cutscene.bin",
    False, True, 1.377, True,
    [19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33],
    [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
    {
        1: [34, 35, 36, 37]
    },
    [0x2DE8]
)  # CS Version
mergeModel(0x67, 0xDA, "k_rool_fight.bin", False, True, 1.377, True, [5, 6, 7, 8, 9, 10, 11], [2, 3, 4])  # Fight Version
mergeModel(0x10, 3, "cranky_model.bin", False, True, None, True, [16, 17, 18, 19, 20, 21, 22, 23], [8, 9, 10, 11, 12, 13, 14, 15])
mergeModel(0x12, 8, "candy_model.bin", False, True, None, True, [22, 23, 24, 25, 26, 27, 28], [15, 16, 17, 18, 19, 20, 21])
mergeModel(0x11, 0, "funky_model.bin", False, True, None, True, [7, 8, 9], [4, 5, 6])
mergeModel(0x2B, 0xDA, "ricardo_model.bin", False, True, 1.377, True, [9, 10, 11], [6, 7, 8])
mergeModel(0x46, 0, "rabbit_model.bin", False, True, None, True, [12, 13, 14], [9, 10, 11])
mergeModel(0x39, 6, "klump_model.bin", False, True, None, True, [10, 11, 12], [13, 14, 15])
# modifyModel(0x11, "funky_model.bin", [7, 8, 9], [4, 5, 6])

with open("k_rool_fight.bin", "r+b") as fh:
    # Remove DL Call
    fh.seek(0x61C0)
    fh.write((0).to_bytes(8, "big"))
    # Remove Return
    fh.seek(0x6420)
    fh.write((0).to_bytes(8, "big"))
