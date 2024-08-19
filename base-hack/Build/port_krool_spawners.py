"""Update the 4 non-Chunky phase maps in the K. Rool sequence to include the correct spawners for the final cutscene."""

import json
import shutil
import os
import zlib
from BuildEnums import Maps, TableNames, Song
from BuildClasses import ROMPointerFile
from BuildLib import ROMName
from typing import BinaryIO

# Start everything from 20 onwards


class KRoolCSMap:
    """Information to store regarding a K Rool map that's being ported."""

    def __init__(self, map_index: Maps, folder: str, fence_start: int, spawner_start: int, kr_actual_id: int, kong_cs_id: int, cs_model: int):
        """Initialize with given parameters."""
        self.map_index = map_index
        self.folder = folder
        self.fence_start = fence_start
        self.spawner_start = spawner_start
        self.kr_actual_id = kr_actual_id  # Spawner ID for K Rool. 1 in Chunky Phase
        self.kong_cs_id = kong_cs_id  # Spawner ID for the cutscene object kong which is tied to the "In the red corner" CS. 2 in Chunky Phase
        self.cs_model = cs_model
        self.file_data = None
        self.file_stream = None
        self.path_data = None
        self.path_stream = None

    def updateFile(self, fh: BinaryIO, file_data: ROMPointerFile):
        """Initialize the file stream."""
        self.file_data = file_data
        if file_data.size == 0:
            self.file_stream = b""
            return
        fh.seek(file_data.start)
        data = fh.read(file_data.size)
        if file_data.compressed:
            data = zlib.decompress(data, (15 + 32))
        self.file_stream = data

    def updatePath(self, fh: BinaryIO, path_data: ROMPointerFile):
        """Initialize the file stream."""
        self.path_data = path_data
        if path_data.size == 0:
            self.path_stream = b""
            return
        fh.seek(path_data.start)
        data = fh.read(path_data.size)
        if path_data.compressed:
            data = zlib.decompress(data, (15 + 32))
        self.path_stream = data


MAP_DATA = [
    KRoolCSMap(Maps.KRoolDK, "dk_phase", 10, 20, 1, 6, 25),
    KRoolCSMap(Maps.KRoolDiddy, "diddy_phase", 10, 20, 1, 6, 21),
    KRoolCSMap(Maps.KRoolLanky, "lanky_phase", 10, 20, 1, 4, 23),
    KRoolCSMap(Maps.KRoolTiny, "tiny_phase", 10, 20, 1, 2, 24),
]

SUB_COMMAND_CONVERSION = {
    # Key is the subcommand, value is the parameter index which contains the spawner id
    4: (0,),
    5: (0,),
    6: (0,),
    0x13: (0,),
    0x14: (0,),
    0x16: (0,),
    0x20: (0,),
    0x21: (0, 1),
    0x24: (0,),
    0x2A: (0,),
    0x37: (0,),
    0x38: (0,),
}

used_subcommands = []


