# fmt: off
"""Logic file for Creepy Castle."""

from randomizer.Enums.Events import Events
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Regions import Regions
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Kongs import Kongs
from randomizer.LogicClasses import Event, Exit, LocationLogic, Region

LogicRegions = {
    Regions.CreepyCastleMain: Region("Creepy Castle Main", Levels.CreepyCastle, True, [
        LocationLogic(Locations.CastleDonkeyMedal, lambda l: l.ColoredBananas[Levels.CreepyCastle][Kongs.donkey] >= 75),
        LocationLogic(Locations.CastleDiddyMedal, lambda l: l.ColoredBananas[Levels.CreepyCastle][Kongs.diddy] >= 75),
        LocationLogic(Locations.CastleLankyMedal, lambda l: l.ColoredBananas[Levels.CreepyCastle][Kongs.lanky] >= 75),
        LocationLogic(Locations.CastleTinyMedal, lambda l: l.ColoredBananas[Levels.CreepyCastle][Kongs.tiny] >= 75),
        LocationLogic(Locations.CastleChunkyMedal, lambda l: l.ColoredBananas[Levels.CreepyCastle][Kongs.chunky] >= 75),
        LocationLogic(Locations.CastleDiddyAboveCastle, lambda l: l.jetpack and l.isdiddy),
        LocationLogic(Locations.CastleLankyKasplat, lambda l: l.islanky),
        LocationLogic(Locations.CastleTinyKasplat, lambda l: l.istiny),
    ], [
        Event(Events.CastleEntered, lambda l: True),
    ], [
        Exit(Regions.CreepyCastleLobby, lambda l: True),
        Exit(Regions.CastleWaterfall, lambda l: True),
        Exit(Regions.CastleTree, lambda l: l.blast),
        Exit(Regions.Library, lambda l: l.superDuperSlam and l.isdonkey),
        Exit(Regions.Ballroom, lambda l: l.superDuperSlam and l.diddy),  # Stays open
        Exit(Regions.Tower, lambda l: l.superDuperSlam and l.islanky),
        Exit(Regions.Greenhouse, lambda l: l.superDuperSlam and l.islanky),
        Exit(Regions.TrashCan, lambda l: l.mini and l.istiny),
        Exit(Regions.Shed, lambda l: l.punch and l.ischunky),
        Exit(Regions.Museum, lambda l: l.superDuperSlam and l.ischunky),
        Exit(Regions.LowerCave, lambda l: True),
        Exit(Regions.UpperCave, lambda l: True),
        Exit(Regions.Cranky, lambda l: True),
        Exit(Regions.Snide, lambda l: True),
        Exit(Regions.CastleBossLobby, lambda l: True),
    ]),

    # This region just exists to facilitate the multiple exits from the upper cave
    Regions.CastleWaterfall: Region("Castle Waterfall", Levels.CreepyCastle, False, [], [], [
        Exit(Regions.CreepyCastleMain, lambda l: True),
        Exit(Regions.UpperCave, lambda l: True),
    ]),

    Regions.CastleTree: Region("Castle Tree", Levels.CreepyCastle, False, [
        LocationLogic(Locations.CastleDonkeyTree, lambda l: l.coconut and l.isdonkey),
        LocationLogic(Locations.CastleChunkyTree, lambda l: l.pineapple and l.punch and l.ischunky),
        LocationLogic(Locations.CastleDonkeyKasplat, lambda l: l.coconut and l.isdonkey),
        LocationLogic(Locations.CastleBananaFairyTree, lambda l: l.camera and l.coconut and l.isdonkey),
    ], [], [
        Exit(Regions.CreepyCastleMain, lambda l: True),
    ]),

    Regions.Library: Region("Library", Levels.CreepyCastle, False, [
        # Another case where you're supposed to use Strong Kong but it can be brute forced
        LocationLogic(Locations.CastleDonkeyLibrary, lambda l: l.superDuperSlam and l.isdonkey),
    ], [], [
        Exit(Regions.CreepyCastleMain, lambda l: True),
    ]),

    Regions.Ballroom: Region("Ballroom", Levels.CreepyCastle, False, [
        LocationLogic(Locations.CastleDiddyBallroom, lambda l: l.jetpack and l.isdiddy),
        LocationLogic(Locations.CastleBananaFairyBallroom, lambda l: l.camera and l.monkeyport and l.istiny),
    ], [], [
        Exit(Regions.CreepyCastleMain, lambda l: True),
        Exit(Regions.CastleTinyRace, lambda l: l.monkeyport and l.mini and l.istiny),
    ]),

    Regions.CastleTinyRace: Region("Castle Tiny Race", Levels.CreepyCastle, False, [
        LocationLogic(Locations.CastleTinyCarRace, lambda l: l.istiny),
    ], [], []),

    Regions.Tower: Region("Tower", Levels.CreepyCastle, False, [
        LocationLogic(Locations.CastleLankyTower, lambda l: l.balloon and l.grape and l.islanky),
    ], [], [
        Exit(Regions.CreepyCastleMain, lambda l: True),
    ]),

    Regions.Greenhouse: Region("Greenhouse", Levels.CreepyCastle, False, [
        # Not sure if sprint is actually required
        LocationLogic(Locations.CastleLankyGreenhouse, lambda l: l.sprint and l.islanky),
        LocationLogic(Locations.CastleBattleArena, lambda l: l.sprint and l.islanky),
    ], [], [
        Exit(Regions.CreepyCastleMain, lambda l: True),
    ]),

    Regions.TrashCan: Region("Trash Can", Levels.CreepyCastle, False, [
        LocationLogic(Locations.CastleTinyTrashCan, lambda l: l.feather and l.istiny),
    ], [], [
        Exit(Regions.CreepyCastleMain, lambda l: True),
    ]),

    Regions.Shed: Region("Shed", Levels.CreepyCastle, False, [
        LocationLogic(Locations.CastleChunkyShed, lambda l: l.punch and l.gorillaGone and l.ischunky),
    ], [], [
        Exit(Regions.CreepyCastleMain, lambda l: True),
    ]),

    Regions.Museum: Region("Museum", Levels.CreepyCastle, False, [
        LocationLogic(Locations.CastleChunkyMuseum, lambda l: l.punch and l.ischunky),
    ], [], [
        Exit(Regions.CreepyCastleMain, lambda l: True),
    ]),

    Regions.LowerCave: Region("Lower Cave", Levels.CreepyCastle, True, [
        LocationLogic(Locations.CastleDiddyKasplat, lambda l: l.isdiddy),
    ], [], [
        Exit(Regions.CreepyCastleMain, lambda l: True),
        Exit(Regions.Crypt, lambda l: (l.coconut and l.isdonkey) or (l.peanut and l.isdiddy) or (l.pineapple and l.ischunky)),
        Exit(Regions.Mausoleum, lambda l: (l.grape and l.islanky) or (l.feather and l.istiny)),
        Exit(Regions.Funky, lambda l: True),
        Exit(Regions.CastleBossLobby, lambda l: True),
    ]),

    Regions.Crypt: Region("Crypt", Levels.CreepyCastle, False, [
        LocationLogic(Locations.CastleDiddyCrypt, lambda l: l.peanut and l.charge and l.isdiddy),
        LocationLogic(Locations.CastleChunkyCrypt, lambda l: l.pineapple and l.punch and l.ischunky),
    ], [], [
        Exit(Regions.LowerCave, lambda l: True),
        Exit(Regions.CastleMinecarts, lambda l: l.coconut and l.grab and l.isdonkey),
    ]),

    Regions.CastleMinecarts: Region("Castle Minecarts", Levels.CreepyCastle, False, [
        LocationLogic(Locations.CastleDonkeyMinecarts, lambda l: l.isdonkey),
    ], [], []),

    Regions.Mausoleum: Region("Mausoleum", Levels.CreepyCastle, False, [
        LocationLogic(Locations.CastleLankyMausoleum, lambda l: l.grape and l.sprint and l.trombone and l.islanky),
        LocationLogic(Locations.CastleTinyMausoleum, lambda l: l.superDuperSlam and l.twirl and l.istiny),
    ], [], [
        Exit(Regions.LowerCave, lambda l: True),
    ]),

    Regions.UpperCave: Region("Upper Cave", Levels.CreepyCastle, True, [
        LocationLogic(Locations.CastleTinyOverChasm, lambda l: l.twirl and l.istiny),
        LocationLogic(Locations.CastleChunkyKasplat, lambda l: l.ischunky),
    ], [], [
        Exit(Regions.CreepyCastleMain, lambda l: True),
        Exit(Regions.CastleWaterfall, lambda l: True),
        Exit(Regions.Dungeon, lambda l: True),
        Exit(Regions.Candy, lambda l: True),
        Exit(Regions.CastleBossLobby, lambda l: True),
    ]),

    Regions.Dungeon: Region("Dungeon", Levels.CreepyCastle, True, [
        LocationLogic(Locations.CastleDonkeyDungeon, lambda l: l.superDuperSlam and l.isdonkey),
        LocationLogic(Locations.CastleDiddyDungeon, lambda l: l.superDuperSlam and l.peanut and l.isdiddy),
        LocationLogic(Locations.CastleLankyDungeon, lambda l: l.superDuperSlam and l.trombone and l.balloon and l.islanky),
    ], [], [
        Exit(Regions.UpperCave, lambda l: True),
    ]),

    Regions.CastleBossLobby: Region("Castle Boss Lobby", Levels.CreepyCastle, True, [], [], [
        Exit(Regions.CastleBoss, lambda l: l.islanky and sum(l.ColoredBananas[Levels.CreepyCastle]) >= 400),
    ]),

    Regions.CastleBoss: Region("Castle Boss", Levels.CreepyCastle, False, [
        LocationLogic(Locations.CastleKey, lambda l: True),
    ], [], []),
}
