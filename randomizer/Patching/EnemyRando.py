"""Apply Boss Locations."""
import random
from email.policy import default

import js
from randomizer.Lists.EnemyTypes import Enemies, EnemyMetaData
from randomizer.Lists.MapsAndExits import Maps
from randomizer.Patching.Patcher import ROM
from randomizer.Spoiler import Spoiler


def getBalancedCrownEnemyRando(crown_setting, damage_ohko_setting):
    """Get array of weighted enemies."""
    # this library will contain a list for every enemy it needs to generate
    enemy_swaps_library = {}

    if crown_setting != "off":

        # library of every crown map. will have a list of all enemies to put in those maps.
        enemy_swaps_library = {
            Maps.JapesCrown: [],
            Maps.AztecCrown: [],
            Maps.FactoryCrown: [],
            Maps.GalleonCrown: [],
            Maps.ForestCrown: [],
            Maps.CavesCrown: [],
            Maps.CastleCrown: [],
            Maps.HelmCrown: [],
            Maps.SnidesCrown: [],
            Maps.LobbyCrown: [],
        }
        # make 5 lists of enemies, per category.
        every_enemy = []  # every enemy (that can appear in crown battles)
        disruptive_max_1 = []  # anything that isn't... "2" disruptive (because disruptive is 1, at most)
        disruptive_at_most_kasplat = []  # anything that isn't marked as "disruptive"
        disruptive_0 = []  # the easiest enemies
        legacy_hard_mode = []  # legacy map with the exact same balance as the old "Hard" mode

        # fill in the lists with the possibilities that belong in them.
        for enemy in EnemyMetaData:
            if EnemyMetaData[enemy].crown_enabled and enemy is not Enemies.GetOut:
                every_enemy.append(enemy)
                if EnemyMetaData[enemy].disruptive <= 1:
                    disruptive_max_1.append(enemy)
                if EnemyMetaData[enemy].kasplat is True:
                    disruptive_at_most_kasplat.append(enemy)
                elif EnemyMetaData[enemy].disruptive == 0:
                    disruptive_at_most_kasplat.append(enemy)
                    disruptive_0.append(enemy)
        # the legacy_hard_mode list is trickier to fill, but here goes:
        bias = 2
        for enemy in EnemyMetaData.keys():
            if EnemyMetaData[enemy].crown_enabled:
                base_weight = EnemyMetaData[enemy].crown_weight
                weight_diff = abs(base_weight - bias)
                new_weight = abs(10 - weight_diff)
                if damage_ohko_setting is False or enemy is not Enemies.GetOut:
                    for count in range(new_weight):
                        legacy_hard_mode.append(enemy)
        # picking enemies to put in the crown battles
        if crown_setting == "easy":
            for map_id in enemy_swaps_library:
                enemy_swaps_library[map_id].append(random.choice(disruptive_max_1))
                enemy_swaps_library[map_id].append(random.choice(disruptive_0))
                enemy_swaps_library[map_id].append(random.choice(disruptive_0))
                if map_id == Maps.GalleonCrown or map_id == Maps.LobbyCrown or map_id == Maps.HelmCrown:
                    enemy_swaps_library[map_id].append(random.choice(disruptive_0))
        elif crown_setting == "medium":
            new_enemy = 0
            for map_id in enemy_swaps_library:
                count_disruptive = 0
                count_kasplats = 0
                number_of_enemies = 3
                get_out_spawned_this_map = False
                if map_id == Maps.GalleonCrown or map_id == Maps.LobbyCrown or map_id == Maps.HelmCrown:
                    number_of_enemies = 4
                for count in range(number_of_enemies):
                    if count_disruptive == 0:
                        if count_kasplats < 2:
                            new_enemy = random.choice(every_enemy)
                        elif count_kasplats == 2:
                            new_enemy = random.choice(disruptive_max_1)
                        elif count_kasplats == 3:
                            new_enemy = random.choice(disruptive_0)
                    elif count_disruptive == 1:
                        if count_kasplats < 2:
                            new_enemy = random.choice(disruptive_max_1)
                        elif count_kasplats == 2:
                            new_enemy = random.choice(disruptive_0)
                    elif count_disruptive == 2:
                        if count_kasplats == 0:
                            new_enemy = random.choice(disruptive_at_most_kasplat)
                        elif count_kasplats == 1:
                            new_enemy = random.choice(disruptive_0)
                    elif count_kasplats > 3 or (count_kasplats > 2 and count_disruptive > 1) or (count_kasplats == 2 and count_disruptive == 2):
                        print("This is a mistake in the crown enemy algorithm. Report this to the devs.")
                        new_enemy = Enemies.BeaverGold
                    # Add in a chance for Get Out to appear in crown battles.
                    if damage_ohko_setting is False and count_disruptive < 2 and get_out_spawned_this_map is False and random.randint(0, 1000) > 994:
                        new_enemy = Enemies.GetOut
                        get_out_spawned_this_map = True
                    # We picked a new enemy, let's update our information and add it to the list
                    if EnemyMetaData[new_enemy].kasplat is True:
                        count_kasplats = count_kasplats + 1
                    count_disruptive = EnemyMetaData[new_enemy].disruptive + count_disruptive
                    enemy_swaps_library[map_id].append(new_enemy)
        elif crown_setting == "hard":
            for map_id in enemy_swaps_library:
                number_of_enemies = 3
                if map_id == Maps.GalleonCrown or map_id == Maps.LobbyCrown or map_id == Maps.HelmCrown:
                    number_of_enemies = 4
                for count in range(number_of_enemies):
                    enemy_swaps_library[map_id].append(random.choice(legacy_hard_mode))
        # one last shuffle, to make sure any enemy can spawn in any spot
        for map_id in enemy_swaps_library:
            if len(enemy_swaps_library[map_id]) > 0:
                random.shuffle(enemy_swaps_library[map_id])
    return enemy_swaps_library


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
        # Maps.ForestSpider, # Causes a lot of enemies to fall into the pit of their own volition
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
    minigame_maps_easy = [
        # Maps.BusyBarrelBarrageEasy, # Requires enemies be of a certain size
        # Maps.BusyBarrelBarrageHard, # ^
        # Maps.BusyBarrelBarrageNormal, # ^
        # Maps.HelmBarrelDiddyKremling, # Only kremlings activate the switch
        Maps.HelmBarrelChunkyHidden,
        Maps.HelmBarrelChunkyShooting,
    ]
    minigame_maps_beatable = [
        Maps.MadMazeMaulEasy,
        Maps.MadMazeMaulNormal,
        Maps.MadMazeMaulHard,
        Maps.MadMazeMaulInsane,
    ]
    minigame_maps_nolimit = [
        Maps.HelmBarrelLankyMaze,
        Maps.StashSnatchEasy,
        Maps.StashSnatchNormal,
        Maps.StashSnatchHard,
        Maps.StashSnatchInsane,
    ]
    minigame_maps_beavers = [
        Maps.BeaverBotherEasy,
        Maps.BeaverBotherNormal,
        Maps.BeaverBotherHard,
    ]
    minigame_maps_total = minigame_maps_easy.copy()
    minigame_maps_total.extend(minigame_maps_beatable)
    minigame_maps_total.extend(minigame_maps_nolimit)
    minigame_maps_total.extend(minigame_maps_beavers)
    enemy_classes = {
        "ground_simple": [
            Enemies.BeaverBlue,
            Enemies.KlaptrapGreen,
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
            Enemies.KlaptrapPurple,
            Enemies.KlaptrapRed,
            Enemies.Guard,
        ],
        "water": [
            Enemies.Shuri,
            Enemies.Gimpfish,
            Enemies.Pufftup,
        ],
    }
    crown_enemies_library = {}
    crown_enemies = []
    for enemy in EnemyMetaData:
        if EnemyMetaData[enemy].crown_enabled is True:
            crown_enemies.append(enemy)
    if spoiler.settings.enemy_rando or spoiler.settings.kasplat_rando or spoiler.settings.crown_enemy_rando != "off":  # TODO: Add option for crown enemy rando
        boolean_damage_is_ohko = spoiler.settings.damage_amount == "ohko"
        crown_enemies_library = getBalancedCrownEnemyRando(spoiler.settings.crown_enemy_rando, boolean_damage_is_ohko)
        minigame_enemies_simple = []
        minigame_enemies_beatable = []
        minigame_enemies_nolimit = []
        minigame_enemies_beavers = []
        for enemy in EnemyMetaData:
            if EnemyMetaData[enemy].minigame_enabled:
                minigame_enemies_nolimit.append(enemy)
                if EnemyMetaData[enemy].beaver:
                    minigame_enemies_beavers.append(enemy)
                if EnemyMetaData[enemy].killable:
                    minigame_enemies_beatable.append(enemy)
                    if EnemyMetaData[enemy].simple:
                        minigame_enemies_simple.append(enemy)
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
            # Generate Enemy Swaps lists
            enemy_swaps = {}
            for enemy_class in enemy_classes:
                arr = []
                for x in range(spawner_count):
                    arr.append(random.choice(enemy_classes[enemy_class]))
                enemy_swaps[enemy_class] = arr
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
            if spoiler.settings.kasplat_rando and not spoiler.settings.kasplat_location_rando:
                # Shuffle within vanilla locations
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
                                if cont_map_id != Maps.ForestSpider or EnemyMetaData[new_enemy_id].aggro != 4:  # Prevent enemies being stuck in the ceiling
                                    if new_enemy_id != Enemies.Book or cont_map_id not in (Maps.CavesDonkeyCabin, Maps.JapesLankyCave, Maps.AngryAztecLobby):
                                        if new_enemy_id != Enemies.Kosha or cont_map_id != Maps.CavesDiddyLowerCabin:
                                            if new_enemy_id != Enemies.Guard or cont_map_id not in (Maps.CavesDiddyLowerCabin, Maps.CavesTinyIgloo, Maps.CavesTinyCabin):
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
                                                    if spoiler.settings.enemy_speed_rando:
                                                        min_speed = EnemyMetaData[new_enemy_id].min_speed
                                                        max_speed = EnemyMetaData[new_enemy_id].max_speed
                                                        if min_speed > 0 and max_speed > 0:
                                                            ROM().seek(cont_map_spawner_address + spawner["offset"] + 0xD)
                                                            agg_speed = random.randint(min_speed, max_speed)
                                                            ROM().writeMultipleBytes(agg_speed, 1)
                                                            ROM().seek(cont_map_spawner_address + spawner["offset"] + 0xC)
                                                            ROM().writeMultipleBytes(random.randint(min_speed, agg_speed), 1)
            if spoiler.settings.enemy_rando and cont_map_id in minigame_maps_total:
                tied_enemy_list = []
                if cont_map_id in minigame_maps_easy:
                    tied_enemy_list = minigame_enemies_simple.copy()
                elif cont_map_id in minigame_maps_beatable:
                    tied_enemy_list = minigame_enemies_beatable.copy()
                elif cont_map_id in minigame_maps_nolimit:
                    tied_enemy_list = minigame_enemies_nolimit.copy()
                elif cont_map_id in minigame_maps_beavers:
                    tied_enemy_list = minigame_enemies_beavers.copy()
                for spawner in vanilla_spawners:
                    if spawner["enemy_id"] in tied_enemy_list:
                        new_enemy_id = random.choice(tied_enemy_list)
                        # Balance beaver bother so it's a 3:1 ratio of blue to gold beavers
                        if cont_map_id in minigame_maps_beavers:
                            comp_id = random.choice(tied_enemy_list)
                            if new_enemy_id != Enemies.BeaverGold or comp_id != Enemies.BeaverGold:
                                new_enemy_id = Enemies.BeaverBlue
                        ROM().seek(cont_map_spawner_address + spawner["offset"])
                        ROM().writeMultipleBytes(new_enemy_id, 1)
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
                            if spoiler.settings.enemy_speed_rando and cont_map_id not in minigame_maps_beavers:
                                min_speed = EnemyMetaData[new_enemy_id].min_speed
                                max_speed = EnemyMetaData[new_enemy_id].max_speed
                                if min_speed > 0 and max_speed > 0:
                                    ROM().seek(cont_map_spawner_address + spawner["offset"] + 0xD)
                                    agg_speed = random.randint(min_speed, max_speed)
                                    ROM().writeMultipleBytes(agg_speed, 1)
                                    ROM().seek(cont_map_spawner_address + spawner["offset"] + 0xC)
                                    ROM().writeMultipleBytes(random.randint(min_speed, agg_speed), 1)
                            if new_enemy_id == Enemies.BeaverGold and cont_map_id in minigame_maps_beavers:
                                for speed_offset in [0xC, 0xD]:
                                    ROM().seek(cont_map_spawner_address + spawner["offset"] + speed_offset)
                                    default_speed = int.from_bytes(ROM().readBytes(1), "big")
                                    new_speed = int(default_speed * 1.1)
                                    if new_speed > 255:
                                        new_speed = 255
                                    ROM().seek(cont_map_spawner_address + spawner["offset"] + speed_offset)
                                    ROM().writeMultipleBytes(new_speed, 1)
            if spoiler.settings.crown_enemy_rando != "off" and cont_map_id in crown_maps:
                # Determine Crown Timer
                low_limit = 5
                if spoiler.settings.crown_enemy_rando == "easy":
                    low_limit = 5
                elif spoiler.settings.crown_enemy_rando == "medium":
                    low_limit = 15
                elif spoiler.settings.crown_enemy_rando == "hard":
                    low_limit = 30
                crown_timer = random.randint(low_limit, 60)
                # Place Enemies
                for spawner in vanilla_spawners:
                    if spawner["enemy_id"] in crown_enemies:
                        new_enemy_id = crown_enemies_library[cont_map_id].pop()
                        ROM().seek(cont_map_spawner_address + spawner["offset"])
                        ROM().writeMultipleBytes(new_enemy_id, 1)
                        if new_enemy_id in EnemyMetaData.keys():
                            ROM().seek(cont_map_spawner_address + spawner["offset"] + 0x10)
                            ROM().writeMultipleBytes(EnemyMetaData[new_enemy_id].aggro, 1)
                            if new_enemy_id == Enemies.RoboKremling:
                                ROM().seek(cont_map_spawner_address + spawner["offset"] + 0xB)
                                ROM().writeMultipleBytes(0xC8, 1)
                            if EnemyMetaData[new_enemy_id].air:
                                ROM().seek(cont_map_spawner_address + spawner["offset"] + 0x6)
                                ROM().writeMultipleBytes(300, 2)
                            if new_enemy_id == Enemies.GetOut:
                                ROM().seek(cont_map_spawner_address + spawner["offset"] + 0xA)
                                get_out_timer = 0
                                if crown_timer > 20:
                                    damage_mult = 1
                                    damage_amts = {
                                        "double": 2,
                                        "quad": 4,
                                        "ohko": 12,
                                    }
                                    if spoiler.settings.damage_amount in damage_amts:
                                        damage_mult = damage_amts[spoiler.settings.damage_amount]
                                    get_out_timer = random.randint(int(crown_timer / (12 / damage_mult)) + 1, crown_timer - 1)
                                ROM().writeMultipleBytes(get_out_timer, 1)
                            ROM().seek(cont_map_spawner_address + spawner["offset"] + 0xF)
                            default_scale = int.from_bytes(ROM().readBytes(1), "big")
                            if EnemyMetaData[new_enemy_id].size_cap > 0:
                                if default_scale > EnemyMetaData[new_enemy_id].size_cap:
                                    ROM().seek(cont_map_spawner_address + spawner["offset"] + 0xF)
                                    ROM().writeMultipleBytes(EnemyMetaData[new_enemy_id].size_cap, 1)
                            if spoiler.settings.enemy_speed_rando:
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
                        ROM().writeMultipleBytes(crown_timer, 1)  # Determine Crown length. DK64 caps at 255 seconds
