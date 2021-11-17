from LogicClasses import Region, Location, Event, Exit, Kongs
from Events import Events

Regions = {
    "Angry Aztec Start": Region("Angry Aztec Start", True, [], [], [
        Exit("Angry Aztec Lobby", lambda l: True),
        Exit("Temple Start", lambda l: (l.peanut and l.isdiddy) or (l.grape and l.islanky) or (l.feather and l.istiny) or (l.pineapple and l.ischunky)),
        Exit("Angry Aztec Main", lambda l: l.jetpack and l.guitar),
        Exit("Candy", lambda l: True),
        Exit("Aztec Boss Lobby", lambda l: True),
    ]),

    "Temple Start": Region("Temple Start", False, [
        Location("Aztec Tiny Klaptrap Room", lambda l: l.mini and l.istiny),
        Location("Aztec Chunky Klaptrap Room", lambda l: l.triangle and l.ischunky),
    ], [], [
        Exit("Angry Aztec Start", lambda l: True),
        Exit("Temple Underwater", lambda l: l.Slam and l.guitar and l.diddyAccess),
    ]),

    "Temple Underwater": Region("Temple Underwater", False, [
        Location("Tiny Kong", lambda l: l.charge and l.isdiddy),
        Location("Aztec Diddy Free Tiny", lambda l: l.charge and l.isdiddy),
        Location("Aztec Lanky Vulture", lambda l: l.Slam and l.grape and l.islanky),
        Location("Aztec Battle Arena", lambda l: l.Slam and l.grape and l.islanky),
    ], [], []),

    "Angry Aztec Main": Region("Angry Aztec Main", True, [
        Location("Aztec Donkey Stealthy Snoop", lambda l: Events.AztecDonkeySwitch in l.Events and l.strongKong and l.isdonkey),
        Location("Aztec Diddy Ram Gongs", lambda l: l.charge and l.jetpack and l.isdiddy),
        Location("Aztec Diddy Vulture Race", lambda l: l.jetpack and l.isdiddy),
        Location("Aztec Chunky Busy Barrel Barrage", lambda l: l.hunkyChunky and l.ischunky),
        Location("Aztec Tiny Kasplat", lambda l: l.istiny),
    ], [
        Event(Events.FedTotem, lambda l: l.jetpack and l.peanut),
        Event(Events.LlamaFreed, lambda l: l.blast),
    ], [
        Exit("Donkey Temple", lambda l: Events.FedTotem in l.Events and l.coconut and l.isdonkey),
        Exit("Diddy Temple", lambda l: Events.FedTotem in l.Events and l.peanut and l.isdiddy),
        Exit("Lanky Temple", lambda l: Events.FedTotem in l.Events and l.grape and l.islanky),
        Exit("Tiny Temple", lambda l: Events.FedTotem in l.Events and l.feather and l.istiny),
        Exit("Chunky Temple", lambda l: Events.FedTotem in l.Events and l.pineapple and l.ischunky),
        Exit("Aztec Tiny Race", lambda l: l.charge and l.jetpack and l.mini and l.saxophone and l.istiny),
        Exit("Llama Temple", lambda l: Events.LlamaFreed in l.Events and ((l.coconut and l.isdonkey) or (l.grape and l.islanky) or (l.feather and l.istiny))),
    ]),

    "Donkey Temple": Region("Donkey Temple", False, [
        Location("Aztec Donkey 5 Door Temple", lambda l: l.coconut and l.isdonkey),
    ], [], [
        Exit("Angry Aztec Main", lambda l: True),
    ]),

    "Diddy Temple": Region("Diddy Temple", False, [
        Location("Aztec Diddy 5 Door Temple", lambda l: l.peanut and l.isdiddy),
    ], [], [
        Exit("Angry Aztec Main", lambda l: True),
    ]),

    "Lanky Temple": Region("Lanky Temple", False, [
        Location("Aztec Lanky 5 Door Temple", lambda l: l.grape and l.islanky),
    ], [], [
        Exit("Angry Aztec Main", lambda l: True),
    ]),

    "Tiny Temple": Region("Tiny Temple", False, [
        Location("Aztec Tiny 5 Door Temple", lambda l: l.feather and l.istiny),
        Location("Aztec Banana Fairy Tiny Temple", lambda l: l.camera and l.feather and l.mini and l.istiny),
    ], [], [
        Exit("Angry Aztec Main", lambda l: True),
    ]),

    "Chunky Temple": Region("Chunky Temple", False, [
        Location("Aztec Chunky 5 Door Temple", lambda l: l.pineapple and l.ischunky),
        Location("Aztec Chunky Kasplat", lambda l: l.pineapple and l.ischunky),
    ], [], [
        Exit("Angry Aztec Main", lambda l: True),
    ]),

    "Aztec Tiny Race": Region("Aztec Tiny Race", False, [
        Location("Aztec Tiny Beetle Race", lambda l: l.istiny),
    ], [], []),

    "Llama Temple": Region("Llama Temple", True, [
        Location("Lanky Kong", lambda l: l.bongos and l.isdonkey),
        Location("Aztec Donkey Free Lanky", lambda l: l.bongos and l.isdonkey),
        Location("Aztec Lanky Teetering Turtle Trouble", lambda l: l.trombone and l.islanky),
        Location("Aztec Lanky Matching Game", lambda l: l.grape and l.Slam and l.islanky),
        Location("Aztec Banana Fairy Llama Temple", lambda l: l.camera),
    ], [
        Event(Events.AztecDonkeySwitch, lambda l: l.Slam and l.isdonkey),
    ], [
        Exit("Angry Aztec Main", lambda l: True),
        Exit("Llama Temple Back", lambda l: l.mini),
    ]),

    "Llama Temple Back": Region("Llama Temple Back", False, [
        Location("Aztec Tiny Llama Temple", lambda l: l.Slam and l.twirl and l.istiny),
        Location("Aztec Lanky Kasplat", lambda l: l.islanky),
    ], [], []),

    "Aztec Boss Lobby": Region("Aztec Boss Lobby", True, [], [], [
        # 120 bananas
        Exit("Aztec Boss", lambda l: l.isdiddy),
    ]),

    "Aztec Boss": Region("Aztec Boss", False, [
        Location("Aztec Key", lambda l: l.isdiddy),
    ], [], []),
}
