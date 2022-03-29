"""Dump the pointer tables of our modified rom."""
from recompute_pointer_table import dumpPointerTableDetails, dumpPointerTableDetailsLegacy, parsePointerTables

ROMName = "./rom/dk64-randomizer-base-dev.z64"

with open(ROMName, "rb") as fh:
    parsePointerTables(fh)
    dumpPointerTableDetails("rom/pointer_tables_modified.log", fh)
    dumpPointerTableDetailsLegacy("rom/pointer_tables_modified.log", fh)
