"""Adjusting the rotation of the pause menu."""

# This has to be done before compilation. The pre-compiler will stick 0x1000 / CHECK_TERMINATOR
# Into whatever code is being ran. Whilst in theory this should be fine, Wii U VC does *NOT* like
# this at all. As such, we have to pre-calculate it ourselves. This script does it for us.

H_FILE = "include/pause.h"

lines = ""
with open(H_FILE, "r") as fh:
    lines = fh.readlines()

check_count = 0
check_count_totals = 0
initated_check_enumeration = False

DEFINITION_TEXT = "#define ROTATION_SPLIT "
DEFINITION_TEXT_TOTALS = "#define ROTATION_SPLIT_TOTALS "
DEFINITION_TEXT_REDUCTION = "#define ROTATION_TOTALS_REDUCTION "
ROTATION_TOTAL = 0x1000
REDUCED_COUNT = 0

new_lines = []
for line in lines:
    raw_line = line.replace("\n", "")
    if initated_check_enumeration:
        if "check_types;" in raw_line:
            initated_check_enumeration = False
            check_count -= 1  # Reduce by 1 because terminator
            check_count_totals -= 1 + REDUCED_COUNT  # Reduce by 2 because terminator and melon crates
        else:
            check_count += 1
            check_count_totals += 1
    if "typedef enum check_types" in raw_line:
        initated_check_enumeration = True
    if DEFINITION_TEXT in raw_line:
        raw_line = f"{DEFINITION_TEXT}{int(ROTATION_TOTAL / check_count)}"
    if DEFINITION_TEXT_TOTALS in raw_line:
        raw_line = f"{DEFINITION_TEXT_TOTALS}{int(ROTATION_TOTAL / check_count)}"
    if DEFINITION_TEXT_REDUCTION in raw_line:
        raw_line = f"{DEFINITION_TEXT_REDUCTION}{REDUCED_COUNT}"
    new_lines.append(raw_line)
with open(H_FILE, "w") as fh:
    fh.write("\n".join(new_lines))
