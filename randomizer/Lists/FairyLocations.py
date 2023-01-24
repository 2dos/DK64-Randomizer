"""Stores the data for each potential fairy location."""

from randomizer.Enums.Levels import Levels
from randomizer.Lists.MapsAndExits import Maps
from randomizer.Enums.Regions import Regions
from randomizer.Enums.Events import Events

class Fence:
    """Stores information about a fence."""
    
    def __init__(self, min_x: int, min_z: int, max_x: int, max_z: int):
        """Initialize with given data."""
        self.min_x = min_x
        self.min_z = min_z
        self.max_x = max_x
        self.max_z = max_z
        self.center_x = int((min_x + max_x) / 2)
        self.center_z = int((min_z + max_z) / 2)

class FairyData:
    """Stores information about a fairy location."""

    def __init__(self, *, name: str = "", map: Maps = Maps.Isles, region: Regions = Regions.GameStart, fence: Fence = None, spawn_y: int = 0, logic=None, is_vanilla: bool = False, spawn_xyz: list = None, natural_index: int = -1):
        """Initialize with given data."""
        self.name = name
        self.map = map
        self.region = region
        self.fence = fence
        self.spawn_y = spawn_y
        self.logic = lambda l: l.camera
        if logic is not None:
            self.logic = logic
        self.is_vanilla = is_vanilla
        if is_vanilla:
            self.spawn_xyz = [0, 0, 0]
            if spawn_xyz is not None:
                self.spawn_xyz = spawn_xyz.copy()
        self.natural_index = natural_index


