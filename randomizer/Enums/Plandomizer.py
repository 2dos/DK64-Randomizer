"""Plandomizer enums and associated maps."""
from enum import IntEnum, auto

from randomizer.Enums.Items import Items


class PlandoItems(IntEnum):
    """Plando item enum."""

    NoItem = auto()

    Donkey = auto()
    Diddy = auto()
    Lanky = auto()
    Tiny = auto()
    Chunky = auto()

    Vines = auto()
    Swim = auto()
    Oranges = auto()
    Barrels = auto()

    ProgressiveSlam = auto()

    # Progressive potions are not used.
    BaboonBlast = auto()
    StrongKong = auto()
    GorillaGrab = auto()

    ChimpyCharge = auto()
    RocketbarrelBoost = auto()
    SimianSpring = auto()

    Orangstand = auto()
    BaboonBalloon = auto()
    OrangstandSprint = auto()

    MiniMonkey = auto()
    PonyTailTwirl = auto()
    Monkeyport = auto()

    HunkyChunky = auto()
    PrimatePunch = auto()
    GorillaGone = auto()

    Coconut = auto()
    Peanut = auto()
    Grape = auto()
    Feather = auto()
    Pineapple = auto()
    HomingAmmo = auto()
    SniperSight = auto()
    ProgressiveAmmoBelt = auto()

    Bongos = auto()
    Guitar = auto()
    Trombone = auto()
    Saxophone = auto()
    Triangle = auto()
    ProgressiveInstrumentUpgrade = auto()

    Camera = auto()
    Shockwave = auto()
    # CameraAndShockwave is not used.

    NintendoCoin = auto()
    RarewareCoin = auto()

    JungleJapesKey = auto()
    AngryAztecKey = auto()
    FranticFactoryKey = auto()
    GloomyGalleonKey = auto()
    FungiForestKey = auto()
    CrystalCavesKey = auto()
    CreepyCastleKey = auto()
    HideoutHelmKey = auto()

    GoldenBanana = auto()
    # ToughBanana is only used for shuffling logic and is not actually a
    # different item, so it is excluded.
    BananaFairy = auto()
    BananaMedal = auto()
    BattleCrown = auto()

    Bean = auto()
    Pearl = auto()
    RainbowCoin = auto()
    FakeItem = auto()

    # A generic junk item to represent all specific junk items.
    JunkItem = auto()

    # BananaHoard is not used.

    # Hints are not used as plando items.

    # A generic blueprint item to represent all specific blueprints.
    Blueprint = auto()

