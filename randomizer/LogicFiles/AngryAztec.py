# fmt: off
"""Logic file for Angry Aztec."""

from randomizer.Enums.Events import Events
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Regions import Regions
from randomizer.LogicClasses import Event, Exit, LocationLogic, Region

LogicRegions = {
    Regions.AngryAztecStart: Region("Angry Aztec Start", Levels.AngryAztec, True, [
        LocationLogic(Locations.AztecDonkeyMedal, lambda l: l.ColoredBananas[Levels.AngryAztec][Kongs.donkey] >= 75),
        LocationLogic(Locations.AztecDiddyMedal, lambda l: l.ColoredBananas[Levels.AngryAztec][Kongs.diddy] >= 75),
        LocationLogic(Locations.AztecLankyMedal, lambda l: l.ColoredBananas[Levels.AngryAztec][Kongs.lanky] >= 75),
        LocationLogic(Locations.AztecTinyMedal, lambda l: l.ColoredBananas[Levels.AngryAztec][Kongs.tiny] >= 75),
        LocationLogic(Locations.AztecChunkyMedal, lambda l: l.ColoredBananas[Levels.AngryAztec][Kongs.chunky] >= 75),
        LocationLogic(Locations.AztecDonkeyFreeLlama, lambda l: Events.LlamaFreed in l.Events and l.isdonkey),
        LocationLogic(Locations.AztecChunkyVases, lambda l: l.pineapple and l.ischunky),
        LocationLogic(Locations.AztecDonkeyKasplat, lambda l: l.coconut and l.strongKong and l.isdonkey),
        LocationLogic(Locations.AztecDiddyKasplat, lambda l: l.jetpack and l.isdiddy),
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
        LocationLogic(Locations.AztecTinyKlaptrapRoom, lambda l: l.mini and l.istiny),
        LocationLogic(Locations.AztecChunkyKlaptrapRoom, lambda l: l.triangle and l.ischunky),
    ], [], [
        Exit(Regions.AngryAztecStart, lambda l: True),
        Exit(Regions.TempleUnderwater, lambda l: l.Slam and l.guitar and l.diddyAccess),
    ]),

    Regions.TempleUnderwater: Region("Temple Underwater", Levels.AngryAztec, False, [
        LocationLogic(Locations.TinyKong, lambda l: l.charge and l.isdiddy),
        LocationLogic(Locations.AztecDiddyFreeTiny, lambda l: l.charge and l.isdiddy),
        LocationLogic(Locations.AztecLankyVulture, lambda l: l.Slam and l.grape and l.islanky),
        LocationLogic(Locations.AztecBattleArena, lambda l: l.Slam and l.grape and l.islanky),
    ], [], []),

    Regions.AngryAztecMain: Region("Angry Aztec Main", Levels.AngryAztec, True, [
        LocationLogic(Locations.AztecDonkeyStealthySnoop, lambda l: Events.AztecDonkeySwitch in l.Events and l.strongKong and l.isdonkey),
        LocationLogic(Locations.AztecDiddyRamGongs, lambda l: l.charge and l.jetpack and l.isdiddy),
        LocationLogic(Locations.AztecDiddyVultureRace, lambda l: l.jetpack and l.isdiddy),
        LocationLogic(Locations.AztecChunkyBusyBarrelBarrage, lambda l: l.hunkyChunky and l.ischunky),
        LocationLogic(Locations.AztecTinyKasplat, lambda l: l.istiny),
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
        LocationLogic(Locations.AztecDonkey5DoorTemple, lambda l: l.coconut and l.isdonkey),
    ], [], [
        Exit(Regions.AngryAztecMain, lambda l: True),
    ]),

    Regions.DiddyTemple: Region("Diddy Temple", Levels.AngryAztec, False, [
        LocationLogic(Locations.AztecDiddy5DoorTemple, lambda l: l.peanut and l.isdiddy),
    ], [], [
        Exit(Regions.AngryAztecMain, lambda l: True),
    ]),

    Regions.LankyTemple: Region("Lanky Temple", Levels.AngryAztec, False, [
        LocationLogic(Locations.AztecLanky5DoorTemple, lambda l: l.grape and l.islanky),
    ], [], [
        Exit(Regions.AngryAztecMain, lambda l: True),
    ]),

    Regions.TinyTemple: Region("Tiny Temple", Levels.AngryAztec, False, [
        LocationLogic(Locations.AztecTiny5DoorTemple, lambda l: l.feather and l.istiny),
        LocationLogic(Locations.AztecBananaFairyTinyTemple, lambda l: l.camera and l.feather and l.mini and l.istiny),
    ], [], [
        Exit(Regions.AngryAztecMain, lambda l: True),
    ]),

    Regions.ChunkyTemple: Region("Chunky Temple", Levels.AngryAztec, False, [
        LocationLogic(Locations.AztecChunky5DoorTemple, lambda l: l.pineapple and l.ischunky),
        LocationLogic(Locations.AztecChunkyKasplat, lambda l: l.pineapple and l.ischunky),
    ], [], [
        Exit(Regions.AngryAztecMain, lambda l: True),
    ]),

    Regions.AztecTinyRace: Region("Aztec Tiny Race", Levels.AngryAztec, False, [
        LocationLogic(Locations.AztecTinyBeetleRace, lambda l: l.istiny),
    ], [], []),

    Regions.LlamaTemple: Region("Llama Temple", Levels.AngryAztec, True, [
        LocationLogic(Locations.LankyKong, lambda l: l.bongos and l.isdonkey),
        LocationLogic(Locations.AztecDonkeyFreeLanky, lambda l: l.bongos and l.isdonkey),
        LocationLogic(Locations.AztecLankyTeeteringTurtleTrouble, lambda l: l.trombone and l.islanky),
        LocationLogic(Locations.AztecLankyMatchingGame, lambda l: l.grape and l.Slam and l.islanky),
        LocationLogic(Locations.AztecBananaFairyLlamaTemple, lambda l: l.camera),
    ], [
        Event(Events.AztecDonkeySwitch, lambda l: l.Slam and l.isdonkey),
    ], [
        Exit(Regions.AngryAztecMain, lambda l: True),
        Exit(Regions.LlamaTempleBack, lambda l: l.mini),
    ]),

    Regions.LlamaTempleBack: Region("Llama Temple Back", Levels.AngryAztec, False, [
        LocationLogic(Locations.AztecTinyLlamaTemple, lambda l: l.Slam and l.twirl and l.istiny),
        LocationLogic(Locations.AztecLankyKasplat, lambda l: l.islanky),
    ], [], []),

    Regions.AztecBossLobby: Region("Aztec Boss Lobby", Levels.AngryAztec, True, [], [], [
        Exit(Regions.AztecBoss, lambda l: l.isdiddy and sum(l.ColoredBananas[Levels.AngryAztec]) >= 120),
    ]),

    Regions.AztecBoss: Region("Aztec Boss", Levels.AngryAztec, False, [
        LocationLogic(Locations.AztecKey, lambda l: l.isdiddy),
    ], [], []),
}
