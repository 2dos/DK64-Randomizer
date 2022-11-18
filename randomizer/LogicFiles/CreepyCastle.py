# fmt: off
"""Logic file for Creepy Castle."""

from randomizer.Enums.Events import Events
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.MinigameType import MinigameType
from randomizer.Enums.Regions import Regions
from randomizer.Enums.Transitions import Transitions
from randomizer.LogicClasses import (Event, LocationLogic, Region,
                                     TransitionFront)

LogicRegions = {
    Regions.CreepyCastleMedals: Region("Creepy Castle Medals", "Creepy Castle Medal Rewards", Levels.CreepyCastle, False, None, [
        LocationLogic(Locations.CastleDonkeyMedal, lambda l: l.ColoredBananas[Levels.CreepyCastle][Kongs.donkey] >= l.settings.medal_cb_req),
        LocationLogic(Locations.CastleDiddyMedal, lambda l: l.ColoredBananas[Levels.CreepyCastle][Kongs.diddy] >= l.settings.medal_cb_req),
        LocationLogic(Locations.CastleLankyMedal, lambda l: l.ColoredBananas[Levels.CreepyCastle][Kongs.lanky] >= l.settings.medal_cb_req),
        LocationLogic(Locations.CastleTinyMedal, lambda l: l.ColoredBananas[Levels.CreepyCastle][Kongs.tiny] >= l.settings.medal_cb_req),
        LocationLogic(Locations.CastleChunkyMedal, lambda l: l.ColoredBananas[Levels.CreepyCastle][Kongs.chunky] >= l.settings.medal_cb_req),
    ], [], []),

    Regions.CreepyCastleMain: Region("Creepy Castle Main", "Castle Surroundings", Levels.CreepyCastle, True, None, [
        LocationLogic(Locations.CastleDiddyAboveCastle, lambda l: l.jetpack and l.isdiddy, MinigameType.BonusBarrel),
        LocationLogic(Locations.CastleKasplatHalfway, lambda l: not l.settings.kasplat_rando),
        LocationLogic(Locations.CastleKasplatLowerLedge, lambda l: not l.settings.kasplat_rando),
    ], [
        Event(Events.CastleEntered, lambda l: True),
    ], [
        TransitionFront(Regions.CreepyCastleMedals, lambda l: True),
        TransitionFront(Regions.CreepyCastleLobby, lambda l: True, Transitions.CastleToIsles),
        TransitionFront(Regions.CastleWaterfall, lambda l: True),
        TransitionFront(Regions.CastleTree, lambda l: Events.CastleTreeOpened in l.Events, Transitions.CastleMainToTree),
        TransitionFront(Regions.Library, lambda l: l.superDuperSlam and l.isdonkey, Transitions.CastleMainToLibraryStart),
        # Special Case for back door - it's only open right when you leave
        # TransitionFront(Regions.Library, lambda l: True, Transitions.CastleMainToLibraryEnd),
        TransitionFront(Regions.Ballroom, lambda l: l.superDuperSlam and l.diddy, Transitions.CastleMainToBallroom),  # Stays open
        TransitionFront(Regions.Tower, lambda l: l.superDuperSlam and l.islanky, Transitions.CastleMainToTower),
        TransitionFront(Regions.Greenhouse, lambda l: l.superDuperSlam and l.islanky, Transitions.CastleMainToGreenhouse),
        TransitionFront(Regions.TrashCan, lambda l: l.mini and l.istiny, Transitions.CastleMainToTrash),
        TransitionFront(Regions.Shed, lambda l: l.punch and l.ischunky, Transitions.CastleMainToShed),
        TransitionFront(Regions.Museum, lambda l: l.superDuperSlam and l.ischunky, Transitions.CastleMainToMuseum),
        TransitionFront(Regions.LowerCave, lambda l: True, Transitions.CastleMainToLower),
        TransitionFront(Regions.UpperCave, lambda l: True, Transitions.CastleMainToUpper),
        TransitionFront(Regions.CrankyCastle, lambda l: True),
        TransitionFront(Regions.Snide, lambda l: True),
        TransitionFront(Regions.CastleBossLobby, lambda l: not l.settings.tns_location_rando),
        TransitionFront(Regions.CastleBaboonBlast, lambda l: l.blast and l.isdonkey)  # , Transitions.CastleMainToBBlast)
    ]),

    Regions.CastleBaboonBlast: Region("Castle Baboon Blast", "Castle Surroundings", Levels.CreepyCastle, False, None, [], [
        Event(Events.CastleTreeOpened, lambda l: l.isdonkey)
    ], [
        TransitionFront(Regions.CreepyCastleMedals, lambda l: True),
        TransitionFront(Regions.CreepyCastleMain, lambda l: True)
    ]),

    # This region just exists to facilitate the multiple exits from the upper cave
    Regions.CastleWaterfall: Region("Castle Waterfall", "Castle Surroundings", Levels.CreepyCastle, False, None, [], [], [
        TransitionFront(Regions.CreepyCastleMedals, lambda l: True),
        TransitionFront(Regions.CreepyCastleMain, lambda l: True),
        TransitionFront(Regions.UpperCave, lambda l: True, Transitions.CastleWaterfallToUpper),
    ]),

    Regions.CastleTree: Region("Castle Tree", "Castle Surroundings", Levels.CreepyCastle, False, -1, [
        LocationLogic(Locations.CastleDonkeyTree, lambda l: l.scope and l.coconut and l.isdonkey),
        LocationLogic(Locations.CastleChunkyTree, lambda l: (l.scope or l.settings.hard_shooting) and l.pineapple and l.punch and l.ischunky, MinigameType.BonusBarrel),
        LocationLogic(Locations.CastleKasplatTree, lambda l: not l.settings.kasplat_rando and l.coconut and l.isdonkey),
        LocationLogic(Locations.CastleBananaFairyTree, lambda l: l.camera and l.coconut and l.isdonkey),
    ], [], [
        TransitionFront(Regions.CreepyCastleMedals, lambda l: True),
        TransitionFront(Regions.CreepyCastleMain, lambda l: True, Transitions.CastleTreeToMain),
        # This doesn't always require swim, but if you ever get the GB it does
        TransitionFront(Regions.CreepyCastleMain, lambda l: l.coconut and l.isdonkey and l.swim, Transitions.CastleTreeDrainToMain),
    ]),

    Regions.Library: Region("Library", "Castle Rooms", Levels.CreepyCastle, False, -1, [
        LocationLogic(Locations.CastleDonkeyLibrary, lambda l: l.superDuperSlam and l.isdonkey and l.strongKong),
    ], [], [
        TransitionFront(Regions.CreepyCastleMedals, lambda l: True),
        TransitionFront(Regions.CreepyCastleMain, lambda l: True, Transitions.CastleLibraryStartToMain),
        TransitionFront(Regions.CreepyCastleMain, lambda l: l.superDuperSlam and l.isdonkey and l.strongKong, Transitions.CastleLibraryEndToMain),
    ]),

    Regions.Ballroom: Region("Ballroom", "Castle Rooms", Levels.CreepyCastle, False, -1, [
        LocationLogic(Locations.CastleDiddyBallroom, lambda l: l.jetpack and l.isdiddy, MinigameType.BonusBarrel),
    ], [], [
        TransitionFront(Regions.CreepyCastleMedals, lambda l: True),
        TransitionFront(Regions.CreepyCastleMain, lambda l: True, Transitions.CastleBallroomToMain),
        TransitionFront(Regions.MuseumBehindGlass, lambda l: l.monkeyport and l.istiny, Transitions.CastleBallroomToMuseum),
    ]),

    Regions.MuseumBehindGlass: Region("Museum Behind Glass", "Castle Rooms", Levels.CreepyCastle, False, -1, [
        LocationLogic(Locations.CastleBananaFairyBallroom, lambda l: l.camera),
    ], [], [
        TransitionFront(Regions.CreepyCastleMedals, lambda l: True),
        TransitionFront(Regions.Ballroom, lambda l: l.monkeyport and l.istiny, Transitions.CastleMuseumToBallroom),
        TransitionFront(Regions.CastleTinyRace, lambda l: l.mini and l.istiny, Transitions.CastleMuseumToCarRace),
    ]),

    Regions.CastleTinyRace: Region("Castle Tiny Race", "Castle Rooms", Levels.CreepyCastle, False, None, [
        LocationLogic(Locations.CastleTinyCarRace, lambda l: l.istiny or l.settings.free_trade_items),
    ], [], [
        TransitionFront(Regions.CreepyCastleMedals, lambda l: True),
        TransitionFront(Regions.MuseumBehindGlass, lambda l: True, Transitions.CastleRaceToMuseum)
    ], Transitions.CastleMuseumToCarRace
    ),

    Regions.Tower: Region("Tower", "Castle Rooms", Levels.CreepyCastle, False, -1, [
        LocationLogic(Locations.CastleLankyTower, lambda l: (l.scope or l.homing) and l.balloon and l.grape and l.islanky, MinigameType.BonusBarrel),
    ], [], [
        TransitionFront(Regions.CreepyCastleMedals, lambda l: True),
        TransitionFront(Regions.CreepyCastleMain, lambda l: True, Transitions.CastleTowerToMain),
    ]),

    Regions.Greenhouse: Region("Greenhouse", "Castle Surroundings", Levels.CreepyCastle, False, -1, [
        # Sprint is not actually required
        LocationLogic(Locations.CastleLankyGreenhouse, lambda l: l.islanky or l.settings.free_trade_items),
        LocationLogic(Locations.CastleBattleArena, lambda l: not l.settings.crown_placement_rando and (l.islanky or l.settings.free_trade_items)),
    ], [], [
        TransitionFront(Regions.CreepyCastleMedals, lambda l: True),
        TransitionFront(Regions.CreepyCastleMain, lambda l: True, Transitions.CastleGreenhouseStartToMain),
        TransitionFront(Regions.CreepyCastleMain, lambda l: l.islanky or l.settings.free_trade_items, Transitions.CastleGreenhouseEndToMain),
    ]),

    Regions.TrashCan: Region("Trash Can", "Castle Surroundings", Levels.CreepyCastle, False, -1, [
        LocationLogic(Locations.CastleTinyTrashCan, lambda l: (l.istiny and (l.saxophone or (l.feather and (l.homing or l.settings.hard_shooting)))) or (l.settings.free_trade_items and (l.HasInstrument(Kongs.any) or (l.HasGun(Kongs.any) and (l.homing or l.settings.hard_shooting))))),
    ], [], [
        TransitionFront(Regions.CreepyCastleMedals, lambda l: True),
        TransitionFront(Regions.CreepyCastleMain, lambda l: True, Transitions.CastleTrashToMain),
    ]),

    Regions.Shed: Region("Shed", "Castle Surroundings", Levels.CreepyCastle, False, None, [
        LocationLogic(Locations.CastleChunkyShed, lambda l: l.punch and ((l.gorillaGone and l.pineapple) or l.triangle) and l.ischunky),
    ], [], [
        TransitionFront(Regions.CreepyCastleMedals, lambda l: True),
        TransitionFront(Regions.CreepyCastleMain, lambda l: True, Transitions.CastleShedToMain),
    ]),

    Regions.Museum: Region("Museum", "Castle Rooms", Levels.CreepyCastle, False, -1, [
        LocationLogic(Locations.CastleChunkyMuseum, lambda l: l.punch and l.ischunky and l.barrels),
    ], [], [
        TransitionFront(Regions.CreepyCastleMedals, lambda l: True),
        TransitionFront(Regions.CreepyCastleMain, lambda l: True, Transitions.CastleMuseumToMain),
    ]),

    Regions.LowerCave: Region("Lower Cave", "Castle Underground", Levels.CreepyCastle, True, -1, [
        LocationLogic(Locations.CastleKasplatCrypt, lambda l: not l.settings.kasplat_rando),
    ], [], [
        TransitionFront(Regions.CreepyCastleMedals, lambda l: True),
        TransitionFront(Regions.CreepyCastleMain, lambda l: True, Transitions.CastleLowerToMain),
        TransitionFront(Regions.Crypt, lambda l: (l.coconut and l.isdonkey) or (l.peanut and l.isdiddy) or (l.pineapple and l.ischunky), Transitions.CastleLowerToCrypt),
        TransitionFront(Regions.Mausoleum, lambda l: (l.grape and l.islanky) or (l.feather and l.istiny), Transitions.CastleLowerToMausoleum),
        TransitionFront(Regions.FunkyCastle, lambda l: True),
        TransitionFront(Regions.CastleBossLobby, lambda l: not l.settings.tns_location_rando),
    ]),

    Regions.Crypt: Region("Crypt", "Castle Underground", Levels.CreepyCastle, False, -1, [
        LocationLogic(Locations.CastleDiddyCrypt, lambda l: l.peanut and l.charge and l.isdiddy),
        LocationLogic(Locations.CastleChunkyCrypt, lambda l: l.pineapple and l.punch and l.ischunky, MinigameType.BonusBarrel),
    ], [], [
        TransitionFront(Regions.CreepyCastleMedals, lambda l: True),
        TransitionFront(Regions.LowerCave, lambda l: True, Transitions.CastleCryptToLower),
        TransitionFront(Regions.CastleMinecarts, lambda l: l.coconut and l.grab and l.isdonkey, Transitions.CastleCryptToCarts),
    ]),

    Regions.CastleMinecarts: Region("Castle Minecarts", "Castle Underground", Levels.CreepyCastle, False, None, [
        LocationLogic(Locations.CastleDonkeyMinecarts, lambda l: l.isdonkey or l.settings.free_trade_items),
    ], [], [
        TransitionFront(Regions.CreepyCastleMedals, lambda l: True),
        TransitionFront(Regions.Crypt, lambda l: True, Transitions.CastleCartsToCrypt),
    ], Transitions.CastleCryptToCarts
    ),

    Regions.Mausoleum: Region("Mausoleum", "Castle Underground", Levels.CreepyCastle, False, None, [
        LocationLogic(Locations.CastleLankyMausoleum, lambda l: l.grape and l.sprint and l.trombone and l.vines and l.islanky),
        LocationLogic(Locations.CastleTinyMausoleum, lambda l: l.superDuperSlam and l.twirl and l.istiny),
    ], [], [
        TransitionFront(Regions.CreepyCastleMedals, lambda l: True),
        TransitionFront(Regions.LowerCave, lambda l: True, Transitions.CastleMausoleumToLower),
    ]),

    Regions.UpperCave: Region("Upper Cave", "Castle Underground", Levels.CreepyCastle, True, -1, [
        LocationLogic(Locations.CastleTinyOverChasm, lambda l: l.twirl and l.istiny, MinigameType.BonusBarrel),
        LocationLogic(Locations.CastleKasplatNearCandy, lambda l: not l.settings.kasplat_rando),
    ], [], [
        TransitionFront(Regions.CreepyCastleMedals, lambda l: True),
        TransitionFront(Regions.CreepyCastleMain, lambda l: True, Transitions.CastleUpperToMain),
        TransitionFront(Regions.CastleWaterfall, lambda l: True, Transitions.CastleUpperToWaterfall),
        TransitionFront(Regions.Dungeon, lambda l: True, Transitions.CastleUpperToDungeon),
        TransitionFront(Regions.CandyCastle, lambda l: True),
        TransitionFront(Regions.CastleBossLobby, lambda l: not l.settings.tns_location_rando),
    ]),

    Regions.Dungeon: Region("Dungeon", "Castle Underground", Levels.CreepyCastle, True, None, [
        LocationLogic(Locations.CastleDonkeyDungeon, lambda l: l.superDuperSlam and l.donkey),
        LocationLogic(Locations.CastleDiddyDungeon, lambda l: l.superDuperSlam and l.scope and l.peanut and l.diddy and l.vines),
        LocationLogic(Locations.CastleLankyDungeon, lambda l: l.superDuperSlam and l.trombone and l.balloon and l.islanky, MinigameType.BonusBarrel),
    ], [], [
        TransitionFront(Regions.CreepyCastleMedals, lambda l: True),
        TransitionFront(Regions.UpperCave, lambda l: True, Transitions.CastleDungeonToUpper),
    ]),

    Regions.CastleBossLobby: Region("Castle Boss Lobby", "Troff 'N' Scoff", Levels.CreepyCastle, True, None, [], [], [
        TransitionFront(Regions.CastleBoss, lambda l: l.IsBossReachable(Levels.CreepyCastle)),
    ]),

    Regions.CastleBoss: Region("Castle Boss", "Troff 'N' Scoff", Levels.CreepyCastle, False, None, [
        LocationLogic(Locations.CastleKey, lambda l: l.IsBossBeatable(Levels.CreepyCastle)),
    ], [], []),
}
