"""Hint Type enum."""
from enum import Enum, auto


class HintType(Enum):
    """Hint type enum."""

    Joke = auto()
    KRoolOrder = auto()
    HelmOrder = auto()
    MoveLocation = auto()
    DirtPatch = auto()
    BLocker = auto()
    TroffNScoff = auto()
    KongLocation = auto()
    MedalsRequired = auto()
    Entrance = auto()
    RequiredKongHint = auto()
    RequiredKeyHint = auto()
    RequiredWinConditionHint = auto()
    RequiredHelmDoorHint = auto()
    FullShopWithItems = auto()
    WothLocation = auto()
    FoolishMove = auto()
    FoolishRegion = auto()
    Multipath = auto()
    ItemRegion = auto()

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
    def __hash__(self):
        return hash(self.value)
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
