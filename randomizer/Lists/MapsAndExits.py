"""List of maps with in-game index."""
from enum import IntEnum

from randomizer.Enums.Levels import Levels
from randomizer.LogicClasses import Regions, TransitionBack


class Maps(IntEnum):
    """List of Maps with in-game index."""

    # DK Isles
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
    HideoutHelmLobby = 170
    TrainingGrounds = 176
    Treehouse = 171
    KLumsy = 97

    # Jungle Japes
    JungleJapes = 7
    JapesTinyHive = 12
    JapesLankyCave = 13
    JapesMountain = 4
    JapesMinecarts = 6
    JapesUnderGround = 33
    JapesBaboonBlast = 37

    # Angry Aztec
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

    # Frantic Factory
    FranticFactory = 26
    FactoryTinyRace = 27
    FactoryPowerHut = 29
    FactoryCrusher = 36
    FactoryBaboonBlast = 110

    # Gloomy Galleon
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

    # Fungi Forest
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

    # Crystal Caves
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

    # Creepy Castle
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

    # Hideout Helm
    HideoutHelm = 17

    # Level Bosses
    JapesBoss = 8
    AztecBoss = 197
    FactoryBoss = 154
    GalleonBoss = 111
    FungiBoss = 83
    CavesBoss = 196
    CastleBoss = 199

    # K rool phases
    KroolDonkeyPhase = 203
    KroolDiddyPhase = 204
    KroolLankyPhase = 205
    KroolTinyPhase = 206
    KroolChunkyPhase = 207

    # Bonus Barrels
    BattyBarrelBanditVEasy = 32
    BattyBarrelBanditEasy = 121
    BattyBarrelBanditNormal = 122
    BattyBarrelBanditHard = 123
    BigBugBashVEasy = 102
    BigBugBashEasy = 148
    BigBugBashNormal = 149
    BigBugBashHard = 150
    BusyBarrelBarrageEasy = 78
    BusyBarrelBarrageNormal = 79
    BusyBarrelBarrageHard = 131
    MadMazeMaulEasy = 68
    MadMazeMaulNormal = 69
    MadMazeMaulHard = 66
    MadMazeMaulInsane = 124
    MinecartMayhemEasy = 77
    MinecartMayhemNormal = 129
    MinecartMayhemHard = 130
    BeaverBotherEasy = 104
    BeaverBotherNormal = 136
    BeaverBotherHard = 137
    TeeteringTurtleTroubleVEasy = 18
    TeeteringTurtleTroubleEasy = 118
    TeeteringTurtleTroubleNormal = 119
    TeeteringTurtleTroubleHard = 120
    StealthySnoopVEasy = 126
    StealthySnoopEasy = 127
    StealthySnoopNormal = 65
    StealthySnoopHard = 128
    StashSnatchEasy = 74
    StashSnatchNormal = 67
    StashSnatchHard = 75
    StashSnatchInsane = 125
    SplishSplashSalvageEasy = 133
    SplishSplashSalvageNormal = 96
    SplishSplashSalvageHard = 132
    SpeedySwingSortieEasy = 99
    SpeedySwingSortieNormal = 134
    SpeedySwingSortieHard = 135
    KrazyKongKlamourEasy = 101
    KrazyKongKlamourNormal = 141
    KrazyKongKlamourHard = 142
    KrazyKongKlamourInsane = 143
    SearchlightSeekVEasy = 103
    SearchlightSeekEasy = 138
    SearchlightSeekNormal = 139
    SearchlightSeekHard = 140
    KremlingKoshVEasy = 10
    KremlingKoshEasy = 115
    KremlingKoshNormal = 116
    KremlingKoshHard = 117
    PerilPathPanicVEasy = 144
    PerilPathPanicEasy = 145
    PerilPathPanicNormal = 146
    PerilPathPanicHard = 147
    HelmBarrelDKTarget = 35
    HelmBarrelDKRambi = 212
    HelmBarrelDiddyKremling = 165
    HelmBarrelDiddyRocketbarrel = 201
    HelmBarrelLankyMaze = 3
    HelmBarrelLankyShooting = 202
    HelmBarrelTinyPTT = 210
    HelmBarrelTinyMush = 50
    HelmBarrelChunkyHidden = 209
    HelmBarrelChunkyShooting = 211

    # Crowns
    JapesCrown = 53
    AztecCrown = 73
    FactoryCrown = 155
    GalleonCrown = 156
    ForestCrown = 159
    CavesCrown = 160
    CastleCrown = 161
    HelmCrown = 162
    SnidesCrown = 158
    LobbyCrown = 157

    # Shops
    Cranky = 5
    Candy = 25
    Funky = 1
    Snide = 15


