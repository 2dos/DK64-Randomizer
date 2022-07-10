"""Adjust simian slam text for cosmetic 3rd melon fix."""

from typing import BinaryIO

pointer_table_address = 0x101C50
pointer_table_index = 0xC
text_index = 0x27


def replaceSimSlam(fh):
    """Write new text."""
    print("Replacing Simian Slam Text")
    fh.seek(pointer_table_address + (4 * pointer_table_index))
    pre = int.from_bytes(fh.read(4), "big")
    ptr_table = pointer_table_address + pre
    fh.seek(ptr_table + (4 * text_index))
    start = int.from_bytes(fh.read(4), "big") + pointer_table_address
    fh.seek(start + 0x31E)
    string = "3RD MELON\0"
    fh.write(string.encode("ascii"))
