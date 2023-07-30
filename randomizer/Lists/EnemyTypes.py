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


class InteractionMethods:
    """Information about interactions with enemies."""

    def __init__(
        self,
        *,
        kill_melee=True,  # Killing can be done with regular attacks
        kill_orange=True,  # Killing can be done with oranges
        kill_gun=True,  # Killing can be done with a gun
        kill_shockwave=True,  # Killing can be done with a shockwave attack
        can_kill=True,  # Master control of all kill variables
        can_bypass=True,  # Enemy can be bypassed without any additional tricks
    ):
        """Initialize with given data."""
        self.kill_melee = kill_melee and can_kill
        self.kill_orange = kill_orange and can_kill
        self.kill_gun = kill_gun and can_kill
        self.kill_shockwave = kill_shockwave and can_kill
        self.can_bypass = can_bypass


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
        interaction: InteractionMethods = None,
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


class EnemyLoc:
    """Information about an enemy."""

    def __init__(self, map: Maps, default_enemy: Enemies, id: int, banned_enemies: list, enable_randomization: bool, respawns: bool = True):
        """Initialize with given parameters."""
        self.map = map
        self.default_enemy = default_enemy
        self.enemy = default_enemy
        self.id = id
        self.banned_enemies = banned_enemies.copy()
        self.enable_randomization = enable_randomization
        self.default_type = EnemySubtype.GroundSimple
        self.allowed_enemies = []
        self.idle_speed: int = None
        self.aggro_speed: int = None
        self.respawns = respawns
        if enable_randomization:
            if default_enemy in EnemyMetaData:
                self.default_type = EnemyMetaData[default_enemy].e_type
            self.allowed_enemies = [enemy for enemy in EnemyMetaData if EnemyMetaData[enemy].e_type == self.default_type and enemy not in banned_enemies]

    def placeNewEnemy(self, enabled_enemies: list, enable_speed: bool) -> Enemies:
        """Place new enemy in slot."""
        if self.enable_randomization:
            permitted = [enemy for enemy in self.allowed_enemies if enemy in enabled_enemies or len(enabled_enemies) == 0]
            if len(permitted) > 0:
                self.enemy = random.choice(permitted)
            if enable_speed and self.enemy in EnemyMetaData:
                enemy_data = EnemyMetaData[self.enemy]
                self.aggro_speed = random.randint(enemy_data.min_speed, enemy_data.max_speed)
        return self.enemy

    def canKill(self) -> bool:
        """Determine if the enemy can be killed."""
        if self.enemy in EnemyMetaData:
            interaction: InteractionMethods = EnemyMetaData[self.enemy].interaction
            if interaction is not None:
                if interaction.kill_melee:
                    return True
                return True  # TODO: Handle logic with the different killing methods
        return False

    def canBypass(self) -> bool:
        """Determine if the enemy can be bypassed."""
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
        interaction=InteractionMethods(kill_melee=False, kill_orange=False, kill_shockwave=False),
    ),  #
    Enemies.Klobber: EnemyData(
        name="Klobber",
        e_type=EnemySubtype.GroundBeefy,
        aggro=4,
        crown_weight=2,
        killable=False,
        disruptive=2,
        interaction=InteractionMethods(kill_gun=False, kill_melee=False),
    ),
    Enemies.Klump: EnemyData(
        name="Klump",
        e_type=EnemySubtype.GroundBeefy,
        crown_weight=1,
        killable=False,
        disruptive=1,
        interaction=InteractionMethods(kill_gun=False, kill_melee=False),
    ),  #
    Enemies.Kaboom: EnemyData(
        name="Kaboom",
        e_type=EnemySubtype.GroundBeefy,
        aggro=4,
        crown_weight=2,
        killable=False,
        disruptive=2,
        interaction=InteractionMethods(kill_gun=False, kill_melee=False),
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
        interaction=InteractionMethods(kill_orange=False, kill_melee=False, kill_shockwave=False),
    ),  #
    Enemies.KlaptrapPurple: EnemyData(
        name="Klaptrap (Purple)",
        e_type=EnemySubtype.GroundBeefy,
        crown_weight=2,
        killable=False,
        disruptive=1,
        interaction=InteractionMethods(kill_gun=False, kill_melee=False, kill_shockwave=False),
    ),  #
    Enemies.KlaptrapRed: EnemyData(
        name="Klaptrap (Red)",
        e_type=EnemySubtype.GroundBeefy,
        crown_weight=2,
        killable=False,
        disruptive=1,
        interaction=InteractionMethods(kill_melee=False, kill_shockwave=False),
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
        interaction=InteractionMethods(kill_melee=False, kill_gun=False),
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
        interaction=InteractionMethods(kill_melee=False, kill_orange=False, kill_shockwave=False),
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
        interaction=InteractionMethods(kill_gun=False, kill_orange=False),
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
        interaction=InteractionMethods(kill_melee=False, kill_orange=False, kill_shockwave=False),
    ),  #
    Enemies.EvilTomato: EnemyData(
        name="Evil Tomato",
        aggro=4,
        crown_enabled=False,
        minigame_enabled=False,
        selector_enabled=False,
        interaction=InteractionMethods(can_kill=False),  # Can be killed with Hunky
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
        interaction=InteractionMethods(kill_gun=False, kill_orange=False, kill_shockwave=False),
    ),  #
    Enemies.Kosha: EnemyData(
        name="Kosha",
        e_type=EnemySubtype.GroundBeefy,
        crown_weight=1,
        killable=False,
        disruptive=2,
        interaction=InteractionMethods(kill_gun=False, kill_melee=False),
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
        interaction=InteractionMethods(kill_melee=False, can_bypass=False),  # Can be meleed with distraction mechanic, but we'll ignore that for now
    ),
    # Enemies.Bug: EnemyData(aggro=0x40,crown_enabled=False,),
}

enemies_nokill_gun = [enemy for enemy in EnemyMetaData if ((not EnemyMetaData[enemy].interaction.kill_gun) and (not EnemyMetaData[enemy].interaction.kill_melee)) or enemy == Enemies.Guard]

