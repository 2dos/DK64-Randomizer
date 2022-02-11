# fmt: off
"""Logic file for Fungi Forest."""

from randomizer.Enums.Events import Events
from randomizer.Enums.Transitions import Transitions
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Regions import Regions
from randomizer.LogicClasses import Event, TransitionFront, LocationLogic, Region

LogicRegions = {
    Regions.FungiForestStart: Region("Fungi Forest Start", Levels.FungiForest, True, None, [
        LocationLogic(Locations.ForestDonkeyMedal, lambda l: l.ColoredBananas[Levels.FungiForest][Kongs.donkey] >= 75),
        LocationLogic(Locations.ForestDiddyMedal, lambda l: l.ColoredBananas[Levels.FungiForest][Kongs.diddy] >= 75),
        LocationLogic(Locations.ForestLankyMedal, lambda l: l.ColoredBananas[Levels.FungiForest][Kongs.lanky] >= 75),
        LocationLogic(Locations.ForestTinyMedal, lambda l: l.ColoredBananas[Levels.FungiForest][Kongs.tiny] >= 75),
        LocationLogic(Locations.ForestChunkyMedal, lambda l: l.ColoredBananas[Levels.FungiForest][Kongs.chunky] >= 75),
    ], [
        Event(Events.ForestEntered, lambda l: True),
        Event(Events.Night, lambda l: (l.coconut and l.donkey) or (l.peanut and l.diddy)
              or (l.grape and l.lanky) or (l.feather and l.tiny) or (l.pineapple and l.chunky)),
        Event(Events.WormGatesOpened, lambda l: (l.feather and l.tiny) and (l.pineapple and l.chunky)),
    ], [
        TransitionFront(Regions.FungiForestLobby, lambda l: True, Transitions.ForestToIsles),
        TransitionFront(Regions.ForestMinecarts, lambda l: l.Slam and l.ischunky),
        TransitionFront(Regions.GiantMushroomArea, lambda l: True),
        TransitionFront(Regions.MillArea, lambda l: True),
        TransitionFront(Regions.WormArea, lambda l: Events.WormGatesOpened in l.Events),
    ]),

    Regions.ForestMinecarts: Region("Forest Minecarts", Levels.FungiForest, False, None, [
        LocationLogic(Locations.ForestChunkyMinecarts, lambda l: l.ischunky),
    ], [], [
        TransitionFront(Regions.FungiForestStart, lambda l: True),
    ],  Transitions.ForestMainToCarts
    ),

    Regions.GiantMushroomArea: Region("Giant Mushroom Area", Levels.FungiForest, True, None, [
        LocationLogic(Locations.ForestDiddyTopofMushroom, lambda l: l.jetpack and l.diddy),
    ], [
        Event(Events.HollowTreeGateOpened, lambda l: l.grape and l.lanky),
    ], [
        TransitionFront(Regions.FungiForestStart, lambda l: True),
        TransitionFront(Regions.MushroomLower, lambda l: True, Transitions.ForestMainToLowerMushroom),
        TransitionFront(Regions.MushroomLowerExterior, lambda l: l.jetpack),
        TransitionFront(Regions.MushroomUpperExterior, lambda l: l.jetpack),
        TransitionFront(Regions.HollowTreeArea, lambda l: Events.HollowTreeGateOpened in l.Events),
        TransitionFront(Regions.Cranky, lambda l: True),
    ]),

    Regions.MushroomLower: Region("Mushroom Lower", Levels.FungiForest, True, None, [
        LocationLogic(Locations.ForestTinySpeedySwingSortie, lambda l: l.superSlam and l.tiny),
    ], [
        Event(Events.MushroomCannonsSpawned, lambda l: l.coconut and l.peanut and l.grape and l.feather and l.pineapple
              and l.donkey and l.diddy and l.lanky and l.tiny and l.chunky),
        Event(Events.DonkeyMushroomSwitch, lambda l: l.superSlam and l.donkey)
    ], [
        TransitionFront(Regions.GiantMushroomArea, lambda l: True, Transitions.ForestLowerMushroomToMain),
        TransitionFront(Regions.MushroomLowerExterior, lambda l: True, Transitions.ForestLowerMushroomToLowerExterior),
        TransitionFront(Regions.MushroomUpper, lambda l: Events.MushroomCannonsSpawned in l.Events),
    ]),

    Regions.MushroomLowerExterior: Region("Mushroom Lower Exterior", Levels.FungiForest, True, -1, [
        LocationLogic(Locations.ForestTinyKasplat, lambda l: l.tiny),
    ], [], [
        TransitionFront(Regions.GiantMushroomArea, lambda l: True),
        TransitionFront(Regions.MushroomLower, lambda l: True, Transitions.ForestLowerExteriorToLowerMushroom),
        TransitionFront(Regions.MushroomUpper, lambda l: True, Transitions.ForestLowerExteriorToUpperMushroom),
        TransitionFront(Regions.ForestBaboonBlast, lambda l: l.blast and l.isdonkey, Transitions.ForestMainToBBlast)
    ]),

    Regions.ForestBaboonBlast: Region("Forest Baboon Blast", Levels.FungiForest, False, None, [
        LocationLogic(Locations.ForestDonkeyBaboonBlast, lambda l: l.isdonkey),
    ], [], [
        TransitionFront(Regions.MushroomLowerExterior, lambda l: True)
    ]),

    Regions.MushroomUpper: Region("Mushroom Upper", Levels.FungiForest, True, -1, [
        LocationLogic(Locations.ForestDonkeyMushroomCannons, lambda l: Events.MushroomCannonsSpawned in l.Events and Events.DonkeyMushroomSwitch in l.Events),
        LocationLogic(Locations.ForestDiddyKasplat, lambda l: l.diddy),
    ], [], [
        TransitionFront(Regions.MushroomLower, lambda l: True),
        TransitionFront(Regions.MushroomLowerExterior, lambda l: True, Transitions.ForestUpperMushroomToLowerExterior),
        TransitionFront(Regions.MushroomUpperExterior, lambda l: True, Transitions.ForestUpperMushroomToUpperExterior),
        TransitionFront(Regions.MushroomNightDoor, lambda l: True),
    ]),

    # This region basically just exists to facilitate the two entrances into upper mushroom
    Regions.MushroomNightDoor: Region("Mushroom Night Door", Levels.FungiForest, False, None, [], [], [
        TransitionFront(Regions.MushroomUpper, lambda l: True),
        TransitionFront(Regions.MushroomNightExterior, lambda l: Events.Night in l.Events, Transitions.ForestNightToExterior),
    ]),

    Regions.MushroomNightExterior: Region("Mushroom Night Exterior", Levels.FungiForest, False, None, [
        LocationLogic(Locations.ForestChunkyKasplat, lambda l: l.ischunky),
    ], [], [
        TransitionFront(Regions.MushroomNightDoor, lambda l: Events.Night in l.Events, Transitions.ForestExteriorToNight),
        TransitionFront(Regions.GiantMushroomArea, lambda l: True),
    ]),

    Regions.MushroomUpperExterior: Region("Mushroom Upper Exterior", Levels.FungiForest, True, -1, [
        LocationLogic(Locations.ForestBattleArena, lambda l: True),
    ], [], [
        TransitionFront(Regions.MushroomUpper, lambda l: True, Transitions.ForestUpperExteriorToUpperMushroom),
        TransitionFront(Regions.MushroomNightExterior, lambda l: True),
        TransitionFront(Regions.GiantMushroomArea, lambda l: True),
        TransitionFront(Regions.MushroomChunkyRoom, lambda l: l.superSlam and l.ischunky, Transitions.ForestExteriorToChunky),
        TransitionFront(Regions.MushroomLankyZingersRoom, lambda l: l.superSlam and l.islanky, Transitions.ForestExteriorToZingers),
        TransitionFront(Regions.MushroomLankyMushroomsRoom, lambda l: l.superSlam and l.islanky, Transitions.ForestExteriorToMushrooms),
        TransitionFront(Regions.ForestBossLobby, lambda l: True),
    ]),

    Regions.MushroomChunkyRoom: Region("Mushroom Chunky Room", Levels.FungiForest, False, -1, [
        LocationLogic(Locations.ForestChunkyFacePuzzle, lambda l: l.pineapple and l.ischunky),
    ], [], [
        TransitionFront(Regions.MushroomUpperExterior, lambda l: True, Transitions.ForestChunkyToExterior),
    ]),

    Regions.MushroomLankyZingersRoom: Region("Mushroom Lanky Zingers Room", Levels.FungiForest, False, -1, [
        LocationLogic(Locations.ForestLankyZingers, lambda l: l.islanky),
    ], [], [
        TransitionFront(Regions.MushroomUpperExterior, lambda l: True, Transitions.ForestZingersToExterior),
    ]),

    Regions.MushroomLankyMushroomsRoom: Region("Mushroom Lanky Mushrooms Room", Levels.FungiForest, False, None, [
        LocationLogic(Locations.ForestLankyColoredMushrooms, lambda l: l.Slam and l.islanky),
    ], [], [
        TransitionFront(Regions.MushroomUpperExterior, lambda l: True, Transitions.ForestMushroomsToExterior),
    ]),

    Regions.HollowTreeArea: Region("Hollow Tree Area", Levels.FungiForest, True, -1, [
        LocationLogic(Locations.ForestDiddyOwlRace, lambda l: Events.Night in l.Events and l.jetpack and l.guitar and l.diddy),
        LocationLogic(Locations.ForestLankyRabbitRace, lambda l: l.trombone and l.sprint and l.lanky),
        LocationLogic(Locations.ForestLankyKasplat, lambda l: l.lanky),
    ], [], [
        TransitionFront(Regions.GiantMushroomArea, lambda l: Events.HollowTreeGateOpened in l.Events),
        TransitionFront(Regions.Anthill, lambda l: l.mini and l.saxophone, Transitions.ForestTreeToAnthill),
        TransitionFront(Regions.ForestBossLobby, lambda l: True),
    ]),

    Regions.Anthill: Region("Anthill", Levels.FungiForest, False, -1, [
        LocationLogic(Locations.ForestTinyAnthill, lambda l: l.istiny),
    ], [
        Event(Events.Bean, lambda l: l.istiny),
    ], [
        TransitionFront(Regions.HollowTreeArea, lambda l: True, Transitions.ForestAnthillToTree),
    ]),

    Regions.MillArea: Region("Mill Area", Levels.FungiForest, True, None, [
        LocationLogic(Locations.ForestDonkeyMill, lambda l: Events.ConveyorActivated in l.Events and Events.Night in l.Events and l.donkey),
        LocationLogic(Locations.ForestDiddyCagedBanana, lambda l: Events.WinchRaised in l.Events and Events.Night in l.Events and l.diddy),
    ], [], [
        TransitionFront(Regions.FungiForestStart, lambda l: True),
        TransitionFront(Regions.MillChunkyArea, lambda l: l.punch and l.ischunky, Transitions.ForestMainToChunkyMill),
        TransitionFront(Regions.MillTinyArea, lambda l: Events.MillBoxBroken in l.Events and l.mini and l.istiny, Transitions.ForestMainToTinyMill),
        TransitionFront(Regions.GrinderRoom, lambda l: True, Transitions.ForestMainToGrinder),
        TransitionFront(Regions.MillRafters, lambda l: Events.Night in l.Events and l.spring and l.isdiddy, Transitions.ForestMainToRafters),
        TransitionFront(Regions.WinchRoom, lambda l: Events.Night in l.Events and l.superSlam and l.isdiddy, Transitions.ForestMainToWinch),
        TransitionFront(Regions.MillAttic, lambda l: Events.Night in l.Events, Transitions.ForestMainToAttic),
        TransitionFront(Regions.ThornvineArea, lambda l: Events.Night in l.Events),
        TransitionFront(Regions.Snide, lambda l: True),
        TransitionFront(Regions.ForestBossLobby, lambda l: True),
    ]),

    # Physically chunky and tiny share an area but they're split for logical convenience
    Regions.MillChunkyArea: Region("Mill Chunky Area", Levels.FungiForest, False, -1, [], [
        Event(Events.GrinderActivated, lambda l: l.triangle and l.ischunky),
        Event(Events.MillBoxBroken, lambda l: l.punch and l.ischunky),
    ], [
        TransitionFront(Regions.MillArea, lambda l: True, Transitions.ForestChunkyMillToMain),
        TransitionFront(Regions.MillTinyArea, lambda l: True),
    ]),

    Regions.MillTinyArea: Region("Mill Tiny Area", Levels.FungiForest, False, -1, [], [], [
        TransitionFront(Regions.MillArea, lambda l: l.mini and l.istiny, Transitions.ForestTinyMillToMain),
        TransitionFront(Regions.MillChunkyArea, lambda l: True),
        TransitionFront(Regions.SpiderRoom, lambda l: Events.Night in l.Events, Transitions.ForestTinyMillToSpider),
        TransitionFront(Regions.GrinderRoom, lambda l: l.mini and l.istiny, Transitions.ForestTinyMillToGrinder),
    ]),

    Regions.SpiderRoom: Region("Spider Room", Levels.FungiForest, False, Regions.MillTinyArea, [
        LocationLogic(Locations.ForestTinySpiderBoss, lambda l: l.feather and l.istiny),
    ], [], [
        TransitionFront(Regions.MillTinyArea, lambda l: True, Transitions.ForestSpiderToTinyMill),
    ]),

    Regions.GrinderRoom: Region("Grinder Room", Levels.FungiForest, True, -1, [
        LocationLogic(Locations.ForestChunkyKegs, lambda l: Events.GrinderActivated in l.Events and Events.ConveyorActivated in l.Events and l.chunky),
    ], [
        Event(Events.ConveyorActivated, lambda l: l.superSlam and l.grab and l.donkey),
    ], [
        TransitionFront(Regions.MillArea, lambda l: True, Transitions.ForestGrinderToMain),
        TransitionFront(Regions.MillTinyArea, lambda l: l.mini and l.istiny, Transitions.ForestGrinderToTinyMill),
    ]),

    Regions.MillRafters: Region("Mill Rafters", Levels.FungiForest, False, None, [
        LocationLogic(Locations.ForestDiddyRafters, lambda l: l.isdiddy),
        LocationLogic(Locations.ForestBananaFairyRafters, lambda l: l.camera),
    ], [], [
        TransitionFront(Regions.MillArea, lambda l: True, Transitions.ForestRaftersToMain),
    ]),

    Regions.WinchRoom: Region("Winch Room", Levels.FungiForest, False, -1, [], [
        Event(Events.WinchRaised, lambda l: l.peanut and l.charge and l.isdiddy),
    ], [
        TransitionFront(Regions.MillArea, lambda l: True, Transitions.ForestWinchToMain),
    ]),

    Regions.MillAttic: Region("Mill Attic", Levels.FungiForest, False, TransitionFront(Regions.FungiForestStart, lambda l: l.superSlam and l.islanky), [
        LocationLogic(Locations.ForestLankyAttic, lambda l: l.grape and l.superSlam and l.islanky),
    ], [], [
        TransitionFront(Regions.MillArea, lambda l: True, Transitions.ForestAtticToMain),
    ]),

    Regions.ThornvineArea: Region("Thornvine Area", Levels.FungiForest, True, -1, [
        LocationLogic(Locations.ForestDonkeyKasplat, lambda l: l.donkey),
    ], [], [
        TransitionFront(Regions.MillArea, lambda l: Events.Night in l.Events),
        # You're supposed to use strong kong to hit the switch in the thorns, but can brute force it
        TransitionFront(Regions.ThornvineBarn, lambda l: l.superSlam and l.isdonkey, Transitions.ForestMainToBarn),
        TransitionFront(Regions.ForestBossLobby, lambda l: True),
    ]),

    Regions.ThornvineBarn: Region("Thornvine Barn", Levels.FungiForest, False, -1, [
        LocationLogic(Locations.ForestDonkeyMinecartMayhem, lambda l: l.Slam and l.isdonkey),
        LocationLogic(Locations.ForestBananaFairyThornvines, lambda l: l.camera),
    ], [], [
        TransitionFront(Regions.ThornvineArea, lambda l: True, Transitions.ForestBarnToMain),
    ]),

    Regions.WormArea: Region("Worm Area", Levels.FungiForest, True, -1, [
        LocationLogic(Locations.ForestTinyBeanstalk, lambda l: Events.Bean in l.Events and l.saxophone and l.mini and l.tiny),
        LocationLogic(Locations.ForestChunkyApple, lambda l: l.hunkyChunky and l.chunky),
    ], [], [
        TransitionFront(Regions.FungiForestStart, lambda l: True),
        TransitionFront(Regions.Funky, lambda l: True),
        TransitionFront(Regions.ForestBossLobby, lambda l: Events.Night in l.Events),
    ]),

    Regions.ForestBossLobby: Region("Forest Boss Lobby", Levels.FungiForest, True, None, [], [], [
        TransitionFront(Regions.ForestBoss, lambda l: l.ischunky and sum(l.ColoredBananas[Levels.FungiForest]) >= l.settings.BossBananas[Levels.FungiForest - 1]),
    ]),

    Regions.ForestBoss: Region("Forest Boss", Levels.FungiForest, False, None, [
        LocationLogic(Locations.ForestKey, lambda l: l.hunkyChunky and l.ischunky),
    ], [], []),
}
