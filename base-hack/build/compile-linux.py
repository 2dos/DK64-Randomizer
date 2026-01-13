"""Compile the C Code and build the MIPS toolchain on Linux or Windows."""

import os
import stat
import subprocess

# ----------------------------
# Setup
# ----------------------------
cwd = os.path.dirname(os.path.abspath(__file__))

strict_aliasing_avoids = [
    "src/initialization/text.c",
    "src/initialization/widescreen.c",
    "src/misc/krusha.c",
]
strict_aliasing_avoids_backslash = [x.replace("/", "\\") for x in strict_aliasing_avoids]

# Optional .avoid file
if os.path.exists(".avoid"):
    with open(".avoid", "r") as avoid_file:
        avoids = [x.strip() for x in avoid_file.readlines()]

if avoids:
    print("AVOIDING THE FOLLOWING FILES:")
    for x in avoids:
        print(f"\t- {x}")

libdragon_dir = os.path.join("build", "libdragon")
armips_dir = os.path.join("build", "armips")

# ----------------------------
# Environment (FIXED)
# ----------------------------
# Persist N64_INST for the entire script
N64_INST = os.environ.get("N64_INST", "/opt/libdragon")
os.environ["N64_INST"] = N64_INST
env = os.environ.copy()

print(f"Using N64_INST={N64_INST}")

toolchain_gcc = os.path.join(N64_INST, "bin", "mips64-elf-gcc")

# ----------------------------
# Prepare libdragon
# ----------------------------

# Clone source if missing
if not os.path.exists(libdragon_dir):
    print("Cloning libdragon source from GitHub...")
    subprocess.run(["git", "clone", "https://github.com/DragonMinded/libdragon.git", libdragon_dir], check=True)

# Build toolchain if missing
if not os.path.exists(toolchain_gcc):
    print("Building libdragon toolchain (this will take a long time)...")
    tools_dir = os.path.join(libdragon_dir, "tools")

    subprocess.run(["chmod", "+x", "build-toolchain.sh"], cwd=tools_dir, check=True)
    subprocess.run(["./build-toolchain.sh"], cwd=tools_dir, env=env, check=True)

    print("Building libdragon libraries and examples...")
    subprocess.run(["chmod", "+x", "build.sh"], cwd=libdragon_dir, check=True)
    subprocess.run(["./build.sh"], cwd=libdragon_dir, env=env, check=True)

print("✅ libdragon toolchain ready")

# ----------------------------
# Prepare ARMIPS
# ----------------------------

if not os.path.exists(armips_dir):
    print("Cloning ARMIPS source from GitHub...")
    subprocess.run(["git", "clone", "--recursive", "https://github.com/Kingcom/armips.git", armips_dir], check=True)

build_path = os.path.join(armips_dir, "build")
os.makedirs(build_path, exist_ok=True)

with open("include/build_os.h", "w") as fh:
    fh.write("#define IS_LINUX\n")

subprocess.run(["cmake", "-DCMAKE_BUILD_TYPE=Release", ".."], cwd=build_path, check=True)
subprocess.run(["cmake", "--build", "."], cwd=build_path, check=True)

armips_exe = os.path.join(build_path, "armips")
if os.path.exists(armips_exe):
    st = os.stat(armips_exe)
    os.chmod(armips_exe, st.st_mode | stat.S_IXUSR)

print("✅ ARMIPS built")

# ----------------------------
# Compile C files with libdragon
# ----------------------------

if not os.path.exists(toolchain_gcc):
    raise RuntimeError(f"libdragon gcc not found at {toolchain_gcc}")

# st = os.stat(toolchain_gcc)
# os.chmod(toolchain_gcc, st.st_mode | stat.S_IXUSR)

os.makedirs("obj", exist_ok=True)
os.makedirs("asm", exist_ok=True)

with open("asm/objects.asm", "w") as obj_asm:
    for root, dirs, files in os.walk("src"):
        for file in files:
            if not file.endswith(".c"):
                continue
            src_path = os.path.join(root, file)
            with open(src_path, "r") as fh:
                first_line = fh.readlines()[0]
                if "//avoid" in first_line:
                    continue

            obj_name = src_path.replace("/", "_").replace("\\", "_").replace(".c", ".o")

            out_obj = os.path.join("obj", obj_name)
            obj_asm.write(f'.importobj "{out_obj}"\n')

            flags = [
                "-c",
                # Optimization
                "-O2",
                # Warnings
                "-Wall",
                "-Wextra",
                "-Wno-unused-parameter",
                "-Wno-implicit-fallthrough",
                # Freestanding / N64-specific
                "-ffreestanding",
                "-fno-builtin-memcpy",
                "-fno-builtin-memset",
                "-fomit-frame-pointer",
                # Disable features that bloat code
                "-fno-stack-protector",
                "-fno-pic",
                "-fno-inline",
                "-fno-unroll-loops",
                "-mno-abicalls",
                "-fno-asynchronous-unwind-tables",
                "-fno-unwind-tables",
                # CPU / ABI
                "-march=vr4300",
                "-mtune=vr4300",
                "-mabi=32",
                # Small data
                "-G0",
                # Include paths
                "-I.",
                "-Isrc",
                "-Iinclude",
                "-Iinclude2",
                # Optional: "-I{N64_INST}/include",
                # Optional: "-I{N64_INST}/mips64-elf/include",
                # Defines
                "-DTARGET_N64",
                "-DF3DEX2_GBI",
            ]

            subprocess.run(
                [toolchain_gcc] + flags + ["-o", out_obj, src_path],
                check=True,
            )

print("✅ Compilation complete!")
