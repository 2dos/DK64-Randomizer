from LogicClasses import Region, Location, Event, Exit, Kongs
from Events import Events

Regions = {
    "Start": Region("Start", False, [], [], [
        Exit("Main", lambda l: True),
        Exit("Cranky", lambda l: True),
    ]),

    "Isles Main": Region("Isles Main", True, [
        Location("Isles Donkey Japes Rock", lambda l: Events.KLumsyTalkedTo in l.Events and l.isdonkey),
        Location("Isles Tiny Caged Banana", lambda l: l.feather and l.istiny),
        Location("Isles Tiny Instrument Pad", lambda l: Events.IslesChunkyBarrelSpawn in l.Events and l.istiny),
        Location("Isles Lanky Caged Banana", lambda l: l.grape and l.islanky),
        Location("Isles Chunky Caged Banana", lambda l: l.pineapple and l.ischunky),
        Location("Isles Chunky Pound the X", lambda l: Events.IslesChunkyBarrelSpawn in l.Events and l.hunkyChunky and l.Slam and l.ischunky),
        Location("Isles Banana Fairy Island", lambda l: l.camera),
        Location("Isles Banana Fairy Crocodisle Isle", lambda l: l.camera and l.monkeyport and l.istiny),
    ], [
        Event(Events.IslesDiddyBarrelSpawn, lambda l: l.chunkyAccess and l.trombone and l.islanky),
        Event(Events.IslesChunkyBarrelSpawn, lambda l: l.monkeyport and l.saxophone and l.istiny),
    ], [
        Exit("Prison", lambda l: True),
        Exit("Banana Fairy Room", lambda l: l.mini and l.istiny),
        Exit("Jungle Japes Lobby", lambda l: Events.KLumsyTalkedTo in l.Events),
        Exit("Angry Aztec Lobby", lambda l: Events.FirstKey in l.Events),
        Exit("Crocodile Isle Beyond Lift", lambda l: Events.SecondKey in l.Events),
        Exit("Gloomy Galleon Lobby", lambda l: Events.SecondKey in l.Events),
        Exit("Cabin Island", lambda l: Events.FourthKey in l.Events),
        Exit("Crystal Caves Lobby", lambda l: Events.FifthKey in l.Events),
        Exit("Creepy Castle Lobby", lambda l: Events.FifthKey in l.Events),
        Exit("Hideout Helm Lobby", lambda l: Events.SeventhKey in l.Events and l.monkeyport and l.istiny),
        Exit("K. Rool", lambda l: Events.EigthKey in l.Events),
    ]),

    "Prison": Region("Prison", False, [
        Location("Isles Lanky Prison Orangsprint", lambda l: l.sprint and l.islanky),
    ], [
        Event(Events.KLumsyTalkedTo, lambda l: True),
        Event(Events.FirstKey, lambda l: l.JapesKey),
        Event(Events.SecondKey, lambda l: l.AztecKey),
        Event(Events.FourthKey, lambda l: l.GalleonKey),
        Event(Events.FifthKey, lambda l: l.ForestKey),
        Event(Events.SeventhKey, lambda l: l.CavesKey and l.CastleKey),
        Event(Events.EigthKey, lambda l: l.FactoryKey and l.HelmKey),
    ], [
        Exit("Isles Main", lambda l: True),
    ]),

    "Banana Fairy Room": Region("Banana Fairy Room", False, [
        Location("Camera and Shockwave", lambda l: True),
        Location("Rareware Banana", lambda l: l.BananaFairies >= 20 and l.istiny),
    ], [], [
        Exit("Isles Main", lambda l: True),
    ]),

    "Jungle Japes Lobby": Region("Jungle Japes Lobby", True, [
        Location("Isles Lanky Instrument Pad", lambda l: l.chunkyAccess and l.trombone and l.islanky),
    ], [], [
        Exit("Isles Main", lambda l: True),
        Exit("Jungle Japes Main", lambda l: l.GoldenBananas >= 1),
    ]),

    "Angry Aztec Lobby": Region("Angry Aztec Lobby", True, [
        Location("Isles Tiny Big Bug Bash", lambda l: l.chimpycharge and l.twirl and l.istiny),
    ], [], [
        Exit("Isles Main", lambda l: True),
        Exit("Angry Aztec Start", lambda l: l.GoldenBananas >= 5),
    ]),

    "Crocodile Isle Beyond Lift": Region("Crocodile Isle Beyond Lift", False, [
        Location("Isles Donkey Caged Banana", lambda l: l.coconut and l.isdonkey),
    ], [], [
        Exit("Isles Snide Room", lambda l: True),
        Exit("Frantic Factory Lobby", lambda l: True),
    ]),

    "Isles Snide Room": Region("Isles Snide Room", True, [
        Location("Isles Diddy Snide's Lobby", lambda l: l.spring and l.isdiddy),
        Location("Isles Battle Arena 1", lambda l: l.ischunky),
    ], [], [
        Exit("Crocodile Isle Beyond Lift", lambda l: True),
        Exit("Snide", lambda l: True),
    ]),

    "Frantic Factory Lobby": Region("Frantic Factory Lobby", True, [
        Location("Isles Donkey Instrument Pad", lambda l: l.grab and l.bongos and l.isdonkey),
        Location("Isles Tiny Kasplat", lambda l: l.punch and l.istiny),
        Location("Isles Banana Fairy Factory Lobby", lambda l: l.camera and l.punch),
    ], [], [
        Exit("Crocodile Isle Beyond Lift", lambda l: True),
        Exit("Frantic Factory Start", lambda l: l.GoldenBananas >= 15),
    ]),

    "Gloomy Galleon Lobby": Region("Gloomy Galleon Lobby", True, [
        Location("Isles Tiny Galleon Lobby", lambda l: l.chunkyAccess and l.Slam >= 2 and l.mini and l.istiny),
        Location("Isles Chunky Kasplat", lambda l: l.ischunky),
    ], [], [
        Exit("Isles Main", lambda l: True),
        Exit("Gloomy Galleon Start", lambda l: l.GoldenBananas >= 30),
    ]),

    "Cabin Isle": Region("Cabin Isle", False, [
        Location("Isles Diddy Caged Banana", lambda l: Events.IslesDiddyBarrelSpawn in l.Events and l.jetpack and l.isdiddy),
        Location("Isles Diddy Summit", lambda l:  Events.IslesDiddyBarrelSpawn in l.Events and l.jetpack and l.peanut and l.isdiddy),
    ], [], [
        Exit("Fungi Forest Lobby", lambda l: True),
    ]),

    "Fungi Forest Lobby": Region("Fungi Forest Lobby", True, [
        Location("Isles Battle Arena 2", lambda l: l.coconut and l.peanut and l.grape and l.feather and l.pineapple and l.gorillaGone),
        Location("Isles Banana Fairy Forest Lobby", lambda l: l.camera and l.feather),
    ], [], [
        Exit("Cabin Isle", lambda l: True),
        Exit("Fungi Forest Start", lambda l: l.GoldenBananas >= 50),
    ]),

    "Crystal Caves Lobby": Region("Crystal Caves Lobby", True, [
        Location("Isles Donkey Lava Banana", lambda l: l.punch and l.strongKong and l.isdonkey),
        Location("Isles Diddy Instrument Pad", lambda l: l.jetpack and l.guitar and l.isdiddy),
        Location("Isles Lanky Kasplat", lambda l: l.punch and l.islanky),
    ], [], [
        Exit("Isles Main", lambda l: True),
        Exit("Crystal Caves Main", lambda l: l.GoldenBananas >= 65),
    ]),

    "Creepy Castle Lobby": Region("Creepy Castle Lobby", True, [
        Location("Isles Lanky Castle Lobby", lambda l: l.punch and l.balloon and l.islanky),
        Location("Isles Diddy Kasplat", lambda l: l.coconut and l.diddy),
    ], [], [
        Exit("Isles Main", lambda l: True),
        Exit("Creepy Castle Main", lambda l: l.GoldenBananas >= 80),
    ]),

    "Hideout Helm Lobby": Region("Hideout Helm Lobby", True, [
        Location("Isles Chunky Kremling Kosh", lambda l: l.gorillaGone),
        Location("Isles Donkey Kasplat", lambda l: l.coconut),
    ], [], [
        Exit("Isles Main", lambda l: True),
        Exit("Hideout Helm Start", lambda l: l.gorillaGone and l.GoldenBananas >= 100),
    ]),

    "K. Rool": Region("K. Rool", True, [
        Location("Banana Hoard", lambda l: l.donkeyAccess and l.jetpack and l.peanut and l.diddyAccess and l.trombone and l.lankyAccess and
            l.mini and l.feather and l.tinyAccess and l.Slam >= 2 and l.gorillaGone and l.hunkyChunky and l.chunkyAccess),
    ], [], []),
}
