"""Stores the data for each potential T&S and Wrinkly door location."""
from randomizer.Lists.MapsAndExits import Maps
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Kongs import Kongs


class DoorData:
    """Stores information about a door location."""

    def __init__(self, *, name="", map=0, location=[0, 0, 0, 0], kong_lst=[Kongs.donkey, Kongs.diddy, Kongs.lanky, Kongs.tiny, Kongs.chunky], 
                tough_spot = False, enabled=False, scale=1):
        """Initialize with provided data."""
        self.name = name
        self.map = map
        self.location = location
        self.kongs = kong_lst
        self.scale = scale
        self.placed = False
        self.assigned_kong = None
        self.tough_spot = tough_spot
        self.enabled = enabled

    def assignDoor(self, kong):
        """Assign door to kong."""
        self.placed = True
        self.assigned_kong = kong


door_locations = {
    Levels.JungleJapes: [
        DoorData(name="Japes Lobby: Middle Right", map=Maps.JungleJapesLobby, location=[169.075, 10.833, 594.613, 90], enabled=True),  # DK Door
        DoorData(name="Japes Lobby: Far Left", map=Maps.JungleJapesLobby, location=[647.565, 0, 791.912, 183], enabled=True),  # Diddy Door
        DoorData(name="Japes Lobby: Close Right", map=Maps.JungleJapesLobby, location=[156.565, 10.833, 494.73, 98], enabled=True),  # Lanky Door
        DoorData(name="Japes Lobby: Far Right", map=Maps.JungleJapesLobby, location=[252.558, 0, 760.733, 163], enabled=True),  # Tiny Door
        DoorData(name="Japes Lobby: Close Left", map=Maps.JungleJapesLobby, location=[821.85, 0, 615.167, 264], enabled=True),  # Chunky Door
    ],
    Levels.AngryAztec: [
        DoorData(name="Aztec Lobby: Pillar Wall", map=Maps.AngryAztecLobby, location=[499.179, 0, 146.628, 0], enabled=True),  # DK Door
        DoorData(name="Aztec Lobby: Lower Right", map=Maps.AngryAztecLobby, location=[441.456, 0, 614.029, 180], enabled=True),  # Diddy Door
        DoorData(name="Aztec Lobby: Left of Portal", map=Maps.AngryAztecLobby, location=[628.762, 80, 713.93, 177], enabled=True),  # Lanky Door
        DoorData(name="Aztec Lobby: Right of Portal", map=Maps.AngryAztecLobby, location=[377.124, 80, 712.484, 179], enabled=True),  # Tiny Door
        DoorData(name="Aztec Lobby: Behind Feather Door", map=Maps.AngryAztecLobby, location=[1070.018, 0, 738.609, 190], enabled=True),  # Custom Chunky Door
        DoorData(name="Next to Candy - right", map=Maps.AngryAztec, location=[2468, 120, 473.5, 298.75]),
    ],
    Levels.FranticFactory: [
        DoorData(name="Factory Lobby: Low Left", map=Maps.FranticFactoryLobby, location=[544.362, 0, 660.802, 182], enabled=True),  # DK Door
        DoorData(name="Factory Lobby: Top Left", map=Maps.FranticFactoryLobby, location=[660.685, 133.5, 660.774, 182], enabled=True),  # Diddy Door
        DoorData(name="Factory Lobby: Top Center", map=Maps.FranticFactoryLobby, location=[468.047, 85.833, 662.907, 180], enabled=True),  # Lanky Door
        DoorData(name="Factory Lobby: Top Right", map=Maps.FranticFactoryLobby, location=[275.533, 133.5, 661.908, 180], enabled=True),  # Tiny Door
        DoorData(name="Factory Lobby: Low Right", map=Maps.FranticFactoryLobby, location=[393.114, 0, 662.562, 182], enabled=True),  # Chunky Door
        DoorData(name="Crusher Room - start", map=Maps.FactoryCrusher, location=[475, 0, 539, 180], enabled=True),
    ],
    Levels.GloomyGalleon: [
        DoorData(name="Galleon Lobby: Far Left", map=Maps.GloomyGalleonLobby, location=[1022.133, 139.667, 846.41, 276], enabled=True),  # DK Door
        DoorData(name="Galleon Lobby: Far Right", map=Maps.GloomyGalleonLobby, location=[345.039, 139.667, 884.162, 92], enabled=True),  # Diddy Door
        DoorData(name="Galleon Lobby: Close Right", map=Maps.GloomyGalleonLobby, location=[464.68, 159.667, 1069.446, 161], enabled=True),  # Lanky Door
        DoorData(name="Galleon Lobby: Near DK Portal", map=Maps.GloomyGalleonLobby, location=[582.36, 159.667, 1088.258, 180], enabled=True),  # Tiny Door
        DoorData(name="Galleon Lobby: Close Left", map=Maps.GloomyGalleonLobby, location=[876.388, 178.667, 1063.828, 192], enabled=True),  # Chunky Door
        DoorData(name="Treasure Chest Exterior", map=Maps.GloomyGalleon, location=[1938, 1440, 524, 330]),
        DoorData(name="Next to Warp 3 in Cranky's Area", map=Maps.GloomyGalleon, location=[3071, 1890, 2838, 0]),
        DoorData(name="In Primate Punch Chest Room - right", map=Maps.GloomyGalleon, location=[3460, 1670, 4001, 180]),
        DoorData(name="Next to Cannonball game", map=Maps.GloomyGalleon, location=[1334, 1610, 2523, 0]),
        DoorData(name="Music Cactus - bottom front left", map=Maps.GloomyGalleon, location=[4239, 1289, 880, 38.31]),
        DoorData(name="Music Cactus - bottom back left", map=Maps.GloomyGalleon, location=[4444, 1290, 803, 307.7]),
        DoorData(name="Music Cactus - bottom front right", map=Maps.GloomyGalleon, location=[4524, 1290, 1145, 218.31]),
        DoorData(name="Music Cactus - bottom back right", map=Maps.GloomyGalleon, location=[4587, 1290, 972, 307.85]),
        DoorData(name="In hallway to Shipyard - Tiny switch", map=Maps.GloomyGalleon, location=[2205, 1620, 2700, 90]),
        DoorData(name="In hallway to Shipyard - Lanky switch", map=Maps.GloomyGalleon, location=[2615, 1620, 2844, 302]),
        DoorData(name="In hallway to Primate Punch Chests", map=Maps.GloomyGalleon, location=[3007, 1670, 3866, 135.42]),
        DoorData(name="Under Baboon Blast pad", map=Maps.GloomyGalleon, location=[1674.5, 1610, 4042.5, 261.15]),
        DoorData(name="Under RocketBarrel barrel", map=Maps.GloomyGalleon, location=[1360, 1609, 4048, 86]),
        DoorData(name="Next to Coconut switch", map=Maps.GloomyGalleon, location=[2065.75, 1628, 3418.75, 28]),
        DoorData(name="Entrance Tunnel - near entrance", map=Maps.GloomyGalleon, location=[2112, 1628, 3223, 135]),
        DoorData(name="Next to Peanut switch", map=Maps.GloomyGalleon, location=[2462, 1619, 2688, 270]),
        DoorData(name="On top of Seal cage", map=Maps.GloomyGalleon, location=[2238, 1837, 4099, 251.7], kong_lst=[Kongs.diddy], tough_spot=True),
    ],
    Levels.FungiForest: [
        DoorData(name="Fungi Lobby: On High Box", map=Maps.FungiForestLobby, location=[449.866, 45.922, 254.6, 270], enabled=True),  # Custom Location (Removing Wheel)
        DoorData(name="Fungi Lobby: Near Gorilla Gone Door", map=Maps.FungiForestLobby, location=[136.842, 0, 669.81, 90], enabled=True),  # Custom Location (Removing Wheel)
        DoorData(name="Fungi Lobby: Opposite Gorilla Gone Door", map=Maps.FungiForestLobby, location=[450.219, 0, 689.048, 270], enabled=True),  # Custom Location (Removing Wheel)
        DoorData(name="Fungi Lobby: Near B. Locker", map=Maps.FungiForestLobby, location=[293, 0, 154.197, 0], enabled=True, scale=1.2),  # Custom Location (Removing Wheel)
        DoorData(name="Fungi Lobby: Near Entrance", map=Maps.FungiForestLobby, location=[450.862, 0, 565.029, 270], enabled=True),  # Custom Location (Removing Wheel)
    ],
    Levels.CrystalCaves: [
        DoorData(name="Caves Lobby: Far Left", map=Maps.CrystalCavesLobby, location=[1103.665, 146.5, 823.872, 194], enabled=True),  # DK Door
        DoorData(name="Caves Lobby: Top Ledge", map=Maps.CrystalCavesLobby, location=[731.84, 280.5, 704.935, 120], enabled=True, kong_lst=[Kongs.diddy]),  # Diddy Door
        DoorData(name="Caves Lobby: Near Left", map=Maps.CrystalCavesLobby, location=[1046.523, 13.5, 476.611, 189], enabled=True),  # Lanky Door
        DoorData(name="Caves Lobby: Far Right", map=Maps.CrystalCavesLobby, location=[955.407, 146.664, 843.472, 187], enabled=True),  # Tiny Door
        DoorData(name="Caves Lobby: Near Right", map=Maps.CrystalCavesLobby, location=[881.545, 13.466, 508.666, 193], enabled=True),  # Chunky Door
    ],
    Levels.CreepyCastle: [
        DoorData(name="Castle Lobby: Central Pillar (1)", map=Maps.CreepyCastleLobby, location=[499.978, 71.833, 634.25, 240], enabled=True),  # DK Door
        DoorData(name="Castle Lobby: Central Pillar (2)", map=Maps.CreepyCastleLobby, location=[499.545, 71.833, 725.653, 300], enabled=True),  # Diddy Door
        DoorData(name="Castle Lobby: Central Pillar (3)", map=Maps.CreepyCastleLobby, location=[661.738, 71.833, 726.433, 60], enabled=True),  # Lanky Door
        DoorData(name="Castle Lobby: Central Pillar (4)", map=Maps.CreepyCastleLobby, location=[660.732, 71.833, 635.288, 118], enabled=True),  # Tiny Door
        DoorData(name="Castle Lobby: Central Pillar (5)", map=Maps.CreepyCastleLobby, location=[581.215, 71.833, 588.444, 182], enabled=True),  # Chunky Door
    ],
}
