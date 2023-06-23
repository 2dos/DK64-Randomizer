"""Static code patching."""
from heap import getHeapData

jump_data_start = 0x1FFF000
with open("rom/dk64-randomizer-base-temp.z64", "rb") as fg:
    fg.seek(jump_data_start + 0x00)
    patch_lag_hook = fg.read(8)


def patchStaticCode(filename):
    """Patch the static related code."""
    with open(filename, "r+b") as fh:
        # RDRAM Address - 0x5FB300 = ROM address
        fh.seek(0xE64)
        fh.write(bytearray([0x8, 0x0, 0x37, 0xA2]))  # Code Hook
        fh.seek(0x15212)
        fh.write(getHeapData()["upper"].to_bytes(2, "big"))  # Heap Shrink
        fh.seek(0x1521A)
        fh.write(getHeapData()["lower"].to_bytes(2, "big"))  # Heap Shrink
        # fh.seek(0x119247)
        # fh.write(bytearray([0x22])) # File Start Map
        # fh.seek(0x11925B)
        # fh.write(bytearray([0x0])) # File Start Exit

        # Kong Colouring
        fh.seek(0x8F32F)
        fh.write(bytearray([0x00]))
        fh.seek(0x8F150)
        fh.write(bytearray([0x00, 0x00, 0x00, 0x00]))
        fh.seek(0x8F158)
        fh.write(bytearray([0x00, 0x00, 0x00, 0x00]))
        # Lag Hook
        fh.seek(0x5374)
        fh.write(patch_lag_hook)
        # Nintendo Logo
        # Width
        dimensions = [256, 132]
        offset = 640 - (2 * dimensions[0])
        fh.seek(0x5BA)  # RDRAM 5FB8BA
        fh.write(dimensions[0].to_bytes(2, "big"))
        # Height
        fh.seek(0x5FA)  # RDRAM 5FB8FA
        fh.write(dimensions[1].to_bytes(2, "big"))
        # Pixels per line?
        fh.seek(0x602)  # RDRAM 5FB902
        fh.write(offset.to_bytes(2, "big"))
        # Screen Position
        fh.seek(0x5AA)  # RDRAM 5FB8AA
        fh.write((0x7840).to_bytes(2, "big"))
