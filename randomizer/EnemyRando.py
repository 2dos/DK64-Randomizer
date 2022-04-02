"""Apply Boss Locations."""
import js
import random
from randomizer.Patcher import ROM
from randomizer.Spoiler import Spoiler
from randomizer.MapsAndExits import Maps


def randomize_enemies(spoiler: Spoiler):
    """Write replaced enemies to ROM."""
    enemy_replacements = [
        {
            "container_map": 7,
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
        }
    ]
    valid_maps = [
        Maps.JapesMountain,
        Maps.JungleJapes,
        Maps.JapesTinyHive,
        Maps.JapesLankyCave,
        Maps.AztecTinyTemple,
        Maps.HideoutHelm,
        Maps.AztecDonkey5DTemple,
        Maps.AztecDiddy5DTemple,
        Maps.AztecLanky5DTemple,
        Maps.AztecTiny5DTemple,
        Maps.AztecChunky5DTemple,
        Maps.AztecLlamaTemple,
        Maps.FranticFactory,
        Maps.FactoryPowerHut,
        Maps.GloomyGalleon,
        Maps.GalleonSickBay,
        Maps.JapesUnderGround,
        Maps.Isles,
        Maps.FactoryCrusher,
        Maps.AngryAztec,
        Maps.GalleonSealRace,
        Maps.JapesBaboonBlast,
        Maps.AztecBaboonBlast,
        Maps.Galleon2DShip,
        Maps.Galleon5DShipDiddyLankyChunky,
        Maps.Galleon5DShipDKTiny,
        Maps.GalleonTreasureChest,
        Maps.GalleonMermaidRoom,
        Maps.FungiForest,
        Maps.GalleonLighthouse,
        Maps.GalleonMechafish,
        Maps.ForestAnthill,
        Maps.GalleonBaboonBlast,
        Maps.ForestMinecarts,
        Maps.ForestMillAttic,
        Maps.ForestRafters,
        Maps.ForestMillAttic,
        Maps.ForestThornvineBarn,
        Maps.ForestSpider,
        Maps.ForestMillFront,
        Maps.ForestMillBack,
        Maps.ForestLankyMushroomsRoom,
        Maps.CrystalCaves,
        Maps.CavesDonkeyIgloo,
        Maps.CavesDiddyIgloo,
        Maps.CavesLankyIgloo,
        Maps.CavesTinyIgloo,
        Maps.CavesChunkyIgloo,
        Maps.CavesDonkeyCabin,
        Maps.CavesDiddyLowerCabin,
        Maps.CavesDiddyUpperCabin,
        Maps.CavesLankyCabin,
        Maps.CavesTinyCabin,
        Maps.CavesChunkyCabin,
        Maps.CreepyCastle,
        Maps.CastleBallroom,
        Maps.CavesRotatingCabin,
        Maps.CavesFrozenCastle,
        Maps.CastleCrypt,
        Maps.CastleMausoleum,
        Maps.CastleUpperCave,
        Maps.CastleLowerCave,
        Maps.CastleTower,
        Maps.CastleMinecarts,
        Maps.FactoryBaboonBlast,
        Maps.CastleMuseum,
        Maps.CastleLibrary,
        Maps.CastleDungeon,
        Maps.CastleTree,
        Maps.CastleShed,
        Maps.CastleTrashCan,
        Maps.JungleJapesLobby,
        Maps.AngryAztecLobby,
        Maps.FranticFactoryLobby,
        Maps.GloomyGalleonLobby,
        Maps.FungiForestLobby,
        Maps.CrystalCavesLobby,
        Maps.CreepyCastleLobby,
        Maps.HideoutHelmLobby,
        Maps.GalleonSubmarine,
        Maps.CavesBaboonBlast,
        Maps.CastleBaboonBlast,
        Maps.ForestBaboonBlast,
        Maps.IslesSnideRoom,
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
        for cont_map_id in valid_maps:
            cont_map_spawner_address = js.pointer_addresses[16]["entries"][cont_map_id]["pointing_to"]
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
            enemy_swaps = {}
            # Generate Enemy Swaps lists
            for enemy_class in enemy_classes:
                arr = []
                for x in range(spawner_count):
                    arr.append(random.choice(enemy_classes[enemy_class]))
                enemy_swaps[enemy_class] = arr
            offset += 2
            for x in range(spawner_count):
                ROM().seek(cont_map_spawner_address + offset)
                enemy_id = int.from_bytes(ROM().readBytes(1), "big")
                init_offset = offset
                ROM().seek(cont_map_spawner_address + offset + 0x11)
                extra_count = int.from_bytes(ROM().readBytes(1), "big")
                offset += 0x16 + (extra_count * 2)
                vanilla_spawners.append({"enemy_id": enemy_id, "offset": init_offset})
            # Comment out kasplat rando until kasplat rando is implemented
            # for kasplat in cont_map["kasplat_swaps"]:
            #     source_kasplat_type = kasplat["vanilla_location"] + 0x3D
            #     replacement_kasplat_type = kasplat["replace_with"] + 0x3D
            #     for spawner in vanilla_spawners:
            #         if spawner["enemy_id"] == source_kasplat_type:
            #             ROM().seek(cont_map_spawner_address + spawner["offset"])
            #             ROM().writeMultipleBytes(replacement_kasplat_type,1)
            for enemy_class in enemy_swaps:
                arr = enemy_swaps[enemy_class]
                class_types = enemy_classes[enemy_class]
                sub_index = 0
                for spawner in vanilla_spawners:
                    if spawner["enemy_id"] in class_types:
                        new_enemy_id = arr[sub_index]
                        ROM().seek(cont_map_spawner_address + spawner["offset"])
                        ROM().writeMultipleBytes(new_enemy_id, 1)
                        sub_index += 1
