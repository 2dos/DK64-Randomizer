# fmt: off
"""Logic file for Gloomy Galleon."""

from randomizer.Enums.Events import Events
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Regions import Regions
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Kongs import Kongs
from randomizer.LogicClasses import Event, Exit, LocationLogic, Region

LogicRegions = {
    Regions.GloomyGalleonStart: Region("Gloomy Galleon Start", Levels.GloomyGalleon, True, [
        LocationLogic(Locations.GalleonDonkeyMedal, lambda l: l.ColoredBananas[Levels.GloomyGalleon][Kongs.donkey] >= 75),
        LocationLogic(Locations.GalleonDiddyMedal, lambda l: l.ColoredBananas[Levels.GloomyGalleon][Kongs.diddy] >= 75),
        LocationLogic(Locations.GalleonLankyMedal, lambda l: l.ColoredBananas[Levels.GloomyGalleon][Kongs.lanky] >= 75),
        LocationLogic(Locations.GalleonTinyMedal, lambda l: l.ColoredBananas[Levels.GloomyGalleon][Kongs.tiny] >= 75),
        LocationLogic(Locations.GalleonChunkyMedal, lambda l: l.ColoredBananas[Levels.GloomyGalleon][Kongs.chunky] >= 75),
        LocationLogic(Locations.GalleonChunkyChest, lambda l: l.punch),
        LocationLogic(Locations.GalleonTinyKasplat, lambda l: l.istiny),
        LocationLogic(Locations.GalleonBattleArena, lambda l: l.punch),
        LocationLogic(Locations.GalleonBananaFairybyCranky, lambda l: l.camera and l.punch),
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

    Regions.GalleonBeyondPineappleGate: Region("Galleon Beyond Pineapple Gate", Levels.GloomyGalleon, False, [
        LocationLogic(Locations.GalleonChunkyCannonGame, lambda l: l.ischunky),
        LocationLogic(Locations.GalleonLankyKasplat, lambda l: l.islanky),
    ], [], []),

    Regions.LighthouseArea: Region("Lighthouse Area", Levels.GloomyGalleon, True, [
        LocationLogic(Locations.GalleonDiddyShipSwitch, lambda l: Events.ActivatedLighthouse in l.Events and l.jetpack and l.Slam),
        LocationLogic(Locations.GalleonLankyEnguardeChest, lambda l: Events.LighthouseEnguarde in l.Events and l.islanky),
        LocationLogic(Locations.GalleonDiddyKasplat, lambda l: l.isdiddy),
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

    Regions.Lighthouse: Region("Lighthouse", Levels.GloomyGalleon, False, [
        LocationLogic(Locations.GalleonDonkeyLighthouse, lambda l: Events.ActivatedLighthouse in l.Events)
    ], [
        Event(Events.ActivatedLighthouse, lambda l: l.grab and l.isdonkey),
    ], [
        Exit(Regions.LighthouseArea, lambda l: True),
    ]),

    Regions.MermaidRoom: Region("Mermaid Room", Levels.GloomyGalleon, False, [
        LocationLogic(Locations.GalleonTinyPearls, lambda l: Events.PearlsCollected in l.Events and l.istiny),
    ], [], [
        Exit(Regions.LighthouseArea, lambda l: True),
    ]),

    Regions.SickBay: Region("Sick Bay", Levels.GloomyGalleon, False, [
        LocationLogic(Locations.GalleonChunkySeasick, lambda l: l.punch and l.ischunky),
    ], [], [
        Exit(Regions.LighthouseArea, lambda l: True),
    ]),

    Regions.Shipyard: Region("Shipyard", Levels.GloomyGalleon, True, [
        LocationLogic(Locations.GalleonDonkeyFreetheSeal, lambda l: Events.SealReleased in l.Events and l.isdonkey),
        LocationLogic(Locations.GalleonChunkyKasplat, lambda l: l.ischunky),
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

    Regions.SealRace: Region("Seal Race", Levels.GloomyGalleon, False, [
        LocationLogic(Locations.GalleonDonkeySealRace, lambda l: l.isdonkey),
    ], [], []),

    Regions.TreasureRoom: Region("Treasure Room", Levels.GloomyGalleon, True, [
        LocationLogic(Locations.GalleonDiddyGoldTower, lambda l: l.spring),
        LocationLogic(Locations.GalleonLankyGoldTower, lambda l: l.balloon),
        LocationLogic(Locations.GalleonDonkeyKasplat, lambda l: Events.TreasureRoomTeleporterUnlocked in l.Events and l.isdonkey),
    ], [
        Event(Events.TreasureRoomTeleporterUnlocked, lambda l: l.spring),
    ], [
        Exit(Regions.TinyChest, lambda l: l.mini and l.istiny),
    ]),

    Regions.TinyChest: Region("Tiny Chest", Levels.GloomyGalleon, False, [], [
        Event(Events.PearlsCollected, lambda l: l.istiny),
    ], [
        Exit(Regions.TreasureRoom, lambda l: True),
    ]),

    Regions.Submarine: Region("Submarine", Levels.GloomyGalleon, False, [
        LocationLogic(Locations.GalleonTinySubmarine, lambda l: l.istiny),
    ], [], [
        Exit(Regions.Shipyard, lambda l: lambda l: True),
    ]),

    Regions.Mechafish: Region("Mechafish", Levels.GloomyGalleon, False, [
        LocationLogic(Locations.GalleonDiddyMechafish, lambda l: l.peanut and l.isdiddy),
    ], [], []),

    Regions.LankyShip: Region("Lanky Ship", Levels.GloomyGalleon, False, [
        LocationLogic(Locations.GalleonLanky2DoorShip, lambda l: l.islanky),
    ], [], [
        Exit(Regions.Shipyard, lambda l: True),
    ]),

    Regions.TinyShip: Region("Tiny Ship", Levels.GloomyGalleon, False, [
        LocationLogic(Locations.GalleonTiny2DoorShip, lambda l: l.istiny),
    ], [], [
        Exit(Regions.Shipyard, lambda l: True),
    ]),

    Regions.BongosShip: Region("Bongos Ship", Levels.GloomyGalleon, False, [
        LocationLogic(Locations.GalleonDonkey5DoorShip, lambda l: l.isdonkey),
    ], [], [
        Exit(Regions.Shipyard, lambda l: True),
    ]),

    Regions.GuitarShip: Region("Guitar Ship", Levels.GloomyGalleon, False, [
        LocationLogic(Locations.GalleonDiddy5DoorShip, lambda l: l.isdiddy),
    ], [], [
        Exit(Regions.Shipyard, lambda l: True),
    ]),

    Regions.TromboneShip: Region("Trombone Ship", Levels.GloomyGalleon, False, [
        LocationLogic(Locations.GalleonLanky5DoorShip, lambda l: l.islanky),
    ], [], [
        Exit(Regions.Shipyard, lambda l: True),
    ]),

    Regions.SaxophoneShip: Region("Saxophone Ship", Levels.GloomyGalleon, False, [
        LocationLogic(Locations.GalleonTiny5DoorShip, lambda l: l.istiny),
        LocationLogic(Locations.GalleonBananaFairy5DoorShip, lambda l: l.camera),
    ], [], [
        Exit(Regions.Shipyard, lambda l: True),
    ]),

    Regions.TriangleShip: Region("Triangle Ship", Levels.GloomyGalleon, False, [
        LocationLogic(Locations.GalleonChunky5DoorShip, lambda l: l.ischunky),
    ], [], [
        Exit(Regions.Shipyard, lambda l: True),
    ]),

    Regions.GalleonBossLobby: Region("Galleon Boss Lobby", Levels.GloomyGalleon, True, [], [], [
        Exit(Regions.GalleonBoss, lambda l: l.islanky and sum(l.ColoredBananas[Levels.GloomyGalleon]) >= 250),
    ]),

    Regions.GalleonBoss: Region("Galleon Boss", Levels.GloomyGalleon, False, [
        LocationLogic(Locations.GalleonKey, lambda l: l.islanky),
    ], [], []),
}
