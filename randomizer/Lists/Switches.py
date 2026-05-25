"""Stores data for each of the game's switches."""

from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Maps import Maps
from randomizer.Enums.Switches import Switches
from randomizer.Enums.SwitchTypes import SwitchType


class SwitchInfo:
    """Store information regarding a switch."""

    def __init__(
        self,
        name: str,
        kong: Kongs,
        switch_type: SwitchType,
        rom_offset: int,
        map_id: int,
        ids: list,
        tied_settings: list = [],
    ):
        """Initialize with given parameters."""
        self.name = name
        self.kong = kong
        self.default_kong = kong
        self.switch_type = switch_type
        self.rom_offset = rom_offset
        self.map_id = map_id
        self.ids = ids
        self.tied_settings = tied_settings


SwitchData = {
    Switches.IslesMonkeyport: SwitchInfo("Isles Monkeyport Pad", Kongs.tiny, SwitchType.PadMove, 0x1C6, Maps.Isles, [0x38]),
    Switches.IslesHelmLobbyGone: SwitchInfo("Helm Lobby Gone Pad", Kongs.chunky, SwitchType.PadMove, 0x1C7, Maps.HideoutHelmLobby, [3]),
    Switches.IslesAztecLobbyFeather: SwitchInfo("Aztec Lobby Feather Switch", Kongs.tiny, SwitchType.GunSwitch, None, Maps.AngryAztecLobby, [16]),
    Switches.IslesFungiLobbyFeather: SwitchInfo("Forest Lobby Feather Switch", Kongs.tiny, SwitchType.GunSwitch, None, Maps.FungiForestLobby, [5]),
    Switches.IslesSpawnRocketbarrel: SwitchInfo("Isles Main Trombone Pad", Kongs.lanky, SwitchType.InstrumentPad, None, Maps.Isles, [0x31]),
    Switches.JapesFeather: SwitchInfo("Japes Hive Area Switches", Kongs.tiny, SwitchType.GunSwitch, None, Maps.JungleJapes, [0x34, 0x35]),
    Switches.JapesRambi: SwitchInfo("Japes Switch to Rambi", Kongs.donkey, SwitchType.GunSwitch, None, Maps.JungleJapes, [0x123]),
    Switches.JapesPainting: SwitchInfo("Japes Switch to Painting", Kongs.diddy, SwitchType.GunSwitch, None, Maps.JungleJapes, [40]),
    Switches.JapesDiddyCave: SwitchInfo("Japes Diddy Cave Switches", Kongs.diddy, SwitchType.GunSwitch, None, Maps.JungleJapes, [0x29, 0x2A]),
    Switches.JapesFreeKong: SwitchInfo("Japes Free Kong Switches", Kongs.donkey, SwitchType.GunSwitch, None, Maps.JungleJapes, [0x30, 0x31, 0x32]),
    Switches.AztecBlueprintDoor: SwitchInfo("Aztec Blueprint Door Switches", Kongs.donkey, SwitchType.GunSwitch, None, Maps.AngryAztec, [0x9D, 0x9E]),
    Switches.AztecLlamaCoconut: SwitchInfo("Aztec Llama Switch (1)", Kongs.donkey, SwitchType.GunSwitch, None, Maps.AngryAztec, [13]),
    Switches.AztecLlamaGrape: SwitchInfo(
        "Aztec Llama Switch (2)",
        Kongs.lanky,
        SwitchType.GunSwitch,
        None,
        Maps.AngryAztec,
        [14],
        [Switches.AztecLlamaCoconut],
    ),
    Switches.AztecLlamaFeather: SwitchInfo(
        "Aztec Llama Switch (3)",
        Kongs.tiny,
        SwitchType.GunSwitch,
        None,
        Maps.AngryAztec,
        [15],
        [Switches.AztecLlamaCoconut, Switches.AztecLlamaGrape],
    ),
    Switches.AztecQuicksandSwitch: SwitchInfo("Aztec Quicksand Tunnel Switch", Kongs.donkey, SwitchType.SlamSwitch, None, Maps.AztecLlamaTemple, [0x69]),
    Switches.AztecGuitar: SwitchInfo("Aztec Guitar Pad", Kongs.diddy, SwitchType.InstrumentPad, None, Maps.AngryAztec, [0x44]),
    Switches.AztecOKONGPuzzle: SwitchInfo("Aztec Tiny Temple Free Kong Switches", Kongs.diddy, SwitchType.PushableButton, None, Maps.AztecTinyTemple, [0x14]),
    Switches.AztecLlamaPuzzle: SwitchInfo("Aztec Llama Temple Free Kong Switches", Kongs.donkey, SwitchType.GunInstrumentCombo, None, Maps.AztecLlamaTemple, [0x12, 0x16]),
    Switches.FactoryFreeKong: SwitchInfo("Factory Free Kong Switch", Kongs.lanky, SwitchType.SlamSwitch, None, Maps.FranticFactory, [0x24]),
    Switches.GalleonLighthouse: SwitchInfo("Galleon Lighthouse Switches", Kongs.donkey, SwitchType.GunSwitch, None, Maps.GloomyGalleon, [0xA, 0xB]),
    Switches.GalleonShipwreck: SwitchInfo("Galleon Shipwreck Switches", Kongs.diddy, SwitchType.GunSwitch, None, Maps.GloomyGalleon, [8, 9]),
    Switches.GalleonCannonGame: SwitchInfo("Galleon Cannon Game Switches", Kongs.chunky, SwitchType.GunSwitch, None, Maps.GloomyGalleon, [6, 7]),
    Switches.FungiYellow: SwitchInfo("Forest Yellow Tunnel Switch", Kongs.lanky, SwitchType.GunSwitch, None, Maps.FungiForest, [30]),
    Switches.FungiGreenFeather: SwitchInfo("Forest Green Tunnel Switches (1)", Kongs.tiny, SwitchType.GunSwitch, None, Maps.FungiForest, [0x18, 0x19]),
    Switches.FungiGreenPineapple: SwitchInfo(
        "Forest Green Tunnel Switches (2)",
        Kongs.chunky,
        SwitchType.GunSwitch,
        None,
        Maps.FungiForest,
        [0x1A, 0x1B],
        [Switches.FungiGreenFeather],
    ),
    Switches.FactoryDarkRoomGrate: SwitchInfo("Factory Grate to Dark Room", Kongs.chunky, SwitchType.PunchGrate, None, Maps.FranticFactory, [0x13C]),
    Switches.FactoryArcadeTunnelGrate: SwitchInfo("Factory Grate to Tunnel Bonus", Kongs.chunky, SwitchType.PunchGrate, None, Maps.FranticFactory, [0x15]),
    Switches.FactoryToyMonsterGrate: SwitchInfo("Factory Grate to Toy Monster", Kongs.chunky, SwitchType.PunchGrate, None, Maps.FranticFactory, [0x3C]),
    Switches.CavesGoneCave: SwitchInfo("Caves Gone Cave", Kongs.chunky, SwitchType.IceWall, None, Maps.CrystalCaves, [0x1E]),
    Switches.CavesSnideCave: SwitchInfo("Caves Snide Cave", Kongs.chunky, SwitchType.IceWall, None, Maps.CrystalCaves, [0x1D]),
    Switches.CavesBoulderCave: SwitchInfo("Caves Boulder Cave", Kongs.chunky, SwitchType.IceWall, None, Maps.CrystalCaves, [0x1F]),
    Switches.CavesLobbyBP: SwitchInfo("Caves Lobby Boulder Side", Kongs.chunky, SwitchType.IceWall, None, Maps.CrystalCavesLobby, [0x0]),
    Switches.CavesLobbyLava: SwitchInfo("Caves Lobby Lava Side", Kongs.chunky, SwitchType.IceWall, None, Maps.CrystalCavesLobby, [0x1]),
    Switches.AztecGongTower: SwitchInfo("Aztec Gong Tower", Kongs.diddy, SwitchType.Gong, None, Maps.AngryAztec, [0x1A, 0x1B, 0x1C, 0x1D]),
    Switches.AztecLobbyGong: SwitchInfo("Aztec Lobby Gongs", Kongs.diddy, SwitchType.Gong, None, Maps.AngryAztecLobby, [0x13, 0x14]),
}

