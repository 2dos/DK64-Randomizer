from LogicClasses import Region, Location, Event, Exit, Kongs
from Events import Events

Regions = {
    "Creepy Castle Main": Region("Creepy Castle Main", True, [
        Location("Castle Diddy Above Castle", lambda l: l.jetpack and l.isdiddy),
        Location("Castle Lanky Kasplat", lambda l: l.islanky),
        Location("Castle Tiny Kasplat", lambda l: l.istiny),
    ], [], [
        Exit("Creepy Castle Lobby", lambda l: True),
        Exit("Castle Waterfall", lambda l: True),
        Exit("Castle Tree", lambda l: l.blast),
        Exit("Library", lambda l: l.superDuperSlam and l.isdonkey),
        Exit("Ballroom", lambda l: l.superDuperSlam and l.diddy), # Stays open
        Exit("Tower", lambda l: l.superDuperSlam and l.islanky),
        Exit("Greenhouse", lambda l: l.superDuperSlam and l.islanky),
        Exit("Trash Can", lambda l: l.mini and l.istiny),
        Exit("Shed", lambda l: l.punch and l.ischunky),
        Exit("Museum", lambda l: l.superDuperSlam and l.ischunky),
        Exit("Lower Cave", lambda l: True),
        Exit("Upper Cave", lambda l: True),
        Exit("Cranky", lambda l: True),
        Exit("Snide", lambda l: True),
        Exit("Castle Boss Lobby", lambda l: True),
    ]),

    # This region just exists to facilitate the multiple exits from the upper cave
    "Castle Waterfall": Region("Castle Waterfall", False, [], [], [
        Exit("Creepy Castle Main", lambda l: True),
        Exit("Upper Cave", lambda l: True),
    ]),

    "Castle Tree": Region("Castle Tree", False, [
        Location("Castle Donkey Tree", lambda l: l.coconut and l.isdonkey),
        Location("Castle Chunky Tree", lambda l: l.pineapple and l.punch and l.ischunky),
        Location("Castle Donkey Kasplat", lambda l: l.coconut and l.isdonkey),
        Location("Castle Banana Fairy Tree", lambda l: l.camera and l.coconut and l.isdonkey),
    ], [], [
        Exit("Creepy Castle Main", lambda l: True),
    ]),

    "Library": Region("Library", False, [
        # Another case where you're supposed to use Strong Kong but it can be brute forced
        Location("Castle Donkey Library", lambda l: l.superDuperSlam and l.isdonkey),
    ], [], [
        Exit("Creepy Castle Main", lambda l: True),
    ]),

    "Ballroom": Region("Ballroom", False, [
        Location("Castle Diddy Ballroom", lambda l: l.jetpack and l.isdiddy),
        Location("Castle Banana Fairy Ballroom", lambda l: l.camera and l.monkeyport and l.istiny),
    ], [], [
        Exit("Creepy Castle Main", lambda l: True),
        Exit("Castle Tiny Race", lambda l: l.monkeyport and l.mini and l.istiny),
    ]),

    "Castle Tiny Race": Region("Castle Tiny Race", False, [
        Location("Castle Tiny Car Race", lambda l: l.istiny),
    ], [], []),

    "Tower": Region("Tower", False, [
        Location("Castle Lanky Tower", lambda l: l.balloon and l.grape and l.islanky),
    ], [], [
        Exit("Creepy Castle Main", lambda l: True),
    ]),

    "Greenhouse": Region("Greenhouse", False, [
        # Not sure if sprint is actually required
        Location("Castle Lanky Greenhouse", lambda l: l.sprint and l.islanky),
        Location("Castle Battle Arena", lambda l: l.sprint and l.islanky),
    ], [], [
        Exit("Creepy Castle Main", lambda l: True),
    ]),

    "Trash Can": Region("Trash Can", False, [
        Location("Castle Tiny Trash Can", lambda l: l.feather and l.istiny),
    ], [], [
        Exit("Creepy Castle Main", lambda l: True),
    ]),

    "Shed": Region("Shed", False, [
        Location("Castle Chunky Shed", lambda l: l.punch and l.gorillaGone and l.ischunky),
    ], [], [
        Exit("Creepy Castle Main", lambda l: True),
    ]),

    "Museum": Region("Museum", False, [
        Location("Castle Chunky Museum", lambda l: l.punch and l.ischunky),
    ], [], [
        Exit("Creepy Castle Main", lambda l: True),
    ]),

    "Lower Cave": Region("Lower Cave", True, [
        Location("Castle Diddy Kasplat", lambda l: l.isdiddy),
    ], [], [
        Exit("Creepy Castle Main", lambda l: True),
        Exit("Crypt", lambda l: (l.coconut and l.isdonkey) or (l.peanut and l.isdiddy) or (l.pineapple and l.ischunky)),
        Exit("Mausoleum", lambda l: (l.grape and l.islanky) or (l.feather and l.istiny)),
        Exit("Funky", lambda l: True),
        Exit("Castle Boss Lobby", lambda l: True),
    ]),

    "Crypt": Region("Crypt", False, [
        Location("Castle Diddy Crypt", lambda l: l.peanut and l.charge and l.isdiddy),
        Location("Castle Chunky Crypt", lambda l: l.pineapple and l.punch and l.ischunky),
    ], [], [
        Exit("Creepy Castle Main", lambda l: True),
        Exit("Castle Minecarts", lambda l: l.coconut and l.grab and l.isdonkey),
    ]),

    "Castle Minecarts": Region("Castle Minecarts", False, [
        Location("Castle Donkey Minecarts", lambda l: l.isdonkey),
    ], [], []),

    "Mausoleum": Region("Mausoleum", False, [
        Location("Castle Lanky Mausoleum", lambda l: l.grape and l.sprint and l.trombone and l.islanky),
        Location("Castle Tiny Mausoleum", lambda l: l.superDuperSlam and l.twirl and l.istiny),
    ], [], [
        Exit("Creepy Castle Main", lambda l: True),
    ]),

    "Upper Cave": Region("Upper Cave", True, [
        Location("Castle Tiny Over Chasm", lambda l: l.twirl and l.istiny),
        Location("Castle Chunky Kasplat", lambda l: l.ischunky),
    ], [], [
        Exit("Creepy Castle Main", lambda l: True),
        Exit("Castle Waterfall", lambda l: True),
        Exit("Dungeon", lambda l: True),
        Exit("Candy", lambda l: True),
        Exit("Castle Boss Lobby", lambda l: True),
    ]),

    "Dungeon": Region("Dungeon", True, [
        Location("Castle Donkey Dungeon", lambda l: l.superDuperSlam and l.isdonkey),
        Location("Castle Diddy Dungeon", lambda l: l.superDuperSlam and l.peanut and l.isdiddy),
        Location("Castle Lanky Dungeon", lambda l: l.superDuperSlam and l.trombone and l.balloon and l.islanky),
    ], [], [
        Exit("Upper Cave", lambda l: True),
    ]),

    "Castle Boss Lobby": Region("Castle Boss Lobby", True, [], [], [
        # 400 bananas
        Exit("Castle Boss", lambda l: l.islanky),
    ]),

    "Castle Boss": Region("Castle Boss", False, [
        Location("Castle Boss Key", lambda l: True),
    ], [], []),
}
