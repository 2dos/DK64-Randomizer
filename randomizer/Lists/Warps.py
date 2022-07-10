"""Designates Bananaport properties."""

from randomizer.Enums.Warps import Warps
from randomizer.Lists.MapsAndExits import Maps


class BananaportData:
    """Information about the bananaport."""

    def __init__(self, *, name="", map_id=0, obj_id_vanilla=0, locked=False, vanilla_warp=0):
        """Initialize with given parameters."""
        self.name = name
        self.map_id = map_id
        self.obj_id_vanilla = obj_id_vanilla
        self.locked = locked
        self.vanilla_warp = vanilla_warp
        self.new_warp = vanilla_warp

    def setNewWarp(self, new_warp):
        """Set new warp type."""
        self.new_warp = new_warp


BananaportVanilla = {
    Warps.JapesNearPortal: BananaportData(name="Jungle Japes: Near Portal", map_id=Maps.JungleJapes, obj_id_vanilla=0x59, vanilla_warp=0),
    Warps.JapesEndOfTunnel: BananaportData(name="Jungle Japes: End of Tunnel", map_id=Maps.JungleJapes, obj_id_vanilla=0x5A, vanilla_warp=0),
    Warps.JapesNearMainTag: BananaportData(name="Jungle Japes: Near Main Tag", map_id=Maps.JungleJapes, obj_id_vanilla=0x98, vanilla_warp=1),
    Warps.JapesNearMountain: BananaportData(name="Jungle Japes: Outside the Mountain", map_id=Maps.JungleJapes, obj_id_vanilla=0x9F, vanilla_warp=1),
    Warps.JapesFarRight: BananaportData(name="Jungle Japes: Near Painting Room", map_id=Maps.JungleJapes, obj_id_vanilla=0x9E, vanilla_warp=2),
    Warps.JapesFarLeft: BananaportData(name="Jungle Japes: Near Baboon Blast", map_id=Maps.JungleJapes, obj_id_vanilla=0x97, vanilla_warp=2),
    Warps.JapesCrankyTunnelNear: BananaportData(name="Jungle Japes: Start of Cranky Tunnel", map_id=Maps.JungleJapes, obj_id_vanilla=0x5E, vanilla_warp=3),
    Warps.JapesCrankyTunnelFar: BananaportData(name="Jungle Japes: Near Cranky", map_id=Maps.JungleJapes, obj_id_vanilla=0x6F, vanilla_warp=3),
    Warps.JapesShellhive: BananaportData(name="Jungle Japes: Outside the Shellhive", map_id=Maps.JungleJapes, obj_id_vanilla=0x12A, vanilla_warp=4),
    Warps.JapesOnMountain: BananaportData(name="Jungle Japes: On top of the Mountain", map_id=Maps.JungleJapes, obj_id_vanilla=0x12B, vanilla_warp=4),
    Warps.AztecNearPortal: BananaportData(name="Angry Aztec: Near Portal", map_id=Maps.AngryAztec, obj_id_vanilla=0x6, vanilla_warp=0),
    Warps.AztecNearCandy: BananaportData(name="Angry Aztec: Near Candy", map_id=Maps.AngryAztec, obj_id_vanilla=0x7, vanilla_warp=0),
    Warps.AztecNearTinyTemple: BananaportData(name="Angry Aztec: Outside Tiny Temple", map_id=Maps.AngryAztec, obj_id_vanilla=0x80, vanilla_warp=1),
    Warps.AztecEndOfTunnel: BananaportData(name="Angry Aztec: End of the Tunnel", map_id=Maps.AngryAztec, obj_id_vanilla=0x7F, vanilla_warp=1),
    Warps.AztecTotemNearLeft: BananaportData(name="Angry Aztec: Near Totem Rocketbarrel", map_id=Maps.AngryAztec, obj_id_vanilla=0x98, vanilla_warp=2),
    Warps.AztecCranky: BananaportData(name="Angry Aztec: Outside Cranky's", map_id=Maps.AngryAztec, obj_id_vanilla=0x95, vanilla_warp=2),
    Warps.AztecTotemNearRight: BananaportData(name="Angry Aztec: Near Llama Temple", map_id=Maps.AngryAztec, obj_id_vanilla=0x73, vanilla_warp=3),
    Warps.AztecFunky: BananaportData(name="Angry Aztec: Outside Funky's", map_id=Maps.AngryAztec, obj_id_vanilla=0xB1, vanilla_warp=3),
    Warps.AztecNearSnide: BananaportData(name="Angry Aztec: Near Snide's", map_id=Maps.AngryAztec, obj_id_vanilla=0x82, vanilla_warp=4),
    Warps.AztecSnoopTunnel: BananaportData(name="Angry Aztec: Sandy Tunnel", map_id=Maps.AngryAztec, obj_id_vanilla=0x87, vanilla_warp=4),
    Warps.LlamaNearLeft: BananaportData(name="Llama Temple: Near the Bongo Pad", map_id=Maps.AztecLlamaTemple, obj_id_vanilla=0x58, vanilla_warp=0),
    Warps.LlamaMatchingGame: BananaportData(name="Llama Temple: Outside Matching Game", map_id=Maps.AztecLlamaTemple, obj_id_vanilla=0x4E, vanilla_warp=0),
    Warps.LlamaNearRight: BananaportData(name="Llama Temple: Near the Trombone Pad", map_id=Maps.AztecLlamaTemple, obj_id_vanilla=0x9A, vanilla_warp=1),
    Warps.LlamaLavaRoom: BananaportData(name="Llama Temple: In the Lava Room", map_id=Maps.AztecLlamaTemple, obj_id_vanilla=0x99, vanilla_warp=1),
    Warps.FactoryNearHatchTunnel: BananaportData(name="Frantic Factory: Near Hatch Tunnel", map_id=Maps.FranticFactory, obj_id_vanilla=0x7D, vanilla_warp=0),
    Warps.FactoryStorageRoom: BananaportData(name="Frantic Factory: Storage Room", map_id=Maps.FranticFactory, obj_id_vanilla=0x142, vanilla_warp=0),
    Warps.FactoryNearBlockTunnel: BananaportData(name="Frantic Factory: Near Block Tower Tunnel", map_id=Maps.FranticFactory, obj_id_vanilla=0x141, vanilla_warp=1),
    Warps.FactoryRAndD: BananaportData(name="Frantic Factory: R&D", map_id=Maps.FranticFactory, obj_id_vanilla=0x144, vanilla_warp=1),
    Warps.FactoryLobbyFar: BananaportData(name="Frantic Factory: Lobby Far", map_id=Maps.FranticFactory, obj_id_vanilla=0xD9, vanilla_warp=2),
    Warps.FactorySnides: BananaportData(name="Frantic Factory: Outside Snide's", map_id=Maps.FranticFactory, obj_id_vanilla=0x143, vanilla_warp=2),
    Warps.FactoryProdBottom: BananaportData(name="Frantic Factory: Production Room (Bottom)", map_id=Maps.FranticFactory, obj_id_vanilla=0x105, vanilla_warp=3),
    Warps.FactoryProdTop: BananaportData(name="Frantic Factory: Production Room (Top)", map_id=Maps.FranticFactory, obj_id_vanilla=0x10C, vanilla_warp=3),
    Warps.FactoryArcade: BananaportData(name="Frantic Factory: Arcade Room", map_id=Maps.FranticFactory, obj_id_vanilla=0x10B, vanilla_warp=4),
    Warps.FactoryFunky: BananaportData(name="Frantic Factory: Outside Funky's", map_id=Maps.FranticFactory, obj_id_vanilla=0xEE, vanilla_warp=4),
    Warps.GalleonNearTunnelIntersection: BananaportData(name="Gloomy Galleon: Near Tunnel Intersection", map_id=Maps.GloomyGalleon, obj_id_vanilla=0x1F7, vanilla_warp=0),
    Warps.GalleonLighthouseRear: BananaportData(name="Gloomy Galleon: Lighthouse Rear", map_id=Maps.GloomyGalleon, obj_id_vanilla=0x1F6, vanilla_warp=0),
    Warps.GalleonNearChestGB: BananaportData(name="Gloomy Galleon: Near Chest Room", map_id=Maps.GloomyGalleon, obj_id_vanilla=0x5F, vanilla_warp=1),
    Warps.GalleonNear2DS: BananaportData(name="Gloomy Galleon: Near 2-Door Ship", map_id=Maps.GloomyGalleon, obj_id_vanilla=0x6C, locked=True, vanilla_warp=1),
    Warps.GalleonNearCranky: BananaportData(name="Gloomy Galleon: Near Cranky's", map_id=Maps.GloomyGalleon, obj_id_vanilla=0x60, vanilla_warp=2),
    Warps.GalleonSnides: BananaportData(name="Gloomy Galleon: Outside Snide's", map_id=Maps.GloomyGalleon, obj_id_vanilla=0x66, vanilla_warp=2),
    Warps.GalleonGoldTower: BananaportData(name="Gloomy Galleon: On a Gold Tower", map_id=Maps.GloomyGalleon, obj_id_vanilla=0x55, vanilla_warp=3),
    Warps.GalleonNearSeal: BananaportData(name="Gloomy Galleon: Near Seal Race", map_id=Maps.GloomyGalleon, obj_id_vanilla=0x56, locked=True, vanilla_warp=3),
    Warps.GalleonNearRocketbarrel: BananaportData(name="Gloomy Galleon: Near Lighthouse Rocketbarrel", map_id=Maps.GloomyGalleon, obj_id_vanilla=0x16, vanilla_warp=4),
    Warps.GalleonNearFunky: BananaportData(name="Gloomy Galleon: Near Funky's", map_id=Maps.GloomyGalleon, obj_id_vanilla=0x15, locked=True, vanilla_warp=4),
    Warps.FungiClock1: BananaportData(name="Fungi Forest: Clock (1)", map_id=Maps.FungiForest, obj_id_vanilla=0x36, vanilla_warp=0),
    Warps.FungiMill: BananaportData(name="Fungi Forest: Mill", map_id=Maps.FungiForest, obj_id_vanilla=0x35, vanilla_warp=0),
    Warps.FungiClock2: BananaportData(name="Fungi Forest: Clock (2)", map_id=Maps.FungiForest, obj_id_vanilla=0x49, vanilla_warp=1),
    Warps.FungiFunky: BananaportData(name="Fungi Forest: Outside Funky's", map_id=Maps.FungiForest, obj_id_vanilla=0x4A, vanilla_warp=1),
    Warps.FungiClock3: BananaportData(name="Fungi Forest: Clock (3)", map_id=Maps.FungiForest, obj_id_vanilla=0x4B, vanilla_warp=2),
    Warps.FungiMushEntrance: BananaportData(name="Fungi Forest: Giant Mushroom Lowest Entrance", map_id=Maps.FungiForest, obj_id_vanilla=0x4E, vanilla_warp=2),
    Warps.FungiClock4: BananaportData(name="Fungi Forest: Clock (4)", map_id=Maps.FungiForest, obj_id_vanilla=0x4F, vanilla_warp=3),
    Warps.FungiOwlTree: BananaportData(name="Fungi Forest: Owl Tree", map_id=Maps.FungiForest, obj_id_vanilla=0x51, vanilla_warp=3),
    Warps.FungiTopMush: BananaportData(name="Fungi Forest: Giant Mushroom (Top)", map_id=Maps.FungiForest, obj_id_vanilla=0x56, vanilla_warp=4),
    Warps.FungiLowMush: BananaportData(name="Fungi Forest: Giant Mushroom (Bottom)", map_id=Maps.FungiForest, obj_id_vanilla=0x55, vanilla_warp=4),
    Warps.CavesNearLeft: BananaportData(name="Crystal Caves: Near Left", map_id=Maps.CrystalCaves, obj_id_vanilla=0x22, vanilla_warp=0),
    Warps.CavesNearChunkyShield: BananaportData(name="Crystal Caves: Near Chunky Shield", map_id=Maps.CrystalCaves, obj_id_vanilla=0x21, vanilla_warp=0),
    Warps.CavesNearRight: BananaportData(name="Crystal Caves: Near Right", map_id=Maps.CrystalCaves, obj_id_vanilla=0x37, vanilla_warp=1),
    Warps.CavesWaterfall: BananaportData(name="Crystal Caves: Near Waterfall", map_id=Maps.CrystalCaves, obj_id_vanilla=0x36, vanilla_warp=1),
    Warps.CavesNearIglooTag: BananaportData(name="Crystal Caves: Near Igloo Tag", map_id=Maps.CrystalCaves, obj_id_vanilla=0x57, vanilla_warp=2),
    Warps.CavesBonusRoom: BananaportData(name="Crystal Caves: Inside Bonus Room", map_id=Maps.CrystalCaves, obj_id_vanilla=0x56, locked=True, vanilla_warp=2),
    Warps.CavesThinPillar: BananaportData(name="Crystal Caves: On the Thin Pillar", map_id=Maps.CrystalCaves, obj_id_vanilla=0x6B, vanilla_warp=3),
    Warps.CavesBlueprintRoom: BananaportData(name="Crystal Caves: Inside Blueprint Room", map_id=Maps.CrystalCaves, obj_id_vanilla=0x6A, locked=True, vanilla_warp=3),
    Warps.CavesThickPillar: BananaportData(name="Crystal Caves: On the Thick Pillar", map_id=Maps.CrystalCaves, obj_id_vanilla=0xB5, locked=True, vanilla_warp=4),
    Warps.CavesCabins: BananaportData(name="Crystal Caves: On the 5-Door Cabin", map_id=Maps.CrystalCaves, obj_id_vanilla=0x60, vanilla_warp=4),
    Warps.CastleCenter1: BananaportData(name="Creepy Castle: Center (1)", map_id=Maps.CreepyCastle, obj_id_vanilla=0x24, vanilla_warp=0),
    Warps.CastleRear: BananaportData(name="Creepy Castle: Rear", map_id=Maps.CreepyCastle, obj_id_vanilla=0x22, vanilla_warp=0),
    Warps.CastleCenter2: BananaportData(name="Creepy Castle: Center (2)", map_id=Maps.CreepyCastle, obj_id_vanilla=0x2B, vanilla_warp=1),
    Warps.CastleRocketbarrel: BananaportData(name="Creepy Castle: Rocketbarrel", map_id=Maps.CreepyCastle, obj_id_vanilla=0x28, vanilla_warp=1),
    Warps.CastleCenter3: BananaportData(name="Creepy Castle: Center (3)", map_id=Maps.CreepyCastle, obj_id_vanilla=0x2C, vanilla_warp=2),
    Warps.CastleCranky: BananaportData(name="Creepy Castle: Outside Cranky's", map_id=Maps.CreepyCastle, obj_id_vanilla=0x23, vanilla_warp=2),
    Warps.CastleCenter4: BananaportData(name="Creepy Castle: Center (4)", map_id=Maps.CreepyCastle, obj_id_vanilla=0x21, vanilla_warp=3),
    Warps.CastleTrashCan: BananaportData(name="Creepy Castle: Outside Trash Can", map_id=Maps.CreepyCastle, obj_id_vanilla=0x29, vanilla_warp=3),
    Warps.CastleCenter5: BananaportData(name="Creepy Castle: Center (5)", map_id=Maps.CreepyCastle, obj_id_vanilla=0x2D, vanilla_warp=4),
    Warps.CastleTop: BananaportData(name="Creepy Castle: Top", map_id=Maps.CreepyCastle, obj_id_vanilla=0x2A, vanilla_warp=4),
    Warps.CryptNearLeft: BananaportData(name="Crypt: Near Left", map_id=Maps.CastleCrypt, obj_id_vanilla=0x18, vanilla_warp=0),
    Warps.CryptFarLeft: BananaportData(name="Crypt: Far Left", map_id=Maps.CastleCrypt, obj_id_vanilla=0x1D, vanilla_warp=0),
    Warps.CryptNearCenter: BananaportData(name="Crypt: Near Center", map_id=Maps.CastleCrypt, obj_id_vanilla=0x19, vanilla_warp=1),
    Warps.CryptFarCenter: BananaportData(name="Crypt: Outside Minecart", map_id=Maps.CastleCrypt, obj_id_vanilla=0x1C, vanilla_warp=1),
    Warps.CryptNearRight: BananaportData(name="Crypt: Near Right", map_id=Maps.CastleCrypt, obj_id_vanilla=0x1A, vanilla_warp=2),
    Warps.CryptFarRight: BananaportData(name="Crypt: Far Right", map_id=Maps.CastleCrypt, obj_id_vanilla=0x1B, vanilla_warp=2),
    Warps.IslesRing1: BananaportData(name="DK Isles: Ring (1)", map_id=Maps.Isles, obj_id_vanilla=0x10, vanilla_warp=0),
    Warps.IslesKLumsy: BananaportData(name="DK Isles: Outside K. Lumsy's Prison", map_id=Maps.Isles, obj_id_vanilla=0x11, vanilla_warp=0),
    Warps.IslesRing2: BananaportData(name="DK Isles: Ring (2)", map_id=Maps.Isles, obj_id_vanilla=0x12, vanilla_warp=1),
    Warps.IslesAztecLobby: BananaportData(name="DK Isles: Outside Aztec Lobby", map_id=Maps.Isles, obj_id_vanilla=0x13, vanilla_warp=1),
    Warps.IslesRing3: BananaportData(name="DK Isles: Ring (3)", map_id=Maps.Isles, obj_id_vanilla=0x16, vanilla_warp=2),
    Warps.IslesWaterfall: BananaportData(name="DK Isles: Waterfall", map_id=Maps.Isles, obj_id_vanilla=0x14, vanilla_warp=2),
    Warps.IslesRing4: BananaportData(name="DK Isles: Ring (4)", map_id=Maps.Isles, obj_id_vanilla=0x17, vanilla_warp=3),
    Warps.IslesFactoryLobby: BananaportData(name="DK Isles: Outside Factory Lobby", map_id=Maps.Isles, obj_id_vanilla=0x18, vanilla_warp=3),
    Warps.IslesRing5: BananaportData(name="DK Isles: Ring (5)", map_id=Maps.Isles, obj_id_vanilla=0x15, vanilla_warp=4),
    Warps.IslesFairyIsland: BananaportData(name="DK Isles: Fairy Island", map_id=Maps.Isles, obj_id_vanilla=0x19, vanilla_warp=4),
}
