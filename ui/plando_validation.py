"""Code to collect and validate the selected plando options."""
import json
import re

import js
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Minigames import Minigames
from randomizer.Enums.Plandomizer import ItemToPlandoItemMap, PlandoItems
from randomizer.Enums.Regions import Regions
from randomizer.Lists.Item import StartingMoveOptions
from randomizer.Lists.Location import LocationListOriginal as LocationList
from randomizer.Lists.Plandomizer import HintLocationList, ItemLocationList, MinigameLocationList, PlannableItemLimits, ShopLocationKongMap, ShopLocationList
from randomizer.LogicFiles.Shops import LogicRegions
from randomizer.PlandoUtils import GetNameFromPlandoItem, PlandoEnumMap
from ui.bindings import bind, bindList
from ui.rando_options import (
    plando_disable_camera_shockwave,
    plando_disable_keys,
    plando_disable_kong_items,
    plando_hide_helm_options,
    plando_hide_krool_options,
    plando_lock_key_8_in_helm,
)


def mark_option_invalid(element, tooltip: str) -> None:
    """Add a Bootstrap tooltip to the given element, and mark it as invalid."""
    element.setAttribute("data-bs-original-title", tooltip)
    element.classList.add("invalid")


def mark_option_valid(element) -> None:
    """Remove a Bootstrap tooltip from the given element, and mark it as valid."""
    element.setAttribute("data-bs-original-title", "")
    element.classList.remove("invalid")


def count_items() -> dict:
    """Count all currently placed items to ensure limits aren't exceeded.

    The result will be a dictionary, where each item is linked to all of the
    HTML selects that have this item selected.
    """
    count_dict = {}

    def add_all_items(locList: list[str], suffix: str):
        """Add all items from the location list into the dict."""
        for itemLocation in locList:
            elemName = f"plando_{itemLocation}{suffix}"
            elemValue = js.document.getElementById(elemName).value
            # The default value, for when no selection is made.
            plandoItemEnum = PlandoItems.Randomize
            if elemValue != "":
                plandoItemEnum = PlandoItems[elemValue]
            if plandoItemEnum in count_dict:
                count_dict[plandoItemEnum].append(elemName)
            else:
                count_dict[plandoItemEnum] = [elemName]

    add_all_items(ItemLocationList, "_item")
    add_all_items(ShopLocationList, "_item")
    return count_dict


def get_shop_location_element(locName: str):
    """Get the element corresponding to the dropdown for this location."""
    return js.document.getElementById(f"plando_{locName}_item")


def shop_has_assigned_item(shopElement) -> bool:
    """Return true if the given shop has an item assigned to it."""
    return shopElement.value and shopElement.value != "NoItem"


############
# BINDINGS #
############

startingMoveValues = [str(item.value) for item in StartingMoveOptions]


@bindList("click", startingMoveValues, prefix="none-")
@bindList("click", startingMoveValues, prefix="start-")
@bindList("click", startingMoveValues, prefix="random-")
@bindList("change", ItemLocationList, prefix="plando_", suffix="_item")
@bindList("change", ShopLocationList, prefix="plando_", suffix="_item")
@bind("click", "starting_moves_reset")
@bind("click", "starting_moves_start_all")
def validate_item_limits(evt):
    """Raise an error if any item has been placed too many times."""
    count_dict = count_items()
    # Add in starting moves, which also count toward the totals.
    startingMoveSet = set()
    for startingMove in StartingMoveOptions:
        startingMoveElem = js.document.getElementById(f"start-{str(startingMove.value)}")
        if startingMoveElem.checked:
            plandoMove = ItemToPlandoItemMap[startingMove]
            startingMoveSet.add(plandoMove)
            if plandoMove in count_dict:
                # Add in None, so we don't attempt to mark a nonexistent
                # element.
                count_dict[plandoMove].append(None)
            else:
                count_dict[plandoMove] = [None]
    for item, locations in count_dict.items():
        if item not in PlannableItemLimits:
            for loc in locations:
                if loc is not None:
                    mark_option_valid(js.document.getElementById(loc))
            continue
        itemCount = len(locations)
        if item == PlandoItems.GoldenBanana:
            # Add 40 items to account for blueprint rewards.
            itemCount += 40
        itemMax = PlannableItemLimits[item]
        if itemCount > itemMax:
            maybePluralTimes = "time" if itemMax == 1 else "times"
            maybeStartingMoves = " (This includes starting moves.)" if None in locations else ""
            errString = f'Item "{GetNameFromPlandoItem(item)}" can be placed at most {itemMax} {maybePluralTimes}, but has been placed {itemCount} times.{maybeStartingMoves}'
            if item == PlandoItems.GoldenBanana:
                errString += " (40 Golden Bananas are always allocated to blueprint rewards.)"
            for loc in locations:
                if loc is not None:
                    mark_option_invalid(js.document.getElementById(loc), errString)
        else:
            for loc in locations:
                if loc is not None:
                    mark_option_valid(js.document.getElementById(loc))


