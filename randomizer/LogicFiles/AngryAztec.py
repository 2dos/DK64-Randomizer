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
    Regions.AngryAztecMedals: Region("Angry Aztec Medals", "Angry Aztec Medal Rewards", Levels.AngryAztec, False, None, [
        LocationLogic(Locations.AztecDonkeyMedal, lambda l: l.ColoredBananas[Levels.AngryAztec][Kongs.donkey] >= l.settings.medal_cb_req),
        LocationLogic(Locations.AztecDiddyMedal, lambda l: l.ColoredBananas[Levels.AngryAztec][Kongs.diddy] >= l.settings.medal_cb_req),
        LocationLogic(Locations.AztecLankyMedal, lambda l: l.ColoredBananas[Levels.AngryAztec][Kongs.lanky] >= l.settings.medal_cb_req),
        LocationLogic(Locations.AztecTinyMedal, lambda l: l.ColoredBananas[Levels.AngryAztec][Kongs.tiny] >= l.settings.medal_cb_req),
        LocationLogic(Locations.AztecChunkyMedal, lambda l: l.ColoredBananas[Levels.AngryAztec][Kongs.chunky] >= l.settings.medal_cb_req),
    ], [], []),

    Regions.AngryAztecStart: Region("Angry Aztec Start", "Various Aztec Tunnels", Levels.AngryAztec, False, None, [], [
        Event(Events.AztecEntered, lambda l: True),
    ], [
        TransitionFront(Regions.AngryAztecMedals, lambda l: True),
        TransitionFront(Regions.AngryAztecLobby, lambda l: True, Transitions.AztecToIsles),
        TransitionFront(Regions.BetweenVinesByPortal, lambda l: l.pathMode or l.vines or (l.istiny and l.twirl)),
    ]),

    Regions.BetweenVinesByPortal: Region("Angry Aztec Between Vines By Portal", "Various Aztec Tunnels", Levels.AngryAztec, False, None, [
        LocationLogic(Locations.AztecChunkyVases, lambda l: l.pineapple and l.chunky and l.barrels),
    ], [], [
        TransitionFront(Regions.AngryAztecMedals, lambda l: True),
        TransitionFront(Regions.AngryAztecStart, lambda l: l.vines or (l.istiny and l.twirl)),
        TransitionFront(Regions.AngryAztecOasis, lambda l: l.pathMode or l.vines or (l.istiny and l.twirl)),
    ]),

    Regions.AztecTunnelBeforeOasis: Region("Angry Aztec Tunnel Before Oasis", "Various Aztec Tunnels", Levels.AngryAztec, False, None, [
        # Damage checks in logic are cringe but we need this to make vanilla kasplat rando interesting in Aztec
        LocationLogic(Locations.AztecKasplatSandyBridge, lambda l: not l.settings.kasplat_rando and l.coconut and ((l.strongKong and l.isdonkey) or l.settings.damage_amount == "default")),
    ], [], [
        TransitionFront(Regions.AngryAztecMedals, lambda l: True),
        TransitionFront(Regions.BetweenVinesByPortal, lambda l: l.vines or (l.istiny and l.twirl)),
        TransitionFront(Regions.AngryAztecOasis, lambda l: True),
    ]),

    Regions.AngryAztecOasis: Region("Angry Aztec Oasis", "Aztec Oasis", Levels.AngryAztec, True, None, [
        LocationLogic(Locations.AztecDonkeyFreeLlama, lambda l: Events.LlamaFreed in l.Events),
        LocationLogic(Locations.AztecKasplatOnTinyTemple, lambda l: not l.settings.kasplat_rando and l.jetpack and l.isdiddy),
    ], [], [
        TransitionFront(Regions.AngryAztecMedals, lambda l: True),
        TransitionFront(Regions.AztecTunnelBeforeOasis, lambda l: True),
        TransitionFront(Regions.TempleStart, lambda l: (l.peanut and l.isdiddy) or (l.grape and l.islanky)
                        or (l.feather and l.istiny) or (l.pineapple and l.ischunky)),
        TransitionFront(Regions.AngryAztecConnectorTunnel, lambda l: l.settings.open_levels or ((l.vines or l.jetpack) and l.guitar and l.diddy)),
        TransitionFront(Regions.CandyAztec, lambda l: True),
        TransitionFront(Regions.AztecBossLobby, lambda l: not l.settings.tns_location_rando),
    ]),

    Regions.TempleStart: Region("Temple Start", "Tiny Temple", Levels.AngryAztec, False, -1, [
        LocationLogic(Locations.AztecChunkyKlaptrapRoom, lambda l: l.triangle and l.ischunky),
    ], [], [
        TransitionFront(Regions.AngryAztecMedals, lambda l: True),
        TransitionFront(Regions.AngryAztecOasis, lambda l: True),
        TransitionFront(Regions.TempleUnderwater, lambda l: l.swim),  # Ice pre-melted, without it would be "l.Slam and l.guitar and l.diddyAccess"
    ]),

    Regions.TempleUnderwater: Region("Temple Underwater", "Tiny Temple", Levels.AngryAztec, False, -1, [
        LocationLogic(Locations.AztecTinyKlaptrapRoom, lambda l: l.mini and l.istiny),
        LocationLogic(Locations.TinyKong, lambda l: l.CanFreeTiny()),
        LocationLogic(Locations.AztecDiddyFreeTiny, lambda l: l.CanFreeTiny()),
        LocationLogic(Locations.AztecLankyVulture, lambda l: l.Slam and l.grape and l.islanky),
        LocationLogic(Locations.AztecBattleArena, lambda l: not l.settings.crown_placement_rando and l.Slam and l.grape and l.lanky),
    ], [], [
        TransitionFront(Regions.AngryAztecMedals, lambda l: True),
        TransitionFront(Regions.TempleStart, lambda l: True),
    ]),

    Regions.AngryAztecConnectorTunnel: Region("Angry Aztec Connector Tunnel", "Various Aztec Tunnels", Levels.AngryAztec, False, None, [
        LocationLogic(Locations.AztecChunkyCagedBarrel, lambda l: l.hunkyChunky and l.ischunky and l.barrels, MinigameType.BonusBarrel),
        LocationLogic(Locations.AztecKasplatNearLab, lambda l: not l.settings.kasplat_rando),
    ], [], [
        TransitionFront(Regions.AngryAztecMedals, lambda l: True),
        TransitionFront(Regions.AngryAztecOasis, lambda l: True),
        TransitionFront(Regions.AngryAztecMain, lambda l: True),
        TransitionFront(Regions.CrankyAztec, lambda l: True),
    ]),

    Regions.AngryAztecMain: Region("Angry Aztec Main", "Aztec Totem Area", Levels.AngryAztec, True, None, [
        LocationLogic(Locations.AztecDiddyRamGongs, lambda l: l.charge and l.jetpack and l.diddy),
        LocationLogic(Locations.AztecDiddyVultureRace, lambda l: l.jetpack and l.diddy),
    ], [
        Event(Events.FedTotem, lambda l: l.settings.high_req or (l.jetpack and l.peanut and l.Slam and l.diddy)),
    ], [
        TransitionFront(Regions.AngryAztecMedals, lambda l: True),
        TransitionFront(Regions.AngryAztecConnectorTunnel, lambda l: True),
        TransitionFront(Regions.DonkeyTemple, lambda l: Events.FedTotem in l.Events and l.coconut and l.isdonkey, Transitions.AztecMainToDonkey),
        TransitionFront(Regions.DiddyTemple, lambda l: Events.FedTotem in l.Events and l.peanut and l.isdiddy, Transitions.AztecMainToDiddy),
        TransitionFront(Regions.LankyTemple, lambda l: Events.FedTotem in l.Events and l.grape and l.islanky, Transitions.AztecMainToLanky),
        TransitionFront(Regions.TinyTemple, lambda l: Events.FedTotem in l.Events and l.feather and l.istiny, Transitions.AztecMainToTiny),
        TransitionFront(Regions.ChunkyTemple, lambda l: Events.FedTotem in l.Events and l.pineapple and l.ischunky, Transitions.AztecMainToChunky),
        TransitionFront(Regions.AztecTinyRace, lambda l: l.charge and l.jetpack and l.diddy and l.mini and l.saxophone and l.istiny, Transitions.AztecMainToRace),
        TransitionFront(Regions.LlamaTemple, lambda l: (l.coconut and l.isdonkey) or (l.grape and l.islanky) or (l.feather and l.istiny)),  # Decision to pre-spawn switches
        TransitionFront(Regions.AztecBaboonBlast, lambda l: l.blast and l.isdonkey),  # , Transitions.AztecMainToBBlast),
        TransitionFront(Regions.Snide, lambda l: True),
        TransitionFront(Regions.FunkyAztec, lambda l: True),
        TransitionFront(Regions.AztecDonkeyQuicksandCave, lambda l: Events.AztecDonkeySwitch in l.Events and l.strongKong and l.isdonkey),
        TransitionFront(Regions.AztecBossLobby, lambda l: not l.settings.tns_location_rando),
    ]),

    Regions.AztecDonkeyQuicksandCave: Region("Aztec Donkey Sand Tunnel", "Various Aztec Tunnels", Levels.AngryAztec, False, -1, [
        LocationLogic(Locations.AztecDonkeyQuicksandCave, lambda l: l.isdonkey or l.settings.free_trade_items, MinigameType.BonusBarrel),
    ], [], [
        TransitionFront(Regions.AngryAztecMedals, lambda l: True),
        TransitionFront(Regions.AngryAztecMain, lambda l: l.isdonkey and l.strongKong)
    ]),

    Regions.AztecBaboonBlast: Region("Aztec Baboon Blast", "Aztec Totem Area", Levels.AngryAztec, False, None, [], [
        Event(Events.LlamaFreed, lambda l: l.isdonkey)
    ], [
        TransitionFront(Regions.AngryAztecMedals, lambda l: True),
        TransitionFront(Regions.AngryAztecMain, lambda l: True)
    ]),

    # All the 5 door temple require their respective gun to die
    Regions.DonkeyTemple: Region("Donkey Temple", "5 Door Temple", Levels.AngryAztec, False, TransitionFront(Regions.AngryAztecStart, lambda l: l.coconut and l.isdonkey), [
        LocationLogic(Locations.AztecDonkey5DoorTemple, lambda l: l.coconut and l.isdonkey),
    ], [], [
        TransitionFront(Regions.AngryAztecMedals, lambda l: True),
        TransitionFront(Regions.AngryAztecMain, lambda l: True, Transitions.AztecDonkeyToMain),
    ]),

    Regions.DiddyTemple: Region("Diddy Temple", "5 Door Temple", Levels.AngryAztec, False, TransitionFront(Regions.AngryAztecStart, lambda l: l.peanut and l.isdiddy), [
        LocationLogic(Locations.AztecDiddy5DoorTemple, lambda l: l.peanut and l.isdiddy),
    ], [], [
        TransitionFront(Regions.AngryAztecMedals, lambda l: True),
        TransitionFront(Regions.AngryAztecMain, lambda l: True, Transitions.AztecDiddyToMain),
    ]),

    Regions.LankyTemple: Region("Lanky Temple", "5 Door Temple", Levels.AngryAztec, False, TransitionFront(Regions.AngryAztecStart, lambda l: l.grape and l.islanky), [
        LocationLogic(Locations.AztecLanky5DoorTemple, lambda l: l.grape and l.islanky, MinigameType.BonusBarrel),
    ], [], [
        TransitionFront(Regions.AngryAztecMedals, lambda l: True),
        TransitionFront(Regions.AngryAztecMain, lambda l: True, Transitions.AztecLankyToMain),
    ]),

    Regions.TinyTemple: Region("Tiny Temple", "5 Door Temple", Levels.AngryAztec, False, TransitionFront(Regions.AngryAztecStart, lambda l: l.feather and l.istiny), [
        LocationLogic(Locations.AztecTiny5DoorTemple, lambda l: l.feather and l.istiny),
        LocationLogic(Locations.AztecBananaFairyTinyTemple, lambda l: l.camera and l.feather and l.mini and l.istiny),
    ], [], [
        TransitionFront(Regions.AngryAztecMedals, lambda l: True),
        TransitionFront(Regions.AngryAztecMain, lambda l: True, Transitions.AztecTinyToMain),
    ]),

    Regions.ChunkyTemple: Region("Chunky Temple", "5 Door Temple", Levels.AngryAztec, False, TransitionFront(Regions.AngryAztecStart, lambda l: l.pineapple and l.ischunky), [
        LocationLogic(Locations.AztecChunky5DoorTemple, lambda l: l.pineapple and l.ischunky, MinigameType.BonusBarrel),
        LocationLogic(Locations.AztecKasplatChunky5DT, lambda l: not l.settings.kasplat_rando and l.pineapple and l.ischunky),
    ], [], [
        TransitionFront(Regions.AngryAztecMedals, lambda l: True),
        TransitionFront(Regions.AngryAztecMain, lambda l: True, Transitions.AztecChunkyToMain),
    ]),

    Regions.AztecTinyRace: Region("Aztec Tiny Race", "Aztec Totem Area", Levels.AngryAztec, False, None, [
        LocationLogic(Locations.AztecTinyBeetleRace, lambda l: l.istiny or l.settings.free_trade_items),
    ], [], [
        TransitionFront(Regions.AngryAztecMedals, lambda l: True),
        TransitionFront(Regions.AngryAztecMain, lambda l: True, Transitions.AztecRaceToMain),
    ], Transitions.AztecMainToRace
    ),

    Regions.LlamaTemple: Region("Llama Temple", "Llama Temple", Levels.AngryAztec, True, -1, [
        LocationLogic(Locations.LankyKong, lambda l: l.CanFreeLanky()),
        LocationLogic(Locations.AztecDonkeyFreeLanky, lambda l: l.CanFreeLanky()),
        LocationLogic(Locations.AztecLankyLlamaTempleBarrel, lambda l: l.trombone and l.handstand and l.islanky, MinigameType.BonusBarrel),
        LocationLogic(Locations.AztecLankyMatchingGame, lambda l: l.grape and l.Slam and l.lanky),
        LocationLogic(Locations.AztecBananaFairyLlamaTemple, lambda l: l.camera),
    ], [
        Event(Events.AztecDonkeySwitch, lambda l: l.Slam and l.donkey),
        Event(Events.AztecLlamaSpit, lambda l: l.CanLlamaSpit()),
    ], [
        TransitionFront(Regions.AngryAztecMedals, lambda l: True),
        TransitionFront(Regions.AngryAztecMain, lambda l: True),
        TransitionFront(Regions.LlamaTempleBack, lambda l: l.mini and l.tiny),
    ]),

    Regions.LlamaTempleBack: Region("Llama Temple Back", "Llama Temple", Levels.AngryAztec, False, -1, [
        LocationLogic(Locations.AztecTinyLlamaTemple, lambda l: l.Slam and l.istiny),
        LocationLogic(Locations.AztecKasplatLlamaTemple, lambda l: not l.settings.kasplat_rando),
    ], [], [
        TransitionFront(Regions.AngryAztecMedals, lambda l: True),
        TransitionFront(Regions.LlamaTemple, lambda l: True),
    ]),

    Regions.AztecBossLobby: Region("Aztec Boss Lobby", "Troff 'N' Scoff", Levels.AngryAztec, True, None, [], [], [
        TransitionFront(Regions.AztecBoss, lambda l: l.IsBossReachable(Levels.AngryAztec)),
    ]),

    Regions.AztecBoss: Region("Aztec Boss", "Troff 'N' Scoff", Levels.AngryAztec, False, None, [
        LocationLogic(Locations.AztecKey, lambda l: l.IsBossBeatable(Levels.AngryAztec)),
    ], [], []),
}