enemy_location_list = {
    # Japes
    # Main
    EnemyLocations.JapesMain_Start: EnemyLoc(Maps.JungleJapes, Enemies.BeaverBlue, 2, [], True),
    EnemyLocations.JapesMain_DiddyCavern: EnemyLoc(Maps.JungleJapes, Enemies.BeaverBlue, 4, [], True),
    EnemyLocations.JapesMain_Tunnel0: EnemyLoc(Maps.JungleJapes, Enemies.BeaverBlue, 5, [], True),
    EnemyLocations.JapesMain_Tunnel1: EnemyLoc(Maps.JungleJapes, Enemies.BeaverBlue, 6, [], True),
    EnemyLocations.JapesMain_Storm0: EnemyLoc(Maps.JungleJapes, Enemies.BeaverBlue, 15, [], True),
    EnemyLocations.JapesMain_Storm1: EnemyLoc(Maps.JungleJapes, Enemies.BeaverBlue, 18, [], True),
    EnemyLocations.JapesMain_Storm2: EnemyLoc(Maps.JungleJapes, Enemies.BeaverBlue, 20, [], True),
    EnemyLocations.JapesMain_Hive0: EnemyLoc(Maps.JungleJapes, Enemies.ZingerLime, 28, [], True),
    EnemyLocations.JapesMain_Hive1: EnemyLoc(Maps.JungleJapes, Enemies.ZingerLime, 29, [], True),
    EnemyLocations.JapesMain_Hive2: EnemyLoc(Maps.JungleJapes, Enemies.ZingerLime, 30, [], True),
    EnemyLocations.JapesMain_Hive3: EnemyLoc(Maps.JungleJapes, Enemies.Kremling, 36, [], True),
    EnemyLocations.JapesMain_Hive4: EnemyLoc(Maps.JungleJapes, Enemies.Kremling, 37, [], True),
    EnemyLocations.JapesMain_KilledInDemo: EnemyLoc(Maps.JungleJapes, Enemies.BeaverBlue, 33, [], True),
    EnemyLocations.JapesMain_NearUnderground: EnemyLoc(Maps.JungleJapes, Enemies.ZingerCharger, 49, [], True),
    EnemyLocations.JapesMain_NearPainting0: EnemyLoc(Maps.JungleJapes, Enemies.BeaverBlue, 34, [], True),
    EnemyLocations.JapesMain_NearPainting1: EnemyLoc(Maps.JungleJapes, Enemies.BeaverBlue, 35, [], True),
    EnemyLocations.JapesMain_NearPainting2: EnemyLoc(Maps.JungleJapes, Enemies.ZingerCharger, 48, [], True),
    EnemyLocations.JapesMain_Mountain: EnemyLoc(Maps.JungleJapes, Enemies.ZingerCharger, 50, [], True),
    EnemyLocations.JapesMain_FeatherTunnel: EnemyLoc(Maps.JungleJapes, Enemies.ZingerLime, 52, [], True),
    EnemyLocations.JapesMain_MiddleTunnel: EnemyLoc(Maps.JungleJapes, Enemies.BeaverBlue, 54, [], True),
    # Lobby
    EnemyLocations.JapesLobby_Enemy0: EnemyLoc(Maps.JungleJapesLobby, Enemies.BeaverBlue, 1, [], True),
    EnemyLocations.JapesLobby_Enemy1: EnemyLoc(Maps.JungleJapesLobby, Enemies.BeaverBlue, 2, [], True),
    # Painting
    EnemyLocations.JapesPainting_Gauntlet0: EnemyLoc(Maps.JapesLankyCave, Enemies.ZingerCharger, 2, enemies_nokill_gun, True),
    EnemyLocations.JapesPainting_Gauntlet1: EnemyLoc(Maps.JapesLankyCave, Enemies.ZingerCharger, 3, enemies_nokill_gun, True),
    EnemyLocations.JapesPainting_Gauntlet2: EnemyLoc(Maps.JapesLankyCave, Enemies.ZingerCharger, 4, enemies_nokill_gun, True),
    EnemyLocations.JapesPainting_Gauntlet3: EnemyLoc(Maps.JapesLankyCave, Enemies.ZingerCharger, 5, enemies_nokill_gun, True),
    EnemyLocations.JapesPainting_Gauntlet4: EnemyLoc(Maps.JapesLankyCave, Enemies.ZingerCharger, 6, enemies_nokill_gun, True),
    # Mountain
    EnemyLocations.JapesMountain_Start0: EnemyLoc(Maps.JapesMountain, Enemies.BeaverBlue, 1, [], True),
    EnemyLocations.JapesMountain_Start1: EnemyLoc(Maps.JapesMountain, Enemies.BeaverBlue, 2, [], True),
    EnemyLocations.JapesMountain_Start2: EnemyLoc(Maps.JapesMountain, Enemies.BeaverBlue, 6, [], True),
    EnemyLocations.JapesMountain_Start3: EnemyLoc(Maps.JapesMountain, Enemies.ZingerCharger, 8, [], True),
    EnemyLocations.JapesMountain_Start4: EnemyLoc(Maps.JapesMountain, Enemies.ZingerCharger, 9, [], True),
    EnemyLocations.JapesMountain_NearGateSwitch0: EnemyLoc(Maps.JapesMountain, Enemies.ZingerLime, 13, [], True),
    EnemyLocations.JapesMountain_NearGateSwitch1: EnemyLoc(Maps.JapesMountain, Enemies.ZingerLime, 14, [], True),
    EnemyLocations.JapesMountain_HiLo: EnemyLoc(Maps.JapesMountain, Enemies.Klump, 15, [], True),
    EnemyLocations.JapesMountain_Conveyor0: EnemyLoc(Maps.JapesMountain, Enemies.Klump, 16, [], True),
    EnemyLocations.JapesMountain_Conveyor1: EnemyLoc(Maps.JapesMountain, Enemies.Klump, 17, [], True),
    # Shellhive
    EnemyLocations.JapesShellhive_FirstRoom: EnemyLoc(Maps.JapesTinyHive, Enemies.KlaptrapPurple, 7, [], True),
    EnemyLocations.JapesShellhive_SecondRoom0: EnemyLoc(Maps.JapesTinyHive, Enemies.KlaptrapPurple, 8, [], True),
    EnemyLocations.JapesShellhive_SecondRoom1: EnemyLoc(Maps.JapesTinyHive, Enemies.KlaptrapPurple, 9, [], True),
    EnemyLocations.JapesShellhive_ThirdRoom0: EnemyLoc(Maps.JapesTinyHive, Enemies.KlaptrapPurple, 10, [], True),
    EnemyLocations.JapesShellhive_ThirdRoom1: EnemyLoc(Maps.JapesTinyHive, Enemies.KlaptrapPurple, 11, [], True),
    EnemyLocations.JapesShellhive_ThirdRoom2: EnemyLoc(Maps.JapesTinyHive, Enemies.ZingerCharger, 12, [], True),
    EnemyLocations.JapesShellhive_ThirdRoom3: EnemyLoc(Maps.JapesTinyHive, Enemies.ZingerCharger, 13, [], True),
    EnemyLocations.JapesShellhive_MainRoom: EnemyLoc(Maps.JapesTinyHive, Enemies.ZingerCharger, 14, [], True),
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
    EnemyLocations.AztecMain_StartingTunnel2: EnemyLoc(Maps.AngryAztec, Enemies.ZingerCharger, 38, [], True),
    EnemyLocations.AztecMain_StartingTunnel3: EnemyLoc(Maps.AngryAztec, Enemies.ZingerCharger, 39, [], True),
    EnemyLocations.AztecMain_Outside5DT: EnemyLoc(Maps.AngryAztec, Enemies.ZingerLime, 41, [], True),
    EnemyLocations.AztecMain_NearSnoopTunnel: EnemyLoc(Maps.AngryAztec, Enemies.Kremling, 42, [], True),
    # Lobby
    EnemyLocations.AztecLobby_Pad0: EnemyLoc(Maps.AngryAztecLobby, Enemies.ZingerCharger, 2, [], True),
    EnemyLocations.AztecLobby_Pad1: EnemyLoc(Maps.AngryAztecLobby, Enemies.ZingerCharger, 3, [], True),
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
    EnemyLocations.AztecTemple_Rotating00: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 1, enemies_nokill_gun, True, False),
    EnemyLocations.AztecTemple_Rotating01: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 2, enemies_nokill_gun, True, False),
    EnemyLocations.AztecTemple_Rotating02: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 3, enemies_nokill_gun, True, False),
    EnemyLocations.AztecTemple_Rotating03: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 4, enemies_nokill_gun, True, False),
    EnemyLocations.AztecTemple_Rotating04: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 5, enemies_nokill_gun, True, False),
    EnemyLocations.AztecTemple_Rotating05: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 6, enemies_nokill_gun, True, False),
    EnemyLocations.AztecTemple_Rotating06: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 7, enemies_nokill_gun, True, False),
    EnemyLocations.AztecTemple_Rotating07: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 8, enemies_nokill_gun, True, False),
    EnemyLocations.AztecTemple_Rotating08: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 9, enemies_nokill_gun, True, False),
    EnemyLocations.AztecTemple_Rotating09: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 10, enemies_nokill_gun, True, False),
    EnemyLocations.AztecTemple_Rotating10: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 11, enemies_nokill_gun, True, False),
    EnemyLocations.AztecTemple_Rotating11: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 12, enemies_nokill_gun, True, False),
    EnemyLocations.AztecTemple_Rotating12: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 13, enemies_nokill_gun, True, False),
    EnemyLocations.AztecTemple_Rotating13: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 14, enemies_nokill_gun, True, False),
    EnemyLocations.AztecTemple_Rotating14: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 15, enemies_nokill_gun, True, False),
    EnemyLocations.AztecTemple_Rotating15: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 16, enemies_nokill_gun, True, False),
    EnemyLocations.AztecTemple_MiniRoom00: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 20, [Enemies.Guard], True, False),
    EnemyLocations.AztecTemple_MiniRoom01: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 21, [Enemies.Guard], True, False),
    EnemyLocations.AztecTemple_MiniRoom02: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 22, [Enemies.Guard], True, False),
    EnemyLocations.AztecTemple_MiniRoom03: EnemyLoc(Maps.AztecTinyTemple, Enemies.KlaptrapGreen, 23, [Enemies.Guard], True, False),
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
    # Factory
    # Main
    EnemyLocations.FactoryMain_CandyCranky0: EnemyLoc(Maps.FranticFactory, Enemies.Kremling, 33, [], True),
    EnemyLocations.FactoryMain_CandyCranky1: EnemyLoc(Maps.FranticFactory, Enemies.Kremling, 72, [], True),
    EnemyLocations.FactoryMain_LobbyLeft: EnemyLoc(Maps.FranticFactory, Enemies.RoboKremling, 74, [], True),
    EnemyLocations.FactoryMain_LobbyRight: EnemyLoc(Maps.FranticFactory, Enemies.RoboKremling, 58, [], True),
    EnemyLocations.FactoryMain_StorageRoom: EnemyLoc(Maps.FranticFactory, Enemies.ZingerRobo, 91, [], True),
    EnemyLocations.FactoryMain_BlockTower0: EnemyLoc(Maps.FranticFactory, Enemies.MrDice1, 78, [], True),
    EnemyLocations.FactoryMain_BlockTower1: EnemyLoc(Maps.FranticFactory, Enemies.SirDomino, 79, [], True),
    EnemyLocations.FactoryMain_BlockTower2: EnemyLoc(Maps.FranticFactory, Enemies.MrDice1, 80, [], True),
    EnemyLocations.FactoryMain_TunnelToHatch: EnemyLoc(Maps.FranticFactory, Enemies.RoboKremling, 59, [Enemies.Guard], True),
    EnemyLocations.FactoryMain_TunnelToProd0: EnemyLoc(Maps.FranticFactory, Enemies.Kremling, 63, [Enemies.Guard], True),
    EnemyLocations.FactoryMain_TunnelToProd1: EnemyLoc(Maps.FranticFactory, Enemies.RoboKremling, 73, [Enemies.Guard], True),
    EnemyLocations.FactoryMain_TunnelToBlockTower: EnemyLoc(Maps.FranticFactory, Enemies.RoboKremling, 84, [], True),
    EnemyLocations.FactoryMain_TunnelToRace0: EnemyLoc(Maps.FranticFactory, Enemies.RoboKremling, 87, [Enemies.Guard], True),
    EnemyLocations.FactoryMain_TunnelToRace1: EnemyLoc(Maps.FranticFactory, Enemies.ZingerRobo, 88, [Enemies.Guard], True),
    EnemyLocations.FactoryMain_LowWarp4: EnemyLoc(Maps.FranticFactory, Enemies.RoboKremling, 66, [], True),
    EnemyLocations.FactoryMain_DiddySwitch: EnemyLoc(Maps.FranticFactory, Enemies.ZingerRobo, 67, [], True),
    EnemyLocations.FactoryMain_ToBlockTowerTunnel: EnemyLoc(Maps.FranticFactory, Enemies.ZingerRobo, 62, [Enemies.Guard], True),
    EnemyLocations.FactoryMain_DarkRoom0: EnemyLoc(Maps.FranticFactory, Enemies.ZingerRobo, 70, [], True),
    EnemyLocations.FactoryMain_DarkRoom1: EnemyLoc(Maps.FranticFactory, Enemies.ZingerRobo, 71, [], True),
    EnemyLocations.FactoryMain_BHDM0: EnemyLoc(Maps.FranticFactory, Enemies.MrDice0, 35, [], False, False),
    EnemyLocations.FactoryMain_BHDM1: EnemyLoc(Maps.FranticFactory, Enemies.SirDomino, 36, [], False, False),
    EnemyLocations.FactoryMain_BHDM2: EnemyLoc(Maps.FranticFactory, Enemies.SirDomino, 37, [], False, False),
    EnemyLocations.FactoryMain_BHDM3: EnemyLoc(Maps.FranticFactory, Enemies.MrDice0, 38, [], False, False),
    EnemyLocations.FactoryMain_BHDM4: EnemyLoc(Maps.FranticFactory, Enemies.MrDice0, 39, [], False, False),
    EnemyLocations.FactoryMain_BHDM5: EnemyLoc(Maps.FranticFactory, Enemies.Ruler, 40, [], False, False),
    EnemyLocations.FactoryMain_BHDM6: EnemyLoc(Maps.FranticFactory, Enemies.Ruler, 41, [], False, False),
    EnemyLocations.FactoryMain_BHDM7: EnemyLoc(Maps.FranticFactory, Enemies.MrDice1, 42, [], False, False),
    EnemyLocations.FactoryMain_BHDM8: EnemyLoc(Maps.FranticFactory, Enemies.SirDomino, 43, [], False, False),
    EnemyLocations.FactoryMain_BHDM9: EnemyLoc(Maps.FranticFactory, Enemies.SirDomino, 44, [], False, False),
    EnemyLocations.FactoryMain_1342Gauntlet0: EnemyLoc(Maps.FranticFactory, Enemies.ZingerRobo, 49, [], True),
    EnemyLocations.FactoryMain_1342Gauntlet1: EnemyLoc(Maps.FranticFactory, Enemies.RoboKremling, 50, [], True),
    EnemyLocations.FactoryMain_1342Gauntlet2: EnemyLoc(Maps.FranticFactory, Enemies.RoboKremling, 51, [], True),
    EnemyLocations.FactoryMain_3124Gauntlet0: EnemyLoc(Maps.FranticFactory, Enemies.MrDice1, 52, [], True),
    EnemyLocations.FactoryMain_3124Gauntlet1: EnemyLoc(Maps.FranticFactory, Enemies.SirDomino, 53, [], True),
    EnemyLocations.FactoryMain_3124Gauntlet2: EnemyLoc(Maps.FranticFactory, Enemies.MrDice1, 54, [], True),
    EnemyLocations.FactoryMain_4231Gauntlet0: EnemyLoc(Maps.FranticFactory, Enemies.RoboKremling, 55, [], True),
    EnemyLocations.FactoryMain_4231Gauntlet1: EnemyLoc(Maps.FranticFactory, Enemies.RoboKremling, 56, [], True),
    # Lobby
    EnemyLocations.FactoryLobby_Enemy0: EnemyLoc(Maps.FranticFactoryLobby, Enemies.ZingerRobo, 1, [], True),
    # Galleon
    # Main
    EnemyLocations.GalleonMain_ChestRoom0: EnemyLoc(Maps.GloomyGalleon, Enemies.Klobber, 12, [], True),
    EnemyLocations.GalleonMain_ChestRoom1: EnemyLoc(Maps.GloomyGalleon, Enemies.Kaboom, 18, [], True),
    EnemyLocations.GalleonMain_NearVineCannon: EnemyLoc(Maps.GloomyGalleon, Enemies.Kaboom, 16, [], True),
    EnemyLocations.GalleonMain_CrankyCannon: EnemyLoc(Maps.GloomyGalleon, Enemies.Kaboom, 17, [], True),
    EnemyLocations.GalleonMain_Submarine: EnemyLoc(Maps.GloomyGalleon, Enemies.Pufftup, 14, [], True),
    EnemyLocations.GalleonMain_5DS0: EnemyLoc(Maps.GloomyGalleon, Enemies.Shuri, 19, [], True),
    EnemyLocations.GalleonMain_5DS1: EnemyLoc(Maps.GloomyGalleon, Enemies.Shuri, 20, [], True),
    EnemyLocations.GalleonMain_PeanutTunnel: EnemyLoc(Maps.GloomyGalleon, Enemies.Kosha, 26, [], True),
    EnemyLocations.GalleonMain_CoconutTunnel: EnemyLoc(Maps.GloomyGalleon, Enemies.Kremling, 27, [], True),
    # Lighthouse
    EnemyLocations.GalleonLighthouse_Enemy0: EnemyLoc(Maps.GalleonLighthouse, Enemies.Klump, 1, [], True),
    EnemyLocations.GalleonLighthouse_Enemy1: EnemyLoc(Maps.GalleonLighthouse, Enemies.Klump, 2, [], True),
    # 5DS Diddy, Lanky, Chunky
    EnemyLocations.Galleon5DSDLC_Diddy: EnemyLoc(Maps.Galleon5DShipDiddyLankyChunky, Enemies.Pufftup, 4, [], True),
    EnemyLocations.Galleon5DSDLC_Chunky: EnemyLoc(Maps.Galleon5DShipDiddyLankyChunky, Enemies.Pufftup, 5, [], True),
    EnemyLocations.Galleon5DSDLC_Lanky: EnemyLoc(Maps.Galleon5DShipDiddyLankyChunky, Enemies.Pufftup, 6, [], True),
    # 5DS DK, Tiny
    EnemyLocations.Galleon5DSDT_DK0: EnemyLoc(Maps.Galleon5DShipDKTiny, Enemies.Shuri, 4, [], True),
    EnemyLocations.Galleon5DSDT_DK1: EnemyLoc(Maps.Galleon5DShipDKTiny, Enemies.Shuri, 5, [], True),
    EnemyLocations.Galleon5DSDT_DK2: EnemyLoc(Maps.Galleon5DShipDKTiny, Enemies.Shuri, 6, [], True),
    EnemyLocations.Galleon5DSDT_TinyCage: EnemyLoc(Maps.Galleon5DShipDKTiny, Enemies.Shuri, 9, [], True),
    EnemyLocations.Galleon5DSDT_TinyBed: EnemyLoc(Maps.Galleon5DShipDKTiny, Enemies.Shuri, 10, [], True),
    # 2DS
    EnemyLocations.Galleon2DS_Tiny0: EnemyLoc(Maps.Galleon2DShip, Enemies.Gimpfish, 3, [], True),
    EnemyLocations.Galleon2DS_Tiny1: EnemyLoc(Maps.Galleon2DShip, Enemies.Gimpfish, 4, [], True),
    # Submarine
    EnemyLocations.GalleonSub_Enemy0: EnemyLoc(Maps.GalleonSubmarine, Enemies.Pufftup, 1, [], True),
    EnemyLocations.GalleonSub_Enemy1: EnemyLoc(Maps.GalleonSubmarine, Enemies.Pufftup, 3, [], True),
    EnemyLocations.GalleonSub_Enemy2: EnemyLoc(Maps.GalleonSubmarine, Enemies.Pufftup, 4, [], True),
    EnemyLocations.GalleonSub_Enemy3: EnemyLoc(Maps.GalleonSubmarine, Enemies.Pufftup, 6, [], True),
    # Fungi
    # Main
    EnemyLocations.FungiMain_HollowTree0: EnemyLoc(Maps.FungiForest, Enemies.Klump, 5, [], True),
    EnemyLocations.FungiMain_HollowTree1: EnemyLoc(Maps.FungiForest, Enemies.Klump, 30, [], True),
    EnemyLocations.FungiMain_HollowTreeEntrance: EnemyLoc(Maps.FungiForest, Enemies.ZingerLime, 34, [], True),
    EnemyLocations.FungiMain_TreeMelonCrate0: EnemyLoc(Maps.FungiForest, Enemies.ZingerLime, 31, [], True),
    EnemyLocations.FungiMain_TreeMelonCrate1: EnemyLoc(Maps.FungiForest, Enemies.ZingerLime, 32, [], True),
    EnemyLocations.FungiMain_TreeMelonCrate2: EnemyLoc(Maps.FungiForest, Enemies.ZingerLime, 33, [], True),
    EnemyLocations.FungiMain_AppleGauntlet0: EnemyLoc(Maps.FungiForest, Enemies.EvilTomato, 9, [], False),
    EnemyLocations.FungiMain_AppleGauntlet1: EnemyLoc(Maps.FungiForest, Enemies.EvilTomato, 10, [], False),
    EnemyLocations.FungiMain_AppleGauntlet2: EnemyLoc(Maps.FungiForest, Enemies.EvilTomato, 11, [], False),
    EnemyLocations.FungiMain_AppleGauntlet3: EnemyLoc(Maps.FungiForest, Enemies.EvilTomato, 12, [], False),
    EnemyLocations.FungiMain_NearBeanstalk0: EnemyLoc(Maps.FungiForest, Enemies.Klump, 55, [], True),
    EnemyLocations.FungiMain_NearBeanstalk1: EnemyLoc(Maps.FungiForest, Enemies.Klump, 56, [], True),
    EnemyLocations.FungiMain_GreenTunnel: EnemyLoc(Maps.FungiForest, Enemies.ZingerLime, 57, [], True),
    EnemyLocations.FungiMain_NearLowWarp5: EnemyLoc(Maps.FungiForest, Enemies.MushroomMan, 23, [], True),
    EnemyLocations.FungiMain_NearPinkTunnelBounceTag: EnemyLoc(Maps.FungiForest, Enemies.MushroomMan, 24, [], True),
    EnemyLocations.FungiMain_NearGMRocketbarrel: EnemyLoc(Maps.FungiForest, Enemies.MushroomMan, 25, [], True),
    EnemyLocations.FungiMain_BetweenRBAndYellowTunnel: EnemyLoc(Maps.FungiForest, Enemies.ZingerLime, 26, [], True),
    EnemyLocations.FungiMain_NearCranky: EnemyLoc(Maps.FungiForest, Enemies.ZingerLime, 27, [], True),
    EnemyLocations.FungiMain_NearPinkTunnelGM: EnemyLoc(Maps.FungiForest, Enemies.ZingerLime, 28, [], True),
    EnemyLocations.FungiMain_GMRearTag: EnemyLoc(Maps.FungiForest, Enemies.ZingerLime, 29, [], True),
    EnemyLocations.FungiMain_NearFacePuzzle: EnemyLoc(Maps.FungiForest, Enemies.ZingerLime, 51, [], True),
    EnemyLocations.FungiMain_NearCrown: EnemyLoc(Maps.FungiForest, Enemies.ZingerLime, 52, [], True),
    EnemyLocations.FungiMain_NearHighWarp5: EnemyLoc(Maps.FungiForest, Enemies.ZingerLime, 53, [], True),
    EnemyLocations.FungiMain_TopOfMushroom: EnemyLoc(Maps.FungiForest, Enemies.Klump, 54, [], True),
    EnemyLocations.FungiMain_NearAppleDropoff: EnemyLoc(Maps.FungiForest, Enemies.ZingerLime, 48, [], True),
    EnemyLocations.FungiMain_NearDKPortal: EnemyLoc(Maps.FungiForest, Enemies.ZingerLime, 49, [], True),
    EnemyLocations.FungiMain_NearWellTag: EnemyLoc(Maps.FungiForest, Enemies.ZingerLime, 50, [], True),
    EnemyLocations.FungiMain_YellowTunnel0: EnemyLoc(Maps.FungiForest, Enemies.MushroomMan, 22, [], True),
    EnemyLocations.FungiMain_YellowTunnel1: EnemyLoc(Maps.FungiForest, Enemies.ZingerLime, 41, [], True),
    EnemyLocations.FungiMain_YellowTunnel2: EnemyLoc(Maps.FungiForest, Enemies.ZingerLime, 42, [], True),
    EnemyLocations.FungiMain_YellowTunnel3: EnemyLoc(Maps.FungiForest, Enemies.Klump, 43, [], True),
    EnemyLocations.FungiMain_NearSnide: EnemyLoc(Maps.FungiForest, Enemies.MushroomMan, 35, [], True),
    EnemyLocations.FungiMain_NearIsoCoin: EnemyLoc(Maps.FungiForest, Enemies.ZingerLime, 38, [], True),
    EnemyLocations.FungiMain_NearBBlast: EnemyLoc(Maps.FungiForest, Enemies.ZingerLime, 39, [], True),
    EnemyLocations.FungiMain_NearDarkAttic: EnemyLoc(Maps.FungiForest, Enemies.Klump, 44, [], True),
    EnemyLocations.FungiMain_NearWellExit: EnemyLoc(Maps.FungiForest, Enemies.ZingerLime, 47, [], True),
    EnemyLocations.FungiMain_NearBlueTunnel: EnemyLoc(Maps.FungiForest, Enemies.Klump, 59, [], True),
    EnemyLocations.FungiMain_Thornvine0: EnemyLoc(Maps.FungiForest, Enemies.Klump, 45, [], True),
    EnemyLocations.FungiMain_Thornvine1: EnemyLoc(Maps.FungiForest, Enemies.Klump, 46, [], True),
    EnemyLocations.FungiMain_Thornvine2: EnemyLoc(Maps.FungiForest, Enemies.ZingerLime, 60, [], True),
    EnemyLocations.FungiMain_ThornvineEntrance: EnemyLoc(Maps.FungiForest, Enemies.Klump, 58, [], True),
    # Anthill
    EnemyLocations.FungiAnthill_Gauntlet0: EnemyLoc(Maps.ForestAnthill, Enemies.KlaptrapPurple, 1, [], True),
    EnemyLocations.FungiAnthill_Gauntlet1: EnemyLoc(Maps.ForestAnthill, Enemies.KlaptrapPurple, 2, [], True),
    EnemyLocations.FungiAnthill_Gauntlet2: EnemyLoc(Maps.ForestAnthill, Enemies.KlaptrapPurple, 3, [], True),
    EnemyLocations.FungiAnthill_Gauntlet3: EnemyLoc(Maps.ForestAnthill, Enemies.KlaptrapPurple, 4, [], True),
    # Winch Room
    EnemyLocations.FungiWinch_Enemy: EnemyLoc(Maps.ForestWinchRoom, Enemies.Bat, 1, [], True),
    # Thornvine Barn
    EnemyLocations.FungiThornBarn_Enemy: EnemyLoc(Maps.ForestThornvineBarn, Enemies.Kosha, 1, [], True),
    # Mill Front
    EnemyLocations.FungiMillFront_Enemy: EnemyLoc(Maps.ForestMillFront, Enemies.ZingerLime, 1, [], True),
    # Mill Rear
    EnemyLocations.FungiMillRear_Enemy: EnemyLoc(Maps.ForestMillBack, Enemies.ZingerLime, 1, [], True),
    # Giant Mushroom
    EnemyLocations.FungiGM_AboveNightDoor: EnemyLoc(Maps.ForestGiantMushroom, Enemies.Klump, 2, [], True),
    EnemyLocations.FungiGM_Path0: EnemyLoc(Maps.ForestGiantMushroom, Enemies.ZingerLime, 3, [], False),
    EnemyLocations.FungiGM_Path1: EnemyLoc(Maps.ForestGiantMushroom, Enemies.ZingerLime, 4, [], False),
    # Lanky Attic
    EnemyLocations.FungiLankyAttic_Gauntlet0: EnemyLoc(Maps.ForestMillAttic, Enemies.Bat, 1, enemies_nokill_gun, True),
    EnemyLocations.FungiLankyAttic_Gauntlet1: EnemyLoc(Maps.ForestMillAttic, Enemies.Bat, 2, enemies_nokill_gun, True),
    EnemyLocations.FungiLankyAttic_Gauntlet2: EnemyLoc(Maps.ForestMillAttic, Enemies.Bat, 3, enemies_nokill_gun, True),
    # Mush Leap
    EnemyLocations.FungiLeap_Enemy0: EnemyLoc(Maps.ForestLankyZingersRoom, Enemies.ZingerLime, 1, [], True),
    EnemyLocations.FungiLeap_Enemy1: EnemyLoc(Maps.ForestLankyZingersRoom, Enemies.ZingerLime, 2, [], True),
    # Face Puzzle
    EnemyLocations.FungiFacePuzzle_Enemy: EnemyLoc(Maps.ForestChunkyFaceRoom, Enemies.ZingerLime, 1, [], True),
    # Spider Boss
    EnemyLocations.FungiSpider_Gauntlet0: EnemyLoc(Maps.ForestSpider, Enemies.SpiderSmall, 2, [Enemies.Klobber, Enemies.Kaboom, Enemies.MushroomMan], False, False),
    EnemyLocations.FungiSpider_Gauntlet1: EnemyLoc(Maps.ForestSpider, Enemies.SpiderSmall, 3, [Enemies.Klobber, Enemies.Kaboom, Enemies.MushroomMan], False, False),
    EnemyLocations.FungiSpider_Gauntlet2: EnemyLoc(Maps.ForestSpider, Enemies.SpiderSmall, 4, [Enemies.Klobber, Enemies.Kaboom, Enemies.MushroomMan], False, False),
    # Caves
    # Main
    EnemyLocations.CavesMain_Start: EnemyLoc(Maps.CrystalCaves, Enemies.Kremling, 10, [], True),
    EnemyLocations.CavesMain_NearIceCastle: EnemyLoc(Maps.CrystalCaves, Enemies.BeaverBlue, 15, [], True),
    EnemyLocations.CavesMain_Outside5DC: EnemyLoc(Maps.CrystalCaves, Enemies.ZingerLime, 17, [], True),
    EnemyLocations.CavesMain_1DCWaterfall: EnemyLoc(Maps.CrystalCaves, Enemies.ZingerLime, 18, [], True),
    EnemyLocations.CavesMain_NearFunky: EnemyLoc(Maps.CrystalCaves, Enemies.ZingerCharger, 19, [], True),
    EnemyLocations.CavesMain_NearSnide: EnemyLoc(Maps.CrystalCaves, Enemies.Kosha, 27, [], True),
    EnemyLocations.CavesMain_NearBonusRoom: EnemyLoc(Maps.CrystalCaves, Enemies.Kosha, 28, [], True),
    EnemyLocations.CavesMain_1DCHeadphones: EnemyLoc(Maps.CrystalCaves, Enemies.Kosha, 29, [], True),
    EnemyLocations.CavesMain_GiantKosha: EnemyLoc(Maps.CrystalCaves, Enemies.Kosha, 31, [], True),
    # DK 5DI
    EnemyLocations.Caves5DIDK_Right: EnemyLoc(Maps.CavesDonkeyIgloo, Enemies.Kosha, 1, [], True),
    EnemyLocations.Caves5DIDK_Left: EnemyLoc(Maps.CavesDonkeyIgloo, Enemies.Kosha, 3, [], True),
    # Lanky 5DI
    EnemyLocations.Caves5DILanky_First0: EnemyLoc(Maps.CavesLankyIgloo, Enemies.BeaverBlue, 1, [], True),
    EnemyLocations.Caves5DILanky_First1: EnemyLoc(Maps.CavesLankyIgloo, Enemies.BeaverBlue, 2, [], True),
    EnemyLocations.Caves5DILanky_Second0: EnemyLoc(Maps.CavesLankyIgloo, Enemies.Kremling, 3, [], True),
    EnemyLocations.Caves5DILanky_Second1: EnemyLoc(Maps.CavesLankyIgloo, Enemies.Kremling, 4, [], True),
    EnemyLocations.Caves5DILanky_Second2: EnemyLoc(Maps.CavesLankyIgloo, Enemies.Kremling, 5, [], True),
    # Tiny 5DI
    EnemyLocations.Caves5DITiny_BigEnemy: EnemyLoc(Maps.CavesTinyIgloo, Enemies.Kosha, 2, [Enemies.Guard], True),
    # Chunky 5DI
    EnemyLocations.Caves5DIChunky_Gauntlet00: EnemyLoc(Maps.CavesChunkyIgloo, Enemies.FireballGlasses, 2, [], False),
    EnemyLocations.Caves5DIChunky_Gauntlet01: EnemyLoc(Maps.CavesChunkyIgloo, Enemies.FireballGlasses, 3, [], False),
    EnemyLocations.Caves5DIChunky_Gauntlet02: EnemyLoc(Maps.CavesChunkyIgloo, Enemies.FireballGlasses, 4, [], False),
    EnemyLocations.Caves5DIChunky_Gauntlet03: EnemyLoc(Maps.CavesChunkyIgloo, Enemies.FireballGlasses, 5, [], False),
    EnemyLocations.Caves5DIChunky_Gauntlet04: EnemyLoc(Maps.CavesChunkyIgloo, Enemies.FireballGlasses, 6, [], False),
    # Lanky 1DC
    EnemyLocations.Caves1DC_Near: EnemyLoc(Maps.CavesLankyCabin, Enemies.Kosha, 2, [], True),
    EnemyLocations.Caves1DC_Far: EnemyLoc(Maps.CavesLankyCabin, Enemies.Kosha, 1, [], True),
    # DK 5DC
    EnemyLocations.Caves5DCDK_Gauntlet0: EnemyLoc(Maps.CavesDonkeyCabin, Enemies.ZingerLime, 1, enemies_nokill_gun, True),
    EnemyLocations.Caves5DCDK_Gauntlet1: EnemyLoc(Maps.CavesDonkeyCabin, Enemies.ZingerLime, 2, enemies_nokill_gun, True),
    EnemyLocations.Caves5DCDK_Gauntlet2: EnemyLoc(Maps.CavesDonkeyCabin, Enemies.ZingerLime, 3, enemies_nokill_gun, True),
    EnemyLocations.Caves5DCDK_Gauntlet3: EnemyLoc(Maps.CavesDonkeyCabin, Enemies.ZingerLime, 4, enemies_nokill_gun, True),
    EnemyLocations.Caves5DCDK_Gauntlet4: EnemyLoc(Maps.CavesDonkeyCabin, Enemies.ZingerLime, 5, enemies_nokill_gun, True),
    EnemyLocations.Caves5DCDK_Gauntlet5: EnemyLoc(Maps.CavesDonkeyCabin, Enemies.ZingerLime, 6, enemies_nokill_gun, True),
    # Diddy Enemies 5DC
    EnemyLocations.Caves5DCDiddyLow_CloseRight: EnemyLoc(Maps.CavesDiddyLowerCabin, Enemies.Klump, 1, [Enemies.Kosha, Enemies.Guard], True, False),
    EnemyLocations.Caves5DCDiddyLow_FarRight: EnemyLoc(Maps.CavesDiddyLowerCabin, Enemies.Kremling, 2, [Enemies.Kosha, Enemies.Guard], True, False),
    EnemyLocations.Caves5DCDiddyLow_CloseLeft: EnemyLoc(Maps.CavesDiddyLowerCabin, Enemies.Klump, 3, [Enemies.Kosha, Enemies.Guard], True, False),
    EnemyLocations.Caves5DCDiddyLow_FarLeft: EnemyLoc(Maps.CavesDiddyLowerCabin, Enemies.Kremling, 4, [Enemies.Kosha, Enemies.Guard], True, False),
    EnemyLocations.Caves5DCDiddyLow_Center0: EnemyLoc(Maps.CavesDiddyLowerCabin, Enemies.Klobber, 5, [Enemies.Kosha, Enemies.Guard], True, False),
    EnemyLocations.Caves5DCDiddyLow_Center1: EnemyLoc(Maps.CavesDiddyLowerCabin, Enemies.Klobber, 6, [Enemies.Kosha, Enemies.Guard], True, False),
    EnemyLocations.Caves5DCDiddyLow_Center2: EnemyLoc(Maps.CavesDiddyLowerCabin, Enemies.Klobber, 7, [Enemies.Kosha, Enemies.Guard], True, False),
    EnemyLocations.Caves5DCDiddyLow_Center3: EnemyLoc(Maps.CavesDiddyLowerCabin, Enemies.Klobber, 8, [Enemies.Kosha, Enemies.Guard], True, False),
    # Diddy Candle 5DC
    EnemyLocations.Caves5DCDiddyUpper_Enemy0: EnemyLoc(Maps.CavesDiddyUpperCabin, Enemies.Kosha, 1, [], True),
    EnemyLocations.Caves5DCDiddyUpper_Enemy1: EnemyLoc(Maps.CavesDiddyUpperCabin, Enemies.Kosha, 2, [], True),
    # Tiny 5DC
    EnemyLocations.Caves5DCTiny_Gauntlet0: EnemyLoc(Maps.CavesTinyCabin, Enemies.KlaptrapPurple, 1, [Enemies.Kosha, Enemies.Guard], True, False),
    EnemyLocations.Caves5DCTiny_Gauntlet1: EnemyLoc(Maps.CavesTinyCabin, Enemies.KlaptrapPurple, 2, [Enemies.Kosha, Enemies.Guard], True, False),
    EnemyLocations.Caves5DCTiny_Gauntlet2: EnemyLoc(Maps.CavesTinyCabin, Enemies.KlaptrapPurple, 3, [Enemies.Kosha, Enemies.Guard], True, False),
    EnemyLocations.Caves5DCTiny_Gauntlet3: EnemyLoc(Maps.CavesTinyCabin, Enemies.KlaptrapPurple, 4, [Enemies.Kosha, Enemies.Guard], True, False),
    EnemyLocations.Caves5DCTiny_Gauntlet4: EnemyLoc(Maps.CavesTinyCabin, Enemies.KlaptrapPurple, 5, [Enemies.Kosha, Enemies.Guard], True, False),
    # Castle
    # Main
    EnemyLocations.CastleMain_NearBridge0: EnemyLoc(Maps.CreepyCastle, Enemies.Krossbones, 4, [], True),
    EnemyLocations.CastleMain_NearBridge1: EnemyLoc(Maps.CreepyCastle, Enemies.Krossbones, 5, [], True),
    EnemyLocations.CastleMain_WoodenExtrusion0: EnemyLoc(Maps.CreepyCastle, Enemies.Kosha, 6, [], True),
    EnemyLocations.CastleMain_WoodenExtrusion1: EnemyLoc(Maps.CreepyCastle, Enemies.Kosha, 7, [], True),
    EnemyLocations.CastleMain_NearShed: EnemyLoc(Maps.CreepyCastle, Enemies.Krossbones, 8, [], True),
    EnemyLocations.CastleMain_NearLibrary: EnemyLoc(Maps.CreepyCastle, Enemies.Krossbones, 9, [], True),
    EnemyLocations.CastleMain_NearTower: EnemyLoc(Maps.CreepyCastle, Enemies.Kosha, 10, [], True),
    EnemyLocations.CastleMain_MuseumSteps: EnemyLoc(Maps.CreepyCastle, Enemies.Ghost, 11, [], True),
    EnemyLocations.CastleMain_NearLowCave: EnemyLoc(Maps.CreepyCastle, Enemies.Krossbones, 12, [], True),
    EnemyLocations.CastleMain_PathToLowKasplat: EnemyLoc(Maps.CreepyCastle, Enemies.Krossbones, 13, [], True),
    EnemyLocations.CastleMain_LowTnS: EnemyLoc(Maps.CreepyCastle, Enemies.Krossbones, 14, [], True),
    EnemyLocations.CastleMain_PathToDungeon: EnemyLoc(Maps.CreepyCastle, Enemies.Krossbones, 15, [], True),
    EnemyLocations.CastleMain_NearHeadphones: EnemyLoc(Maps.CreepyCastle, Enemies.Krossbones, 16, [], True),
    # Lobby
    EnemyLocations.CastleLobby_Left: EnemyLoc(Maps.CreepyCastleLobby, Enemies.Kosha, 2, [], True),
    EnemyLocations.CastleLobby_FarRight: EnemyLoc(Maps.CreepyCastleLobby, Enemies.Kosha, 3, [], True),
    EnemyLocations.CastleLobby_NearRight: EnemyLoc(Maps.CreepyCastleLobby, Enemies.Kosha, 4, [], True),
    # Ballroom
    EnemyLocations.CastleBallroom_Board00: EnemyLoc(Maps.CastleBallroom, Enemies.Krossbones, 1, [], True, False),
    EnemyLocations.CastleBallroom_Board01: EnemyLoc(Maps.CastleBallroom, Enemies.Ghost, 2, [], True, False),
    EnemyLocations.CastleBallroom_Board02: EnemyLoc(Maps.CastleBallroom, Enemies.Ghost, 3, [], True, False),
    EnemyLocations.CastleBallroom_Board03: EnemyLoc(Maps.CastleBallroom, Enemies.Ghost, 4, [], True, False),
    EnemyLocations.CastleBallroom_Board04: EnemyLoc(Maps.CastleBallroom, Enemies.Krossbones, 5, [], True, False),
    EnemyLocations.CastleBallroom_Start: EnemyLoc(Maps.CastleBallroom, Enemies.Kosha, 6, [], True),
    # Dungeon
    EnemyLocations.CastleDungeon_FaceRoom: EnemyLoc(Maps.CastleDungeon, Enemies.Krossbones, 1, [], True),
    EnemyLocations.CastleDungeon_ChairRoom: EnemyLoc(Maps.CastleDungeon, Enemies.Kosha, 2, [], True),
    EnemyLocations.CastleDungeon_OutsideLankyRoom: EnemyLoc(Maps.CastleDungeon, Enemies.Kosha, 3, [], True),
    # Shed
    EnemyLocations.CastleShed_Gauntlet00: EnemyLoc(Maps.CastleShed, Enemies.Bat, 1, enemies_nokill_gun, True),
    EnemyLocations.CastleShed_Gauntlet01: EnemyLoc(Maps.CastleShed, Enemies.Bat, 2, enemies_nokill_gun, True),
    EnemyLocations.CastleShed_Gauntlet02: EnemyLoc(Maps.CastleShed, Enemies.Bat, 3, enemies_nokill_gun, True),
    EnemyLocations.CastleShed_Gauntlet03: EnemyLoc(Maps.CastleShed, Enemies.Bat, 4, enemies_nokill_gun, True),
    EnemyLocations.CastleShed_Gauntlet04: EnemyLoc(Maps.CastleShed, Enemies.Bat, 5, enemies_nokill_gun, True),
    # Lower Cave
    EnemyLocations.CastleLowCave_NearCrypt: EnemyLoc(Maps.CastleLowerCave, Enemies.Kosha, 3, [], True),
    EnemyLocations.CastleLowCave_StairRight: EnemyLoc(Maps.CastleLowerCave, Enemies.Kosha, 4, [], True),
    EnemyLocations.CastleLowCave_StairLeft: EnemyLoc(Maps.CastleLowerCave, Enemies.Krossbones, 5, [], True),
    EnemyLocations.CastleLowCave_NearMausoleum: EnemyLoc(Maps.CastleLowerCave, Enemies.Bat, 6, [], True),
    EnemyLocations.CastleLowCave_NearFunky: EnemyLoc(Maps.CastleLowerCave, Enemies.Bat, 7, [], True),
    EnemyLocations.CastleLowCave_NearTag: EnemyLoc(Maps.CastleLowerCave, Enemies.Bat, 8, [], True),
    # Crypt
    EnemyLocations.CastleCrypt_DiddyCoffin0: EnemyLoc(Maps.CastleCrypt, Enemies.Ghost, 1, [], True),
    EnemyLocations.CastleCrypt_DiddyCoffin1: EnemyLoc(Maps.CastleCrypt, Enemies.Ghost, 2, [], True),
    EnemyLocations.CastleCrypt_DiddyCoffin2: EnemyLoc(Maps.CastleCrypt, Enemies.Krossbones, 3, [], True),
    EnemyLocations.CastleCrypt_DiddyCoffin3: EnemyLoc(Maps.CastleCrypt, Enemies.Ghost, 4, [], True),
    EnemyLocations.CastleCrypt_ChunkyCoffin0: EnemyLoc(Maps.CastleCrypt, Enemies.Krossbones, 5, [], True),
    EnemyLocations.CastleCrypt_ChunkyCoffin1: EnemyLoc(Maps.CastleCrypt, Enemies.Krossbones, 6, [], True),
    EnemyLocations.CastleCrypt_ChunkyCoffin2: EnemyLoc(Maps.CastleCrypt, Enemies.Ghost, 7, [], True),
    EnemyLocations.CastleCrypt_ChunkyCoffin3: EnemyLoc(Maps.CastleCrypt, Enemies.Krossbones, 8, [], True),
    EnemyLocations.CastleCrypt_MinecartEntry: EnemyLoc(Maps.CastleCrypt, Enemies.Krossbones, 9, [], True),
    EnemyLocations.CastleCrypt_Fork: EnemyLoc(Maps.CastleCrypt, Enemies.Krossbones, 10, [], True),
    EnemyLocations.CastleCrypt_NearDiddy: EnemyLoc(Maps.CastleCrypt, Enemies.Krossbones, 11, [], True),
    EnemyLocations.CastleCrypt_NearChunky: EnemyLoc(Maps.CastleCrypt, Enemies.Krossbones, 12, [], True),
    # Mausoleum
    EnemyLocations.CastleMausoleum_TinyPath: EnemyLoc(Maps.CastleMausoleum, Enemies.Krossbones, 1, [], True),
    EnemyLocations.CastleMausoleum_LankyPath0: EnemyLoc(Maps.CastleMausoleum, Enemies.Krossbones, 2, [], True),
    EnemyLocations.CastleMausoleum_LankyPath1: EnemyLoc(Maps.CastleMausoleum, Enemies.Krossbones, 3, [], True),
    # Upper Cave
    EnemyLocations.CastleUpperCave_NearDungeon: EnemyLoc(Maps.CastleUpperCave, Enemies.Bat, 3, [], True),
    EnemyLocations.CastleUpperCave_Pit: EnemyLoc(Maps.CastleUpperCave, Enemies.Bat, 4, [], True),
    EnemyLocations.CastleUpperCave_NearPit: EnemyLoc(Maps.CastleUpperCave, Enemies.Bat, 5, [], True),
    EnemyLocations.CastleUpperCave_NearEntrance: EnemyLoc(Maps.CastleUpperCave, Enemies.Krossbones, 6, [], True),
    # Kut Out
    EnemyLocations.CastleKKO_CenterEnemy: EnemyLoc(Maps.CastleBoss, Enemies.Ghost, 7, [], True, False),
    EnemyLocations.CastleKKO_WaterEnemy00: EnemyLoc(Maps.CastleBoss, Enemies.Pufftup, 8, [], True, False),
    EnemyLocations.CastleKKO_WaterEnemy01: EnemyLoc(Maps.CastleBoss, Enemies.Pufftup, 9, [], True, False),
    EnemyLocations.CastleKKO_WaterEnemy02: EnemyLoc(Maps.CastleBoss, Enemies.Pufftup, 10, [], True, False),
    EnemyLocations.CastleKKO_WaterEnemy03: EnemyLoc(Maps.CastleBoss, Enemies.Pufftup, 11, [], True, False),
    # Library
    EnemyLocations.CastleLibrary_Gauntlet00: EnemyLoc(Maps.CastleLibrary, Enemies.Krossbones, 1, [], True, False),
    EnemyLocations.CastleLibrary_Gauntlet01: EnemyLoc(Maps.CastleLibrary, Enemies.Ghost, 2, [], True, False),
    EnemyLocations.CastleLibrary_Gauntlet02: EnemyLoc(Maps.CastleLibrary, Enemies.Ghost, 3, [], True, False),
    EnemyLocations.CastleLibrary_Gauntlet03: EnemyLoc(Maps.CastleLibrary, Enemies.Krossbones, 4, [], True, False),
    EnemyLocations.CastleLibrary_Corridor00: EnemyLoc(Maps.CastleLibrary, Enemies.Book, 5, [], True),
    EnemyLocations.CastleLibrary_Corridor01: EnemyLoc(Maps.CastleLibrary, Enemies.Book, 7, [], True),
    EnemyLocations.CastleLibrary_Corridor02: EnemyLoc(Maps.CastleLibrary, Enemies.Book, 8, [], True),
    EnemyLocations.CastleLibrary_Corridor03: EnemyLoc(Maps.CastleLibrary, Enemies.Book, 9, [], True),
    EnemyLocations.CastleLibrary_Corridor04: EnemyLoc(Maps.CastleLibrary, Enemies.Book, 10, [], True),
    EnemyLocations.CastleLibrary_Corridor05: EnemyLoc(Maps.CastleLibrary, Enemies.Book, 11, [], True),
    EnemyLocations.CastleLibrary_ForkLeft0: EnemyLoc(Maps.CastleLibrary, Enemies.Bat, 12, [], True),
    EnemyLocations.CastleLibrary_ForkLeft1: EnemyLoc(Maps.CastleLibrary, Enemies.Bat, 15, [], True),
    EnemyLocations.CastleLibrary_ForkCenter: EnemyLoc(Maps.CastleLibrary, Enemies.Bat, 13, [], True),
    EnemyLocations.CastleLibrary_ForkRight: EnemyLoc(Maps.CastleLibrary, Enemies.Bat, 14, [], True),
    # Museum
    EnemyLocations.CastleMuseum_MainFloor0: EnemyLoc(Maps.CastleMuseum, Enemies.Ghost, 1, [], True),
    EnemyLocations.CastleMuseum_MainFloor1: EnemyLoc(Maps.CastleMuseum, Enemies.Ghost, 2, [], True),
    EnemyLocations.CastleMuseum_MainFloor2: EnemyLoc(Maps.CastleMuseum, Enemies.Ghost, 3, [], True),
    EnemyLocations.CastleMuseum_MainFloor3: EnemyLoc(Maps.CastleMuseum, Enemies.Ghost, 4, [], True),
    EnemyLocations.CastleMuseum_Start: EnemyLoc(Maps.CastleMuseum, Enemies.Kosha, 6, [], True),
    # Tower
    EnemyLocations.CastleTower_Gauntlet0: EnemyLoc(Maps.CastleTower, Enemies.Ghost, 1, [], True),
    EnemyLocations.CastleTower_Gauntlet1: EnemyLoc(Maps.CastleTower, Enemies.Ghost, 2, [], True),
    EnemyLocations.CastleTower_Gauntlet2: EnemyLoc(Maps.CastleTower, Enemies.Ghost, 3, [], True),
    EnemyLocations.CastleTower_Gauntlet3: EnemyLoc(Maps.CastleTower, Enemies.Ghost, 4, [], True),
    EnemyLocations.CastleTower_Gauntlet4: EnemyLoc(Maps.CastleTower, Enemies.Ghost, 5, [], True),
    # Trash Can
    EnemyLocations.CastleTrash_Gauntlet0: EnemyLoc(Maps.CastleTrashCan, Enemies.Bug, 1, [], True),
    EnemyLocations.CastleTrash_Gauntlet1: EnemyLoc(Maps.CastleTrashCan, Enemies.Bug, 2, [], True),
    EnemyLocations.CastleTrash_Gauntlet2: EnemyLoc(Maps.CastleTrashCan, Enemies.Bug, 3, [], True),
    EnemyLocations.CastleTrash_Gauntlet3: EnemyLoc(Maps.CastleTrashCan, Enemies.Bug, 4, [], True),
    EnemyLocations.CastleTrash_Gauntlet4: EnemyLoc(Maps.CastleTrashCan, Enemies.Bug, 5, [], True),
    # Tree
    EnemyLocations.CastleTree_StartRoom0: EnemyLoc(Maps.CastleTree, Enemies.Bat, 3, [], True),
    EnemyLocations.CastleTree_StartRoom1: EnemyLoc(Maps.CastleTree, Enemies.Bat, 5, [], True),
    # Helm
    # Main
    EnemyLocations.HelmMain_Start0: EnemyLoc(Maps.HideoutHelm, Enemies.KlaptrapGreen, 2, [], True),
    EnemyLocations.HelmMain_Start1: EnemyLoc(Maps.HideoutHelm, Enemies.Kremling, 3, [], True),
    EnemyLocations.HelmMain_Hill: EnemyLoc(Maps.HideoutHelm, Enemies.Klump, 4, [], True),
    EnemyLocations.HelmMain_SwitchRoom0: EnemyLoc(Maps.HideoutHelm, Enemies.Klump, 5, [], True),
    EnemyLocations.HelmMain_SwitchRoom1: EnemyLoc(Maps.HideoutHelm, Enemies.KlaptrapGreen, 16, [], True),
    EnemyLocations.HelmMain_MiniRoom0: EnemyLoc(Maps.HideoutHelm, Enemies.Kremling, 7, [], True),
    EnemyLocations.HelmMain_MiniRoom1: EnemyLoc(Maps.HideoutHelm, Enemies.Kremling, 8, [], True),
    EnemyLocations.HelmMain_MiniRoom2: EnemyLoc(Maps.HideoutHelm, Enemies.KlaptrapGreen, 17, [], True),
    EnemyLocations.HelmMain_MiniRoom3: EnemyLoc(Maps.HideoutHelm, Enemies.KlaptrapGreen, 18, [], True),
    EnemyLocations.HelmMain_DKRoom: EnemyLoc(Maps.HideoutHelm, Enemies.Kremling, 10, [], True),
    EnemyLocations.HelmMain_ChunkyRoom0: EnemyLoc(Maps.HideoutHelm, Enemies.Kremling, 11, [], True),
    EnemyLocations.HelmMain_ChunkyRoom1: EnemyLoc(Maps.HideoutHelm, Enemies.KlaptrapGreen, 19, [], True),
    EnemyLocations.HelmMain_TinyRoom: EnemyLoc(Maps.HideoutHelm, Enemies.Klump, 12, [], True),
    EnemyLocations.HelmMain_LankyRoom0: EnemyLoc(Maps.HideoutHelm, Enemies.Klump, 13, [], True),
    EnemyLocations.HelmMain_LankyRoom1: EnemyLoc(Maps.HideoutHelm, Enemies.KlaptrapGreen, 20, [], True),
    EnemyLocations.HelmMain_DiddyRoom0: EnemyLoc(Maps.HideoutHelm, Enemies.KlaptrapGreen, 21, [], True),
    EnemyLocations.HelmMain_DiddyRoom1: EnemyLoc(Maps.HideoutHelm, Enemies.KlaptrapGreen, 22, [], True),
    EnemyLocations.HelmMain_NavRight: EnemyLoc(Maps.HideoutHelm, Enemies.Kremling, 23, [], True),
    EnemyLocations.HelmMain_NavLeft: EnemyLoc(Maps.HideoutHelm, Enemies.KlaptrapGreen, 24, [], True),
    # Isles
    # Main
    EnemyLocations.IslesMain_PineappleCage0: EnemyLoc(Maps.Isles, Enemies.BeaverBlue, 1, [], True),
    EnemyLocations.IslesMain_FungiCannon0: EnemyLoc(Maps.Isles, Enemies.BeaverBlue, 2, [], True),
    EnemyLocations.IslesMain_JapesEntrance: EnemyLoc(Maps.Isles, Enemies.BeaverBlue, 3, [], True),
    EnemyLocations.IslesMain_MonkeyportPad: EnemyLoc(Maps.Isles, Enemies.Kremling, 4, [], True),
    EnemyLocations.IslesMain_UpperFactoryPath: EnemyLoc(Maps.Isles, Enemies.Kremling, 5, [], True),
    EnemyLocations.IslesMain_NearAztec: EnemyLoc(Maps.Isles, Enemies.ZingerCharger, 8, [], True),
    EnemyLocations.IslesMain_FungiCannon1: EnemyLoc(Maps.Isles, Enemies.ZingerCharger, 9, [], True),
    EnemyLocations.IslesMain_PineappleCage1: EnemyLoc(Maps.Isles, Enemies.ZingerCharger, 10, [], True),
    EnemyLocations.IslesMain_LowerFactoryPath0: EnemyLoc(Maps.Isles, Enemies.ZingerLime, 11, [], True),
    EnemyLocations.IslesMain_LowerFactoryPath1: EnemyLoc(Maps.Isles, Enemies.ZingerLime, 12, [], True),
}

EnemySelector = []
for enemyEnum, enemy in EnemyMetaData.items():
    if enemy.selector_enabled:
        EnemySelector.append({"name": enemy.name, "value": enemyEnum.name, "tooltip": ""})
EnemySelector = sorted(EnemySelector.copy(), key=lambda d: d["name"])