SwitchNameDict = {
    Kongs.donkey: {
        SwitchType.GunSwitch: "Coconut Shooter (Donkey)",
        SwitchType.InstrumentPad: "Bongo Blast (Donkey)",
        SwitchType.MiscActivator: "Gorilla Grab (Donkey)",
        SwitchType.PadMove: "Barrel Blast (Donkey)",
        SwitchType.SlamSwitch: "Donkey",
    },
    Kongs.diddy: {
        SwitchType.GunSwitch: "Peanut Popgun (Diddy)",
        SwitchType.InstrumentPad: "Guitar Gazump (Diddy)",
        SwitchType.MiscActivator: "Chimpy Charge (Diddy)",
        SwitchType.PadMove: "Simian Spring (Diddy)",
        SwitchType.SlamSwitch: "Diddy",
    },
    Kongs.lanky: {
        SwitchType.GunSwitch: "Grape Shooter (Lanky)",
        SwitchType.InstrumentPad: "Trombone Tremor (Lanky)",
        SwitchType.PadMove: "Baboon Balloon (Lanky)",
        SwitchType.SlamSwitch: "Lanky",
    },
    Kongs.tiny: {
        SwitchType.GunSwitch: "Feather Bow (Tiny)",
        SwitchType.InstrumentPad: "Saxophone Slam (Tiny)",
        SwitchType.PadMove: "Monkeyport (Tiny)",
        SwitchType.SlamSwitch: "Tiny",
    },
    Kongs.chunky: {
        SwitchType.GunSwitch: "Pineapple Launcher (Chunky)",
        SwitchType.InstrumentPad: "Triangle Trample (Chunky)",
        SwitchType.PadMove: "Gorilla Gone (Chunky)",
        SwitchType.SlamSwitch: "Chunky",
    },
    Kongs.any: {
        SwitchType.GunSwitch: "Any Gun",
        SwitchType.InstrumentPad: "Any Instrument",
    },
}
