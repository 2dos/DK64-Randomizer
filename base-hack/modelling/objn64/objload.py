"""Based on https://github.com/n64dev/objn64."""

from objlib import Object

def endianFlip(value: int) -> int:
    """Flip the endianness of a specified value."""
    return ((value & 0xFF) << 8) | ((value & 0xFF00) >> 8)

def objLoadObj(file: str, obj: Object) -> Object:
    """Load the object file."""