"""Methods to handle plando settings importing and exporting."""

from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Minigames import Minigames
from randomizer.Enums.Plandomizer import PlandoItems
from randomizer.Enums.Switches import Switches
from randomizer.Enums.SwitchTypes import SwitchType
from randomizer.Lists.CustomLocations import CustomLocations
from randomizer.Lists.DoorLocations import DoorType, door_locations
from randomizer.Lists.FairyLocations import fairy_locations
from randomizer.Lists.KasplatLocations import KasplatLocationList
from randomizer.Lists.Location import LocationListOriginal as LocationList
from randomizer.Lists.Plandomizer import KasplatLocationEnumList
from randomizer.Enums.Transitions import Transitions
from randomizer.Enums.Items import Items
from randomizer.Enums.Plandomizer import ItemToPlandoItemMap, PlandoItems
from randomizer.Lists.Item import StartingMoveOptions

import js
import json
from ui.bindings import bind, bindList
from ui.plando_validation import (
    full_validate_no_reward_with_random_location,
    lock_key_8_in_helm,
    populate_plando_options,
    reset_plando_options_no_prompt,
    validate_custom_arena_locations,
    validate_custom_crate_locations,
    validate_custom_doors_no_duplicate_locations,
    validate_custom_fairy_locations,
    validate_custom_kasplat_locations,
    validate_custom_locations_no_duplicates,
    validate_custom_patch_locations,
    validate_helm_order_no_duplicates,
    validate_hint_count,
    validate_hint_text,
    validate_item_limits,
    validate_krool_order_no_duplicates,
    validate_level_order_no_duplicates,
    validate_no_crate_items_with_shuffled_crates,
    validate_no_crown_items_with_shuffled_crowns,
    validate_no_dirt_items_with_shuffled_patches,
    validate_no_fairy_items_with_shuffled_fairies,
    validate_no_kasplat_items_with_location_shuffle,
    validate_shuffle_shops_no_conflict,
    validate_smaller_shops_no_conflict,
    validate_starting_kong_count,
    level_options,
    kong_options,
)


# Assemble sets of custom locations, for validation.
customLocationSet = set()
for level, locations in CustomLocations.items():
    for location in locations:
        fullLoc = f"{level.name}: {location.name}"
        customLocationSet.add(fullLoc)
customFairyLocationSet = set()
for level, locations in fairy_locations.items():
    for location in locations:
        fullLoc = f"{level.name}: {location.name}"
        customFairyLocationSet.add(fullLoc)
customKasplatLocationSet = set()
for _, locations in KasplatLocationList.items():
    for location in locations:
        customKasplatLocationSet.add(location.name)
customWrinklyDoorLocationSet = {}
customTnsPortalLocationSet = {}
for level, locations in door_locations.items():
    customWrinklyDoorLocationSet[level] = set()
    customTnsPortalLocationSet[level] = set()
    for location in locations:
        if DoorType.wrinkly in location.door_type:
            customWrinklyDoorLocationSet[level].add(location.name)
        if DoorType.boss in location.door_type:
            customTnsPortalLocationSet[level].add(location.name)


@bind("click", "export_plando_string")
def export_plando_string(evt):
    """Generate the plando json string."""
    # Serialize the form into json
    form = js.jquery("#form").serializeArray()

    # Plandomizer data is processed separately.
    plando_form_data = populate_plando_options(form)
    js.plando_string.value = json.dumps(plando_form_data)


