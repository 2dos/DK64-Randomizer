"""Dump the item preview enum to a h file."""

from BuildEnums import ItemPreview, CompTextFiles
from typing import BinaryIO

warning_text_data = [
    "This is a pre-generated file. Please don't directly modify this file as this will be overwritten upon next build.",
    "Visit build/dump_previews.py to modify this output.",
    "\nThanks,",
    "\tBallaam",
]
warning_text = "/*\n\t" + "\n\t".join(warning_text_data) + "\n*/\n"


def dumpEnum(file: BinaryIO, enum_name: str, predicate: str, enum_class):
    """Write an enum to a h file."""
    file.write(f"typedef enum {enum_name} {{\n")
    counter = 0
    for name, member in enum_class.__members__.items():
        end_text = ""
        if counter == 0:
            end_text = f" = {hex(member.value)}"
        file.write(f"\t/* {hex(member.value)} */ {predicate.upper()}_{name.upper()}{end_text},\n")
        counter += 1
    file.write(f"}} {enum_name};\n")


with open("include/previews.h", "w") as fh:
    fh.write(warning_text)
    fh.write("\n")
    dumpEnum(fh, "item_previews", "item_preview", ItemPreview)
    fh.write("\n")
    dumpEnum(fh, "comp_text_files", "comp_text", CompTextFiles)
