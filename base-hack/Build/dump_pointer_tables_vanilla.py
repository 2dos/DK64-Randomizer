"""Dump pointer tables of the vanilla rom."""
from recompute_pointer_table import dumpPointerTableDetails, parsePointerTables
from BuildLib import ROMName

with open(ROMName, "rb") as fh:
    parsePointerTables(fh)
    dumpPointerTableDetails("rom/pointer_tables_vanilla.log", fh, False)
