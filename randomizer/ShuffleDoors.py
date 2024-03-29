"""Shuffle Wrinkly and T&S Doors based on settings."""

import random
import math

from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Regions import Regions
from randomizer.Lists import Exceptions
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
    # Hint doors have Locations tied to them. If we're about to add new ones, then we must remove the old ones.
    if spoiler.settings.wrinkly_location_rando:
        ClearHintDoorLogic(spoiler)
    # Assign Wrinkly Doors & T&S Portals
    for level in door_locations:
        # Get all door locations that can be given a door
        available_doors = []
        for door_index, door in enumerate(door_locations[level]):
            if door.placed == "none" and (spoiler.settings.wrinkly_location_rando or spoiler.settings.tns_location_rando):
                available_doors.append(door_index)
            elif spoiler.settings.remove_wrinkly_puzzles and door.default_placed == "wrinkly":
                available_doors.append(door_index)
        # Prevent plandomized doors from being used as portals
        plando_indexes = []
        if spoiler.settings.enable_plandomizer and spoiler.settings.plandomizer_dict["plando_wrinkly_doors"] != -1:
            plando_indexes = [x for x in available_doors if door_locations[level][x].name in spoiler.settings.plandomizer_dict["plando_wrinkly_doors"].values()]
            for planned_door in plando_indexes:
                available_doors.remove(planned_door)
        random.shuffle(available_doors)
        if spoiler.settings.tns_location_rando:
            plando_portal_indexes = []
            number_of_portals_in_level = random.choice([3, 4, 5])
            allow_multiple_portals_per_group = False
            # Make sure selected locations will be suitable to be a T&S portal
            available_portals = [door for door in available_doors if door_locations[level][door].door_type != "wrinkly"]
            if spoiler.settings.enable_plandomizer and spoiler.settings.plandomizer_dict["plando_tns_portals"] != -1:
                level_to_string = str(level.value)
                if level_to_string in spoiler.settings.plandomizer_dict["plando_tns_portals"].keys():
                    plando_portal_indexes = [x for x in available_portals if door_locations[level][x].name in spoiler.settings.plandomizer_dict["plando_tns_portals"][level_to_string]]
                    if len(plando_portal_indexes) != len([x for x in spoiler.settings.plandomizer_dict["plando_tns_portals"][level_to_string]]):
                        raise Exceptions.PlandoIncompatibleException(f"Not every selected portal is available in level {level}")
                    for planned_portal in plando_portal_indexes:
                        available_portals.remove(planned_portal)
            for new_portal in range(number_of_portals_in_level):
                if len(available_portals) > 0:  # Should only fail if we don't have enough door locations
                    if len(plando_portal_indexes) > 0:
                        selected_door_index = plando_portal_indexes.pop()
                        allow_multiple_portals_per_group = True
                    elif new_portal > 0:
                        selected_door_index = available_portals.pop()
                    else:
                        # On the first iteration, make sure at least 1 TnS portal is accessible without any moves
                        selected_door_index = random.choice([door for door in available_portals if door_locations[level][door].moveless is True])
                        available_portals.remove(selected_door_index)
                    selected_portal = door_locations[level][selected_door_index]
                    if not allow_multiple_portals_per_group:
                        # Only place one T&S portal per group so we don't stack portals too heavily
                        available_portals = [door for door in available_portals if door_locations[level][door].group != selected_portal.group]
                    # update available_doors separately as wrinkly doors should not be affected by the T&S grouping
                    available_doors.remove(selected_door_index)
                    selected_portal.assignPortal(spoiler)
                    human_portal_doors[level_list[level]]["T&S #" + str(new_portal + 1)] = selected_portal.name
                    shuffled_door_data[level].append((selected_door_index, "tns"))
        if spoiler.settings.wrinkly_location_rando:
            # Place one hint door per kong
            for kong in range(5):  # NOTE: If testing all locations, replace "range(5) with range(len(door_locations[level]))"
                assignee = Kongs(kong % 5)
                if len(available_doors) > 0:  # Should only fail if we don't have enough door locations
                    # Give plandomizer an opportunity to get the final say
                    retry = True
                    location_var = str(GetDoorLocationForKongAndLevel(kong, level).value)
                    if (
                        spoiler.settings.enable_plandomizer
                        and spoiler.settings.plandomizer_dict["plando_wrinkly_doors"] != -1
                        and location_var in spoiler.settings.plandomizer_dict["plando_wrinkly_doors"].keys()
                    ):
                        if spoiler.settings.plandomizer_dict["plando_wrinkly_doors"][location_var] not in ("", -1):
                            selected_door_index = [x for x in plando_indexes if door_locations[level][x].name == spoiler.settings.plandomizer_dict["plando_wrinkly_doors"][location_var]][0]
                            retry = False
                        else:
                            selected_door_index = available_doors.pop()
                    else:
                        selected_door_index = available_doors.pop(0)  # Popping from the top of the list makes it possible to append the selected door back into the list, if it's a bad pick
                    # Make sure that the kong is eligible to be assigned to the selected door, and that the door location is suitable to be a hint door
                    while (assignee not in door_locations[level][selected_door_index].kongs) or (door_locations[level][selected_door_index].door_type == "tns"):
                        if retry:
                            available_doors.append(selected_door_index)
                            selected_door_index = available_doors.pop(0)
                        else:
                            name = spoiler.settings.plandomizer_dict["plando_wrinkly_doors"][location_var]
                            raise Exceptions.PlandoIncompatibleException(f"Bad door location: {name}.")
                    selected_door = door_locations[level][selected_door_index]
                    selected_door.assignDoor(assignee)  # Clamp to within [0,4], preventing list index errors
                    human_hint_doors[level_list[level]][str(Kongs(kong % 5).name).capitalize()] = selected_door.name
                    shuffled_door_data[level].append((selected_door_index, "wrinkly", (kong % 5)))
                    # Add logic for the new door location
                    doorLocation = GetDoorLocationForKongAndLevel(kong, level)
                    region = spoiler.RegionList[selected_door.logicregion]
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
    ClearHintDoorLogic(spoiler)
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
        locked_tns.assignPortal(spoiler)
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
            region = spoiler.RegionList[selected_door.logicregion]
            region.locations.append(LocationLogic(doorLocation, selected_door.logic))
        # Any remaining vanilla door that isn't occupied and is a T&S door will get a T&S - the number of doors here will vary based on how many hints were placed in lobby vs level
        placed_tns_count = 1
        for door_index in vanilla_door_indexes:
            vanilla_door = door_locations[level][door_index]
            if vanilla_door.placed == "none" and vanilla_door.default_placed == "tns" and vanilla_door.door_type != "wrinkly":
                placed_tns_count += 1
                vanilla_door.assignPortal(spoiler)
                human_portal_doors[level_list[level]]["T&S #" + str(placed_tns_count)] = vanilla_door.name
                shuffled_door_data[level].append((door_index, "tns"))

    # Track all touched doors in a variable and put it in the spoiler because changes to the static list do not save
    spoiler.shuffled_door_data = shuffled_door_data
    # Give human text to spoiler log
    if spoiler.settings.wrinkly_location_rando:
        spoiler.human_hint_doors = human_hint_doors
    if spoiler.settings.tns_location_rando:
        spoiler.human_portal_doors = human_portal_doors


