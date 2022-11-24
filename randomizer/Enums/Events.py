"""Event enum."""
from enum import IntEnum, auto


class Events(IntEnum):
    """Event enum."""

    # DK Isles events
    IslesDiddyBarrelSpawn = auto()
    IslesChunkyBarrelSpawn = auto()
    KLumsyTalkedTo = auto()
    JapesKeyTurnedIn = auto()
    AztecKeyTurnedIn = auto()
    FactoryKeyTurnedIn = auto()
    GalleonKeyTurnedIn = auto()
    ForestKeyTurnedIn = auto()
    CavesKeyTurnedIn = auto()
    CastleKeyTurnedIn = auto()
    HelmKeyTurnedIn = auto()

    # Jungle Japes events
    Rambi = auto()
    JapesFreeKongOpenGates = auto()
    JapesDonkeySwitch = auto()
    JapesDiddySwitch1 = auto()
    JapesLankySwitch = auto()
    JapesTinySwitch = auto()
    JapesChunkySwitch = auto()
    JapesDiddySwitch2 = auto()
    JapesSpawnW5 = auto()
    JapesMountainTopGB = auto()

    # Angry Aztec events
    FedTotem = auto()
    LlamaFreed = auto()
    AztecDonkeySwitch = auto()
    AztecLlamaSpit = auto()

    # Frantic Factory events
    HatchOpened = auto()
    DartsPlayed = auto()
    MainCoreActivated = auto()
    ArcadeLeverSpawned = auto()
    TestingGateOpened = auto()
    DiddyCoreSwitch = auto()
    LankyCoreSwitch = auto()
    TinyCoreSwitch = auto()
    ChunkyCoreSwitch = auto()

    # Gloomy Galleon events
    GalleonLankySwitch = auto()
    GalleonTinySwitch = auto()
    LighthouseGateOpened = auto()
    ShipyardGateOpened = auto()
    WaterSwitch = auto()
    LighthouseEnguarde = auto()
    SealReleased = auto()
    MechafishSummoned = auto()
    GalleonDonkeyPad = auto()
    GalleonDiddyPad = auto()
    GalleonLankyPad = auto()
    GalleonTinyPad = auto()
    GalleonChunkyPad = auto()
    ActivatedLighthouse = auto()
    ShipyardEnguarde = auto()
    ShipyardTreasureRoomOpened = auto()
    TreasureRoomTeleporterUnlocked = auto()
    PearlsCollected = auto()

    # Fungi Forest events
    Night = auto()
    WormGatesOpened = auto()
    HollowTreeGateOpened = auto()
    MushroomCannonsSpawned = auto()
    DonkeyMushroomSwitch = auto()
    Bean = auto()
    GrinderActivated = auto()
    MillBoxBroken = auto()
    ConveyorActivated = auto()
    WinchRaised = auto()

    # Crystal Caves events
    CavesSmallBoulderButton = auto()
    CavesLargeBoulderButton = auto()
    GiantKoshaDefeated = auto()

    # Creepy Castle Events
    CastleTreeOpened = auto()

    # Hideout Helm Events
    HelmDoorsOpened = auto()
    HelmDonkeyDone = auto()
    HelmChunkyDone = auto()
    HelmTinyDone = auto()
    HelmLankyDone = auto()
    HelmDiddyDone = auto()
    HelmKeyAccess = auto()

    # K Rool Phases
    KRoolDonkey = auto()
    KRoolDiddy = auto()
    KRoolLanky = auto()
    KRoolTiny = auto()
    KRoolChunky = auto()
    KRoolDefeated = auto()

    # Level entered events for shops
    JapesEntered = auto()
    AztecEntered = auto()
    FactoryEntered = auto()
    GalleonEntered = auto()
    ForestEntered = auto()
    CavesEntered = auto()
    CastleEntered = auto()
