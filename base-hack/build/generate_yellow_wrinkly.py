"""File to modify Chunky Wrinkly door to a yellow one to place inside the DK Wrinkly slot."""

import os
import shutil
import zlib

from BuildClasses import ROMPointerFile
from BuildEnums import TableNames, ExtraTextures, Kong
from BuildLib import ROMName, getBonusSkinOffset

hint_file = "assets/Gong/hint_door.bin"
switch_file = "assets/Gong/sprint_switch.bin"
door_file = "assets/Gong/factory_door.bin"
any_gun_file = "assets/Gong/any_gun.bin"
any_ins_file = "assets/Gong/any_ins.bin"

image_offsets = {
    Kong.DK: 0xF0,
    Kong.Diddy: 0xF2,
    Kong.Lanky: 0xEF,
    Kong.Tiny: 0x67,
    Kong.Chunky: 0xF1,
}
NULL_IMAGE_0 = 0x249
NULL_IMAGE_1 = 0x24F


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
        base_offset = 0x1324
        wrinkly_door.seek(base_offset)
        wrinkly_door.write((3).to_bytes(4, "big"))
        wrinkly_door.seek(base_offset + 8)
        wrinkly_door.write(NULL_IMAGE_0.to_bytes(4, "big"))
        wrinkly_door.seek(base_offset + 0x84)
        wrinkly_door.write((3).to_bytes(4, "big"))
        wrinkly_door.seek(base_offset + 0x84 + 8)
        wrinkly_door.write(NULL_IMAGE_1.to_bytes(4, "big"))


def modifyOtherWrinklyDoors():
    """Modify the other wrinkly doors to include a null image."""
    for kong in (Kong.Diddy, Kong.Lanky, Kong.Tiny, Kong.Chunky):
        file_name = f"assets/Gong/hint_door_{kong.name.lower()}.bin"
        with open(ROMName, "rb") as fh:
            wrinkly_f = ROMPointerFile(fh, TableNames.ModelTwoGeometry, image_offsets[kong])
            fh.seek(wrinkly_f.start)
            dec = zlib.decompress(fh.read(wrinkly_f.size), 15 + 32)
            with open(file_name, "wb") as fg:
                fg.write(dec)
        with open(file_name, "r+b") as wrinkly_door:
            base_offset = 0x1324
            wrinkly_door.seek(base_offset)
            wrinkly_door.write((3).to_bytes(4, "big"))
            wrinkly_door.seek(base_offset + 8)
            wrinkly_door.write(NULL_IMAGE_0.to_bytes(4, "big"))
            wrinkly_door.seek(base_offset + 0x84)
            wrinkly_door.write((3).to_bytes(4, "big"))
            wrinkly_door.seek(base_offset + 0x84 + 8)
            wrinkly_door.write(NULL_IMAGE_1.to_bytes(4, "big"))


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


FACTORY_DOOR_WALL = [
    [
        (60, 80, 0),
        (-59, 80, 0),
        (-59, -39, 0),
    ],
    [
        (60, 80, 0),
        (-59, -39, 0),
        (60, -39, 0),
    ],
]


def fixFactoryDoor():
    """Fix the collision on the door to Factory lobby."""
    with open(ROMName, "rb") as fh:
        door_obj = ROMPointerFile(fh, TableNames.ModelTwoGeometry, 619)
        fh.seek(door_obj.start)
        dec = zlib.decompress(fh.read(door_obj.size), 15 + 32)
        other_start = None
        other_start_0 = None
        with open(door_file, "wb") as fg:
            fg.write(dec[:0x5A8])
            fg.write(len(FACTORY_DOOR_WALL).to_bytes(4, "big"))
            for tri in FACTORY_DOOR_WALL:
                for vert in tri:
                    for coord in vert:
                        value = coord
                        if value < 0:
                            value += 0x10000
                        fg.write(value.to_bytes(2, "big"))
                fg.write((0xFF00).to_bytes(4, "big"))
            other_start = fg.tell()
            fg.write(dec[0x5AC:0x5C8])
            fg.write((0x80).to_bytes(4, "big"))
            for _ in range(0x1C):
                fg.write((0xFF).to_bytes(1, "big"))
            other_start_0 = fg.tell()
            fg.write(dec[0x5C8:])
        inc = None
        with open(door_file, "r+b") as fg:
            fg.seek(0x20)
            fg.write((0x54).to_bytes(4, "big"))
            for idx in range(9):
                offset = 0x50 + (idx * 4)
                fg.seek(offset)
                old = int.from_bytes(fg.read(4), "big")
                if idx == 0:
                    inc = other_start - old
                elif idx == 5:
                    inc = other_start_0 - old
                new = old + inc
                fg.seek(offset)
                fg.write(new.to_bytes(4, "big"))


def buildAnyKongSwitches():
    """Build the prop models for the any kong switches."""
    with open(ROMName, "rb") as fh:
        gun_f = ROMPointerFile(fh, TableNames.ModelTwoGeometry, 0x125)
        fh.seek(gun_f.start)
        dec = zlib.decompress(fh.read(gun_f.size), 15 + 32)
        with open(any_gun_file, "wb") as fg:
            fg.write(dec)

    with open(any_gun_file, "r+b") as switch_f:
        switch_f.seek(0x22C)
        switch_f.write((getBonusSkinOffset(ExtraTextures.AnyGunFront)).to_bytes(4, "big"))

    with open(ROMName, "rb") as fh:
        ins_f = ROMPointerFile(fh, TableNames.ModelTwoGeometry, 0xAB)
        fh.seek(ins_f.start)
        dec = zlib.decompress(fh.read(ins_f.size), 15 + 32)
        with open(any_ins_file, "wb") as fg:
            fg.write(dec)

    with open(any_ins_file, "r+b") as pad_f:
        pad_f.seek(0x324)
        pad_f.write((getBonusSkinOffset(ExtraTextures.AnyInsLeft)).to_bytes(4, "big"))
        pad_f.seek(0x384)
        pad_f.write((getBonusSkinOffset(ExtraTextures.AnyInsRight)).to_bytes(4, "big"))
        pad_f.seek(0x50)
        floor_start = int.from_bytes(pad_f.read(4), "big")
        pad_f.seek(floor_start)
        floor_count = int.from_bytes(pad_f.read(4), "big")
        for x in range(floor_count):
            tri_start = floor_start + 0x10 + (0x18 * x)
            pad_f.seek(tri_start + 0x15)
            pad_f.write((2).to_bytes(1, "big"))
