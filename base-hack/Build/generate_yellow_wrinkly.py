"""File to modify Chunky Wrinkly door to a yellow one to place inside the DK Wrinkly slot."""
import shutil
import zlib
import os

new_file = "assets/Non-Code/Gong/hint_door.bin"


def generateYellowWrinkly():
    """Pull geo file from ROM and modify."""
    pointer_table_offset = 0x101C50
    with open("rom/dk64.z64", "rb") as fh:
        fh.seek(pointer_table_offset + (4 * 4))
        om2_geo_table = pointer_table_offset + int.from_bytes(fh.read(4), "big")
        fh.seek(om2_geo_table + (4 * 0xF1))
        chunky_wrinkly_start = pointer_table_offset + int.from_bytes(fh.read(4), "big")
        fh.seek(om2_geo_table + (4 * 0xF1) + 4)
        chunky_wrinkly_end = pointer_table_offset + int.from_bytes(fh.read(4), "big")
        geo_size = chunky_wrinkly_end - chunky_wrinkly_start
        fh.seek(chunky_wrinkly_start)
        dec = zlib.decompress(fh.read(geo_size), 15 + 32)
        with open(new_file, "wb") as fg:
            fg.write(dec)

    with open(new_file, "r+b") as wrinkly_door:
        for x in range(int((0xC00 - 0x600) / 0x10)):
            wrinkly_door.seek(0x60C + (0x10 * x))
            rgb_val = []
            for y in range(3):
                rgb_val.append(int.from_bytes(wrinkly_door.read(1), "big"))
            if rgb_val[0] == 0x6E and rgb_val[1] == 0xE4 and rgb_val[2] == 0x30:
                wrinkly_door.seek(0x60C + (0x10 * x))
                wrinkly_door.write(bytearray([0xFF, 0xFF, 0x00]))
            elif rgb_val[0] == 0x3E and rgb_val[1] == 0x82 and rgb_val[2] == 0x1A:
                wrinkly_door.seek(0x60C + (0x10 * x))
                wrinkly_door.write(bytearray([0x91, 0x91, 0x00]))
        left = 583
        right = 590
        wrinkly_door.seek(0x132A)
        wrinkly_door.write(left.to_bytes(2, "big"))
        wrinkly_door.seek(0x13AE)
        wrinkly_door.write(right.to_bytes(2, "big"))
