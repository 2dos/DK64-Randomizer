"""Gets name data for spoiler for Kasplat locations."""

from randomizer.MapsAndExits import Maps


class KasplatLocation:
    """Class which stores name, map id and location for Kasplat location."""

    def __init__(self, name, map_id, vanilla_kong):
        """Initialize with given parameters."""
        self.name = name
        self.map = map_id
        self.location = vanilla_kong


KasplatLocationData = [
    # Japes
    KasplatLocation("Jungle Japes: Left Tunnel (Near)", Maps.JungleJapes, 0),
    KasplatLocation("Jungle Japes: Near Painting Room", Maps.JungleJapes, 1),
    KasplatLocation("Jungle Japes: Near Cranky's Lab", Maps.JungleJapes, 2),
    KasplatLocation("Jungle Japes: Left Tunnel (Far)", Maps.JungleJapes, 3),
    KasplatLocation("Jungle Japes: Underground", Maps.JapesUnderGround, 4),
    # Aztec
    KasplatLocation("Angry Aztec: Sandy Bridge", Maps.AngryAztec, 0),
    KasplatLocation("Angry Aztec: On Tiny Temple", Maps.AngryAztec, 1),
    KasplatLocation("Angry Aztec: Inside Llama Temple", Maps.AztecLlamaTemple, 2),
    KasplatLocation("Angry Aztec: Near Cranky's Lab", Maps.AngryAztec, 3),
    KasplatLocation("Angry Aztec: Inside Chunky's 5-Door Temple", Maps.AztecChunky5DTemple, 4),
    # Factory
    KasplatLocation("Frantic Factory: Top of Production Room", Maps.FranticFactory, 0),
    KasplatLocation("Frantic Factory: Bottom of Production Room", Maps.FranticFactory, 1),
    KasplatLocation("Frantic Factory: Research and Development", Maps.FranticFactory, 2),
    KasplatLocation("Frantic Factory: Storage Room", Maps.FranticFactory, 3),
    KasplatLocation("Frantic Factory: Block Tower Room", Maps.FranticFactory, 4),
    # Galleon
    KasplatLocation("Gloomy Galleon: Gold Tower Room", Maps.GloomyGalleon, 0),
    KasplatLocation("Gloomy Galleon: Lighthouse Area", Maps.GloomyGalleon, 1),
    KasplatLocation("Gloomy Galleon: Cannon Room", Maps.GloomyGalleon, 2),
    KasplatLocation("Gloomy Galleon: Near Cranky's Lab", Maps.GloomyGalleon, 3),
    KasplatLocation("Gloomy Galleon: Near Submarine", Maps.GloomyGalleon, 4),
    # Fungi
    KasplatLocation("Fungi Forest: Near Thorny Barn", Maps.FungiForest, 0),
    KasplatLocation("Fungi Forest: Inside Giant Mushroom", Maps.ForestGiantMushroom, 1),
    KasplatLocation("Fungi Forest: Owl Tree", Maps.FungiForest, 2),
    KasplatLocation("Fungi Forest: Lower Giant Mushroom Exterior", Maps.FungiForest, 3),
    KasplatLocation("Fungi Forest: Upper Giant Mushroom Exterior", Maps.FungiForest, 4),
    # Caves
    KasplatLocation("Crystal Caves: Near Cranky's Lab", Maps.CrystalCaves, 0),
    KasplatLocation("Crystal Caves: Near Funky's Hut", Maps.CrystalCaves, 1),
    KasplatLocation("Crystal Caves: On the large pillar", Maps.CrystalCaves, 2),
    KasplatLocation("Crystal Caves: Near Candy's Music Shop", Maps.CrystalCaves, 3),
    KasplatLocation("Crystal Caves: On the 5-Door Igloo", Maps.CrystalCaves, 4),
    # Castle
    KasplatLocation("Creepy Castle: Inside the Tree", Maps.CastleTree, 0),
    KasplatLocation("Creepy Castle: Inside the Crypt", Maps.CastleLowerCave, 1),
    KasplatLocation("Creepy Castle: Half-way up the castle", Maps.CreepyCastle, 2),
    KasplatLocation("Creepy Castle: Lower Ledge", Maps.CreepyCastle, 3),
    KasplatLocation("Creepy Castle: Near Candy's Music Shop", Maps.CastleUpperCave, 4),
    # Isles
    KasplatLocation("DK Isles: Hideout Helm Lobby", Maps.HideoutHelmLobby, 0),
    KasplatLocation("DK Isles: Creepy Castle Lobby", Maps.CreepyCastleLobby, 1),
    KasplatLocation("DK Isles: Crystal Caves Lobby", Maps.CrystalCavesLobby, 2),
    KasplatLocation("DK Isles: Frantic Factory Lobby", Maps.FranticFactoryLobby, 3),
    KasplatLocation("DK Isles: Gloomy Galleon Lobby", Maps.GloomyGalleonLobby, 4),
]
