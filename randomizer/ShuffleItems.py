"""Shuffles items for Item Rando."""

import random

import randomizer.Lists.Exceptions as Ex
from randomizer.Enums.Items import Items
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Settings import RandomPrices
from randomizer.Enums.Types import Types
from randomizer.Lists.Item import ItemList, NameFromKong
from randomizer.Lists.Location import LocationList
from randomizer.Spoiler import Spoiler


class LocationSelection:
    """Class which contains information pertaining to assortment."""

    def __init__(
        self,
        *,
        vanilla_item=None,
        placement_data=None,
        is_reward_point=False,
        flag=None,
        kong=Kongs.any,
        location=None,
        name="",
        is_shop=False,
        price=0,
        placement_index=0,
        can_have_item=True,
        can_place_item=True,
        shop_locked=False,
        shared=False,
        order=0,
        move_name="",
    ):
        """Initialize with given data."""
        self.name = name
        self.old_item = vanilla_item
        self.placement_data = placement_data
        self.old_flag = flag
        self.old_kong = kong
        self.reward_spot = is_reward_point
        self.location = location
        self.is_shop = is_shop
        self.price = price
        self.placement_index = placement_index
        self.can_have_item = can_have_item
        self.can_place_item = can_place_item
        self.shop_locked = shop_locked
        self.shared = shared
        self.order = order
        self.move_name = ""
        self.new_item = None
        self.new_flag = None
        self.new_kong = None
        self.new_subitem = None

    def PlaceFlag(self, flag, kong):
        """Place item for assortment."""
        self.new_flag = flag
        self.new_kong = kong


class MoveData:
    """Class which contains information pertaining to a move's attributes."""

    def __init__(self, subtype, kong, index, shared=False, count=1):
        """Initialize with given data."""
        self.subtype = subtype
        self.kong = kong
        self.index = index
        self.shared = shared
        self.count = count


move_list = {
    Items.BaboonBlast: MoveData(0, Kongs.donkey, 1),
    Items.ChimpyCharge: MoveData(0, Kongs.diddy, 1),
    Items.Orangstand: MoveData(0, Kongs.lanky, 1),
    Items.MiniMonkey: MoveData(0, Kongs.tiny, 1),
    Items.HunkyChunky: MoveData(0, Kongs.chunky, 1),
    Items.Coconut: MoveData(2, Kongs.donkey, 1),
    Items.Peanut: MoveData(2, Kongs.diddy, 1),
    Items.Grape: MoveData(2, Kongs.lanky, 1),
    Items.Feather: MoveData(2, Kongs.tiny, 1),
    Items.Pineapple: MoveData(2, Kongs.chunky, 1),
    Items.StrongKong: MoveData(0, Kongs.donkey, 2),
    Items.RocketbarrelBoost: MoveData(0, Kongs.diddy, 2),
    Items.Bongos: MoveData(4, Kongs.donkey, 1),
    Items.Guitar: MoveData(4, Kongs.diddy, 1),
    Items.Trombone: MoveData(4, Kongs.lanky, 1),
    Items.Saxophone: MoveData(4, Kongs.tiny, 1),
    Items.Triangle: MoveData(4, Kongs.chunky, 1),
    Items.GorillaGrab: MoveData(0, Kongs.donkey, 3),
    Items.SimianSpring: MoveData(0, Kongs.diddy, 3),
    Items.BaboonBalloon: MoveData(0, Kongs.lanky, 2),
    Items.PonyTailTwirl: MoveData(0, Kongs.tiny, 2),
    Items.PrimatePunch: MoveData(0, Kongs.chunky, 2),
    Items.ProgressiveAmmoBelt: MoveData(3, Kongs.any, 1, True, 2),
    Items.ProgressiveInstrumentUpgrade: MoveData(4, Kongs.any, 2, True, 3),
    Items.ProgressiveSlam: MoveData(1, Kongs.any, 2, True, 2),
    Items.HomingAmmo: MoveData(2, Kongs.any, 2, True, 1),
    Items.OrangstandSprint: MoveData(0, Kongs.lanky, 3),
    Items.Monkeyport: MoveData(0, Kongs.tiny, 3),
    Items.GorillaGone: MoveData(0, Kongs.chunky, 3),
    Items.SniperSight: MoveData(2, Kongs.any, 3, True, 1),
}


