"""Builds Cutscene Database from CSV."""

from BuildLib import newROMName

csv_file = "assets/cutscenes/cutscenes_skipped.csv"
write_file = "src/misc/cutscene_database.c"

# https://docs.google.com/spreadsheets/d/1X7lYw9l7xpfEcQjvD0WzucBwi3uUHW4FfsjrOqDwj_o/edit#gid=308050567

with open(csv_file, "r") as csv:
    rows = csv.read().split("\n")
    data = []
    for row in rows[2:]:
        data.append(row.split(","))
    map_data = []
    for map_index in range(216):
        cutscenes_skipped = []
        for cs in data:
            col = (2 * map_index) + 1
            cs_name = cs[2 * map_index]
            bool_v = False
            if cs_name != "":
                text = cs[col]
                bool_v = text == "TRUE"
            cutscenes_skipped.append(bool_v)
        cs_lo = 0
        cs_hi = 0
        for cs_index, cs in enumerate(cutscenes_skipped):
            if cs:
                if cs_index < 32:
                    cs_lo |= 1 << cs_index
                else:
                    cs_hi |= 1 << (cs_index - 32)
        map_data.extend([cs_lo, cs_hi])
    with open(newROMName, "r+b") as fh:
        fh.seek(0x1FF3800)
        for m in map_data:
            fh.write(m.to_bytes(4, "big"))
