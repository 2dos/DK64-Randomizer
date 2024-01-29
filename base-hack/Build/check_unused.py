"""Check for unused symbols."""

import os

src_folder = "/src"
symbols_file = "/asm/symbols.asm"

c_files = []
c_lines = []

for root, dirs, files in os.walk("../" + src_folder):
    # select file name
    for file in files:
        # check the extension of files
        if file.endswith(".c"):
            c_files.append(os.path.join(root, file))

for x in c_files:
    with open(x, "r") as fh:
        ln = fh.readlines()
        for y in ln:
            c_lines.append(y.split("//")[0])

with open("../" + symbols_file, "r") as fh:
    for x in fh.readlines():
        if x.split(".definelabel")[0] == "":
            name = x.split(".definelabel ")[1].split(",")[0]
            found_name = False
            for y in c_lines:
                if name in y:
                    found_name = True
            if not found_name:
                print(name)

# print(c_lines)
