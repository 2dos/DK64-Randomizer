"""Dump pointer tables of the vanilla rom."""
from recompute_pointer_table import dumpPointerTableDetails, parsePointerTables

newROMName = "./rom/dk64.z64"

with open(newROMName, "rb") as fh:
    parsePointerTables(fh)
    dumpPointerTableDetails("rom/pointer_tables_vanilla.log", fh)
