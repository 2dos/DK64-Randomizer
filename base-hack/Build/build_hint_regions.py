"""Build hint region information into ROM."""

from BuildClasses import hint_region_list

H_FILE = "include/hint_regions.h"
C_FILE = "src/pause/hint_region_list.c"

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
    fh.write(f"extern char* hint_region_names[{len(hint_region_list)}];")
    fh.write(f"extern char* unknown_hints[5];")

with open(C_FILE, "w") as fh:
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
        '#include "../../include/common.h"',
        "",
    ]
    for w in warning:
        fh.write(f"{w}\n")
    fh.write("char* hint_region_names[] = {\n")
    max_length_text = ""
    for region in hint_region_list:
        fh.write(f'\t"{region.region_name.upper()}",\n')
        if len(region.region_name) > len(max_length_text):
            max_length_text = region.region_name
    fh.write("};\n\n")
    fh.write("char* unknown_hints[] = {\n")
    for _ in range(5):
        fh.write(f'\t"??? - {max_length_text.upper()}",\n')
    fh.write("};\n")