async def import_plando_options(jsonString):
    """Import plando settings from a provided JSON file."""
    fileContents = json.loads(jsonString)

    # Inform the user their current settings will be erased.
    if not js.window.confirm("This will replace your current plandomizer settings. Continue?"):
        return

    # First, ensure this is an actual valid plando file.
    validate_plando_file(fileContents)

    # Reset all of the plando options to their defaults.
    reset_plando_options_no_prompt()

    # We need to record all hints and shop costs so we can validate them later.
    hintList = []
    shopCostList = []

    if "Settings String" in fileContents.keys():
        js.settings_string.value = fileContents["Settings String"]
        js.import_settings_string(None)

    # Set all of the options specified in the plando file.
    for option, value in fileContents.items():
        # Ignore settings strings here, we're always processing that first.
        if option == "Settings String":
            continue
        # Process item locations.
        if option == "locations":
            for location, item in value.items():
                # These items represent custom Kasplat locations and are
                # handled later.
                if location not in KasplatLocationEnumList:
                    js.document.getElementById(f"plando_{location}_item").value = item
        # Process shop costs.
        elif option == "prices":
            for location, price in value.items():
                shopElem = js.document.getElementById(f"plando_{location}_shop_cost")
                shopCostList.append(shopElem)
                shopElem.value = price
        # Process switches.
        elif option == "plando_switchsanity":
            for location, switchInfo in value.items():
                switchValue = switchInfo["kong"]
                if "switch_type" in switchInfo:
                    switchValue += f';{switchInfo["switch_type"]}'
                js.document.getElementById(f"plando_{location}_switch").value = switchValue
        # Process minigame selections.
        elif option == "plando_bonus_barrels":
            for location, minigame in value.items():
                js.document.getElementById(f"plando_{location}_minigame").value = minigame
        # Process custom locations.
        elif option in [
            "plando_place_arenas",
            "plando_place_crates",
            "plando_place_fairies",
            "plando_place_kasplats",
            "plando_place_patches",
            "plando_place_tns",
            "plando_place_wrinkly",
        ]:
            js.document.getElementById(option).checked = value
        elif option == "plando_battle_arenas":
            for enumLocation, customLocation in value.items():
                locValue = "" if customLocation == "Randomize" else customLocation
                js.document.getElementById(f"plando_{enumLocation}_location").value = locValue
                if enumLocation in fileContents["locations"]:
                    reward = fileContents["locations"][enumLocation]
                    js.document.getElementById(f"plando_{enumLocation}_location_reward").value = reward
        elif option == "plando_dirt_patches":
            for i, dirtPatch in enumerate(value):
                locationValue = "" if dirtPatch["location"] == "Randomize" else f'{dirtPatch["level"]};{dirtPatch["location"]}'
                js.document.getElementById(f"plando_patch_{i}_location").value = locationValue
                reward = "" if dirtPatch["reward"] == "Randomize" else dirtPatch["reward"]
                js.document.getElementById(f"plando_patch_{i}_location_reward").value = reward
        elif option == "plando_fairies":
            for i, fairy in enumerate(value):
                locationValue = "" if fairy["location"] == "Randomize" else f'{fairy["level"]};{fairy["location"]}'
                js.document.getElementById(f"plando_fairy_{i}_location").value = locationValue
                reward = "" if fairy["reward"] == "Randomize" else fairy["reward"]
                js.document.getElementById(f"plando_fairy_{i}_location_reward").value = reward
        elif option == "plando_kasplats":
            for enumLocation, customLocation in value.items():
                locValue = "" if customLocation == "Randomize" else customLocation
                js.document.getElementById(f"plando_{enumLocation}_location").value = locValue
                if enumLocation in fileContents["locations"]:
                    reward = fileContents["locations"][enumLocation]
                    js.document.getElementById(f"plando_{enumLocation}_location_reward").value = reward
        elif option == "plando_melon_crates":
            for i, crate in enumerate(value):
                locationValue = "" if crate["location"] == "Randomize" else f'{crate["level"]};{crate["location"]}'
                js.document.getElementById(f"plando_crate_{i}_location").value = locationValue
                reward = "" if crate["reward"] == "Randomize" else crate["reward"]
                js.document.getElementById(f"plando_crate_{i}_location_reward").value = reward
        elif option == "plando_tns_portals":
            for level, doorList in value.items():
                for i, door in enumerate(doorList):
                    locationValue = door
                    if door == "Randomize":
                        locationValue = ""
                    elif door == "":
                        locationValue = "none"
                    elemName = f"plando_{level}_{i}_tns_portal"
                    js.document.getElementById(elemName).value = locationValue
                # Set any remaining doors to "none".
                for i in range(len(doorList), 5):
                    elemName = f"plando_{level}_{i}_tns_portal"
                    js.document.getElementById(elemName).value = "none"
        elif option == "plando_wrinkly_doors":
            for enumLocation, doorLocation in value.items():
                locationValue = "" if doorLocation == "Randomize" else doorLocation
                elemName = f"plando_{enumLocation}_wrinkly_door"
                js.document.getElementById(elemName).value = locationValue
        # Process hints.
        elif option == "hints":
            for location, hint in value.items():
                hintElem = js.document.getElementById(f"plando_{location}_hint")
                hintList.append(hintElem)
                hintElem.value = hint
        # Process this one multi-select.
        elif option == "plando_starting_kongs_selected":
            starting_kongs = set()
            for kong in value:
                starting_kongs.add("" if kong == "Randomize" else kong)
            kongs_element = js.document.getElementById("plando_starting_kongs_selected")
            for i in range(6):
                starting_option = kongs_element.options.item(i)
                starting_option.selected = starting_option.value in starting_kongs
        # Process all other options.
        else:
            final_value = "" if value == "Randomize" else value
            js.document.getElementById(option).value = final_value

    # Run validation functions.
    for hintLocation in hintList:
        validate_hint_text(hintLocation)
    # for shopLocation in shopCostList:
    #     validate_shop_costs(shopLocation)
    plando_disable_keys(None)
    plando_disable_kong_items(None)
    js.plando_hide_helm_options(None)
    js.plando_hide_krool_options(None)
    js.plando_toggle_custom_arena_locations(None)
    js.plando_toggle_custom_crate_locations(None)
    js.plando_toggle_custom_fairy_locations(None)
    js.plando_toggle_custom_kasplat_locations(None)
    js.plando_toggle_custom_patch_locations(None)
    js.plando_toggle_custom_tns_locations(None)
    js.plando_toggle_custom_wrinkly_locations(None)
    js.plando_toggle_custom_locations_tab(None)
    js.plando_disable_isles_medals(None)
    js.plando_disable_krool_phases_as_bosses(None)
    lock_key_8_in_helm(None)
    validate_custom_arena_locations(None)
    validate_custom_crate_locations(None)
    validate_custom_fairy_locations(None)
    validate_custom_kasplat_locations(None)
    validate_custom_patch_locations(None)
    validate_custom_doors_no_duplicate_locations(None)
    validate_custom_locations_no_duplicates(None)
    validate_hint_count(None)
    validate_smaller_shops_no_conflict(None)
    validate_shuffle_shops_no_conflict(None)
    validate_starting_kong_count(None)
    validate_level_order_no_duplicates(None)
    validate_krool_order_no_duplicates(None)
    validate_helm_order_no_duplicates(None)
    validate_no_crate_items_with_shuffled_crates(None)
    validate_no_crown_items_with_shuffled_crowns(None)
    validate_no_dirt_items_with_shuffled_patches(None)
    validate_no_fairy_items_with_shuffled_fairies(None)
    validate_no_kasplat_items_with_location_shuffle(None)
    full_validate_no_reward_with_random_location()
    validate_item_limits(None)


