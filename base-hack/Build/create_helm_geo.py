"""Build Helm Geometry file."""

import zlib
from BuildLib import main_pointer_table_offset

rom_file = "./rom/dk64.z64"
geo_file = "helm.bin"

with open(rom_file, "rb") as rom:
    rom.seek(main_pointer_table_offset + (4 * 1))
    geo_table = main_pointer_table_offset + int.from_bytes(rom.read(4), "big")
    rom.seek(geo_table + (0x11 * 4))
    helm_start = main_pointer_table_offset + (int.from_bytes(rom.read(4), "big") & 0x7FFFFFFF)
    helm_end = main_pointer_table_offset + (int.from_bytes(rom.read(4), "big") & 0x7FFFFFFF)
    helm_size = helm_end - helm_start
    rom.seek(helm_start)
    compress = rom.read(helm_size)
    rom.seek(helm_start)
    compress_0 = int.from_bytes(rom.read(2), "big")
    if compress_0 == 0x1F8B:
        data = zlib.decompress(compress, (15 + 32))
    else:
        data = compress
    with open(geo_file, "wb") as geo:
        geo.write(data)
    with open(geo_file, "r+b") as geo:
        geo_points = [0x37C4, 0x3834, 0x3894, 0x38F4, 0x3954, 0x39BC, 0x3A1C, 0x3A7C, 0x3ADC, 0x3B3C]
        geo_overwrite = 4761
        for point in geo_points:
            geo.seek(point)
            geo.write(geo_overwrite.to_bytes(4, "big"))
