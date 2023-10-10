"""Vendor enum."""
from enum import IntEnum, auto


class VendorType(IntEnum):
    """Vendor Type enum."""

    Cranky = 0
    Funky = auto()
    Candy = auto()
