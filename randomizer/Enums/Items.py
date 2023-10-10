"""Item enum."""
from enum import Enum, auto


class Items(Enum):
    """Item enum."""

    NoItem = auto()
    TestItem = auto()

    Donkey = auto()
    Diddy = auto()
    Lanky = auto()
    Tiny = auto()
    Chunky = auto()

    Vines = auto()
    Swim = auto()
    Oranges = auto()
    Barrels = auto()

    ProgressiveSlam = auto()
    ProgressiveSlam2 = auto()

    ProgressiveDonkeyPotion = auto()
    BaboonBlast = auto()
    StrongKong = auto()
    GorillaGrab = auto()

    ProgressiveDiddyPotion = auto()
    ChimpyCharge = auto()
    RocketbarrelBoost = auto()
    SimianSpring = auto()

    ProgressiveLankyPotion = auto()
    Orangstand = auto()
    BaboonBalloon = auto()
    OrangstandSprint = auto()

    ProgressiveTinyPotion = auto()
    MiniMonkey = auto()
    PonyTailTwirl = auto()
    Monkeyport = auto()

    ProgressiveChunkyPotion = auto()
    HunkyChunky = auto()
    PrimatePunch = auto()
    GorillaGone = auto()

    Coconut = auto()
    Peanut = auto()
    Grape = auto()
    Feather = auto()
    Pineapple = auto()
    HomingAmmo = auto()
    SniperSight = auto()
    ProgressiveAmmoBelt = auto()
    ProgressiveAmmoBelt2 = auto()

    Bongos = auto()
    Guitar = auto()
    Trombone = auto()
    Saxophone = auto()
    Triangle = auto()
    ProgressiveInstrumentUpgrade = auto()
    ProgressiveInstrumentUpgrade2 = auto()
    ProgressiveInstrumentUpgrade3 = auto()

    Camera = auto()
    Shockwave = auto()
    CameraAndShockwave = auto()

    NintendoCoin = auto()
    RarewareCoin = auto()

    # Key items must be in order for best fills
    JungleJapesKey = auto()
    AngryAztecKey = auto()
    FranticFactoryKey = auto()
    GloomyGalleonKey = auto()
    FungiForestKey = auto()
    CrystalCavesKey = auto()
    CreepyCastleKey = auto()
    HideoutHelmKey = auto()

    HelmDonkey1 = auto()
    HelmDonkey2 = auto()
    HelmDiddy1 = auto()
    HelmDiddy2 = auto()
    HelmLanky1 = auto()
    HelmLanky2 = auto()
    HelmTiny1 = auto()
    HelmTiny2 = auto()
    HelmChunky1 = auto()
    HelmChunky2 = auto()

    GoldenBanana = auto()
    BananaFairy = auto()
    BananaMedal = auto()
    BattleCrown = auto()

    Bean = auto()
    Pearl = auto()
    RainbowCoin = auto()
    FakeItem = auto()

    JunkCrystal = auto()
    JunkMelon = auto()
    JunkAmmo = auto()
    JunkFilm = auto()
    JunkOrange = auto()
    CrateMelon = auto()  # Separate from junk melon due to separate settings
    EnemyItem = auto()  # Separate item

    BananaHoard = auto()

    JapesDonkeyHint = auto()
    JapesDiddyHint = auto()
    JapesLankyHint = auto()
    JapesTinyHint = auto()
    JapesChunkyHint = auto()
    AztecDonkeyHint = auto()
    AztecDiddyHint = auto()
    AztecLankyHint = auto()
    AztecTinyHint = auto()
    AztecChunkyHint = auto()
    FactoryDonkeyHint = auto()
    FactoryDiddyHint = auto()
    FactoryLankyHint = auto()
    FactoryTinyHint = auto()
    FactoryChunkyHint = auto()
    GalleonDonkeyHint = auto()
    GalleonDiddyHint = auto()
    GalleonLankyHint = auto()
    GalleonTinyHint = auto()
    GalleonChunkyHint = auto()
    ForestDonkeyHint = auto()
    ForestDiddyHint = auto()
    ForestLankyHint = auto()
    ForestTinyHint = auto()
    ForestChunkyHint = auto()
    CavesDonkeyHint = auto()
    CavesDiddyHint = auto()
    CavesLankyHint = auto()
    CavesTinyHint = auto()
    CavesChunkyHint = auto()
    CastleDonkeyHint = auto()
    CastleDiddyHint = auto()
    CastleLankyHint = auto()
    CastleTinyHint = auto()
    CastleChunkyHint = auto()

    # Blueprint items are intentionally grouped together in this specific order for Kasplat location logic.
    JungleJapesDonkeyBlueprint = auto()
    JungleJapesDiddyBlueprint = auto()
    JungleJapesLankyBlueprint = auto()
    JungleJapesTinyBlueprint = auto()
    JungleJapesChunkyBlueprint = auto()
    AngryAztecDonkeyBlueprint = auto()
    AngryAztecDiddyBlueprint = auto()
    AngryAztecLankyBlueprint = auto()
    AngryAztecTinyBlueprint = auto()
    AngryAztecChunkyBlueprint = auto()
    FranticFactoryDonkeyBlueprint = auto()
    FranticFactoryDiddyBlueprint = auto()
    FranticFactoryLankyBlueprint = auto()
    FranticFactoryTinyBlueprint = auto()
    FranticFactoryChunkyBlueprint = auto()
    GloomyGalleonDonkeyBlueprint = auto()
    GloomyGalleonDiddyBlueprint = auto()
    GloomyGalleonLankyBlueprint = auto()
    GloomyGalleonTinyBlueprint = auto()
    GloomyGalleonChunkyBlueprint = auto()
    FungiForestDonkeyBlueprint = auto()
    FungiForestDiddyBlueprint = auto()
    FungiForestLankyBlueprint = auto()
    FungiForestTinyBlueprint = auto()
    FungiForestChunkyBlueprint = auto()
    CrystalCavesDonkeyBlueprint = auto()
    CrystalCavesDiddyBlueprint = auto()
    CrystalCavesLankyBlueprint = auto()
    CrystalCavesTinyBlueprint = auto()
    CrystalCavesChunkyBlueprint = auto()
    CreepyCastleDonkeyBlueprint = auto()
    CreepyCastleDiddyBlueprint = auto()
    CreepyCastleLankyBlueprint = auto()
    CreepyCastleTinyBlueprint = auto()
    CreepyCastleChunkyBlueprint = auto()
    DKIslesDonkeyBlueprint = auto()
    DKIslesDiddyBlueprint = auto()
    DKIslesLankyBlueprint = auto()
    DKIslesTinyBlueprint = auto()
    DKIslesChunkyBlueprint = auto()

    # Adding new items to the end of the list preserves existing item selectors
    ProgressiveSlam3 = auto()

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
