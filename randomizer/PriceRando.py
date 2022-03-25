"""Randomize Price Locations."""
from randomizer.Enums.Locations import Locations
from randomizer.Patcher import ROM
from randomizer.Spoiler import Spoiler

def randomize_prices(spoiler: Spoiler):
    """Write prices to ROM variable space based on settings"""
    if spoiler.settings.random_prices != "vanilla" or spoiler.settings.shuffle_items != "none":
        varspaceOffset = 0x1FED020  # TODO: Define this as constant in a more global place
        pricesOffset = 0x035
        ROM().seek(varspaceOffset + pricesOffset)
        # /* 0x035 */ char price_rando_on; // 0 = Price Randomizer off, 1 = On
        if (spoiler.settings.random_prices != "vanilla"):
            ROM().write(1)
        else:
            ROM().write(0)
        # 0x036 */ unsigned char special_move_prices[5][3]; // Array of an array of prices [[1,2,3],[1,2,3],[1,2,3],[1,2,3],[1,2,3]]. Each item of the parent array is for a kong, each item of the sub arrays is the price of the moves in order of their vanilla purchase (eg. DK: Baboon Blast > Strong Kong > Gorilla Grab)
        ROM().write(spoiler.settings.prices[Locations.BaboonBlast])
        ROM().write(spoiler.settings.prices[Locations.StrongKong])
        ROM().write(spoiler.settings.prices[Locations.GorillaGrab])
        ROM().write(spoiler.settings.prices[Locations.ChimpyCharge])
        ROM().write(spoiler.settings.prices[Locations.RocketbarrelBoost])
        ROM().write(spoiler.settings.prices[Locations.SimianSpring])
        ROM().write(spoiler.settings.prices[Locations.Orangstand])
        ROM().write(spoiler.settings.prices[Locations.BaboonBalloon])
        ROM().write(spoiler.settings.prices[Locations.OrangstandSprint])
        ROM().write(spoiler.settings.prices[Locations.MiniMonkey])
        ROM().write(spoiler.settings.prices[Locations.PonyTailTwirl])
        ROM().write(spoiler.settings.prices[Locations.Monkeyport])
        ROM().write(spoiler.settings.prices[Locations.HunkyChunky])
        ROM().write(spoiler.settings.prices[Locations.PrimatePunch])
        ROM().write(spoiler.settings.prices[Locations.GorillaGone])
        # /* 0x045 */ unsigned char slam_prices[2]; // Array of simian slam upgrade prices: [1,2]. First item is super simian slam (blue), 2nd is super duper simian slam (red)
        ROM().write(spoiler.settings.prices[Locations.SuperSimianSlam])
        ROM().write(spoiler.settings.prices[Locations.SuperDuperSimianSlam])
        # /* 0x047 */ unsigned char gun_prices[5]; // Array of prices for the base gun for each kong. [1,2,3,4,5]. 1 item for each kong
        ROM().write(spoiler.settings.prices[Locations.CoconutGun])
        ROM().write(spoiler.settings.prices[Locations.PeanutGun])
        ROM().write(spoiler.settings.prices[Locations.GrapeGun])
        ROM().write(spoiler.settings.prices[Locations.FeatherGun])
        ROM().write(spoiler.settings.prices[Locations.PineappleGun])
        # /* 0x04C */ unsigned char instrument_prices[5]; // Array of prices for the base instrument for each kong. [1,2,3,4,5]. 1 item for each kong
        ROM().write(spoiler.settings.prices[Locations.Bongos])
        ROM().write(spoiler.settings.prices[Locations.Guitar])
        ROM().write(spoiler.settings.prices[Locations.Trombone])
        ROM().write(spoiler.settings.prices[Locations.Saxophone])
        ROM().write(spoiler.settings.prices[Locations.Triangle])
        # /* 0x051 */ unsigned char gun_upgrade_prices[2]; // Array of gun upgrade prices: [1,2]. First item is homing ammo upgrade. 2nd is Sniper Scope (Zoom)
        ROM().write(spoiler.settings.prices[Locations.HomingAmmo])
        ROM().write(spoiler.settings.prices[Locations.SniperSight])
        # /* 0x053 */ unsigned char ammo_belt_prices[2]; // Array of ammo belt prices: [1,2]. 1 item for each level of ammo belt
        ROM().write(spoiler.settings.prices[Locations.AmmoBelt1])
        ROM().write(spoiler.settings.prices[Locations.AmmoBelt2])
        # /* 0x055 */ unsigned char instrument_upgrade_prices[3]; // Array of instrument upgrade prices: [1,2,3]. 1st and 3rd items are the Upgrades 1 and 2 respectively. 2nd item is the 3rd melon cost
        ROM().write(spoiler.settings.prices[Locations.MusicUpgrade1])
        ROM().write(spoiler.settings.prices[Locations.ThirdMelon])
        ROM().write(spoiler.settings.prices[Locations.MusicUpgrade2])
        