def raise_plando_validation_error(err_string: str) -> None:
    """Raise an error and display a message about an invalid plando file."""
    plando_errors_element = js.document.getElementById("plando_import_errors")
    plando_errors_element.innerText = err_string
    plando_errors_element.style = ""
    raise ValueError(err_string)


def validate_plando_option_value(file_obj: dict, option: str, enum_type: type, field_type: str = "option") -> None:
    """Evaluate a given plando option to see if its value is valid.

    Args:
        file_obj (dict) - The object where the option can be found. Usually
            this is the entire plando file dictionary, but it may be a subset
            of it (i.e. only locations, or shop prices).
        option (str) - The name of the option being tested.
        enum_type (type) - The type of enum that we should attempt to convert
            the value to.
        field_type (str) - The type of field that has an invalid option. Only
            for error reporting purposes. E.g. "location", "minigame", "hint".
    """
    try:
        if option not in file_obj:
            return
        if file_obj[option] == "Randomize":
            return
        _ = enum_type[file_obj[option]]
    except KeyError:
        errString = f'The plandomizer file is invalid: {field_type} "{option}" has invalid value "{file_obj[option]}".'
        raise_plando_validation_error(errString)


def validate_plando_enum(item_name: str, enum_type: type, field_type: str = "option") -> None:
    """Validate that a given string represents an enum value."""
    try:
        _ = enum_type[item_name]
    except KeyError:
        errString = f'The plandomizer file is invalid: "{item_name}" is not a valid {field_type}.'
        raise_plando_validation_error(errString)


