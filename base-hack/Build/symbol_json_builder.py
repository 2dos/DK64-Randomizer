"""Build symbols.json."""

import json

LOWER_LIMIT_DISABLE = False
UPPER_LIMIT_DISABLE = True
PATH_PRE = ""  # "../" if running this file directly
DELIMITER = "\r\n"
NUM_CHARS = [str(x) for x in list(range(10))] + ["-"]

data = {
    "symbols": {},
    "vars": {},
    "enums": {},
}
with open(f"{PATH_PRE}rom/dev-symbols.sym", "r") as fh:
    # SYMBOLS CANNOT BE USED FOR COSMETIC CHANGES
    text = fh.read()
    if "\r\n" not in text:
        DELIMITER = "\n"
    lines = text.split(DELIMITER)
    for x in lines:
        line_split = x.split(" ")
        if len(line_split) < 2:
            # Ensure there's a symbol addr pair
            continue
        if line_split[1] == "0":
            # Disable whatever that 0 thing is
            continue
        if line_split[1][0] == ".":
            # Disable `.byt` stuff sneaking through
            continue
        addr_int = int(line_split[0], 16)
        if addr_int < 0x80400000 and not LOWER_LIMIT_DISABLE:
            # Disable out-of-range stuff (lower bound)
            continue
        elif addr_int > 0x805FAE00 and not UPPER_LIMIT_DISABLE:
            # Disable out-of-range stuff (upper bound)
            continue
        data["symbols"][line_split[1]] = addr_int
with open(f"{PATH_PRE}include/vars.h", "r") as fh:
    text = fh.read()
    lines = text.split(DELIMITER)
    start = "#define"
    for x in lines:
        if x[: len(start)] == start:
            segs = x.split(" ")
            value = segs[2]
            if value[-1:] == "f":
                value = float(value[:-1])
            elif len(value) > 2 and value[1] == "x":
                value = int(value, 16)
            elif len([y for y in value if y not in NUM_CHARS]) == 0:
                value = int(value)
            else:
                # Can't be parsed
                continue
            data["vars"][segs[1].lower()] = value
for f in ["exported_enums", "item_data"]:
    with open(f"{PATH_PRE}include/{f}.h", "r") as fh:
        enum_count = 0
        started_enum = False
        text = fh.read()
        lines = text.split(DELIMITER)
        start = "typedef enum"
        for x in lines:
            if x[: len(start)] == start:
                enum_count = 0
                started_enum = True
            elif len(x) > 0:
                if x[0] == "}":
                    started_enum = False
                elif started_enum:
                    segs = x.split(" ")
                    name = None
                    for y in segs:
                        if len(y) > 0:
                            if y[-1] == ",":
                                name = y[:-1].lower()
                    if name in data["enums"]:
                        raise Exception(f"Duplicate enum entry found. Enum: {name}")
                    data["enums"][name] = enum_count
                    enum_count += 1
with open(f"{PATH_PRE}../static/patches/symbols.json", "w") as fg:
    fg.write(json.dumps(data, indent=4))
