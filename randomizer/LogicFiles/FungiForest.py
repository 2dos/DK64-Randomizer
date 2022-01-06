# fmt: off
"""Logic file for Fungi Forest."""

from randomizer.Enums.Events import Events
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Regions import Regions
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Kongs import Kongs
from randomizer.LogicClasses import Event, Exit, LocationLogic, Region

LogicRegions = {
    Regions.FungiForestStart: Region("Fungi Forest Start", Levels.FungiForest, True, [
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
        Exit(Regions.FungiForestLobby, lambda l: True),
        Exit(Regions.ForestMinecarts, lambda l: l.Slam and l.ischunky),
        Exit(Regions.GiantMushroomArea, lambda l: True),
        Exit(Regions.MillArea, lambda l: True),
        Exit(Regions.WormArea, lambda l: Events.WormGatesOpened in l.Events),
    ]),

    Regions.ForestMinecarts: Region("Forest Minecarts", Levels.FungiForest, False, [
        LocationLogic(Locations.ForestChunkyMinecarts, lambda l: l.ischunky),
    ], [], []),

    Regions.GiantMushroomArea: Region("Giant Mushroom Area", Levels.FungiForest, True, [
        LocationLogic(Locations.ForestDiddyTopofMushroom, lambda l: l.jetpack and l.diddy),
    ], [
        Event(Events.HollowTreeGateOpened, lambda l: l.grape and l.lanky),
    ], [
        Exit(Regions.FungiForestStart, lambda l: True),
        Exit(Regions.MushroomLower, lambda l: True),
        Exit(Regions.MushroomLowerExterior, lambda l: l.jetpack),
        Exit(Regions.MushroomUpperExterior, lambda l: l.jetpack),
        Exit(Regions.HollowTreeArea, lambda l: Events.HollowTreeGateOpened in l.Events),
        Exit(Regions.Cranky, lambda l: True),
    ]),

    Regions.MushroomLower: Region("Mushroom Lower", Levels.FungiForest, True, [
        LocationLogic(Locations.ForestTinySpeedySwingSortie, lambda l: l.superSlam and l.tiny),
    ], [
        Event(Events.MushroomCannonsSpawned, lambda l: l.coconut and l.peanut and l.grape and l.feather and l.pineapple
            and l.donkey and l.diddy and l.lanky and l.tiny and l.chunky),
        Event(Events.DonkeyMushroomSwitch, lambda l: l.superSlam and l.donkey)
    ], [
        Exit(Regions.GiantMushroomArea, lambda l: True),
        Exit(Regions.MushroomLowerExterior, lambda l: True),
        Exit(Regions.MushroomUpper, lambda l: Events.MushroomCannonsSpawned in l.Events),
    ]),

    Regions.MushroomLowerExterior: Region("Mushroom Lower Exterior", Levels.FungiForest, True, [
        LocationLogic(Locations.ForestDonkeyBaboonBlast, lambda l: l.blast and l.donkey),
        LocationLogic(Locations.ForestTinyKasplat, lambda l: l.tiny),
    ], [], [
        Exit(Regions.GiantMushroomArea, lambda l: True),
        Exit(Regions.MushroomLower, lambda l: True),
        Exit(Regions.MushroomUpper, lambda l: True),
    ]),

    Regions.MushroomUpper: Region("Mushroom Upper", Levels.FungiForest, True, [
        LocationLogic(Locations.ForestDonkeyMushroomCannons, lambda l: Events.MushroomCannonsSpawned in l.Events and Events.DonkeyMushroomSwitch in l.Events),
        LocationLogic(Locations.ForestDiddyKasplat, lambda l: l.diddy),
    ], [], [
        Exit(Regions.MushroomLower, lambda l: True),
        Exit(Regions.MushroomLowerExterior, lambda l: True),
        Exit(Regions.MushroomUpperExterior, lambda l: True),
        Exit(Regions.MushroomNightDoor, lambda l: True),
    ]),

    # This region basically just exists to facilitate the two entrances into upper mushroom
    Regions.MushroomNightDoor: Region("Mushroom Night Door", Levels.FungiForest, False, [], [], [
        Exit(Regions.MushroomUpper, lambda l: True),
        Exit(Regions.MushroomNightExterior, lambda l: Events.Night in l.Events),
    ]),

    Regions.MushroomNightExterior: Region("Mushroom Night Exterior", Levels.FungiForest, False, [
        LocationLogic(Locations.ForestChunkyKasplat, lambda l: l.ischunky),
    ], [], [
        Exit(Regions.MushroomNightDoor, lambda l: Events.Night in l.Events),
        Exit(Regions.GiantMushroomArea, lambda l: True),
    ]),

    Regions.MushroomUpperExterior: Region("Mushroom Upper Exterior", Levels.FungiForest, True, [
        LocationLogic(Locations.ForestBattleArena, lambda l: True),
    ], [], [
        Exit(Regions.MushroomUpper, lambda l: True),
        Exit(Regions.MushroomNightExterior, lambda l: True),
        Exit(Regions.GiantMushroomArea, lambda l: True),
        Exit(Regions.MushroomChunkyRoom, lambda l: l.superSlam and l.ischunky),
        Exit(Regions.MushroomLankyZingersRoom, lambda l: l.superSlam and l.islanky),
        Exit(Regions.MushroomLankyMushroomsRoom, lambda l: l.superSlam and l.islanky),
        Exit(Regions.ForestBossLobby, lambda l: True),
    ]),

    Regions.MushroomChunkyRoom: Region("Mushroom Chunky Room", Levels.FungiForest, False, [
        LocationLogic(Locations.ForestChunkyFacePuzzle, lambda l: l.pineapple and l.ischunky),
    ], [], [
        Exit(Regions.MushroomUpperExterior, lambda l: True),
    ]),

    Regions.MushroomLankyZingersRoom: Region("Mushroom Lanky Zingers Room", Levels.FungiForest, False, [
        LocationLogic(Locations.ForestLankyZingers, lambda l: l.grape and l.islanky),
    ], [], [
        Exit(Regions.MushroomUpperExterior, lambda l: True),
    ]),

    Regions.MushroomLankyMushroomsRoom: Region("Mushroom Lanky Mushrooms Room", Levels.FungiForest, False, [
        LocationLogic(Locations.ForestLankyColoredMushrooms, lambda l: l.Slam and l.islanky),
    ], [], [
        Exit(Regions.MushroomUpperExterior, lambda l: True),
    ]),

    Regions.HollowTreeArea: Region("Hollow Tree Area", Levels.FungiForest, True, [
        LocationLogic(Locations.ForestDiddyOwlRace, lambda l: Events.Night in l.Events and l.jetpack and l.guitar and l.diddy),
        LocationLogic(Locations.ForestLankyRabbitRace, lambda l: l.trombone and l.sprint and l.lanky),
        LocationLogic(Locations.ForestLankyKasplat, lambda l: l.lanky),
    ], [], [
        Exit(Regions.GiantMushroomArea, lambda l: Events.HollowTreeGateOpened in l.Events),
        Exit(Regions.Anthill, lambda l: l.mini and l.saxophone),
        Exit(Regions.ForestBossLobby, lambda l: True),
    ]),

    Regions.Anthill: Region("Anthill", Levels.FungiForest, False, [
        LocationLogic(Locations.ForestTinyAnthill, lambda l: l.istiny),
    ], [
        Event(Events.Bean, lambda l: l.istiny),
    ], [
        Exit(Regions.HollowTreeArea, lambda l: True),
    ]),

    Regions.MillArea: Region("Mill Area", Levels.FungiForest, True, [
        LocationLogic(Locations.ForestDonkeyMill, lambda l: Events.ConveyorActivated in l.Events and Events.Night in l.Events and l.donkey),
        LocationLogic(Locations.ForestDiddyCagedBanana, lambda l: Events.WenchRaised in l.Events and Events.Night in l.Events and l.diddy),
    ], [], [
        Exit(Regions.FungiForestStart, lambda l: True),
        Exit(Regions.MillChunkyArea, lambda l: l.punch and l.ischunky),
        Exit(Regions.MillTinyArea, lambda l: Events.MillBoxBroken in l.Events and l.mini and l.istiny),
        Exit(Regions.GrinderRoom, lambda l: True),
        Exit(Regions.MillRafters, lambda l: Events.Night in l.Events and l.spring and l.isdiddy),
        Exit(Regions.WenchRoom, lambda l: Events.Night in l.Events and l.superSlam and l.isdiddy),
        Exit(Regions.MillAttic, lambda l: Events.Night in l.Events),
        Exit(Regions.ThornvineArea, lambda l: Events.Night in l.Events),
        Exit(Regions.Snide, lambda l: True),
        Exit(Regions.ForestBossLobby, lambda l: True),
    ]),

    # Physically chunky and tiny share an area but they're split for logical convenience
    Regions.MillChunkyArea: Region("Mill Chunky Area", Levels.FungiForest, False, [], [
        Event(Events.GrinderActivated, lambda l: l.triangle and l.ischunky),
        Event(Events.MillBoxBroken, lambda l: l.punch and l.ischunky),
    ], [
        Exit(Regions.MillArea, lambda l: True),
        Exit(Regions.MillTinyArea, lambda l: True),
    ]),

    Regions.MillTinyArea: Region("Mill Tiny Area", Levels.FungiForest, False, [], [], [
        Exit(Regions.MillChunkyArea, lambda l: True),
        Exit(Regions.MillArea, lambda l: l.mini and l.istiny),
        Exit(Regions.SpiderRoom, lambda l: Events.Night in l.Events),
        Exit(Regions.GrinderRoom, lambda l: l.mini and l.istiny),
    ]),

    Regions.SpiderRoom: Region("Spider Room", Levels.FungiForest, False, [
        LocationLogic(Locations.ForestTinySpiderBoss, lambda l: l.feather and l.istiny),
    ], [], [
        Exit(Regions.MillTinyArea, lambda l: True),
    ]),

    Regions.GrinderRoom: Region("Grinder Room", Levels.FungiForest, True, [
        LocationLogic(Locations.ForestChunkyKegs, lambda l: Events.GrinderActivated in l.Events and Events.ConveyorActivated in l.Events and l.chunky),
    ], [
        Event(Events.ConveyorActivated, lambda l: l.superSlam and l.grab and l.donkey),
    ], [
        Exit(Regions.MillArea, lambda l: True),
        Exit(Regions.MillTinyArea, lambda l: l.mini and l.istiny),
    ]),

    Regions.MillRafters: Region("Mill Rafters", Levels.FungiForest, False, [
        LocationLogic(Locations.ForestDiddyRafters, lambda l: l.isdiddy),
        LocationLogic(Locations.ForestBananaFairyRafters, lambda l: l.camera),
    ], [], [
        Exit(Regions.MillArea, lambda l: True),
    ]),

    Regions.WenchRoom: Region("Wench Room", Levels.FungiForest, False, [], [
        Event(Events.WenchRaised, lambda l: l.peanut and l.charge and l.isdiddy),
    ], [
        Exit(Regions.MillArea, lambda l: True),
    ]),

    Regions.MillAttic: Region("Mill Attic", Levels.FungiForest, False, [
        LocationLogic(Locations.ForestLankyAttic, lambda l: l.grape and l.superSlam and l.islanky),
    ], [], [
        Exit(Regions.MillArea, lambda l: True),
    ]),

    Regions.ThornvineArea: Region("Thornvine Area", Levels.FungiForest, True, [
        LocationLogic(Locations.ForestDonkeyKasplat, lambda l: l.donkey),
    ], [], [
        Exit(Regions.MillArea, lambda l: Events.Night in l.Events),
        # You're supposed to use strong kong to hit the switch in the thorns, but can brute force it
        Exit(Regions.ThornvineBarn, lambda l: l.superSlam and l.isdonkey),
        Exit(Regions.ForestBossLobby, lambda l: True),
    ]),

    Regions.ThornvineBarn: Region("Thornvine Barn", Levels.FungiForest, False, [
        LocationLogic(Locations.ForestDonkeyMinecartMayhem, lambda l: l.Slam and l.isdonkey),
        LocationLogic(Locations.ForestBananaFairyThornvines, lambda l: l.camera),
    ], [], [
        Exit(Regions.ThornvineArea, lambda l: True),
    ]),

    Regions.WormArea: Region("Worm Area", Levels.FungiForest, True, [
        LocationLogic(Locations.ForestTinyBeanstalk, lambda l: Events.Bean in l.Events and l.saxophone and l.mini and l.tiny),
        LocationLogic(Locations.ForestChunkyApple, lambda l: l.hunkyChunky and l.chunky),
    ], [], [
        Exit(Regions.FungiForestStart, lambda l: True),
        Exit(Regions.Funky, lambda l: True),
        Exit(Regions.ForestBossLobby, lambda l: Events.Night in l.Events),
    ]),

    Regions.ForestBossLobby: Region("Forest Boss Lobby", Levels.FungiForest, True, [], [], [
        Exit(Regions.ForestBoss, lambda l: l.ischunky and sum(l.ColoredBananas[Levels.FungiForest]) >= l.settings.BossBananas[Levels.FungiForest - 1]),
    ]),

    Regions.ForestBoss: Region("Forest Boss", Levels.FungiForest, False, [
        LocationLogic(Locations.ForestKey, lambda l: l.hunkyChunky and l.ischunky),
    ], [], []),
}
