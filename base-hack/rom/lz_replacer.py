lz_replacements = [
	{
		"find": {
			"map": 0xB0, # Training Grounds
			"exit": 0, # From Isles
		},
		"replace": {
			"map": 0x11, # Hideout Helm
			"exit": 1, # From Kong Prison
		}
	}
]

valid_lz_types = [9,12,13,16]

def intToArr(val,size):
	tmp = val
	arr = []
	for x in range(size):
		arr.append(0)
	slot = size - 1;
	while slot > -1:
		tmpv = tmp % 256;
		arr[slot] = tmpv;
		slot -= 1;
		tmp = int((tmp - tmpv) / 256);
		if slot == -1:
			break;
		elif tmp == 0:
			break;
	return arr

with open("dk64-randomizer-base-dev.z64","r+b") as fh:
	dk_isles_lzs = 0x22750fa
	fh.seek(dk_isles_lzs)
	lz_count = int.from_bytes(fh.read(2),"big")
	for x in range(lz_count):
		start = (x * 0x38) + 2
		fh.seek(dk_isles_lzs + start + 0x10)
		lz_type = int.from_bytes(fh.read(2), "big")
		#print(lz_type)
		if lz_type in valid_lz_types:
			fh.seek(dk_isles_lzs + start + 0x12)
			lz_map = int.from_bytes(fh.read(2), "big")
			fh.seek(dk_isles_lzs + start + 0x14)
			lz_exit = int.from_bytes(fh.read(2), "big")
			for y in lz_replacements:
				if lz_map == y["find"]["map"]:
					if lz_exit == y["find"]["exit"]:
						fh.seek(dk_isles_lzs + start + 0x12)
						map_bytes = intToArr(y["replace"]["map"],2)
						fh.write(bytearray(map_bytes))
						fh.seek(dk_isles_lzs + start + 0x14)
						exit_bytes = intToArr(y["replace"]["exit"],2)
						fh.write(bytearray(exit_bytes))
						# write replacement map and exit