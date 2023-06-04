"""Designates Bananaport properties."""

from re import sub

from randomizer.Enums.Events import Events
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Regions import Regions
from randomizer.Enums.Warps import Warps
from randomizer.Lists.MapsAndExits import Maps


class BananaportData:
    """Information about the bananaport."""

    def __init__(self, *, name="", map_id=0, region_id=0, obj_id_vanilla=0, locked=False, vanilla_warp=0, swap_index=None, event=None, restricted=False):
        """Initialize with given parameters."""
        self.name = name
        self.map_id = map_id
        self.region_id = region_id
        self.destination_region_id = None
        self.obj_id_vanilla = obj_id_vanilla
        self.locked = locked
        self.vanilla_warp = vanilla_warp
        self.new_warp = vanilla_warp
        self.swap_index = swap_index
        self.restricted = restricted  # Defined by whether all kongs can access the bananaport without tag anywhere or bananaports
        self.event = event
        self.event_logic = lambda l: event in l.Events
        self.cross_map_placed = False
        vanilla_pair_index = swap_index % 2
        if vanilla_pair_index == 0:
            self.tied_index = swap_index + 1
        else:
            self.tied_index = swap_index - 1

    def setNewWarp(self, new_warp):
        """Set new warp type."""
        self.new_warp = new_warp


