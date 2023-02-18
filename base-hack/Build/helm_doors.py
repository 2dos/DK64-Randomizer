"""Generate models for the two Helm doors."""
import zlib
from BuildLib import main_pointer_table_offset

rom_file = "rom/dk64.z64"


def getHelmDoorModel(new_item_image: int, new_number_image: int, filename: str):
    """Get the model file for the Helm coin door, which will be the template for both doors."""
    with open(rom_file, "rb") as rom:
        rom.seek(main_pointer_table_offset + (4 << 2))
        om2_table = main_pointer_table_offset + int.from_bytes(rom.read(4), "big")
        rom.seek(om2_table + (423 << 2))
        file_start = main_pointer_table_offset + (int.from_bytes(rom.read(4), "big") & 0x7FFFFFFF)
        file_end = main_pointer_table_offset + (int.from_bytes(rom.read(4), "big") & 0x7FFFFFFF)
        file_size = file_end - file_start
        rom.seek(file_start)
        indic = int.from_bytes(rom.read(2), "big")
        rom.seek(file_start)
        data = rom.read(file_size)
        if indic == 0x1F8B:
            data = zlib.decompress(data, (15 + 32))
        with open(filename, "wb") as fh:
            fh.write(data)
        with open(filename, "r+b") as fh:
            # Rareware - 0xD48
            # Nintendo - 0xD49
            # Both are 44x44 RGBA5551
            fh.seek(0x4CC)
            fh.write(new_item_image.to_bytes(4, "big"))
            fh.seek(0x534)
            fh.write(new_number_image.to_bytes(4, "big"))
