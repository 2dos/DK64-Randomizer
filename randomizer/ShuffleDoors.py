"""Shuffle Wrinkly and T&S Doors based on settings."""
import random

import randomizer.Logic as Logic
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Lists.DoorLocations import door_locations
from randomizer.LogicClasses import LocationLogic

level_list = ["Jungle Japes", "Angry Aztec", "Frantic Factory", "Gloomy Galleon", "Fungi Forest", "Crystal Caves", "Creepy Castle"]
human_hint_doors = {
    "Jungle Japes": {},
    "Angry Aztec": {},
    "Frantic Factory": {},
    "Gloomy Galleon": {},
    "Fungi Forest": {},
    "Crystal Caves": {},
    "Creepy Castle": {},
}
human_portal_doors = {
    "Jungle Japes": {},
    "Angry Aztec": {},
    "Frantic Factory": {},
    "Gloomy Galleon": {},
    "Fungi Forest": {},
    "Crystal Caves": {},
    "Creepy Castle": {},
}
shuffled_door_data = {
    Levels.JungleJapes: [],
    Levels.AngryAztec: [],
    Levels.FranticFactory: [],
    Levels.GloomyGalleon: [],
    Levels.FungiForest: [],
    Levels.CrystalCaves: [],
    Levels.CreepyCastle: [],
}


def GetDoorLocationForKongAndLevel(kong, level):
    """For the Level and Kong enum values, return the generic Blueprint Location enum tied to it."""
    baseOffset = int(Locations.JapesDonkeyDoor)  # Japes/Donkey is the first door location and they're all grouped together
    levelOffset = int(level)
    return Locations(baseOffset + (5 * levelOffset) + int(kong))


def ShuffleDoors(spoiler):
    """Shuffle Wrinkly and T&S Doors based on settings."""
    # Reset Doors
    for level in door_locations:
        # Also reset the data structures that share info across processes
        shuffled_door_data[level] = []
        human_hint_doors[level_list[level]] = {}
        human_portal_doors[level_list[level]] = {}
        for door in door_locations[level]:
            door.placed = door.default_placed
            if spoiler.settings.wrinkly_location_rando:
                if door.placed == "wrinkly":
                    door.placed = "none"
            if spoiler.settings.tns_location_rando:
                if door.placed == "tns":
                    door.placed = "none"
    # Assign Wrinkly Doors & T&S Portals
    for level in door_locations:
        # Get all door locations that can be given a door
        available_doors = []
        for door_index, door in enumerate(door_locations[level]):
            if door.placed == "none" and (spoiler.settings.wrinkly_location_rando or spoiler.settings.tns_location_rando):
                available_doors.append(door_index)
            elif spoiler.settings.remove_wrinkly_puzzles and door.default_placed == "wrinkly":
                available_doors.append(door_index)
        random.shuffle(available_doors)
        if spoiler.settings.tns_location_rando:
            number_of_portals_in_level = random.choice([3, 4, 5])
            # Make sure selected locations will be suitable to be a T&S portal
            available_portals = [door for door in available_doors if door_locations[level][door].door_type != "wrinkly"]
            for new_portal in range(number_of_portals_in_level):
                if len(available_portals) > 0:  # Should only fail if we don't have enough door locations
                    if new_portal > 0:
                        selected_door_index = available_portals.pop()
                        selected_portal = door_locations[level][selected_door_index]
                        # Only place one T&S portal per group so we don't stack portals too heavily
                        available_portals = [door for door in available_portals if door_locations[level][door].group != selected_portal.group]
                        # update available_doors separately as wrinkly doors should not be affected by the T&S grouping
                        available_doors.remove(selected_door_index)
                        selected_portal.assignPortal()
                        human_portal_doors[level_list[level]]["T&S #" + str(new_portal + 1)] = selected_portal.name
                        shuffled_door_data[level].append((selected_door_index, "tns"))
                    else:
                        # On the first iteration, make sure at least 1 TnS portal is accessible without any moves
                        selected_door_index = random.choice([door for door in available_portals if door_locations[level][door].moveless is True])
                        selected_portal = door_locations[level][selected_door_index]
                        # Only place one T&S portal per group so we don't stack portals too heavily
                        available_portals = [door for door in available_portals if door_locations[level][door].group != selected_portal.group]
                        # update available_doors separately as wrinkly doors should not be affected by the T&S grouping
                        available_doors.remove(selected_door_index)
                        selected_portal.assignPortal()
                        human_portal_doors[level_list[level]]["T&S #" + str(new_portal + 1)] = selected_portal.name
                        shuffled_door_data[level].append((selected_door_index, "tns"))
        if spoiler.settings.wrinkly_location_rando:
            # Place one hint door per kong
            for kong in range(5):  # NOTE: If testing all locations, replace "range(5) with range(len(door_locations[level]))"
                assignee = Kongs(kong % 5)
                if len(available_doors) > 0:  # Should only fail if we don't have enough door locations
                    selected_door_index = available_doors.pop(0)  # Popping from the top of the list makes it possible to append the selected door back into the list, if it's a bad pick
                    # Make sure that the kong is eligible to be assigned to the selected door, and that the door location is suitable to be a hint door
                    while (assignee not in door_locations[level][selected_door_index].kongs) or (door_locations[level][selected_door_index].door_type == "tns"):
                        available_doors.append(selected_door_index)
                        selected_door_index = available_doors.pop(0)
                    selected_door = door_locations[level][selected_door_index]
                    selected_door.assignDoor(assignee)  # Clamp to within [0,4], preventing list index errors
                    human_hint_doors[level_list[level]][str(Kongs(kong % 5).name).capitalize()] = selected_door.name
                    shuffled_door_data[level].append((selected_door_index, "wrinkly", (kong % 5)))
                    # Add logic for the new door location
                    doorLocation = GetDoorLocationForKongAndLevel(kong, level)
                    region = Logic.Regions[selected_door.logicregion]
                    region.locations.append(LocationLogic(doorLocation, selected_door.logic))
        elif spoiler.settings.remove_wrinkly_puzzles:
            # place vanilla wrinkly doors
            vanilla_wrinkly_doors = [door for door in available_doors if door_locations[level][door].default_placed == "wrinkly"]
            for kong in range(5):
                if len(vanilla_wrinkly_doors) > 0:  # Should only fail if we don't have enough door locations
                    selected_door_index = vanilla_wrinkly_doors.pop()
                    selected_door = door_locations[level][selected_door_index]
                    assignee = selected_door.default_kong
                    selected_door.assignDoor(assignee)
                    human_hint_doors[level_list[level]][str(assignee).capitalize()] = selected_door.name
                    shuffled_door_data[level].append((selected_door_index, "wrinkly", int(assignee)))

    # Track all touched doors in a variable and put it in the spoiler because changes to the static list do not save
    spoiler.shuffled_door_data = shuffled_door_data
    # Give human text to spoiler log
    if spoiler.settings.wrinkly_location_rando:
        spoiler.human_hint_doors = human_hint_doors
    if spoiler.settings.tns_location_rando:
        spoiler.human_portal_doors = human_portal_doors


