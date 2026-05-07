"""Dump the pointer tables of our modified rom."""

from BuildLib import finalROM
from recompute_pointer_table import dumpPointerTableDetails, dumpPointerTableDetailsLegacy, parsePointerTables

with open(finalROM, "rb") as fh:
    parsePointerTables(fh)
    dumpPointerTableDetails("rom/pointer_tables_modified.log", fh, True)
    dumpPointerTableDetailsLegacy("rom/pointer_tables_modified.log", fh)
