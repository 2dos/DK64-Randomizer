"""Apply cosmetic elements of Kong Rando."""
from imp import source_from_cache
from random import shuffle

import js
from randomizer.Patcher import ROM
from randomizer.Spoiler import Spoiler
from randomizer.EnemyTypes import Enemies


def apply_kongrando_cosmetic(spoiler: Spoiler):
    """Rando write bananaport locations."""
    if spoiler.settings.kong_rando:
        gunswitches = [0x129, 0x126, 0x128, 0x127, 0x125]
        greenslamswitches = [0x94, 0x93, 0x95, 0x96, 0x92]
        instrumentpads = [0xA8, 0xA9, 0xAC, 0xAA, 0xAB]
        actors = [Enemies.CutsceneDK, Enemies.CutsceneDiddy, Enemies.CutsceneLanky, Enemies.CutsceneTiny, Enemies.CutsceneChunky]

        llama_entrance_switch = []
        # llama_kong = spoiler.shuffled_kong_placement["Llama Temple"]["puzzle"]["kong"]
        # if llama_kong in [1, 4]:
        #     llama_entrance_switch.append({"index": 0xD, "new_type": gunswitches[llama_kong]})

        kongrando_changes = [
            {
                "map_index": 7,
                "model2_changes": [
                    {
                        "index": 0x30,
                        "new_type": gunswitches[spoiler.shuffled_kong_placement["Jungle Japes"]["puzzle"]["kong"]],
                    },
                    {
                        "index": 0x31,
                        "new_type": gunswitches[spoiler.shuffled_kong_placement["Jungle Japes"]["puzzle"]["kong"]],
                    },
                    {
                        "index": 0x32,
                        "new_type": gunswitches[spoiler.shuffled_kong_placement["Jungle Japes"]["puzzle"]["kong"]],
                    },
                ],
                "charspawner_changes": [
                    {"type": Enemies.CutsceneDiddy, "new_type": actors[spoiler.shuffled_kong_placement["Jungle Japes"]["locked"]["kong"]]},
                ],
            },
            {"map_index": 0x26, "model2_changes": llama_entrance_switch, "charspawner_changes": []},
            {
                "map_index": 0x14,
                "model2_changes": [
                    {
                        "index": 0x16,
                        "new_type": instrumentpads[spoiler.shuffled_kong_placement["Llama Temple"]["puzzle"]["kong"]],
                    },
                    {
                        "index": 0x12,
                        "new_type": gunswitches[spoiler.shuffled_kong_placement["Llama Temple"]["puzzle"]["kong"]],
                    },
                ],
                "charspawner_changes": [
                    {"type": Enemies.CutsceneLanky, "new_type": actors[spoiler.shuffled_kong_placement["Llama Temple"]["locked"]["kong"]]},
                ],
            },
            {
                "map_index": 0x10,
                "model2_changes": [
                    {
                        "index": 0x0,
                        "new_type": greenslamswitches[spoiler.shuffled_kong_placement["Tiny Temple"]["puzzle"]["kong"]],
                    },
                    {
                        "index": 0x4,
                        "new_type": instrumentpads[spoiler.shuffled_kong_placement["Tiny Temple"]["puzzle"]["kong"]],
                    },
                ],
                "charspawner_changes": [
                    {"type": Enemies.CutsceneTiny, "new_type": actors[spoiler.shuffled_kong_placement["Tiny Temple"]["locked"]["kong"]]},
                ],
            },
            {
                "map_index": 0x1A,
                "model2_changes": [
                    {
                        "index": 0x24,
                        "new_type": greenslamswitches[spoiler.shuffled_kong_placement["Frantic Factory"]["puzzle"]["kong"]],
                    },
                ],
                "charspawner_changes": [
                    {"type": Enemies.CutsceneChunky, "new_type": actors[spoiler.shuffled_kong_placement["Frantic Factory"]["locked"]["kong"]]},
                ],
            },
        ]

        for kong_map in spoiler.shuffled_kong_placement.keys():
            for link_type in spoiler.shuffled_kong_placement[kong_map].keys():
                ROM().seek(0x1FED020 + spoiler.shuffled_kong_placement[kong_map][link_type]["write"])
                ROM().writeMultipleBytes(spoiler.shuffled_kong_placement[kong_map][link_type]["kong"], 1)

        for cont_map in kongrando_changes:
            cont_map_id = int(cont_map["map_index"])
            # Setup
            cont_map_setup_address = js.pointer_addresses[9]["entries"][cont_map_id]["pointing_to"]
            ROM().seek(cont_map_setup_address)
            model2_count = int.from_bytes(ROM().readBytes(4), "big")
            for x in range(model2_count):
                start = cont_map_setup_address + 4 + (x * 0x30)
                ROM().seek(start + 0x2A)
                obj_id = int.from_bytes(ROM().readBytes(2), "big")
                has_id = False
                new_type = 0
                for model2 in cont_map["model2_changes"]:
                    if model2["index"] == obj_id:
                        has_id = True
                        new_type = model2["new_type"]
                if has_id:
                    ROM().seek(start + 0x28)
                    ROM().writeMultipleBytes(new_type, 2)
            # Character Spawners
            cont_map_spawner_address = js.pointer_addresses[16]["entries"][cont_map_id]["pointing_to"]
            ROM().seek(cont_map_spawner_address)
            fence_count = int.from_bytes(ROM().readBytes(2), "big")
            offset = 2
            if fence_count > 0:
                for x in range(fence_count):
                    ROM().seek(cont_map_spawner_address + offset)
                    point_count = int.from_bytes(ROM().readBytes(2), "big")
                    offset += (point_count * 6) + 2
                    ROM().seek(cont_map_spawner_address + offset)
                    point0_count = int.from_bytes(ROM().readBytes(2), "big")
                    offset += (point0_count * 10) + 6
            ROM().seek(cont_map_spawner_address + offset)
            spawner_count = int.from_bytes(ROM().readBytes(2), "big")
            offset += 2
            for x in range(spawner_count):
                ROM().seek(cont_map_spawner_address + offset)
                enemy_id = int.from_bytes(ROM().readBytes(1), "big")
                init_offset = offset
                ROM().seek(cont_map_spawner_address + offset + 0x11)
                extra_count = int.from_bytes(ROM().readBytes(1), "big")
                offset += 0x16 + (extra_count * 2)
                has_id = False
                new_type = 0
                for char in cont_map["charspawner_changes"]:
                    if char["type"] == enemy_id:
                        has_id = True
                        new_type = char["new_type"]
                if has_id:
                    ROM().seek(cont_map_spawner_address + init_offset)
                    ROM().writeMultipleBytes(new_type, 1)