def validate_plando_location(location_name: str) -> None:
    """Validate that a given plando location is valid."""
    try:
        _ = Locations[location_name]
    except KeyError:
        errString = f'The plandomizer file is invalid: "{location_name}" is not a valid location.'
        raise_plando_validation_error(errString)


def validate_plando_switch_location(location_name: str) -> None:
    """Validate that a given plando switch location is valid."""
    try:
        _ = Switches[location_name]
    except KeyError:
        errString = f'The plandomizer file is invalid: "{location_name}" is not a valid switch location.'
        raise_plando_validation_error(errString)


def validate_custom_location(cust_location: dict, cust_set: set, loc_type: str) -> None:
    """Validate that a given custom location is valid.

    Args:
        cust_location (dict) - The object containing custom location data.
        cust_set (set) - The specific set where this location should be found.
        loc_type (str) - The kind of custom location, e.g. "dirt patch". Only
            used for logging errors.
    """
    for field in ["level", "location", "reward"]:
        if field not in cust_location:
            errString = f'The plandomizer file is invalid: a custom {loc_type} location is missing data field "{field}".'
            raise_plando_validation_error(errString)
    location = f'{cust_location["level"]}: {cust_location["location"]}'
    if location != "Randomize: Randomize" and location not in cust_set:
        errString = f'The plandomizer file is invalid: "{location}" is not a valid {loc_type} location.'
        raise_plando_validation_error(errString)
    reward = cust_location["reward"]
    if reward != "Randomize":
        try:
            _ = PlandoItems[reward]
        except KeyError:
            errString = f'The plandomizer file is invalid: custom {loc_type} location "{location}" has invalid reward "{reward}".'
            raise_plando_validation_error(errString)


def validate_custom_enum_location(enum_location: str, location_str: str, cust_set: set, loc_type: str) -> None:
    """Validate that a given enum-based custom location is valid.

    Args:
        enum_location (str) - The string name of the Location enum that this
            custom location is being assigned to.
        location_str (str) - The string representing the custom location.
        cust_set (set) - The specific set where this location should be found.
        loc_type (str) - The kind of custom location, e.g. "dirt patch". Only
            used for logging errors.
    """
    try:
        _ = Locations[enum_location]
    except KeyError:
        errString = f'The plandomizer file is invalid: "{enum_location}" is not a valid {loc_type} enum value.'
        raise_plando_validation_error(errString)
    if location_str not in cust_set:
        errString = f'The plandomizer file is invalid: "{location_str}" is not a valid {loc_type} location.'
        raise_plando_validation_error(errString)


def validate_fairy_position(fairy: dict, index: int) -> None:
    """Ensure fairies are assigned to the correct level."""
    fairyLevelIndexMap = {
        Levels.JungleJapes: 2,
        Levels.AngryAztec: 4,
        Levels.FranticFactory: 6,
        Levels.GloomyGalleon: 8,
        Levels.FungiForest: 10,
        Levels.CrystalCaves: 12,
        Levels.CreepyCastle: 14,
        Levels.DKIsles: 18,
        Levels.HideoutHelm: 20,
    }
    if fairy["level"] == "Randomize":
        return
    for level, i in fairyLevelIndexMap.items():
        if index < i:
            if fairy["level"] != level.name:
                errString = f'The plandomizer file is invalid: fairy {index+1} needs to be assigned to {level.name}, but is assigned to {fairy["level"]}.'
                raise_plando_validation_error(errString)
            return


