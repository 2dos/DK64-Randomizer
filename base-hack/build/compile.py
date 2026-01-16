"""Compile the C Code."""

import os
import shutil
import subprocess
import zipfile
from BuildLib import convertToRGBA32, convertToRGBA5551, convertToIA8, convertToIA4, convertToI8, convertToI4

import requests

# Compile C Code
avoids = []
strict_aliasing_avoids = [
    "src/initialization/text.c",
    "src/initialization/widescreen.c",
    "src/misc/krusha.c",
]
strict_aliasing_avoids_backslash = [x.replace("/", "\\") for x in strict_aliasing_avoids]
print(strict_aliasing_avoids_backslash)

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
with open("include/build_os.h", "w") as fh:
    fh.write("#define IS_WINDOWS\n")
source_asm = []
created_asm = {}
for root, dirs, files in os.walk("src/minigames"):
    for file in files:
        if not file.endswith(".c"):
            continue
        src_path = os.path.join(root, file)
        minigame = None
        modified = False
        lines = None
        original_lines = None
        with open(src_path, "r") as fh:
            lines = fh.readlines()
            first_line = lines[0]
            if "//avoid" in first_line:
                continue
            original_lines = lines.copy()
            for index, line in enumerate(lines):
                if "__LOAD_SPRITE(" in line:
                    modified = True
                    img_path = line.split("__LOAD_SPRITE(")[1].split(",")[0].replace("\"", "").strip()
                    img_format = line.split("__LOAD_SPRITE(")[1].split(",")[1].split(")")[0].replace("\"", "").strip()
                    img_bytes = []
                    if img_format == "RGBA5551":
                        convertToRGBA5551(img_path)
                    elif img_format == "RGBA32":
                        convertToRGBA32(img_path)
                    elif img_format == "I4":
                        convertToI4(img_path)
                    elif img_format == "I8":
                        convertToI8(img_path)
                    elif img_format == "IA4":
                        convertToIA4(img_path)
                    elif img_format == "IA8":
                        convertToIA8(img_path)
                    with open(img_path.replace(".png", f".{img_format.lower()}"), "rb") as fh:
                        data = fh.read()
                        img_bytes = [x for x in data]
                    md = len(img_bytes) % 8
                    if md != 0:
                        for x in range(8 - md):
                            img_bytes.append(0)
                    # img_bytes.extend([0xDF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
                    pre_amble = line.split("__LOAD_SPRITE(")[0]
                    lines[index] = pre_amble + "{" + ", ".join([hex(x) for x in img_bytes]) + "};\n"
        if modified:
            created_asm[src_path.replace(".c", "-translated.c")] = "".join(lines)
            source_asm.append(src_path)
            with open(src_path, "w") as fh:
                fh.write("//avoid\n")
                fh.write("".join(original_lines))
for name, text in created_asm.items():
    with open(name, "w") as fh:
        fh.write(text)
genned_minigames = []
minigame_libs = []
minigame_asms = []
with open("asm/objects.asm", "w") as obj_asm:
    # traverse whole directory
    for root, dirs, files in os.walk(r"src"):
        # select file name
        for file in files:
            # check the extension of files
            if file.endswith(".c") and file[:-2] not in avoids:
                # print whole path of files
                _o = os.path.join(root, file).replace("/", "_").replace("\\", "_").replace(".c", ".o")
                pth = os.path.join(root, file)
                minigame = None
                with open(pth, "r") as fh:
                    first_line = fh.readlines()[0]
                    if "//avoid" in first_line:
                        continue
                    if "// minigame:" in first_line:
                        minigame = first_line.split("// minigame:")[1].strip()
                        print("Found minigame:", minigame)                    
                out_obj = f"obj/{_o}"
                if minigame is None:
                    obj_asm.write(f'.importobj "{out_obj}"\n')
                elif minigame == "all":
                    minigame_libs.append(out_obj)
                else:
                    os.makedirs(f"asm/minigames/{minigame}", exist_ok=True)
                    mode = "a" if minigame in genned_minigames else "w"
                    asm_f = f"asm/minigames/{minigame}/objects.asm"
                    with open(asm_f, mode) as obj_asm2:
                        obj_asm2.write(f'.importobj "{out_obj}"\n')
                    if minigame not in genned_minigames:
                        genned_minigames.append(minigame)
                    if asm_f not in minigame_asms:
                        minigame_asms.append(asm_f)
                reduced_optimization = False
                if "\\" in pth:
                    if pth in strict_aliasing_avoids_backslash:
                        reduced_optimization = True
                else:
                    if pth in strict_aliasing_avoids:
                        reduced_optimization = True
                o_level = "-O1" if reduced_optimization else "-O2"
                subprocess.run(
                    [
                        f"{cwd}\\n64chain\\tools\\bin\\mips64-elf-gcc",
                        "-w",
                        "-Wall",
                        o_level,
                        "-mtune=vr4300",
                        "-march=vr4300",
                        "-mabi=32",
                        "-fomit-frame-pointer",
                        "-fno-toplevel-reorder",
                        "-G0",
                        "-c",
                        "-nostdinc",
                        "-I.",
                        "-Iinclude2",
                        "-Iinclude2/libc",
                        "-DTARGET_N64",
                        "-DF3DEX2_GBI",
                        pth,
                    ]
                )
                shutil.move("./" + file.replace(".c", ".o"), "./obj/" + _o)

for asm in minigame_asms:
    with open(asm, "a") as fh:
        for lib in minigame_libs:
            fh.write(f'.importobj "{lib}"\n')
print("✅ Compilation complete!")
WRITE_ADDR = 0x80024390  # Arcade *can* be written earlier, but jetpac has some extra loader code that mandates a later write
os.makedirs("minigame", exist_ok=True)
open("minigame/dummy.bin", "wb").close()
for minigame in genned_minigames:
    with open(f"asm/minigames/{minigame}/main.asm", "w") as asm:
        asm.write(".n64 // Let armips know we're coding for the N64 architecture\n")
        asm.write(f".open \"minigame/dummy.bin\", \"minigame/{minigame}.bin\", 0 // Open the ROM file\n")
        asm.write(f".include \"asm/symbols.asm\" // Include dk64.asm to tell armips' linker where to find the game's function(s)\n")
        asm.write(f".headersize {hex(WRITE_ADDR)}\n")
        asm.write(f".org {hex(WRITE_ADDR)}\n")
        asm.write(f".include \"asm/minigames/{minigame}/objects.asm\"\n")
        asm.write(".close // Close the ROM file\n")
    BASE_DIR = os.getcwd()
    armips = os.path.join(BASE_DIR, "build", "armips", "build", "armips")
    asm = os.path.join(BASE_DIR, "asm", "minigames", minigame, "main.asm")
    sym = os.path.join(BASE_DIR, "minigame", f"{minigame}-symbols.sym")

    subprocess.run(
        [armips, asm, "-sym", sym],
        check=True
    )
os.remove("minigame/dummy.bin")

for asm in created_asm:
    if os.path.exists(asm):
        os.remove(asm)
for asm in source_asm:
    lines = []
    with open(asm, "r") as fh:
        lines = fh.readlines()
    with open(asm, "w") as fh:
        fh.write("".join(lines[1:]))