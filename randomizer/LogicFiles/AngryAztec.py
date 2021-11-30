# fmt: off

from LogicClasses import Region, Location, Event, Exit
from Enums.Events import Events
from Enums.Regions import Regions
from Enums.Levels import Levels

LogicRegions = {
    Regions.AngryAztecStart: Region("Angry Aztec Start", Levels.AngryAztec, True, [
        Location("Aztec Donkey Free Llama", lambda l: Events.LlamaFreed in l.Events and l.isdonkey),
        Location("Aztec Chunky Vases", lambda l: l.pineapple and l.ischunky),
        Location("Aztec Donkey Kasplat", lambda l: l.coconut and l.strongKong and l.isdonkey),
        Location("Aztec Diddy Kasplat", lambda l: l.jetpack and l.isdiddy),
    ], [
        Event(Events.AztecEntered, lambda l: True),
    ], [
        Exit(Regions.AngryAztecLobby, lambda l: True),
        Exit(Regions.TempleStart, lambda l: (l.peanut and l.isdiddy) or (l.grape and l.islanky) or (l.feather and l.istiny) or (l.pineapple and l.ischunky)),
        Exit(Regions.AngryAztecMain, lambda l: l.jetpack and l.guitar),
        Exit(Regions.Candy, lambda l: True),
        Exit(Regions.AztecBossLobby, lambda l: True),
    ]),

    Regions.TempleStart: Region("Temple Start", Levels.AngryAztec, False, [
        Location("Aztec Tiny Klaptrap Room", lambda l: l.mini and l.istiny),
        Location("Aztec Chunky Klaptrap Room", lambda l: l.triangle and l.ischunky),
    ], [], [
        Exit(Regions.AngryAztecStart, lambda l: True),
        Exit(Regions.TempleUnderwater, lambda l: l.Slam and l.guitar and l.diddyAccess),
    ]),

    Regions.TempleUnderwater: Region("Temple Underwater", Levels.AngryAztec, False, [
        Location("Tiny Kong", lambda l: l.charge and l.isdiddy),
        Location("Aztec Diddy Free Tiny", lambda l: l.charge and l.isdiddy),
        Location("Aztec Lanky Vulture", lambda l: l.Slam and l.grape and l.islanky),
        Location("Aztec Battle Arena", lambda l: l.Slam and l.grape and l.islanky),
    ], [], []),

    Regions.AngryAztecMain: Region("Angry Aztec Main", Levels.AngryAztec, True, [
        Location("Aztec Donkey Stealthy Snoop", lambda l: Events.AztecDonkeySwitch in l.Events and l.strongKong and l.isdonkey),
        Location("Aztec Diddy Ram Gongs", lambda l: l.charge and l.jetpack and l.isdiddy),
        Location("Aztec Diddy Vulture Race", lambda l: l.jetpack and l.isdiddy),
        Location("Aztec Chunky Busy Barrel Barrage", lambda l: l.hunkyChunky and l.ischunky),
        Location("Aztec Tiny Kasplat", lambda l: l.istiny),
    ], [
        Event(Events.FedTotem, lambda l: l.jetpack and l.peanut),
        Event(Events.LlamaFreed, lambda l: l.blast),
    ], [
        Exit(Regions.DonkeyTemple, lambda l: Events.FedTotem in l.Events and l.coconut and l.isdonkey),
        Exit(Regions.DiddyTemple, lambda l: Events.FedTotem in l.Events and l.peanut and l.isdiddy),
        Exit(Regions.LankyTemple, lambda l: Events.FedTotem in l.Events and l.grape and l.islanky),
        Exit(Regions.TinyTemple, lambda l: Events.FedTotem in l.Events and l.feather and l.istiny),
        Exit(Regions.ChunkyTemple, lambda l: Events.FedTotem in l.Events and l.pineapple and l.ischunky),
        Exit(Regions.AztecTinyRace, lambda l: l.charge and l.jetpack and l.mini and l.saxophone and l.istiny),
        Exit(Regions.LlamaTemple, lambda l: Events.LlamaFreed in l.Events and ((l.coconut and l.isdonkey) or (l.grape and l.islanky) or (l.feather and l.istiny))),
    ]),

    Regions.DonkeyTemple: Region("Donkey Temple", Levels.AngryAztec, False, [
        Location("Aztec Donkey 5 Door Temple", lambda l: l.coconut and l.isdonkey),
    ], [], [
        Exit(Regions.AngryAztecMain, lambda l: True),
    ]),

    Regions.DiddyTemple: Region("Diddy Temple", Levels.AngryAztec, False, [
        Location("Aztec Diddy 5 Door Temple", lambda l: l.peanut and l.isdiddy),
    ], [], [
        Exit(Regions.AngryAztecMain, lambda l: True),
    ]),

    Regions.LankyTemple: Region("Lanky Temple", Levels.AngryAztec, False, [
        Location("Aztec Lanky 5 Door Temple", lambda l: l.grape and l.islanky),
    ], [], [
        Exit(Regions.AngryAztecMain, lambda l: True),
    ]),

    Regions.TinyTemple: Region("Tiny Temple", Levels.AngryAztec, False, [
        Location("Aztec Tiny 5 Door Temple", lambda l: l.feather and l.istiny),
        Location("Aztec Banana Fairy Tiny Temple", lambda l: l.camera and l.feather and l.mini and l.istiny),
    ], [], [
        Exit(Regions.AngryAztecMain, lambda l: True),
    ]),

    Regions.ChunkyTemple: Region("Chunky Temple", Levels.AngryAztec, False, [
        Location("Aztec Chunky 5 Door Temple", lambda l: l.pineapple and l.ischunky),
        Location("Aztec Chunky Kasplat", lambda l: l.pineapple and l.ischunky),
    ], [], [
        Exit(Regions.AngryAztecMain, lambda l: True),
    ]),

    Regions.AztecTinyRace: Region("Aztec Tiny Race", Levels.AngryAztec, False, [
        Location("Aztec Tiny Beetle Race", lambda l: l.istiny),
    ], [], []),

    Regions.LlamaTemple: Region("Llama Temple", Levels.AngryAztec, True, [
        Location("Lanky Kong", lambda l: l.bongos and l.isdonkey),
        Location("Aztec Donkey Free Lanky", lambda l: l.bongos and l.isdonkey),
        Location("Aztec Lanky Teetering Turtle Trouble", lambda l: l.trombone and l.islanky),
        Location("Aztec Lanky Matching Game", lambda l: l.grape and l.Slam and l.islanky),
        Location("Aztec Banana Fairy Llama Temple", lambda l: l.camera),
    ], [
        Event(Events.AztecDonkeySwitch, lambda l: l.Slam and l.isdonkey),
    ], [
        Exit(Regions.AngryAztecMain, lambda l: True),
        Exit(Regions.LlamaTempleBack, lambda l: l.mini),
    ]),

    Regions.LlamaTempleBack: Region("Llama Temple Back", Levels.AngryAztec, False, [
        Location("Aztec Tiny Llama Temple", lambda l: l.Slam and l.twirl and l.istiny),
        Location("Aztec Lanky Kasplat", lambda l: l.islanky),
    ], [], []),

    Regions.AztecBossLobby: Region("Aztec Boss Lobby", Levels.AngryAztec, True, [], [], [
        # 120 bananas
        Exit(Regions.AztecBoss, lambda l: l.isdiddy),
    ]),

    Regions.AztecBoss: Region("Aztec Boss", Levels.AngryAztec, False, [
        Location("Aztec Key", lambda l: l.isdiddy),
    ], [], []),
}
