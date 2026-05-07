"""Builds Cutscene Database from CSV."""

from BuildLib import newROMName
from skipped_cutscenes import skipped

with open(newROMName, "r+b") as fh:
    fh.seek(0x1FF3800)
    for map_index in range(216):
        cs_lo = 0
        cs_hi = 0
        if map_index in list(skipped.keys()):
            for cs_index in skipped[map_index]:
                if cs_index < 32:
                    cs_lo |= 1 << cs_index
                else:
                    cs_hi |= 1 << (cs_index - 32)
        fh.write(cs_lo.to_bytes(4, "big"))
        fh.write(cs_hi.to_bytes(4, "big"))
