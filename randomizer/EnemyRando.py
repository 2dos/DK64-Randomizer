"""Apply Boss Locations."""
from randomizer.Patcher import ROM
from randomizer.Spoiler import Spoiler

def randomize_enemies(spoiler: Spoiler):
    enemy_replacements = [
        {
            "container_map": 0x7,
            "kasplat_swaps": [
                {
                    "vanilla_location": 0,  # Kong index which is tied to the kasplat. Eg. This would take the DK Kasplat location (DK is kong 0)
                    "replace_with": 1,  # Which Kasplat will go in that position (0 = DK, 1 = Diddy etc)
                },
                {
                    "vanilla_location": 1,
                    "replace_with": 3,
                },
                {
                    "vanilla_location": 2,
                    "replace_with": 0,
                },
                {"vanilla_location": 3, "replace_with": 2},
            ],
            "enemy_swaps": {
                "ground_simple": [4, 3, 2, 3, 6, 12, 7, 3, 8, 3, 3, 12, 0, 5, 6, 10, 4, 12, 6, 8, 11, 7, 5, 9, 1, 7, 5, 5, 8, 6],
                "air": [1, 3, 2, 2, 2, 1, 2, 2, 1, 1, 3, 3, 1, 0, 0, 2, 0, 3, 2, 2, 1, 3, 0, 1, 1, 2, 3, 2, 2, 3],
                "ground_beefyboys": [1, 0, 2, 0, 1, 3, 0, 3, 3, 0, 0, 3, 0, 1, 2, 0, 0, 3, 0, 2, 0, 2, 3, 3, 2, 0, 3, 0, 2, 0],
                "water": [2, 1, 1, 0, 1, 0, 0, 0, 2, 0, 1, 1, 2, 0, 1, 1, 2, 1, 2, 1, 0, 1, 0, 0, 0, 1, 0, 2, 0, 0],
            },
        }
    ]

    enemy_classes = {
        "ground_simple": [
            0x00,  # Blue Beaver
            # 0x06, # Klobber (General Barrel Hider)
            # 0x10, # Kaboom (TNT Barrel Hider)
            0x1B,  # Klaptrap (Green)
            0x1E,  # Klaptrap (Purple)
            0x1F,  # Klaptrap (Red)
            0x21,  # Gold Beaver
            # 0x2C, # Mushroom Man
            0x33,  # Ruler
            0x3B,  # Kremling
            0x54,  # Krossbones
            0x57,  # Mr. Dice (0)
            0x58,  # Sir Domino
            0x59,  # Mr. Dice (1)
            0x5F,  # Spiderling
            0x65,  # Kritter-in-a-sheet
        ],
        "air": [
            0x05,  # Zinger (Charger)
            0x1C,  # Zinger (Bomber)
            0x53,  # Robo-Zinger
            0x63,  # Bat
        ],
        "ground_beefyboys": [
            0x09,  # Klump
            0x38,  # Robo-Kremling
            0x64,  # Evil Tomato
            0x67,  # Kosha
        ],
        "water": [
            0x55,  # Shuri
            0x56,  # Gimpfish
            0x66,  # Pufftup
        ],
    }

    if spoiler.settings.enemy_rando or spoiler.settings.kasplat_rando:
        cont_map_id = int(cont_map["container_map"])
        cont_map_spawner_address = js.pointer_addresses[16]["entries"][cont_map_id]["pointing_to"]
        for cont_map in enemy_replacements: # TODO: Change "enemy_replacements" with the appropriate spoiler array
            vanilla_spawners = []
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
                vanilla_spawners.append({"enemy_id": enemy_id, "offset": init_offset})
            for kasplat in cont_map["kasplat_swaps"]:
                source_kasplat_type = kasplat["vanilla_location"] + 0x3D
                replacement_kasplat_type = kasplat["replace_with"] + 0x3D
                for spawner in vanilla_spawners:
                    if spawner["enemy_id"] == source_kasplat_type:
                        ROM().seek(cont_map_spawner_address + spawner["offset"])
                        ROM().write(replacement_kasplat_type.to_bytes(1, "big"))
            for enemy_class in cont_map["enemy_swaps"]:
                arr = cont_map["enemy_swaps"][enemy_class]
                class_types = enemy_classes[enemy_class]
                sub_index = 0
                for spawner in vanilla_spawners:
                    if spawner["enemy_id"] in class_types:
                        new_class_index = arr[sub_index]
                        new_enemy_id = class_types[new_class_index]
                        ROM().seek(cont_map_spawner_address + spawner["offset"])
                        ROM().write(new_enemy_id.to_bytes(1, "big"))
                        sub_index += 1
