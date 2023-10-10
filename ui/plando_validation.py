"""Code to collect and validate the selected plando options."""
import re

import js
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Minigames import Minigames
from randomizer.Enums.Plandomizer import PlandoItems
from randomizer.Enums.Regions import Regions
from randomizer.Lists.Location import LocationListData
from randomizer.Lists.Plandomizer import HintLocationList, ItemLocationList, PlannableItemLimits, ShopLocationList
from randomizer.LogicFiles.Shops import LogicRegions
from randomizer.PlandoUtils import GetNameFromPlandoItem, PlandoEnumMap
from ui.bindings import bind, bindList


def invalidate_option(element, tooltip):
    """Add a Bootstrap tooltip to the given element, and mark it as invalid."""
    element.setAttribute("data-bs-original-title", tooltip)
    element.classList.add("invalid")


def validate_option(element):
    """Remove a Bootstrap tooltip from the given element, and mark it as valid."""
    element.setAttribute("data-bs-original-title", "")
    element.classList.remove("invalid")


def count_items():
    """Count all currently placed items to ensure limits aren't exceeded.

    The result will be a dictionary, where each item is linked to all of the
    HTML selects that have this item selected.
    """
    count_dict = {}

    def add_all_items(locList, suffix):
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


############
# BINDINGS #
############


@bindList("change", ItemLocationList, prefix="plando_", suffix="_item")
@bindList("change", ShopLocationList, prefix="plando_", suffix="_item")
def validate_item_limits(evt):
    """Raise an error if any item has been placed too many times."""
    count_dict = count_items()
    for item, locations in count_dict.items():
        if item not in PlannableItemLimits:
            for loc in locations:
                validate_option(js.document.getElementById(loc))
            continue
        itemCount = len(locations)
        if item == PlandoItems.GoldenBanana:
            # Add 40 items to account for blueprint rewards.
            itemCount += 40
        itemMax = PlannableItemLimits[item]
        if itemCount > itemMax:
            maybePluralTimes = "time" if itemMax == 1 else "times"
            errString = f'Item "{GetNameFromPlandoItem(item)}" can be placed at most {itemMax} {maybePluralTimes}, but has been placed {itemCount} times.'
            if item == PlandoItems.GoldenBanana:
                errString += " (40 Golden Bananas are always allocated to blueprint rewards.)"
            for loc in locations:
                invalidate_option(js.document.getElementById(loc), errString)
        else:
            for loc in locations:
                validate_option(js.document.getElementById(loc))


@bindList("change", HintLocationList, prefix="plando_", suffix="_hint")
@bindList("keyup", HintLocationList, prefix="plando_", suffix="_hint")
def validate_hint_text(evt):
    """Raise an error if any hint contains invalid characters."""
    hintString = evt.target.value
    if re.search("[^A-Za-z0-9 \,\.\-\?!]", hintString) is not None:
        invalidate_option(evt.target, "Only letters, numbers, spaces, and the characters ,.-?! are allowed in hints.")
    else:
        validate_option(evt.target)


@bindList("change", ShopLocationList, prefix="plando_", suffix="_shop_cost")
@bindList("keyup", ShopLocationList, prefix="plando_", suffix="_shop_cost")
def validate_shop_costs(evt):
    """Raise an error if any shops have an invalid cost."""
    shopCost = evt.target.value
    if shopCost == "":
        validate_option(evt.target)
    elif shopCost.isdigit() and int(shopCost) >= 0 and int(shopCost) <= 255:
        validate_option(evt.target)
    else:
        invalidate_option(evt.target, "Shop costs must be a whole number between 0 and 255.")


@bind("change", "starting_kongs_count")
@bind("change", "plando_starting_kongs_selected")
def validate_starting_kong_count(evt):
    """Raise an error if the starting Kongs don't match the selected count."""
    startingKongs = js.document.getElementById("plando_starting_kongs_selected")
    selectedKongs = {x.value for x in startingKongs.selectedOptions}
    numStartingKongs = int(js.document.getElementById("starting_kongs_count").value)
    if len(selectedKongs) > numStartingKongs or (len(selectedKongs) < numStartingKongs and "" not in selectedKongs):
        maybePluralKongText = "Kong was selected as a starting Kong" if len(selectedKongs) == 1 else "Kongs were selected as starting Kongs"
        errSuffix = "." if len(selectedKongs) > numStartingKongs else ', and "Random Kong(s)" was not chosen.'
        errString = f"The number of starting Kongs was set to {numStartingKongs}, but {len(selectedKongs)} {maybePluralKongText}{errSuffix}"
        invalidate_option(startingKongs, errString)
    else:
        validate_option(startingKongs)


@bind("change", "plando_level_order_", 7)
def validate_level_order_no_duplicates_level(evt):
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
                validate_option(selectElem)
        else:
            for select in selects:
                selectElem = js.document.getElementById(select)
                invalidate_option(selectElem, "The same level cannot be used twice in the level order.")


@bind("change", "plando_krool_order_", 5)
def validate_level_order_no_duplicates_krool(evt):
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
                validate_option(selectElem)
        else:
            for select in selects:
                selectElem = js.document.getElementById(select)
                invalidate_option(selectElem, "The same Kong cannot be used twice in the K. Rool order.")


@bind("change", "plando_helm_order_", 5)
def validate_level_order_no_duplicates_helm(evt):
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
                validate_option(selectElem)
        else:
            for select in selects:
                selectElem = js.document.getElementById(select)
                invalidate_option(selectElem, "The same Kong cannot be used twice in the Helm order.")


