"""Shrink Models and create a duplicate."""
import zlib
from BuildLib import intf_to_float, float_to_hex, main_pointer_table_offset


def shrinkModel(is_file: bool, file_name: str, file_index: int, scale: float, output_file: str, realign_bones: bool):
    """Shrink Model according to scale."""
    data = b""
    # Get data
    if is_file:
        with open(file_name, "rb") as fh:
            data = fh.read()
    else:
        with open("rom/dk64.z64", "rb") as fh:
            fh.seek(main_pointer_table_offset + (5 << 2))
            actor_table = main_pointer_table_offset + int.from_bytes(fh.read(4), "big")
            fh.seek(actor_table + (file_index << 2))
            file_start = main_pointer_table_offset + (int.from_bytes(fh.read(4), "big") & 0x7FFFFFFF)
            file_finish = main_pointer_table_offset + (int.from_bytes(fh.read(4), "big") & 0x7FFFFFFF)
            file_size = file_finish - file_start
            fh.seek(file_start)
            indicator = int.from_bytes(fh.read(2), "big")
            fh.seek(file_start)
            data = fh.read(file_size)
            if indicator == 0x1F8B:
                data = zlib.decompress(data, (15 + 32))
    with open(output_file, "wb") as fh:
        fh.write(data)
    with open(output_file, "r+b") as fh:
        offset = int.from_bytes(fh.read(4), "big")
        dl_end = (int.from_bytes(fh.read(4), "big") - offset) + 0x28
        fh.seek(dl_end)
        vert_end = (int.from_bytes(fh.read(4), "big") - offset) + 0x28
        vert_count = int((vert_end - 0x28) / 0x10)
        for v in range(vert_count):
            fh.seek(0x28 + (0x10 * v))
            coords = [0] * 3
            for ci in range(3):
                val = int.from_bytes(fh.read(2), "big")
                if val > 32767:
                    val -= 65536
                coords[ci] = val * scale
            fh.seek(0x28 + (0x10 * v))
            for c in coords:
                val = c
                if val < 0:
                    val += 65536
                fh.write(int(val).to_bytes(2, "big"))
        if realign_bones:
            fh.seek(8)
            bones_start = (int.from_bytes(fh.read(4), "big") - offset) + 0x28
            bones_end = (int.from_bytes(fh.read(4), "big") - offset) + 0x28
            bones_count = int((bones_end - bones_start) / 0x10)
            for b in range(bones_count):
                fh.seek(bones_start + (0x10 * b) + 4)
                bones = [0] * 3
                for bi in range(3):
                    bones[bi] = intf_to_float(int.from_bytes(fh.read(4), "big")) * scale
                fh.seek(bones_start + (0x10 * b) + 4)
                for bv in bones:
                    fh.write(int(float_to_hex(bv), 16).to_bytes(4, "big"))
