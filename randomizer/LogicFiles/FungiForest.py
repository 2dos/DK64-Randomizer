# fmt: off
"""Logic file for Fungi Forest."""

from randomizer.Enums.Events import Events
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.MinigameType import MinigameType
from randomizer.Enums.Regions import Regions
from randomizer.Enums.Time import Time
from randomizer.Enums.Transitions import Transitions
from randomizer.LogicClasses import (Event, LocationLogic, Region,
                                     TransitionFront)

LogicRegions = {
    Regions.FungiForestMedals: Region("Fungi Forest Medals", "Fungi Forest Medal Rewards", Levels.FungiForest, False, None, [
        LocationLogic(Locations.ForestDonkeyMedal, lambda l: l.ColoredBananas[Levels.FungiForest][Kongs.donkey] >= l.settings.medal_cb_req),
        LocationLogic(Locations.ForestDiddyMedal, lambda l: l.ColoredBananas[Levels.FungiForest][Kongs.diddy] >= l.settings.medal_cb_req),
        LocationLogic(Locations.ForestLankyMedal, lambda l: l.ColoredBananas[Levels.FungiForest][Kongs.lanky] >= l.settings.medal_cb_req),
        LocationLogic(Locations.ForestTinyMedal, lambda l: l.ColoredBananas[Levels.FungiForest][Kongs.tiny] >= l.settings.medal_cb_req),
        LocationLogic(Locations.ForestChunkyMedal, lambda l: l.ColoredBananas[Levels.FungiForest][Kongs.chunky] >= l.settings.medal_cb_req),
    ], [], [], restart=-1),

    Regions.FungiForestStart: Region("Fungi Forest Start", "Forest Center and Beanstalk", Levels.FungiForest, True, None, [], [
        Event(Events.ForestEntered, lambda l: True),
        Event(Events.Night, lambda l: l.HasGun(Kongs.any)),
        Event(Events.WormGatesOpened, lambda l: l.settings.open_levels or (l.feather and l.tiny and l.pineapple and l.chunky)),
        Event(Events.ForestW1aTagged, lambda l: True),
        Event(Events.ForestW2aTagged, lambda l: True),
        Event(Events.ForestW3aTagged, lambda l: True),
        Event(Events.ForestW4aTagged, lambda l: True),
    ], [
        TransitionFront(Regions.FungiForestMedals, lambda l: True),
        TransitionFront(Regions.FungiForestLobby, lambda l: True, Transitions.ForestToIsles),
        TransitionFront(Regions.ForestMinecarts, lambda l: l.Slam and l.ischunky),
        TransitionFront(Regions.GiantMushroomArea, lambda l: True),
        TransitionFront(Regions.MillArea, lambda l: True),
        TransitionFront(Regions.WormArea, lambda l: Events.WormGatesOpened in l.Events or l.phasewalk or l.CanPhaseswim()),
    ]),

    Regions.ForestMinecarts: Region("Forest Minecarts", "Forest Center and Beanstalk", Levels.FungiForest, False, None, [
        LocationLogic(Locations.ForestChunkyMinecarts, lambda l: l.ischunky or l.settings.free_trade_items),
    ], [], [
        TransitionFront(Regions.FungiForestStart, lambda l: True),
    ], Transitions.ForestMainToCarts
    ),

    Regions.GiantMushroomArea: Region("Giant Mushroom Area", "Giant Mushroom Exterior", Levels.FungiForest, True, None, [
        LocationLogic(Locations.ForestDiddyTopofMushroom, lambda l: l.jetpack and l.isdiddy, MinigameType.BonusBarrel),
        LocationLogic(Locations.ForestLankyRabbitRace, lambda l: (l.CanOStandTBSNoclip() and l.spawn_snags), isAuxiliary=True),
    ], [
        Event(Events.HollowTreeGateOpened, lambda l: l.grape and l.lanky),
        Event(Events.ForestW3bTagged, lambda l: True),
        Event(Events.ForestW5bTagged, lambda l: True),
    ], [
        TransitionFront(Regions.FungiForestMedals, lambda l: True),
        TransitionFront(Regions.FungiForestStart, lambda l: True),
        TransitionFront(Regions.MushroomLower, lambda l: True, Transitions.ForestMainToLowerMushroom),
        TransitionFront(Regions.MushroomLowerExterior, lambda l: (l.jetpack and l.isdiddy) or (l.advanced_platforming and l.twirl and l.istiny)),
        TransitionFront(Regions.MushroomUpperExterior, lambda l: l.jetpack and l.isdiddy),
        TransitionFront(Regions.HollowTreeArea, lambda l: l.settings.open_levels or Events.HollowTreeGateOpened in l.Events or l.CanPhaseswim() or l.phasewalk or l.CanOStandTBSNoclip()),
        TransitionFront(Regions.Anthill, lambda l: l.CanSkew(True), Transitions.ForestTreeToAnthill),
        TransitionFront(Regions.CrankyForest, lambda l: True),
    ]),

    Regions.MushroomLower: Region("Mushroom Lower", "Giant Mushroom Insides", Levels.FungiForest, True, -1, [
        LocationLogic(Locations.ForestTinyMushroomBarrel, lambda l: l.CanSlamSwitch(Levels.FungiForest, 2) and l.istiny, MinigameType.BonusBarrel),
    ], [
        Event(Events.MushroomCannonsSpawned, lambda l: l.coconut and l.peanut and l.grape and l.feather and l.pineapple
              and l.donkey and l.diddy and l.lanky and l.tiny and l.chunky),
        Event(Events.DonkeyMushroomSwitch, lambda l: l.CanSlamSwitch(Levels.FungiForest, 2) and l.donkey)
    ], [
        TransitionFront(Regions.FungiForestMedals, lambda l: True),
        TransitionFront(Regions.GiantMushroomArea, lambda l: True, Transitions.ForestLowerMushroomToMain),
        TransitionFront(Regions.MushroomLowerExterior, lambda l: True, Transitions.ForestLowerMushroomToLowerExterior),
        TransitionFront(Regions.MushroomUpper, lambda l: Events.MushroomCannonsSpawned in l.Events),
    ]),

    Regions.MushroomLowerExterior: Region("Mushroom Lower Exterior", "Giant Mushroom Exterior", Levels.FungiForest, True, None, [
        LocationLogic(Locations.ForestKasplatLowerMushroomExterior, lambda l: not l.settings.kasplat_rando),
    ], [], [
        TransitionFront(Regions.FungiForestMedals, lambda l: True),
        TransitionFront(Regions.GiantMushroomArea, lambda l: True),
        TransitionFront(Regions.MushroomLower, lambda l: True, Transitions.ForestLowerExteriorToLowerMushroom),
        TransitionFront(Regions.MushroomUpper, lambda l: True, Transitions.ForestLowerExteriorToUpperMushroom),
        TransitionFront(Regions.ForestBaboonBlast, lambda l: l.blast and l.isdonkey)  # , Transitions.ForestMainToBBlast)
    ]),

    Regions.ForestBaboonBlast: Region("Forest Baboon Blast", "Giant Mushroom Exterior", Levels.FungiForest, False, None, [
        LocationLogic(Locations.ForestDonkeyBaboonBlast, lambda l: l.isdonkey, MinigameType.BonusBarrel),
    ], [], [
        TransitionFront(Regions.FungiForestMedals, lambda l: True),
        TransitionFront(Regions.MushroomLowerExterior, lambda l: True)
    ]),

    Regions.MushroomUpper: Region("Mushroom Upper", "Giant Mushroom Insides", Levels.FungiForest, True, -1, [
        LocationLogic(Locations.ForestDonkeyMushroomCannons, lambda l: Events.MushroomCannonsSpawned in l.Events and Events.DonkeyMushroomSwitch in l.Events),
        LocationLogic(Locations.ForestKasplatInsideMushroom, lambda l: not l.settings.kasplat_rando),
    ], [], [
        TransitionFront(Regions.FungiForestMedals, lambda l: True),
        TransitionFront(Regions.MushroomLower, lambda l: True),
        TransitionFront(Regions.MushroomLowerExterior, lambda l: True, Transitions.ForestUpperMushroomToLowerExterior),
        TransitionFront(Regions.MushroomUpperExterior, lambda l: True, Transitions.ForestUpperMushroomToUpperExterior),
        TransitionFront(Regions.MushroomNightDoor, lambda l: l.vines),
    ]),

    # This region basically just exists to facilitate the two entrances into upper mushroom
    Regions.MushroomNightDoor: Region("Mushroom Night Door", "Giant Mushroom Insides", Levels.FungiForest, False, None, [], [], [
        TransitionFront(Regions.FungiForestMedals, lambda l: True),
        TransitionFront(Regions.MushroomUpper, lambda l: True),
        TransitionFront(Regions.MushroomNightExterior, lambda l: True, Transitions.ForestNightToExterior, time=Time.Night),
    ]),

    Regions.MushroomNightExterior: Region("Mushroom Night Exterior", "Giant Mushroom Exterior", Levels.FungiForest, False, None, [
        LocationLogic(Locations.ForestKasplatUpperMushroomExterior, lambda l: not l.settings.kasplat_rando),
    ], [], [
        TransitionFront(Regions.FungiForestMedals, lambda l: True),
        TransitionFront(Regions.MushroomNightDoor, lambda l: True, Transitions.ForestExteriorToNight, time=Time.Night),
        TransitionFront(Regions.GiantMushroomArea, lambda l: True),
    ]),

    Regions.MushroomUpperExterior: Region("Mushroom Upper Exterior", "Giant Mushroom Exterior", Levels.FungiForest, True, -1, [
        LocationLogic(Locations.ForestBattleArena, lambda l: not l.settings.crown_placement_rando),
    ], [
        Event(Events.ForestW5aTagged, lambda l: True),
    ], [
        TransitionFront(Regions.FungiForestMedals, lambda l: True),
        TransitionFront(Regions.MushroomUpper, lambda l: True, Transitions.ForestUpperExteriorToUpperMushroom),
        TransitionFront(Regions.MushroomNightExterior, lambda l: True),
        TransitionFront(Regions.GiantMushroomArea, lambda l: True),
        TransitionFront(Regions.MushroomChunkyRoom, lambda l: (l.CanSlamSwitch(Levels.FungiForest, 2) and l.ischunky) or l.phasewalk or l.CanOStandTBSNoclip(), Transitions.ForestExteriorToChunky),
        TransitionFront(Regions.MushroomLankyZingersRoom, lambda l: (l.handstand and l.CanSlamSwitch(Levels.FungiForest, 2) and l.islanky) or l.CanOStandTBSNoclip(), Transitions.ForestExteriorToZingers),
        TransitionFront(Regions.MushroomLankyMushroomsRoom, lambda l: (l.handstand and l.CanSlamSwitch(Levels.FungiForest, 2) and l.islanky) or l.phasewalk or l.CanOStandTBSNoclip(), Transitions.ForestExteriorToMushrooms),
        TransitionFront(Regions.ForestBossLobby, lambda l: not l.settings.tns_location_rando),
    ]),

    Regions.MushroomChunkyRoom: Region("Mushroom Chunky Room", "Giant Mushroom Insides", Levels.FungiForest, False, -1, [
        LocationLogic(Locations.ForestChunkyFacePuzzle, lambda l: l.pineapple and l.CanSlamSwitch(Levels.FungiForest, 2) and l.ischunky),
    ], [], [
        TransitionFront(Regions.FungiForestMedals, lambda l: True),
        TransitionFront(Regions.MushroomUpperExterior, lambda l: True, Transitions.ForestChunkyToExterior),
    ]),

    Regions.MushroomLankyZingersRoom: Region("Mushroom Lanky Zingers Room", "Giant Mushroom Insides", Levels.FungiForest, False, -1, [
        LocationLogic(Locations.ForestLankyZingers, lambda l: l.islanky or l.settings.free_trade_items),
    ], [], [
        TransitionFront(Regions.FungiForestMedals, lambda l: True),
        TransitionFront(Regions.MushroomUpperExterior, lambda l: True, Transitions.ForestZingersToExterior),
    ]),

    Regions.MushroomLankyMushroomsRoom: Region("Mushroom Lanky Mushrooms Room", "Giant Mushroom Insides", Levels.FungiForest, False, None, [
        LocationLogic(Locations.ForestLankyColoredMushrooms, lambda l: l.Slam and (l.islanky or l.settings.free_trade_items), MinigameType.BonusBarrel),
    ], [], [
        TransitionFront(Regions.FungiForestMedals, lambda l: True),
        TransitionFront(Regions.MushroomUpperExterior, lambda l: True, Transitions.ForestMushroomsToExterior),
    ]),

    Regions.HollowTreeArea: Region("Hollow Tree Area", "Owl Tree", Levels.FungiForest, True, -1, [
        LocationLogic(Locations.ForestDiddyOwlRace, lambda l: l.TimeAccess(Regions.HollowTreeArea, Time.Night) and l.jetpack and l.guitar and l.isdiddy, MinigameType.BonusBarrel),
        LocationLogic(Locations.ForestLankyRabbitRace, lambda l: l.TimeAccess(Regions.HollowTreeArea, Time.Day) and l.trombone and l.sprint and l.lanky),
        LocationLogic(Locations.ForestKasplatOwlTree, lambda l: not l.settings.kasplat_rando),
    ], [
        Event(Events.ForestW4bTagged, lambda l: True),
    ], [
        TransitionFront(Regions.FungiForestMedals, lambda l: True),
        TransitionFront(Regions.GiantMushroomArea, lambda l: l.settings.open_levels or Events.HollowTreeGateOpened in l.Events or l.phasewalk),
        TransitionFront(Regions.Anthill, lambda l: l.mini and l.saxophone and l.istiny, Transitions.ForestTreeToAnthill),
        TransitionFront(Regions.ForestBossLobby, lambda l: not l.settings.tns_location_rando),
    ]),

    Regions.Anthill: Region("Anthill", "Owl Tree", Levels.FungiForest, False, -1, [
        LocationLogic(Locations.ForestTinyAnthill, lambda l: (l.istiny or l.settings.free_trade_items) and (l.oranges or l.saxophone or (l.settings.free_trade_items and l.HasInstrument(Kongs.any)))),
        LocationLogic(Locations.ForestBean, lambda l: (l.istiny or l.settings.free_trade_items) and (l.oranges or l.saxophone or (l.settings.free_trade_items and l.HasInstrument(Kongs.any)))),
    ], [], [
        TransitionFront(Regions.FungiForestMedals, lambda l: True),
        TransitionFront(Regions.HollowTreeArea, lambda l: (l.istiny or l.settings.free_trade_items) and (l.oranges or l.saxophone or (l.settings.free_trade_items and l.HasInstrument(Kongs.any))), Transitions.ForestAnthillToTree),
    ]),

    Regions.MillArea: Region("Mill Area", "Forest Mills", Levels.FungiForest, True, None, [
        LocationLogic(Locations.ForestDonkeyMill, lambda l: (l.TimeAccess(Regions.MillArea, Time.Night) or l.phasewalk or l.CanPhaseswim() or l.ledgeclip) and Events.ConveyorActivated in l.Events and l.donkey),
        LocationLogic(Locations.ForestDiddyCagedBanana, lambda l: (l.TimeAccess(Regions.MillArea, Time.Night) and Events.WinchRaised in l.Events and l.guitar and l.diddy) or ((l.CanPhaseswim() or l.ledgeclip) and (l.isdiddy or l.settings.free_trade_items))),
        LocationLogic(Locations.RainbowCoin_Location07, lambda l: l.shockwave),
    ], [
        Event(Events.ForestW1bTagged, lambda l: True),
    ], [
        TransitionFront(Regions.FungiForestMedals, lambda l: True),
        TransitionFront(Regions.FungiForestStart, lambda l: True),
        TransitionFront(Regions.MillChunkyTinyArea, lambda l: (l.punch and l.ischunky) or l.phasewalk or l.CanPhaseswim() or l.ledgeclip, Transitions.ForestMainToChunkyMill, time=Time.Day),
        TransitionFront(Regions.MillChunkyTinyArea, lambda l: (Events.MillBoxBroken in l.Events and l.mini and l.istiny) or l.phasewalk or l.CanPhaseswim() or l.ledgeclip, Transitions.ForestMainToTinyMill),
        TransitionFront(Regions.GrinderRoom, lambda l: True, Transitions.ForestMainToGrinder, time=Time.Day),
        TransitionFront(Regions.MillRafters, lambda l: l.spring and l.isdiddy, Transitions.ForestMainToRafters, time=Time.Night),
        TransitionFront(Regions.WinchRoom, lambda l: (l.CanSlamSwitch(Levels.FungiForest, 2) and l.isdiddy) or (l.CanMoonkick()), Transitions.ForestMainToWinch, time=Time.Night),
        TransitionFront(Regions.MillAttic, lambda l: True, Transitions.ForestMainToAttic, time=Time.Night),
        TransitionFront(Regions.ThornvineArea, lambda l: True, time=Time.Night),
        TransitionFront(Regions.Snide, lambda l: True, time=Time.Day),
        TransitionFront(Regions.ForestBossLobby, lambda l: not l.settings.tns_location_rando, time=Time.Day),
        TransitionFront(Regions.ThornvineBarn, lambda l: l.CanPhaseswim(), Transitions.ForestMainToBarn, isGlitchTransition=True),
    ]),

    Regions.MillChunkyTinyArea: Region("Mill Back Room", "Forest Mills", Levels.FungiForest, False, -1, [], [
        Event(Events.GrinderActivated, lambda l: l.punch and l.triangle and l.ischunky),
        Event(Events.MillBoxBroken, lambda l: l.punch and l.ischunky),
    ], [
        TransitionFront(Regions.FungiForestMedals, lambda l: True),
        TransitionFront(Regions.MillArea, lambda l: l.ischunky, Transitions.ForestChunkyMillToMain, time=Time.Day),
        TransitionFront(Regions.MillArea, lambda l: (Events.MillBoxBroken in l.Events and l.mini and l.istiny) or l.phasewalk or l.ledgeclip, Transitions.ForestTinyMillToMain),
        TransitionFront(Regions.SpiderRoom, lambda l: True, Transitions.ForestTinyMillToSpider, time=Time.Night),
        TransitionFront(Regions.GrinderRoom, lambda l: (l.mini and l.istiny) or l.phasewalk or l.ledgeclip, Transitions.ForestTinyMillToGrinder),
    ]),

    Regions.SpiderRoom: Region("Spider Room", "Forest Mills", Levels.FungiForest, False, Regions.MillChunkyTinyArea, [
        # FTA Spider boss temporarily disabled for Night rework, will also need: or (l.settings.free_trade_items and l.HasGun(Kongs.any))),
        LocationLogic(Locations.ForestTinySpiderBoss, lambda l: l.HasGun(Kongs.tiny)),
    ], [], [
        TransitionFront(Regions.FungiForestMedals, lambda l: True),
        TransitionFront(Regions.MillChunkyTinyArea, lambda l: True, Transitions.ForestSpiderToTinyMill),
    ]),

    Regions.GrinderRoom: Region("Grinder Room", "Forest Mills", Levels.FungiForest, True, -1, [
        LocationLogic(Locations.ForestChunkyKegs, lambda l: Events.GrinderActivated in l.Events and Events.ConveyorActivated in l.Events and l.chunky and l.barrels),
    ], [
        Event(Events.ConveyorActivated, lambda l: (l.CanSlamSwitch(Levels.FungiForest, 2) or l.phasewalk or l.generalclips) and l.grab and l.donkey),
    ], [
        TransitionFront(Regions.FungiForestMedals, lambda l: True),
        TransitionFront(Regions.MillArea, lambda l: True, Transitions.ForestGrinderToMain, time=Time.Day),
        TransitionFront(Regions.MillChunkyTinyArea, lambda l: (l.mini and l.istiny) or l.phasewalk or l.generalclips, Transitions.ForestGrinderToTinyMill),
    ]),

    Regions.MillRafters: Region("Mill Rafters", "Forest Mills", Levels.FungiForest, False, None, [
        LocationLogic(Locations.ForestDiddyRafters, lambda l: l.guitar and l.isdiddy),
        LocationLogic(Locations.ForestBananaFairyRafters, lambda l: l.guitar and l.isdiddy and l.camera),
    ], [], [
        TransitionFront(Regions.FungiForestMedals, lambda l: True),
        TransitionFront(Regions.MillArea, lambda l: True, Transitions.ForestRaftersToMain),
    ]),

    Regions.WinchRoom: Region("Winch Room", "Forest Mills", Levels.FungiForest, False, -1, [], [
        Event(Events.WinchRaised, lambda l: l.peanut and l.charge and l.isdiddy),
    ], [
        TransitionFront(Regions.FungiForestMedals, lambda l: True),
        TransitionFront(Regions.MillArea, lambda l: True, Transitions.ForestWinchToMain),
    ]),

    Regions.MillAttic: Region("Mill Attic", "Forest Mills", Levels.FungiForest, False, None, [
        LocationLogic(Locations.ForestLankyAttic, lambda l: l.CanSlamSwitch(Levels.FungiForest, 2) and (l.homing or l.settings.hard_shooting) and l.grape and l.islanky),
    ], [], [
        TransitionFront(Regions.FungiForestMedals, lambda l: True),
        TransitionFront(Regions.MillArea, lambda l: True, Transitions.ForestAtticToMain),
    ]),

    Regions.ThornvineArea: Region("Thornvine Area", "Forest Mills", Levels.FungiForest, True, -1, [
        LocationLogic(Locations.ForestKasplatNearBarn, lambda l: not l.settings.kasplat_rando),
    ], [], [
        TransitionFront(Regions.FungiForestMedals, lambda l: True),
        TransitionFront(Regions.MillArea, lambda l: True, time=Time.Night),
        TransitionFront(Regions.ThornvineBarn, lambda l: (l.CanSlamSwitch(Levels.FungiForest, 2) and l.isdonkey and l.strongKong) or l.phasewalk, Transitions.ForestMainToBarn),
        TransitionFront(Regions.ForestBossLobby, lambda l: not l.settings.tns_location_rando),
    ]),

    Regions.ThornvineBarn: Region("Thornvine Barn", "Forest Mills", Levels.FungiForest, False, -1, [
        LocationLogic(Locations.ForestDonkeyBarn, lambda l: l.CanSlamSwitch(Levels.FungiForest, 1) and l.isdonkey and (l.vines or l.advanced_platforming), MinigameType.BonusBarrel),  # Krusha can make it by jumping onto the beam first.
        LocationLogic(Locations.ForestBananaFairyThornvines, lambda l: l.Slam and l.camera),
    ], [], [
        TransitionFront(Regions.FungiForestMedals, lambda l: True),
        TransitionFront(Regions.ThornvineArea, lambda l: True, Transitions.ForestBarnToMain),
    ]),

    Regions.WormArea: Region("Worm Area", "Forest Center and Beanstalk", Levels.FungiForest, True, -1, [
        LocationLogic(Locations.ForestTinyBeanstalk, lambda l: l.saxophone and l.mini and l.istiny and l.Beans >= 1),
        LocationLogic(Locations.ForestChunkyApple, lambda l: Events.WormGatesOpened in l.Events and l.hunkyChunky and l.ischunky and l.barrels),
        LocationLogic(Locations.RainbowCoin_Location08, lambda l: l.shockwave),
    ], [
        Event(Events.ForestW2aTagged, lambda l: True),
        Event(Events.WormGatesOpened, lambda l: l.settings.open_levels),
    ], [
        TransitionFront(Regions.FungiForestMedals, lambda l: True),
        TransitionFront(Regions.FungiForestStart, lambda l: Events.WormGatesOpened in l.Events),
        TransitionFront(Regions.FunkyForest, lambda l: True),
        TransitionFront(Regions.ForestBossLobby, lambda l: not l.settings.tns_location_rando, time=Time.Night),
    ]),

    Regions.ForestBossLobby: Region("Forest Boss Lobby", "Troff 'N' Scoff", Levels.FungiForest, True, None, [], [], [
        TransitionFront(Regions.ForestBoss, lambda l: l.IsBossReachable(Levels.FungiForest)),
    ]),

    Regions.ForestBoss: Region("Forest Boss", "Troff 'N' Scoff", Levels.FungiForest, False, None, [
        LocationLogic(Locations.ForestKey, lambda l: l.IsBossBeatable(Levels.FungiForest)),
    ], [], []),
}
