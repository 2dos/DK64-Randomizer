import subprocess
import os
import shutil

# Finalize ROM Python Script
# Credit to Isotarge
# Shamelessly ripped off/expanded by Ballaam

ROMName = "DK64_Randomizer.z64"

#crcresult = subprocess.check_output(['gzip', '-9', '-k', '0113F0_ZLib.bin'])
#print(crcresult)

if os.path.exists(ROMName):
  os.remove(ROMName)

shutil.copyfile("vanillaDK64.z64", ROMName)

with open('RDRAM.bin', 'rb') as fh:
  fh.seek(0x72C);
  patch132C = fh.read(8);
  fh.seek(0xA30);
  patch1630 = fh.read(1696);
  fh.seek(0xDE88);
  patchEA88 = fh.read(3920);
  fh.seek(0x5DAE00);
  patchAppend = fh.read(0x20000);

with open('0113F0_ZLib.bin.gz', 'rb') as fh:
    patch113F0 = fh.read()

patch113F0size = os.stat('0113F0_ZLib.bin.gz');
if patch113F0size.st_size > 726496:
  print('0113F0_ZLib.bin.gz is too big to fit in ROM, size is:' + patch113F0size.st_size + ' max size is 726496')
  exit

with open(ROMName, 'r+b') as fh:
    fh.seek(0x132C)
    fh.write(patch132C)
    fh.seek(0x1630)
    fh.write(patch1630)
    fh.seek(0xEA88)
    fh.write(patchEA88)
    fh.seek(0x113F0)
    fh.write(patch113F0)
    fh.seek(0x2000000);
    fh.write(patchAppend)

    # apply crc patch
    fh.seek(0x3154)
    fh.write(bytearray([0, 0, 0 ,0]))

crcresult = subprocess.check_output(['n64crc', ROMName])
print(crcresult)
