"""Functions and data for setting and calculating prices."""

from math import ceil
import random

from randomizer.Enums.Items import Items
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Locations import Locations
from randomizer.ItemPool import TrainingBarrelAbilities
from randomizer.Lists.Location import ChunkyMoveLocations, DiddyMoveLocations, DonkeyMoveLocations, LankyMoveLocations, LocationList, SharedMoveLocations, TinyMoveLocations, TrainingBarrelLocations

VanillaPrices = {
    Items.Vines: 0,
    Items.Swim: 0,
    Items.Barrels: 0,
    Items.Oranges: 0,
    Items.Camera: 0,
    Items.Shockwave: 0,
    Items.CameraAndShockwave: 0,
    Items.BaboonBlast: 3,
    Items.StrongKong: 5,
    Items.GorillaGrab: 7,
    Items.ChimpyCharge: 3,
    Items.RocketbarrelBoost: 5,
    Items.SimianSpring: 7,
    Items.Orangstand: 3,
    Items.BaboonBalloon: 5,
    Items.OrangstandSprint: 7,
    Items.MiniMonkey: 3,
    Items.PonyTailTwirl: 5,
    Items.Monkeyport: 7,
    Items.HunkyChunky: 3,
    Items.PrimatePunch: 5,
    Items.GorillaGone: 7,
    Items.Coconut: 3,
    Items.Peanut: 3,
    Items.Grape: 3,
    Items.Feather: 3,
    Items.Pineapple: 3,
    Items.HomingAmmo: 5,
    Items.SniperSight: 7,
    Items.Bongos: 3,
    Items.Guitar: 3,
    Items.Trombone: 3,
    Items.Saxophone: 3,
    Items.Triangle: 3,
    Items.ProgressiveSlam: [5, 7],
    Items.ProgressiveAmmoBelt: [3, 5],
    Items.ProgressiveInstrumentUpgrade: [5, 7, 9],
}

ProgressiveMoves = {
    Items.ProgressiveSlam: 2,
    Items.ProgressiveAmmoBelt: 2,
    Items.ProgressiveInstrumentUpgrade: 3,
}


def GetPriceWeights(weight):
    """Get the parameters for the price distribution."""
    # Each kong can buy up to 14 items
    # Vanilla: Can spend up to 74 coins, avg. price per item 5.2857
    # Low: 1-4 coins most of the time
    # Medium: 1-8 coins most of the time
    # High: 1-12 coins (cannot be greater than 12)
    # Extreme: Average of 11, can be up to 15, requires starting with Shockwave
    # Free: All moves are zero coins
    avg = 4.5
    stddev = 2
    upperLimit = 9
    if weight == "high":
        avg = 6.5
        stddev = 3
        upperLimit = 12
    elif weight == "low":
        avg = 2.5
        stddev = 1
        upperLimit = 6
    elif weight == "extreme":
        avg = 11
        stddev = 2
        upperLimit = 15
    return (avg, stddev, upperLimit)


def RandomizePrices(weight):
    """Generate randomized prices based on given weight (free, low, medium, or high)."""
    prices = VanillaPrices.copy()
    parameters = GetPriceWeights(weight)
    # Generate random prices using normal distribution with avg and std. deviation
    # Round each price to nearest int
    for item in prices.keys():
        # Special Case for progressive moves, supply an array of prices, one for each time it appears
        if item in ProgressiveMoves.keys():
            prices[item] = []
            for i in range(ProgressiveMoves[item]):
                prices[item].append(GenerateRandomPrice(weight, parameters[0], parameters[1], parameters[2]))
        else:
            prices[item] = GenerateRandomPrice(weight, parameters[0], parameters[1], parameters[2])
            # Make training barrel moves cheaper because they'll be early and are super important
            if item in TrainingBarrelAbilities():
                prices[item] = ceil(prices[item] * 0.5)
    return prices


def GenerateRandomPrice(weight, avg, stddev, upperLimit):
    """Generate a random price to assign."""
    lowerLimit = 1
    if weight == "free":
        newPrice = 0
    else:
        newPrice = round(random.normalvariate(avg, stddev))
        if newPrice < lowerLimit:
            newPrice = lowerLimit
        elif newPrice > upperLimit:
            newPrice = upperLimit
    return newPrice


def GetMaxForKong(settings, kong):
    """Get the maximum amount of coins the given kong can spend."""
    # Track shared moves specifically because their prices are stored specially
    found_slams = 0
    found_instrument_upgrades = 0
    found_ammo_belts = 0
    total_price = 0
    # Look for moves placed in shared move locations that have prices
    paidSharedMoveLocations = SharedMoveLocations - TrainingBarrelLocations - {Locations.CameraAndShockwave}
    for location in paidSharedMoveLocations:
        item_id = LocationList[location].item
        if item_id is not None and item_id != Items.NoItem:
            if item_id == Items.ProgressiveSlam:
                total_price += settings.prices[item_id][found_slams]
                found_slams += 1
            elif item_id == Items.ProgressiveInstrumentUpgrade:
                total_price += settings.prices[item_id][found_instrument_upgrades]
                found_instrument_upgrades += 1
            elif item_id == Items.ProgressiveAmmoBelt:
                total_price += settings.prices[item_id][found_ammo_belts]
                found_ammo_belts += 1

            else:
                total_price += settings.prices[item_id]

    kongMoveLocations = DiddyMoveLocations.copy()
    if kong == Kongs.donkey:
        kongMoveLocations = DonkeyMoveLocations.copy()
        total_price += 2  # For Arcade round 2
    elif kong == Kongs.lanky:
        kongMoveLocations = LankyMoveLocations.copy()
    elif kong == Kongs.tiny:
        kongMoveLocations = TinyMoveLocations.copy()
    elif kong == Kongs.chunky:
        kongMoveLocations = ChunkyMoveLocations.copy()

    for location in kongMoveLocations:
        item_id = LocationList[location].item
        if item_id is not None and item_id != Items.NoItem:
            if item_id == Items.ProgressiveSlam:
                total_price += settings.prices[item_id][found_slams]
                found_slams += 1
            elif item_id == Items.ProgressiveInstrumentUpgrade:
                total_price += settings.prices[item_id][found_instrument_upgrades]
                found_instrument_upgrades += 1
            elif item_id == Items.ProgressiveAmmoBelt:
                total_price += settings.prices[item_id][found_ammo_belts]
                found_ammo_belts += 1
            else:
                total_price += settings.prices[item_id]
    return total_price


