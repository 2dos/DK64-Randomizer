"""Apply Boss Locations."""
import random

import js
from randomizer.Enums.EnemySubtypes import EnemySubtype
from randomizer.Enums.Settings import CrownEnemyRando, DamageAmount
from randomizer.Lists.EnemyTypes import Enemies, EnemyMetaData
from randomizer.Lists.MapsAndExits import Maps
from randomizer.Patching.Patcher import ROM, LocalROM


class PkmnSnapEnemy:
    """Class which determines if an enemy is available for the pkmn snap goal."""

    def __init__(self, enemy):
        """Initialize with given parameters."""
        self.enemy = enemy
        if enemy in (Enemies.KasplatDK, Enemies.KasplatDiddy, Enemies.KasplatLanky, Enemies.KasplatTiny, Enemies.KasplatChunky, Enemies.Book, Enemies.EvilTomato):
            # Always spawned, not in pool
            self.spawned = True
        else:
            self.spawned = False
        self.default = self.spawned

    def addEnemy(self):
        """Add enemy as spawned."""
        self.spawned = True

    def reset(self):
        """Reset enemy to default state."""
        self.spawned = self.default


class Spawner:
    """Class which stores information pertaining to a spawner."""

    def __init__(self, enemy_id: int, offset: int, index: int):
        """Initialize with given parameters."""
        self.enemy_id = enemy_id
        self.offset = offset
        self.index = index


