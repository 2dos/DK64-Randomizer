import itertools

from Enums.Items import Items

def Blueprints():
    blueprints = [
        Items.DKIslesDonkeyBlueprint,
        Items.DKIslesDiddyBlueprint,
        Items.DKIslesLankyBlueprint,
        Items.DKIslesTinyBlueprint,
        Items.DKIslesChunkyBlueprint,
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
    ]
    return blueprints

def Keys():
    keys = [
        Items.JungleJapesKey,
        Items.AngryAztecKey,
        Items.FranticFactoryKey,
        Items.GloomyGalleonKey,
        Items.FungiForestKey,
        Items.CrystalCavesKey,
        Items.CreepyCastleKey,
        Items.HideoutHelmKey,
    ]
    return keys

def Kongs():
    kongs = [
        Items.Diddy,
        Items.Lanky,
        Items.Tiny,
        Items.Chunky,
    ]
    return kongs

def Guns():
    guns = [
        Items.Coconut,
        Items.Peanut,
        Items.Grape,
        Items.Feather,
        Items.Pineapple,
    ]
    return guns

def Instruments():
    instruments = [
        Items.Bongos,
        Items.Guitar,
        Items.Trombone,
        Items.Saxophone,
        Items.Triangle,
    ]
    return instruments

def Upgrades():
    upgrades = [
        Items.BaboonBlast,
        Items.StrongKong,
        Items.GorillaGrab,
        Items.ChimpyCharge,
        Items.RocketbarrelBoost,
        Items.SimianSpring,
        Items.Orangstand,
        Items.BaboonBalloon,
        Items.OrangstandSprint,
        Items.MiniMonkey,
        Items.PonyTailTwirl,
        Items.Monkeyport,
        Items.HunkyChunky,
        Items.PrimatePunch,
        Items.GorillaGone,
        Items.CameraAndShockwave,
    ]
    upgrades.extend(itertools.repeat(Items.ProgressiveSlam, 3))
    return upgrades

# Get all items which are of high importance logically
# Placing these first prevents fill failures
def HighPriorityItems():
    itemPool = Keys()
    itemPool.extend(Kongs())
    itemPool.extend(Guns())
    itemPool.extend(Instruments())
    itemPool.extend(Upgrades())
    return itemPool

# While most of these items still have logical value they are not as important
def LowPriorityItems():
    itemPool = []

    # Weapon upgrades
    itemPool.extend([
        Items.HomingAmmo,
        Items.SniperSight,
    ])
    itemPool.extend(itertools.repeat(Items.ProgressiveAmmoBelt, 2))

    # Instrument upgrades
    itemPool.extend(itertools.repeat(Items.ProgressiveInstrumentUpgrade, 3))

    # Collectibles
    itemPool.extend(itertools.repeat(Items.GoldenBanana, 201))
    itemPool.extend(itertools.repeat(Items.BananaFairy, 20))
    itemPool.extend(itertools.repeat(Items.BattleCrown, 10))
    itemPool.extend(itertools.repeat(Items.BananaMedal, 5))
    itemPool.append(Items.NintendoCoin)
    itemPool.append(Items.RarewareCoin)

    return itemPool
