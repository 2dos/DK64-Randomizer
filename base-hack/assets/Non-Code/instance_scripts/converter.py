"""Convert vanilla scripts into modified rando scripts."""

from instance_script_maps import instance_script_maps
import zlib
import os
import shutil

instance_name = "instance_script_maps.py"
instance_copy = f"../../../Build/{instance_name}"
shutil.copyfile(instance_copy, instance_name)

rom_dir = "../../../rom/dk64.z64"
dump_dir = "./dump"
pointer_table_offset = 0x101C50
table = 10


def getScriptName(script_list, id):
    """Grab script name from ID."""
    for item in script_list:
        if item["id"] == id:
            return item["name"]
    return ""


def addToFile(name, folder, line):
    """Add line to file if script is being modified."""
    if name != "":
        new_folder = f"{dump_dir}/{folder}"
        if not os.path.exists(new_folder):
            os.mkdir(new_folder)
        file_name = f"{new_folder}/{name}.txt"
        with open(file_name, "a" if os.path.exists(file_name) else "w") as dump_file:
            dump_file.write(f"{line}\n")


def parseData(data, folder_name, scripts_list):
    """Parse a script file into subscripts."""
    temp_file = "temp.bin"
    with open(temp_file, "wb") as fh:
        fh.write(data)
    with open(temp_file, "rb") as fh:
        fh.seek(0)
        script_count = int.from_bytes(fh.read(2), "big")
        read_location = 2
        for script_item in range(script_count):
            fh.seek(read_location)
            id = int.from_bytes(fh.read(2), "big")
            name = getScriptName(scripts_list, id)
            block_count = int.from_bytes(fh.read(2), "big")
            behav_9C = int.from_bytes(fh.read(2), "big")
            read_location += 6
            for block_item in range(block_count):
                fh.seek(read_location)
                cond_count = int.from_bytes(fh.read(2), "big")
                read_location += 2
                for cond_item in range(cond_count):
                    fh.seek(read_location)
                    func = int.from_bytes(fh.read(2), "big")
                    cond_text = "COND"
                    if func & 0x8000:
                        cond_text = "CONDINV"
                    params = [0, 0, 0]
                    param_chain = ""
                    for p in range(3):
                        params[p] = int.from_bytes(fh.read(2), "big")
                        param_chain += str(params[p]) + " "
                    addToFile(name, folder_name, f"{cond_text} {func} | {param_chain[:-1]}")
                    read_location += 8
                exec_count = int.from_bytes(fh.read(2), "big")
                read_location += 2
                for exec_item in range(exec_count):
                    fh.seek(read_location)
                    func = int.from_bytes(fh.read(2), "big")
                    params = [0, 0, 0]
                    param_chain = ""
                    for p in range(3):
                        params[p] = int.from_bytes(fh.read(2), "big")
                        param_chain += str(params[p]) + " "
                    addToFile(name, folder_name, f"EXEC {func} | {param_chain[:-1]}")
                    read_location += 8
                addToFile(name, folder_name, "ENDBLOCK")
    if os.path.exists(temp_file):
        os.remove(temp_file)
    return len(scripts_list) != 0


def unpackFiles():
    """Unpack ROM to grab script files."""
    with open(rom_dir, "rb") as rom:
        rom.seek(pointer_table_offset + (table * 4))
        table_location = pointer_table_offset + int.from_bytes(rom.read(4), "big")
        if os.path.exists(dump_dir):
            shutil.rmtree(dump_dir)
        if not os.path.exists(dump_dir):
            os.mkdir(dump_dir)
        _idx = 0
        for instance_map in instance_script_maps:
            print(f"[{_idx + 1} / {len(instance_script_maps)}] Converting \"{instance_map['name']}\"")
            file_index = instance_map["map"]
            rom.seek(table_location + (file_index * 4))
            file_start = pointer_table_offset + int.from_bytes(rom.read(4), "big")
            file_end = pointer_table_offset + int.from_bytes(rom.read(4), "big")
            file_size = file_end - file_start
            rom.seek(file_start)
            compress = rom.read(file_size)
            decompress = zlib.decompress(compress, (15 + 32))
            created = parseData(decompress, instance_map["name"], instance_map["scripts"].copy())
            if not created:
                with open(f"./dump/{instance_map['name']}.bin", "wb") as fh:
                    fh.write(decompress)
            _idx += 1


unpackFiles()
