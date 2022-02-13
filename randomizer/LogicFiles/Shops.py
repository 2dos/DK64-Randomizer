# fmt: off
"""Logic file for shops."""

from randomizer.Enums.Items import Items
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Regions import Regions
from randomizer.LogicClasses import LocationLogic, Region, TransitionFront

"""
So for coin logic, we want to make sure the player can't spend coins incorrectly and lock themselves out.
This means every buyable item has to account for, potentially, buying every other possible item first.
So each price will be inflated by a lot for logic purposes.
Total prices are as follows:
Cranky generic: 12
Cranky specific: 15
Candy generic: 21
Candy specific: 3
Funky generic: 20
Funky specific: 3
Total one kong can possibly spend: 74
So basically, whatever "line" the kong is buying from, need to subtract prices
from future entries in that line from 74.
So since Cranky's upgrades cost 3, 5, and 7, the logical price of his
first upgrade will be 74 - 7 - 5 = 62.
"""

LogicRegions = {
    Regions.FunkyGeneric: Region("Funky Generic", Levels.Shops, False, None, [], [], [
        TransitionFront(Regions.FunkyJapes, lambda l: l.settings.shuffle_items == "none"),
        TransitionFront(Regions.FunkyFactory, lambda l: l.settings.shuffle_items == "none"),
        TransitionFront(Regions.FunkyForest, lambda l: l.settings.shuffle_items == "none"),
        TransitionFront(Regions.FunkyCaves, lambda l: l.settings.shuffle_items == "none"),
        TransitionFront(Regions.FunkyCastle, lambda l: l.settings.shuffle_items == "none"),
    ]),

    Regions.FunkyJapes: Region("Funky Japes", Levels.Shops, False, None, [
        LocationLogic(Locations.CoconutGun, lambda l: l.LevelEntered(Levels.JungleJapes) and l.isdonkey and l.Coins[Kongs.donkey] >= 54),
        LocationLogic(Locations.PeanutGun, lambda l: l.LevelEntered(Levels.JungleJapes) and l.isdiddy and l.Coins[Kongs.diddy] >= 54),
        LocationLogic(Locations.GrapeGun, lambda l: l.LevelEntered(Levels.JungleJapes) and l.islanky and l.Coins[Kongs.lanky] >= 54),
        LocationLogic(Locations.FeatherGun, lambda l: l.LevelEntered(Levels.JungleJapes) and l.istiny and l.Coins[Kongs.tiny] >= 54),
        LocationLogic(Locations.PineappleGun, lambda l: l.LevelEntered(Levels.JungleJapes) and l.ischunky and l.Coins[Kongs.chunky] >= 54),
    ], [], [
        TransitionFront(Regions.FunkyGeneric, lambda l: l.settings.shuffle_items == "none"),
    ]),

    Regions.FunkyFactory: Region("Funky Factory", Levels.Shops, False, None, [
        LocationLogic(Locations.AmmoBelt1, lambda l: l.LevelEntered(Levels.FranticFactory) and any(x >= 57 for x in l.Coins)),
    ], [], [
        TransitionFront(Regions.FunkyGeneric, lambda l: l.settings.shuffle_items == "none"),
    ]),

    Regions.FunkyForest: Region("Funky Forest", Levels.Shops, False, None, [
        LocationLogic(Locations.HomingAmmo, lambda l: l.LevelEntered(Levels.FungiForest) and any(x >= 62 for x in l.Coins)),
    ], [], [
        TransitionFront(Regions.FunkyGeneric, lambda l: l.settings.shuffle_items == "none"),
    ]),

    Regions.FunkyCaves: Region("Funky Caves", Levels.Shops, False, None, [
        LocationLogic(Locations.AmmoBelt2, lambda l: l.LevelEntered(Levels.CrystalCaves) and any(x >= 67 for x in l.Coins)),
    ], [], [
        TransitionFront(Regions.FunkyGeneric, lambda l: l.settings.shuffle_items == "none"),
    ]),

    Regions.FunkyCastle: Region("Funky Castle", Levels.Shops, False, None, [
        # Sniper sight is the only non-Snide shop location not zeroed out when starting with all shop moves.
        LocationLogic(Locations.SniperSight, lambda l: l.LevelEntered(Levels.CreepyCastle)
                      and (any(x >= 74 for x in l.Coins) or (l.settings.unlock_all_moves and any(x >= 7 for x in l.Coins)))),
    ], [], [
        TransitionFront(Regions.FunkyGeneric, lambda l: l.settings.shuffle_items == "none"),
    ]),

    Regions.CandyGeneric: Region("Candy Generic", Levels.Shops, False, None, [], [], [
        TransitionFront(Regions.CandyAztec, lambda l: l.settings.shuffle_items == "none"),
        TransitionFront(Regions.CandyGalleon, lambda l: l.settings.shuffle_items == "none"),
        TransitionFront(Regions.CandyCaves, lambda l: l.settings.shuffle_items == "none"),
        TransitionFront(Regions.CandyCastle, lambda l: l.settings.shuffle_items == "none"),
    ]),

    Regions.CandyAztec: Region("Candy Aztec", Levels.Shops, False, None, [
        LocationLogic(Locations.Bongos, lambda l: l.LevelEntered(Levels.AngryAztec) and l.isdonkey and l.Coins[Kongs.donkey] >= 53),
        LocationLogic(Locations.Guitar, lambda l: l.LevelEntered(Levels.AngryAztec) and l.isdiddy and l.Coins[Kongs.diddy] >= 53),
        LocationLogic(Locations.Trombone, lambda l: l.LevelEntered(Levels.AngryAztec) and l.islanky and l.Coins[Kongs.lanky] >= 53),
        LocationLogic(Locations.Saxophone, lambda l: l.LevelEntered(Levels.AngryAztec) and l.istiny and l.Coins[Kongs.tiny] >= 53),
        LocationLogic(Locations.Triangle, lambda l: l.LevelEntered(Levels.AngryAztec) and l.ischunky and l.Coins[Kongs.chunky] >= 53),
    ], [], [
        TransitionFront(Regions.CandyGeneric, lambda l: l.settings.shuffle_items == "none"),
    ]),

    Regions.CandyGalleon: Region("Candy Galleon", Levels.Shops, False, None, [
        LocationLogic(Locations.MusicUpgrade1, lambda l: l.LevelEntered(Levels.GloomyGalleon) and any(x >= 58 for x in l.Coins)),
    ], [], [
        TransitionFront(Regions.CandyGeneric, lambda l: l.settings.shuffle_items == "none"),
    ]),

    Regions.CandyCaves: Region("Candy Caves", Levels.Shops, False, None, [
        LocationLogic(Locations.ThirdMelon, lambda l: l.LevelEntered(Levels.CrystalCaves) and any(x >= 65 for x in l.Coins)),
    ], [], [
        TransitionFront(Regions.CandyGeneric, lambda l: l.settings.shuffle_items == "none"),
    ]),

    Regions.CandyCastle: Region("Candy Castle", Levels.Shops, False, None, [
        LocationLogic(Locations.MusicUpgrade2, lambda l: l.LevelEntered(Levels.CreepyCastle) and any(x >= 57 for x in l.Coins)),
    ], [], [
        TransitionFront(Regions.CandyGeneric, lambda l: l.settings.shuffle_items == "none"),
    ]),

    Regions.CrankyGeneric: Region("Cranky Generic", Levels.Shops, False, None, [
        LocationLogic(Locations.SimianSlam, lambda l: True),
        LocationLogic(Locations.RarewareCoin, lambda l: l.BananaMedals >= 15),
    ], [], [
        TransitionFront(Regions.CrankyJapes, lambda l: l.settings.shuffle_items == "none"),
        TransitionFront(Regions.CrankyAztec, lambda l: l.settings.shuffle_items == "none"),
        TransitionFront(Regions.CrankyFactory, lambda l: l.settings.shuffle_items == "none"),
        TransitionFront(Regions.CrankyForest, lambda l: l.settings.shuffle_items == "none"),
        TransitionFront(Regions.CrankyCaves, lambda l: l.settings.shuffle_items == "none"),
        TransitionFront(Regions.CrankyCastle, lambda l: l.settings.shuffle_items == "none"),
    ]),

    Regions.CrankyJapes: Region("Cranky Japes", Levels.Shops, False, None, [
        LocationLogic(Locations.BaboonBlast, lambda l: l.LevelEntered(Levels.JungleJapes) and l.isdonkey and l.Coins[Kongs.donkey] >= 62),
        LocationLogic(Locations.ChimpyCharge, lambda l: l.LevelEntered(Levels.JungleJapes) and l.isdiddy and l.Coins[Kongs.diddy] >= 62),
        LocationLogic(Locations.Orangstand, lambda l: l.LevelEntered(Levels.JungleJapes) and l.islanky and l.Coins[Kongs.lanky] >= 62),
        LocationLogic(Locations.MiniMonkey, lambda l: l.LevelEntered(Levels.JungleJapes) and l.istiny and l.Coins[Kongs.tiny] >= 62),
        LocationLogic(Locations.HunkyChunky, lambda l: l.LevelEntered(Levels.JungleJapes) and l.ischunky and l.Coins[Kongs.chunky] >= 62),
    ], [], [
        TransitionFront(Regions.CrankyGeneric, lambda l: True),
    ]),

    Regions.CrankyAztec: Region("Cranky Aztec", Levels.Shops, False, None, [
        LocationLogic(Locations.StrongKong, lambda l: l.LevelEntered(Levels.AngryAztec) and l.isdonkey and l.Coins[Kongs.donkey] >= 67),
        LocationLogic(Locations.RocketbarrelBoost, lambda l: l.LevelEntered(Levels.AngryAztec) and l.isdiddy and l.Coins[Kongs.diddy] >= 67),
    ], [], [
        TransitionFront(Regions.CrankyGeneric, lambda l: True),
    ]),

    Regions.CrankyFactory: Region("Cranky Factory", Levels.Shops, False, None, [
        LocationLogic(Locations.GorillaGrab, lambda l: l.LevelEntered(Levels.FranticFactory) and l.isdonkey and l.Coins[Kongs.donkey] >= 74),
        LocationLogic(Locations.SimianSpring, lambda l: l.LevelEntered(Levels.FranticFactory) and l.isdiddy and l.Coins[Kongs.diddy] >= 74),
        LocationLogic(Locations.BaboonBalloon, lambda l: l.LevelEntered(Levels.FranticFactory) and l.islanky and l.Coins[Kongs.lanky] >= 67),
        LocationLogic(Locations.PonyTailTwirl, lambda l: l.LevelEntered(Levels.FranticFactory) and l.istiny and l.Coins[Kongs.tiny] >= 67),
        LocationLogic(Locations.PrimatePunch, lambda l: l.LevelEntered(Levels.FranticFactory) and l.ischunky and l.Coins[Kongs.chunky] >= 67),
    ], [], [
        TransitionFront(Regions.CrankyGeneric, lambda l: True),
    ]),

    Regions.CrankyForest: Region("Cranky Forest", Levels.Shops, False, None, [
        LocationLogic(Locations.SuperSimianSlam, lambda l: l.LevelEntered(Levels.FungiForest) and any(x >= 67 for x in l.Coins)),
    ], [], [
        TransitionFront(Regions.CrankyGeneric, lambda l: True),
    ]),

    Regions.CrankyCaves: Region("Cranky Caves", Levels.Shops, False, None, [
        LocationLogic(Locations.OrangstandSprint, lambda l: l.LevelEntered(Levels.CrystalCaves) and l.islanky and l.Coins[Kongs.lanky] >= 74),
        LocationLogic(Locations.Monkeyport, lambda l: l.LevelEntered(Levels.CrystalCaves) and l.istiny and l.Coins[Kongs.tiny] >= 74),
        LocationLogic(Locations.GorillaGone, lambda l: l.LevelEntered(Levels.CrystalCaves) and l.ischunky and l.Coins[Kongs.chunky] >= 74),
    ], [], [
        TransitionFront(Regions.CrankyGeneric, lambda l: True),
    ]),

    Regions.CrankyCastle: Region("Cranky Castle", Levels.Shops, False, None, [
        LocationLogic(Locations.SuperDuperSimianSlam, lambda l: l.LevelEntered(Levels.CreepyCastle) and any(x >= 74 for x in l.Coins)),
    ], [], [
        TransitionFront(Regions.CrankyGeneric, lambda l: True),
    ]),

    Regions.Snide: Region("Snide", Levels.Shops, False, None, [
        LocationLogic(Locations.TurnInDKIslesDonkeyBlueprint, lambda l: Items.DKIslesDonkeyBlueprint in l.Blueprints),
        LocationLogic(Locations.TurnInDKIslesDiddyBlueprint, lambda l: Items.DKIslesDiddyBlueprint in l.Blueprints),
        LocationLogic(Locations.TurnInDKIslesLankyBlueprint, lambda l: Items.DKIslesLankyBlueprint in l.Blueprints),
        LocationLogic(Locations.TurnInDKIslesTinyBlueprint, lambda l: Items.DKIslesTinyBlueprint in l.Blueprints),
        LocationLogic(Locations.TurnInDKIslesChunkyBlueprint, lambda l: Items.DKIslesChunkyBlueprint in l.Blueprints),

        LocationLogic(Locations.TurnInJungleJapesDonkeyBlueprint, lambda l: Items.JungleJapesDonkeyBlueprint in l.Blueprints),
        LocationLogic(Locations.TurnInJungleJapesDiddyBlueprint, lambda l: Items.JungleJapesDiddyBlueprint in l.Blueprints),
        LocationLogic(Locations.TurnInJungleJapesLankyBlueprint, lambda l: Items.JungleJapesLankyBlueprint in l.Blueprints),
        LocationLogic(Locations.TurnInJungleJapesTinyBlueprint, lambda l: Items.JungleJapesTinyBlueprint in l.Blueprints),
        LocationLogic(Locations.TurnInJungleJapesChunkyBlueprint, lambda l: Items.JungleJapesChunkyBlueprint in l.Blueprints),

        LocationLogic(Locations.TurnInAngryAztecDonkeyBlueprint, lambda l: Items.AngryAztecDonkeyBlueprint in l.Blueprints),
        LocationLogic(Locations.TurnInAngryAztecDiddyBlueprint, lambda l: Items.AngryAztecDiddyBlueprint in l.Blueprints),
        LocationLogic(Locations.TurnInAngryAztecLankyBlueprint, lambda l: Items.AngryAztecLankyBlueprint in l.Blueprints),
        LocationLogic(Locations.TurnInAngryAztecTinyBlueprint, lambda l: Items.AngryAztecTinyBlueprint in l.Blueprints),
        LocationLogic(Locations.TurnInAngryAztecChunkyBlueprint, lambda l: Items.AngryAztecChunkyBlueprint in l.Blueprints),

        LocationLogic(Locations.TurnInFranticFactoryDonkeyBlueprint, lambda l: Items.FranticFactoryDonkeyBlueprint in l.Blueprints),
        LocationLogic(Locations.TurnInFranticFactoryDiddyBlueprint, lambda l: Items.FranticFactoryDiddyBlueprint in l.Blueprints),
        LocationLogic(Locations.TurnInFranticFactoryLankyBlueprint, lambda l: Items.FranticFactoryLankyBlueprint in l.Blueprints),
        LocationLogic(Locations.TurnInFranticFactoryTinyBlueprint, lambda l: Items.FranticFactoryTinyBlueprint in l.Blueprints),
        LocationLogic(Locations.TurnInFranticFactoryChunkyBlueprint, lambda l: Items.FranticFactoryChunkyBlueprint in l.Blueprints),

        LocationLogic(Locations.TurnInGloomyGalleonDonkeyBlueprint, lambda l: Items.GloomyGalleonDonkeyBlueprint in l.Blueprints),
        LocationLogic(Locations.TurnInGloomyGalleonDiddyBlueprint, lambda l: Items.GloomyGalleonDiddyBlueprint in l.Blueprints),
        LocationLogic(Locations.TurnInGloomyGalleonLankyBlueprint, lambda l: Items.GloomyGalleonLankyBlueprint in l.Blueprints),
        LocationLogic(Locations.TurnInGloomyGalleonTinyBlueprint, lambda l: Items.GloomyGalleonTinyBlueprint in l.Blueprints),
        LocationLogic(Locations.TurnInGloomyGalleonChunkyBlueprint, lambda l: Items.GloomyGalleonChunkyBlueprint in l.Blueprints),

        LocationLogic(Locations.TurnInFungiForestDonkeyBlueprint, lambda l: Items.FungiForestDonkeyBlueprint in l.Blueprints),
        LocationLogic(Locations.TurnInFungiForestDiddyBlueprint, lambda l: Items.FungiForestDiddyBlueprint in l.Blueprints),
        LocationLogic(Locations.TurnInFungiForestLankyBlueprint, lambda l: Items.FungiForestLankyBlueprint in l.Blueprints),
        LocationLogic(Locations.TurnInFungiForestTinyBlueprint, lambda l: Items.FungiForestTinyBlueprint in l.Blueprints),
        LocationLogic(Locations.TurnInFungiForestChunkyBlueprint, lambda l: Items.FungiForestChunkyBlueprint in l.Blueprints),

        LocationLogic(Locations.TurnInCrystalCavesDonkeyBlueprint, lambda l: Items.CrystalCavesDonkeyBlueprint in l.Blueprints),
        LocationLogic(Locations.TurnInCrystalCavesDiddyBlueprint, lambda l: Items.CrystalCavesDiddyBlueprint in l.Blueprints),
        LocationLogic(Locations.TurnInCrystalCavesLankyBlueprint, lambda l: Items.CrystalCavesLankyBlueprint in l.Blueprints),
        LocationLogic(Locations.TurnInCrystalCavesTinyBlueprint, lambda l: Items.CrystalCavesTinyBlueprint in l.Blueprints),
        LocationLogic(Locations.TurnInCrystalCavesChunkyBlueprint, lambda l: Items.CrystalCavesChunkyBlueprint in l.Blueprints),

        LocationLogic(Locations.TurnInCreepyCastleDonkeyBlueprint, lambda l: Items.CreepyCastleDonkeyBlueprint in l.Blueprints),
        LocationLogic(Locations.TurnInCreepyCastleDiddyBlueprint, lambda l: Items.CreepyCastleDiddyBlueprint in l.Blueprints),
        LocationLogic(Locations.TurnInCreepyCastleLankyBlueprint, lambda l: Items.CreepyCastleLankyBlueprint in l.Blueprints),
        LocationLogic(Locations.TurnInCreepyCastleTinyBlueprint, lambda l: Items.CreepyCastleTinyBlueprint in l.Blueprints),
        LocationLogic(Locations.TurnInCreepyCastleChunkyBlueprint, lambda l: Items.CreepyCastleChunkyBlueprint in l.Blueprints),
    ], [], []),
}
