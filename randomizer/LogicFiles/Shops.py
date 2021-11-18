from LogicClasses import Region, Location, Event, Exit
from Enums.Events import Events
from Enums.Levels import Levels

Regions = {
    "Funky": Region("Funky", False, [
        Location("Coconut Gun", lambda l: l.LevelEntered(Levels.JungleJapes) and l.isdonkey),
        Location("Peanut Gun", lambda l: l.LevelEntered(Levels.JungleJapes) and l.isdiddy),
        Location("Grape Gun", lambda l: l.LevelEntered(Levels.JungleJapes) and l.islanky),
        Location("Feather Gun", lambda l: l.LevelEntered(Levels.JungleJapes) and l.istiny),
        Location("Pineapple Gun", lambda l: l.LevelEntered(Levels.JungleJapes) and l.ischunky),

        Location("Ammo Belt 1", lambda l: l.LevelEntered(Levels.FranticFactory)),
        Location("Homing Ammo", lambda l: l.LevelEntered(Levels.FungiForest)),
        Location("Ammo Belt 2", lambda l: l.LevelEntered(Levels.CrystalCaves)),
        Location("Sniper Sight", lambda l: l.LevelEntered(Levels.CreepyCastle)),
    ], [], []),

    "Candy": Region("Candy", False, [
        Location("Bongos", lambda l: l.LevelEntered(Levels.AngryAztec) and l.isdonkey),
        Location("Guitar", lambda l: l.LevelEntered(Levels.AngryAztec) and l.isdiddy),
        Location("Trombone", lambda l: l.LevelEntered(Levels.AngryAztec) and l.islanky),
        Location("Saxophone", lambda l: l.LevelEntered(Levels.AngryAztec) and l.istiny),
        Location("Triangle", lambda l: l.LevelEntered(Levels.AngryAztec) and l.ischunky),

        Location("Music Upgrade 1", lambda l: l.LevelEntered(Levels.GloomyGalleon)),
        Location("Third Melon", lambda l: l.LevelEntered(Levels.CrystalCaves)),
        Location("Music Upgrade 2", lambda l: l.LevelEntered(Levels.CreepyCastle)),
    ], [], []),

    "Cranky": Region("Cranky", False, [
        Location("Simian Slam", lambda l: True),
        Location("Super Simian Slam", lambda l: l.LevelEntered(Levels.FungiForest)),
        Location("Super Duper Simian Slam", lambda l: l.LevelEntered(Levels.CreepyCastle)),

        Location("Baboon Blast", lambda l: l.LevelEntered(Levels.JungleJapes) and l.isdonkey),
        Location("Strong Kong", lambda l: l.LevelEntered(Levels.AngryAztec) and l.isdonkey),
        Location("Gorilla Grab", lambda l: l.LevelEntered(Levels.FranticFactory) and l.isdonkey),

        Location("Chimpy Charge", lambda l: l.LevelEntered(Levels.JungleJapes) and l.isdiddy),
        Location("Rocketbarrel Boost", lambda l: l.LevelEntered(Levels.AngryAztec) and l.isdiddy),
        Location("Simian Spring", lambda l: l.LevelEntered(Levels.FranticFactory) and l.isdiddy),

        Location("Orangstand", lambda l: l.LevelEntered(Levels.JungleJapes) and l.islanky),
        Location("Baboon Balloon", lambda l: l.LevelEntered(Levels.FranticFactory) and l.islanky),
        Location("Orangstand Sprint", lambda l: l.LevelEntered(Levels.CrystalCaves) and l.islanky),

        Location("Mini Monkey", lambda l: l.LevelEntered(Levels.JungleJapes) and l.istiny),
        Location("Pony Tail Twirl", lambda l: l.LevelEntered(Levels.FranticFactory) and l.istiny),
        Location("Monkeyport", lambda l: l.LevelEntered(Levels.CrystalCaves) and l.istiny),

        Location("Hunky Chunky", lambda l: l.LevelEntered(Levels.JungleJapes) and l.ischunky),
        Location("Primate Punch", lambda l: l.LevelEntered(Levels.FranticFactory) and l.ischunky),
        Location("Gorilla Gone", lambda l: l.LevelEntered(Levels.CrystalCaves) and l.ischunky),
    ], [], []),

    "Snide": Region("Snide", False, [

    ], [], []),
}
