"""Stores the item class and a list of each item with its attributes."""
from randomizer.Enums.Items import Items
from randomizer.Enums.Kongs import Kongs


class Item:
    """Stores information about an item."""

    def __init__(self, name, playthrough):
        """Initialize with given parameters."""
        self.name = name
        self.playthrough = playthrough


def ItemFromKong(kong):
    """Get the item representation of a Kong enum."""
    if kong == Kongs.donkey:
        return Items.Donkey
    elif kong == Kongs.diddy:
        return Items.Diddy
    elif kong == Kongs.lanky:
        return Items.Lanky
    elif kong == Kongs.tiny:
        return Items.Tiny
    else:
        return Items.Chunky


ItemList = {
    Items.NoItem: Item("No Item", False),
    Items.Donkey: Item("Donkey", True),
    Items.Diddy: Item("Diddy", True),
    Items.Lanky: Item("Lanky", True),
    Items.Tiny: Item("Tiny", True),
    Items.Chunky: Item("Chunky", True),
    Items.Vines: Item("Vines", True),
    Items.Swim: Item("Swim", True),
    Items.Oranges: Item("Oranges", True),
    Items.Barrels: Item("Barrels", True),
    Items.ProgressiveSlam: Item("Progressive Slam", True),
    Items.ProgressiveDonkeyPotion: Item("Progressive Donkey Potion", True),
    Items.BaboonBlast: Item("Baboon Blast", True),
    Items.StrongKong: Item("Strong Kong", True),
    Items.GorillaGrab: Item("Gorilla Grab", True),
    Items.ProgressiveDiddyPotion: Item("Progressive Diddy Potion", True),
    Items.ChimpyCharge: Item("Chimpy Charge", True),
    Items.RocketbarrelBoost: Item("Rocketbarrel Boost", True),
    Items.SimianSpring: Item("Simian Spring", True),
    Items.ProgressiveLankyPotion: Item("Progressive Lanky Potion", True),
    Items.Orangstand: Item("Orangstand", True),
    Items.BaboonBalloon: Item("Baboon Balloon", True),
    Items.OrangstandSprint: Item("Orangstand Sprint", True),
    Items.ProgressiveTinyPotion: Item("Progressive Tiny Potion", True),
    Items.MiniMonkey: Item("Mini Monkey", True),
    Items.PonyTailTwirl: Item("Pony Tail Twirl", True),
    Items.Monkeyport: Item("Monkeyport", True),
    Items.ProgressiveChunkyPotion: Item("Progressive Chunky Potion", True),
    Items.HunkyChunky: Item("Hunky Chunky", True),
    Items.PrimatePunch: Item("Primate Punch", True),
    Items.GorillaGone: Item("Gorilla Gone", True),
    Items.Coconut: Item("Coconut", True),
    Items.Peanut: Item("Peanut", True),
    Items.Grape: Item("Grape", True),
    Items.Feather: Item("Feather", True),
    Items.Pineapple: Item("Pineapple", True),
    Items.HomingAmmo: Item("Homing Ammo", False),
    Items.SniperSight: Item("Sniper Sight", False),
    Items.ProgressiveAmmoBelt: Item("Progressive Ammo Belt", False),
    Items.Bongos: Item("Bongos", True),
    Items.Guitar: Item("Guitar", True),
    Items.Trombone: Item("Trombone", True),
    Items.Saxophone: Item("Saxophone", True),
    Items.Triangle: Item("Triangle", True),
    Items.ProgressiveInstrumentUpgrade: Item("Progressive Instrument Upgrade", False),
    Items.NintendoCoin: Item("Nintendo Coin", True),
    Items.RarewareCoin: Item("Rareware Coin", True),
    Items.CameraAndShockwave: Item("Camera and Shockwave", True),
    Items.JungleJapesKey: Item("Jungle Japes Key", True),
    Items.AngryAztecKey: Item("Angry Aztec Key", True),
    Items.FranticFactoryKey: Item("Frantic Factory Key", True),
    Items.GloomyGalleonKey: Item("Gloomy Galleon Key", True),
    Items.FungiForestKey: Item("Fungi Forest Key", True),
    Items.CrystalCavesKey: Item("Crystal Caves Key", True),
    Items.CreepyCastleKey: Item("Creepy Castle Key", True),
    Items.HideoutHelmKey: Item("Hideout Helm Key", True),
    Items.HelmDonkey1: Item("Helm Donkey Barrel 1", False),
    Items.HelmDonkey2: Item("Helm Donkey Barrel 2", False),
    Items.HelmDiddy1: Item("Helm Diddy Barrel 1", False),
    Items.HelmDiddy2: Item("Helm Diddy Barrel 2", False),
    Items.HelmLanky1: Item("Helm Lanky Barrel 1", False),
    Items.HelmLanky2: Item("Helm Lanky Barrel 2", False),
    Items.HelmTiny1: Item("Helm Tiny Barrel 1", False),
    Items.HelmTiny2: Item("Helm Tiny Barrel 2", False),
    Items.HelmChunky1: Item("Helm Chunky Barrel 1", False),
    Items.HelmChunky2: Item("Helm Chunky Barrel 2", False),
    Items.GoldenBanana: Item("Golden Banana", False),
    Items.BananaFairy: Item("Banana Fairy", False),
    Items.BananaMedal: Item("Banana Medal", False),
    Items.BattleCrown: Item("Battle Crown", False),
    Items.DKIslesDonkeyBlueprint: Item("DK Isles Donkey Blueprint", False),
    Items.DKIslesDiddyBlueprint: Item("DK Isles Diddy Blueprint", False),
    Items.DKIslesLankyBlueprint: Item("DK Isles Lanky Blueprint", False),
    Items.DKIslesTinyBlueprint: Item("DK Isles Tiny Blueprint", False),
    Items.DKIslesChunkyBlueprint: Item("DK Isles Chunky Blueprint", False),
    Items.JungleJapesDonkeyBlueprint: Item("Jungle Japes Donkey Blueprint", False),
    Items.JungleJapesDiddyBlueprint: Item("Jungle Japes Diddy Blueprint", False),
    Items.JungleJapesLankyBlueprint: Item("Jungle Japes Lanky Blueprint", False),
    Items.JungleJapesTinyBlueprint: Item("Jungle Japes Tiny Blueprint", False),
    Items.JungleJapesChunkyBlueprint: Item("Jungle Japes Chunky Blueprint", False),
    Items.AngryAztecDonkeyBlueprint: Item("Angry Aztec Donkey Blueprint", False),
    Items.AngryAztecDiddyBlueprint: Item("Angry Aztec Diddy Blueprint", False),
    Items.AngryAztecLankyBlueprint: Item("Angry Aztec Lanky Blueprint", False),
    Items.AngryAztecTinyBlueprint: Item("Angry Aztec Tiny Blueprint", False),
    Items.AngryAztecChunkyBlueprint: Item("Angry Aztec Chunky Blueprint", False),
    Items.FranticFactoryDonkeyBlueprint: Item("Frantic Factory Donkey Blueprint", False),
    Items.FranticFactoryDiddyBlueprint: Item("Frantic Factory Diddy Blueprint", False),
    Items.FranticFactoryLankyBlueprint: Item("Frantic Factory Lanky Blueprint", False),
    Items.FranticFactoryTinyBlueprint: Item("Frantic Factory Tiny Blueprint", False),
    Items.FranticFactoryChunkyBlueprint: Item("Frantic Factory Chunky Blueprint", False),
    Items.GloomyGalleonDonkeyBlueprint: Item("Gloomy Galleon Donkey Blueprint", False),
    Items.GloomyGalleonDiddyBlueprint: Item("Gloomy Galleon Diddy Blueprint", False),
    Items.GloomyGalleonLankyBlueprint: Item("Gloomy Galleon Lanky Blueprint", False),
    Items.GloomyGalleonTinyBlueprint: Item("Gloomy Galleon Tiny Blueprint", False),
    Items.GloomyGalleonChunkyBlueprint: Item("Gloomy Galleon Chunky Blueprint", False),
    Items.FungiForestDonkeyBlueprint: Item("Fungi Forest Donkey Blueprint", False),
    Items.FungiForestDiddyBlueprint: Item("Fungi Forest Diddy Blueprint", False),
    Items.FungiForestLankyBlueprint: Item("Fungi Forest Lanky Blueprint", False),
    Items.FungiForestTinyBlueprint: Item("Fungi Forest Tiny Blueprint", False),
    Items.FungiForestChunkyBlueprint: Item("Fungi Forest Chunky Blueprint", False),
    Items.CrystalCavesDonkeyBlueprint: Item("Crystal Caves Donkey Blueprint", False),
    Items.CrystalCavesDiddyBlueprint: Item("Crystal Caves Diddy Blueprint", False),
    Items.CrystalCavesLankyBlueprint: Item("Crystal Caves Lanky Blueprint", False),
    Items.CrystalCavesTinyBlueprint: Item("Crystal Caves Tiny Blueprint", False),
    Items.CrystalCavesChunkyBlueprint: Item("Crystal Caves Chunky Blueprint", False),
    Items.CreepyCastleDonkeyBlueprint: Item("Creepy Castle Donkey Blueprint", False),
    Items.CreepyCastleDiddyBlueprint: Item("Creepy Castle Diddy Blueprint", False),
    Items.CreepyCastleLankyBlueprint: Item("Creepy Castle Lanky Blueprint", False),
    Items.CreepyCastleTinyBlueprint: Item("Creepy Castle Tiny Blueprint", False),
    Items.CreepyCastleChunkyBlueprint: Item("Creepy Castle Chunky Blueprint", False),
    Items.BananaHoard: Item("Banana Hoard", True),
}
