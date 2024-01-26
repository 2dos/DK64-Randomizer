"""Dump the pointer tables of our modified rom."""

from BuildLib import finalROM
from recompute_pointer_table import dumpPointerTableDetails, dumpPointerTableDetailsLegacy, parsePointerTables

with open(finalROM, "rb") as fh:
    export_json = False
    with open("./Build/BuildingBPS.txt", "r") as fg:
        if "1" in str(fg.read()):
            export_json = True
    parsePointerTables(fh)
    dumpPointerTableDetails("rom/pointer_tables_modified.log", fh, export_json)
    dumpPointerTableDetailsLegacy("rom/pointer_tables_modified.log", fh)
