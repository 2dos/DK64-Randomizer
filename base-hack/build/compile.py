"""Compile the C Code and build the MIPS toolchain on Windows."""

import os
import subprocess
import sys
from BuildLib import (
    convertToRGBA32,
    convertToRGBA5551,
    convertToIA8,
    convertToIA4,
    convertToI8,
    convertToI4,
)

# ----------------------------
# Setup
# ----------------------------
BASH = r"C:\Program Files\Git\bin\bash.exe"
cwd = os.path.dirname(os.path.abspath(__file__))


def is_windows():
    return os.name == "nt"


def exe(name):
    return name + ".exe" if is_windows() else name


# ----------------------------
# Environment
# ----------------------------
N64_INST = os.environ.get("N64_INST", os.path.abspath("libdragon_install"))
os.environ["N64_INST"] = N64_INST
env = os.environ.copy()

print(f"Using N64_INST={N64_INST}")

toolchain_gcc = os.path.join(N64_INST, "bin", exe("mips64-elf-gcc"))

libdragon_dir = os.path.join("build", "libdragon")
armips_dir = os.path.join("build", "armips")


# ----------------------------
# Helper
# ----------------------------
def run(cmd, cwd=None):
    print(">>", " ".join(cmd))
    subprocess.run(cmd, cwd=cwd, env=env, check=True)


# ----------------------------
# Prepare libdragon
# ----------------------------
if not os.path.exists(libdragon_dir):
    print("Cloning libdragon...")
    run(["git", "clone", "https://github.com/DragonMinded/libdragon.git", libdragon_dir])

if not os.path.exists(toolchain_gcc):
    print("Building libdragon toolchain...")

    tools_dir = os.path.join(libdragon_dir, "tools")

    if is_windows():
        # Requires bash (Git Bash / MSYS2 / WSL)
        run([BASH, "build-toolchain.sh"], cwd=tools_dir)
        run([BASH, "../build.sh"], cwd=tools_dir)
    else:
        run(["./build-toolchain.sh"], cwd=tools_dir)
        run(["./build.sh"], cwd=libdragon_dir)

print("✅ libdragon ready")

# ----------------------------
# Prepare ARMIPS
# ----------------------------
if not os.path.exists(armips_dir):
    print("Cloning ARMIPS...")
    run(["git", "clone", "--recursive", "https://github.com/Kingcom/armips.git", armips_dir])

build_path = os.path.join(armips_dir, "build")
os.makedirs(build_path, exist_ok=True)

with open("include/build_os.h", "w") as fh:
    fh.write("#define IS_WINDOWS\n")

run(["cmake", "-DCMAKE_BUILD_TYPE=Release", ".."], cwd=build_path)
run(["cmake", "--build", "."], cwd=build_path)

armips_exe = os.path.join(build_path, exe("armips"))

print("✅ ARMIPS built")

# ----------------------------
# Compile
# ----------------------------
if not os.path.exists(toolchain_gcc):
    raise RuntimeError("Toolchain not found!")

os.makedirs("obj", exist_ok=True)
os.makedirs("asm", exist_ok=True)


def process_sprite(line):
    if "__LOAD_SPRITE(" not in line:
        return line

    img_path = line.split("__LOAD_SPRITE(")[1].split(",")[0].replace('"', "").strip()
    img_format = line.split(",")[1].split(")")[0].replace('"', "").strip()

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

    return "{" + ", ".join(hex(x) for x in data) + "};\n"


# ----------------------------
# Compile loop
# ----------------------------
for root, _, files in os.walk("src"):
    for file in files:
        if not file.endswith(".c"):
            continue

        src_path = os.path.join(root, file)

        with open(src_path, "r") as fh:
            lines = fh.readlines()

        if lines and "//avoid" in lines[0]:
            continue

        lines = [process_sprite(line) for line in lines]

        obj_name = src_path.replace("\\", "_").replace("/", "_").replace(".c", ".o")
        out_obj = os.path.join("obj", obj_name)

        flags = [
            "-c",
            "-O2",
            "-Wall",
            "-Wextra",
            "-ffreestanding",
            "-fno-builtin",
            "-march=vr4300",
            "-mtune=vr4300",
            "-mabi=32",
            "-G0",
            "-I.",
            "-Isrc",
            "-Iinclude",
            "-DTARGET_N64",
        ]

        run([toolchain_gcc] + flags + ["-o", out_obj, src_path])

print("✅ Compilation complete!")

# ----------------------------
# Assemble
# ----------------------------
WRITE_ADDR = 0x80024390
os.makedirs("minigame", exist_ok=True)

for root, dirs, _ in os.walk("asm/minigames"):
    for d in dirs:
        asm_main = os.path.join(root, d, "main.asm")

        with open(asm_main, "w") as f:
            f.write(".n64\n")
            f.write(f".headersize {hex(WRITE_ADDR)}\n")
            f.write(f".org {hex(WRITE_ADDR)}\n")
            f.write(f'.include "asm/minigames/{d}/objects.asm"\n')

        out_bin = os.path.join("minigame", f"{d}.bin")
        sym = os.path.join("minigame", f"{d}.sym")

        run([armips_exe, asm_main, "-sym", sym])

print("✅ Done!")
