from enum import Enum, auto

class Events(Enum):

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
    LighthouseEngarde = auto()
    SealReleased = auto()
    MechafishSummoned = auto()
    GalleonChunkyPad = auto()
    ActivateLighthouse = auto()
    ShipyardEngarde = auto()
    TreasureRoomTeleporterUnlocked = auto()
    PearlsCollected = auto()
    
    # Fungi Forest events
    Night = auto()
    ForestCannonsSpawned = auto()
    DonkeyMushroomSwitch = auto()
    GrinderActivated = auto()
    MillBoxBroken = auto()
    ConveyorActivated = auto()
    WenchRaised = auto()
    
    # Crystal Caves events
    CavesSmallBoulderButton = auto()
    CavesLargeBoulderButton = auto()
    GiantKoshaDefeated = auto()
    
    # No Creepy Castle Events

    # Hideout Helm Events
    HideoutDoorsOpened = auto()
    HideoutDonkeyDone = auto()
    HideoutChunkyDone = auto()
    HideoutTinyDone = auto()
    HideoutLankyDone = auto()
    HideoutDiddyDone = auto()
    HideoutKeyAccess = auto()
    