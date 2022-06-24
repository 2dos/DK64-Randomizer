"""Designates Dirt Patch Location Properties."""

from randomizer.Lists.MapsAndExits import Maps


class DirtPatchData:
    """Information about the dirt patch location."""

    def __init__(self, *, name="", map_id=0, vanilla=False, x=0, y=0, z=0, rotation=0, logic=0):
        """Initialize with given parameters."""
        self.name = name
        self.map_id = map_id
        self.vanilla = vanilla
        self.x = x
        self.y = y
        self.z = z
        self.rotation = rotation
        self.logic = logic
        self.selected = vanilla

    def setPatch(self, used):
        """Set patch's state regarding rando."""
        self.selected = used


DirtPatchLocations = [
    DirtPatchData(name="DK Isles: On Aztec Building", map_id=Maps.Isles, x=3509.673, y=1170.0, z=1733.509, rotation=1784, vanilla=True),
    DirtPatchData(name="DK Isles: Under Caves Lobby Entrance", map_id=Maps.Isles, x=2401.601, y=800.0, z=1571.532, rotation=4028, vanilla=True),
    DirtPatchData(name="DK Isles: Front of Fungi Building", map_id=Maps.Isles, x=2647.643, y=1498.0, z=929.797, rotation=748, vanilla=True),
    DirtPatchData(name="DK Isles - Training Grounds: Banana Hoard", map_id=Maps.TrainingGrounds, x=2497.648, y=191.0, z=1036.583, rotation=0, vanilla=True),
    DirtPatchData(name="DK Isles - Training Grounds: Rear Inside Tunnel", map_id=Maps.TrainingGrounds, x=1123.714, y=37.208, z=2200.538, rotation=1002, vanilla=True),
    DirtPatchData(name="DK Isles - K Lumsy: Inside K. Lumsy's Cage", map_id=Maps.KLumsy, x=1499.675, y=95.0, z=1233.831, rotation=2736, vanilla=True),
    DirtPatchData(name="DK Isles - Creepy Castle Lobby: Castle Lobby", map_id=Maps.CreepyCastleLobby, x=579.809, y=245.5, z=681.709, rotation=2074, vanilla=True),
    DirtPatchData(name="DK Isles: Isles Boulders", map_id=Maps.Isles, x=2813.0, y=1058.0, z=2054.0, rotation=3959),
    DirtPatchData(name="DK Isles: Behind BFI", map_id=Maps.Isles, x=754.0, y=500.0, z=2386.0, rotation=807),
    DirtPatchData(name="DK Isles: Back of Kroc Isle (Lower)", map_id=Maps.Isles, x=2019.0, y=590.0, z=4146.0, rotation=1615),
    DirtPatchData(name="DK Isles: Back of Kroc Isle (Middle)", map_id=Maps.Isles, x=2350.0, y=1199.0, z=3887.0, rotation=1956),
    DirtPatchData(name="DK Isles: Kroc Isle Left Arm", map_id=Maps.Isles, x=2313.0, y=1620.0, z=3214.0, rotation=3891),
    DirtPatchData(name="DK Isles: In Fungi Boulder", map_id=Maps.Isles, x=3516.0, y=500.0, z=633.0, rotation=1934),
    DirtPatchData(name="DK Isles: Behind Fungi Building", map_id=Maps.Isles, x=2436.0, y=1498.0, z=817.0, rotation=637),
    DirtPatchData(name="DK Isles: Behind Aztec Building", map_id=Maps.Isles, x=3643.0, y=1020.0, z=1790.0, rotation=2742),
    DirtPatchData(name="DK Isles - Banana Fairy Room: Behind Fairy Chair", map_id=Maps.BananaFairyRoom, x=835.0, y=37.0, z=563.0, rotation=1080),
    DirtPatchData(name="DK Isles - Banana Fairy Room: Behind the Rareware Door", map_id=Maps.BananaFairyRoom, x=644.0, y=37.0, z=1085.0, rotation=2048),
    DirtPatchData(name="DK Isles - K Lumsy: Under K. Lumsy", map_id=Maps.KLumsy, x=1020.0, y=50.0, z=1001.0, rotation=682),
    DirtPatchData(name="DK Isles - Hideout Helm Lobby: Bonus Barrel Platform", map_id=Maps.HideoutHelmLobby, x=683.0, y=196.0, z=638.0, rotation=1024),
    DirtPatchData(name="DK Isles - Hideout Helm Lobby: Blueprint Platform", map_id=Maps.HideoutHelmLobby, x=325.0, y=191.0, z=643.0, rotation=0),
    DirtPatchData(name="DK Isles - Jungle Japes Lobby: Near Tag Barrel", map_id=Maps.JungleJapesLobby, x=713.0, y=4.0, z=266.0, rotation=1945),
    DirtPatchData(name="DK Isles - Angry Aztec Lobby: Behind Feather Door", map_id=Maps.AngryAztecLobby, x=1128.0, y=0.0, z=586.0, rotation=694),
    DirtPatchData(name="DK Isles - Frantic Factory Lobby: High Platform", map_id=Maps.FranticFactoryLobby, x=674.0, y=133.0, z=376.0, rotation=1024),
    DirtPatchData(name="DK Isles - Gloomy Galleon Lobby: Behind Mini Monkey Gate", map_id=Maps.GloomyGalleonLobby, x=838.0, y=99.0, z=232.0, rotation=978),
    DirtPatchData(name="DK Isles - Fungi Forest Lobby: Behind Gorilla Gone Door", map_id=Maps.FungiForestLobby, x=99.0, y=4.0, z=533.0, rotation=1024),
    DirtPatchData(name="DK Isles - Fungi Forest Lobby: On Tag Crate", map_id=Maps.FungiForestLobby, x=436.0, y=46.0, z=252.0, rotation=1024),
    DirtPatchData(name="DK Isles - Crystal Caves Lobby: On the Lava", map_id=Maps.CrystalCavesLobby, x=387.0, y=2.0, z=207.0, rotation=785),
    DirtPatchData(name="DK Isles - Creepy Castle Lobby: Behind the entrance", map_id=Maps.CreepyCastleLobby, x=577.0, y=60.0, z=67.0, rotation=773),
    DirtPatchData(name="DK Isles - Isles Snide Room: Next to Snides", map_id=Maps.IslesSnideRoom, x=576.0, y=0.0, z=450.0, rotation=341),
    DirtPatchData(name="DK Isles - Training Grounds: On the entrance hill", map_id=Maps.TrainingGrounds, x=1108.0, y=220.0, z=701.0, rotation=3026),
    DirtPatchData(name="DK Isles - Training Grounds: On the rear hill", map_id=Maps.TrainingGrounds, x=1086.0, y=252.0, z=1833.0, rotation=489),
    DirtPatchData(name="DK Isles - Treehouse: Back of the treehouse", map_id=Maps.Treehouse, x=288.0, y=85.0, z=488.0, rotation=3072),
    DirtPatchData(name="Jungle Japes: On Painting Hill", map_id=Maps.JungleJapes, x=550.814, y=370.167, z=1873.436, rotation=1070, vanilla=True),
    DirtPatchData(name="Jungle Japes: Inside Diddy's Cavern", map_id=Maps.JungleJapes, x=2475.0, y=280.0, z=508.0, rotation=2427),
    DirtPatchData(name="Jungle Japes - Japes Mountain: On a Barrel", map_id=Maps.JapesMountain, x=691.0, y=135.0, z=753.0, rotation=4061),
    DirtPatchData(name="Jungle Japes: Minecart Exit", map_id=Maps.JungleJapes, x=1108.0, y=288.0, z=1970.0, rotation=659),
    DirtPatchData(name="Jungle Japes: Under Chunky's Barrel", map_id=Maps.JungleJapes, x=2345.0, y=551.0, z=3152.0, rotation=3208),
    DirtPatchData(name="Angry Aztec: Oasis", map_id=Maps.AngryAztec, x=2426.34, y=115.5, z=960.642, rotation=2618, vanilla=True),
    DirtPatchData(name="Angry Aztec - Aztec Chunky5D Temple: Chunky 5DT", map_id=Maps.AztecChunky5DTemple, x=652.778, y=85.0, z=1544.845, rotation=1036, vanilla=True),
    DirtPatchData(name="Angry Aztec: Behind Chunky Cage", map_id=Maps.AngryAztec, x=4395.0, y=120.0, z=2409.0, rotation=944),
    DirtPatchData(name="Frantic Factory: Dark Room", map_id=Maps.FranticFactory, x=1850.584, y=6.5, z=666.077, rotation=3110, vanilla=True),
    DirtPatchData(name="Frantic Factory: Toy Room Under Stairs", map_id=Maps.FranticFactory, x=2015.0, y=1026.0, z=1364.0, rotation=3026),
    DirtPatchData(name="Gloomy Galleon - Galleon Lighthouse: Interior Rear", map_id=Maps.GalleonLighthouse, x=457.54, y=0.0, z=716.299, rotation=18, vanilla=True),
    DirtPatchData(name="Gloomy Galleon: Outside Cranky", map_id=Maps.GloomyGalleon, x=3068.0, y=1790.0, z=3386.0, rotation=1092),
    DirtPatchData(name="Gloomy Galleon: Behind the shipwreck near Cranky", map_id=Maps.GloomyGalleon, x=3210.0, y=1670.0, z=3429.0, rotation=79),
    DirtPatchData(name="Fungi Forest: Beanstalk", map_id=Maps.FungiForest, x=2279.848, y=228.931, z=600.56, rotation=1020, vanilla=True),
    DirtPatchData(name="Fungi Forest: Mill Grass", map_id=Maps.FungiForest, x=4674.706, y=149.873, z=4165.153, rotation=2584, vanilla=True),
    DirtPatchData(name="Fungi Forest: Top of Owl Tree", map_id=Maps.FungiForest, x=1268.0, y=575.0, z=3840.0, rotation=34),
    DirtPatchData(name="Fungi Forest: Near BBlast", map_id=Maps.FungiForest, x=752.0, y=589.0, z=1296.0, rotation=534),
    DirtPatchData(name="Crystal Caves: Giant Kosha Room", map_id=Maps.CrystalCaves, x=1820.313, y=231.833, z=3596.593, rotation=2006, vanilla=True),
    DirtPatchData(name="Crystal Caves: Near 1DC", map_id=Maps.CrystalCaves, x=2735.0, y=162.0, z=1795.0, rotation=2127),
    DirtPatchData(name="Creepy Castle: Top of Castle near shop", map_id=Maps.CreepyCastle, x=655.9, y=1794.167, z=1386.9, rotation=3094, vanilla=True),
    DirtPatchData(name="Creepy Castle: Catacombs Door", map_id=Maps.CreepyCastle, x=1319.0, y=523.0, z=1885.0, rotation=3151),
    DirtPatchData(name="Creepy Castle: Upper Gravestone", map_id=Maps.CreepyCastle, x=746.0, y=521.0, z=1873.0, rotation=3280),
    DirtPatchData(name="Creepy Castle: Top of Castle near fence", map_id=Maps.CreepyCastle, x=1696.0, y=1731.0, z=1384.0, rotation=1479),
    DirtPatchData(name="Creepy Castle - Castle Ballroom: Back Left", map_id=Maps.CastleBallroom, x=261.0, y=40.0, z=241.0, rotation=2594),
    DirtPatchData(name="Creepy Castle - Castle Ballroom: Back Right", map_id=Maps.CastleBallroom, x=825.0, y=40.0, z=258.0, rotation=1262),
    DirtPatchData(name="Creepy Castle - Castle Museum: Pillar Front", map_id=Maps.CastleMuseum, x=1003.0, y=200.0, z=1513.0, rotation=921),
    DirtPatchData(name="Creepy Castle - Castle Museum: Pillar Back Right", map_id=Maps.CastleMuseum, x=1238.0, y=200.0, z=1612.0, rotation=580),
    DirtPatchData(name="Creepy Castle - Castle Museum: Pillar Back Left", map_id=Maps.CastleMuseum, x=1236.0, y=200.0, z=1400.0, rotation=1649),
]