@bindList("change", ShopLocationList, prefix="plando_", suffix="_item")
def validate_shop_kongs(evt):
    """Raise an error if a shop has both individual and shared rewards."""
    errString = "Shop vendors cannot have both shared rewards and Kong rewards assigned in the same level."
    for _, vendors in ShopLocationKongMap.items():
        for _, vendor_locations in vendors.items():
            # Check the shared location for this vendor.
            if not vendor_locations["shared"]:
                # This vendor is not in this level.
                continue
            vendor_shared_element = get_shop_location_element(vendor_locations["shared"]["name"])
            if not shop_has_assigned_item(vendor_shared_element):
                # This vendor has nothing assigned for its shared location.
                continue
            # Check each of the individual locations.
            shared_location_valid = True
            for location in vendor_locations["individual"]:
                vendor_element = get_shop_location_element(location["name"])
                if shop_has_assigned_item(vendor_element):
                    # An individual shop has an assigned item.
                    # This is always a conflict at this point.
                    shared_location_valid = False
                    mark_option_invalid(vendor_element, errString)
                else:
                    mark_option_valid(vendor_element)
            if shared_location_valid:
                mark_option_valid(vendor_shared_element)
            else:
                mark_option_invalid(vendor_shared_element, errString)


@bindList("change", ShopLocationList, prefix="plando_", suffix="_item")
@bind("change", "smaller_shops")
def validate_smaller_shops_no_conflict(evt):
    """Raise an error if we have a conflict with Smaller Shops.

    If the user is using the Smaller Shops setting, they cannot place anything
    in the shops. This causes fill issues.
    """
    assignedShops = []
    for locationName in ShopLocationList:
        shopElem = js.document.getElementById(f"plando_{locationName}_item")
        mark_option_valid(shopElem)
        if shopElem.value != "":
            assignedShops.append(shopElem)
    useSmallerShops = js.document.getElementById("smaller_shops").checked
    if not useSmallerShops:
        return
    for assignedShop in assignedShops:
        mark_option_invalid(assignedShop, 'Shop locations cannot be assigned if "Smaller Shops" is selected.')


@bindList("change", HintLocationList, prefix="plando_", suffix="_hint")
@bindList("keyup", HintLocationList, prefix="plando_", suffix="_hint")
def validate_hint_text_binding(evt):
    """Raise an error if this target's hint contains invalid characters."""
    validate_hint_text(evt.target)


def validate_hint_text(element) -> None:
    """Raise an error if the element's hint contains invalid characters."""
    hintString = element.value
    if re.search("[^A-Za-z0-9 \,\.\-\?!]", hintString) is not None:
        mark_option_invalid(element, "Only letters, numbers, spaces, and the characters ',.-?! are allowed in hints.")
    else:
        mark_option_valid(element)


