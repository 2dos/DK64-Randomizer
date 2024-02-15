"""Methods to handle plando settings importing and exporting."""

from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Minigames import Minigames
from randomizer.Enums.Plandomizer import PlandoItems

import js
import json
from ui.bindings import bind
from ui.download import download_json_file
from ui.generate_buttons import export_settings_string, import_settings_string
from ui.plando_validation import (
    lock_key_8_in_helm,
    populate_plando_options,
    reset_plando_options_no_prompt,
    validate_group_limits,
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
from ui.rando_options import (
    plando_disable_camera_shockwave,
    plando_disable_keys,
    plando_disable_kong_items,
    plando_hide_helm_options,
    plando_hide_krool_options,
)


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
        import_settings_string(None)

    # Set all of the options specified in the plando file.
    for option, value in fileContents.items():
        # Ignore settings strings here, we're always processing that first.
        if option == "Settings String":
            continue
        # Process item locations.
        if option == "locations":
            for location, item in value.items():
                js.document.getElementById(f"plando_{location}_item").value = item
        # Process shop costs.
        elif option == "prices":
            for location, price in value.items():
                shopElem = js.document.getElementById(f"plando_{location}_shop_cost")
                shopCostList.append(shopElem)
                shopElem.value = price
        # Process minigame selections.
        elif option == "plando_bonus_barrels":
            for location, minigame in value.items():
                js.document.getElementById(f"plando_{location}_minigame").value = minigame
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
    plando_disable_camera_shockwave(None)
    plando_disable_keys(None)
    plando_disable_kong_items(None)
    plando_hide_helm_options(None)
    plando_hide_krool_options(None)
    lock_key_8_in_helm(None)
    validate_item_limits(None)
    validate_group_limits(None)
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
    js.savesettings()


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


def validate_plando_location(location_name: str) -> None:
    """Validate that a given plando location is valid."""
    try:
        _ = Locations[location_name]
    except KeyError:
        errString = f'The plandomizer file is invalid: "{location_name}" is not a valid location.'
        raise_plando_validation_error(errString)


def validate_plando_file(file_obj: dict) -> None:
    """Validate the contents of a given plando file."""
    # Hide the div for import errors.
    plando_errors_element = js.document.getElementById("plando_import_errors")
    plando_errors_element.style.display = "none"

    # validate_plando_option_value(file_obj, "plando_spawn_location", Locations)
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
    export_settings_string(None)
    plandoData["Settings String"] = js.settings_string.value
    download_json_file(plandoData, "plando_settings.json")
