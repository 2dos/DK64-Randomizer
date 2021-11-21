from LogicClasses import Region, Location, Event, Exit
from Enums.Events import Events
from Enums.Regions import Regions

LogicRegions = {
    Regions.Start: Region("Start", True, [], [], [
        Exit(Regions.IslesMain, lambda l: True),
        Exit(Regions.Cranky, lambda l: True),
    ]),

    Regions.IslesMain: Region("Isles Main", True, [
        Location("Isles Donkey Japes Rock", lambda l: Events.KLumsyTalkedTo in l.Events and l.isdonkey),
        Location("Isles Tiny Caged Banana", lambda l: l.feather and l.istiny),
        Location("Isles Tiny Instrument Pad", lambda l: Events.IslesChunkyBarrelSpawn in l.Events and l.istiny),
        Location("Isles Lanky Caged Banana", lambda l: l.grape and l.islanky),
        Location("Isles Chunky Caged Banana", lambda l: l.pineapple and l.ischunky),
        Location("Isles Chunky Instrument Pad", lambda l: l.triangle and l.ischunky),
        Location("Isles Chunky Pound the X", lambda l: Events.IslesChunkyBarrelSpawn in l.Events and l.hunkyChunky and l.Slam and l.ischunky),
        Location("Isles Banana Fairy Island", lambda l: l.camera),
        Location("Isles Banana Fairy Crocodisle Isle", lambda l: l.camera and l.monkeyport and l.istiny),
    ], [
        Event(Events.IslesDiddyBarrelSpawn, lambda l: l.chunkyAccess and l.trombone and l.islanky),
        Event(Events.IslesChunkyBarrelSpawn, lambda l: l.monkeyport and l.saxophone and l.istiny),
    ], [
        Exit(Regions.Prison, lambda l: True),
        Exit(Regions.BananaFairyRoom, lambda l: l.mini and l.istiny),
        Exit(Regions.JungleJapesLobby, lambda l: Events.KLumsyTalkedTo in l.Events),
        Exit(Regions.AngryAztecLobby, lambda l: True),
        Exit(Regions.CrocodileIsleBeyondLift, lambda l: True),
        Exit(Regions.GloomyGalleonLobby, lambda l: True),
        Exit(Regions.CabinIsle, lambda l: True),
        Exit(Regions.CrystalCavesLobby, lambda l: True),
        Exit(Regions.CreepyCastleLobby, lambda l: True),
        Exit(Regions.HideoutHelmLobby, lambda l: True and l.monkeyport and l.istiny),
        Exit(Regions.KRool, lambda l: Events.EigthKey in l.Events),
    ]),

    Regions.Prison: Region("Prison", False, [
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
        Exit(Regions.IslesMain, lambda l: True),
    ]),

    Regions.BananaFairyRoom: Region("Banana Fairy Room", False, [
        Location("Camera and Shockwave", lambda l: True),
        Location("Rareware Banana", lambda l: l.BananaFairies >= 20 and l.istiny),
    ], [], [
        Exit(Regions.IslesMain, lambda l: True),
    ]),

    Regions.JungleJapesLobby: Region("Jungle Japes Lobby", True, [
        Location("Isles Lanky Instrument Pad", lambda l: l.chunkyAccess and l.trombone and l.islanky),
    ], [], [
        Exit(Regions.IslesMain, lambda l: True),
        Exit(Regions.JungleJapesMain, lambda l: True),
    ]),

    Regions.AngryAztecLobby: Region("Angry Aztec Lobby", True, [
        Location("Isles Tiny Big Bug Bash", lambda l: l.charge and l.twirl and l.istiny),
    ], [], [
        Exit(Regions.IslesMain, lambda l: True),
        Exit(Regions.AngryAztecStart, lambda l: True),
    ]),

    Regions.CrocodileIsleBeyondLift: Region("Crocodile Isle Beyond Lift", False, [
        Location("Isles Donkey Caged Banana", lambda l: l.coconut and l.isdonkey),
    ], [], [
        Exit(Regions.IslesSnideRoom, lambda l: True),
        Exit(Regions.FranticFactoryLobby, lambda l: True),
    ]),

    Regions.IslesSnideRoom: Region("Isles Snide Room", True, [
        Location("Isles Diddy Snide's Lobby", lambda l: l.spring and l.isdiddy),
        Location("Isles Battle Arena 1", lambda l: l.ischunky),
    ], [], [
        Exit(Regions.CrocodileIsleBeyondLift, lambda l: True),
        Exit(Regions.Snide, lambda l: True),
    ]),

    Regions.FranticFactoryLobby: Region("Frantic Factory Lobby", True, [
        Location("Isles Donkey Instrument Pad", lambda l: l.grab and l.bongos and l.isdonkey),
        Location("Isles Tiny Kasplat", lambda l: l.punch and l.istiny),
        Location("Isles Banana Fairy Factory Lobby", lambda l: l.camera and l.punch),
    ], [], [
        Exit(Regions.CrocodileIsleBeyondLift, lambda l: True),
        Exit(Regions.FranticFactoryStart, lambda l: True),
    ]),

    Regions.GloomyGalleonLobby: Region("Gloomy Galleon Lobby", True, [
        Location("Isles Tiny Galleon Lobby", lambda l: l.chunkyAccess and l.superSlam and l.mini and l.istiny),
        Location("Isles Chunky Kasplat", lambda l: l.ischunky),
    ], [], [
        Exit(Regions.IslesMain, lambda l: True),
        Exit(Regions.GloomyGalleonStart, lambda l: True),
    ]),

    Regions.CabinIsle: Region("Cabin Isle", False, [
        Location("Isles Diddy Caged Banana", lambda l: Events.IslesDiddyBarrelSpawn in l.Events and l.jetpack and l.isdiddy),
        Location("Isles Diddy Summit", lambda l:  Events.IslesDiddyBarrelSpawn in l.Events and l.jetpack and l.peanut and l.isdiddy),
    ], [], [
        Exit(Regions.FungiForestLobby, lambda l: True),
    ]),

    Regions.FungiForestLobby: Region("Fungi Forest Lobby", True, [
        Location("Isles Battle Arena 2", lambda l: l.coconut and l.peanut and l.grape and l.feather and l.pineapple and l.gorillaGone),
        Location("Isles Banana Fairy Forest Lobby", lambda l: l.camera and l.feather),
    ], [], [
        Exit(Regions.CabinIsle, lambda l: True),
        Exit(Regions.FungiForestStart, lambda l: True),
    ]),

    Regions.CrystalCavesLobby: Region("Crystal Caves Lobby", True, [
        Location("Isles Donkey Lava Banana", lambda l: l.punch and l.strongKong and l.isdonkey),
        Location("Isles Diddy Instrument Pad", lambda l: l.jetpack and l.guitar and l.isdiddy),
        Location("Isles Lanky Kasplat", lambda l: l.punch and l.islanky),
    ], [], [
        Exit(Regions.IslesMain, lambda l: True),
        Exit(Regions.CrystalCavesMain, lambda l: True),
    ]),

    Regions.CreepyCastleLobby: Region("Creepy Castle Lobby", True, [
        Location("Isles Lanky Castle Lobby", lambda l: l.punch and l.balloon and l.islanky),
        Location("Isles Diddy Kasplat", lambda l: l.coconut and l.diddy),
    ], [], [
        Exit(Regions.IslesMain, lambda l: True),
        Exit(Regions.CreepyCastleMain, lambda l: True),
    ]),

    Regions.HideoutHelmLobby: Region("Hideout Helm Lobby", True, [
        Location("Isles Chunky Kremling Kosh", lambda l: l.gorillaGone),
        Location("Isles Donkey Kasplat", lambda l: l.coconut),
    ], [], [
        Exit(Regions.IslesMain, lambda l: True),
        Exit(Regions.HideoutHelmStart, lambda l: l.gorillaGone),
    ]),

    Regions.KRool: Region("K. Rool", True, [
        Location("Banana Hoard", lambda l: l.donkeyAccess and l.jetpack and l.peanut and l.diddyAccess and l.trombone and l.lankyAccess and
            l.mini and l.feather and l.tinyAccess and l.superSlam and l.gorillaGone and l.hunkyChunky and l.chunkyAccess),
    ], [], []),
}
