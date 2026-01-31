"""Correct the roms file size."""

from BuildLib import finalROM

with open(finalROM, "r+b") as fh:
    fh.seek(0x3154)
    fh.write((0).to_bytes(4, "big"))
    length = len(fh.read())
    print("Original Size:", hex(length))
    to_add = length % 0x10
    if to_add != 0:
        arr = []
        to_add = 0x10 - to_add
        for x in range(to_add):
            arr.append(0)
        fh.write(bytearray(arr))
