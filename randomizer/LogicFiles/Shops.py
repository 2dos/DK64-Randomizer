# fmt: off
"""Logic file for shops."""

from randomizer.Enums.Items import Items
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Regions import Regions
from randomizer.Lists.Location import Location
from randomizer.LogicClasses import LocationLogic, Region, TransitionFront

LogicRegions = {
    Regions.FunkyGeneric: Region("Funky Generic", Levels.Shops, False, None, [], [], [
        TransitionFront(Regions.FunkyJapes, lambda l: False),
        TransitionFront(Regions.FunkyFactory, lambda l: False),
        TransitionFront(Regions.FunkyForest, lambda l: False),
        TransitionFront(Regions.FunkyCaves, lambda l: False),
        TransitionFront(Regions.FunkyCastle, lambda l: False),
    ]),

    Regions.FunkyJapes: Region("Funky Japes", Levels.Shops, False, None, [
        LocationLogic(Locations.SharedJapesGun, lambda l: l.LevelEntered(Levels.JungleJapes) and l.CanBuy(Locations.SharedJapesGun)),
        LocationLogic(Locations.CoconutGun, lambda l: l.LevelEntered(Levels.JungleJapes) and l.isdonkey and l.CanBuy(Locations.CoconutGun)),
        LocationLogic(Locations.PeanutGun, lambda l: l.LevelEntered(Levels.JungleJapes) and l.isdiddy and l.CanBuy(Locations.PeanutGun)),
        LocationLogic(Locations.GrapeGun, lambda l: l.LevelEntered(Levels.JungleJapes) and l.islanky and l.CanBuy(Locations.GrapeGun)),
        LocationLogic(Locations.FeatherGun, lambda l: l.LevelEntered(Levels.JungleJapes) and l.istiny and l.CanBuy(Locations.FeatherGun)),
        LocationLogic(Locations.PineappleGun, lambda l: l.LevelEntered(Levels.JungleJapes) and l.ischunky and l.CanBuy(Locations.PineappleGun)),
    ], [], [
        TransitionFront(Regions.FunkyGeneric, lambda l: False),
    ]),

    Regions.FunkyAztec: Region("Funky Aztec", Levels.Shops, False, None, [
        LocationLogic(Locations.SharedAztecGun, lambda l: l.LevelEntered(Levels.AngryAztec) and l.CanBuy(Locations.SharedAztecGun)),
        LocationLogic(Locations.DonkeyAztecGun, lambda l: l.LevelEntered(Levels.AngryAztec) and l.isdonkey and l.CanBuy(Locations.DonkeyAztecGun)),
        LocationLogic(Locations.DiddyAztecGun, lambda l: l.LevelEntered(Levels.AngryAztec) and l.isdiddy and l.CanBuy(Locations.DiddyAztecGun)),
        LocationLogic(Locations.LankyAztecGun, lambda l: l.LevelEntered(Levels.AngryAztec) and l.islanky and l.CanBuy(Locations.LankyAztecGun)),
        LocationLogic(Locations.TinyAztecGun, lambda l: l.LevelEntered(Levels.AngryAztec) and l.istiny and l.CanBuy(Locations.TinyAztecGun)),
        LocationLogic(Locations.ChunkyAztecGun, lambda l: l.LevelEntered(Levels.AngryAztec) and l.ischunky and l.CanBuy(Locations.ChunkyAztecGun)),
    ], [], [
        TransitionFront(Regions.FunkyGeneric, lambda l: False),
    ]),

    Regions.FunkyFactory: Region("Funky Factory", Levels.Shops, False, None, [
        LocationLogic(Locations.AmmoBelt1, lambda l: l.LevelEntered(Levels.FranticFactory) and l.CanBuy(Locations.AmmoBelt1)),
        LocationLogic(Locations.DonkeyFactoryGun, lambda l: l.LevelEntered(Levels.FranticFactory) and l.isdonkey and l.CanBuy(Locations.DonkeyFactoryGun)),
        LocationLogic(Locations.DiddyFactoryGun, lambda l: l.LevelEntered(Levels.FranticFactory) and l.isdiddy and l.CanBuy(Locations.DiddyFactoryGun)),
        LocationLogic(Locations.LankyFactoryGun, lambda l: l.LevelEntered(Levels.FranticFactory) and l.islanky and l.CanBuy(Locations.LankyFactoryGun)),
        LocationLogic(Locations.TinyFactoryGun, lambda l: l.LevelEntered(Levels.FranticFactory) and l.istiny and l.CanBuy(Locations.TinyFactoryGun)),
        LocationLogic(Locations.ChunkyFactoryGun, lambda l: l.LevelEntered(Levels.FranticFactory) and l.ischunky and l.CanBuy(Locations.ChunkyFactoryGun)),
    ], [], [
        TransitionFront(Regions.FunkyGeneric, lambda l: False),
    ]),

    Regions.FunkyGalleon: Region("Funky Galleon", Levels.Shops, False, None, [
        LocationLogic(Locations.SharedGalleonGun, lambda l: l.LevelEntered(Levels.GloomyGalleon) and l.CanBuy(Locations.SharedGalleonGun)),
        LocationLogic(Locations.DonkeyGalleonGun, lambda l: l.LevelEntered(Levels.GloomyGalleon) and l.isdonkey and l.CanBuy(Locations.DonkeyGalleonGun)),
        LocationLogic(Locations.DiddyGalleonGun, lambda l: l.LevelEntered(Levels.GloomyGalleon) and l.isdiddy and l.CanBuy(Locations.DiddyGalleonGun)),
        LocationLogic(Locations.LankyGalleonGun, lambda l: l.LevelEntered(Levels.GloomyGalleon) and l.islanky and l.CanBuy(Locations.LankyGalleonGun)),
        LocationLogic(Locations.TinyGalleonGun, lambda l: l.LevelEntered(Levels.GloomyGalleon) and l.istiny and l.CanBuy(Locations.TinyGalleonGun)),
        LocationLogic(Locations.ChunkyGalleonGun, lambda l: l.LevelEntered(Levels.GloomyGalleon) and l.ischunky and l.CanBuy(Locations.ChunkyGalleonGun)),
    ], [], [
        TransitionFront(Regions.FunkyGeneric, lambda l: False),
    ]),

    Regions.FunkyForest: Region("Funky Forest", Levels.Shops, False, None, [
        LocationLogic(Locations.HomingAmmo, lambda l: l.LevelEntered(Levels.FungiForest) and l.CanBuy(Locations.HomingAmmo)),
        LocationLogic(Locations.DonkeyForestGun, lambda l: l.LevelEntered(Levels.FungiForest) and l.isdonkey and l.CanBuy(Locations.DonkeyForestGun)),
        LocationLogic(Locations.DiddyForestGun, lambda l: l.LevelEntered(Levels.FungiForest) and l.isdiddy and l.CanBuy(Locations.DiddyForestGun)),
        LocationLogic(Locations.LankyForestGun, lambda l: l.LevelEntered(Levels.FungiForest) and l.islanky and l.CanBuy(Locations.LankyForestGun)),
        LocationLogic(Locations.TinyForestGun, lambda l: l.LevelEntered(Levels.FungiForest) and l.istiny and l.CanBuy(Locations.TinyForestGun)),
        LocationLogic(Locations.ChunkyForestGun, lambda l: l.LevelEntered(Levels.FungiForest) and l.ischunky and l.CanBuy(Locations.ChunkyForestGun)),
    ], [], [
        TransitionFront(Regions.FunkyGeneric, lambda l: False),
    ]),

    Regions.FunkyCaves: Region("Funky Caves", Levels.Shops, False, None, [
        LocationLogic(Locations.AmmoBelt2, lambda l: l.LevelEntered(Levels.CrystalCaves) and l.CanBuy(Locations.AmmoBelt2)),
        LocationLogic(Locations.DonkeyCavesGun, lambda l: l.LevelEntered(Levels.CrystalCaves) and l.isdonkey and l.CanBuy(Locations.DonkeyCavesGun)),
        LocationLogic(Locations.DiddyCavesGun, lambda l: l.LevelEntered(Levels.CrystalCaves) and l.isdiddy and l.CanBuy(Locations.DiddyCavesGun)),
        LocationLogic(Locations.LankyCavesGun, lambda l: l.LevelEntered(Levels.CrystalCaves) and l.islanky and l.CanBuy(Locations.LankyCavesGun)),
        LocationLogic(Locations.TinyCavesGun, lambda l: l.LevelEntered(Levels.CrystalCaves) and l.istiny and l.CanBuy(Locations.TinyCavesGun)),
        LocationLogic(Locations.ChunkyCavesGun, lambda l: l.LevelEntered(Levels.CrystalCaves) and l.ischunky and l.CanBuy(Locations.ChunkyCavesGun)),
    ], [], [
        TransitionFront(Regions.FunkyGeneric, lambda l: False),
    ]),

    Regions.FunkyCastle: Region("Funky Castle", Levels.Shops, False, None, [
        LocationLogic(Locations.SniperSight, lambda l: l.LevelEntered(Levels.CreepyCastle) and l.CanBuy(Locations.SniperSight)),
        LocationLogic(Locations.DonkeyCastleGun, lambda l: l.LevelEntered(Levels.CreepyCastle) and l.isdonkey and l.CanBuy(Locations.DonkeyCastleGun)),
        LocationLogic(Locations.DiddyCastleGun, lambda l: l.LevelEntered(Levels.CreepyCastle) and l.isdiddy and l.CanBuy(Locations.DiddyCavesGun)),
        LocationLogic(Locations.LankyCastleGun, lambda l: l.LevelEntered(Levels.CreepyCastle) and l.islanky and l.CanBuy(Locations.LankyCastleGun)),
        LocationLogic(Locations.TinyCastleGun, lambda l: l.LevelEntered(Levels.CreepyCastle) and l.istiny and l.CanBuy(Locations.TinyCastleGun)),
        LocationLogic(Locations.ChunkyCastleGun, lambda l: l.LevelEntered(Levels.CreepyCastle) and l.ischunky and l.CanBuy(Locations.ChunkyCastleGun)),
    ], [], [
        TransitionFront(Regions.FunkyGeneric, lambda l: False),
    ]),

    Regions.CandyGeneric: Region("Candy Generic", Levels.Shops, False, None, [], [], [
        TransitionFront(Regions.CandyAztec, lambda l: False),
        TransitionFront(Regions.CandyGalleon, lambda l: False),
        TransitionFront(Regions.CandyCaves, lambda l: False),
        TransitionFront(Regions.CandyCastle, lambda l: False),
    ]),

    Regions.CandyAztec: Region("Candy Aztec", Levels.Shops, False, None, [
        LocationLogic(Locations.SharedAztecInstrument, lambda l: l.LevelEntered(Levels.AngryAztec) and l.CanBuy(Locations.SharedAztecInstrument)),
        LocationLogic(Locations.Bongos, lambda l: l.LevelEntered(Levels.AngryAztec) and l.isdonkey and l.CanBuy(Locations.Bongos)),
        LocationLogic(Locations.Guitar, lambda l: l.LevelEntered(Levels.AngryAztec) and l.isdiddy and l.CanBuy(Locations.Guitar)),
        LocationLogic(Locations.Trombone, lambda l: l.LevelEntered(Levels.AngryAztec) and l.islanky and l.CanBuy(Locations.Trombone)),
        LocationLogic(Locations.Saxophone, lambda l: l.LevelEntered(Levels.AngryAztec) and l.istiny and l.CanBuy(Locations.Saxophone)),
        LocationLogic(Locations.Triangle, lambda l: l.LevelEntered(Levels.AngryAztec) and l.ischunky and l.CanBuy(Locations.Triangle)),
    ], [], [
        TransitionFront(Regions.CandyGeneric, lambda l: False),
    ]),

    Regions.CandyFactory: Region("Candy Factory", Levels.Shops, False, None, [
        LocationLogic(Locations.SharedFactoryInstrument, lambda l: l.LevelEntered(Levels.FranticFactory) and l.CanBuy(Locations.SharedFactoryInstrument)),
        LocationLogic(Locations.DonkeyFactoryInstrument, lambda l: l.LevelEntered(Levels.FranticFactory) and l.isdonkey and l.CanBuy(Locations.DonkeyFactoryInstrument)),
        LocationLogic(Locations.DiddyFactoryInstrument, lambda l: l.LevelEntered(Levels.FranticFactory) and l.isdiddy and l.CanBuy(Locations.DiddyFactoryInstrument)),
        LocationLogic(Locations.LankyFactoryInstrument, lambda l: l.LevelEntered(Levels.FranticFactory) and l.islanky and l.CanBuy(Locations.LankyFactoryInstrument)),
        LocationLogic(Locations.TinyFactoryInstrument, lambda l: l.LevelEntered(Levels.FranticFactory) and l.istiny and l.CanBuy(Locations.TinyFactoryInstrument)),
        LocationLogic(Locations.ChunkyFactoryInstrument, lambda l: l.LevelEntered(Levels.FranticFactory) and l.ischunky and l.CanBuy(Locations.ChunkyFactoryInstrument)),
    ], [], [
        TransitionFront(Regions.CandyGeneric, lambda l: False),
    ]),

    Regions.CandyGalleon: Region("Candy Galleon", Levels.Shops, False, None, [
        LocationLogic(Locations.MusicUpgrade1, lambda l: l.LevelEntered(Levels.GloomyGalleon) and l.CanBuy(Locations.MusicUpgrade1)),
        LocationLogic(Locations.DonkeyGalleonInstrument, lambda l: l.LevelEntered(Levels.GloomyGalleon) and l.isdonkey and l.CanBuy(Locations.DonkeyGalleonInstrument)),
        LocationLogic(Locations.DiddyGalleonInstrument, lambda l: l.LevelEntered(Levels.GloomyGalleon) and l.isdiddy and l.CanBuy(Locations.DiddyGalleonInstrument)),
        LocationLogic(Locations.LankyGalleonInstrument, lambda l: l.LevelEntered(Levels.GloomyGalleon) and l.islanky and l.CanBuy(Locations.LankyGalleonInstrument)),
        LocationLogic(Locations.TinyGalleonInstrument, lambda l: l.LevelEntered(Levels.GloomyGalleon) and l.istiny and l.CanBuy(Locations.TinyGalleonInstrument)),
        LocationLogic(Locations.ChunkyGalleonInstrument, lambda l: l.LevelEntered(Levels.GloomyGalleon) and l.ischunky and l.CanBuy(Locations.ChunkyGalleonInstrument)),
    ], [], [
        TransitionFront(Regions.CandyGeneric, lambda l: False),
    ]),

    Regions.CandyCaves: Region("Candy Caves", Levels.Shops, False, None, [
        LocationLogic(Locations.ThirdMelon, lambda l: l.LevelEntered(Levels.CrystalCaves) and l.CanBuy(Locations.ThirdMelon)),
        LocationLogic(Locations.DonkeyCavesInstrument, lambda l: l.LevelEntered(Levels.CrystalCaves) and l.isdonkey and l.CanBuy(Locations.DonkeyCavesInstrument)),
        LocationLogic(Locations.DiddyCavesInstrument, lambda l: l.LevelEntered(Levels.CrystalCaves) and l.isdiddy and l.CanBuy(Locations.DiddyCavesInstrument)),
        LocationLogic(Locations.LankyCavesInstrument, lambda l: l.LevelEntered(Levels.CrystalCaves) and l.islanky and l.CanBuy(Locations.LankyCavesInstrument)),
        LocationLogic(Locations.TinyCavesInstrument, lambda l: l.LevelEntered(Levels.CrystalCaves) and l.istiny and l.CanBuy(Locations.TinyCavesInstrument)),
        LocationLogic(Locations.ChunkyCavesInstrument, lambda l: l.LevelEntered(Levels.CrystalCaves) and l.ischunky and l.CanBuy(Locations.ChunkyCavesInstrument)),
    ], [], [
        TransitionFront(Regions.CandyGeneric, lambda l: False),
    ]),

    Regions.CandyCastle: Region("Candy Castle", Levels.Shops, False, None, [
        LocationLogic(Locations.MusicUpgrade2, lambda l: l.LevelEntered(Levels.CreepyCastle) and l.CanBuy(Locations.MusicUpgrade2)),
        LocationLogic(Locations.DonkeyCastleInstrument, lambda l: l.LevelEntered(Levels.CreepyCastle) and l.isdonkey and l.CanBuy(Locations.DonkeyCastleInstrument)),
        LocationLogic(Locations.DiddyCastleInstrument, lambda l: l.LevelEntered(Levels.CreepyCastle) and l.isdiddy and l.CanBuy(Locations.DiddyCastleInstrument)),
        LocationLogic(Locations.LankyCastleInstrument, lambda l: l.LevelEntered(Levels.CreepyCastle) and l.islanky and l.CanBuy(Locations.LankyCastleInstrument)),
        LocationLogic(Locations.TinyCastleInstrument, lambda l: l.LevelEntered(Levels.CreepyCastle) and l.istiny and l.CanBuy(Locations.TinyCastleInstrument)),
        LocationLogic(Locations.ChunkyCastleInstrument, lambda l: l.LevelEntered(Levels.CreepyCastle) and l.ischunky and l.CanBuy(Locations.ChunkyCastleInstrument)),
    ], [], [
        TransitionFront(Regions.CandyGeneric, lambda l: False),
    ]),

    Regions.CrankyGeneric: Region("Cranky Generic", Levels.Shops, False, None, [
        LocationLogic(Locations.SimianSlam, lambda l: True),
        LocationLogic(Locations.RarewareCoin, lambda l: l.BananaMedals >= l.settings.BananaMedalsRequired),
    ], [], [
        TransitionFront(Regions.CrankyJapes, lambda l: False),
        TransitionFront(Regions.CrankyAztec, lambda l: False),
        TransitionFront(Regions.CrankyFactory, lambda l: False),
        TransitionFront(Regions.CrankyForest, lambda l: False),
        TransitionFront(Regions.CrankyCaves, lambda l: False),
        TransitionFront(Regions.CrankyCastle, lambda l: False),
    ]),

    Regions.CrankyJapes: Region("Cranky Japes", Levels.Shops, False, None, [
        LocationLogic(Locations.SharedJapesPotion, lambda l: l.LevelEntered(Levels.JungleJapes) and l.CanBuy(Locations.SharedJapesPotion)),
        LocationLogic(Locations.BaboonBlast, lambda l: l.LevelEntered(Levels.JungleJapes) and l.isdonkey and l.CanBuy(Locations.BaboonBlast)),
        LocationLogic(Locations.ChimpyCharge, lambda l: l.LevelEntered(Levels.JungleJapes) and l.isdiddy and l.CanBuy(Locations.ChimpyCharge)),
        LocationLogic(Locations.Orangstand, lambda l: l.LevelEntered(Levels.JungleJapes) and l.islanky and l.CanBuy(Locations.Orangstand)),
        LocationLogic(Locations.MiniMonkey, lambda l: l.LevelEntered(Levels.JungleJapes) and l.istiny and l.CanBuy(Locations.MiniMonkey)),
        LocationLogic(Locations.HunkyChunky, lambda l: l.LevelEntered(Levels.JungleJapes) and l.ischunky and l.CanBuy(Locations.HunkyChunky)),
    ], [], [
        TransitionFront(Regions.CrankyGeneric, lambda l: True),
    ]),

    Regions.CrankyAztec: Region("Cranky Aztec", Levels.Shops, False, None, [
        LocationLogic(Locations.SharedAztecPotion, lambda l: l.LevelEntered(Levels.AngryAztec) and l.CanBuy(Locations.SharedAztecPotion)),
        LocationLogic(Locations.StrongKong, lambda l: l.LevelEntered(Levels.AngryAztec) and l.isdonkey and l.CanBuy(Locations.StrongKong)),
        LocationLogic(Locations.RocketbarrelBoost, lambda l: l.LevelEntered(Levels.AngryAztec) and l.isdiddy and l.CanBuy(Locations.RocketbarrelBoost)),
        LocationLogic(Locations.LankyAztecPotion, lambda l: l.LevelEntered(Levels.AngryAztec) and l.islanky and l.CanBuy(Locations.LankyAztecPotion)),
        LocationLogic(Locations.TinyAztecPotion, lambda l: l.LevelEntered(Levels.AngryAztec) and l.istiny and l.CanBuy(Locations.TinyAztecPotion)),
        LocationLogic(Locations.ChunkyAztecPotion, lambda l: l.LevelEntered(Levels.AngryAztec) and l.ischunky and l.CanBuy(Locations.ChunkyAztecPotion)),
    ], [], [
        TransitionFront(Regions.CrankyGeneric, lambda l: True),
    ]),

    Regions.CrankyFactory: Region("Cranky Factory", Levels.Shops, False, None, [
        LocationLogic(Locations.SharedFactoryPotion, lambda l: l.LevelEntered(Levels.FranticFactory) and l.CanBuy(Locations.SharedFactoryPotion)),
        LocationLogic(Locations.GorillaGrab, lambda l: l.LevelEntered(Levels.FranticFactory) and l.isdonkey and l.CanBuy(Locations.GorillaGrab)),
        LocationLogic(Locations.SimianSpring, lambda l: l.LevelEntered(Levels.FranticFactory) and l.isdiddy and l.CanBuy(Locations.SimianSpring)),
        LocationLogic(Locations.BaboonBalloon, lambda l: l.LevelEntered(Levels.FranticFactory) and l.islanky and l.CanBuy(Locations.BaboonBalloon)),
        LocationLogic(Locations.PonyTailTwirl, lambda l: l.LevelEntered(Levels.FranticFactory) and l.istiny and l.CanBuy(Locations.PonyTailTwirl)),
        LocationLogic(Locations.PrimatePunch, lambda l: l.LevelEntered(Levels.FranticFactory) and l.ischunky and l.CanBuy(Locations.PrimatePunch)),
    ], [], [
        TransitionFront(Regions.CrankyGeneric, lambda l: True),
    ]),

    Regions.CrankyGalleon: Region("Cranky Galleon", Levels.Shops, False, None, [
        LocationLogic(Locations.SharedGalleonPotion, lambda l: l.LevelEntered(Levels.GloomyGalleon) and l.CanBuy(Locations.SharedGalleonPotion)),
        LocationLogic(Locations.DonkeyGalleonPotion, lambda l: l.LevelEntered(Levels.GloomyGalleon) and l.isdonkey and l.CanBuy(Locations.DonkeyGalleonPotion)),
        LocationLogic(Locations.DiddyGalleonPotion, lambda l: l.LevelEntered(Levels.GloomyGalleon) and l.isdiddy and l.CanBuy(Locations.DiddyGalleonPotion)),
        LocationLogic(Locations.LankyGalleonPotion, lambda l: l.LevelEntered(Levels.GloomyGalleon) and l.islanky and l.CanBuy(Locations.LankyGalleonPotion)),
        LocationLogic(Locations.TinyGalleonPotion, lambda l: l.LevelEntered(Levels.GloomyGalleon) and l.istiny and l.CanBuy(Locations.TinyGalleonPotion)),
        LocationLogic(Locations.ChunkyGalleonPotion, lambda l: l.LevelEntered(Levels.GloomyGalleon) and l.ischunky and l.CanBuy(Locations.ChunkyGalleonPotion)),
    ], [], [
        TransitionFront(Regions.CrankyGeneric, lambda l: True),
    ]),

    Regions.CrankyForest: Region("Cranky Forest", Levels.Shops, False, None, [
        LocationLogic(Locations.SuperSimianSlam, lambda l: l.LevelEntered(Levels.FungiForest) and l.CanBuy(Locations.SuperSimianSlam)),
        LocationLogic(Locations.DonkeyForestPotion, lambda l: l.LevelEntered(Levels.FungiForest) and l.isdonkey and l.CanBuy(Locations.DonkeyForestPotion)),
        LocationLogic(Locations.DiddyForestPotion, lambda l: l.LevelEntered(Levels.FungiForest) and l.isdiddy and l.CanBuy(Locations.DiddyForestPotion)),
        LocationLogic(Locations.LankyForestPotion, lambda l: l.LevelEntered(Levels.FungiForest) and l.islanky and l.CanBuy(Locations.LankyForestPotion)),
        LocationLogic(Locations.TinyForestPotion, lambda l: l.LevelEntered(Levels.FungiForest) and l.istiny and l.CanBuy(Locations.TinyForestPotion)),
        LocationLogic(Locations.ChunkyForestPotion, lambda l: l.LevelEntered(Levels.FungiForest) and l.ischunky and l.CanBuy(Locations.ChunkyForestPotion)),
    ], [], [
        TransitionFront(Regions.CrankyGeneric, lambda l: True),
    ]),

    Regions.CrankyCaves: Region("Cranky Caves", Levels.Shops, False, None, [
        LocationLogic(Locations.SharedCavesPotion, lambda l: l.LevelEntered(Levels.CrystalCaves) and l.CanBuy(Locations.SharedCavesPotion)),
        LocationLogic(Locations.OrangstandSprint, lambda l: l.LevelEntered(Levels.CrystalCaves) and l.islanky and l.CanBuy(Locations.OrangstandSprint)),
        LocationLogic(Locations.Monkeyport, lambda l: l.LevelEntered(Levels.CrystalCaves) and l.istiny and l.CanBuy(Locations.Monkeyport)),
        LocationLogic(Locations.GorillaGone, lambda l: l.LevelEntered(Levels.CrystalCaves) and l.ischunky and l.CanBuy(Locations.GorillaGone)),
        LocationLogic(Locations.DonkeyCavesPotion, lambda l: l.LevelEntered(Levels.CrystalCaves) and l.isdonkey and l.CanBuy(Locations.DonkeyCavesPotion)),
        LocationLogic(Locations.DiddyCavesPotion, lambda l: l.LevelEntered(Levels.CrystalCaves) and l.isdiddy and l.CanBuy(Locations.DiddyCavesPotion)),
    ], [], [
        TransitionFront(Regions.CrankyGeneric, lambda l: True),
    ]),

    Regions.CrankyCastle: Region("Cranky Castle", Levels.Shops, False, None, [
        LocationLogic(Locations.SuperDuperSimianSlam, lambda l: l.LevelEntered(Levels.CreepyCastle) and l.CanBuy(Locations.SuperDuperSimianSlam)),
        LocationLogic(Locations.DonkeyCastlePotion, lambda l: l.LevelEntered(Levels.CreepyCastle) and l.isdonkey and l.CanBuy(Locations.DonkeyCastlePotion)),
        LocationLogic(Locations.DiddyCastlePotion, lambda l: l.LevelEntered(Levels.CreepyCastle) and l.isdiddy and l.CanBuy(Locations.DiddyCastlePotion)),
        LocationLogic(Locations.LankyCastlePotion, lambda l: l.LevelEntered(Levels.CreepyCastle) and l.islanky and l.CanBuy(Locations.LankyCastlePotion)),
        LocationLogic(Locations.TinyCastlePotion, lambda l: l.LevelEntered(Levels.CreepyCastle) and l.istiny and l.CanBuy(Locations.TinyCastlePotion)),
        LocationLogic(Locations.ChunkyCastlePotion, lambda l: l.LevelEntered(Levels.CreepyCastle) and l.ischunky and l.CanBuy(Locations.ChunkyCastlePotion)),
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