def validate_door_location(door_name: str, level: Levels, door_dict: dict, field_name: str, none_allowed=True) -> None:
    """Validate a door location for a given level.

    Args:
        door_name (str) - The name of the door we are validating.
        level (Levels) - The level in which this door is being placed.
        door_dict (dict) - A dictionary of all possible doors that should be
            able to appear in each level.
        field_type (str) - The type of field that has an invalid option. Only
            for error reporting purposes. E.g. "location", "minigame", "hint".
    """
    if (door_name == "" and none_allowed) or door_name == "Randomize":
        return
    if door_name not in door_dict[level]:
        errString = f'The plandomizer file is invalid: door "{door_name}" is not a valid {field_name} for level {level.name}.'
        raise_plando_validation_error(errString)


def validate_plando_file(file_obj: dict) -> None:
    """Validate the contents of a given plando file."""
    # Hide the div for import errors.
    plando_errors_element = js.document.getElementById("plando_import_errors")
    plando_errors_element.style.display = "none"

    validate_plando_option_value(file_obj, "plando_starting_exit", Transitions)
    for starting_kong in file_obj["plando_starting_kongs_selected"]:
        if starting_kong != "Randomize":
            try:
                _ = Kongs[starting_kong]
            except KeyError as err:
                errString = f'The plandomizer file is invalid: option "plando_starting_kongs_selected" has invalid value "{starting_kong}".'
                raise_plando_validation_error(errString)
    # if file_obj["plando_101"] not in [True, False]:
    #     raise_plando_validation_error("plando_101", file_obj["plando_101"])
    for option in level_options:
        validate_plando_option_value(file_obj, option, Levels)
    for option in kong_options:
        validate_plando_option_value(file_obj, option, Kongs)

    # Inspect all item locations.
    for location in file_obj["locations"].keys():
        validate_plando_location(location)
        validate_plando_option_value(file_obj["locations"], location, PlandoItems, "location")
    # Inspect all switches.
    for switchLoc, switchInfo in file_obj["plando_switchsanity"].items():
        validate_plando_switch_location(switchLoc)
        if "kong" not in switchInfo:
            errString = f'The plandomizer file is invalid: switch "{switchLoc}" does not have the necessary field "kong".'
            raise_plando_validation_error(errString)
        validate_plando_option_value(switchInfo, "kong", Kongs)
        if switchLoc == "IslesHelmLobbyGone" and "switch_type" not in switchInfo:
            errString = f'The plandomizer file is invalid: switch "{switchLoc}" does not have the necessary field "switch_type".'
            raise_plando_validation_error(errString)
        if "switch_type" in switchInfo:
            validate_plando_option_value(switchInfo, "switch_type", SwitchType)
    # Inspect all minigames.
    for minigame in file_obj["plando_bonus_barrels"].keys():
        validate_plando_location(minigame)
        validate_plando_option_value(file_obj["plando_bonus_barrels"], minigame, Minigames, "minigame")
    # Inspect all shop prices.
    # for shop in file_obj["prices"].keys():
    #     validate_plando_location(shop)
    #     price = file_obj["prices"][shop]
    #     if not isinstance(price, int):
    #         errString = f'The plandomizer file is invalid: shop "{shop}" has invalid price "{price}".'
    #         raise_plando_validation_error(errString)
    # Inspect all custom locations.
    for patch in file_obj["plando_dirt_patches"]:
        validate_custom_location(patch, customLocationSet, "dirt patch")
    for crate in file_obj["plando_melon_crates"]:
        validate_custom_location(crate, customLocationSet, "melon crate")
    for i, fairy in enumerate(file_obj["plando_fairies"]):
        validate_custom_location(fairy, customFairyLocationSet, "fairy")
        validate_fairy_position(fairy, i)
    for arena, location in file_obj["plando_battle_arenas"].items():
        if location == "Randomize":
            continue
        try:
            level = LocationList[Locations[arena]].level.name
        except KeyError:
            errString = f'The plandomizer file is invalid: "{arena}" is not a valid battle arena enum value.'
            raise_plando_validation_error(errString)
        fullLocation = f"{level}: {location}"
        validate_custom_enum_location(arena, fullLocation, customLocationSet, "battle arena")
    for kasplat, location in file_obj["plando_kasplats"].items():
        if location == "Randomize":
            continue
        validate_custom_enum_location(kasplat, location, customKasplatLocationSet, "Kasplat")
    for wrinklyDoor, location in file_obj["plando_wrinkly_doors"].items():
        validate_plando_enum(wrinklyDoor, Locations, "Wrinkly door location")
        level = LocationList[Locations[wrinklyDoor]].level
        validate_door_location(location, level, customWrinklyDoorLocationSet, "Wrinkly door", False)
    for levelName, doorList in file_obj["plando_tns_portals"].items():
        validate_plando_enum(levelName, Levels, "level")
        level = Levels[levelName]
        if len(doorList) < 3 or len(doorList) > 5:
            errString = f"The plandomizer file is invalid: the list of TnS portals for level {levelName} should contain between 3 and 5 doors, but contains {len(doorList)}."
            raise_plando_validation_error(errString)
        for i, door in enumerate(doorList):
            validate_door_location(door, level, customTnsPortalLocationSet, "Troff 'n' Scoff portal")
    # Inspect all hints.
    for hint_location in file_obj["hints"].keys():
        validate_plando_location(hint_location)
        hint = file_obj["hints"][hint_location]
        if type(hint) is not str:
            errString = f'The plandomizer file is invalid: hint location "{hint_location}" has invalid hint "{hint}".'
            raise_plando_validation_error(errString)


