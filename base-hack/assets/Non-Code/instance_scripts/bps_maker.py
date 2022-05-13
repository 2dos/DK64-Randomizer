"""Generate the BPS files from the .raw script files."""

import os
import subprocess
import shutil
from instance_script_maps import instance_script_maps

instance_name = "instance_script_maps.py"
instance_copy = f"../../../Build/{instance_name}"
shutil.copyfile(instance_copy, instance_name)

maps = instance_script_maps.copy()

script_dir = "../../../../../map_scripts/map_scripts/"
files = [f for f in os.listdir(".") if os.path.isfile(f)]
printed = False
file_total = 0
converted = 0
shutil.copyfile("..\\..\\..\\build\\flips.exe", "flips.exe")
for f in files:
    if ".raw" in f:
        file_total += 1
        file_name = f.replace(".raw", "")
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
                    temp_bps = f.replace(".raw", "_.bps")
                    orig_bps = f.replace(".raw", ".bps")
                    subprocess.Popen(["flips.exe", "--create", vanilla_script, f, temp_bps, "--bps"]).wait()
                    if os.path.exists(temp_bps):
                        if os.path.exists(orig_bps):
                            os.remove(orig_bps)
                        if os.path.exists(f):
                            os.remove(f)
                        shutil.copyfile(temp_bps, orig_bps)
                        os.remove(temp_bps)
                        print(f"Created script for {folder_name}")
                        converted += 1

if os.path.exists("flips.exe"):
    os.remove("flips.exe")
print(f"{converted}/{file_total} scripts converted")
