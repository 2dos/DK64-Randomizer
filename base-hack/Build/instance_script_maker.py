"""Make Instance Scripts."""

import json
import os
import zlib

from BuildLib import ROMName, main_pointer_table_offset

instance_dir = "./assets/instance_scripts"
script_table = 0x0
temp_file = "temp.bin"
COMMENT_TAG = "//"

new_block_count = 0
new_cond_count = 0
new_exec_count = 0
new_blocks = []
new_block = []
new_conds = []
new_execs = []


class bcolors:
    """Color codes for printing to console."""

    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def resetCond(reset_block):
    """Reset block data with relation to script."""
    global new_block_count
    global new_cond_count
    global new_exec_count
    global new_blocks
    global new_block
    global new_conds
    global new_execs
    if reset_block:
        new_block_count = 0
        new_blocks = []
    new_cond_count = 0
    new_exec_count = 0
    new_block = []
    new_conds = []
    new_execs = []


def BuildInstanceScripts():
    """Build instance scripts."""
    global new_block_count
    global new_cond_count
    global new_exec_count
    global new_blocks
    global new_block
    global new_conds
    global new_execs

    print("\nCOMPILING SCRIPTS")
    with open(ROMName, "rb") as fh:
        fh.seek(main_pointer_table_offset + (10 * 4))
        script_table = main_pointer_table_offset + int.from_bytes(fh.read(4), "big")
        map_data = []

        if script_table != 0:
            folders = [x[0] for x in os.walk(instance_dir)]
            for f in folders:
                if f != "./" and "pycache" not in f:
                    files = [x[2] for x in os.walk(f)][0]
                    map_index = -1
                    if ".map" in files:
                        with open(f"{f}/.map", "r") as map_info:
                            data = map_info.readlines()
                            map_index = data[0]
                            if "x" in map_index:
                                map_index = int(map_index, 16)
                            else:
                                map_index = int(map_index)
                    script_list = []
                    if map_index > -1:
                        # .Map index found
                        map_data.append({"name": f, "map": map_index})
                        fh.seek(script_table + (map_index * 4))
                        vanilla_start = main_pointer_table_offset + (int.from_bytes(fh.read(4), "big") & 0x7FFFFFFF)
                        vanilla_end = main_pointer_table_offset + (int.from_bytes(fh.read(4), "big") & 0x7FFFFFFF)
                        vanilla_size = vanilla_end - vanilla_start
                        fh.seek(vanilla_start)
                        compress = fh.read(vanilla_size)
                        if int.from_bytes(compress[0:1], "big") == 0x1F and int.from_bytes(compress[1:2], "big") == 0x8B:
                            data = zlib.decompress(compress, 15 + 32)
                        else:
                            data = compress
                        with open(temp_file, "wb") as tp:
                            tp.write(data)
                        with open(temp_file, "rb") as tp:
                            tp.seek(0)
                            script_count = int.from_bytes(tp.read(2), "big")
                            if script_count > 0:
                                read_location = 2
                                for script_index in range(script_count):
                                    script_start = read_location
                                    tp.seek(read_location)
                                    id = int.from_bytes(tp.read(2), "big")
                                    block_count = int.from_bytes(tp.read(2), "big")
                                    behav_9C = int.from_bytes(tp.read(2), "big")
                                    read_location += 6
                                    for block_index in range(block_count):
                                        tp.seek(read_location)
                                        cond_count = int.from_bytes(tp.read(2), "big")
                                        read_location += 2 + (cond_count * 8)
                                        tp.seek(read_location)
                                        exec_count = int.from_bytes(tp.read(2), "big")
                                        read_location += 2 + (exec_count * 8)
                                    script_end = read_location
                                    script_size = script_end - script_start
                                    tp.seek(script_start)
                                    script_list.append({"id": id, "behav_9C": behav_9C, "data": tp.read(script_size)})
                        if os.path.exists(temp_file):
                            os.remove(temp_file)
                        for file in files:
                            if file != ".map":
                                if ".json" in file:
                                    with open(f"{f}/{file}", "r") as script_file:
                                        print(f"{f}/{file}")
                                        script_data = json.loads(script_file.read())
                                        pre_message = f"[x] - Ignoring"
                                        new_data = {
                                            "id": script_data.get("id", 0),
                                            "behav_9C": script_data.get("behav_9C", 0),
                                            "ignore": script_data.get("ignore", False),
                                            "script": script_data["script"],
                                        }
                                        script_data = new_data.copy()
                                        if script_data["ignore"] == 0:
                                            pre_message = f"    - Compiling"
                                        print(f"{pre_message} {file.replace('.json','')} ({hex(script_data['id'])})")
                                        resetCond(True)
                                        new_block_count = len(script_data["script"])
                                        for block in script_data["script"]:
                                            arr = [len(block["conditions"])]
                                            for cond in block["conditions"]:
                                                cond_or = 0
                                                if cond["inverted"]:
                                                    cond_or = 0x8000
                                                cond_arr = [int(cond["function"]) | cond_or]
                                                cond_arr.extend(cond["parameters"])
                                                arr.extend(cond_arr)
                                            arr.append(len(block["executions"]))
                                            for exec in block["executions"]:
                                                exec_arr = [exec["function"]]
                                                exec_arr.extend(exec["parameters"])
                                                arr.extend(exec_arr)
                                            new_blocks.append(arr)
                                            resetCond(False)
                                elif ".script" in file:
                                    with open(f"{f}/{file}", "r") as script_file:
                                        script_info = script_file.readlines()
                                        contains_code = False
                                        contains_data = False
                                        code_start = -1
                                        data_end = len(script_info) - 1
                                        data_start = -1
                                        for line_index, script_line in enumerate(script_info):
                                            if ".code" in script_line:
                                                contains_code = True
                                                code_start = line_index + 1
                                                data_end = line_index
                                            elif ".data" in script_line:
                                                contains_data = True
                                                data_start = line_index + 1
                                        script_data = {"id": -1, "behav_9C": -1, "ignore": 0}
                                        if contains_data and data_start > -1:
                                            for data_line in script_info[data_start:data_end]:
                                                data_line = data_line.replace("\n", "")
                                                for attr in ["id", "behav_9C", "ignore"]:
                                                    if f"{attr} = " in data_line:
                                                        val = data_line.split(f"{attr} = ")[1]
                                                        if "0x" in val:
                                                            val = int(val, 16)
                                                        else:
                                                            val = int(val)
                                                        script_data[attr] = val
                                        pre_message = f"[x] - Ignoring"
                                        if script_data["ignore"] == 0:
                                            pre_message = f"    - Compiling"
                                        print(f"{pre_message} {file.replace('.script','')} ({hex(script_data['id'])})")
                                        if contains_code and code_start > -1:
                                            resetCond(True)
                                            for code_line in [x.split(COMMENT_TAG)[0].strip() for x in script_info[code_start:] if len(x.split(COMMENT_TAG)[0].strip()) > 0]:
                                                code_line = code_line.replace("\n", "")
                                                # print(code_line)
                                                code_split = code_line.split(" ")
                                                if "COND" in code_line.upper():
                                                    cond_or = 0
                                                    if "CONDINV" in code_line.upper():
                                                        cond_or = 0x8000
                                                    arr = [int(code_split[1]) | cond_or]
                                                    for i in range(3):
                                                        arr.append(int(code_split[3 + i]))
                                                    new_conds.append(arr)
                                                    new_cond_count += 1
                                                elif "EXEC" in code_line.upper():
                                                    arr = [int(code_split[1])]
                                                    for i in range(3):
                                                        arr.append(int(code_split[3 + i]))
                                                    new_execs.append(arr)
                                                    new_exec_count += 1
                                                elif "ENDBLOCK" in code_line.upper():
                                                    arr = [new_cond_count]
                                                    for x_i in new_conds:
                                                        arr.extend(x_i)
                                                    arr.append(new_exec_count)
                                                    for x_i in new_execs:
                                                        arr.extend(x_i)
                                                    new_blocks.append(arr)
                                                    resetCond(False)
                                                    new_block_count += 1
                                # Convert blocks
                                if script_data["id"] > -1 and script_data["ignore"] == 0:
                                    found_existing = False
                                    found_index = -1
                                    found_9c = -1
                                    for script_index, script_item in enumerate(script_list):
                                        if script_item["id"] == script_data["id"]:
                                            found_index = script_index
                                            found_9c = script_item["behav_9C"]
                                            found_existing = True
                                    if found_existing and found_index > -1:
                                        data = [script_data["id"], new_block_count, found_9c]
                                        for n in new_blocks:
                                            data.extend(n)
                                        with open(temp_file, "wb") as tp:
                                            for d in data:
                                                d = d % 65536
                                                tp.write(d.to_bytes(2, "big"))
                                        with open(temp_file, "rb") as tp:
                                            script_list[found_index]["data"] = tp.read()
                                        if os.path.exists(temp_file):
                                            os.remove(temp_file)
                                    else:
                                        data = [script_data["id"], new_block_count, script_data["behav_9C"]]
                                        for n in new_blocks:
                                            data.extend(n)
                                        with open(temp_file, "wb") as tp:
                                            for d in data:
                                                d = d % 65536
                                                tp.write(d.to_bytes(2, "big"))
                                        with open(temp_file, "rb") as tp:
                                            script_list.append({"id": script_data["id"], "behav_9C": script_data["behav_9C"], "data": tp.read()})
                                        if os.path.exists(temp_file):
                                            os.remove(temp_file)
                        with open(f"{f.replace('./','')}.raw", "wb") as new_raw:
                            new_raw.write(len(script_list).to_bytes(2, "big"))
                            for script in script_list:
                                new_raw.write(script["data"])
                            new_size = new_raw.tell()
                            offset = new_size % 16
                            if offset > 0:
                                to_add = 16 - offset
                                new_raw.write((0).to_bytes(to_add, "big"))
                with open("./instance_scripts_data.json", "w") as fg:
                    json.dump(map_data, fg)
        else:
            print("Couldn't find instance script table")