@bind("click", "export_plando_settings")
def export_plando_options(evt):
    """Export the current plando settings to a JSON file."""
    form = js.jquery("#form").serializeArray()
    plandoData = populate_plando_options(form, True)
    js.export_settings_string(None)
    plandoData["Settings String"] = js.settings_string.value
    js.download_json_file(json.dumps(plandoData), "plando_settings.json")


@bind("change", "plando_starting_kongs_selected")
def plando_disable_kong_items(evt):
    """Do not allow starting Kongs to be placed as items."""
    starting_kongs = js.document.getElementById("plando_starting_kongs_selected")
    selected_kongs = {x.value for x in starting_kongs.selectedOptions}
    item_dropdowns = js.document.getElementsByClassName("plando-item-select")
    for kong in ["Donkey", "Diddy", "Lanky", "Tiny", "Chunky"]:
        if kong.lower() in selected_kongs:
            kong_options = js.document.getElementsByClassName(f"plando-{kong}-option")
            # Disable this Kong as a dropdown option.
            for option in kong_options:
                option.setAttribute("disabled", "disabled")
            # De-select this Kong everywhere they are selected.
            for dropdown in item_dropdowns:
                if dropdown.value == kong:
                    dropdown.value = ""
        else:
            kong_options = js.document.getElementsByClassName(f"plando-{kong}-option")
            # Re-enable this Kong as a dropdown option.
            for option in kong_options:
                option.removeAttribute("disabled")


# @bindList("click", [str(i) for i in range(1, 6)], prefix="starting_moves_list_mover_")
# @bindList("change", [str(i) for i in range(1, 6)], prefix="starting_moves_list_count_")
# @bind("click", "starting_moves_start_all")
# @bind("click", "starting_moves_start_vanilla")
# @bind("click", "starting_moves_reset")
# def plando_disable_starting_moves(evt):
#     """Do not allow starting moves to be placed as items."""
#     startingMoveSet = set()
#     # Look at every list, and if any list will have all of its items given,
#     # add those moves to the set.
#     for i in range(1, 6):
#         moveListElem = js.document.getElementById(f"starting_moves_list_{i}")
#         moveCountElem = js.document.getElementById(f"starting_moves_list_count_{i}")
#         givenMoveCount = 0 if moveCountElem.value == "" else int(moveCountElem.value)
#         listedMoveCount = 0
#         for opt in moveListElem.options:
#             if not opt.hidden:
#                 listedMoveCount += 1
#         if givenMoveCount == listedMoveCount:
#             for opt in moveListElem.options:
#                 moveId = re.search("^starting_move_(.+)$", opt.id)[1]
#                 plandoMove = ItemToPlandoItemMap[Items(int(moveId))]
#                 startingMoveSet.add(plandoMove)

