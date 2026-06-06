const requirement_data = {
    "Japes": {
        "DK": [
            new Requirement(10, [[Moves.Moveless]]), // 1 bunch in JungleJapesMain; 1 bunch in JungleJapesStart
            new Requirement(15, [[Moves.ClimbingCheck]]), // 1 bunch in JapesCannonPlatform; 1 bunch in JapesHill; 1 bunch in JapesHillTop
            new Requirement(10, [[Moves.Coconut]]), // 1 balloon in JungleJapesStart
            new Requirement(9, [[Moves.JapesCoconut]]), // 9 bananas in JapesBeyondCoconutGate2
            new Requirement(10, [[Moves.Vines, Moves.ClimbingCheck]]), // 1 bunch in JapesTnSAlcove; 5 bananas in JungleJapesStart
            new Requirement(6, [ // 6 bananas in JapesHillTop
                [Moves.ClimbingCheck],
                [Moves.AllWarps],
            ]),
            new Requirement(20, [[Moves.Coconut, Moves.JapesCoconut]]), // 1 balloon, 1 bunch, 1 bunch in JapesBeyondCoconutGate2
            new Requirement(10, [[Moves.Vines, Moves.ClimbingCheck, Moves.Blast]]), // 2 bunches in JapesBaboonBlast
            new Requirement(10, [ // 1 balloon in JapesHillTop
                [Moves.ClimbingCheck, Moves.Coconut],
                [Moves.Coconut, Moves.AllWarps],
            ]),
        ],
        "Diddy": [
            new Requirement(5, [[Moves.Moveless]]), // 5 bananas in JungleJapesStart
            new Requirement(10, [[Moves.Diving]]), // 2 bunches in JungleJapesStart
            new Requirement(20, [[Moves.ClimbingCheck]]), // 2 bunches in JungleJapesMain; 2 bunches in JungleJapesStart
            new Requirement(10, [[Moves.Peanut]]), // 1 balloon in JapesBeyondPeanutGate
            new Requirement(3, [[Moves.JapesCoconut]]), // 3 bananas in JapesBeyondCoconutGate2
            new Requirement(7, [ // 7 bananas in JapesHillTop
                [Moves.ClimbingCheck],
                [Moves.AllWarps],
            ]),
            new Requirement(5, [[Moves.Coconut, Moves.JapesCoconut]]), // 1 bunch in JapesBeyondCoconutGate2
            new Requirement(20, [ // 1 balloon in JapesTopOfMountain; 1 bunch, 5 bananas in Mine
                [Moves.ClimbingCheck, Moves.Peanut],
                [Moves.Peanut, Moves.AllWarps],
            ]),
            new Requirement(15, [ // 1 balloon, 1 bunch in Mine
                [Moves.ClimbingCheck, Moves.LevelSlam, Moves.Peanut],
                [Moves.LevelSlam, Moves.Peanut, Moves.AllWarps],
            ]),
            new Requirement(5, [ // 1 bunch in Mine
                [Moves.ClimbingCheck, Moves.LevelSlam, Moves.Peanut, Moves.Charge],
                [Moves.LevelSlam, Moves.Peanut, Moves.Charge, Moves.AllWarps],
            ]),
        ],
        "Lanky": [
            new Requirement(1, [[Moves.Moveless]]), // 1 banana in JungleJapesStart
            new Requirement(5, [[Moves.Diving]]), // 5 bananas in JungleJapesStart
            new Requirement(5, [[Moves.ClimbingCheck]]), // 1 bunch in JapesHillTop
            new Requirement(2, [[Moves.Orangstand]]), // 2 bananas in JapesPaintingRoomHill
            new Requirement(3, [[Moves.JapesCoconut]]), // 1 banana, 2 bananas in JapesBeyondCoconutGate2
            new Requirement(5, [ // 1 bunch in JapesHillTop
                [Moves.ClimbingCheck],
                [Moves.AllWarps],
            ]),
            new Requirement(5, [[Moves.ClimbingCheck, Moves.JapesCoconut]]), // 1 bunch in JapesBeyondCoconutGate2
            new Requirement(10, [[Moves.Coconut, Moves.JapesCoconut]]), // 5 bananas in BeyondRambiGate; 1 bunch in JapesBeyondCoconutGate2
            new Requirement(5, [[Moves.Peanut, Moves.Grape]]), // 1 bunch in JapesBeyondPeanutGate
            new Requirement(20, [[Moves.Peanut, Moves.Orangstand]]), // 2 bunches, 2 bunches in JapesLankyCave
            new Requirement(20, [[Moves.Grape, Moves.JapesCoconut]]), // 1 balloon, 1 balloon in JapesBeyondCoconutGate2
            new Requirement(9, [[Moves.Orangstand, Moves.JapesCoconut]]), // 2 bananas in JapesBeyondCoconutGate2; 1 bunch, 2 bananas in JapesUselessSlope
            new Requirement(10, [[Moves.Peanut, Moves.Grape, Moves.Orangstand]]), // 1 balloon in JapesLankyCave
        ],
        "Tiny": [
            new Requirement(5, [[Moves.Moveless]]), // 5 bananas in JungleJapesStart
            new Requirement(2, [[Moves.JapesCoconut]]), // 2 bananas in JapesBeyondCoconutGate2
            new Requirement(5, [[Moves.ClimbingCheck, Moves.JapesCoconut]]), // 1 bunch in JapesBeyondCoconutGate2
            new Requirement(10, [[Moves.Coconut, Moves.JapesCoconut]]), // 5 bananas in BeyondRambiGate; 1 bunch in JapesBeyondCoconutGate2
            new Requirement(5, [[Moves.Peanut, Moves.Feather]]), // 1 bunch in JapesBeyondPeanutGate
            new Requirement(10, [[Moves.Feather, Moves.JapesCoconut]]), // 1 balloon in JapesBeyondCoconutGate2
            new Requirement(10, [[Moves.Coconut, Moves.Feather, Moves.JapesCoconut]]), // 1 balloon in BeyondRambiGate
            new Requirement(5, [ // 1 bunch in JapesBeyondFeatherGate
                [Moves.Peanut, Moves.AllWarps],
                [Moves.JapesCoconut, Moves.JapesShellhive],
            ]),
            new Requirement(30, [ // 3 bunches, 3 bunches in JapesBeyondFeatherGate
                [Moves.Peanut, Moves.Mini, Moves.AllWarps],
                [Moves.Mini, Moves.JapesCoconut, Moves.JapesShellhive],
            ]),
            new Requirement(10, [ // 1 balloon in TinyHive
                [Moves.Peanut, Moves.Feather, Moves.Mini, Moves.AllWarps],
                [Moves.Feather, Moves.Mini, Moves.JapesCoconut, Moves.JapesShellhive],
            ]),
            new Requirement(8, [ // 8 bananas in TinyHive
                [Moves.Oranges, Moves.LevelSlam, Moves.Peanut, Moves.Mini, Moves.AllWarps],
                [Moves.Oranges, Moves.LevelSlam, Moves.Mini, Moves.JapesCoconut, Moves.JapesShellhive],
                [Moves.LevelSlam, Moves.Peanut, Moves.Sax, Moves.Mini, Moves.AllWarps],
                [Moves.LevelSlam, Moves.Sax, Moves.Mini, Moves.JapesCoconut, Moves.JapesShellhive],
            ]),
        ],
        "Chunky": [
            new Requirement(5, [[Moves.Moveless]]), // 5 bananas in JungleJapesStart
            new Requirement(15, [[Moves.Barrels, Moves.Slam]]), // 2 bunches, 5 bananas in JapesCatacomb
            new Requirement(10, [ // 2 bunches in JapesHillTop
                [Moves.ClimbingCheck],
                [Moves.AllWarps],
            ]),
            new Requirement(5, [[Moves.ClimbingCheck, Moves.JapesCoconut]]), // 1 bunch in JapesBeyondCoconutGate2
            new Requirement(5, [[Moves.Barrels, Moves.Coconut, Moves.JapesCoconut]]), // 1 bunch in BeyondRambiGate
            new Requirement(30, [[Moves.Coconut, Moves.Pineapple, Moves.JapesCoconut]]), // 3 balloons in BeyondRambiGate
            new Requirement(10, [ // 10 bananas in JapesBeyondCoconutGate1
                [Moves.JapesCoconut],
                [Moves.Peanut, Moves.AllWarps],
            ]),
            new Requirement(20, [ // 4 bunches in JapesBeyondFeatherGate
                [Moves.ClimbingCheck, Moves.Peanut, Moves.Hunky, Moves.AllWarps],
                [Moves.ClimbingCheck, Moves.Hunky, Moves.JapesCoconut, Moves.JapesShellhive],
            ]),
        ],
    },
    "Aztec": {
        "DK": [
            new Requirement(3, [[Moves.Moveless]]), // 3 bananas in AngryAztecOasis
            new Requirement(15, [[Moves.ClimbingCheck]]), // 3 bunches in AngryAztecOasis
            new Requirement(10, [[Moves.Coconut, Moves.Strong]]), // 2 bunches in AngryAztecOasis
            new Requirement(7, [ // 3 bananas, 4 bananas in AngryAztecMain
                [Moves.AllWarps],
                [Moves.AztecTunnelDoor],
            ]),
            new Requirement(30, [ // 1 balloon, 2 balloons in AngryAztecMain
                [Moves.Coconut, Moves.AllWarps],
                [Moves.Coconut, Moves.AztecTunnelDoor],
            ]),
            new Requirement(20, [ // 4 bunches in AztecDonkeyQuicksandCave
                [Moves.Strong, Moves.AllWarps],
                [Moves.LevelSlam, Moves.Coconut, Moves.Strong, Moves.AztecTunnelDoor, Moves.AztecLlama],
                [Moves.LevelSlam, Moves.Strong, Moves.Grape, Moves.AztecTunnelDoor, Moves.AztecLlama],
                [Moves.LevelSlam, Moves.Strong, Moves.Feather, Moves.AztecTunnelDoor, Moves.AztecLlama],
            ]),
            new Requirement(15, [ // 15 bananas in LlamaTemple
                [Moves.Coconut, Moves.AllWarps, Moves.AztecLlama],
                [Moves.Coconut, Moves.AztecTunnelDoor, Moves.AztecLlama],
                [Moves.Grape, Moves.AllWarps, Moves.AztecLlama],
                [Moves.Grape, Moves.AztecTunnelDoor, Moves.AztecLlama],
                [Moves.Feather, Moves.AllWarps, Moves.AztecLlama],
                [Moves.Feather, Moves.AztecTunnelDoor, Moves.AztecLlama],
            ]),
        ],
        "Diddy": [
            new Requirement(5, [[Moves.Moveless]]), // 1 bunch in AngryAztecOasis
            new Requirement(10, [[Moves.Peanut]]), // 1 balloon in AngryAztecOasis
            new Requirement(18, [[Moves.LevelSlam, Moves.Peanut]]), // 3 bananas, 3 bunches in TempleStart
            new Requirement(15, [ // 3 bananas, 3 bananas, 4 bananas, 5 bananas in AngryAztecMain
                [Moves.AllWarps],
                [Moves.AztecTunnelDoor],
            ]),
            new Requirement(7, [[Moves.Diving, Moves.Peanut, Moves.TinyTempleIce]]), // 7 bananas in TempleUnderwater
            new Requirement(10, [ // 1 bunch, 1 bunch in AngryAztecMain
                [Moves.Rocket, Moves.AllWarps],
                [Moves.Rocket, Moves.AztecTunnelDoor],
            ]),
            new Requirement(10, [ // 1 balloon in DiddyTemple
                [Moves.Peanut, Moves.AllWarps, Moves.Aztec5DT],
                [Moves.Peanut, Moves.AztecTunnelDoor, Moves.Aztec5DT],
            ]),
            new Requirement(15, [ // 3 bunches in AngryAztecMain
                [Moves.ClimbingCheck, Moves.AllWarps],
                [Moves.ClimbingCheck, Moves.AztecTunnelDoor],
                [Moves.Rocket, Moves.AllWarps],
                [Moves.Rocket, Moves.AztecTunnelDoor],
            ]),
            new Requirement(10, [ // 1 balloon in AztecDonkeyQuicksandCave
                [Moves.Peanut, Moves.AllWarps],
                [Moves.LevelSlam, Moves.Coconut, Moves.Strong, Moves.Peanut, Moves.AztecTunnelDoor, Moves.AztecLlama, Moves.AztecW5Bonus],
                [Moves.LevelSlam, Moves.Strong, Moves.Peanut, Moves.Grape, Moves.AztecTunnelDoor, Moves.AztecLlama, Moves.AztecW5Bonus],
                [Moves.LevelSlam, Moves.Strong, Moves.Peanut, Moves.Feather, Moves.AztecTunnelDoor, Moves.AztecLlama, Moves.AztecW5Bonus],
            ]),
        ],
        "Lanky": [
            new Requirement(5, [[Moves.Moveless]]), // 5 bananas in AngryAztecOasis
            new Requirement(10, [ // 1 bunch, 5 bananas in AngryAztecMain
                [Moves.AllWarps],
                [Moves.AztecTunnelDoor],
            ]),
            new Requirement(14, [[Moves.Diving, Moves.Grape, Moves.TinyTempleIce]]), // 1 bunch, 9 bananas in TempleVultureRoom
            new Requirement(25, [ // 5 bunches in AngryAztecMain
                [Moves.ClimbingCheck, Moves.AllWarps],
                [Moves.ClimbingCheck, Moves.AztecTunnelDoor],
            ]),
            new Requirement(10, [ // 1 balloon in LankyTemple
                [Moves.Grape, Moves.AllWarps, Moves.Aztec5DT],
                [Moves.Grape, Moves.AztecTunnelDoor, Moves.Aztec5DT],
            ]),
            new Requirement(5, [ // 1 bunch in LlamaTempleMatching
                [Moves.Vines, Moves.Grape, Moves.AllWarps, Moves.AztecLlama],
                [Moves.Vines, Moves.Grape, Moves.AztecTunnelDoor, Moves.AztecLlama],
            ]),
            new Requirement(20, [ // 2 balloons in LlamaTemple
                [Moves.Diving, Moves.Grape, Moves.AllWarps, Moves.AztecLlama],
                [Moves.Diving, Moves.Grape, Moves.AztecTunnelDoor, Moves.AztecLlama],
            ]),
            new Requirement(11, [ // 1 bunch, 6 bananas in LlamaTemple
                [Moves.Coconut, Moves.AllWarps, Moves.AztecLlama],
                [Moves.Coconut, Moves.AztecTunnelDoor, Moves.AztecLlama],
                [Moves.Grape, Moves.AllWarps, Moves.AztecLlama],
                [Moves.Grape, Moves.AztecTunnelDoor, Moves.AztecLlama],
                [Moves.Feather, Moves.AllWarps, Moves.AztecLlama],
                [Moves.Feather, Moves.AztecTunnelDoor, Moves.AztecLlama],
            ]),
        ],
        "Tiny": [
            new Requirement(25, [ // 1 bunch, 1 bunch, 10 bananas, 5 bananas in AngryAztecMain
                [Moves.AllWarps],
                [Moves.AztecTunnelDoor],
            ]),
            new Requirement(20, [[Moves.Diving, Moves.Feather, Moves.TinyTempleIce]]), // 2 balloons in TempleKONGRoom
            new Requirement(5, [[Moves.Diving, Moves.Feather, Moves.Mini, Moves.TinyTempleIce]]), // 5 bananas in TempleUnderwater
            new Requirement(10, [ // 1 balloon in LlamaTemple
                [Moves.Feather, Moves.AllWarps, Moves.AztecLlama],
                [Moves.Feather, Moves.AztecTunnelDoor, Moves.AztecLlama],
            ]),
            new Requirement(25, [ // 5 bunches in AngryAztecMain
                [Moves.ClimbingCheck, Moves.AllWarps],
                [Moves.ClimbingCheck, Moves.AztecTunnelDoor],
                [Moves.Twirl, Moves.AllWarps],
                [Moves.Twirl, Moves.AztecTunnelDoor],
            ]),
            new Requirement(3, [ // 3 bananas in LlamaTemple
                [Moves.Coconut, Moves.AllWarps, Moves.AztecLlama],
                [Moves.Coconut, Moves.AztecTunnelDoor, Moves.AztecLlama],
                [Moves.Grape, Moves.AllWarps, Moves.AztecLlama],
                [Moves.Grape, Moves.AztecTunnelDoor, Moves.AztecLlama],
                [Moves.Feather, Moves.AllWarps, Moves.AztecLlama],
                [Moves.Feather, Moves.AztecTunnelDoor, Moves.AztecLlama],
            ]),
            new Requirement(2, [ // 2 bananas in LlamaTempleBack
                [Moves.Coconut, Moves.AllWarps, Moves.AztecLlama],
                [Moves.Grape, Moves.AllWarps, Moves.AztecLlama],
                [Moves.Feather, Moves.AllWarps, Moves.AztecLlama],
                [Moves.Coconut, Moves.Mini, Moves.AztecTunnelDoor, Moves.AztecLlama],
                [Moves.Grape, Moves.Mini, Moves.AztecTunnelDoor, Moves.AztecLlama],
                [Moves.Feather, Moves.Mini, Moves.AztecTunnelDoor, Moves.AztecLlama],
            ]),
            new Requirement(10, [ // 2 bunches in LlamaTempleBack
                [Moves.LevelSlam, Moves.Coconut, Moves.AllWarps, Moves.AztecLlama],
                [Moves.LevelSlam, Moves.Grape, Moves.AllWarps, Moves.AztecLlama],
                [Moves.LevelSlam, Moves.Feather, Moves.AllWarps, Moves.AztecLlama],
                [Moves.LevelSlam, Moves.Coconut, Moves.Mini, Moves.AztecTunnelDoor, Moves.AztecLlama],
                [Moves.LevelSlam, Moves.Grape, Moves.Mini, Moves.AztecTunnelDoor, Moves.AztecLlama],
                [Moves.LevelSlam, Moves.Feather, Moves.Mini, Moves.AztecTunnelDoor, Moves.AztecLlama],
            ]),
        ],
        "Chunky": [
            new Requirement(29, [[Moves.Pineapple]]), // 4 bananas, 5 bunches in TempleStart
            new Requirement(16, [ // 10 bananas, 6 bananas in AngryAztecMain
                [Moves.AllWarps],
                [Moves.AztecTunnelDoor],
            ]),
            new Requirement(5, [ // 5 bananas in BetweenVinesByPortal
                [Moves.Vines],
                [Moves.Twirl],
                [Moves.AllWarps],
            ]),
            new Requirement(10, [[Moves.Diving, Moves.Pineapple, Moves.TinyTempleIce]]), // 1 balloon in TempleVultureRoom
            new Requirement(20, [ // 4 bunches in BetweenVinesByPortal
                [Moves.Vines, Moves.Pineapple],
                [Moves.Twirl, Moves.Pineapple],
                [Moves.Pineapple, Moves.AllWarps],
            ]),
            new Requirement(20, [ // 2 balloons in ChunkyTemple
                [Moves.Pineapple, Moves.AllWarps, Moves.Aztec5DT],
                [Moves.Pineapple, Moves.AztecTunnelDoor, Moves.Aztec5DT],
            ]),
        ],
    },
    "Factory": {
        "DK": [
            new Requirement(15, [[Moves.Moveless]]), // 4 bananas, 6 bananas in BeyondHatch; 5 bananas in FranticFactoryStart
            new Requirement(10, [[Moves.Coconut]]), // 1 balloon in BeyondHatch
            new Requirement(20, [[Moves.Blast]]), // 4 bunches in FactoryBaboonBlast
            new Requirement(15, [[Moves.Strong, Moves.FactoryProduction]]), // 3 bunches in InsideCore
            new Requirement(5, [ // 5 bananas in Testing
                [Moves.AllWarps],
                [Moves.ClimbingCheck, Moves.FactoryTesting],
            ]),
            new Requirement(10, [ // 1 balloon in Testing
                [Moves.Coconut, Moves.AllWarps],
                [Moves.ClimbingCheck, Moves.Coconut, Moves.FactoryTesting],
            ]),
            new Requirement(10, [ // 1 balloon in RandDUpper
                [Moves.ClimbingCheck, Moves.Coconut, Moves.AllWarps],
                [Moves.ClimbingCheck, Moves.Coconut, Moves.FactoryTesting],
            ]),
            new Requirement(15, [ // 3 bunches in PowerHut
                [Moves.ClimbingCheck, Moves.Coconut, Moves.AllWarps],
                [Moves.ClimbingCheck, Moves.Coconut, Moves.FactoryTesting],
                [Moves.Coconut, Moves.IsDiddy, Moves.AllWarps],
                [Moves.Coconut, Moves.IsTiny, Moves.AllWarps],
            ]),
        ],
        "Diddy": [
            new Requirement(12, [[Moves.Moveless]]), // 12 bananas in BeyondHatch
            new Requirement(10, [ // 1 bunch, 5 bananas in FactoryArcadeTunnel
                [Moves.ClimbingCheck],
                [Moves.AllWarps],
            ]),
            new Requirement(8, [ // 1 bunch, 3 bananas in Testing
                [Moves.AllWarps],
                [Moves.ClimbingCheck, Moves.FactoryTesting],
            ]),
            new Requirement(15, [ // 3 bunches in UpperCore
                [Moves.ClimbingCheck, Moves.FactoryProduction],
                [Moves.AllWarps, Moves.FactoryProduction],
            ]),
            new Requirement(25, [ // 5 bunches in Testing
                [Moves.Spring, Moves.AllWarps],
                [Moves.ClimbingCheck, Moves.Spring, Moves.FactoryTesting],
            ]),
            new Requirement(30, [ // 3 balloons in RandDUpper
                [Moves.Peanut, Moves.Guitar, Moves.AllWarps],
                [Moves.ClimbingCheck, Moves.Peanut, Moves.Guitar, Moves.FactoryTesting],
            ]),
        ],
        "Lanky": [
            new Requirement(11, [[Moves.Moveless]]), // 1 banana, 5 bananas in BeyondHatch; 1 bunch in FranticFactoryStart
            new Requirement(4, [[Moves.Orangstand]]), // 4 bananas in FactoryStoragePipe
            new Requirement(10, [[Moves.Grape, Moves.FactoryProduction]]), // 1 balloon in InsideCore
            new Requirement(10, [ // 1 bunch, 5 bananas in RandD
                [Moves.AllWarps],
                [Moves.ClimbingCheck, Moves.FactoryTesting],
            ]),
            new Requirement(15, [ // 3 bunches in SpinningCore
                [Moves.AllWarps],
                [Moves.ClimbingCheck, Moves.FactoryProduction],
            ]),
            new Requirement(5, [ // 5 bananas in RandDUpper
                [Moves.ClimbingCheck, Moves.AllWarps],
                [Moves.ClimbingCheck, Moves.FactoryTesting],
            ]),
            new Requirement(5, [ // 1 bunch in UpperCore
                [Moves.ClimbingCheck, Moves.FactoryProduction],
                [Moves.AllWarps, Moves.FactoryProduction],
            ]),
            new Requirement(10, [ // 1 balloon in UpperCore
                [Moves.ClimbingCheck, Moves.Grape, Moves.FactoryProduction],
                [Moves.Grape, Moves.AllWarps, Moves.FactoryProduction],
            ]),
            new Requirement(20, [ // 4 bunches in UpperCore
                [Moves.ClimbingCheck, Moves.Orangstand, Moves.FactoryProduction],
                [Moves.Orangstand, Moves.AllWarps, Moves.FactoryProduction],
            ]),
            new Requirement(10, [ // 1 balloon in RandD
                [Moves.Grape, Moves.Trombone, Moves.AllWarps],
                [Moves.ClimbingCheck, Moves.Grape, Moves.Trombone, Moves.FactoryTesting],
            ]),
        ],
        "Tiny": [
            new Requirement(13, [[Moves.Moveless]]), // 2 bunches in AlcoveBeyondHatch; 3 bananas in FranticFactoryStart
            new Requirement(5, [ // 1 bunch in FactoryArcadeTunnel
                [Moves.ClimbingCheck],
                [Moves.AllWarps],
            ]),
            new Requirement(22, [ // 10 bananas in RandD; 1 bunch, 7 bananas in Testing
                [Moves.AllWarps],
                [Moves.ClimbingCheck, Moves.FactoryTesting],
            ]),
            new Requirement(20, [ // 4 bunches in UpperCore
                [Moves.ClimbingCheck, Moves.FactoryProduction],
                [Moves.AllWarps, Moves.FactoryProduction],
            ]),
            new Requirement(10, [ // 1 balloon in MiddleCore
                [Moves.Feather, Moves.AllWarps],
                [Moves.Feather, Moves.FactoryProduction],
            ]),
            new Requirement(20, [ // 1 balloon, 1 balloon in Testing
                [Moves.Feather, Moves.AllWarps],
                [Moves.ClimbingCheck, Moves.Feather, Moves.FactoryTesting],
            ]),
            new Requirement(5, [ // 1 bunch in Testing
                [Moves.Mini, Moves.AllWarps],
                [Moves.ClimbingCheck, Moves.Mini, Moves.FactoryTesting],
            ]),
            new Requirement(5, [ // 1 bunch in UpperCore
                [Moves.ClimbingCheck, Moves.Twirl, Moves.FactoryProduction],
                [Moves.Twirl, Moves.AllWarps, Moves.FactoryProduction],
            ]),
        ],
        "Chunky": [
            new Requirement(20, [[Moves.Moveless]]), // 1 bunch in BeyondHatch; 1 bunch, 10 bananas in FranticFactoryStart
            new Requirement(10, [[Moves.Pineapple]]), // 1 balloon in FranticFactoryStart
            new Requirement(15, [[Moves.Punch]]), // 3 bunches in BeyondHatch
            new Requirement(5, [ // 1 bunch in Testing
                [Moves.AllWarps],
                [Moves.ClimbingCheck, Moves.FactoryTesting],
            ]),
            new Requirement(20, [ // 4 bunches in SpinningCore
                [Moves.AllWarps],
                [Moves.ClimbingCheck, Moves.FactoryProduction],
            ]),
            new Requirement(10, [ // 1 balloon in Testing
                [Moves.Pineapple, Moves.AllWarps],
                [Moves.ClimbingCheck, Moves.Pineapple, Moves.FactoryTesting],
            ]),
            new Requirement(10, [ // 10 bananas in RandDUpper
                [Moves.ClimbingCheck, Moves.Triangle, Moves.Punch, Moves.AllWarps],
                [Moves.ClimbingCheck, Moves.Triangle, Moves.Punch, Moves.FactoryTesting],
            ]),
            new Requirement(10, [ // 1 balloon in RandDUpper
                [Moves.ClimbingCheck, Moves.Pineapple, Moves.Triangle, Moves.Punch, Moves.AllWarps],
                [Moves.ClimbingCheck, Moves.Pineapple, Moves.Triangle, Moves.Punch, Moves.FactoryTesting],
            ]),
        ],
    },
    "Galleon": {
        "DK": [
            new Requirement(10, [[Moves.Coconut]]), // 1 balloon in GloomyGalleonStart
            new Requirement(15, [ // 3 bunches in ShipyardUnderwater
                [Moves.Diving, Moves.AllWarps],
                [Moves.Diving, Moves.GalleonPeanut],
            ]),
            new Requirement(10, [ // 1 balloon in LighthousePlatform
                [Moves.Coconut, Moves.AllWarps],
                [Moves.Coconut, Moves.RaisedWater, Moves.GalleonLighthouse],
            ]),
            new Requirement(15, [ // 3 bunches in GalleonBaboonBlast
                [Moves.Blast, Moves.AllWarps],
                [Moves.Blast, Moves.RaisedWater, Moves.GalleonLighthouse],
            ]),
            new Requirement(10, [ // 10 bananas in BongosShip
                [Moves.Diving, Moves.Bongos, Moves.AllWarps],
                [Moves.Diving, Moves.Bongos, Moves.GalleonPeanut],
            ]),
            new Requirement(10, [ // 10 bananas in LighthouseEnguardeDoor
                [Moves.Diving, Moves.AllWarps, Moves.Enguarde],
                [Moves.Diving, Moves.GalleonLighthouse, Moves.Enguarde],
            ]),
            new Requirement(20, [ // 4 bunches in LighthouseAboveLadder
                [Moves.ClimbingCheck, Moves.LevelSlam, Moves.AllWarps],
                [Moves.ClimbingCheck, Moves.LevelSlam, Moves.RaisedWater, Moves.GalleonLighthouse],
            ]),
            new Requirement(10, [ // 1 balloon in Lighthouse
                [Moves.ClimbingCheck, Moves.LevelSlam, Moves.Coconut, Moves.AllWarps],
                [Moves.ClimbingCheck, Moves.LevelSlam, Moves.Coconut, Moves.RaisedWater, Moves.GalleonLighthouse],
            ]),
        ],
        "Diddy": [
            new Requirement(10, [[Moves.Moveless]]), // 2 bunches in GloomyGalleonStart
            new Requirement(36, [ // 10 bananas, 4 bunches, 6 bananas in ShipyardUnderwater
                [Moves.Diving, Moves.AllWarps],
                [Moves.Diving, Moves.GalleonPeanut],
            ]),
            new Requirement(10, [ // 1 balloon in Shipyard
                [Moves.Peanut, Moves.AllWarps],
                [Moves.Peanut, Moves.GalleonPeanut],
            ]),
            new Requirement(10, [ // 1 balloon in LighthousePlatform
                [Moves.Peanut, Moves.AllWarps],
                [Moves.Peanut, Moves.RaisedWater, Moves.GalleonLighthouse],
            ]),
            new Requirement(10, [ // 2 bunches in LighthousePlatform
                [Moves.Rocket, Moves.AllWarps],
                [Moves.Rocket, Moves.RaisedWater, Moves.GalleonLighthouse],
            ]),
            new Requirement(10, [ // 1 balloon in TreasureRoom
                [Moves.Peanut, Moves.AllWarps],
                [Moves.Diving, Moves.Peanut, Moves.GalleonPeanut, Moves.GalleonTreasure],
            ]),
            new Requirement(14, [ // 2 bunches, 4 bananas in GuitarShip
                [Moves.Diving, Moves.Guitar, Moves.AllWarps, Moves.LoweredWater],
                [Moves.Diving, Moves.Guitar, Moves.LoweredWater, Moves.GalleonPeanut],
            ]),
        ],
        "Lanky": [
            new Requirement(5, [[Moves.Moveless]]), // 5 bananas in GloomyGalleonStart
            new Requirement(20, [[Moves.Grape, Moves.Punch]]), // 2 balloons in GloomyGalleonStart
            new Requirement(25, [ // 4 bunches, 5 bananas in LighthouseUnderwater
                [Moves.Diving, Moves.AllWarps],
                [Moves.Diving, Moves.GalleonLighthouse],
            ]),
            new Requirement(5, [ // 1 bunch in ShipyardUnderwater
                [Moves.Diving, Moves.AllWarps],
                [Moves.Diving, Moves.GalleonPeanut],
            ]),
            new Requirement(10, [ // 1 balloon in Shipyard
                [Moves.Grape, Moves.AllWarps],
                [Moves.Grape, Moves.GalleonPeanut],
            ]),
            new Requirement(10, [ // 1 bunch, 5 bananas in LankyShip
                [Moves.Diving, Moves.LevelSlam, Moves.AllWarps],
                [Moves.Diving, Moves.LevelSlam, Moves.GalleonPeanut],
            ]),
            new Requirement(1, [ // 1 banana in TreasureRoom
                [Moves.AllWarps, Moves.RaisedWater],
                [Moves.Diving, Moves.RaisedWater, Moves.GalleonPeanut, Moves.GalleonTreasure],
            ]),
            new Requirement(15, [ // 3 bunches in TromboneShip
                [Moves.Diving, Moves.Trombone, Moves.AllWarps, Moves.LoweredWater],
                [Moves.Diving, Moves.Trombone, Moves.LoweredWater, Moves.GalleonPeanut],
            ]),
            new Requirement(5, [ // 1 bunch in Shipyard
                [Moves.Diving, Moves.AllWarps],
                [Moves.Diving, Moves.GalleonPeanut],
                [Moves.AllWarps, Moves.LoweredWater],
                [Moves.LoweredWater, Moves.GalleonPeanut],
            ]),
            new Requirement(4, [ // 4 bananas in TreasureRoom
                [Moves.Balloon, Moves.AllWarps, Moves.RaisedWater],
                [Moves.Diving, Moves.Balloon, Moves.RaisedWater, Moves.GalleonPeanut, Moves.GalleonTreasure],
            ]),
        ],
        "Tiny": [
            new Requirement(9, [[Moves.Moveless]]), // 4 bananas, 5 bananas in GloomyGalleonStart
            new Requirement(15, [[Moves.Pineapple, Moves.RaisedWater]]), // 3 bunches in GalleonBeyondPineappleGate
            new Requirement(8, [ // 1 bunch, 3 bananas in GalleonPastVines
                [Moves.Vines],
                [Moves.AllWarps, Moves.RaisedWater],
            ]),
            new Requirement(5, [ // 1 bunch in TreasureRoom
                [Moves.Diving, Moves.AllWarps],
                [Moves.Diving, Moves.GalleonPeanut, Moves.GalleonTreasure],
            ]),
            new Requirement(5, [ // 1 bunch in LighthouseSnideAlcove
                [Moves.Vines, Moves.AllWarps],
                [Moves.AllWarps, Moves.RaisedWater],
                [Moves.RaisedWater, Moves.GalleonLighthouse],
            ]),
            new Requirement(10, [ // 2 bunches in TinyShip
                [Moves.Diving, Moves.LevelSlam, Moves.AllWarps],
                [Moves.Diving, Moves.LevelSlam, Moves.GalleonPeanut],
            ]),
            new Requirement(18, [ // 2 bunches, 8 bananas in SaxophoneShip
                [Moves.Diving, Moves.Sax, Moves.AllWarps],
                [Moves.Diving, Moves.Sax, Moves.GalleonPeanut],
            ]),
            new Requirement(10, [ // 1 balloon in TreasureRoom
                [Moves.Feather, Moves.AllWarps],
                [Moves.Diving, Moves.Feather, Moves.GalleonPeanut, Moves.GalleonTreasure],
            ]),
            new Requirement(10, [ // 1 balloon in LighthouseSurface
                [Moves.Feather, Moves.AllWarps, Moves.LoweredWater],
                [Moves.Feather, Moves.LoweredWater, Moves.GalleonLighthouse],
            ]),
            new Requirement(10, [ // 1 balloon in LighthouseSnideAlcove
                [Moves.Vines, Moves.Feather, Moves.AllWarps],
                [Moves.Feather, Moves.AllWarps, Moves.RaisedWater],
                [Moves.Feather, Moves.RaisedWater, Moves.GalleonLighthouse],
            ]),
        ],
        "Chunky": [
            new Requirement(12, [[Moves.Moveless]]), // 1 bunch, 2 bananas, 5 bananas in GloomyGalleonStart
            new Requirement(10, [[Moves.Pineapple, Moves.RaisedWater]]), // 1 balloon in GalleonBeyondPineappleGate
            new Requirement(3, [ // 3 bananas in GalleonPastVines
                [Moves.Vines],
                [Moves.AllWarps, Moves.RaisedWater],
            ]),
            new Requirement(10, [ // 10 bananas in LighthouseUnderwater
                [Moves.Diving, Moves.AllWarps],
                [Moves.Diving, Moves.GalleonLighthouse],
            ]),
            new Requirement(15, [ // 3 bunches in ShipyardUnderwater
                [Moves.Diving, Moves.AllWarps],
                [Moves.Diving, Moves.GalleonPeanut],
            ]),
            new Requirement(20, [ // 1 balloon, 1 balloon in Shipyard
                [Moves.Pineapple, Moves.AllWarps],
                [Moves.Pineapple, Moves.GalleonPeanut],
            ]),
            new Requirement(5, [ // 1 bunch in Shipyard
                [Moves.AllWarps, Moves.RaisedWater],
                [Moves.RaisedWater, Moves.GalleonPeanut],
            ]),
            new Requirement(20, [ // 4 bunches in SickBay
                [Moves.Slam, Moves.AllWarps, Moves.GalleonShipSpawned],
                [Moves.Slam, Moves.RaisedWater, Moves.GalleonLighthouse, Moves.GalleonShipSpawned],
            ]),
            new Requirement(5, [ // 1 bunch in SickBay
                [Moves.Slam, Moves.Punch, Moves.AllWarps, Moves.GalleonShipSpawned],
                [Moves.Slam, Moves.Punch, Moves.RaisedWater, Moves.GalleonLighthouse, Moves.GalleonShipSpawned],
            ]),
        ],
    },
    "Fungi": {
        "DK": [
            new Requirement(15, [[Moves.Moveless]]), // 5 bananas, 5 bananas in FungiForestStart; 1 bunch in GiantMushroomArea
            new Requirement(10, [[Moves.Coconut]]), // 1 balloon in MillArea
            new Requirement(5, [[Moves.Night]]), // 5 bananas in ThornvineArea
            new Requirement(15, [[Moves.CheckOfLegends]]), // 3 bunches in MushroomLower
            new Requirement(5, [[Moves.Slam, Moves.Day]]), // 1 bunch in GrinderRoom
            new Requirement(10, [[Moves.LevelSlam, Moves.Coconut]]), // 1 balloon in GrinderRoom
            new Requirement(5, [[Moves.Strong, Moves.Night]]), // 1 bunch in ThornvineArea
            new Requirement(5, [[Moves.LevelSlam, Moves.Strong, Moves.Night]]), // 1 bunch in ThornvineBarn
            new Requirement(20, [ // 2 bananas in MushroomBlastLevelExterior; 13 bananas in MushroomLowerExterior; 1 bunch in MushroomUpperExterior
                [Moves.ClimbingCheck],
                [Moves.Rocket],
                [Moves.AllWarps],
                [Moves.CheckOfLegends],
            ]),
            new Requirement(10, [ // 2 bunches in ForestBaboonBlast
                [Moves.ClimbingCheck, Moves.Blast],
                [Moves.Blast, Moves.Rocket],
                [Moves.Blast, Moves.AllWarps],
                [Moves.Blast, Moves.CheckOfLegends],
            ]),
        ],
        "Diddy": [
            new Requirement(28, [[Moves.Moveless]]), // 1 bunch, 2 bunches in FungiForestStart; 2 bunches in GiantMushroomArea; 3 bananas in MillArea
            new Requirement(10, [[Moves.Peanut]]), // 1 balloon in SnideArea
            new Requirement(5, [[Moves.Spring]]), // 1 bunch in MillArea
            new Requirement(15, [ // 1 bunch, 10 bananas in HollowTreeArea
                [Moves.AllWarps],
                [Moves.ForestYellowTunnel],
            ]),
            new Requirement(10, [[Moves.ClimbingCheck, Moves.LevelSlam, Moves.Peanut]]), // 1 balloon in WinchRoom
            new Requirement(10, [[Moves.Guitar, Moves.Spring, Moves.Night]]), // 2 bunches in MillRafters
            new Requirement(17, [ // 7 bananas in MushroomMiddle; 10 bananas in MushroomUpperExterior
                [Moves.ClimbingCheck],
                [Moves.Rocket],
                [Moves.AllWarps],
                [Moves.CheckOfLegends],
            ]),
            new Requirement(5, [ // 1 bunch in HollowTreeArea
                [Moves.Rocket, Moves.AllWarps],
                [Moves.Rocket, Moves.ForestYellowTunnel],
            ]),
        ],
        "Lanky": [
            new Requirement(21, [[Moves.Moveless]]), // 1 bunch in FungiForestStart; 1 bunch, 10 bananas in GiantMushroomArea; 1 banana in MillArea
            new Requirement(2, [[Moves.ClimbingCheck]]), // 2 bananas in ForestVeryTopOfMill
            new Requirement(10, [[Moves.Grape]]), // 1 balloon in MushroomLower
            new Requirement(9, [ // 1 bunch, 4 bananas in ForestTopOfMill
                [Moves.ClimbingCheck],
                [Moves.Balloon],
            ]),
            new Requirement(18, [ // 1 bunch, 10 bananas, 3 bananas in HollowTreeArea
                [Moves.AllWarps],
                [Moves.ForestYellowTunnel],
            ]),
            new Requirement(10, [ // 1 bunch in ForestTopOfMill; 1 bunch in MillAttic
                [Moves.ClimbingCheck, Moves.Night],
                [Moves.Balloon, Moves.Night],
            ]),
            new Requirement(10, [ // 1 balloon in MushroomUpper
                [Moves.ClimbingCheck, Moves.Grape],
                [Moves.Rocket, Moves.Grape],
                [Moves.Grape, Moves.AllWarps],
                [Moves.Grape, Moves.CheckOfLegends],
            ]),
            new Requirement(5, [ // 1 bunch in MushroomVeryTopExterior
                [Moves.ClimbingCheck, Moves.Orangstand],
                [Moves.Rocket, Moves.Orangstand],
                [Moves.Orangstand, Moves.AllWarps],
                [Moves.Orangstand, Moves.CheckOfLegends],
            ]),
            new Requirement(15, [ // 1 bunch in MushroomLankyMushroomsRoom; 2 bunches in MushroomLankyZingersRoom
                [Moves.LevelSlam, Moves.Rocket],
                [Moves.ClimbingCheck, Moves.LevelSlam, Moves.Orangstand],
                [Moves.LevelSlam, Moves.Orangstand, Moves.AllWarps],
                [Moves.LevelSlam, Moves.Orangstand, Moves.CheckOfLegends],
            ]),
        ],
        "Tiny": [
            new Requirement(10, [[Moves.Moveless]]), // 1 bunch in FungiForestStart; 1 bunch in MushroomLower
            new Requirement(17, [[Moves.Diving]]), // 17 bananas in MillArea
            new Requirement(10, [[Moves.Feather]]), // 1 balloon in ThornvineArea
            new Requirement(4, [[Moves.ForestGreenTunnelFeather]]), // 4 bananas in FungiForestStart
            new Requirement(10, [[Moves.Mini, Moves.Day]]), // 2 bunches in MillChunkyTinyArea
            new Requirement(8, [ // 8 bananas in HollowTreeArea
                [Moves.AllWarps],
                [Moves.ForestYellowTunnel],
            ]),
            new Requirement(5, [[Moves.Mini, Moves.Punch, Moves.Day]]), // 1 bunch in MillChunkyTinyArea
            new Requirement(1, [ // 1 banana in WormArea
                [Moves.AllWarps],
                [Moves.ForestGreenTunnelFeather, Moves.ForestGreenTunnelPineapple],
            ]),
            new Requirement(5, [[Moves.Mini, Moves.Punch, Moves.Night, Moves.Day]]), // 1 bunch in SpiderRoom
            new Requirement(15, [ // 3 bunches in WormArea
                [Moves.ClimbingCheck, Moves.AllWarps],
                [Moves.ClimbingCheck, Moves.ForestGreenTunnelFeather, Moves.ForestGreenTunnelPineapple],
            ]),
            new Requirement(5, [ // 1 bunch in HollowTreeArea
                [Moves.Sax, Moves.Mini, Moves.AllWarps],
                [Moves.Sax, Moves.Mini, Moves.ForestYellowTunnel],
            ]),
            new Requirement(10, [ // 1 balloon in MushroomLowerExterior
                [Moves.ClimbingCheck, Moves.Feather],
                [Moves.Rocket, Moves.Feather],
                [Moves.Feather, Moves.AllWarps],
                [Moves.Feather, Moves.CheckOfLegends],
            ]),
        ],
        "Chunky": [
            new Requirement(10, [[Moves.Moveless]]), // 1 bunch, 1 bunch in FungiForestStart
            new Requirement(5, [[Moves.Punch, Moves.Day]]), // 1 bunch in MillChunkyTinyArea
            new Requirement(14, [ // 1 bunch, 9 bananas in WormArea
                [Moves.AllWarps],
                [Moves.ForestGreenTunnelFeather, Moves.ForestGreenTunnelPineapple],
            ]),
            new Requirement(41, [ // 1 bunch, 3 bananas in MushroomLowerBetweenLadders; 1 bunch, 3 bananas in MushroomLowerMid; 1 bunch, 3 bananas, 3 bananas in MushroomUpper; 1 bunch, 3 bananas, 3 bananas in MushroomUpperMid; 3 bananas in MushroomUpperVineFloor
                [Moves.ClimbingCheck],
                [Moves.Rocket],
                [Moves.AllWarps],
                [Moves.CheckOfLegends],
            ]),
            new Requirement(5, [ // 1 bunch in MushroomChunkyRoom
                [Moves.ClimbingCheck, Moves.LevelSlam],
                [Moves.LevelSlam, Moves.Rocket],
                [Moves.LevelSlam, Moves.AllWarps],
                [Moves.LevelSlam, Moves.CheckOfLegends],
            ]),
            new Requirement(10, [ // 1 balloon in MushroomNightExterior
                [Moves.ClimbingCheck, Moves.Pineapple],
                [Moves.Rocket, Moves.Pineapple],
                [Moves.Pineapple, Moves.AllWarps],
                [Moves.Pineapple, Moves.CheckOfLegends],
            ]),
            new Requirement(10, [ // 1 balloon in MushroomChunkyRoom
                [Moves.ClimbingCheck, Moves.LevelSlam, Moves.Pineapple],
                [Moves.LevelSlam, Moves.Rocket, Moves.Pineapple],
                [Moves.LevelSlam, Moves.Pineapple, Moves.AllWarps],
                [Moves.LevelSlam, Moves.Pineapple, Moves.CheckOfLegends],
            ]),
            new Requirement(5, [ // 1 bunch in MushroomNightDoor
                [Moves.Vines, Moves.ClimbingCheck],
                [Moves.Vines, Moves.Rocket],
                [Moves.Vines, Moves.AllWarps],
                [Moves.Vines, Moves.CheckOfLegends],
                [Moves.ClimbingCheck, Moves.Night],
                [Moves.Rocket, Moves.Night],
                [Moves.AllWarps, Moves.Night],
                [Moves.Night, Moves.CheckOfLegends],
            ]),
        ],
    },
    "Caves": {
        "DK": [
            new Requirement(25, [[Moves.Moveless]]), // 1 bunch in CabinArea; 1 bunch, 5 bananas in CrystalCavesMain; 1 bunch, 5 bananas in IglooArea
            new Requirement(10, [[Moves.Bongos]]), // 1 bunch in DonkeyCabin; 1 bunch in RotatingCabin
            new Requirement(20, [[Moves.Blast]]), // 4 bunches in CavesBaboonBlast
            new Requirement(3, [[Moves.CavesIceWalls]]), // 3 bananas in BoulderCave
            new Requirement(20, [[Moves.Coconut, Moves.CavesIceWalls]]), // 1 balloon in BoulderCave; 1 balloon in CavesGGRoom
            new Requirement(5, [[Moves.Bongos, Moves.CavesIglooPads]]), // 1 bunch in DonkeyIgloo
            new Requirement(10, [[Moves.Coconut, Moves.Bongos, Moves.CavesIglooPads]]), // 1 balloon in DonkeyIgloo
            new Requirement(7, [[Moves.Bongos, Moves.Strong, Moves.CavesIglooPads]]), // 7 bananas in DonkeyIgloo
        ],
        "Diddy": [
            new Requirement(5, [[Moves.Moveless]]), // 5 bananas in CrystalCavesMain
            new Requirement(20, [[Moves.Peanut]]), // 1 balloon in CabinArea; 1 balloon in CrystalCavesMain
            new Requirement(5, [[Moves.Guitar]]), // 5 bananas in DiddyLowerCabin
            new Requirement(30, [[Moves.Rocket]]), // 1 bunch, 1 bunch in CrystalCavesMain; 4 bunches in IglooArea
            new Requirement(5, [[Moves.Guitar, Moves.Rocket]]), // 1 bunch in DiddyLowerCabin
            new Requirement(10, [[Moves.Peanut, Moves.Guitar, Moves.CavesIglooPads]]), // 1 balloon in DiddyIgloo
            new Requirement(15, [[Moves.Guitar, Moves.Rocket, Moves.Spring]]), // 3 bunches in DiddyUpperCabin
            new Requirement(10, [ // 1 bunch, 5 bananas in CavesBlueprintCave
                [Moves.Rocket, Moves.AllWarps],
                [Moves.Rocket, Moves.Twirl, Moves.Mini],
                [Moves.Twirl, Moves.Mini, Moves.AllWarps],
            ]),
        ],
        "Lanky": [
            new Requirement(15, [[Moves.Moveless]]), // 10 bananas in CabinArea; 5 bananas in CrystalCavesMain
            new Requirement(10, [[Moves.Grape]]), // 1 balloon in CabinArea
            new Requirement(20, [[Moves.Balloon]]), // 1 bunch in CavesSprintCabinRoof; 3 bunches in CrystalCavesMain
            new Requirement(10, [[Moves.LevelSlam, Moves.Grape]]), // 1 balloon in FrozenCastle
            new Requirement(5, [[Moves.LevelSlam, Moves.Balloon]]), // 1 bunch in CrystalCavesMain
            new Requirement(20, [ // 4 bunches in CavesBlueprintPillar
                [Moves.Rocket],
                [Moves.AllWarps],
            ]),
            new Requirement(5, [[Moves.Trombone, Moves.Balloon]]), // 1 bunch in LankyCabin
            new Requirement(1, [[Moves.Trombone, Moves.CavesIglooPads]]), // 1 banana in LankyIgloo
            new Requirement(10, [[Moves.Grape, Moves.Trombone, Moves.CavesIglooPads]]), // 1 balloon in LankyIgloo
            new Requirement(4, [[Moves.Trombone, Moves.Balloon, Moves.CavesIglooPads]]), // 4 bananas in LankyIgloo
        ],
        "Tiny": [
            new Requirement(15, [[Moves.Moveless]]), // 10 bananas in CrystalCavesMain; 1 bunch in IglooArea
            new Requirement(10, [[Moves.Feather]]), // 1 balloon in CabinArea
            new Requirement(10, [[Moves.Sax]]), // 2 bunches in TinyCabin
            new Requirement(5, [[Moves.Mini]]), // 1 bunch in CrystalCavesMain
            new Requirement(10, [[Moves.Feather, Moves.Sax]]), // 1 balloon in TinyCabin
            new Requirement(5, [[Moves.Sax, Moves.CavesIglooPads]]), // 1 bunch in TinyIgloo
            new Requirement(10, [[Moves.Feather, Moves.Sax, Moves.CavesIglooPads]]), // 1 balloon in TinyIgloo
            new Requirement(20, [[Moves.Barrels, Moves.Monkeyport, Moves.Hunky, Moves.CavesIceWalls]]), // 4 bunches in GiantKosha
            new Requirement(10, [ // 1 balloon in CavesBlueprintCave
                [Moves.Rocket, Moves.Feather, Moves.AllWarps],
                [Moves.Feather, Moves.Twirl, Moves.Mini],
            ]),
            new Requirement(5, [ // 1 bunch in IglooArea
                [Moves.Rocket, Moves.Monkeyport, Moves.AllWarps],
                [Moves.Twirl, Moves.Mini, Moves.Monkeyport],
            ]),
        ],
        "Chunky": [
            new Requirement(18, [[Moves.Moveless]]), // 1 bunch in CabinArea; 1 bunch, 1 bunch, 3 bananas in CrystalCavesMain
            new Requirement(5, [[Moves.Barrels]]), // 1 bunch in CrystalCavesMain
            new Requirement(11, [[Moves.CavesIceWalls]]), // 1 bunch, 3 bananas in CavesGGRoom; 3 bananas in CavesSnideArea
            new Requirement(6, [[Moves.Barrels, Moves.CavesIceWalls]]), // 6 bananas in BoulderCave
            new Requirement(10, [[Moves.Pineapple, Moves.CavesIceWalls]]), // 1 balloon in CavesSnideArea
            new Requirement(10, [[Moves.Barrels, Moves.Hunky, Moves.CavesIceWalls]]), // 1 bunch in BoulderCave; 5 bananas in IglooArea
            new Requirement(20, [[Moves.Slam, Moves.Triangle, Moves.Gone]]), // 4 bunches in ChunkyCabin
            new Requirement(10, [[Moves.Pineapple, Moves.Triangle, Moves.CavesIglooPads]]), // 1 balloon in ChunkyIgloo
            new Requirement(10, [ // 1 balloon in CavesBonusCave
                [Moves.Pineapple, Moves.AllWarps],
                [Moves.Mini, Moves.Pineapple, Moves.CavesW3Bonus],
            ]),
        ],
    },
    "Castle": {
        "DK": [
            new Requirement(50, [[Moves.Moveless]]), // 45 bananas, 5 bananas in CreepyCastleMain
            new Requirement(10, [[Moves.LevelSlam]]), // 1 bunch in Dungeon; 1 bunch in Library
            new Requirement(5, [[Moves.CryptDKEntry]]), // 1 bunch in Crypt
            new Requirement(10, [[Moves.LevelSlam, Moves.Strong]]), // 2 bunches in LibraryPastSlam
            new Requirement(15, [[Moves.Coconut, Moves.Blast]]), // 1 balloon, 1 bunch in CastleTree
            new Requirement(10, [[Moves.Coconut, Moves.CryptDKEntry]]), // 1 balloon in CryptDonkeyRoom
        ],
        "Diddy": [
            new Requirement(20, [[Moves.Peanut]]), // 1 balloon in CreepyCastleMain; 1 balloon in LowerCave
            new Requirement(10, [[Moves.Rocket]]), // 1 bunch, 1 bunch in CreepyCastleMain
            new Requirement(20, [[Moves.Punch]]), // 2 bunches, 2 bunches in Dungeon
            new Requirement(5, [[Moves.CryptDiddyEntry]]), // 1 bunch in Crypt
            new Requirement(20, [[Moves.LevelSlam, Moves.Peanut]]), // 1 balloon in Ballroom; 1 balloon in Dungeon
            new Requirement(15, [[Moves.LevelSlam, Moves.Rocket]]), // 3 bunches in Ballroom
            new Requirement(10, [[Moves.Peanut, Moves.Charge, Moves.CryptDiddyEntry]]), // 1 balloon in CryptDiddyRoom
        ],
        "Lanky": [
            new Requirement(30, [[Moves.Moveless]]), // 5 bananas, 5 bunches in LowerCave
            new Requirement(30, [[Moves.LevelSlam]]), // 6 bunches in Greenhouse
            new Requirement(20, [[Moves.LevelSlam, Moves.Grape]]), // 1 balloon in Dungeon; 1 balloon in Tower
            new Requirement(10, [[Moves.Grape, Moves.Sprint, Moves.CryptLankyEntry]]), // 1 balloon in Mausoleum
            new Requirement(10, [[Moves.LevelSlam, Moves.Grape, Moves.Trombone, Moves.Balloon]]), // 1 balloon in Dungeon
        ],
        "Tiny": [
            new Requirement(50, [[Moves.Moveless]]), // 1 bunch, 45 bananas in CreepyCastleMain
            new Requirement(10, [[Moves.Feather]]), // 1 balloon in LowerCave
            new Requirement(5, [[Moves.Mini]]), // 1 bunch in TrashCan
            new Requirement(5, [[Moves.LevelSlam, Moves.Diddy]]), // 1 bunch in Ballroom
            new Requirement(5, [[Moves.Twirl, Moves.CryptTinyEntry]]), // 1 bunch in Mausoleum
            new Requirement(15, [[Moves.LevelSlam, Moves.Monkeyport, Moves.Diddy]]), // 1 bunch, 2 bunches in MuseumBehindGlass
            new Requirement(10, [[Moves.LevelSlam, Moves.Feather, Moves.Monkeyport, Moves.Diddy]]), // 1 balloon in MuseumBehindGlass
        ],
        "Chunky": [
            new Requirement(30, [[Moves.Moveless]]), // 30 bananas in UpperCave
            new Requirement(5, [[Moves.Blast]]), // 1 bunch in CastleTree
            new Requirement(10, [[Moves.LevelSlam, Moves.Pineapple]]), // 1 balloon in Museum
            new Requirement(30, [[Moves.Pineapple, Moves.Punch]]), // 2 balloons in Dungeon; 1 balloon in Shed
            new Requirement(10, [[Moves.Punch, Moves.CryptChunkyEntry]]), // 2 bunches in CryptChunkyRoom
            new Requirement(5, [[Moves.Barrels, Moves.LevelSlam, Moves.Punch]]), // 1 bunch in Museum
            new Requirement(10, [[Moves.Blast, Moves.Pineapple, Moves.Punch]]), // 1 balloon in CastleTreePastPunch
        ],
    },
}
