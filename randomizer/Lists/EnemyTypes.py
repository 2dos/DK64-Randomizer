"""List of enemies with in-game index."""
from enum import IntEnum
from os import kill
from randomizer.Lists.MapsAndExits import Maps
from randomizer.Enums.EnemyLocations import EnemyLocations
from randomizer.Enums.EnemySubtypes import EnemySubtype
import random


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
        name="",
        e_type=EnemySubtype.NoType,
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
        disruptive=0,
        bbbarrage_min_scale=50,
        selector_enabled=True,
        interaction=None,
    ):
        """Initialize with given parameters."""
        self.name = name
        self.e_type = e_type
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
        self.bbbarrage_min_scale = bbbarrage_min_scale
        self.selector_enabled = selector_enabled
        self.interaction = interaction
        if air:
            self.minigame_enabled = False


class InteractionMethods:
    """Information about interactions with enemies."""

    def __init__(
        self,
        *,
        kill_melee=True,  # Killing can be done with regular attacks
        kill_orange=True,  # Killing can be done with oranges
        kill_gun=True,  # Killing can be done with a gun
        kill_shockwave=True, # Killing can be done with a shockwave attack
        can_kill=True, # Master control of all kill variables
        can_bypass=True,  # Enemy can be bypassed without any additional tricks
    ):
        """Initialize with given data."""
        self.kill_melee = kill_melee and can_kill
        self.kill_orange = kill_orange and can_kill
        self.kill_gun = kill_gun and can_kill
        self.kill_shockwave = kill_shockwave and can_kill
        self.can_bypass = can_bypass


class EnemyLoc:
    """Information about an enemy"""

    def __init__(self, map: Maps, default_enemy: Enemies, id: int, banned_enemies: list, enable_randomization: bool):
        """Initialize with given parameters."""
        self.map = map
        self.default_enemy = default_enemy
        self.enemy = default_enemy
        self.id = id
        self.banned_enemies = banned_enemies.copy()
        self.enable_randomization = enable_randomization
        self.default_type = EnemySubtype.GroundSimple
        self.allowed_enemies = []
        if enable_randomization:
            if default_enemy in EnemyMetaData:
                self.default_type = EnemyMetaData[default_enemy].e_type
            self.allowed_enemies = [enemy for enemy in EnemyMetaData if EnemyMetaData[enemy].e_type == self.default_type and enemy not in banned_enemies]

    def placeNewEnemy(self, enabled_enemies: list):
        """Places new enemy in slot."""
        permitted = [enemy for enemy in self.allowed_enemies if enemy in enabled_enemies]
        if len(permitted) > 0:
            self.enemy = random.choice(permitted)

    def canKill(self) -> bool:
        """Determines if the enemy can be killed"""
        if self.enemy in EnemyMetaData:
            interaction: InteractionMethods = EnemyMetaData[self.enemy].interaction
            if interaction is not None:
                if interaction.kill_melee:
                    return True
                return True # TODO: Handle logic with the different killing methods
        return False
    
    def canBypass(self) -> bool:
        if self.enemy in EnemyMetaData:
            interaction: InteractionMethods = EnemyMetaData[self.enemy].interaction
            if interaction is not None:
                return interaction.can_bypass
        return False


