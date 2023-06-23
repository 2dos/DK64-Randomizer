"""Generate models for the two Helm doors."""
import zlib

from BuildClasses import ROMPointerFile
from BuildEnums import TableNames
from BuildLib import ROMName


def getHelmDoorModel(new_item_image: int, new_number_image: int, filename: str):
    """Get the model file for the Helm coin door, which will be the template for both doors."""
    with open(ROMName, "rb") as rom:
        door_f = ROMPointerFile(rom, TableNames.ModelTwoGeometry, 423)
        rom.seek(door_f.start)
        data = rom.read(door_f.size)
        if door_f.compressed:
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
