"""Shuffles items for Item Rando."""

import random
import copy
from randomizer.Lists.Location import LocationList
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Types import Types
from randomizer.Spoiler import Spoiler
from randomizer.Enums.Kongs import Kongs
from randomizer.Lists.Item import NameFromKong
from randomizer.Enums.Items import Items


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
        self.placed = False

    def place(self, item, flag, kong):
        """Place item for assortment."""
        self.new_item = item
        self.new_flag = flag
        self.new_kong = kong
        self.placed = True


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
    # TODO: Moves in item spots means there is going to have to be a TONNE of checks to make sure that
    # it doesn't place an item in a place which needs that item to access.
    # Totally random with no checks would create a lot of bad assortments
    successful_gen = False
    gen_counter = 5
    tbarrel_names = ("Diving", "Vine Swinging", "Orange Throwing", "Barrel Throwing")
    while not successful_gen and gen_counter > 0:
        successful_gen = True
        location_data = []
        order = 0
        for location_enum in LocationList:
            item_location = LocationList[location_enum]
            if item_location.default_mapid_data is not None and item_location.type in spoiler.settings.shuffled_location_types:
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
                        order=order,
                    )
                )
                order += 1
        # Shops - TODO: Check if shop in shuffled list
        item_index = 0
        item_list = []
        for item in move_list:
            for x in range(move_list[item].count):
                print(item.name)
                item_list.append(item)
        banned_shops = [
            [1, 0],
            [1, 4],
            [1, 7],
            [2, 7],
        ]
        for shop_index, shop in enumerate(["Cranky", "Candy", "Funky"]):
            for level_index, level in enumerate(["Japes", "Aztec", "Factory", "Galleon", "Fungi", "Caves", "Castle", "Isles"]):
                for kong_index, kong in enumerate(["DK", "Diddy", "Lanky", "Tiny", "Chunky"]):
                    if [shop_index, level_index] not in banned_shops:
                        item_place = True
                        move_name = "No Item"
                        if item_index < len(item_list):
                            data = move_list[item_list[item_index]]
                            move_name = item_list[item_index].name
                        else:
                            data = MoveData(7, Kongs.donkey, 0)
                            item_place = False
                        location_data.append(
                            LocationSelection(
                                vanilla_item=Types.Shop,
                                flag=0x8000 | (data.kong << 12) | (data.subtype << 8) | data.index,
                                placement_data={},
                                is_reward_point=True,
                                kong=data.kong,
                                name=f"{level} {kong} {shop}",
                                is_shop=True,
                                placement_index=(shop_index * 40) + (kong_index * 8) + level_index,
                                can_place_item=item_place,
                                shop_locked=data.shared, # Should be data.count>1, but would have to reimplement searching algorithm if homing/sniper gets placed in a shop outside of initial phase
                                shared=data.shared,
                                order=order,
                                move_name=move_name,
                            )
                        )
                        item_index += 1
                        order += 1
        # Training Barrels - TODO: Check if  training barrel is in shuffled list
        for flag in range(0x182, 0x186):
            location_data.append(
                LocationSelection(
                    vanilla_item=Types.TrainingBarrel,
                    flag=flag,
                    placement_data={},
                    is_reward_point=True,
                    kong=Kongs.any,
                    name=tbarrel_names[flag - 0x182],
                    is_shop=True,
                    placement_index=120 + (flag - 0x182),
                    shop_locked=True, # Should be false, but temporarily making true to prevent having to place a copy of the shop generation algo check
                    shared=True,
                    order=order,
                    move_name=tbarrel_names[flag - 0x182],
                )
            )
            order += 1
        # Fairy Items - TODO: Check if shockwave is in shuffled list
        for item in range(2):
            location_data.append(
                LocationSelection(
                    vanilla_item=Types.Shockwave,
                    flag=[0x179, 0x2FD][item],
                    placement_data={},
                    is_reward_point=True,
                    kong=Kongs.any,
                    name=["Fairy Island", "Null Spot"][item],
                    is_shop=True,
                    placement_index=[124, None][item],
                    can_have_item=[True, False][item],
                    shop_locked=True, # Should be false, but temporarily making true to prevent having to place a copy of the shop generation algo check
                    shared=True,
                    order=order,
                    move_name=["Fairy Island", "Null Spot"][item],
                )
            )
            order += 1
        reward_items = (
            # Items which can be spawned as an actor
            Types.Banana,  # Actor 45
            Types.Blueprint,  # HAS to correspond to intended actor for item, actors 75-79 (Diddy, Chunky, Lanky, DK, Tiny)
            Types.Key,  # Actor 72
            Types.Crown,  # Actor 86
            Types.Coin,  # Actors 151, 152 (Nin, RW)
            Types.Shop, # Actors 157-162
            Types.Shockwave, # Actor 162
            Types.TrainingBarrel, # Actor 162
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
        print(hex(0x8000 | (7 << 8)))
        for item in shuffled_items:
            if item.can_place_item is False or item.old_flag == (0x8000 | (7 << 8)):
                item.placed = True
        random.shuffle(shuffled_items)
        random.shuffle(location_data)
        # Fill shop-locked items
        for item in shuffled_items:
            if not item.placed and item.shop_locked:
                found_location = False
                for shop_index in range(29):
                    if not found_location:
                        vacant_bitfield = 0
                        selected_slot = 0
                        vacant_count = 0
                        shared_limit = 5
                        if shop_index < 24:
                            acceptable_values = []
                            for kong_index in range(5):
                                acceptable_values.append((shop_index & 7) + (kong_index * 8) + (40 * int(shop_index / 8)))
                            for location in location_data:
                                if not location.placed and location.placement_index in acceptable_values and location.is_shop:
                                    vacant_bitfield |= (1 << acceptable_values.index(location.placement_index))
                            for kong_index in range(5):
                                selection_list = []
                                if vacant_bitfield & (1 << kong_index):
                                    selection_list.append(kong_index)
                                    vacant_count += 1
                                if vacant_count > 0:
                                    selected_slot = random.choice(selection_list)
                        else:
                            for location in location_data:
                                if not location.placed and location.placement_index == (shop_index + 96) and location.is_shop:
                                    vacant_count += 1
                            shared_limit = 1
                        if item.shared:
                            if vacant_count == shared_limit:
                                print(f"{vacant_count} | {shared_limit} | {item.old_flag}")
                                found_location = True
                                if shop_index < 24:
                                    acceptable_values = []
                                    for kong_index in range(5):
                                        acceptable_values.append((shop_index & 7) + (kong_index * 8) + (40 * int(shop_index / 8)))
                                    for location in location_data:
                                        if not location.placed and location.placement_index in acceptable_values and location.is_shop:
                                            location.place(item.old_item, item.old_flag, item.old_kong)
                                else:
                                    for location in location_data:
                                        if not location.placed and location.placement_index == (shop_index + 96) and location.is_shop:
                                            location.place(item.old_item, item.old_flag, item.old_kong)
                                item.placed = True
                        else:
                            found_location = True
                            if shop_index < 24:
                                acceptable_value = (shop_index & 7) + (selected_slot * 8) + (40 * int(shop_index / 8))
                                for location in location_data:
                                        if not location.placed and location.placement_index == acceptable_value and location.is_shop:
                                            location.place(item.old_item, item.old_flag, item.old_kong)
                            else:
                                for location in location_data:
                                    if not location.placed and location.placement_index == (shop_index + 96) and location.is_shop:
                                        location.place(item.old_item, item.old_flag, item.old_kong)
                            item.placed = True
        for item in shuffled_items:
            if item.placed:
                shuffled_items.remove(item)
        # Place items for slots which are reward points, and thus have a restricted placement item list
        for location in location_data:
            if not location.placed and location.reward_spot and location.old_item != Types.Medal and location.is_shop is False:  # Disregard Medals since they don't spawn an object
                found_item = False
                shuffled_items_index = 0
                while not found_item and shuffled_items_index < len(shuffled_items):
                    relevant_slot = shuffled_items[shuffled_items_index]
                    if not relevant_slot.placed and relevant_slot.old_item in reward_items:  # Ensure item is a reward item
                        if relevant_slot.old_item == Types.Blueprint:
                            if location.old_kong == relevant_slot.old_kong:
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
                    successful_gen = False
        # Fill special coin locations
        for location in location_data:
            if not location.placed and location.old_item == Types.Coin:
                found_item = False
                shuffled_items_index = 0
                while not found_item and shuffled_items_index < len(shuffled_items):
                    relevant_slot = shuffled_items[shuffled_items_index]
                    if not relevant_slot.placed and relevant_slot.old_item != Types.Banana:
                        if relevant_slot.old_item == Types.Blueprint:
                            if location.old_kong == relevant_slot.old_kong:
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
                    successful_gen = False
        # Fill remaining locations
        for location in location_data:
            if not location.placed and location.can_have_item is True:
                found_item = False
                shuffled_items_index = 0
                if len(shuffled_items) == 0:
                    location.place(None, None, None)
                else:
                    while not found_item and shuffled_items_index < len(shuffled_items):
                        relevant_slot = shuffled_items[shuffled_items_index]
                        if not relevant_slot.placed:
                            if relevant_slot.old_item == Types.Blueprint:
                                if location.location not in bad_bp_locations:  # Ensure location isn't bad bp location
                                    if location.old_kong == relevant_slot.old_kong:
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
                        successful_gen = False
        if not successful_gen:
            gen_counter -= 1
            if gen_counter == 0:
                print("ERROR: COULDN'T GEN ASSORTMENT")
    location_data = sorted(location_data, key=lambda x: x.order)
    spoiler.item_assignment = location_data.copy()
    human_item_data = {}
    for loc in location_data:
        if loc.can_have_item:
            name = "Nothing"
            if loc.new_item is not None:
                name = loc.new_item.name
            if loc.new_item == Types.Shop:
                item_kong = (loc.new_flag >> 12) & 7
                item_subtype = (loc.new_flag >> 8) & 0xF
                item_subindex = loc.new_flag & 0xFF
                if loc.new_flag == 0x8700:
                    name = "Nothing (Shop)"
                else:
                    for item in move_list:
                        if move_list[item].kong == item_kong and move_list[item].index == item_subindex and move_list[item].subtype == item_subtype:
                            name = "".join(map(lambda x: x if x.islower() else " " + x, item.name)).strip()
            elif loc.new_item == Types.TrainingBarrel:
                name = tbarrel_names[loc.new_flag - 0x182]
            elif loc.new_item == Types.Shockwave:
                name = "Shockwave"
                if loc.new_flag == 0x2FD:
                    name = "Camera"
            location_name = loc.name
            if "Kasplat" in location_name:
                location_name = f"{location_name.split('Kasplat')[0]} {NameFromKong(loc.old_kong)} Kasplat"
            human_item_data[location_name] = name
    spoiler.human_item_assignment = human_item_data
