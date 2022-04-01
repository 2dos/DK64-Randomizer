"""Stores the requirements for each minigame."""

from randomizer.Enums.Locations import Locations
from randomizer.Enums.Minigames import Minigames
from randomizer.MapsAndExits import Maps


class Minigame:
    """Class which stores name and logic for a minigame."""

    def __init__(self, name, map_id, helm_enabled, can_repeat, difficulty_lvl, logic):
        """Initialize with given parameters."""
        self.name = name
        self.map = map_id
        self.helm_enabled = helm_enabled
        self.repeat = can_repeat
        self.difficulty = difficulty_lvl
        self.logic = logic

class MinigameLocationData:
    """Class which stores container map and barrel id for a minigame barrel"""

    def __init__(self, map_id, barrel_id):
        """Initialize with given parameters"""
        self.map = map_id
        self.barrel_id = barrel_id

MinigameRequirements = {
    Minigames.NoGame: Minigame("No Game", True, lambda l: True),
    # Batty Barrel Bandit
    Minigames.BattyBarrelBanditVEasy: Minigame("Batty Barrel Bandit (Slow)", Maps.BattyBarrelBanditVEasy, True, True, 0, lambda l: True),
    Minigames.BattyBarrelBanditEasy: Minigame("Batty Barrel Bandit (Progressive Speed)", Maps.BattyBarrelBanditEasy, True, True, 1, lambda l: True),
    Minigames.BattyBarrelBanditNormal: Minigame("Batty Barrel Bandit (Medium)", Maps.BattyBarrelBanditNormal, True, True, 2, lambda l: True),
    Minigames.BattyBarrelBanditHard: Minigame("Batty Barrel Bandit (Fast)", Maps.BattyBarrelBanditHard, True, True, 3, lambda l: True),
    # Big Bug Bash
    Minigames.BigBugBashVEasy: Minigame("Big Bug Bash (4 Bugs)", Maps.BigBugBashVEasy, True, True, 0, lambda l: True),
    Minigames.BigBugBashEasy: Minigame("Big Bug Bash (6 Bugs)", Maps.BigBugBashEasy, True, True, 1, lambda l: True),
    Minigames.BigBugBashNormal: Minigame("Big Bug Bash (8 Bugs)", Maps.BigBugBashNormal, True, True, 2, lambda l: True),
    Minigames.BigBugBashHard: Minigame("Big Bug Bash (10 Bugs)", Maps.BigBugBashHard, True, True, 3, lambda l: True),
    # Busy Barrel Barrage - Lanky excluded because gun is too long
    Minigames.BusyBarrelBarrageEasy: Minigame("Busy Barrel Barrage (45 seconds, Slow Respawn)", Maps.BusyBarrelBarrageEasy, True, True, 0, lambda l: (l.isdonkey and l.coconut) or (l.isdiddy and l.peanut) or (l.istiny and l.feather) or (l.ischunky and l.pineapple)),
    Minigames.BusyBarrelBarrageNormal: Minigame("Busy Barrel Barrage (45 seconds, Medium Respawn)", Maps.BusyBarrelBarrageNormal, True, True, 1, lambda l: (l.isdonkey and l.coconut) or (l.isdiddy and l.peanut) or (l.istiny and l.feather) or (l.ischunky and l.pineapple)),
    Minigames.BusyBarrelBarrageHard: Minigame("Busy Barrel Barrage (60 seconds, Random Spawns)", Maps.BusyBarrelBarrageHard, True, True, 2, lambda l: (l.isdonkey and l.coconut) or (l.isdiddy and l.peanut) or (l.istiny and l.feather) or (l.ischunky and l.pineapple)),
    # Mad Maze Maul - 120/11 requires shockwave to beat, as such, banned from Helm
    Minigames.MadMazeMaulEasy: Minigame("Mad Maze Maul (60 seconds, 5 enemies)", Maps.MadMazeMaulEasy, True, True, 0, lambda l: True),
    Minigames.MadMazeMaulNormal: Minigame("Mad Maze Maul (60 seconds, 7 enemies)", Maps.MadMazeMaulNormal, True, True, 1, lambda l: True),
    Minigames.MadMazeMaulHard: Minigame("Mad Maze Maul (120 seconds, 11 enemies)", Maps.MadMazeMaulHard, False, True, 2, lambda l: l.shockwave),
    Minigames.MadMazeMaulInsane: Minigame("Mad Maze Maul (125 seconds, 10 enemies)", Maps.MadMazeMaulInsane, True, True, 3, lambda l: True),
    # Minecart Mayhem - Higher two difficulties are too hard for those who don't have a guide to do in Helm
    Minigames.MinecartMayhemEasy: Minigame("Minecart Mayhem (30 seconds, 1 TNT)", Maps.MinecartMayhemEasy, True, True, 0, lambda l: True),
    Minigames.MinecartMayhemNormal: Minigame("Minecart Mayhem (45 seconds, 2 TNT)", Maps.MinecartMayhemNormal, False, True, 1, lambda l: True),
    Minigames.MinecartMayhemHard: Minigame("Minecart Mayhem (60 seconds, 2 TNT)", Maps.MinecartMayhemHard, False, True, 2, lambda l: True),
    # Beaver Bother - Banned from Helm due to widespread difficulty
    Minigames.BeaverBotherEasy: Minigame("Beaver Bother (12 Beavers)", Maps.BeaverBotherEasy, False, True, 0, lambda l: True),
    Minigames.BeaverBotherNormal: Minigame("Beaver Bother (15 Slow Beavers)", Maps.BeaverBotherNormal, False, True, 1, lambda l: True),
    Minigames.BeaverBotherHard: Minigame("Beaver Bother (15 Fast Beavers)", Maps.BeaverBotherHard, False, True, 2, lambda l: True),
    # Teetering Turtle Trouble
    Minigames.TeeteringTurtleTroubleVEasy: Minigame("Teetering Turtle Trouble (45 seconds, 2.5% help chance)", Maps.TeeteringTurtleTroubleVEasy, True, True, 0, lambda l: True),
    Minigames.TeeteringTurtleTroubleEasy: Minigame("Teetering Turtle Trouble (45 seconds, 4% help chance)", Maps.TeeteringTurtleTroubleEasy, True, True, 1, lambda l: True),
    Minigames.TeeteringTurtleTroubleNormal: Minigame("Teetering Turtle Trouble (60 seconds, 5% help chance)", Maps.TeeteringTurtleTroubleNormal, True, True, 2, lambda l: True),
    Minigames.TeeteringTurtleTroubleHard: Minigame("Teetering Turtle Trouble (60 seconds, 7.5% help chance)", Maps.TeeteringTurtleTroubleHard, True, True, 3, lambda l: True),
    # Stealthy Snoop
    Minigames.StealthySnoopVEasy: Minigame("Stealthy Snoop (50 seconds)", Maps.StealthySnoopVEasy, True, True, 0, lambda l: True),
    Minigames.StealthySnoopEasy: Minigame("Stealthy Snoop (60 seconds)", Maps.StealthySnoopEasy, True, True, 1, lambda l: True),
    Minigames.StealthySnoopNormal: Minigame("Stealthy Snoop (70 seconds)", Maps.StealthySnoopNormal, True, True, 2, lambda l: True),
    Minigames.StealthySnoopHard: Minigame("Stealthy Snoop (90 seconds)", Maps.StealthySnoopHard, True, True, 3, lambda l: True),
    # Stash Snatch - SSnatch Hybrid determined too difficulty for Helm
    Minigames.StashSnatchEasy: Minigame("Stash Snatch (60 seconds, 6 coins)", Maps.StashSnatchEasy, True, True, 0, lambda l: True),
    Minigames.StashSnatchNormal: Minigame("Stash Snatch (60 seconds, 16 coins)", Maps.StashSnatchNormal, True, True, 1, lambda l: True),
    Minigames.StashSnatchHard: Minigame("Stash Snatch (120 seconds, 4 coins, Stash Snatch Hybrid)", Maps.StashSnatchHard, False, True, 2, lambda l: True),
    Minigames.StashSnatchInsane: Minigame("Stash Snatch (120 seconds, 33 coins)", Maps.StashSnatchInsane, True, True, 3, lambda l: True),
    # Splish Splash Salvage
    Minigames.SplishSplashSalvageEasy: Minigame("Splish Splash Salvage (8 coins)", Maps.SplishSplashSalvageEasy, True, True, 0, lambda l: l.swim and l.vines),
    Minigames.SplishSplashSalvageNormal: Minigame("Splish Splash Salvage (10 coins)", Maps.SplishSplashSalvageNormal, True, True, 1, lambda l: l.swim),
    Minigames.SplishSplashSalvageHard: Minigame("Splish Splash Salvage (15 coins)", Maps.SplishSplashSalvageHard, True, True, 2, lambda l: l.swim),
    # Speedy Swing Sortie
    Minigames.SpeedySwingSortieEasy: Minigame("Speedy Swing Sortie (40 seconds, 9 coins)", Maps.SpeedySwingSortieEasy, True, True, 0, lambda l: l.vines),
    Minigames.SpeedySwingSortieNormal: Minigame("Speedy Swing Sortie (45 seconds, 14 coins)", Maps.SpeedySwingSortieNormal, True, True, 1, lambda l: l.vines and l.twirl and l.istiny),
    Minigames.SpeedySwingSortieHard: Minigame("Speedy Swing Sortie (60 seconds, 6 coins)", Maps.SpeedySwingSortieHard, True, True, 2, lambda l: l.vines),
    # Krazy Kong Klamour - Fast flicker games banned from Helm because Wii U semi-requires pause buffer to hit Bananas. Not expecting users to know this trick
    Minigames.KrazyKongKlamourEasy: Minigame("Krazy Kong Klamour (10 Bananas, Slow Flicker)", Maps.KrazyKongKlamourEasy, True, True, 0, lambda l: True),
    Minigames.KrazyKongKlamourNormal: Minigame("Krazy Kong Klamour (15 Bananas, Slow Flicker)", Maps.KrazyKongKlamourNormal, True, True, 1, lambda l: True),
    Minigames.KrazyKongKlamourHard: Minigame("Krazy Kong Klamour (5 Bananas, Fast Flicker)", Maps.KrazyKongKlamourHard, False, True, 2, lambda l: True),
    Minigames.KrazyKongKlamourInsane: Minigame("Krazy Kong Klamour (10 Bananas, Fast Flicker)", Maps.KrazyKongKlamourInsane, False, True, 3, lambda l: True),
    # Searchlight Seek
    Minigames.SearchlightSeekVEasy: Minigame("Searchlight Seek (4 Klaptraps)", Maps.SearchlightSeekVEasy, True, True, 0, lambda l: True),
    Minigames.SearchlightSeekEasy: Minigame("Searchlight Seek (6 Klaptraps)", Maps.SearchlightSeekEasy, True, True, 1, lambda l: True),
    Minigames.SearchlightSeekNormal: Minigame("Searchlight Seek (8 Klaptraps)", Maps.SearchlightSeekNormal, True, True, 2, lambda l: True),
    Minigames.SearchlightSeekHard: Minigame("Searchlight Seek (10 Klaptraps)", Maps.SearchlightSeekHard, True, True, 3, lambda l: True),
    # Kremling Kosh
    Minigames.KremlingKoshVEasy: Minigame("Kremling Kosh (18 points)", Maps.KremlingKoshVEasy, True, True, 0, lambda l: True),
    Minigames.KremlingKoshEasy: Minigame("Kremling Kosh (22 points)", Maps.KremlingKoshEasy, True, True, 1, lambda l: True),
    Minigames.KremlingKoshNormal: Minigame("Kremling Kosh (25 points)", Maps.KremlingKoshNormal, True, True, 2, lambda l: True),
    Minigames.KremlingKoshHard: Minigame("Kremling Kosh (28 points)", Maps.KremlingKoshHard, True, True, 3, lambda l: True),
    # Peril Path Panic
    Minigames.PerilPathPanicVEasy: Minigame("Peril Path Panic (6 points)", Maps.PerilPathPanicVEasy, True, True, 0, lambda l: True),
    Minigames.PerilPathPanicEasy: Minigame("Peril Path Panic (8 points)", Maps.PerilPathPanicEasy, True, True, 1, lambda l: True),
    Minigames.PerilPathPanicNormal: Minigame("Peril Path Panic (10 points)", Maps.PerilPathPanicNormal, True, True, 2, lambda l: True),
    Minigames.PerilPathPanicHard: Minigame("Peril Path Panic (12 points)", Maps.PerilPathPanicHard, True, True, 3, lambda l: True),
    # Helm barrels
    Minigames.DonkeyRambi: Minigame("Hideout Helm: DK Rambi", Maps.HelmBarrelDKRambi, True, False, 0, lambda l: True),
    Minigames.DonkeyTarget: Minigame("Hideout Helm: DK Targets", Maps.HelmBarrelDKTarget, True, False, 0, lambda l: l.isdonkey),
    Minigames.DiddyKremling: Minigame("Hideout Helm: Diddy Kremlings", Maps.HelmBarrelDiddyKremling, True, False, 0, lambda l: l.Slam),
    Minigames.DiddyRocketbarrel: Minigame("Hideout Helm: Diddy Rocketbarrel", Maps.HelmBarrelDiddyRocketbarrel, True, False, 0, lambda l: l.Slam and l.jetpack and l.peanut and l.isdiddy),
    # Supposed to use sprint but can make it without), even with Chunky
    Minigames.LankyMaze: Minigame("Hideout Helm: Lanky Maze", Maps.HelmBarrelLankyMaze, True, False, 0, lambda l: True),
    Minigames.LankyShooting: Minigame(
        "Hideout Helm: Lanky Shooting",
        Maps.HelmBarrelLankyShooting,
        True,
        False,
        0,
        lambda l: (l.isdonkey and l.coconut) or (l.isdiddy and l.peanut) or (l.islanky and l.grape) or (l.istiny and l.feather) or (l.ischunky and l.pineapple),
    ),
    Minigames.TinyMushroom: Minigame("Hideout Helm: Tiny Mushroom", Maps.HelmBarrelTinyMush, True, False, 0, lambda l: True),
    Minigames.TinyPonyTailTwirl: Minigame("Hideout Helm: Tiny Ponytail Twirl", Maps.HelmBarrelTinyPTT, True, False, 0, lambda l: l.twirl and l.istiny),
    Minigames.ChunkyHiddenKremling: Minigame("Hideout Helm: Chunky Hidden Kremling", Maps.HelmBarrelChunkyHidden, True, False, 0, lambda l: l.hunkyChunky and l.punch and l.ischunky),
    Minigames.ChunkyShooting: Minigame(
        "Hideout Helm: Chunky Shooting",
        Maps.HelmBarrelChunkyShooting,
        True,
        False,
        0,
        lambda l: (l.scope or l.homing or l.settings.hard_shooting) and ((l.isdonkey and l.coconut) or (l.isdiddy and l.peanut) or (l.islanky and l.grape) or (l.istiny and l.feather) or (l.ischunky and l.pineapple)),
    ),
}