@bindList("change", HintLocationList, prefix="plando_", suffix="_hint")
@bindList("keyup", HintLocationList, prefix="plando_", suffix="_hint")
@bind("change", "wrinkly_hints")
def validate_hint_count(evt):
    """Raise an error if there are too many hints for the current settings."""
    # Mark all hints as valid, since we don't know which ones were recently
    # removed, and take note of all the plando'd hints.
    plandoHintList = []
    for hint in HintLocationList:
        hintElem = js.document.getElementById(f"plando_{hint}_hint")
        mark_option_valid(hintElem)
        if hintElem.value != "":
            plandoHintList.append(hintElem)
    # If we're not using fixed hints, return here after we've marked all the
    # hints as valid.
    if js.document.getElementById("wrinkly_hints").value != "fixed_racing":
        return
    # If there are more than five hints, and we are using fixed hints, this is
    # an error.
    if len(plandoHintList) > 5:
        for hintElem in plandoHintList:
            mark_option_invalid(hintElem, "Fixed hints are incompatible with more than 5 plandomized hints.")


@bindList("change", ShopLocationList, prefix="plando_", suffix="_shop_cost")
@bindList("keyup", ShopLocationList, prefix="plando_", suffix="_shop_cost")
def validate_shop_costs_binding(evt):
    """Raise an error if this target's shop has an invalid cost."""
    validate_shop_costs(evt.target)


def validate_shop_costs(element) -> None:
    """Raise an error if this element's shop has an invalid cost."""
    shopCost = element.value
    if shopCost == "":
        mark_option_valid(element)
    elif shopCost.isdigit() and int(shopCost) >= 0 and int(shopCost) <= 255:
        mark_option_valid(element)
    else:
        mark_option_invalid(element, "Shop costs must be a whole number between 0 and 255.")


@bind("change", "starting_kongs_count")
@bind("change", "plando_starting_kongs_selected")
def validate_starting_kong_count(evt):
    """Raise an error if the starting Kongs don't match the selected count."""
    startingKongs = js.document.getElementById("plando_starting_kongs_selected")
    selectedKongs = {x.value for x in startingKongs.selectedOptions}
    numStartingKongs = int(js.document.getElementById("starting_kongs_count").value)
    isRandomStartingKongCount = js.document.getElementById("starting_random").checked
    if isRandomStartingKongCount:
        # With a random starting Kong count, everything is fair game in this box and it'll try to meet expectations as best as it can
        mark_option_valid(startingKongs)
    elif len(selectedKongs) > numStartingKongs or (len(selectedKongs) < numStartingKongs and "" not in selectedKongs):
        maybePluralKongText = "Kong was selected as a starting Kong" if len(selectedKongs) == 1 else "Kongs were selected as starting Kongs"
        errSuffix = "." if len(selectedKongs) > numStartingKongs else ', and "Random Kong(s)" was not chosen.'
        errString = f"The number of starting Kongs was set to {numStartingKongs}, but {len(selectedKongs)} {maybePluralKongText}{errSuffix}"
        mark_option_invalid(startingKongs, errString)
    else:
        mark_option_valid(startingKongs)


@bind("change", "plando_level_order_", 7)
def validate_level_order_no_duplicates(evt):
    """Raise an error if the same level is chosen twice in the level order."""
    levelDict = {}
    # Count the instances of each level.
    for i in range(0, 7):
        levelElemName = f"plando_level_order_{i}"
        levelOrderElem = js.document.getElementById(levelElemName)
        level = levelOrderElem.value
        if level in levelDict:
            levelDict[level].append(levelElemName)
        else:
            levelDict[level] = [levelElemName]
    # Invalidate any selects that re-use the same level.
    for level, selects in levelDict.items():
        if level == "" or len(selects) == 1:
            for select in selects:
                selectElem = js.document.getElementById(select)
                mark_option_valid(selectElem)
        else:
            for select in selects:
                selectElem = js.document.getElementById(select)
                mark_option_invalid(selectElem, "The same level cannot be used twice in the level order.")