ItemToPlandoItemMap = {
    Items.NoItem: PlandoItems.NoItem,
    Items.Donkey: PlandoItems.Donkey,
    Items.Diddy: PlandoItems.Diddy,
    Items.Lanky: PlandoItems.Lanky,
    Items.Tiny: PlandoItems.Tiny,
    Items.Chunky: PlandoItems.Chunky,
    Items.Vines: PlandoItems.Vines,
    Items.Swim: PlandoItems.Swim,
    Items.Oranges: PlandoItems.Oranges,
    Items.Barrels: PlandoItems.Barrels,
    Items.ProgressiveSlam: PlandoItems.ProgressiveSlam,
    Items.BaboonBlast: PlandoItems.BaboonBlast,
    Items.StrongKong: PlandoItems.StrongKong,
    Items.GorillaGrab: PlandoItems.GorillaGrab,
    Items.ChimpyCharge: PlandoItems.ChimpyCharge,
    Items.RocketbarrelBoost: PlandoItems.RocketbarrelBoost,
    Items.SimianSpring: PlandoItems.SimianSpring,
    Items.Orangstand: PlandoItems.Orangstand,
    Items.BaboonBalloon: PlandoItems.BaboonBalloon,
    Items.OrangstandSprint: PlandoItems.OrangstandSprint,
    Items.MiniMonkey: PlandoItems.MiniMonkey,
    Items.PonyTailTwirl: PlandoItems.PonyTailTwirl,
    Items.Monkeyport: PlandoItems.Monkeyport,
    Items.HunkyChunky: PlandoItems.HunkyChunky,
    Items.PrimatePunch: PlandoItems.PrimatePunch,
    Items.GorillaGone: PlandoItems.GorillaGone,
    Items.Coconut: PlandoItems.Coconut,
    Items.Peanut: PlandoItems.Peanut,
    Items.Grape: PlandoItems.Grape,
    Items.Feather: PlandoItems.Feather,
    Items.Pineapple: PlandoItems.Pineapple,
    Items.HomingAmmo: PlandoItems.HomingAmmo,
    Items.SniperSight: PlandoItems.SniperSight,
    Items.ProgressiveAmmoBelt: PlandoItems.ProgressiveAmmoBelt,
    Items.Bongos: PlandoItems.Bongos,
    Items.Guitar: PlandoItems.Guitar,
    Items.Trombone: PlandoItems.Trombone,
    Items.Saxophone: PlandoItems.Saxophone,
    Items.Triangle: PlandoItems.Triangle,
    Items.ProgressiveInstrumentUpgrade: PlandoItems.ProgressiveInstrumentUpgrade,
    Items.Camera: PlandoItems.Camera,
    Items.Shockwave: PlandoItems.Shockwave,
    Items.NintendoCoin: PlandoItems.NintendoCoin,
    Items.RarewareCoin: PlandoItems.RarewareCoin,
    Items.JungleJapesKey: PlandoItems.JungleJapesKey,
    Items.AngryAztecKey: PlandoItems.AngryAztecKey,
    Items.FranticFactoryKey: PlandoItems.FranticFactoryKey,
    Items.GloomyGalleonKey: PlandoItems.GloomyGalleonKey,
    Items.FungiForestKey: PlandoItems.FungiForestKey,
    Items.CrystalCavesKey: PlandoItems.CrystalCavesKey,
    Items.CreepyCastleKey: PlandoItems.CreepyCastleKey,
    Items.HideoutHelmKey: PlandoItems.HideoutHelmKey,
    Items.GoldenBanana: PlandoItems.GoldenBanana,
    Items.BananaFairy: PlandoItems.BananaFairy,
    Items.BananaMedal: PlandoItems.BananaMedal,
    Items.BattleCrown: PlandoItems.BattleCrown,
    Items.Bean: PlandoItems.Bean,
    Items.Pearl: PlandoItems.Pearl,
    Items.RainbowCoin: PlandoItems.RainbowCoin,
    Items.FakeItem: PlandoItems.FakeItem,
    # All of the individual junk items map to the same plando item.
    Items.JunkCrystal: PlandoItems.JunkItem,
    Items.JunkMelon: PlandoItems.JunkItem,
    Items.JunkAmmo: PlandoItems.JunkItem,
    Items.JunkFilm: PlandoItems.JunkItem,
    Items.JunkOrange: PlandoItems.JunkItem,
    # All of the individual blueprints map to the same plando item.
    Items.JungleJapesDonkeyBlueprint: PlandoItems.Blueprint,
    Items.JungleJapesDiddyBlueprint: PlandoItems.Blueprint,
    Items.JungleJapesLankyBlueprint: PlandoItems.Blueprint,
    Items.JungleJapesTinyBlueprint: PlandoItems.Blueprint,
    Items.JungleJapesChunkyBlueprint: PlandoItems.Blueprint,
    Items.AngryAztecDonkeyBlueprint: PlandoItems.Blueprint,
    Items.AngryAztecDiddyBlueprint: PlandoItems.Blueprint,
    Items.AngryAztecLankyBlueprint: PlandoItems.Blueprint,
    Items.AngryAztecTinyBlueprint: PlandoItems.Blueprint,
    Items.AngryAztecChunkyBlueprint: PlandoItems.Blueprint,
    Items.FranticFactoryDonkeyBlueprint: PlandoItems.Blueprint,
    Items.FranticFactoryDiddyBlueprint: PlandoItems.Blueprint,
    Items.FranticFactoryLankyBlueprint: PlandoItems.Blueprint,
    Items.FranticFactoryTinyBlueprint: PlandoItems.Blueprint,
    Items.FranticFactoryChunkyBlueprint: PlandoItems.Blueprint,
    Items.GloomyGalleonDonkeyBlueprint: PlandoItems.Blueprint,
    Items.GloomyGalleonDiddyBlueprint: PlandoItems.Blueprint,
    Items.GloomyGalleonLankyBlueprint: PlandoItems.Blueprint,
    Items.GloomyGalleonTinyBlueprint: PlandoItems.Blueprint,
    Items.GloomyGalleonChunkyBlueprint: PlandoItems.Blueprint,
    Items.FungiForestDonkeyBlueprint: PlandoItems.Blueprint,
    Items.FungiForestDiddyBlueprint: PlandoItems.Blueprint,
    Items.FungiForestLankyBlueprint: PlandoItems.Blueprint,
    Items.FungiForestTinyBlueprint: PlandoItems.Blueprint,
    Items.FungiForestChunkyBlueprint: PlandoItems.Blueprint,
    Items.CrystalCavesDonkeyBlueprint: PlandoItems.Blueprint,
    Items.CrystalCavesDiddyBlueprint: PlandoItems.Blueprint,
    Items.CrystalCavesLankyBlueprint: PlandoItems.Blueprint,
    Items.CrystalCavesTinyBlueprint: PlandoItems.Blueprint,
    Items.CrystalCavesChunkyBlueprint: PlandoItems.Blueprint,
    Items.CreepyCastleDonkeyBlueprint: PlandoItems.Blueprint,
    Items.CreepyCastleDiddyBlueprint: PlandoItems.Blueprint,
    Items.CreepyCastleLankyBlueprint: PlandoItems.Blueprint,
    Items.CreepyCastleTinyBlueprint: PlandoItems.Blueprint,
    Items.CreepyCastleChunkyBlueprint: PlandoItems.Blueprint,
    Items.DKIslesDonkeyBlueprint: PlandoItems.Blueprint,
    Items.DKIslesDiddyBlueprint: PlandoItems.Blueprint,
    Items.DKIslesLankyBlueprint: PlandoItems.Blueprint,
    Items.DKIslesTinyBlueprint: PlandoItems.Blueprint,
    Items.DKIslesChunkyBlueprint: PlandoItems.Blueprint
}

