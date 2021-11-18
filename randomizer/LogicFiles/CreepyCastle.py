from LogicClasses import Region, Location, Event, Exit
from Enums.Events import Events
from Enums.Regions import Regions

LogicRegions = {
    Regions.CreepyCastleMain: Region("Creepy Castle Main", True, [
        Location("Castle Diddy Above Castle", lambda l: l.jetpack and l.isdiddy),
        Location("Castle Lanky Kasplat", lambda l: l.islanky),
        Location("Castle Tiny Kasplat", lambda l: l.istiny),
    ], [
        Event(Events.CastleEntered, lambda l: True),
    ], [
        Exit(Regions.CreepyCastleLobby, lambda l: True),
        Exit(Regions.CastleWaterfall, lambda l: True),
        Exit(Regions.CastleTree, lambda l: l.blast),
        Exit(Regions.Library, lambda l: l.superDuperSlam and l.isdonkey),
        Exit(Regions.Ballroom, lambda l: l.superDuperSlam and l.diddy), # Stays open
        Exit(Regions.Tower, lambda l: l.superDuperSlam and l.islanky),
        Exit(Regions.Greenhouse, lambda l: l.superDuperSlam and l.islanky),
        Exit(Regions.TrashCan, lambda l: l.mini and l.istiny),
        Exit(Regions.Shed, lambda l: l.punch and l.ischunky),
        Exit(Regions.Museum, lambda l: l.superDuperSlam and l.ischunky),
        Exit(Regions.LowerCave, lambda l: True),
        Exit(Regions.UpperCave, lambda l: True),
        Exit(Regions.Cranky, lambda l: True),
        Exit(Regions.Snide, lambda l: True),
        Exit(Regions.CastleBossLobby, lambda l: True),
    ]),

    # This region just exists to facilitate the multiple exits from the upper cave
    Regions.CastleWaterfall: Region("Castle Waterfall", False, [], [], [
        Exit(Regions.CreepyCastleMain, lambda l: True),
        Exit(Regions.UpperCave, lambda l: True),
    ]),

    Regions.CastleTree: Region("Castle Tree", False, [
        Location("Castle Donkey Tree", lambda l: l.coconut and l.isdonkey),
        Location("Castle Chunky Tree", lambda l: l.pineapple and l.punch and l.ischunky),
        Location("Castle Donkey Kasplat", lambda l: l.coconut and l.isdonkey),
        Location("Castle Banana Fairy Tree", lambda l: l.camera and l.coconut and l.isdonkey),
    ], [], [
        Exit(Regions.CreepyCastleMain, lambda l: True),
    ]),

    Regions.Library: Region("Library", False, [
        # Another case where you're supposed to use Strong Kong but it can be brute forced
        Location("Castle Donkey Library", lambda l: l.superDuperSlam and l.isdonkey),
    ], [], [
        Exit(Regions.CreepyCastleMain, lambda l: True),
    ]),

    Regions.Ballroom: Region("Ballroom", False, [
        Location("Castle Diddy Ballroom", lambda l: l.jetpack and l.isdiddy),
        Location("Castle Banana Fairy Ballroom", lambda l: l.camera and l.monkeyport and l.istiny),
    ], [], [
        Exit(Regions.CreepyCastleMain, lambda l: True),
        Exit(Regions.CastleTinyRace, lambda l: l.monkeyport and l.mini and l.istiny),
    ]),

    Regions.CastleTinyRace: Region("Castle Tiny Race", False, [
        Location("Castle Tiny Car Race", lambda l: l.istiny),
    ], [], []),

    Regions.Tower: Region("Tower", False, [
        Location("Castle Lanky Tower", lambda l: l.balloon and l.grape and l.islanky),
    ], [], [
        Exit(Regions.CreepyCastleMain, lambda l: True),
    ]),

    Regions.Greenhouse: Region("Greenhouse", False, [
        # Not sure if sprint is actually required
        Location("Castle Lanky Greenhouse", lambda l: l.sprint and l.islanky),
        Location("Castle Battle Arena", lambda l: l.sprint and l.islanky),
    ], [], [
        Exit(Regions.CreepyCastleMain, lambda l: True),
    ]),

    Regions.TrashCan: Region("Trash Can", False, [
        Location("Castle Tiny Trash Can", lambda l: l.feather and l.istiny),
    ], [], [
        Exit(Regions.CreepyCastleMain, lambda l: True),
    ]),

    Regions.Shed: Region("Shed", False, [
        Location("Castle Chunky Shed", lambda l: l.punch and l.gorillaGone and l.ischunky),
    ], [], [
        Exit(Regions.CreepyCastleMain, lambda l: True),
    ]),

    Regions.Museum: Region("Museum", False, [
        Location("Castle Chunky Museum", lambda l: l.punch and l.ischunky),
    ], [], [
        Exit(Regions.CreepyCastleMain, lambda l: True),
    ]),

    Regions.LowerCave: Region("Lower Cave", True, [
        Location("Castle Diddy Kasplat", lambda l: l.isdiddy),
    ], [], [
        Exit(Regions.CreepyCastleMain, lambda l: True),
        Exit(Regions.Crypt, lambda l: (l.coconut and l.isdonkey) or (l.peanut and l.isdiddy) or (l.pineapple and l.ischunky)),
        Exit(Regions.Mausoleum, lambda l: (l.grape and l.islanky) or (l.feather and l.istiny)),
        Exit(Regions.Funky, lambda l: True),
        Exit(Regions.CastleBossLobby, lambda l: True),
    ]),

    Regions.Crypt: Region("Crypt", False, [
        Location("Castle Diddy Crypt", lambda l: l.peanut and l.charge and l.isdiddy),
        Location("Castle Chunky Crypt", lambda l: l.pineapple and l.punch and l.ischunky),
    ], [], [
        Exit(Regions.LowerCave, lambda l: True),
        Exit(Regions.CastleMinecarts, lambda l: l.coconut and l.grab and l.isdonkey),
    ]),

    Regions.CastleMinecarts: Region("Castle Minecarts", False, [
        Location("Castle Donkey Minecarts", lambda l: l.isdonkey),
    ], [], []),

    Regions.Mausoleum: Region("Mausoleum", False, [
        Location("Castle Lanky Mausoleum", lambda l: l.grape and l.sprint and l.trombone and l.islanky),
        Location("Castle Tiny Mausoleum", lambda l: l.superDuperSlam and l.twirl and l.istiny),
    ], [], [
        Exit(Regions.LowerCave, lambda l: True),
    ]),

    Regions.UpperCave: Region("Upper Cave", True, [
        Location("Castle Tiny Over Chasm", lambda l: l.twirl and l.istiny),
        Location("Castle Chunky Kasplat", lambda l: l.ischunky),
    ], [], [
        Exit(Regions.CreepyCastleMain, lambda l: True),
        Exit(Regions.CastleWaterfall, lambda l: True),
        Exit(Regions.Dungeon, lambda l: True),
        Exit(Regions.Candy, lambda l: True),
        Exit(Regions.CastleBossLobby, lambda l: True),
    ]),

    Regions.Dungeon: Region("Dungeon", True, [
        Location("Castle Donkey Dungeon", lambda l: l.superDuperSlam and l.isdonkey),
        Location("Castle Diddy Dungeon", lambda l: l.superDuperSlam and l.peanut and l.isdiddy),
        Location("Castle Lanky Dungeon", lambda l: l.superDuperSlam and l.trombone and l.balloon and l.islanky),
    ], [], [
        Exit(Regions.UpperCave, lambda l: True),
    ]),

    Regions.CastleBossLobby: Region("Castle Boss Lobby", True, [], [], [
        # 400 bananas
        Exit(Regions.CastleBoss, lambda l: l.islanky),
    ]),

    Regions.CastleBoss: Region("Castle Boss", False, [
        Location("Castle Boss Key", lambda l: True),
    ], [], []),
}