MinigameAssociations = {
    Locations.IslesDiddySnidesLobby: Minigames.BattyBarrelBandit,
    Locations.IslesTinyAztecLobby: Minigames.BigBugBash,
    Locations.IslesChunkyHelmLobby: Minigames.KremlingKosh,
    Locations.IslesDiddySummit: Minigames.PerilPathPanic,
    Locations.IslesLankyCastleLobby: Minigames.SearchlightSeek,
    Locations.JapesLankyGrapeGate: Minigames.MadMazeMaulEasy,
    Locations.JapesChunkyGiantBonusBarrel: Minigames.MinecartMayhemEasy,
    Locations.JapesLankySlope: Minigames.SpeedySwingSortieEasy,
    Locations.JapesTinyFeatherGateBarrel: Minigames.SplishSplashSalvageNormal,
    Locations.AztecLanky5DoorTemple: Minigames.BigBugBashVEasy,
    Locations.AztecChunkyCagedBarrel: Minigames.BusyBarrelBarrageEasy,
    Locations.AztecChunky5DoorTemple: Minigames.KremlingKoshVEasy,
    Locations.AztecDonkeyQuicksandCave: Minigames.StealthySnoopVEasy,
    Locations.AztecLankyLlamaTempleBarrel: Minigames.TeeteringTurtleTroubleVEasy,
    Locations.FactoryLankyTestingRoomBarrel: Minigames.BattyBarrelBanditEasy,
    Locations.FactoryDiddyChunkyRoomBarrel: Minigames.BeaverBotherEasy,
    Locations.FactoryTinyProductionRoom: Minigames.KrazyKongKlamourEasy,
    Locations.FactoryDiddyBlockTower: Minigames.PerilPathPanicVEasy,
    Locations.FactoryChunkybyArcade: Minigames.StashSnatchEasy,
    Locations.GalleonChunky5DoorShip: Minigames.BattyBarrelBanditVEasy,
    Locations.GalleonTinySubmarine: Minigames.BigBugBashEasy,
    Locations.GalleonDonkey5DoorShip: Minigames.KrazyKongKlamourEasy,
    Locations.GalleonTiny2DoorShip: Minigames.KremlingKoshEasy,
    Locations.GalleonLankyGoldTower: Minigames.SearchlightSeekVEasy,
    Locations.GalleonDiddy5DoorShip: Minigames.SplishSplashSalvageEasy,
    Locations.GalleonDiddyGoldTower: Minigames.StealthySnoopNormal,
    Locations.ForestDiddyOwlRace: Minigames.BusyBarrelBarrageNormal,
    Locations.ForestLankyColoredMushrooms: Minigames.KrazyKongKlamourHard,
    Locations.ForestDonkeyBarn: Minigames.MinecartMayhemNormal,
    Locations.ForestDonkeyBaboonBlast: Minigames.PerilPathPanicEasy,
    Locations.ForestTinyMushroomBarrel: Minigames.SpeedySwingSortieNormal,
    Locations.ForestDiddyTopofMushroom: Minigames.TeeteringTurtleTroubleEasy,
    Locations.CavesDonkeyBaboonBlast: Minigames.BusyBarrelBarrageHard,
    Locations.CavesTinyCaveBarrel: Minigames.KrazyKongKlamourHard,
    Locations.CavesDiddyJetpackBarrel: Minigames.MadMazeMaulNormal,
    Locations.CavesChunky5DoorCabin: Minigames.SearchlightSeekNormal,
    Locations.CastleLankyTower: Minigames.BeaverBotherNormal,
    Locations.CastleChunkyTree: Minigames.BeaverBotherNormal,
    Locations.CastleDiddyAboveCastle: Minigames.BigBugBashHard,
    Locations.CastleLankyDungeon: Minigames.KremlingKoshNormal,
    Locations.CastleDiddyBallroom: Minigames.MinecartMayhemHard,
    Locations.CastleChunkyCrypt: Minigames.SearchlightSeekHard,
    Locations.CastleTinyOverChasm: Minigames.TeeteringTurtleTroubleNormal,
    Locations.HelmDonkey1: Minigames.DonkeyRambi,
    Locations.HelmDonkey2: Minigames.DonkeyTarget,
    Locations.HelmDiddy1: Minigames.DiddyKremling,
    Locations.HelmDiddy2: Minigames.DiddyRocketbarrel,
    Locations.HelmLanky1: Minigames.LankyMaze,
    Locations.HelmLanky2: Minigames.LankyShooting,
    Locations.HelmTiny1: Minigames.TinyMushroom,
    Locations.HelmTiny2: Minigames.TinyPonyTailTwirl,
    Locations.HelmChunky1: Minigames.ChunkyHiddenKremling,
    Locations.HelmChunky2: Minigames.ChunkyShooting,
}

