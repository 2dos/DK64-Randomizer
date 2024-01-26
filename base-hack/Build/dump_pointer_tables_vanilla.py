"""Dump pointer tables of the vanilla rom."""

from BuildLib import ROMName
from recompute_pointer_table import dumpPointerTableDetails, parsePointerTables

with open(ROMName, "rb") as fh:
    parsePointerTables(fh)
    dumpPointerTableDetails("rom/pointer_tables_vanilla.log", fh, False)