EnemyMetaData = {
    Enemies.BeaverBlue: EnemyData(
        name="Beaver (Blue)",
        e_type=EnemySubtype.GroundSimple,
        crown_weight=10,
        simple=True,
        bbbarrage_min_scale=70,
        beaver=True,
        interaction=InteractionMethods(),
    ),  #
    Enemies.Book: EnemyData(
        name="Book",
        aggro=6,
        crown_enabled=False,
        air=True,
        minigame_enabled=False,
        selector_enabled=False,
        interaction=InteractionMethods(can_kill=False),
    ),
    Enemies.ZingerCharger: EnemyData(
        name="Zinger (Charger)",
        e_type=EnemySubtype.Air,
        air=True,
        crown_weight=7,
        disruptive=1,
        interaction=InteractionMethods(kill_melee=False,kill_orange=False,kill_shockwave=False),
    ),  #
    Enemies.Klobber: EnemyData(
        name="Klobber",
        e_type=EnemySubtype.GroundBeefy,
        aggro=4,
        crown_weight=2,
        killable=False,
        disruptive=2,
        interaction=InteractionMethods(kill_gun=False,kill_melee=False),
    ),
    Enemies.Klump: EnemyData(
        name="Klump",
        e_type=EnemySubtype.GroundBeefy,
        crown_weight=1,
        killable=False,
        disruptive=1,
        interaction=InteractionMethods(kill_gun=False,kill_melee=False),
    ),  #
    Enemies.Kaboom: EnemyData(
        name="Kaboom",
        e_type=EnemySubtype.GroundBeefy,
        aggro=4,
        crown_weight=2,
        killable=False,
        disruptive=2,
        interaction=InteractionMethods(kill_gun=False,kill_melee=False),
    ),
    Enemies.KlaptrapGreen: EnemyData(
        name="Klaptrap (Green)",
        e_type=EnemySubtype.GroundSimple,
        crown_weight=8,
        simple=True,
        bbbarrage_min_scale=100,
        interaction=InteractionMethods(),
    ),  #
    Enemies.ZingerLime: EnemyData(
        name="Zinger (Lime Thrower)",
        e_type=EnemySubtype.Air,
        air=True,
        crown_weight=5,
        disruptive=1,
        interaction=InteractionMethods(kill_orange=False,kill_melee=False,kill_shockwave=False),
    ),  #
    Enemies.KlaptrapPurple: EnemyData(
        name="Klaptrap (Purple)",
        e_type=EnemySubtype.GroundBeefy,
        crown_weight=2,
        killable=False,
        disruptive=1,
        interaction=InteractionMethods(kill_gun=False,kill_melee=False,kill_shockwave=False),
    ),  #
    Enemies.KlaptrapRed: EnemyData(
        name="Klaptrap (Red)",
        e_type=EnemySubtype.GroundBeefy,
        crown_weight=2,
        killable=False,
        disruptive=1,
        interaction=InteractionMethods(kill_melee=False,kill_shockwave=False),
    ),  #
    Enemies.BeaverGold: EnemyData(
        name="Beaver (Gold)",
        e_type=EnemySubtype.GroundSimple,
        crown_weight=10,
        simple=True,
        bbbarrage_min_scale=70,
        beaver=True,
        interaction=InteractionMethods(),
    ),  #
    Enemies.MushroomMan: EnemyData(
        name="Mushroom Man",
        e_type=EnemySubtype.GroundSimple,
        aggro=4,
        size_cap=60,
        crown_weight=10,
        simple=True,
        bbbarrage_min_scale=50,
        interaction=InteractionMethods(),
    ),
    Enemies.Ruler: EnemyData(
        name="Ruler",
        e_type=EnemySubtype.GroundSimple,
        crown_weight=10,
        simple=True,
        bbbarrage_min_scale=50,
        interaction=InteractionMethods(),
    ),  #
    Enemies.RoboKremling: EnemyData(
        name="Robo-Kremling",
        e_type=EnemySubtype.GroundBeefy,
        crown_weight=2,
        killable=False,
        disruptive=1,
        interaction=InteractionMethods(kill_melee=False,kill_gun=False),
    ),  #
    Enemies.Kremling: EnemyData(
        name="Kremling",
        e_type=EnemySubtype.GroundSimple,
        crown_weight=10,
        simple=True,
        bbbarrage_min_scale=50,
        interaction=InteractionMethods(),
    ),  #
    Enemies.KasplatDK: EnemyData(
        name="Kasplat (DK)",
        crown_weight=6,
        kasplat=True,
        interaction=InteractionMethods(),
    ),  #
    Enemies.KasplatDiddy: EnemyData(
        name="Kasplat (Diddy)",
        crown_weight=6,
        kasplat=True,
        interaction=InteractionMethods(),
    ),  #
    Enemies.KasplatLanky: EnemyData(
        name="Kasplat (Lanky)",
        crown_weight=6,
        kasplat=True,
        interaction=InteractionMethods(),
    ),  #
    Enemies.KasplatTiny: EnemyData(
        name="Kasplat (Tiny)",
        crown_weight=6,
        kasplat=True,
        interaction=InteractionMethods(),
    ),  #
    Enemies.KasplatChunky: EnemyData(
        name="Kasplat (Chunky)",
        crown_weight=6,
        kasplat=True,
        interaction=InteractionMethods(),
    ),  #
    Enemies.ZingerRobo: EnemyData(
        name="Robo-Zingers",
        e_type=EnemySubtype.Air,
        air=True,
        crown_weight=5,
        disruptive=1,
        interaction=InteractionMethods(kill_melee=False,kill_orange=False,kill_shockwave=False),
    ),  #
    Enemies.Krossbones: EnemyData(
        name="Krossbones",
        e_type=EnemySubtype.GroundSimple,
        crown_weight=10,
        simple=True,
        bbbarrage_min_scale=50,
        interaction=InteractionMethods(),
    ),  #
    Enemies.Shuri: EnemyData(
        name="Shuri",
        e_type=EnemySubtype.Water,
        crown_enabled=False,
        minigame_enabled=False,
        interaction=InteractionMethods(can_kill=False),
    ),  #
    Enemies.Gimpfish: EnemyData(
        name="Gimpfish",
        e_type=EnemySubtype.Water,
        aggro=1,
        crown_enabled=False,
        minigame_enabled=False,
        interaction=InteractionMethods(can_kill=False),
    ),
    Enemies.MrDice0: EnemyData(
        name="Mr Dice (Green)",
        e_type=EnemySubtype.GroundSimple,
        crown_weight=10,
        simple=True,
        bbbarrage_min_scale=80,
        interaction=InteractionMethods(),
    ),  # Should be aggro 4, but I think this is because it normally spawns in the BHDM fight
    Enemies.SirDomino: EnemyData(
        name="Sir Domino",
        e_type=EnemySubtype.GroundSimple,
        crown_weight=10,
        simple=True,
        bbbarrage_min_scale=60,
        interaction=InteractionMethods(),
    ),  #
    Enemies.MrDice1: EnemyData(
        name="Mr Dice (Red)",
        e_type=EnemySubtype.GroundSimple,
        crown_weight=10,
        simple=True,
        bbbarrage_min_scale=100,
        interaction=InteractionMethods(),
    ),  #
    Enemies.FireballGlasses: EnemyData(
        name="Fireball with Glasses",
        e_type=EnemySubtype.GroundSimple,
        aggro=35,
        min_speed=100,
        max_speed=255,
        crown_weight=10,
        killable=False,
        interaction=InteractionMethods(kill_gun=False,kill_orange=False),
    ),  # 29 for if you want them to respond to the rabbit
    Enemies.SpiderSmall: EnemyData(
        name="Spider",
        e_type=EnemySubtype.GroundSimple,
        crown_weight=7,
        disruptive=1,
        crown_enabled=False,
        interaction=InteractionMethods(),
    ),  # with projectiles, disruptive will need to be set to 2
    Enemies.Bat: EnemyData(
        name="Bat",
        e_type=EnemySubtype.Air,
        air=True,
        crown_weight=5,
        minigame_enabled=False,
        disruptive=1,
        interaction=InteractionMethods(kill_melee=False,kill_orange=False,kill_shockwave=False),
    ),  #
    Enemies.EvilTomato: EnemyData(
        name="Evil Tomato",
        aggro=4,
        crown_enabled=False,
        minigame_enabled=False,
        selector_enabled=False,
        interaction=InteractionMethods(can_kill=False), # Can be killed with Hunky
    ),
    Enemies.Ghost: EnemyData(
        name="Ghost",
        e_type=EnemySubtype.GroundSimple,
        crown_weight=10,
        simple=True,
        bbbarrage_min_scale=70,
        interaction=InteractionMethods(),
    ),  #
    Enemies.Pufftup: EnemyData(
        name="Pufftup",
        e_type=EnemySubtype.Water,
        crown_enabled=False,
        size_cap=40,
        minigame_enabled=False,
        interaction=InteractionMethods(kill_gun=False,kill_orange=False,kill_shockwave=False),
    ),  #
    Enemies.Kosha: EnemyData(
        name="Kosha",
        e_type=EnemySubtype.GroundBeefy,
        crown_weight=1,
        killable=False,
        disruptive=2,
        interaction=InteractionMethods(kill_gun=False,kill_melee=False),
    ),  #
    Enemies.GetOut: EnemyData(
        name="Get Out Guy",
        aggro=6,
        crown_weight=1,
        minigame_enabled=False,
        disruptive=1,
        interaction=InteractionMethods(can_kill=False),
    ),
    Enemies.Guard: EnemyData(
        name="Kop",
        e_type=EnemySubtype.GroundBeefy,
        aggro=1,
        crown_enabled=False,
        minigame_enabled=False,
        interaction=InteractionMethods(kill_melee=False, can_bypass=False), # Can be meleed with distraction mechanic, but we'll ignore that for now
    ),
    # Enemies.Bug: EnemyData(aggro=0x40,crown_enabled=False,),
}

