# fmt: off
"""Logic file for Creepy Castle."""

from randomizer.Enums.Events import Events
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Regions import Regions
from randomizer.Enums.Exits import Exits
from randomizer.LogicClasses import Event, Exit, LocationLogic, Region

LogicRegions = {
    Regions.CreepyCastleMain: Region("Creepy Castle Main", Levels.CreepyCastle, True, [
        LocationLogic(Locations.CastleDonkeyMedal, lambda l: l.ColoredBananas[Levels.CreepyCastle][Kongs.donkey] >= 75),
        LocationLogic(Locations.CastleDiddyMedal, lambda l: l.ColoredBananas[Levels.CreepyCastle][Kongs.diddy] >= 75),
        LocationLogic(Locations.CastleLankyMedal, lambda l: l.ColoredBananas[Levels.CreepyCastle][Kongs.lanky] >= 75),
        LocationLogic(Locations.CastleTinyMedal, lambda l: l.ColoredBananas[Levels.CreepyCastle][Kongs.tiny] >= 75),
        LocationLogic(Locations.CastleChunkyMedal, lambda l: l.ColoredBananas[Levels.CreepyCastle][Kongs.chunky] >= 75),
        LocationLogic(Locations.CastleDiddyAboveCastle, lambda l: l.jetpack and l.diddy),
        LocationLogic(Locations.CastleLankyKasplat, lambda l: l.lanky),
        LocationLogic(Locations.CastleTinyKasplat, lambda l: l.tiny),
    ], [
        Event(Events.CastleEntered, lambda l: True),
    ], [
        Exit(Regions.CreepyCastleLobby, lambda l: True, Exits.CastleToIsles),
        Exit(Regions.CastleWaterfall, lambda l: True),
        Exit(Regions.CastleTree, lambda l: l.blast, Exits.CastleMainToTree),
        Exit(Regions.Library, lambda l: l.superDuperSlam and l.isdonkey, Exits.CastleMainToLibrary),
        Exit(Regions.Ballroom, lambda l: l.superDuperSlam and l.diddy, Exits.CastleMainToBallroom),  # Stays open
        Exit(Regions.Tower, lambda l: l.superDuperSlam and l.islanky, Exits.CastleMainToTower),
        Exit(Regions.Greenhouse, lambda l: l.superDuperSlam and l.islanky, Exits.CastleMainToGreenhouse),
        Exit(Regions.TrashCan, lambda l: l.mini and l.istiny, Exits.CastleMainToTrash),
        Exit(Regions.Shed, lambda l: l.punch and l.ischunky, Exits.CastleMainToShed),
        Exit(Regions.Museum, lambda l: l.superDuperSlam and l.ischunky, Exits.CastleMainToMuseum),
        Exit(Regions.LowerCave, lambda l: True, Exits.CastleMainToLower),
        Exit(Regions.UpperCave, lambda l: True, Exits.CastleMainToUpper),
        Exit(Regions.Cranky, lambda l: True),
        Exit(Regions.Snide, lambda l: True),
        Exit(Regions.CastleBossLobby, lambda l: True),
    ]),

    # This region just exists to facilitate the multiple exits from the upper cave
    Regions.CastleWaterfall: Region("Castle Waterfall", Levels.CreepyCastle, False, [], [], [
        Exit(Regions.CreepyCastleMain, lambda l: True),
        Exit(Regions.UpperCave, lambda l: True, Exits.CastleWaterfallToUpper),
    ]),

    Regions.CastleTree: Region("Castle Tree", Levels.CreepyCastle, False, [
        LocationLogic(Locations.CastleDonkeyTree, lambda l: l.coconut and l.isdonkey),
        LocationLogic(Locations.CastleChunkyTree, lambda l: l.pineapple and l.punch and l.ischunky),
        LocationLogic(Locations.CastleDonkeyKasplat, lambda l: l.coconut and l.isdonkey),
        LocationLogic(Locations.CastleBananaFairyTree, lambda l: l.camera and l.coconut and l.isdonkey),
    ], [], [
        Exit(Regions.CreepyCastleMain, lambda l: True, Exits.CastleTreeToMain),
    ]),

    Regions.Library: Region("Library", Levels.CreepyCastle, False, [
        # Another case where you're supposed to use Strong Kong but it can be brute forced
        LocationLogic(Locations.CastleDonkeyLibrary, lambda l: l.superDuperSlam and l.isdonkey),
    ], [], [
        Exit(Regions.CreepyCastleMain, lambda l: True, Exits.CastleLibraryToMain),
    ]),

    Regions.Ballroom: Region("Ballroom", Levels.CreepyCastle, False, [
        LocationLogic(Locations.CastleDiddyBallroom, lambda l: l.jetpack and l.isdiddy),
        LocationLogic(Locations.CastleBananaFairyBallroom, lambda l: l.camera and l.monkeyport and l.istiny),
    ], [], [
        Exit(Regions.CreepyCastleMain, lambda l: True, Exits.CastleBallroomToMain),
        Exit(Regions.CastleTinyRace, lambda l: l.monkeyport and l.mini and l.istiny, Exits.CastleBallroomToRace),
    ]),

    Regions.CastleTinyRace: Region("Castle Tiny Race", Levels.CreepyCastle, False, [
        LocationLogic(Locations.CastleTinyCarRace, lambda l: l.istiny),
    ], [], [
        Exit(Regions.Ballroom, lambda l: True, Exits.CastleRaceToBallroom)
    ]),

    Regions.Tower: Region("Tower", Levels.CreepyCastle, False, [
        LocationLogic(Locations.CastleLankyTower, lambda l: l.balloon and l.grape and l.islanky),
    ], [], [
        Exit(Regions.CreepyCastleMain, lambda l: True, Exits.CastleTowerToMain),
    ]),

    Regions.Greenhouse: Region("Greenhouse", Levels.CreepyCastle, False, [
        # Not sure if sprint is actually required
        LocationLogic(Locations.CastleLankyGreenhouse, lambda l: l.sprint and l.islanky),
        LocationLogic(Locations.CastleBattleArena, lambda l: l.sprint and l.islanky),
    ], [], [
        Exit(Regions.CreepyCastleMain, lambda l: True, Exits.CastleGreenhouseToMain),
    ]),

    Regions.TrashCan: Region("Trash Can", Levels.CreepyCastle, False, [
        LocationLogic(Locations.CastleTiny, lambda l: l.feather and l.istiny),
    ], [], [
        Exit(Regions.CreepyCastleMain, lambda l: True, Exits.CastleTrashToMain),
    ]),

    Regions.Shed: Region("Shed", Levels.CreepyCastle, False, [
        LocationLogic(Locations.CastleChunkyShed, lambda l: l.punch and l.gorillaGone and l.ischunky),
    ], [], [
        Exit(Regions.CreepyCastleMain, lambda l: True, Exits.CastleShedToMain),
    ]),

    Regions.Museum: Region("Museum", Levels.CreepyCastle, False, [
        LocationLogic(Locations.CastleChunkyMuseum, lambda l: l.punch and l.ischunky),
    ], [], [
        Exit(Regions.CreepyCastleMain, lambda l: True, Exits.CastleMuseumToMain),
    ]),

    Regions.LowerCave: Region("Lower Cave", Levels.CreepyCastle, True, [
        LocationLogic(Locations.CastleDiddyKasplat, lambda l: l.diddy),
    ], [], [
        Exit(Regions.CreepyCastleMain, lambda l: True, Exits.CastleLowerToMain),
        Exit(Regions.Crypt, lambda l: (l.coconut and l.isdonkey) or (l.peanut and l.isdiddy) or (l.pineapple and l.ischunky), Exits.CastleLowerToCrypt),
        Exit(Regions.Mausoleum, lambda l: (l.grape and l.islanky) or (l.feather and l.istiny), Exits.CastleLowerToMauseoleum),
        Exit(Regions.Funky, lambda l: True),
        Exit(Regions.CastleBossLobby, lambda l: True),
    ]),

    Regions.Crypt: Region("Crypt", Levels.CreepyCastle, False, [
        LocationLogic(Locations.CastleDiddyCrypt, lambda l: l.peanut and l.charge and l.isdiddy),
        LocationLogic(Locations.CastleChunkyCrypt, lambda l: l.pineapple and l.punch and l.ischunky),
    ], [], [
        Exit(Regions.LowerCave, lambda l: True, Exits.CastleCryptToLower),
        Exit(Regions.CastleMinecarts, lambda l: l.coconut and l.grab and l.isdonkey, Exits.CastleCryptToCarts),
    ]),

    Regions.CastleMinecarts: Region("Castle Minecarts", Levels.CreepyCastle, False, [
        LocationLogic(Locations.CastleDonkeyMinecarts, lambda l: l.isdonkey),
    ], [], [
        Exit(Regions.Crypt, lambda l: True, Exits.CastleCartsToCrypt),
    ]),

    Regions.Mausoleum: Region("Mausoleum", Levels.CreepyCastle, False, [
        LocationLogic(Locations.CastleLankyMausoleum, lambda l: l.grape and l.sprint and l.trombone and l.islanky),
        LocationLogic(Locations.CastleTinyMausoleum, lambda l: l.superDuperSlam and l.twirl and l.istiny),
    ], [], [
        Exit(Regions.LowerCave, lambda l: True, Exits.CastleMausoleumToLower),
    ]),

    Regions.UpperCave: Region("Upper Cave", Levels.CreepyCastle, True, [
        LocationLogic(Locations.CastleTinyOverChasm, lambda l: l.twirl and l.tiny),
        LocationLogic(Locations.CastleChunkyKasplat, lambda l: l.chunky),
    ], [], [
        Exit(Regions.CreepyCastleMain, lambda l: True, Exits.CastleUpperToMain),
        Exit(Regions.CastleWaterfall, lambda l: True, Exits.CastleUpperToWaterfall),
        Exit(Regions.Dungeon, lambda l: True, Exits.CastleUpperToDungeon),
        Exit(Regions.Candy, lambda l: True),
        Exit(Regions.CastleBossLobby, lambda l: True),
    ]),

    Regions.Dungeon: Region("Dungeon", Levels.CreepyCastle, True, [
        LocationLogic(Locations.CastleDonkeyDungeon, lambda l: l.superDuperSlam and l.donkey),
        LocationLogic(Locations.CastleDiddyDungeon, lambda l: l.superDuperSlam and l.peanut and l.diddy),
        LocationLogic(Locations.CastleLankyDungeon, lambda l: l.superDuperSlam and l.trombone and l.balloon and l.lanky),
    ], [], [
        Exit(Regions.UpperCave, lambda l: True, Exits.CastleDungeonToUpper),
    ]),

    Regions.CastleBossLobby: Region("Castle Boss Lobby", Levels.CreepyCastle, True, [], [], [
        Exit(Regions.CastleBoss, lambda l: l.islanky and sum(l.ColoredBananas[Levels.CreepyCastle]) >= l.settings.BossBananas[Levels.CreepyCastle - 1]),
    ]),

    Regions.CastleBoss: Region("Castle Boss", Levels.CreepyCastle, False, [
        LocationLogic(Locations.CastleKey, lambda l: True),
    ], [], []),
}
