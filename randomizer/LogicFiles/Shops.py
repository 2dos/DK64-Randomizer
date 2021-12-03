# fmt: off
"""Logic file for shops."""

from randomizer.LogicClasses import Region, Location, Event, Exit
from randomizer.Enums.Items import Items
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Regions import Regions
from randomizer.Enums.Levels import Levels

LogicRegions = {
    Regions.Funky: Region("Funky", Levels.Shops, False, [
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

    Regions.Candy: Region("Candy", Levels.Shops, False, [
        Location("Bongos", lambda l: l.LevelEntered(Levels.AngryAztec) and l.isdonkey),
        Location("Guitar", lambda l: l.LevelEntered(Levels.AngryAztec) and l.isdiddy),
        Location("Trombone", lambda l: l.LevelEntered(Levels.AngryAztec) and l.islanky),
        Location("Saxophone", lambda l: l.LevelEntered(Levels.AngryAztec) and l.istiny),
        Location("Triangle", lambda l: l.LevelEntered(Levels.AngryAztec) and l.ischunky),

        Location("Music Upgrade 1", lambda l: l.LevelEntered(Levels.GloomyGalleon)),
        Location("Third Melon", lambda l: l.LevelEntered(Levels.CrystalCaves)),
        Location("Music Upgrade 2", lambda l: l.LevelEntered(Levels.CreepyCastle)),
    ], [], []),

    Regions.Cranky: Region("Cranky", Levels.Shops, False, [
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

        Location("Rareware Coin", lambda l: l.BananaMedals >= 5),
    ], [], []),

    Regions.Snide: Region("Snide", Levels.Shops, False, [
        Location("Turn In DK Isles Donkey Blueprint", lambda l: Items.DKIslesDonkeyBlueprint in l.Blueprints),
        Location("Turn In DK Isles Diddy Blueprint", lambda l: Items.DKIslesDiddyBlueprint in l.Blueprints),
        Location("Turn In DK Isles Lanky Blueprint", lambda l: Items.DKIslesLankyBlueprint in l.Blueprints),
        Location("Turn In DK Isles Tiny Blueprint", lambda l: Items.DKIslesTinyBlueprint in l.Blueprints),
        Location("Turn In DK Isles Chunky Blueprint", lambda l: Items.DKIslesChunkyBlueprint in l.Blueprints),

        Location("Turn In Jungle Japes Donkey Blueprint", lambda l: Items.JungleJapesDonkeyBlueprint in l.Blueprints),
        Location("Turn In Jungle Japes Diddy Blueprint", lambda l: Items.JungleJapesDiddyBlueprint in l.Blueprints),
        Location("Turn In Jungle Japes Lanky Blueprint", lambda l: Items.JungleJapesLankyBlueprint in l.Blueprints),
        Location("Turn In Jungle Japes Tiny Blueprint", lambda l: Items.JungleJapesTinyBlueprint in l.Blueprints),
        Location("Turn In Jungle Japes Chunky Blueprint", lambda l: Items.JungleJapesChunkyBlueprint in l.Blueprints),

        Location("Turn In Angry Aztec Donkey Blueprint", lambda l: Items.AngryAztecDonkeyBlueprint in l.Blueprints),
        Location("Turn In Angry Aztec Diddy Blueprint", lambda l: Items.AngryAztecDiddyBlueprint in l.Blueprints),
        Location("Turn In Angry Aztec Lanky Blueprint", lambda l: Items.AngryAztecLankyBlueprint in l.Blueprints),
        Location("Turn In Angry Aztec Tiny Blueprint", lambda l: Items.AngryAztecTinyBlueprint in l.Blueprints),
        Location("Turn In Angry Aztec Chunky Blueprint", lambda l: Items.AngryAztecChunkyBlueprint in l.Blueprints),

        Location("Turn In Frantic Factory Donkey Blueprint", lambda l: Items.FranticFactoryDonkeyBlueprint in l.Blueprints),
        Location("Turn In Frantic Factory Diddy Blueprint", lambda l: Items.FranticFactoryDiddyBlueprint in l.Blueprints),
        Location("Turn In Frantic Factory Lanky Blueprint", lambda l: Items.FranticFactoryLankyBlueprint in l.Blueprints),
        Location("Turn In Frantic Factory Tiny Blueprint", lambda l: Items.FranticFactoryTinyBlueprint in l.Blueprints),
        Location("Turn In Frantic Factory Chunky Blueprint", lambda l: Items.FranticFactoryChunkyBlueprint in l.Blueprints),

        Location("Turn In Gloomy Galleon Donkey Blueprint", lambda l: Items.GloomyGalleonDonkeyBlueprint in l.Blueprints),
        Location("Turn In Gloomy Galleon Diddy Blueprint", lambda l: Items.GloomyGalleonDiddyBlueprint in l.Blueprints),
        Location("Turn In Gloomy Galleon Lanky Blueprint", lambda l: Items.GloomyGalleonLankyBlueprint in l.Blueprints),
        Location("Turn In Gloomy Galleon Tiny Blueprint", lambda l: Items.GloomyGalleonTinyBlueprint in l.Blueprints),
        Location("Turn In Gloomy Galleon Chunky Blueprint", lambda l: Items.GloomyGalleonChunkyBlueprint in l.Blueprints),

        Location("Turn In Fungi Forest Donkey Blueprint", lambda l: Items.FungiForestDonkeyBlueprint in l.Blueprints),
        Location("Turn In Fungi Forest Diddy Blueprint", lambda l: Items.FungiForestDiddyBlueprint in l.Blueprints),
        Location("Turn In Fungi Forest Lanky Blueprint", lambda l: Items.FungiForestLankyBlueprint in l.Blueprints),
        Location("Turn In Fungi Forest Tiny Blueprint", lambda l: Items.FungiForestTinyBlueprint in l.Blueprints),
        Location("Turn In Fungi Forest Chunky Blueprint", lambda l: Items.FungiForestChunkyBlueprint in l.Blueprints),

        Location("Turn In Crystal Caves Donkey Blueprint", lambda l: Items.CrystalCavesDonkeyBlueprint in l.Blueprints),
        Location("Turn In Crystal Caves Diddy Blueprint", lambda l: Items.CrystalCavesDiddyBlueprint in l.Blueprints),
        Location("Turn In Crystal Caves Lanky Blueprint", lambda l: Items.CrystalCavesLankyBlueprint in l.Blueprints),
        Location("Turn In Crystal Caves Tiny Blueprint", lambda l: Items.CrystalCavesTinyBlueprint in l.Blueprints),
        Location("Turn In Crystal Caves Chunky Blueprint", lambda l: Items.CrystalCavesChunkyBlueprint in l.Blueprints),

        Location("Turn In Creepy Castle Donkey Blueprint", lambda l: Items.CreepyCastleDonkeyBlueprint in l.Blueprints),
        Location("Turn In Creepy Castle Diddy Blueprint", lambda l: Items.CreepyCastleDiddyBlueprint in l.Blueprints),
        Location("Turn In Creepy Castle Lanky Blueprint", lambda l: Items.CreepyCastleLankyBlueprint in l.Blueprints),
        Location("Turn In Creepy Castle Tiny Blueprint", lambda l: Items.CreepyCastleTinyBlueprint in l.Blueprints),
        Location("Turn In Creepy Castle Chunky Blueprint", lambda l: Items.CreepyCastleChunkyBlueprint in l.Blueprints),
    ], [], []),
}