PlandoItemToItemMap = {
    PlandoItems.NoItem: Items.NoItem,
    PlandoItems.Donkey: Items.Donkey,
    PlandoItems.Diddy: Items.Diddy,
    PlandoItems.Lanky: Items.Lanky,
    PlandoItems.Tiny: Items.Tiny,
    PlandoItems.Chunky: Items.Chunky,
    PlandoItems.Vines: Items.Vines,
    PlandoItems.Swim: Items.Swim,
    PlandoItems.Oranges: Items.Oranges,
    PlandoItems.Barrels: Items.Barrels,
    PlandoItems.ProgressiveSlam: Items.ProgressiveSlam,
    PlandoItems.BaboonBlast: Items.BaboonBlast,
    PlandoItems.StrongKong: Items.StrongKong,
    PlandoItems.GorillaGrab: Items.GorillaGrab,
    PlandoItems.ChimpyCharge: Items.ChimpyCharge,
    PlandoItems.RocketbarrelBoost: Items.RocketbarrelBoost,
    PlandoItems.SimianSpring: Items.SimianSpring,
    PlandoItems.Orangstand: Items.Orangstand,
    PlandoItems.BaboonBalloon: Items.BaboonBalloon,
    PlandoItems.OrangstandSprint: Items.OrangstandSprint,
    PlandoItems.MiniMonkey: Items.MiniMonkey,
    PlandoItems.PonyTailTwirl: Items.PonyTailTwirl,
    PlandoItems.Monkeyport: Items.Monkeyport,
    PlandoItems.HunkyChunky: Items.HunkyChunky,
    PlandoItems.PrimatePunch: Items.PrimatePunch,
    PlandoItems.GorillaGone: Items.GorillaGone,
    PlandoItems.Coconut: Items.Coconut,
    PlandoItems.Peanut: Items.Peanut,
    PlandoItems.Grape: Items.Grape,
    PlandoItems.Feather: Items.Feather,
    PlandoItems.Pineapple: Items.Pineapple,
    PlandoItems.HomingAmmo: Items.HomingAmmo,
    PlandoItems.SniperSight: Items.SniperSight,
    PlandoItems.ProgressiveAmmoBelt: Items.ProgressiveAmmoBelt,
    PlandoItems.Bongos: Items.Bongos,
    PlandoItems.Guitar: Items.Guitar,
    PlandoItems.Trombone: Items.Trombone,
    PlandoItems.Saxophone: Items.Saxophone,
    PlandoItems.Triangle: Items.Triangle,
    PlandoItems.ProgressiveInstrumentUpgrade: Items.ProgressiveInstrumentUpgrade,
    PlandoItems.Camera: Items.Camera,
    PlandoItems.Shockwave: Items.Shockwave,
    PlandoItems.NintendoCoin: Items.NintendoCoin,
    PlandoItems.RarewareCoin: Items.RarewareCoin,
    PlandoItems.JungleJapesKey: Items.JungleJapesKey,
    PlandoItems.AngryAztecKey: Items.AngryAztecKey,
    PlandoItems.FranticFactoryKey: Items.FranticFactoryKey,
    PlandoItems.GloomyGalleonKey: Items.GloomyGalleonKey,
    PlandoItems.FungiForestKey: Items.FungiForestKey,
    PlandoItems.CrystalCavesKey: Items.CrystalCavesKey,
    PlandoItems.CreepyCastleKey: Items.CreepyCastleKey,
    PlandoItems.HideoutHelmKey: Items.HideoutHelmKey,
    PlandoItems.GoldenBanana: Items.GoldenBanana,
    PlandoItems.BananaFairy: Items.BananaFairy,
    PlandoItems.BananaMedal: Items.BananaMedal,
    PlandoItems.BattleCrown: Items.BattleCrown,
    PlandoItems.Bean: Items.Bean,
    PlandoItems.Pearl: Items.Pearl,
    PlandoItems.RainbowCoin: Items.RainbowCoin,
    PlandoItems.FakeItem: Items.FakeItem
}

