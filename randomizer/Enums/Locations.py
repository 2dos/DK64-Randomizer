"""Location enum."""

from enum import IntEnum, auto


class Locations(IntEnum):
    """Location enum."""

    # Training Barrel locations
    IslesVinesTrainingBarrel = auto()  # ID: 1
    IslesSwimTrainingBarrel = auto()
    IslesOrangesTrainingBarrel = auto()
    IslesBarrelsTrainingBarrel = auto()

    # Pre-given move locations (36 locations + training grounds reward) - the integer value of these matter for starting move count
    IslesFirstMove = auto()  # ID: 5
    PreGiven_Location00 = auto()
    PreGiven_Location01 = auto()
    PreGiven_Location02 = auto()
    PreGiven_Location03 = auto()
    PreGiven_Location04 = auto()
    PreGiven_Location05 = auto()
    PreGiven_Location06 = auto()
    PreGiven_Location07 = auto()
    PreGiven_Location08 = auto()
    PreGiven_Location09 = auto()
    PreGiven_Location10 = auto()
    PreGiven_Location11 = auto()
    PreGiven_Location12 = auto()
    PreGiven_Location13 = auto()
    PreGiven_Location14 = auto()
    PreGiven_Location15 = auto()
    PreGiven_Location16 = auto()
    PreGiven_Location17 = auto()
    PreGiven_Location18 = auto()
    PreGiven_Location19 = auto()
    PreGiven_Location20 = auto()
    PreGiven_Location21 = auto()
    PreGiven_Location22 = auto()
    PreGiven_Location23 = auto()
    PreGiven_Location24 = auto()
    PreGiven_Location25 = auto()
    PreGiven_Location26 = auto()
    PreGiven_Location27 = auto()
    PreGiven_Location28 = auto()
    PreGiven_Location29 = auto()
    PreGiven_Location30 = auto()
    PreGiven_Location31 = auto()
    PreGiven_Location32 = auto()
    PreGiven_Location33 = auto()
    PreGiven_Location34 = auto()
    PreGiven_Location35 = auto()
    PreGiven_Location36 = auto()

    # DK Isles locations
    IslesDonkeyMedal = auto()  # ID: 42
    IslesDiddyMedal = auto()
    IslesLankyMedal = auto()
    IslesTinyMedal = auto()
    IslesChunkyMedal = auto()
    IslesDonkeyJapesRock = auto()
    IslesTinyCagedBanana = auto()
    IslesTinyInstrumentPad = auto()
    IslesLankyCagedBanana = auto()
    IslesChunkyCagedBanana = auto()
    IslesChunkyInstrumentPad = auto()
    IslesChunkyPoundtheX = auto()
    IslesBananaFairyIsland = auto()
    IslesBananaFairyCrocodisleIsle = auto()
    IslesLankyPrisonOrangsprint = auto()
    CameraAndShockwave = auto()
    RarewareBanana = auto()
    IslesLankyInstrumentPad = auto()
    IslesTinyAztecLobby = auto()
    IslesDonkeyCagedBanana = auto()
    IslesDiddySnidesLobby = auto()
    IslesDonkeyInstrumentPad = auto()
    IslesKasplatFactoryLobby = auto()
    IslesBananaFairyFactoryLobby = auto()
    IslesTinyGalleonLobby = auto()
    IslesKasplatGalleonLobby = auto()
    IslesDiddyCagedBanana = auto()
    IslesDiddySummit = auto()
    IslesBananaFairyForestLobby = auto()
    IslesDonkeyLavaBanana = auto()
    IslesDiddyInstrumentPad = auto()
    IslesKasplatCavesLobby = auto()
    IslesLankyCastleLobby = auto()
    IslesKasplatCastleLobby = auto()
    IslesChunkyHelmLobby = auto()
    IslesKasplatHelmLobby = auto()
    BananaHoard = auto()

    # Jungle Japes location
    JapesDonkeyMedal = auto()  # ID: 79
    JapesDiddyMedal = auto()
    JapesLankyMedal = auto()
    JapesTinyMedal = auto()
    JapesChunkyMedal = auto()
    DiddyKong = auto()
    JapesDonkeyFrontofCage = auto()
    JapesDonkeyFreeDiddy = auto()
    JapesDonkeyCagedBanana = auto()
    JapesDonkeyBaboonBlast = auto()
    JapesDiddyCagedBanana = auto()
    JapesDiddyMountain = auto()
    JapesLankyCagedBanana = auto()
    JapesTinyCagedBanana = auto()
    JapesChunkyBoulder = auto()
    JapesChunkyCagedBanana = auto()
    JapesDiddyTunnel = auto()
    JapesLankyGrapeGate = auto()
    JapesTinyFeatherGateBarrel = auto()
    JapesKasplatLeftTunnelNear = auto()
    JapesKasplatLeftTunnelFar = auto()
    JapesTinyStump = auto()
    JapesChunkyGiantBonusBarrel = auto()
    JapesTinyBeehive = auto()
    JapesLankySlope = auto()
    JapesKasplatNearPaintingRoom = auto()
    JapesKasplatNearLab = auto()
    JapesBananaFairyRambiCave = auto()
    JapesLankyFairyCave = auto()
    JapesBananaFairyLankyCave = auto()
    JapesDiddyMinecarts = auto()
    JapesChunkyUnderground = auto()
    JapesKasplatUnderground = auto()
    JapesKey = auto()

    # Angry Aztec
    AztecDonkeyMedal = auto()  # ID: 113
    AztecDiddyMedal = auto()
    AztecLankyMedal = auto()
    AztecTinyMedal = auto()
    AztecChunkyMedal = auto()
    AztecDonkeyFreeLlama = auto()
    AztecChunkyVases = auto()
    AztecKasplatSandyBridge = auto()
    AztecKasplatOnTinyTemple = auto()
    AztecTinyKlaptrapRoom = auto()
    AztecChunkyKlaptrapRoom = auto()
    TinyKong = auto()
    AztecDiddyFreeTiny = auto()
    AztecLankyVulture = auto()
    AztecDonkeyQuicksandCave = auto()
    AztecDiddyRamGongs = auto()
    AztecDiddyVultureRace = auto()
    AztecChunkyCagedBarrel = auto()
    AztecKasplatNearLab = auto()
    AztecDonkey5DoorTemple = auto()
    AztecDiddy5DoorTemple = auto()
    AztecLanky5DoorTemple = auto()
    AztecTiny5DoorTemple = auto()
    AztecBananaFairyTinyTemple = auto()
    AztecChunky5DoorTemple = auto()
    AztecKasplatChunky5DT = auto()
    AztecTinyBeetleRace = auto()
    LankyKong = auto()
    AztecDonkeyFreeLanky = auto()
    AztecLankyLlamaTempleBarrel = auto()
    AztecLankyMatchingGame = auto()
    AztecBananaFairyLlamaTemple = auto()
    AztecTinyLlamaTemple = auto()
    AztecKasplatLlamaTemple = auto()
    AztecKey = auto()

    # Frantic Factory locations
    FactoryDonkeyMedal = auto()  # 147
    FactoryDiddyMedal = auto()
    FactoryLankyMedal = auto()
    FactoryTinyMedal = auto()
    FactoryChunkyMedal = auto()
    FactoryDonkeyNumberGame = auto()
    FactoryDiddyBlockTower = auto()
    FactoryLankyTestingRoomBarrel = auto()
    FactoryTinyDartboard = auto()
    FactoryKasplatBlocks = auto()
    FactoryBananaFairybyCounting = auto()
    FactoryBananaFairybyFunky = auto()
    FactoryDiddyRandD = auto()
    FactoryLankyRandD = auto()
    FactoryChunkyRandD = auto()
    FactoryKasplatRandD = auto()
    FactoryTinyCarRace = auto()
    FactoryDiddyChunkyRoomBarrel = auto()
    FactoryDonkeyPowerHut = auto()
    ChunkyKong = auto()
    NintendoCoin = auto()
    FactoryDonkeyDKArcade = auto()
    FactoryLankyFreeChunky = auto()
    FactoryTinybyArcade = auto()
    FactoryChunkyDarkRoom = auto()
    FactoryChunkybyArcade = auto()
    FactoryKasplatProductionBottom = auto()
    FactoryKasplatStorage = auto()
    FactoryDonkeyCrusherRoom = auto()
    FactoryDiddyProductionRoom = auto()
    FactoryLankyProductionRoom = auto()
    FactoryTinyProductionRoom = auto()
    FactoryChunkyProductionRoom = auto()
    FactoryKasplatProductionTop = auto()
    FactoryKey = auto()

    # Gloomy Galleon locations
    GalleonDonkeyMedal = auto()  # ID: 183
    GalleonDiddyMedal = auto()
    GalleonLankyMedal = auto()
    GalleonTinyMedal = auto()
    GalleonChunkyMedal = auto()
    GalleonChunkyChest = auto()
    GalleonKasplatNearLab = auto()
    GalleonBananaFairybyCranky = auto()
    GalleonChunkyCannonGame = auto()
    GalleonKasplatCannons = auto()
    GalleonDiddyShipSwitch = auto()
    GalleonLankyEnguardeChest = auto()
    GalleonKasplatLighthouseArea = auto()
    GalleonDonkeyLighthouse = auto()
    GalleonTinyPearls = auto()
    GalleonChunkySeasick = auto()
    GalleonDonkeyFreetheSeal = auto()
    GalleonKasplatNearSub = auto()
    GalleonDonkeySealRace = auto()
    GalleonDiddyGoldTower = auto()
    GalleonLankyGoldTower = auto()
    GalleonKasplatGoldTower = auto()
    GalleonTinySubmarine = auto()
    GalleonDiddyMechafish = auto()
    GalleonLanky2DoorShip = auto()
    GalleonTiny2DoorShip = auto()
    GalleonDonkey5DoorShip = auto()
    GalleonDiddy5DoorShip = auto()
    GalleonLanky5DoorShip = auto()
    GalleonTiny5DoorShip = auto()
    GalleonBananaFairy5DoorShip = auto()
    GalleonChunky5DoorShip = auto()
    GalleonPearl0 = auto()
    GalleonPearl1 = auto()
    GalleonPearl2 = auto()
    GalleonPearl3 = auto()
    GalleonPearl4 = auto()
    GalleonKey = auto()

    # Fungi Forest locations
    ForestDonkeyMedal = auto()  # ID: 221
    ForestDiddyMedal = auto()
    ForestLankyMedal = auto()
    ForestTinyMedal = auto()
    ForestChunkyMedal = auto()
    ForestChunkyMinecarts = auto()
    ForestDiddyTopofMushroom = auto()
    ForestTinyMushroomBarrel = auto()
    ForestDonkeyBaboonBlast = auto()
    ForestKasplatLowerMushroomExterior = auto()
    ForestDonkeyMushroomCannons = auto()
    ForestKasplatInsideMushroom = auto()
    ForestKasplatUpperMushroomExterior = auto()
    ForestChunkyFacePuzzle = auto()
    ForestLankyZingers = auto()
    ForestLankyColoredMushrooms = auto()
    ForestDiddyOwlRace = auto()
    ForestLankyRabbitRace = auto()
    ForestKasplatOwlTree = auto()
    ForestTinyAnthill = auto()
    ForestDonkeyMill = auto()
    ForestDiddyCagedBanana = auto()
    ForestTinySpiderBoss = auto()
    ForestChunkyKegs = auto()
    ForestDiddyRafters = auto()
    ForestBananaFairyRafters = auto()
    ForestLankyAttic = auto()
    ForestKasplatNearBarn = auto()
    ForestDonkeyBarn = auto()
    ForestBananaFairyThornvines = auto()
    ForestTinyBeanstalk = auto()
    ForestChunkyApple = auto()
    ForestBean = auto()
    ForestKey = auto()

    # Crystal Caves locations
    CavesDonkeyMedal = auto()  # ID: 255
    CavesDiddyMedal = auto()
    CavesLankyMedal = auto()
    CavesTinyMedal = auto()
    CavesChunkyMedal = auto()
    CavesDonkeyBaboonBlast = auto()
    CavesDiddyJetpackBarrel = auto()
    CavesTinyCaveBarrel = auto()
    CavesTinyMonkeyportIgloo = auto()
    CavesChunkyGorillaGone = auto()
    CavesKasplatNearLab = auto()
    CavesKasplatNearFunky = auto()
    CavesKasplatPillar = auto()
    CavesKasplatNearCandy = auto()
    CavesLankyBeetleRace = auto()
    CavesLankyCastle = auto()
    CavesChunkyTransparentIgloo = auto()
    CavesKasplatOn5DI = auto()
    CavesDonkey5DoorIgloo = auto()
    CavesDiddy5DoorIgloo = auto()
    CavesLanky5DoorIgloo = auto()
    CavesTiny5DoorIgloo = auto()
    CavesBananaFairyIgloo = auto()
    CavesChunky5DoorIgloo = auto()
    CavesDonkeyRotatingCabin = auto()
    CavesDonkey5DoorCabin = auto()
    CavesDiddy5DoorCabinLower = auto()
    CavesDiddy5DoorCabinUpper = auto()
    CavesBananaFairyCabin = auto()
    CavesLanky1DoorCabin = auto()
    CavesTiny5DoorCabin = auto()
    CavesChunky5DoorCabin = auto()
    CavesKey = auto()

    # Creepy Castle locations
    CastleDonkeyMedal = auto()  # ID: 288
    CastleDiddyMedal = auto()
    CastleLankyMedal = auto()
    CastleTinyMedal = auto()
    CastleChunkyMedal = auto()
    CastleDiddyAboveCastle = auto()
    CastleKasplatHalfway = auto()
    CastleKasplatLowerLedge = auto()
    CastleDonkeyTree = auto()
    CastleChunkyTree = auto()
    CastleKasplatTree = auto()
    CastleBananaFairyTree = auto()
    CastleDonkeyLibrary = auto()
    CastleDiddyBallroom = auto()
    CastleBananaFairyBallroom = auto()
    CastleTinyCarRace = auto()
    CastleLankyTower = auto()
    CastleLankyGreenhouse = auto()
    CastleTinyTrashCan = auto()
    CastleChunkyShed = auto()
    CastleChunkyMuseum = auto()
    CastleKasplatCrypt = auto()
    CastleDiddyCrypt = auto()
    CastleChunkyCrypt = auto()
    CastleDonkeyMinecarts = auto()
    CastleLankyMausoleum = auto()
    CastleTinyMausoleum = auto()
    CastleTinyOverChasm = auto()
    CastleKasplatNearCandy = auto()
    CastleDonkeyDungeon = auto()
    CastleDiddyDungeon = auto()
    CastleLankyDungeon = auto()
    CastleKey = auto()

    # Hideout Helm locations
    HelmDonkey1 = auto()  # ID: 321
    HelmDonkey2 = auto()
    HelmDiddy1 = auto()
    HelmDiddy2 = auto()
    HelmLanky1 = auto()
    HelmLanky2 = auto()
    HelmTiny1 = auto()
    HelmTiny2 = auto()
    HelmChunky1 = auto()
    HelmChunky2 = auto()
    HelmDonkeyMedal = auto()
    HelmChunkyMedal = auto()
    HelmTinyMedal = auto()
    HelmLankyMedal = auto()
    HelmDiddyMedal = auto()
    HelmBananaFairy1 = auto()
    HelmBananaFairy2 = auto()
    HelmKey = auto()

    # Shop locations
    CoconutGun = auto()  # ID: 339
    PeanutGun = auto()
    GrapeGun = auto()
    FeatherGun = auto()
    PineappleGun = auto()
    AmmoBelt1 = auto()
    HomingAmmo = auto()
    AmmoBelt2 = auto()
    SniperSight = auto()
    Bongos = auto()
    Guitar = auto()
    Trombone = auto()
    Saxophone = auto()
    Triangle = auto()
    MusicUpgrade1 = auto()
    ThirdMelon = auto()
    MusicUpgrade2 = auto()
    SimianSlam = auto()
    SuperSimianSlam = auto()
    SuperDuperSimianSlam = auto()
    BaboonBlast = auto()
    StrongKong = auto()
    GorillaGrab = auto()
    ChimpyCharge = auto()
    RocketbarrelBoost = auto()
    SimianSpring = auto()
    Orangstand = auto()
    BaboonBalloon = auto()
    OrangstandSprint = auto()
    MiniMonkey = auto()
    PonyTailTwirl = auto()
    Monkeyport = auto()
    HunkyChunky = auto()
    PrimatePunch = auto()
    GorillaGone = auto()
    RarewareCoin = auto()
    # These act as placeholders for shuffled move locations. In Vanilla game there is no move here
    DonkeyGalleonPotion = auto()  # ID: 375
    DonkeyForestPotion = auto()
    DonkeyCavesPotion = auto()
    DonkeyCastlePotion = auto()
    DonkeyIslesPotion = auto()
    DiddyGalleonPotion = auto()
    DiddyForestPotion = auto()
    DiddyCavesPotion = auto()
    DiddyCastlePotion = auto()
    DiddyIslesPotion = auto()
    LankyAztecPotion = auto()
    LankyGalleonPotion = auto()
    LankyForestPotion = auto()
    LankyCastlePotion = auto()
    LankyIslesPotion = auto()
    TinyAztecPotion = auto()
    TinyGalleonPotion = auto()
    TinyForestPotion = auto()
    TinyCastlePotion = auto()
    TinyIslesPotion = auto()
    ChunkyAztecPotion = auto()
    ChunkyGalleonPotion = auto()
    ChunkyForestPotion = auto()
    ChunkyCastlePotion = auto()
    ChunkyIslesPotion = auto()
    SharedJapesPotion = auto()
    SharedAztecPotion = auto()
    SharedFactoryPotion = auto()
    SharedGalleonPotion = auto()
    SharedCavesPotion = auto()
    DonkeyAztecGun = auto()
    DonkeyFactoryGun = auto()
    DonkeyGalleonGun = auto()
    DonkeyForestGun = auto()
    DonkeyCavesGun = auto()
    DonkeyCastleGun = auto()
    DiddyAztecGun = auto()
    DiddyFactoryGun = auto()
    DiddyGalleonGun = auto()
    DiddyForestGun = auto()
    DiddyCavesGun = auto()
    DiddyCastleGun = auto()
    LankyAztecGun = auto()
    LankyFactoryGun = auto()
    LankyGalleonGun = auto()
    LankyForestGun = auto()
    LankyCavesGun = auto()
    LankyCastleGun = auto()
    TinyAztecGun = auto()
    TinyFactoryGun = auto()
    TinyGalleonGun = auto()
    TinyForestGun = auto()
    TinyCavesGun = auto()
    TinyCastleGun = auto()
    ChunkyAztecGun = auto()
    ChunkyFactoryGun = auto()
    ChunkyGalleonGun = auto()
    ChunkyForestGun = auto()
    ChunkyCavesGun = auto()
    ChunkyCastleGun = auto()
    SharedJapesGun = auto()
    SharedAztecGun = auto()
    SharedGalleonGun = auto()
    DonkeyFactoryInstrument = auto()  # ID: 433
    DonkeyGalleonInstrument = auto()
    DonkeyCavesInstrument = auto()
    DonkeyCastleInstrument = auto()
    DiddyFactoryInstrument = auto()
    DiddyGalleonInstrument = auto()
    DiddyCavesInstrument = auto()
    DiddyCastleInstrument = auto()
    LankyFactoryInstrument = auto()
    LankyGalleonInstrument = auto()
    LankyCavesInstrument = auto()
    LankyCastleInstrument = auto()
    TinyFactoryInstrument = auto()
    TinyGalleonInstrument = auto()
    TinyCavesInstrument = auto()
    TinyCastleInstrument = auto()
    ChunkyFactoryInstrument = auto()
    ChunkyGalleonInstrument = auto()
    ChunkyCavesInstrument = auto()
    ChunkyCastleInstrument = auto()
    SharedAztecInstrument = auto()
    SharedFactoryInstrument = auto()

    TurnInDKIslesDonkeyBlueprint = auto()  # ID: 460
    TurnInDKIslesDiddyBlueprint = auto()
    TurnInDKIslesLankyBlueprint = auto()
    TurnInDKIslesTinyBlueprint = auto()
    TurnInDKIslesChunkyBlueprint = auto()
    TurnInJungleJapesDonkeyBlueprint = auto()
    TurnInJungleJapesDiddyBlueprint = auto()
    TurnInJungleJapesLankyBlueprint = auto()
    TurnInJungleJapesTinyBlueprint = auto()
    TurnInJungleJapesChunkyBlueprint = auto()
    TurnInAngryAztecDonkeyBlueprint = auto()
    TurnInAngryAztecDiddyBlueprint = auto()
    TurnInAngryAztecLankyBlueprint = auto()
    TurnInAngryAztecTinyBlueprint = auto()
    TurnInAngryAztecChunkyBlueprint = auto()
    TurnInFranticFactoryDonkeyBlueprint = auto()
    TurnInFranticFactoryDiddyBlueprint = auto()
    TurnInFranticFactoryLankyBlueprint = auto()
    TurnInFranticFactoryTinyBlueprint = auto()
    TurnInFranticFactoryChunkyBlueprint = auto()
    TurnInGloomyGalleonDonkeyBlueprint = auto()
    TurnInGloomyGalleonDiddyBlueprint = auto()
    TurnInGloomyGalleonLankyBlueprint = auto()
    TurnInGloomyGalleonTinyBlueprint = auto()
    TurnInGloomyGalleonChunkyBlueprint = auto()
    TurnInFungiForestDonkeyBlueprint = auto()
    TurnInFungiForestDiddyBlueprint = auto()
    TurnInFungiForestLankyBlueprint = auto()
    TurnInFungiForestTinyBlueprint = auto()
    TurnInFungiForestChunkyBlueprint = auto()
    TurnInCrystalCavesDonkeyBlueprint = auto()
    TurnInCrystalCavesDiddyBlueprint = auto()
    TurnInCrystalCavesLankyBlueprint = auto()
    TurnInCrystalCavesTinyBlueprint = auto()
    TurnInCrystalCavesChunkyBlueprint = auto()
    TurnInCreepyCastleDonkeyBlueprint = auto()
    TurnInCreepyCastleDiddyBlueprint = auto()
    TurnInCreepyCastleLankyBlueprint = auto()
    TurnInCreepyCastleTinyBlueprint = auto()
    TurnInCreepyCastleChunkyBlueprint = auto()  # ID: 499

    # Door locations must remain grouped together in this specific order for hint door location logic
    JapesDonkeyDoor = auto()  # ID: 500
    JapesDiddyDoor = auto()
    JapesLankyDoor = auto()
    JapesTinyDoor = auto()
    JapesChunkyDoor = auto()
    AztecDonkeyDoor = auto()
    AztecDiddyDoor = auto()
    AztecLankyDoor = auto()
    AztecTinyDoor = auto()
    AztecChunkyDoor = auto()
    FactoryDonkeyDoor = auto()
    FactoryDiddyDoor = auto()
    FactoryLankyDoor = auto()
    FactoryTinyDoor = auto()
    FactoryChunkyDoor = auto()
    GalleonDonkeyDoor = auto()
    GalleonDiddyDoor = auto()
    GalleonLankyDoor = auto()
    GalleonTinyDoor = auto()
    GalleonChunkyDoor = auto()
    ForestDonkeyDoor = auto()
    ForestDiddyDoor = auto()
    ForestLankyDoor = auto()
    ForestTinyDoor = auto()
    ForestChunkyDoor = auto()
    CavesDonkeyDoor = auto()
    CavesDiddyDoor = auto()
    CavesLankyDoor = auto()
    CavesTinyDoor = auto()
    CavesChunkyDoor = auto()
    CastleDonkeyDoor = auto()
    CastleDiddyDoor = auto()
    CastleLankyDoor = auto()
    CastleTinyDoor = auto()
    CastleChunkyDoor = auto()  # ID: 534

    # Crown locations must stay grouped in this order
    JapesBattleArena = auto()  # ID: 535
    AztecBattleArena = auto()
    FactoryBattleArena = auto()
    GalleonBattleArena = auto()
    ForestBattleArena = auto()
    CavesBattleArena = auto()
    CastleBattleArena = auto()
    IslesBattleArena1 = auto()
    IslesBattleArena2 = auto()
    HelmBattleArena = auto()  # ID: 544

    # These locations are only utilized in kasplat rando and must stay grouped in this order
    JapesDonkeyKasplatRando = auto()  # ID: 545
    JapesDiddyKasplatRando = auto()
    JapesLankyKasplatRando = auto()
    JapesTinyKasplatRando = auto()
    JapesChunkyKasplatRando = auto()
    AztecDonkeyKasplatRando = auto()
    AztecDiddyKasplatRando = auto()
    AztecLankyKasplatRando = auto()
    AztecTinyKasplatRando = auto()
    AztecChunkyKasplatRando = auto()
    FactoryDonkeyKasplatRando = auto()
    FactoryDiddyKasplatRando = auto()
    FactoryLankyKasplatRando = auto()
    FactoryTinyKasplatRando = auto()
    FactoryChunkyKasplatRando = auto()
    GalleonDonkeyKasplatRando = auto()
    GalleonDiddyKasplatRando = auto()
    GalleonLankyKasplatRando = auto()
    GalleonTinyKasplatRando = auto()
    GalleonChunkyKasplatRando = auto()
    ForestDonkeyKasplatRando = auto()
    ForestDiddyKasplatRando = auto()
    ForestLankyKasplatRando = auto()
    ForestTinyKasplatRando = auto()
    ForestChunkyKasplatRando = auto()
    CavesDonkeyKasplatRando = auto()
    CavesDiddyKasplatRando = auto()
    CavesLankyKasplatRando = auto()
    CavesTinyKasplatRando = auto()
    CavesChunkyKasplatRando = auto()
    CastleDonkeyKasplatRando = auto()
    CastleDiddyKasplatRando = auto()
    CastleLankyKasplatRando = auto()
    CastleTinyKasplatRando = auto()
    CastleChunkyKasplatRando = auto()
    IslesDonkeyKasplatRando = auto()
    IslesDiddyKasplatRando = auto()
    IslesLankyKasplatRando = auto()
    IslesTinyKasplatRando = auto()
    IslesChunkyKasplatRando = auto()  # ID: 584

    # Rainbow Coin Locations used for dirt patch rando and item rando. Must remain in this order
    RainbowCoin_Location00 = auto()  # ID: 585
    RainbowCoin_Location01 = auto()
    RainbowCoin_Location02 = auto()
    RainbowCoin_Location03 = auto()
    RainbowCoin_Location04 = auto()
    RainbowCoin_Location05 = auto()
    RainbowCoin_Location06 = auto()
    RainbowCoin_Location07 = auto()
    RainbowCoin_Location08 = auto()
    RainbowCoin_Location09 = auto()
    RainbowCoin_Location10 = auto()
    RainbowCoin_Location11 = auto()
    RainbowCoin_Location12 = auto()
    RainbowCoin_Location13 = auto()
    RainbowCoin_Location14 = auto()
    RainbowCoin_Location15 = auto()  # ID: 600

    # Melon Crate Locations
    MelonCrate_Location00 = auto()  # ID: 601
    MelonCrate_Location01 = auto()
    MelonCrate_Location02 = auto()
    MelonCrate_Location03 = auto()
    MelonCrate_Location04 = auto()
    MelonCrate_Location05 = auto()
    MelonCrate_Location06 = auto()
    MelonCrate_Location07 = auto()
    MelonCrate_Location08 = auto()
    MelonCrate_Location09 = auto()
    MelonCrate_Location10 = auto()
    MelonCrate_Location11 = auto()
    MelonCrate_Location12 = auto()  # ID: 613

    # Shop Owner Locations
    ShopOwner_Location00 = auto()  # ID: 614
    ShopOwner_Location01 = auto()
    ShopOwner_Location02 = auto()
    ShopOwner_Location03 = auto()  # ID: 617

    # Enemies
    # Japes
    # Main
    JapesMainEnemy_Start = auto()  # Beaver, 2
    JapesMainEnemy_DiddyCavern = auto()  # Beaver, 4
    JapesMainEnemy_Tunnel0 = auto()  # Beaver, 5
    JapesMainEnemy_Tunnel1 = auto()  # Beaver, 6
    JapesMainEnemy_Storm0 = auto()  # Beaver, 15
    JapesMainEnemy_Storm1 = auto()  # Beaver, 18
    JapesMainEnemy_Storm2 = auto()  # Beaver, 20
    JapesMainEnemy_Hive0 = auto()  # Zinger (0x1C), 28
    JapesMainEnemy_Hive1 = auto()  # Zinger (0x1C), 29
    JapesMainEnemy_Hive2 = auto()  # Zinger (0x1C), 30
    JapesMainEnemy_Hive3 = auto()  # Kremling, 36
    JapesMainEnemy_Hive4 = auto()  # Kremling, 37
    JapesMainEnemy_KilledInDemo = auto()  # Beaver, 33
    JapesMainEnemy_NearUnderground = auto()  # Zinger (0x5), 49
    JapesMainEnemy_NearPainting0 = auto()  # Beaver, 34
    JapesMainEnemy_NearPainting1 = auto()  # Beaver, 35
    JapesMainEnemy_NearPainting2 = auto()  # Zinger (0x5), 48
    JapesMainEnemy_Mountain = auto()  # Zinger (0x5), 50
    JapesMainEnemy_FeatherTunnel = auto()  # Zinger (0x1C), 52
    JapesMainEnemy_MiddleTunnel = auto()  # Beaver, 54

    # Lobby
    JapesLobbyEnemy_Enemy0 = auto()  # Beaver, 1
    JapesLobbyEnemy_Enemy1 = auto()  # Beaver, 2

    # Painting
    JapesPaintingEnemy_Gauntlet0 = auto()  # Zinger (0x5), 2
    JapesPaintingEnemy_Gauntlet1 = auto()  # Zinger (0x5), 3
    JapesPaintingEnemy_Gauntlet2 = auto()  # Zinger (0x5), 4
    JapesPaintingEnemy_Gauntlet3 = auto()  # Zinger (0x5), 5
    JapesPaintingEnemy_Gauntlet4 = auto()  # Zinger (0x5), 6

    # Mountain
    JapesMountainEnemy_Start0 = auto()  # Beaver, 1
    JapesMountainEnemy_Start1 = auto()  # Beaver, 2
    JapesMountainEnemy_Start2 = auto()  # Beaver, 6
    JapesMountainEnemy_Start3 = auto()  # Zinger (0x5), 8
    JapesMountainEnemy_Start4 = auto()  # Zinger (0x5), 9
    JapesMountainEnemy_NearGateSwitch0 = auto()  # Zinger (0x1C), 13
    JapesMountainEnemy_NearGateSwitch1 = auto()  # Zinger (0x1C), 14
    JapesMountainEnemy_HiLo = auto()  # Klump, 15
    JapesMountainEnemy_Conveyor0 = auto()  # Klump, 16
    JapesMountainEnemy_Conveyor1 = auto()  # Klump, 17

    # Shellhive
    JapesShellhiveEnemy_FirstRoom = auto()  # P Klaptrap, 7
    JapesShellhiveEnemy_SecondRoom0 = auto()  # P Klaptrap, 8
    JapesShellhiveEnemy_SecondRoom1 = auto()  # P Klaptrap, 9
    JapesShellhiveEnemy_ThirdRoom0 = auto()  # P Klaptrap, 10
    JapesShellhiveEnemy_ThirdRoom1 = auto()  # P Klaptrap, 11
    JapesShellhiveEnemy_ThirdRoom2 = auto()  # Zinger (0x5), 12
    JapesShellhiveEnemy_ThirdRoom3 = auto()  # Zinger (0x5), 13
    JapesShellhiveEnemy_MainRoom = auto()  # Zinger (0x5), 14

    # Angry Aztec
    # Main
    AztecMainEnemy_VaseRoom0 = auto()  # Zinger (0x1C), 2
    AztecMainEnemy_VaseRoom1 = auto()  # Zinger (0x1C), 4
    AztecMainEnemy_TunnelPad0 = auto()  # Zinger (0x1C), 10
    AztecMainEnemy_TunnelCage0 = auto()  # Klaptrap, 13
    AztecMainEnemy_TunnelCage1 = auto()  # Klaptrap, 14
    AztecMainEnemy_TunnelCage2 = auto()  # Klaptrap, 15
    AztecMainEnemy_StartingTunnel0 = auto()  # Kremling, 20
    AztecMainEnemy_StartingTunnel1 = auto()  # Kremling, 21
    AztecMainEnemy_OasisDoor = auto()  # Kremling, 23
    AztecMainEnemy_TunnelCage3 = auto()  # Kremling, 26
    AztecMainEnemy_OutsideLlama = auto()  # Kremling, 27
    AztecMainEnemy_OutsideTower = auto()  # Kremling, 28
    AztecMainEnemy_TunnelPad1 = auto()  # Zinger (0x1C), 31
    AztecMainEnemy_NearCandy = auto()  # Zinger (0x1C), 32
    AztecMainEnemy_AroundTotem = auto()  # Klaptrap, 33
    AztecMainEnemy_StartingTunnel2 = auto()  # Zinger (0x5), 38
    AztecMainEnemy_StartingTunnel3 = auto()  # Zinger (0x5), 39
    AztecMainEnemy_OutsideSnide = auto()  # Klaptrap, 40
    AztecMainEnemy_Outside5DT = auto()  # Zinger (0x1C), 41
    AztecMainEnemy_NearSnoopTunnel = auto()  # Kremling, 42

    # Lobby
    AztecLobbyEnemy_Pad0 = auto()  # Zinger (0x5), 2
    AztecLobbyEnemy_Pad1 = auto()  # Zinger (0x5), 3

    # DK 5DT
    AztecDK5DTEnemy_StartTrap0 = auto()  # Kaboom, 5
    AztecDK5DTEnemy_StartTrap1 = auto()  # Kaboom, 6
    AztecDK5DTEnemy_StartTrap2 = auto()  # Kaboom, 7
    AztecDK5DTEnemy_EndTrap0 = auto()  # Kaboom, 10
    AztecDK5DTEnemy_EndTrap1 = auto()  # Kaboom, 11
    AztecDK5DTEnemy_EndTrap2 = auto()  # Kaboom, 12
    AztecDK5DTEnemy_EndPath0 = auto()  # P Klaptrap, 13
    AztecDK5DTEnemy_EndPath1 = auto()  # P Klaptrap, 14
    AztecDK5DTEnemy_StartPath = auto()  # P Klaptrap, 15

    # Diddy 5DT
    AztecDiddy5DTEnemy_EndTrap0 = auto()  # Klobber, 4
    AztecDiddy5DTEnemy_EndTrap1 = auto()  # Klobber, 5
    AztecDiddy5DTEnemy_EndTrap2 = auto()  # Klobber, 6
    AztecDiddy5DTEnemy_StartLeft0 = auto()  # Kremling, 9
    AztecDiddy5DTEnemy_StartLeft1 = auto()  # Kremling, 10
    AztecDiddy5DTEnemy_Reward = auto()  # Klump, 11
    AztecDiddy5DTEnemy_SecondSwitch = auto()  # Kremling, 12

    # Lanky 5DT
    AztecLanky5DTEnemy_JoiningPaths = auto()  # Klump, 2
    AztecLanky5DTEnemy_EndTrap = auto()  # Klump, 3
    AztecLanky5DTEnemy_Reward = auto()  # Klump, 4

    # Tiny 5DT
    AztecTiny5DTEnemy_StartRightFront = auto()  # Zinger (0x1C), 2
    AztecTiny5DTEnemy_StartLeftBack = auto()  # Zinger (0x1C), 4
    AztecTiny5DTEnemy_StartRightBack = auto()  # Zinger (0x1C), 5
    AztecTiny5DTEnemy_StartLeftFront = auto()  # Zinger (0x1C), 6
    AztecTiny5DTEnemy_Reward0 = auto()  # Zinger (0x1C), 7
    AztecTiny5DTEnemy_Reward1 = auto()  # Zinger (0x1C), 8
    AztecTiny5DTEnemy_DeadEnd0 = auto()  # Zinger (0x1C), 9
    AztecTiny5DTEnemy_DeadEnd1 = auto()  # Zinger (0x1C), 10

    # Chunky 5DT
    AztecChunky5DTEnemy_StartRight = auto()  # Klobber, 2
    AztecChunky5DTEnemy_StartLeft = auto()  # Klobber, 3
    AztecChunky5DTEnemy_SecondRight = auto()  # Klobber, 5
    AztecChunky5DTEnemy_SecondLeft = auto()  # Klobber, 6
    AztecChunky5DTEnemy_Reward = auto()  # Zinger (0x1C), 7

    # Llama Temple
    AztecLlamaEnemy_KongFreeInstrument = auto()  # P Klaptrap, 5
    AztecLlamaEnemy_DinoInstrument = auto()  # P Klaptrap, 6
    AztecLlamaEnemy_Matching0 = auto()  # Kremling, 10
    AztecLlamaEnemy_Matching1 = auto()  # Kremling, 11
    AztecLlamaEnemy_Right = auto()  # Kremling, 14
    AztecLlamaEnemy_Left = auto()  # Kremling, 15
    AztecLlamaEnemy_MelonCrate = auto()  # P Klaptrap, 16
    AztecLlamaEnemy_SlamSwitch = auto()  # P Klaptrap, 17

    # Tiny Temple
    AztecTempleEnemy_Rotating00 = auto()  # Klaptrap, 1
    AztecTempleEnemy_Rotating01 = auto()  # Klaptrap, 2
    AztecTempleEnemy_Rotating02 = auto()  # Klaptrap, 3
    AztecTempleEnemy_Rotating03 = auto()  # Klaptrap, 4
    AztecTempleEnemy_Rotating04 = auto()  # Klaptrap, 5
    AztecTempleEnemy_Rotating05 = auto()  # Klaptrap, 6
    AztecTempleEnemy_Rotating06 = auto()  # Klaptrap, 7
    AztecTempleEnemy_Rotating07 = auto()  # Klaptrap, 8
    AztecTempleEnemy_Rotating08 = auto()  # Klaptrap, 9
    AztecTempleEnemy_Rotating09 = auto()  # Klaptrap, 10
    AztecTempleEnemy_Rotating10 = auto()  # Klaptrap, 11
    AztecTempleEnemy_Rotating11 = auto()  # Klaptrap, 12
    AztecTempleEnemy_Rotating12 = auto()  # Klaptrap, 13
    AztecTempleEnemy_Rotating13 = auto()  # Klaptrap, 14
    AztecTempleEnemy_Rotating14 = auto()  # Klaptrap, 15
    AztecTempleEnemy_Rotating15 = auto()  # Klaptrap, 16
    AztecTempleEnemy_MiniRoom00 = auto()  # Klaptrap, 20
    AztecTempleEnemy_MiniRoom01 = auto()  # Klaptrap, 21
    AztecTempleEnemy_MiniRoom02 = auto()  # Klaptrap, 22
    AztecTempleEnemy_MiniRoom03 = auto()  # Klaptrap, 23
    AztecTempleEnemy_GuardRotating0 = auto()  # Klobber, 24
    AztecTempleEnemy_GuardRotating1 = auto()  # Klobber, 36
    AztecTempleEnemy_MainRoom0 = auto()  # Kremling, 26
    AztecTempleEnemy_MainRoom1 = auto()  # Kremling, 28
    AztecTempleEnemy_MainRoom2 = auto()  # Klaptrap, 35
    AztecTempleEnemy_KongRoom0 = auto()  # Klaptrap, 29
    AztecTempleEnemy_KongRoom1 = auto()  # Klaptrap, 30
    AztecTempleEnemy_KongRoom2 = auto()  # Kremling, 32
    AztecTempleEnemy_KongRoom3 = auto()  # Kremling, 33
    AztecTempleEnemy_KongRoom4 = auto()  # Klaptrap, 34
    AztecTempleEnemy_Underwater = auto()  # Shuri, 37

    # Factory
    # Main
    FactoryMainEnemy_CandyCranky0 = auto()  # Kremling, 33
    FactoryMainEnemy_CandyCranky1 = auto()  # Kremling, 72
    FactoryMainEnemy_LobbyLeft = auto()  # Robo-Kremling, 74
    FactoryMainEnemy_LobbyRight = auto()  # Robo-Kremling, 58
    FactoryMainEnemy_StorageRoom = auto()  # Robo-Zinger, 91
    FactoryMainEnemy_BlockTower0 = auto()  # Mr Dice (0x59), 78
    FactoryMainEnemy_BlockTower1 = auto()  # Sir Domino, 79
    FactoryMainEnemy_BlockTower2 = auto()  # Mr Dice (0x59), 80
    FactoryMainEnemy_TunnelToHatch = auto()  # Robo-Kremling, 59
    FactoryMainEnemy_TunnelToProd0 = auto()  # Kremling, 63
    FactoryMainEnemy_TunnelToProd1 = auto()  # Robo-Kremling, 73
    FactoryMainEnemy_TunnelToBlockTower = auto()  # Robo-Kremling, 84
    FactoryMainEnemy_TunnelToRace0 = auto()  # Robo-Kremling, 87
    FactoryMainEnemy_TunnelToRace1 = auto()  # Robo-Zinger, 88
    FactoryMainEnemy_LowWarp4 = auto()  # Robo-Kremling, 66
    FactoryMainEnemy_DiddySwitch = auto()  # Robo-Zinger, 67
    FactoryMainEnemy_ToBlockTowerTunnel = auto()  # Robo-Zinger, 62
    FactoryMainEnemy_DarkRoom0 = auto()  # Robo-Zinger, 70
    FactoryMainEnemy_DarkRoom1 = auto()  # Robo-Zinger, 71
    FactoryMainEnemy_BHDM0 = auto()  # Mr Dice (0x57), 35
    FactoryMainEnemy_BHDM1 = auto()  # Sir Domino, 36
    FactoryMainEnemy_BHDM2 = auto()  # Sir Domino, 37
    FactoryMainEnemy_BHDM3 = auto()  # Mr Dice (0x57), 38
    FactoryMainEnemy_BHDM4 = auto()  # Mr Dice (0x57), 39
    FactoryMainEnemy_BHDM5 = auto()  # Ruler, 40
    FactoryMainEnemy_BHDM6 = auto()  # Ruler, 41
    FactoryMainEnemy_BHDM7 = auto()  # Mr Dice (0x59), 42
    FactoryMainEnemy_BHDM8 = auto()  # Sir Domino, 43
    FactoryMainEnemy_BHDM9 = auto()  # Sir Domino, 44
    FactoryMainEnemy_1342Gauntlet0 = auto()  # Robo-Zinger, 49
    FactoryMainEnemy_1342Gauntlet1 = auto()  # Robo-Kremling, 50
    FactoryMainEnemy_1342Gauntlet2 = auto()  # Robo-Kremling, 51
    FactoryMainEnemy_3124Gauntlet0 = auto()  # Mr Dice (0x59), 52
    FactoryMainEnemy_3124Gauntlet1 = auto()  # Sir Domino, 53
    FactoryMainEnemy_3124Gauntlet2 = auto()  # Mr Dice (0x59), 54
    FactoryMainEnemy_4231Gauntlet0 = auto()  # Robo-Kremling, 55
    FactoryMainEnemy_4231Gauntlet1 = auto()  # Robo-Kremling, 56

    # Lobby
    FactoryLobbyEnemy_Enemy0 = auto()  # Robo-Zinger, 1

    # Galleon
    # Main
    GalleonMainEnemy_ChestRoom0 = auto()  # Klobber, 12
    GalleonMainEnemy_ChestRoom1 = auto()  # Kaboom, 18
    GalleonMainEnemy_NearVineCannon = auto()  # Kaboom, 16
    GalleonMainEnemy_CrankyCannon = auto()  # Kaboom, 17
    GalleonMainEnemy_Submarine = auto()  # Pufftup, 14
    GalleonMainEnemy_5DS0 = auto()  # Shuri, 19
    GalleonMainEnemy_5DS1 = auto()  # Shuri, 20
    GalleonMainEnemy_PeanutTunnel = auto()  # Kosha, 26
    GalleonMainEnemy_CoconutTunnel = auto()  # Kremling, 27

    # Lighthouse
    GalleonLighthouseEnemy_Enemy0 = auto()  # Klump, 1
    GalleonLighthouseEnemy_Enemy1 = auto()  # Klump, 2

    # 5DS Diddy, Lanky, Chunky
    Galleon5DSDLCEnemy_Diddy = auto()  # Pufftup, 4
    Galleon5DSDLCEnemy_Chunky = auto()  # Pufftup, 5
    Galleon5DSDLCEnemy_Lanky = auto()  # Pufftup, 6

    # 5DS DK, Tiny
    Galleon5DSDTEnemy_DK0 = auto()  # Shuri, 4
    Galleon5DSDTEnemy_DK1 = auto()  # Shuri, 5
    Galleon5DSDTEnemy_DK2 = auto()  # Shuri, 6
    Galleon5DSDTEnemy_TinyCage = auto()  # Shuri, 9
    Galleon5DSDTEnemy_TinyBed = auto()  # Shuri, 10

    # 2DS
    Galleon2DSEnemy_Tiny0 = auto()  # Gimpfish, 3
    Galleon2DSEnemy_Tiny1 = auto()  # Gimpfish, 4

    # Submarine
    GalleonSubEnemy_Enemy0 = auto()  # Pufftup, 1
    GalleonSubEnemy_Enemy1 = auto()  # Pufftup, 3
    GalleonSubEnemy_Enemy2 = auto()  # Pufftup, 4
    GalleonSubEnemy_Enemy3 = auto()  # Pufftup, 6

    # Fungi
    # Main
    ForestMainEnemy_HollowTree0 = auto()  # Klump, 5
    ForestMainEnemy_HollowTree1 = auto()  # Klump, 30
    ForestMainEnemy_HollowTreeEntrance = auto()  # Zinger (0x1C), 34
    ForestMainEnemy_TreeMelonCrate0 = auto()  # Zinger (0x1C), 31
    ForestMainEnemy_TreeMelonCrate1 = auto()  # Zinger (0x1C), 32
    ForestMainEnemy_TreeMelonCrate2 = auto()  # Zinger (0x1C), 33
    ForestMainEnemy_AppleGauntlet0 = auto()  # Tomato, 9
    ForestMainEnemy_AppleGauntlet1 = auto()  # Tomato, 10
    ForestMainEnemy_AppleGauntlet2 = auto()  # Tomato, 11
    ForestMainEnemy_AppleGauntlet3 = auto()  # Tomato, 12
    ForestMainEnemy_NearBeanstalk0 = auto()  # Klump, 55
    ForestMainEnemy_NearBeanstalk1 = auto()  # Klump, 56
    ForestMainEnemy_GreenTunnel = auto()  # Zinger (0x1C), 57
    ForestMainEnemy_NearLowWarp5 = auto()  # Mushroom, 23
    ForestMainEnemy_NearPinkTunnelBounceTag = auto()  # Mushroom, 24
    ForestMainEnemy_NearGMRocketbarrel = auto()  # Mushroom, 25
    ForestMainEnemy_BetweenRBAndYellowTunnel = auto()  # Zinger (0x1C), 26
    ForestMainEnemy_NearCranky = auto()  # Zinger (0x1C), 27
    ForestMainEnemy_NearPinkTunnelGM = auto()  # Zinger (0x1C), 28
    ForestMainEnemy_GMRearTag = auto()  # Zinger (0x1C), 29
    ForestMainEnemy_NearFacePuzzle = auto()  # Zinger (0x1C), 51
    ForestMainEnemy_NearCrown = auto()  # Zinger (0x1C), 52
    ForestMainEnemy_NearHighWarp5 = auto()  # Zinger (0x1C), 53
    ForestMainEnemy_TopOfMushroom = auto()  # Klump, 54
    ForestMainEnemy_NearAppleDropoff = auto()  # Zinger (0x1C), 48
    ForestMainEnemy_NearDKPortal = auto()  # Zinger (0x1C), 49
    ForestMainEnemy_NearWellTag = auto()  # Zinger (0x1C), 50
    ForestMainEnemy_YellowTunnel0 = auto()  # Mushroom, 22
    ForestMainEnemy_YellowTunnel1 = auto()  # Zinger (0x1C), 41
    ForestMainEnemy_YellowTunnel2 = auto()  # Zinger (0x1C), 42
    ForestMainEnemy_YellowTunnel3 = auto()  # Klump, 43
    ForestMainEnemy_NearSnide = auto()  # Mushroom, 35
    ForestMainEnemy_NearIsoCoin = auto()  # Zinger (0x1C), 38
    ForestMainEnemy_NearBBlast = auto()  # Zinger (0x1C), 39
    ForestMainEnemy_NearDarkAttic = auto()  # Klump, 44
    ForestMainEnemy_NearWellExit = auto()  # Zinger (0x1C), 47
    ForestMainEnemy_NearBlueTunnel = auto()  # Klump, 59
    ForestMainEnemy_Thornvine0 = auto()  # Klump, 45
    ForestMainEnemy_Thornvine1 = auto()  # Klump, 46
    ForestMainEnemy_Thornvine2 = auto()  # Zinger (0x1C), 60
    ForestMainEnemy_ThornvineEntrance = auto()  # Klump, 58

    # Anthill
    ForestAnthillEnemy_Gauntlet0 = auto()  # P Klaptrap, 1
    ForestAnthillEnemy_Gauntlet1 = auto()  # P Klaptrap, 2
    ForestAnthillEnemy_Gauntlet2 = auto()  # P Klaptrap, 3
    ForestAnthillEnemy_Gauntlet3 = auto()  # P Klaptrap, 4

    # Winch Room
    ForestWinchEnemy_Enemy = auto()  # Bat, 1

    # Thornvine Barn
    ForestThornBarnEnemy_Enemy = auto()  # Kosha, 1

    # Mill Front
    ForestMillFrontEnemy_Enemy = auto()  # Zinger (0x1C), 1

    # Mill Rear
    ForestMillRearEnemy_Enemy = auto()  # Zinger (0x1C), 1

    # Giant Mushroom
    ForestGMEnemy_AboveNightDoor = auto()  # Klump, 2
    ForestGMEnemy_Path0 = auto()  # Zinger (0x1C), 3
    ForestGMEnemy_Path1 = auto()  # Zinger (0x1C), 4

    # Lanky Attic
    ForestLankyAtticEnemy_Gauntlet0 = auto()  # Bat, 1
    ForestLankyAtticEnemy_Gauntlet1 = auto()  # Bat, 2
    ForestLankyAtticEnemy_Gauntlet2 = auto()  # Bat, 3

    # Mush Leap
    ForestLeapEnemy_Enemy0 = auto()  # Zinger (0x1C), 1
    ForestLeapEnemy_Enemy1 = auto()  # Zinger (0x1C), 2

    # Face Puzzle
    ForestFacePuzzleEnemy_Enemy = auto()  # Zinger (0x1C), 1

    # Spider Boss
    ForestSpiderEnemy_Gauntlet0 = auto()  # Small Spider, 2
    ForestSpiderEnemy_Gauntlet1 = auto()  # Small Spider, 3
    ForestSpiderEnemy_Gauntlet2 = auto()  # Small Spider, 4

    # Caves
    # Main
    CavesMainEnemy_Start = auto()  # Kremling, 10
    CavesMainEnemy_NearIceCastle = auto()  # Beaver, 15
    CavesMainEnemy_Outside5DC = auto()  # Zinger (0x1C), 17
    CavesMainEnemy_1DCWaterfall = auto()  # Zinger (0x1C), 18
    CavesMainEnemy_NearFunky = auto()  # Zinger (0x5), 19
    CavesMainEnemy_NearSnide = auto()  # Kosha, 27
    CavesMainEnemy_NearBonusRoom = auto()  # Kosha, 28
    CavesMainEnemy_1DCHeadphones = auto()  # Kosha, 29
    CavesMainEnemy_GiantKosha = auto()  # Kosha, 31

    # DK 5DI
    Caves5DIDKEnemy_Right = auto()  # Kosha, 1
    Caves5DIDKEnemy_Left = auto()  # Kosha, 3

    # Lanky 5DI
    Caves5DILankyEnemy_First0 = auto()  # Beaver, 1
    Caves5DILankyEnemy_First1 = auto()  # Beaver, 2
    Caves5DILankyEnemy_Second0 = auto()  # Kremling, 3
    Caves5DILankyEnemy_Second1 = auto()  # Kremling, 4
    Caves5DILankyEnemy_Second2 = auto()  # Kremling, 5

    # Tiny 5DI
    Caves5DITinyEnemy_BigEnemy = auto()  # Kosha, 2

    # Chunky 5DI
    Caves5DIChunkyEnemy_Gauntlet00 = auto()  # Fireball, 2
    Caves5DIChunkyEnemy_Gauntlet01 = auto()  # Fireball, 3
    Caves5DIChunkyEnemy_Gauntlet02 = auto()  # Fireball, 4
    Caves5DIChunkyEnemy_Gauntlet03 = auto()  # Fireball, 5
    Caves5DIChunkyEnemy_Gauntlet04 = auto()  # Fireball, 6

    # Lanky 1DC
    Caves1DCEnemy_Near = auto()  # Kosha, 2
    Caves1DCEnemy_Far = auto()  # Kosha, 1

    # DK 5DC
    Caves5DCDKEnemy_Gauntlet0 = auto()  # Zinger (0x1C), 1
    Caves5DCDKEnemy_Gauntlet1 = auto()  # Zinger (0x1C), 2
    Caves5DCDKEnemy_Gauntlet2 = auto()  # Zinger (0x1C), 3
    Caves5DCDKEnemy_Gauntlet3 = auto()  # Zinger (0x1C), 4
    Caves5DCDKEnemy_Gauntlet4 = auto()  # Zinger (0x1C), 5
    Caves5DCDKEnemy_Gauntlet5 = auto()  # Zinger (0x1C), 6

    # Diddy Enemies 5DC
    Caves5DCDiddyLowEnemy_CloseRight = auto()  # Klump, 1
    Caves5DCDiddyLowEnemy_FarRight = auto()  # Kremling, 2
    Caves5DCDiddyLowEnemy_CloseLeft = auto()  # Klump, 3
    Caves5DCDiddyLowEnemy_FarLeft = auto()  # Kremling, 4
    Caves5DCDiddyLowEnemy_Center0 = auto()  # Klobber, 5
    Caves5DCDiddyLowEnemy_Center1 = auto()  # Klobber, 6
    Caves5DCDiddyLowEnemy_Center2 = auto()  # Klobber, 7
    Caves5DCDiddyLowEnemy_Center3 = auto()  # Klobber, 8

    # Diddy Candle 5DC
    Caves5DCDiddyUpperEnemy_Enemy0 = auto()  # Kosha, 1
    Caves5DCDiddyUpperEnemy_Enemy1 = auto()  # Kosha, 2

    # Tiny 5DC
    Caves5DCTinyEnemy_Gauntlet0 = auto()  # P Klaptrap, 1
    Caves5DCTinyEnemy_Gauntlet1 = auto()  # P Klaptrap, 2
    Caves5DCTinyEnemy_Gauntlet2 = auto()  # P Klaptrap, 3
    Caves5DCTinyEnemy_Gauntlet3 = auto()  # P Klaptrap, 4
    Caves5DCTinyEnemy_Gauntlet4 = auto()  # P Klaptrap, 5

    # Castle
    # Main
    CastleMainEnemy_NearBridge0 = auto()  # Krossbones, 4
    CastleMainEnemy_NearBridge1 = auto()  # Krossbones, 5
    CastleMainEnemy_WoodenExtrusion0 = auto()  # Kosha, 6
    CastleMainEnemy_WoodenExtrusion1 = auto()  # Kosha, 7
    CastleMainEnemy_NearShed = auto()  # Krossbones, 8
    CastleMainEnemy_NearLibrary = auto()  # Krossbones, 9
    CastleMainEnemy_NearTower = auto()  # Kosha, 10
    CastleMainEnemy_MuseumSteps = auto()  # Ghost, 11
    CastleMainEnemy_NearLowCave = auto()  # Krossbones, 12
    CastleMainEnemy_PathToLowKasplat = auto()  # Krossbones, 13
    CastleMainEnemy_LowTnS = auto()  # Krossbones, 14
    CastleMainEnemy_PathToDungeon = auto()  # Krossbones, 15
    CastleMainEnemy_NearHeadphones = auto()  # Krossbones, 16

    # Lobby
    CastleLobbyEnemy_Left = auto()  # Kosha, 2
    CastleLobbyEnemy_FarRight = auto()  # Kosha, 3
    CastleLobbyEnemy_NearRight = auto()  # Kosha, 4

    # Ballroom
    CastleBallroomEnemy_Board00 = auto()  # Krossbones, 1
    CastleBallroomEnemy_Board01 = auto()  # Ghost, 2
    CastleBallroomEnemy_Board02 = auto()  # Ghost, 3
    CastleBallroomEnemy_Board03 = auto()  # Ghost, 4
    CastleBallroomEnemy_Board04 = auto()  # Krossbones, 5
    CastleBallroomEnemy_Start = auto()  # Kosha, 6

    # Dungeon
    CastleDungeonEnemy_FaceRoom = auto()  # Krossbones, 1
    CastleDungeonEnemy_ChairRoom = auto()  # Kosha, 2
    CastleDungeonEnemy_OutsideLankyRoom = auto()  # Kosha, 3

    # Shed
    CastleShedEnemy_Gauntlet00 = auto()  # Bat, 1
    CastleShedEnemy_Gauntlet01 = auto()  # Bat, 2
    CastleShedEnemy_Gauntlet02 = auto()  # Bat, 3
    CastleShedEnemy_Gauntlet03 = auto()  # Bat, 4
    CastleShedEnemy_Gauntlet04 = auto()  # Bat, 5

    # Lower Cave
    CastleLowCaveEnemy_NearCrypt = auto()  # Kosha, 3
    CastleLowCaveEnemy_StairRight = auto()  # Kosha, 4
    CastleLowCaveEnemy_StairLeft = auto()  # Krossbones, 5
    CastleLowCaveEnemy_NearMausoleum = auto()  # Bat, 6
    CastleLowCaveEnemy_NearFunky = auto()  # Bat, 7
    CastleLowCaveEnemy_NearTag = auto()  # Bat, 8

    # Crypt
    CastleCryptEnemy_DiddyCoffin0 = auto()  # Ghost, 1
    CastleCryptEnemy_DiddyCoffin1 = auto()  # Ghost, 2
    CastleCryptEnemy_DiddyCoffin2 = auto()  # Krossbones, 3
    CastleCryptEnemy_DiddyCoffin3 = auto()  # Ghost, 4
    CastleCryptEnemy_ChunkyCoffin0 = auto()  # Krossbones, 5
    CastleCryptEnemy_ChunkyCoffin1 = auto()  # Krossbones, 6
    CastleCryptEnemy_ChunkyCoffin2 = auto()  # Ghost, 7
    CastleCryptEnemy_ChunkyCoffin3 = auto()  # Krossbones, 8
    CastleCryptEnemy_MinecartEntry = auto()  # Krossbones, 9
    CastleCryptEnemy_Fork = auto()  # Krossbones, 10
    CastleCryptEnemy_NearDiddy = auto()  # Krossbones, 11
    CastleCryptEnemy_NearChunky = auto()  # Krossbones, 12

    # Mausoleum
    CastleMausoleumEnemy_TinyPath = auto()  # Krossbones, 1
    CastleMausoleumEnemy_LankyPath0 = auto()  # Krossbones, 2
    CastleMausoleumEnemy_LankyPath1 = auto()  # Krossbones, 3

    # Upper Cave
    CastleUpperCaveEnemy_NearDungeon = auto()  # Bat, 3
    CastleUpperCaveEnemy_Pit = auto()  # Bat, 4
    CastleUpperCaveEnemy_NearPit = auto()  # Bat, 5
    CastleUpperCaveEnemy_NearEntrance = auto()  # Krossbones, 6

    # Kut Out
    CastleKKOEnemy_CenterEnemy = auto()  # Ghost, 7
    CastleKKOEnemy_WaterEnemy00 = auto()  # Pufftup, 8
    CastleKKOEnemy_WaterEnemy01 = auto()  # Pufftup, 9
    CastleKKOEnemy_WaterEnemy02 = auto()  # Pufftup, 10
    CastleKKOEnemy_WaterEnemy03 = auto()  # Pufftup, 11

    # Library
    CastleLibraryEnemy_Gauntlet00 = auto()  # Krossbones, 1
    CastleLibraryEnemy_Gauntlet01 = auto()  # Ghost, 2
    CastleLibraryEnemy_Gauntlet02 = auto()  # Ghost, 3
    CastleLibraryEnemy_Gauntlet03 = auto()  # Krossbones, 4
    CastleLibraryEnemy_Corridor00 = auto()  # Book, 5
    CastleLibraryEnemy_Corridor01 = auto()  # Book, 7
    CastleLibraryEnemy_Corridor02 = auto()  # Book, 8
    CastleLibraryEnemy_Corridor03 = auto()  # Book, 9
    CastleLibraryEnemy_Corridor04 = auto()  # Book, 10
    CastleLibraryEnemy_Corridor05 = auto()  # Book, 11
    CastleLibraryEnemy_ForkLeft0 = auto()  # Bat, 12
    CastleLibraryEnemy_ForkLeft1 = auto()  # Bat, 15
    CastleLibraryEnemy_ForkCenter = auto()  # Bat, 13
    CastleLibraryEnemy_ForkRight = auto()  # Bat, 14

    # Museum
    CastleMuseumEnemy_MainFloor0 = auto()  # Ghost, 1
    CastleMuseumEnemy_MainFloor1 = auto()  # Ghost, 2
    CastleMuseumEnemy_MainFloor2 = auto()  # Ghost, 3
    CastleMuseumEnemy_MainFloor3 = auto()  # Ghost, 4
    CastleMuseumEnemy_Start = auto()  # Kosha, 6

    # Tower
    CastleTowerEnemy_Gauntlet0 = auto()  # Ghost, 1
    CastleTowerEnemy_Gauntlet1 = auto()  # Ghost, 2
    CastleTowerEnemy_Gauntlet2 = auto()  # Ghost, 3
    CastleTowerEnemy_Gauntlet3 = auto()  # Ghost, 4
    CastleTowerEnemy_Gauntlet4 = auto()  # Ghost, 5

    # Trash Can
    CastleTrashEnemy_Gauntlet0 = auto()  # Bug, 1
    CastleTrashEnemy_Gauntlet1 = auto()  # Bug, 2
    CastleTrashEnemy_Gauntlet2 = auto()  # Bug, 3
    CastleTrashEnemy_Gauntlet3 = auto()  # Bug, 4
    CastleTrashEnemy_Gauntlet4 = auto()  # Bug, 5

    # Tree
    CastleTreeEnemy_StartRoom0 = auto()  # Bat, 3
    CastleTreeEnemy_StartRoom1 = auto()  # Bat, 5

    # Helm
    # Main
    HelmMainEnemy_Start0 = auto()  # Klaptrap, 2
    HelmMainEnemy_Start1 = auto()  # Kremling, 3
    HelmMainEnemy_Hill = auto()  # Klump, 4
    HelmMainEnemy_SwitchRoom0 = auto()  # Klump, 5
    HelmMainEnemy_SwitchRoom1 = auto()  # Klaptrap, 16
    HelmMainEnemy_MiniRoom0 = auto()  # Kremling, 7
    HelmMainEnemy_MiniRoom1 = auto()  # Kremling, 8
    HelmMainEnemy_MiniRoom2 = auto()  # Klaptrap, 17
    HelmMainEnemy_MiniRoom3 = auto()  # Klaptrap, 18
    HelmMainEnemy_DKRoom = auto()  # Kremling, 10
    HelmMainEnemy_ChunkyRoom0 = auto()  # Kremling, 11
    HelmMainEnemy_ChunkyRoom1 = auto()  # Klaptrap, 19
    HelmMainEnemy_TinyRoom = auto()  # Klump, 12
    HelmMainEnemy_LankyRoom0 = auto()  # Klump, 13
    HelmMainEnemy_LankyRoom1 = auto()  # Klaptrap, 20
    HelmMainEnemy_DiddyRoom0 = auto()  # Klaptrap, 21
    HelmMainEnemy_DiddyRoom1 = auto()  # Klaptrap, 22
    HelmMainEnemy_NavRight = auto()  # Kremling, 23
    HelmMainEnemy_NavLeft = auto()  # Klaptrap, 24

    # Isles
    # Main
    IslesMainEnemy_PineappleCage0 = auto()  # Beaver, 1
    IslesMainEnemy_FungiCannon0 = auto()  # Beaver, 2
    IslesMainEnemy_JapesEntrance = auto()  # Beaver, 3
    IslesMainEnemy_MonkeyportPad = auto()  # Kremling, 4
    IslesMainEnemy_UpperFactoryPath = auto()  # Kremling, 5
    IslesMainEnemy_NearAztec = auto()  # Zinger (0x5), 8
    IslesMainEnemy_FungiCannon1 = auto()  # Zinger (0x5), 9
    IslesMainEnemy_PineappleCage1 = auto()  # Zinger (0x5), 10
    IslesMainEnemy_LowerFactoryPath0 = auto()  # Zinger (0x1C), 11
    IslesMainEnemy_LowerFactoryPath1 = auto()  # Zinger (0x1C), 12

    # Progressive Hint locations must remain grouped together in this specific order for progressive hint location logic
    ProgressiveHint_01 = auto()  # ID: 1045
    ProgressiveHint_02 = auto()
    ProgressiveHint_03 = auto()
    ProgressiveHint_04 = auto()
    ProgressiveHint_05 = auto()
    ProgressiveHint_06 = auto()
    ProgressiveHint_07 = auto()
    ProgressiveHint_08 = auto()
    ProgressiveHint_09 = auto()
    ProgressiveHint_10 = auto()
    ProgressiveHint_11 = auto()
    ProgressiveHint_12 = auto()
    ProgressiveHint_13 = auto()
    ProgressiveHint_14 = auto()
    ProgressiveHint_15 = auto()
    ProgressiveHint_16 = auto()
    ProgressiveHint_17 = auto()
    ProgressiveHint_18 = auto()
    ProgressiveHint_19 = auto()
    ProgressiveHint_20 = auto()
    ProgressiveHint_21 = auto()
    ProgressiveHint_22 = auto()
    ProgressiveHint_23 = auto()
    ProgressiveHint_24 = auto()
    ProgressiveHint_25 = auto()
    ProgressiveHint_26 = auto()
    ProgressiveHint_27 = auto()
    ProgressiveHint_28 = auto()
    ProgressiveHint_29 = auto()
    ProgressiveHint_30 = auto()
    ProgressiveHint_31 = auto()
    ProgressiveHint_32 = auto()
    ProgressiveHint_33 = auto()
    ProgressiveHint_34 = auto()
    ProgressiveHint_35 = auto()  # ID: 1079
