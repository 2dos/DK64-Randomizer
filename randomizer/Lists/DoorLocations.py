"""Stores the data for each potential T&S and Wrinkly door location."""
from randomizer.Enums.Events import Events
from randomizer.Lists.MapsAndExits import Maps
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Regions import Regions
from randomizer.Enums.Time import Time
from randomizer.Enums.Kongs import Kongs


class DoorData:
    """Stores information about a door location."""

    def __init__(
        self,
        *,
        name="",
        map=0,
        logicregion="",
        location=[0, 0, 0, 0],
        rx=0,
        rz=0,
        kong_lst=[Kongs.donkey, Kongs.diddy, Kongs.lanky, Kongs.tiny, Kongs.chunky],
        wrinkly_only=False,
        placed=None,
        scale=1,
        logic=0
    ):
        """Initialize with provided data."""
        self.name = name
        self.map = map
        self.location = location
        self.logicregion = logicregion
        self.rx = rx
        self.rz = rz
        self.kongs = kong_lst
        self.scale = scale
        self.logic = logic
        self.placed = placed
        self.default_placed = placed
        self.assigned_kong = None
        self.wrinkly_only = wrinkly_only  # not a suitable T&S portal location, because of higher requirements, or because it's not very easy to find

    def assignDoor(self, kong):
        """Assign door to kong."""
        self.placed = "wrinkly"
        self.assigned_kong = kong

    def assignPortal(self):
        """Assign T&S Portal to slot."""
        self.placed = "tns"