PlandoItemToItemListMap = {
    PlandoItems.JunkItem: [
        Items.JunkCrystal,
        Items.JunkMelon,
        Items.JunkAmmo,
        Items.JunkFilm,
        Items.JunkOrange
    ],
    PlandoItems.Blueprint: [
        Items.JungleJapesDonkeyBlueprint,
        Items.JungleJapesDiddyBlueprint,
        Items.JungleJapesLankyBlueprint,
        Items.JungleJapesTinyBlueprint,
        Items.JungleJapesChunkyBlueprint,
        Items.AngryAztecDonkeyBlueprint,
        Items.AngryAztecDiddyBlueprint,
        Items.AngryAztecLankyBlueprint,
        Items.AngryAztecTinyBlueprint,
        Items.AngryAztecChunkyBlueprint,
        Items.FranticFactoryDonkeyBlueprint,
        Items.FranticFactoryDiddyBlueprint,
        Items.FranticFactoryLankyBlueprint,
        Items.FranticFactoryTinyBlueprint,
        Items.FranticFactoryChunkyBlueprint,
        Items.GloomyGalleonDonkeyBlueprint,
        Items.GloomyGalleonDiddyBlueprint,
        Items.GloomyGalleonLankyBlueprint,
        Items.GloomyGalleonTinyBlueprint,
        Items.GloomyGalleonChunkyBlueprint,
        Items.FungiForestDonkeyBlueprint,
        Items.FungiForestDiddyBlueprint,
        Items.FungiForestLankyBlueprint,
        Items.FungiForestTinyBlueprint,
        Items.FungiForestChunkyBlueprint,
        Items.CrystalCavesDonkeyBlueprint,
        Items.CrystalCavesDiddyBlueprint,
        Items.CrystalCavesLankyBlueprint,
        Items.CrystalCavesTinyBlueprint,
        Items.CrystalCavesChunkyBlueprint,
        Items.CreepyCastleDonkeyBlueprint,
        Items.CreepyCastleDiddyBlueprint,
        Items.CreepyCastleLankyBlueprint,
        Items.CreepyCastleTinyBlueprint,
        Items.CreepyCastleChunkyBlueprint,
        Items.DKIslesDonkeyBlueprint,
        Items.DKIslesDiddyBlueprint,
        Items.DKIslesLankyBlueprint,
        Items.DKIslesTinyBlueprint,
        Items.DKIslesChunkyBlueprint
    ]
}

def GetItemFromPlandoItem(plandoItemEnum):
    if plandoItemEnum in PlandoItemToItemMap:
        return [PlandoItemToItemMap[plandoItemEnum]]
    if plandoItemEnum in PlandoItemToItemListMap:
        return PlandoItemToItemListMap[plandoItemEnum]
    return None