@bind("change", "plando_krool_order_", 5)
def validate_krool_order_no_duplicates(evt):
    """Raise an error if the same Kong is chosen twice in the K. Rool order."""
    kongDict = {}
    # Count the instances of each Kong.
    for i in range(0, 5):
        kroolElemName = f"plando_krool_order_{i}"
        kroolOrderElem = js.document.getElementById(kroolElemName)
        kong = kroolOrderElem.value
        if kong in kongDict:
            kongDict[kong].append(kroolElemName)
        else:
            kongDict[kong] = [kroolElemName]
    # Invalidate any selects that re-use the same Kong.
    for kong, selects in kongDict.items():
        if kong == "" or len(selects) == 1:
            for select in selects:
                selectElem = js.document.getElementById(select)
                mark_option_valid(selectElem)
        else:
            for select in selects:
                selectElem = js.document.getElementById(select)
                mark_option_invalid(selectElem, "The same Kong cannot be used twice in the K. Rool order.")


@bind("change", "plando_helm_order_", 5)
def validate_helm_order_no_duplicates(evt):
    """Raise an error if the same Kong is chosen twice in the Helm order."""
    kongDict = {}
    # Count the instances of each Kong.
    for i in range(0, 5):
        helmElemName = f"plando_helm_order_{i}"
        helmOrderElem = js.document.getElementById(helmElemName)
        kong = helmOrderElem.value
        if kong in kongDict:
            kongDict[kong].append(helmElemName)
        else:
            kongDict[kong] = [helmElemName]
    # Invalidate any selects that re-use the same Kong.
    for kong, selects in kongDict.items():
        if kong == "" or len(selects) == 1:
            for select in selects:
                selectElem = js.document.getElementById(select)
                mark_option_valid(selectElem)
        else:
            for select in selects:
                selectElem = js.document.getElementById(select)
                mark_option_invalid(selectElem, "The same Kong cannot be used twice in the Helm order.")


@bind("click", "nav-plando-tab")
def validate_on_nav(evt):
    """Fallback for errors with Bootstrap sliders."""
    validate_starting_kong_count(evt)


@bind("click", "export_plando_string")
def export_plando_string(evt):
    """Generate the plando json string."""
    # Serialize the form into json
    form = js.jquery("#form").serializeArray()

    # Plandomizer data is processed separately.
    plando_form_data = populate_plando_options(form)
    js.plando_string.value = json.dumps(plando_form_data)


######################
# SETTINGS FUNCTIONS #
######################


@bind("click", "import_plando_settings")
def plando_filebox(evt):
    """Open a file upload prompt and begin importing plando settings."""
    input = js.document.createElement("input")
    input.type = "file"
    input.accept = ".json"

    input.onchange = lambda e: import_plando_options(e.target.files.item(0))

    input.click()


async def import_plando_options(file):
    """Import plando settings from a provided JSON file."""
    fileText = await file.text()
    fileContents = json.loads(fileText)

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

    # Set all of the options specified in the plando file.
    for option, value in fileContents.items():
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
        elif option == "minigames":
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
    plando_lock_key_8_in_helm(None)
    validate_item_limits(None)
    validate_hint_count(None)
    validate_smaller_shops_no_conflict(None)
    validate_starting_kong_count(None)
    validate_level_order_no_duplicates(None)
    validate_krool_order_no_duplicates(None)
    validate_helm_order_no_duplicates(None)
    js.savesettings()