pkmn_snap_enemies = [
    PkmnSnapEnemy(Enemies.Kaboom),
    PkmnSnapEnemy(Enemies.BeaverBlue),
    PkmnSnapEnemy(Enemies.Book),
    PkmnSnapEnemy(Enemies.Klobber),
    PkmnSnapEnemy(Enemies.ZingerCharger),
    PkmnSnapEnemy(Enemies.Klump),
    PkmnSnapEnemy(Enemies.KlaptrapGreen),
    PkmnSnapEnemy(Enemies.ZingerLime),
    PkmnSnapEnemy(Enemies.KlaptrapPurple),
    PkmnSnapEnemy(Enemies.KlaptrapRed),
    PkmnSnapEnemy(Enemies.BeaverGold),
    PkmnSnapEnemy(Enemies.MushroomMan),
    PkmnSnapEnemy(Enemies.Ruler),
    PkmnSnapEnemy(Enemies.RoboKremling),
    PkmnSnapEnemy(Enemies.Kremling),
    PkmnSnapEnemy(Enemies.KasplatDK),
    PkmnSnapEnemy(Enemies.KasplatDiddy),
    PkmnSnapEnemy(Enemies.KasplatLanky),
    PkmnSnapEnemy(Enemies.KasplatTiny),
    PkmnSnapEnemy(Enemies.KasplatChunky),
    PkmnSnapEnemy(Enemies.Guard),
    PkmnSnapEnemy(Enemies.ZingerRobo),
    PkmnSnapEnemy(Enemies.Krossbones),
    PkmnSnapEnemy(Enemies.Shuri),
    PkmnSnapEnemy(Enemies.Gimpfish),
    PkmnSnapEnemy(Enemies.MrDice0),
    PkmnSnapEnemy(Enemies.SirDomino),
    PkmnSnapEnemy(Enemies.MrDice1),
    PkmnSnapEnemy(Enemies.FireballGlasses),
    PkmnSnapEnemy(Enemies.SpiderSmall),
    PkmnSnapEnemy(Enemies.Bat),
    PkmnSnapEnemy(Enemies.EvilTomato),
    PkmnSnapEnemy(Enemies.Ghost),
    PkmnSnapEnemy(Enemies.Pufftup),
    PkmnSnapEnemy(Enemies.Kosha),
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
crown_maps = [Maps.JapesCrown, Maps.AztecCrown, Maps.FactoryCrown, Maps.GalleonCrown, Maps.ForestCrown, Maps.CavesCrown, Maps.CastleCrown, Maps.HelmCrown, Maps.SnidesCrown, Maps.LobbyCrown]
minigame_maps_easy = [
    Maps.BusyBarrelBarrageEasy,
    Maps.BusyBarrelBarrageHard,
    Maps.BusyBarrelBarrageNormal,
    # Maps.HelmBarrelDiddyKremling, # Only kremlings activate the switch
    Maps.HelmBarrelChunkyHidden,
    Maps.HelmBarrelChunkyShooting,
]
minigame_maps_beatable = [Maps.MadMazeMaulEasy, Maps.MadMazeMaulNormal, Maps.MadMazeMaulHard, Maps.MadMazeMaulInsane]
minigame_maps_nolimit = [Maps.HelmBarrelLankyMaze, Maps.StashSnatchEasy, Maps.StashSnatchNormal, Maps.StashSnatchHard, Maps.StashSnatchInsane]
minigame_maps_beavers = [Maps.BeaverBotherEasy, Maps.BeaverBotherNormal, Maps.BeaverBotherHard]
minigame_maps_total = minigame_maps_easy.copy()
minigame_maps_total.extend(minigame_maps_beatable)
minigame_maps_total.extend(minigame_maps_nolimit)
minigame_maps_total.extend(minigame_maps_beavers)
bbbarrage_maps = (Maps.BusyBarrelBarrageEasy, Maps.BusyBarrelBarrageNormal, Maps.BusyBarrelBarrageHard)
banned_speed_maps = list(bbbarrage_maps).copy() + minigame_maps_beavers.copy()
replacement_priority = {
    EnemySubtype.GroundSimple: [EnemySubtype.GroundBeefy, EnemySubtype.Water, EnemySubtype.Air],
    EnemySubtype.GroundBeefy: [EnemySubtype.GroundSimple, EnemySubtype.Water, EnemySubtype.Air],
    EnemySubtype.Water: [EnemySubtype.Air, EnemySubtype.GroundSimple, EnemySubtype.GroundBeefy],
    EnemySubtype.Air: [EnemySubtype.GroundSimple, EnemySubtype.GroundBeefy, EnemySubtype.Water],
}
banned_enemy_maps = {
    Enemies.Book: [Maps.CavesDonkeyCabin, Maps.JapesLankyCave, Maps.AngryAztecLobby],
    Enemies.Kosha: [Maps.CavesDiddyLowerCabin, Maps.CavesTinyCabin],
    Enemies.Guard: [Maps.CavesDiddyLowerCabin, Maps.CavesTinyIgloo, Maps.CavesTinyCabin],
}


def isBanned(new_enemy_id: Enemies, cont_map_id: Maps, spawner: Spawner, no_ground_simple_selected: bool) -> bool:
    """Define if enemy is banned in current circumstances."""
    if new_enemy_id in banned_enemy_maps:
        if cont_map_id in banned_enemy_maps[new_enemy_id]:
            return True
    if no_ground_simple_selected:
        if cont_map_id == Maps.AztecTinyTemple and spawner.index in list(range(20, 24)):
            return True
        if cont_map_id == Maps.CastleBallroom and spawner.index <= 5:
            return True
        if cont_map_id == Maps.CastleLibrary and spawner.index <= 4:
            return True
    if cont_map_id == Maps.ForestSpider and EnemyMetaData[new_enemy_id].aggro == 4:
        return True
    if cont_map_id == Maps.ForestGiantMushroom and spawner.index in (3, 4):
        return True
    if new_enemy_id == Enemies.Guard and cont_map_id == Maps.FranticFactory:
        if spawner.index in (59, 62, 63, 73, 87, 88):  # Various enemies that are in tight hallways that are difficult to navigate around
            return True
    gun_enemy_gauntlets = (
        Maps.ForestMillAttic,
        Maps.CavesDonkeyCabin,
        Maps.JapesLankyCave,
        Maps.CastleShed,
    )
    enemies_cant_kill_gun = (
        Enemies.Klump,
        Enemies.RoboKremling,
        Enemies.Kosha,
        Enemies.Klobber,
        Enemies.Kaboom,
        Enemies.KlaptrapPurple,
        Enemies.Guard,
    )
    if (cont_map_id in gun_enemy_gauntlets or (cont_map_id == Maps.AztecTinyTemple and spawner.index < 17)) and new_enemy_id in enemies_cant_kill_gun:
        return True
    return False


def resetPkmnSnap():
    """Reset Pokemon Snap Listing."""
    for enemy in pkmn_snap_enemies:
        enemy.reset()


def setPkmnSnapEnemy(focused_enemy):
    """Set enemy to being spawned."""
    for enemy in pkmn_snap_enemies:
        if enemy.enemy == focused_enemy:
            enemy.addEnemy()


def getBalancedCrownEnemyRando(spoiler, crown_setting, damage_ohko_setting):
    """Get array of weighted enemies."""
    # this library will contain a list for every enemy it needs to generate
    enemy_swaps_library = {}

    if crown_setting != CrownEnemyRando.off:
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

        # Determine whether any crown-enabled enemies have been selected
        crown_enemy_found = False
        for enemy in EnemyMetaData:
            if enemy in spoiler.settings.enemies_selected and EnemyMetaData[enemy].crown_enabled is True and enemy is not Enemies.GetOut:
                crown_enemy_found = True
                break
        # Determine whether only GetOut is the only selected enemy that can appear in crown battles
        # If True, guarantees that there is 1 GetOut in every crown battle
        oops_all_get_out = False
        if crown_enemy_found is False and Enemies.GetOut in spoiler.settings.enemies_selected and damage_ohko_setting is False:
            oops_all_get_out = True
        # fill in the lists with the possibilities that belong in them.
        for enemy in EnemyMetaData:
            if EnemyMetaData[enemy].crown_enabled and enemy is not Enemies.GetOut:
                if enemy in spoiler.settings.enemies_selected or crown_enemy_found is False:
                    every_enemy.append(enemy)
                    if EnemyMetaData[enemy].disruptive <= 1:
                        disruptive_max_1.append(enemy)
                    if EnemyMetaData[enemy].kasplat is True:
                        disruptive_at_most_kasplat.append(enemy)
                    elif EnemyMetaData[enemy].disruptive == 0:
                        disruptive_at_most_kasplat.append(enemy)
                        disruptive_0.append(enemy)
        # Make sure every list is populated, even if too few crown-enabled enemies have been selected
        # This breaks the crown balancing, but what the player wants, the player gets
        if len(disruptive_max_1) == 0:
            disruptive_max_1.extend(every_enemy.copy())
            for enemy in EnemyMetaData:
                if EnemyMetaData[enemy].disruptive > 1:
                    EnemyMetaData[enemy].disruptive = 1
        if len(disruptive_at_most_kasplat) == 0:
            disruptive_at_most_kasplat.extend(disruptive_max_1.copy())
        if len(disruptive_0) == 0:
            disruptive_0.extend(disruptive_at_most_kasplat)
            for enemy in EnemyMetaData:
                if EnemyMetaData[enemy].disruptive > 0:
                    EnemyMetaData[enemy].disruptive = 0
        # the legacy_hard_mode list is trickier to fill, but here goes:
        bias = 2
        for enemy in EnemyMetaData.keys():
            if EnemyMetaData[enemy].crown_enabled:
                if enemy in spoiler.settings.enemies_selected or crown_enemy_found is False:
                    base_weight = EnemyMetaData[enemy].crown_weight
                    weight_diff = abs(base_weight - bias)
                    new_weight = abs(10 - weight_diff)
                    if enemy == Enemies.GetOut:
                        new_weight = 1
                    if damage_ohko_setting is False or enemy is not Enemies.GetOut:
                        for count in range(new_weight):
                            legacy_hard_mode.append(enemy)
        # picking enemies to put in the crown battles
        if crown_setting == CrownEnemyRando.easy:
            for map_id in enemy_swaps_library:
                enemy_swaps_library[map_id].append(random.choice(disruptive_max_1))
                if oops_all_get_out is True:
                    enemy_swaps_library[map_id].append(Enemies.GetOut)
                else:
                    enemy_swaps_library[map_id].append(random.choice(disruptive_0))
                enemy_swaps_library[map_id].append(random.choice(disruptive_0))
                if map_id == Maps.GalleonCrown or map_id == Maps.LobbyCrown or map_id == Maps.HelmCrown:
                    enemy_swaps_library[map_id].append(random.choice(disruptive_0))
        elif crown_setting == CrownEnemyRando.medium:
            new_enemy = 0
            for map_id in enemy_swaps_library:
                count_disruptive = 0
                count_kasplats = 0
                number_of_enemies = 3
                if map_id == Maps.GalleonCrown or map_id == Maps.LobbyCrown or map_id == Maps.HelmCrown:
                    number_of_enemies = 4
                for count in range(number_of_enemies):
                    if count == 0 and oops_all_get_out is True:
                        new_enemy = Enemies.GetOut
                    elif count_disruptive == 0:
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
                    if count_kasplats > 3 or (count_kasplats > 2 and count_disruptive > 1) or (count_kasplats == 2 and count_disruptive == 2):
                        print("This is a mistake in the crown enemy algorithm. Report this to the devs.")
                        new_enemy = Enemies.BeaverGold
                    # We picked a new enemy, let's update our information and add it to the list
                    if EnemyMetaData[new_enemy].kasplat is True:
                        count_kasplats = count_kasplats + 1
                    count_disruptive = EnemyMetaData[new_enemy].disruptive + count_disruptive
                    enemy_swaps_library[map_id].append(new_enemy)
        elif crown_setting == CrownEnemyRando.hard:
            for map_id in enemy_swaps_library:
                number_of_enemies = 3
                if map_id == Maps.GalleonCrown or map_id == Maps.LobbyCrown or map_id == Maps.HelmCrown:
                    number_of_enemies = 4
                get_out_spawned_this_hard_map = False
                for count in range(number_of_enemies):
                    if count == 0 and oops_all_get_out is True:
                        enemy_to_place = Enemies.GetOut
                        get_out_spawned_this_hard_map = True
                    elif get_out_spawned_this_hard_map:
                        enemy_to_place = random.choice([possible_enemy for possible_enemy in legacy_hard_mode if possible_enemy != Enemies.GetOut])
                    else:
                        enemy_to_place = random.choice(legacy_hard_mode)
                        if enemy_to_place == Enemies.GetOut:
                            get_out_spawned_this_hard_map = True
                    enemy_swaps_library[map_id].append(enemy_to_place)
        # one last shuffle, to make sure any enemy can spawn in any spot
        for map_id in enemy_swaps_library:
            if len(enemy_swaps_library[map_id]) > 0:
                random.shuffle(enemy_swaps_library[map_id])
    return enemy_swaps_library


def writeEnemy(spoiler, cont_map_spawner_address: int, new_enemy_id: int, spawner: Spawner, cont_map_id: Maps, crown_timer: int = 0):
    """Write enemy to ROM."""
    LocalROM().seek(cont_map_spawner_address + spawner.offset)
    LocalROM().writeMultipleBytes(new_enemy_id, 1)
    # Enemy fixes
    if new_enemy_id in EnemyMetaData.keys():
        LocalROM().seek(cont_map_spawner_address + spawner.offset + 0x10)
        LocalROM().writeMultipleBytes(EnemyMetaData[new_enemy_id].aggro, 1)
        if new_enemy_id == Enemies.RoboKremling:
            LocalROM().seek(cont_map_spawner_address + spawner.offset + 0xB)
            LocalROM().writeMultipleBytes(0xC8, 1)
        elif new_enemy_id == Enemies.SpiderSmall:
            LocalROM().seek(cont_map_spawner_address + spawner.offset + 0x1)
            LocalROM().writeMultipleBytes(0, 1)
            LocalROM().seek(cont_map_spawner_address + spawner.offset + 0xB)
            LocalROM().writeMultipleBytes(0, 1)
            # Spawning fixes
            # Prevent respawn anim if that's how they initially appear
            LocalROM().seek(cont_map_spawner_address + spawner.offset + 0x12)
            init_respawn_state = int.from_bytes(LocalROM().readBytes(1), "big")
            if init_respawn_state == 3:
                LocalROM().seek(cont_map_spawner_address + spawner.offset + 0x12)
                LocalROM().writeMultipleBytes(0, 1)
            # Prevent them respawning
            LocalROM().seek(cont_map_spawner_address + spawner.offset + 0x14)
            LocalROM().writeMultipleBytes(0, 1)

        if (cont_map_id in crown_maps or cont_map_id in minigame_maps_total) and EnemyMetaData[new_enemy_id].air:
            height = 300
            if cont_map_id in crown_maps:
                height = int(random.uniform(250, 300))
            LocalROM().seek(cont_map_spawner_address + spawner.offset + 0x6)
            LocalROM().writeMultipleBytes(height, 2)
        if cont_map_id in crown_maps and new_enemy_id == Enemies.GetOut:
            LocalROM().seek(cont_map_spawner_address + spawner.offset + 0xA)
            get_out_timer = 20
            if crown_timer > 20:
                damage_mult = 1
                damage_amts = {DamageAmount.double: 2, DamageAmount.quad: 4, DamageAmount.ohko: 12}
                if spoiler.settings.damage_amount in damage_amts:
                    damage_mult = damage_amts[spoiler.settings.damage_amount]
                get_out_timer = random.randint(int(crown_timer / (12 / damage_mult)) + 1, crown_timer - 1)
            if get_out_timer == 0:
                get_out_timer = 1
            LocalROM().writeMultipleBytes(get_out_timer, 1)
            LocalROM().writeMultipleBytes(get_out_timer, 1)
        # Scale Adjustment
        LocalROM().seek(cont_map_spawner_address + spawner.offset + 0xF)
        default_scale = int.from_bytes(LocalROM().readBytes(1), "big")
        if EnemyMetaData[new_enemy_id].size_cap > 0:
            if default_scale > EnemyMetaData[new_enemy_id].size_cap:
                LocalROM().seek(cont_map_spawner_address + spawner.offset + 0xF)
                LocalROM().writeMultipleBytes(EnemyMetaData[new_enemy_id].size_cap, 1)
        LocalROM().seek(cont_map_spawner_address + spawner.offset + 0xF)
        pre_size = int.from_bytes(LocalROM().readBytes(1), "big")
        if pre_size < EnemyMetaData[new_enemy_id].bbbarrage_min_scale and cont_map_id in bbbarrage_maps:
            LocalROM().seek(cont_map_spawner_address + spawner.offset + 0xF)
            LocalROM().writeMultipleBytes(EnemyMetaData[new_enemy_id].bbbarrage_min_scale, 1)
        # Speed Adjustment
        if spoiler.settings.enemy_speed_rando:
            if cont_map_id not in banned_speed_maps:
                min_speed = EnemyMetaData[new_enemy_id].min_speed
                max_speed = EnemyMetaData[new_enemy_id].max_speed
                if min_speed > 0 and max_speed > 0:
                    LocalROM().seek(cont_map_spawner_address + spawner.offset + 0xD)
                    agg_speed = random.randint(min_speed, max_speed)
                    LocalROM().writeMultipleBytes(agg_speed, 1)
                    LocalROM().seek(cont_map_spawner_address + spawner.offset + 0xC)
                    LocalROM().writeMultipleBytes(random.randint(min_speed, agg_speed), 1)
        if cont_map_id in bbbarrage_maps:
            # Reduce Speeds
            LocalROM().seek(cont_map_spawner_address + spawner.offset + 0xC)
            speeds = []
            for x in range(2):
                speeds.append(int.from_bytes(LocalROM().readBytes(1), "big"))
            LocalROM().seek(cont_map_spawner_address + spawner.offset + 0xC)
            for x in speeds:
                LocalROM().writeMultipleBytes(int(x * 0.75), 1)
        elif cont_map_id in minigame_maps_beavers and new_enemy_id == Enemies.BeaverGold:
            for speed_offset in [0xC, 0xD]:
                LocalROM().seek(cont_map_spawner_address + spawner.offset + speed_offset)
                default_speed = int.from_bytes(LocalROM().readBytes(1), "big")
                new_speed = int(default_speed * 1.1)
                if new_speed > 255:
                    new_speed = 255
                LocalROM().seek(cont_map_spawner_address + spawner.offset + speed_offset)
                LocalROM().writeMultipleBytes(new_speed, 1)


def randomize_enemies(spoiler):
    """Write replaced enemies to ROM."""
    # Define Enemy Classes, Used for detection of if an enemy will be replaced
    enemy_classes = {
        EnemySubtype.GroundSimple: [
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
        EnemySubtype.Air: [
            Enemies.ZingerCharger,
            Enemies.ZingerLime,
            Enemies.ZingerRobo,
            Enemies.Bat,
            # Enemies.Bug, # Crashes on N64
            # Enemies.Book, # Causes way too many problems
        ],
        EnemySubtype.GroundBeefy: [
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
        EnemySubtype.Water: [Enemies.Shuri, Enemies.Gimpfish, Enemies.Pufftup],
    }
    resetPkmnSnap()

    # Define Enemies that can be placed in those classes
    enemy_placement_classes = {}
    banned_classes = []
    no_ground_simple_selected = False
    for enemy_class in enemy_classes:
        class_list = []
        for enemy in enemy_classes[enemy_class]:
            if enemy in spoiler.settings.enemies_selected:
                class_list.append(enemy)
        if enemy_class == EnemySubtype.GroundSimple and len(class_list) == 0:
            no_ground_simple_selected = True
        if len(class_list) == 0:
            # Nothing present, use backup
            for repl_type in replacement_priority[enemy_class]:
                if len(class_list) == 0:
                    for enemy in enemy_classes[repl_type]:
                        if enemy in spoiler.settings.enemies_selected:
                            class_list.append(enemy)
        if len(class_list) > 0:
            enemy_placement_classes[enemy_class] = class_list.copy()
        else:
            # Replace Nothing
            banned_classes.append(enemy_class)
    for enemy_class in banned_classes:
        del enemy_classes[enemy_class]
    # Crown Enemy Stuff
    crown_enemies_library = {}
    crown_enemies = []
    for enemy in EnemyMetaData:
        if EnemyMetaData[enemy].crown_enabled is True:
            crown_enemies.append(enemy)
    if spoiler.settings.enemy_rando or spoiler.settings.crown_enemy_rando != CrownEnemyRando.off:
        boolean_damage_is_ohko = spoiler.settings.damage_amount == DamageAmount.ohko
        crown_enemies_library = getBalancedCrownEnemyRando(spoiler, spoiler.settings.crown_enemy_rando, boolean_damage_is_ohko)
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
            LocalROM().seek(cont_map_spawner_address)
            fence_count = int.from_bytes(LocalROM().readBytes(2), "big")
            offset = 2
            if fence_count > 0:
                for x in range(fence_count):
                    LocalROM().seek(cont_map_spawner_address + offset)
                    point_count = int.from_bytes(LocalROM().readBytes(2), "big")
                    offset += (point_count * 6) + 2
                    LocalROM().seek(cont_map_spawner_address + offset)
                    point0_count = int.from_bytes(LocalROM().readBytes(2), "big")
                    offset += (point0_count * 10) + 6
            LocalROM().seek(cont_map_spawner_address + offset)
            spawner_count = int.from_bytes(LocalROM().readBytes(2), "big")
            # Generate Enemy Swaps lists
            enemy_swaps = {}
            for enemy_class in enemy_classes:
                arr = []
                for x in range(spawner_count):
                    arr.append(random.choice(enemy_placement_classes[enemy_class]))
                enemy_swaps[enemy_class] = arr
            offset += 2
            for _ in range(spawner_count):
                LocalROM().seek(cont_map_spawner_address + offset)
                enemy_id = int.from_bytes(LocalROM().readBytes(1), "big")
                LocalROM().seek(cont_map_spawner_address + offset + 0x13)
                enemy_index = int.from_bytes(LocalROM().readBytes(1), "big")
                init_offset = offset
                LocalROM().seek(cont_map_spawner_address + offset + 0x11)
                extra_count = int.from_bytes(LocalROM().readBytes(1), "big")
                offset += 0x16 + (extra_count * 2)
                vanilla_spawners.append(Spawner(enemy_id, init_offset, enemy_index))
            if spoiler.settings.enemy_rando and cont_map_id in valid_maps:
                for enemy_class in enemy_swaps:
                    arr = enemy_swaps[enemy_class]
                    class_types = enemy_classes[enemy_class]
                    sub_index = 0
                    for spawner in vanilla_spawners:
                        if spawner.enemy_id in class_types:
                            if cont_map_id != Maps.FranticFactory or spawner.index < 35 or spawner.index > 44:
                                new_enemy_id = arr[sub_index]
                                sub_index += 1
                                if not isBanned(new_enemy_id, cont_map_id, spawner, no_ground_simple_selected):
                                    writeEnemy(spoiler, cont_map_spawner_address, new_enemy_id, spawner, cont_map_id, 0)
            if spoiler.settings.enemy_rando and cont_map_id in minigame_maps_total:
                tied_enemy_list = []
                if cont_map_id in minigame_maps_easy:
                    tied_enemy_list = minigame_enemies_simple.copy()
                    if cont_map_id in bbbarrage_maps:
                        if Enemies.KlaptrapGreen in tied_enemy_list:
                            tied_enemy_list.remove(Enemies.KlaptrapGreen)  # Remove Green Klaptrap out of BBBarrage pool
                elif cont_map_id in minigame_maps_beatable:
                    tied_enemy_list = minigame_enemies_beatable.copy()
                elif cont_map_id in minigame_maps_nolimit:
                    tied_enemy_list = minigame_enemies_nolimit.copy()
                elif cont_map_id in minigame_maps_beavers:
                    tied_enemy_list = minigame_enemies_beavers.copy()
                for spawner in vanilla_spawners:
                    if spawner.enemy_id in tied_enemy_list:
                        new_enemy_id = random.choice(tied_enemy_list)
                        # Balance beaver bother so it's a 4:1 ratio of blue to gold beavers, guarantee 1 gold
                        if cont_map_id in minigame_maps_beavers:
                            if spawner.index == 1:
                                new_enemy_id = Enemies.BeaverGold
                            else:
                                selection = random.uniform(0, 1)
                                new_enemy_id = Enemies.BeaverBlue
                                if selection < 0.2:
                                    new_enemy_id = Enemies.BeaverGold
                        writeEnemy(spoiler, cont_map_spawner_address, new_enemy_id, spawner, cont_map_id, 0)
            if spoiler.settings.crown_enemy_rando != CrownEnemyRando.off and cont_map_id in crown_maps:
                # Determine Crown Timer
                limits = {
                    CrownEnemyRando.easy: 5,
                    CrownEnemyRando.medium: 15,
                    CrownEnemyRando.hard: 30,
                }
                low_limit = limits.get(spoiler.settings.crown_enemy_rando, 5)
                crown_timer = random.randint(low_limit, 60)
                # Place Enemies
                for spawner in vanilla_spawners:
                    if spawner.enemy_id in crown_enemies:
                        new_enemy_id = crown_enemies_library[cont_map_id].pop()
                        writeEnemy(spoiler, cont_map_spawner_address, new_enemy_id, spawner, cont_map_id, crown_timer)
                    elif spawner.enemy_id == Enemies.BattleCrownController:
                        LocalROM().seek(cont_map_spawner_address + spawner.offset + 0xB)
                        LocalROM().writeMultipleBytes(crown_timer, 1)  # Determine Crown length. DK64 caps at 255 seconds
            non_pkmn_snap_maps = [Maps.ForestSpider, Maps.CavesDiddyLowerCabin, Maps.CavesTinyCabin, Maps.CastleBoss]
            if cont_map_id in valid_maps and cont_map_id not in non_pkmn_snap_maps:
                # Check Pokemon Snap
                for spawner in vanilla_spawners:
                    if cont_map_id == Maps.AztecTinyTemple and spawner.index < 17:
                        # Prevent One-Time-Only Enemies in Tiny Temple from being required
                        continue
                    if cont_map_id == Maps.CastleBallroom and spawner.index < 6:
                        # Prevent One-Time-Only Enemies in Castle BallRoom from being required
                        continue
                    if cont_map_id == Maps.CastleLibrary and spawner.index < 5:
                        # Prevent One-Time-Only Enemies in Castle Library from being required
                        continue
                    if cont_map_id == Maps.AztecTinyTemple and spawner.index > 19 and spawner.index < 24:
                        # Prevent One-Time-Only Enemies in Tiny Temple from being required
                        continue
                    if cont_map_id == Maps.FranticFactory and spawner.index > 34 and spawner.index < 45:
                        # Prevent One-Time-Only Enemies in Toy Boss Fight from being required
                        continue
                    if cont_map_id == Maps.CrystalCaves and spawner.index < 10:
                        # Prevent Unused Enemies in Caves
                        continue
                    LocalROM().seek(cont_map_spawner_address + spawner.offset)
                    setPkmnSnapEnemy(int.from_bytes(LocalROM().readBytes(1), "big"))
            values = [0, 0, 0, 0, 0]
            for enemy_index, enemy in enumerate(pkmn_snap_enemies):
                if enemy.spawned:
                    offset = enemy_index >> 3
                    shift = enemy_index & 7
                    values[offset] |= 1 << shift
            LocalROM().seek(spoiler.settings.rom_data + 0x117)
            for value in values:
                LocalROM().writeMultipleBytes(value, 1)
