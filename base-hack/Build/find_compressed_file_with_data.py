"""Find a file with a matching set of bytes within decompressed ROM."""

import os
from tkinter.filedialog import askdirectory

search_data = [0xF8, 0x01, 0xF8, 0x01, 0xF8, 0x01, 0xF8, 0x01]
f_path = askdirectory()
print(f_path)
files = [f for f in os.listdir(f_path) if os.path.isfile(os.path.join(f_path, f))]
for f in files:
    if ".bin" in f:
        with open(os.path.join(f_path, f), "rb") as fh:
            find_b = fh.read(len(search_data))
            search_b = bytearray(search_data)
            if find_b == search_b:
                fh.seek(0)
                size_b = len(fh.read())
                print(f"{f} (Size: {hex(size_b)})")
