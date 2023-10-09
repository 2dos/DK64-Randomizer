"""TransitionFront enum."""
from enum import Enum, auto


class Transitions(Enum):
    """Transition enum, specifically for shufflable transitions."""

    # Placeholder entrance for marking something as temporarily unassigned or invalid
    Empty = auto()

    # Level entrances
    IslesToJapes = auto()
    JapesToIsles = auto()
    IslesToAztec = auto()
    AztecToIsles = auto()
    IslesToFactory = auto()
    FactoryToIsles = auto()
    IslesToGalleon = auto()
    GalleonToIsles = auto()
    IslesToForest = auto()
    ForestToIsles = auto()
    IslesToCaves = auto()
    CavesToIsles = auto()
    IslesToCastle = auto()
    CastleToIsles = auto()

    # DK Isles exits
    IslesMainToStart = auto()
    IslesStartToMain = auto()
    IslesStartToTreehouse = auto()
    IslesTreehouseToStart = auto()
    IslesMainToFairy = auto()
    IslesFairyToMain = auto()
    IslesMainToSnideRoom = auto()
    IslesSnideRoomToMain = auto()
    IslesMainToJapesLobby = auto()
    IslesJapesLobbyToMain = auto()
    IslesMainToAztecLobby = auto()
    IslesAztecLobbyToMain = auto()
    IslesMainToFactoryLobby = auto()
    IslesFactoryLobbyToMain = auto()
    IslesMainToGalleonLobby = auto()
    IslesGalleonLobbyToMain = auto()
    IslesMainToForestLobby = auto()
    IslesForestLobbyToMain = auto()
    IslesMainToCavesLobby = auto()
    IslesCavesLobbyToMain = auto()
    IslesMainToCastleLobby = auto()
    IslesCastleLobbyToMain = auto()
    IslesMainToHelmLobby = auto()
    IslesHelmLobbyToMain = auto()

    # Jungle Japes Exits
    JapesMainToMine = auto()
    JapesMineToMain = auto()
    JapesMainToLankyCave = auto()
    JapesLankyCaveToMain = auto()
    JapesMainToCatacomb = auto()
    JapesCatacombToMain = auto()
    JapesMainToTinyHive = auto()
    JapesTinyHiveToMain = auto()
    JapesMineToCarts = auto()
    JapesMainToBBlast = auto()
    JapesCartsToMain = auto()

    # Angry Aztec Exits
    AztecStartToTemple = auto()
    AztecTempleToStart = auto()
    AztecMainToDonkey = auto()
    AztecDonkeyToMain = auto()
    AztecMainToDiddy = auto()
    AztecDiddyToMain = auto()
    AztecMainToLanky = auto()
    AztecLankyToMain = auto()
    AztecMainToTiny = auto()
    AztecTinyToMain = auto()
    AztecMainToChunky = auto()
    AztecChunkyToMain = auto()
    AztecMainToRace = auto()
    AztecRaceToMain = auto()
    AztecMainToLlama = auto()
    AztecLlamaToMain = auto()
    AztecMainToBBlast = auto()

    # Frantic Factory Exits
    FactoryRandDToRace = auto()
    FactoryRaceToRandD = auto()
    FactoryChunkyRoomToPower = auto()
    FactoryPowerToChunkyRoom = auto()
    FactoryBeyondHatchToInsideCore = auto()
    FactoryInsideCoreToBeyondHatch = auto()
    FactoryMainToBBlast = auto()

    # Gloomy Galleon Exits
    GalleonLighthouseAreaToLighthouse = auto()
    GalleonLighthouseToLighthouseArea = auto()
    GalleonLighthouseAreaToMermaid = auto()
    GalleonMermaidToLighthouseArea = auto()
    GalleonLighthouseAreaToSickBay = auto()
    GalleonSickBayToLighthouseArea = auto()
    GalleonShipyardToSeal = auto()
    GalleonSealToShipyard = auto()
    GalleonShipyardToSubmarine = auto()
    GalleonSubmarineToShipyard = auto()
    GalleonShipyardToLanky = auto()
    GalleonLankyToShipyard = auto()
    GalleonShipyardToTiny = auto()
    GalleonTinyToShipyard = auto()
    GalleonShipyardToBongos = auto()
    GalleonBongosToShipyard = auto()
    GalleonShipyardToGuitar = auto()
    GalleonGuitarToShipyard = auto()
    GalleonShipyardToTrombone = auto()
    GalleonTromboneToShipyard = auto()
    GalleonShipyardToSaxophone = auto()
    GalleonSaxophoneToShipyard = auto()
    GalleonShipyardToTriangle = auto()
    GalleonTriangleToShipyard = auto()
    GalleonTreasureToChest = auto()
    GalleonChestToTreasure = auto()
    GalleonMainToBBlast = auto()

    # Fungi Forest Exits
    ForestMainToCarts = auto()
    ForestCartsToMain = auto()
    ForestMainToLowerMushroom = auto()
    ForestLowerMushroomToMain = auto()
    ForestLowerExteriorToLowerMushroom = auto()
    ForestLowerMushroomToLowerExterior = auto()
    ForestLowerExteriorToUpperMushroom = auto()
    ForestUpperMushroomToLowerExterior = auto()
    ForestUpperExteriorToUpperMushroom = auto()
    ForestUpperMushroomToUpperExterior = auto()
    ForestExteriorToNight = auto()
    ForestNightToExterior = auto()
    ForestExteriorToChunky = auto()
    ForestChunkyToExterior = auto()
    ForestExteriorToZingers = auto()
    ForestZingersToExterior = auto()
    ForestExteriorToMushrooms = auto()
    ForestMushroomsToExterior = auto()
    ForestTreeToAnthill = auto()
    ForestAnthillToTree = auto()
    ForestMainToChunkyMill = auto()
    ForestChunkyMillToMain = auto()
    ForestMainToTinyMill = auto()
    ForestTinyMillToMain = auto()
    ForestMainToGrinder = auto()
    ForestGrinderToMain = auto()
    ForestMainToRafters = auto()
    ForestRaftersToMain = auto()
    ForestMainToWinch = auto()
    ForestWinchToMain = auto()
    ForestMainToAttic = auto()
    ForestAtticToMain = auto()
    ForestTinyMillToSpider = auto()
    ForestSpiderToTinyMill = auto()
    ForestTinyMillToGrinder = auto()
    ForestGrinderToTinyMill = auto()
    ForestMainToBarn = auto()
    ForestBarnToMain = auto()
    ForestMainToBBlast = auto()

    # Crystal Caves Exits
    CavesMainToRace = auto()
    CavesRaceToMain = auto()
    CavesMainToCastle = auto()
    CavesCastleToMain = auto()
    CavesIglooToDonkey = auto()
    CavesDonkeyToIgloo = auto()
    CavesIglooToDiddy = auto()
    CavesDiddyToIgloo = auto()
    CavesIglooToLanky = auto()
    CavesLankyToIgloo = auto()
    CavesIglooToTiny = auto()
    CavesTinyToIgloo = auto()
    CavesIglooToChunky = auto()
    CavesChunkyToIgloo = auto()
    CavesCabinToRotating = auto()
    CavesRotatingToCabin = auto()
    CavesCabinToDonkey = auto()
    CavesDonkeyToCabin = auto()
    CavesCabinToDiddyLower = auto()
    CavesDiddyLowerToCabin = auto()
    CavesCabinToDiddyUpper = auto()
    CavesDiddyUpperToCabin = auto()
    CavesCabinToLanky = auto()
    CavesLankyToCabin = auto()
    CavesCabinToTiny = auto()
    CavesTinyToCabin = auto()
    CavesCabinToChunky = auto()
    CavesChunkyToCabin = auto()
    CavesMainToBBlast = auto()

    # Creepy Castle Exits
    CastleMainToTree = auto()
    CastleTreeToMain = auto()
    CastleTreeDrainToMain = auto()
    CastleMainToLibraryStart = auto()
    CastleLibraryStartToMain = auto()
    CastleMainToLibraryEnd = auto()
    CastleLibraryEndToMain = auto()
    CastleMainToBallroom = auto()
    CastleBallroomToMain = auto()
    CastleMainToTower = auto()
    CastleTowerToMain = auto()
    CastleMainToGreenhouse = auto()
    CastleGreenhouseStartToMain = auto()
    CastleGreenhouseEndToMain = auto()
    CastleMainToTrash = auto()
    CastleTrashToMain = auto()
    CastleMainToShed = auto()
    CastleShedToMain = auto()
    CastleMainToMuseum = auto()
    CastleMuseumToMain = auto()
    CastleMainToLower = auto()
    CastleLowerToMain = auto()
    CastleMainToUpper = auto()
    CastleUpperToMain = auto()
    CastleWaterfallToUpper = auto()
    CastleUpperToWaterfall = auto()
    CastleBallroomToMuseum = auto()
    CastleMuseumToBallroom = auto()
    CastleMuseumToCarRace = auto()
    CastleRaceToMuseum = auto()
    CastleLowerToCrypt = auto()
    CastleCryptToLower = auto()
    CastleLowerToMausoleum = auto()
    CastleMausoleumToLower = auto()
    CastleCryptToCarts = auto()
    CastleCartsToCrypt = auto()
    CastleUpperToDungeon = auto()
    CastleDungeonToUpper = auto()
    CastleMainToBBlast = auto()

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
