from LogicClasses import Region, Location, Event, Exit
from Enums.Events import Events

Regions = {
    "Fungi Forest Start": Region("Fungi Forest Start", True, [], [
        Event(Events.ForestEntered, lambda l: True),
        Event(Events.Night, lambda l: l.coconut or l.peanut or l.grape or l.feather or l.pineapple),
    ], [
        Exit("Fungi Forest Lobby", lambda l: True),
        Exit("Forest Minecarts", lambda l: l.Slam and l.ischunky),
        Exit("Giant Mushroom Area", lambda l: True),
        Exit("Mill Area", lambda l: True),
        Exit("Worm Area", lambda l: l.feather and l.pineapple),
    ]),

    "Forest Minecarts": Region("Forest Minecarts", False, [
        Location("Forest Chunky Minecarts", lambda l: l.ischunky),
    ], [], []),

    "Giant Mushroom Area": Region("Giant Mushroom Area", True, [
        Location("Forest Diddy Top of Mushroom", lambda l: l.jetpack),
    ], [], [
        Exit("Mushroom Lower", lambda l: True),
        Exit("Mushroom Lower Exterior", lambda l: l.jetpack),
        Exit("Mushroom Upper Exterior", lambda l: l.jetpack),
        Exit("Hollow Tree Area", lambda l: l.grape),
        Exit("Cranky", lambda l: True),
    ]),

    "Mushroom Lower": Region("Mushroom Lower", True, [
        Location("Forest Tiny Speedy Swing Sortie", lambda l: l.superSlam and l.istiny),
    ], [
        Event(Events.MushroomCannonsSpawned, lambda l: l.coconut and l.peanut and l.grape and l.feather and l.pineapple),
        Event(Events.DonkeyMushroomSwitch, lambda l: l.superSlam and l.isdonkey)
    ], [
        Exit("Giant Mushroom Area", lambda l: True),
        Exit("Mushroom Lower Exterior", lambda l: True),
        Exit("Mushroom Upper", lambda l: Events.MushroomCannonsSpawned in l.Event),
    ]),

    "Mushroom Lower Exterior": Region("Mushroom Lower Exterior", True, [
        Location("Forest Donkey Baboon Blast", lambda l: l.blast and l.isdonkey),
        Location("Forest Tiny Kasplat", lambda l: l.istiny),
    ], [], [
        Exit("Giant Mushroom Area", lambda l: True),
        Exit("Mushroom Lower", lambda l: True),
        Exit("Mushroom Upper", lambda l: True),
    ]),

    "Mushroom Upper": Region("Mushroom Upper", True, [
        Location("Forest Donkey Mushroom Cannons", lambda l: Events.MushroomCannonsSpawned in l.Events and Events.DonkeyMushroomSwitch in l.Events),
    ], [], [
        Exit("Mushroom Lower", lambda l: True),
        Exit("Mushroom Lower Exterior", lambda l: True),
        Exit("Mushroom Upper Exterior", lambda l: True),
        Exit("Mushroom Night Door", lambda l: True),
    ]),

    # This region basically just exists to facilitate the two entrances into upper mushroom
    "Mushroom Night Door": Region("Mushroom Night Door", False, [], [], [
        Exit("Mushroom Tower Night Exterior", lambda l: Events.Night in l.Events),
    ]),

    "Mushroom Night Exterior": Region("Mushroom Night Exterior", False, [
        Location("Forest Chunky Kasplat", lambda l: l.ischunky),
    ], [], [
        Exit("Mushroom Night Door", lambda l: Events.Night in l.Events),
        Exit("Giant Mushroom Area", lambda l: True),
    ]),

    "Mushroom Upper Exterior": Region("Mushroom Upper Exterior", True, [
        Location("Forest Battle Arena", lambda l: True),
    ], [], [
        Exit("Mushroom Upper", lambda l: True),
        Exit("Mushroom Night Exterior", lambda l: True),
        Exit("Giant Mushroom Area", lambda l: True),
        Exit("Mushroom Chunky Room", lambda l: l.superSlam and l.ischunky),
        Exit("Mushroom Lanky Zingers Room", lambda l: l.superSlam and l.islanky),
        Exit("Mushroom Lanky Mushrooms Room", lambda l: l.superSlam and l.islanky),
        Exit("Forest Boss Lobby", lambda l: True),
    ]),

    "Mushroom Chunky Room": Region("Mushroom Chunky Room", False, [
        Location("Forest Chunky Face Puzzle", lambda l: l.pineapple and l.ischunky),
    ], [], [
        Exit("Mushroom Upper Exterior", lambda l: True),
    ]),

    "Mushroom Lanky Zingers Room": Region("Mushroom Lanky Zingers Room", False, [
        Location("Forest Lanky Zingers", lambda l: l.grape and l.islanky),
    ], [], [
        Exit("Mushroom Upper Exterior", lambda l: True),
    ]),

    "Mushroom Lanky Mushrooms Room": Region("Mushroom Lanky Mushrooms Room", False, [
        Location("Forest Lanky Colored Mushrooms", lambda l: l.Slam and l.islanky),
    ], [], [
        Exit("Mushroom Upper Exterior", lambda l: True),
    ]),

    "Hollow Tree Area": Region("Hollow Tree Area", True, [
        Location("Forest Diddy Owl Race", lambda l: Events.Night in l.Events and l.jetpack and l.guitar),
        Location("Forest Lanky Rabbit Race", lambda l: l.trombone and l.sprint),
        Location("Forest Lanky Kasplat", lambda l: l.islanky),
    ], [], [
        Exit("Anthill", lambda l: l.mini and l.saxophone),
        Exit("Forest Boss Lobby", lambda l: True),
    ]),

    "Anthill": Region("Anthill", False, [
        Location("Forest Tiny Anthill", lambda l: l.istiny),
    ], [
        Event(Events.Bean, lambda l: l.istiny),
    ], [
        Exit("Hollow Tree Area", lambda l: True),
    ]),

    "Mill Area": Region("Mill Area", True, [
        Location("Forest Donkey Mill", lambda l: Events.ConveyorActivated in l.Events and Events.Night in l.Events and l.isdonkey),
        Location("Forest Diddy Caged Banana", lambda l: Events.WenchRaised in l.Events and Events.Night in l.Events and l.isdiddy),
    ], [], [
        Exit("Mill Chunky Area", lambda l: l.punch and l.ischunky),
        Exit("Mill Tiny Area", lambda l: Events.MillBoxBroken in l.Events and l.mini and l.istiny),
        Exit("Grinder Room", lambda l: True),
        Exit("Mill Rafters", lambda l: Events.Night in l.Events and l.spring and l.isdiddy),
        Exit("Wench Room", lambda l: Events.Night in l.Events and l.superSlam and l.isdiddy),
        Exit("Mill Attic", lambda l: Events.Night in l.Events),
        Exit("Thornvine Area", lambda l: Events.Night in l.Events),
        Exit("Snide", lambda l: True),
        Exit("Forest Boss Lobby", lambda l: True),
    ]),

    # Physically chunky and tiny share an area but they're split for logical convenience
    "Mill Chunky Area": Region("Mill Chunky Area", False, [], [
        Event(Events.GrinderActivated, lambda l: l.triangle and l.ischunky),
        Event(Events.MillBoxBroken, lambda l: l.punch and l.ischunky),
    ], [
        Exit("Mill Area", lambda l: True),
    ]),

    "Mill Tiny Area": Region("Mill Tiny Area", False, [], [], [
        Exit("Mill Area", lambda l: l.mini and l.istiny),
        Exit("Spider Room", lambda l: Events.Night in l.Events),
        Exit("Grinder Room", lambda l: l.mini and l.istiny),
    ]),

    "Spider Room": Region("Spider Room", False, [
        Location("Forest Tiny Spider Boss", lambda l: l.feather and l.istiny),
    ], [], [
        Exit("Mill Tiny Area", lambda l: True),
    ]),

    "Grinder Room": Region("Grinder Room", True, [
        Location("Forest Chunky Kegs", lambda l: Events.GrinderActivated in l.Events and Events.ConveyorActivated in l.Events and l.ischunky),
    ], [
        Event(Events.ConveyorActivated, lambda l: l.superSlam and l.grab and l.isdonkey),
    ], [
        Exit("Mill Area", lambda l: True),
        Exit("Mill Tiny Area", lambda l: l.mini and l.istiny),
    ]),

    "Mill Rafters": Region("Mill Rafters", False, [
        Location("Forest Diddy Rafters", lambda l: l.isdiddy),
        Location("Forest Banana Fairy Rafters", lambda l: l.camera),
    ], [], [
        Exit("Mill Area", lambda l: True),
    ]),

    "Wench Room": Region("Wench Room", False, [], [
        Event(Events.WenchRaised, lambda l: l.peanut and l.charge and l.isdiddy),
    ], [
        Exit("Mill Area", lambda l: True),
    ]),

    "Mill Attic": Region("Mill Attic", False, [
        Location("Forest Lanky Attic", lambda l: l.grape and l.superSlam and l.islanky),
    ], [], [
        Exit("Mill Area", lambda l: True),
    ]),

    "Thornvine Area": Region("Thornvine Area", True, [
        Location("Forest Donkey Kasplat", lambda l: l.isdonkey),
    ], [], [
        # You're supposed to use strong kong to hit the switch in the thorns, but can brute force it
        Exit("Thornvine Hut", lambda l: l.superSlam and l.isdonkey),
        Exit("Forest Boss Lobby", lambda l: True),
    ]),

    "Thornvine Hut": Region("Thornvine Hut", False, [
        Location("Forest Donkey Minecart Mayhem", lambda l: l.Slam and l.isdonkey),
    ], [], [
        Exit("Thornvine Area", lambda l: True),
    ]),

    "Worm Area": Region("Worm Area", True, [
        Location("Forest Tiny Beanstalk", lambda l: Events.Bean in l.Events and l.saxophone and l.mini),
        Location("Forest Chunky Apple", lambda l: l.hunkyChunky),
    ], [], [
        Exit("Funky", lambda l: True),
        Exit("Forest Boss Lobby", lambda l: Events.Night in l.Events),
    ]),

    "Forest Boss Lobby": Region("Forest Boss Lobby", True, [], [], [
        # 300 bananas
        Exit("Forest Boss", lambda l: l.ischunky),
    ]),

    "Forest Boss": Region("Forest Boss", False, [
        Location("Forest Boss Key", lambda l: l.hunkyChunky and l.ischunky),
    ], [], []),
}
