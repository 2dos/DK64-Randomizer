"""Log the dropsanity level data."""

from randomizer.Lists.Location import LocationListOriginal, Location
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Levels import Levels
import os

START_LOC = Locations.JapesMainEnemy_Start
END_LOC = Locations.IslesMainEnemy_LowerFactoryPath1
LEVEL_MAPPING = {
    Levels.JungleJapes: 0,
    Levels.AngryAztec: 1,
    Levels.FranticFactory: 2,
    Levels.GloomyGalleon: 3,
    Levels.FungiForest: 4,
    Levels.CrystalCaves: 5,
    Levels.CreepyCastle: 6,
    Levels.HideoutHelm: 8,
    Levels.DKIsles: 7,
}

count = (END_LOC - START_LOC) + 1
if (count & 1) == 1:
    count += 1
print(count >> 1)
ds_levels = [9] * count
for loc in Locations:
    if loc < START_LOC or loc > END_LOC:
        continue
    offset = loc - START_LOC
    if loc in LocationListOriginal:
        data: Location = LocationListOriginal[loc]
        idx = LEVEL_MAPPING.get(data.level, 9)
        ds_levels[offset] = idx
directory = os.getcwd().split("/")[-1].split("\\")[-1]
path = "src/lib_dropsanity.c"
if directory != "base-hack":
    path = f"base-hack/{path}"
with open(path, "w") as fh:
    warning = [
        '#include "../include/common.h"',
        "",
        "/*",
        "\tThis file is automatically written to by dropsanity_logger.py",
        "\tDon't directly modify this file, instead modify the script",
        "\tOtherwise your changes will be overwritten on next build",
        "",
        "\tThanks,",
        "\t\tBallaam",
        "*/",
        "",
    ]
    for w in warning:
        fh.write(f"{w}\n")
    fh.write("ROM_RODATA_NUM const unsigned char dropsanity_levels[] = {\n")
    for x in range(len(ds_levels) >> 1):
        first = ds_levels[x << 1]
        second = ds_levels[(x << 1) + 1]
        fh.write(f"\t({first} << 4) | {second},\n")
    fh.write("};\n")
