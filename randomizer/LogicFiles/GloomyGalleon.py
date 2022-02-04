# fmt: off
"""Logic file for Gloomy Galleon."""

from randomizer.Enums.Events import Events
from randomizer.Enums.TransitionFronts import TransitionFronts
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Regions import Regions
from randomizer.LogicClasses import Event, TransitionFront, LocationLogic, Region

LogicRegions = {
    Regions.GloomyGalleonStart: Region("Gloomy Galleon Start", Levels.GloomyGalleon, True, None, [
        LocationLogic(Locations.GalleonDonkeyMedal, lambda l: l.ColoredBananas[Levels.GloomyGalleon][Kongs.donkey] >= 75),
        LocationLogic(Locations.GalleonDiddyMedal, lambda l: l.ColoredBananas[Levels.GloomyGalleon][Kongs.diddy] >= 75),
        LocationLogic(Locations.GalleonLankyMedal, lambda l: l.ColoredBananas[Levels.GloomyGalleon][Kongs.lanky] >= 75),
        LocationLogic(Locations.GalleonTinyMedal, lambda l: l.ColoredBananas[Levels.GloomyGalleon][Kongs.tiny] >= 75),
        LocationLogic(Locations.GalleonChunkyMedal, lambda l: l.ColoredBananas[Levels.GloomyGalleon][Kongs.chunky] >= 75),
        LocationLogic(Locations.GalleonChunkyChest, lambda l: l.punch and l.chunky),
        LocationLogic(Locations.GalleonTinyKasplat, lambda l: l.tiny),
        LocationLogic(Locations.GalleonBattleArena, lambda l: l.punch and l.chunky),
        LocationLogic(Locations.GalleonBananaFairybyCranky, lambda l: l.camera and l.punch and l.chunky),
    ], [
        Event(Events.GalleonEntered, lambda l: True),
        Event(Events.GalleonLankySwitch, lambda l: l.Slam and l.lanky),
        Event(Events.GalleonTinySwitch, lambda l: l.Slam and l.tiny),
        Event(Events.LighthouseGateOpened, lambda l: l.coconut and l.donkey),
        Event(Events.ShipyardGateOpened, lambda l: l.peanut and l.diddy),
    ], [
        TransitionFront(Regions.GloomyGalleonLobby, lambda l: True, TransitionFronts.GalleonToIsles),
        TransitionFront(Regions.GalleonBeyondPineappleGate, lambda l: Events.WaterSwitch in l.Events and l.pineapple and l.chunky),
        TransitionFront(Regions.LighthouseArea, lambda l: l.settings.shuffle_loading_zones == "all" or Events.LighthouseGateOpened in l.Events),
        # Gate to shipyard opened in rando if loading zones randomized
        TransitionFront(Regions.Shipyard, lambda l: l.settings.shuffle_loading_zones == "all" or Events.ShipyardGateOpened in l.Events),
        TransitionFront(Regions.Cranky, lambda l: True),
        TransitionFront(Regions.GalleonBossLobby, lambda l: True),
    ]),

    Regions.GalleonBeyondPineappleGate: Region("Galleon Beyond Pineapple Gate", Levels.GloomyGalleon, False, None, [
        LocationLogic(Locations.GalleonChunkyCannonGame, lambda l: l.ischunky),
        LocationLogic(Locations.GalleonLankyKasplat, lambda l: l.islanky),
    ], [], [
        TransitionFront(Regions.GloomyGalleonStart, lambda l: True),
    ]),

    Regions.LighthouseArea: Region("Lighthouse Area", Levels.GloomyGalleon, True, -1, [
        LocationLogic(Locations.GalleonDiddyShipSwitch, lambda l: Events.ActivatedLighthouse in l.Events and l.jetpack and l.Slam and l.diddy),
        LocationLogic(Locations.GalleonLankyEnguardeChest, lambda l: Events.LighthouseEnguarde in l.Events and l.lanky),
        LocationLogic(Locations.GalleonDiddyKasplat, lambda l: l.diddy),
    ], [
        Event(Events.WaterSwitch, lambda l: True),
        Event(Events.LighthouseEnguarde, lambda l: l.lanky),
        Event(Events.SealReleased, lambda l: l.blast and l.donkey),
        Event(Events.MechafishSummoned, lambda l: l.jetpack and l.guitar and l.diddy),
        Event(Events.GalleonChunkyPad, lambda l: l.triangle and l.chunky),
    ], [
        # Rare case of needing to open gate before being able to go through backwards
        TransitionFront(Regions.GloomyGalleonStart, lambda l: l.settings.shuffle_loading_zones == "all" or Events.LighthouseGateOpened in l.Events),
        TransitionFront(Regions.Lighthouse, lambda l: l.Slam and l.isdonkey, TransitionFronts.GalleonLighthouseAreaToLighthouse),
        TransitionFront(Regions.MermaidRoom, lambda l: l.mini and l.istiny, TransitionFronts.GalleonLighthousAreaToMermaid),
        TransitionFront(Regions.SickBay, lambda l: Events.ActivatedLighthouse in l.Events and l.Slam and l.ischunky, TransitionFronts.GalleonLighthouseAreaToSickBay),
        TransitionFront(Regions.Snide, lambda l: True),
        TransitionFront(Regions.GalleonBossLobby, lambda l: Events.LighthouseEnguarde in l.Events),
    ]),

    Regions.Lighthouse: Region("Lighthouse", Levels.GloomyGalleon, False, -1, [
        LocationLogic(Locations.GalleonDonkeyLighthouse, lambda l: Events.ActivatedLighthouse in l.Events)
    ], [
        Event(Events.ActivatedLighthouse, lambda l: l.grab and l.isdonkey),
    ], [
        TransitionFront(Regions.LighthouseArea, lambda l: True, TransitionFronts.GalleonLighthouseToLighthouseArea),
    ]),

    Regions.MermaidRoom: Region("Mermaid Room", Levels.GloomyGalleon, False, None, [
        LocationLogic(Locations.GalleonTinyPearls, lambda l: Events.PearlsCollected in l.Events and l.istiny),
    ], [], [
        TransitionFront(Regions.LighthouseArea, lambda l: True, TransitionFronts.GalleonMermaidToLighthouseArea),
    ]),

    Regions.SickBay: Region("Sick Bay", Levels.GloomyGalleon, False, -1, [
        LocationLogic(Locations.GalleonChunkySeasick, lambda l: l.punch and l.ischunky),
    ], [], [
        TransitionFront(Regions.LighthouseArea, lambda l: True, TransitionFronts.GalleonSickBayToLighthouseArea),
    ]),

    Regions.Shipyard: Region("Shipyard", Levels.GloomyGalleon, True, None, [
        LocationLogic(Locations.GalleonDonkeyFreetheSeal, lambda l: Events.SealReleased in l.Events and Events.WaterSwitch in l.Events and l.donkey),
        LocationLogic(Locations.GalleonChunkyKasplat, lambda l: l.chunky),
    ], [
        Event(Events.ShipyardEnguarde, lambda l: l.lanky),
        Event(Events.ShipyardTreasureRoomOpened, lambda l: Events.ShipyardEnguarde in l.Events and Events.WaterSwitch in l.Events),
    ], [
        TransitionFront(Regions.GloomyGalleonStart, lambda l: Events.ShipyardGateOpened in l.Events),
        TransitionFront(Regions.SealRace, lambda l: Events.SealReleased in l.Events and Events.WaterSwitch in l.Events and l.isdonkey, TransitionFronts.GalleonShipyardToSeal),
        TransitionFront(Regions.TreasureRoom, lambda l: Events.ShipyardTreasureRoomOpened in l.Events),
        TransitionFront(Regions.Submarine, lambda l: l.mini and l.istiny, TransitionFronts.GalleonShipyardToSubmarine),
        TransitionFront(Regions.Mechafish, lambda l: Events.MechafishSummoned in l.Events and l.isdiddy),
        TransitionFront(Regions.LankyShip, lambda l: Events.GalleonLankySwitch in l.Events and l.islanky, TransitionFronts.GalleonShipyardToLanky),
        TransitionFront(Regions.TinyShip, lambda l: Events.GalleonTinySwitch in l.Events and l.istiny, TransitionFronts.GalleonShipyardToTiny),
        TransitionFront(Regions.BongosShip, lambda l: l.bongos and l.isdonkey, TransitionFronts.GalleonShipyardToBongos),
        TransitionFront(Regions.GuitarShip, lambda l: l.guitar and l.isdiddy, TransitionFronts.GalleonShipyardToGuitar),
        TransitionFront(Regions.TromboneShip, lambda l: l.trombone and l.islanky, TransitionFronts.GalleonShipyardToTrombone),
        TransitionFront(Regions.SaxophoneShip, lambda l: l.saxophone and l.istiny, TransitionFronts.GalleonShipyardToSaxophone),
        TransitionFront(Regions.TriangleShip, lambda l: Events.GalleonChunkyPad in l.Events and l.ischunky, TransitionFronts.GalleonShipyardToTriangle),
        TransitionFront(Regions.Candy, lambda l: True),
        TransitionFront(Regions.Funky, lambda l: True),
        TransitionFront(Regions.GalleonBossLobby, lambda l: True),
    ]),

    Regions.SealRace: Region("Seal Race", Levels.GloomyGalleon, False, None, [
        LocationLogic(Locations.GalleonDonkeySealRace, lambda l: l.isdonkey),
    ], [], [
        TransitionFront(Regions.Shipyard, lambda l: True, TransitionFronts.GalleonSealToShipyard),
    ]),

    # Water level needs to be raised and you spring up as diddy to get killed by the kasplat
    # Or, any kong having teleporter access works too
    Regions.TreasureRoom: Region("Treasure Room", Levels.GloomyGalleon, True, TransitionFront(Regions.GloomyGalleonStart, lambda l: Events.TreasureRoomTeleporterUnlocked in l.Events and l.HasAccess(Regions.Shipyard, Kongs.rainbow) or (Events.WaterSwitch in l.Events and l.spring and l.isdiddy)), [
        LocationLogic(Locations.GalleonDiddyGoldTower, lambda l: l.spring and l.diddy),
        LocationLogic(Locations.GalleonLankyGoldTower, lambda l: l.balloon and l.lanky),
        LocationLogic(Locations.GalleonDonkeyKasplat, lambda l: Events.TreasureRoomTeleporterUnlocked in l.Events and l.HasAccess(Regions.Shipyard, Kongs.donkey)),
    ], [
        Event(Events.TreasureRoomTeleporterUnlocked, lambda l: l.spring and l.diddy),
    ], [
        TransitionFront(Regions.Shipyard, lambda l: Events.ShipyardTreasureRoomOpened in l.Events),
        TransitionFront(Regions.TinyChest, lambda l: l.mini and l.istiny, TransitionFronts.GalleonTreasureToChest),
    ]),

    Regions.TinyChest: Region("Tiny Chest", Levels.GloomyGalleon, False, -1, [], [
        Event(Events.PearlsCollected, lambda l: l.istiny),
    ], [
        TransitionFront(Regions.TreasureRoom, lambda l: True, TransitionFronts.GalleonChestToTreasure),
    ]),

    Regions.Submarine: Region("Submarine", Levels.GloomyGalleon, False, -1, [
        LocationLogic(Locations.GalleonTinySubmarine, lambda l: l.istiny),
    ], [], [
        TransitionFront(Regions.Shipyard, lambda l: True, TransitionFronts.GalleonSubmarineToShipyard),
    ]),

    Regions.Mechafish: Region("Mechafish", Levels.GloomyGalleon, False, -1, [
        LocationLogic(Locations.GalleonDiddyMechafish, lambda l: l.peanut and l.isdiddy),
    ], [], [
        TransitionFront(Regions.Shipyard, lambda l: True)
    ]),

    Regions.LankyShip: Region("Lanky Ship", Levels.GloomyGalleon, False, None, [
        LocationLogic(Locations.GalleonLanky2DoorShip, lambda l: l.islanky),
    ], [], [
        TransitionFront(Regions.Shipyard, lambda l: True, TransitionFronts.GalleonLankyToShipyard),
    ]),

    Regions.TinyShip: Region("Tiny Ship", Levels.GloomyGalleon, False, -1, [
        LocationLogic(Locations.GalleonTiny2DoorShip, lambda l: l.istiny),
    ], [], [
        TransitionFront(Regions.Shipyard, lambda l: True, TransitionFronts.GalleonTinyToShipyard),
    ]),

    Regions.BongosShip: Region("Bongos Ship", Levels.GloomyGalleon, False, -1, [
        LocationLogic(Locations.GalleonDonkey5DoorShip, lambda l: l.isdonkey),
    ], [], [
        TransitionFront(Regions.Shipyard, lambda l: True, TransitionFronts.GalleonBongosToShipyard),
    ]),

    Regions.GuitarShip: Region("Guitar Ship", Levels.GloomyGalleon, False, -1, [
        LocationLogic(Locations.GalleonDiddy5DoorShip, lambda l: l.isdiddy),
    ], [], [
        TransitionFront(Regions.Shipyard, lambda l: True, TransitionFronts.GalleonGuitarToShipyard),
    ]),

    Regions.TromboneShip: Region("Trombone Ship", Levels.GloomyGalleon, False, -1, [
        LocationLogic(Locations.GalleonLanky5DoorShip, lambda l: l.islanky),
    ], [], [
        TransitionFront(Regions.Shipyard, lambda l: True, TransitionFronts.GalleonTromboneToShipyard),
    ]),

    Regions.SaxophoneShip: Region("Saxophone Ship", Levels.GloomyGalleon, False, -1, [
        LocationLogic(Locations.GalleonTiny5DoorShip, lambda l: l.istiny),
        LocationLogic(Locations.GalleonBananaFairy5DoorShip, lambda l: l.camera),
    ], [], [
        TransitionFront(Regions.Shipyard, lambda l: True, TransitionFronts.GalleonSaxophoneToShipyard),
    ]),

    Regions.TriangleShip: Region("Triangle Ship", Levels.GloomyGalleon, False, -1, [
        LocationLogic(Locations.GalleonChunky5DoorShip, lambda l: l.ischunky),
    ], [], [
        TransitionFront(Regions.Shipyard, lambda l: True, TransitionFronts.GalleonTriangleToShipyard),
    ]),

    Regions.GalleonBossLobby: Region("Galleon Boss Lobby", Levels.GloomyGalleon, True, None, [], [], [
        TransitionFront(Regions.GalleonBoss, lambda l: l.islanky and sum(l.ColoredBananas[Levels.GloomyGalleon]) >= l.settings.BossBananas[Levels.GloomyGalleon - 1]),
    ]),

    Regions.GalleonBoss: Region("Galleon Boss", Levels.GloomyGalleon, False, None, [
        LocationLogic(Locations.GalleonKey, lambda l: l.islanky),
    ], [], []),
}
