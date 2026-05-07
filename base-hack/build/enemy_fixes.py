"""Enemy fixes for the base hack."""

from typing import BinaryIO
import zlib
from BuildEnums import TableNames, Maps, Enemies
from BuildLib import main_pointer_table_offset

default_control_states = {
    Enemies.ZingerRobo: 1,  # Robo-Zinger
    Enemies.RoboKremling: 1,  # Robo-Kremling
}


def fixFactoryDiddyPincodeEnemies(fh: BinaryIO):
    """Remove the feature where enemies in Diddy R&D are not responsive to instrument."""
    # Get Spawner File
    with open("factory_spawners.bin", "wb") as fg:
        fh.seek(main_pointer_table_offset + (4 * TableNames.Spawners))
        spawner_table = main_pointer_table_offset + int.from_bytes(fh.read(4), "big")
        fh.seek(spawner_table + (4 * Maps.Factory))
        spawner_start = main_pointer_table_offset + int.from_bytes(fh.read(4), "big")
        spawner_end = main_pointer_table_offset + int.from_bytes(fh.read(4), "big")
        spawner_size = spawner_end - spawner_start
        fh.seek(spawner_start)
        data = zlib.decompress(fh.read(spawner_size), (15 + 32))
        fg.write(data)
    # Manip file
    with open("factory_spawners.bin", "r+b") as fg:
        fence_count = int.from_bytes(fg.read(2), "big")
        offset = 2
        if fence_count > 0:
            for _ in range(fence_count):
                fg.seek(offset)
                point_count = int.from_bytes(fg.read(2), "big")
                offset += (point_count * 6) + 2
                fg.seek(offset)
                point0_count = int.from_bytes(fg.read(2), "big")
                offset += (point0_count * 10) + 6
        fg.seek(offset)
        spawner_count = int.from_bytes(fg.read(2), "big")
        offset += 2
        for _ in range(spawner_count):
            fg.seek(offset)
            enemy_id = int.from_bytes(fg.read(1), "big")
            fg.seek(offset + 0x13)
            enemy_index = int.from_bytes(fg.read(1), "big")
            if enemy_index >= 49 and enemy_index <= 56:
                # Pincode room enemy
                if enemy_id in default_control_states:
                    fg.seek(offset + 0x10)
                    fg.write(default_control_states[enemy_id].to_bytes(1, "big"))
            fg.seek(offset + 0x11)
            extra_count = int.from_bytes(fg.read(1), "big")
            offset += 0x16 + (extra_count * 2)