def ShuffleVanillaDoors(spoiler):
    """Shuffle T&S and Wrinkly doors amongst the vanilla locations."""
    for level in door_locations:
        # Reset the data structures for door shuffling information sharing
        shuffled_door_data[level] = []
        human_hint_doors[level_list[level]] = {}
        human_portal_doors[level_list[level]] = {}
        # Find the vanilla doors that are valid hint locations and clear their door
        vanilla_door_indexes = []
        for door_index, door in enumerate(door_locations[level]):
            if door.default_placed != "none":
                door.placed = "none"
                vanilla_door_indexes.append(door_index)
        random.shuffle(vanilla_door_indexes)
        # One random vanilla T&S per level is locked to being a T&S
        locked_tns_options = [idx for idx in vanilla_door_indexes if door_locations[level][idx].default_placed == "tns" and door_locations[level][idx].door_type != "wrinkly"]
        locked_tns_index = random.choice(locked_tns_options)
        locked_tns = door_locations[level][locked_tns_index]
        locked_tns.assignPortal()
        human_portal_doors[level_list[level]]["T&S #1"] = locked_tns.name
        shuffled_door_data[level].append((locked_tns_index, "tns"))
        vanilla_door_indexes.remove(locked_tns_index)
        # All other locations are fair game for hint doors - place one per kong
        for kong in range(5):
            assignee = Kongs(kong % 5)
            # Pick a door, any door
            selected_door_index = vanilla_door_indexes.pop(0)  # This should never fail
            selected_door = door_locations[level][selected_door_index]
            # Assign it to this Kong
            selected_door.assignDoor(assignee)
            human_hint_doors[level_list[level]][str(assignee.name).capitalize()] = selected_door.name
            shuffled_door_data[level].append((selected_door_index, "wrinkly", int(assignee)))
            # Add this hint door's location back to the logic
            doorLocation = GetDoorLocationForKongAndLevel(kong, level)
            region = Logic.Regions[selected_door.logicregion]
            region.locations.append(LocationLogic(doorLocation, selected_door.logic))
        # Any remaining vanilla door that isn't occupied and is a T&S door will get a T&S - the number of doors here will vary based on how many hints were placed in lobby vs level
        placed_tns_count = 1
        for door_index in vanilla_door_indexes:
            vanilla_door = door_locations[level][door_index]
            if vanilla_door.placed == "none" and vanilla_door.default_placed == "tns" and vanilla_door.door_type != "wrinkly":
                placed_tns_count += 1
                vanilla_door.assignPortal()
                human_portal_doors[level_list[level]]["T&S #" + str(placed_tns_count)] = vanilla_door.name
                shuffled_door_data[level].append((door_index, "tns"))

    # Track all touched doors in a variable and put it in the spoiler because changes to the static list do not save
    spoiler.shuffled_door_data = shuffled_door_data
    # Give human text to spoiler log
    if spoiler.settings.wrinkly_location_rando:
        spoiler.human_hint_doors = human_hint_doors
    if spoiler.settings.tns_location_rando:
        spoiler.human_portal_doors = human_portal_doors
