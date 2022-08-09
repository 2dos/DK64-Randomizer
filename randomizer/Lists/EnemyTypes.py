"""List of enemies with in-game index."""
from enum import IntEnum
from os import kill


class Enemies(IntEnum):
    """List of Enemies with in-game index."""

    BeaverBlue = 0
    GiantClam = 1
    Krash = 2
    Book = 3
    ZingerCharger = 5
    Klobber = 6
    Snide = 7
    ArmyDillo = 8
    Klump = 9
    Cranky = 11
    Funky = 12
    Candy = 13
    Beetle = 14
    Mermaid = 15
    Kaboom = 16
    VultureTemple = 17
    Squawks = 18
    CutsceneDK = 19
    CutsceneDiddy = 20
    CutsceneLanky = 21
    CutsceneTiny = 22
    CutsceneChunky = 23
    TandSPadlock = 24
    Llama = 25
    MadJack = 26
    KlaptrapGreen = 27
    ZingerLime = 28
    VultureRace = 29
    KlaptrapPurple = 30
    KlaptrapRed = 31
    GetOut = 32
    BeaverGold = 33
    FireColumn = 35
    TNTMinecart0 = 36
    TNTMinecart1 = 37
    Pufftoss = 38
    SeasickCannon = 39
    KRoolFoot = 40
    Fireball = 42
    MushroomMan = 44
    Troff = 46
    BadHitDetectionMan = 48
    Ruler = 51
    ToyBox = 52
    Squawks1 = 53
    Seal = 54
    Scoff = 55
    RoboKremling = 56
    Dogadon = 57
    Kremling = 59
    SpotlightFish = 60
    KasplatDK = 61
    KasplatDiddy = 62
    KasplatLanky = 63
    KasplatTiny = 64
    KasplatChunky = 65
    MechFish = 66
    Seal1 = 67
    Fairy = 68
    SquawksSpotlight = 69
    Rabbit = 72
    Owl = 73
    NintendoLogo = 74
    FireBreath = 75
    MinigameController = 76
    BattleCrownController = 77
    ToyCar = 78
    TNTMinecart2 = 79
    CutsceneObject = 80
    Guard = 81
    RarewareLogo = 82
    ZingerRobo = 83
    Krossbones = 84
    Shuri = 85
    Gimpfish = 86
    MrDice0 = 87
    SirDomino = 88
    MrDice1 = 89
    Rabbit1 = 90
    FireballGlasses = 92
    KLumsy = 93
    SpiderBoss = 94
    SpiderSmall = 95
    Squawks2 = 96
    KRoolDK = 97
    SkeletonHead = 98
    Bat = 99
    EvilTomato = 100
    Ghost = 101
    Pufftup = 102
    Kosha = 103
    EnemyCar = 105
    KRoolDiddy = 106
    KRoolLanky = 107
    KRoolTiny = 108
    KRoolChunky = 109
    Bug = 110
    FairyQueen = 111
    IceTomato = 112


class EnemyData:
    """Information about the enemy."""

    def __init__(
        self,
        *,
        aggro=1,
        min_speed=15,
        max_speed=150,
        crown_enabled=True,
        air=False,
        size_cap=0,
        crown_weight=0,
        simple=False,
        minigame_enabled=True,
        killable=True,
        beaver=False,
        kasplat=False,
        disruptive=0
    ):
        """Initialize with given parameters."""
        self.aggro = aggro
        self.min_speed = min_speed
        self.max_speed = max_speed
        self.crown_enabled = crown_enabled
        self.air = air
        self.size_cap = size_cap
        self.crown_weight = crown_weight
        self.simple = simple
        self.minigame_enabled = minigame_enabled
        self.killable = killable
        self.beaver = beaver
        self.kasplat = kasplat
        self.disruptive = disruptive
        if air:
            self.minigame_enabled = False