door_locations = {
    Levels.JungleJapes: [
        DoorData(name="Japes Lobby: Middle Right", map=Maps.JungleJapesLobby, logicregion=Regions.JungleJapesLobby, location=[169.075, 10.833, 594.613, 90], placed="wrinkly"),  # DK Door
        DoorData(name="Japes Lobby: Far Left", map=Maps.JungleJapesLobby, logicregion=Regions.JungleJapesLobby, location=[647.565, 0, 791.912, 183], placed="wrinkly"),  # Diddy Door
        DoorData(name="Japes Lobby: Close Right", map=Maps.JungleJapesLobby, logicregion=Regions.JungleJapesLobby, location=[156.565, 10.833, 494.73, 98], placed="wrinkly"),  # Lanky Door
        DoorData(name="Japes Lobby: Far Right", map=Maps.JungleJapesLobby, logicregion=Regions.JungleJapesLobby, location=[252.558, 0, 760.733, 163], placed="wrinkly"),  # Tiny Door
        DoorData(name="Japes Lobby: Close Left", map=Maps.JungleJapesLobby, logicregion=Regions.JungleJapesLobby, location=[821.85, 0, 615.167, 264], placed="wrinkly"),  # Chunky Door
        DoorData(name="Japes: Diddy Cave", map=Maps.JungleJapes, location=[2489.96, 280, 736.892, 179], placed="tns"),  # T&S Door in Diddy Cave
        # DoorData(name="Japes: Near Painting Room", map=Maps.JungleJapes, location=[722.473, 538, 2386.608, 141], placed="tns"),  # T&S Door in Near Painting Room. Omitted because the indicator is weird
        DoorData(name="Japes: Fairy Cave", map=Maps.JungleJapes, location=[901.203, 279, 3795.889, 202], placed="tns"),  # T&S Door in Fairy Cave
    ],
    Levels.AngryAztec: [
        DoorData(name="Aztec Lobby: Pillar Wall", map=Maps.AngryAztecLobby, logicregion=Regions.AngryAztecLobby, location=[499.179, 0, 146.628, 0], placed="wrinkly"),  # DK Door
        DoorData(name="Aztec Lobby: Lower Right", map=Maps.AngryAztecLobby, logicregion=Regions.AngryAztecLobby, location=[441.456, 0, 614.029, 180], placed="wrinkly"),  # Diddy Door
        DoorData(name="Aztec Lobby: Left of Portal", map=Maps.AngryAztecLobby, logicregion=Regions.AngryAztecLobby, location=[628.762, 80, 713.93, 177], placed="wrinkly"),  # Lanky Door
        DoorData(name="Aztec Lobby: Right of Portal", map=Maps.AngryAztecLobby, logicregion=Regions.AngryAztecLobby, location=[377.124, 80, 712.484, 179], placed="wrinkly"),  # Tiny Door
        DoorData(name="Aztec Lobby: Behind Feather Door", map=Maps.AngryAztecLobby, logicregion=Regions.AngryAztecLobby, location=[1070.018, 0, 738.609, 190], placed="wrinkly"),  # Custom Chunky Door
        DoorData(name="Aztec: Near Funky's", map=Maps.AngryAztec, location=[2801.765, 121.333, 4439.293, 66], placed="tns"),  # T&S Portal by Funky
        DoorData(name="Aztec: Near Cranky's", map=Maps.AngryAztec, location=[2787.908, 120, 2674.299, 198], placed="tns"),  # T&S Portal by Cranky
        DoorData(name="Aztec: Near Candy's", map=Maps.AngryAztec, location=[2268.343, 120, 448.669, 59], placed="tns"),  # T&S Portal by Candy
        DoorData(name="Aztec: Near Snide's", map=Maps.AngryAztec, location=[3573.712, 120, 4456.399, 285], placed="tns"),  # T&S Portal by Snide
        DoorData(name="Aztec: Behind 5DT", map=Maps.AngryAztec, location=[1968.329, 180, 3457.189, 244], placed="tns"),  # T&S Portal behind 5DT
        DoorData(name="Next to Candy - right", map=Maps.AngryAztec, logicregion=Regions.AngryAztecStart, location=[2468, 120, 473.5, 298.75]),
        DoorData(name="5Door Temple's 6th Door", map=Maps.AngryAztec, logicregion=Regions.AngryAztecMain, location=[2212, 180, 3687.3, 62.9], scale=1.47),
    ],
    Levels.FranticFactory: [
        DoorData(name="Factory Lobby: Low Left", map=Maps.FranticFactoryLobby, logicregion=Regions.FranticFactoryLobby, location=[544.362, 0, 660.802, 182], placed="wrinkly"),  # DK Door
        DoorData(name="Factory Lobby: Top Left", map=Maps.FranticFactoryLobby, logicregion=Regions.FranticFactoryLobby, location=[660.685, 133.5, 660.774, 182], placed="wrinkly"),  # Diddy Door
        DoorData(name="Factory Lobby: Top Center", map=Maps.FranticFactoryLobby, logicregion=Regions.FranticFactoryLobby, location=[468.047, 85.833, 662.907, 180], placed="wrinkly"),  # Lanky Door
        DoorData(name="Factory Lobby: Top Right", map=Maps.FranticFactoryLobby, logicregion=Regions.FranticFactoryLobby, location=[275.533, 133.5, 661.908, 180], placed="wrinkly"),  # Tiny Door
        DoorData(name="Factory Lobby: Low Right", map=Maps.FranticFactoryLobby, logicregion=Regions.FranticFactoryLobby, location=[393.114, 0, 662.562, 182], placed="wrinkly"),  # Chunky Door
        DoorData(name="Factory: Arcade Room", map=Maps.FranticFactory, location=[1778.702, 1106.667, 1220.515, 357], placed="tns"),  # T&S Portal in Arcade Room
        DoorData(name="Factory: Production Room", map=Maps.FranticFactory, location=[381.573, 605, 1032.929, 45], placed="tns"),  # T&S Portal in Production Room
        DoorData(name="Factory: R&D", map=Maps.FranticFactory, location=[3827.127, 1264, 847.458, 222], placed="tns"),  # T&S Portal in R&D
        DoorData(name="Factory: Block Tower", map=Maps.FranticFactory, location=[2259.067, 1126.824, 1614.609, 182], placed="tns"),  # T&S Portal in Block Tower Room
        DoorData(name="Factory: Storage Room", map=Maps.FranticFactory, location=[1176.912, 6.5, 472.114, 1], placed="tns"),  # T&S Portal in Storage Room
        DoorData(name="Crusher Room - start", map=Maps.FactoryCrusher, logicregion=Regions.FranticFactoryLobby, location=[475, 0, 539, 180]),
    ],
    Levels.GloomyGalleon: [
        DoorData(name="Galleon Lobby: Far Left", map=Maps.GloomyGalleonLobby, logicregion=Regions.GloomyGalleonLobby, location=[1022.133, 139.667, 846.41, 276], placed="wrinkly"),  # DK Door
        DoorData(name="Galleon Lobby: Far Right", map=Maps.GloomyGalleonLobby, logicregion=Regions.GloomyGalleonLobby, location=[345.039, 139.667, 884.162, 92], placed="wrinkly"),  # Diddy Door
        DoorData(name="Galleon Lobby: Close Right", map=Maps.GloomyGalleonLobby, logicregion=Regions.GloomyGalleonLobby, location=[464.68, 159.667, 1069.446, 161], placed="wrinkly"),  # Lanky Door
        DoorData(name="Galleon Lobby: Near DK Portal", map=Maps.GloomyGalleonLobby, logicregion=Regions.GloomyGalleonLobby, location=[582.36, 159.667, 1088.258, 180], placed="wrinkly"),  # Tiny Door
        DoorData(name="Galleon Lobby: Close Left", map=Maps.GloomyGalleonLobby, logicregion=Regions.GloomyGalleonLobby, location=[876.388, 178.667, 1063.828, 192], placed="wrinkly"),  # Chunky Door
        DoorData(name="Galleon: Near Cranky's", map=Maps.GloomyGalleon, location=[3423.707, 1890.471, 3098.15, 243], placed="tns"),  # T&S Door Near Cranky's
        DoorData(name="Galleon: Deep Hole", map=Maps.GloomyGalleon, location=[1975.898, 100, 4498.375, 256], placed="tns"),  # T&S Door in meme hole
        DoorData(name="Galleon: Behind 2DS", map=Maps.GloomyGalleon, location=[803.636, 1053.997, 1955.268, 92], placed="tns"),  # T&S Door behind 2DS
        DoorData(name="Galleon: Behind Enguarde Door", map=Maps.GloomyGalleon, location=[645.832, 1460, 4960.476, 133], placed="tns"),  # T&S Door behind Enguarde Door
        DoorData(name="Galleon: Cactus", map=Maps.GloomyGalleon, location=[4517.923, 1290, 894.527, 308], placed="tns"),  # T&S Door near Cactus
        DoorData(name="Treasure Chest Exterior", map=Maps.GloomyGalleon, logicregion=Regions.TreasureRoom, location=[1938, 1440, 524, 330]),
        DoorData(name="Next to Warp 3 in Cranky's Area", map=Maps.GloomyGalleon, logicregion=Regions.GloomyGalleonStart, location=[3071, 1890, 2838, 0]),
        DoorData(name="In Primate Punch Chest Room - right", map=Maps.GloomyGalleon, logicregion=Regions.GloomyGalleonStart, location=[3460, 1670, 4001, 180]),
        DoorData(
            name="Next to Cannonball game", map=Maps.GloomyGalleon, logicregion=Regions.GalleonBeyondPineappleGate, location=[1334, 1610, 2523, 0], logic=lambda l: Events.WaterSwitch in l.Events
        ),
        DoorData(name="Music Cactus - bottom front left", map=Maps.GloomyGalleon, logicregion=Regions.Shipyard, location=[4239, 1289, 880, 38.31]),
        DoorData(name="Music Cactus - bottom back left", map=Maps.GloomyGalleon, logicregion=Regions.Shipyard, location=[4444, 1290, 803, 307.7]),
        DoorData(name="Music Cactus - bottom front right", map=Maps.GloomyGalleon, logicregion=Regions.Shipyard, location=[4524, 1290, 1145, 218.31]),
        DoorData(name="Music Cactus - bottom back right", map=Maps.GloomyGalleon, logicregion=Regions.Shipyard, location=[4587, 1290, 972, 307.85]),
        DoorData(name="In hallway to Shipyard - Tiny switch", map=Maps.GloomyGalleon, logicregion=Regions.GloomyGalleonStart, location=[2205, 1620, 2700, 90]),
        DoorData(name="In hallway to Shipyard - Lanky switch", map=Maps.GloomyGalleon, logicregion=Regions.GloomyGalleonStart, location=[2615, 1620, 2844, 302]),
        DoorData(name="In hallway to Primate Punch Chests", map=Maps.GloomyGalleon, logicregion=Regions.GloomyGalleonStart, location=[3007, 1670, 3866, 135.42]),
        DoorData(name="Under Baboon Blast pad", map=Maps.GloomyGalleon, logicregion=Regions.LighthousePlatform, location=[1674.5, 1610, 4042.5, 261.15]),
        DoorData(name="Under RocketBarrel barrel", map=Maps.GloomyGalleon, logicregion=Regions.LighthousePlatform, location=[1360, 1609, 4048, 86]),
        DoorData(name="Next to Coconut switch", map=Maps.GloomyGalleon, logicregion=Regions.GloomyGalleonStart, location=[2065.75, 1628, 3418.75, 28]),
        DoorData(name="Entrance Tunnel - near entrance", map=Maps.GloomyGalleon, logicregion=Regions.GloomyGalleonStart, location=[2112, 1628, 3223, 135]),
        DoorData(name="Next to Peanut switch", map=Maps.GloomyGalleon, logicregion=Regions.GloomyGalleonStart, location=[2462, 1619, 2688, 270]),
        DoorData(name="Tiny's 5D ship", map=Maps.Galleon5DShipDKTiny, logicregion=Regions.SaxophoneShip, location=[735, 0, 1336, 270], kong_lst=[Kongs.tiny]),
        DoorData(name="Lanky's 5D ship", map=Maps.Galleon5DShipDiddyLankyChunky, logicregion=Regions.TromboneShip, location=[1099, 0, 1051, 270], kong_lst=[Kongs.lanky]),
        DoorData(name="Behind Chunky punch gate in Cranky Area", map=Maps.GloomyGalleon, location=[3275, 1670, 2353.65, 13.65], kong_lst=[Kongs.chunky], logic=lambda l: l.punch),
        DoorData(name="Lighthouse Interior", map=Maps.GalleonLighthouse, logicregion=Regions.Lighthouse, location=[508, 200, 409, 135.2], kong_lst=[Kongs.donkey]),
        DoorData(name="Low water alcove in lighthouse area", map=Maps.GloomyGalleon, logicregion=Regions.LighthouseSurface, location=[540.3, 1564, 4094, 110]),
        DoorData(name="Behind boxes in Cranky Area", map=Maps.GloomyGalleon, logicregion=Regions.GloomyGalleonStart, location=[2891.5, 1688, 3493, 124]),
        DoorData(name="Lanky's 2D ship", map=Maps.Galleon2DShip, logicregion=Regions.LankyShip, location=[1616, 0, 939, 179.5], kong_lst=[Kongs.lanky]),
        DoorData(name="Mech Fish Gate - far left", map=Maps.GloomyGalleon, logicregion=Regions.Shipyard, location=[2651, 140.5, 503, 92]),
        DoorData(name="Mech Fish Gate - left", map=Maps.GloomyGalleon, logicregion=Regions.Shipyard, location=[2792, 175, 299.3, 15.9], rz=7.3),
        DoorData(name="Mech Fish Gate - middle", map=Maps.GloomyGalleon, logicregion=Regions.Shipyard, location=[3225, 205, 303, 329], rz=-4.7),
        DoorData(name="Mech Fish Gate - right", map=Maps.GloomyGalleon, logicregion=Regions.Shipyard, location=[3406, 166, 531, 260], rx=290, rz=-290),
        DoorData(name="Mech Fish Gate - far right", map=Maps.GloomyGalleon, logicregion=Regions.Shipyard, location=[3310, 147, 828, 216.5], rx=16, rz=-16),
        DoorData(name="Cannonball Area Exit", map=Maps.GloomyGalleon, logicregion=Regions.GalleonBeyondPineappleGate, location=[1524.1, 1461, 2898, 278]),
        DoorData(name="2Dship's secret 3rd door", map=Maps.GloomyGalleon, logicregion=Regions.Shipyard, location=[1109, 1189.9, 1978, 95], rz=-47),
        DoorData(name="In Mermaid's Palace", map=Maps.GalleonMermaidRoom, logicregion=Regions.MermaidRoom, location=[274, 0, 481, 150], kong_lst=[Kongs.tiny]),
        DoorData(name="Near Mermaid's Palace - right", map=Maps.GloomyGalleon, logicregion=Regions.LighthouseUnderwater, location=[1445, 141, 4859, 180]),
        DoorData(name="Near Mermaid's Palace - left", map=Maps.GloomyGalleon, logicregion=Regions.LighthouseUnderwater, location=[1400, 112.8, 4215, 346.5], rz=3),
        DoorData(name="Near Mermaid's Palace - Under Tag Barrel", map=Maps.GloomyGalleon, logicregion=Regions.LighthouseUnderwater, location=[915, 164, 3967, 30], rx=7, rz=3),
        DoorData(
            name="On top of Seal cage",
            map=Maps.GloomyGalleon,
            logicregion=Regions.LighthousePlatform,
            location=[2238, 1837, 4099, 251.7],
            kong_lst=[Kongs.diddy],
            logic=lambda l: l.jetpack,
            wrinkly_only=True,
        ),
    ],
    Levels.FungiForest: [
        DoorData(
            name="Fungi Lobby: On High Box", map=Maps.FungiForestLobby, logicregion=Regions.FungiForestLobby, location=[449.866, 45.922, 254.6, 270], placed="wrinkly"
        ),  # Custom Location (Removing Wheel)
        DoorData(
            name="Fungi Lobby: Near Gorilla Gone Door", map=Maps.FungiForestLobby, logicregion=Regions.FungiForestLobby, location=[136.842, 0, 669.81, 90], placed="wrinkly"
        ),  # Custom Location (Removing Wheel)
        DoorData(
            name="Fungi Lobby: Opposite Gorilla Gone Door", map=Maps.FungiForestLobby, logicregion=Regions.FungiForestLobby, location=[450.219, 0, 689.048, 270], placed="wrinkly"
        ),  # Custom Location (Removing Wheel)
        DoorData(
            name="Fungi Lobby: Near B. Locker", map=Maps.FungiForestLobby, logicregion=Regions.FungiForestLobby, location=[293, 0, 154.197, 0], placed="wrinkly", scale=1.2
        ),  # Custom Location (Removing Wheel)
        DoorData(
            name="Fungi Lobby: Near Entrance", map=Maps.FungiForestLobby, logicregion=Regions.FungiForestLobby, location=[450.862, 0, 565.029, 270], placed="wrinkly"
        ),  # Custom Location (Removing Wheel)
        DoorData(name="Fungi: Behind DK Barn", map=Maps.FungiForest, location=[3515.885, 115.009, 1248.55, 31], placed="tns"),  # T&S Portal behind DK Barn
        DoorData(name="Fungi: Beanstalk Area", map=Maps.FungiForest, location=[3665.871, 186.833, 945.745, 252], placed="tns"),  # T&S Portal in Beanstalk Area
        DoorData(name="Fungi: Near Snide's", map=Maps.FungiForest, location=[3240.033, 268.5, 3718.017, 178], placed="tns"),  # T&S Portal near Snide's
        DoorData(name="Fungi: Top of Giant Mushroom", map=Maps.FungiForest, location=[1171.791, 1250, 1236.572, 52], placed="tns"),  # T&S Portal at Top of GMush
        DoorData(name="Fungi: Owl Area", map=Maps.FungiForest, location=[203.663, 199.333, 3844.253, 92], placed="tns"),  # T&S Portal near Owl Race
    ],
    Levels.CrystalCaves: [
        DoorData(name="Caves Lobby: Far Left", map=Maps.CrystalCavesLobby, logicregion=Regions.CrystalCavesLobby, location=[1103.665, 146.5, 823.872, 194], placed="wrinkly"),  # DK Door
        DoorData(
            name="Caves Lobby: Top Ledge",
            map=Maps.CrystalCavesLobby,
            logicregion=Regions.CrystalCavesLobby,
            location=[731.84, 280.5, 704.935, 120],
            placed="wrinkly",
            kong_lst=[Kongs.diddy],
        ),  # Diddy Door
        DoorData(name="Caves Lobby: Near Left", map=Maps.CrystalCavesLobby, logicregion=Regions.CrystalCavesLobby, location=[1046.523, 13.5, 476.611, 189], placed="wrinkly"),  # Lanky Door
        DoorData(name="Caves Lobby: Far Right", map=Maps.CrystalCavesLobby, logicregion=Regions.CrystalCavesLobby, location=[955.407, 146.664, 843.472, 187], placed="wrinkly"),  # Tiny Door
        DoorData(name="Caves Lobby: Near Right", map=Maps.CrystalCavesLobby, logicregion=Regions.CrystalCavesLobby, location=[881.545, 13.466, 508.666, 193], placed="wrinkly"),  # Chunky Door
        DoorData(name="Caves: On Rotating Room", map=Maps.CrystalCaves, location=[2853.776, 436.949, 2541.475, 207], placed="tns"),  # T&S Portal on Rotating Room
        DoorData(name="Caves: Near Snide's", map=Maps.CrystalCaves, location=[1101.019, 64.5, 467.76, 69], placed="tns"),  # T&S Portal near Snide's
        DoorData(name="Caves: Giant Boulder Room", map=Maps.CrystalCaves, location=[1993.556, 277.108, 2795.365, 193], placed="tns"),  # T&S Portal in Giant Boulder Room
        DoorData(name="Caves: On Sprint Cabin", map=Maps.CrystalCaves, location=[2196.449, 394.167, 1937.031, 93], placed="tns"),  # T&S Portal on Sprint Cabin
        DoorData(name="Caves: Near 5DI", map=Maps.CrystalCaves, location=[120.997, 50.167, 1182.974, 75.146], placed="tns"),  # T&S Portal near 5DI (Custom)
        DoorData(name="Outside Lanky's Cabin", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[2400, 276, 1892.5, 21.75]),
        DoorData(name="Outside Chunky's Cabin", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[3515.65, 175, 1893, 273.7]),
        DoorData(name="Outside Diddy's Lower Cabin", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[3697.5, 260, 1505, 291]),
        DoorData(name="Outside Diddy's Upper Cabin", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[3666.7, 343, 1762, 273.8]),
        DoorData(name="Under the Waterfall (Cabin Area)", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[2230, 0, 2178, 100]),
        DoorData(name="Across from the 5Door Cabin", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[2970, 128, 1499, 68.5], rx=9, rz=11),
        DoorData(name="5Door Igloo - DK's instrument pad", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[481, 0, 1444, 328]),
        DoorData(name="5Door Igloo - Diddy's instrument pad", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[698.5, 0, 1424.5, 40.5]),
        DoorData(name="5Door Igloo - Tiny's instrument pad", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[747, 0, 1212.5, 111.8]),
        DoorData(name="5Door Igloo - Chunky's instrument pad", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[561, 0, 1101, 184]),
        DoorData(name="5Door Igloo - Lanky's instrument pad", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[396, 0, 1244, 256]),
        DoorData(name="Ice Castle Area - Near Rock Switch", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[1349.6, 330, 1079, 86.7], rx=4),
        DoorData(name="In Chunky's 5Door Cabin on a Book Shelf", map=Maps.CavesChunkyCabin, logicregion=Regions.ChunkyCabin, location=[403.5, 44, 579, 180], kong_lst=[Kongs.chunky]),
        DoorData(name="Between Funky and Ice Castle - on land", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[2240.65, 65.8, 1185, 89.25]),
        DoorData(name="Between Funky and Ice Castle - underwater", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[2370, 0, 1096, 196]),
        DoorData(name="In Water Near W4 Opposite Cranky - right", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[1187, 0, 2410, 133.5]),
        DoorData(name="In Water Near W4 Opposite Cranky - left", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[1441, 0, 2385, 208]),
        DoorData(name="Under Bridge to Cranky", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[1140, 0, 1704, 350.4]),
        DoorData(name="Under Handstand Slope", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[1263.3, 93, 1291, 73.5]),
        DoorData(name="Mini Monkey Ledge", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[3112.3, 257, 1142, 262], rx=5, scale=0.4),
        DoorData(name="Across from Snide", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[1818.5, 82, 1450, 218.5], rx=-14, rz=21),
        DoorData(name="Slope to Cranky with Mini Monkey Hole", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[1047, 190, 2426, 175], rz=5.5),
        DoorData(name="Level Entrance - right", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[1827, -29, 342, 225]),
        DoorData(name="Level Entrance - left", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[1828, -29, 91, 315.5]),
        DoorData(name="Ice Castle - left", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[2190.5, 343, 986.5, 314.2], scale=0.67),
        DoorData(name="Ice Castle - right", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[2221, 343, 957, 134.2], scale=0.67),
        DoorData(name="Igloo Area - left of entrance", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[637, 0, 1605, 174.75], rx=-4),
        DoorData(name="Igloo Area - Behind Tag Barrel Island", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[157, 0, 1575, 122]),
        DoorData(name="Igloo Area - Behind Warp 1", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[282.5, 0, 892, 58]),
        DoorData(name="Igloo Area - right of entrance", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[956, 0, 1222, 270.5]),
        DoorData(name="Under Funky's Store", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[2868, 0, 1246, 113]),
        DoorData(name="Next to Waterfall that's Next to Funky", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[3093, 0, 1262, 268]),
        DoorData(name="In Water Under Funky - left", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[3055, 0, 658, 1.28]),
        DoorData(name="In Water Under Funky - center", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[3221, 0, 820, 292.5]),
        DoorData(name="In Water Under Funky - right", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[3218, 0, 933, 256.3]),
    ],
    Levels.CreepyCastle: [
        DoorData(name="Castle Lobby: Central Pillar (1)", map=Maps.CreepyCastleLobby, logicregion=Regions.CreepyCastleLobby, location=[499.978, 71.833, 634.25, 240], placed="wrinkly"),  # DK Door
        DoorData(name="Castle Lobby: Central Pillar (2)", map=Maps.CreepyCastleLobby, logicregion=Regions.CreepyCastleLobby, location=[499.545, 71.833, 725.653, 300], placed="wrinkly"),  # Diddy Door
        DoorData(name="Castle Lobby: Central Pillar (3)", map=Maps.CreepyCastleLobby, logicregion=Regions.CreepyCastleLobby, location=[661.738, 71.833, 726.433, 60], placed="wrinkly"),  # Lanky Door
        DoorData(name="Castle Lobby: Central Pillar (4)", map=Maps.CreepyCastleLobby, logicregion=Regions.CreepyCastleLobby, location=[660.732, 71.833, 635.288, 118], placed="wrinkly"),  # Tiny Door
        DoorData(name="Castle Lobby: Central Pillar (5)", map=Maps.CreepyCastleLobby, logicregion=Regions.CreepyCastleLobby, location=[581.215, 71.833, 588.444, 182], placed="wrinkly"),  # Chunky Door
        DoorData(name="Castle: Near Greenhouse", map=Maps.CreepyCastle, location=[1543.986, 1381.167, 1629.089, 3], placed="tns"),  # T&S Portal by Greenhouse
        DoorData(name="Castle: Small Plateau", map=Maps.CreepyCastle, location=[1759.241, 903.75, 1060.8, 138], placed="tns"),  # T&S Portal by W2
        DoorData(name="Castle: Back of Castle", map=Maps.CreepyCastle, location=[1704.55, 368.026, 1896.767, 4], placed="tns"),  # T&S Portal around back
        DoorData(name="Castle: Near Funky's", map=Maps.CastleLowerCave, location=[1619.429, 200, 313.484, 299], placed="tns"),  # T&S Portal in Crypt Hub
        DoorData(name="Castle: Near Candy's", map=Maps.CastleUpperCave, location=[1025.262, 300, 1960.308, 359], placed="tns"),  # T&S Portal in Dungeon Tunnel
    ],
}
