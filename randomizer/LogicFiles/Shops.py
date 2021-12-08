# fmt: off
"""Logic file for shops."""

from randomizer.Enums.Items import Items
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Regions import Regions
from randomizer.Enums.Locations import Locations
from randomizer.LogicClasses import Event, Exit, LocationLogic, Region

LogicRegions = {
    Regions.Funky: Region("Funky", Levels.Shops, False, [
        LocationLogic(Locations.CoconutGun, lambda l: l.LevelEntered(Levels.JungleJapes) and l.isdonkey),
        LocationLogic(Locations.PeanutGun, lambda l: l.LevelEntered(Levels.JungleJapes) and l.isdiddy),
        LocationLogic(Locations.GrapeGun, lambda l: l.LevelEntered(Levels.JungleJapes) and l.islanky),
        LocationLogic(Locations.FeatherGun, lambda l: l.LevelEntered(Levels.JungleJapes) and l.istiny),
        LocationLogic(Locations.PineappleGun, lambda l: l.LevelEntered(Levels.JungleJapes) and l.ischunky),

        LocationLogic(Locations.AmmoBelt1, lambda l: l.LevelEntered(Levels.FranticFactory)),
        LocationLogic(Locations.HomingAmmo, lambda l: l.LevelEntered(Levels.FungiForest)),
        LocationLogic(Locations.AmmoBelt2, lambda l: l.LevelEntered(Levels.CrystalCaves)),
        LocationLogic(Locations.SniperSight, lambda l: l.LevelEntered(Levels.CreepyCastle)),
    ], [], []),

    Regions.Candy: Region("Candy", Levels.Shops, False, [
        LocationLogic(Locations.Bongos, lambda l: l.LevelEntered(Levels.AngryAztec) and l.isdonkey),
        LocationLogic(Locations.Guitar, lambda l: l.LevelEntered(Levels.AngryAztec) and l.isdiddy),
        LocationLogic(Locations.Trombone, lambda l: l.LevelEntered(Levels.AngryAztec) and l.islanky),
        LocationLogic(Locations.Saxophone, lambda l: l.LevelEntered(Levels.AngryAztec) and l.istiny),
        LocationLogic(Locations.Triangle, lambda l: l.LevelEntered(Levels.AngryAztec) and l.ischunky),

        LocationLogic(Locations.MusicUpgrade1, lambda l: l.LevelEntered(Levels.GloomyGalleon)),
        LocationLogic(Locations.ThirdMelon, lambda l: l.LevelEntered(Levels.CrystalCaves)),
        LocationLogic(Locations.MusicUpgrade2, lambda l: l.LevelEntered(Levels.CreepyCastle)),
    ], [], []),

    Regions.Cranky: Region("Cranky", Levels.Shops, False, [
        LocationLogic(Locations.SimianSlam, lambda l: True),
        LocationLogic(Locations.SuperSimianSlam, lambda l: l.LevelEntered(Levels.FungiForest)),
        LocationLogic(Locations.SuperDuperSimianSlam, lambda l: l.LevelEntered(Levels.CreepyCastle)),

        LocationLogic(Locations.BaboonBlast, lambda l: l.LevelEntered(Levels.JungleJapes) and l.isdonkey),
        LocationLogic(Locations.StrongKong, lambda l: l.LevelEntered(Levels.AngryAztec) and l.isdonkey),
        LocationLogic(Locations.GorillaGrab, lambda l: l.LevelEntered(Levels.FranticFactory) and l.isdonkey),

        LocationLogic(Locations.ChimpyCharge, lambda l: l.LevelEntered(Levels.JungleJapes) and l.isdiddy),
        LocationLogic(Locations.RocketbarrelBoost, lambda l: l.LevelEntered(Levels.AngryAztec) and l.isdiddy),
        LocationLogic(Locations.SimianSpring, lambda l: l.LevelEntered(Levels.FranticFactory) and l.isdiddy),

        LocationLogic(Locations.Orangstand, lambda l: l.LevelEntered(Levels.JungleJapes) and l.islanky),
        LocationLogic(Locations.BaboonBalloon, lambda l: l.LevelEntered(Levels.FranticFactory) and l.islanky),
        LocationLogic(Locations.OrangstandSprint, lambda l: l.LevelEntered(Levels.CrystalCaves) and l.islanky),

        LocationLogic(Locations.MiniMonkey, lambda l: l.LevelEntered(Levels.JungleJapes) and l.istiny),
        LocationLogic(Locations.PonyTailTwirl, lambda l: l.LevelEntered(Levels.FranticFactory) and l.istiny),
        LocationLogic(Locations.Monkeyport, lambda l: l.LevelEntered(Levels.CrystalCaves) and l.istiny),

        LocationLogic(Locations.HunkyChunky, lambda l: l.LevelEntered(Levels.JungleJapes) and l.ischunky),
        LocationLogic(Locations.PrimatePunch, lambda l: l.LevelEntered(Levels.FranticFactory) and l.ischunky),
        LocationLogic(Locations.GorillaGone, lambda l: l.LevelEntered(Levels.CrystalCaves) and l.ischunky),

        LocationLogic(Locations.RarewareCoin, lambda l: l.BananaMedals >= 15),
    ], [], []),

    Regions.Snide: Region("Snide", Levels.Shops, False, [
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
