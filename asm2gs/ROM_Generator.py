import subprocess
import os
import shutil

# Finalize ROM Python Script
# Credit to Isotarge
# Shamelessly ripped off/expanded by Ballaam

ROMName = "DK64_Randomizer.z64"

if os.path.exists(ROMName):
    os.remove(ROMName)

shutil.copyfile("randoSetupDK64.z64", ROMName)

result = subprocess.check_output(['lua', '-l', 'loadASM', '-e', "loadASMPatch('../settings.asm')"])
print(result)

def processBytePatch(addr,val):
	val = bytes([val])
	if addr >= 0x72C and addr < (0x72C + 8):
		diff = addr - 0x72C
		with open(ROMName, "r+b") as fh:
			fh.seek(0x132C + diff)
			fh.write(val)
		#print("Boot hook code")
	elif addr >= 0xA30 and addr < (0xA30 + 1696):
		diff = addr - 0xA30
		with open(ROMName, "r+b") as fh:
			fh.seek(0x1630 + diff)
			fh.write(val)
		#print("Expansion Pak Draw Code")
	elif addr >= 0xDE88 and addr < (0xDE88 + 3920):
		diff = addr - 0xDE88
		with open(ROMName, "r+b") as fh:
			fh.seek(0xEA88 + diff)
			fh.write(val)
		#print("Expansion Pak Picture")
	elif addr >= 0x5DAE00 and addr < (0x5DAE00 + 0x20000):
		diff = addr - 0x5DAE00
		with open(ROMName, "r+b") as fh:
			fh.seek(0x2000000 + diff)
			fh.write(val)
		#print("Heap Shrink Space")

f = open("codeOutput.txt","r")
for x in f:
	line = x
	segs = line.split(":")
	processBytePatch(int(segs[0]),int(segs[1]))
	#print(hex(int(segs[0])))
	#print(hex(int(segs[1])))
# apply crc patch
with open(ROMName, "r+b") as fh:
    fh.seek(0x3154)
    fh.write(bytearray([0, 0, 0, 0]))
crcresult = subprocess.check_output(["n64crc", ROMName])
print(crcresult)
print("Your ROM is ready")