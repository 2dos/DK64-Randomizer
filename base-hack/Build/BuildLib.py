"""Library functions for the build procedure."""
import struct

main_pointer_table_offset = 0x101C50
BLOCK_COLOR_SIZE = 64  # Bytes allocated to a block 32x32 image. Brute forcer says we can go as low as 0x25 bytes, but leaving some room for me to have left out something
ROMName = "rom/dk64.z64"
newROMName = "rom/dk64-randomizer-base.z64"
finalROM = "rom/dk64-randomizer-base-dev.z64"
music_size = 0x8000
heap_size = 0x34000 + music_size
flut_size = 0x640


def intf_to_float(intf):
    """Convert float as int format to float."""
    if intf == 0:
        return 0
    else:
        return struct.unpack("!f", bytes.fromhex("{:08X}".format(intf)))[0]


def float_to_hex(f):
    """Convert float to hex."""
    if f == 0:
        return "0x00000000"
    return hex(struct.unpack("<I", struct.pack("<f", f))[0])