# Plando options where the value is of type Levels.
level_options = ["plando_level_order_0", "plando_level_order_1", "plando_level_order_2", "plando_level_order_3", "plando_level_order_4", "plando_level_order_5", "plando_level_order_6"]
# Plando options where the value is of type Kongs.
kong_options = [
    "plando_kong_rescue_diddy",
    "plando_kong_rescue_lanky",
    "plando_kong_rescue_tiny",
    "plando_kong_rescue_chunky",
    "plando_krool_order_0",
    "plando_krool_order_1",
    "plando_krool_order_2",
    "plando_krool_order_3",
    "plando_krool_order_4",
    "plando_helm_order_0",
    "plando_helm_order_1",
    "plando_helm_order_2",
    "plando_helm_order_3",
    "plando_helm_order_4",
]


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
    # for minigame in file_obj["minigames"].keys():
    #     validate_plando_location(minigame)
    #     validate_plando_option_value(file_obj["minigames"], minigame, Minigames, "minigame")
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
    plandoFileData = json.dumps(populate_plando_options(form, True), indent=4)

    # Create a link to the file and download it automatically.
    blob = js.Blob.new([plandoFileData], {type: "application/json"})
    blob.name = "plando_settings.json"
    url = js.window.URL.createObjectURL(blob)
    link = js.document.createElement("a")
    link.href = url
    link.download = blob.name
    js.document.body.appendChild(link)
    link.click()

    # Delete the link.
    js.document.body.removeChild(link)
    js.window.URL.revokeObjectURL(url)


@bind("click", "reset_plando_settings")
def reset_plando_options(evt):
    """Return all plandomizer options to their default settings.

    Issues a prompt first, warning the user.
    """
    if js.window.confirm("Are you sure you want to reset all plandomizer settings?"):
        reset_plando_options_no_prompt()
        js.savesettings()


def reset_plando_options_no_prompt() -> None:
    """Return all plandomizer options to their default settings."""
    # Reset general settings.

    # These settings are TBD
    # js.document.getElementById("plando_spawn_location").value = ""
    # js.document.getElementById("plando_101").value = False

    for option in level_options + kong_options:
        option_element = js.document.getElementById(option)
        option_element.value = ""
        mark_option_valid(option_element)
    kongs_element = js.document.getElementById("plando_starting_kongs_selected")
    kongs_element.options.item(0).selected = True
    for i in range(1, 6):
        kongs_element.options.item(i).selected = False
    mark_option_valid(kongs_element)

    for location in ItemLocationList + ShopLocationList:
        location_element = js.document.getElementById(f"plando_{location}_item")
        location_element.value = ""
        mark_option_valid(location_element)
    for shop in ShopLocationList:
        # Skip the Rareware Coin location, which has no price.
        if shop == "RarewareCoin":
            continue
        price_element = js.document.getElementById(f"plando_{shop}_shop_cost")
        price_element.value = ""
        mark_option_valid(price_element)
    for minigame in MinigameLocationList:
        minigame_element = js.document.getElementById(f"plando_{minigame}_minigame")
        minigame_element.value = ""
        mark_option_valid(minigame_element)
    for hint in HintLocationList:
        hint_element = js.document.getElementById(f"plando_{hint}_hint")
        hint_element.value = ""
        mark_option_valid(hint_element)

    # Fire off a few functions that should react to changes.
    plando_disable_kong_items(None)