BarrelMetaData = {
    Locations.IslesDiddySnidesLobby: MinigameLocationData(Maps.IslesSnideRoom,2),
    Locations.IslesTinyAztecLobby: MinigameLocationData(Maps.AngryAztecLobby,1),
    Locations.IslesChunkyHelmLobby: MinigameLocationData(Maps.HideoutHelmLobby,10),
    Locations.IslesDiddySummit: MinigameLocationData(Maps.Isles,11),
    Locations.IslesLankyCastleLobby: MinigameLocationData(Maps.CreepyCastleLobby,2),
    Locations.JapesLankyGrapeGate: MinigameLocationData(Maps.JungleJapes,32),
    Locations.JapesChunkyGiantBonusBarrel: MinigameLocationData(Maps.JungleJapes,33),
    Locations.JapesLankySlope: MinigameLocationData(Maps.JungleJapes,34),
    Locations.JapesTinyFeatherGateBarrel: MinigameLocationData(Maps.JungleJapes,31),
    Locations.AztecLanky5DoorTemple: MinigameLocationData(Maps.AztecLanky5DoorTemple,0),
    Locations.AztecChunkyCagedBarrel: MinigameLocationData(Maps.AngryAztec,35),
    Locations.AztecChunky5DoorTemple: MinigameLocationData(Maps.AztecChunky5DoorTemple,0),
    Locations.AztecDonkeyQuicksandCave: MinigameLocationData(Maps.AngryAztec,33),
    Locations.AztecLankyLlamaTempleBarrel: MinigameLocationData(Maps.AztecLlamaTemple,2),
    Locations.FactoryLankyTestingRoomBarrel: MinigameLocationData(Maps.FranticFactory,15),
    Locations.FactoryDiddyChunkyRoomBarrel: MinigameLocationData(Maps.FranticFactory,13),
    Locations.FactoryTinyProductionRoom: MinigameLocationData(Maps.FranticFactory,16),
    Locations.FactoryDiddyBlockTower: MinigameLocationData(Maps.FranticFactory,0),
    Locations.FactoryChunkybyArcade: MinigameLocationData(Maps.FranticFactory,14),
    Locations.GalleonChunky5DoorShip: MinigameLocationData(Maps.Galleon5DShipDiddyLankyChunky,1),
    Locations.GalleonTinySubmarine: MinigameLocationData(Maps.GalleonSubmarine,3),
    Locations.GalleonDonkey5DoorShip: MinigameLocationData(Maps.Galleon5DShipDKTiny,0),
    Locations.GalleonTiny2DoorShip: MinigameLocationData(Maps.Galleon2DShip,0),
    Locations.GalleonLankyGoldTower: MinigameLocationData(Maps.GloomyGalleon,7),
    Locations.GalleonDiddy5DoorShip: MinigameLocationData(Maps.Galleon5DShipDiddyLankyChunky,0),
    Locations.GalleonDiddyGoldTower: MinigameLocationData(Maps.GloomyGalleon,6),
    Locations.ForestDiddyOwlRace: MinigameLocationData(Maps.FungiForest,21),
    Locations.ForestLankyColoredMushrooms: MinigameLocationData(Maps.ForestLankyMushroomsRoom,0),
    Locations.ForestDonkeyBarn: MinigameLocationData(Maps.ForestThornvineBarn,3),
    Locations.ForestDonkeyBaboonBlast: MinigameLocationData(Maps.ForestBaboonBlast,22),
    Locations.ForestTinyMushroomBarrel: MinigameLocationData(Maps.ForestGiantMushroom,8),
    Locations.ForestDiddyTopofMushroom: MinigameLocationData(Maps.FungiForest,18),
    Locations.CavesDonkeyBaboonBlast: MinigameLocationData(Maps.CavesBaboonBlast,19),
    Locations.CavesTinyCaveBarrel: MinigameLocationData(Maps.CrystalCaves,7),
    Locations.CavesDiddyJetpackBarrel: MinigameLocationData(Maps.CrystalCaves,6),
    Locations.CavesChunky5DoorCabin: MinigameLocationData(Maps.CavesChunkyCabin,0),
    Locations.CastleLankyTower: MinigameLocationData(Maps.CastleTower,0),
    Locations.CastleChunkyTree: MinigameLocationData(Maps.CastleTree,0),
    Locations.CastleDiddyAboveCastle: MinigameLocationData(Maps.CreepyCastle,9),
    Locations.CastleLankyDungeon: MinigameLocationData(Maps.CastleDungeon,0),
    Locations.CastleDiddyBallroom: MinigameLocationData(Maps.CastleBallroom,1),
    Locations.CastleChunkyCrypt: MinigameLocationData(Maps.CastleCrypt,0),
    Locations.CastleTinyOverChasm: MinigameLocationData(Maps.CastleUpperCave,0),
    Locations.HelmDonkey1: MinigameLocationData(Maps.HideoutHelm,16),
    Locations.HelmDonkey2: MinigameLocationData(Maps.HideoutHelm,15),
    Locations.HelmDiddy1: MinigameLocationData(Maps.HideoutHelm,8),
    Locations.HelmDiddy2: MinigameLocationData(Maps.HideoutHelm,9),
    Locations.HelmLanky1: MinigameLocationData(Maps.HideoutHelm,10),
    Locations.HelmLanky2: MinigameLocationData(Maps.HideoutHelm,11),
    Locations.HelmTiny1: MinigameLocationData(Maps.HideoutHelm,13),
    Locations.HelmTiny2: MinigameLocationData(Maps.HideoutHelm,12),
    Locations.HelmChunky1: MinigameLocationData(Maps.HideoutHelm,14),
    Locations.HelmChunky2: MinigameLocationData(Maps.HideoutHelm,7),
}
