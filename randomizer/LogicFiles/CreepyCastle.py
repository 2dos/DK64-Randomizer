# fmt: off
"""Logic file for Creepy Castle."""

from randomizer.Enums.Events import Events
from randomizer.Enums.TransitionFronts import TransitionFronts
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Regions import Regions
from randomizer.LogicClasses import TransitionFront, Event, LocationLogic, Region

LogicRegions = {
    Regions.CreepyCastleMain: Region("Creepy Castle Main", Levels.CreepyCastle, True, None, [
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
        TransitionFront(Regions.CreepyCastleLobby, lambda l: True, TransitionFronts.CastleToIsles),
        TransitionFront(Regions.CastleWaterfall, lambda l: True),
        TransitionFront(Regions.CastleTree, lambda l: l.blast, TransitionFronts.CastleMainToTree),
        TransitionFront(Regions.Library, lambda l: l.superDuperSlam and l.isdonkey, TransitionFronts.CastleMainToLibrary),
        TransitionFront(Regions.Ballroom, lambda l: l.superDuperSlam and l.diddy, TransitionFronts.CastleMainToBallroom),  # Stays open
        TransitionFront(Regions.Tower, lambda l: l.superDuperSlam and l.islanky, TransitionFronts.CastleMainToTower),
        TransitionFront(Regions.Greenhouse, lambda l: l.superDuperSlam and l.islanky, TransitionFronts.CastleMainToGreenhouse),
        TransitionFront(Regions.TrashCan, lambda l: l.mini and l.istiny, TransitionFronts.CastleMainToTrash),
        TransitionFront(Regions.Shed, lambda l: l.punch and l.ischunky, TransitionFronts.CastleMainToShed),
        TransitionFront(Regions.Museum, lambda l: l.superDuperSlam and l.ischunky, TransitionFronts.CastleMainToMuseum),
        TransitionFront(Regions.LowerCave, lambda l: True, TransitionFronts.CastleMainToLower),
        TransitionFront(Regions.UpperCave, lambda l: True, TransitionFronts.CastleMainToUpper),
        TransitionFront(Regions.Cranky, lambda l: True),
        TransitionFront(Regions.Snide, lambda l: True),
        TransitionFront(Regions.CastleBossLobby, lambda l: True),
    ]),

    # This region just exists to facilitate the multiple exits from the upper cave
    Regions.CastleWaterfall: Region("Castle Waterfall", Levels.CreepyCastle, False, None, [], [], [
        TransitionFront(Regions.CreepyCastleMain, lambda l: True),
        TransitionFront(Regions.UpperCave, lambda l: True, TransitionFronts.CastleWaterfallToUpper),
    ]),

    Regions.CastleTree: Region("Castle Tree", Levels.CreepyCastle, False, -1, [
        LocationLogic(Locations.CastleDonkeyTree, lambda l: l.coconut and l.isdonkey),
        LocationLogic(Locations.CastleChunkyTree, lambda l: l.pineapple and l.punch and l.ischunky),
        LocationLogic(Locations.CastleDonkeyKasplat, lambda l: l.coconut and l.isdonkey),
        LocationLogic(Locations.CastleBananaFairyTree, lambda l: l.camera and l.coconut and l.isdonkey),
    ], [], [
        TransitionFront(Regions.CreepyCastleMain, lambda l: True, TransitionFronts.CastleTreeToMain),
        TransitionFront(Regions.CreepyCastleMain, lambda l: True), #Exits.CastleTreeDrainToMain
    ]),

    Regions.Library: Region("Library", Levels.CreepyCastle, False, -1, [
        # Another case where you're supposed to use Strong Kong but it can be brute forced
        LocationLogic(Locations.CastleDonkeyLibrary, lambda l: l.superDuperSlam and l.isdonkey),
    ], [], [
        TransitionFront(Regions.CreepyCastleMain, lambda l: True, TransitionFronts.CastleLibraryToMain),
    ]),

    Regions.Ballroom: Region("Ballroom", Levels.CreepyCastle, False, -1, [
        LocationLogic(Locations.CastleDiddyBallroom, lambda l: l.jetpack and l.isdiddy),
        LocationLogic(Locations.CastleBananaFairyBallroom, lambda l: l.camera and l.monkeyport and l.istiny),
    ], [], [
        TransitionFront(Regions.CreepyCastleMain, lambda l: True, TransitionFronts.CastleBallroomToMain),
        TransitionFront(Regions.CastleTinyRace, lambda l: l.monkeyport and l.mini and l.istiny, TransitionFronts.CastleBallroomToRace),
    ]),

    Regions.CastleTinyRace: Region("Castle Tiny Race", Levels.CreepyCastle, False, None, [
        LocationLogic(Locations.CastleTinyCarRace, lambda l: l.istiny),
    ], [], [
        TransitionFront(Regions.Ballroom, lambda l: True, TransitionFronts.CastleRaceToBallroom)
    ]),

    Regions.Tower: Region("Tower", Levels.CreepyCastle, False, -1, [
        LocationLogic(Locations.CastleLankyTower, lambda l: l.balloon and l.grape and l.islanky),
    ], [], [
        TransitionFront(Regions.CreepyCastleMain, lambda l: True, TransitionFronts.CastleTowerToMain),
    ]),

    Regions.Greenhouse: Region("Greenhouse", Levels.CreepyCastle, False, -1, [
        # Not sure if sprint is actually required
        LocationLogic(Locations.CastleLankyGreenhouse, lambda l: l.sprint and l.islanky),
        LocationLogic(Locations.CastleBattleArena, lambda l: l.sprint and l.islanky),
    ], [], [
        TransitionFront(Regions.CreepyCastleMain, lambda l: True, TransitionFronts.CastleGreenhouseToMain),
    ]),

    Regions.TrashCan: Region("Trash Can", Levels.CreepyCastle, False, -1, [
        LocationLogic(Locations.CastleTinyTrashCan, lambda l: (l.saxophone or l.feather) and l.istiny),
    ], [], [
        TransitionFront(Regions.CreepyCastleMain, lambda l: True, TransitionFronts.CastleTrashToMain),
    ]),

    Regions.Shed: Region("Shed", Levels.CreepyCastle, False, None, [
        LocationLogic(Locations.CastleChunkyShed, lambda l: l.punch and l.gorillaGone and l.ischunky),
    ], [], [
        TransitionFront(Regions.CreepyCastleMain, lambda l: True, TransitionFronts.CastleShedToMain),
    ]),

    Regions.Museum: Region("Museum", Levels.CreepyCastle, False, -1, [
        LocationLogic(Locations.CastleChunkyMuseum, lambda l: l.punch and l.ischunky),
    ], [], [
        TransitionFront(Regions.CreepyCastleMain, lambda l: True, TransitionFronts.CastleMuseumToMain),
    ]),

    Regions.LowerCave: Region("Lower Cave", Levels.CreepyCastle, True, -1, [
        LocationLogic(Locations.CastleDiddyKasplat, lambda l: l.diddy),
    ], [], [
        TransitionFront(Regions.CreepyCastleMain, lambda l: True, TransitionFronts.CastleLowerToMain),
        TransitionFront(Regions.Crypt, lambda l: (l.coconut and l.isdonkey) or (l.peanut and l.isdiddy) or (l.pineapple and l.ischunky), TransitionFronts.CastleLowerToCrypt),
        TransitionFront(Regions.Mausoleum, lambda l: (l.grape and l.islanky) or (l.feather and l.istiny), TransitionFronts.CastleLowerToMausoleum),
        TransitionFront(Regions.Funky, lambda l: True),
        TransitionFront(Regions.CastleBossLobby, lambda l: True),
    ]),

    Regions.Crypt: Region("Crypt", Levels.CreepyCastle, False, -1, [
        LocationLogic(Locations.CastleDiddyCrypt, lambda l: l.peanut and l.charge and l.isdiddy),
        LocationLogic(Locations.CastleChunkyCrypt, lambda l: l.pineapple and l.punch and l.ischunky),
    ], [], [
        TransitionFront(Regions.LowerCave, lambda l: True, TransitionFronts.CastleCryptToLower),
        TransitionFront(Regions.CastleMinecarts, lambda l: l.coconut and l.grab and l.isdonkey, TransitionFronts.CastleCryptToCarts),
    ]),

    Regions.CastleMinecarts: Region("Castle Minecarts", Levels.CreepyCastle, False, None, [
        LocationLogic(Locations.CastleDonkeyMinecarts, lambda l: l.isdonkey),
    ], [], [
        TransitionFront(Regions.Crypt, lambda l: True, TransitionFronts.CastleCartsToCrypt),
    ]),

    Regions.Mausoleum: Region("Mausoleum", Levels.CreepyCastle, False, None, [
        LocationLogic(Locations.CastleLankyMausoleum, lambda l: l.grape and l.sprint and l.trombone and l.islanky),
        LocationLogic(Locations.CastleTinyMausoleum, lambda l: l.superDuperSlam and l.twirl and l.istiny),
    ], [], [
        TransitionFront(Regions.LowerCave, lambda l: True, TransitionFronts.CastleMausoleumToLower),
    ]),

    Regions.UpperCave: Region("Upper Cave", Levels.CreepyCastle, True, -1, [
        LocationLogic(Locations.CastleTinyOverChasm, lambda l: l.twirl and l.tiny),
        LocationLogic(Locations.CastleChunkyKasplat, lambda l: l.chunky),
    ], [], [
        TransitionFront(Regions.CreepyCastleMain, lambda l: True, TransitionFronts.CastleUpperToMain),
        TransitionFront(Regions.CastleWaterfall, lambda l: True, TransitionFronts.CastleUpperToWaterfall),
        TransitionFront(Regions.Dungeon, lambda l: True, TransitionFronts.CastleUpperToDungeon),
        TransitionFront(Regions.Candy, lambda l: True),
        TransitionFront(Regions.CastleBossLobby, lambda l: True),
    ]),

    Regions.Dungeon: Region("Dungeon", Levels.CreepyCastle, True, None, [
        LocationLogic(Locations.CastleDonkeyDungeon, lambda l: l.superDuperSlam and l.donkey),
        LocationLogic(Locations.CastleDiddyDungeon, lambda l: l.superDuperSlam and l.peanut and l.diddy),
        LocationLogic(Locations.CastleLankyDungeon, lambda l: l.superDuperSlam and l.trombone and l.balloon and l.lanky),
    ], [], [
        TransitionFront(Regions.UpperCave, lambda l: True, TransitionFronts.CastleDungeonToUpper),
    ]),

    Regions.CastleBossLobby: Region("Castle Boss Lobby", Levels.CreepyCastle, True, None, [], [], [
        TransitionFront(Regions.CastleBoss, lambda l: l.islanky and sum(l.ColoredBananas[Levels.CreepyCastle]) >= l.settings.BossBananas[Levels.CreepyCastle - 1]),
    ]),

    Regions.CastleBoss: Region("Castle Boss", Levels.CreepyCastle, False, None, [
        LocationLogic(Locations.CastleKey, lambda l: True),
    ], [], []),
}
