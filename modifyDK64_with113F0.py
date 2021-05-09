"""Finalize the ROM."""
import os
import shutil
import subprocess

# Finalize ROM Python Script
# Credit to Isotarge
# Shamelessly ripped off/expanded by Ballaam

ROMName = "randoSetupDK64.z64"

# crcresult = subprocess.check_output(['gzip', '-9', '-k', '0113F0_ZLib.bin'])
# print(crcresult)

if os.path.exists(ROMName):
    os.remove(ROMName)

shutil.copyfile("DK64.z64", ROMName)

with open("0113F0_ZLib.bin.gz", "rb") as fh:
    patch113F0 = fh.read()

patch113F0size = os.stat("0113F0_ZLib.bin.gz")
if patch113F0size.st_size > 726496:
    print("0113F0_ZLib.bin.gz is too big to fit in ROM, size is:" + patch113F0size.st_size + " max size is 726496")
    exit

with open(ROMName, "r+b") as fh:
    fh.seek(0x113F0)
    fh.write(patch113F0)

    # apply crc patch
    fh.seek(0x3154)
    fh.write(bytearray([0, 0, 0, 0]))

crcresult = subprocess.check_output(["n64crc", ROMName])
print(crcresult)