fairy_locations = {
    Levels.JungleJapes: [
        FairyData(
            name="Jungle Japes: Rambi Door Pool", 
            map=Maps.JungleJapes,
            region=Regions.BeyondRambiGate,
            is_vanilla=True,
            spawn_xyz=[564, 270, 2916],
            natural_index=0,
        ),
        FairyData(
            name="Jungle Japes: Painting Room", 
            map=Maps.JapesLankyCave,
            region=Regions.JapesLankyCave,
            is_vanilla=True,
            spawn_xyz=[218, 174, 391],
            logic=lambda l: (((l.grape or l.trombone) and l.Slam) or l.generalclips) and l.islanky and l.camera,
            natural_index=1,
        ),
        FairyData(
            name="Jungle Japes: Near Kong Cage",
            map=Maps.JungleJapes,
            region=Regions.JungleJapesMain,
            fence=Fence(1000, 2345, 1206, 2482),
            spawn_y=1040,
        ),
        FairyData(
            name="Jungle Japes: Near Mountain",
            map=Maps.JungleJapes,
            region=Regions.JungleJapesMain,
            fence=Fence(1300, 1793, 1950, 2162),
            spawn_y=916,
        ),
        FairyData(
            name="Jungle Japes: Above Underground Entrance",
            map=Maps.JungleJapes,
            region=Regions.JungleJapesMain,
            fence=Fence(2223, 1255, 2524, 1322),
            spawn_y=370,
        ),
        FairyData(
            name="Jungle Japes: Hive Area",
            map=Maps.JungleJapes,
            region=Regions.JapesBeyondFeatherGate,
            fence=Fence(1934, 3153, 2607, 3207),
            spawn_y=727,
        ),
        FairyData(
            name="Jungle Japes: Storm Area",
            map=Maps.JungleJapes,
            region=Regions.JapesBeyondCoconutGate2,
            fence=Fence(1450, 3678, 1910, 4280),
            spawn_y=475,
        ),
        FairyData(
            name="Jungle Japes: Inside Hive",
            map=Maps.JapesTinyHive,
            region=Regions.TinyHive,
            fence=Fence(1259, 1204, 1487, 1603),
            spawn_y=236,
        ),
        FairyData(
            name="Jungle Japes: Underground Pathway",
            map=Maps.JapesUnderGround,
            region=Regions.JapesCatacomb,
            fence=Fence(886, 524, 903, 1105),
            spawn_y=64,
        ),
        FairyData(
            name="Jungle Japes: Underground Vine Area",
            map=Maps.JapesUnderGround,
            region=Regions.JapesCatacomb,
            fence=Fence(121, 651, 354, 925),
            spawn_y=53,
        ),
        FairyData(
            name="Jungle Japes: Mine Entry",
            map=Maps.JapesMountain,
            region=Regions.Mine,
            fence=Fence(717, 274, 724, 646),
            spawn_y=125,
        ),
    ],
    Levels.AngryAztec: [
        FairyData(
            name="Angry Aztec: Tiny 5-Door Temple",
            map=Maps.AztecTiny5DTemple,
            region=Regions.TinyTemple,
            is_vanilla=True,
            spawn_xyz=[1178, 95, 704],
            logic=lambda l: l.camera and ((l.feather and l.mini and l.istiny) or l.phasewalk),
            natural_index=1,
        ),
        FairyData(
            name="Angry Aztec: Llama Temple",
            map=Maps.AztecLlamaTemple,
            region=Regions.LlamaTemple,
            is_vanilla=True,
            spawn_xyz=[1646, 500, 3091],
            natural_index=0,
        ),
        FairyData(
            name="Angry Aztec: Vase Room",
            map=Maps.AngryAztec,
            region=Regions.BetweenVinesByPortal,
            fence=Fence(127, 626, 463, 902),
            spawn_y=151,
            logic=lambda l: l.camera and ((l.pineapple and l.chunky) or l.phasewalk),
        ),
        FairyData(
            name="Angry Aztec: Oasis",
            map=Maps.AngryAztec,
            region=Regions.AngryAztecOasis,
            fence=Fence(2206, 691, 2773, 1124),
            spawn_y=218,
        ),
        FairyData(
            name="Angry Aztec: Behind Tiny Temple",
            map=Maps.AngryAztec,
            region=Regions.AngryAztecOasis,
            fence=Fence(3190, 424, 3503, 688),
            spawn_y=363,
        ),
        FairyData(
            name="Angry Aztec: Near Snake Road",
            map=Maps.AngryAztec,
            region=Regions.AngryAztecConnectorTunnel,
            fence=Fence(3129, 1724, 3365, 1958),
            spawn_y=136,
        ),
        FairyData(
            name="Angry Aztec: Bonus Cage",
            map=Maps.AngryAztec,
            region=Regions.AngryAztecConnectorTunnel,
            fence=Fence(4027, 2277, 4358, 2551),
            spawn_y=138,
        ),
        FairyData(
            name="Angry Aztec: Around Totem",
            map=Maps.AngryAztec,
            region=Regions.AngryAztecMain,
            fence=Fence(2965, 3650, 3513, 4063),
            spawn_y=324,
        ),
        FairyData(
            name="Angry Aztec: Gong Tower",
            map=Maps.AngryAztec,
            region=Regions.AngryAztecMain,
            fence=Fence(4183, 3144, 4561, 3241),
            spawn_y=422,
        ),
        FairyData(
            name="Angry Aztec: Donkey 5DT",
            map=Maps.AztecDonkey5DTemple,
            region=Regions.DonkeyTemple,
            fence=Fence(699, 259, 755, 870),
            spawn_y=67,
            logic=lambda l: l.camera and ((l.coconut and l.isdonkey) or l.phasewalk),
        ),
        FairyData(
            name="Angry Aztec: Chunky 5DT",
            map=Maps.AztecChunky5DTemple,
            region=Regions.ChunkyTemple,
            fence=Fence(600, 601, 678, 1222),
            spawn_y=94,
            logic=lambda l: l.camera and ((l.pineapple and l.ischunky) or l.phasewalk),
        ),
        FairyData(
            name="Angry Aztec: Diddy 5DT",
            map=Maps.AztecDiddy5DTemple,
            region=Regions.DiddyTemple,
            fence=Fence(707, 236, 782, 363),
            spawn_y=47,
        ),
        FairyData(
            name="Angry Aztec: Lanky 5DT",
            map=Maps.AztecLanky5DTemple,
            region=Regions.LankyTemple,
            fence=Fence(426, 621, 496, 1209),
            spawn_y=94,
            logic=lambda l: l.camera and ((l.grape and l.islanky) or l.phasewalk),
        ),
        FairyData(
            name="Angry Aztec: Start of Llama Temple",
            map=Maps.AztecLlamaTemple,
            region=Regions.LlamaTemple,
            fence=Fence(2051, 2121, 2400, 2673),
            spawn_y=569,
        ),
        FairyData(
            name="Angry Aztec: Matching Room",
            map=Maps.AztecLlamaTemple,
            region=Regions.LlamaTemple,
            fence=Fence(952, 2101, 1153, 2667),
            spawn_y=769,
            logic=lambda l: l.camera and ((l.grape and l.islanky) or l.phasewalk or l.CanOStandTBSNoclip()),
        ),
        FairyData(
            name="Angry Aztec: Tiny Temple Start",
            map=Maps.AztecTinyTemple,
            region=Regions.TempleStart,
            fence=Fence(1195, 647, 1766, 1069),
            spawn_y=378,
        ),
        FairyData(
            name="Angry Aztec: Tiny Temple Kong Cage Room",
            map=Maps.AztecTinyTemple,
            region=Regions.TempleUnderwater,
            fence=Fence(280, 1288, 721, 1614),
            spawn_y=442,
        ),
    ],
    Levels.FranticFactory: [
        FairyData(
            name="Frantic Factory: Number Game",
            map=Maps.FranticFactory,
            region=Regions.Testing,
            is_vanilla=True,
            spawn_xyz=[2967, 1094, 1646],
            natural_index=1,
        ),
        FairyData(
            name="Frantic Factory: Near Funky's",
            map=Maps.FranticFactory,
            region=Regions.Testing,
            is_vanilla=True,
            spawn_xyz=[1535, 1231, 518],
            logic=lambda l: l.camera and Events.DartsPlayed in l.Events,
            natural_index=0,
        ),
    ],
    Levels.GloomyGalleon: [
        FairyData(
            name="Gloomy Galleon: In a chest",
            map=Maps.GloomyGalleon,
            region=Regions.GloomyGalleonStart,
            is_vanilla=True,
            spawn_xyz=[3547, 1795, 3703],
            logic=lambda l: l.camera and l.punch and l.chunky,
            natural_index=0,
        ),
        FairyData(
            name="Gloomy Galleon: In Tiny's 5-Door Ship",
            map=Maps.Galleon5DShipDKTiny,
            region=Regions.SaxophoneShip,
            is_vanilla=True,
            spawn_xyz=[1089, 62, 2022],
            natural_index=1,
        ),
    ],
    Levels.FungiForest: [
        FairyData(
            name="Fungi Forest: DK's Barn",
            map=Maps.ForestThornvineBarn,
            region=Regions.ThornvineBarn,
            is_vanilla=True,
            spawn_xyz=[497, 162, 502],
            logic=lambda l: l.Slam and l.camera,
            natural_index=1,
        ),
        FairyData(
            name="Fungi Forest: Dark Attic",
            map=Maps.ForestRafters,
            region=Regions.MillRafters,
            is_vanilla=True,
            spawn_xyz=[355, 50, 342],
            logic=lambda l: l.guitar and l.isdiddy and l.camera,
            natural_index=0,
        ),
    ],
    Levels.CrystalCaves: [
        FairyData(
            name="Crystal Caves: Diddy Candles Cabin",
            map=Maps.CavesDiddyUpperCabin,
            region=Regions.DiddyUpperCabin,
            is_vanilla=True,
            spawn_xyz=[140, 100, 505],
            logic=lambda l: l.camera and (l.guitar or l.oranges) and l.spring and l.jetpack and l.isdiddy,
            natural_index=1,
        ),
        FairyData(
            name="Crystal Caves: Tiny Igloo",
            map=Maps.CavesTinyIgloo,
            region=Regions.TinyIgloo,
            is_vanilla=True,
            spawn_xyz=[309, 90, 438],
            logic=lambda l: l.Slam and (l.istiny or l.settings.free_trade_items) and l.camera,
            natural_index=0,
        ),
    ],
    Levels.CreepyCastle: [
        FairyData(
            name="Creepy Castle: Tree Sniper Room",
            map=Maps.CastleTree,
            region=Regions.CastleTree,
            is_vanilla=True,
            spawn_xyz=[1696, 400, 1054],
            logic=lambda l: l.camera and (((l.coconut or l.generalclips) and l.isdonkey) or l.phasewalk),
            natural_index=1,
        ),
        FairyData(
            name="Creepy Castle: Near Car Race",
            map=Maps.CastleMuseum,
            region=Regions.MuseumBehindGlass,
            is_vanilla=True,
            spawn_xyz=[277, 247, 1598],
            natural_index=0,
        ),
    ],
    Levels.DKIsles: [
        FairyData(
            name="DK Isles: Small Island",
            map=Maps.Isles,
            region=Regions.IslesMain,
            is_vanilla=True,
            spawn_xyz=[1057, 634, 1456],
            natural_index=2,
        ),
        FairyData(
            name="DK Isles: Upper Krem Isles",
            map=Maps.Isles,
            region=Regions.KremIsleTopLevel,
            is_vanilla=True,
            spawn_xyz=[2358, 1798, 3884],
            natural_index=3,
        ),
        FairyData(
            name="DK Isles: Factory Lobby",
            map=Maps.FranticFactoryLobby,
            region=Regions.FranticFactoryLobby,
            is_vanilla=True,
            spawn_xyz=[245, 81, 150],
            logic=lambda l: l.camera and l.punch and l.chunky,
            natural_index=0,
        ),
        FairyData(
            name="DK Isles: Fungi Lobby",
            map=Maps.FungiForestLobby,
            region=Regions.FungiForestLobby,
            is_vanilla=True,
            spawn_xyz=[472, 163, 612],
            logic=lambda l: l.camera and l.feather and l.tiny,
            natural_index=1,
        ),
    ],
    Levels.HideoutHelm: [
        FairyData(
            name="Hideout Helm: Key 8 Room (1)",
            map=Maps.HideoutHelm,
            region=Regions.HideoutHelmAfterBoM,
            is_vanilla=True,
            spawn_xyz=[164, 118, 5213],
            logic=lambda l: l.camera and Events.HelmKeyAccess in l.Events,
            natural_index=0,
        ),
        FairyData(
            name="Hideout Helm: Key 8 Room (2)",
            map=Maps.HideoutHelm,
            region=Regions.HideoutHelmAfterBoM,
            is_vanilla=True,
            spawn_xyz=[135, 98, 5224],
            logic=lambda l: l.camera and Events.HelmKeyAccess in l.Events,
            natural_index=1,
        ),
    ],
}