RegionMapList = {
    # Isles
    Regions.Treehouse: Maps.Treehouse,
    Regions.TrainingGrounds: Maps.TrainingGrounds,
    Regions.IslesMain: Maps.Isles,
    Regions.IslesMainUpper: Maps.Isles,
    Regions.KremIsle: Maps.Isles,
    Regions.KremIsleBeyondLift: Maps.Isles,
    Regions.KremIsleTopLevel: Maps.Isles,
    Regions.IslesSnideRoom: Maps.IslesSnideRoom,
    Regions.CabinIsle: Maps.Isles,
    Regions.BananaFairyRoom: Maps.BananaFairyRoom,
    Regions.JungleJapesLobby: Maps.JungleJapesLobby,
    Regions.AngryAztecLobby: Maps.AngryAztecLobby,
    Regions.FranticFactoryLobby: Maps.FranticFactoryLobby,
    Regions.GloomyGalleonLobby: Maps.GloomyGalleonLobby,
    Regions.GloomyGalleonLobbyEntrance: Maps.GloomyGalleonLobby,
    Regions.FungiForestLobby: Maps.FungiForestLobby,
    Regions.CrystalCavesLobby: Maps.CrystalCavesLobby,
    Regions.CreepyCastleLobby: Maps.CreepyCastleLobby,
    # Japes
    Regions.JungleJapesStart: Maps.JungleJapes,
    Regions.JungleJapesMain: Maps.JungleJapes,
    Regions.JapesBeyondCoconutGate1: Maps.JungleJapes,
    Regions.JapesBeyondCoconutGate2: Maps.JungleJapes,
    Regions.JapesBeyondPeanutGate: Maps.JungleJapes,
    Regions.JapesBeyondFeatherGate: Maps.JungleJapes,
    Regions.TinyHive: Maps.JapesTinyHive,
    Regions.BeyondRambiGate: Maps.JungleJapes,
    Regions.JapesLankyCave: Maps.JapesLankyCave,
    Regions.Mine: Maps.JapesMountain,
    Regions.JapesMinecarts: Maps.JapesMinecarts,
    Regions.JapesCatacomb: Maps.JapesUnderGround,
    Regions.JapesBaboonBlast: Maps.JapesBaboonBlast,
    # Aztec
    Regions.AngryAztecStart: Maps.AngryAztec,
    Regions.BetweenVinesByPortal: Maps.AngryAztec,
    Regions.AngryAztecOasis: Maps.AngryAztec,
    Regions.TempleStart: Maps.AztecTinyTemple,
    Regions.TempleUnderwater: Maps.AztecTinyTemple,
    Regions.AngryAztecMain: Maps.AngryAztec,
    Regions.DonkeyTemple: Maps.AztecDonkey5DTemple,
    Regions.DiddyTemple: Maps.AztecDiddy5DTemple,
    Regions.LankyTemple: Maps.AztecLanky5DTemple,
    Regions.TinyTemple: Maps.AztecTiny5DTemple,
    Regions.ChunkyTemple: Maps.AztecChunky5DTemple,
    Regions.AztecTinyRace: Maps.AztecTinyRace,
    Regions.LlamaTemple: Maps.AztecLlamaTemple,
    Regions.LlamaTempleBack: Maps.AztecLlamaTemple,
    Regions.AztecBaboonBlast: Maps.AztecBaboonBlast,
    # Factory
    Regions.FranticFactoryStart: Maps.FranticFactory,
    Regions.Testing: Maps.FranticFactory,
    Regions.RandD: Maps.FranticFactory,
    Regions.FactoryTinyRaceLobby: Maps.FranticFactory,
    Regions.FactoryTinyRace: Maps.FactoryTinyRace,
    Regions.ChunkyRoomPlatform: Maps.FranticFactory,
    Regions.PowerHut: Maps.FactoryPowerHut,
    Regions.BeyondHatch: Maps.FranticFactory,
    Regions.InsideCore: Maps.FactoryCrusher,
    Regions.MiddleCore: Maps.FranticFactory,
    Regions.UpperCore: Maps.FranticFactory,
    Regions.FactoryBaboonBlast: Maps.FactoryBaboonBlast,
    # Galleon
    Regions.GloomyGalleonStart: Maps.GloomyGalleon,
    Regions.GalleonPastVines: Maps.GloomyGalleon,
    Regions.GalleonBeyondPineappleGate: Maps.GloomyGalleon,
    Regions.LighthouseSurface: Maps.GloomyGalleon,
    Regions.LighthousePlatform: Maps.GloomyGalleon,
    Regions.LighthouseUnderwater: Maps.GloomyGalleon,
    Regions.LighthouseSnideAlcove: Maps.GloomyGalleon,
    Regions.Lighthouse: Maps.GalleonLighthouse,
    Regions.MermaidRoom: Maps.GalleonMermaidRoom,
    Regions.SickBay: Maps.GalleonSickBay,
    Regions.Shipyard: Maps.GloomyGalleon,
    Regions.SealRace: Maps.GalleonSealRace,
    Regions.TreasureRoom: Maps.GloomyGalleon,
    Regions.TinyChest: Maps.GalleonTreasureChest,
    Regions.Submarine: Maps.GalleonSubmarine,
    Regions.Mechafish: Maps.GalleonMechafish,
    Regions.LankyShip: Maps.Galleon2DShip,
    Regions.TinyShip: Maps.Galleon2DShip,
    Regions.BongosShip: Maps.Galleon5DShipDKTiny,
    Regions.SaxophoneShip: Maps.Galleon5DShipDKTiny,
    Regions.GuitarShip: Maps.Galleon5DShipDiddyLankyChunky,
    Regions.TromboneShip: Maps.Galleon5DShipDiddyLankyChunky,
    Regions.TriangleShip: Maps.Galleon5DShipDiddyLankyChunky,
    Regions.GalleonBaboonBlast: Maps.GalleonBaboonBlast,
    # Fungi
    Regions.FungiForestStart: Maps.FungiForest,
    Regions.ForestMinecarts: Maps.ForestMinecarts,
    Regions.GiantMushroomArea: Maps.FungiForest,
    Regions.MushroomLower: Maps.ForestGiantMushroom,
    Regions.MushroomLowerExterior: Maps.FungiForest,
    Regions.MushroomUpper: Maps.ForestGiantMushroom,
    Regions.MushroomNightDoor: Maps.ForestGiantMushroom,
    Regions.MushroomNightExterior: Maps.FungiForest,
    Regions.MushroomUpperExterior: Maps.FungiForest,
    Regions.MushroomChunkyRoom: Maps.ForestChunkyFaceRoom,
    Regions.MushroomLankyMushroomsRoom: Maps.ForestLankyMushroomsRoom,
    Regions.MushroomLankyZingersRoom: Maps.ForestLankyZingersRoom,
    Regions.HollowTreeArea: Maps.FungiForest,
    Regions.Anthill: Maps.ForestAnthill,
    Regions.MillArea: Maps.FungiForest,
    Regions.MillChunkyTinyArea: Maps.ForestMillBack,
    Regions.SpiderRoom: Maps.ForestSpider,
    Regions.GrinderRoom: Maps.ForestMillFront,
    Regions.MillRafters: Maps.ForestRafters,
    Regions.WinchRoom: Maps.ForestWinchRoom,
    Regions.MillAttic: Maps.ForestMillAttic,
    Regions.ThornvineArea: Maps.FungiForest,
    Regions.ThornvineBarn: Maps.ForestThornvineBarn,
    Regions.WormArea: Maps.FungiForest,
    Regions.ForestBaboonBlast: Maps.ForestBaboonBlast,
    # Caves
    Regions.CrystalCavesMain: Maps.CrystalCaves,
    Regions.BoulderCave: Maps.CrystalCaves,
    Regions.CavesLankyRace: Maps.CavesLankyRace,
    Regions.FrozenCastle: Maps.CavesFrozenCastle,
    Regions.IglooArea: Maps.CrystalCaves,
    Regions.GiantKosha: Maps.CrystalCaves,
    Regions.DonkeyIgloo: Maps.CavesDonkeyIgloo,
    Regions.DiddyIgloo: Maps.CavesDiddyIgloo,
    Regions.LankyIgloo: Maps.CavesLankyIgloo,
    Regions.TinyIgloo: Maps.CavesTinyIgloo,
    Regions.ChunkyIgloo: Maps.CavesChunkyIgloo,
    Regions.CabinArea: Maps.CrystalCaves,
    Regions.RotatingCabin: Maps.CavesRotatingCabin,
    Regions.DonkeyCabin: Maps.CavesDonkeyCabin,
    Regions.DiddyLowerCabin: Maps.CavesDiddyLowerCabin,
    Regions.DiddyUpperCabin: Maps.CavesDiddyUpperCabin,
    Regions.LankyCabin: Maps.CavesLankyCabin,
    Regions.TinyCabin: Maps.CavesTinyCabin,
    Regions.ChunkyCabin: Maps.CavesChunkyCabin,
    Regions.CavesBaboonBlast: Maps.CavesBaboonBlast,
    # Castle
    Regions.CreepyCastleMain: Maps.CreepyCastle,
    Regions.CastleWaterfall: Maps.CreepyCastle,
    Regions.CastleTree: Maps.CastleTree,
    Regions.Library: Maps.CastleLibrary,
    Regions.Ballroom: Maps.CastleBallroom,
    Regions.MuseumBehindGlass: Maps.CastleMuseum,
    Regions.CastleTinyRace: Maps.CastleTinyRace,
    Regions.Tower: Maps.CastleTower,
    Regions.Greenhouse: Maps.CastleGreenhouse,
    Regions.TrashCan: Maps.CastleTrashCan,
    Regions.Shed: Maps.CastleShed,
    Regions.Museum: Maps.CastleMuseum,
    Regions.LowerCave: Maps.CastleLowerCave,
    Regions.Crypt: Maps.CastleCrypt,
    Regions.CastleMinecarts: Maps.CastleMinecarts,
    Regions.Mausoleum: Maps.CastleMausoleum,
    Regions.UpperCave: Maps.CastleUpperCave,
    Regions.Dungeon: Maps.CastleDungeon,
    Regions.CastleBaboonBlast: Maps.CastleBaboonBlast,
}

