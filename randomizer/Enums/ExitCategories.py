"""Exit Categories enum."""
from enum import Enum, auto


class ExitCategories(Enum):
    """These categories are used to categorize maps with multiple entrances."""

    IslesExterior = auto()
    IslesTrainingGrounds = auto()
    JapesLobby = auto()
    AztecLobby = auto()
    FactoryLobby = auto()
    GalleonLobby = auto()
    ForestLobby = auto()
    CavesLobby = auto()
    CastleLobby = auto()
    JapesExterior = auto()
    AztecExterior = auto()
    FactoryExterior = auto()
    GalleonExterior = auto()
    ForestExterior = auto()
    ForestMushroom = auto()
    ForestMill = auto()
    ForestGrinder = auto()
    CavesExterior = auto()
    CastleExterior = auto()
    CastleLower = auto()
    CastleUpper = auto()
    CastleBallroom = auto()
    CastleCarRaceExterior = auto()
    CastleCrypt = auto()

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

    def to_bytes(self, length, byteorder="big", signed=False):
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

    def __index__(self):
        return self.value
