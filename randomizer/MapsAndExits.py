from enum import IntEnum

from randomizer.LogicClasses import TransitionBack

class Maps(IntEnum):
    '''List of Maps with in-game index'''

    # DK Isles Regions
    Isles = 34
    BananaFairyRoom = 189
    JungleJapesLobby = 169
    AngryAztecLobby = 173
    IslesSnideRoom = 195
    FranticFactoryLobby = 175
    GloomyGalleonLobby = 174
    FungiForestLobby = 178
    CrystalCavesLobby = 194
    CreepyCastleLobby = 193

    # Jungle Japes Regions
    JungleJapes = 7
    JapesTinyHive = 12
    JapesLankyCave = 13
    JapesMountain = 5
    JapesMinecarts = 6
    JapesUnderGround = 33
    JapesBaboonBlast = 37

    # Angry Aztec Regions
    AngryAztec = 38
    AztecTinyTemple = 16
    AztecDonkey5DTemple = 19
    AztecDiddy5DTemple = 21
    AztecLanky5DTemple = 23
    AztecTiny5DTemple = 22
    AztecChunky5DTemple = 24
    AztecTinyRace = 14
    AztecLlamaTemple = 20
    AztecBaboonBlast = 41

    # Frantic Factory Regions
    FranticFactory = 26
    FactoryTinyRace = 27
    FactoryPowerHut = 29
    FactoryCrusher = 36
    FactoryBaboonBlast = 110

    # Gloomy Galleon Regions
    GloomyGalleon = 30
    GalleonLighthouse = 49
    GalleonMermaidRoom = 45
    GalleonSickBay = 31
    GalleonSealRace = 39
    GalleonTreasureChest = 44
    GalleonSubmarine = 179
    GalleonMechafish = 51
    Galleon5DShipDKTiny = 46
    Galleon5DShipDiddyLankyChunky = 43
    Galleon2DShip = 47
    GalleonBaboonBlast = 54

    # Fungi Forest Regions
    FungiForest = 48
    ForestMinecarts = 55
    ForestGiantMushroom = 64
    ForestChunkyFaceRoom = 71
    ForestLankyZingersRoom = 70
    ForestLankyMushroomsRoom = 63
    ForestAnthill = 52
    ForestMillFront = 61
    ForestMillBack = 62
    ForestSpider = 60
    ForestRafters = 56
    ForestWinchRoom = 57
    ForestMillAttic = 58
    ForestThornvineBarn = 59
    ForestBaboonBlast = 188

    # Crystal Caves Regions
    CrystalCaves = 72
    CavesLankyRace = 82
    CavesFrozenCastle = 98
    CavesDonkeyIgloo = 86
    CavesDiddyIgloo = 100
    CavesLankyIgloo = 85
    CavesTinyIgloo = 84
    CavesChunkyIgloo = 95
    CavesRotatingCabin = 89
    CavesDonkeyCabin = 91
    CavesDiddyLowerCabin = 92
    CavesDiddyUpperCabin = 200
    CavesLankyCabin = 94
    CavesTinyCabin = 93
    CavesChunkyCabin = 90
    CavesBaboonBlast = 186

    # Creepy Castle Regions
    CreepyCastle = 87
    CastleTree = 164
    CastleLibrary = 114
    CastleBallroom = 88
    CastleMuseum = 113
    CastleTinyRace = 185
    CastleTower = 105
    CastleGreenhouse = 168
    CastleTrashCan = 167
    CastleShed = 166
    CastleLowerCave = 183
    CastleCrypt = 112
    CastleMinecarts = 106
    CastleMausoleum = 108
    CastleUpperCave = 151
    CastleDungeon = 163
    CastleBaboonBlast = 187

