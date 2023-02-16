"""Global classes for the build process."""
from enum import IntEnum, auto
from recompute_pointer_table import getFileInfo
from image_converter import convertToRGBA32
from typing import BinaryIO
import os
import zlib
import subprocess

BLOCK_COLOR_SIZE = 64  # Bytes allocated to a block 32x32 image. Brute forcer says we can go as low as 0x25 bytes, but leaving some room for me to have left out something

class ChangeType(IntEnum):
    """Change Type Enum."""

    Undefined = auto()
    PointerTable = auto()
    FixedLocation = auto()

class TextureFormat(IntEnum):
    """Texture Format Enum."""

    Null = auto()
    RGBA5551 = auto()
    RGBA32 = auto()
    I8 = auto()
    I4 = auto()
    IA8 = auto()
    IA4 = auto()

class File:
    """Class to store information regarding file changes."""

    def __init__(self,
                 *, 
                 name="", 
                 subtype:ChangeType=ChangeType.PointerTable, 
                 start=None, 
                 compressed_size=0, 
                 source_file="", 
                 use_external_gzip=False,
                 use_zlib=False,
                 patcher=None,
                 pointer_table_index=0,
                 file_index=0,
                 texture_format:TextureFormat=TextureFormat.Null,
                 bps_file=None,
                 do_not_delete_source=False,
                 do_not_delete_output=False,
                 do_not_delete = False,
                 target_compressed_size=None,
                 target_uncompressed_size=None,
                 do_not_extract=False,
                 do_not_compress=False,
                 do_not_recompress=False,
                 ):
        """Initialize with given parameters."""
        self.name = name
        self.subtype = subtype
        self.start = start
        self.compressed_size = compressed_size
        self.source_file = source_file
        self.use_external_gzip = use_external_gzip
        self.use_zlib = use_zlib
        self.patcher = patcher
        self.pointer_table_index = pointer_table_index
        self.file_index = file_index
        self.texture_format = texture_format
        self.bps_file = bps_file
        self.do_not_delete_source = do_not_delete_source
        self.do_not_delete_output = do_not_delete_output
        self.do_not_delete = do_not_delete
        self.target_compressed_size = target_compressed_size
        self.target_uncompressed_size = target_uncompressed_size
        self.do_not_extract = do_not_extract
        self.do_not_compress = do_not_compress
        self.do_not_recompress = do_not_recompress
        # Static files
        self.output_file = None

    def getTextureFormatName(self) -> int:
        """Get name of texture format used for n64tex."""
        return self.texture_format.name.lower()

    def generateOutputFile(self):
        """Generate output file name."""
        if self.texture_format != TextureFormat.Null:
            self.do_not_extract = True
            extension = f".{self.getTextureFormatName()}"
            self.output_file = self.source_file.replace(".png", extension)

        if self.output_file is None:
            self.output_file = self.source_file

    def extract(self, fh: BinaryIO):
        """Extract file."""
        if not self.do_not_extract:
            byte_read = bytes()
            if self.subtype == ChangeType.PointerTable:
                file_info = getFileInfo(self.pointer_table_index, self.file_index)
                if file_info:
                    self.start = file_info["new_absolute_address"]
                    self.compressed_size = len(file_info["data"])
            if self.start is None:
                print(self)
            fh.seek(self.start)
            byte_read = fh.read(self.compressed_size)

            print(f"{self.name} - {hex(self.start)}")
            if not self.do_not_delete_source:
                if os.path.exists(self.source_file):
                    os.remove(self.source_file)

                with open(self.source_file, "wb") as fg:
                    fh.seek(self.start)
                    if int.from_bytes(fh.read(2), "big") == 0x1F8B:
                        dec = zlib.decompress(byte_read, 15 + 32)
                    else:
                        dec = byte_read
                    fg.write(dec)

    def generateTextureFile(self):
        """Generate Texture File."""
        if self.texture_format != TextureFormat.Null:
            if self.texture_format in [TextureFormat.RGBA5551, TextureFormat.I4, TextureFormat.I8, TextureFormat.IA4, TextureFormat.IA8]:
                result = subprocess.check_output(["./build/n64tex.exe", self.getTextureFormatName(), self.source_file])
                if self.target_compressed_size is not None:
                    self.source_file = self.source_file.replace(".png", f".{self.getTextureFormatName()}")
            elif self.texture_format == TextureFormat.RGBA32:
                convertToRGBA32(self.source_file)
                self.source_file = self.source_file.replace(".png", ".rgba32")
            else:
                print(" - ERROR: Unsupported texture format " + self.getTextureFormatName())