"""Minigames enum."""
from enum import Enum, auto


class Minigames(Enum):
    """Minigames enum."""

    NoGame = auto()
    BattyBarrelBanditVEasy = auto()
    BattyBarrelBanditEasy = auto()
    BattyBarrelBanditNormal = auto()
    BattyBarrelBanditHard = auto()
    BigBugBashVEasy = auto()
    BigBugBashEasy = auto()
    BigBugBashNormal = auto()
    BigBugBashHard = auto()
    BusyBarrelBarrageEasy = auto()
    BusyBarrelBarrageNormal = auto()
    BusyBarrelBarrageHard = auto()
    MadMazeMaulEasy = auto()
    MadMazeMaulNormal = auto()
    MadMazeMaulHard = auto()
    MadMazeMaulInsane = auto()
    MinecartMayhemEasy = auto()
    MinecartMayhemNormal = auto()
    MinecartMayhemHard = auto()
    BeaverBotherEasy = auto()
    BeaverBotherNormal = auto()
    BeaverBotherHard = auto()
    TeeteringTurtleTroubleVEasy = auto()
    TeeteringTurtleTroubleEasy = auto()
    TeeteringTurtleTroubleNormal = auto()
    TeeteringTurtleTroubleHard = auto()
    StealthySnoopVEasy = auto()
    StealthySnoopEasy = auto()
    StealthySnoopNormal = auto()
    StealthySnoopHard = auto()
    StashSnatchEasy = auto()
    StashSnatchNormal = auto()
    StashSnatchHard = auto()
    StashSnatchInsane = auto()
    SplishSplashSalvageEasy = auto()
    SplishSplashSalvageNormal = auto()
    SplishSplashSalvageHard = auto()
    SpeedySwingSortieEasy = auto()
    SpeedySwingSortieNormal = auto()
    SpeedySwingSortieHard = auto()
    KrazyKongKlamourEasy = auto()
    KrazyKongKlamourNormal = auto()
    KrazyKongKlamourHard = auto()
    KrazyKongKlamourInsane = auto()
    SearchlightSeekVEasy = auto()
    SearchlightSeekEasy = auto()
    SearchlightSeekNormal = auto()
    SearchlightSeekHard = auto()
    KremlingKoshVEasy = auto()
    KremlingKoshEasy = auto()
    KremlingKoshNormal = auto()
    KremlingKoshHard = auto()
    PerilPathPanicVEasy = auto()
    PerilPathPanicEasy = auto()
    PerilPathPanicNormal = auto()
    PerilPathPanicHard = auto()
    DonkeyRambi = auto()
    DonkeyTarget = auto()
    DiddyKremling = auto()
    DiddyRocketbarrel = auto()
    LankyMaze = auto()
    LankyShooting = auto()
    TinyMushroom = auto()
    TinyPonyTailTwirl = auto()
    ChunkyHiddenKremling = auto()
    ChunkyShooting = auto()
    RambiArena = auto()
    EnguardeArena = auto()

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
