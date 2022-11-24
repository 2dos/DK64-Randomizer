"""Crown Location List."""
from randomizer.Lists.MapsAndExits import Maps
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Regions import Regions
from randomizer.Enums.Events import Events


class CrownLocation:
    """Class to store information pertaining to a crown location."""

    def __init__(self, *, map=0, name="", x=0, y=0, z=0, scale=1, region=0, logic=None, is_vanilla=False, is_rotating_room=False, default_index=0):
        """Initialize with given data."""
        self.map = map
        self.name = name
        self.coords = [x, y, z]
        self.scale = scale
        self.logic = logic
        self.region = region
        self.is_vanilla = is_vanilla
        self.is_rotating_room = is_rotating_room
        self.default_index = default_index
        self.placement_subindex = default_index
        if logic is None:
            self.logic = lambda l: True
        else:
            self.logic = logic


CrownLocations = {
    Levels.JungleJapes: [
        CrownLocation(map=Maps.JungleJapes, name="Jungle Japes: Near Funky", x=1989.7, y=520, z=2086.71, scale=0.45, region=Regions.JungleJapesMain, is_vanilla=True),
        CrownLocation(map=Maps.JungleJapes, name="Jungle Japes: On Tree (Starting Area)", x=1101, y=478, z=266, scale=0.25, region=Regions.JungleJapesMain),
        CrownLocation(map=Maps.JungleJapes, name="Jungle Japes: Diddy Cavern", x=2381, y=280, z=392, scale=0.35, region=Regions.JapesBeyondPeanutGate),
        CrownLocation(map=Maps.JungleJapes, name="Jungle Japes: Painting Hill", x=554, y=370, z=1804, scale=0.35, region=Regions.JungleJapesMain, logic=lambda l: l.handstand and l.lanky),
        CrownLocation(map=Maps.JungleJapes, name="Jungle Japes: Shellhive Island", x=2337, y=551, z=3156, scale=0.6, region=Regions.JapesBeyondFeatherGate),
        CrownLocation(map=Maps.JungleJapes, name="Jungle Japes: Near Stump", x=1912, y=539, z=3289, scale=0.45, region=Regions.JapesBeyondFeatherGate),
        CrownLocation(map=Maps.JungleJapes, name="Jungle Japes: Near Log", x=2419, y=539, z=2834, scale=0.45, region=Regions.JapesBeyondFeatherGate),
        CrownLocation(map=Maps.JungleJapes, name="Jungle Japes: Vine Pit", x=1150, y=230, z=2613, scale=0.45, region=Regions.JapesBeyondCoconutGate2),
        CrownLocation(map=Maps.JungleJapes, name="Jungle Japes: Lanky Alcove Hill", x=2209, y=339, z=3205, scale=0.4, region=Regions.JapesBeyondCoconutGate2, logic=lambda l: l.handstand and l.lanky),
        CrownLocation(map=Maps.JungleJapes, name="Jungle Japes: Fairy Pool", x=597, y=240, z=3123, scale=0.4, region=Regions.BeyondRambiGate),
        CrownLocation(map=Maps.JungleJapes, name="Jungle Japes: Behind Lanky Hut", x=2052, y=280, z=4350, scale=0.35, region=Regions.JapesBeyondCoconutGate2),
        CrownLocation(map=Maps.JungleJapes, name="Jungle Japes: Behind DK Hut", x=1307, y=280, z=4327, scale=0.35, region=Regions.JapesBeyondCoconutGate2),
        # CrownLocation(map=Maps.JungleJapes, name="Jungle Japes: On Cranky's Lab", x=1696, y=360, z=4002, scale=0.25, region=0,), # Doesn't work with shop rando
        CrownLocation(map=Maps.JungleJapes, name="Jungle Japes: Behind Storm Area Shop", x=1705, y=280, z=4233, scale=0.45, region=Regions.JapesBeyondCoconutGate2),
        CrownLocation(map=Maps.JungleJapes, name="Jungle Japes: Minecart Alcove", x=1106, y=288, z=1967, scale=0.3, region=Regions.JungleJapesMain),
        CrownLocation(map=Maps.JungleJapes, name="Jungle Japes: Near High Shop", x=2045, y=680, z=2522, scale=0.35, region=Regions.JungleJapesMain),
        CrownLocation(map=Maps.JungleJapes, name="Jungle Japes: On Mountain", x=1616, y=989, z=2439, scale=0.5, region=Regions.JapesTopOfMountain),
        CrownLocation(map=Maps.JungleJapes, name="Jungle Japes: Near Kong Cage", x=949, y=852, z=2384, scale=0.35, region=Regions.JungleJapesMain),
        CrownLocation(map=Maps.JungleJapes, name="Jungle Japes: Near Cannon Platform", x=1282, y=520, z=2262, scale=0.35, region=Regions.JungleJapesMain),
        CrownLocation(map=Maps.JungleJapes, name="Jungle Japes: In T&S Alcove", x=770, y=538, z=2332, scale=0.35, region=Regions.JungleJapesMain, logic=lambda l: l.vines),
        # CrownLocation(
        #     map=Maps.JungleJapes,
        #     name="Jungle Japes: Near Underground Entrance",
        #     x=2446,
        #     y=280,
        #     z=1143,
        #     scale=0.4,
        #     region=Regions.JungleJapesMain,
        # ),
        CrownLocation(map=Maps.JungleJapes, name="Jungle Japes: Lower River", x=2381, y=280, z=1685, scale=0.45, region=Regions.JungleJapesMain),
        CrownLocation(map=Maps.JungleJapes, name="Jungle Japes: Starting Area (Low)", x=742, y=286, z=825, scale=0.35, region=Regions.JungleJapesMain),
        CrownLocation(map=Maps.JapesUnderGround, name="Jungle Japes - Underground: Behind Cannon", x=433, y=20, z=104, scale=0.25, region=Regions.JapesCatacomb),
        CrownLocation(map=Maps.JapesUnderGround, name="Jungle Japes - Underground: Near Vines", x=453, y=20, z=814, scale=0.35, region=Regions.JapesCatacomb),
        CrownLocation(map=Maps.JapesLankyCave, name="Jungle Japes - Painting Room: Near Peg", x=100, y=80, z=346, scale=0.3, region=Regions.JapesLankyCave),
        CrownLocation(map=Maps.JapesMountain, name="Jungle Japes - Mountain: Near Entrance (Ground)", x=328, y=40, z=471, scale=0.3, region=Regions.Mine),
        CrownLocation(map=Maps.JapesMountain, name="Jungle Japes - Mountain: Near Entrance (High)", x=497, y=140, z=512, scale=0.35, region=Regions.Mine),
        CrownLocation(map=Maps.JapesMountain, name="Jungle Japes - Mountain: On Barrel", x=690, y=135, z=757, scale=0.4, region=Regions.Mine),
        CrownLocation(map=Maps.JapesMountain, name="Jungle Japes - Mountain: Near HiLo Machine", x=326, y=133, z=1510, scale=0.2, region=Regions.Mine, logic=lambda l: l.charge and l.diddy),
        CrownLocation(map=Maps.JapesMountain, name="Jungle Japes - Mountain: Under Conveyor", x=42, y=220, z=1056, scale=0.3, region=Regions.Mine, logic=lambda l: l.Slam and l.diddy),
        CrownLocation(map=Maps.JapesTinyHive, name="Jungle Japes - Shell: Main Room", x=1385, y=212, z=1381, scale=0.7, region=Regions.TinyHive),
        CrownLocation(map=Maps.JapesTinyHive, name="Jungle Japes - Shell: 1st Room", x=610, y=130, z=1279, scale=0.6, region=Regions.TinyHive),
        CrownLocation(map=Maps.JapesTinyHive, name="Jungle Japes - Shell: 3rd Room", x=2547, y=254, z=1354, scale=0.6, region=Regions.TinyHive, logic=lambda l: l.Slam and l.tiny),
    ],
    Levels.AngryAztec: [
        CrownLocation(
            map=Maps.AztecTinyTemple,
            name="Angry Aztec - Tiny Temple: Vulture Room",
            x=1466.42,
            y=305.33,
            z=2340.39,
            scale=0.41,
            region=Regions.TempleUnderwater,
            is_vanilla=True,
            logic=lambda l: l.Slam and l.grape and l.islanky,
        ),
        CrownLocation(map=Maps.AztecTinyTemple, name="Angry Aztec - Tiny Temple: Starting Room (Low)", x=1802, y=283, z=611, scale=0.5, region=Regions.TempleStart),
        CrownLocation(
            map=Maps.AztecTinyTemple, name="Angry Aztec - Tiny Temple: Starting Room (High)", x=1370, y=490, z=1126, scale=0.3, region=Regions.TempleStart, logic=lambda l: l.Slam and l.diddy
        ),
        CrownLocation(map=Maps.AztecTinyTemple, name="Angry Aztec - Tiny Temple: Kong Free Room", x=524, y=344, z=1468, scale=0.5, region=Regions.TempleUnderwater),
        CrownLocation(
            map=Maps.AngryAztec,
            name="Angry Aztec: Blueprint Room",
            x=1224,
            y=120,
            z=740,
            scale=0.25,
            region=Regions.AngryAztecOasis,
            logic=lambda l: l.coconut and ((l.strongKong and l.isdonkey) or l.settings.damage_amount == "default"),
        ),
        CrownLocation(map=Maps.AngryAztec, name="Angry Aztec: Oasis", x=2151, y=120, z=983, scale=0.35, region=Regions.AngryAztecOasis),
        CrownLocation(map=Maps.AngryAztec, name="Angry Aztec: Behind Tiny Temple", x=3345, y=153, z=507, scale=0.3, region=Regions.AngryAztecOasis),
        CrownLocation(map=Maps.AngryAztec, name="Angry Aztec: On Tiny Temple", x=3192, y=352, z=500, scale=0.3, region=Regions.AngryAztecOasis, logic=lambda l: l.jetpack and l.diddy),
        CrownLocation(map=Maps.AngryAztec, name="Angry Aztec: Near Oasis Shop", x=2430, y=120, z=509, scale=0.35, region=Regions.CandyAztec),
        CrownLocation(map=Maps.AngryAztec, name="Angry Aztec: Near Hunky Chunky Barrel", x=3216, y=120, z=1490, scale=0.35, region=Regions.AngryAztecMain),
        CrownLocation(map=Maps.AngryAztec, name="Angry Aztec: Next to Chunky Cage (1)", x=4276.6, y=120, z=2266, scale=0.4, region=Regions.AngryAztecMain),
        CrownLocation(map=Maps.AngryAztec, name="Angry Aztec: Next to Chunky Cage (2)", x=4283, y=120, z=2543.6, scale=0.4, region=Regions.AngryAztecMain),
        CrownLocation(map=Maps.AngryAztec, name="Angry Aztec: Near Llama Temple (Left)", x=2781, y=160, z=3264, scale=0.35, region=Regions.AngryAztecMain),
        CrownLocation(map=Maps.AngryAztec, name="Angry Aztec: Near Llama Temple (Right)", x=3154, y=160, z=3172, scale=0.35, region=Regions.AngryAztecMain),
        CrownLocation(map=Maps.AngryAztec, name="Angry Aztec: On Llama Temple", x=2884, y=437, z=2903, scale=0.4, region=Regions.AngryAztecMain, logic=lambda l: l.jetpack and l.diddy),
        CrownLocation(map=Maps.AngryAztec, name="Angry Aztec: Near Snoop Tunnel Shop", x=3000, y=120, z=4532, scale=0.35, region=Regions.AngryAztecMain),
        CrownLocation(map=Maps.AngryAztec, name="Angry Aztec: On 5-Door Temple", x=2056, y=420, z=3648, scale=0.3, region=Regions.AngryAztecMain, logic=lambda l: l.jetpack and l.diddy),
        CrownLocation(map=Maps.AngryAztec, name="Angry Aztec: Near Snoop Tunnel Exterior Warp", x=3422, y=120, z=4514, scale=0.35, region=Regions.AngryAztecMain),
        CrownLocation(map=Maps.AngryAztec, name="Angry Aztec: Near Vulture Cage", x=4013, y=226, z=4589, scale=0.18, region=Regions.AngryAztecMain, logic=lambda l: l.vines),
        CrownLocation(map=Maps.AngryAztec, name="Angry Aztec: Under Vulture Cage", x=4102, y=120, z=4548, scale=0.4, region=Regions.AngryAztecMain),
        CrownLocation(map=Maps.AngryAztec, name="Angry Aztec: Near Gong Tower", x=4212, y=80, z=2959, scale=0.4, region=Regions.AngryAztecMain),
        CrownLocation(map=Maps.AngryAztec, name="Angry Aztec: Snoop Tunnel", x=2783, y=120, z=4817, scale=0.35, region=Regions.AztecDonkeyQuicksandCave),
        CrownLocation(map=Maps.AztecDonkey5DTemple, name="Angry Aztec - DK 5DT: Dead End", x=99, y=20, z=464, scale=0.4, region=Regions.DonkeyTemple, logic=lambda l: l.coconut and l.isdonkey),
        CrownLocation(map=Maps.AztecDiddy5DTemple, name="Angry Aztec - Diddy 5DT: Dead End", x=1060, y=20, z=493, scale=0.4, region=Regions.DiddyTemple, logic=lambda l: l.peanut and l.isdiddy),
        CrownLocation(map=Maps.AztecLanky5DTemple, name="Angry Aztec - Lanky 5DT: Dead End", x=767, y=122, z=916, scale=0.3, region=Regions.LankyTemple, logic=lambda l: l.grape and l.islanky),
        CrownLocation(
            map=Maps.AztecLanky5DTemple, name="Angry Aztec - Lanky 5DT: Near Vanilla Balloon", x=180, y=47, z=658, scale=0.45, region=Regions.LankyTemple, logic=lambda l: l.grape and l.islanky
        ),
        CrownLocation(map=Maps.AztecTiny5DTemple, name="Angry Aztec - Tiny 5DT: Dead End", x=329, y=123, z=1420, scale=0.3, region=Regions.TinyTemple, logic=lambda l: l.feather and l.istiny),
        CrownLocation(
            map=Maps.AztecChunky5DTemple, name="Angry Aztec - Chunky 5DT: Path Split (1)", x=375, y=20, z=321, scale=0.45, region=Regions.ChunkyTemple, logic=lambda l: l.pineapple and l.ischunky
        ),
        CrownLocation(
            map=Maps.AztecChunky5DTemple, name="Angry Aztec - Chunky 5DT: Path Split (2)", x=779, y=47, z=678, scale=0.45, region=Regions.ChunkyTemple, logic=lambda l: l.pineapple and l.ischunky
        ),
        CrownLocation(map=Maps.AztecLlamaTemple, name="Angry Aztec - Llama Temple: Llama Right", x=1737, y=472, z=2548, scale=0.45, region=Regions.LlamaTemple),
        CrownLocation(map=Maps.AztecLlamaTemple, name="Angry Aztec - Llama Temple: Llama Left", x=1737, y=472, z=2200, scale=0.45, region=Regions.LlamaTemple),
        CrownLocation(map=Maps.AztecLlamaTemple, name="Angry Aztec - Llama Temple: Matching Room", x=1082, y=641, z=2186, scale=0.45, region=Regions.LlamaTemple, logic=lambda l: l.grape and l.lanky),
        CrownLocation(map=Maps.AztecLlamaTemple, name="Angry Aztec - Llama Temple: Snoop Switch", x=1695, y=433, z=1704, scale=0.3, region=Regions.LlamaTemple),
        CrownLocation(map=Maps.AztecLlamaTemple, name="Angry Aztec - Llama Temple: Lava Room", x=1227, y=420, z=3572, scale=0.35, region=Regions.LlamaTempleBack),
    ],
    Levels.FranticFactory: [
        CrownLocation(
            map=Maps.FranticFactory, name="Frantic Factory: Under R&D Grate (1)", x=4119, y=1313, z=1165.81, scale=0.51, region=Regions.RandD, logic=lambda l: l.grab and l.donkey, is_vanilla=True
        ),
        CrownLocation(map=Maps.FranticFactory, name="Frantic Factory: Foyer Carpet", x=1265, y=830, z=2504, scale=0.6, region=Regions.FranticFactoryStart),
        CrownLocation(map=Maps.FranticFactory, name="Frantic Factory: Foyer far left", x=1106, y=842, z=2106, scale=0.4, region=Regions.FranticFactoryStart),
        CrownLocation(map=Maps.FranticFactory, name="Frantic Factory: Near Hatch", x=519, y=804, z=1958, scale=0.35, region=Regions.FranticFactoryStart),
        CrownLocation(map=Maps.FranticFactory, name="Frantic Factory: Hatch Pole Center", x=644, y=459, z=1778, scale=0.45, region=Regions.BeyondHatch),
        CrownLocation(map=Maps.FranticFactory, name="Frantic Factory: Hatch Pole Bottom", x=654, y=167, z=1988, scale=0.4, region=Regions.BeyondHatch),
        CrownLocation(map=Maps.FranticFactory, name="Frantic Factory: Production Room Lower Section", x=517, y=188, z=1331, scale=0.3, region=Regions.BeyondHatch),
        CrownLocation(map=Maps.FranticFactory, name="Frantic Factory: Under High Conveyors", x=783, y=677, z=970, scale=0.25, region=Regions.UpperCore),
        CrownLocation(map=Maps.FranticFactory, name="Frantic Factory: Past Tiny Production Bonus", x=400, y=858.5, z=1615, scale=0.2, region=Regions.UpperCore, logic=lambda l: l.twirl and l.tiny),
        CrownLocation(map=Maps.FranticFactory, name="Frantic Factory: On Production outside box", x=988, y=322, z=1175, scale=0.25, region=Regions.UpperCore),
        CrownLocation(map=Maps.FranticFactory, name="Frantic Factory: Storage Room Corner", x=974, y=66.5, z=908, scale=0.2, region=Regions.BeyondHatch),
        CrownLocation(map=Maps.FranticFactory, name="Frantic Factory: Cranky/Candy Room", x=316, y=165, z=805, scale=0.4, region=Regions.BeyondHatch),
        CrownLocation(map=Maps.FranticFactory, name="Frantic Factory: Dark Room", x=1850, y=6, z=525, scale=0.45, region=Regions.BeyondHatch, logic=lambda l: l.punch and l.chunky),
        CrownLocation(map=Maps.FranticFactory, name="Frantic Factory: Arcade Room Bench", x=1922, y=1143, z=1515, scale=0.25, region=Regions.BeyondHatch),
        CrownLocation(map=Maps.FranticFactory, name="Frantic Factory: Snide's Room", x=1702, y=810, z=2240, scale=0.3, region=Regions.Testing),
        CrownLocation(map=Maps.FranticFactory, name="Frantic Factory: Right Corridor", x=1710, y=837, z=2328, scale=0.3, region=Regions.Testing),
        CrownLocation(map=Maps.FranticFactory, name="Frantic Factory: Number Game", x=2666, y=1002, z=1952, scale=0.3, region=Regions.Testing),
        CrownLocation(map=Maps.FranticFactory, name="Frantic Factory: Under Block Tower Stairs", x=2014, y=1027, z=1348, scale=0.45, region=Regions.Testing),
        CrownLocation(map=Maps.FranticFactory, name="Frantic Factory: Block Tower Lower Bonus", x=2634, y=1026, z=1101, scale=0.5, region=Regions.Testing),
        CrownLocation(map=Maps.FranticFactory, name="Frantic Factory: Funky's Room", x=1595, y=1113, z=760, scale=0.4, region=Regions.Testing),
        CrownLocation(map=Maps.FranticFactory, name="Frantic Factory: Near Funky's", x=1370, y=1131, z=551, scale=0.3, region=Regions.Testing),
        # CrownLocation(
        #     map=Maps.FranticFactory,
        #     name="Frantic Factory: Piano Room",
        #     x=3382,
        #     y=1264,
        #     z=641,
        #     scale=0.35,
        #     region=Regions.RandD,
        #     logic=lambda l: l.trombone and l.lanky,
        # ),
        # CrownLocation(
        #     map=Maps.FranticFactory,
        #     name="Frantic Factory: Diddy R&D",
        #     x=4450,
        #     y=1336,
        #     z=735,
        #     scale=0.45,
        #     region=Regions.RandD,
        #     logic=lambda l: l.guitar and l.diddy,
        # ),
        # CrownLocation(
        #     map=Maps.FranticFactory,
        #     name="Frantic Factory: Chunky R&D", # Entering a crown battle during the Toy Boss fight would break the fight until level re-entry
        #     x=4574,
        #     y=1336,
        #     z=1350,
        #     scale=0.4,
        #     region=Regions.RandD,
        #     logic=lambda l: l.triangle and l.chunky and l.punch,
        # ),
        CrownLocation(map=Maps.FranticFactory, name="Frantic Factory: Near Car Race", x=3553, y=1264, z=1383, scale=0.3, region=Regions.RandD, logic=lambda l: l.mini and l.istiny),
        CrownLocation(map=Maps.FranticFactory, name="Frantic Factory: Under R&D Grate (2)", x=4054, y=1313, z=776, scale=0.5, region=Regions.RandD, logic=lambda l: l.grab and l.donkey),
        CrownLocation(
            map=Maps.FactoryCrusher, name="Frantic Factory - Crusher: Central Safehaven", x=116, y=0.5, z=468, scale=0.45, region=Regions.InsideCore, logic=lambda l: l.strongKong and l.isdonkey
        ),
        CrownLocation(map=Maps.FactoryPowerHut, name="Frantic Factory - Power Shed: Corner", x=62, y=0, z=64, scale=0.3, region=Regions.PowerHut),
    ],
    Levels.GloomyGalleon: [
        CrownLocation(
            map=Maps.GloomyGalleon,
            name="Gloomy Galleon: Under Cranky",
            x=3296.94,
            y=1670,
            z=2450.29,
            scale=0.53,
            region=Regions.GloomyGalleonStart,
            logic=lambda l: l.punch and l.chunky,
            is_vanilla=True,
        ),
        CrownLocation(map=Maps.GloomyGalleon, name="Gloomy Galleon: Near Chest Cannon (1)", x=3072, y=1790, z=3501, scale=0.3, region=Regions.GloomyGalleonStart),
        CrownLocation(map=Maps.GloomyGalleon, name="Gloomy Galleon: Near Chest Cannon (2)", x=3072, y=1790, z=3360, scale=0.45, region=Regions.GloomyGalleonStart),
        CrownLocation(map=Maps.GloomyGalleon, name="Gloomy Galleon: Near Chest GB Tunnel", x=3048, y=1670, z=3832, scale=0.4, region=Regions.GloomyGalleonStart),
        CrownLocation(map=Maps.GloomyGalleon, name="Gloomy Galleon: Near Chest GB", x=3506, y=1670, z=3802, scale=0.55, region=Regions.GloomyGalleonStart),
        CrownLocation(map=Maps.GloomyGalleon, name="Gloomy Galleon: Left of Cranky", x=3175, y=1670, z=2527, scale=0.35, region=Regions.GloomyGalleonStart),
        # CrownLocation(
        #     map=Maps.GloomyGalleon,
        #     name="Gloomy Galleon: Front of Cranky",
        #     x=3314,
        #     y=1790,
        #     z=2474,
        #     scale=0.4,
        #     region=Regions.GloomyGalleonStart,
        # ),
        # CrownLocation(map=Maps.GloomyGalleon, name="Gloomy Galleon: On Cranky", x=3290, y=1870, z=2372, scale=0.2, region=0,),
        CrownLocation(map=Maps.GloomyGalleon, name="Gloomy Galleon: Near Bridge Warp 3", x=3116, y=1890, z=2896, scale=0.25, region=Regions.GalleonPastVines),
        CrownLocation(map=Maps.GloomyGalleon, name="Gloomy Galleon: On Lighthouse Platform (Rocketbarrel)", x=1396, y=1610, z=4150, scale=0.35, region=Regions.LighthousePlatform),
        CrownLocation(map=Maps.GloomyGalleon, name="Gloomy Galleon: On Lighthouse Platform (Baboon Blast)", x=1618, y=1610, z=4175, scale=0.35, region=Regions.LighthousePlatform),
        CrownLocation(map=Maps.GloomyGalleon, name="Gloomy Galleon: On Rocketbarrel platform", x=1336, y=1660, z=4071, scale=0.2, region=Regions.LighthousePlatform),
        CrownLocation(map=Maps.GloomyGalleon, name="Gloomy Galleon: Blueprint Alcove", x=680, y=1564, z=3940, scale=0.55, region=Regions.LighthouseSurface),
        CrownLocation(map=Maps.GloomyGalleon, name="Gloomy Galleon: Behind Snide's", x=2071, y=1610, z=4823, scale=0.3, region=Regions.LighthouseSnideAlcove),
        CrownLocation(map=Maps.GloomyGalleon, name="Gloomy Galleon: On Gold Tower", x=1660, y=2040, z=487, scale=0.25, region=Regions.TreasureRoomDiddyGoldTower),
        CrownLocation(map=Maps.GalleonSickBay, name="Gloomy Galleon - Seasick Ship: Left of Cannon", x=718, y=20, z=129, scale=0.35, region=Regions.SickBay),
        CrownLocation(map=Maps.GalleonSickBay, name="Gloomy Galleon - Seasick Ship: Right of Cannon", x=544, y=20, z=129, scale=0.35, region=Regions.SickBay),
        # CrownLocation(
        #     map=Maps.GalleonSickBay,
        #     name="Gloomy Galleon - Seasick Ship: In Corner",
        #     x=703,
        #     y=20,
        #     z=911,
        #     scale=0.4,
        #     region=Regions.SickBay,
        # ),
        CrownLocation(
            map=Maps.GalleonSickBay, name="Gloomy Galleon - Seasick Ship: Behind Spinning Barrels", x=142, y=20, z=851, scale=0.4, region=Regions.SickBay, logic=lambda l: l.punch and l.ischunky
        ),
        CrownLocation(map=Maps.GalleonLighthouse, name="Gloomy Galleon - Lighthouse: Bottom Left", x=703, y=0, z=469, scale=0.5, region=Regions.Lighthouse),
        CrownLocation(map=Maps.GalleonLighthouse, name="Gloomy Galleon - Lighthouse: Back Right", x=282, y=0, z=670, scale=0.5, region=Regions.Lighthouse),
    ],
    Levels.FungiForest: [
        CrownLocation(
            map=Maps.FungiForest,
            name="Fungi Forest: Giant Mushroom High Ladder Platform",
            x=1254.33,
            y=1079.33,
            z=1307.16,
            scale=0.49,
            region=Regions.MushroomUpperExterior,
            logic=lambda l: Events.Night in l.Events,
            is_vanilla=True,
        ),
        CrownLocation(map=Maps.FungiForest, name="Fungi Forest: Near Well", x=2399, y=110, z=3186, scale=0.6, region=Regions.FungiForestStart),
        CrownLocation(map=Maps.FungiForest, name="Fungi Forest: Behind Clock", x=2300, y=603, z=2322, scale=0.35, region=Regions.FungiForestStart),
        CrownLocation(map=Maps.FungiForest, name="Fungi Forest: In front of Clock", x=2591, y=603, z=2237, scale=0.4, region=Regions.FungiForestStart),
        CrownLocation(map=Maps.FungiForest, name="Fungi Forest: Near Blue Tunnel", x=3210, y=167, z=2613, scale=0.35, region=Regions.FungiForestStart),
        CrownLocation(map=Maps.FungiForest, name="Fungi Forest: Near Snide's HQ", x=3154, y=268, z=3682, scale=0.35, region=Regions.Snide),
        CrownLocation(map=Maps.FungiForest, name="Fungi Forest: Behind Diddy Barn", x=3139, y=272, z=4343, scale=0.4, region=Regions.MillArea),
        CrownLocation(map=Maps.FungiForest, name="Fungi Forest: Left of Diddy Barn", x=3400, y=272, z=4652, scale=0.4, region=Regions.MillArea),
        CrownLocation(map=Maps.FungiForest, name="Fungi Forest: Near Mill Tag", x=4706, y=139, z=4373, scale=0.4, region=Regions.MillArea),
        CrownLocation(map=Maps.FungiForest, name="Fungi Forest: Near Well Exit", x=5279, y=207, z=3556, scale=0.45, region=Regions.MillArea),
        CrownLocation(map=Maps.FungiForest, name="Fungi Forest: Near Winch", x=4533, y=162, z=3372, scale=0.45, region=Regions.MillArea),
        CrownLocation(map=Maps.FungiForest, name="Fungi Forest: Near Mill Punch Door", x=4439, y=162, z=3853, scale=0.45, region=Regions.MillArea),
        CrownLocation(map=Maps.FungiForest, name="Fungi Forest: En route to DK Barn", x=4604, y=206, z=2844, scale=0.4, region=Regions.ThornvineArea),
        CrownLocation(map=Maps.FungiForest, name="Fungi Forest: Right of DK Barn", x=4492, y=116, z=1959, scale=0.5, region=Regions.ThornvineArea),
        CrownLocation(map=Maps.FungiForest, name="Fungi Forest: Far Right of DK Barn", x=4147, y=115, z=1496, scale=0.4, region=Regions.ThornvineArea),
        CrownLocation(map=Maps.FungiForest, name="Fungi Forest: Behind DK Barn", x=3486, y=115, z=1427, scale=0.35, region=Regions.ThornvineArea),
        CrownLocation(map=Maps.FungiForest, name="Fungi Forest: Far Left of DK Barn", x=3529, y=115, z=2035, scale=0.5, region=Regions.ThornvineArea),
        CrownLocation(map=Maps.FungiForest, name="Fungi Forest: Near DK Barn", x=4151, y=115, z=1784, scale=0.4, region=Regions.ThornvineArea),
        # CrownLocation(map=Maps.FungiForest, name="Fungi Forest: Behind Beanstalk Night Gate", x=3621, y=186, z=936, scale=0.3, region=0,),
        CrownLocation(map=Maps.FungiForest, name="Fungi Forest: Near Funky's", x=2890, y=174, z=189, scale=0.4, region=Regions.WormArea),
        CrownLocation(map=Maps.FungiForest, name="Fungi Forest: Near Beanstalk Area Entrance", x=2721, y=200, z=982, scale=0.4, region=Regions.WormArea),
        CrownLocation(map=Maps.FungiForest, name="Fungi Forest: Near Beanstalk", x=1991, y=231, z=829, scale=0.45, region=Regions.WormArea),
        CrownLocation(map=Maps.FungiForest, name="Fungi Forest: Near Beanstalk Mini Monkey", x=1902, y=227, z=369, scale=0.45, region=Regions.WormArea),
        CrownLocation(map=Maps.FungiForest, name="Fungi Forest: Near Giant Mushroom", x=1642, y=234, z=867, scale=0.4, region=Regions.GiantMushroomArea),
        CrownLocation(map=Maps.FungiForest, name="Fungi Forest: Near Yellow Tunnel", x=236, y=179, z=1307, scale=0.6, region=Regions.GiantMushroomArea),
        CrownLocation(map=Maps.FungiForest, name="Fungi Forest: Near Cranky", x=583, y=182, z=272, scale=0.45, region=Regions.GiantMushroomArea),
        CrownLocation(map=Maps.FungiForest, name="Fungi Forest: Near Lower Baboon Blast Ladder", x=567, y=389, z=731, scale=0.4, region=Regions.MushroomLowerExterior),
        # CrownLocation(
        #     map=Maps.FungiForest,
        #     name="Fungi Forest: Behind Upper Baboon Blast Ladder",
        #     x=751,
        #     y=589,
        #     z=1297,
        #     scale=0.4,
        #     region=Regions.MushroomLowerExterior,
        # ),
        CrownLocation(map=Maps.FungiForest, name="Fungi Forest: Above Upper Baboon Blast Ladder", x=671, y=779, z=1320, scale=0.35, region=Regions.MushroomLowerExterior),
        CrownLocation(map=Maps.FungiForest, name="Fungi Forest: Highest Giant Mushroom Platform", x=1196, y=1250, z=1315, scale=0.4, region=Regions.MushroomUpperExterior),
        CrownLocation(map=Maps.FungiForest, name="Fungi Forest: Behind Rabbit", x=2408, y=142, z=3705, scale=0.5, region=Regions.HollowTreeArea),
        CrownLocation(map=Maps.FungiForest, name="Fungi Forest: Under Owl Tree", x=1274, y=249, z=3750, scale=0.45, region=Regions.HollowTreeArea),
        CrownLocation(map=Maps.FungiForest, name="Fungi Forest: Near Owl Rocketbarrel (1)", x=534, y=189, z=3948, scale=0.45, region=Regions.HollowTreeArea),
        CrownLocation(map=Maps.FungiForest, name="Fungi Forest: Near Owl Rocketbarrel (2)", x=278, y=190, z=3707, scale=0.6, region=Regions.HollowTreeArea),
        CrownLocation(map=Maps.FungiForest, name="Fungi Forest: On Mill", x=4164, y=376, z=3526, scale=0.4, region=Regions.MillArea),
        CrownLocation(map=Maps.ForestAnthill, name="Fungi Forest - Anthill: Orange Platform", x=768, y=205, z=421, scale=0.35, region=Regions.Anthill),
        CrownLocation(map=Maps.ForestWinchRoom, name="Fungi Forest - Winch Room: Opposite Entrance", x=310, y=0, z=342, scale=0.4, region=Regions.WinchRoom),
        CrownLocation(map=Maps.ForestThornvineBarn, name="Fungi Forest - DK Barn: Near Entrance", x=537, y=4, z=143, scale=0.45, region=Regions.ThornvineBarn),
        CrownLocation(map=Maps.ForestThornvineBarn, name="Fungi Forest - DK Barn: Near Ladder", x=106, y=4, z=590, scale=0.4, region=Regions.ThornvineBarn),
        CrownLocation(map=Maps.ForestMillFront, name="Fungi Forest - Mill Front: Near Conveyor", x=63, y=0, z=400, scale=0.3, region=Regions.MillChunkyArea),
        CrownLocation(map=Maps.ForestMillFront, name="Fungi Forest - Mill Front: Near Mini Monkey", x=256, y=0, z=196, scale=0.5, region=Regions.MillChunkyArea),
        CrownLocation(map=Maps.ForestGiantMushroom, name="Fungi Forest - Giant Mushroom: Near Tiny Bonus", x=550, y=409, z=200, scale=0.45, region=Regions.MushroomLower),
        CrownLocation(map=Maps.ForestGiantMushroom, name="Fungi Forest - Giant Mushroom: Near Gun Switches", x=448, y=82, z=195, scale=0.4, region=Regions.MushroomLower),
        CrownLocation(map=Maps.ForestGiantMushroom, name="Fungi Forest - Giant Mushroom: Near Bottom Cannon", x=596, y=0, z=680, scale=0.45, region=Regions.MushroomLower),
        CrownLocation(map=Maps.ForestGiantMushroom, name="Fungi Forest - Giant Mushroom: Near Night Door Vines", x=218, y=979, z=529, scale=0.4, region=Regions.MushroomUpper),
        CrownLocation(map=Maps.ForestGiantMushroom, name="Fungi Forest - Giant Mushroom: On Top Viney Platform", x=543, y=1169, z=700, scale=0.5, region=Regions.MushroomUpper),
        CrownLocation(map=Maps.ForestMillAttic, name="Fungi Forest - Mill Attic: Near Box", x=138, y=0, z=310, scale=0.4, region=Regions.MillAttic),
        CrownLocation(map=Maps.ForestLankyZingersRoom, name="Fungi Forest - Mushroom Leap: Opposite Entrance", x=414, y=0, z=282, scale=0.4, region=Regions.MushroomLankyZingersRoom),
        CrownLocation(map=Maps.ForestLankyMushroomsRoom, name="Fungi Forest - Mushroom Slam: Opposite Entrance", x=408, y=0, z=309, scale=0.4, region=Regions.MushroomLankyMushroomsRoom),
        CrownLocation(map=Maps.ForestChunkyFaceRoom, name="Fungi Forest - Face Puzzle: Near Puzzle", x=229, y=0, z=441, scale=0.4, region=Regions.MushroomChunkyRoom),
        CrownLocation(map=Maps.ForestMillBack, name="Fungi Forest - Mill Rear: Near Thatch", x=449, y=0, z=610, scale=0.5, region=Regions.MillTinyArea),
        CrownLocation(map=Maps.ForestSpider, name="Fungi Forest - Spider: Opposite Entrance", x=917, y=172, z=599, scale=0.45, region=Regions.SpiderRoom),
    ],
    Levels.CrystalCaves: [
        CrownLocation(
            map=Maps.CrystalCaves,
            name="Crystal Caves: In Tiny Ice Shield",
            x=311,
            y=48,
            z=1719,
            scale=0.2,
            region=Regions.CrystalCavesMain,
            logic=lambda l: l.monkeyport and l.mini and l.twirl and l.tiny,
        ),
        CrownLocation(
            map=Maps.CrystalCaves, name="Crystal Caves: In Chunky Ice Shield", x=755, y=48, z=818, scale=0.2, region=Regions.IglooArea, logic=lambda l: Events.CavesLargeBoulderButton in l.Events
        ),
        CrownLocation(
            map=Maps.CrystalCaves,
            name="Crystal Caves: On 5DI Pillar",
            x=328,
            y=132.5,
            z=1522,
            scale=0.15,
            region=Regions.IglooArea,
            logic=lambda l: (l.jetpack and l.isdiddy) or (l.twirl and l.istiny),
        ),
        CrownLocation(map=Maps.CrystalCaves, name="Crystal Caves: In Hidden Bonus Room", x=453, y=180, z=2571, scale=0.4, region=Regions.CavesBonusCave),
        CrownLocation(map=Maps.CrystalCaves, name="Crystal Caves: In Giant Boulder Room", x=1941, y=280, z=2338, scale=0.5, region=Regions.BoulderCave),
        CrownLocation(map=Maps.CrystalCaves, name="Crystal Caves: In front of Cranky", x=1202, y=281, z=1649, scale=0.25, region=Regions.CrystalCavesMain),
        CrownLocation(map=Maps.CrystalCaves, name="Crystal Caves: Near Ice Castle Tag (1)", x=2066, y=151, z=1145, scale=0.25, region=Regions.CrystalCavesMain),
        CrownLocation(map=Maps.CrystalCaves, name="Crystal Caves: Near Ice Castle Tag (2)", x=1952, y=172, z=1181, scale=0.25, region=Regions.CrystalCavesMain),
        CrownLocation(map=Maps.CrystalCaves, name="Crystal Caves: Near Ice Castle Tag (3)", x=2164, y=280, z=1304, scale=0.3, region=Regions.CrystalCavesMain),
        CrownLocation(
            map=Maps.CrystalCaves,
            name="Crystal Caves: On Ice Castle",
            x=2176,
            y=343.5,
            z=1002,
            scale=0.2,
            region=Regions.CrystalCavesMain,
            logic=lambda l: (l.balloon and l.islanky) or (l.jetpack and l.isdiddy),
        ),
        CrownLocation(map=Maps.CrystalCaves, name="Crystal Caves: Near Small Boulder", x=1598, y=276, z=970, scale=0.35, region=Regions.CrystalCavesMain),
        CrownLocation(map=Maps.CrystalCaves, name="Crystal Caves: Near Snide's HQ", x=1220, y=64, z=587, scale=0.4, region=Regions.CavesSnideArea),
        CrownLocation(map=Maps.CrystalCaves, name="Crystal Caves: Under Small Boulder", x=1412, y=90, z=1013, scale=0.4, region=Regions.CrystalCavesMain),
        # CrownLocation(map=Maps.CrystalCaves, name="Crystal Caves: Near Entrance (OoB)", x=1718, y=-29, z=30, scale=0.4, region=0,),
        CrownLocation(map=Maps.CrystalCaves, name="Crystal Caves: Near Gorilla Gone Room", x=2149, y=13, z=152, scale=0.4, region=Regions.CrystalCavesMain),
        CrownLocation(map=Maps.CrystalCaves, name="Crystal Caves: In Gorilla Gone Room", x=2650, y=13, z=469, scale=0.4, region=Regions.CrystalCavesMain, logic=lambda l: l.punch and l.chunky),
        CrownLocation(map=Maps.CrystalCaves, name="Crystal Caves: Near Kasplat Spire", x=2700, y=152, z=772, scale=0.4, region=Regions.CrystalCavesMain),
        CrownLocation(map=Maps.CrystalCaves, name="Crystal Caves: Near Funky's", x=2543, y=172, z=1173, scale=0.25, region=Regions.CrystalCavesMain),
        CrownLocation(map=Maps.CrystalCaves, name="Crystal Caves: Hidden Kasplat Room", x=3554, y=286, z=619, scale=0.4, region=Regions.CavesBlueprintCave),
        CrownLocation(map=Maps.CrystalCaves, name="Crystal Caves: Near 1DC Headphones", x=2987, y=118, z=1615, scale=0.4, region=Regions.CabinArea),
        # CrownLocation(map=Maps.CrystalCaves, name="Crystal Caves: Near Ice Tag (Mid-Air)", x=2238, y=394, z=1169, scale=0.25, region=0,),
        # CrownLocation(
        #     map=Maps.CrystalCaves,
        #     name="Crystal Caves: Near 1DC",
        #     x=2412,
        #     y=277,
        #     z=1960,
        #     scale=0.4,
        #     region=Regions.CabinArea,
        # ),
        CrownLocation(map=Maps.CrystalCaves, name="Crystal Caves: Near Rotating Room (1)", x=2903.5, y=281.8, z=2312, scale=0.35, region=Regions.CabinArea),
        CrownLocation(map=Maps.CrystalCaves, name="Crystal Caves: Near Rotating Room (2)", x=2672, y=281, z=2500, scale=0.35, region=Regions.CabinArea),
        CrownLocation(map=Maps.CrystalCaves, name="Crystal Caves: High Cabin Kasplat Platform", x=2984, y=373, z=1848, scale=0.4, region=Regions.CabinArea),
        CrownLocation(map=Maps.CrystalCaves, name="Crystal Caves: Near Rotating Room Rocketbarrel", x=2465, y=206.8, z=2530, scale=0.25, region=Regions.CabinArea),
        CrownLocation(map=Maps.CrystalCaves, name="Crystal Caves: Near Tiny 5DC", x=3551, y=260, z=1900, scale=0.3, region=Regions.CabinArea),
        CrownLocation(map=Maps.CrystalCaves, name="Crystal Caves: Near Diddy Upper 5DC", x=3684, y=343, z=1886, scale=0.25, region=Regions.CabinArea),
        CrownLocation(
            map=Maps.CavesRotatingCabin,
            name="Crystal Caves - Rotating Room: Left Portion",
            x=329,
            y=0,
            z=193,
            scale=0.35,
            region=Regions.RotatingCabin,
            logic=lambda l: l.Slam and l.isdonkey,
            is_vanilla=True,
            is_rotating_room=True,
        ),
        CrownLocation(map=Maps.CavesDiddyIgloo, name="Crystal Caves - Diddy 5DI: Center", x=286, y=0, z=295, scale=0.4, region=Regions.DiddyIgloo),
        CrownLocation(map=Maps.CavesDonkeyIgloo, name="Crystal Caves - DK 5DI: Behind Maze", x=469, y=0, z=177, scale=0.5, region=Regions.DonkeyIgloo),
        CrownLocation(map=Maps.CavesLankyIgloo, name="Crystal Caves - Lanky 5DI: High Platform", x=273, y=123.3, z=245, scale=0.25, region=Regions.LankyIgloo, logic=lambda l: l.balloon and l.islanky),
        CrownLocation(map=Maps.CavesTinyIgloo, name="Crystal Caves - Tiny 5DI: Opposite Entrance", x=385, y=0, z=200, scale=0.4, region=Regions.TinyIgloo),
        CrownLocation(map=Maps.CavesLankyCabin, name="Crystal Caves - Lanky 1DC: Carpet", x=448, y=0, z=332, scale=0.45, region=Regions.LankyCabin),
        CrownLocation(map=Maps.CavesChunkyCabin, name="Crystal Caves - Chunky 5DC: Back Left Corner", x=493, y=0, z=536, scale=0.35, region=Regions.ChunkyCabin),
        CrownLocation(map=Maps.CavesDiddyUpperCabin, name="Crystal Caves - Diddy Upper 5DC: Right", x=106, y=0, z=353, scale=0.45, region=Regions.DiddyUpperCabin),
        CrownLocation(map=Maps.CavesDonkeyCabin, name="Crystal Caves - DK 5DC: Opposite Entrance", x=165, y=0, z=463, scale=0.35, region=Regions.DonkeyCabin),
        CrownLocation(map=Maps.CavesTinyCabin, name="Crystal Caves - Tiny Cabin: Interior", x=179, y=0, z=255, scale=0.35, region=Regions.TinyCabin),
    ],
    Levels.CreepyCastle: [
        CrownLocation(map=Maps.CastleGreenhouse, name="Creepy Castle - Greenhouse: Center", x=503.276, y=0, z=581.451, scale=0.33, region=Regions.Greenhouse, is_vanilla=True),
        CrownLocation(map=Maps.CastleGreenhouse, name="Creepy Castle - Greenhouse: Dead End (1)", x=224, y=0, z=494, scale=0.2, region=Regions.Greenhouse),
        CrownLocation(map=Maps.CastleGreenhouse, name="Creepy Castle - Greenhouse: Dead End (2)", x=874, y=0, z=522, scale=0.2, region=Regions.Greenhouse),
        CrownLocation(map=Maps.CastleGreenhouse, name="Creepy Castle - Greenhouse: GB Box", x=349, y=0, z=302, scale=0.35, region=Regions.Greenhouse),
        CrownLocation(map=Maps.CastleGreenhouse, name="Creepy Castle - Greenhouse: Dead End (3)", x=779, y=0, z=125, scale=0.2, region=Regions.Greenhouse),
        CrownLocation(map=Maps.CreepyCastle, name="Creepy Castle: Near Tree", x=1201, y=471.5, z=105, scale=0.5, region=Regions.CreepyCastleMain),
        CrownLocation(map=Maps.CreepyCastle, name="Creepy Castle: Near Crypt Entrance (1)", x=1361, y=366, z=2108, scale=0.4, region=Regions.CreepyCastleMain),
        CrownLocation(map=Maps.CreepyCastle, name="Creepy Castle: Near Crypt Entrance (2)", x=420, y=366, z=1934, scale=0.4, region=Regions.CreepyCastleMain),
        CrownLocation(map=Maps.CreepyCastle, name="Creepy Castle: Near Crypt Entrance (3)", x=500, y=523, z=1660, scale=0.4, region=Regions.CreepyCastleMain),
        CrownLocation(map=Maps.CreepyCastle, name="Creepy Castle: Near Dungeon Tunnel Steps", x=1298, y=523, z=1777, scale=0.4, region=Regions.CreepyCastleMain),
        CrownLocation(map=Maps.CreepyCastle, name="Creepy Castle: Near Dungeon Tunnel", x=902, y=648, z=1620, scale=0.4, region=Regions.CreepyCastleMain),
        CrownLocation(map=Maps.CreepyCastle, name="Creepy Castle: Near Kasplat Pole", x=204, y=628, z=1433, scale=0.45, region=Regions.CreepyCastleMain),
        # CrownLocation(
        #     map=Maps.CreepyCastle,
        #     name="Creepy Castle: Near Drawbridge Entrance",
        #     x=664,
        #     y=548.8,
        #     z=532,
        #     scale=0.5,
        #     region=Regions.CreepyCastleMain,
        # ),
        CrownLocation(map=Maps.CreepyCastle, name="Creepy Castle: Near Lower Rocketbarrel", x=176, y=622, z=578, scale=0.35, region=Regions.CreepyCastleMain),
        CrownLocation(map=Maps.CreepyCastle, name="Creepy Castle: Near Lower Tag Barrel", x=1623, y=673, z=655, scale=0.35, region=Regions.CreepyCastleMain),
        CrownLocation(map=Maps.CreepyCastle, name="Creepy Castle: Near Headphones", x=1778, y=676, z=921, scale=0.3, region=Regions.CreepyCastleMain),
        CrownLocation(map=Maps.CreepyCastle, name="Creepy Castle: Near Drawbridge Exit", x=763, y=673, z=1016, scale=0.4, region=Regions.CreepyCastleMain),
        CrownLocation(map=Maps.CreepyCastle, name="Creepy Castle: Near Cranky", x=483, y=1135, z=1379, scale=0.4, region=Regions.CreepyCastleMain),
        CrownLocation(map=Maps.CreepyCastle, name="Creepy Castle: Near Shed", x=1688, y=1391, z=1802, scale=0.35, region=Regions.CreepyCastleMain),
        CrownLocation(map=Maps.CreepyCastle, name="Creepy Castle: Near Wind Tower (1)", x=1707, y=1731, z=1255, scale=0.4, region=Regions.CreepyCastleMain),
        # CrownLocation(
        #     map=Maps.CreepyCastle,
        #     name="Creepy Castle: Near Wind Tower (2)",
        #     x=1707,
        #     y=1731,
        #     z=1375,
        #     scale=0.4,
        #     region=Regions.CreepyCastleMain,
        # ),
        CrownLocation(map=Maps.CreepyCastle, name="Creepy Castle: Near Snide's HQ", x=713, y=1794, z=1243, scale=0.4, region=Regions.CreepyCastleMain),
        CrownLocation(map=Maps.CreepyCastle, name="Creepy Castle: On Wind Tower", x=1560, y=2023, z=1322, scale=0.5, region=Regions.CreepyCastleMain, logic=lambda l: l.jetpack and l.isdiddy),
        CrownLocation(map=Maps.CastleBallroom, name="Creepy Castle - Ballroom: Near Left Candle", x=410, y=40, z=221, scale=0.55, region=Regions.Ballroom),
        CrownLocation(map=Maps.CastleBallroom, name="Creepy Castle - Ballroom: Near Right Candle", x=847, y=40, z=454, scale=0.55, region=Regions.Ballroom),
        # CrownLocation(map=Maps.CastleDungeon, name="Creepy Castle - Dungeon: Diddy Room (OoB)", x=403, y=90, z=3307, scale=0.45, region=0,),
        CrownLocation(map=Maps.CastleDungeon, name="Creepy Castle - Dungeon: Near Diddy Room Entrance", x=442, y=115, z=2595, scale=0.4, region=Regions.Dungeon),
        CrownLocation(map=Maps.CastleDungeon, name="Creepy Castle - Dungeon: DK Dungeon Room", x=1492, y=170, z=2000, scale=0.5, region=Regions.Dungeon, logic=lambda l: l.superDuperSlam and l.donkey),
        CrownLocation(map=Maps.CastleShed, name="Creepy Castle - Shed: Near Entrance", x=179, y=0, z=219, scale=0.4, region=Regions.Shed),
        CrownLocation(map=Maps.CastleLowerCave, name="Creepy Castle - Crypt Hub: Lower Portion", x=559, y=90, z=1153, scale=0.4, region=Regions.LowerCave),
        CrownLocation(map=Maps.CastleLowerCave, name="Creepy Castle - Crypt Hub: Behind Lanky Crypt", x=1848, y=320, z=1186, scale=0.4, region=Regions.LowerCave),
        CrownLocation(map=Maps.CastleLowerCave, name="Creepy Castle - Crypt Hub: Near Funky's", x=1359, y=200, z=433, scale=0.4, region=Regions.LowerCave),
        CrownLocation(map=Maps.CastleCrypt, name="Creepy Castle - Chunky Crypt: Near Coffin", x=1280, y=160, z=2867, scale=0.45, region=Regions.Crypt, logic=lambda l: l.pineapple and l.ischunky),
        CrownLocation(map=Maps.CastleCrypt, name="Creepy Castle - Diddy Crypt: Near Coffin", x=2069, y=0, z=593, scale=0.45, region=Regions.Crypt, logic=lambda l: l.peanut and l.isdiddy),
        CrownLocation(map=Maps.CastleMausoleum, name="Creepy Castle - Lanky Crypt: Lanky Tunnel", x=1186, y=160, z=130, scale=0.4, region=Regions.Mausoleum),
        CrownLocation(map=Maps.CastleUpperCave, name="Creepy Castle - Tunnel: Near Pit", x=704, y=200, z=852, scale=0.4, region=Regions.UpperCave),
        CrownLocation(map=Maps.CastleUpperCave, name="Creepy Castle - Tunnel: Near Candy's", x=1104, y=300, z=2241, scale=0.4, region=Regions.UpperCave),
        CrownLocation(map=Maps.CastleLibrary, name="Creepy Castle - Library: Enemy Gauntlet Room", x=289, y=190, z=530, scale=0.5, region=Regions.Library),
        CrownLocation(
            map=Maps.CastleLibrary,
            name="Creepy Castle - Library: Flying Book Room",
            x=2772,
            y=180,
            z=500,
            scale=0.4,
            region=Regions.Library,
            logic=lambda l: l.superDuperSlam and l.isdonkey and (l.strongKong or l.settings.damage_amount == "default"),
        ),
        CrownLocation(map=Maps.CastleMuseum, name="Creepy Castle - Museum: Near Race", x=312, y=200, z=1784, scale=0.4, region=Regions.MuseumBehindGlass),
        CrownLocation(
            map=Maps.CastleMuseum, name="Creepy Castle - Museum: Behind Pillar", x=1265, y=200, z=1525, scale=0.4, region=Regions.MuseumBehindGlass, logic=lambda l: l.monkeyport and l.istiny
        ),
        CrownLocation(map=Maps.CastleMuseum, name="Creepy Castle - Museum: Main Room", x=595, y=100, z=440, scale=0.6, region=Regions.Museum),
        CrownLocation(map=Maps.CastleTrashCan, name="Creepy Castle - Trash Can: Near Cheese", x=465, y=15, z=510, scale=0.6, region=Regions.TrashCan),
        CrownLocation(map=Maps.CastleTree, name="Creepy Castle - Tree: Starting Room", x=972, y=400, z=884, scale=0.4, region=Regions.CastleTree),
    ],
    Levels.DKIsles: [
        CrownLocation(
            map=Maps.IslesSnideRoom,
            name="DK Isles - Snide's Room: Under Rock",
            x=361.02,
            y=0,
            z=280.06,
            scale=0.43,
            region=Regions.IslesSnideRoom,
            logic=lambda l: l.chunky and l.barrels,
            is_vanilla=True,
            default_index=1,
        ),
        CrownLocation(
            map=Maps.FungiForestLobby,
            name="DK Isles - Fungi Lobby: Gorilla Gone Box",
            x=290.99,
            y=20,
            z=637.07,
            scale=0.35,
            region=Regions.FungiForestLobby,
            logic=lambda l: l.coconut and l.peanut and l.grape and l.feather and l.pineapple and l.donkey and l.diddy and l.lanky and l.tiny and l.chunky and l.gorillaGone,
            is_vanilla=True,
        ),
        CrownLocation(map=Maps.Isles, name="DK Isles: Fungi Platform", x=2683, y=1498, z=818, scale=0.4, region=Regions.CabinIsle),
        CrownLocation(
            map=Maps.Isles,
            name="DK Isles: Waterfall Platform",
            x=3049,
            y=1490,
            z=1234,
            scale=0.4,
            region=Regions.CabinIsle,
            logic=lambda l: Events.IslesDiddyBarrelSpawn in l.Events and l.jetpack and l.peanut and l.isdiddy,
        ),
        CrownLocation(map=Maps.Isles, name="DK Isles: Near Caves Lobby Tree (1)", x=2497, y=507, z=1903, scale=0.4, region=Regions.IslesMain),
        CrownLocation(map=Maps.Isles, name="DK Isles: Near K. Rool", x=3005, y=500, z=855, scale=0.5, region=Regions.IslesMain),
        CrownLocation(map=Maps.Isles, name="DK Isles: Near Fungi Cannon", x=3440, y=495, z=1222, scale=0.4, region=Regions.IslesMain),
        CrownLocation(map=Maps.Isles, name="DK Isles: Near Caves Lobby Tree (2)", x=2427, y=600, z=1822, scale=0.4, region=Regions.IslesMain),
        # CrownLocation(
        #     map=Maps.Isles,
        #     name="DK Isles: Behind Aztec Building",
        #     x=3650,
        #     y=1020,
        #     z=1776,
        #     scale=0.4,
        #     region=Regions.IslesMainUpper,
        # ),
        CrownLocation(map=Maps.Isles, name="DK Isles: Front of Aztec Building", x=3225, y=1000, z=1613, scale=0.35, region=Regions.IslesMainUpper),
        CrownLocation(map=Maps.Isles, name="DK Isles: Near K. Lumsy", x=3107, y=520, z=3500, scale=0.3, region=Regions.IslesMain),
        CrownLocation(map=Maps.Isles, name="DK Isles: Near Monkeyport (1)", x=2519, y=550, z=4152, scale=0.5, region=Regions.IslesMain),
        CrownLocation(map=Maps.Isles, name="DK Isles: Near Monkeyport (2)", x=1852, y=600, z=3920, scale=0.5, region=Regions.IslesMain),
        CrownLocation(map=Maps.Isles, name="DK Isles: Under DK Caged GB", x=2000, y=550, z=3325, scale=0.5, region=Regions.IslesMain),
        CrownLocation(map=Maps.Isles, name="DK Isles: Behind Factory Lobby Entrance", x=2395, y=1200, z=3899, scale=0.4, region=Regions.CrocodileIsleBeyondLift),
        CrownLocation(map=Maps.Isles, name="DK Isles: Right of Factory Lobby Entrance", x=2159, y=1200, z=3518, scale=0.4, region=Regions.CrocodileIsleBeyondLift),
        CrownLocation(map=Maps.Isles, name="DK Isles: Behind Helm Lobby Entrance", x=2370, y=1720, z=3809, scale=0.25, region=Regions.IslesMain, logic=lambda l: l.monkeyport and l.istiny),
        CrownLocation(map=Maps.Isles, name="DK Isles: Left Kroc Isle Arm", x=2218, y=1620, z=3488, scale=0.5, region=Regions.IslesMain, logic=lambda l: l.monkeyport and l.istiny),
        CrownLocation(map=Maps.Isles, name="DK Isles: Right Kroc Isle Arm", x=2700, y=1620, z=3315, scale=0.5, region=Regions.IslesMain, logic=lambda l: l.monkeyport and l.istiny),
        CrownLocation(map=Maps.Isles, name="DK Isles: Fairy Isle", x=885, y=500, z=2307, scale=0.4, region=Regions.IslesMain),
        CrownLocation(map=Maps.Isles, name="DK Isles: Small Island", x=965, y=500, z=1410, scale=0.5, region=Regions.IslesMain),
        CrownLocation(map=Maps.JungleJapesLobby, name="DK Isles - Japes Lobby: Near Portal", x=711, y=0, z=632, scale=0.4, region=Regions.JungleJapesLobby),
        CrownLocation(map=Maps.AngryAztecLobby, name="DK Isles - Aztec Lobby: In Front of Feather Door", x=680, y=0, z=439, scale=0.4, region=Regions.AngryAztecLobby),
        CrownLocation(map=Maps.AngryAztecLobby, name="DK Isles - Aztec Lobby: Behind Feather Door", x=930, y=0, z=637, scale=0.4, region=Regions.AngryAztecLobby, logic=lambda l: l.feather and l.tiny),
        CrownLocation(map=Maps.FranticFactoryLobby, name="DK Isles - Factory Lobby: Near Lever", x=280, y=0, z=292, scale=0.4, region=Regions.FranticFactoryLobby),
        CrownLocation(
            map=Maps.FranticFactoryLobby, name="DK Isles - Factory Lobby: Above Portal", x=677, y=134, z=367, scale=0.4, region=Regions.FranticFactoryLobby, logic=lambda l: l.grab and l.donkey
        ),
        CrownLocation(map=Maps.GloomyGalleonLobby, name="DK Isles - Galleon Lobby: Right of Portal", x=429, y=139.6, z=942, scale=0.4, region=Regions.GloomyGalleonLobby),
        CrownLocation(map=Maps.GloomyGalleonLobby, name="DK Isles - Galleon Lobby: Left of Portal", x=855, y=119.6, z=886, scale=0.35, region=Regions.GloomyGalleonLobby),
        CrownLocation(map=Maps.CrystalCavesLobby, name="DK Isles - Caves Lobby: Right of Portal", x=1091, y=118, z=541, scale=0.4, region=Regions.CrystalCavesLobby),
        CrownLocation(
            map=Maps.CrystalCavesLobby, name="DK Isles - Caves Lobby: High Platform", x=794, y=280.4, z=739, scale=0.35, region=Regions.CrystalCavesLobby, logic=lambda l: l.jetpack and l.isdiddy
        ),
        CrownLocation(
            map=Maps.CrystalCavesLobby, name="DK Isles - Caves Lobby: Blueprint Room", x=1751, y=13.5, z=532, scale=0.4, region=Regions.CrystalCavesLobby, logic=lambda l: l.punch and l.chunky
        ),
        CrownLocation(map=Maps.CreepyCastleLobby, name="DK Isles - Castle Lobby: Right of Entrance", x=355, y=60, z=269, scale=0.4, region=Regions.CreepyCastleLobby),
        CrownLocation(map=Maps.CreepyCastleLobby, name="DK Isles - Castle Lobby: Left of Portal", x=803, y=60, z=1066, scale=0.4, region=Regions.CreepyCastleLobby),
        CrownLocation(
            map=Maps.HideoutHelmLobby,
            name="DK Isles - Helm Lobby: Bonus Platform",
            x=690,
            y=196.4,
            z=638,
            scale=0.3,
            region=Regions.HideoutHelmLobby,
            logic=lambda l: l.vines and l.gorillaGone and l.ischunky,
        ),
        CrownLocation(
            map=Maps.TrainingGrounds, name="DK Isles - Training Grounds: Far Mountain", x=1153, y=252, z=1822, scale=0.45, region=Regions.TrainingGrounds, logic=lambda l: l.twirl and l.istiny
        ),
        CrownLocation(
            map=Maps.TrainingGrounds, name="DK Isles - Training Grounds: Near Mountain", x=1187, y=225, z=734, scale=0.45, region=Regions.TrainingGrounds, logic=lambda l: l.twirl and l.istiny
        ),
        CrownLocation(map=Maps.TrainingGrounds, name="DK Isles - Training Grounds: Rear Cave", x=1196, y=36.4, z=2119, scale=0.35, region=Regions.TrainingGrounds),
        CrownLocation(map=Maps.TrainingGrounds, name="DK Isles - Training Grounds: Banana Hoard", x=2500, y=211, z=920, scale=0.35, region=Regions.TrainingGrounds, logic=lambda l: l.vines),
        CrownLocation(map=Maps.TrainingGrounds, name="DK Isles - Training Grounds: Near Pool", x=1625, y=36, z=1585, scale=0.45, region=Regions.TrainingGrounds),
        CrownLocation(map=Maps.BananaFairyRoom, name="DK Isles - Fairy Island: Right of Queen", x=648, y=37.5, z=133, scale=0.5, region=Regions.BananaFairyRoom),
        CrownLocation(map=Maps.BananaFairyRoom, name="DK Isles - Fairy Island: Behind Queen", x=1025, y=37.5, z=508, scale=0.5, region=Regions.BananaFairyRoom),
        CrownLocation(
            map=Maps.BananaFairyRoom,
            name="DK Isles - Fairy Island: Rareware Room",
            x=446,
            y=37.5,
            z=1227,
            scale=0.6,
            region=Regions.BananaFairyRoom,
            logic=lambda l: l.BananaFairies >= l.settings.rareware_gb_fairies and l.istiny,
        ),
        CrownLocation(map=Maps.KLumsy, name="DK Isles - K. Lumsy: Back Right", x=1580, y=95, z=868, scale=0.5, region=Regions.Prison),
        CrownLocation(map=Maps.KLumsy, name="DK Isles - K. Lumsy: Near Left", x=560, y=95, z=1340, scale=0.5, region=Regions.Prison),
    ],
    Levels.HideoutHelm: [
        CrownLocation(
            map=Maps.HideoutHelm,
            name="Hideout Helm - Metal grate by Mini Monkey barrel",
            x=841,
            y=-136,
            z=2545,
            scale=0.5,
            region=Regions.HideoutHelmStart,
            logic=lambda l: l.lanky
            and l.handstand
            and l.chunky
            and l.pineapple
            and l.vines
            and (
                l.settings.helm_setting == "skip_all"
                or (
                    Events.HelmDonkeyDone in l.Events
                    and Events.HelmChunkyDone in l.Events
                    and Events.HelmTinyDone in l.Events
                    and Events.HelmLankyDone in l.Events
                    and Events.HelmDiddyDone in l.Events
                )
            ),
        ),
        CrownLocation(
            map=Maps.HideoutHelm,
            name="Hideout Helm - Mini Monkey room right side",
            x=1010,
            y=-132,
            z=2243,
            scale=0.5,
            region=Regions.HideoutHelmStart,
            logic=lambda l: l.lanky
            and l.handstand
            and l.chunky
            and l.pineapple
            and l.vines
            and (
                l.settings.helm_setting == "skip_all"
                or (
                    Events.HelmDonkeyDone in l.Events
                    and Events.HelmChunkyDone in l.Events
                    and Events.HelmTinyDone in l.Events
                    and Events.HelmLankyDone in l.Events
                    and Events.HelmDiddyDone in l.Events
                )
            ),
        ),
        CrownLocation(
            map=Maps.HideoutHelm,
            name="Hideout Helm - Pineapple switch room in ammo alcove",
            x=1077,
            y=-164,
            z=1261,
            scale=0.5,
            region=Regions.HideoutHelmStart,
            logic=lambda l: l.lanky
            and l.handstand
            and l.settings.helm_setting == "skip_all"
            or (Events.HelmDonkeyDone in l.Events and Events.HelmChunkyDone in l.Events and Events.HelmTinyDone in l.Events and Events.HelmLankyDone in l.Events and Events.HelmDiddyDone in l.Events),
        ),
        CrownLocation(
            map=Maps.HideoutHelm,
            name="Hideout Helm - First room left of Tag barrel",
            x=2065,
            y=-461,
            z=480,
            scale=0.5,
            region=Regions.HideoutHelmStart,
            logic=lambda l: (
                l.settings.helm_setting == "skip_all"
                or (
                    Events.HelmDonkeyDone in l.Events
                    and Events.HelmChunkyDone in l.Events
                    and Events.HelmTinyDone in l.Events
                    and Events.HelmLankyDone in l.Events
                    and Events.HelmDiddyDone in l.Events
                )
            ),
        ),
        CrownLocation(
            map=Maps.HideoutHelm,
            name="Hideout Helm - Top of Blast-o-Matic",
            x=1047.6,
            y=448.1,
            z=3391.4,
            scale=0.25,
            region=Regions.HideoutHelmMain,
            is_vanilla=True,
            logic=lambda l: l.jetpack
            and l.isdiddy
            and (
                l.settings.helm_setting == "skip_all"
                or (
                    Events.HelmDonkeyDone in l.Events
                    and Events.HelmChunkyDone in l.Events
                    and Events.HelmTinyDone in l.Events
                    and Events.HelmLankyDone in l.Events
                    and Events.HelmDiddyDone in l.Events
                )
            ),
        ),
        # CrownLocation(
        #     map=Maps.HideoutHelm,
        #     name="Hideout Helm - DK's room",
        #     x=396,
        #     y=-132,
        #     z=3841,
        #     scale=0.5,
        #     region=Regions.HideoutHelmMain,
        #     logic=lambda l: Events.HelmDoorsOpened in l.Events and l.punch and l.bongos and l.isdonkey,
        # ),
        # CrownLocation(
        #     map=Maps.HideoutHelm,
        #     name="Hideout Helm - Chunky's room",
        #     x=1518,
        #     y=-72,
        #     z=2761,
        #     scale=0.5,
        #     region=Regions.HideoutHelmMain,
        #     logic=lambda l: Events.HelmDoorsOpened in l.Events and l.punch and l.triangle and l.ischunky,
        # ),
        # CrownLocation(
        #     map=Maps.HideoutHelm,
        #     name="Hideout Helm - Tiny's room",
        #     x=281,
        #     y=-32,
        #     z=3281,
        #     scale=0.5,
        #     region=Regions.HideoutHelmMain,
        #     logic=lambda l: Events.HelmDoorsOpened in l.Events and l.punch and l.saxophone and l.istiny,
        # ),
        # CrownLocation(
        #     map=Maps.HideoutHelm,
        #     name="Hideout Helm - Lanky's room",
        #     x=1824,
        #     y=48,
        #     z=3272,
        #     scale=0.5,
        #     region=Regions.HideoutHelmMain,
        #     logic=lambda l: Events.HelmDoorsOpened in l.Events and l.punch and l.trombone and l.islanky,
        # ),
        # CrownLocation(
        #     map=Maps.HideoutHelm,
        #     name="Hideout Helm - Diddy's room",
        #     x=583,
        #     y=208,
        #     z=2741,
        #     scale=0.5,
        #     region=Regions.HideoutHelmMain,
        #     logic=lambda l: Events.HelmDoorsOpened in l.Events and l.punch and l.jetpack and l.guitar and l.isdiddy,
        # ),
        CrownLocation(
            map=Maps.HideoutHelm,
            name="Hideout Helm - Blast-o-Matic platform left side",
            x=1048,
            y=-2,
            z=3266,
            scale=0.4,
            region=Regions.HideoutHelmMain,
            logic=lambda l: (
                l.settings.helm_setting == "skip_all"
                or (
                    Events.HelmDonkeyDone in l.Events
                    and Events.HelmChunkyDone in l.Events
                    and Events.HelmTinyDone in l.Events
                    and Events.HelmLankyDone in l.Events
                    and Events.HelmDiddyDone in l.Events
                )
            ),
        ),
        CrownLocation(
            map=Maps.HideoutHelm,
            name="Hideout Helm - Blast-o-Matic platform right side",
            x=1051,
            y=-2,
            z=3518,
            scale=0.4,
            region=Regions.HideoutHelmMain,
            logic=lambda l: (
                l.settings.helm_setting == "skip_all"
                or (
                    Events.HelmDonkeyDone in l.Events
                    and Events.HelmChunkyDone in l.Events
                    and Events.HelmTinyDone in l.Events
                    and Events.HelmLankyDone in l.Events
                    and Events.HelmDiddyDone in l.Events
                )
            ),
        ),
        CrownLocation(
            map=Maps.HideoutHelm,
            name="Hideout Helm - Under K. Rool door",
            x=1054,
            y=-132,
            z=3721,
            scale=0.4,
            region=Regions.HideoutHelmMain,
            logic=lambda l: (
                l.settings.helm_setting == "skip_all"
                or (
                    Events.HelmDonkeyDone in l.Events
                    and Events.HelmChunkyDone in l.Events
                    and Events.HelmTinyDone in l.Events
                    and Events.HelmLankyDone in l.Events
                    and Events.HelmDiddyDone in l.Events
                )
            ),
        ),
        CrownLocation(
            map=Maps.HideoutHelm,
            name="Hideout Helm - Navigation room near terminals",
            x=1262,
            y=10,
            z=4467,
            scale=0.75,
            region=Regions.HideoutHelmMain,
            logic=lambda l: (
                l.settings.helm_setting == "skip_all"
                or (
                    Events.HelmDonkeyDone in l.Events
                    and Events.HelmChunkyDone in l.Events
                    and Events.HelmTinyDone in l.Events
                    and Events.HelmLankyDone in l.Events
                    and Events.HelmDiddyDone in l.Events
                )
            ),
        ),
        CrownLocation(
            map=Maps.HideoutHelm,
            name="Hideout Helm - Navigation room near left window",
            x=1584,
            y=10,
            z=4349,
            scale=0.5,
            region=Regions.HideoutHelmMain,
            logic=lambda l: (
                l.settings.helm_setting == "skip_all"
                or (
                    Events.HelmDonkeyDone in l.Events
                    and Events.HelmChunkyDone in l.Events
                    and Events.HelmTinyDone in l.Events
                    and Events.HelmLankyDone in l.Events
                    and Events.HelmDiddyDone in l.Events
                )
            ),
        ),
        CrownLocation(
            map=Maps.HideoutHelm,
            name="Hideout Helm - Navigation room near right window",
            x=1577,
            y=10,
            z=4593,
            scale=0.5,
            region=Regions.HideoutHelmMain,
            logic=lambda l: (
                l.settings.helm_setting == "skip_all"
                or (
                    Events.HelmDonkeyDone in l.Events
                    and Events.HelmChunkyDone in l.Events
                    and Events.HelmTinyDone in l.Events
                    and Events.HelmLankyDone in l.Events
                    and Events.HelmDiddyDone in l.Events
                )
            ),
        ),
        CrownLocation(
            map=Maps.HideoutHelm,
            name="Hideout Helm - K. Rool room near kong faces",
            x=523,
            y=74,
            z=5341,
            scale=0.6,
            region=Regions.HideoutHelmMain,
            logic=lambda l: (
                l.settings.helm_setting == "skip_all"
                or (
                    Events.HelmDonkeyDone in l.Events
                    and Events.HelmChunkyDone in l.Events
                    and Events.HelmTinyDone in l.Events
                    and Events.HelmLankyDone in l.Events
                    and Events.HelmDiddyDone in l.Events
                )
            ),
        ),
        CrownLocation(
            map=Maps.HideoutHelm,
            name="Hideout Helm - K. Rool room in front of chair",
            x=548,
            y=74,
            z=5036,
            scale=0.6,
            region=Regions.HideoutHelmMain,
            logic=lambda l: (
                l.settings.helm_setting == "skip_all"
                or (
                    Events.HelmDonkeyDone in l.Events
                    and Events.HelmChunkyDone in l.Events
                    and Events.HelmTinyDone in l.Events
                    and Events.HelmLankyDone in l.Events
                    and Events.HelmDiddyDone in l.Events
                )
            ),
        ),
    ],
}
