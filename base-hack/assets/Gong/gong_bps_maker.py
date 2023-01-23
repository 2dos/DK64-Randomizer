"""Generate the BPS files from the .bin gong files."""

import os
import shutil
import subprocess

shutil.copyfile("..\\..\\..\\build\\flips.exe", "flips.exe")
subprocess.Popen(["flips.exe", "--create", "85722C_ZLib.bin", "gong_source.bin", "gong_geometry.bps", "--bps"]).wait()

if os.path.exists("flips.exe"):
    os.remove("flips.exe")
print("File converted")