MapExitTable = {
    Maps.Isles: [
        "From Training Grounds",
        "From K-Lumsy",
        "From Japes Lobby",
        "From Aztec Lobby",
        "From Factory Lobby",
        "From Galleon Lobby",
        "From Fungi Lobby",
        "From Helm Lobby",
        "From Banana Fairy Isle",
        "From Snide's Room",
        "From Caves Lobby",
        "From Castle Lobby",
        "From K Rool",
        "From Training Grounds"
    ],
    Maps.JungleJapes: [
        "From Japes Lobby",
        "From Beehive",
        "From Mountain",
        "From Cranky",
        "From Funky",
        "From Painting Room",
        "From Snide's",
        "From BBlast",
        "From Underground",
        "From T&S (Diddy Cave)",
        "From T&S (Near Cannon)",
        "From ? (Other hill near SSSortie)",
        "From T&S (Near Pool Fairy)",
        "From ? (Near Pool Fairy)",
        "From Minecart",
        "From Japes Lobby",
        "From DK Rap (DKTV Demo)",
        "From Japes Lobby (Intro)"
    ],
    Maps.AngryAztec: [
        "From Aztec Lobby",
        "From Tiny Temple",
        "From Llama Temple",
        "From Tiny 5DTemple",
        "From Chunky 5DTemple",
        "From DK 5DTemple",
        "From Diddy 5DTemple",
        "From Lanky 5DTemple",
        "From Candy's",
        "From Snide's",
        "From Cranky's",
        "From BBlast",
        "From T&S (Candy's)",
        "From T&S (W5)",
        "From T&S (5DTemple)",
        "From T&S (Cranky's)",
        "From T&S (Funky's)",
        "From Beetle Race",
        "From Funky's",
        "From Aztec Lobby"
    ],
    Maps.FranticFactory: [
        "From Factory Lobby",
        "From Arcade Area (near Tiny BP)",
        "From Tiny BP Area (To Arcade Area)",
        "From Power Shed",
        "From R&D Area (To Storage Room)",
        "From Snide's",
        "From Funky's",
        "From Cranky's",
        "From Crusher Room",
        "From T&S (Block Tower)",
        "From T&S (Arcade)",
        "From T&S (R&D)",
        "From T&S (Production Room)",
        "From T&S (Storage Room)",
        "From ? (Near Bad Hit Detection Man)",
        "From BBlast",
        "From Car Race",
        "From Candy's",
        "From Factory Lobby"
    ],
    Maps.GloomyGalleon: [
        "From Galleon Lobby",
        "From Diddy 5DShip",
        "From Chunky 5DShip",
        "From Lanky 5DShip",
        "From Treasure Chest",
        "From Mermaid",
        "From Tiny 5DShip",
        "From Donkey 5DShip",
        "From Tiny 2DShip",
        "From Lanky 2DShip",
        "From Lighthouse",
        "From Seasick Ship",
        "From T&S (Cactus)",
        "From T&S (Near Cranky's)",
        "From T&S (2DShip)",
        "From T&S (Enguarde Door)",
        "From BBlast",
        "From Snide's",
        "From Candy's",
        "From Seal Race",
        "From T&S (Meme Hole)",
        "From Submarine",
        "From Cranky's",
        "From Funky's",
        "From Galleon Lobby"
    ],
    Maps.Galleon5DShipDiddyLankyChunky: [
        "From Galleon (Diddy Entrance)",
        "From Galleon (Chunky Entrance)",
        "From Galleon (Lanky Entrance)",
        "From Galleon (Diddy Entrance)"
    ],
    Maps.Galleon5DShipDKTiny: [
        "From Galleon (DK Entrance)",
        "From Galleon (Tiny Entrance)",
        "From Galleon (DK Entrance)"
    ],
    Maps.Galleon2DShip: [
        "From Galleon (Tiny Entrance)",
        "From Galleon (Lanky Entrance)",
        "From Galleon (Tiny Entrance)"
    ],
    Maps.FungiForest: [
        "From Fungi Lobby",
        "From Mill Attic",
        "From Winch",
        "From Rafters",
        "From Thornvine Barn",
        "From Mill (PPunch Door)",
        "From Mill (Front)",
        "From Mill (Tiny Hole)",
        "From G. Mush (Low)",
        "From G. Mush (Low Middle)",
        "From G. Mush (Middle)",
        "From G. Mush (High Middle)",
        "From G. Mush (High)",
        "From Face Puzzle (Chunky)",
        "From Mushrooms Room (Lanky)",
        "From Zingers Room (Lanky)",
        "From Minecart",
        "From Cranky's",
        "From Funky's",
        "From Snide's",
        "From T&S (DK Barn)",
        "From T&S (Snide's)",
        "From T&S (Beanstalk)",
        "From Anthill",
        "From T&S (G. Mush)",
        "From T&S (Tree)",
        "From BBlast",
        "From Fungi Lobby (?)",
        "From Fungi Lobby"
    ],
    Maps.ForestMillFront: [
        "From Fungi (Front)",
        "From Mill (Rear)",
        "From Fungi (Front)"
    ],
    Maps.ForestMillBack: [
        "From Fungi (PPunch Door)",
        "From Spider Boss",
        "From Mill (Front)",
        "From Fungi (Tiny Hole)",
        "From Fungi (PPunch Door)"
    ],
    Maps.ForestGiantMushroom: [
        "From Fungi (Low)",
        "From Fungi (Middle)",
        "From Fungi (Low Middle)",
        "From Fungi (High Middle)",
        "From Fungi (High)",
        "From Fungi (Low)"
    ],
    Maps.CrystalCaves: [
        "From Caves Lobby",
        "From Diddy 5DIgloo",
        "From DK 5DIgloo",
        "From Lanky 5DIgloo",
        "From Chunky 5DIgloo",
        "From Tiny 5DIgloo",
        "From Beetle Race",
        "From ? (Near Rotating Room)",
        "From ? (Near 1DC)",
        "From ? (Near 5DC)",
        "From ? (Near W3 Room)",
        "From ? (5DIgloo W3, Beta T&S)",
        "From Cranky's",
        "From Funky's",
        "From DK 5DCabin",
        "From Chunky 5DCabin",
        "From Tiny 5DCabin",
        "From Diddy Lower 5DCabin",
        "From Diddy Upper 5DCabin",
        "From Rotating Cabin",
        "From Lanky Cabin",
        "From Candy's",
        "From Snide's",
        "From T&S (Snide's)",
        "From T&S (Rotating Room)",
        "From T&S (1DC)",
        "From T&S (Giant Boulder)",
        "From ? (Behind W3 Room)",
        "From BBlast",
        "From ? (Giant Kosha Room)",
        "From Tile Flipping",
        "From DK Treehouse (Secret Exit)",
        "From Caves Lobby"
    ],
    Maps.CreepyCastle: [
        "From Castle Lobby",
        "From Tree (Exit)",
        "From Tunnel (Front)",
        "From T&S (W2)",
        "From Lower Cave",
        "From Tunnel (Rear)",
        "From T&S (Rear)",
        "From Museum",
        "From Greenhouse (Start)",
        "From Shed",
        "From T&S (W4)",
        "From Ballroom",
        "From Library (Start)",
        "From Library (End)",
        "From Tower",
        "From Tree (Entrance)",
        "From Trash Can",
        "From BBlast",
        "From Cranky's",
        "From Snide's",
        "From Greenhouse (End)",
        "From Castle Lobby (Intro)",
        "From Castle Lobby"
    ],
    Maps.CastleBallroom: [
        "From Castle Main",
        "From Museum (Monkeyport)",
        "From Castle Main"
    ],
    Maps.CastleCrypt: [
        "From Lower Cave",
        "From Minecart",
        "From Lower Cave"
    ],
    Maps.CastleMuseum: [
        "From Castle Main",
        "From Car Race",
        "From Ballroom (Monkeyport)",
        "From Castle Main"
    ],
    Maps.CastleLibrary: [
        "From Castle Main (Start)",
        "From Castle Main (End)",
    ],
    Maps.CastleUpperCave: [
        "From Castle (Front)",
        "From Candy's",
        "From Castle (Rear)",
        "From T&S",
        "From Dungeon",
        "From Castle (Front)"
    ],
    Maps.CastleLowerCave: [
        "From Castle Main",
        "From Funky's",
        "From T&S",
        "From Crypt (DK/Diddy/Chunky)",
        "From Mausoleum (Lanky/Tiny)",
        "From Castle Main"
    ],
    Maps.JungleJapesLobby: [
        "From DK Isles",
        "From Japes",
        "From DK Isles"
    ],
    Maps.AngryAztecLobby: [
        "From DK Isles",
        "From Aztec",
        "From DK Isles"
    ],
    Maps.GloomyGalleonLobby: [
        "From DK Isles",
        "From Galleon",
        "From DK Isles"
    ],
    Maps.FranticFactoryLobby: [
        "From DK Isles",
        "From Factory",
        "From DK Isles"
    ],
    Maps.FungiForestLobby: [
        "From DK Isles",
        "From Fungi",
        "From DK Isles"
    ],
    Maps.CreepyCastleLobby: [
        "From DK Isles",
        "From Castle",
        "From DK Isles"
    ],
    Maps.CrystalCavesLobby: [
        "From DK Isles",
        "From Caves",
        "From DK Isles"
    ],
}

def GetExitId(back:TransitionBack):
    if back.mapId in MapExitTable:
        return MapExitTable[back.mapId].index(back.name)
    else:
        # Default exit number should be zero for all maps that don't have multiple exits
        return 0