def populate_plando_options(form: dict, for_plando_file: bool = False) -> dict:
    """Collect all of the plandomizer options into one object.

    Args:
        form (dict) - The serialized form data containing all HTML inputs.
        for_plando_file (boolean) - True if the output is intended for a
            plando file. Some data will not be written out, and enums will
            be written with their string names instead of their int values.
    Returns:
        plando_form_data (dict) - The collected plando data. May be None if
            plandomizer is disabled, or the selections are invalid.
    """
    # If the plandomizer is disabled, return nothing.
    enable_plandomizer = js.document.getElementById("enable_plandomizer")
    if not enable_plandomizer.checked:
        return None

    plando_form_data = {}
    item_objects = []
    shop_cost_objects = []
    minigame_objects = []
    hint_objects = []

    def is_number(s) -> bool:
        """Check if a string is a number or not."""
        try:
            int(s)
            return True
        except ValueError:
            return False

    def get_plando_value(enum_val):
        """Return either the value of a given enum or the display name."""
        return enum_val.name if for_plando_file else enum_val

    def get_enum_or_string_value(valueString: str, settingName: str):
        """Obtain the enum or string value for the provided setting.

        Args:
            valueString (str) - The value from the HTML input.
            settingName (str) - The name of the HTML input.
        """
        # Convert empty string values to PlandoItems.Randomize.
        # This is always valid for the plandomizer specifically.
        if valueString == "":
            return get_plando_value(PlandoItems.Randomize)
        elif settingName in PlandoEnumMap:
            return get_plando_value(PlandoEnumMap[settingName][valueString])
        else:
            return valueString

    def is_plando_input(inputName: str) -> bool:
        """Determine if an input is a plando input."""
        return inputName is not None and inputName.startswith("plando_")

    # Process all the plando-related inputs.
    for obj in form:
        if not is_plando_input(obj.name):
            continue
        if obj.name == "plando_string":  # Don't export the plando string, it causes headaches
            continue
        # Sort the selects into their appropriate lists.
        if obj.name.endswith("_shop_cost"):
            shop_cost_objects.append(obj)
            continue
        elif obj.name.endswith("_item"):
            item_objects.append(obj)
            continue
        elif obj.name.endswith("_minigame"):
            minigame_objects.append(obj)
            continue
        elif obj.name.endswith("_hint"):
            hint_objects.append(obj)
            continue

        # Process any input that hasn't been sorted.
        if obj.value.lower() in ["true", "false"]:
            plando_form_data[obj.name] = bool(obj.value)
        else:
            if is_number(obj.value):
                plando_form_data[obj.name] = int(obj.value)
            else:
                plando_form_data[obj.name] = get_enum_or_string_value(obj.value, obj.name)

    # Find all input boxes and verify their checked status.
    for element in js.document.getElementsByTagName("input"):
        if not is_plando_input(element.name):
            continue
        if element.type == "checkbox" and not element.checked:
            if not plando_form_data.get(element.name):
                plando_form_data[element.name] = False

    # Modify multi-selects to provide value lists.
    for element in js.document.getElementsByTagName("select"):
        if not is_plando_input(element.getAttribute("name")):
            continue
        if element.getAttribute("name").endswith("_selected"):
            length = element.options.length
            values = []
            for i in range(0, length):
                if element.options.item(i).selected:
                    val = get_enum_or_string_value(element.options.item(i).value, element.getAttribute("name"))
                    values.append(val)
            plando_form_data[element.getAttribute("name")] = values

    locations_map = {}
    # Process all of the inputs we previously sorted into lists.
    for item in item_objects:
        # Extract the location name.
        location_name = re.search("^plando_(.+)_item$", item.name)[1]
        location = get_plando_value(Locations[location_name])
        if item.value != "":
            locations_map[location] = get_plando_value(PlandoItems[item.value])
    # Revisit all of this when BPs aren't always on blueprint rewards
    # Place Golden Bananas on all of the blueprint rewards. Don't bother adding this for plando files.
    # if not for_plando_file:
    # for blueprint in LogicRegions[Regions.Snide].locations:
    #     locations_map[blueprint.id] = PlandoItems.GoldenBanana
    plando_form_data["locations"] = locations_map

    shops_map = {}
    for shop_cost in shop_cost_objects:
        # Extract the location name.
        location_name = re.search("^plando_(.+)_shop_cost$", shop_cost.name)[1]
        location = get_plando_value(Locations[location_name])
        if shop_cost.value != "":
            item_cost = int(shop_cost.value)
            shops_map[location] = item_cost
    plando_form_data["prices"] = shops_map

    # Minigame picking coming in future version
    # minigames_map = {}
    # for minigame in minigame_objects:
    #     # Extract the barrel location name.
    #     location_name = re.search("^plando_(.+)_minigame$", minigame.name)[1]
    #     location = get_plando_value(Locations[location_name])
    #     if minigame.value != "":
    #         minigames_map[location] = get_plando_value(Minigames[minigame.value])
    # plando_form_data["minigames"] = minigames_map

    hints_map = {}
    for hint in hint_objects:
        # Extract the hint location.
        location_name = re.search("^plando_(.+)_hint$", hint.name)[1]
        location = get_plando_value(Locations[location_name])
        if hint.value != "":
            hints_map[location] = hint.value
    plando_form_data["hints"] = hints_map

    return plando_form_data


