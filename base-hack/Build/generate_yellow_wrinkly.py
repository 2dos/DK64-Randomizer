"""File to modify Chunky Wrinkly door to a yellow one to place inside the DK Wrinkly slot."""

import os
import shutil
import zlib

from BuildClasses import ROMPointerFile
from BuildEnums import TableNames, ExtraTextures
from BuildLib import ROMName, getBonusSkinOffset

hint_file = "assets/Gong/hint_door.bin"
switch_file = "assets/Gong/sprint_switch.bin"


def generateYellowWrinkly():
    """Pull geo file from ROM and modify."""
    with open(ROMName, "rb") as fh:
        wrinkly_f = ROMPointerFile(fh, TableNames.ModelTwoGeometry, 0xF1)
        fh.seek(wrinkly_f.start)
        dec = zlib.decompress(fh.read(wrinkly_f.size), 15 + 32)
        with open(hint_file, "wb") as fg:
            fg.write(dec)

    with open(hint_file, "r+b") as wrinkly_door:
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


def generateSprintSwitch():
    """Pull geo file from ROM and modify."""
    with open(ROMName, "rb") as fh:
        switch_obj = ROMPointerFile(fh, TableNames.ModelTwoGeometry, 0x16C)
        fh.seek(switch_obj.start)
        dec = zlib.decompress(fh.read(switch_obj.size), 15 + 32)
        with open(switch_file, "wb") as fg:
            fg.write(dec)

    # SWITCH COLORS:
    # Green: 0x32EF32FF
    # Blue:  0x2CBEFFFF
    # Red:   0xFF0000FF
    # Grey:  0xB3DCF6FF

    grey_rgba = 0xB3DCF6FF
    with open(switch_file, "r+b") as fh:
        # Change color from blue to grey
        for x in range(6):
            fh.seek(0x724 + (x * 0x10))
            fh.write(grey_rgba.to_bytes(4, "big"))
        # Change face
        fh.seek(0x35C)
        fh.write(getBonusSkinOffset(ExtraTextures.OSprintLogoRight).to_bytes(4, "big"))
        fh.seek(0x3BC)
        fh.write(getBonusSkinOffset(ExtraTextures.OSprintLogoLeft).to_bytes(4, "big"))
