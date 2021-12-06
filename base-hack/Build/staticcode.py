
def patchStaticCode(filename):
		
	with open(filename, "r+b") as fh:
		# RDRAM Address - 0x5FB300 = ROM address
		fh.seek(0xE64)
		fh.write(bytearray([0x8,0x0,0x37,0xA2])) #Code Hook
		fh.seek(0x15212)
		fh.write(bytearray([0x80,0x5D])) # Heap Shrink
		# fh.seek(0x119247)
		# fh.write(bytearray([0x22])) # File Start Map
		# fh.seek(0x11925B)
		# fh.write(bytearray([0x0])) # File Start Exit

		# Kong Colouring
		fh.seek(0x8F32F)
		fh.write(bytearray([0x00]))
		fh.seek(0x8F150)
		fh.write(bytearray([0x00,0x00,0x00,0x00]))
		fh.seek(0x8F158)
		fh.write(bytearray([0x00,0x00,0x00,0x00]))