def updateCutsceneScripts(pre: str = ""):
    """Update the cutscene scripts to shift the spawner IDs appropriately."""
    for m in MAP_DATA:
        m_path = f"{pre}assets/cutscene_scripts/{m.folder}"
        if os.path.exists(m_path):
            shutil.rmtree(m_path)
        os.mkdir(m_path)
        with open(f"{m_path}/.map", "w") as fh:
            fh.write(str(int(m.map_index)))
        for x in range(3):
            with open(f"{pre}assets/cutscene_scripts/k_rool_cs/end_cs_p{x + 1}.json", "r") as fh:
                data = json.load(fh)
                points = data["point_data"]
                for point_index, point in enumerate(points):
                    if point["command"] == 13:
                        detailed_command = point["detailed_command"]
                        sub_command = detailed_command["sub_command"]
                        if sub_command not in used_subcommands:
                            used_subcommands.append(sub_command)
                        if x == 2 and m.map_index == Maps.KRoolDK:
                            if sub_command == 4:
                                if detailed_command["params"][0] == 18:
                                    if detailed_command["params"][1] == 23:
                                        data["point_data"][point_index]["detailed_command"]["params"][2] = 1
                        if sub_command in SUB_COMMAND_CONVERSION:
                            arg_indexes = SUB_COMMAND_CONVERSION[sub_command]
                            if sub_command == 19:
                                data["point_data"][point_index]["detailed_command"]["params"][1] += m.fence_start
                            for k in arg_indexes:
                                id = detailed_command["params"][k]
                                if sub_command == 20 and id > 0x7FF:
                                    continue
                                new_id = None
                                if id == 4:
                                    new_id = m.spawner_start
                                elif id == 1:
                                    new_id = m.kr_actual_id
                                elif id == 2:
                                    new_id = m.kong_cs_id
                                else:
                                    new_id = (id - 10) + m.spawner_start + 1
                                if new_id is None:
                                    raise Exception("Invalid Bijection")
                                data["point_data"][point_index]["detailed_command"]["params"][k] = new_id
                if x == 0:
                    song_call = {
                        "unk0": 5,
                        "command": 13,
                        "head": [0, 0],
                        "detailed_command": {
                            "sub_command": 23,
                            "params": [Song.KRoolEntrance, 0, 0, 0],
                        },
                        "duration": 0,
                    }
                    data["point_data"].insert(0, song_call)
                    if m.map_index in (Maps.KRoolDiddy, Maps.KRoolTiny):
                        spawner_id = 12 if m.map_index == Maps.KRoolTiny else 4
                        remove_kr_call = {
                            "unk0": 5,
                            "command": 13,
                            "head": [0, 0],
                            "detailed_command": {
                                "sub_command": 4,
                                "params": [spawner_id, 17, 0, 0],
                            },
                            "duration": 0,
                        }
                        data["point_data"].insert(0, remove_kr_call)
                with open(f"{m_path}/end_cs_p{x + 1}.json", "w") as fg:
                    fg.write(json.dumps(data, indent=4))


