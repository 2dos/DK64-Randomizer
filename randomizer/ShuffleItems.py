"""Shuffles items for Item Rando."""

import random
import copy
from randomizer.Lists.Location import LocationList
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Types import Types
from randomizer.Spoiler import Spoiler
from randomizer.Enums.Kongs import Kongs


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
        self.placed = False

    def place(self, item, flag, kong):
        """Place item for assortment."""
        self.new_item = item
        self.new_flag = flag
        self.new_kong = kong
        self.placed = True


def ShuffleItems(spoiler: Spoiler):
    """Shuffle items into assortment."""
    spoiler.shuffled_item_types = (
        Types.Banana,
        Types.Blueprint,
        Types.Coin,
        Types.Key,
        Types.Crown,
        Types.Medal,
    )
    location_data = []
    for location_enum in LocationList:
        item_location = LocationList[location_enum]
        if item_location.default_mapid_data is not None and item_location.type in spoiler.shuffled_item_types:
            # Can be shuffled
            placement_info = {}
            is_reward = False
            for location in item_location.default_mapid_data:
                placement_info[location.map] = location.id
                if location.id == -1:
                    is_reward = True
            location_data.append(
                LocationSelection(
                    vanilla_item=item_location.type,
                    flag=item_location.default_mapid_data[0].flag,
                    placement_data=placement_info,
                    is_reward_point=is_reward,
                    kong=item_location.default_mapid_data[0].kong,
                    location=location_enum,
                    name=item_location.name,
                )
            )
    reward_items = (
        # Items which can be spawned as an actor
        Types.Banana,  # Actor 45
        Types.Blueprint,  # HAS to correspond to intended actor for item, actors 75-79 (Diddy, Chunky, Lanky, DK, Tiny)
        Types.Key,  # Actor 72
        Types.Crown,  # Actor 86
    )
    bad_bp_locations = (
        Locations.IslesDonkeyJapesRock,
        Locations.JapesDonkeyFrontofCage,
        Locations.JapesDonkeyFreeDiddy,
        Locations.AztecDiddyFreeTiny,
        Locations.AztecDonkeyFreeLanky,
        Locations.FactoryLankyFreeChunky,
    )
    shuffled_items = copy.deepcopy(location_data)
    random.shuffle(shuffled_items)
    blueprint_count = [8, 8, 8, 8, 8, 0]  # 5 sets of 8, 0 at end for Kongs.any
    # First, place items for slots which are reward points, and thus have a restricted placement item list
    for location in location_data:
        if not location.placed and location.reward_spot and location.old_item != Types.Medal:  # Disregard Medals since they don't spawn an object
            found_item = False
            shuffled_items_index = 0
            while not found_item and shuffled_items_index < len(shuffled_items):
                relevant_slot = shuffled_items[shuffled_items_index]
                if not relevant_slot.placed and relevant_slot.old_item in reward_items:  # Ensure item is a reward item
                    if relevant_slot.old_item == Types.Blueprint:
                        if location.old_kong != Kongs.any and blueprint_count[location.old_kong] > 0:  # If Blueprint, ensure that there's enough for kong
                            blueprint_count[location.old_kong] -= 1
                            location.place(relevant_slot.old_item, relevant_slot.old_flag, relevant_slot.old_kong)
                            shuffled_items.remove(relevant_slot)
                            found_item = True
                        else:
                            shuffled_items_index += 1
                    else:
                        location.place(relevant_slot.old_item, relevant_slot.old_flag, relevant_slot.old_kong)
                        shuffled_items.remove(relevant_slot)
                        found_item = True
                else:
                    shuffled_items_index += 1
            if not found_item:
                print(f"EXCEPTION: COULDN'T FIND ITEM ({location.name}), REWARD)")
    # Secondly, fill special coin locations
    for location in location_data:
        if not location.placed and location.old_item == Types.Coin:
            found_item = False
            shuffled_items_index = 0
            while not found_item and shuffled_items_index < len(shuffled_items):
                relevant_slot = shuffled_items[shuffled_items_index]
                if not relevant_slot.placed and relevant_slot.old_item != Types.Banana:
                    if relevant_slot.old_item == Types.Blueprint:
                        if location.location not in bad_bp_locations:  # Ensure location isn't bad bp location
                            kong = location.old_kong
                            if location.location == Locations.HelmKey:
                                valid_kongs = []
                                for bp_i, bp in enumerate(blueprint_count):
                                    if bp > 0:
                                        valid_kongs.append(bp_i)
                                if len(valid_kongs) > 0:
                                    kong = random.choice(valid_kongs)
                            if (location.old_kong != Kongs.any or location.location == Locations.HelmKey) and blueprint_count[kong] > 0:  # If Blueprint, ensure that there's enough for kong
                                blueprint_count[kong] -= 1
                                location.place(relevant_slot.old_item, relevant_slot.old_flag, relevant_slot.old_kong)
                                shuffled_items.remove(relevant_slot)
                                found_item = True
                            else:
                                shuffled_items_index += 1
                        else:
                            shuffled_items_index += 1
                    else:
                        location.place(relevant_slot.old_item, relevant_slot.old_flag, relevant_slot.old_kong)
                        shuffled_items.remove(relevant_slot)
                        found_item = True
                else:
                    shuffled_items_index += 1
            if not found_item:
                print(f"EXCEPTION: COULDN'T FIND ITEM ({location.name}), SPECIAL COIN)")
    # Finally, fill remaining locations
    for location in location_data:
        if not location.placed:
            found_item = False
            shuffled_items_index = 0
            while not found_item and shuffled_items_index < len(shuffled_items):
                relevant_slot = shuffled_items[shuffled_items_index]
                if not relevant_slot.placed:
                    if relevant_slot.old_item == Types.Blueprint:
                        if location.location not in bad_bp_locations:  # Ensure location isn't bad bp location
                            kong = location.old_kong
                            if location.location == Locations.HelmKey:
                                valid_kongs = []
                                for bp_i, bp in enumerate(blueprint_count):
                                    if bp > 0:
                                        valid_kongs.append(bp_i)
                                if len(valid_kongs) > 0:
                                    kong = random.choice(valid_kongs)
                            if (location.old_kong != Kongs.any or location.location == Locations.HelmKey) and blueprint_count[kong] > 0:  # If Blueprint, ensure that there's enough for kong
                                blueprint_count[kong] -= 1
                                location.place(relevant_slot.old_item, relevant_slot.old_flag, relevant_slot.old_kong)
                                shuffled_items.remove(relevant_slot)
                                found_item = True
                            else:
                                shuffled_items_index += 1
                        else:
                            shuffled_items_index += 1
                    else:
                        location.place(relevant_slot.old_item, relevant_slot.old_flag, relevant_slot.old_kong)
                        shuffled_items.remove(relevant_slot)
                        found_item = True
                else:
                    shuffled_items_index += 1
            if not found_item:
                print(f"EXCEPTION: COULDN'T FIND ITEM ({location.name}), REGULAR)")
    spoiler.item_assignment = location_data.copy()
    human_item_data = {}
    for loc in location_data:
        name = "Nothing"
        if loc.new_item is not None:
            name = loc.new_item.name
        human_item_data[loc.name] = name
    spoiler.human_item_assignment = human_item_data
