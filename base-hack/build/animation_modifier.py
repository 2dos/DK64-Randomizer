"""File responsible for modifying the animation code file."""

import zlib
from typing import BinaryIO
from BuildClasses import ROMPointerFile
from BuildEnums import TableNames
from BuildLib import ROMName

anim_file = "animation_code.bin"


class AnimChange:
    """Class to store information pertaining to an animation coding change."""

    def __init__(self, animation: int, offset: int, value: int, value_size: int):
        """Initialize with given parameters."""
        self.animation = animation
        self.offset = offset
        self.value = value
        self.value_size = value_size

    def enact(self, fh: BinaryIO):
        """Apply the animation change."""
        fh.seek(self.animation * 4)
        header = int.from_bytes(fh.read(4), "big")
        fh.seek(header + self.offset)
        fh.write((self.value).to_bytes(self.value_size, "big"))


anim_changes = [
    AnimChange(0x2C1, 0x26 + 3, 0xFF, 1),  # Increase kop volume to 255
    AnimChange(0x2C1, 0x1C + 2, 15, 1),  # Double the chance of a kop making a noise
]


def modifyAnimationCode():
    """Pull geo file from ROM and modify."""
    with open(ROMName, "rb") as fh:
        anim_code_file = ROMPointerFile(fh, TableNames.Unknown13, 0)
        fh.seek(anim_code_file.start)
        dec = zlib.decompress(fh.read(anim_code_file.size), 15 + 32)
        with open(anim_file, "wb") as fg:
            fg.write(dec)
    with open(anim_file, "r+b") as fh:
        for change in anim_changes:
            change.enact(fh)