enemy_location_list = {
    # Angry Aztec
    # Main
    EnemyLocations.AztecMain_VaseRoom0: EnemyLoc(Maps.AngryAztec, Enemies.ZingerLime, 2, [], True),
    EnemyLocations.AztecMain_VaseRoom1: EnemyLoc(Maps.AngryAztec, Enemies.ZingerLime, 4, [], True),
    EnemyLocations.AztecMain_TunnelPad0: EnemyLoc(Maps.AngryAztec, Enemies.ZingerLime, 10, [], True),
    EnemyLocations.AztecMain_TunnelCage0: EnemyLoc(Maps.AngryAztec, Enemies.KlaptrapGreen, 13, [], True),
    EnemyLocations.AztecMain_TunnelCage1: EnemyLoc(Maps.AngryAztec, Enemies.KlaptrapGreen, 14, [], True),
    EnemyLocations.AztecMain_TunnelCage2: EnemyLoc(Maps.AngryAztec, Enemies.KlaptrapGreen, 15, [], True),
    EnemyLocations.AztecMain_StartingTunnel0: EnemyLoc(Maps.AngryAztec, Enemies.Kremling, 20, [], True),
    EnemyLocations.AztecMain_StartingTunnel1: EnemyLoc(Maps.AngryAztec, Enemies.Kremling, 21, [], True),
    EnemyLocations.AztecMain_OasisDoor: EnemyLoc(Maps.AngryAztec, Enemies.Kremling, 23, [], True),
    EnemyLocations.AztecMain_TunnelCage3: EnemyLoc(Maps.AngryAztec, Enemies.Kremling, 26, [], True),
    EnemyLocations.AztecMain_OutsideLlama: EnemyLoc(Maps.AngryAztec, Enemies.Kremling, 27, [], True),
    EnemyLocations.AztecMain_OutsideTower: EnemyLoc(Maps.AngryAztec, Enemies.Kremling, 28, [], True),
    EnemyLocations.AztecMain_TunnelPad1: EnemyLoc(Maps.AngryAztec, Enemies.ZingerLime, 31, [], True),
    EnemyLocations.AztecMain_NearCandy: EnemyLoc(Maps.AngryAztec, Enemies.ZingerLime, 32, [], True),
    EnemyLocations.AztecMain_AroundTotem: EnemyLoc(Maps.AngryAztec, Enemies.KlaptrapGreen, 33, [], True),
    EnemyLocations.AztecMain_StartingTunnel2: EnemyLoc(Maps.AngryAztec, Enemies.ZingerLime, 38, [], True),
    EnemyLocations.AztecMain_StartingTunnel3: EnemyLoc(Maps.AngryAztec, Enemies.ZingerLime, 39, [], True),
    EnemyLocations.AztecMain_Outside5DT: EnemyLoc(Maps.AngryAztec, Enemies.ZingerLime, 41, [], True),
    EnemyLocations.AztecMain_NearSnoopTunnel: EnemyLoc(Maps.AngryAztec, Enemies.Kremling, 42, [], True),
    # Lobby
    EnemyLocations.AztecLobby_Pad0: EnemyLoc(Maps.AngryAztecLobby, Enemies.ZingerLime, 2, [], True),
    EnemyLocations.AztecLobby_Pad1: EnemyLoc(Maps.AngryAztecLobby, Enemies.ZingerLime, 3, [], True),
    # DK 5DT
    EnemyLocations.AztecDK5DT_StartTrap0: EnemyLoc(Maps.AztecDonkey5DTemple, Enemies.Kaboom, 5, [], True),
    EnemyLocations.AztecDK5DT_StartTrap1: EnemyLoc(Maps.AztecDonkey5DTemple, Enemies.Kaboom, 6, [], True),
    EnemyLocations.AztecDK5DT_StartTrap2: EnemyLoc(Maps.AztecDonkey5DTemple, Enemies.Kaboom, 7, [], True),
    EnemyLocations.AztecDK5DT_EndTrap0: EnemyLoc(Maps.AztecDonkey5DTemple, Enemies.Kaboom, 10, [], True),
    EnemyLocations.AztecDK5DT_EndTrap1: EnemyLoc(Maps.AztecDonkey5DTemple, Enemies.Kaboom, 11, [], True),
    EnemyLocations.AztecDK5DT_EndTrap2: EnemyLoc(Maps.AztecDonkey5DTemple, Enemies.Kaboom, 12, [], True),
    EnemyLocations.AztecDK5DT_EndPath0: EnemyLoc(Maps.AztecDonkey5DTemple, Enemies.KlaptrapPurple, 13, [], True),
    EnemyLocations.AztecDK5DT_EndPath1: EnemyLoc(Maps.AztecDonkey5DTemple, Enemies.KlaptrapPurple, 14, [], True),
    EnemyLocations.AztecDK5DT_StartPath: EnemyLoc(Maps.AztecDonkey5DTemple, Enemies.KlaptrapPurple, 15, [], True),
    # Diddy 5DT
    EnemyLocations.AztecDiddy5DT_EndTrap0: EnemyLoc(Maps.AztecDiddy5DTemple, Enemies.Klobber, 4, [], True),
    EnemyLocations.AztecDiddy5DT_EndTrap1: EnemyLoc(Maps.AztecDiddy5DTemple, Enemies.Klobber, 5, [], True),
    EnemyLocations.AztecDiddy5DT_EndTrap2: EnemyLoc(Maps.AztecDiddy5DTemple, Enemies.Klobber, 6, [], True),
    EnemyLocations.AztecDiddy5DT_StartLeft0: EnemyLoc(Maps.AztecDiddy5DTemple, Enemies.Kremling, 9, [], True),
    EnemyLocations.AztecDiddy5DT_StartLeft1: EnemyLoc(Maps.AztecDiddy5DTemple, Enemies.Kremling, 10, [], True),
    EnemyLocations.AztecDiddy5DT_Reward: EnemyLoc(Maps.AztecDiddy5DTemple, Enemies.Klump, 11, [], True),
    EnemyLocations.AztecDiddy5DT_SecondSwitch: EnemyLoc(Maps.AztecDiddy5DTemple, Enemies.Kremling, 12, [], True),
    # Lanky 5DT
    EnemyLocations.AztecLanky5DT_JoiningPaths: EnemyLoc(Maps.AztecLanky5DTemple, Enemies.Klump, 2, [], True),
    EnemyLocations.AztecLanky5DT_EndTrap: EnemyLoc(Maps.AztecLanky5DTemple, Enemies.Klump, 3, [], True),
    EnemyLocations.AztecLanky5DT_Reward: EnemyLoc(Maps.AztecLanky5DTemple, Enemies.Klump, 4, [], True),
    # Tiny 5DT
    EnemyLocations.AztecTiny5DT_StartRightFront: EnemyLoc(Maps.AztecTiny5DTemple, Enemies.ZingerLime, 2, [], True),
    EnemyLocations.AztecTiny5DT_StartLeftBack: EnemyLoc(Maps.AztecTiny5DTemple, Enemies.ZingerLime, 4, [], True),
    EnemyLocations.AztecTiny5DT_StartRightBack: EnemyLoc(Maps.AztecTiny5DTemple, Enemies.ZingerLime, 5, [], True),
    EnemyLocations.AztecTiny5DT_StartLeftFront: EnemyLoc(Maps.AztecTiny5DTemple, Enemies.ZingerLime, 6, [], True),
    EnemyLocations.AztecTiny5DT_Reward0: EnemyLoc(Maps.AztecTiny5DTemple, Enemies.ZingerLime, 7, [], True),
    EnemyLocations.AztecTiny5DT_Reward1: EnemyLoc(Maps.AztecTiny5DTemple, Enemies.ZingerLime, 8, [], True),
    EnemyLocations.AztecTiny5DT_DeadEnd0: EnemyLoc(Maps.AztecTiny5DTemple, Enemies.ZingerLime, 9, [], True),
    EnemyLocations.AztecTiny5DT_DeadEnd1: EnemyLoc(Maps.AztecTiny5DTemple, Enemies.ZingerLime, 10, [], True),
    # Chunky 5DT
    EnemyLocations.AztecChunky5DT_StartRight: EnemyLoc(Maps.AztecChunky5DTemple, Enemies.Klobber, 2, [], True),
    EnemyLocations.AztecChunky5DT_StartLeft: EnemyLoc(Maps.AztecChunky5DTemple, Enemies.Klobber, 3, [], True),
    EnemyLocations.AztecChunky5DT_SecondRight: EnemyLoc(Maps.AztecChunky5DTemple, Enemies.Klobber, 5, [], True),
    EnemyLocations.AztecChunky5DT_SecondLeft: EnemyLoc(Maps.AztecChunky5DTemple, Enemies.Klobber, 6, [], True),
    EnemyLocations.AztecChunky5DT_Reward: EnemyLoc(Maps.AztecChunky5DTemple, Enemies.ZingerLime, 7, [], True),
    # Llama Temple
    EnemyLocations.AztecLlama_KongFreeInstrument: EnemyLoc(Maps.AztecLlamaTemple, Enemies.KlaptrapPurple, 5, [], True),
    EnemyLocations.AztecLlama_DinoInstrument: EnemyLoc(Maps.AztecLlamaTemple, Enemies.KlaptrapPurple, 6, [], True),
    EnemyLocations.AztecLlama_Matching0: EnemyLoc(Maps.AztecLlamaTemple, Enemies.Kremling, 10, [], True),
    EnemyLocations.AztecLlama_Matching1: EnemyLoc(Maps.AztecLlamaTemple, Enemies.Kremling, 11, [], True),
    EnemyLocations.AztecLlama_Right: EnemyLoc(Maps.AztecLlamaTemple, Enemies.Kremling, 14, [], True),
    EnemyLocations.AztecLlama_Left: EnemyLoc(Maps.AztecLlamaTemple, Enemies.Kremling, 15, [], True),
    EnemyLocations.AztecLlama_MelonCrate: EnemyLoc(Maps.AztecLlamaTemple, Enemies.KlaptrapPurple, 16, [], True),
    EnemyLocations.AztecLlama_SlamSwitch: EnemyLoc(Maps.AztecLlamaTemple, Enemies.KlaptrapPurple, 17, [], True),
    # Tiny Temple
    EnemyLocations.AztecTemple_Rotating00: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 1, [], True),
    EnemyLocations.AztecTemple_Rotating01: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 2, [], True),
    EnemyLocations.AztecTemple_Rotating02: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 3, [], True),
    EnemyLocations.AztecTemple_Rotating03: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 4, [], True),
    EnemyLocations.AztecTemple_Rotating04: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 5, [], True),
    EnemyLocations.AztecTemple_Rotating05: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 6, [], True),
    EnemyLocations.AztecTemple_Rotating06: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 7, [], True),
    EnemyLocations.AztecTemple_Rotating07: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 8, [], True),
    EnemyLocations.AztecTemple_Rotating08: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 9, [], True),
    EnemyLocations.AztecTemple_Rotating09: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 10, [], True),
    EnemyLocations.AztecTemple_Rotating10: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 11, [], True),
    EnemyLocations.AztecTemple_Rotating11: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 12, [], True),
    EnemyLocations.AztecTemple_Rotating12: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 13, [], True),
    EnemyLocations.AztecTemple_Rotating13: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 14, [], True),
    EnemyLocations.AztecTemple_Rotating14: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 15, [], True),
    EnemyLocations.AztecTemple_Rotating15: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 16, [], True),
    EnemyLocations.AztecTemple_MiniRoom00: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 20, [], True),
    EnemyLocations.AztecTemple_MiniRoom01: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 21, [], True),
    EnemyLocations.AztecTemple_MiniRoom02: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 22, [], True),
    EnemyLocations.AztecTemple_MiniRoom03: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 23, [], True),
    EnemyLocations.AztecTemple_GuardRotating0: EnemyLoc(Maps.AztecTinyTemple, Enemies.Klobber, 24, [], True),
    EnemyLocations.AztecTemple_GuardRotating1: EnemyLoc(Maps.AztecTinyTemple, Enemies.Klobber, 36, [], True),
    EnemyLocations.AztecTemple_MainRoom0: EnemyLoc(Maps.AztecTinyTemple, Enemies.Kremling, 26, [], True),
    EnemyLocations.AztecTemple_MainRoom1: EnemyLoc(Maps.AztecTinyTemple, Enemies.Kremling, 28, [], True),
    EnemyLocations.AztecTemple_MainRoom2: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 35, [], True),
    EnemyLocations.AztecTemple_KongRoom0: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 29, [], True),
    EnemyLocations.AztecTemple_KongRoom1: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 30, [], True),
    EnemyLocations.AztecTemple_KongRoom2: EnemyLoc(Maps.AztecTinyTemple, Enemies.Kremling, 32, [], True),
    EnemyLocations.AztecTemple_KongRoom3: EnemyLoc(Maps.AztecTinyTemple, Enemies.Kremling, 33, [], True),
    EnemyLocations.AztecTemple_KongRoom4: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 34, [], True),
    EnemyLocations.AztecTemple_Underwater: EnemyLoc(Maps.AztecTinyTemple, Enemies.Shuri, 37, [], True),
}

EnemySelector = []
for enemyEnum, enemy in EnemyMetaData.items():
    if enemy.selector_enabled:
        EnemySelector.append({"name": enemy.name, "value": enemyEnum.name, "tooltip": ""})
EnemySelector = sorted(EnemySelector.copy(), key=lambda d: d["name"])
