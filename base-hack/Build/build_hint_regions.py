"""Build hint region information into ROM."""

from BuildClasses import hint_region_list

H_FILE = "include/hint_regions.h"

with open(H_FILE, "w") as fh:
    warning = [
        "/*",
        "\tThis file is automatically written to by build_hint_regions.py",
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
    fh.write("typedef enum regions {\n")
    for index, region in enumerate(hint_region_list):
        hx = "000" + hex(index)[2:].upper()
        hx = "0x" + hx[-3:]
        fh.write(f"\t/* {hx} */ REGION_{region.enum_name.upper()}, // {region.region_name}\n")
    fh.write("} regions;\n")
