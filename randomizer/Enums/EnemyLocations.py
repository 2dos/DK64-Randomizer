"""Enemy Locations enum."""
from enum import IntEnum, auto


class EnemyLocations(IntEnum):
    """Enemy Locations enum."""

    # Japes
    # Main
    JapesMain_Start = auto()  # Beaver, 2
    JapesMain_DiddyCavern = auto()  # Beaver, 4
    JapesMain_Tunnel0 = auto()  # Beaver, 5
    JapesMain_Tunnel1 = auto()  # Beaver, 6
    JapesMain_Storm0 = auto()  # Beaver, 15
    JapesMain_Storm1 = auto()  # Beaver, 18
    JapesMain_Storm2 = auto()  # Beaver, 20
    JapesMain_Hive0 = auto()  # Zinger (0x1C), 28
    JapesMain_Hive1 = auto()  # Zinger (0x1C), 29
    JapesMain_Hive2 = auto()  # Zinger (0x1C), 30
    JapesMain_Hive3 = auto()  # Kremling, 36
    JapesMain_Hive4 = auto()  # Kremling, 37
    JapesMain_KilledInDemo = auto()  # Beaver, 33
    JapesMain_NearUnderground = auto()  # Zinger (0x5), 49
    JapesMain_NearPainting0 = auto()  # Beaver, 34
    JapesMain_NearPainting1 = auto()  # Beaver, 35
    JapesMain_NearPainting2 = auto()  # Zinger (0x5), 48
    JapesMain_Mountain = auto()  # Zinger (0x5), 50
    JapesMain_FeatherTunnel = auto()  # Zinger (0x1C), 52
    JapesMain_MiddleTunnel = auto()  # Beaver, 54

    # Lobby
    JapesLobby_Enemy0 = auto()  # Beaver, 1
    JapesLobby_Enemy1 = auto()  # Beaver, 2

    # Painting
    JapesPainting_Gauntlet0 = auto()  # Zinger (0x5), 2
    JapesPainting_Gauntlet1 = auto()  # Zinger (0x5), 3
    JapesPainting_Gauntlet2 = auto()  # Zinger (0x5), 4
    JapesPainting_Gauntlet3 = auto()  # Zinger (0x5), 5
    JapesPainting_Gauntlet4 = auto()  # Zinger (0x5), 6

    # Mountain
    JapesMountain_Start0 = auto()  # Beaver, 1
    JapesMountain_Start1 = auto()  # Beaver, 2
    JapesMountain_Start2 = auto()  # Beaver, 6
    JapesMountain_Start3 = auto()  # Zinger (0x5), 8
    JapesMountain_Start4 = auto()  # Zinger (0x5), 9
    JapesMountain_NearGateSwitch0 = auto()  # Zinger (0x1C), 13
    JapesMountain_NearGateSwitch1 = auto()  # Zinger (0x1C), 14
    JapesMountain_HiLo = auto()  # Klump, 15
    JapesMountain_Conveyor0 = auto()  # Klump, 16
    JapesMountain_Conveyor1 = auto()  # Klump, 17

    # Shellhive
    JapesShellhive_FirstRoom = auto()  # P Klaptrap, 7
    JapesShellhive_SecondRoom0 = auto()  # P Klaptrap, 8
    JapesShellhive_SecondRoom1 = auto()  # P Klaptrap, 9
    JapesShellhive_ThirdRoom0 = auto()  # P Klaptrap, 10
    JapesShellhive_ThirdRoom1 = auto()  # P Klaptrap, 11
    JapesShellhive_ThirdRoom2 = auto()  # Zinger (0x5), 12
    JapesShellhive_ThirdRoom3 = auto()  # Zinger (0x5), 13
    JapesShellhive_MainRoom = auto()  # Zinger (0x5), 14

    # Angry Aztec
    # Main
    AztecMain_VaseRoom0 = auto()  # Zinger (0x1C), 2
    AztecMain_VaseRoom1 = auto()  # Zinger (0x1C), 4
    AztecMain_TunnelPad0 = auto()  # Zinger (0x1C), 10
    AztecMain_TunnelCage0 = auto()  # Klaptrap, 13
    AztecMain_TunnelCage1 = auto()  # Klaptrap, 14
    AztecMain_TunnelCage2 = auto()  # Klaptrap, 15
    AztecMain_StartingTunnel0 = auto()  # Kremling, 20
    AztecMain_StartingTunnel1 = auto()  # Kremling, 21
    AztecMain_OasisDoor = auto()  # Kremling, 23
    AztecMain_TunnelCage3 = auto()  # Kremling, 26
    AztecMain_OutsideLlama = auto()  # Kremling, 27
    AztecMain_OutsideTower = auto()  # Kremling, 28
    AztecMain_TunnelPad1 = auto()  # Zinger (0x1C), 31
    AztecMain_NearCandy = auto()  # Zinger (0x1C), 32
    AztecMain_AroundTotem = auto()  # Klaptrap, 33
    AztecMain_StartingTunnel2 = auto()  # Zinger (0x5), 38
    AztecMain_StartingTunnel3 = auto()  # Zinger (0x5), 39
    AztecMain_Outside5DT = auto()  # Zinger (0x1C), 41
    AztecMain_NearSnoopTunnel = auto()  # Kremling, 42

    # Lobby
    AztecLobby_Pad0 = auto()  # Zinger (0x5), 2
    AztecLobby_Pad1 = auto()  # Zinger (0x5), 3

    # DK 5DT
    AztecDK5DT_StartTrap0 = auto()  # Kaboom, 5
    AztecDK5DT_StartTrap1 = auto()  # Kaboom, 6
    AztecDK5DT_StartTrap2 = auto()  # Kaboom, 7
    AztecDK5DT_EndTrap0 = auto()  # Kaboom, 10
    AztecDK5DT_EndTrap1 = auto()  # Kaboom, 11
    AztecDK5DT_EndTrap2 = auto()  # Kaboom, 12
    AztecDK5DT_EndPath0 = auto()  # P Klaptrap, 13
    AztecDK5DT_EndPath1 = auto()  # P Klaptrap, 14
    AztecDK5DT_StartPath = auto()  # P Klaptrap, 15

    # Diddy 5DT
    AztecDiddy5DT_EndTrap0 = auto()  # Klobber, 4
    AztecDiddy5DT_EndTrap1 = auto()  # Klobber, 5
    AztecDiddy5DT_EndTrap2 = auto()  # Klobber, 6
    AztecDiddy5DT_StartLeft0 = auto()  # Kremling, 9
    AztecDiddy5DT_StartLeft1 = auto()  # Kremling, 10
    AztecDiddy5DT_Reward = auto()  # Klump, 11
    AztecDiddy5DT_SecondSwitch = auto()  # Kremling, 12

    # Lanky 5DT
    AztecLanky5DT_JoiningPaths = auto()  # Klump, 2
    AztecLanky5DT_EndTrap = auto()  # Klump, 3
    AztecLanky5DT_Reward = auto()  # Klump, 4

    # Tiny 5DT
    AztecTiny5DT_StartRightFront = auto()  # Zinger (0x1C), 2
    AztecTiny5DT_StartLeftBack = auto()  # Zinger (0x1C), 4
    AztecTiny5DT_StartRightBack = auto()  # Zinger (0x1C), 5
    AztecTiny5DT_StartLeftFront = auto()  # Zinger (0x1C), 6
    AztecTiny5DT_Reward0 = auto()  # Zinger (0x1C), 7
    AztecTiny5DT_Reward1 = auto()  # Zinger (0x1C), 8
    AztecTiny5DT_DeadEnd0 = auto()  # Zinger (0x1C), 9
    AztecTiny5DT_DeadEnd1 = auto()  # Zinger (0x1C), 10

    # Chunky 5DT
    AztecChunky5DT_StartRight = auto()  # Klobber, 2
    AztecChunky5DT_StartLeft = auto()  # Klobber, 3
    AztecChunky5DT_SecondRight = auto()  # Klobber, 5
    AztecChunky5DT_SecondLeft = auto()  # Klobber, 6
    AztecChunky5DT_Reward = auto()  # Zinger (0x1C), 7

    # Llama Temple
    AztecLlama_KongFreeInstrument = auto()  # P Klaptrap, 5
    AztecLlama_DinoInstrument = auto()  # P Klaptrap, 6
    AztecLlama_Matching0 = auto()  # Kremling, 10
    AztecLlama_Matching1 = auto()  # Kremling, 11
    AztecLlama_Right = auto()  # Kremling, 14
    AztecLlama_Left = auto()  # Kremling, 15
    AztecLlama_MelonCrate = auto()  # P Klaptrap, 16
    AztecLlama_SlamSwitch = auto()  # P Klaptrap, 17

    # Tiny Temple
    AztecTemple_Rotating00 = auto()  # Klaptrap, 1
    AztecTemple_Rotating01 = auto()  # Klaptrap, 2
    AztecTemple_Rotating02 = auto()  # Klaptrap, 3
    AztecTemple_Rotating03 = auto()  # Klaptrap, 4
    AztecTemple_Rotating04 = auto()  # Klaptrap, 5
    AztecTemple_Rotating05 = auto()  # Klaptrap, 6
    AztecTemple_Rotating06 = auto()  # Klaptrap, 7
    AztecTemple_Rotating07 = auto()  # Klaptrap, 8
    AztecTemple_Rotating08 = auto()  # Klaptrap, 9
    AztecTemple_Rotating09 = auto()  # Klaptrap, 10
    AztecTemple_Rotating10 = auto()  # Klaptrap, 11
    AztecTemple_Rotating11 = auto()  # Klaptrap, 12
    AztecTemple_Rotating12 = auto()  # Klaptrap, 13
    AztecTemple_Rotating13 = auto()  # Klaptrap, 14
    AztecTemple_Rotating14 = auto()  # Klaptrap, 15
    AztecTemple_Rotating15 = auto()  # Klaptrap, 16
    AztecTemple_MiniRoom00 = auto()  # Klaptrap, 20
    AztecTemple_MiniRoom01 = auto()  # Klaptrap, 21
    AztecTemple_MiniRoom02 = auto()  # Klaptrap, 22
    AztecTemple_MiniRoom03 = auto()  # Klaptrap, 23
    AztecTemple_GuardRotating0 = auto()  # Klobber, 24
    AztecTemple_GuardRotating1 = auto()  # Klobber, 36
    AztecTemple_MainRoom0 = auto()  # Kremling, 26
    AztecTemple_MainRoom1 = auto()  # Kremling, 28
    AztecTemple_MainRoom2 = auto()  # Klaptrap, 35
    AztecTemple_KongRoom0 = auto()  # Klaptrap, 29
    AztecTemple_KongRoom1 = auto()  # Klaptrap, 30
    AztecTemple_KongRoom2 = auto()  # Kremling, 32
    AztecTemple_KongRoom3 = auto()  # Kremling, 33
    AztecTemple_KongRoom4 = auto()  # Klaptrap, 34
    AztecTemple_Underwater = auto()  # Shuri, 37

    # Factory
    # Main
    FactoryMain_CandyCranky0 = auto()  # Kremling, 33
    FactoryMain_CandyCranky1 = auto()  # Kremling, 72
    FactoryMain_LobbyLeft = auto()  # Robo-Kremling, 74
    FactoryMain_LobbyRight = auto()  # Robo-Kremling, 58
    FactoryMain_StorageRoom = auto()  # Robo-Zinger, 91
    FactoryMain_BlockTower0 = auto()  # Mr Dice (0x59), 78
    FactoryMain_BlockTower1 = auto()  # Sir Domino, 79
    FactoryMain_BlockTower2 = auto()  # Mr Dice (0x59), 80
    FactoryMain_TunnelToHatch = auto()  # Robo-Kremling, 59
    FactoryMain_TunnelToProd0 = auto()  # Kremling, 63
    FactoryMain_TunnelToProd1 = auto()  # Robo-Kremling, 73
    FactoryMain_TunnelToBlockTower = auto()  # Robo-Kremling, 84
    FactoryMain_TunnelToRace0 = auto()  # Robo-Kremling, 87
    FactoryMain_TunnelToRace1 = auto()  # Robo-Zinger, 88
    FactoryMain_LowWarp4 = auto()  # Robo-Kremling, 66
    FactoryMain_DiddySwitch = auto()  # Robo-Zinger, 67
    FactoryMain_ToBlockTowerTunnel = auto()  # Robo-Zinger, 62
    FactoryMain_DarkRoom0 = auto()  # Robo-Zinger, 70
    FactoryMain_DarkRoom1 = auto()  # Robo-Zinger, 71
    FactoryMain_BHDM0 = auto()  # Mr Dice (0x57), 35
    FactoryMain_BHDM1 = auto()  # Sir Domino, 36
    FactoryMain_BHDM2 = auto()  # Sir Domino, 37
    FactoryMain_BHDM3 = auto()  # Mr Dice (0x57), 38
    FactoryMain_BHDM4 = auto()  # Mr Dice (0x57), 39
    FactoryMain_BHDM5 = auto()  # Ruler, 40
    FactoryMain_BHDM6 = auto()  # Ruler, 41
    FactoryMain_BHDM7 = auto()  # Mr Dice (0x59), 42
    FactoryMain_BHDM8 = auto()  # Sir Domino, 43
    FactoryMain_BHDM9 = auto()  # Sir Domino, 44
    FactoryMain_1342Gauntlet0 = auto()  # Robo-Zinger, 49
    FactoryMain_1342Gauntlet1 = auto()  # Robo-Kremling, 50
    FactoryMain_1342Gauntlet2 = auto()  # Robo-Kremling, 51
    FactoryMain_3124Gauntlet0 = auto()  # Mr Dice (0x59), 52
    FactoryMain_3124Gauntlet1 = auto()  # Sir Domino, 53
    FactoryMain_3124Gauntlet2 = auto()  # Mr Dice (0x59), 54
    FactoryMain_4231Gauntlet0 = auto()  # Robo-Kremling, 55
    FactoryMain_4231Gauntlet1 = auto()  # Robo-Kremling, 56

    # Lobby
    FactoryLobby_Enemy0 = auto()  # Robo-Zinger, 1

    # Galleon
    # Main
    GalleonMain_ChestRoom0 = auto()  # Klobber, 12
    GalleonMain_ChestRoom1 = auto()  # Kaboom, 18
    GalleonMain_NearVineCannon = auto()  # Kaboom, 16
    GalleonMain_CrankyCannon = auto()  # Kaboom, 17
    GalleonMain_Submarine = auto()  # Pufftup, 14
    GalleonMain_5DS0 = auto()  # Shuri, 19
    GalleonMain_5DS1 = auto()  # Shuri, 20
    GalleonMain_PeanutTunnel = auto()  # Kosha, 26
    GalleonMain_CoconutTunnel = auto()  # Kremling, 27

    # Lighthouse
    GalleonLighthouse_Enemy0 = auto()  # Klump, 1
    GalleonLighthouse_Enemy1 = auto()  # Klump, 2

    # 5DS Diddy, Lanky, Chunky
    Galleon5DSDLC_Diddy = auto()  # Pufftup, 4
    Galleon5DSDLC_Chunky = auto()  # Pufftup, 5
    Galleon5DSDLC_Lanky = auto()  # Pufftup, 6

    # 5DS DK, Tiny
    Galleon5DSDT_DK0 = auto()  # Shuri, 4
    Galleon5DSDT_DK1 = auto()  # Shuri, 5
    Galleon5DSDT_DK2 = auto()  # Shuri, 6
    Galleon5DSDT_TinyCage = auto()  # Shuri, 9
    Galleon5DSDT_TinyBed = auto()  # Shuri, 10

    # 2DS
    Galleon2DS_Tiny0 = auto()  # Gimpfish, 3
    Galleon2DS_Tiny1 = auto()  # Gimpfish, 4

    # Submarine
    GalleonSub_Enemy0 = auto()  # Pufftup, 1
    GalleonSub_Enemy1 = auto()  # Pufftup, 3
    GalleonSub_Enemy2 = auto()  # Pufftup, 4
    GalleonSub_Enemy3 = auto()  # Pufftup, 6

    # Fungi
    # Main
    FungiMain_HollowTree0 = auto()  # Klump, 5
    FungiMain_HollowTree1 = auto()  # Klump, 30
    FungiMain_HollowTreeEntrance = auto()  # Zinger (0x1C), 34
    FungiMain_TreeMelonCrate0 = auto()  # Zinger (0x1C), 31
    FungiMain_TreeMelonCrate1 = auto()  # Zinger (0x1C), 32
    FungiMain_TreeMelonCrate2 = auto()  # Zinger (0x1C), 33
    FungiMain_AppleGauntlet0 = auto()  # Tomato, 9
    FungiMain_AppleGauntlet1 = auto()  # Tomato, 10
    FungiMain_AppleGauntlet2 = auto()  # Tomato, 11
    FungiMain_AppleGauntlet3 = auto()  # Tomato, 12
    FungiMain_NearBeanstalk0 = auto()  # Klump, 55
    FungiMain_NearBeanstalk1 = auto()  # Klump, 56
    FungiMain_GreenTunnel = auto()  # Zinger (0x1C), 57
    FungiMain_NearLowWarp5 = auto()  # Mushroom, 23
    FungiMain_NearPinkTunnelBounceTag = auto()  # Mushroom, 24
    FungiMain_NearGMRocketbarrel = auto()  # Mushroom, 25
    FungiMain_BetweenRBAndYellowTunnel = auto()  # Zinger (0x1C), 26
    FungiMain_NearCranky = auto()  # Zinger (0x1C), 27
    FungiMain_NearPinkTunnelGM = auto()  # Zinger (0x1C), 28
    FungiMain_GMRearTag = auto()  # Zinger (0x1C), 29
    FungiMain_NearFacePuzzle = auto()  # Zinger (0x1C), 51
    FungiMain_NearCrown = auto()  # Zinger (0x1C), 52
    FungiMain_NearHighWarp5 = auto()  # Zinger (0x1C), 53
    FungiMain_TopOfMushroom = auto()  # Klump, 54
    FungiMain_NearAppleDropoff = auto()  # Zinger (0x1C), 48
    FungiMain_NearDKPortal = auto()  # Zinger (0x1C), 49
    FungiMain_NearWellTag = auto()  # Zinger (0x1C), 50
    FungiMain_YellowTunnel0 = auto()  # Mushroom, 22
    FungiMain_YellowTunnel1 = auto()  # Zinger (0x1C), 41
    FungiMain_YellowTunnel2 = auto()  # Zinger (0x1C), 42
    FungiMain_YellowTunnel3 = auto()  # Klump, 43
    FungiMain_NearSnide = auto()  # Mushroom, 35
    FungiMain_NearIsoCoin = auto()  # Zinger (0x1C), 38
    FungiMain_NearBBlast = auto()  # Zinger (0x1C), 39
    FungiMain_NearDarkAttic = auto()  # Klump, 44
    FungiMain_NearWellExit = auto()  # Zinger (0x1C), 47
    FungiMain_NearBlueTunnel = auto()  # Klump, 59
    FungiMain_Thornvine0 = auto()  # Klump, 45
    FungiMain_Thornvine1 = auto()  # Klump, 46
    FungiMain_Thornvine2 = auto()  # Zinger (0x1C), 60
    FungiMain_ThornvineEntrance = auto()  # Klump, 58

    # Anthill
    FungiAnthill_Gauntlet0 = auto()  # P Klaptrap, 1
    FungiAnthill_Gauntlet1 = auto()  # P Klaptrap, 2
    FungiAnthill_Gauntlet2 = auto()  # P Klaptrap, 3
    FungiAnthill_Gauntlet3 = auto()  # P Klaptrap, 4

    # Winch Room
    FungiWinch_Enemy = auto()  # Bat, 1

    # Thornvine Barn
    FungiThornBarn_Enemy = auto()  # Kosha, 1

    # Mill Front
    FungiMillFront_Enemy = auto()  # Zinger (0x1C), 1

    # Mill Rear
    FungiMillRear_Enemy = auto()  # Zinger (0x1C), 1

    # Giant Mushroom
    FungiGM_AboveNightDoor = auto()  # Klump, 2
    FungiGM_Path0 = auto()  # Zinger (0x1C), 3
    FungiGM_Path1 = auto()  # Zinger (0x1C), 4

    # Lanky Attic
    FungiLankyAttic_Gauntlet0 = auto()  # Bat, 1
    FungiLankyAttic_Gauntlet1 = auto()  # Bat, 2
    FungiLankyAttic_Gauntlet2 = auto()  # Bat, 3

    # Mush Leap
    FungiLeap_Enemy0 = auto()  # Zinger (0x1C), 1
    FungiLeap_Enemy1 = auto()  # Zinger (0x1C), 2

    # Face Puzzle
    FungiFacePuzzle_Enemy = auto()  # Zinger (0x1C), 1

    # Spider Boss
    FungiSpider_Gauntlet0 = auto()  # Small Spider, 2
    FungiSpider_Gauntlet1 = auto()  # Small Spider, 3
    FungiSpider_Gauntlet2 = auto()  # Small Spider, 4

    # Caves
    # Main
    CavesMain_Start = auto()  # Kremling, 10
    CavesMain_NearIceCastle = auto()  # Beaver, 15
    CavesMain_Outside5DC = auto()  # Zinger (0x1C), 17
    CavesMain_1DCWaterfall = auto()  # Zinger (0x1C), 18
    CavesMain_NearFunky = auto()  # Zinger (0x5), 19
    CavesMain_NearSnide = auto()  # Kosha, 27
    CavesMain_NearBonusRoom = auto()  # Kosha, 28
    CavesMain_1DCHeadphones = auto()  # Kosha, 29
    CavesMain_GiantKosha = auto()  # Kosha, 31

    # DK 5DI
    Caves5DIDK_Right = auto()  # Kosha, 1
    Caves5DIDK_Left = auto()  # Kosha, 3

    # Lanky 5DI
    Caves5DILanky_First0 = auto()  # Beaver, 1
    Caves5DILanky_First1 = auto()  # Beaver, 2
    Caves5DILanky_Second0 = auto()  # Kremling, 3
    Caves5DILanky_Second1 = auto()  # Kremling, 4
    Caves5DILanky_Second2 = auto()  # Kremling, 5

    # Tiny 5DI
    Caves5DITiny_BigEnemy = auto()  # Kosha, 2

    # Chunky 5DI
    Caves5DIChunky_Gauntlet00 = auto()  # Fireball, 2
    Caves5DIChunky_Gauntlet01 = auto()  # Fireball, 3
    Caves5DIChunky_Gauntlet02 = auto()  # Fireball, 4
    Caves5DIChunky_Gauntlet03 = auto()  # Fireball, 5
    Caves5DIChunky_Gauntlet04 = auto()  # Fireball, 6

    # Lanky 1DC
    Caves1DC_Near = auto()  # Kosha, 2
    Caves1DC_Far = auto()  # Kosha, 1

    # DK 5DC
    Caves5DCDK_Gauntlet0 = auto()  # Zinger (0x1C), 1
    Caves5DCDK_Gauntlet1 = auto()  # Zinger (0x1C), 2
    Caves5DCDK_Gauntlet2 = auto()  # Zinger (0x1C), 3
    Caves5DCDK_Gauntlet3 = auto()  # Zinger (0x1C), 4
    Caves5DCDK_Gauntlet4 = auto()  # Zinger (0x1C), 5
    Caves5DCDK_Gauntlet5 = auto()  # Zinger (0x1C), 6

    # Diddy Enemies 5DC
    Caves5DCDiddyLow_CloseRight = auto()  # Klump, 1
    Caves5DCDiddyLow_FarRight = auto()  # Kremling, 2
    Caves5DCDiddyLow_CloseLeft = auto()  # Klump, 3
    Caves5DCDiddyLow_FarLeft = auto()  # Kremling, 4
    Caves5DCDiddyLow_Center0 = auto()  # Klobber, 5
    Caves5DCDiddyLow_Center1 = auto()  # Klobber, 6
    Caves5DCDiddyLow_Center2 = auto()  # Klobber, 7
    Caves5DCDiddyLow_Center3 = auto()  # Klobber, 8

    # Diddy Candle 5DC
    Caves5DCDiddyUpper_Enemy0 = auto()  # Kosha, 1
    Caves5DCDiddyUpper_Enemy1 = auto()  # Kosha, 2

    # Tiny 5DC
    Caves5DCTiny_Gauntlet0 = auto()  # P Klaptrap, 1
    Caves5DCTiny_Gauntlet1 = auto()  # P Klaptrap, 2
    Caves5DCTiny_Gauntlet2 = auto()  # P Klaptrap, 3
    Caves5DCTiny_Gauntlet3 = auto()  # P Klaptrap, 4
    Caves5DCTiny_Gauntlet4 = auto()  # P Klaptrap, 5

    # Castle
    # Main
    CastleMain_NearBridge0 = auto()  # Krossbones, 4
    CastleMain_NearBridge1 = auto()  # Krossbones, 5
    CastleMain_WoodenExtrusion0 = auto()  # Kosha, 6
    CastleMain_WoodenExtrusion1 = auto()  # Kosha, 7
    CastleMain_NearShed = auto()  # Krossbones, 8
    CastleMain_NearLibrary = auto()  # Krossbones, 9
    CastleMain_NearTower = auto()  # Kosha, 10
    CastleMain_MuseumSteps = auto()  # Ghost, 11
    CastleMain_NearLowCave = auto()  # Krossbones, 12
    CastleMain_PathToLowKasplat = auto()  # Krossbones, 13
    CastleMain_LowTnS = auto()  # Krossbones, 14
    CastleMain_PathToDungeon = auto()  # Krossbones, 15
    CastleMain_NearHeadphones = auto()  # Krossbones, 16

    # Lobby
    CastleLobby_Left = auto()  # Kosha, 2
    CastleLobby_FarRight = auto()  # Kosha, 3
    CastleLobby_NearRight = auto()  # Kosha, 4

    # Ballroom
    CastleBallroom_Board00 = auto()  # Krossbones, 1
    CastleBallroom_Board01 = auto()  # Ghost, 2
    CastleBallroom_Board02 = auto()  # Ghost, 3
    CastleBallroom_Board03 = auto()  # Ghost, 4
    CastleBallroom_Board04 = auto()  # Krossbones, 5
    CastleBallroom_Start = auto()  # Kosha, 6

    # Dungeon
    CastleDungeon_FaceRoom = auto()  # Krossbones, 1
    CastleDungeon_ChairRoom = auto()  # Kosha, 2
    CastleDungeon_OutsideLankyRoom = auto()  # Kosha, 3

    # Shed
    CastleShed_Gauntlet00 = auto()  # Bat, 1
    CastleShed_Gauntlet01 = auto()  # Bat, 2
    CastleShed_Gauntlet02 = auto()  # Bat, 3
    CastleShed_Gauntlet03 = auto()  # Bat, 4
    CastleShed_Gauntlet04 = auto()  # Bat, 5

    # Lower Cave
    CastleLowCave_NearCrypt = auto()  # Kosha, 3
    CastleLowCave_StairRight = auto()  # Kosha, 4
    CastleLowCave_StairLeft = auto()  # Krossbones, 5
    CastleLowCave_NearMausoleum = auto()  # Bat, 6
    CastleLowCave_NearFunky = auto()  # Bat, 7
    CastleLowCave_NearTag = auto()  # Bat, 8

    # Crypt
    CastleCrypt_DiddyCoffin0 = auto()  # Ghost, 1
    CastleCrypt_DiddyCoffin1 = auto()  # Ghost, 2
    CastleCrypt_DiddyCoffin2 = auto()  # Krossbones, 3
    CastleCrypt_DiddyCoffin3 = auto()  # Ghost, 4
    CastleCrypt_ChunkyCoffin0 = auto()  # Krossbones, 5
    CastleCrypt_ChunkyCoffin1 = auto()  # Krossbones, 6
    CastleCrypt_ChunkyCoffin2 = auto()  # Ghost, 7
    CastleCrypt_ChunkyCoffin3 = auto()  # Krossbones, 8
    CastleCrypt_MinecartEntry = auto()  # Krossbones, 9
    CastleCrypt_Fork = auto()  # Krossbones, 10
    CastleCrypt_NearDiddy = auto()  # Krossbones, 11
    CastleCrypt_NearChunky = auto()  # Krossbones, 12

    # Mausoleum
    CastleMausoleum_TinyPath = auto()  # Krossbones, 1
    CastleMausoleum_LankyPath0 = auto()  # Krossbones, 2
    CastleMausoleum_LankyPath1 = auto()  # Krossbones, 3

    # Upper Cave
    CastleUpperCave_NearDungeon = auto()  # Bat, 3
    CastleUpperCave_Pit = auto()  # Bat, 4
    CastleUpperCave_NearPit = auto()  # Bat, 5
    CastleUpperCave_NearEntrance = auto()  # Krossbones, 6

    # Kut Out
    CastleKKO_CenterEnemy = auto()  # Ghost, 7
    CastleKKO_WaterEnemy00 = auto()  # Pufftup, 8
    CastleKKO_WaterEnemy01 = auto()  # Pufftup, 9
    CastleKKO_WaterEnemy02 = auto()  # Pufftup, 10
    CastleKKO_WaterEnemy03 = auto()  # Pufftup, 11

    # Library
    CastleLibrary_Gauntlet00 = auto()  # Krossbones, 1
    CastleLibrary_Gauntlet01 = auto()  # Ghost, 2
    CastleLibrary_Gauntlet02 = auto()  # Ghost, 3
    CastleLibrary_Gauntlet03 = auto()  # Krossbones, 4
    CastleLibrary_Corridor00 = auto()  # Book, 5
    CastleLibrary_Corridor01 = auto()  # Book, 7
    CastleLibrary_Corridor02 = auto()  # Book, 8
    CastleLibrary_Corridor03 = auto()  # Book, 9
    CastleLibrary_Corridor04 = auto()  # Book, 10
    CastleLibrary_Corridor05 = auto()  # Book, 11
    CastleLibrary_ForkLeft0 = auto()  # Bat, 12
    CastleLibrary_ForkLeft1 = auto()  # Bat, 15
    CastleLibrary_ForkCenter = auto()  # Bat, 13
    CastleLibrary_ForkRight = auto()  # Bat, 14

    # Museum
    CastleMuseum_MainFloor0 = auto()  # Ghost, 1
    CastleMuseum_MainFloor1 = auto()  # Ghost, 2
    CastleMuseum_MainFloor2 = auto()  # Ghost, 3
    CastleMuseum_MainFloor3 = auto()  # Ghost, 4
    CastleMuseum_Start = auto()  # Kosha, 6

    # Tower
    CastleTower_Gauntlet0 = auto()  # Ghost, 1
    CastleTower_Gauntlet1 = auto()  # Ghost, 2
    CastleTower_Gauntlet2 = auto()  # Ghost, 3
    CastleTower_Gauntlet3 = auto()  # Ghost, 4
    CastleTower_Gauntlet4 = auto()  # Ghost, 5

    # Trash Can
    CastleTrash_Gauntlet0 = auto()  # Bug, 1
    CastleTrash_Gauntlet1 = auto()  # Bug, 2
    CastleTrash_Gauntlet2 = auto()  # Bug, 3
    CastleTrash_Gauntlet3 = auto()  # Bug, 4
    CastleTrash_Gauntlet4 = auto()  # Bug, 5

    # Tree
    CastleTree_StartRoom0 = auto()  # Bat, 3
    CastleTree_StartRoom1 = auto()  # Bat, 5

    # Helm
    # Main
    HelmMain_Start0 = auto()  # Klaptrap, 2
    HelmMain_Start1 = auto()  # Kremling, 3
    HelmMain_Hill = auto()  # Klump, 4
    HelmMain_SwitchRoom0 = auto()  # Klump, 5
    HelmMain_SwitchRoom1 = auto()  # Klaptrap, 16
    HelmMain_MiniRoom0 = auto()  # Kremling, 7
    HelmMain_MiniRoom1 = auto()  # Kremling, 8
    HelmMain_MiniRoom2 = auto()  # Klaptrap, 17
    HelmMain_MiniRoom3 = auto()  # Klaptrap, 18
    HelmMain_DKRoom = auto()  # Kremling, 10
    HelmMain_ChunkyRoom0 = auto()  # Kremling, 11
    HelmMain_ChunkyRoom1 = auto()  # Klaptrap, 19
    HelmMain_TinyRoom = auto()  # Klump, 12
    HelmMain_LankyRoom0 = auto()  # Klump, 13
    HelmMain_LankyRoom1 = auto()  # Klaptrap, 20
    HelmMain_DiddyRoom0 = auto()  # Klaptrap, 21
    HelmMain_DiddyRoom1 = auto()  # Klaptrap, 22
    HelmMain_NavRight = auto()  # Kremling, 23
    HelmMain_NavLeft = auto()  # Klaptrap, 24

    # Isles
    # Main
    IslesMain_PineappleCage0 = auto()  # Beaver, 1
    IslesMain_FungiCannon0 = auto()  # Beaver, 2
    IslesMain_JapesEntrance = auto()  # Beaver, 3
    IslesMain_MonkeyportPad = auto()  # Kremling, 4
    IslesMain_UpperFactoryPath = auto()  # Kremling, 5
    IslesMain_NearAztec = auto()  # Zinger (0x5), 8
    IslesMain_FungiCannon1 = auto()  # Zinger (0x5), 9
    IslesMain_PineappleCage1 = auto()  # Zinger (0x5), 10
    IslesMain_LowerFactoryPath0 = auto()  # Zinger (0x1C), 11
    IslesMain_LowerFactoryPath1 = auto()  # Zinger (0x1C), 12
