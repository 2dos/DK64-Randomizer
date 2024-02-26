"""Build symbols.json."""

import json

with open("rom/dev-symbols.sym", "r") as fh:
    # SYMBOLS CANNOT BE USED FOR COSMETIC CHANGES
    data = {}
    text = fh.read()
    delimiter = "\r\n"
    if "\r\n" not in text:
        delimiter = "\n"
    lines = text.split(delimiter)
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
        if addr_int < 0x80400000:
            # Disable out-of-range stuff (lower bound)
            continue
        elif addr_int > 0x805FAE00:
            # Disable out-of-range stuff (upper bound)
            continue
        data[line_split[1]] = addr_int
    with open("../static/patches/symbols.json", "w") as fg:
        fg.write(json.dumps(data, indent=4))
