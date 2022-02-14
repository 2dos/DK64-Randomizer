"""Functions and data for setting and calculating prices."""

from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Locations import Locations
from randomizer.ItemPool import DonkeyMoveLocations, DiddyMoveLocations, LankyMoveLocations, TinyMoveLocations, ChunkyMoveLocations, SharedMoveLocations

VanillaPrices = {
    Locations.SuperSimianSlam: 5,
    Locations.SuperDuperSimianSlam: 7,
    Locations.BaboonBlast: 3,
    Locations.StrongKong: 5,
    Locations.GorillaGrab: 7,
    Locations.ChimpyCharge: 3,
    Locations.RocketbarrelBoost: 5,
    Locations.SimianSpring: 7,
    Locations.Orangstand: 3,
    Locations.BaboonBalloon: 5,
    Locations.OrangstandSprint: 7,
    Locations.MiniMonkey: 3,
    Locations.PonyTailTwirl: 5,
    Locations.Monkeyport: 7,
    Locations.HunkyChunky: 3,
    Locations.PrimatePunch: 5,
    Locations.GorillaGone: 7,
    Locations.CoconutGun: 3,
    Locations.PeanutGun: 3,
    Locations.GrapeGun: 3,
    Locations.FeatherGun: 3,
    Locations.PineappleGun: 3,
    Locations.AmmoBelt1: 3,
    Locations.HomingAmmo: 5,
    Locations.AmmoBelt2: 5,
    Locations.SniperSight: 7,
    Locations.Bongos: 3,
    Locations.Guitar: 3,
    Locations.Trombone: 3,
    Locations.Saxophone: 3,
    Locations.Triangle: 3,
    Locations.MusicUpgrade1: 5,
    Locations.ThirdMelon: 7,
    Locations.MusicUpgrade2: 9,
}

# Get the maximum amount of coins the given kong can spend
def GetMaxForKong(settings, kong):
    total = sum([value for key, value in settings.prices.items() if key in SharedMoveLocations])
    if kong == Kongs.donkey:
        total += sum([value for key, value in settings.prices.items() if key in DonkeyMoveLocations])
    elif kong == Kongs.diddy:
        total += sum([value for key, value in settings.prices.items() if key in DiddyMoveLocations])
    elif kong == Kongs.lanky:
        total += sum([value for key, value in settings.prices.items() if key in LankyMoveLocations])
    elif kong == Kongs.tiny:
        total += sum([value for key, value in settings.prices.items() if key in TinyMoveLocations])
    else:  # chunky
        total += sum([value for key, value in settings.prices.items() if key in ChunkyMoveLocations])
    return total

CrankySequence = [
    Locations.SuperSimianSlam,
    Locations.SuperDuperSimianSlam
]
FunkySequence = [
    [Locations.CoconutGun, Locations.PeanutGun, Locations.GrapeGun, Locations.FeatherGun, Locations.PineappleGun],
    Locations.AmmoBelt1,
    Locations.HomingAmmo,
    Locations.AmmoBelt2,
    Locations.SniperSight,
]
CandySequence = [
    [Locations.Bongos, Locations.Guitar, Locations.Trombone, Locations.Saxophone, Locations.Triangle],
    Locations.MusicUpgrade1,
    Locations.ThirdMelon,
    Locations.MusicUpgrade2,
]
DonkeySequence = [
    Locations.BaboonBlast,
    Locations.StrongKong,
    Locations.GorillaGrab,
]
DiddySequence = [
    Locations.ChimpyCharge,
    Locations.RocketbarrelBoost,
    Locations.SimianSpring,
]
LankySequence = [
    Locations.Orangstand,
    Locations.BaboonBalloon,
    Locations.OrangstandSprint,
]
TinySequence = [
    Locations.MiniMonkey,
    Locations.PonyTailTwirl,
    Locations.Monkeyport,
]
ChunkySequence = [
    Locations.HunkyChunky,
    Locations.PrimatePunch,
    Locations.GorillaGone,
]
Sequences = [
    CrankySequence,
    FunkySequence,
    CandySequence,
    DonkeySequence,
    DiddySequence,
    LankySequence,
    TinySequence,
    ChunkySequence,
]

"""
So for coin logic, we want to make sure the player can't spend coins incorrectly and lock themselves out.
This means every buyable item has to account for, potentially, buying every other possible item first.
So each price will be inflated by a lot for logic purposes.
Total prices are as follows, in vanilla:
Cranky generic: 12
Cranky specific: 15
Candy generic: 21
Candy specific: 3
Funky generic: 20
Funky specific: 3
Total one kong can possibly spend: 74

The following only applies if move locations are not decoupled, meaning certain locations must be bought in sequence:
So basically, whatever "line" the kong is buying from, need to subtract prices
from future entries in that line from 74 (or whatever the max is if prices are random).
So since Cranky's upgrades cost 3, 5, and 7, the logical price of his
first upgrade will be 74 - 7 - 5 = 62.
Since prices can be randomized, we will dynamically subtract the prices of future purchases
in any given sequence.

If moves are decoupled so that they don't need be bought in sequence, then any location could be the final location,
meaning we just must consider the maximum price for every location.
"""

def KongCanBuy(location, coins, settings, kong):
    """Check if given kong can logically purchase the specified location."""
    # Special case: If shop moves are unlocked then all are already bought except scope
    if settings.unlock_all_moves and location == Locations.SniperSight:
        return coins[kong] >= settings.prices[location] 
    # Get the max coins this kong can possibly spend
    max = GetMaxForKong(settings, kong)
    # If locations can be bought in any order, just check greater than the max
    if settings.shuffle_items != "none":
        return coins[kong] >= max
    # Else, can subtract future entries in the item's sequence from the price
    # Find which sequence this location belongs to
    sequence = None
    for seq in Sequences:
        # If given location is in this sequence, or in the first element of the sequence if it's a list
        if location in seq or (isinstance(seq[0], list) and location in seq[0]):
            sequence = seq
            break
    # Now set the initial price as the max, but subtract amount from future entries in sequence
    price = max
    i = len(sequence) - 1
    # Don't check first item in sequence since there's no reason to
    while i > 0:
        if sequence[i] == location:
            break
        price -= settings.prices[sequence[i]]
        i -= 1
    # Now that the final price has been determined, check if kong can afford it
    return coins[kong] >= price


def AnyKongCanBuy(location, coins, settings):
    for kong in [Kongs.donkey, Kongs.diddy, Kongs.lanky, Kongs.tiny, Kongs.chunky]:
        if KongCanBuy(location, coins, settings, kong):
            return True
    return False

def CanBuy(location, coins, settings):
    """Check if an appropriate kong can logically purchase this location."""
    if location in DonkeyMoveLocations:
        return KongCanBuy(location, coins, settings, Kongs.donkey)
    elif location in DiddyMoveLocations:
        return KongCanBuy(location, coins, settings, Kongs.diddy)
    elif location in LankyMoveLocations:
        return KongCanBuy(location, coins, settings, Kongs.lanky)
    elif location in TinyMoveLocations:
        return KongCanBuy(location, coins, settings, Kongs.tiny)
    elif location in ChunkyMoveLocations:
        return KongCanBuy(location, coins, settings, Kongs.chunky)
    else:  # Shared locations
        return AnyKongCanBuy(location, coins, settings)
