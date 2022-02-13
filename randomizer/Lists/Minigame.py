"""Stores the requirements for each minigame."""

from randomizer.Enums.Locations import Locations
from randomizer.Enums.Minigames import Minigames


class Minigame:
    """Class which stores name and logic for a minigame."""

    def __init__(self, name, logic):
        """Initialize with given parameters."""
        self.name = name
        self.logic = logic


MinigameRequirements = {
    Minigames.NoGame: Minigame("No Game", lambda l: True),
    # Misc. Barrels
    Minigames.BattyBarrelBandit: Minigame("Batty Barrel Bandit", lambda l: True),
    Minigames.BigBugBash: Minigame("Big Bug Bash", lambda l: True),
    Minigames.BeaverBother: Minigame("Beaver Bother", lambda l: True),
    Minigames.MinecartMayhem: Minigame("Minecart Mayhem", lambda l: True),
    Minigames.KremlingKosh: Minigame("Kremling Kosh", lambda l: True),
    Minigames.PerilPathPanic: Minigame("Peril Path Panic", lambda l: True),
    Minigames.SearchlightSeek: Minigame("Searchlight Seek", lambda l: True),
    Minigames.TeeteringTurtleTrouble: Minigame("Teetering Turtle Trouble", lambda l: True),
    Minigames.KrazyKongKlamour: Minigame("Krazy Kong Klamour", lambda l: True),
    Minigames.StashSnatch: Minigame("Stash Snatch", lambda l: True),
    Minigames.StealthySnoop: Minigame("Stealthy Snoop", lambda l: True),
    Minigames.MadMazeMaul: Minigame("Mad Maze Maul", lambda l: True),
    Minigames.MadMazeMaulShockwave: Minigame("Mad Maze Maul (Shockwave)", lambda l: l.shockwave),
    Minigames.SpeedySwingSortie: Minigame("Speedy Swing Sortie", lambda l: l.vines),
    Minigames.SpeedySwingSortieTwirl: Minigame("Speedy Swing Sortie (Twirl)", lambda l: l.vines and l.twirl and l.istiny),
    Minigames.SplishSplashSalvage: Minigame("Splish Splash Salvage", lambda l: l.swim),
    Minigames.SplishSplashSalvageVines: Minigame("Splish Splash Salvage (Vines)", lambda l: l.swim and l.vines),
    # Lanky excluded from this game because his gun is too long
    Minigames.BusyBarrelBarrage: Minigame("Busy Barrel Barrage", lambda l: (l.isdonkey and l.coconut) or (l.isdiddy and l.peanut) or (l.istiny and l.feather) or (l.ischunky and l.pineapple)),
    # Helm barrels
    Minigames.DonkeyRambi: Minigame("Donkey Rambi", lambda l: True),
    Minigames.DonkeyTarget: Minigame("Donkey Targets", lambda l: l.isdonkey),
    Minigames.DiddyKremling: Minigame("Diddy Kremlings", lambda l: l.Slam),
    Minigames.DiddyRocketbarrel: Minigame("Diddy Rocketbarrel", lambda l: l.Slam and l.jetpack and l.peanut and l.isdiddy),
    # Supposed to use sprint but can make it without), even with Chunky
    Minigames.LankyMaze: Minigame("Lanky Maze", lambda l: True),
    Minigames.LankyShooting: Minigame(
        "Lanky Shooting", lambda l: (l.isdonkey and l.coconut) or (l.isdiddy and l.peanut) or (l.islanky and l.grape) or (l.istiny and l.feather) or (l.ischunky and l.pineapple)
    ),
    Minigames.TinyMushroom: Minigame("Tiny Mushrooms", lambda l: True),
    Minigames.TinyPonyTailTwirl: Minigame("Tiny PonyTail Twirl", lambda l: l.twirl and l.istiny),
    Minigames.ChunkyHiddenKremling: Minigame("Chunky Hidden Kremling", lambda l: l.hunkyChunky and l.punch and l.ischunky),
    Minigames.ChunkyShooting: Minigame(
        "Chunky Shooting", lambda l: (l.isdonkey and l.coconut) or (l.isdiddy and l.peanut) or (l.islanky and l.grape) or (l.istiny and l.feather) or (l.ischunky and l.pineapple)
    ),
}

