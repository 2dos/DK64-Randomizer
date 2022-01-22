"""Event enum."""
from enum import IntEnum, auto


class Events(IntEnum):
    """Event enum."""

    # DK Isles events
    IslesDiddyBarrelSpawn = auto()
    IslesChunkyBarrelSpawn = auto()
    KLumsyTalkedTo = auto()
    FirstKey = auto()
    SecondKey = auto()
    FourthKey = auto()
    FifthKey = auto()
    SeventhKey = auto()
    EigthKey = auto()

    # Jungle Japes events
    Rambi = auto()
    JapesDonkeySwitch = auto()
    JapesDiddySwitch1 = auto()
    JapesLankySwitch = auto()
    JapesTinySwitch = auto()
    JapesChunkySwitch = auto()
    JapesDiddySwitch2 = auto()

    # Angry Aztec events
    FedTotem = auto()
    LlamaFreed = auto()
    AztecDonkeySwitch = auto()

    # Frantic Factory events
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
    WaterSwitch = auto()
    LighthouseEnguarde = auto()
    SealReleased = auto()
    MechafishSummoned = auto()
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

    # No Creepy Castle Events

    # Hideout Helm Events
    HelmDoorsOpened = auto()
    HelmDonkeyDone = auto()
    HelmChunkyDone = auto()
    HelmTinyDone = auto()
    HelmLankyDone = auto()
    HelmDiddyDone = auto()
    HelmKeyAccess = auto()

    # Level entered events for shops
    JapesEntered = auto()
    AztecEntered = auto()
    FactoryEntered = auto()
    GalleonEntered = auto()
    ForestEntered = auto()
    CavesEntered = auto()
    CastleEntered = auto()