def validate_plando_options(settings_dict: dict) -> list[str]:
    """Validate the plando options against a set of rules.

    Args:
        settings_dict (dict) - The dictionary containing the full settings.
    Returns:
        err (str[]) - A list of error strings to be displayed to the user.
            Will be an empty list if there are no errors.
    """
    if "plandomizer_data" not in settings_dict:
        return []

    plando_dict = json.loads(settings_dict["plandomizer_data"])
    errList = []
    # Count all of the items to ensure none have been over-placed.
    count_dict = {}
    for item in plando_dict["locations"].values():
        if item == PlandoItems.Randomize:
            continue
        if item in count_dict:
            count_dict[item] += 1
        else:
            count_dict[item] = 1
    # Add in starting moves, which also count toward the totals.
    startingMoveSet = set()
    for startingMove in StartingMoveOptions:
        startingMoveElem = js.document.getElementById(f"start-{str(startingMove.value)}")
        if startingMoveElem.checked:
            plandoMove = ItemToPlandoItemMap[startingMove]
            startingMoveSet.add(plandoMove)
            if plandoMove in count_dict:
                count_dict[plandoMove] += 1
            else:
                count_dict[plandoMove] = 1
    # If any items have exceeded their maximum amounts, add an error.
    for item, itemCount in count_dict.items():
        if item not in PlannableItemLimits:
            continue
        itemMax = PlannableItemLimits[item]
        if itemCount > itemMax:
            maybePluralTimes = "time" if itemMax == 1 else "times"
            errString = f'Item "{GetNameFromPlandoItem(item)}" can be placed at most {itemMax} {maybePluralTimes}, but has been placed {itemCount} times.'
            if item in startingMoveSet:
                errString += " (This includes starting moves.)"
            if item == PlandoItems.GoldenBanana:
                errString += " (40 Golden Bananas are always allocated to blueprint rewards.)"
            errList.append(errString)

    # Ensure that no shop has both a shared reward and an individual reward.
    errString = "Shop vendors cannot have both shared rewards and Kong rewards assigned in the same level."
    for _, vendors in ShopLocationKongMap.items():
        for _, vendor_locations in vendors.items():
            # Check the shared location for this vendor.
            vendor_shared = vendor_locations["shared"]
            if not vendor_shared:
                # This vendor is not in this level.
                continue
            vendor_shared_element = get_shop_location_element(vendor_shared["name"])
            if not shop_has_assigned_item(vendor_shared_element):
                # This vendor has nothing assigned for its shared location.
                continue
            # Check each of the individual locations.
            for ind_location in vendor_locations["individual"]:
                vendor_element = get_shop_location_element(ind_location["name"])
                if shop_has_assigned_item(vendor_element):
                    # An individual shop has an assigned item.
                    # This is always a conflict at this point.
                    shared_shop_name = vendor_shared["value"].name
                    ind_shop_name = ind_location["value"].name
                    errString = f'Shop locations "{shared_shop_name}" and "{ind_shop_name}" both have rewards assigned, which is invalid.'
                    errList.append(errString)

    # Ensure that no shops are assigned if "Smaller Shops" is used.
    useSmallerShops = js.document.getElementById("smaller_shops").checked
    if useSmallerShops:
        for locationName in ShopLocationList:
            locationEnum = Locations[locationName]
            locEnumStr = str(locationEnum.value)
            if locEnumStr in plando_dict["locations"] and plando_dict["locations"][locEnumStr] != PlandoItems.Randomize:
                shopName = LocationList[locationEnum].name
                errString = f'Shop locations cannot be assigned if "Smaller Shops" is selected, but shop "{shopName}" has an assigned value.'
                errList.append(errString)

    # Ensure that shop costs are within allowed limits.
    for shopLocation, price in plando_dict["prices"].items():
        if price == PlandoItems.Randomize:
            continue
        if price < 0 or price > 255:
            shopName = LocationList[shopLocation].name
            errString = f'Shop costs must be between 0 and 255 coins, but shop "{shopName}" has a cost of {price} coins.'
            errList.append(errString)

    # Ensure that the number of chosen Kongs matches the "number of starting
    # Kongs" setting, or that "Random Kong(s)" has been chosen. If too many
    # Kongs have been selected, that is always an error.
    chosenKongs = plando_dict["plando_starting_kongs_selected"]
    numStartingKongs = int(settings_dict["starting_kongs_count"])
    isRandomStartingKongCount = js.document.getElementById("starting_random").checked
    if not isRandomStartingKongCount and (len(chosenKongs) > numStartingKongs or (len(chosenKongs) < numStartingKongs and PlandoItems.Randomize not in chosenKongs)):
        maybePluralKongText = "Kong was selected as a starting Kong" if len(chosenKongs) == 1 else "Kongs were selected as starting Kongs"
        errSuffix = "." if len(chosenKongs) > numStartingKongs else ', and "Random Kong(s)" was not chosen.'
        errString = f"The number of starting Kongs was set to {numStartingKongs}, but {len(chosenKongs)} {maybePluralKongText}{errSuffix}"
        errList.append(errString)

    # Ensure that no level was selected more than once in the level order.
    levelOrderSet = set()
    for i in range(0, 7):
        level = plando_dict[f"plando_level_order_{i}"]
        if level == PlandoItems.Randomize:
            continue
        if level in levelOrderSet:
            errString = "The same level cannot be used twice in the level order."
            errList.append(errString)
            break
        else:
            levelOrderSet.add(level)

    # Ensure that no Kong was selected more than once in the K. Rool order.
    kroolOrderSet = set()
    for i in range(0, 5):
        kong = plando_dict[f"plando_krool_order_{i}"]
        if kong == PlandoItems.Randomize:
            continue
        if kong in kroolOrderSet:
            errString = "The same Kong cannot be used twice in the K. Rool order."
            errList.append(errString)
            break
        else:
            kroolOrderSet.add(kong)

    # Ensure that no Kong was selected more than once in the Helm order.
    helmOrderSet = set()
    for i in range(0, 5):
        kong = plando_dict[f"plando_helm_order_{i}"]
        if kong == PlandoItems.Randomize:
            continue
        if kong in helmOrderSet:
            errString = "The same Kong cannot be used twice in the Helm order."
            errList.append(errString)
            break
        else:
            helmOrderSet.add(kong)

    # Ensure that hints are below the length limit and have valid characters.
    for hintLocation, hint in plando_dict["hints"].items():
        if hint == PlandoItems.Randomize:
            continue
        hintLocationName = LocationList[int(hintLocation)].name
        if len(hint) > 123:
            errString = f'The hint for location "{hintLocationName}" is longer than the limit of 123 characters.'
            errList.append(errString)
        if re.search("[^A-Za-z0-9 '\,\.\-\?!]", hint) is not None:
            errString = f'The hint for location "{hintLocationName}" contains invalid characters. Only letters, numbers, spaces, and the characters \',.-?! are valid.'
            errList.append(errString)

    # Ensure there aren't too many hints for the current settings.
    if js.document.getElementById("wrinkly_hints").value == "fixed_racing":
        # Take note of all the plando'd hints.
        plandoHintCount = 0
        for hint in HintLocationList:
            hintElem = js.document.getElementById(f"plando_{hint}_hint")
            if hintElem.value != "":
                plandoHintCount += 1
        # If there are more than five hints, and we are using fixed hints, this is
        # an error.
        if plandoHintCount > 5:
            errString = "Fixed hints are incompatible with more than 5 plandomized hints."
            errList.append(errString)

    print(errList)
    return errList
