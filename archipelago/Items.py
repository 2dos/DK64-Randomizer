"""Item table for Donkey Kong 64."""

import math
import typing

from BaseClasses import Item, ItemClassification
from worlds.AutoWorld import World
from types import SimpleNamespace

from randomizer.Enums.Levels import Levels
from randomizer.Lists import Item as DK64RItem
from randomizer.Enums.Items import Items as DK64RItems
from randomizer.Enums.Types import Types as DK64RTypes
import randomizer.ItemPool as DK64RItemPoolUtility

BASE_ID = 0xD64000


class ItemData(typing.NamedTuple):
    """Data for an item."""

    code: typing.Optional[int]
    progression: bool
    quantity: int = 1
    event: bool = False


class DK64Item(Item):
    """A DK64 item."""

    game: str = "Donkey Kong 64"


# Separate tables for each type of item.
junk_table = {}

collectable_table = {}

event_table = {
    "Victory": ItemData(0xD64000, True),  # Temp
}

# Complete item table
full_item_table = {item.name: ItemData(int(BASE_ID + index), item.playthrough) for index, item in DK64RItem.ItemList.items()}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in full_item_table.items()}

full_item_table.update(event_table)  # Temp for generating goal item


def setup_items(world: World) -> typing.List[DK64Item]:
    """Set up the item table for the world."""
    item_table = []

    # Figure out how many GB are progression - the Helm B. Locker is assumed to be the maximum value
    # V1 LIMITATION: Assuming GBs are needed for B. Lockers - no Chaos B. Lockers as of yet
    # V1 LIMITATION: Currently assuming Helm is your last and most expensive level
    gb_item = DK64RItem.ItemList[DK64RItems.GoldenBanana]
    for i in range(min(161, world.logic_holder.settings.BLockerEntryCount[Levels.HideoutHelm])):
        item_table.append(DK64Item(gb_item.name, ItemClassification.progression_skip_balancing, full_item_table[gb_item.name].code, world.player))
    for i in range(161 - world.logic_holder.settings.BLockerEntryCount[Levels.HideoutHelm]):
        item_table.append(DK64Item(gb_item.name, ItemClassification.useful, full_item_table[gb_item.name].code, world.player))
    # Figure out how many Medals are progression
    medal_item = DK64RItem.ItemList[DK64RItems.BananaMedal]
    for i in range(world.logic_holder.settings.medal_requirement):
        item_table.append(DK64Item(medal_item.name, ItemClassification.progression_skip_balancing, full_item_table[medal_item.name].code, world.player))
    for i in range(40 - world.logic_holder.settings.medal_requirement):
        item_table.append(DK64Item(medal_item.name, ItemClassification.useful, full_item_table[medal_item.name].code, world.player))
    # Figure out how many Fairies are progression
    fairy_item = DK64RItem.ItemList[DK64RItems.BananaFairy]
    for i in range(world.logic_holder.settings.rareware_gb_fairies):
        item_table.append(DK64Item(fairy_item.name, ItemClassification.progression_skip_balancing, full_item_table[fairy_item.name].code, world.player))
    for i in range(20 - world.logic_holder.settings.rareware_gb_fairies):
        item_table.append(DK64Item(fairy_item.name, ItemClassification.useful, full_item_table[fairy_item.name].code, world.player))

    # V1 LIMITATION: Tough GBs must be in the pool - this can likely be worked around later
    all_shuffled_items = DK64RItemPoolUtility.GetItemsNeedingToBeAssumed(
        world.logic_holder.settings, [DK64RTypes.Medal, DK64RTypes.Fairy, DK64RTypes.Banana, DK64RTypes.ToughBanana, DK64RTypes.Bean, DK64RTypes.Pearl], []
    )
    # Due to some latent (harmless) bugs in the above method, it isn't precise enough for our purposes and we need to manually add a few things
    # The Bean and Pearls wreak havoc on this method due to a latent bug, so it's easiest to just add them manually
    all_shuffled_items.extend([DK64RItems.Bean, DK64RItems.Pearl, DK64RItems.Pearl, DK64RItems.Pearl, DK64RItems.Pearl, DK64RItems.Pearl])
    # Junk moves are never assumed because they're just not needed for anything
    all_shuffled_items.extend(DK64RItemPoolUtility.JunkSharedMoves)
    # Key 8 may not be included from the assumption method, but we need it in this list to complete the item table. It won't count towards the item pool size if it is statically placed later.
    if DK64RItems.HideoutHelmKey not in all_shuffled_items:
        all_shuffled_items.append(DK64RItems.HideoutHelmKey)

    for seed_item in all_shuffled_items:
        item = DK64RItem.ItemList[seed_item]
        if item.type in [DK64RItems.JunkCrystal, DK64RItems.JunkMelon, DK64RItems.JunkAmmo, DK64RItems.JunkFilm, DK64RItems.JunkOrange, DK64RItems.CrateMelon]:
            classification = ItemClassification.filler
        elif item.type in [DK64RItems.IceTrapBubble, DK64RItems.IceTrapReverse, DK64RItems.IceTrapSlow]:
            classification = ItemClassification.trap
        elif item.type == DK64RTypes.Key:
            classification = ItemClassification.progression
        # The playthrough tag doesn't quite 1-to-1 map to Archipelago's "progression" type - some items we don't consider "playthrough" can affect logic
        elif item.playthrough is True or item.type in (DK64RTypes.Blueprint, DK64RTypes.Pearl, DK64RTypes.Bean):
            classification = ItemClassification.progression_skip_balancing
        else:  # double check jetpac, eh?
            classification = ItemClassification.useful
        if seed_item == DK64RItems.HideoutHelmKey and world.logic_holder.settings.key_8_helm:
            world.multiworld.get_location("The End of Helm", world.player).place_locked_item(DK64Item("Key 8", ItemClassification.progression, full_item_table[item.name].code, world.player))
            world.logic_holder.location_pool_size -= 1
            continue
        item_table.append(DK64Item(item.name, classification, full_item_table[item.name].code, world.player))
        # print("Adding item: " + seed_item.name + " | " + str(classification))

    # Extract starting moves from the item table - these items will be placed in your starting inventory directly
    for move in world.options.start_inventory:
        for i in range(world.options.start_inventory[move]):
            for item in item_table:
                if item.name == move:
                    item_table.remove(item)
                    break

    # Handle starting Kong list here
    for kong in world.logic_holder.settings.starting_kong_list:
        kong_item = DK64RItemPoolUtility.ItemFromKong(kong)
        if kong == world.logic_holder.settings.starting_kong:
            world.multiworld.push_precollected(DK64Item(kong_item.name, ItemClassification.progression, full_item_table[DK64RItem.ItemList[kong_item].name].code, world.player))
        for item in item_table:
            if item.name == kong_item.name:
                # Conveniently, this guarantees we have at least one precollected item!
                world.multiworld.push_precollected(DK64Item(item.name, ItemClassification.progression, full_item_table[DK64RItem.ItemList[kong_item].name].code, world.player))
                item_table.remove(item)
                break

    # Handle starting move alterations here
    all_eligible_starting_moves = DK64RItemPoolUtility.AllKongMoves()
    all_eligible_starting_moves.extend(DK64RItemPoolUtility.TrainingBarrelAbilities())
    # Either include Climbing as an eligible starting move or place it in the starting inventory
    if world.options.climbing_shuffle:
        all_eligible_starting_moves.extend(DK64RItemPoolUtility.ClimbingAbilities())
    else:
        world.multiworld.push_precollected(DK64Item("Climbing", ItemClassification.progression, full_item_table[DK64RItem.ItemList[DK64RItems.Climbing].name].code, world.player))
        for item in item_table:
            if item.name == "Climbing":
                item_table.remove(item)
                break

    world.random.shuffle(all_eligible_starting_moves)
    for i in range(world.options.starting_move_count):
        if len(all_eligible_starting_moves) == 0:
            break
        move_id = all_eligible_starting_moves.pop()
        move = DK64RItem.ItemList[move_id]
        # We don't want to pick anything we're already starting with. As an aside, the starting inventory move name may or may not have spaces in it.
        if move_id.name in world.options.start_inventory.options or move.name in world.options.start_inventory.options:
            # If we were to choose a move we're forcibly starting with, pick another
            i = -1
            continue
        for item in item_table:
            if item.name == move_id.name or item.name == move.name:
                world.multiworld.push_precollected(item)
                item_table.remove(item)
                break

    # print("location comparison: " + str(world.logic_holder.location_pool_size - 1))
    # print("non-junk items: " + str(len(item_table)))
    if world.logic_holder.location_pool_size - len(item_table) - 1 < 0:
        raise Exception("Too many DK64 items to be placed in too few DK64 locations")

    # If there's too many locations and not enough items, add some junk
    filler_item_count: int = world.logic_holder.location_pool_size - len(item_table) - 1  # The last 1 is for the Banana Hoard

    trap_weights = []
    trap_weights += [DK64RItems.IceTrapBubble] * world.options.bubble_trap_weight.value
    trap_weights += [DK64RItems.IceTrapReverse] * world.options.reverse_trap_weight.value
    trap_weights += [DK64RItems.IceTrapSlow] * world.options.slow_trap_weight.value

    trap_count = 0 if (len(trap_weights) == 0) else math.ceil(filler_item_count * (world.options.trap_fill_percentage.value / 100.0))
    filler_item_count -= trap_count

    possible_junk = [DK64RItems.JunkMelon]
    # possible_junk = [DK64RItems.JunkCrystal, DK64RItems.JunkMelon, DK64RItems.JunkAmmo, DK64RItems.JunkFilm, DK64RItems.JunkOrange] # Someday...

    for i in range(filler_item_count):
        junk_enum = world.random.choice(possible_junk)
        junk_item = DK64RItem.ItemList[junk_enum]
        item_table.append(DK64Item(junk_item.name, ItemClassification.filler, full_item_table[junk_item.name].code, world.player))

    possible_traps = [DK64RItems.IceTrapBubble, DK64RItems.IceTrapReverse, DK64RItems.IceTrapSlow]

    for i in range(trap_count):
        trap_enum = world.random.choice(trap_weights)
        trap_item = DK64RItem.ItemList[trap_enum]
        item_table.append(DK64Item(trap_item.name, ItemClassification.trap, full_item_table[trap_item.name].code, world.player))

    # print("projected available locations: " + str(world.logic_holder.location_pool_size - 1))
    # print("projected items to place: " + str(len(item_table)))

    # Example of accessing Option result
    if world.options.goal == "krool":
        pass

    # DEBUG
    # for k, v in full_item_table.items():
    #    print(k + ": " + hex(v.code) + " | " + str(v.progression))

    return item_table
