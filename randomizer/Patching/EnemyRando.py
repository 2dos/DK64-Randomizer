"""Apply Boss Locations."""
import random

import js
from randomizer.Lists.EnemyTypes import Enemies, EnemyMetaData
from randomizer.Lists.MapsAndExits import Maps
from randomizer.Patching.Patcher import ROM
from randomizer.Spoiler import Spoiler


def getBalancedCrownEnemyRando():
    """Get array of weighted enemies."""
    temp = []
    for enemy in EnemyMetaData.keys():
        if EnemyMetaData[enemy].crown_enabled:
            for x in range(EnemyMetaData[enemy].crown_weight):
                temp.append(enemy)
    return temp


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
        # Maps.CavesChunkyIgloo, # Fireball with glasses is here
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
        Maps.ForestGiantMushroom,
        Maps.ForestLankyZingersRoom,
        Maps.CastleBoss,
    ]
    crown_maps = [
        Maps.JapesCrown,
        Maps.AztecCrown,
        Maps.FactoryCrown,
        Maps.GalleonCrown,
        Maps.ForestCrown,
        Maps.CavesCrown,
        Maps.CastleCrown,
        Maps.HelmCrown,
        Maps.SnidesCrown,
        Maps.LobbyCrown,
    ]
    enemy_classes = {
        "ground_simple": [
            Enemies.BeaverBlue,
            Enemies.KlaptrapGreen,
            Enemies.KlaptrapPurple,
            Enemies.KlaptrapRed,
            Enemies.BeaverGold,
            Enemies.MushroomMan,
            Enemies.Ruler,
            Enemies.Kremling,
            Enemies.Krossbones,
            Enemies.MrDice0,
            Enemies.MrDice1,
            Enemies.SirDomino,
            Enemies.FireballGlasses,
            Enemies.SpiderSmall,
            Enemies.Ghost,
        ],
        "air": [
            Enemies.ZingerCharger,
            Enemies.ZingerLime,
            Enemies.ZingerRobo,
            Enemies.Bat,
            # Enemies.Bug, # Crashes on N64
            # Enemies.Book, # Causes way too many problems
        ],
        "ground_beefyboys": [
            Enemies.Klump,
            Enemies.RoboKremling,
            # Enemies.EvilTomato, # Causes way too many problems
            Enemies.Kosha,
            Enemies.Klobber,
            Enemies.Kaboom,
        ],
        "water": [
            Enemies.Shuri,
            Enemies.Gimpfish,
            Enemies.Pufftup,
        ],
    }
    crown_enemies = []
    if spoiler.settings.enemy_rando or spoiler.settings.kasplat_rando:  # TODO: Add option for crown enemy rando
        crown_enemies = getBalancedCrownEnemyRando()
        for cont_map_id in range(216):
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
            crown_swaps = []
            # Generate Enemy Swaps lists
            for enemy_class in enemy_classes:
                arr = []
                for x in range(spawner_count):
                    arr.append(random.choice(enemy_classes[enemy_class]))
                enemy_swaps[enemy_class] = arr
            for x in range(spawner_count):
                crown_swaps.append(random.choice(crown_enemies))
            offset += 2
            for x in range(spawner_count):
                ROM().seek(cont_map_spawner_address + offset)
                enemy_id = int.from_bytes(ROM().readBytes(1), "big")
                ROM().seek(cont_map_spawner_address + offset + 0x13)
                enemy_index = int.from_bytes(ROM().readBytes(1), "big")
                init_offset = offset
                ROM().seek(cont_map_spawner_address + offset + 0x11)
                extra_count = int.from_bytes(ROM().readBytes(1), "big")
                offset += 0x16 + (extra_count * 2)
                vanilla_spawners.append({"enemy_id": enemy_id, "offset": init_offset, "index": enemy_index})
            if spoiler.settings.kasplat_rando:
                for cont_map in spoiler.enemy_replacements:
                    if cont_map["container_map"] == cont_map_id:
                        for kasplat in cont_map["kasplat_swaps"]:
                            source_kasplat_type = kasplat["vanilla_location"] + Enemies.KasplatDK
                            replacement_kasplat_type = kasplat["replace_with"] + Enemies.KasplatDK
                            for spawner in vanilla_spawners:
                                if spawner["enemy_id"] == source_kasplat_type:
                                    ROM().seek(cont_map_spawner_address + spawner["offset"])
                                    ROM().writeMultipleBytes(replacement_kasplat_type, 1)
            if spoiler.settings.enemy_rando and cont_map_id in valid_maps:
                for enemy_class in enemy_swaps:
                    arr = enemy_swaps[enemy_class]
                    class_types = enemy_classes[enemy_class]
                    sub_index = 0
                    for spawner in vanilla_spawners:
                        if spawner["enemy_id"] in class_types:
                            if cont_map_id != Maps.FranticFactory or spawner["index"] < 35 or spawner["index"] > 44:
                                new_enemy_id = arr[sub_index]
                                sub_index += 1
                                if new_enemy_id != Enemies.Book or cont_map_id not in (Maps.CavesDonkeyCabin, Maps.JapesLankyCave, Maps.AngryAztecLobby):
                                    if new_enemy_id != Enemies.Bug or cont_map_id != Maps.CavesDiddyLowerCabin:
                                        ROM().seek(cont_map_spawner_address + spawner["offset"])
                                        ROM().writeMultipleBytes(new_enemy_id, 1)
                                        if new_enemy_id in EnemyMetaData.keys():
                                            ROM().seek(cont_map_spawner_address + spawner["offset"] + 0x10)
                                            ROM().writeMultipleBytes(EnemyMetaData[new_enemy_id].aggro, 1)
                                            if new_enemy_id == Enemies.RoboKremling:
                                                ROM().seek(cont_map_spawner_address + spawner["offset"] + 0xB)
                                                ROM().writeMultipleBytes(0xC8, 1)
                                            ROM().seek(cont_map_spawner_address + spawner["offset"] + 0xF)
                                            default_scale = int.from_bytes(ROM().readBytes(1), "big")
                                            if EnemyMetaData[new_enemy_id].size_cap > 0:
                                                if default_scale > EnemyMetaData[new_enemy_id].size_cap:
                                                    ROM().seek(cont_map_spawner_address + spawner["offset"] + 0xF)
                                                    ROM().writeMultipleBytes(EnemyMetaData[new_enemy_id].size_cap, 1)
                                            min_speed = EnemyMetaData[new_enemy_id].min_speed
                                            max_speed = EnemyMetaData[new_enemy_id].max_speed
                                            if min_speed > 0 and max_speed > 0:
                                                ROM().seek(cont_map_spawner_address + spawner["offset"] + 0xD)
                                                agg_speed = random.randint(min_speed, max_speed)
                                                ROM().writeMultipleBytes(agg_speed, 1)
                                                ROM().seek(cont_map_spawner_address + spawner["offset"] + 0xC)
                                                ROM().writeMultipleBytes(random.randint(min_speed, agg_speed), 1)
            if spoiler.settings.enemy_rando and cont_map_id in crown_maps:  # TODO: Change the first condition to a unique condition
                crown_index = 0
                for spawner in vanilla_spawners:
                    if spawner["enemy_id"] in crown_enemies:
                        new_enemy_id = crown_swaps[crown_index]
                        ROM().seek(cont_map_spawner_address + spawner["offset"])
                        ROM().writeMultipleBytes(new_enemy_id, 1)
                        crown_index += 1
                        if new_enemy_id in EnemyMetaData.keys():
                            ROM().seek(cont_map_spawner_address + spawner["offset"] + 0x10)
                            ROM().writeMultipleBytes(EnemyMetaData[new_enemy_id].aggro, 1)
                            if new_enemy_id == Enemies.RoboKremling:
                                ROM().seek(cont_map_spawner_address + spawner["offset"] + 0xB)
                                ROM().writeMultipleBytes(0xC8, 1)
                            if EnemyMetaData[new_enemy_id].air:
                                ROM().seek(cont_map_spawner_address + spawner["offset"] + 0x6)
                                ROM().writeMultipleBytes(300, 2)
                            ROM().seek(cont_map_spawner_address + spawner["offset"] + 0xF)
                            default_scale = int.from_bytes(ROM().readBytes(1), "big")
                            if EnemyMetaData[new_enemy_id].size_cap > 0:
                                if default_scale > EnemyMetaData[new_enemy_id].size_cap:
                                    ROM().seek(cont_map_spawner_address + spawner["offset"] + 0xF)
                                    ROM().writeMultipleBytes(EnemyMetaData[new_enemy_id].size_cap, 1)
                            min_speed = EnemyMetaData[new_enemy_id].min_speed
                            max_speed = EnemyMetaData[new_enemy_id].max_speed
                            if min_speed > 0 and max_speed > 0:
                                ROM().seek(cont_map_spawner_address + spawner["offset"] + 0xD)
                                agg_speed = random.randint(min_speed, max_speed)
                                ROM().writeMultipleBytes(agg_speed, 1)
                                ROM().seek(cont_map_spawner_address + spawner["offset"] + 0xC)
                                ROM().writeMultipleBytes(random.randint(min_speed, agg_speed), 1)
                    elif spawner["enemy_id"] == Enemies.BattleCrownController:
                        ROM().seek(cont_map_spawner_address + spawner["offset"] + 0xB)
                        ROM().writeMultipleBytes(random.randint(5, 60), 1)  # Determine Crown length. DK64 caps at 255 seconds
