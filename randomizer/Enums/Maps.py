"""Maps enum."""
from enum import Enum


class Maps(Enum):
    """List of Maps with in-game index."""

    # DK Isles
    Isles = 34
    BananaFairyRoom = 189
    JungleJapesLobby = 169
    AngryAztecLobby = 173
    IslesSnideRoom = 195
    FranticFactoryLobby = 175
    GloomyGalleonLobby = 174
    FungiForestLobby = 178
    CrystalCavesLobby = 194
    CreepyCastleLobby = 193
    HideoutHelmLobby = 170
    TrainingGrounds = 176
    Treehouse = 171
    KLumsy = 97

    # Jungle Japes
    JungleJapes = 7
    JapesTinyHive = 12
    JapesLankyCave = 13
    JapesMountain = 4
    JapesMinecarts = 6
    JapesUnderGround = 33
    JapesBaboonBlast = 37

    # Angry Aztec
    AngryAztec = 38
    AztecTinyTemple = 16
    AztecDonkey5DTemple = 19
    AztecDiddy5DTemple = 21
    AztecLanky5DTemple = 23
    AztecTiny5DTemple = 22
    AztecChunky5DTemple = 24
    AztecTinyRace = 14
    AztecLlamaTemple = 20
    AztecBaboonBlast = 41

    # Frantic Factory
    FranticFactory = 26
    FactoryTinyRace = 27
    FactoryPowerHut = 29
    FactoryCrusher = 36
    FactoryBaboonBlast = 110

    # Gloomy Galleon
    GloomyGalleon = 30
    GalleonLighthouse = 49
    GalleonMermaidRoom = 45
    GalleonSickBay = 31
    GalleonSealRace = 39
    GalleonTreasureChest = 44
    GalleonSubmarine = 179
    GalleonMechafish = 51
    Galleon5DShipDKTiny = 46
    Galleon5DShipDiddyLankyChunky = 43
    Galleon2DShip = 47
    GalleonBaboonBlast = 54

    # Fungi Forest
    FungiForest = 48
    ForestMinecarts = 55
    ForestGiantMushroom = 64
    ForestChunkyFaceRoom = 71
    ForestLankyZingersRoom = 70
    ForestLankyMushroomsRoom = 63
    ForestAnthill = 52
    ForestMillFront = 61
    ForestMillBack = 62
    ForestSpider = 60
    ForestRafters = 56
    ForestWinchRoom = 57
    ForestMillAttic = 58
    ForestThornvineBarn = 59
    ForestBaboonBlast = 188

    # Crystal Caves
    CrystalCaves = 72
    CavesLankyRace = 82
    CavesFrozenCastle = 98
    CavesDonkeyIgloo = 86
    CavesDiddyIgloo = 100
    CavesLankyIgloo = 85
    CavesTinyIgloo = 84
    CavesChunkyIgloo = 95
    CavesRotatingCabin = 89
    CavesDonkeyCabin = 91
    CavesDiddyLowerCabin = 92
    CavesDiddyUpperCabin = 200
    CavesLankyCabin = 94
    CavesTinyCabin = 93
    CavesChunkyCabin = 90
    CavesBaboonBlast = 186

    # Creepy Castle
    CreepyCastle = 87
    CastleTree = 164
    CastleLibrary = 114
    CastleBallroom = 88
    CastleMuseum = 113
    CastleTinyRace = 185
    CastleTower = 105
    CastleGreenhouse = 168
    CastleTrashCan = 167
    CastleShed = 166
    CastleLowerCave = 183
    CastleCrypt = 112
    CastleMinecarts = 106
    CastleMausoleum = 108
    CastleUpperCave = 151
    CastleDungeon = 163
    CastleBaboonBlast = 187

    # Hideout Helm
    HideoutHelm = 17

    # Level Bosses
    JapesBoss = 8
    AztecBoss = 197
    FactoryBoss = 154
    GalleonBoss = 111
    FungiBoss = 83
    CavesBoss = 196
    CastleBoss = 199

    # K rool phases
    KroolDonkeyPhase = 203
    KroolDiddyPhase = 204
    KroolLankyPhase = 205
    KroolTinyPhase = 206
    KroolChunkyPhase = 207

    # Bonus Barrels
    BattyBarrelBanditVEasy = 32
    BattyBarrelBanditEasy = 121
    BattyBarrelBanditNormal = 122
    BattyBarrelBanditHard = 123
    BigBugBashVEasy = 102
    BigBugBashEasy = 148
    BigBugBashNormal = 149
    BigBugBashHard = 150
    BusyBarrelBarrageEasy = 78
    BusyBarrelBarrageNormal = 79
    BusyBarrelBarrageHard = 131
    MadMazeMaulEasy = 68
    MadMazeMaulNormal = 69
    MadMazeMaulHard = 66
    MadMazeMaulInsane = 124
    MinecartMayhemEasy = 77
    MinecartMayhemNormal = 129
    MinecartMayhemHard = 130
    BeaverBotherEasy = 104
    BeaverBotherNormal = 136
    BeaverBotherHard = 137
    TeeteringTurtleTroubleVEasy = 18
    TeeteringTurtleTroubleEasy = 118
    TeeteringTurtleTroubleNormal = 119
    TeeteringTurtleTroubleHard = 120
    StealthySnoopVEasy = 126
    StealthySnoopEasy = 127
    StealthySnoopNormal = 65
    StealthySnoopHard = 128
    StashSnatchEasy = 74
    StashSnatchNormal = 67
    StashSnatchHard = 75
    StashSnatchInsane = 125
    SplishSplashSalvageEasy = 133
    SplishSplashSalvageNormal = 96
    SplishSplashSalvageHard = 132
    SpeedySwingSortieEasy = 99
    SpeedySwingSortieNormal = 134
    SpeedySwingSortieHard = 135
    KrazyKongKlamourEasy = 101
    KrazyKongKlamourNormal = 141
    KrazyKongKlamourHard = 142
    KrazyKongKlamourInsane = 143
    SearchlightSeekVEasy = 103
    SearchlightSeekEasy = 138
    SearchlightSeekNormal = 139
    SearchlightSeekHard = 140
    KremlingKoshVEasy = 10
    KremlingKoshEasy = 115
    KremlingKoshNormal = 116
    KremlingKoshHard = 117
    PerilPathPanicVEasy = 144
    PerilPathPanicEasy = 145
    PerilPathPanicNormal = 146
    PerilPathPanicHard = 147
    HelmBarrelDKTarget = 35
    HelmBarrelDKRambi = 212
    HelmBarrelDiddyKremling = 165
    HelmBarrelDiddyRocketbarrel = 201
    HelmBarrelLankyMaze = 3
    HelmBarrelLankyShooting = 202
    HelmBarrelTinyPTT = 210
    HelmBarrelTinyMush = 50
    HelmBarrelChunkyHidden = 209
    HelmBarrelChunkyShooting = 211
    RambiArena = 191
    EnguardeArena = 184

    # Crowns
    JapesCrown = 53
    AztecCrown = 73
    FactoryCrown = 155
    GalleonCrown = 156
    ForestCrown = 159
    CavesCrown = 160
    CastleCrown = 161
    HelmCrown = 162
    SnidesCrown = 158
    LobbyCrown = 157

    # Shops
    Cranky = 5
    Candy = 25
    Funky = 1
    Snide = 15

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
