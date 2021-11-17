from LogicClasses import Region, Location, Event, Exit, Kongs
from Events import Events

Regions = {
    "Gloomy Galleon Start": Region("Gloomy Galleon Start", True, [
        Location("Galleon Chunky Chest", lambda l: l.punch),
        Location("Galleon Tiny Kasplat", lambda l: l.istiny),
        Location("Galleon Battle Arena", lambda l: l.punch),
        Location("Galleon Banana Fairy by Cranky", lambda l: l.camera and l.punch),
    ], [
        Event(Events.GalleonLankySwitch, lambda l: l.Slam and l.islanky),
        Event(Events.GalleonTinySwitch, lambda l: l.Slam and l.istiny),
    ], [
        Exit("Gloomy Galleon Lobby", lambda l: True),
        Exit("Galleon Beyond Pineapple Gate", lambda l: l.pineapple),
        Exit("Lighthouse Area", lambda l: l.coconut),
        Exit("Shipyard", lambda l: l.peanut),
        Exit("Cranky", lambda l: True),
        Exit("Galleon Boss Lobby", lambda l: True),
    ]),

    "Galleon Beyond Pineapple Gate": Region("Galleon Beyond Pineapple Gate", False, [
        Location("Galleon Chunky Cannon Game", lambda l: l.ischunky),
        Location("Galleon Lanky Kasplat", lambda l: l.islanky),
    ], [], []),

    "Lighthouse Area": Region("Lighthouse Area", True, [
        Location("Gellon Diddy Ship Switch", lambda l: Events.ActivatedLighthouse in l.Events and l.jetpack and l.Slam),
        Location("Galleon Lanky Enguarde Chest", lambda l: Events.LighthouseEnguarde in l.Events and l.islanky),
        Location("Galleon Diddy Kasplat", lambda l: l.isdiddy),
    ], [
        Event(Events.LighthouseEnguarde, lambda l: l.islanky),
        Event(Events.SealReleased, lambda l: l.blast),
        Event(Events.MechafishSummoned, lambda l: l.jetpack and l.guitar),
        Event(Events.GalleonChunkyPad, lambda l: l.triangle),
    ], [
        Exit("Lighthouse", lambda l: l.Slam and l.isdonkey),
        Exit("Mermaid Room", lambda l: l.mini and l.istiny),
        Exit("Sick Bay", lambda l: Events.ActivatedLighthouse in l.Events and l.Slam and l.ischunky),
        Exit("Snide", lambda l: True),
        Exit("Galleon Boss Lobby", lambda l: Events.LighthouseEnguarde in l.Events),
    ]),

    "Lighthouse": Region("Lighthouse", False, [
        Location("Galleon Donkey Lighthouse", lambda l: Events.ActivatedLighthouse in l.Events)
    ], [
        Event(Events.ActivatedLighthouse, lambda l: l.grab and l.isdonkey)
    ], [
        Exit("Lighthouse Area", lambda l: True),
    ]),

    "Mermaid Room": Region("Mermaid Room", False, [
        Location("Galleon Tiny Pearls", lambda l: Events.PearlsCollected in l.Events and l.istiny),
    ], [], [
        Exit("Lighthouse Area", lambda l: True),
    ]),

    "Sick Bay": Region("Sick Bay", False, [
        Location("Galleon Chunky Seasick", lambda l: l.punch and l.ischunky),
    ], [], [
        Exit("Lighthouse Area", lambda l: True),
    ]),

    "Shipyard": Region("Shipyard", True, [
        Location("Galleon Donkey Free the Seal", lambda l: Events.SealReleased in l.Events and l.isdonkey),
    ], [
        Event(Events.ShipyardEnguarde, lambda l: l.islanky),
    ], [
        Exit("Seal Race", lambda l: Events.SealReleased in l.Events and l.isdonkey),
        Exit("Treasure Room", lambda l: Events.ShipyardEnguarde in l.Events),
        Exit("Submarine", lambda l: l.mini and l.istiny),
        Exit("Mechafish", lambda l: Events.MechafishSummoned in l.Events and l.isdiddy),
        Exit("Lanky Ship", lambda l: Events.GalleonLankySwitch in l.Events and l.islanky),
        Exit("Tiny Ship", lambda l: Events.GalleonTinySwitch in l.Events and l.istiny),
        Exit("Bongos Ship", lambda l: l.bongos and l.isdonkey),
        Exit("Guitar Ship", lambda l: l.guitar and l.isdiddy),
        Exit("Trombone Ship", lambda l: l.trombone and l.islanky),
        Exit("Saxophone Ship", lambda l: l.saxophone and l.istiny),
        Exit("Triangle Ship", lambda l: Events.GalleonChunkyPad in l.Events and l.ischunky),
        Exit("Candy", lambda l: True),
        Exit("Funky", lambda l: True),
        Exit("Galleon Boss Lobby", lambda l: True),
    ]),

    "Seal Race": Region("Seal Race", False, [
        Location("Donkey Seal Race", lambda l: l.isdonkey),
    ], [], []),

    "Treasure Room": Region("Treasure Room", True, [
        Location("Galleon Diddy Gold Tower", lambda l: l.spring),
        Location("Galleon Lanky Gold Tower", lambda l: l.balloon),
        Location("Galleon Donkey Kasplat", lambda l: Events.TreasureRoomTeleporterUnlocked in l.Events and l.isdonkey),
    ], [
        Event(Events.TreasureRoomTeleporterUnlocked, lambda l: l.spring)
    ], [
        Exit("Tiny Chest", lambda l: l.mini and l.istiny),
    ]),

    "Tiny Chest": Region("Tiny Chest", False, [], [
        Event(Events.PearlsCollected, lambda l: l.istiny)
    ], [
        Exit("Treasure Room", lambda l: True),
    ]),

    "Submarine": Region("Submarine", False, [
        Location("Galleon Tiny Submarine", lambda l: l.istiny),
    ], [], [
        Exit("Shipyard", lambda l: lambda l: True),
    ]),

    "Mechafish": Region("Mechafish", False, [
        Location("Galleon Diddy Mechafish", lambda l: l.peanut and l.isdiddy),
    ], [], []),

    "Lanky Ship": Region("Lanky Ship", False, [
        Location("Galleon Lanky 2 Door Ship", lambda l: l.islanky),
    ], [], [
        Exit("Shipyard", lambda l: True),
    ]),

    "Tiny Ship": Region("Tiny Ship", False, [
        Location("Galleon Tiny 2 Door Ship", lambda l: l.istiny),
    ], [], [
        Exit("Shipyard", lambda l: True),
    ]),

    "Bongos Ship": Region("Bongos Ship", False, [
        Location("Galleon Donkey 5 Door Ship", lambda l: l.isdonkey),
    ], [], [
        Exit("Shipyard", lambda l: True),
    ]),

    "Guitar Ship": Region("Guitar Ship", False, [
        Location("Galleon Diddy 5 Door Ship", lambda l: l.isdiddy),
    ], [], [
        Exit("Shipyard", lambda l: True),
    ]),

    "Trombone Ship": Region("Trombone Ship", False, [
        Location("Galleon Lanky 5 Door Ship", lambda l: l.islanky),
    ], [], [
        Exit("Shipyard", lambda l: True),
    ]),

    "Saxophone Ship": Region("Saxophone Ship", False, [
        Location("Galleon Tiny 5 Door Ship", lambda l: l.istiny),
        Location("Galleon Banana Fairy 5 Door Ship", lambda l: l.camera),
    ], [], [
        Exit("Shipyard", lambda l: True),
    ]),

    "Triangle Ship": Region("Triangle Ship", False, [
        Location("Galleon Chunky 5 Door Ship", lambda l: l.ischunky),
    ], [], [
        Exit("Shipyard", lambda l: True),
    ]),

    "Galleon Boss Lobby": Region("Galleon Boss Lobby", True, [], [], [
        # 250 bananas
        Exit("Galleon Boss", lambda l: l.islanky),
    ]),

    "Galleon Boss": Region("Galleon Boss", False, [
        Location("Galleon Key", lambda l: l.islanky),
    ], [], []),
}
