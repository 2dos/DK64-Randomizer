import itertools

from Items import Items

levels = [
    "DK Isles",
    "Jungle Japes",
    "Angry Aztec",
    "Frantic Factory",
    "Gloomy Galleon",
    "Fungi Forest",
    "Crystal Caves",
    "Creepy Castle",
]

kongs = [
    "Donkey",
    "Diddy",
    "Lanky",
    "Tiny",
    "Chunky",
]

def GenerateBlueprints():
    blueprints = []
    for level in levels:
        for kong in kongs:
            blueprints.append(level + " " + kong + " Blueprint")
    return blueprints


def GenerateItemPool():
    itemPool = []

    # Kongs
    itemPool.extend([
        Items.Diddy,
        Items.Lanky,
        Items.Tiny,
        Items.Chunky,
    ])

    # Cranky abilities
    itemPool.extend(itertools.repeat(Items.ProgressiveSlam, 3))
    itemPool.extend([
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
        Items.Mokeyport,
        Items.HunkyChunky,
        Items.PrimatePunch,
        Items.GorillaGone,
    ])

    # Weapons and their upgrades
    itemPool.extend([
        Items.Coconut,
        Items.Peanut,
        Items.Grape,
        Items.Feather,
        Items.Pineapple,
        Items.HomingAmmo,
        Items.SniperSight,
    ])
    itemPool.extend(itertools.repeat(Items.ProgressiveAmmoBelt, 2))

    # Instruments and their upgrades
    itemPool.extend([
        Items.Bongos,
        Items.Guitar,
        Items.Trombone,
        Items.Saxophone,
        Items.Triangle,
    ])
    itemPool.extend(itertools.repeat(Items.ProgressiveInstrumentUpgrade, 3))

    # Keys
    itemPool.extend([
        Items.JungleJapesKey,
        Items.AngryAztecKey,
        Items.FranticFactoryKey,
        Items.GloomyGalleonKey,
        Items.FungiForestKey,
        Items.CrystalCavesKey,
        Items.CreepyCastleKey,
        Items.HideoutHelmKey,
    ])

    # Collectibles
    itemPool.extend(itertools.repeat(Items.GoldenBanana, 201))
    itemPool.extend(GenerateBlueprints())
    itemPool.extend(itertools.repeat(Items.BananaFairy, 20))
    itemPool.extend(itertools.repeat(Items.BattleCrown, 10))
    itemPool.extend(itertools.repeat(Items.BananaMedal, 5))
    itemPool.append(Items.NintendoCoin)
    itemPool.append(Items.RarewareCoin)

    itemPool.append(Items.CameraAndShockwave)

    return itemPool