MinigameAssociations = {
    Locations.IslesDiddySnidesLobby: Minigames.BattyBarrelBandit,
    Locations.IslesTinyAztecLobby: Minigames.BigBugBash,
    Locations.IslesChunkyHelmLobby: Minigames.KremlingKosh,
    Locations.IslesDiddySummit: Minigames.PerilPathPanic,
    Locations.IslesLankyCastleLobby: Minigames.SearchlightSeek,
    Locations.JapesLankyGrapeGate: Minigames.MadMazeMaul,
    Locations.JapesChunkyGiantBonusBarrel: Minigames.MinecartMayhem,
    Locations.JapesLankySlope: Minigames.SpeedySwingSortie,
    Locations.JapesTinyFeatherGateBarrel: Minigames.SplishSplashSalvage,
    Locations.AztecLanky5DoorTemple: Minigames.BigBugBash,
    Locations.AztecChunkyCagedBarrel: Minigames.BusyBarrelBarrage,
    Locations.AztecChunky5DoorTemple: Minigames.KremlingKosh,
    Locations.AztecDonkeyQuicksandCave: Minigames.StealthySnoop,
    Locations.AztecLankyLlamaTempleBarrel: Minigames.TeeteringTurtleTrouble,
    Locations.FactoryLankyTestingRoomBarrel: Minigames.BattyBarrelBandit,
    Locations.FactoryDiddyChunkyRoomBarrel: Minigames.BeaverBother,
    Locations.FactoryTinyProductionRoom: Minigames.KrazyKongKlamour,
    Locations.FactoryDiddyBlockTower: Minigames.PerilPathPanic,
    Locations.FactoryChunkybyArcade: Minigames.StashSnatch,
    Locations.GalleonChunky5DoorShip: Minigames.BattyBarrelBandit,
    Locations.GalleonTinySubmarine: Minigames.BigBugBash,
    Locations.GalleonDonkey5DoorShip: Minigames.KrazyKongKlamour,
    Locations.GalleonTiny2DoorShip: Minigames.KremlingKosh,
    Locations.GalleonLankyGoldTower: Minigames.SearchlightSeek,
    Locations.GalleonDiddy5DoorShip: Minigames.SplishSplashSalvageVines,
    Locations.GalleonDiddyGoldTower: Minigames.StealthySnoop,
    Locations.ForestDiddyOwlRace: Minigames.BusyBarrelBarrage,
    Locations.ForestLankyColoredMushrooms: Minigames.KrazyKongKlamour,
    Locations.ForestDonkeyBarn: Minigames.MinecartMayhem,
    Locations.ForestDonkeyBaboonBlast: Minigames.PerilPathPanic,
    Locations.ForestTinyMushroomBarrel: Minigames.SpeedySwingSortieTwirl,
    Locations.ForestDiddyTopofMushroom: Minigames.TeeteringTurtleTrouble,
    Locations.CavesDonkeyBaboonBlast: Minigames.BusyBarrelBarrage,
    Locations.CavesTinyCaveBarrel: Minigames.KrazyKongKlamour,
    Locations.CavesDiddyJetpackBarrel: Minigames.MadMazeMaul,
    Locations.CavesChunky5DoorCabin: Minigames.SearchlightSeek,
    Locations.CastleLankyTower: Minigames.BeaverBother,
    Locations.CastleChunkyTree: Minigames.BeaverBother,
    Locations.CastleDiddyAboveCastle: Minigames.BigBugBash,
    Locations.CastleLankyDungeon: Minigames.KremlingKosh,
    Locations.CastleDiddyBallroom: Minigames.MinecartMayhem,
    Locations.CastleChunkyCrypt: Minigames.SearchlightSeek,
    Locations.CastleTinyOverChasm: Minigames.TeeteringTurtleTrouble,
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
