"""Stores the data for each potential T&S and Wrinkly door location."""
from randomizer.Lists.MapsAndExits import Maps
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Kongs import Kongs


class DoorData:
    """Stores information about a door location."""

    def __init__(self, *, name="", map=0, location=[0, 0, 0, 0], kong_lst=[Kongs.donkey, Kongs.diddy, Kongs.lanky, Kongs.tiny, Kongs.chunky], scale=1, placed="none"):
        """Initialize with provided data."""
        self.name = name
        self.map = map
        self.location = location
        self.kongs = kong_lst
        self.scale = scale
        self.placed = placed
        self.default_placed = placed
        self.assigned_kong = None

    def assignDoor(self, kong):
        """Assign door to kong."""
        self.placed = "wrinkly"
        self.assigned_kong = kong

    def assignPortal(self):
        self.placed = "tns"


door_locations = {
    Levels.JungleJapes: [
        DoorData(name="Japes Lobby: Middle Right", map=Maps.JungleJapesLobby, location=[169.075, 10.833, 594.613, 90], placed="wrinkly"),  # DK Door
        DoorData(name="Japes Lobby: Far Left", map=Maps.JungleJapesLobby, location=[647.565, 0, 791.912, 183], placed="wrinkly"),  # Diddy Door
        DoorData(name="Japes Lobby: Close Right", map=Maps.JungleJapesLobby, location=[156.565, 10.833, 494.73, 98], placed="wrinkly"),  # Lanky Door
        DoorData(name="Japes Lobby: Far Right", map=Maps.JungleJapesLobby, location=[252.558, 0, 760.733, 163], placed="wrinkly"),  # Tiny Door
        DoorData(name="Japes Lobby: Close Left", map=Maps.JungleJapesLobby, location=[821.85, 0, 615.167, 264], placed="wrinkly"),  # Chunky Door
        DoorData(name="Japes: Diddy Cave", map=Maps.JungleJapes, location=[2489.96, 280, 736.892, 179], placed="tns"),  # T&S Door in Diddy Cave
        # DoorData(name="Japes: Near Painting Room", map=Maps.JungleJapes, location=[722.473, 538, 2386.608, 141], placed="tns"),  # T&S Door in Near Painting Room. Omitted because the indicator is weird
        DoorData(name="Japes: Fairy Cave", map=Maps.JungleJapes, location=[901.203, 279, 3795.889, 202], placed="tns"),  # T&S Door in Fairy Cave
    ],
    Levels.AngryAztec: [
        DoorData(name="Aztec Lobby: Pillar Wall", map=Maps.AngryAztecLobby, location=[499.179, 0, 146.628, 0], placed="wrinkly"),  # DK Door
        DoorData(name="Aztec Lobby: Lower Right", map=Maps.AngryAztecLobby, location=[441.456, 0, 614.029, 180], placed="wrinkly"),  # Diddy Door
        DoorData(name="Aztec Lobby: Left of Portal", map=Maps.AngryAztecLobby, location=[628.762, 80, 713.93, 177], placed="wrinkly"),  # Lanky Door
        DoorData(name="Aztec Lobby: Right of Portal", map=Maps.AngryAztecLobby, location=[377.124, 80, 712.484, 179], placed="wrinkly"),  # Tiny Door
        DoorData(name="Aztec Lobby: Behind Feather Door", map=Maps.AngryAztecLobby, location=[1070.018, 0, 738.609, 190], placed="wrinkly"),  # Custom Chunky Door
        DoorData(name="Aztec: Near Funky's", map=Maps.AngryAztec, location=[2801.765, 121.333, 4439.293, 66], placed="tns"), # T&S Portal by Funky
        DoorData(name="Aztec: Near Cranky's", map=Maps.AngryAztec, location=[2787.908, 120, 2674.299, 198], placed="tns"), # T&S Portal by Cranky
        DoorData(name="Aztec: Near Candy's", map=Maps.AngryAztec, location=[2268.343, 120, 448.669, 59], placed="tns"), # T&S Portal by Candy
        DoorData(name="Aztec: Near Snide's", map=Maps.AngryAztec, location=[3573.712, 120, 4456.399, 285], placed="tns"), # T&S Portal by Snide
        DoorData(name="Aztec: Behind 5DT", map=Maps.AngryAztec, location=[1968.329, 180, 3457.189, 244], placed="tns"), # T&S Portal behind 5DT
    ],
    Levels.FranticFactory: [
        DoorData(name="Factory Lobby: Low Left", map=Maps.FranticFactoryLobby, location=[544.362, 0, 660.802, 182], placed="wrinkly"),  # DK Door
        DoorData(name="Factory Lobby: Top Left", map=Maps.FranticFactoryLobby, location=[660.685, 133.5, 660.774, 182], placed="wrinkly"),  # Diddy Door
        DoorData(name="Factory Lobby: Top Center", map=Maps.FranticFactoryLobby, location=[468.047, 85.833, 662.907, 180], placed="wrinkly"),  # Lanky Door
        DoorData(name="Factory Lobby: Top Right", map=Maps.FranticFactoryLobby, location=[275.533, 133.5, 661.908, 180], placed="wrinkly"),  # Tiny Door
        DoorData(name="Factory Lobby: Low Right", map=Maps.FranticFactoryLobby, location=[393.114, 0, 662.562, 182], placed="wrinkly"),  # Chunky Door
        DoorData(name="Factory: Arcade Room", map=Maps.FranticFactory, location=[1778.702, 1106.667, 1220.515, 357], placed="tns"),  # T&S Portal in Arcade Room
        DoorData(name="Factory: Production Room", map=Maps.FranticFactory, location=[381.573, 605, 1032.929, 45], placed="tns"),  # T&S Portal in Production Room
        DoorData(name="Factory: R&D", map=Maps.FranticFactory, location=[3827.127, 1264, 847.458, 222], placed="tns"),  # T&S Portal in R&D
        DoorData(name="Factory: Block Tower", map=Maps.FranticFactory, location=[2259.067, 1126.824, 1614.609, 182], placed="tns"),  # T&S Portal in Block Tower Room
        DoorData(name="Factory: Storage Room", map=Maps.FranticFactory, location=[1176.912, 6.5, 472.114, 1], placed="tns"),  # T&S Portal in Storage Room
    ],
    Levels.GloomyGalleon: [
        DoorData(name="Galleon Lobby: Far Left", map=Maps.GloomyGalleonLobby, location=[1022.133, 139.667, 846.41, 276], placed="wrinkly"),  # DK Door
        DoorData(name="Galleon Lobby: Far Right", map=Maps.GloomyGalleonLobby, location=[345.039, 139.667, 884.162, 92], placed="wrinkly"),  # Diddy Door
        DoorData(name="Galleon Lobby: Close Right", map=Maps.GloomyGalleonLobby, location=[464.68, 159.667, 1069.446, 161], placed="wrinkly"),  # Lanky Door
        DoorData(name="Galleon Lobby: Near DK Portal", map=Maps.GloomyGalleonLobby, location=[582.36, 159.667, 1088.258, 180], placed="wrinkly"),  # Tiny Door
        DoorData(name="Galleon Lobby: Close Left", map=Maps.GloomyGalleonLobby, location=[876.388, 178.667, 1063.828, 192], placed="wrinkly"),  # Chunky Door
        DoorData(name="Galleon: Near Cranky's", map=Maps.GloomyGalleon, location=[3423.707, 1890.471, 3098.15, 243], placed="tns"),  # T&S Door Near Cranky's
        DoorData(name="Galleon: Deep Hole", map=Maps.GloomyGalleon, location=[1975.898, 100, 4498.375, 256], placed="tns"),  # T&S Door in meme hole
        DoorData(name="Galleon: Behind 2DS", map=Maps.GloomyGalleon, location=[803.636, 1053.997, 1955.268, 92], placed="tns"),  # T&S Door behind 2DS
        DoorData(name="Galleon: Behind Enguarde Door", map=Maps.GloomyGalleon, location=[645.832, 1460, 4960.476, 133], placed="tns"),  # T&S Door behind Enguarde Door
        DoorData(name="Galleon: Cactus", map=Maps.GloomyGalleon, location=[4517.923, 1290, 894.527, 308], placed="tns"),  # T&S Door near Cactus
    ],
    Levels.FungiForest: [
        DoorData(name="Fungi Lobby: On High Box", map=Maps.FungiForestLobby, location=[449.866, 45.922, 254.6, 270], placed="wrinkly"),  # Custom Location (Removing Wheel)
        DoorData(name="Fungi Lobby: Near Gorilla Gone Door", map=Maps.FungiForestLobby, location=[136.842, 0, 669.81, 90], placed="wrinkly"),  # Custom Location (Removing Wheel)
        DoorData(name="Fungi Lobby: Opposite Gorilla Gone Door", map=Maps.FungiForestLobby, location=[450.219, 0, 689.048, 270], placed="wrinkly"),  # Custom Location (Removing Wheel)
        DoorData(name="Fungi Lobby: Near B. Locker", map=Maps.FungiForestLobby, location=[293, 0, 154.197, 0], scale=1.2, placed="wrinkly"),  # Custom Location (Removing Wheel)
        DoorData(name="Fungi Lobby: Near Entrance", map=Maps.FungiForestLobby, location=[450.862, 0, 565.029, 270], placed="wrinkly"),  # Custom Location (Removing Wheel)
        DoorData(name="Fungi: Behind DK Barn", map=Maps.FungiForest, location=[3515.885, 115.009, 1248.55, 31], placed="tns"),  # T&S Portal behind DK Barn
        DoorData(name="Fungi: Beanstalk Area", map=Maps.FungiForest, location=[3665.871, 186.833, 945.745, 252], placed="tns"),  # T&S Portal in Beanstalk Area
        DoorData(name="Fungi: Near Snide's", map=Maps.FungiForest, location=[3240.033, 268.5, 3718.017, 178], placed="tns"),  # T&S Portal near Snide's
        DoorData(name="Fungi: Top of Giant Mushroom", map=Maps.FungiForest, location=[1171.791, 1250, 1236.572, 52], placed="tns"),  # T&S Portal at Top of GMush
        DoorData(name="Fungi: Owl Area", map=Maps.FungiForest, location=[203.663, 199.333, 3844.253, 92], placed="tns"),  # T&S Portal near Owl Race
    ],
    Levels.CrystalCaves: [
        DoorData(name="Caves Lobby: Far Left", map=Maps.CrystalCavesLobby, location=[1103.665, 146.5, 823.872, 194], placed="wrinkly"),  # DK Door
        DoorData(name="Caves Lobby: Top Ledge", map=Maps.CrystalCavesLobby, location=[731.84, 280.5, 704.935, 120], kong_lst=[Kongs.diddy], placed="wrinkly"),  # Diddy Door
        DoorData(name="Caves Lobby: Near Left", map=Maps.CrystalCavesLobby, location=[1046.523, 13.5, 476.611, 189], placed="wrinkly"),  # Lanky Door
        DoorData(name="Caves Lobby: Far Right", map=Maps.CrystalCavesLobby, location=[955.407, 146.664, 843.472, 187], placed="wrinkly"),  # Tiny Door
        DoorData(name="Caves Lobby: Near Right", map=Maps.CrystalCavesLobby, location=[881.545, 13.466, 508.666, 193], placed="wrinkly"),  # Chunky Door
        DoorData(name="Caves: On Rotating Room", map=Maps.CrystalCaves, location=[2853.776, 436.949, 2541.475, 207], placed="tns"),  # T&S Portal on Rotating Room
        DoorData(name="Caves: Near Snide's", map=Maps.CrystalCaves, location=[1101.019, 64.5, 467.76, 69], placed="tns"),  # T&S Portal near Snide's
        DoorData(name="Caves: Giant Boulder Room", map=Maps.CrystalCaves, location=[1993.556, 277.108, 2795.365, 193], placed="tns"),  # T&S Portal in Giant Boulder Room
        DoorData(name="Caves: On Sprint Cabin", map=Maps.CrystalCaves, location=[2196.449, 394.167, 1937.031, 93], placed="tns"),  # T&S Portal on Sprint Cabin
        DoorData(name="Caves: Near 5DI", map=Maps.CrystalCaves, location=[120.997, 50.167, 1182.974, 75.146], placed="tns"),  # T&S Portal near 5DI (Custom)
    ],
    Levels.CreepyCastle: [
        DoorData(name="Castle Lobby: Central Pillar (1)", map=Maps.CreepyCastleLobby, location=[499.978, 71.833, 634.25, 240], placed="wrinkly"),  # DK Door
        DoorData(name="Castle Lobby: Central Pillar (2)", map=Maps.CreepyCastleLobby, location=[499.545, 71.833, 725.653, 300], placed="wrinkly"),  # Diddy Door
        DoorData(name="Castle Lobby: Central Pillar (3)", map=Maps.CreepyCastleLobby, location=[661.738, 71.833, 726.433, 60], placed="wrinkly"),  # Lanky Door
        DoorData(name="Castle Lobby: Central Pillar (4)", map=Maps.CreepyCastleLobby, location=[660.732, 71.833, 635.288, 118], placed="wrinkly"),  # Tiny Door
        DoorData(name="Castle Lobby: Central Pillar (5)", map=Maps.CreepyCastleLobby, location=[581.215, 71.833, 588.444, 182], placed="wrinkly"),  # Chunky Door
        DoorData(name="Castle: Near Greenhouse", map=Maps.CreepyCastle, location=[1543.986, 1381.167, 1629.089, 3], placed="tns"),  # T&S Portal by Greenhouse
        DoorData(name="Castle: Small Plateau", map=Maps.CreepyCastle, location=[1759.241, 903.75, 1060.8, 138], placed="tns"),  # T&S Portal by W2
        DoorData(name="Castle: Back of Castle", map=Maps.CreepyCastle, location=[1704.55, 368.026, 1896.767, 4], placed="tns"),  # T&S Portal around back
        DoorData(name="Castle: Near Funky's", map=Maps.CastleLowerCave, location=[1619.429, 200, 313.484, 299], placed="tns"),  # T&S Portal in Crypt Hub
        DoorData(name="Castle: Near Candy's", map=Maps.CastleUpperCave, location=[1025.262, 300, 1960.308, 359], placed="tns"),  # T&S Portal in Dungeon Tunnel
    ],
}
