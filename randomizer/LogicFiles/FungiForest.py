from LogicClasses import Region, Location, Event, Exit
from Enums.Events import Events
from Enums.Regions import Regions
from Enums.Levels import Levels

LogicRegions = {
    Regions.FungiForestStart: Region("Fungi Forest Start", Levels.FungiForest, True, [], [
        Event(Events.ForestEntered, lambda l: True),
        Event(Events.Night, lambda l: l.coconut or l.peanut or l.grape or l.feather or l.pineapple),
    ], [
        Exit(Regions.FungiForestLobby, lambda l: True),
        Exit(Regions.ForestMinecarts, lambda l: l.Slam and l.ischunky),
        Exit(Regions.GiantMushroomArea, lambda l: True),
        Exit(Regions.MillArea, lambda l: True),
        Exit(Regions.WormArea, lambda l: l.feather and l.pineapple),
    ]),

    Regions.ForestMinecarts: Region("Forest Minecarts", Levels.FungiForest, False, [
        Location("Forest Chunky Minecarts", lambda l: l.ischunky),
    ], [], []),

    Regions.GiantMushroomArea: Region("Giant Mushroom Area", Levels.FungiForest, True, [
        Location("Forest Diddy Top of Mushroom", lambda l: l.jetpack),
    ], [], [
        Exit(Regions.MushroomLower, lambda l: True),
        Exit(Regions.MushroomLowerExterior, lambda l: l.jetpack),
        Exit(Regions.MushroomUpperExterior, lambda l: l.jetpack),
        Exit(Regions.HollowTreeArea, lambda l: l.grape),
        Exit(Regions.Cranky, lambda l: True),
    ]),

    Regions.MushroomLower: Region("Mushroom Lower", Levels.FungiForest, True, [
        Location("Forest Tiny Speedy Swing Sortie", lambda l: l.superSlam and l.istiny),
    ], [
        Event(Events.MushroomCannonsSpawned, lambda l: l.coconut and l.peanut and l.grape and l.feather and l.pineapple),
        Event(Events.DonkeyMushroomSwitch, lambda l: l.superSlam and l.isdonkey)
    ], [
        Exit(Regions.GiantMushroomArea, lambda l: True),
        Exit(Regions.MushroomLowerExterior, lambda l: True),
        Exit(Regions.MushroomUpper, lambda l: Events.MushroomCannonsSpawned in l.Events),
    ]),

    Regions.MushroomLowerExterior: Region("Mushroom Lower Exterior", Levels.FungiForest, True, [
        Location("Forest Donkey Baboon Blast", lambda l: l.blast and l.isdonkey),
        Location("Forest Tiny Kasplat", lambda l: l.istiny),
    ], [], [
        Exit(Regions.GiantMushroomArea, lambda l: True),
        Exit(Regions.MushroomLower, lambda l: True),
        Exit(Regions.MushroomUpper, lambda l: True),
    ]),

    Regions.MushroomUpper: Region("Mushroom Upper", Levels.FungiForest, True, [
        Location("Forest Donkey Mushroom Cannons", lambda l: Events.MushroomCannonsSpawned in l.Events and Events.DonkeyMushroomSwitch in l.Events),
        Location("Forest Diddy Kasplat", lambda l: l.isdiddy),
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
        Location("Forest Chunky Kasplat", lambda l: l.ischunky),
    ], [], [
        Exit(Regions.MushroomNightDoor, lambda l: Events.Night in l.Events),
        Exit(Regions.GiantMushroomArea, lambda l: True),
    ]),

    Regions.MushroomUpperExterior: Region("Mushroom Upper Exterior", Levels.FungiForest, True, [
        Location("Forest Battle Arena", lambda l: True),
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
        Location("Forest Chunky Face Puzzle", lambda l: l.pineapple and l.ischunky),
    ], [], [
        Exit(Regions.MushroomUpperExterior, lambda l: True),
    ]),

    Regions.MushroomLankyZingersRoom: Region("Mushroom Lanky Zingers Room", Levels.FungiForest, False, [
        Location("Forest Lanky Zingers", lambda l: l.grape and l.islanky),
    ], [], [
        Exit(Regions.MushroomUpperExterior, lambda l: True),
    ]),

    Regions.MushroomLankyMushroomsRoom: Region("Mushroom Lanky Mushrooms Room", Levels.FungiForest, False, [
        Location("Forest Lanky Colored Mushrooms", lambda l: l.Slam and l.islanky),
    ], [], [
        Exit(Regions.MushroomUpperExterior, lambda l: True),
    ]),

    Regions.HollowTreeArea: Region("Hollow Tree Area", Levels.FungiForest, True, [
        Location("Forest Diddy Owl Race", lambda l: Events.Night in l.Events and l.jetpack and l.guitar),
        Location("Forest Lanky Rabbit Race", lambda l: l.trombone and l.sprint),
        Location("Forest Lanky Kasplat", lambda l: l.islanky),
    ], [], [
        Exit(Regions.Anthill, lambda l: l.mini and l.saxophone),
        Exit(Regions.ForestBossLobby, lambda l: True),
    ]),

    Regions.Anthill: Region("Anthill", Levels.FungiForest, False, [
        Location("Forest Tiny Anthill", lambda l: l.istiny),
    ], [
        Event(Events.Bean, lambda l: l.istiny),
    ], [
        Exit(Regions.HollowTreeArea, lambda l: True),
    ]),

    Regions.MillArea: Region("Mill Area", Levels.FungiForest, True, [
        Location("Forest Donkey Mill", lambda l: Events.ConveyorActivated in l.Events and Events.Night in l.Events and l.isdonkey),
        Location("Forest Diddy Caged Banana", lambda l: Events.WenchRaised in l.Events and Events.Night in l.Events and l.isdiddy),
    ], [], [
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
    ]),

    Regions.MillTinyArea: Region("Mill Tiny Area", Levels.FungiForest, False, [], [], [
        Exit(Regions.MillArea, lambda l: l.mini and l.istiny),
        Exit(Regions.SpiderRoom, lambda l: Events.Night in l.Events),
        Exit(Regions.GrinderRoom, lambda l: l.mini and l.istiny),
    ]),

    Regions.SpiderRoom: Region("Spider Room", Levels.FungiForest, False, [
        Location("Forest Tiny Spider Boss", lambda l: l.feather and l.istiny),
    ], [], [
        Exit(Regions.MillTinyArea, lambda l: True),
    ]),

    Regions.GrinderRoom: Region("Grinder Room", Levels.FungiForest, True, [
        Location("Forest Chunky Kegs", lambda l: Events.GrinderActivated in l.Events and Events.ConveyorActivated in l.Events and l.ischunky),
    ], [
        Event(Events.ConveyorActivated, lambda l: l.superSlam and l.grab and l.isdonkey),
    ], [
        Exit(Regions.MillArea, lambda l: True),
        Exit(Regions.MillTinyArea, lambda l: l.mini and l.istiny),
    ]),

    Regions.MillRafters: Region("Mill Rafters", Levels.FungiForest, False, [
        Location("Forest Diddy Rafters", lambda l: l.isdiddy),
        Location("Forest Banana Fairy Rafters", lambda l: l.camera),
    ], [], [
        Exit(Regions.MillArea, lambda l: True),
    ]),

    Regions.WenchRoom: Region("Wench Room", Levels.FungiForest, False, [], [
        Event(Events.WenchRaised, lambda l: l.peanut and l.charge and l.isdiddy),
    ], [
        Exit(Regions.MillArea, lambda l: True),
    ]),

    Regions.MillAttic: Region("Mill Attic", Levels.FungiForest, False, [
        Location("Forest Lanky Attic", lambda l: l.grape and l.superSlam and l.islanky),
    ], [], [
        Exit(Regions.MillArea, lambda l: True),
    ]),

    Regions.ThornvineArea: Region("Thornvine Area", Levels.FungiForest, True, [
        Location("Forest Donkey Kasplat", lambda l: l.isdonkey),
    ], [], [
        # You're supposed to use strong kong to hit the switch in the thorns, but can brute force it
        Exit(Regions.ThornvineHut, lambda l: l.superSlam and l.isdonkey),
        Exit(Regions.ForestBossLobby, lambda l: True),
    ]),

    Regions.ThornvineHut: Region("Thornvine Hut", Levels.FungiForest, False, [
        Location("Forest Donkey Minecart Mayhem", lambda l: l.Slam and l.isdonkey),
        Location("Forest Banana Fairy Thornvines", lambda l: l.camera),
    ], [], [
        Exit(Regions.ThornvineArea, lambda l: True),
    ]),

    Regions.WormArea: Region("Worm Area", Levels.FungiForest, True, [
        Location("Forest Tiny Beanstalk", lambda l: Events.Bean in l.Events and l.saxophone and l.mini),
        Location("Forest Chunky Apple", lambda l: l.hunkyChunky),
    ], [], [
        Exit(Regions.Funky, lambda l: True),
        Exit(Regions.ForestBossLobby, lambda l: Events.Night in l.Events),
    ]),

    Regions.ForestBossLobby: Region("Forest Boss Lobby", Levels.FungiForest, True, [], [], [
        # 300 bananas
        Exit(Regions.ForestBoss, lambda l: l.ischunky),
    ]),

    Regions.ForestBoss: Region("Forest Boss", Levels.FungiForest, False, [
        Location("Forest Key", lambda l: l.hunkyChunky and l.ischunky),
    ], [], []),
}
