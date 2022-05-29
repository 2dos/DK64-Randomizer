"""Stores the item class and a list of each item with its attributes."""

from randomizer.Enums.Items import Items
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.MoveTypes import MoveTypes
from randomizer.Enums.Types import Types


class Item:
    """Stores information about an item."""

    def __init__(self, name, playthrough, type, data=None):
        """Initialize with given parameters."""
        if data is None:
            data = []
        self.name = name
        self.playthrough = playthrough
        self.type = type
        if type == Types.Shop:
            self.kong = data[0]
            self.movetype = data[1]
            self.index = data[2]


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
    elif kong == Kongs.chunky:
        return Items.Chunky
    else:
        return Items.NoItem


def NameFromKong(kong):
    """Get the name of a kong from its Kong enum value."""
    if kong == Kongs.donkey:
        return "Donkey"
    elif kong == Kongs.diddy:
        return "Diddy"
    elif kong == Kongs.lanky:
        return "Lanky"
    elif kong == Kongs.tiny:
        return "Tiny"
    elif kong == Kongs.chunky:
        return "Chunky"
    else:
        return "No Kong"


def KongFromItem(item):
    """Get the Kong enum representation of a kong item."""
    if item == Items.Donkey:
        return Kongs.donkey
    elif item == Items.Diddy:
        return Kongs.diddy
    elif item == Items.Lanky:
        return Kongs.lanky
    elif item == Items.Tiny:
        return Kongs.tiny
    elif item == Items.Chunky:
        return Kongs.chunky
    else:
        return Kongs.any


