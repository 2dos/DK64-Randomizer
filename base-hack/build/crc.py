"""Python recreation of the CRC32 Algorithm."""

import math
from typing import BinaryIO
import sys
import os

# ----------------------------
# Utilities
# ----------------------------


def pad_zeroes(int_val, n_bytes):
    """Pad a hex number with a series of zeroes."""
    hex_string = format(int_val, "x")
    return hex_string.zfill(n_bytes * 2)


def modulo(a, b):
    """Return the modulo of a number."""
    return a - math.floor(a / b) * b


def to_integer(x):
    """Convert a number to an integer correctly."""
    x = int(x)
    return math.ceil(x) if x < 0 else math.floor(x)


def to_uint32(x):
    """Truncate a number to a 32-bit integer."""
    return modulo(to_integer(x), 2 ** 32)


def rol(i, b):
    """idk."""
    return to_uint32(((i << b) | (i >> (32 - b))) & 0xFFFFFFFF)


# ----------------------------
# CRC32 TABLE
# ----------------------------

def _make_crc32_table():
    """Create the CRC32 table."""
    table = []
    for n in range(256):
        c = n
        for _ in range(8):
            c = 0xEDB88320 ^ (c >> 1) if (c & 1) else (c >> 1)
        table.append(c & 0xFFFFFFFF)
    return table


CRC32_TABLE = _make_crc32_table()


def crc32(file: BinaryIO, headerSize=0, ignoreLast4Bytes=False):
    """CRC32 algorithm."""
    if headerSize:
        file.seek(headerSize)
        data = file.read()
    else:
        file.seek(0)
        data = file.read()

    crc = 0xFFFFFFFF
    length = len(data) - 4 if ignoreLast4Bytes else len(data)

    for i in range(length):
        crc = (crc >> 8) ^ CRC32_TABLE[(crc ^ int.from_bytes(data[i], "big")) & 0xFF]

    return (crc ^ 0xFFFFFFFF) & 0xFFFFFFFF


# ----------------------------
# Checksum helpers
# ----------------------------


def recalculate_checksum(file: BinaryIO):
    """Calculate the CRC32 checksum."""
    n = 0x00001000
    seed = 0xDF26F436

    t1 = t2 = t3 = t4 = t5 = t6 = seed

    while n < 0x00001000 + 0x00100000:
        file.seek(n)
        d = int.from_bytes(file.read(4), "big")

        if to_uint32(t6 + d) < t6:
            t4 = to_uint32(t4 + 1)

        t6 = to_uint32(t6 + d)
        t3 = to_uint32(t3 ^ d)

        r = rol(d, d & 0x1F)
        t5 = to_uint32(t5 + r)

        if t2 > d:
            t2 = to_uint32(t2 ^ r)
        else:
            t2 = to_uint32(t2 ^ t6 ^ d)

        idx = 0x40 + 0x0710 + (n & 0xFF)
        file.seek(idx)
        t1 = to_uint32(
            t1 + (int.from_bytes(file.read(4), "big") ^ d)
        )

        n += 4

    crc0 = to_uint32(t6 ^ t4 ^ t3)
    crc1 = to_uint32(t5 ^ t2 ^ t1)

    return [crc0, crc1]


# ----------------------------
# Writing back checksum
# ----------------------------


def update_checksum(file: BinaryIO, newChecksum: list[int]):
    """Update the CRC32 checksum in ROM."""
    file.seek(0x10)
    file.write(newChecksum[0].to_bytes(4, "big"))

    file.seek(0x14)
    file.write(newChecksum[1].to_bytes(4, "big"))


def fix_checksum(file):
    """Fix the checksum for an N64 ROM."""
    new_checksum = recalculate_checksum(file)
    update_checksum(file, new_checksum)


if os.path.exists(sys.argv[1]):
    with open(sys.argv[1], "r+b") as fh:
        fix_checksum(fh)