BananaportVanilla = {
    # Japes
    Warps.JapesNearPortal: BananaportData(
        name="Jungle Japes: Near Portal", map_id=Maps.JungleJapes, region_id=Regions.JungleJapesStart, obj_id_vanilla=0x59, vanilla_warp=0, swap_index=10, event=Events.JapesW1aTagged
    ),
    Warps.JapesEndOfTunnel: BananaportData(
        name="Jungle Japes: End of Tunnel", map_id=Maps.JungleJapes, region_id=Regions.JungleJapesStart, obj_id_vanilla=0x5A, vanilla_warp=0, swap_index=11, event=Events.JapesW1bTagged
    ),
    Warps.JapesNearMainTag: BananaportData(
        name="Jungle Japes: Near Main Tag", map_id=Maps.JungleJapes, region_id=Regions.JungleJapesStart, obj_id_vanilla=0x98, vanilla_warp=1, swap_index=12, event=Events.JapesW2aTagged
    ),
    Warps.JapesNearMountain: BananaportData(
        name="Jungle Japes: Outside the Mountain", map_id=Maps.JungleJapes, region_id=Regions.JungleJapesMain, obj_id_vanilla=0x9F, vanilla_warp=1, swap_index=13, event=Events.JapesW2bTagged
    ),
    Warps.JapesFarRight: BananaportData(
        name="Jungle Japes: Near Painting Room", map_id=Maps.JungleJapes, region_id=Regions.JungleJapesMain, obj_id_vanilla=0x9E, vanilla_warp=2, swap_index=14, event=Events.JapesW3aTagged
    ),
    Warps.JapesFarLeft: BananaportData(
        name="Jungle Japes: Near Baboon Blast", map_id=Maps.JungleJapes, region_id=Regions.JungleJapesStart, obj_id_vanilla=0x97, vanilla_warp=2, swap_index=15, event=Events.JapesW3bTagged
    ),
    Warps.JapesCrankyTunnelNear: BananaportData(
        name="Jungle Japes: Start of Cranky Tunnel", map_id=Maps.JungleJapes, region_id=Regions.JapesBeyondCoconutGate2, obj_id_vanilla=0x5E, vanilla_warp=3, swap_index=16, event=Events.JapesW4aTagged
    ),
    Warps.JapesCrankyTunnelFar: BananaportData(
        name="Jungle Japes: Near Cranky", map_id=Maps.JungleJapes, region_id=Regions.JapesBeyondCoconutGate2, obj_id_vanilla=0x6F, vanilla_warp=3, swap_index=17, event=Events.JapesW4bTagged
    ),
    Warps.JapesShellhive: BananaportData(
        name="Jungle Japes: Outside the Shellhive", map_id=Maps.JungleJapes, region_id=Regions.JapesBeyondFeatherGate, obj_id_vanilla=0x12A, vanilla_warp=4, swap_index=18, event=Events.JapesW5aTagged
    ),
    Warps.JapesOnMountain: BananaportData(
        name="Jungle Japes: On top of the Mountain",
        map_id=Maps.JungleJapes,
        region_id=Regions.JapesTopOfMountain,
        obj_id_vanilla=0x12B,
        vanilla_warp=4,
        swap_index=19,
        event=Events.JapesW5bTagged,
        restricted=True,
    ),
    # Aztec
    Warps.AztecNearPortal: BananaportData(
        name="Angry Aztec: Near Portal", map_id=Maps.AngryAztec, region_id=Regions.BetweenVinesByPortal, obj_id_vanilla=0x6, vanilla_warp=0, swap_index=20, event=Events.AztecW1aTagged
    ),
    Warps.AztecNearCandy: BananaportData(
        name="Angry Aztec: Near Candy", map_id=Maps.AngryAztec, region_id=Regions.AngryAztecOasis, obj_id_vanilla=0x7, vanilla_warp=0, swap_index=21, event=Events.AztecW1bTagged
    ),
    Warps.AztecNearTinyTemple: BananaportData(
        name="Angry Aztec: Outside Tiny Temple", map_id=Maps.AngryAztec, region_id=Regions.AngryAztecOasis, obj_id_vanilla=0x80, vanilla_warp=1, swap_index=22, event=Events.AztecW2aTagged
    ),
    Warps.AztecEndOfTunnel: BananaportData(
        name="Angry Aztec: End of the Tunnel", map_id=Maps.AngryAztec, region_id=Regions.AngryAztecMain, obj_id_vanilla=0x7F, vanilla_warp=1, swap_index=23, event=Events.AztecW2bTagged
    ),
    Warps.AztecTotemNearLeft: BananaportData(
        name="Angry Aztec: Near Totem Rocketbarrel", map_id=Maps.AngryAztec, region_id=Regions.AngryAztecMain, obj_id_vanilla=0x98, vanilla_warp=2, swap_index=24, event=Events.AztecW3aTagged
    ),
    Warps.AztecCranky: BananaportData(
        name="Angry Aztec: Outside Cranky's", map_id=Maps.AngryAztec, region_id=Regions.AngryAztecConnectorTunnel, obj_id_vanilla=0x95, vanilla_warp=2, swap_index=25, event=Events.AztecW3bTagged
    ),
    Warps.AztecTotemNearRight: BananaportData(
        name="Angry Aztec: Near Llama Temple", map_id=Maps.AngryAztec, region_id=Regions.AngryAztecMain, obj_id_vanilla=0x73, vanilla_warp=3, swap_index=26, event=Events.AztecW4aTagged
    ),
    Warps.AztecFunky: BananaportData(
        name="Angry Aztec: Outside Funky's", map_id=Maps.AngryAztec, region_id=Regions.AngryAztecMain, obj_id_vanilla=0xB1, vanilla_warp=3, swap_index=27, event=Events.AztecW4bTagged
    ),
    Warps.AztecNearSnide: BananaportData(
        name="Angry Aztec: Near Snide's", map_id=Maps.AngryAztec, region_id=Regions.AngryAztecMain, obj_id_vanilla=0x82, vanilla_warp=4, swap_index=28, event=Events.AztecW5aTagged
    ),
    Warps.AztecSnoopTunnel: BananaportData(
        name="Angry Aztec: Sandy Tunnel",
        map_id=Maps.AngryAztec,
        region_id=Regions.AztecDonkeyQuicksandCave,
        obj_id_vanilla=0x87,
        vanilla_warp=4,
        swap_index=29,
        event=Events.AztecW5bTagged,
        restricted=True,
    ),
    # Llama Temple
    Warps.LlamaNearLeft: BananaportData(
        name="Llama Temple: Near the Bongo Pad", map_id=Maps.AztecLlamaTemple, region_id=Regions.LlamaTemple, obj_id_vanilla=0x58, vanilla_warp=0, swap_index=30, event=Events.LlamaW1aTagged
    ),
    Warps.LlamaMatchingGame: BananaportData(
        name="Llama Temple: Outside Matching Game", map_id=Maps.AztecLlamaTemple, region_id=Regions.LlamaTemple, obj_id_vanilla=0x4E, vanilla_warp=0, swap_index=31, event=Events.LlamaW1bTagged
    ),
    Warps.LlamaNearRight: BananaportData(
        name="Llama Temple: Near the Trombone Pad", map_id=Maps.AztecLlamaTemple, region_id=Regions.LlamaTemple, obj_id_vanilla=0x9A, vanilla_warp=1, swap_index=33, event=Events.LlamaW2aTagged
    ),
    Warps.LlamaLavaRoom: BananaportData(
        name="Llama Temple: In the Lava Room",
        map_id=Maps.AztecLlamaTemple,
        region_id=Regions.LlamaTempleBack,
        obj_id_vanilla=0x99,
        vanilla_warp=1,
        swap_index=32,
        event=Events.LlamaW2bTagged,
        restricted=True,
    ),
    # Factory
    Warps.FactoryNearHatchTunnel: BananaportData(
        name="Frantic Factory: Near Hatch Tunnel", map_id=Maps.FranticFactory, region_id=Regions.FranticFactoryStart, obj_id_vanilla=0x7D, vanilla_warp=0, swap_index=34, event=Events.FactoryW1aTagged
    ),
    Warps.FactoryStorageRoom: BananaportData(
        name="Frantic Factory: Storage Room", map_id=Maps.FranticFactory, region_id=Regions.BeyondHatch, obj_id_vanilla=0x142, vanilla_warp=0, swap_index=35, event=Events.FactoryW1bTagged
    ),
    Warps.FactoryNearBlockTunnel: BananaportData(
        name="Frantic Factory: Near Block Tower Tunnel",
        map_id=Maps.FranticFactory,
        region_id=Regions.FranticFactoryStart,
        obj_id_vanilla=0x141,
        vanilla_warp=1,
        swap_index=36,
        event=Events.FactoryW2aTagged,
    ),
    Warps.FactoryRAndD: BananaportData(
        name="Frantic Factory: R&D", map_id=Maps.FranticFactory, region_id=Regions.RandD, obj_id_vanilla=0x144, vanilla_warp=1, swap_index=37, event=Events.FactoryW2bTagged
    ),
    Warps.FactoryLobbyFar: BananaportData(
        name="Frantic Factory: Lobby Far", map_id=Maps.FranticFactory, region_id=Regions.FranticFactoryStart, obj_id_vanilla=0xD9, vanilla_warp=2, swap_index=38, event=Events.FactoryW3aTagged
    ),
    Warps.FactorySnides: BananaportData(
        name="Frantic Factory: Outside Snide's", map_id=Maps.FranticFactory, region_id=Regions.Testing, obj_id_vanilla=0x143, vanilla_warp=2, swap_index=39, event=Events.FactoryW3bTagged
    ),
    Warps.FactoryProdBottom: BananaportData(
        name="Frantic Factory: Production Room (Bottom)", map_id=Maps.FranticFactory, region_id=Regions.BeyondHatch, obj_id_vanilla=0x105, vanilla_warp=3, swap_index=41, event=Events.FactoryW4aTagged
    ),
    Warps.FactoryProdTop: BananaportData(
        name="Frantic Factory: Production Room (Top)", map_id=Maps.FranticFactory, region_id=Regions.MiddleCore, obj_id_vanilla=0x10C, vanilla_warp=3, swap_index=40, event=Events.FactoryW4bTagged
    ),
    Warps.FactoryArcade: BananaportData(
        name="Frantic Factory: Arcade Room", map_id=Maps.FranticFactory, region_id=Regions.BeyondHatch, obj_id_vanilla=0x10B, vanilla_warp=4, swap_index=43, event=Events.FactoryW5aTagged
    ),
    Warps.FactoryFunky: BananaportData(
        name="Frantic Factory: Outside Funky's", map_id=Maps.FranticFactory, region_id=Regions.Testing, obj_id_vanilla=0xEE, vanilla_warp=4, swap_index=42, event=Events.FactoryW5bTagged
    ),
    # Galleon
    Warps.GalleonNearTunnelIntersection: BananaportData(
        name="Gloomy Galleon: Near Tunnel Intersection",
        map_id=Maps.GloomyGalleon,
        region_id=Regions.GloomyGalleonStart,
        obj_id_vanilla=0x1F7,
        vanilla_warp=0,
        swap_index=45,
        event=Events.GalleonW1aTagged,
    ),
    Warps.GalleonLighthouseRear: BananaportData(
        name="Gloomy Galleon: Lighthouse Rear", map_id=Maps.GloomyGalleon, region_id=Regions.LighthousePlatform, obj_id_vanilla=0x1F6, vanilla_warp=0, swap_index=44, event=Events.GalleonW1bTagged
    ),
    Warps.GalleonNearChestGB: BananaportData(
        name="Gloomy Galleon: Near Chest Room", map_id=Maps.GloomyGalleon, region_id=Regions.GloomyGalleonStart, obj_id_vanilla=0x5F, vanilla_warp=1, swap_index=46, event=Events.GalleonW2aTagged
    ),
    Warps.GalleonNear2DS: BananaportData(
        name="Gloomy Galleon: Near 2-Door Ship", map_id=Maps.GloomyGalleon, region_id=Regions.Shipyard, obj_id_vanilla=0x6C, locked=True, vanilla_warp=1, swap_index=47, event=Events.GalleonW2bTagged
    ),
    Warps.GalleonNearCranky: BananaportData(
        name="Gloomy Galleon: Near Cranky's", map_id=Maps.GloomyGalleon, region_id=Regions.GalleonPastVines, obj_id_vanilla=0x60, vanilla_warp=2, swap_index=48, event=Events.GalleonW3aTagged
    ),
    Warps.GalleonSnides: BananaportData(
        name="Gloomy Galleon: Outside Snide's", map_id=Maps.GloomyGalleon, region_id=Regions.LighthouseSnideAlcove, obj_id_vanilla=0x66, vanilla_warp=2, swap_index=49, event=Events.GalleonW3bTagged
    ),
    Warps.GalleonGoldTower: BananaportData(
        name="Gloomy Galleon: On a Gold Tower",
        map_id=Maps.GloomyGalleon,
        region_id=Regions.TreasureRoomDiddyGoldTower,
        obj_id_vanilla=0x55,
        vanilla_warp=3,
        swap_index=50,
        event=Events.GalleonW4aTagged,
        restricted=True,
    ),
    Warps.GalleonNearSeal: BananaportData(
        name="Gloomy Galleon: Near Seal Race", map_id=Maps.GloomyGalleon, region_id=Regions.Shipyard, obj_id_vanilla=0x56, locked=True, vanilla_warp=3, swap_index=51, event=Events.GalleonW4bTagged
    ),
    Warps.GalleonNearRocketbarrel: BananaportData(
        name="Gloomy Galleon: Near Lighthouse Rocketbarrel",
        map_id=Maps.GloomyGalleon,
        region_id=Regions.LighthousePlatform,
        obj_id_vanilla=0x16,
        vanilla_warp=4,
        swap_index=53,
        event=Events.GalleonW5aTagged,
    ),
    Warps.GalleonNearFunky: BananaportData(
        name="Gloomy Galleon: Near Funky's", map_id=Maps.GloomyGalleon, region_id=Regions.Shipyard, obj_id_vanilla=0x15, locked=True, vanilla_warp=4, swap_index=52, event=Events.GalleonW5bTagged
    ),
    # Fungi
    Warps.FungiClock1: BananaportData(
        name="Fungi Forest: Clock (1)", map_id=Maps.FungiForest, region_id=Regions.FungiForestStart, obj_id_vanilla=0x36, vanilla_warp=0, swap_index=54, event=Events.ForestW1aTagged
    ),
    Warps.FungiMill: BananaportData(name="Fungi Forest: Mill", map_id=Maps.FungiForest, region_id=Regions.MillArea, obj_id_vanilla=0x35, vanilla_warp=0, swap_index=55, event=Events.ForestW1bTagged),
    Warps.FungiClock2: BananaportData(
        name="Fungi Forest: Clock (2)", map_id=Maps.FungiForest, region_id=Regions.FungiForestStart, obj_id_vanilla=0x49, vanilla_warp=1, swap_index=56, event=Events.ForestW2aTagged
    ),
    Warps.FungiFunky: BananaportData(
        name="Fungi Forest: Outside Funky's", map_id=Maps.FungiForest, region_id=Regions.WormArea, obj_id_vanilla=0x4A, vanilla_warp=1, swap_index=57, event=Events.ForestW2bTagged
    ),
    Warps.FungiClock3: BananaportData(
        name="Fungi Forest: Clock (3)", map_id=Maps.FungiForest, region_id=Regions.FungiForestStart, obj_id_vanilla=0x4B, vanilla_warp=2, swap_index=58, event=Events.ForestW3aTagged
    ),
    Warps.FungiMushEntrance: BananaportData(
        name="Fungi Forest: Giant Mushroom Lowest Entrance",
        map_id=Maps.FungiForest,
        region_id=Regions.GiantMushroomArea,
        obj_id_vanilla=0x4E,
        vanilla_warp=2,
        swap_index=59,
        event=Events.ForestW3bTagged,
    ),
    Warps.FungiClock4: BananaportData(
        name="Fungi Forest: Clock (4)", map_id=Maps.FungiForest, region_id=Regions.FungiForestStart, obj_id_vanilla=0x4F, vanilla_warp=3, swap_index=60, event=Events.ForestW4aTagged
    ),
    Warps.FungiOwlTree: BananaportData(
        name="Fungi Forest: Owl Tree", map_id=Maps.FungiForest, region_id=Regions.HollowTreeArea, obj_id_vanilla=0x51, vanilla_warp=3, swap_index=61, event=Events.ForestW4bTagged
    ),
    Warps.FungiTopMush: BananaportData(
        name="Fungi Forest: Giant Mushroom (Top)", map_id=Maps.FungiForest, region_id=Regions.MushroomUpperExterior, obj_id_vanilla=0x56, vanilla_warp=4, swap_index=63, event=Events.ForestW5aTagged
    ),
    Warps.FungiLowMush: BananaportData(
        name="Fungi Forest: Giant Mushroom (Bottom)", map_id=Maps.FungiForest, region_id=Regions.GiantMushroomArea, obj_id_vanilla=0x55, vanilla_warp=4, swap_index=62, event=Events.ForestW5bTagged
    ),
    # Caves
    Warps.CavesNearLeft: BananaportData(
        name="Crystal Caves: Near Left", map_id=Maps.CrystalCaves, region_id=Regions.CrystalCavesMain, obj_id_vanilla=0x22, vanilla_warp=0, swap_index=64, event=Events.CavesW1aTagged
    ),
    Warps.CavesNearChunkyShield: BananaportData(
        name="Crystal Caves: Near Chunky Shield", map_id=Maps.CrystalCaves, region_id=Regions.IglooArea, obj_id_vanilla=0x21, vanilla_warp=0, swap_index=65, event=Events.CavesW1bTagged
    ),
    Warps.CavesNearRight: BananaportData(
        name="Crystal Caves: Near Right", map_id=Maps.CrystalCaves, region_id=Regions.CrystalCavesMain, obj_id_vanilla=0x37, vanilla_warp=1, swap_index=66, event=Events.CavesW2aTagged
    ),
    Warps.CavesWaterfall: BananaportData(
        name="Crystal Caves: Near Waterfall", map_id=Maps.CrystalCaves, region_id=Regions.CabinArea, obj_id_vanilla=0x36, vanilla_warp=1, swap_index=67, event=Events.CavesW2bTagged
    ),
    Warps.CavesNearIglooTag: BananaportData(
        name="Crystal Caves: Near Igloo Tag", map_id=Maps.CrystalCaves, region_id=Regions.IglooArea, obj_id_vanilla=0x57, vanilla_warp=2, swap_index=69, event=Events.CavesW3aTagged
    ),
    Warps.CavesBonusRoom: BananaportData(
        name="Crystal Caves: Inside Bonus Room",
        map_id=Maps.CrystalCaves,
        region_id=Regions.CavesBonusCave,
        obj_id_vanilla=0x56,
        locked=True,
        vanilla_warp=2,
        swap_index=68,
        event=Events.CavesW3bTagged,
        restricted=True,
    ),
    Warps.CavesThinPillar: BananaportData(
        name="Crystal Caves: On the Thin Pillar",
        map_id=Maps.CrystalCaves,
        region_id=Regions.CavesBananaportSpire,
        obj_id_vanilla=0x6B,
        vanilla_warp=3,
        swap_index=71,
        event=Events.CavesW4aTagged,
        restricted=True,
    ),
    Warps.CavesBlueprintRoom: BananaportData(
        name="Crystal Caves: Inside Blueprint Room",
        map_id=Maps.CrystalCaves,
        region_id=Regions.CavesBlueprintCave,
        obj_id_vanilla=0x6A,
        locked=True,
        vanilla_warp=3,
        swap_index=70,
        event=Events.CavesW4bTagged,
        restricted=True,
    ),
    Warps.CavesThickPillar: BananaportData(
        name="Crystal Caves: On the Thick Pillar",
        map_id=Maps.CrystalCaves,
        region_id=Regions.CavesBlueprintPillar,
        obj_id_vanilla=0xB5,
        locked=True,
        vanilla_warp=4,
        swap_index=72,
        event=Events.CavesW5aTagged,
        restricted=True,
    ),
    Warps.CavesCabins: BananaportData(
        name="Crystal Caves: On the 5-Door Cabin", map_id=Maps.CrystalCaves, region_id=Regions.CabinArea, obj_id_vanilla=0x60, vanilla_warp=4, swap_index=73, event=Events.CavesW5bTagged
    ),
    # Castle
    Warps.CastleCenter1: BananaportData(
        name="Creepy Castle: Center (1)", map_id=Maps.CreepyCastle, region_id=Regions.CreepyCastleMain, obj_id_vanilla=0x24, vanilla_warp=0, swap_index=74, event=Events.CastleW1aTagged
    ),
    Warps.CastleRear: BananaportData(
        name="Creepy Castle: Rear", map_id=Maps.CreepyCastle, region_id=Regions.CreepyCastleMain, obj_id_vanilla=0x22, vanilla_warp=0, swap_index=75, event=Events.CastleW1bTagged
    ),
    Warps.CastleCenter2: BananaportData(
        name="Creepy Castle: Center (2)", map_id=Maps.CreepyCastle, region_id=Regions.CreepyCastleMain, obj_id_vanilla=0x2B, vanilla_warp=1, swap_index=77, event=Events.CastleW2aTagged
    ),
    Warps.CastleRocketbarrel: BananaportData(
        name="Creepy Castle: Rocketbarrel", map_id=Maps.CreepyCastle, region_id=Regions.CreepyCastleMain, obj_id_vanilla=0x28, vanilla_warp=1, swap_index=76, event=Events.CastleW2bTagged
    ),
    Warps.CastleCenter3: BananaportData(
        name="Creepy Castle: Center (3)", map_id=Maps.CreepyCastle, region_id=Regions.CreepyCastleMain, obj_id_vanilla=0x2C, vanilla_warp=2, swap_index=78, event=Events.CastleW3aTagged
    ),
    Warps.CastleCranky: BananaportData(
        name="Creepy Castle: Outside Cranky's", map_id=Maps.CreepyCastle, region_id=Regions.CreepyCastleMain, obj_id_vanilla=0x23, vanilla_warp=2, swap_index=79, event=Events.CastleW3bTagged
    ),
    Warps.CastleCenter4: BananaportData(
        name="Creepy Castle: Center (4)", map_id=Maps.CreepyCastle, region_id=Regions.CreepyCastleMain, obj_id_vanilla=0x21, vanilla_warp=3, swap_index=80, event=Events.CastleW4aTagged
    ),
    Warps.CastleTrashCan: BananaportData(
        name="Creepy Castle: Outside Trash Can", map_id=Maps.CreepyCastle, region_id=Regions.CreepyCastleMain, obj_id_vanilla=0x29, vanilla_warp=3, swap_index=81, event=Events.CastleW4bTagged
    ),
    Warps.CastleCenter5: BananaportData(
        name="Creepy Castle: Center (5)", map_id=Maps.CreepyCastle, region_id=Regions.CreepyCastleMain, obj_id_vanilla=0x2D, vanilla_warp=4, swap_index=83, event=Events.CastleW5aTagged
    ),
    Warps.CastleTop: BananaportData(
        name="Creepy Castle: Top", map_id=Maps.CreepyCastle, region_id=Regions.CreepyCastleMain, obj_id_vanilla=0x2A, vanilla_warp=4, swap_index=82, event=Events.CastleW5bTagged
    ),
    # Crypt
    Warps.CryptNearLeft: BananaportData(name="Crypt: Near Left", map_id=Maps.CastleCrypt, region_id=Regions.Crypt, obj_id_vanilla=0x18, vanilla_warp=0, swap_index=84, event=Events.CryptW1aTagged),
    Warps.CryptFarLeft: BananaportData(name="Crypt: Far Left", map_id=Maps.CastleCrypt, region_id=Regions.Crypt, obj_id_vanilla=0x1D, vanilla_warp=0, swap_index=85, event=Events.CryptW1bTagged),
    Warps.CryptNearCenter: BananaportData(name="Crypt: Near Center", map_id=Maps.CastleCrypt, region_id=Regions.Crypt, obj_id_vanilla=0x19, vanilla_warp=1, swap_index=86, event=Events.CryptW2aTagged),
    Warps.CryptFarCenter: BananaportData(
        name="Crypt: Outside Minecart", map_id=Maps.CastleCrypt, region_id=Regions.Crypt, obj_id_vanilla=0x1C, vanilla_warp=1, swap_index=87, event=Events.CryptW2bTagged
    ),
    Warps.CryptNearRight: BananaportData(name="Crypt: Near Right", map_id=Maps.CastleCrypt, region_id=Regions.Crypt, obj_id_vanilla=0x1A, vanilla_warp=2, swap_index=88, event=Events.CryptW3aTagged),
    Warps.CryptFarRight: BananaportData(name="Crypt: Far Right", map_id=Maps.CastleCrypt, region_id=Regions.Crypt, obj_id_vanilla=0x1B, vanilla_warp=2, swap_index=89, event=Events.CryptW3bTagged),
    # Isles
    Warps.IslesRing1: BananaportData(name="DK Isles: Ring (1)", map_id=Maps.Isles, region_id=Regions.IslesMain, obj_id_vanilla=0x10, vanilla_warp=0, swap_index=0, event=Events.IslesW1aTagged),
    Warps.IslesKLumsy: BananaportData(
        name="DK Isles: Outside K. Lumsy's Prison", map_id=Maps.Isles, region_id=Regions.IslesMain, obj_id_vanilla=0x11, vanilla_warp=0, swap_index=1, event=Events.IslesW1bTagged
    ),
    Warps.IslesRing2: BananaportData(name="DK Isles: Ring (2)", map_id=Maps.Isles, region_id=Regions.IslesMain, obj_id_vanilla=0x12, vanilla_warp=1, swap_index=2, event=Events.IslesW2aTagged),
    Warps.IslesAztecLobby: BananaportData(
        name="DK Isles: Outside Aztec Lobby", map_id=Maps.Isles, region_id=Regions.IslesMainUpper, obj_id_vanilla=0x13, vanilla_warp=1, swap_index=3, event=Events.IslesW2bTagged
    ),
    Warps.IslesRing3: BananaportData(name="DK Isles: Ring (3)", map_id=Maps.Isles, region_id=Regions.IslesMain, obj_id_vanilla=0x16, vanilla_warp=2, swap_index=5, event=Events.IslesW3aTagged),
    Warps.IslesWaterfall: BananaportData(name="DK Isles: Waterfall", map_id=Maps.Isles, region_id=Regions.IslesMain, obj_id_vanilla=0x14, vanilla_warp=2, swap_index=4, event=Events.IslesW3bTagged),
    Warps.IslesRing4: BananaportData(name="DK Isles: Ring (4)", map_id=Maps.Isles, region_id=Regions.IslesMain, obj_id_vanilla=0x17, vanilla_warp=3, swap_index=6, event=Events.IslesW4aTagged),
    Warps.IslesFactoryLobby: BananaportData(
        name="DK Isles: Outside Factory Lobby", map_id=Maps.Isles, region_id=Regions.KremIsleBeyondLift, obj_id_vanilla=0x18, vanilla_warp=3, swap_index=7, event=Events.IslesW4bTagged
    ),
    Warps.IslesRing5: BananaportData(name="DK Isles: Ring (5)", map_id=Maps.Isles, region_id=Regions.IslesMain, obj_id_vanilla=0x15, vanilla_warp=4, swap_index=8, event=Events.IslesW5aTagged),
    Warps.IslesFairyIsland: BananaportData(
        name="DK Isles: Fairy Island", map_id=Maps.Isles, region_id=Regions.IslesMain, obj_id_vanilla=0x19, vanilla_warp=4, swap_index=9, event=Events.IslesW5bTagged
    ),
}

VanillaBananaportSelector = []
result = []
for warp in BananaportVanilla.values():
    if warp.map_id not in result:
        # this regex is used to turn 'CamelCaseNames' into 'Camel Case Names' for the purpose of being displayed on the site's selector
        VanillaBananaportSelector.append(
            {"name": " ".join(sub("([A-Z][a-z]+)", r" \1", sub("([A-Z]+)", r" \1", (str(warp.map_id.name).split(".")[-1]).split(".")[-1])).split()), "value": warp.map_id.name, "tooltip": ""}
        )
        result.append(warp.map_id)
