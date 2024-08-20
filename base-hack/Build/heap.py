"""Handle heap size."""

from datetime import datetime
from BuildLib import flut_size, heap_size, music_size

code_end = 0x805FAE00

variables = {
    "start": code_end - heap_size,
    "upper": ((code_end - heap_size) >> 16) & 0xFFFF,
    "lower": (code_end - heap_size) & 0xFFFF,
}


def getHeapSize() -> int:
    """Get heap size."""
    return heap_size


def getHeapData() -> dict:
    """Get dict of heap variables."""
    return variables


def getLabel(label: str, value: int):
    """Get formatted asm label."""
    return f".definelabel {label}, {hex(value)}\n"


def handleHeap(size: int, rando_flut_size: int):
    """Write data regarding heap size."""
    with open("asm/variables/heap.asm", "w") as fh:
        fh.write("; Don't modify this file. Instead, modify build/heap.py\n")
        fh.write(getLabel("heap_start", variables["start"]))
        fh.write(getLabel("heap_start_upper", variables["upper"]))
        fh.write(getLabel("heap_start_lower", variables["lower"]))
        fh.write(getLabel("heap_size", size))
        # fh.write(getLabel("ItemRando_FLUT", 0x805FAE00 - rando_flut_size))
    with open("asm/header.asm", "w") as fh:
        fh.write(f".headersize {hex(0x7E000000 | (variables['start'] & 0xFFFFFF))}\n")
        fh.write(f".org {hex(variables['start'])}")
    with open("include/music.h", "w") as fh:
        fh.write(f"#define MUSIC_SIZE {hex(music_size)}")


handleHeap(heap_size, flut_size)
