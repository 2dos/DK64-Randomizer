"""Generate the BPS files from the .raw script files"""

import os
import subprocess
import shutil

maps = [
	{"name":"aztec","map":0x26},
	{"name":"ballroom","map":88},
	{"name":"caves","map":0x48},
	{"name":"chunky_phase","map":207},
	{"name":"diddy_5dc_upper","map":200},
	{"name":"dungeon","map":163},
	{"name":"factory","map":0x1A},
	{"name":"fungi","map":0x30},
	{"name":"galleon","map":0x1E},
	{"name":"giant_mushroom","map":64},
	{"name":"helm","map":0x11},
	{"name":"isles","map":0x22},
	{"name":"japes","map":0x7},
	{"name":"japes_mountain","map":4},
	{"name":"llama_temple","map":0x14},
	{"name":"mill_front","map":61},
	{"name":"mill_rear","map":62},
	{"name":"museum","map":113},
	{"name":"tgrounds","map":0xB0},
	{"name":"tiny_temple","map":0x10},
	{"name":"wind_tower","map":105},
]

script_dir = "../../../../../map_script_stuff/map_scripts_us/"
files = [f for f in os.listdir(".") if os.path.isfile(f)]
printed = False
file_total = 0
converted = 0
shutil.copyfile("..\\..\\..\\build\\flips.exe","flips.exe")
for f in files:
	if ".raw" in f:
		file_total += 1
		file_name = f.replace(".raw","")
		map_index = -1
		for map_obj in maps:
			if map_obj["name"] == file_name:
				map_index = map_obj["map"]
		if map_index > -1:
			map_index_str = str(map_index)
			script_folder_list = [f for f in os.listdir(script_dir) if not os.path.isfile(f)]
			for folder in script_folder_list:
				index = folder.split(" - ")[0]
				folder_name = folder.split(" - ")[1]
				if map_index_str == index:
					vanilla_script = f"{script_dir}{folder}/scripts.raw"
					temp_bps = f.replace(".raw","_.bps")
					orig_bps = f.replace(".raw",".bps")
					subprocess.Popen(["flips.exe", "--create", vanilla_script, f, temp_bps, "--bps"]).wait()
					if os.path.exists(temp_bps):
						if os.path.exists(orig_bps):
							os.remove(orig_bps)
						if os.path.exists(f):
							os.remove(f)
						shutil.copyfile(temp_bps,orig_bps)
						os.remove(temp_bps)
						print(f"Created script for {folder_name}")
						converted += 1

if os.path.exists("flips.exe"):
	os.remove("flips.exe")
print(f"{converted}/{file_total} scripts converted")