"""Compile the C Code."""
import os
import shutil
import subprocess
import zipfile

import requests

# Compile C Code
avoids = []

with open(".avoid", "r") as avoid_file:
    for x in avoid_file.readlines():
        avoids.append(x.replace("\n", ""))

if len(avoids) > 0:
    print("AVOIDING THE FOLLOWING FILES")
    for x in avoids:
        print("\t- " + x)
if not os.path.exists("build/n64chain"):
    print("Downloading N64Chain from GitHub. This may take a while...")
    url = "https://github.com/tj90241/n64chain/releases/download/9.1.0/n64chain-windows.zip"
    r = requests.get(url, allow_redirects=True)
    open("n64chain.zip", "wb").write(r.content)
    with zipfile.ZipFile("n64chain.zip", "r") as zip_ref:
        zip_ref.extractall("build/n64chain/")
cwd = os.path.dirname(os.path.abspath(__file__))
print(f"{cwd}\\n64chain\\tools\\bin\\mips64-elf-gcc")
with open("asm/objects.asm", "w") as obj_asm:
    # traverse whole directory
    for root, dirs, files in os.walk(r"src"):
        # select file name
        for file in files:
            # check the extension of files
            if file.endswith(".c") and file[:-2] not in avoids:
                # print whole path of files
                _o = os.path.join(root, file).replace("/", "_").replace("\\", "_").replace(".c", ".o")
                print(os.path.join(root, file))
                obj_asm.write('.importobj "obj/' + _o + '"\n')
                cmd = [f"{cwd}\\n64chain\\tools\\bin\\mips64-elf-gcc", "-Wall", "-O1", "-mtune=vr4300", "-march=vr4300", "-mabi=32", "-fomit-frame-pointer", "-G0", "-c", os.path.join(root, file)]
                subprocess.Popen(cmd).wait()
                shutil.move("./" + file.replace(".c", ".o"), "./obj/" + _o)
