"""Hint enums for kong type and locations."""
from enum import Enum, auto


class WrinklyKong(Enum):
    """Kong for wrinkly to assign to.

    Args:
        Enum (int): Enum of the kong.
    """

    ftt = auto()
    dk = auto()
    diddy = auto()
    tiny = auto()
    lanky = auto()
    chunky = auto()

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


class WrinklyLocation(Enum):
    """Lobby location of the wrinkly hint.

    Args:
        Enum (int): Enum of the location.
    """

    ftt = auto()
    japes = auto()
    aztec = auto()
    factory = auto()
    galleon = auto()
    fungi = auto()
    caves = auto()
    castle = auto()

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

    def __hash__(self):
        return hash(self.value)

    def __le__(self, other):
        if isinstance(other, type(self)):
            return self.value <= other.value
        elif isinstance(other, int):
            return self.value <= other
        return NotImplemented

    def __index__(self):
        return self.value

    def __lt__(self, other):
        if isinstance(other, int):
            return self.value < other
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, type(self)):
            return self.value > other.value
        elif isinstance(other, int):
            return self.value > other
        return NotImplemented
