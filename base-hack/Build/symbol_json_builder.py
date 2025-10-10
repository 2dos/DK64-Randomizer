"""Build symbols.json."""

import json

LOWER_LIMIT_DISABLE = False
UPPER_LIMIT_DISABLE = True
PATH_PRE = ""  # "../" if running this file directly
DELIMITER = "\r\n"
NUM_CHARS = [str(x) for x in list(range(10))] + ["-"]


def parseEnumLine(line: str) -> tuple:
    """Parse an enum line and returns the name and value."""
    line = line.split("//")[0].strip()  # Remove any // comment
    new_line = ""
    in_comment = 0
    for index, char in enumerate(line):
        if char in ["*", "/"]:
            if in_comment == 0 and char == "/":
                in_comment = 1
                continue
            elif in_comment == 1 and char == "*":
                in_comment = 3
                continue
            elif in_comment == 2 and char == "/":
                in_comment = 0
                continue
            elif in_comment == 3 and char == "*":
                in_comment = 2
                continue
        if in_comment < 3:
            if in_comment in (1, 2):
                new_line += line[index - 1]
            new_line += char
            in_comment = 0
    if len(new_line) == 0:
        return None, None
    if "=" in new_line:
        name = new_line.split("=")[0].strip()
        value = new_line.split("=")[1].strip()
        if value[-1] == ",":
            value = value[:-1].strip()
        if "x" in value:
            value = int(value, 16)
        else:
            value = int(value)
        return name, value
    name = new_line.strip()
    if len(name) == 0:
        return None, None
    if name[-1] == ",":
        return name[:-1].strip(), None
    return name, None


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
for fname in ("vars", "item_rando", "item_data", "pause"):
    with open(f"{PATH_PRE}include/{fname}.h", "r") as fh:
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
for f in ["exported_enums", "item_data", "common_enums", "pause"]:
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
                    name, temp_value = parseEnumLine(x)
                    if temp_value is not None:
                        enum_count = temp_value
                    if name is not None:
                        name = name.lower()
                        if name in data["enums"]:
                            raise Exception(f"Duplicate enum entry found. Enum: {name}")
                        data["enums"][name] = enum_count
                        enum_count += 1
with open(f"{PATH_PRE}../static/patches/symbols.json", "w") as fg:
    fg.write(json.dumps(data, indent=4))