#     # Obtain the list of PlandoItems moves to disable.
#     progressiveMoves = [
#         PlandoItems.ProgressiveAmmoBelt,
#         PlandoItems.ProgressiveInstrumentUpgrade,
#         PlandoItems.ProgressiveSlam,
#     ]
#     selectedPlandoMoves = set([move for move in startingMoveSet if move not in progressiveMoves])
#     # Progressive moves are handled differently. Only disable these if all
#     # instances are included as starting moves.
#     if set([Items.ProgressiveSlam, Items.ProgressiveSlam2, Items.ProgressiveSlam3]).issubset(startingMoveSet):
#         selectedPlandoMoves.add(PlandoItems.ProgressiveSlam)
#     if set([Items.ProgressiveAmmoBelt, Items.ProgressiveAmmoBelt2]).issubset(startingMoveSet):
#         selectedPlandoMoves.add(PlandoItems.ProgressiveAmmoBelt)
#     if set([Items.ProgressiveInstrumentUpgrade, Items.ProgressiveInstrumentUpgrade2, Items.ProgressiveInstrumentUpgrade3]).issubset(startingMoveSet):
#         selectedPlandoMoves.add(PlandoItems.ProgressiveInstrumentUpgrade)

#     # Disable all the plando moves across the dropdowns.
#     for moveName in js.MoveSet:
#         moveEnum = PlandoItems[moveName]
#         # Ignore these moves.
#         if moveEnum in {PlandoItems.Camera, PlandoItems.Shockwave}:
#             continue
#         move_options = js.document.getElementsByClassName(f"plando-{moveName}-option")
#         if moveEnum in selectedPlandoMoves:
#             # Disable this move as a dropdown option.
#             for option in move_options:
#                 option.setAttribute("disabled", "disabled")
#         else:
#             # Re-enable this move as a dropdown option.
#             for option in move_options:
#                 option.removeAttribute("disabled")
#     # Deselect all the plando moves across the dropdowns.
#     item_dropdowns = js.document.getElementsByClassName("plando-item-select")
#     for dropdown in item_dropdowns:
#         if dropdown.value == "":
#             continue
#         move = PlandoItems[dropdown.value]
#         if move in selectedPlandoMoves:
#             dropdown.value = ""


@bind("click", "key_8_helm")
@bind("click", "select_keys")
@bind("click", "starting_keys_list_selected")
def plando_disable_keys(evt):
    """Disable keys from being selected for locations in the plandomizer, depending on the current settings."""
    # This dict will map our key strings to enum values.
    keyDict = {
        1: "JungleJapesKey",
        2: "AngryAztecKey",
        3: "FranticFactoryKey",
        4: "GloomyGalleonKey",
        5: "FungiForestKey",
        6: "CrystalCavesKey",
        7: "CreepyCastleKey",
        8: "HideoutHelmKey",
    }
    # Determine which keys are enabled and which are disabled.
    disabled_keys = set()
    if js.document.getElementById("select_keys").checked:
        starting_keys_list_selected = js.document.getElementById("starting_keys_list_selected")
        # All keys the user starts with are disabled.
        disabled_keys.update({x.value for x in starting_keys_list_selected.selectedOptions})
    # If Key 8 is locked in Helm, it gets disabled.
    if js.document.getElementById("key_8_helm").checked:
        disabled_keys.add("HideoutHelmKey")
    item_dropdowns = js.document.getElementsByClassName("plando-item-select")
    # Look at every key and react if it's enabled or disabled.
    for i in range(1, 9):
        key_string = keyDict[i]
        if key_string in disabled_keys:
            key_options = js.document.getElementsByClassName(f"plando-{key_string}-option")
            # Disable this key as a dropdown option.
            for option in key_options:
                option.setAttribute("disabled", "disabled")
            # De-select this key everywhere it is selected.
            for dropdown in item_dropdowns:
                if dropdown.value == key_string:
                    dropdown.value = ""
        else:
            key_options = js.document.getElementsByClassName(f"plando-{key_string}-option")
            # Re-enable this key as a dropdown option.
            for option in key_options:
                option.removeAttribute("disabled")
