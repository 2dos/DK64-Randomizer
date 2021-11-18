from LogicClasses import Region, Location, Event, Exit
from Enums.Events import Events

Regions = {
    "Frantic Factory Start": Region("Frantic Factory Start", False, [], [
        Event(Events.FactoryEntered, lambda l: True),
    ], [
        Exit("Frantic Factory Lobby", lambda l: True),
        Exit("Testing", lambda l: Events.TestingGateOpened in l.Events),
        Exit("Beyond Hatch", lambda l: l.Slam),
    ]),

    "Testing": Region("Testing", True, [
        Location("Factory Donkey Number Game", lambda l: l.Slam and l.isdonkey),
        Location("Factory Diddy Block Tower", lambda l: l.spring and l.isdiddy),
        Location("Factory Lanky Batty Barrel Bandit", lambda l: l.balloon and l.islanky),
        Location("Factory Tiny Dartboard", lambda l: Events.DartsPlayed in l.Events and l.istiny),
        Location("Factory Chunky Kasplat", lambda l: l.ischunky),
        Location("Factory Banana Fairy by Counting", lambda l: l.camera),
        Location("Factory Banana Fairy by Funky", lambda l: l.camera and Events.DartsPlayed in l.Events),
    ], [
        Event(Events.DartsPlayed, lambda l: l.Slam and l.mini and l.feather),
    ], [
        Exit("R&D", lambda l: True),
        Exit("Snide", lambda l: True),
        Exit("Funky", lambda l: Events.DartsPlayed in l.Events),
        Exit("Factory Boss Lobby", lambda l: True),
    ]),

    "R&D": Region("R&D", True, [
        Location("Factory Diddy R&D", lambda l: l.guitar and l.charge and l.isdiddy),
        Location("Factory Lanky R&D", lambda l: l.trombone and l.Slam and l.islanky),
        Location("Factory Chunky R&D", lambda l: l.triangle and l.punch and l.hunkyChunky and l.ischunky),
        Location("Factory Lanky Kasplat", lambda l: l.islanky),
        Location("Factory Battle Arena", lambda l: l.grab),
    ], [], [
        Exit("Factory Tiny Race", lambda l: l.mini and l.istiny),
        Exit("Chunky Room Platform", lambda l: True),
        Exit("Factory Boss Lobby", lambda l: True),
    ]),

    "Factory Tiny Race": Region("Factory Tiny Race", False, [
        Location("Factory Tiny Car Race", lambda l: l.istiny),
    ], [], []),

    "Chunky Room Platform": Region("Chunky Room Platform", False, [
        Location("Factory Diddy Beaver Bother", lambda l: l.Slam and l.isdiddy),
    ], [], [
        Exit("Power Hut", lambda l: True),
        Exit("Beyond Hatch", lambda l: True),
    ]),

    "Power Hut": Region("Power Hut", False, [
        Location("Factory Donkey Power Hut", lambda l: Events.MainCoreActivated in l.Events and l.isdonkey),
    ], [
        Event(Events.MainCoreActivated, lambda l: l.coconut and l.grab and l.isdonkey),
    ], [
        Exit("Chunky Room Platform", lambda l: True),
    ]),

    "Beyond Hatch": Region("Beyond Hatch", True, [
        Location("Chunky Kong", lambda l: l.handstand and l.Slam and l.islanky),
        Location("Nintendo Coin", lambda l: Events.ArcadeLeverSpawned in l.Events and l.grab),
        Location("Factory Donkey DK Arcade", lambda l: Events.ArcadeLeverSpawned in l.Events and l.grab),
        Location("Factory Lanky Free Chunky", lambda l: l.handstand and l.Slam and l.islanky),
        Location("Factory Tiny by Arcade", lambda l: l.mini and l.istiny),
        Location("Factory Chunky Dark Room", lambda l: l.punch and l.Slam and l.ischunky),
        Location("Factory Chunky Stash Snatch", lambda l: l.punch and l.ischunky),
        Location("Factory Tiny Kasplat", lambda l: l.istiny),
    ], [
        Events(Events.ArcadeLeverSpawned, lambda l: l.blast and l.isdonkey),
        Events(Events.TestingGateOpened, lambda l: l.Slam),
        Events(Events.DiddyCoreSwitch, lambda l: l.Slam and l.isdiddy),
        Events(Events.LankyCoreSwitch, lambda l: l.Slam and l.islanky),
        Events(Events.TinyCoreSwitch, lambda l: l.Slam and l.istiny),
        Events(Events.ChunkyCoreSwitch, lambda l: l.Slam and l.ischunky),
    ], [
        Exit("Inside Core", lambda l: Events.MainCoreActivated in l.Events),
        Exit("Main Core", lambda l: Events.MainCoreActivated in l.Events),
        Exit("Cranky", lambda l: True),
        Exit("Candy", lambda l: True),
        Exit("Factory Boss Lobby", lambda l: True),
    ]),

    "Inside Core": Region("Inside Core", False, [
        Location("Factory Donkey Crusher Room", lambda l: l.strongKong and l.isdonkey),
    ], [], [
        Exit("Beyond Hatch", lambda l: True),
    ]),

    "Main Core": Region("Main Core", True, [
        Location("Factory Diddy Production Room", lambda l: Events.DiddyCoreSwitch in l.Events and l.spring and l.isdiddy),
        Location("Factory Lanky Production Room", lambda l: Events.LankyCoreSwitch in l.Events and l.handstand and l.islanky),
        Location("Factory Tiny Production Room", lambda l: Events.TinyCoreSwitch in l.Events and l.twirl and l.istiny),
        Location("Factory Chunky Production Room", lambda l: Events.ChunkyCoreSwitch in l.Events and l.ischunky),
    ], [], []),

    "Factory Boss Lobby": Region("Factory Boss Lobby", False, [], [], [
        # 200 bananas
        Exit("Factory Boss", lambda l: l.istiny),
    ]),

    "Factory Boss": Region("Factory Boss", False, [
        Location("Factory Boss Key", lambda l: l.twirl and l.istiny),
    ], [], []),
}
