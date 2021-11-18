from LogicClasses import Region, Location, Event, Exit
from Enums.Events import Events

Regions = {
    "Crystal Caves Main": Region("Crystal Caves Main", True, [
        Location("Caves Donkey Baboon Blast", lambda l: l.blast and l.isdonkey),
        Location("Caves Tiny Krazy Kong Klamour", lambda l: l.mini and l.istiny),
        Location("Caves Tiny Monkeyport Igloo", lambda l: l.monkeyport and l.mini and l.twirl and l.istiny),
        Location("Caves Chunky Gorilla Gone", lambda l: l.punch and l.gorillaGone and l.ischunky),
        Location("Caves Donkey Kasplat", lambda l: l.isdonkey),
        Location("Caves Diddy Kasplat", lambda l: l.mini and l.twirl and l.isdiddy),
        Location("Caves Lanky Kasplat", lambda l: l.jetpack and l.islanky),
        Location("Caves Tiny Kasplat", lambda l: l.istiny),
    ], [
        Event(Events.CavesEntered, lambda l: True),
        Event(Events.CavesSmallBoulderButton, lambda l: l.ischunky),
    ], [
        Exit("Crystal Caves Lobby", lambda l: True),
        Exit("Boulder Igloo", lambda l: l.punch),
        Exit("Caves Lanky Race", lambda l: l.superSlam and l.balloon and l.islanky),
        Exit("Frozen Castle", lambda l: l.superSlam and l.islanky),
        Exit("Igloo Area", lambda l: True),
        Exit("Cabin Area", lambda l: True),
        Exit("Funky", lambda l: True),
        Exit("Cranky", lambda l: True),
        Exit("Snide", lambda l: l.punch),
        Exit("Caves Boss Lobby", lambda l: l.punch),
    ]),

    "Boulder Igloo": Region("Boulder Igloo", True, [], [
        Event(Events.CavesLargeBoulderButton, lambda l: Events.CavesSmallBoulderButton in l.Events and l.hunkyChunky),
    ], [
        Exit("Caves Boss Lobby", lambda l: True),
    ]),

    "Caves Lanky Race": Region("Caves Lanky Race", False, [
        Location("Caves Lanky Beetle Race", lambda l: l.sprint and l.islanky),
    ], [], []),

    "Frozen Castle": Region("Frozen Castle", False, [
        Location("Caves Lanky Castle", lambda l: l.Slam and l.islanky),
    ], [], [
        Exit("Crystal Caves Main", lambda l: True),
    ]),

    "Igloo Area": Region("Igloo Area", True, [
        Location("Caves Chunky Transparent Igloo", lambda l: Events.CavesLargeBoulderButton in l.Events and l.ischunky),
        Location("Caves Chunky Kasplat", lambda l: l.ischunky),
    ], [], [
        Exit("Giant Kosha", lambda l: Events.CavesLargeBoulderButton in l.Events and l.monkeyport and l.istiny),
        Exit("Donkey Igloo", lambda l: l.jetpack and l.bongos and l.isdonkey),
        Exit("Diddy Igloo", lambda l: l.jetpack and l.guitar and l.isdiddy),
        Exit("Lanky Igloo", lambda l: l.jetpack and l.trombone and l.islanky),
        Exit("Tiny Igloo", lambda l: l.jetpack and l.saxophone and l.istiny),
        Exit("Chunky Igloo", lambda l: l.jetpack and l.triangle and l.ischunky),
    ]),

    "Giant Kosha": Region("Giant Kosha", False, [], [
        Event(Events.GiantKoshaDefeated, lambda l: l.shockwave or l.saxophone),
    ], []),

    "Donkey Igloo": Region("Donkey Igloo", False, [
        Location("Caves Donkey 5 Door Igloo", lambda l: l.isdonkey),
    ], [], [
        Exit("Igloo Area", lambda l: True),
    ]),

    "Diddy Igloo": Region("Diddy Igloo", False, [
        Location("Caves Diddy 5 Door Igloo", lambda l: l.isdiddy),
    ], [], [
        Exit("Igloo Area", lambda l: True),
    ]),

    "Lanky Igloo": Region("Lanky Igloo", False, [
        Location("Caves Lanky 5 Door Igloo", lambda l: l.balloon and l.islanky),
    ], [], [
        Exit("Igloo Area", lambda l: True),
    ]),

    "Tiny Igloo": Region("Tiny Igloo", False, [
        Location("Caves Tiny 5 Door Igloo", lambda l: l.Slam and l.istiny),
        Location("Caves Banana Fairy Igloo", lambda l: l.camera),
    ], [], [
        Exit("Igloo Area", lambda l: True),
    ]),

    "Chunky Igloo": Region("Chunky Igloo", False, [
        Location("Caves Chunky 5 Door Igloo", lambda l: l.ischunky),
    ], [], [
        Exit("Igloo Area", lambda l: True),
    ]),

    "Cabin Area": Region("Cabin Area", True, [], [], [
        Exit("Rotating Cabin", lambda l: l.bongos and l.isdonkey),
        Exit("Donkey Cabin", lambda l: l.bongos and l.isdonkey),
        Exit("Diddy Lower Cabin", lambda l: l.guitar and l.isdiddy),
        Exit("Diddy Upper Cabin", lambda l: l.guitar and l.isdiddy),
        Exit("Lanky Cabin", lambda l: l.trombone and l.balloon and l.islanky),
        Exit("Tiny Cabin", lambda l: l.saxophone and l.istiny),
        Exit("Chunky Cabin", lambda l: l.triangle and l.ischunky),
        Exit("Candy", lambda l: True),
        Exit("Caves Boss Lobby", lambda l: l.jetpack or l.balloon),
    ]),

    "Rotating Cabin": Region("Rotating Cabin", False, [
        Location("Caves Donkey Rotating Cabin", lambda l: l.Slam and l.isdonkey),
        Location("Caves Battle Crown", lambda l: l.Slam),
    ], [], [
        Exit("Cabin Area", lambda l: True),
    ]),

    "Donkey Cabin": Region("Donkey Cabin", False, [
        Location("Caves Donkey 5 Door Cabin", lambda l: l.isdonkey),
    ], [], [
        Exit("Cabin Area", lambda l: True),
    ]),

    "Diddy Lower Cabin": Region("Diddy Lower Cabin", False, [
        # You're supposed to use the jetpack to get up the platforms,
        # but you can just backflip onto them
        Location("Caves Donkey 5 Door Cabin", lambda l: l.isdiddy),
    ], [], [
        Exit("Cabin Area", lambda l: True),
    ]),

    "Diddy Upper Cabin": Region("Diddy Upper Cabin", False, [
        Location("Caves Donkey 5 Door Cabin", lambda l: (l.guitar or l.shockwave) and l.spring and l.jetpack and l.isdiddy),
        Location("Caves Banana Fairy Cabin", lambda l: l.camera and (l.guitar or l.shockwave) and l.spring and l.jetpack and l.isdiddy),
    ], [], [
        Exit("Cabin Area", lambda l: True),
    ]),

    "Lanky Cabin": Region("Lanky Cabin", False, [
        Location("Caves Lanky 1 Door Cabin", lambda l: l.sprint and l.balloon and l.islanky),
    ], [], [
        Exit("Cabin Area", lambda l: True),
    ]),

    "Tiny Cabin": Region("Tiny Cabin", False, [
        Location("Caves Tiny 5 Door Cabin", lambda l: l.istiny),
    ], [], [
        Exit("Cabin Area", lambda l: True),
    ]),

    "Chunky Cabin": Region("Chunky Cabin", False, [
        Location("Caves Chunky 5 Door Cabin", lambda l: l.gorillaGone and l.Slam and l.ischunky),
    ], [], [
        Exit("Cabin Area", lambda l: True),
    ]),

    "Caves Boss Lobby": Region("Caves Boss Lobby", True, [], [], [
        # 350 bananas
        Exit("Caves Boss", lambda l: l.isdonkey),
    ]),

    "Caves Boss": Region("Caves Boss", False, [
        Location("Caves Boss Key", lambda l: l.isdonkey),
    ], [], []),
}
