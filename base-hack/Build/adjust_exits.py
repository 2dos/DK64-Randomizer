"""Adjust exits to prevent logical problems with LZR"""
from typing import BinaryIO

pointer_table_address = 0x101C50
pointer_table_index = 23

exit_adjustments = [
	{
		"containing_map": 0x30, # Fungi Main
		"exits":[
			{
				# Dark Attic
				"exit_index":3,
				"x":3429,
				"y":462,
				"z":4494
			},
			{
				# Mill (W1 Exit)
				"exit_index":6,
				"x":4153,
				"y":163,
				"z":3721
			},
			{
				# DK Barn
				"exit_index":4,
				"x":3982,
				"y":115,
				"z":2026
			}
		]
	},
	{
		"containing_map": 0x1E, # Galleon
		"exits":[
			{
				# Lighthouse
				"exit_index":10,
				"x":1524,
				"y":1754,
				"z":3964,
			},
			{
				# Seal Race
				"exit_index":19,
				"x":3380,
				"y":1640,
				"z":120
			}
		]
	},
	{
		"containing_map":112,
		"exits":[
			{
				# Minecart
				"exit_index":1,
				"x":1515,
				"y":80,
				"z":2506
			}
		]
	}
]

def adjustExits(fh):
	"""Write new exits"""
	print("Adjusting Exits")
	fh.seek(pointer_table_address + (4 * pointer_table_index))
	ptr_table = pointer_table_address + int.from_bytes(fh.read(4),"big")
	for x in exit_adjustments:
		_map = x["containing_map"]
		fh.seek(ptr_table + (4 * _map))
		start = int.from_bytes(fh.read(4),"big") + pointer_table_address
		print(f"{hex(_map)}: {hex(start)}")
		for exit in x["exits"]:
			fh.seek(start + (exit["exit_index"] * 0xA) + 0)
			fh.write(exit["x"].to_bytes(2,"big"))
			fh.seek(start + (exit["exit_index"] * 0xA) + 2)
			fh.write(exit["y"].to_bytes(2,"big"))
			fh.seek(start + (exit["exit_index"] * 0xA) + 4)
			fh.write(exit["z"].to_bytes(2,"big"))


# with open("../rom/dk64-randomizer-base-dev.z64","r+b") as fh:
# 	adjustExits(fh)