def ClearHintDoorLogic(spoiler):
    """Remove existing hint door locations from the logic in preparation for custom door locations to be added."""
    for id, region in spoiler.RegionList.items():
        region.locations = [loclogic for loclogic in region.locations if loclogic.id < Locations.JapesDonkeyDoor or loclogic.id > Locations.CastleChunkyDoor]


def SetProgressiveHintDoorLogic(spoiler):
    """Set up hint door location logic for progressive hints to unlock them with GB amounts."""
    # Clear out old hint logic, including any custom logic that may have been placed. Don't need any of it.
    ClearHintDoorLogic(spoiler)
    hint_count = 35
    hint_costs = []
    for i in range(hint_count):
        door_location = Locations.JapesDonkeyDoor + i  # Hint door locations are ordered in their unlocking
        hint_slot = i  # This is to determine what pack of hints this door belongs to
        if i < 34:
            hint_slot = i & 0xFC
        required_gb_count = int(spoiler.settings.progressive_hint_text + spoiler.settings.progressive_hint_text * math.sin(math.pi * 0.5 * ((1 / hint_count) * (hint_slot + 1) + 3)))
        if required_gb_count == 0:
            required_gb_count = 1
        if i == 34:
            required_gb_count = spoiler.settings.progressive_hint_text
        hint_costs.append(required_gb_count)
    # I probably hate this more than you do but lambda functions in python REALLY like to mutate apparently
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.JapesDonkeyDoor, lambda l: l.GoldenBananas >= hint_costs[0]))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.JapesDiddyDoor, lambda l: l.GoldenBananas >= hint_costs[1]))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.JapesLankyDoor, lambda l: l.GoldenBananas >= hint_costs[2]))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.JapesTinyDoor, lambda l: l.GoldenBananas >= hint_costs[3]))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.JapesChunkyDoor, lambda l: l.GoldenBananas >= hint_costs[4]))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.AztecDonkeyDoor, lambda l: l.GoldenBananas >= hint_costs[5]))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.AztecDiddyDoor, lambda l: l.GoldenBananas >= hint_costs[6]))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.AztecLankyDoor, lambda l: l.GoldenBananas >= hint_costs[7]))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.AztecTinyDoor, lambda l: l.GoldenBananas >= hint_costs[8]))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.AztecChunkyDoor, lambda l: l.GoldenBananas >= hint_costs[9]))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.FactoryDonkeyDoor, lambda l: l.GoldenBananas >= hint_costs[10]))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.FactoryDiddyDoor, lambda l: l.GoldenBananas >= hint_costs[11]))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.FactoryLankyDoor, lambda l: l.GoldenBananas >= hint_costs[12]))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.FactoryTinyDoor, lambda l: l.GoldenBananas >= hint_costs[13]))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.FactoryChunkyDoor, lambda l: l.GoldenBananas >= hint_costs[14]))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.GalleonDonkeyDoor, lambda l: l.GoldenBananas >= hint_costs[15]))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.GalleonDiddyDoor, lambda l: l.GoldenBananas >= hint_costs[16]))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.GalleonLankyDoor, lambda l: l.GoldenBananas >= hint_costs[17]))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.GalleonTinyDoor, lambda l: l.GoldenBananas >= hint_costs[18]))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.GalleonChunkyDoor, lambda l: l.GoldenBananas >= hint_costs[19]))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.ForestDonkeyDoor, lambda l: l.GoldenBananas >= hint_costs[20]))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.ForestDiddyDoor, lambda l: l.GoldenBananas >= hint_costs[21]))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.ForestLankyDoor, lambda l: l.GoldenBananas >= hint_costs[22]))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.ForestTinyDoor, lambda l: l.GoldenBananas >= hint_costs[23]))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.ForestChunkyDoor, lambda l: l.GoldenBananas >= hint_costs[24]))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.CavesDonkeyDoor, lambda l: l.GoldenBananas >= hint_costs[25]))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.CavesDiddyDoor, lambda l: l.GoldenBananas >= hint_costs[26]))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.CavesLankyDoor, lambda l: l.GoldenBananas >= hint_costs[27]))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.CavesTinyDoor, lambda l: l.GoldenBananas >= hint_costs[28]))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.CavesChunkyDoor, lambda l: l.GoldenBananas >= hint_costs[29]))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.CastleDonkeyDoor, lambda l: l.GoldenBananas >= hint_costs[30]))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.CastleDiddyDoor, lambda l: l.GoldenBananas >= hint_costs[31]))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.CastleLankyDoor, lambda l: l.GoldenBananas >= hint_costs[32]))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.CastleTinyDoor, lambda l: l.GoldenBananas >= hint_costs[33]))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.CastleChunkyDoor, lambda l: l.GoldenBananas >= hint_costs[34]))