ItemList = {
    Items.NoItem: Item("No Item", False, Types.Constant),
    Items.Donkey: Item("Donkey", True, Types.Kong),
    Items.Diddy: Item("Diddy", True, Types.Kong),
    Items.Lanky: Item("Lanky", True, Types.Kong),
    Items.Tiny: Item("Tiny", True, Types.Kong),
    Items.Chunky: Item("Chunky", True, Types.Kong),
    Items.Vines: Item("Vines", True, Types.TrainingBarrel),
    Items.Swim: Item("Swim", True, Types.TrainingBarrel),
    Items.Oranges: Item("Oranges", True, Types.TrainingBarrel),
    Items.Barrels: Item("Barrels", True, Types.TrainingBarrel),
    Items.ProgressiveSlam: Item("Progressive Slam", True, Types.Shop, [Kongs.any, MoveTypes.Slam, 2]),
    Items.ProgressiveDonkeyPotion: Item("Progressive Donkey Potion", True, Types.Shop, [Kongs.donkey, MoveTypes.Moves, 1]),
    Items.BaboonBlast: Item("Baboon Blast", True, Types.Shop, [Kongs.donkey, MoveTypes.Moves, 1]),
    Items.StrongKong: Item("Strong Kong", True, Types.Shop, [Kongs.donkey, MoveTypes.Moves, 2]),
    Items.GorillaGrab: Item("Gorilla Grab", True, Types.Shop, [Kongs.donkey, MoveTypes.Moves, 3]),
    Items.ProgressiveDiddyPotion: Item("Progressive Diddy Potion", True, Types.Shop, [Kongs.diddy, MoveTypes.Moves, 1]),
    Items.ChimpyCharge: Item("Chimpy Charge", True, Types.Shop, [Kongs.diddy, MoveTypes.Moves, 1]),
    Items.RocketbarrelBoost: Item("Rocketbarrel Boost", True, Types.Shop, [Kongs.diddy, MoveTypes.Moves, 2]),
    Items.SimianSpring: Item("Simian Spring", True, Types.Shop, [Kongs.diddy, MoveTypes.Moves, 3]),
    Items.ProgressiveLankyPotion: Item("Progressive Lanky Potion", True, Types.Shop, [Kongs.lanky, MoveTypes.Moves, 1]),
    Items.Orangstand: Item("Orangstand", True, Types.Shop, [Kongs.lanky, MoveTypes.Moves, 1]),
    Items.BaboonBalloon: Item("Baboon Balloon", True, Types.Shop, [Kongs.lanky, MoveTypes.Moves, 2]),
    Items.OrangstandSprint: Item("Orangstand Sprint", True, Types.Shop, [Kongs.lanky, MoveTypes.Moves, 3]),
    Items.ProgressiveTinyPotion: Item("Progressive Tiny Potion", True, Types.Shop, [Kongs.tiny, MoveTypes.Moves, 1]),
    Items.MiniMonkey: Item("Mini Monkey", True, Types.Shop, [Kongs.tiny, MoveTypes.Moves, 1]),
    Items.PonyTailTwirl: Item("Pony Tail Twirl", True, Types.Shop, [Kongs.tiny, MoveTypes.Moves, 2]),
    Items.Monkeyport: Item("Monkeyport", True, Types.Shop, [Kongs.tiny, MoveTypes.Moves, 3]),
    Items.ProgressiveChunkyPotion: Item("Progressive Chunky Potion", True, Types.Shop, [Kongs.chunky, MoveTypes.Moves, 1]),
    Items.HunkyChunky: Item("Hunky Chunky", True, Types.Shop, [Kongs.chunky, MoveTypes.Moves, 1]),
    Items.PrimatePunch: Item("Primate Punch", True, Types.Shop, [Kongs.chunky, MoveTypes.Moves, 2]),
    Items.GorillaGone: Item("Gorilla Gone", True, Types.Shop, [Kongs.chunky, MoveTypes.Moves, 3]),
    Items.Coconut: Item("Coconut", True, Types.Shop, [Kongs.donkey, MoveTypes.Guns, 1]),
    Items.Peanut: Item("Peanut", True, Types.Shop, [Kongs.diddy, MoveTypes.Guns, 1]),
    Items.Grape: Item("Grape", True, Types.Shop, [Kongs.lanky, MoveTypes.Guns, 1]),
    Items.Feather: Item("Feather", True, Types.Shop, [Kongs.tiny, MoveTypes.Guns, 1]),
    Items.Pineapple: Item("Pineapple", True, Types.Shop, [Kongs.chunky, MoveTypes.Guns, 1]),
    Items.HomingAmmo: Item("Homing Ammo", True, Types.Shop, [Kongs.any, MoveTypes.Guns, 2]),
    Items.SniperSight: Item("Sniper Sight", True, Types.Shop, [Kongs.any, MoveTypes.Guns, 3]),
    Items.ProgressiveAmmoBelt: Item("Progressive Ammo Belt", False, Types.Shop, [Kongs.any, MoveTypes.AmmoBelt, 1]),
    Items.Bongos: Item("Bongos", True, Types.Shop, [Kongs.donkey, MoveTypes.Instruments, 1]),
    Items.Guitar: Item("Guitar", True, Types.Shop, [Kongs.diddy, MoveTypes.Instruments, 1]),
    Items.Trombone: Item("Trombone", True, Types.Shop, [Kongs.lanky, MoveTypes.Instruments, 1]),
    Items.Saxophone: Item("Saxophone", True, Types.Shop, [Kongs.tiny, MoveTypes.Instruments, 1]),
    Items.Triangle: Item("Triangle", True, Types.Shop, [Kongs.chunky, MoveTypes.Instruments, 1]),
    Items.ProgressiveInstrumentUpgrade: Item("Progressive Instrument Upgrade", False, Types.Shop, [Kongs.any, MoveTypes.Instruments, 2]),
    Items.NintendoCoin: Item("Nintendo Coin", True, Types.Coin),
    Items.RarewareCoin: Item("Rareware Coin", True, Types.Coin),
    Items.CameraAndShockwave: Item("Camera and Shockwave", True, Types.Shockwave),
    Items.JungleJapesKey: Item("Jungle Japes Key", True, Types.Key),
    Items.AngryAztecKey: Item("Angry Aztec Key", True, Types.Key),
    Items.FranticFactoryKey: Item("Frantic Factory Key", True, Types.Key),
    Items.GloomyGalleonKey: Item("Gloomy Galleon Key", True, Types.Key),
    Items.FungiForestKey: Item("Fungi Forest Key", True, Types.Key),
    Items.CrystalCavesKey: Item("Crystal Caves Key", True, Types.Key),
    Items.CreepyCastleKey: Item("Creepy Castle Key", True, Types.Key),
    Items.HideoutHelmKey: Item("Hideout Helm Key", True, Types.Key),
    Items.HelmDonkey1: Item("Helm Donkey Barrel 1", False, Types.Constant),
    Items.HelmDonkey2: Item("Helm Donkey Barrel 2", False, Types.Constant),
    Items.HelmDiddy1: Item("Helm Diddy Barrel 1", False, Types.Constant),
    Items.HelmDiddy2: Item("Helm Diddy Barrel 2", False, Types.Constant),
    Items.HelmLanky1: Item("Helm Lanky Barrel 1", False, Types.Constant),
    Items.HelmLanky2: Item("Helm Lanky Barrel 2", False, Types.Constant),
    Items.HelmTiny1: Item("Helm Tiny Barrel 1", False, Types.Constant),
    Items.HelmTiny2: Item("Helm Tiny Barrel 2", False, Types.Constant),
    Items.HelmChunky1: Item("Helm Chunky Barrel 1", False, Types.Constant),
    Items.HelmChunky2: Item("Helm Chunky Barrel 2", False, Types.Constant),
    Items.GoldenBanana: Item("Golden Banana", False, Types.Banana),
    Items.BananaFairy: Item("Banana Fairy", False, Types.Fairy),
    Items.BananaMedal: Item("Banana Medal", False, Types.Medal),
    Items.BattleCrown: Item("Battle Crown", False, Types.Crown),
    Items.DKIslesDonkeyBlueprint: Item("DK Isles Donkey Blueprint", False, Types.Blueprint),
    Items.DKIslesDiddyBlueprint: Item("DK Isles Diddy Blueprint", False, Types.Blueprint),
    Items.DKIslesLankyBlueprint: Item("DK Isles Lanky Blueprint", False, Types.Blueprint),
    Items.DKIslesTinyBlueprint: Item("DK Isles Tiny Blueprint", False, Types.Blueprint),
    Items.DKIslesChunkyBlueprint: Item("DK Isles Chunky Blueprint", False, Types.Blueprint),
    Items.JungleJapesDonkeyBlueprint: Item("Jungle Japes Donkey Blueprint", False, Types.Blueprint),
    Items.JungleJapesDiddyBlueprint: Item("Jungle Japes Diddy Blueprint", False, Types.Blueprint),
    Items.JungleJapesLankyBlueprint: Item("Jungle Japes Lanky Blueprint", False, Types.Blueprint),
    Items.JungleJapesTinyBlueprint: Item("Jungle Japes Tiny Blueprint", False, Types.Blueprint),
    Items.JungleJapesChunkyBlueprint: Item("Jungle Japes Chunky Blueprint", False, Types.Blueprint),
    Items.AngryAztecDonkeyBlueprint: Item("Angry Aztec Donkey Blueprint", False, Types.Blueprint),
    Items.AngryAztecDiddyBlueprint: Item("Angry Aztec Diddy Blueprint", False, Types.Blueprint),
    Items.AngryAztecLankyBlueprint: Item("Angry Aztec Lanky Blueprint", False, Types.Blueprint),
    Items.AngryAztecTinyBlueprint: Item("Angry Aztec Tiny Blueprint", False, Types.Blueprint),
    Items.AngryAztecChunkyBlueprint: Item("Angry Aztec Chunky Blueprint", False, Types.Blueprint),
    Items.FranticFactoryDonkeyBlueprint: Item("Frantic Factory Donkey Blueprint", False, Types.Blueprint),
    Items.FranticFactoryDiddyBlueprint: Item("Frantic Factory Diddy Blueprint", False, Types.Blueprint),
    Items.FranticFactoryLankyBlueprint: Item("Frantic Factory Lanky Blueprint", False, Types.Blueprint),
    Items.FranticFactoryTinyBlueprint: Item("Frantic Factory Tiny Blueprint", False, Types.Blueprint),
    Items.FranticFactoryChunkyBlueprint: Item("Frantic Factory Chunky Blueprint", False, Types.Blueprint),
    Items.GloomyGalleonDonkeyBlueprint: Item("Gloomy Galleon Donkey Blueprint", False, Types.Blueprint),
    Items.GloomyGalleonDiddyBlueprint: Item("Gloomy Galleon Diddy Blueprint", False, Types.Blueprint),
    Items.GloomyGalleonLankyBlueprint: Item("Gloomy Galleon Lanky Blueprint", False, Types.Blueprint),
    Items.GloomyGalleonTinyBlueprint: Item("Gloomy Galleon Tiny Blueprint", False, Types.Blueprint),
    Items.GloomyGalleonChunkyBlueprint: Item("Gloomy Galleon Chunky Blueprint", False, Types.Blueprint),
    Items.FungiForestDonkeyBlueprint: Item("Fungi Forest Donkey Blueprint", False, Types.Blueprint),
    Items.FungiForestDiddyBlueprint: Item("Fungi Forest Diddy Blueprint", False, Types.Blueprint),
    Items.FungiForestLankyBlueprint: Item("Fungi Forest Lanky Blueprint", False, Types.Blueprint),
    Items.FungiForestTinyBlueprint: Item("Fungi Forest Tiny Blueprint", False, Types.Blueprint),
    Items.FungiForestChunkyBlueprint: Item("Fungi Forest Chunky Blueprint", False, Types.Blueprint),
    Items.CrystalCavesDonkeyBlueprint: Item("Crystal Caves Donkey Blueprint", False, Types.Blueprint),
    Items.CrystalCavesDiddyBlueprint: Item("Crystal Caves Diddy Blueprint", False, Types.Blueprint),
    Items.CrystalCavesLankyBlueprint: Item("Crystal Caves Lanky Blueprint", False, Types.Blueprint),
    Items.CrystalCavesTinyBlueprint: Item("Crystal Caves Tiny Blueprint", False, Types.Blueprint),
    Items.CrystalCavesChunkyBlueprint: Item("Crystal Caves Chunky Blueprint", False, Types.Blueprint),
    Items.CreepyCastleDonkeyBlueprint: Item("Creepy Castle Donkey Blueprint", False, Types.Blueprint),
    Items.CreepyCastleDiddyBlueprint: Item("Creepy Castle Diddy Blueprint", False, Types.Blueprint),
    Items.CreepyCastleLankyBlueprint: Item("Creepy Castle Lanky Blueprint", False, Types.Blueprint),
    Items.CreepyCastleTinyBlueprint: Item("Creepy Castle Tiny Blueprint", False, Types.Blueprint),
    Items.CreepyCastleChunkyBlueprint: Item("Creepy Castle Chunky Blueprint", False, Types.Blueprint),
    Items.BananaHoard: Item("Banana Hoard", True, Types.Constant),
}
