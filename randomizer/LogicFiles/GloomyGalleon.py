from LogicClasses import Region, Location, Event, Exit
from Enums.Events import Events
from Enums.Regions import Regions

LogicRegions = {
    Regions.GloomyGalleonStart: Region("Gloomy Galleon Start", True, [
        Location("Galleon Chunky Chest", lambda l: l.punch),
        Location("Galleon Tiny Kasplat", lambda l: l.istiny),
        Location("Galleon Battle Arena", lambda l: l.punch),
        Location("Galleon Banana Fairy by Cranky", lambda l: l.camera and l.punch),
    ], [
        Event(Events.GalleonEntered, lambda l: True),
        Event(Events.GalleonLankySwitch, lambda l: l.Slam and l.islanky),
        Event(Events.GalleonTinySwitch, lambda l: l.Slam and l.istiny),
    ], [
        Exit(Regions.GloomyGalleonLobby, lambda l: True),
        Exit(Regions.GalleonBeyondPineappleGate, lambda l: l.pineapple),
        Exit(Regions.LighthouseArea, lambda l: l.coconut),
        Exit(Regions.Shipyard, lambda l: l.peanut),
        Exit(Regions.Cranky, lambda l: True),
        Exit(Regions.GalleonBossLobby, lambda l: True),
    ]),

    Regions.GalleonBeyondPineappleGate: Region("Galleon Beyond Pineapple Gate", False, [
        Location("Galleon Chunky Cannon Game", lambda l: l.ischunky),
        Location("Galleon Lanky Kasplat", lambda l: l.islanky),
    ], [], []),

    Regions.LighthouseArea: Region("Lighthouse Area", True, [
        Location("Gellon Diddy Ship Switch", lambda l: Events.ActivatedLighthouse in l.Events and l.jetpack and l.Slam),
        Location("Galleon Lanky Enguarde Chest", lambda l: Events.LighthouseEnguarde in l.Events and l.islanky),
        Location("Galleon Diddy Kasplat", lambda l: l.isdiddy),
    ], [
        Event(Events.LighthouseEnguarde, lambda l: l.islanky),
        Event(Events.SealReleased, lambda l: l.blast),
        Event(Events.MechafishSummoned, lambda l: l.jetpack and l.guitar),
        Event(Events.GalleonChunkyPad, lambda l: l.triangle),
    ], [
        Exit(Regions.Lighthouse, lambda l: l.Slam and l.isdonkey),
        Exit(Regions.MermaidRoom, lambda l: l.mini and l.istiny),
        Exit(Regions.SickBay, lambda l: Events.ActivatedLighthouse in l.Events and l.Slam and l.ischunky),
        Exit(Regions.Snide, lambda l: True),
        Exit(Regions.GalleonBossLobby, lambda l: Events.LighthouseEnguarde in l.Events),
    ]),

    Regions.Lighthouse: Region("Lighthouse", False, [
        Location("Galleon Donkey Lighthouse", lambda l: Events.ActivatedLighthouse in l.Events)
    ], [
        Event(Events.ActivatedLighthouse, lambda l: l.grab and l.isdonkey),
    ], [
        Exit(Regions.LighthouseArea, lambda l: True),
    ]),

    Regions.MermaidRoom: Region("Mermaid Room", False, [
        Location("Galleon Tiny Pearls", lambda l: Events.PearlsCollected in l.Events and l.istiny),
    ], [], [
        Exit(Regions.LighthouseArea, lambda l: True),
    ]),

    Regions.SickBay: Region("Sick Bay", False, [
        Location("Galleon Chunky Seasick", lambda l: l.punch and l.ischunky),
    ], [], [
        Exit(Regions.LighthouseArea, lambda l: True),
    ]),

    Regions.Shipyard: Region("Shipyard", True, [
        Location("Galleon Donkey Free the Seal", lambda l: Events.SealReleased in l.Events and l.isdonkey),
        Location("Galleon Chunky Kasplat", lambda l: l.ischunky),
    ], [
        Event(Events.ShipyardEnguarde, lambda l: l.islanky),
    ], [
        Exit(Regions.SealRace, lambda l: Events.SealReleased in l.Events and l.isdonkey),
        Exit(Regions.TreasureRoom, lambda l: Events.ShipyardEnguarde in l.Events),
        Exit(Regions.Submarine, lambda l: l.mini and l.istiny),
        Exit(Regions.Mechafish, lambda l: Events.MechafishSummoned in l.Events and l.isdiddy),
        Exit(Regions.LankyShip, lambda l: Events.GalleonLankySwitch in l.Events and l.islanky),
        Exit(Regions.TinyShip, lambda l: Events.GalleonTinySwitch in l.Events and l.istiny),
        Exit(Regions.BongosShip, lambda l: l.bongos and l.isdonkey),
        Exit(Regions.GuitarShip, lambda l: l.guitar and l.isdiddy),
        Exit(Regions.TromboneShip, lambda l: l.trombone and l.islanky),
        Exit(Regions.SaxophoneShip, lambda l: l.saxophone and l.istiny),
        Exit(Regions.TriangleShip, lambda l: Events.GalleonChunkyPad in l.Events and l.ischunky),
        Exit(Regions.Candy, lambda l: True),
        Exit(Regions.Funky, lambda l: True),
        Exit(Regions.GalleonBossLobby, lambda l: True),
    ]),

    Regions.SealRace: Region("Seal Race", False, [
        Location("Donkey Seal Race", lambda l: l.isdonkey),
    ], [], []),

    Regions.TreasureRoom: Region("Treasure Room", True, [
        Location("Galleon Diddy Gold Tower", lambda l: l.spring),
        Location("Galleon Lanky Gold Tower", lambda l: l.balloon),
        Location("Galleon Donkey Kasplat", lambda l: Events.TreasureRoomTeleporterUnlocked in l.Events and l.isdonkey),
    ], [
        Event(Events.TreasureRoomTeleporterUnlocked, lambda l: l.spring),
    ], [
        Exit(Regions.TinyChest, lambda l: l.mini and l.istiny),
    ]),

    Regions.TinyChest: Region("Tiny Chest", False, [], [
        Event(Events.PearlsCollected, lambda l: l.istiny),
    ], [
        Exit(Regions.TreasureRoom, lambda l: True),
    ]),

    Regions.Submarine: Region("Submarine", False, [
        Location("Galleon Tiny Submarine", lambda l: l.istiny),
    ], [], [
        Exit(Regions.Shipyard, lambda l: lambda l: True),
    ]),

    Regions.Mechafish: Region("Mechafish", False, [
        Location("Galleon Diddy Mechafish", lambda l: l.peanut and l.isdiddy),
    ], [], []),

    Regions.LankyShip: Region("Lanky Ship", False, [
        Location("Galleon Lanky 2 Door Ship", lambda l: l.islanky),
    ], [], [
        Exit(Regions.Shipyard, lambda l: True),
    ]),

    Regions.TinyShip: Region("Tiny Ship", False, [
        Location("Galleon Tiny 2 Door Ship", lambda l: l.istiny),
    ], [], [
        Exit(Regions.Shipyard, lambda l: True),
    ]),

    Regions.BongosShip: Region("Bongos Ship", False, [
        Location("Galleon Donkey 5 Door Ship", lambda l: l.isdonkey),
    ], [], [
        Exit(Regions.Shipyard, lambda l: True),
    ]),

    Regions.GuitarShip: Region("Guitar Ship", False, [
        Location("Galleon Diddy 5 Door Ship", lambda l: l.isdiddy),
    ], [], [
        Exit(Regions.Shipyard, lambda l: True),
    ]),

    Regions.TromboneShip: Region("Trombone Ship", False, [
        Location("Galleon Lanky 5 Door Ship", lambda l: l.islanky),
    ], [], [
        Exit(Regions.Shipyard, lambda l: True),
    ]),

    Regions.SaxophoneShip: Region("Saxophone Ship", False, [
        Location("Galleon Tiny 5 Door Ship", lambda l: l.istiny),
        Location("Galleon Banana Fairy 5 Door Ship", lambda l: l.camera),
    ], [], [
        Exit(Regions.Shipyard, lambda l: True),
    ]),

    Regions.TriangleShip: Region("Triangle Ship", False, [
        Location("Galleon Chunky 5 Door Ship", lambda l: l.ischunky),
    ], [], [
        Exit(Regions.Shipyard, lambda l: True),
    ]),

    Regions.GalleonBossLobby: Region("Galleon Boss Lobby", True, [], [], [
        # 250 bananas
        Exit(Regions.GalleonBoss, lambda l: l.islanky),
    ]),

    Regions.GalleonBoss: Region("Galleon Boss", False, [
        Location("Galleon Key", lambda l: l.islanky),
    ], [], []),
}