SlamProgressiveSequence = [Locations.SuperSimianSlam, Locations.SuperDuperSimianSlam]
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
    SlamProgressiveSequence,
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


def GetPriceOfMoveItem(item, settings, slamLevel, ammoBelts, instUpgrades):
    """Get price of a move item. Needs to know current level of owned progressive moves to give correct price for progressive items."""
    # We may not have a price for this item and need to generate one - this should only happen in full item rando
    if item == Items.ProgressiveSlam:
        if item not in settings.prices.keys():
            parameters = GetPriceWeights(settings.random_prices)
            settings.prices[item] = [
                GenerateRandomPrice(settings.random_prices, parameters[0], parameters[1], parameters[2]),
                GenerateRandomPrice(settings.random_prices, parameters[0], parameters[1], parameters[2]),
            ]
        if slamLevel in [1, 2]:
            return settings.prices[item][slamLevel - 1]
        else:
            # If already have max slam, there's move to buy
            return None
    elif item == Items.ProgressiveAmmoBelt:
        if item not in settings.prices.keys():
            parameters = GetPriceWeights(settings.random_prices)
            settings.prices[item] = [
                GenerateRandomPrice(settings.random_prices, parameters[0], parameters[1], parameters[2]),
                GenerateRandomPrice(settings.random_prices, parameters[0], parameters[1], parameters[2]),
            ]
        if ammoBelts in [0, 1]:
            return settings.prices[item][ammoBelts]
        else:
            # If already have max ammo belt, there's move to buy
            return None
    elif item == Items.ProgressiveInstrumentUpgrade:
        if item not in settings.prices.keys():
            parameters = GetPriceWeights(settings.random_prices)
            settings.prices[item] = [
                GenerateRandomPrice(settings.random_prices, parameters[0], parameters[1], parameters[2]),
                GenerateRandomPrice(settings.random_prices, parameters[0], parameters[1], parameters[2]),
                GenerateRandomPrice(settings.random_prices, parameters[0], parameters[1], parameters[2]),
            ]
        if instUpgrades in [0, 1, 2]:
            return settings.prices[item][instUpgrades]
        else:
            # If already have max instrument upgrade, there's move to buy
            return None
    else:
        if item not in settings.prices.keys():
            parameters = GetPriceWeights(settings.random_prices)
            settings.prices[item] = GenerateRandomPrice(settings.random_prices, parameters[0], parameters[1], parameters[2])
        return settings.prices[item]


def KongCanBuy(location, logic, kong):
    """Check if given kong can logically purchase the specified location."""
    # If nothing is sold here, return true
    if LocationList[location].item is None or LocationList[location].item == Items.NoItem:
        return True
    price = GetPriceOfMoveItem(LocationList[location].item, logic.settings, logic.Slam, logic.AmmoBelts, logic.InstUpgrades)

    # Simple price check - combination of purchases will be considered outside this method
    if price is not None:
        # print("KongCanBuy checking item: " + str(LocationList[location].item))
        # print("for kong: " + kong.name + " with " + str(coins[kong]) + " coins")
        # print("has price: " + str(price))
        return logic.Coins[kong] >= price
    else:
        return False


def AnyKongCanBuy(location, logic):
    """Check if any kong can logically purchase this location."""
    return any(KongCanBuy(location, logic, kong) for kong in [Kongs.donkey, Kongs.diddy, Kongs.lanky, Kongs.tiny, Kongs.chunky])


def EveryKongCanBuy(location, logic):
    """Check if any kong can logically purchase this location."""
    return all(KongCanBuy(location, logic, kong) for kong in [Kongs.donkey, Kongs.diddy, Kongs.lanky, Kongs.tiny, Kongs.chunky])


def CanBuy(location, logic):
    """Check if an appropriate kong can logically purchase this location."""
    # If it's in a location that doesn't care about prices, it's free!
    if location in TrainingBarrelLocations or location == Locations.CameraAndShockwave:
        return True
    # Either have the setting that any kong can buy any move or it's a shared location so any kong can anyway
    if location in SharedMoveLocations:
        return AnyKongCanBuy(location, logic)
    # Else a specific kong is required to buy it, so check that that's the current kong and they have enough coins
    elif location in DonkeyMoveLocations:
        return KongCanBuy(location, logic, Kongs.donkey)
    elif location in DiddyMoveLocations:
        return KongCanBuy(location, logic, Kongs.diddy)
    elif location in LankyMoveLocations:
        return KongCanBuy(location, logic, Kongs.lanky)
    elif location in TinyMoveLocations:
        return KongCanBuy(location, logic, Kongs.tiny)
    elif location in ChunkyMoveLocations:
        return KongCanBuy(location, logic, Kongs.chunky)