LevelMapTable = {
    Levels.JungleJapes: [Maps.JungleJapes, Maps.JapesTinyHive, Maps.JapesLankyCave, Maps.JapesMountain, Maps.JapesMinecarts, Maps.JapesUnderGround, Maps.JapesBaboonBlast],
    Levels.AngryAztec: [
        Maps.AngryAztec,
        Maps.AztecTinyTemple,
        Maps.AztecDonkey5DTemple,
        Maps.AztecDiddy5DTemple,
        Maps.AztecLanky5DTemple,
        Maps.AztecTiny5DTemple,
        Maps.AztecChunky5DTemple,
        Maps.AztecTinyRace,
        Maps.AztecLlamaTemple,
        Maps.AztecBaboonBlast,
    ],
    Levels.FranticFactory: [Maps.FranticFactory, Maps.FactoryTinyRace, Maps.FactoryPowerHut, Maps.FactoryCrusher, Maps.FactoryBaboonBlast],
    Levels.GloomyGalleon: [
        Maps.GloomyGalleon,
        Maps.GalleonLighthouse,
        Maps.GalleonMermaidRoom,
        Maps.GalleonSickBay,
        Maps.GalleonSealRace,
        Maps.GalleonTreasureChest,
        Maps.GalleonSubmarine,
        Maps.GalleonMechafish,
        Maps.Galleon5DShipDKTiny,
        Maps.Galleon5DShipDiddyLankyChunky,
        Maps.Galleon2DShip,
        Maps.GalleonBaboonBlast,
    ],
    Levels.FungiForest: [
        Maps.FungiForest,
        Maps.ForestMinecarts,
        Maps.ForestGiantMushroom,
        Maps.ForestChunkyFaceRoom,
        Maps.ForestLankyZingersRoom,
        Maps.ForestLankyMushroomsRoom,
        Maps.ForestAnthill,
        Maps.ForestMillFront,
        Maps.ForestMillBack,
        Maps.ForestSpider,
        Maps.ForestRafters,
        Maps.ForestWinchRoom,
        Maps.ForestMillAttic,
        Maps.ForestThornvineBarn,
        Maps.ForestBaboonBlast,
    ],
    Levels.CrystalCaves: [
        Maps.CrystalCaves,
        Maps.CavesLankyRace,
        Maps.CavesFrozenCastle,
        Maps.CavesDonkeyIgloo,
        Maps.CavesDiddyIgloo,
        Maps.CavesLankyIgloo,
        Maps.CavesTinyIgloo,
        Maps.CavesChunkyIgloo,
        Maps.CavesRotatingCabin,
        Maps.CavesDonkeyCabin,
        Maps.CavesDiddyLowerCabin,
        Maps.CavesDiddyUpperCabin,
        Maps.CavesLankyCabin,
        Maps.CavesTinyCabin,
        Maps.CavesChunkyCabin,
        Maps.CavesBaboonBlast,
    ],
    Levels.CreepyCastle: [
        Maps.CreepyCastle,
        Maps.CastleTree,
        Maps.CastleLibrary,
        Maps.CastleBallroom,
        Maps.CastleMuseum,
        Maps.CastleTinyRace,
        Maps.CastleTower,
        Maps.CastleGreenhouse,
        Maps.CastleTrashCan,
        Maps.CastleShed,
        Maps.CastleLowerCave,
        Maps.CastleCrypt,
        Maps.CastleMinecarts,
        Maps.CastleMausoleum,
        Maps.CastleUpperCave,
        Maps.CastleDungeon,
        Maps.CastleBaboonBlast,
    ],
    Levels.DKIsles: [
        Maps.Isles,
        Maps.BananaFairyRoom,
        Maps.JungleJapesLobby,
        Maps.AngryAztecLobby,
        Maps.IslesSnideRoom,
        Maps.FranticFactoryLobby,
        Maps.GloomyGalleonLobby,
        Maps.FungiForestLobby,
        Maps.CrystalCavesLobby,
        Maps.CreepyCastleLobby,
        Maps.HideoutHelmLobby,
        Maps.TrainingGrounds,
        Maps.Treehouse,
        Maps.KLumsy,
    ],
    Levels.HideoutHelm: [Maps.HideoutHelm],
}