def ShuffleItems(spoiler: Spoiler):
    """Shuffle items into assortment."""
    progressive_move_flag_dict = {
        Items.ProgressiveSlam: [0x290, 0x291],
        Items.ProgressiveAmmoBelt: [0x292, 0x293],
        Items.ProgressiveInstrumentUpgrade: [0x294, 0x295, 0x296],
        Items.FakeItem: list(range(0x2AE, 0x2BE)),
    }
    junk_flag_dict = list(range(0x320, 0x320 + 100))
    flag_dict = {}
    blueprint_flag_dict = {}
    locations_not_needing_flags = []
    locations_needing_flags = []

    for location_enum in LocationList:
        item_location = LocationList[location_enum]
        # If location is a shuffled one...
        if (
            (
                item_location.default_mapid_data is not None
                or item_location.type in (Types.Shop, Types.Shockwave)
                or (
                    item_location.type == Types.TrainingBarrel and not item_location.constant
                )  # Depending on starting moves, training barrels can be empty (only when constant). This quick check prevents weirdness later in this method.
            )
            and not item_location.inaccessible
            and item_location.type in spoiler.settings.shuffled_location_types
        ):
            # Create placement info for the patcher to use
            placement_info = {}
            # Items that need specific placement in the world, either as a reward or something spawned in
            if item_location.default_mapid_data:
                for location in item_location.default_mapid_data:
                    placement_info[location.map] = location.id
                old_flag = item_location.default_mapid_data[0].flag
                old_kong = item_location.default_mapid_data[0].kong
                placement_index = [-1]  # Irrelevant for non-shop locations
            # Shop locations: Cranky, Funky, Candy, Training Barrels, and BFI
            else:
                old_flag = -1  # Irrelevant for shop locations
                old_kong = item_location.kong
                placement_index = item_location.placement_index
            price = 0
            if item_location.type == Types.Shop:
                # Vanilla prices are based on item, not location
                if spoiler.settings.random_prices == RandomPrices.vanilla:
                    # If it's not in the prices dictionary, the item is free
                    if item_location.item in spoiler.settings.prices.keys():
                        price = spoiler.settings.prices[item_location.item]
                else:
                    price = spoiler.settings.prices[location_enum]
            location_selection = LocationSelection(
                vanilla_item=ItemList[item_location.default].type,
                flag=old_flag,
                placement_data=placement_info,
                is_reward_point=item_location.is_reward,
                is_shop=item_location.type in (Types.Shop, Types.TrainingBarrel, Types.Shockwave),
                price=price,
                placement_index=placement_index,
                kong=old_kong,
                location=location_enum,
                name=item_location.name,
            )
            # Get the item at this location
            if item_location.item is None or item_location.item == Items.NoItem:
                new_item = None
            else:
                new_item = ItemList[item_location.item]
            # If this location isn't empty, set the new item and required kong
            if new_item is not None:
                location_selection.new_item = new_item.type
                location_selection.new_kong = new_item.kong
                location_selection.new_subitem = item_location.item
                # If this item has a dedicated specific flag, then set it now (Moves, Kongs, andKeys right now)
                if new_item.rando_flag is not None or new_item.type == Types.FakeItem:
                    if new_item.rando_flag == -1 or new_item.type == Types.FakeItem:  # This means it's a progressive move or fake item and they need special flags
                        location_selection.new_flag = progressive_move_flag_dict[item_location.item].pop()
                    else:
                        location_selection.new_flag = new_item.rando_flag
                    locations_not_needing_flags.append(location_selection)
                # Company Coins keep their original flag
                elif new_item.type == Types.Coin:
                    location_selection.new_flag = new_item.flag
                    locations_not_needing_flags.append(location_selection)
                elif new_item.type == Types.JunkItem:
                    location_selection.new_flag = junk_flag_dict.pop()
                    locations_not_needing_flags.append(location_selection)
                # Otherwise we need to put it in the list of locations needing flags
                else:
                    locations_needing_flags.append(location_selection)
            # If this location is empty, it doesn't need a flag and we need to None out these fields
            else:
                location_selection.new_item = None
                location_selection.new_kong = None
                location_selection.new_flag = None
                locations_not_needing_flags.append(location_selection)
            # Add this location's flag to the lists of available flags by location
            # Initialize relevant list if it doesn't exist
            if item_location.type not in flag_dict.keys() and item_location.type != Types.Blueprint:
                flag_dict[item_location.type] = []
            # Add this location's vanilla flag as a valid flag for this type of item/kong pairing
            vanilla_item_type = ItemList[item_location.default].type
            if item_location.type == Types.Shop:  # Except for shop locations - many of these are non-vanilla locations and won't have a valid vanilla item
                flag_dict[item_location.type].append(old_flag)
            # Link blueprint Items to their default flags stored in their Location
            elif item_location.type == Types.Blueprint:
                blueprint_flag_dict[item_location.default] = item_location.default_mapid_data[0].flag
            else:
                flag_dict[vanilla_item_type].append(old_flag)
    # Shuffle the list of locations needing flags so the flags are assigned randomly across seeds
    random.shuffle(locations_needing_flags)
    for location in locations_needing_flags:
        if location.new_flag is None:
            if location.new_item == Types.Blueprint:
                location.new_flag = blueprint_flag_dict[LocationList[location.location].item]
            else:
                location.new_flag = flag_dict[location.new_item].pop()

    # If we failed to give any location a flag, something is very wrong
    if any([data for data in locations_needing_flags if data.new_flag is None]):
        debug_flags = [data for data in locations_needing_flags if data.new_flag is None]
        raise Ex.FillException("ERROR: Failed to create a valid flag assignment for this fill!")
    spoiler.item_assignment = locations_needing_flags + locations_not_needing_flags
    # Generate human-readable version for debugging purposes
    human_item_data = {}
    for loc in spoiler.item_assignment:
        name = "Nothing"
        if loc.new_item is not None:
            name = ItemList[LocationList[loc.location].item].name
        location_name = loc.name
        if "Kasplat" in location_name:
            location_name = f"{location_name.split('Kasplat')[0]} {NameFromKong(loc.old_kong)} Kasplat"
        human_item_data[location_name] = name
    spoiler.debug_human_item_assignment = human_item_data