def updateSpawnerFiles(pre: str = ""):
    """Update spawner files to include all the spawners used for the cutscenes."""
    with open(f"{pre}{ROMName}", "rb") as fh:
        chunky_phase_file = ROMPointerFile(fh, TableNames.Spawners, Maps.KRoolChunky)
        for m in MAP_DATA:
            m.updateFile(fh, ROMPointerFile(fh, TableNames.Spawners, m.map_index))
        with open("temp.bin", "wb") as fg:
            fh.seek(chunky_phase_file.start)
            data = fh.read(chunky_phase_file.size)
            if chunky_phase_file.compressed:
                data = zlib.decompress(data, (15 + 32))
            fg.write(data)
    chunky_phase_data = {
        4: None,
        10: None,
        11: None,
        12: None,
        13: None,
        14: None,
        15: None,
        16: None,
        17: None,
        18: None,
    }
    # Get data from the chunky phase file
    with open("temp.bin", "rb") as fh:
        fence_count = int.from_bytes(fh.read(2), "big")
        offset = 2
        fence_data = {}
        if fence_count > 0:
            for _ in range(fence_count):
                current_fence = {
                    "fence_6": [],
                    "fence_A": [],
                    "foot": None,
                    "fence_id": None,
                }
                fh.seek(offset)
                point_count = int.from_bytes(fh.read(2), "big")
                for _ in range(point_count):
                    fx = int.from_bytes(fh.read(2), "big")
                    fy = int.from_bytes(fh.read(2), "big")
                    fz = int.from_bytes(fh.read(2), "big")
                    current_fence["fence_6"].append(
                        {
                            "x": fx,
                            "y": fy,
                            "z": fz,
                        }
                    )
                offset += (point_count * 6) + 2
                fh.seek(offset)
                point0_count = int.from_bytes(fh.read(2), "big")
                for _ in range(point0_count):
                    fx = int.from_bytes(fh.read(2), "big")
                    fy = int.from_bytes(fh.read(2), "big")
                    fz = int.from_bytes(fh.read(2), "big")
                    fa = int.from_bytes(fh.read(2), "big")
                    fb = int.from_bytes(fh.read(2), "big")
                    current_fence["fence_A"].append(
                        {
                            "x": fx,
                            "y": fy,
                            "z": fz,
                            "a": fa,
                            "b": fb,
                        }
                    )
                offset += (point0_count * 10) + 6
                fence_finish = offset
                fh.seek(fence_finish - 4)
                fence_id = int.from_bytes(fh.read(2), "big")
                current_fence["fence_id"] = fence_id
                current_fence["foot"] = int.from_bytes(fh.read(2), "big")
                fence_data[fence_id] = current_fence
                fh.seek(fence_finish)
        fh.seek(offset)
        spawner_count = int.from_bytes(fh.read(2), "big")
        offset += 2
        for _ in range(spawner_count):
            # Parse spawners
            fh.seek(offset + 0x13)
            enemy_index = int.from_bytes(fh.read(1), "big")
            grab_spawner = enemy_index in chunky_phase_data
            fh.seek(offset + 0xE)
            fence_index = int.from_bytes(fh.read(1), "big")
            init_offset = offset
            fh.seek(offset + 0x11)
            extra_count = int.from_bytes(fh.read(1), "big")
            offset += 0x16 + (extra_count * 2)
            end_offset = offset
            # Pass data to storage if necessary
            if grab_spawner:
                fh.seek(init_offset)
                spawner_size = end_offset - init_offset
                chunky_phase_data[enemy_index] = {"fence": fence_data[fence_index], "spawner_bytes": fh.read(spawner_size)}
    # Create new spawner files
    for m in MAP_DATA:
        # Write stored file stream
        with open(f"{pre}spawner_{m.folder}.bin", "wb") as fh:
            fh.write(m.file_stream)
        fence_data = []
        spawner_data = []
        used_fence_ids = []
        # Grab data from vanilla spawners
        with open(f"{pre}spawner_{m.folder}.bin", "rb") as fh:
            fence_count = int.from_bytes(fh.read(2), "big")
            offset = 2
            if fence_count > 0:
                for _ in range(fence_count):
                    fence_start = offset
                    fh.seek(offset)
                    point_count = int.from_bytes(fh.read(2), "big")
                    offset += (point_count * 6) + 2
                    fh.seek(offset)
                    point0_count = int.from_bytes(fh.read(2), "big")
                    offset += (point0_count * 10) + 6
                    fence_finish = offset
                    fh.seek(fence_finish - 4)
                    fence_id = int.from_bytes(fh.read(2), "big")
                    used_fence_ids.append(fence_id)
                    fh.seek(fence_start)
                    fence_data.append(fh.read(fence_finish - fence_start))
                    fh.seek(fence_finish)
            fh.seek(offset)
            spawner_count = int.from_bytes(fh.read(2), "big")
            offset += 2
            for _ in range(spawner_count):
                # Parse spawners
                init_offset = offset
                fh.seek(offset + 0x11)
                extra_count = int.from_bytes(fh.read(1), "big")
                offset += 0x16 + (extra_count * 2)
                end_offset = offset
                fh.seek(init_offset)
                spawner_data.append(fh.read(end_offset - init_offset))
        # Write new stuff in
        placed_fence_ids = []
        with open(f"{pre}spawner_{m.folder}.bin", "wb") as fh:
            fence_tying = {}
            fence_count = len(fence_data) + 3
            spawner_count = len(spawner_data) + len(list(chunky_phase_data.keys()))
            # Fences
            fh.write(fence_count.to_bytes(2, "big"))
            for f in fence_data:
                fh.write(f)
            for i in chunky_phase_data:
                i_data = chunky_phase_data[i]
                fence_id = m.fence_start + i_data["fence"]["fence_id"]
                fence_tying[i] = fence_id
                if fence_id in placed_fence_ids:
                    continue
                placed_fence_ids.append(fence_id)
                fh.write(len(i_data["fence"]["fence_6"]).to_bytes(2, "big"))
                for j in i_data["fence"]["fence_6"]:
                    fh.write(j["x"].to_bytes(2, "big"))
                    fh.write(j["y"].to_bytes(2, "big"))
                    fh.write(j["z"].to_bytes(2, "big"))
                fh.write(len(i_data["fence"]["fence_A"]).to_bytes(2, "big"))
                for j in i_data["fence"]["fence_A"]:
                    fh.write(j["x"].to_bytes(2, "big"))
                    fh.write(j["y"].to_bytes(2, "big"))
                    fh.write(j["z"].to_bytes(2, "big"))
                    fh.write(j["a"].to_bytes(2, "big"))
                    fh.write(j["b"].to_bytes(2, "big"))
                fh.write(fence_id.to_bytes(2, "big"))
                fh.write(i_data["fence"]["foot"].to_bytes(2, "big"))
            # Spawners
            fh.write(spawner_count.to_bytes(2, "big"))
            for s in spawner_data:
                fh.write(s)
            for i in chunky_phase_data:
                s_start = fh.tell()
                i_data = chunky_phase_data[i]
                fh.write(i_data["spawner_bytes"])
                s_end = fh.tell()
                fh.seek(s_start + 0x13)
                new_id = None
                if i == 4:
                    new_id = m.spawner_start
                elif id == 1:
                    new_id = m.kr_actual_id
                elif id == 2:
                    new_id = m.kong_cs_id
                else:
                    new_id = (i - 10) + m.spawner_start + 1
                fh.write(new_id.to_bytes(1, "big"))
                fh.seek(s_start + 0xE)
                fh.write(fence_tying[i].to_bytes(1, "big"))
                # I *think* this causes crashes on N64
                # if i == 11:
                #     fh.seek(s_start + 0xA)
                #     fh.write(m.cs_model.to_bytes(1, "big"))
                fh.seek(s_end)
    if os.path.exists("temp.bin"):
        os.remove("temp.bin")


