# fmt: off
"""Logic file for Gloomy Galleon."""

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
    Regions.GloomyGalleonMedals: Region("Gloomy Galleon Medals", "Gloomy Galleon Medal Rewards", Levels.GloomyGalleon, False, None, [
        LocationLogic(Locations.GalleonDonkeyMedal, lambda l: l.ColoredBananas[Levels.GloomyGalleon][Kongs.donkey] >= l.settings.medal_cb_req),
        LocationLogic(Locations.GalleonDiddyMedal, lambda l: l.ColoredBananas[Levels.GloomyGalleon][Kongs.diddy] >= l.settings.medal_cb_req),
        LocationLogic(Locations.GalleonLankyMedal, lambda l: l.ColoredBananas[Levels.GloomyGalleon][Kongs.lanky] >= l.settings.medal_cb_req),
        LocationLogic(Locations.GalleonTinyMedal, lambda l: l.ColoredBananas[Levels.GloomyGalleon][Kongs.tiny] >= l.settings.medal_cb_req),
        LocationLogic(Locations.GalleonChunkyMedal, lambda l: l.ColoredBananas[Levels.GloomyGalleon][Kongs.chunky] >= l.settings.medal_cb_req),
    ], [], []),

    Regions.GloomyGalleonStart: Region("Gloomy Galleon Start", "Galleon Caves", Levels.GloomyGalleon, True, None, [
        LocationLogic(Locations.GalleonChunkyChest, lambda l: l.punch and l.chunky),
        LocationLogic(Locations.GalleonBattleArena, lambda l: not l.settings.crown_placement_rando and l.punch and l.chunky),
        LocationLogic(Locations.GalleonBananaFairybyCranky, lambda l: l.camera and l.punch and l.chunky),
    ], [
        Event(Events.GalleonEntered, lambda l: True),
        Event(Events.GalleonLankySwitch, lambda l: l.Slam and l.lanky),
        Event(Events.GalleonTinySwitch, lambda l: l.Slam and l.tiny),
        Event(Events.LighthouseGateOpened, lambda l: l.coconut and l.donkey),
        # Gate to shipyard always open in rando
        Event(Events.ShipyardGateOpened, lambda l: True),
    ], [
        TransitionFront(Regions.GloomyGalleonMedals, lambda l: True),
        TransitionFront(Regions.GloomyGalleonLobby, lambda l: True, Transitions.GalleonToIsles),
        TransitionFront(Regions.GalleonPastVines, lambda l: l.vines),
        TransitionFront(Regions.GalleonBeyondPineappleGate, lambda l: l.pineapple and l.chunky),
        TransitionFront(Regions.LighthouseSurface, lambda l: l.settings.open_levels or Events.LighthouseGateOpened in l.Events),
        TransitionFront(Regions.Shipyard, lambda l: Events.ShipyardGateOpened in l.Events),
        TransitionFront(Regions.CrankyGalleon, lambda l: True),
    ]),

    Regions.GalleonPastVines: Region("Galleon Past Vines", "Galleon Caves", Levels.GloomyGalleon, False, None, [
        LocationLogic(Locations.GalleonKasplatNearLab, lambda l: not l.settings.kasplat_rando),
    ], [], [
        TransitionFront(Regions.GloomyGalleonMedals, lambda l: True),
        TransitionFront(Regions.GloomyGalleonStart, lambda l: True),
        TransitionFront(Regions.GalleonBossLobby, lambda l: not l.settings.tns_location_rando),
    ]),

    Regions.GalleonBeyondPineappleGate: Region("Galleon Beyond Pineapple Gate", "Galleon Caves", Levels.GloomyGalleon, False, None, [
        LocationLogic(Locations.GalleonChunkyCannonGame, lambda l: Events.WaterSwitch in l.Events and l.ischunky and l.barrels),
        LocationLogic(Locations.GalleonKasplatCannons, lambda l: not l.settings.kasplat_rando and Events.WaterSwitch in l.Events),
    ], [], [
        TransitionFront(Regions.GloomyGalleonMedals, lambda l: True),
        TransitionFront(Regions.GloomyGalleonStart, lambda l: True),
    ]),

    Regions.LighthouseSurface: Region("Lighthouse Surface", "Lighthouse Area", Levels.GloomyGalleon, False, -1, [
        LocationLogic(Locations.GalleonKasplatLighthouseArea, lambda l: not l.settings.kasplat_rando),
    ], [
        Event(Events.GalleonChunkyPad, lambda l: (l.triangle and l.chunky) and (l.swim or l.settings.high_req)),
    ], [
        TransitionFront(Regions.GloomyGalleonMedals, lambda l: True),
        TransitionFront(Regions.GloomyGalleonStart, lambda l: l.settings.open_levels or Events.LighthouseGateOpened in l.Events),
        TransitionFront(Regions.LighthouseUnderwater, lambda l: l.swim),
        TransitionFront(Regions.LighthousePlatform, lambda l: Events.WaterSwitch in l.Events),
        TransitionFront(Regions.LighthouseSnideAlcove, lambda l: Events.WaterSwitch in l.Events),
    ]),

    Regions.LighthousePlatform: Region("Lighthouse Platform", "Lighthouse Area", Levels.GloomyGalleon, False, None, [
        LocationLogic(Locations.GalleonDiddyShipSwitch, lambda l: Events.ActivatedLighthouse in l.Events and l.jetpack and l.Slam and l.isdiddy),
    ], [
        Event(Events.MechafishSummoned, lambda l: l.jetpack and l.guitar and l.isdiddy),
    ], [
        TransitionFront(Regions.GloomyGalleonMedals, lambda l: True),
        TransitionFront(Regions.LighthouseSurface, lambda l: True),
        # Rare case of needing to open gate before being able to go through backwards
        TransitionFront(Regions.Lighthouse, lambda l: l.Slam and l.isdonkey, Transitions.GalleonLighthouseAreaToLighthouse),
        TransitionFront(Regions.SickBay, lambda l: Events.ActivatedLighthouse in l.Events and l.Slam and l.ischunky, Transitions.GalleonLighthouseAreaToSickBay),
        TransitionFront(Regions.GalleonBaboonBlast, lambda l: l.blast and l.isdonkey)  # , Transitions.GalleonMainToBBlast)
    ]),

    Regions.LighthouseUnderwater: Region("Lighthouse Underwater", "Lighthouse Area", Levels.GloomyGalleon, True, None, [
        LocationLogic(Locations.GalleonLankyEnguardeChest, lambda l: Events.LighthouseEnguarde in l.Events and l.lanky),
    ], [
        Event(Events.WaterSwitch, lambda l: True),
        Event(Events.LighthouseEnguarde, lambda l: l.lanky),
    ], [
        TransitionFront(Regions.GloomyGalleonMedals, lambda l: True),
        TransitionFront(Regions.LighthouseSurface, lambda l: True),
        TransitionFront(Regions.MermaidRoom, lambda l: l.mini and l.istiny, Transitions.GalleonLighthousAreaToMermaid),
        TransitionFront(Regions.GalleonBossLobby, lambda l: not l.settings.tns_location_rando),  # T&S past Enguarde is redundant with meme hole
    ]),

    Regions.LighthouseSnideAlcove: Region("Lighthouse Snide Alcove", "Lighthouse Area", Levels.GloomyGalleon, True, None, [], [], [
        TransitionFront(Regions.GloomyGalleonMedals, lambda l: True),
        TransitionFront(Regions.LighthouseSurface, lambda l: True),
        TransitionFront(Regions.Snide, lambda l: True),
    ]),

    Regions.GalleonBaboonBlast: Region("Galleon Baboon Blast", "Lighthouse Area", Levels.GloomyGalleon, False, None, [], [
        Event(Events.SealReleased, lambda l: l.isdonkey)
    ], [
        TransitionFront(Regions.GloomyGalleonMedals, lambda l: True),
        TransitionFront(Regions.LighthousePlatform, lambda l: True)
    ]),

    Regions.Lighthouse: Region("Lighthouse", "Lighthouse Area", Levels.GloomyGalleon, False, -1, [
        LocationLogic(Locations.GalleonDonkeyLighthouse, lambda l: Events.ActivatedLighthouse in l.Events and (l.isdonkey or l.settings.free_trade_items))
    ], [
        Event(Events.ActivatedLighthouse, lambda l: l.settings.high_req or (l.Slam and l.grab and l.isdonkey)),
    ], [
        TransitionFront(Regions.GloomyGalleonMedals, lambda l: True),
        TransitionFront(Regions.LighthousePlatform, lambda l: True, Transitions.GalleonLighthouseToLighthouseArea),
    ]),

    Regions.MermaidRoom: Region("Mermaid Room", "Lighthouse Area", Levels.GloomyGalleon, False, None, [
        LocationLogic(Locations.GalleonTinyPearls, lambda l: Events.PearlsCollected in l.Events and (l.istiny or l.settings.free_trade_items)),
    ], [], [
        TransitionFront(Regions.GloomyGalleonMedals, lambda l: True),
        TransitionFront(Regions.LighthouseUnderwater, lambda l: True, Transitions.GalleonMermaidToLighthouseArea),
    ]),

    Regions.SickBay: Region("Sick Bay", "Lighthouse Area", Levels.GloomyGalleon, False, -1, [
        LocationLogic(Locations.GalleonChunkySeasick, lambda l: l.punch and l.ischunky),
    ], [], [
        TransitionFront(Regions.GloomyGalleonMedals, lambda l: True),
        TransitionFront(Regions.LighthousePlatform, lambda l: True, Transitions.GalleonSickBayToLighthouseArea),
    ]),

    Regions.Shipyard: Region("Shipyard", "Shipyard Area", Levels.GloomyGalleon, True, None, [
        LocationLogic(Locations.GalleonDonkeyFreetheSeal, lambda l: Events.SealReleased in l.Events and (l.isdonkey or l.settings.free_trade_items)),
        LocationLogic(Locations.GalleonKasplatNearSub, lambda l: not l.settings.kasplat_rando),
    ], [
        Event(Events.ShipyardTreasureRoomOpened, lambda l: Events.ShipyardEnguarde in l.Events and Events.WaterSwitch in l.Events),
        Event(Events.GalleonDonkeyPad, lambda l: l.bongos and l.isdonkey and (l.swim or l.settings.high_req)),
        Event(Events.GalleonDiddyPad, lambda l: l.guitar and l.isdiddy and (l.swim or l.settings.high_req)),
        Event(Events.GalleonLankyPad, lambda l: l.trombone and l.islanky and (l.swim or l.settings.high_req)),
        Event(Events.GalleonTinyPad, lambda l: l.saxophone and l.istiny and (l.swim or l.settings.high_req)),
    ], [
        TransitionFront(Regions.GloomyGalleonMedals, lambda l: True),
        TransitionFront(Regions.GloomyGalleonStart, lambda l: l.settings.shuffle_loading_zones == "all" or Events.ShipyardGateOpened in l.Events),
        TransitionFront(Regions.ShipyardUnderwater, lambda l: l.swim),
        TransitionFront(Regions.SealRace, lambda l: Events.SealReleased in l.Events and Events.WaterSwitch in l.Events and l.isdonkey, Transitions.GalleonShipyardToSeal),
        TransitionFront(Regions.CandyGalleon, lambda l: True),
        TransitionFront(Regions.FunkyGalleon, lambda l: True),
    ]),

    Regions.ShipyardUnderwater: Region("Shipyard Underwater", "Shipyard Area", Levels.GloomyGalleon, True, None, [], [
        Event(Events.ShipyardEnguarde, lambda l: l.lanky),
    ], [
        TransitionFront(Regions.GloomyGalleonMedals, lambda l: True),
        TransitionFront(Regions.TreasureRoom, lambda l: Events.ShipyardTreasureRoomOpened in l.Events),
        TransitionFront(Regions.Submarine, lambda l: l.mini and l.istiny, Transitions.GalleonShipyardToSubmarine),
        TransitionFront(Regions.Mechafish, lambda l: Events.MechafishSummoned in l.Events and l.isdiddy),
        TransitionFront(Regions.LankyShip, lambda l: Events.GalleonLankySwitch in l.Events and l.islanky, Transitions.GalleonShipyardToLanky),
        TransitionFront(Regions.TinyShip, lambda l: Events.GalleonTinySwitch in l.Events and l.istiny, Transitions.GalleonShipyardToTiny),
        TransitionFront(Regions.BongosShip, lambda l: Events.GalleonDonkeyPad in l.Events and l.isdonkey, Transitions.GalleonShipyardToBongos),
        TransitionFront(Regions.GuitarShip, lambda l: Events.GalleonDiddyPad in l.Events and l.isdiddy, Transitions.GalleonShipyardToGuitar),
        TransitionFront(Regions.TromboneShip, lambda l: Events.GalleonLankyPad in l.Events and l.islanky, Transitions.GalleonShipyardToTrombone),
        TransitionFront(Regions.SaxophoneShip, lambda l: Events.GalleonTinyPad in l.Events and l.istiny, Transitions.GalleonShipyardToSaxophone),
        TransitionFront(Regions.TriangleShip, lambda l: Events.GalleonChunkyPad in l.Events and l.ischunky, Transitions.GalleonShipyardToTriangle),
        TransitionFront(Regions.GalleonBossLobby, lambda l: not l.settings.tns_location_rando),
    ]),

    Regions.SealRace: Region("Seal Race", "Shipyard Area", Levels.GloomyGalleon, False, None, [
        LocationLogic(Locations.GalleonDonkeySealRace, lambda l: l.isdonkey or l.settings.free_trade_items),
    ], [], [
        TransitionFront(Regions.GloomyGalleonMedals, lambda l: True),
        TransitionFront(Regions.Shipyard, lambda l: True, Transitions.GalleonSealToShipyard),
    ], Transitions.GalleonShipyardToSeal
    ),

    Regions.TreasureRoom: Region("Treasure Room", "Treasure Room", Levels.GloomyGalleon, True, None, [
        LocationLogic(Locations.GalleonLankyGoldTower, lambda l: Events.WaterSwitch in l.Events and l.balloon and l.islanky, MinigameType.BonusBarrel),
    ], [], [
        TransitionFront(Regions.GloomyGalleonMedals, lambda l: True),
        TransitionFront(Regions.ShipyardUnderwater, lambda l: Events.ShipyardTreasureRoomOpened in l.Events and l.swim),
        TransitionFront(Regions.TinyChest, lambda l: l.mini and l.istiny and l.swim, Transitions.GalleonTreasureToChest),
        TransitionFront(Regions.TreasureRoomDiddyGoldTower, lambda l: Events.WaterSwitch in l.Events and l.spring and l.diddy)
    ]),

    Regions.TreasureRoomDiddyGoldTower: Region("Treasure Room Diddy Gold Tower", "Treasure Room", Levels.GloomyGalleon, False, -1, [  # Deathwarp is possible without the kasplat, but you can only take fall damage once
        LocationLogic(Locations.GalleonDiddyGoldTower, lambda l: l.spring and l.isdiddy, MinigameType.BonusBarrel),
        LocationLogic(Locations.GalleonKasplatGoldTower, lambda l: not l.settings.kasplat_rando),
    ], [
        Event(Events.TreasureRoomTeleporterUnlocked, lambda l: l.spring and l.isdiddy),  # TODO: Add logic to ensure bonus barrel reward is collectable, like if it's the diddy jetpack helm minigame
    ], [
        TransitionFront(Regions.GloomyGalleonMedals, lambda l: True),
        TransitionFront(Regions.TreasureRoom, lambda l: True)
    ]),

    Regions.TinyChest: Region("Tiny Chest", "Treasure Room", Levels.GloomyGalleon, False, -1, [], [
        Event(Events.PearlsCollected, lambda l: True),
    ], [
        TransitionFront(Regions.GloomyGalleonMedals, lambda l: True),
        TransitionFront(Regions.TreasureRoom, lambda l: True, Transitions.GalleonChestToTreasure),
    ]),

    Regions.Submarine: Region("Submarine", "Shipyard Area", Levels.GloomyGalleon, False, -1, [
        LocationLogic(Locations.GalleonTinySubmarine, lambda l: l.istiny or l.settings.free_trade_items, MinigameType.BonusBarrel),
    ], [], [
        TransitionFront(Regions.GloomyGalleonMedals, lambda l: True),
        TransitionFront(Regions.ShipyardUnderwater, lambda l: True, Transitions.GalleonSubmarineToShipyard),
    ]),

    Regions.Mechafish: Region("Mechafish", "Shipyard Area", Levels.GloomyGalleon, False, -1, [
        LocationLogic(Locations.GalleonDiddyMechafish, lambda l: l.HasGun(Kongs.diddy) or (l.settings.free_trade_items and l.HasGun(Kongs.any))),
    ], [], [
        TransitionFront(Regions.GloomyGalleonMedals, lambda l: True),
        TransitionFront(Regions.ShipyardUnderwater, lambda l: True)
    ]),

    Regions.LankyShip: Region("Lanky Ship", "Shipyard Area", Levels.GloomyGalleon, False, None, [
        LocationLogic(Locations.GalleonLanky2DoorShip, lambda l: l.islanky or l.settings.free_trade_items),
    ], [], [
        TransitionFront(Regions.GloomyGalleonMedals, lambda l: True),
        TransitionFront(Regions.ShipyardUnderwater, lambda l: True, Transitions.GalleonLankyToShipyard),
    ]),

    Regions.TinyShip: Region("Tiny Ship", "Shipyard Area", Levels.GloomyGalleon, False, -1, [
        LocationLogic(Locations.GalleonTiny2DoorShip, lambda l: l.istiny or l.settings.free_trade_items, MinigameType.BonusBarrel),
    ], [], [
        TransitionFront(Regions.GloomyGalleonMedals, lambda l: True),
        TransitionFront(Regions.ShipyardUnderwater, lambda l: True, Transitions.GalleonTinyToShipyard),
    ]),

    Regions.BongosShip: Region("Bongos Ship", "Shipyard Area", Levels.GloomyGalleon, False, -1, [
        LocationLogic(Locations.GalleonDonkey5DoorShip, lambda l: l.isdonkey or l.settings.free_trade_items, MinigameType.BonusBarrel),
    ], [], [
        TransitionFront(Regions.GloomyGalleonMedals, lambda l: True),
        TransitionFront(Regions.ShipyardUnderwater, lambda l: True, Transitions.GalleonBongosToShipyard),
    ]),

    Regions.GuitarShip: Region("Guitar Ship", "Shipyard Area", Levels.GloomyGalleon, False, -1, [
        LocationLogic(Locations.GalleonDiddy5DoorShip, lambda l: l.isdiddy or l.settings.free_trade_items, MinigameType.BonusBarrel),
    ], [], [
        TransitionFront(Regions.GloomyGalleonMedals, lambda l: True),
        TransitionFront(Regions.ShipyardUnderwater, lambda l: True, Transitions.GalleonGuitarToShipyard),
    ]),

    Regions.TromboneShip: Region("Trombone Ship", "Shipyard Area", Levels.GloomyGalleon, False, -1, [
        LocationLogic(Locations.GalleonLanky5DoorShip, lambda l: l.islanky or l.settings.free_trade_items),
    ], [], [
        TransitionFront(Regions.GloomyGalleonMedals, lambda l: True),
        TransitionFront(Regions.ShipyardUnderwater, lambda l: True, Transitions.GalleonTromboneToShipyard),
    ]),

    Regions.SaxophoneShip: Region("Saxophone Ship", "Shipyard Area", Levels.GloomyGalleon, False, -1, [
        LocationLogic(Locations.GalleonTiny5DoorShip, lambda l: l.istiny or l.settings.free_trade_items),
        LocationLogic(Locations.GalleonBananaFairy5DoorShip, lambda l: l.camera),
    ], [], [
        TransitionFront(Regions.GloomyGalleonMedals, lambda l: True),
        TransitionFront(Regions.ShipyardUnderwater, lambda l: True, Transitions.GalleonSaxophoneToShipyard),
    ]),

    Regions.TriangleShip: Region("Triangle Ship", "Shipyard Area", Levels.GloomyGalleon, False, -1, [
        LocationLogic(Locations.GalleonChunky5DoorShip, lambda l: l.ischunky or l.settings.free_trade_items, MinigameType.BonusBarrel),
    ], [], [
        TransitionFront(Regions.GloomyGalleonMedals, lambda l: True),
        TransitionFront(Regions.ShipyardUnderwater, lambda l: True, Transitions.GalleonTriangleToShipyard),
    ]),

    Regions.GalleonBossLobby: Region("Galleon Boss Lobby", "Troff 'N' Scoff", Levels.GloomyGalleon, True, None, [], [], [
        TransitionFront(Regions.GalleonBoss, lambda l: l.IsBossReachable(Levels.GloomyGalleon)),
    ]),

    Regions.GalleonBoss: Region("Galleon Boss", "Troff 'N' Scoff", Levels.GloomyGalleon, False, None, [
        LocationLogic(Locations.GalleonKey, lambda l: l.IsBossBeatable(Levels.GloomyGalleon)),
    ], [], []),
}
