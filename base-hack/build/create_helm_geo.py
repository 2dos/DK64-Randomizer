"""Build Helm Geometry file."""

import zlib

from BuildClasses import ROMPointerFile
from BuildEnums import TableNames, ExtraTextures
from BuildLib import ROMName, getBonusSkinOffset

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
        geo_points = {
            0x37C4: ExtraTextures.FinalBoss5Left,  # 0273
            0x3834: ExtraTextures.FinalBoss5Right,  # 0274
            0x3894: ExtraTextures.FinalBoss4Right,  # 0275
            0x38F4: ExtraTextures.FinalBoss4Left,  # 0276
            0x3954: ExtraTextures.FinalBoss3Left,  # 0277
            0x39BC: ExtraTextures.FinalBoss3Right,  # 0278
            0x3A1C: ExtraTextures.FinalBoss2Left,  # 0279
            0x3A7C: ExtraTextures.FinalBoss2Right,  # 027A
            0x3ADC: ExtraTextures.FinalBoss1Right,  # 027B
            0x3B3C: ExtraTextures.FinalBoss1Left,  # 027C
        }
        for point, texture in geo_points.items():
            geo.seek(point)
            geo.write(getBonusSkinOffset(texture).to_bytes(4, "big"))
