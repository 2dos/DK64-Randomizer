"""Shuffle Wrinkly and T&S Doors based on settings."""
import random
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Regions import Regions
from randomizer.Lists.DoorLocations import door_locations

level_list = ["Jungle Japes", "Angry Aztec", "Frantic Factory", "Gloomy Galleon", "Fungi Forest", "Crystal Caves", "Creepy Castle", "Hideout Helm"]


def ShuffleDoors(spoiler):
    """Shuffle Wrinkly and T&S Doors based on settings."""
    human_hint_doors = {}
    human_portal_doors = {}
    for level in level_list:
        human_hint_doors[level] = {}
        human_portal_doors[level] = {}
    shuffled_door_data = {}
    # Reset Doors
    for level in door_locations:
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
        shuffled_door_data[level] = []
        # Get all door locations that can be given a door
        available_doors = []
        for door_index, door in enumerate(door_locations[level]):
            if door.placed == "none" and (spoiler.settings.wrinkly_location_rando or spoiler.settings.tns_location_rando):
                available_doors.append(door_index)
            elif ("remove_wrinkly_puzzles" in spoiler.settings.misc_changes_selected or len(spoiler.settings.misc_changes_selected) == 0) and door.default_placed == "wrinkly":
                available_doors.append(door_index)
        random.shuffle(available_doors)
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
        elif "remove_wrinkly_puzzles" in spoiler.settings.misc_changes_selected or len(spoiler.settings.misc_changes_selected) == 0:
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
        if spoiler.settings.tns_location_rando:
            number_of_portals_in_level = random.choice([3, 4, 5])
            moveless_portal_selected = False
            # Make sure selected locations will be suitable to be a T&S portal
            available_doors = [door for door in available_doors if door_locations[level][door].door_type != "wrinkly"]
            for new_portal in range(number_of_portals_in_level):
                if len(available_doors) > 0:  # Should only fail if we don't have enough door locations
                    if new_portal < (number_of_portals_in_level - 1) or moveless_portal_selected is True:
                        selected_door_index = available_doors.pop()
                        selected_portal = door_locations[level][selected_door_index]
                        if selected_portal.moveless is True:
                            moveless_portal_selected = True
                        # Only place one T&S portal per group so we don't stack portals too heavily
                        available_doors = [door for door in available_doors if door_locations[level][door].group != selected_portal.group]
                        selected_portal.assignPortal()
                        human_portal_doors[level_list[level]][" T&S #" + str(new_portal + 1)] = selected_portal.name
                        shuffled_door_data[level].append((selected_door_index, "tns"))
                    else:
                        # On the last iteration, make sure at least 1 TnS portal is accessible without any moves
                        selected_door_index = random.choice([door for door in available_doors if door_locations[level][door].moveless is True])
                        selected_portal = door_locations[level][selected_door_index]
                        selected_portal.assignPortal()
                        human_portal_doors[level_list[level]][" T&S #" + str(new_portal + 1)] = selected_portal.name
                        shuffled_door_data[level].append((selected_door_index, "tns"))

    # Track all touched doors in a variable and put it in the spoiler because changes to the static list do not save
    spoiler.shuffled_door_data = shuffled_door_data
    # Give human text to spoiler log
    if spoiler.settings.wrinkly_location_rando:
        spoiler.human_hint_doors = human_hint_doors
    if spoiler.settings.tns_location_rando:
        spoiler.human_portal_doors = human_portal_doors
