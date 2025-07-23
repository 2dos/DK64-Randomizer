const requirement_data = {
    "Japes": {
        "DK": [
            new Requirement(10, [[Moves.Moveless]]), // 1 bunch in JungleJapesMain; 1 bunch in JungleJapesStart
            new Requirement(21, [[Moves.ClimbingCheck]]), // 1 bunch in JapesCannonPlatform; 1 bunch in JapesHill; 1 bunch, 6 bananas in JapesHillTop
            new Requirement(10, [[Moves.Coconut]]), // 1 balloon in JungleJapesStart
            new Requirement(9, [[Moves.JapesCoconut]]), // 9 bananas in JapesBeyondCoconutGate2
            new Requirement(10, [[Moves.Vines, Moves.ClimbingCheck]]), // 1 bunch in JapesTnSAlcove; 5 bananas in JungleJapesStart
            new Requirement(10, [[Moves.ClimbingCheck, Moves.Coconut]]), // 1 balloon in JapesHillTop
            new Requirement(20, [[Moves.Coconut, Moves.JapesCoconut]]), // 1 balloon, 1 bunch, 1 bunch in JapesBeyondCoconutGate2
            new Requirement(10, [[Moves.Vines, Moves.ClimbingCheck, Moves.Blast]]), // 2 bunches in JapesBaboonBlast
        ],
        "Diddy": [
            new Requirement(5, [[Moves.Moveless]]), // 5 bananas in JungleJapesStart
            new Requirement(10, [[Moves.Diving]]), // 2 bunches in JungleJapesStart
            new Requirement(27, [[Moves.ClimbingCheck]]), // 7 bananas in JapesHillTop; 2 bunches in JungleJapesMain; 2 bunches in JungleJapesStart
            new Requirement(10, [[Moves.Peanut]]), // 1 balloon in JapesBeyondPeanutGate
            new Requirement(3, [[Moves.JapesCoconut]]), // 3 bananas in JapesBeyondCoconutGate2
            new Requirement(20, [[Moves.ClimbingCheck, Moves.Peanut]]), // 1 balloon in JapesTopOfMountain; 1 bunch, 5 bananas in Mine
            new Requirement(5, [[Moves.Coconut, Moves.JapesCoconut]]), // 1 bunch in JapesBeyondCoconutGate2
            new Requirement(15, [[Moves.ClimbingCheck, Moves.LevelSlam, Moves.Peanut]]), // 1 balloon, 1 bunch in Mine
            new Requirement(5, [[Moves.ClimbingCheck, Moves.LevelSlam, Moves.Peanut, Moves.Charge]]), // 1 bunch in Mine
        ],
        "Lanky": [
            new Requirement(1, [[Moves.Moveless]]), // 1 banana in JungleJapesStart
            new Requirement(5, [[Moves.Diving]]), // 5 bananas in JungleJapesStart
            new Requirement(10, [[Moves.ClimbingCheck]]), // 1 bunch, 1 bunch in JapesHillTop
            new Requirement(3, [[Moves.JapesCoconut]]), // 1 banana, 2 bananas in JapesBeyondCoconutGate2
            new Requirement(5, [[Moves.ClimbingCheck, Moves.JapesCoconut]]), // 1 bunch in JapesBeyondCoconutGate2
            new Requirement(10, [[Moves.Coconut, Moves.JapesCoconut]]), // 5 bananas in BeyondRambiGate; 1 bunch in JapesBeyondCoconutGate2
            new Requirement(5, [[Moves.Peanut, Moves.Grape]]), // 1 bunch in JapesBeyondPeanutGate
            new Requirement(20, [[Moves.Grape, Moves.JapesCoconut]]), // 1 balloon, 1 balloon in JapesBeyondCoconutGate2
            new Requirement(9, [[Moves.Orangstand, Moves.JapesCoconut]]), // 2 bananas in JapesBeyondCoconutGate2; 1 bunch, 2 bananas in JapesUselessSlope
            new Requirement(2, [ // 2 bananas in JapesPaintingRoomHill
                [Moves.Orangstand],
                [Moves.ClimbingCheck, Moves.Twirl],
            ]),
            new Requirement(20, [ // 2 bunches, 2 bunches in JapesLankyCave
                [Moves.Peanut, Moves.Orangstand],
                [Moves.ClimbingCheck, Moves.Peanut, Moves.Twirl],
            ]),
            new Requirement(10, [ // 1 balloon in JapesLankyCave
                [Moves.Peanut, Moves.Grape, Moves.Orangstand],
                [Moves.ClimbingCheck, Moves.Peanut, Moves.Grape, Moves.Twirl],
            ]),
        ],
        "Tiny": [
            new Requirement(5, [[Moves.Moveless]]), // 5 bananas in JungleJapesStart
            new Requirement(2, [[Moves.JapesCoconut]]), // 2 bananas in JapesBeyondCoconutGate2
            new Requirement(5, [[Moves.ClimbingCheck, Moves.JapesCoconut]]), // 1 bunch in JapesBeyondCoconutGate2
            new Requirement(10, [[Moves.Coconut, Moves.JapesCoconut]]), // 5 bananas in BeyondRambiGate; 1 bunch in JapesBeyondCoconutGate2
            new Requirement(5, [[Moves.Peanut, Moves.Feather]]), // 1 bunch in JapesBeyondPeanutGate
            new Requirement(10, [[Moves.Feather, Moves.JapesCoconut]]), // 1 balloon in JapesBeyondCoconutGate2
            new Requirement(5, [[Moves.JapesCoconut, Moves.JapesShellhive]]), // 1 bunch in JapesBeyondFeatherGate
            new Requirement(10, [[Moves.Coconut, Moves.Feather, Moves.JapesCoconut]]), // 1 balloon in BeyondRambiGate
            new Requirement(30, [[Moves.Mini, Moves.JapesCoconut, Moves.JapesShellhive]]), // 3 bunches, 3 bunches in JapesBeyondFeatherGate
            new Requirement(10, [[Moves.Feather, Moves.Mini, Moves.JapesCoconut, Moves.JapesShellhive]]), // 1 balloon in TinyHive
            new Requirement(8, [ // 8 bananas in TinyHive
                [Moves.Oranges, Moves.LevelSlam, Moves.Mini, Moves.JapesCoconut, Moves.JapesShellhive],
                [Moves.LevelSlam, Moves.Sax, Moves.Mini, Moves.JapesCoconut, Moves.JapesShellhive],
            ]),
        ],
        "Chunky": [
            new Requirement(5, [[Moves.Moveless]]), // 5 bananas in JungleJapesStart
            new Requirement(10, [[Moves.ClimbingCheck]]), // 2 bunches in JapesHillTop
            new Requirement(10, [[Moves.JapesCoconut]]), // 10 bananas in JapesBeyondCoconutGate1
            new Requirement(15, [[Moves.Barrels, Moves.Slam]]), // 2 bunches, 5 bananas in JapesCatacomb
            new Requirement(5, [[Moves.ClimbingCheck, Moves.JapesCoconut]]), // 1 bunch in JapesBeyondCoconutGate2
            new Requirement(5, [[Moves.Barrels, Moves.Coconut, Moves.JapesCoconut]]), // 1 bunch in BeyondRambiGate
            new Requirement(30, [[Moves.Coconut, Moves.Pineapple, Moves.JapesCoconut]]), // 3 balloons in BeyondRambiGate
            new Requirement(20, [[Moves.ClimbingCheck, Moves.Hunky, Moves.JapesCoconut, Moves.JapesShellhive]]), // 4 bunches in JapesBeyondFeatherGate
        ],
    },
    "Aztec": {
        "DK": [
            new Requirement(3, [[Moves.Moveless]]), // 3 bananas in AngryAztecOasis
            new Requirement(15, [[Moves.ClimbingCheck]]), // 3 bunches in AngryAztecOasis
            new Requirement(7, [[Moves.AztecTunnelDoor]]), // 3 bananas, 4 bananas in AngryAztecMain
            new Requirement(10, [[Moves.Coconut, Moves.Strong]]), // 2 bunches in AngryAztecOasis
            new Requirement(30, [[Moves.Coconut, Moves.AztecTunnelDoor]]), // 1 balloon, 2 balloons in AngryAztecMain
            new Requirement(15, [ // 15 bananas in LlamaTemple
                [Moves.Coconut, Moves.AztecTunnelDoor, Moves.AztecLlama],
                [Moves.Grape, Moves.AztecTunnelDoor, Moves.AztecLlama],
                [Moves.Feather, Moves.AztecTunnelDoor, Moves.AztecLlama],
            ]),
            new Requirement(20, [ // 4 bunches in AztecDonkeyQuicksandCave
                [Moves.LevelSlam, Moves.Coconut, Moves.Strong, Moves.AztecTunnelDoor, Moves.AztecLlama],
                [Moves.LevelSlam, Moves.Strong, Moves.Grape, Moves.AztecTunnelDoor, Moves.AztecLlama],
                [Moves.LevelSlam, Moves.Strong, Moves.Feather, Moves.AztecTunnelDoor, Moves.AztecLlama],
            ]),
        ],
        "Diddy": [
            new Requirement(5, [[Moves.Moveless]]), // 1 bunch in AngryAztecOasis
            new Requirement(10, [[Moves.Peanut]]), // 1 balloon in AngryAztecOasis
            new Requirement(15, [[Moves.AztecTunnelDoor]]), // 3 bananas, 3 bananas, 4 bananas, 5 bananas in AngryAztecMain
            new Requirement(18, [[Moves.LevelSlam, Moves.Peanut]]), // 3 bananas, 3 bunches in TempleStart
            new Requirement(10, [[Moves.Rocket, Moves.AztecTunnelDoor]]), // 1 bunch, 1 bunch in AngryAztecMain
            new Requirement(7, [[Moves.Diving, Moves.Peanut, Moves.TinyTempleIce]]), // 7 bananas in TempleUnderwater
            new Requirement(10, [[Moves.Peanut, Moves.AztecTunnelDoor, Moves.Aztec5DT]]), // 1 balloon in DiddyTemple
            new Requirement(15, [ // 3 bunches in AngryAztecMain
                [Moves.ClimbingCheck, Moves.AztecTunnelDoor],
                [Moves.Rocket, Moves.AztecTunnelDoor],
            ]),
            new Requirement(10, [ // 1 balloon in AztecDonkeyQuicksandCave
                [Moves.LevelSlam, Moves.Coconut, Moves.Strong, Moves.Peanut, Moves.AztecTunnelDoor, Moves.AztecLlama],
                [Moves.LevelSlam, Moves.Strong, Moves.Peanut, Moves.Grape, Moves.AztecTunnelDoor, Moves.AztecLlama],
                [Moves.LevelSlam, Moves.Strong, Moves.Peanut, Moves.Feather, Moves.AztecTunnelDoor, Moves.AztecLlama],
            ]),
        ],
        "Lanky": [
            new Requirement(5, [[Moves.Moveless]]), // 5 bananas in AngryAztecOasis
            new Requirement(10, [[Moves.AztecTunnelDoor]]), // 1 bunch, 5 bananas in AngryAztecMain
            new Requirement(25, [[Moves.ClimbingCheck, Moves.AztecTunnelDoor]]), // 5 bunches in AngryAztecMain
            new Requirement(14, [[Moves.Diving, Moves.Grape, Moves.TinyTempleIce]]), // 1 bunch, 9 bananas in TempleVultureRoom
            new Requirement(20, [[Moves.Grape, Moves.AztecTunnelDoor, Moves.AztecLlama]]), // 2 balloons in LlamaTemple
            new Requirement(10, [[Moves.Grape, Moves.AztecTunnelDoor, Moves.Aztec5DT]]), // 1 balloon in LankyTemple
            new Requirement(5, [[Moves.Vines, Moves.Grape, Moves.AztecTunnelDoor, Moves.AztecLlama]]), // 1 bunch in LlamaTempleMatching
            new Requirement(11, [ // 1 bunch, 6 bananas in LlamaTemple
                [Moves.Coconut, Moves.AztecTunnelDoor, Moves.AztecLlama],
                [Moves.Grape, Moves.AztecTunnelDoor, Moves.AztecLlama],
                [Moves.Feather, Moves.AztecTunnelDoor, Moves.AztecLlama],
            ]),
        ],
        "Tiny": [
            new Requirement(25, [[Moves.AztecTunnelDoor]]), // 1 bunch, 1 bunch, 10 bananas, 5 bananas in AngryAztecMain
            new Requirement(20, [[Moves.Diving, Moves.Feather, Moves.TinyTempleIce]]), // 2 balloons in TempleKONGRoom
            new Requirement(10, [[Moves.Feather, Moves.AztecTunnelDoor, Moves.AztecLlama]]), // 1 balloon in LlamaTemple
            new Requirement(5, [[Moves.Diving, Moves.Feather, Moves.Mini, Moves.TinyTempleIce]]), // 5 bananas in TempleUnderwater
            new Requirement(25, [ // 5 bunches in AngryAztecMain
                [Moves.ClimbingCheck, Moves.AztecTunnelDoor],
                [Moves.Twirl, Moves.AztecTunnelDoor],
            ]),
            new Requirement(3, [ // 3 bananas in LlamaTemple
                [Moves.Coconut, Moves.AztecTunnelDoor, Moves.AztecLlama],
                [Moves.Grape, Moves.AztecTunnelDoor, Moves.AztecLlama],
                [Moves.Feather, Moves.AztecTunnelDoor, Moves.AztecLlama],
            ]),
            new Requirement(2, [ // 2 bananas in LlamaTempleBack
                [Moves.Coconut, Moves.Mini, Moves.AztecTunnelDoor, Moves.AztecLlama],
                [Moves.Grape, Moves.Mini, Moves.AztecTunnelDoor, Moves.AztecLlama],
                [Moves.Feather, Moves.Mini, Moves.AztecTunnelDoor, Moves.AztecLlama],
            ]),
            new Requirement(10, [ // 2 bunches in LlamaTempleBack
                [Moves.LevelSlam, Moves.Coconut, Moves.Mini, Moves.AztecTunnelDoor, Moves.AztecLlama],
                [Moves.LevelSlam, Moves.Grape, Moves.Mini, Moves.AztecTunnelDoor, Moves.AztecLlama],
                [Moves.LevelSlam, Moves.Feather, Moves.Mini, Moves.AztecTunnelDoor, Moves.AztecLlama],
            ]),
        ],
        "Chunky": [
            new Requirement(29, [[Moves.Pineapple]]), // 4 bananas, 5 bunches in TempleStart
            new Requirement(16, [[Moves.AztecTunnelDoor]]), // 10 bananas, 6 bananas in AngryAztecMain
            new Requirement(5, [ // 5 bananas in BetweenVinesByPortal
                [Moves.Vines],
                [Moves.Twirl],
            ]),
            new Requirement(10, [[Moves.Diving, Moves.Pineapple, Moves.TinyTempleIce]]), // 1 balloon in TempleVultureRoom
            new Requirement(20, [[Moves.Pineapple, Moves.AztecTunnelDoor, Moves.Aztec5DT]]), // 2 balloons in ChunkyTemple
            new Requirement(20, [ // 4 bunches in BetweenVinesByPortal
                [Moves.Vines, Moves.Pineapple],
                [Moves.Twirl, Moves.Pineapple],
            ]),
        ],
    },
    "Factory": {
        "DK": [
            new Requirement(15, [[Moves.Moveless]]), // 4 bananas, 6 bananas in BeyondHatch; 5 bananas in FranticFactoryStart
            new Requirement(10, [[Moves.Coconut]]), // 1 balloon in BeyondHatch
            new Requirement(20, [[Moves.Blast]]), // 4 bunches in FactoryBaboonBlast
            new Requirement(5, [[Moves.ClimbingCheck, Moves.FactoryTesting]]), // 5 bananas in Testing
            new Requirement(15, [[Moves.Strong, Moves.FactoryProduction]]), // 3 bunches in InsideCore
            new Requirement(35, [[Moves.ClimbingCheck, Moves.Coconut, Moves.FactoryTesting]]), // 3 bunches in PowerHut; 1 balloon in RandDUpper; 1 balloon in Testing
        ],
        "Diddy": [
            new Requirement(12, [[Moves.Moveless]]), // 12 bananas in BeyondHatch
            new Requirement(10, [[Moves.ClimbingCheck]]), // 1 bunch, 5 bananas in FactoryArcadeTunnel
            new Requirement(8, [[Moves.ClimbingCheck, Moves.FactoryTesting]]), // 1 bunch, 3 bananas in Testing
            new Requirement(15, [[Moves.ClimbingCheck, Moves.FactoryProduction]]), // 3 bunches in UpperCore
            new Requirement(25, [[Moves.ClimbingCheck, Moves.Spring, Moves.FactoryTesting]]), // 5 bunches in Testing
            new Requirement(30, [[Moves.ClimbingCheck, Moves.Peanut, Moves.Guitar, Moves.FactoryTesting]]), // 3 balloons in RandDUpper
        ],
        "Lanky": [
            new Requirement(11, [[Moves.Moveless]]), // 1 banana, 5 bananas in BeyondHatch; 1 bunch in FranticFactoryStart
            new Requirement(4, [[Moves.Orangstand]]), // 4 bananas in FactoryStoragePipe
            new Requirement(15, [[Moves.ClimbingCheck, Moves.FactoryTesting]]), // 1 bunch, 5 bananas in RandD; 5 bananas in RandDUpper
            new Requirement(20, [[Moves.ClimbingCheck, Moves.FactoryProduction]]), // 3 bunches in SpinningCore; 1 bunch in UpperCore
            new Requirement(10, [[Moves.Grape, Moves.FactoryProduction]]), // 1 balloon in InsideCore
            new Requirement(10, [[Moves.ClimbingCheck, Moves.Grape, Moves.FactoryProduction]]), // 1 balloon in UpperCore
            new Requirement(20, [[Moves.ClimbingCheck, Moves.Orangstand, Moves.FactoryProduction]]), // 4 bunches in UpperCore
            new Requirement(10, [[Moves.ClimbingCheck, Moves.Grape, Moves.Trombone, Moves.FactoryTesting]]), // 1 balloon in RandD
        ],
        "Tiny": [
            new Requirement(13, [[Moves.Moveless]]), // 2 bunches in AlcoveBeyondHatch; 3 bananas in FranticFactoryStart
            new Requirement(5, [[Moves.ClimbingCheck]]), // 1 bunch in FactoryArcadeTunnel
            new Requirement(22, [[Moves.ClimbingCheck, Moves.FactoryTesting]]), // 10 bananas in RandD; 1 bunch, 7 bananas in Testing
            new Requirement(20, [[Moves.ClimbingCheck, Moves.FactoryProduction]]), // 4 bunches in UpperCore
            new Requirement(10, [[Moves.Feather, Moves.FactoryProduction]]), // 1 balloon in MiddleCore
            new Requirement(20, [[Moves.ClimbingCheck, Moves.Feather, Moves.FactoryTesting]]), // 1 balloon, 1 balloon in Testing
            new Requirement(5, [[Moves.ClimbingCheck, Moves.Twirl, Moves.FactoryProduction]]), // 1 bunch in UpperCore
            new Requirement(5, [[Moves.ClimbingCheck, Moves.Mini, Moves.FactoryTesting]]), // 1 bunch in Testing
        ],
        "Chunky": [
            new Requirement(20, [[Moves.Moveless]]), // 1 bunch in BeyondHatch; 1 bunch, 10 bananas in FranticFactoryStart
            new Requirement(10, [[Moves.Pineapple]]), // 1 balloon in FranticFactoryStart
            new Requirement(15, [[Moves.Punch]]), // 3 bunches in BeyondHatch
            new Requirement(5, [[Moves.ClimbingCheck, Moves.FactoryTesting]]), // 1 bunch in Testing
            new Requirement(20, [[Moves.ClimbingCheck, Moves.FactoryProduction]]), // 4 bunches in SpinningCore
            new Requirement(10, [[Moves.ClimbingCheck, Moves.Pineapple, Moves.FactoryTesting]]), // 1 balloon in Testing
            new Requirement(10, [[Moves.ClimbingCheck, Moves.Triangle, Moves.Punch, Moves.FactoryTesting]]), // 10 bananas in RandDUpper
            new Requirement(10, [[Moves.ClimbingCheck, Moves.Pineapple, Moves.Triangle, Moves.Punch, Moves.FactoryTesting]]), // 1 balloon in RandDUpper
        ],
    },
    "Galleon": {
        "DK": [
            new Requirement(10, [[Moves.Coconut]]), // 1 balloon in GloomyGalleonStart
            new Requirement(15, [[Moves.Diving, Moves.GalleonPeanut]]), // 3 bunches in ShipyardUnderwater
            new Requirement(10, [[Moves.Diving, Moves.Bongos, Moves.GalleonPeanut]]), // 10 bananas in BongosShip
            new Requirement(10, [[Moves.Diving, Moves.GalleonLighthouse, Moves.Enguarde]]), // 10 bananas in LighthouseEnguardeDoor
            new Requirement(10, [[Moves.Coconut, Moves.RaisedWater, Moves.GalleonLighthouse]]), // 1 balloon in LighthousePlatform
            new Requirement(15, [[Moves.Blast, Moves.RaisedWater, Moves.GalleonLighthouse]]), // 3 bunches in GalleonBaboonBlast
            new Requirement(20, [[Moves.ClimbingCheck, Moves.LevelSlam, Moves.RaisedWater, Moves.GalleonLighthouse]]), // 4 bunches in LighthouseAboveLadder
            new Requirement(10, [[Moves.ClimbingCheck, Moves.LevelSlam, Moves.Coconut, Moves.RaisedWater, Moves.GalleonLighthouse]]), // 1 balloon in Lighthouse
        ],
        "Diddy": [
            new Requirement(10, [[Moves.Moveless]]), // 2 bunches in GloomyGalleonStart
            new Requirement(36, [[Moves.Diving, Moves.GalleonPeanut]]), // 10 bananas, 4 bunches, 6 bananas in ShipyardUnderwater
            new Requirement(10, [[Moves.Peanut, Moves.GalleonPeanut]]), // 1 balloon in Shipyard
            new Requirement(10, [[Moves.Peanut, Moves.RaisedWater, Moves.GalleonLighthouse]]), // 1 balloon in LighthousePlatform
            new Requirement(10, [[Moves.Rocket, Moves.RaisedWater, Moves.GalleonLighthouse]]), // 2 bunches in LighthousePlatform
            new Requirement(10, [[Moves.Diving, Moves.Peanut, Moves.GalleonPeanut, Moves.GalleonTreasure]]), // 1 balloon in TreasureRoom
            new Requirement(14, [[Moves.Diving, Moves.Guitar, Moves.LoweredWater, Moves.GalleonPeanut]]), // 2 bunches, 4 bananas in GuitarShip
        ],
        "Lanky": [
            new Requirement(5, [[Moves.Moveless]]), // 5 bananas in GloomyGalleonStart
            new Requirement(5, [[Moves.GalleonPeanut]]), // 1 bunch in Shipyard
            new Requirement(25, [[Moves.Diving, Moves.GalleonLighthouse]]), // 4 bunches, 5 bananas in LighthouseUnderwater
            new Requirement(5, [[Moves.Diving, Moves.GalleonPeanut]]), // 1 bunch in ShipyardUnderwater
            new Requirement(20, [[Moves.Grape, Moves.Punch]]), // 2 balloons in GloomyGalleonStart
            new Requirement(10, [[Moves.Grape, Moves.GalleonPeanut]]), // 1 balloon in Shipyard
            new Requirement(10, [[Moves.Diving, Moves.LevelSlam, Moves.GalleonPeanut]]), // 1 bunch, 5 bananas in LankyShip
            new Requirement(15, [[Moves.Diving, Moves.Trombone, Moves.LoweredWater, Moves.GalleonPeanut]]), // 3 bunches in TromboneShip
            new Requirement(1, [[Moves.Diving, Moves.RaisedWater, Moves.GalleonPeanut, Moves.GalleonTreasure]]), // 1 banana in TreasureRoom
            new Requirement(4, [[Moves.Diving, Moves.Balloon, Moves.RaisedWater, Moves.GalleonPeanut, Moves.GalleonTreasure]]), // 4 bananas in TreasureRoom
        ],
        "Tiny": [
            new Requirement(9, [[Moves.Moveless]]), // 4 bananas, 5 bananas in GloomyGalleonStart
            new Requirement(8, [[Moves.Vines]]), // 1 bunch, 3 bananas in GalleonPastVines
            new Requirement(15, [[Moves.Pineapple, Moves.RaisedWater]]), // 3 bunches in GalleonBeyondPineappleGate
            new Requirement(5, [[Moves.RaisedWater, Moves.GalleonLighthouse]]), // 1 bunch in LighthouseSnideAlcove
            new Requirement(10, [[Moves.Diving, Moves.LevelSlam, Moves.GalleonPeanut]]), // 2 bunches in TinyShip
            new Requirement(18, [[Moves.Diving, Moves.Sax, Moves.GalleonPeanut]]), // 2 bunches, 8 bananas in SaxophoneShip
            new Requirement(5, [[Moves.Diving, Moves.GalleonPeanut, Moves.GalleonTreasure]]), // 1 bunch in TreasureRoom
            new Requirement(10, [[Moves.Feather, Moves.RaisedWater, Moves.GalleonLighthouse]]), // 1 balloon in LighthouseSnideAlcove
            new Requirement(10, [[Moves.Feather, Moves.LoweredWater, Moves.GalleonLighthouse]]), // 1 balloon in LighthouseSurface
            new Requirement(10, [[Moves.Diving, Moves.Feather, Moves.GalleonPeanut, Moves.GalleonTreasure]]), // 1 balloon in TreasureRoom
        ],
        "Chunky": [
            new Requirement(12, [[Moves.Moveless]]), // 1 bunch, 2 bananas, 5 bananas in GloomyGalleonStart
            new Requirement(3, [[Moves.Vines]]), // 3 bananas in GalleonPastVines
            new Requirement(10, [[Moves.Diving, Moves.GalleonLighthouse]]), // 10 bananas in LighthouseUnderwater
            new Requirement(15, [[Moves.Diving, Moves.GalleonPeanut]]), // 3 bunches in ShipyardUnderwater
            new Requirement(10, [[Moves.Pineapple, Moves.RaisedWater]]), // 1 balloon in GalleonBeyondPineappleGate
            new Requirement(20, [[Moves.Pineapple, Moves.GalleonPeanut]]), // 1 balloon, 1 balloon in Shipyard
            new Requirement(5, [[Moves.RaisedWater, Moves.GalleonPeanut]]), // 1 bunch in Shipyard
            new Requirement(20, [[Moves.Slam, Moves.RaisedWater, Moves.GalleonLighthouse, Moves.GalleonShipSpawned]]), // 4 bunches in SickBay
            new Requirement(5, [[Moves.Slam, Moves.Punch, Moves.RaisedWater, Moves.GalleonLighthouse, Moves.GalleonShipSpawned]]), // 1 bunch in SickBay
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
            new Requirement(20, [ // 2 bananas in MushroomBlastLevelExterior; 13 bananas in MushroomLowerExterior; 1 bunch in MushroomUpperExterior
                [Moves.ClimbingCheck],
                [Moves.Rocket],
                [Moves.CheckOfLegends],
            ]),
            new Requirement(5, [[Moves.LevelSlam, Moves.Strong, Moves.Night]]), // 1 bunch in ThornvineBarn
            new Requirement(10, [ // 2 bunches in ForestBaboonBlast
                [Moves.ClimbingCheck, Moves.Blast],
                [Moves.Blast, Moves.Rocket],
                [Moves.Blast, Moves.CheckOfLegends],
            ]),
        ],
        "Diddy": [
            new Requirement(28, [[Moves.Moveless]]), // 1 bunch, 2 bunches in FungiForestStart; 2 bunches in GiantMushroomArea; 3 bananas in MillArea
            new Requirement(10, [[Moves.Peanut]]), // 1 balloon in MillArea
            new Requirement(5, [[Moves.Spring]]), // 1 bunch in MillArea
            new Requirement(15, [[Moves.ForestYellowTunnel]]), // 1 bunch, 10 bananas in HollowTreeArea
            new Requirement(5, [[Moves.Rocket, Moves.ForestYellowTunnel]]), // 1 bunch in HollowTreeArea
            new Requirement(10, [[Moves.ClimbingCheck, Moves.LevelSlam, Moves.Peanut]]), // 1 balloon in WinchRoom
            new Requirement(17, [ // 7 bananas in MushroomMiddle; 10 bananas in MushroomUpperExterior
                [Moves.ClimbingCheck],
                [Moves.Rocket],
                [Moves.CheckOfLegends],
            ]),
            new Requirement(10, [[Moves.Guitar, Moves.Spring, Moves.Night]]), // 2 bunches in MillRafters
        ],
        "Lanky": [
            new Requirement(21, [[Moves.Moveless]]), // 1 bunch in FungiForestStart; 1 bunch, 10 bananas in GiantMushroomArea; 1 banana in MillArea
            new Requirement(2, [[Moves.ClimbingCheck]]), // 2 bananas in ForestVeryTopOfMill
            new Requirement(10, [[Moves.Grape]]), // 1 balloon in MushroomLower
            new Requirement(18, [[Moves.ForestYellowTunnel]]), // 1 bunch, 10 bananas, 3 bananas in HollowTreeArea
            new Requirement(9, [ // 1 bunch, 4 bananas in ForestTopOfMill
                [Moves.ClimbingCheck],
                [Moves.Balloon],
            ]),
            new Requirement(10, [ // 1 bunch in ForestTopOfMill; 1 bunch in MillAttic
                [Moves.ClimbingCheck, Moves.Night],
                [Moves.Balloon, Moves.Night],
            ]),
            new Requirement(10, [ // 1 balloon in MushroomUpper
                [Moves.ClimbingCheck, Moves.Grape],
                [Moves.Rocket, Moves.Grape],
                [Moves.Grape, Moves.CheckOfLegends],
            ]),
            new Requirement(5, [ // 1 bunch in MushroomUpperExterior
                [Moves.ClimbingCheck, Moves.Orangstand],
                [Moves.Rocket, Moves.Orangstand],
                [Moves.Orangstand, Moves.CheckOfLegends],
            ]),
            new Requirement(15, [ // 1 bunch in MushroomLankyMushroomsRoom; 2 bunches in MushroomLankyZingersRoom
                [Moves.ClimbingCheck, Moves.LevelSlam, Moves.Orangstand],
                [Moves.LevelSlam, Moves.Rocket, Moves.Orangstand],
                [Moves.LevelSlam, Moves.Orangstand, Moves.CheckOfLegends],
            ]),
        ],
        "Tiny": [
            new Requirement(10, [[Moves.Moveless]]), // 1 bunch in FungiForestStart; 1 bunch in MushroomLower
            new Requirement(17, [[Moves.Diving]]), // 17 bananas in MillArea
            new Requirement(10, [[Moves.Feather]]), // 1 balloon in ThornvineArea
            new Requirement(8, [[Moves.ForestYellowTunnel]]), // 8 bananas in HollowTreeArea
            new Requirement(4, [[Moves.ForestGreenTunnelFeather]]), // 4 bananas in FungiForestStart
            new Requirement(5, [[Moves.Punch, Moves.Day]]), // 1 bunch in MillChunkyTinyArea
            new Requirement(1, [[Moves.ForestGreenTunnelFeather, Moves.ForestGreenTunnelPineapple]]), // 1 banana in WormArea
            new Requirement(15, [[Moves.ClimbingCheck, Moves.ForestGreenTunnelFeather, Moves.ForestGreenTunnelPineapple]]), // 3 bunches in WormArea
            new Requirement(5, [[Moves.Sax, Moves.Mini, Moves.ForestYellowTunnel]]), // 1 bunch in HollowTreeArea
            new Requirement(10, [ // 2 bunches in MillChunkyTinyArea
                [Moves.Mini, Moves.Day],
                [Moves.Punch, Moves.Day],
            ]),
            new Requirement(10, [ // 1 balloon in MushroomLowerExterior
                [Moves.ClimbingCheck, Moves.Feather],
                [Moves.Rocket, Moves.Feather],
                [Moves.Feather, Moves.CheckOfLegends],
            ]),
            new Requirement(5, [ // 1 bunch in SpiderRoom
                [Moves.Mini, Moves.Night, Moves.Day],
                [Moves.Punch, Moves.Night, Moves.Day],
            ]),
        ],
        "Chunky": [
            new Requirement(10, [[Moves.Moveless]]), // 1 bunch, 1 bunch in FungiForestStart
            new Requirement(5, [[Moves.Punch, Moves.Day]]), // 1 bunch in MillChunkyTinyArea
            new Requirement(14, [[Moves.ForestGreenTunnelFeather, Moves.ForestGreenTunnelPineapple]]), // 1 bunch, 9 bananas in WormArea
            new Requirement(41, [ // 1 bunch, 3 bananas in MushroomLowerBetweenLadders; 1 bunch, 3 bananas in MushroomLowerMid; 1 bunch, 3 bananas, 3 bananas in MushroomUpper; 1 bunch, 3 bananas, 3 bananas in MushroomUpperMid; 3 bananas in MushroomUpperVineFloor
                [Moves.ClimbingCheck],
                [Moves.Rocket],
                [Moves.CheckOfLegends],
            ]),
            new Requirement(5, [ // 1 bunch in MushroomChunkyRoom
                [Moves.ClimbingCheck, Moves.LevelSlam],
                [Moves.LevelSlam, Moves.Rocket],
                [Moves.LevelSlam, Moves.CheckOfLegends],
            ]),
            new Requirement(10, [ // 1 balloon in MushroomNightExterior
                [Moves.ClimbingCheck, Moves.Pineapple],
                [Moves.Rocket, Moves.Pineapple],
                [Moves.Pineapple, Moves.CheckOfLegends],
            ]),
            new Requirement(10, [ // 1 balloon in MushroomChunkyRoom
                [Moves.ClimbingCheck, Moves.LevelSlam, Moves.Pineapple],
                [Moves.LevelSlam, Moves.Rocket, Moves.Pineapple],
                [Moves.LevelSlam, Moves.Pineapple, Moves.CheckOfLegends],
            ]),
            new Requirement(5, [ // 1 bunch in MushroomNightDoor
                [Moves.Vines, Moves.ClimbingCheck],
                [Moves.Vines, Moves.Rocket],
                [Moves.Vines, Moves.CheckOfLegends],
                [Moves.ClimbingCheck, Moves.Night],
                [Moves.Rocket, Moves.Night],
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
            new Requirement(10, [[Moves.Rocket, Moves.Twirl, Moves.Mini]]), // 1 bunch, 5 bananas in CavesBlueprintCave
        ],
        "Lanky": [
            new Requirement(15, [[Moves.Moveless]]), // 10 bananas in CabinArea; 5 bananas in CrystalCavesMain
            new Requirement(20, [[Moves.Rocket]]), // 4 bunches in CavesBlueprintPillar
            new Requirement(10, [[Moves.Grape]]), // 1 balloon in CabinArea
            new Requirement(20, [[Moves.Balloon]]), // 1 bunch in CavesSprintCabinRoof; 3 bunches in CrystalCavesMain
            new Requirement(10, [[Moves.LevelSlam, Moves.Grape]]), // 1 balloon in FrozenCastle
            new Requirement(5, [[Moves.LevelSlam, Moves.Balloon]]), // 1 bunch in CrystalCavesMain
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
            new Requirement(10, [[Moves.Feather, Moves.Twirl, Moves.Mini]]), // 1 balloon in CavesBlueprintCave
            new Requirement(5, [[Moves.Twirl, Moves.Mini, Moves.Monkeyport]]), // 1 bunch in IglooArea
            new Requirement(20, [[Moves.Barrels, Moves.Monkeyport, Moves.Hunky, Moves.CavesIceWalls]]), // 4 bunches in GiantKosha
        ],
        "Chunky": [
            new Requirement(18, [[Moves.Moveless]]), // 1 bunch in CabinArea; 1 bunch, 1 bunch, 3 bananas in CrystalCavesMain
            new Requirement(5, [[Moves.Barrels]]), // 1 bunch in CrystalCavesMain
            new Requirement(11, [[Moves.CavesIceWalls]]), // 1 bunch, 3 bananas in CavesGGRoom; 3 bananas in CavesSnideArea
            new Requirement(6, [[Moves.Barrels, Moves.CavesIceWalls]]), // 6 bananas in BoulderCave
            new Requirement(10, [[Moves.Mini, Moves.Pineapple]]), // 1 balloon in CavesBonusCave
            new Requirement(10, [[Moves.Pineapple, Moves.CavesIceWalls]]), // 1 balloon in CavesSnideArea
            new Requirement(10, [[Moves.Barrels, Moves.Hunky, Moves.CavesIceWalls]]), // 1 bunch in BoulderCave; 5 bananas in IglooArea
            new Requirement(20, [[Moves.Slam, Moves.Triangle, Moves.Gone]]), // 4 bunches in ChunkyCabin
            new Requirement(10, [[Moves.Pineapple, Moves.Triangle, Moves.CavesIglooPads]]), // 1 balloon in ChunkyIgloo
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
            new Requirement(5, [[Moves.LevelSlam]]), // 1 bunch in Ballroom
            new Requirement(10, [[Moves.Feather]]), // 1 balloon in LowerCave
            new Requirement(5, [[Moves.Mini]]), // 1 bunch in TrashCan
            new Requirement(15, [[Moves.LevelSlam, Moves.Monkeyport]]), // 1 bunch, 2 bunches in MuseumBehindGlass
            new Requirement(5, [[Moves.Twirl, Moves.CryptTinyEntry]]), // 1 bunch in Mausoleum
            new Requirement(10, [[Moves.LevelSlam, Moves.Feather, Moves.Monkeyport]]), // 1 balloon in MuseumBehindGlass
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
