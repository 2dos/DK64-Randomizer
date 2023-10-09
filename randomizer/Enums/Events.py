"""Event enum."""
from enum import Enum, auto


class Events(Enum):
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
    PearlsCollected = auto()
    GalleonCannonRoomOpened = auto()

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
    CavesMonkeyportAccess = auto()

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

    # Warp tagged events
    JapesW1aTagged = auto()
    JapesW1bTagged = auto()
    JapesW2aTagged = auto()
    JapesW2bTagged = auto()
    JapesW3aTagged = auto()
    JapesW3bTagged = auto()
    JapesW4aTagged = auto()
    JapesW4bTagged = auto()
    JapesW5aTagged = auto()
    JapesW5bTagged = auto()
    AztecW1aTagged = auto()
    AztecW1bTagged = auto()
    AztecW2aTagged = auto()
    AztecW2bTagged = auto()
    AztecW3aTagged = auto()
    AztecW3bTagged = auto()
    AztecW4aTagged = auto()
    AztecW4bTagged = auto()
    AztecW5aTagged = auto()
    AztecW5bTagged = auto()
    LlamaW1aTagged = auto()
    LlamaW1bTagged = auto()
    LlamaW2aTagged = auto()
    LlamaW2bTagged = auto()
    FactoryW1aTagged = auto()
    FactoryW1bTagged = auto()
    FactoryW2aTagged = auto()
    FactoryW2bTagged = auto()
    FactoryW3aTagged = auto()
    FactoryW3bTagged = auto()
    FactoryW4aTagged = auto()
    FactoryW4bTagged = auto()
    FactoryW5aTagged = auto()
    FactoryW5bTagged = auto()
    GalleonW1aTagged = auto()
    GalleonW1bTagged = auto()
    GalleonW2aTagged = auto()
    GalleonW2bTagged = auto()
    GalleonW3aTagged = auto()
    GalleonW3bTagged = auto()
    GalleonW4aTagged = auto()
    GalleonW4bTagged = auto()
    GalleonW5aTagged = auto()
    GalleonW5bTagged = auto()
    ForestW1aTagged = auto()
    ForestW1bTagged = auto()
    ForestW2aTagged = auto()
    ForestW2bTagged = auto()
    ForestW3aTagged = auto()
    ForestW3bTagged = auto()
    ForestW4aTagged = auto()
    ForestW4bTagged = auto()
    ForestW5aTagged = auto()
    ForestW5bTagged = auto()
    CavesW1aTagged = auto()
    CavesW1bTagged = auto()
    CavesW2aTagged = auto()
    CavesW2bTagged = auto()
    CavesW3aTagged = auto()
    CavesW3bTagged = auto()
    CavesW4aTagged = auto()
    CavesW4bTagged = auto()
    CavesW5aTagged = auto()
    CavesW5bTagged = auto()
    CastleW1aTagged = auto()
    CastleW1bTagged = auto()
    CastleW2aTagged = auto()
    CastleW2bTagged = auto()
    CastleW3aTagged = auto()
    CastleW3bTagged = auto()
    CastleW4aTagged = auto()
    CastleW4bTagged = auto()
    CastleW5aTagged = auto()
    CastleW5bTagged = auto()
    CryptW1aTagged = auto()
    CryptW1bTagged = auto()
    CryptW2aTagged = auto()
    CryptW2bTagged = auto()
    CryptW3aTagged = auto()
    CryptW3bTagged = auto()
    IslesW1aTagged = auto()
    IslesW1bTagged = auto()
    IslesW2aTagged = auto()
    IslesW2bTagged = auto()
    IslesW3aTagged = auto()
    IslesW3bTagged = auto()
    IslesW4aTagged = auto()
    IslesW4bTagged = auto()
    IslesW5aTagged = auto()
    IslesW5bTagged = auto()

    # Lobbies Entered Events - keep these in order!
    JapesLobbyAccessed = auto()
    AztecLobbyAccessed = auto()
    FactoryLobbyAccessed = auto()
    GalleonLobbyAccessed = auto()
    ForestLobbyAccessed = auto()
    CavesLobbyAccessed = auto()
    CastleLobbyAccessed = auto()
    HelmLobbyAccessed = auto()

    def __eq__(self, other):
        """Return True if self is equal to other."""
        if isinstance(other, type(self)):
            return self is other
        elif isinstance(other, int):
            return self.value == other
        return NotImplemented

    def __ne__(self, other):
        """Return True if self is not equal to other."""
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result

    def __mod__(self, other):
        """Return the modulo of self and other."""
        if isinstance(other, int):
            return self.value % other
        raise TypeError("Unsupported operand types for % ({} and {})".format(type(self).__name__, type(other).__name__))

    def to_bytes(self, length, byteorder="big", signed=False):
        """Return the bytes representation of self."""
        return self.value.to_bytes(length, byteorder, signed=signed)

    def __sub__(self, other):
        """Return the subtraction of self and other."""
        if isinstance(other, int):
            return self.value - other
        raise TypeError("Unsupported operand types for - ({} and {})".format(type(self).__name__, type(other).__name__))

    def __ge__(self, other):
        """Return True if self is greater than or equal to other."""
        if isinstance(other, type(self)):
            return self.value >= other.value
        elif isinstance(other, int):
            return self.value >= other
        return NotImplemented

    def __le__(self, other):
        """Return True if self is less than or equal to other."""
        if isinstance(other, type(self)):
            return self.value <= other.value
        elif isinstance(other, int):
            return self.value <= other
        return NotImplemented

    def __hash__(self):
        """Return the hash value of self."""
        return hash(self.value)

    def __index__(self):
        """Return the index of self."""
        return self.value

    def __lt__(self, other):
        """Return True if self is less than other."""
        if isinstance(other, int):
            return self.value < other
        return NotImplemented

    def __gt__(self, other):
        """Return True if self is greater than other."""
        if isinstance(other, type(self)):
            return self.value > other.value
        elif isinstance(other, int):
            return self.value > other
        return NotImplemented

    def __lshift__(self, other):
        """Return the left shift of self and other."""
        if isinstance(other, int):
            return self.value << other
        raise TypeError("Unsupported operand types for << ({} and {})".format(type(self).__name__, type(other).__name__))

    def __add__(self, other):
        """Return the addition of self and other."""
        if isinstance(other, int):
            return self.value + other

        raise TypeError("Unsupported operand types for + ({} and {})".format(type(self).__name__, type(other).__name__))