@bind("click", "nav-plando-tab")
def validate_on_nav(evt):
    """Fallback for errors with Bootstrap sliders."""
    validate_starting_kong_count(evt)


######################
# SETTINGS FUNCTIONS #
######################


def populate_plando_options(form):
    """Collect all of the plandomizer options into one object.

    Args:
        form (dict) - The serialized form data containing all HTML inputs.
    Returns:
        plando_form_data (dict) - The collected plando data. May be None if
            plandomizer is disabled, or the selections are invalid.
        err (str[]) - A list of error strings to be displayed to the user.
            Will be an empty list if there are no errors.
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

    def is_number(s):
        """Check if a string is a number or not."""
        try:
            int(s)
            return True
        except ValueError:
            return False

    def get_enum_or_string_value(valueString, settingName):
        """Obtain the enum or string value for the provided setting.

        Args:
            valueString (str) - The value from the HTML input.
            settingName (str) - The name of the HTML input.
        """
        # Convert empty string values to PlandoItems.Randomize.
        # This is always valid for the plandomizer specifically.
        if valueString == "":
            return PlandoItems.Randomize
        elif settingName in PlandoEnumMap:
            return PlandoEnumMap[settingName][valueString]
        else:
            return valueString

    def is_plando_input(inputName):
        """Determine if an input is a plando input."""
        return inputName is not None and inputName.startswith("plando_")

    # Process all the plando-related inputs.
    for obj in form:
        if not is_plando_input(obj.name):
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
        location = Locations[location_name]
        if item.value != "":
            locations_map[location] = PlandoItems[item.value]
    # Place Golden Bananas on all of the blueprint rewards.
    for blueprint in LogicRegions[Regions.Snide].locations:
        locations_map[blueprint.id] = PlandoItems.GoldenBanana
    plando_form_data["locations"] = locations_map

    shops_map = {}
    for shop_cost in shop_cost_objects:
        # Extract the location name.
        location_name = re.search("^plando_(.+)_shop_cost$", shop_cost.name)[1]
        location = Locations[location_name]
        if shop_cost.value != "":
            item_cost = int(shop_cost.value)
            shops_map[location] = item_cost
    plando_form_data["prices"] = shops_map

    minigames_map = {}
    for minigame in minigame_objects:
        # Extract the barrel location name.
        location_name = re.search("^plando_(.+)_minigame$", minigame.name)[1]
        location = Locations[location_name]
        if minigame.value != "":
            minigames_map[location] = Minigames[minigame.value]
    plando_form_data["minigames"] = minigames_map

    hints_map = {}
    for hint in hint_objects:
        # Extract the hint location.
        location_name = re.search("^plando_(.+)_hint$", hint.name)[1]
        location = Locations[location_name]
        if hint.value != "":
            hints_map[location] = hint.value
    plando_form_data["hints"] = hints_map

    return plando_form_data


def validate_plando_options(settings_dict):
    """Validate the plando options against a set of rules.

    Args:
        settings_dict (str) - The dictionary containing the full settings.
    """
    if "plandomizer" not in settings_dict:
        return []

    plando_dict = settings_dict["plandomizer"]
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
    # If any items have exceeded their maximum amounts, add an error.
    for item, itemCount in count_dict.items():
        if item not in PlannableItemLimits:
            continue
        itemMax = PlannableItemLimits[item]
        if itemCount > itemMax:
            maybePluralTimes = "time" if itemMax == 1 else "times"
            errString = f'Item "{GetNameFromPlandoItem(item)}" can be placed at most {itemMax} {maybePluralTimes}, but has been placed {itemCount} times.'
            if item in plando_dict["plando_starting_moves_selected"]:
                errString += " (This includes starting moves.)"
            if item == PlandoItems.GoldenBanana:
                errString += " (40 Golden Bananas are always allocated to blueprint rewards.)"
            errList.append(errString)

    # Ensure that shop costs are within allowed limits.
    for shopLocation, price in plando_dict["prices"].items():
        if price == PlandoItems.Randomize:
            continue
        if price < 0 or price > 255:
            shopName = LocationListData().LocationList[shopLocation].name
            errString = f'Shop costs must be between 0 and 255 coins, but shop "{shopName}" has a cost of {price} coins.'
            errList.append(errString)

    # Ensure that the number of chosen Kongs matches the "number of starting
    # Kongs" setting, or that "Random Kong(s)" has been chosen. If too many
    # Kongs have been selected, that is always an error.
    chosenKongs = plando_dict["plando_starting_kongs_selected"]
    numStartingKongs = int(settings_dict["starting_kongs_count"])
    if len(chosenKongs) > numStartingKongs or (len(chosenKongs) < numStartingKongs and PlandoItems.Randomize not in chosenKongs):
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
        hintLocationName = LocationListData().LocationList[hintLocation].name
        if len(hint) > 900:
            errString = f'The hint for location "{hintLocationName}" is longer than the limit of 900 characters.'
            errList.append(errString)
        if re.search("[^A-Za-z0-9 \,\.\-\?!]", hint) is not None:
            errString = f'The hint for location "{hintLocationName}" contains invalid characters. Only letters, numbers, spaces, and the characters ,.-?! are valid.'
            if "'" in hint:
                errString += " (Apostrophes are not allowed.)"
            errList.append(errString)

    return errList