def getLevelFromMap(map_enum):
    """Get level from map index referencing lookup table."""
    for level in LevelMapTable:
        if map_enum in LevelMapTable[level]:
            return level
    return None


MapExitTable = {
    Maps.TrainingGrounds: ["From DK Isles", "From Treehouse"],
    Maps.Treehouse: ["Test Cutscene", "From Training Grounds"],
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
        "From Training Grounds",
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
        "From Japes Lobby (Intro)",
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
        "From Aztec Lobby",
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
        "From Factory Lobby",
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
        "From Galleon Lobby",
    ],
    Maps.Galleon5DShipDiddyLankyChunky: ["From Galleon (Diddy Entrance)", "From Galleon (Chunky Entrance)", "From Galleon (Lanky Entrance)", "From Galleon (Diddy Entrance)"],
    Maps.Galleon5DShipDKTiny: ["From Galleon (DK Entrance)", "From Galleon (Tiny Entrance)", "From Galleon (DK Entrance)"],
    Maps.Galleon2DShip: ["From Galleon (Tiny Entrance)", "From Galleon (Lanky Entrance)", "From Galleon (Tiny Entrance)"],
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
        "From Fungi Lobby",
    ],
    Maps.ForestMillFront: ["From Fungi (Front)", "From Mill (Rear)", "From Fungi (Front)"],
    Maps.ForestMillBack: ["From Fungi (PPunch Door)", "From Spider Boss", "From Mill (Front)", "From Fungi (Tiny Hole)", "From Fungi (PPunch Door)"],
    Maps.ForestGiantMushroom: ["From Fungi (Low)", "From Fungi (Middle)", "From Fungi (Low Middle)", "From Fungi (High Middle)", "From Fungi (High)", "From Fungi (Low)"],
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
        "From Caves Lobby",
    ],
    Maps.CreepyCastle: [
        "From Castle Lobby",
        "From Tree (Drain)",
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
        "From Castle Lobby",
    ],
    Maps.CastleBallroom: ["From Castle Main", "From Museum (Monkeyport)", "From Castle Main"],
    Maps.CastleCrypt: ["From Lower Cave", "From Minecart", "From Lower Cave"],
    Maps.CastleMuseum: ["From Castle Main", "From Car Race", "From Ballroom (Monkeyport)", "From Castle Main"],
    Maps.CastleLibrary: ["From Castle Main (Start)", "From Castle Main (End)"],
    Maps.CastleUpperCave: ["From Castle (Front)", "From Candy's", "From Castle (Rear)", "From T&S", "From Dungeon", "From Castle (Front)"],
    Maps.CastleLowerCave: ["From Castle Main", "From Funky's", "From T&S", "From Crypt (DK/Diddy/Chunky)", "From Mausoleum (Lanky/Tiny)", "From Castle Main"],
    Maps.JungleJapesLobby: ["From DK Isles", "From Japes", "From DK Isles"],
    Maps.AngryAztecLobby: ["From DK Isles", "From Aztec", "From DK Isles"],
    Maps.GloomyGalleonLobby: ["From DK Isles", "From Galleon", "From DK Isles"],
    Maps.FranticFactoryLobby: ["From DK Isles", "From Factory", "From DK Isles"],
    Maps.FungiForestLobby: ["From DK Isles", "From Fungi", "From DK Isles"],
    Maps.CreepyCastleLobby: ["From DK Isles", "From Castle", "From DK Isles"],
    Maps.CrystalCavesLobby: ["From DK Isles", "From Caves", "From DK Isles"],
}


def GetMapId(regionId):
    """Get the map id of a transition."""
    return RegionMapList[regionId]


def GetExitId(back: TransitionBack):
    """Get exit id of a transition."""
    mapId = GetMapId(back.regionId)
    if mapId in MapExitTable:
        return MapExitTable[mapId].index(back.name)
    else:
        # Default exit number should be zero for all maps that don't have multiple exits
        return 0
