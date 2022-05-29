# fmt: off
"""Logic file for Angry Aztec."""

from randomizer.Enums.Events import Events
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.MinigameType import MinigameType
from randomizer.Enums.Regions import Regions
from randomizer.Enums.Transitions import Transitions
from randomizer.LogicClasses import (Event, LocationLogic, Region,
                                     TransitionFront)

LogicRegions = {
    Regions.AngryAztecStart: Region("Angry Aztec Start", Levels.AngryAztec, True, None, [
        LocationLogic(Locations.AztecDonkeyMedal, lambda l: l.ColoredBananas[Levels.AngryAztec][Kongs.donkey] >= 75),
        LocationLogic(Locations.AztecDiddyMedal, lambda l: l.ColoredBananas[Levels.AngryAztec][Kongs.diddy] >= 75),
        LocationLogic(Locations.AztecLankyMedal, lambda l: l.ColoredBananas[Levels.AngryAztec][Kongs.lanky] >= 75),
        LocationLogic(Locations.AztecTinyMedal, lambda l: l.ColoredBananas[Levels.AngryAztec][Kongs.tiny] >= 75),
        LocationLogic(Locations.AztecChunkyMedal, lambda l: l.ColoredBananas[Levels.AngryAztec][Kongs.chunky] >= 75),
        LocationLogic(Locations.AztecDonkeyFreeLlama, lambda l: Events.LlamaFreed in l.Events and l.donkey),
        LocationLogic(Locations.AztecChunkyVases, lambda l: l.pineapple and l.chunky),
        # If default damage can just walk to the bridge and take damage with any kong, otherwise need strong kong and to be donkey
        LocationLogic(Locations.AztecKasplatSandyBridge, lambda l: l.coconut and ((l.strongKong and l.isdonkey) or l.settings.damage_amount == "default")),
        LocationLogic(Locations.AztecKasplatOnTinyTemple, lambda l: l.jetpack),
    ], [
        Event(Events.AztecEntered, lambda l: True),
    ], [
        TransitionFront(Regions.AngryAztecLobby, lambda l: True, Transitions.AztecToIsles),
        TransitionFront(Regions.TempleStart, lambda l: (l.peanut and l.isdiddy) or (l.grape and l.islanky)
                        or (l.feather and l.istiny) or (l.pineapple and l.ischunky)),
        TransitionFront(Regions.AngryAztecMain, lambda l: l.guitar and l.diddy),
        TransitionFront(Regions.CandyAztec, lambda l: True),
        TransitionFront(Regions.AztecBossLobby, lambda l: True),
    ]),

    Regions.TempleStart: Region("Temple Start", Levels.AngryAztec, False, -1, [
        LocationLogic(Locations.AztecTinyKlaptrapRoom, lambda l: l.mini and l.istiny),
        LocationLogic(Locations.AztecChunkyKlaptrapRoom, lambda l: l.triangle and l.ischunky),
    ], [], [
        TransitionFront(Regions.AngryAztecStart, lambda l: True),
        TransitionFront(Regions.TempleUnderwater, lambda l: True),  # Ice pre-melted, without it would be "l.Slam and l.guitar and l.diddyAccess"
    ]),

    Regions.TempleUnderwater: Region("Temple Underwater", Levels.AngryAztec, False, -1, [
        LocationLogic(Locations.TinyKong, lambda l: l.CanFreeTiny()),
        LocationLogic(Locations.AztecDiddyFreeTiny, lambda l: l.CanFreeTiny()),
        LocationLogic(Locations.AztecLankyVulture, lambda l: l.Slam and l.grape and l.islanky),
        LocationLogic(Locations.AztecBattleArena, lambda l: l.Slam and l.grape and l.islanky),
    ], [], [
        TransitionFront(Regions.TempleStart, lambda l: True),
    ]),

    Regions.AngryAztecMain: Region("Angry Aztec Main", Levels.AngryAztec, True, None, [
        LocationLogic(Locations.AztecDonkeyQuicksandCave, lambda l: Events.AztecDonkeySwitch in l.Events and l.strongKong and l.isdonkey, MinigameType.BonusBarrel),
        LocationLogic(Locations.AztecDiddyRamGongs, lambda l: l.charge and l.jetpack and l.diddy),
        LocationLogic(Locations.AztecDiddyVultureRace, lambda l: l.jetpack and l.diddy),
        LocationLogic(Locations.AztecChunkyCagedBarrel, lambda l: l.hunkyChunky and l.ischunky, MinigameType.BonusBarrel),
        LocationLogic(Locations.AztecKasplatNearLab, lambda l: True),
    ], [
        Event(Events.FedTotem, lambda l: l.jetpack and l.peanut and l.Slam and l.diddy),
    ], [
        TransitionFront(Regions.AngryAztecStart, lambda l: True),
        TransitionFront(Regions.DonkeyTemple, lambda l: Events.FedTotem in l.Events and l.coconut and l.isdonkey, Transitions.AztecMainToDonkey),
        TransitionFront(Regions.DiddyTemple, lambda l: Events.FedTotem in l.Events and l.peanut and l.isdiddy, Transitions.AztecMainToDiddy),
        TransitionFront(Regions.LankyTemple, lambda l: Events.FedTotem in l.Events and l.grape and l.islanky, Transitions.AztecMainToLanky),
        TransitionFront(Regions.TinyTemple, lambda l: Events.FedTotem in l.Events and l.feather and l.istiny, Transitions.AztecMainToTiny),
        TransitionFront(Regions.ChunkyTemple, lambda l: Events.FedTotem in l.Events and l.pineapple and l.ischunky, Transitions.AztecMainToChunky),
        TransitionFront(Regions.AztecTinyRace, lambda l: l.charge and l.jetpack and l.diddy and l.mini and l.saxophone and l.istiny, Transitions.AztecMainToRace),
        TransitionFront(Regions.LlamaTemple, lambda l: (l.coconut and l.isdonkey) or (l.grape and l.islanky) or (l.feather and l.istiny)),  # Decision to pre-spawn switches
        TransitionFront(Regions.AztecBaboonBlast, lambda l: l.blast and l.isdonkey),  # , Transitions.AztecMainToBBlast),
        TransitionFront(Regions.CrankyAztec, lambda l: True),
        TransitionFront(Regions.Snide, lambda l: True),
        TransitionFront(Regions.FunkyAztec, lambda l: True),
    ]),

    Regions.AztecBaboonBlast: Region("Aztec Baboon Blast", Levels.AngryAztec, False, None, [], [
        Event(Events.LlamaFreed, lambda l: l.isdonkey)
    ], [
        TransitionFront(Regions.AngryAztecMain, lambda l: True)
    ]),

    # All the 5 door temple require their respective gun to die
    Regions.DonkeyTemple: Region("Donkey Temple", Levels.AngryAztec, False, TransitionFront(Regions.AngryAztecStart, lambda l: l.coconut and l.isdonkey), [
        LocationLogic(Locations.AztecDonkey5DoorTemple, lambda l: l.coconut and l.isdonkey),
    ], [], [
        TransitionFront(Regions.AngryAztecMain, lambda l: True, Transitions.AztecDonkeyToMain),
    ]),

    Regions.DiddyTemple: Region("Diddy Temple", Levels.AngryAztec, False, TransitionFront(Regions.AngryAztecStart, lambda l: l.peanut and l.isdiddy), [
        LocationLogic(Locations.AztecDiddy5DoorTemple, lambda l: l.peanut and l.isdiddy),
    ], [], [
        TransitionFront(Regions.AngryAztecMain, lambda l: True, Transitions.AztecDiddyToMain),
    ]),

    Regions.LankyTemple: Region("Lanky Temple", Levels.AngryAztec, False, TransitionFront(Regions.AngryAztecStart, lambda l: l.grape and l.islanky), [
        LocationLogic(Locations.AztecLanky5DoorTemple, lambda l: l.grape and l.islanky, MinigameType.BonusBarrel),
    ], [], [
        TransitionFront(Regions.AngryAztecMain, lambda l: True, Transitions.AztecLankyToMain),
    ]),

    Regions.TinyTemple: Region("Tiny Temple", Levels.AngryAztec, False, TransitionFront(Regions.AngryAztecStart, lambda l: l.feather and l.istiny), [
        LocationLogic(Locations.AztecTiny5DoorTemple, lambda l: l.feather and l.istiny),
        LocationLogic(Locations.AztecBananaFairyTinyTemple, lambda l: l.camera and l.feather and l.mini and l.istiny),
    ], [], [
        TransitionFront(Regions.AngryAztecMain, lambda l: True, Transitions.AztecTinyToMain),
    ]),

    Regions.ChunkyTemple: Region("Chunky Temple", Levels.AngryAztec, False, TransitionFront(Regions.AngryAztecStart, lambda l: l.pineapple and l.ischunky), [
        LocationLogic(Locations.AztecChunky5DoorTemple, lambda l: l.pineapple and l.ischunky, MinigameType.BonusBarrel),
        LocationLogic(Locations.AztecKasplatChunky5DT, lambda l: l.pineapple and l.ischunky),
    ], [], [
        TransitionFront(Regions.AngryAztecMain, lambda l: True, Transitions.AztecChunkyToMain),
    ]),

    Regions.AztecTinyRace: Region("Aztec Tiny Race", Levels.AngryAztec, False, None, [
        LocationLogic(Locations.AztecTinyBeetleRace, lambda l: l.istiny),
    ], [], [
        TransitionFront(Regions.AngryAztecMain, lambda l: True, Transitions.AztecRaceToMain),
    ], Transitions.AztecMainToRace
    ),

    Regions.LlamaTemple: Region("Llama Temple", Levels.AngryAztec, True, -1, [
        LocationLogic(Locations.LankyKong, lambda l: l.CanFreeLanky()),
        LocationLogic(Locations.AztecDonkeyFreeLanky, lambda l: l.CanFreeLanky()),
        LocationLogic(Locations.AztecLankyLlamaTempleBarrel, lambda l: l.trombone and l.islanky, MinigameType.BonusBarrel),
        LocationLogic(Locations.AztecLankyMatchingGame, lambda l: l.grape and l.Slam and l.lanky),
        LocationLogic(Locations.AztecBananaFairyLlamaTemple, lambda l: l.camera),
    ], [
        Event(Events.AztecDonkeySwitch, lambda l: l.Slam and l.donkey),
        Event(Events.AztecLlamaSpit, lambda l: l.bongos and l.donkey),
    ], [
        TransitionFront(Regions.AngryAztecMain, lambda l: True),
        TransitionFront(Regions.LlamaTempleBack, lambda l: l.mini and l.tiny),
    ]),

    Regions.LlamaTempleBack: Region("Llama Temple Back", Levels.AngryAztec, False, -1, [
        LocationLogic(Locations.AztecTinyLlamaTemple, lambda l: l.Slam and l.twirl and l.istiny),
        LocationLogic(Locations.AztecKasplatLlamaTemple, lambda l: True),
    ], [], [
        TransitionFront(Regions.LlamaTemple, lambda l: True),
    ]),

    Regions.AztecBossLobby: Region("Aztec Boss Lobby", Levels.AngryAztec, True, None, [], [], [
        TransitionFront(Regions.AztecBoss, lambda l: l.IsBossReachable(Levels.AngryAztec)),
    ]),

    Regions.AztecBoss: Region("Aztec Boss", Levels.AngryAztec, False, None, [
        LocationLogic(Locations.AztecKey, lambda l: l.IsBossBeatable(Levels.AngryAztec)),
    ], [], []),
}
