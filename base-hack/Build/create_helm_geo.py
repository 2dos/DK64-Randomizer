"""Build Helm Geometry file."""

import zlib

from BuildClasses import ROMPointerFile
from BuildEnums import TableNames
from BuildLib import ROMName

geo_file = "helm.bin"

with open(ROMName, "rb") as rom:
    geo_f = ROMPointerFile(rom, TableNames.MapGeometry, 0x11)
    rom.seek(geo_f.start)
    data = rom.read(geo_f.size)
    if geo_f.compressed:
        data = zlib.decompress(data, (15 + 32))
    with open(geo_file, "wb") as geo:
        geo.write(data)
    with open(geo_file, "r+b") as geo:
        geo_points = [0x37C4, 0x3834, 0x3894, 0x38F4, 0x3954, 0x39BC, 0x3A1C, 0x3A7C, 0x3ADC, 0x3B3C]
        geo_overwrite = 4761
        for point in geo_points:
            geo.seek(point)
            geo.write(geo_overwrite.to_bytes(4, "big"))
