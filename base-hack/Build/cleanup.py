"""Clean up the repo to remove any files it doesn't need."""
import os

from BuildLib import finalROM, flut_size, heap_size

[os.remove(f) for f in os.listdir(".") if os.path.isfile(f) and os.path.exists(f) and ".bin" in f]
instance_dir = "./assets/instance_scripts/"
for f in os.listdir(instance_dir):
    joined = os.path.join(instance_dir, f)
    if os.path.isfile(joined) and os.path.exists(joined) and ".raw" in f:
        os.remove(joined)
if os.path.exists(finalROM):
    with open(finalROM, "rb") as fh:
        fh.seek(((0x2000000 + heap_size) - flut_size) - 4)
        data = int.from_bytes(fh.read(4), "big")
        if data != 0:
            raise Exception("Code is too big. Suggest increasing the heap.")