def updatePathFiles(pre: str = ""):
    """Update path files so that the boot follows the correct path."""
    with open(f"{pre}{ROMName}", "rb") as fh:
        chunky_phase_file = ROMPointerFile(fh, TableNames.Paths, Maps.KRoolChunky)
        for m in MAP_DATA:
            m.updatePath(fh, ROMPointerFile(fh, TableNames.Paths, m.map_index))
        with open("temp.bin", "wb") as fg:
            fh.seek(chunky_phase_file.start)
            data = fh.read(chunky_phase_file.size)
            if chunky_phase_file.compressed:
                data = zlib.decompress(data, (15 + 32))
            fg.write(data)
    # Grab Chunky Phase data (Just skip the count)
    boot_path = None
    with open("temp.bin", "rb") as fh:
        fh.seek(2)
        boot_path = fh.read()
    for m in MAP_DATA:
        local_paths = []
        used_indexes = []
        path_count = 0
        with open(f"path_{m.folder}.bin", "wb") as fg:
            fg.write(m.path_stream)
        with open(f"path_{m.folder}.bin", "rb") as fg:
            path_count = int.from_bytes(fg.read(2), "big")
            for _ in range(path_count):
                path_start = fg.tell()
                path_index = int.from_bytes(fg.read(2), "big")
                point_count = int.from_bytes(fg.read(2), "big")
                used_indexes.append(path_index)
                path_size = 6 + (point_count * 10)
                fg.seek(path_start)
                local_paths.append(fg.read(path_size))
                fg.seek(path_start + path_size)
        with open(f"path_{m.folder}.bin", "wb") as fg:
            new_path_count = path_count + 1
            fg.write(new_path_count.to_bytes(2, "big"))
            for k in local_paths:
                fg.write(k)
            new_path_index = 0
            while new_path_index in used_indexes:
                new_path_index += 1
            fg.write(new_path_index.to_bytes(2, "big"))
            fg.write(boot_path[2:])
    if os.path.exists("temp.bin"):
        os.remove("temp.bin")
