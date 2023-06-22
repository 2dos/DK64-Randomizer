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
    ], [], [], restart=-1),

    Regions.CrystalCavesMain: Region("Crystal Caves Main", "Main Caves Area", Levels.CrystalCaves, True, None, [
        LocationLogic(Locations.CavesDiddyJetpackBarrel, lambda l: ((l.jetpack and l.isdiddy) or ((not l.settings.shuffle_shops) and l.advanced_platforming and ((l.isdonkey and l.settings.krusha_kong != Kongs.donkey) or (l.istiny and l.twirl)) and l.settings.free_trade_items)), MinigameType.BonusBarrel),
        LocationLogic(Locations.CavesChunkyGorillaGone, lambda l: (l.punch or l.phasewalk or l.CanPhaseswim()) and l.gorillaGone and l.ischunky),
        LocationLogic(Locations.CavesKasplatNearLab, lambda l: not l.settings.kasplat_rando),
    ], [
        Event(Events.CavesEntered, lambda l: True),
        Event(Events.CavesSmallBoulderButton, lambda l: l.ischunky and l.barrels),
        Event(Events.CavesW1aTagged, lambda l: True),
        Event(Events.CavesW2aTagged, lambda l: True),
    ], [
        TransitionFront(Regions.CrystalCavesMedals, lambda l: True),
        TransitionFront(Regions.CrystalCavesLobby, lambda l: True, Transitions.CavesToIsles),
        TransitionFront(Regions.CavesBlueprintCave, lambda l: (l.mini and l.twirl and l.tiny) or l.phasewalk or l.CanSkew(True)),
        TransitionFront(Regions.CavesBonusCave, lambda l: (l.mini and l.istiny) or l.phasewalk or l.CanSkew(True)),
        TransitionFront(Regions.CavesBlueprintPillar, lambda l: (l.jetpack and l.diddy) or (l.advanced_platforming and l.balloon and l.lanky)),
        TransitionFront(Regions.CavesBananaportSpire, lambda l: (l.jetpack and l.diddy) or l.advanced_platforming),
        TransitionFront(Regions.BoulderCave, lambda l: (l.punch and l.chunky) or l.CanSkew(True)),
        TransitionFront(Regions.CavesLankyRace, lambda l: (l.CanSlamSwitch(Levels.CrystalCaves, 2) and (l.balloon or l.advanced_platforming) and l.islanky) or l.phasewalk or l.CanSkew(True), Transitions.CavesMainToRace),
        TransitionFront(Regions.FrozenCastle, lambda l: (l.CanSlamSwitch(Levels.CrystalCaves, 2) and l.islanky) or l.CanSkew(True), Transitions.CavesMainToCastle),
        TransitionFront(Regions.IglooArea, lambda l: True),
        TransitionFront(Regions.CabinArea, lambda l: True),
        TransitionFront(Regions.FunkyCaves, lambda l: True),
        TransitionFront(Regions.CrankyCaves, lambda l: True),
        TransitionFront(Regions.CavesSnideArea, lambda l: (l.punch and l.chunky) or l.phasewalk or l.CanPhaseswim()),
        TransitionFront(Regions.CavesBossLobby, lambda l: not l.settings.tns_location_rando and ((l.punch and l.chunky) or l.phasewalk or l.CanPhaseswim())),
        TransitionFront(Regions.CavesBaboonBlast, lambda l: l.blast and l.isdonkey)  # , Transitions.CavesMainToBBlast)
    ]),

    Regions.CavesSnideArea: Region("Caves Snide Area", "Main Caves Area", Levels.CrystalCaves, False, None, [], [], [
        TransitionFront(Regions.CrystalCavesMedals, lambda l: True),
        TransitionFront(Regions.Snide, lambda l: True),
        TransitionFront(Regions.CavesBossLobby, lambda l: not l.settings.tns_location_rando),
    ]),

    Regions.CavesBlueprintCave: Region("Caves Blueprint Cave", "Main Caves Area", Levels.CrystalCaves, False, None, [
        LocationLogic(Locations.CavesKasplatNearFunky, lambda l: not l.settings.kasplat_rando),
    ], [
        Event(Events.CavesMonkeyportAccess, lambda l: l.istiny and l.monkeyport),
        Event(Events.CavesW4bTagged, lambda l: True),
    ], [
        TransitionFront(Regions.CrystalCavesMedals, lambda l: True),
        TransitionFront(Regions.CrystalCavesMain, lambda l: (l.mini and l.istiny) or l.phasewalk or l.CanSkew(True))
    ]),

    Regions.CavesBonusCave: Region("Caves Bonus Cave", "Main Caves Area", Levels.CrystalCaves, False, None, [
        LocationLogic(Locations.CavesTinyCaveBarrel, lambda l: l.istiny or l.settings.free_trade_items, MinigameType.BonusBarrel),
    ], [
        Event(Events.CavesW3bTagged, lambda l: Locations.CavesTinyCaveBarrel in l.SpecialLocationsReached),
    ], [
        TransitionFront(Regions.CrystalCavesMedals, lambda l: True),
        TransitionFront(Regions.CrystalCavesMain, lambda l: (l.mini and l.istiny) or l.phasewalk or l.CanSkew(True))
    ]),

    Regions.CavesBlueprintPillar: Region("Caves Blueprint Pillar", "Main Caves Area", Levels.CrystalCaves, False, None, [
        LocationLogic(Locations.CavesKasplatPillar, lambda l: not l.settings.kasplat_rando),
    ], [
        Event(Events.CavesW5aTagged, lambda l: True),
    ], [
        TransitionFront(Regions.CrystalCavesMedals, lambda l: True),
        TransitionFront(Regions.CrystalCavesMain, lambda l: True),
    ]),

    Regions.CavesBananaportSpire: Region("Caves Bananaport Spire", "Main Caves Area", Levels.CrystalCaves, False, None, [], [
        Event(Events.CavesW4aTagged, lambda l: True),
    ], [
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
        LocationLogic(Locations.CavesTinyMonkeyportIgloo, lambda l: ((Events.CavesMonkeyportAccess in l.Events or l.CanPhaseswim()) and l.istiny) or (l.CanPhaseswim() and l.settings.free_trade_items)),  # GB is in this region but the rest is not
        LocationLogic(Locations.CavesChunkyTransparentIgloo, lambda l: ((Events.CavesLargeBoulderButton in l.Events or l.generalclips or l.CanPhaseswim()) and l.chunky) or ((l.generalclips or l.CanPhaseswim()) and l.settings.free_trade_items)),
        LocationLogic(Locations.CavesKasplatOn5DI, lambda l: not l.settings.kasplat_rando),
    ], [
        Event(Events.CavesW1bTagged, lambda l: True),
        Event(Events.CavesW3aTagged, lambda l: True),
    ], [
        TransitionFront(Regions.CrystalCavesMedals, lambda l: True),
        TransitionFront(Regions.CrystalCavesMain, lambda l: True),
        TransitionFront(Regions.GiantKosha, lambda l: Events.CavesLargeBoulderButton in l.Events and l.monkeyport and l.istiny),
        TransitionFront(Regions.DonkeyIgloo, lambda l: ((l.settings.high_req or (l.jetpack and l.diddy)) and (l.bongos and l.isdonkey)) or l.CanPhaseswim() or l.phasewalk, Transitions.CavesIglooToDonkey),
        TransitionFront(Regions.DiddyIgloo, lambda l: ((l.settings.high_req or (l.jetpack and l.diddy)) and (l.guitar and l.isdiddy)) or l.CanPhaseswim() or l.phasewalk, Transitions.CavesIglooToDiddy),
        TransitionFront(Regions.LankyIgloo, lambda l: ((l.settings.high_req or (l.jetpack and l.diddy)) and (l.trombone and l.islanky)) or l.CanPhaseswim() or l.phasewalk, Transitions.CavesIglooToLanky),
        TransitionFront(Regions.TinyIgloo, lambda l: ((l.settings.high_req or (l.jetpack and l.diddy)) and (l.saxophone and l.istiny)) or l.CanPhaseswim() or l.phasewalk, Transitions.CavesIglooToTiny),
        TransitionFront(Regions.ChunkyIgloo, lambda l: ((l.settings.high_req or (l.jetpack and l.diddy)) and (l.triangle and l.ischunky)) or l.CanPhaseswim() or l.phasewalk, Transitions.CavesIglooToChunky),
        TransitionFront(Regions.CavesBossLobby, lambda l: not l.settings.tns_location_rando),
    ]),

    Regions.GiantKosha: Region("Giant Kosha", "Igloo Area", Levels.CrystalCaves, False, -1, [
        LocationLogic(Locations.RainbowCoin_Location10, lambda l: l.shockwave),
    ], [
        Event(Events.GiantKoshaDefeated, lambda l: l.shockwave or l.HasInstrument(Kongs.any)),
    ], [
        TransitionFront(Regions.CrystalCavesMedals, lambda l: True),
    ]),

    # Deaths in Donkey and Diddy's igloos take you back to them, the others to the beginning of the level
    Regions.DonkeyIgloo: Region("Donkey Igloo", "Igloo Area", Levels.CrystalCaves, False, None, [
        LocationLogic(Locations.CavesDonkey5DoorIgloo, lambda l: (l.strongKong and l.isdonkey) or l.CanMoonkick()),
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

    Regions.LankyIgloo: Region("Lanky Igloo", "Igloo Area", Levels.CrystalCaves, False, TransitionFront(Regions.CrystalCavesMain, lambda l: ((l.balloon or l.advanced_platforming) and l.islanky) or (l.settings.free_trade_items and l.advanced_platforming and (l.isdiddy or l.istiny))), [
        LocationLogic(Locations.CavesLanky5DoorIgloo, lambda l: ((l.balloon or l.advanced_platforming) and l.islanky) or (l.settings.free_trade_items and l.advanced_platforming and (l.isdiddy or l.istiny))),
    ], [], [
        TransitionFront(Regions.CrystalCavesMedals, lambda l: True),
        TransitionFront(Regions.IglooArea, lambda l: True, Transitions.CavesLankyToIgloo),
    ]),

    Regions.TinyIgloo: Region("Tiny Igloo", "Igloo Area", Levels.CrystalCaves, False, -1, [
        LocationLogic(Locations.CavesTiny5DoorIgloo, lambda l: l.Slam and l.istiny),
        LocationLogic(Locations.CavesBananaFairyIgloo, lambda l: l.Slam and l.istiny and l.camera),
    ], [], [
        TransitionFront(Regions.CrystalCavesMedals, lambda l: True),
        TransitionFront(Regions.IglooArea, lambda l: True, Transitions.CavesTinyToIgloo),
    ]),

    Regions.ChunkyIgloo: Region("Chunky Igloo", "Igloo Area", Levels.CrystalCaves, False, None, [
        LocationLogic(Locations.CavesChunky5DoorIgloo, lambda l: l.ischunky or l.settings.free_trade_items),
    ], [], [
        TransitionFront(Regions.CrystalCavesMedals, lambda l: True),
        TransitionFront(Regions.IglooArea, lambda l: True, Transitions.CavesChunkyToIgloo),
    ]),

    Regions.CabinArea: Region("Cabin Area", "Cabins Area", Levels.CrystalCaves, True, None, [
        LocationLogic(Locations.CavesKasplatNearCandy, lambda l: not l.settings.kasplat_rando),
    ], [
        Event(Events.CavesW2bTagged, lambda l: True),
        Event(Events.CavesW5bTagged, lambda l: True),
    ], [
        TransitionFront(Regions.CrystalCavesMedals, lambda l: True),
        TransitionFront(Regions.CrystalCavesMain, lambda l: True),
        TransitionFront(Regions.RotatingCabin, lambda l: (l.bongos and l.isdonkey) or l.phasewalk or l.CanSkew(True), Transitions.CavesCabinToRotating),
        TransitionFront(Regions.DonkeyCabin, lambda l: (l.bongos and l.isdonkey) or l.phasewalk or l.CanSkew(True) or l.generalclips, Transitions.CavesCabinToDonkey),
        TransitionFront(Regions.DiddyLowerCabin, lambda l: (l.guitar and l.isdiddy) or l.phasewalk or l.CanSkew(True), Transitions.CavesCabinToDiddyLower),
        TransitionFront(Regions.DiddyUpperCabin, lambda l: (l.guitar and l.isdiddy) or l.phasewalk or l.CanSkew(True), Transitions.CavesCabinToDiddyUpper),
        TransitionFront(Regions.LankyCabin, lambda l: (l.trombone and l.balloon and l.islanky) or l.phasewalk or l.CanSkew(True), Transitions.CavesCabinToLanky),
        TransitionFront(Regions.TinyCabin, lambda l: (l.saxophone and l.istiny) or l.phasewalk or l.CanSkew(True), Transitions.CavesCabinToTiny),
        TransitionFront(Regions.ChunkyCabin, lambda l: (l.triangle and l.ischunky) or l.phasewalk or l.CanSkew(True), Transitions.CavesCabinToChunky),
        TransitionFront(Regions.CandyCaves, lambda l: True),
        TransitionFront(Regions.CavesBossLobby, lambda l: not l.settings.tns_location_rando and ((l.jetpack and l.isdiddy) or (l.balloon or l.islanky) or l.CanMoonkick() or ((l.isdiddy or l.istiny or l.islanky) and l.advanced_platforming) or l.phasewalk)),
    ]),

    Regions.RotatingCabin: Region("Rotating Cabin", "Cabins Area", Levels.CrystalCaves, False, None, [
        LocationLogic(Locations.CavesDonkeyRotatingCabin, lambda l: (l.Slam and l.isdonkey) or l.CanMoonkick()),
        LocationLogic(Locations.CavesBattleArena, lambda l: not l.settings.crown_placement_rando and l.Slam and l.isdonkey),
    ], [], [
        TransitionFront(Regions.CrystalCavesMedals, lambda l: True),
        TransitionFront(Regions.CabinArea, lambda l: True, Transitions.CavesRotatingToCabin),
    ]),

    # Lanky's and Diddy's cabins take you to the beginning of the level, others respawn there
    Regions.DonkeyCabin: Region("Donkey Cabin", "Cabins Area", Levels.CrystalCaves, False, None, [
        LocationLogic(Locations.CavesDonkey5DoorCabin, lambda l: (l.homing or l.settings.hard_shooting) and (l.HasGun(Kongs.donkey) or (l.settings.free_trade_items and l.HasGun(Kongs.any)))),
    ], [], [
        TransitionFront(Regions.CrystalCavesMedals, lambda l: True),
        TransitionFront(Regions.CabinArea, lambda l: True, Transitions.CavesDonkeyToCabin),
    ]),

    Regions.DiddyLowerCabin: Region("Diddy Lower Cabin", "Cabins Area", Levels.CrystalCaves, False, None, [
        # You're supposed to use the jetpack to get up the platforms,
        # but you can just backflip onto them
        LocationLogic(Locations.CavesDiddy5DoorCabinLower, lambda l: l.isdiddy and l.oranges),
    ], [], [
        TransitionFront(Regions.CrystalCavesMedals, lambda l: True),
        TransitionFront(Regions.CabinArea, lambda l: True, Transitions.CavesDiddyLowerToCabin),
    ]),

    Regions.DiddyUpperCabin: Region("Diddy Upper Cabin", "Cabins Area", Levels.CrystalCaves, False, None, [
        LocationLogic(Locations.CavesDiddy5DoorCabinUpper, lambda l: (l.guitar or l.oranges) and l.spring and l.jetpack and l.isdiddy),
        LocationLogic(Locations.CavesBananaFairyCabin, lambda l: l.camera and (l.guitar or l.oranges) and l.spring and l.jetpack and l.isdiddy),
    ], [], [
        TransitionFront(Regions.CrystalCavesMedals, lambda l: True),
        TransitionFront(Regions.CabinArea, lambda l: True, Transitions.CavesDiddyUpperToCabin),
    ]),

    Regions.LankyCabin: Region("Lanky Cabin", "Cabins Area", Levels.CrystalCaves, False, -1, [
        LocationLogic(Locations.CavesLanky1DoorCabin, lambda l: l.sprint and l.balloon and l.islanky),
    ], [], [
        TransitionFront(Regions.CrystalCavesMedals, lambda l: True),
        TransitionFront(Regions.CabinArea, lambda l: True, Transitions.CavesLankyToCabin),
    ]),

    Regions.TinyCabin: Region("Tiny Cabin", "Cabins Area", Levels.CrystalCaves, False, None, [
        LocationLogic(Locations.CavesTiny5DoorCabin, lambda l: (l.istiny or l.settings.free_trade_items) and l.oranges),
    ], [], [
        TransitionFront(Regions.CrystalCavesMedals, lambda l: True),
        TransitionFront(Regions.CabinArea, lambda l: True, Transitions.CavesTinyToCabin),
    ]),

    Regions.ChunkyCabin: Region("Chunky Cabin", "Cabins Area", Levels.CrystalCaves, False, None, [
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
