"""Shuffles items for Item Rando."""

import random
import randomizer.Lists.Exceptions as Ex
from randomizer.Enums.Items import Items
from randomizer.Lists.Location import LocationList
from randomizer.Enums.Types import Types
from randomizer.Spoiler import Spoiler
from randomizer.Enums.Kongs import Kongs
from randomizer.Lists.Item import ItemList


class LocationSelection:
    """Class which contains information pertaining to assortment."""

    def __init__(self, *, vanilla_item=None, placement_data=None, is_reward_point=False, flag=None, kong=Kongs.any, location=None, name=""):
        """Initialize with given data."""
        self.name = name
        self.old_item = vanilla_item
        self.placement_data = placement_data
        self.old_flag = flag
        self.old_kong = kong
        self.reward_spot = is_reward_point
        self.location = location
        self.new_item = None
        self.new_flag = None
        self.new_kong = None

    def PlaceFlag(self, flag, kong):
        """Place item for assortment."""
        self.new_flag = flag
        self.new_kong = kong


def ShuffleItems(spoiler: Spoiler):
    """Shuffle items into assortment."""
    flag_dict = {}
    locations_not_needing_flags = []
    locations_needing_flags = []

    for location_enum in LocationList:
        item_location = LocationList[location_enum]
        # If location is a shuffled one...
        if item_location.default_mapid_data is not None and item_location.type in spoiler.settings.shuffled_location_types:
            # Create placement info for the patcher to use
            placement_info = {}
            for location in item_location.default_mapid_data:
                placement_info[location.map] = location.id
            location_selection = LocationSelection(
                vanilla_item=item_location.type,
                flag=item_location.default_mapid_data[0].flag,
                placement_data=placement_info,
                is_reward_point=item_location.is_reward,
                kong=item_location.default_mapid_data[0].kong,
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
                # If this item has a dedicated specific flag, then set it now (Keys and Coins right now)
                if new_item.rando_flag is not None:
                    location_selection.new_flag = new_item.rando_flag
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
            if item_location.type not in flag_dict.keys():
                if item_location.type == Types.Blueprint:
                    flag_dict[item_location.type] = {}
                    flag_dict[item_location.type][Kongs.donkey] = []
                    flag_dict[item_location.type][Kongs.diddy] = []
                    flag_dict[item_location.type][Kongs.lanky] = []
                    flag_dict[item_location.type][Kongs.tiny] = []
                    flag_dict[item_location.type][Kongs.chunky] = []
                else:
                    flag_dict[item_location.type] = []
            # Add this location's flag as a valid flag for this type of item/kong pairing
            if item_location.type == Types.Blueprint:
                flag_dict[item_location.type][item_location.default_mapid_data[0].kong].append(item_location.default_mapid_data[0].flag)
            else:
                flag_dict[item_location.type].append(item_location.default_mapid_data[0].flag)
    # Shuffle the list of locations needing flags so the flags are assigned randomly across seeds
    random.shuffle(locations_needing_flags)
    for location in locations_needing_flags:
        if location.new_flag is None:
            if location.new_item == Types.Blueprint:
                location.new_flag = flag_dict[location.new_item][location.new_kong].pop()
            else:
                location.new_flag = flag_dict[location.new_item].pop()

    # If we failed to give any location a flag, something is very wrong
    if any([data for data in locations_needing_flags if data.new_flag is None]):
        debug_flags = [data for data in locations_needing_flags if data.new_flag is None]
        raise Ex.FillException("ERROR: Failed to create a valid flag assignment for this fill!")
    spoiler.item_assignment = locations_needing_flags + locations_not_needing_flags
