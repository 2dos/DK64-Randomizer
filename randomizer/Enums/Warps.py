"""Bananaports enum."""
from enum import Enum, auto


class Warps(Enum):
    """Bananaports enum."""

    JapesNearPortal = auto()
    JapesEndOfTunnel = auto()
    JapesNearMainTag = auto()
    JapesNearMountain = auto()
    JapesFarRight = auto()
    JapesFarLeft = auto()
    JapesCrankyTunnelNear = auto()
    JapesCrankyTunnelFar = auto()
    JapesShellhive = auto()
    JapesOnMountain = auto()
    AztecNearPortal = auto()
    AztecNearCandy = auto()
    AztecNearTinyTemple = auto()
    AztecEndOfTunnel = auto()
    AztecTotemNearLeft = auto()
    AztecCranky = auto()
    AztecTotemNearRight = auto()
    AztecFunky = auto()
    AztecNearSnide = auto()
    AztecSnoopTunnel = auto()
    LlamaNearLeft = auto()
    LlamaMatchingGame = auto()
    LlamaNearRight = auto()
    LlamaLavaRoom = auto()
    FactoryNearHatchTunnel = auto()
    FactoryStorageRoom = auto()
    FactoryNearBlockTunnel = auto()
    FactoryRAndD = auto()
    FactoryLobbyFar = auto()
    FactorySnides = auto()
    FactoryProdBottom = auto()
    FactoryProdTop = auto()
    FactoryArcade = auto()
    FactoryFunky = auto()
    GalleonNearTunnelIntersection = auto()
    GalleonLighthouseRear = auto()
    GalleonNearChestGB = auto()
    GalleonNear2DS = auto()
    GalleonNearCranky = auto()
    GalleonSnides = auto()
    GalleonGoldTower = auto()
    GalleonNearSeal = auto()
    GalleonNearRocketbarrel = auto()
    GalleonNearFunky = auto()
    FungiClock1 = auto()
    FungiMill = auto()
    FungiClock2 = auto()
    FungiFunky = auto()
    FungiClock3 = auto()
    FungiMushEntrance = auto()
    FungiClock4 = auto()
    FungiOwlTree = auto()
    FungiTopMush = auto()
    FungiLowMush = auto()
    CavesNearLeft = auto()
    CavesNearChunkyShield = auto()
    CavesNearRight = auto()
    CavesWaterfall = auto()
    CavesNearIglooTag = auto()
    CavesBonusRoom = auto()
    CavesThinPillar = auto()
    CavesBlueprintRoom = auto()
    CavesThickPillar = auto()
    CavesCabins = auto()
    CastleCenter1 = auto()
    CastleRear = auto()
    CastleCenter2 = auto()
    CastleRocketbarrel = auto()
    CastleCenter3 = auto()
    CastleCranky = auto()
    CastleCenter4 = auto()
    CastleTrashCan = auto()
    CastleCenter5 = auto()
    CastleTop = auto()
    CryptNearLeft = auto()
    CryptFarLeft = auto()
    CryptNearCenter = auto()
    CryptFarCenter = auto()
    CryptNearRight = auto()
    CryptFarRight = auto()
    IslesRing1 = auto()
    IslesKLumsy = auto()
    IslesRing2 = auto()
    IslesAztecLobby = auto()
    IslesRing3 = auto()
    IslesWaterfall = auto()
    IslesRing4 = auto()
    IslesFactoryLobby = auto()
    IslesRing5 = auto()
    IslesFairyIsland = auto()
    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self is other
        elif isinstance(other, int):
            return self.value == other
        return NotImplemented

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result

    def __mod__(self, other):
        if isinstance(other, int):
            return self.value % other
        raise TypeError("Unsupported operand types for % ({} and {})".format(type(self).__name__, type(other).__name__))

    def __to_bytes(self, length, byteorder, signed):
        return self.value.to_bytes(length, byteorder, signed=signed)

    def to_bytes(self, length, byteorder='big', signed=False):
        return self.__to_bytes(length, byteorder, signed)

    def __sub__(self, other):
        if isinstance(other, int):
            return self.value - other
        raise TypeError("Unsupported operand types for - ({} and {})".format(type(self).__name__, type(other).__name__))

    def __ge__(self, other):
        if isinstance(other, type(self)):
            return self.value >= other.value
        elif isinstance(other, int):
            return self.value >= other
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, type(self)):
            return self.value <= other.value
        elif isinstance(other, int):
            return self.value <= other
        return NotImplemented