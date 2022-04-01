images = [
	{
		"name":"bongos",
		"format":"rgba16",
		"table": 25,
		"index":5548,
		"w":40,
		"h":40,
	},
	{
		"name":"crown",
		"format":"rgba16",
		"table":25,
		"index":5893,
		"w":44,
		"h":44
	},
	{
		"name":"dk_coin",
		"format":"rgba16",
		"table":7,
		"index":500,
		"w":48,
		"h":44
	},
	{
		"name":"fairy",
		"format":"rgba32",
		"table": 25,
		"index":5869,
		"w":32,
		"h":32
	},
	{
		"name":"guitar",
		"format":"rgba16",
		"table": 25,
		"index":5547,
		"w":40,
		"h":40,
	},
	{
		"name":"nin_coin",
		"format":"rgba16",
		"table": 25,
		"index":5912,
		"w":44,
		"h":44
	},
	{
		"name":"orange",
		"format":"rgba16",
		"table": 7,
		"index": 309,
		"w":32,
		"h":32,
	},
	{
		"name":"rainbow_coin",
		"format":"rgba16",
		"table":25,
		"index":5963,
		"w":48,
		"h":44
	},
	{
		"name":"rw_coin",
		"format":"rgba16",
		"table": 25,
		"index":5905,
		"w":44,
		"h":44
	},
	{
		"name":"saxaphone",
		"format":"rgba16",
		"table": 25,
		"index":5549,
		"w":40,
		"h":40,
	}
]


ptr_offset = 0x101C50

import zlib
with open("dk64.z64","rb") as fh:
	for x in images:
		fh.seek(ptr_offset + (x["table"] * 4))
		ptr_table = ptr_offset + int.from_bytes(fh.read(4),"big")
		fh.seek(ptr_table + (x["index"] * 4))
		img_start = ptr_offset + int.from_bytes(fh.read(4),"big")
		fh.seek(ptr_table + ((x["index"] + 1) * 4))
		img_end = ptr_offset + int.from_bytes(fh.read(4),"big")
		img_size = img_end - img_start;
		fh.seek(img_start)
		if x["table"] == 25:
			dec = zlib.decompress(fh.read(img_size),15 + 32)
		else:
			dec = fh.read(img_size)
		with open(f"hashimg_{x['name']}.bin","wb") as fg:
			fg.write(dec)