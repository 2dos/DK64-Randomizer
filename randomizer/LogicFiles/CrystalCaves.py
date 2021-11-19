from LogicClasses import Region, Location, Event, Exit
from Enums.Events import Events
from Enums.Regions import Regions

LogicRegions = {
    Regions.CrystalCavesMain: Region("Crystal Caves Main", True, [
        Location("Caves Donkey Baboon Blast", lambda l: l.blast and l.isdonkey),
        Location("Caves Diddy Jetpack Barrel", lambda l: l.jetpack and l.isdiddy),
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
        Exit(Regions.CrystalCavesLobby, lambda l: True),
        Exit(Regions.BoulderIgloo, lambda l: l.punch),
        Exit(Regions.CavesLankyRace, lambda l: l.superSlam and l.balloon and l.islanky),
        Exit(Regions.FrozenCastle, lambda l: l.superSlam and l.islanky),
        Exit(Regions.IglooArea, lambda l: True),
        Exit(Regions.CabinArea, lambda l: True),
        Exit(Regions.Funky, lambda l: True),
        Exit(Regions.Cranky, lambda l: True),
        Exit(Regions.Snide, lambda l: l.punch),
        Exit(Regions.CavesBossLobby, lambda l: l.punch),
    ]),

    Regions.BoulderIgloo: Region("Boulder Igloo", True, [], [
        Event(Events.CavesLargeBoulderButton, lambda l: Events.CavesSmallBoulderButton in l.Events and l.hunkyChunky),
    ], [
        Exit(Regions.CavesBossLobby, lambda l: True),
    ]),

    Regions.CavesLankyRace: Region("Caves Lanky Race", False, [
        Location("Caves Lanky Beetle Race", lambda l: l.sprint and l.islanky),
    ], [], []),

    Regions.FrozenCastle: Region("Frozen Castle", False, [
        Location("Caves Lanky Castle", lambda l: l.Slam and l.islanky),
    ], [], [
        Exit(Regions.CrystalCavesMain, lambda l: True),
    ]),

    Regions.IglooArea: Region("Igloo Area", True, [
        Location("Caves Chunky Transparent Igloo", lambda l: Events.CavesLargeBoulderButton in l.Events and l.ischunky),
        Location("Caves Chunky Kasplat", lambda l: l.ischunky),
    ], [], [
        Exit(Regions.GiantKosha, lambda l: Events.CavesLargeBoulderButton in l.Events and l.monkeyport and l.istiny),
        Exit(Regions.DonkeyIgloo, lambda l: l.jetpack and l.bongos and l.isdonkey),
        Exit(Regions.DiddyIgloo, lambda l: l.jetpack and l.guitar and l.isdiddy),
        Exit(Regions.LankyIgloo, lambda l: l.jetpack and l.trombone and l.islanky),
        Exit(Regions.TinyIgloo, lambda l: l.jetpack and l.saxophone and l.istiny),
        Exit(Regions.ChunkyIgloo, lambda l: l.jetpack and l.triangle and l.ischunky),
    ]),

    Regions.GiantKosha: Region("Giant Kosha", False, [], [
        Event(Events.GiantKoshaDefeated, lambda l: l.shockwave or l.saxophone),
    ], []),

    Regions.DonkeyIgloo: Region("Donkey Igloo", False, [
        Location("Caves Donkey 5 Door Igloo", lambda l: l.isdonkey),
    ], [], [
        Exit(Regions.IglooArea, lambda l: True),
    ]),

    Regions.DiddyIgloo: Region("Diddy Igloo", False, [
        Location("Caves Diddy 5 Door Igloo", lambda l: l.isdiddy),
    ], [], [
        Exit(Regions.IglooArea, lambda l: True),
    ]),

    Regions.LankyIgloo: Region("Lanky Igloo", False, [
        Location("Caves Lanky 5 Door Igloo", lambda l: l.balloon and l.islanky),
    ], [], [
        Exit(Regions.IglooArea, lambda l: True),
    ]),

    Regions.TinyIgloo: Region("Tiny Igloo", False, [
        Location("Caves Tiny 5 Door Igloo", lambda l: l.Slam and l.istiny),
        Location("Caves Banana Fairy Igloo", lambda l: l.camera),
    ], [], [
        Exit(Regions.IglooArea, lambda l: True),
    ]),

    Regions.ChunkyIgloo: Region("Chunky Igloo", False, [
        Location("Caves Chunky 5 Door Igloo", lambda l: l.ischunky),
    ], [], [
        Exit(Regions.IglooArea, lambda l: True),
    ]),

    Regions.CabinArea: Region("Cabin Area", True, [], [], [
        Exit(Regions.RotatingCabin, lambda l: l.bongos and l.isdonkey),
        Exit(Regions.DonkeyCabin, lambda l: l.bongos and l.isdonkey),
        Exit(Regions.DiddyLowerCabin, lambda l: l.guitar and l.isdiddy),
        Exit(Regions.DiddyUpperCabin, lambda l: l.guitar and l.isdiddy),
        Exit(Regions.LankyCabin, lambda l: l.trombone and l.balloon and l.islanky),
        Exit(Regions.TinyCabin, lambda l: l.saxophone and l.istiny),
        Exit(Regions.ChunkyCabin, lambda l: l.triangle and l.ischunky),
        Exit(Regions.Candy, lambda l: True),
        Exit(Regions.CavesBossLobby, lambda l: l.jetpack or l.balloon),
    ]),

    Regions.RotatingCabin: Region("Rotating Cabin", False, [
        Location("Caves Donkey Rotating Cabin", lambda l: l.Slam and l.isdonkey),
        Location("Caves Battle Crown", lambda l: l.Slam),
    ], [], [
        Exit(Regions.CabinArea, lambda l: True),
    ]),

    Regions.DonkeyCabin: Region("Donkey Cabin", False, [
        Location("Caves Donkey 5 Door Cabin", lambda l: l.isdonkey),
    ], [], [
        Exit(Regions.CabinArea, lambda l: True),
    ]),

    Regions.DiddyLowerCabin: Region("Diddy Lower Cabin", False, [
        # You're supposed to use the jetpack to get up the platforms,
        # but you can just backflip onto them
        Location("Caves Diddy 5 Door Cabin Lower", lambda l: l.isdiddy),
    ], [], [
        Exit(Regions.CabinArea, lambda l: True),
    ]),

    Regions.DiddyUpperCabin: Region("Diddy Upper Cabin", False, [
        Location("Caves Diddy 5 Door Cabin Upper", lambda l: (l.guitar or l.shockwave) and l.spring and l.jetpack and l.isdiddy),
        Location("Caves Banana Fairy Cabin", lambda l: l.camera and (l.guitar or l.shockwave) and l.spring and l.jetpack and l.isdiddy),
    ], [], [
        Exit(Regions.CabinArea, lambda l: True),
    ]),

    Regions.LankyCabin: Region("Lanky Cabin", False, [
        Location("Caves Lanky 1 Door Cabin", lambda l: l.sprint and l.balloon and l.islanky),
    ], [], [
        Exit(Regions.CabinArea, lambda l: True),
    ]),

    Regions.TinyCabin: Region("Tiny Cabin", False, [
        Location("Caves Tiny 5 Door Cabin", lambda l: l.istiny),
    ], [], [
        Exit(Regions.CabinArea, lambda l: True),
    ]),

    Regions.ChunkyCabin: Region("Chunky Cabin", False, [
        Location("Caves Chunky 5 Door Cabin", lambda l: l.gorillaGone and l.Slam and l.ischunky),
    ], [], [
        Exit(Regions.CabinArea, lambda l: True),
    ]),

    Regions.CavesBossLobby: Region("Caves Boss Lobby", True, [], [], [
        # 350 bananas
        Exit(Regions.CavesBoss, lambda l: l.isdonkey),
    ]),

    Regions.CavesBoss: Region("Caves Boss", False, [
        Location("Caves Key", lambda l: l.isdonkey),
    ], [], []),
}
