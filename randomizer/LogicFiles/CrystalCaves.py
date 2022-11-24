# fmt: off
"""Logic file for Crystal Caves."""

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
    Regions.CrystalCavesMedals: Region("Crystal Caves Medals", "Crystal Caves Medal Rewards", Levels.CrystalCaves, False, None, [
        LocationLogic(Locations.CavesDonkeyMedal, lambda l: l.ColoredBananas[Levels.CrystalCaves][Kongs.donkey] >= l.settings.medal_cb_req),
        LocationLogic(Locations.CavesDiddyMedal, lambda l: l.ColoredBananas[Levels.CrystalCaves][Kongs.diddy] >= l.settings.medal_cb_req),
        LocationLogic(Locations.CavesLankyMedal, lambda l: l.ColoredBananas[Levels.CrystalCaves][Kongs.lanky] >= l.settings.medal_cb_req),
        LocationLogic(Locations.CavesTinyMedal, lambda l: l.ColoredBananas[Levels.CrystalCaves][Kongs.tiny] >= l.settings.medal_cb_req),
        LocationLogic(Locations.CavesChunkyMedal, lambda l: l.ColoredBananas[Levels.CrystalCaves][Kongs.chunky] >= l.settings.medal_cb_req),
    ], [], []),

    Regions.CrystalCavesMain: Region("Crystal Caves Main", "Main Caves Area", Levels.CrystalCaves, True, None, [
        LocationLogic(Locations.CavesDiddyJetpackBarrel, lambda l: l.jetpack and l.isdiddy, MinigameType.BonusBarrel),
        LocationLogic(Locations.CavesChunkyGorillaGone, lambda l: l.punch and l.gorillaGone and l.ischunky),
        LocationLogic(Locations.CavesKasplatNearLab, lambda l: not l.settings.kasplat_rando),
        LocationLogic(Locations.CavesKasplatNearCandy, lambda l: not l.settings.kasplat_rando),
    ], [
        Event(Events.CavesEntered, lambda l: True),
        Event(Events.CavesSmallBoulderButton, lambda l: l.ischunky and l.barrels),
    ], [
        TransitionFront(Regions.CrystalCavesMedals, lambda l: True),
        TransitionFront(Regions.CrystalCavesLobby, lambda l: True, Transitions.CavesToIsles),
        TransitionFront(Regions.CavesBlueprintCave, lambda l: l.mini and l.twirl and l.tiny),
        TransitionFront(Regions.CavesBonusCave, lambda l: l.mini and l.tiny),
        TransitionFront(Regions.CavesBlueprintPillar, lambda l: l.jetpack and l.diddy),
        TransitionFront(Regions.CavesBananaportSpire, lambda l: l.jetpack and l.diddy),
        TransitionFront(Regions.BoulderCave, lambda l: l.punch and l.chunky),
        TransitionFront(Regions.CavesLankyRace, lambda l: l.superSlam and l.balloon and l.islanky, Transitions.CavesMainToRace),
        TransitionFront(Regions.FrozenCastle, lambda l: l.superSlam and l.islanky, Transitions.CavesMainToCastle),
        TransitionFront(Regions.IglooArea, lambda l: True),
        TransitionFront(Regions.CabinArea, lambda l: True),
        TransitionFront(Regions.FunkyCaves, lambda l: True),
        TransitionFront(Regions.CrankyCaves, lambda l: True),
        TransitionFront(Regions.CavesSnideArea, lambda l: l.punch and l.chunky),
        TransitionFront(Regions.CavesBossLobby, lambda l: not l.settings.tns_location_rando and l.punch),
        TransitionFront(Regions.CavesBaboonBlast, lambda l: l.blast and l.isdonkey)  # , Transitions.CavesMainToBBlast)
    ]),

    Regions.CavesSnideArea: Region("Caves Snide Area", "Main Caves Area", Levels.CrystalCaves, False, None, [], [], [
        TransitionFront(Regions.CrystalCavesMedals, lambda l: True),
        TransitionFront(Regions.Snide, lambda l: True),
        TransitionFront(Regions.CavesBossLobby, lambda l: not l.settings.tns_location_rando),
    ]),

    Regions.CavesBlueprintCave: Region("Caves Blueprint Cave", "Main Caves Area", Levels.CrystalCaves, False, None, [
        LocationLogic(Locations.CavesKasplatNearFunky, lambda l: not l.settings.kasplat_rando),
    ], [], [
        TransitionFront(Regions.CrystalCavesMedals, lambda l: True),
        TransitionFront(Regions.CrystalCavesMain, lambda l: l.mini and l.istiny)
    ]),

    Regions.CavesBonusCave: Region("Caves Bonus Cave", "Main Caves Area", Levels.CrystalCaves, False, None, [
        LocationLogic(Locations.CavesTinyCaveBarrel, lambda l: l.istiny or l.settings.free_trade_items, MinigameType.BonusBarrel),
    ], [], [
        TransitionFront(Regions.CrystalCavesMedals, lambda l: True),
        TransitionFront(Regions.CrystalCavesMain, lambda l: l.mini and l.istiny)
    ]),

    Regions.CavesBlueprintPillar: Region("Caves Blueprint Pillar", "Main Caves Area", Levels.CrystalCaves, False, None, [
        LocationLogic(Locations.CavesKasplatPillar, lambda l: not l.settings.kasplat_rando),
    ], [], [
        TransitionFront(Regions.CrystalCavesMedals, lambda l: True),
        TransitionFront(Regions.CrystalCavesMain, lambda l: True)
    ]),

    Regions.CavesBananaportSpire: Region("Caves Bananaport Spire", "Main Caves Area", Levels.CrystalCaves, False, None, [], [], [
        TransitionFront(Regions.CrystalCavesMedals, lambda l: True),
        TransitionFront(Regions.CrystalCavesMain, lambda l: True)
    ]),

    Regions.CavesBaboonBlast: Region("Caves Baboon Blast", "Main Caves Area", Levels.CrystalCaves, False, None, [
        LocationLogic(Locations.CavesDonkeyBaboonBlast, lambda l: l.isdonkey, MinigameType.BonusBarrel),
    ], [], [
        TransitionFront(Regions.CrystalCavesMedals, lambda l: True),
        TransitionFront(Regions.CrystalCavesMain, lambda l: True)
    ]),

    Regions.BoulderCave: Region("Boulder Cave", "Main Caves Area", Levels.CrystalCaves, True, None, [], [
        Event(Events.CavesLargeBoulderButton, lambda l: Events.CavesSmallBoulderButton in l.Events and l.hunkyChunky and l.chunky and l.barrels),
    ], [
        TransitionFront(Regions.CrystalCavesMedals, lambda l: True),
        TransitionFront(Regions.CrystalCavesMain, lambda l: True),
        TransitionFront(Regions.CavesBossLobby, lambda l: not l.settings.tns_location_rando),
    ]),

    Regions.CavesLankyRace: Region("Caves Lanky Race", "Main Caves Area", Levels.CrystalCaves, False, None, [
        LocationLogic(Locations.CavesLankyBeetleRace, lambda l: l.sprint and l.islanky),
    ], [], [
        TransitionFront(Regions.CrystalCavesMedals, lambda l: True),
        TransitionFront(Regions.CrystalCavesMain, lambda l: True, Transitions.CavesRaceToMain),
    ], Transitions.CavesMainToRace
    ),

    Regions.FrozenCastle: Region("Frozen Castle", "Main Caves Area", Levels.CrystalCaves, False, None, [
        LocationLogic(Locations.CavesLankyCastle, lambda l: l.Slam and (l.islanky or l.settings.free_trade_items)),
    ], [], [
        TransitionFront(Regions.CrystalCavesMedals, lambda l: True),
        TransitionFront(Regions.CrystalCavesMain, lambda l: True, Transitions.CavesCastleToMain),
    ]),

    Regions.IglooArea: Region("Igloo Area", "Igloo Area", Levels.CrystalCaves, True, None, [
        LocationLogic(Locations.CavesTinyMonkeyportIgloo, lambda l: l.monkeyport and l.mini and l.twirl and l.istiny),  # GB is in this region but the rest is not
        LocationLogic(Locations.CavesChunkyTransparentIgloo, lambda l: Events.CavesLargeBoulderButton in l.Events and l.chunky),
        LocationLogic(Locations.CavesKasplatOn5DI, lambda l: not l.settings.kasplat_rando),
    ], [], [
        TransitionFront(Regions.CrystalCavesMedals, lambda l: True),
        TransitionFront(Regions.CrystalCavesMain, lambda l: True),
        TransitionFront(Regions.GiantKosha, lambda l: Events.CavesLargeBoulderButton in l.Events and l.monkeyport and l.istiny),
        TransitionFront(Regions.DonkeyIgloo, lambda l: (l.settings.high_req or l.jetpack) and l.bongos and l.isdonkey, Transitions.CavesIglooToDonkey),
        TransitionFront(Regions.DiddyIgloo, lambda l: (l.settings.high_req or l.jetpack) and l.guitar and l.isdiddy, Transitions.CavesIglooToDiddy),
        TransitionFront(Regions.LankyIgloo, lambda l: (l.settings.high_req or l.jetpack) and l.trombone and l.islanky, Transitions.CavesIglooToLanky),
        TransitionFront(Regions.TinyIgloo, lambda l: (l.settings.high_req or l.jetpack) and l.saxophone and l.istiny, Transitions.CavesIglooToTiny),
        TransitionFront(Regions.ChunkyIgloo, lambda l: (l.settings.high_req or l.jetpack) and l.triangle and l.ischunky, Transitions.CavesIglooToChunky),
        TransitionFront(Regions.CavesBossLobby, lambda l: not l.settings.tns_location_rando),
    ]),

    Regions.GiantKosha: Region("Giant Kosha", "Igloo Area", Levels.CrystalCaves, False, -1, [], [
        Event(Events.GiantKoshaDefeated, lambda l: l.shockwave or l.HasInstrument(Kongs.any)),
    ], [
        TransitionFront(Regions.CrystalCavesMedals, lambda l: True),
    ]),

    # Deaths in Donkey and Diddy's igloos take you back to them, the others to the beginning of the level
    Regions.DonkeyIgloo: Region("Donkey Igloo", "Igloo Area", Levels.CrystalCaves, False, None, [
        LocationLogic(Locations.CavesDonkey5DoorIgloo, lambda l: l.strongKong and l.isdonkey),
    ], [], [
        TransitionFront(Regions.CrystalCavesMedals, lambda l: True),
        TransitionFront(Regions.IglooArea, lambda l: True, Transitions.CavesDonkeyToIgloo),
    ]),

    Regions.DiddyIgloo: Region("Diddy Igloo", "Igloo Area", Levels.CrystalCaves, False, None, [
        LocationLogic(Locations.CavesDiddy5DoorIgloo, lambda l: (l.isdiddy or l.settings.free_trade_items) and l.barrels),
    ], [], [
        TransitionFront(Regions.CrystalCavesMedals, lambda l: True),
        TransitionFront(Regions.IglooArea, lambda l: True, Transitions.CavesDiddyToIgloo),
    ]),

    Regions.LankyIgloo: Region("Lanky Igloo", "Igloo Area", Levels.CrystalCaves, False, -1, [
        LocationLogic(Locations.CavesLanky5DoorIgloo, lambda l: l.balloon and l.islanky),
    ], [], [
        TransitionFront(Regions.CrystalCavesMedals, lambda l: True),
        TransitionFront(Regions.IglooArea, lambda l: True, Transitions.CavesLankyToIgloo),
    ]),

    Regions.TinyIgloo: Region("Tiny Igloo", "Igloo Area", Levels.CrystalCaves, False, -1, [
        LocationLogic(Locations.CavesTiny5DoorIgloo, lambda l: l.Slam and (l.istiny or l.settings.free_trade_items)),
        LocationLogic(Locations.CavesBananaFairyIgloo, lambda l: l.Slam and (l.istiny or l.settings.free_trade_items) and l.camera),
    ], [], [
        TransitionFront(Regions.CrystalCavesMedals, lambda l: True),
        TransitionFront(Regions.IglooArea, lambda l: True, Transitions.CavesTinyToIgloo),
    ]),

    Regions.ChunkyIgloo: Region("Chunky Igloo", "Igloo Area", Levels.CrystalCaves, False, -1, [
        LocationLogic(Locations.CavesChunky5DoorIgloo, lambda l: l.ischunky or l.settings.free_trade_items),
    ], [], [
        TransitionFront(Regions.CrystalCavesMedals, lambda l: True),
        TransitionFront(Regions.IglooArea, lambda l: True, Transitions.CavesChunkyToIgloo),
    ]),

    Regions.CabinArea: Region("Cabin Area", "Caves Cabins", Levels.CrystalCaves, True, None, [], [], [
        TransitionFront(Regions.CrystalCavesMedals, lambda l: True),
        TransitionFront(Regions.CrystalCavesMain, lambda l: True),
        TransitionFront(Regions.RotatingCabin, lambda l: l.bongos and l.isdonkey, Transitions.CavesCabinToRotating),
        TransitionFront(Regions.DonkeyCabin, lambda l: l.bongos and l.isdonkey, Transitions.CavesCabinToDonkey),
        TransitionFront(Regions.DiddyLowerCabin, lambda l: l.guitar and l.isdiddy, Transitions.CavesCabinToDiddyLower),
        TransitionFront(Regions.DiddyUpperCabin, lambda l: l.guitar and l.isdiddy, Transitions.CavesCabinToDiddyUpper),
        TransitionFront(Regions.LankyCabin, lambda l: l.trombone and l.balloon and l.islanky, Transitions.CavesCabinToLanky),
        TransitionFront(Regions.TinyCabin, lambda l: l.saxophone and l.istiny, Transitions.CavesCabinToTiny),
        TransitionFront(Regions.ChunkyCabin, lambda l: l.triangle and l.ischunky, Transitions.CavesCabinToChunky),
        TransitionFront(Regions.CandyCaves, lambda l: True),
        TransitionFront(Regions.CavesBossLobby, lambda l: not l.settings.tns_location_rando and (l.jetpack or l.balloon)),
    ]),

    Regions.RotatingCabin: Region("Rotating Cabin", "Caves Cabins", Levels.CrystalCaves, False, None, [
        LocationLogic(Locations.CavesDonkeyRotatingCabin, lambda l: l.Slam and l.isdonkey),
        LocationLogic(Locations.CavesBattleArena, lambda l: not l.settings.crown_placement_rando and l.Slam and l.isdonkey),
    ], [], [
        TransitionFront(Regions.CrystalCavesMedals, lambda l: True),
        TransitionFront(Regions.CabinArea, lambda l: True, Transitions.CavesRotatingToCabin),
    ]),

    # Lanky's and Diddy's cabins take you to the beginning of the level, others respawn there
    Regions.DonkeyCabin: Region("Donkey Cabin", "Caves Cabins", Levels.CrystalCaves, False, -1, [
        LocationLogic(Locations.CavesDonkey5DoorCabin, lambda l: (l.homing or l.settings.hard_shooting) and (l.HasGun(Kongs.donkey) or (l.settings.free_trade_items and l.HasGun(Kongs.any)))),
    ], [], [
        TransitionFront(Regions.CrystalCavesMedals, lambda l: True),
        TransitionFront(Regions.CabinArea, lambda l: True, Transitions.CavesDonkeyToCabin),
    ]),

    Regions.DiddyLowerCabin: Region("Diddy Lower Cabin", "Caves Cabins", Levels.CrystalCaves, False, None, [
        # You're supposed to use the jetpack to get up the platforms,
        # but you can just backflip onto them
        LocationLogic(Locations.CavesDiddy5DoorCabinLower, lambda l: l.isdiddy and l.oranges),
    ], [], [
        TransitionFront(Regions.CrystalCavesMedals, lambda l: True),
        TransitionFront(Regions.CabinArea, lambda l: True, Transitions.CavesDiddyLowerToCabin),
    ]),

    Regions.DiddyUpperCabin: Region("Diddy Upper Cabin", "Caves Cabins", Levels.CrystalCaves, False, None, [
        LocationLogic(Locations.CavesDiddy5DoorCabinUpper, lambda l: (l.guitar or l.oranges) and l.spring and l.jetpack and l.isdiddy),
        LocationLogic(Locations.CavesBananaFairyCabin, lambda l: l.camera and (l.guitar or l.oranges) and l.spring and l.jetpack and l.isdiddy),
    ], [], [
        TransitionFront(Regions.CrystalCavesMedals, lambda l: True),
        TransitionFront(Regions.CabinArea, lambda l: True, Transitions.CavesDiddyUpperToCabin),
    ]),

    Regions.LankyCabin: Region("Lanky Cabin", "Caves Cabins", Levels.CrystalCaves, False, -1, [
        LocationLogic(Locations.CavesLanky1DoorCabin, lambda l: l.sprint and l.balloon and l.islanky),
    ], [], [
        TransitionFront(Regions.CrystalCavesMedals, lambda l: True),
        TransitionFront(Regions.CabinArea, lambda l: True, Transitions.CavesLankyToCabin),
    ]),

    Regions.TinyCabin: Region("Tiny Cabin", "Caves Cabins", Levels.CrystalCaves, False, None, [
        LocationLogic(Locations.CavesTiny5DoorCabin, lambda l: (l.istiny or l.settings.free_trade_items) and l.oranges),
    ], [], [
        TransitionFront(Regions.CrystalCavesMedals, lambda l: True),
        TransitionFront(Regions.CabinArea, lambda l: True, Transitions.CavesTinyToCabin),
    ]),

    Regions.ChunkyCabin: Region("Chunky Cabin", "Caves Cabins", Levels.CrystalCaves, False, None, [
        LocationLogic(Locations.CavesChunky5DoorCabin, lambda l: l.gorillaGone and l.Slam and l.ischunky, MinigameType.BonusBarrel),
    ], [], [
        TransitionFront(Regions.CrystalCavesMedals, lambda l: True),
        TransitionFront(Regions.CabinArea, lambda l: True, Transitions.CavesChunkyToCabin),
    ]),

    Regions.CavesBossLobby: Region("Caves Boss Lobby", "Troff 'N' Scoff", Levels.CrystalCaves, True, None, [], [], [
        TransitionFront(Regions.CavesBoss, lambda l: l.IsBossReachable(Levels.CrystalCaves)),
    ]),

    Regions.CavesBoss: Region("Caves Boss", "Troff 'N' Scoff", Levels.CrystalCaves, False, None, [
        LocationLogic(Locations.CavesKey, lambda l: l.IsBossBeatable(Levels.CrystalCaves)),
    ], [], []),
}