EnemyMetaData = {
    Enemies.BeaverBlue: EnemyData(crown_weight=10, simple=True, beaver=True),  #
    Enemies.Book: EnemyData(aggro=6, crown_enabled=False, air=True, minigame_enabled=False),
    Enemies.ZingerCharger: EnemyData(air=True, crown_weight=7, disruptive=1),  #
    Enemies.Klobber: EnemyData(aggro=4, crown_weight=2, killable=False, disruptive=2),
    Enemies.Klump: EnemyData(crown_weight=1, killable=False, disruptive=1),  #
    Enemies.Kaboom: EnemyData(aggro=4, crown_weight=2, killable=False, disruptive=2),
    Enemies.KlaptrapGreen: EnemyData(crown_weight=8, simple=True),  #
    Enemies.ZingerLime: EnemyData(air=True, crown_weight=5, disruptive=1),  #
    Enemies.KlaptrapPurple: EnemyData(crown_weight=2, killable=False, disruptive=1),  #
    Enemies.KlaptrapRed: EnemyData(crown_weight=2, killable=False, disruptive=1),  #
    Enemies.BeaverGold: EnemyData(crown_weight=10, simple=True, beaver=True),  #
    Enemies.MushroomMan: EnemyData(aggro=4, size_cap=60, crown_weight=10, simple=True),
    Enemies.Ruler: EnemyData(crown_weight=10, simple=True),  #
    Enemies.RoboKremling: EnemyData(crown_weight=2, killable=False, disruptive=1),  #
    Enemies.Kremling: EnemyData(crown_weight=10, simple=True),  #
    Enemies.KasplatDK: EnemyData(crown_weight=6, kasplat=True),  #
    Enemies.KasplatDiddy: EnemyData(crown_weight=6, kasplat=True),  #
    Enemies.KasplatLanky: EnemyData(crown_weight=6, kasplat=True),  #
    Enemies.KasplatTiny: EnemyData(crown_weight=6, kasplat=True),  #
    Enemies.KasplatChunky: EnemyData(crown_weight=6, kasplat=True),  #
    Enemies.ZingerRobo: EnemyData(air=True, crown_weight=5, disruptive=1),  #
    Enemies.Krossbones: EnemyData(crown_weight=10, simple=True),  #
    Enemies.Shuri: EnemyData(crown_enabled=False, minigame_enabled=False),  #
    Enemies.Gimpfish: EnemyData(aggro=1, crown_enabled=False, minigame_enabled=False),
    Enemies.MrDice0: EnemyData(crown_weight=10, simple=True),  # Should be aggro 4, but I think this is because it normally spawns in the BHDM fight
    Enemies.SirDomino: EnemyData(crown_weight=10, simple=True),  #
    Enemies.MrDice1: EnemyData(crown_weight=10, simple=True),  #
    Enemies.FireballGlasses: EnemyData(aggro=35, min_speed=100, max_speed=255, crown_weight=10, killable=False),  # 29 for if you want them to respond to the rabbit
    Enemies.SpiderSmall: EnemyData(crown_weight=7, disruptive=1),  # with projectiles, disruptive will need to be set to 2
    Enemies.Bat: EnemyData(air=True, crown_weight=5, minigame_enabled=False, disruptive=1),  #
    Enemies.EvilTomato: EnemyData(aggro=4, crown_enabled=False, minigame_enabled=False),
    Enemies.Ghost: EnemyData(crown_weight=10, simple=True),  #
    Enemies.Pufftup: EnemyData(crown_enabled=False, size_cap=40, minigame_enabled=False),  #
    Enemies.Kosha: EnemyData(crown_weight=1, killable=False, disruptive=2),  #
    Enemies.GetOut: EnemyData(aggro=6, crown_enabled=False, minigame_enabled=False),
    Enemies.Guard: EnemyData(aggro=1, crown_enabled=False, minigame_enabled=False),
    # Enemies.Bug: EnemyData(aggro=0x40,crown_enabled=False),
}
