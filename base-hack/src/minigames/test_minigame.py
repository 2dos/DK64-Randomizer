from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os
from typing import BinaryIO
import json
import sys

ROM_BASE_CACHE = "rom_cache.txt"

# Hide the root tkinter window
Tk().withdraw()

def replaceMinigame(fh: BinaryIO, ovl_index: int, data: bytes, kb_limit: int, loop_addr: int):
    if len(data) > kb_limit * 1024:
        print(f"Could not write minigame - Too large ({len(data)})")
        return
    fh.seek(0x1FFB000 + (8 * ovl_index))
    ovl_offset = int.from_bytes(fh.read(4), "big")
    if ovl_offset in (0, 0xFFFFFFFF):
        print(f"Could not find overlay {ovl_index}")
        return
    # Write bin
    fh.seek(ovl_offset + (0x80024390 - 0x80024000))
    fh.write(data)
    # Write loop
    write_loc = 0x800242FC if ovl_index == 9 else 0x8002433C
    fh.seek(ovl_offset + (write_loc - 0x80024000))
    fh.write((0x0C000000 | ((loop_addr & 0xFFFFFF) >> 2)).to_bytes(4, "big"))

bin_path = f"../../minigame/{sys.argv[1]}.bin" if len(sys.argv) > 1 else None
load_style = sys.argv[2] == "fast" if len(sys.argv) > 2 else False

if os.path.exists(ROM_BASE_CACHE):
    with open(ROM_BASE_CACHE, "r") as fh:
        rom_path = fh.read()
else:
    rom_path = askopenfilename(
        title="Select your Rando ROM File",
        filetypes=[
            ("All Files", "*.z64")
        ]
    )
    with open(ROM_BASE_CACHE, "w") as fh:
        fh.write(rom_path)

# Only show dialog if no argument was provided
if not bin_path:
    bin_path = askopenfilename(
        title="Select your Minigame .bin File",
        filetypes=[
            ("All Files", "*.bin")
        ]
    )

with open(bin_path, "rb") as fh:
    bin_data = fh.read()

minigame_name = os.path.splitext(os.path.basename(bin_path))[0]

with open("../../../static/patches/symbols.json", "r") as fh:
    syms = json.load(fh)

loop_addr = syms["minigames"][f"{minigame_name}.loop"]

with open(rom_path, "r+b") as fh:
    replaceMinigame(fh, 10, bin_data, 43, loop_addr)  # Jetpac
    replaceMinigame(fh, 9, bin_data, 157, loop_addr)  # Arcade
    map_id = 2 if load_style else 0x22
    fh.seek(0x1FED020 + 0x10C)
    fh.write(map_id.to_bytes(1, "big"))