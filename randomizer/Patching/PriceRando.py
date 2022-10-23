"""Randomize Price Locations."""
from randomizer.Enums.Items import Items
from randomizer.Patching.Patcher import ROM
from randomizer.Spoiler import Spoiler


def randomize_prices(spoiler: Spoiler):
    """Write prices to ROM variable space based on settings."""
    if spoiler.settings.random_prices != "vanilla" or spoiler.settings.shuffle_items != "none":
        varspaceOffset = spoiler.settings.rom_data
        pricesOffset = 0x035
        tbarrelPricesOffset = 0x0A8
        fairyPricesOffset = 0x0AC
        ROM().seek(varspaceOffset + pricesOffset)
        # /* 0x035 */ char price_rando_on; // 0 = Price Randomizer off, 1 = On
        if spoiler.settings.random_prices != "vanilla":
            ROM().write(1)
        else:
            ROM().write(0)
        # 0x036 */ unsigned char special_move_prices[5][3]; // Array of an array of prices [[1,2,3],[1,2,3],[1,2,3],[1,2,3],[1,2,3]]. Each item of the parent array is for a kong, each item of the sub arrays is the price of the moves in order of their vanilla purchase (eg. DK: Baboon Blast > Strong Kong > Gorilla Grab)
        
        items_with_prices = [
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
            Items.Coconut,
            Items.Peanut,
            Items.Grape,
            Items.Feather,
            Items.Pineapple,
            Items.Bongos,
            Items.Guitar,
            Items.Trombone,
            Items.Saxophone,
            Items.Triangle,
            Items.HomingAmmo,
            Items.SniperSight,
            Items.Swim,
            Items.Oranges,
            Items.Barrels,
            Items.Vines,
            Items.Camera,
            Items.Shockwave,
            Items.CameraAndShockwave,
        ]
        for item in items_with_prices:
            if item not in spoiler.settings.prices:
                spoiler.settings.prices[item] = 0
        progressive_items = {
            Items.ProgressiveAmmoBelt: 2,
            Items.ProgressiveInstrumentUpgrade: 3,
            Items.ProgressiveSlam: 2,
        }
        for item in progressive_items:
            if item not in spoiler.settings.prices:
                spoiler.settings.prices[item] = []
            length = progressive_items[item]
            if len(spoiler.settings.prices[item]) < length:
                diff = length - len(spoiler.settings.prices[item])
                for d in range(diff):
                    spoiler.settings.prices[item].append(0)
        ROM().write(spoiler.settings.prices[Items.BaboonBlast])
        ROM().write(spoiler.settings.prices[Items.StrongKong])
        ROM().write(spoiler.settings.prices[Items.GorillaGrab])
        ROM().write(spoiler.settings.prices[Items.ChimpyCharge])
        ROM().write(spoiler.settings.prices[Items.RocketbarrelBoost])
        ROM().write(spoiler.settings.prices[Items.SimianSpring])
        ROM().write(spoiler.settings.prices[Items.Orangstand])
        ROM().write(spoiler.settings.prices[Items.BaboonBalloon])
        ROM().write(spoiler.settings.prices[Items.OrangstandSprint])
        ROM().write(spoiler.settings.prices[Items.MiniMonkey])
        ROM().write(spoiler.settings.prices[Items.PonyTailTwirl])
        ROM().write(spoiler.settings.prices[Items.Monkeyport])
        ROM().write(spoiler.settings.prices[Items.HunkyChunky])
        ROM().write(spoiler.settings.prices[Items.PrimatePunch])
        ROM().write(spoiler.settings.prices[Items.GorillaGone])
        # /* 0x045 */ unsigned char slam_prices[2]; // Array of simian slam upgrade prices: [1,2]. First item is super simian slam (blue), 2nd is super duper simian slam (red)
        ROM().write(spoiler.settings.prices[Items.ProgressiveSlam][0])
        ROM().write(spoiler.settings.prices[Items.ProgressiveSlam][1])
        # /* 0x047 */ unsigned char gun_prices[5]; // Array of prices for the base gun for each kong. [1,2,3,4,5]. 1 item for each kong
        ROM().write(spoiler.settings.prices[Items.Coconut])
        ROM().write(spoiler.settings.prices[Items.Peanut])
        ROM().write(spoiler.settings.prices[Items.Grape])
        ROM().write(spoiler.settings.prices[Items.Feather])
        ROM().write(spoiler.settings.prices[Items.Pineapple])
        # /* 0x04C */ unsigned char instrument_prices[5]; // Array of prices for the base instrument for each kong. [1,2,3,4,5]. 1 item for each kong
        ROM().write(spoiler.settings.prices[Items.Bongos])
        ROM().write(spoiler.settings.prices[Items.Guitar])
        ROM().write(spoiler.settings.prices[Items.Trombone])
        ROM().write(spoiler.settings.prices[Items.Saxophone])
        ROM().write(spoiler.settings.prices[Items.Triangle])
        # /* 0x051 */ unsigned char gun_upgrade_prices[2]; // Array of gun upgrade prices: [1,2]. First item is homing ammo upgrade. 2nd is Sniper Scope (Zoom)
        ROM().write(spoiler.settings.prices[Items.HomingAmmo])
        ROM().write(spoiler.settings.prices[Items.SniperSight])
        # /* 0x053 */ unsigned char ammo_belt_prices[2]; // Array of ammo belt prices: [1,2]. 1 item for each level of ammo belt
        ROM().write(spoiler.settings.prices[Items.ProgressiveAmmoBelt][0])
        ROM().write(spoiler.settings.prices[Items.ProgressiveAmmoBelt][1])
        # /* 0x055 */ unsigned char instrument_upgrade_prices[3]; // Array of instrument upgrade prices: [1,2,3]. 1st and 3rd items are the Upgrades 1 and 2 respectively. 2nd item is the 3rd melon cost
        ROM().write(spoiler.settings.prices[Items.ProgressiveInstrumentUpgrade][0])
        ROM().write(spoiler.settings.prices[Items.ProgressiveInstrumentUpgrade][1])
        ROM().write(spoiler.settings.prices[Items.ProgressiveInstrumentUpgrade][2])

        # /* 0x0A8 */ unsigned char tbarrel_prices[4]; // Array of training barrel move prices in this order: Swim, Oranges, Barrels, Vines
        ROM().seek(varspaceOffset + tbarrelPricesOffset)
        ROM().write(spoiler.settings.prices[Items.Swim])
        ROM().write(spoiler.settings.prices[Items.Oranges])
        ROM().write(spoiler.settings.prices[Items.Barrels])
        ROM().write(spoiler.settings.prices[Items.Vines])

        # /* 0x0A8 */ unsigned char fairy_prices[2]; // Array of training barrel move prices in this order: Swim, Oranges, Barrels, Vines
        ROM().seek(varspaceOffset + fairyPricesOffset)
        if spoiler.settings.shockwave_status == "shuffled_decoupled":
            ROM().write(spoiler.settings.prices[Items.Camera])
            ROM().write(spoiler.settings.prices[Items.Shockwave])
        else:
            ROM().write(spoiler.settings.prices[Items.CameraAndShockwave])
