"""Patcher class and Functions for modifying ROM files."""

from __future__ import annotations

import os
from io import BytesIO
from typing import TYPE_CHECKING, Union
import struct

import js

if TYPE_CHECKING:
    from randomizer.Enums.Kongs import Kongs
    from randomizer.Lists.EnemyTypes import Enemies
    from randomizer.Lists.MapsAndExits import Maps
    from randomizer.Patching.ItemRando import CustomActors


def ftoi(f: float) -> str:
    """Convert float to int representation."""
    if f == 0:
        return 0
    return struct.unpack("<I", struct.pack("<f", f))[0]


# Try except for when the browser is trying to load this file
def load_base_rom() -> None:
    """Load the base ROM file for patching."""
    try:
        print("Loading base rom")
        from randomizer.Patching import BPS as bps

        try:
            patch = open("./static/patches/shrink-dk64.bps", "rb")
        except Exception:
            try:
                patch = BytesIO(bytes(js.getFile("static/patches/shrink-dk64.bps")))
            except Exception:
                patch = open("./worlds/dk64/static/patches/shrink-dk64.bps", "rb")

        original = open("dk64.z64", "rb")
        og_patched_rom = BytesIO(bps.patch(original, patch).read())
        return og_patched_rom
    except Exception as e:
        print(e)
        raise Exception("Unable to load BPS.") from e
        pass


class LocalROM:
    """Patcher for ROM files loaded via Rompatcherjs."""

    def __init__(self) -> None:
        """Patch functions for the ROM loaded within Rompatcherjs.

        This is mostly a hint file, you could directly call the javascript functions,
        but to keep this a bit more logical for team members we just import it and treat
        this like a bytesIO object.

        Args:
            file ([type], optional): [description]. Defaults to None.
        """
        patchedRom = None
        if "PYTEST_CURRENT_TEST" in os.environ:
            data_size = 32 * 1024  # 32KB = 32 * 1024 bytes
            data = bytes(range(256)) * (data_size // 256)  # Repeat values from 0 to 255 to fill 32KB
            # Create a BytesIO object
            patchedRom = BytesIO(data)
        else:
            if not os.path.exists("dk64.z64"):
                raise Exception("No ROM was loaded, please make sure you have dk64.z64 in the root directory of the project.")
            elif patchedRom is None:
                patchedRom = load_base_rom()

        self.rom = patchedRom

    def write(self, val: Union[Maps, int]) -> None:
        """Write value to current position.

        Starts at 0x0 as the inital position without seeking.

        Args:
            val (int): Int value to write.
        """
        self.rom.write((val).to_bytes(1, byteorder="big", signed=False))

    def writeBytes(self, byte_data: Union[bytearray, bytes]) -> None:
        """Write an array a bytes to the current position.

        Starts at 0x0 as the inital position without seeking.

        Args:
            byte_data (bytes): Bytes object to write to current position.
        """
        self.rom.write(bytes(byte_data))

    def writeMultipleBytes(self, value: Union[int, Enemies, Maps, Kongs, CustomActors], size: int) -> None:
        """Write multiple bytes of a size to the current position.

        Starts at 0x0 as the inital position without seeking.

        Args:
            value (int): Value to write.
            size (int): Size of the bytes to write.
        """
        # Keeps the low bytes of the value, so negative values wrap around
        self.rom.write((int(value or 0) & ((1 << (8 * size)) - 1)).to_bytes(size, "big"))

    def writeFloat(self, value: float):
        """Write 32-bit floating point value to the current position."""
        self.writeMultipleBytes(ftoi(value), 4)

    def seek(self, val: int) -> None:
        """Seek to position in current file.

        Args:
            val (int): Position to seek to.
        """
        self.rom.seek(val)

    def readBytes(self, len: int) -> bytes:
        """Read bytes from current position.

        Starts at 0x0 as the inital position without seeking.

        Args:
            len (int): Length to read.

        Returns:
            bytes: List of bytes read from current position.
        """
        return self.rom.read(len)


class ROM(LocalROM):
    """Patcher for the ROM loaded via Rompatcherjs."""

    def __init__(self, file=None):
        """Copy the ROM loaded within Rompatcherjs into Python."""
        self.js_rom = js.patchedRom if file is None else file
        if self.js_rom is None:
            raise RuntimeError("js.patchedRom is not initialized.")
        self._u8array = self.js_rom._u8array
        self.rom = BytesIO(self._u8array.to_bytes())

    def write(self, val: int) -> None:
        """Write one byte, wrapping out of range valuess."""
        self.rom.write(bytes([int(val or 0) & 0xFF]))

    def readBytes(self, size: int) -> bytes:
        """Read bytes from the current position."""
        data = self.rom.read(size)
        if len(data) != size:
            raise RuntimeError(f"readBytes read past end of ROM: tried to read {size} bytes.")
        return data

    def updateJsRom(self) -> None:
        """Copy the Python copy back into the JS ROM."""
        self._u8array.assign(self.rom.getbuffer()[: self._u8array.length])

    def save(self, file_name: str):
        """Save the patched file to a downloadable file."""
        self.updateJsRom()
        self.js_rom.fileName = file_name
        self.js_rom.save()

    def fixChecksum(self):
        """Fix the checksum of the current file."""
        self.updateJsRom()
        js.fixChecksum(self.js_rom)
        # Pick up the checksum the JS side just wrote
        self.rom = BytesIO(self._u8array.to_bytes())

    def fixSecurityValue(self):
        """Set the security code and update the rom checksum."""
        self.seek(0x3154)
        self.write(0)
        self.fixChecksum()
