"""Code to collect and validate the selected plando options."""

from enum import IntEnum, auto
import json
import re

import js
from randomizer.Enums.Items import Items
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Minigames import Minigames
from randomizer.Enums.Plandomizer import ItemToPlandoItemMap, PlandoGroupMap, PlandoItems
from randomizer.Enums.Settings import KasplatRandoSetting
from randomizer.Lists.Item import StartingMoveOptions
from randomizer.Lists.Location import LocationListOriginal as LocationList
from randomizer.Lists.Plandomizer import (
    CrownLocationList,
    DirtPatchLocationList,
    FairyLocationList,
    HintLocationList,
    ItemLocationList,
    KasplatLocationList,
    MelonCrateLocationList,
    MinigameLocationList,
    PlannableGroupLimits,
    PlannableItemLimits,
    ShopLocationKongMap,
    ShopLocationList,
)
from randomizer.LogicFiles.Shops import LogicRegions
from randomizer.PlandoUtils import GetNameFromPlandoItem, PlandoEnumMap
from ui.bindings import bind, bindList


class ValidationError(IntEnum):
    """Specific validation failures associated with an element."""

    exceeds_item_limits = auto()
    exceeds_group_limits = auto()
    shop_has_shared_and_solo_rewards = auto()
    smaller_shops_conflict = auto()
    invalid_hint_text = auto()
    too_many_hints_with_fixed_hints = auto()
    invalid_shop_cost = auto()
    invalid_starting_kong_count = auto()
    level_order_duplicates = auto()
    krool_order_duplicates = auto()
    helm_order_duplicates = auto()
    assigned_shop_when_shuffled = auto()
    assigned_dirt_patch_when_shuffled = auto()
    assigned_fairy_when_shuffled = auto()
    assigned_crown_when_shuffled = auto()
    assigned_crate_when_shuffled = auto()
    assigned_kasplat_when_shuffled = auto()
    key_8_locked_in_helm = auto()


# This dictionary stores all elements that have either been disabled or marked
# invalid. It stores the current errors that apply to each element. This will
# prevent us from marking an element as enabled or valid if there is still an
# error with it.
element_error_dict = dict()


def get_errors(elementId: str) -> dict:
    """Get, or create, the dict of current errors for this element."""
    if elementId not in element_error_dict:
        element_error_dict[elementId] = {
            # Each of these two dictionaries maps ValidationError enums to
            # error strings.
            "invalid": dict(),
            "disabled": dict(),
        }
    return element_error_dict[elementId]


def write_current_tooltip(elementId) -> None:
    """Add a Bootstrap tooltip to the given element for its current errors."""
    tooltips = []
    elemErrors = get_errors(elementId)
    for _, invalidError in elemErrors["invalid"].items():
        if invalidError != "":
            tooltips.append(invalidError)
    for _, disabledError in elemErrors["disabled"].items():
        if disabledError != "":
            tooltips.append(disabledError)
    wrapper = js.document.getElementById(f"{elementId}_wrapper")
    wrapper.setAttribute("data-bs-original-title", "\n".join(tooltips))


def mark_option_invalid(element, errType: ValidationError, errMessage: str) -> None:
    """Mark the given option as invalid, and add an associated error."""
    if errMessage == "":
        raise ValueError("The error string passed to mark_option_invalid must be non-empty.")
    elemErrors = get_errors(element.id)
    elemErrors["invalid"][errType] = errMessage
    element.classList.add("invalid")
    write_current_tooltip(element.id)


def mark_option_valid(element, errType: ValidationError) -> None:
    """Remove an error from a given option, and maybe mark it as valid."""
    elemErrors = get_errors(element.id)
    elemErrors["invalid"][errType] = ""
    # If there are no more invalid-style errors, mark this as valid.
    valid = True
    for _, errString in elemErrors["invalid"].items():
        if errString != "":
            valid = False
    if valid:
        element.classList.remove("invalid")
    write_current_tooltip(element.id)


def mark_option_disabled(element, errType: ValidationError, errMessage: str, optionValue: str = "") -> None:
    """Disable the given option, and add an associated error."""
    if errMessage == "":
        raise ValueError("The error string passed to mark_option_disabled must be non-empty.")
    elemErrors = get_errors(element.id)
    elemErrors["disabled"][errType] = errMessage
    element.value = optionValue
    element.setAttribute("disabled", "disabled")
    write_current_tooltip(element.id)


def mark_option_enabled(element, errType: ValidationError) -> None:
    """Remove an error from a given option, and maybe enable it."""
    elemErrors = get_errors(element.id)
    elemErrors["disabled"][errType] = ""
    # If there are no more disabled-style errors, enable this.
    enabled = True
    for _, errString in elemErrors["disabled"].items():
        if errString != "":
            enabled = False
    if enabled:
        element.removeAttribute("disabled")
    write_current_tooltip(element.id)


def remove_all_errors_from_option(element) -> None:
    """Remove all errors from a given option, and mark it as valid/enabled."""
    elemErrors = get_errors(element.id)
    elemErrors["invalid"] = dict()
    elemErrors["disabled"] = dict()
    element.removeAttribute("disabled")
    element.classList.remove("invalid")
    write_current_tooltip(element.id)


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


########################
# VALIDATION FUNCTIONS #
########################


def hint_text_validation_fn(hintString: str) -> str:
    """Return an error if the element's hint contains invalid characters."""
    colors = ["orange", "red", "blue", "purple", "lightgreen", "magenta", "cyan", "rust", "paleblue", "green"]
    # Test the hint string without color tags.
    trimmedHintString = hintString
    for color in colors:
        trimmedHintString = trimmedHintString.replace(f"[{color}]", "")
        trimmedHintString = trimmedHintString.replace(f"[/{color}]", "")
    if re.search("[^A-Za-z0-9 '\,\.\-\?!]", trimmedHintString) is not None:
        errString = "Only letters, numbers, spaces, the characters ',.-?! and color tags are allowed in hints."
        return errString
    if len(trimmedHintString) > 123:
        errString = "Hints can be a maximum of 123 characters (excluding color tags)."
        return errString

    # Ensure that the color tags are correctly utilized.
    tagRegex = r"\[\/?(?:orange|red|blue|purple|lightgreen|magenta|cyan|rust|paleblue|green)\]"
    tags = re.finditer(tagRegex, hintString)
    currentTag = None
    for tag in tags:
        if currentTag is None:
            # Is there a closing tag before an opening one?
            if "/" in tag[0]:
                errString = f"Closing color tag {tag[0]} has no opening tag."
                return errString
            currentTag = tag
        else:
            # Is the next tag a closing tag?
            if "/" not in tag[0]:
                errString = f"Color tag {tag[0]} overlaps color tag {currentTag[0]}."
                return errString
            # Do the two tags match in color?
            currentTagColor = re.search("^\[\/?(.+)\]$", currentTag[0])[1]
            newTagColor = re.search("^\[\/?(.+)\]$", tag[0])[1]
            if currentTagColor != newTagColor:
                errString = f"Color tag {currentTag[0]} has non-matching closing tag {tag[0]}."
                return errString
            # Is there any text at all between the tags?
            if currentTag.end(0) == tag.start(0):
                errString = f"There is no text within color tag {currentTag[0]}."
                return errString
            # Erase the current tag, as it's been matched.
            currentTag = None

    # If we still have a tag, they are unmatched.
    if currentTag:
        errString = f"Color tag {currentTag[0]} is unmatched."
        return errString

    # If we've made it to this point, the element is valid.
    return None


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
                    mark_option_valid(js.document.getElementById(loc), ValidationError.exceeds_item_limits)
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
                    mark_option_invalid(js.document.getElementById(loc), ValidationError.exceeds_item_limits, errString)
        else:
            for loc in locations:
                if loc is not None:
                    mark_option_valid(js.document.getElementById(loc), ValidationError.exceeds_item_limits)


@bindList("click", startingMoveValues, prefix="none-")
@bindList("click", startingMoveValues, prefix="start-")
@bindList("click", startingMoveValues, prefix="random-")
@bindList("change", ItemLocationList, prefix="plando_", suffix="_item")
@bindList("change", ShopLocationList, prefix="plando_", suffix="_item")
@bind("click", "starting_moves_reset")
@bind("click", "starting_moves_start_all")
@bind("change", "plando_starting_kongs_selected")
@bind("change", "select_keys")
@bind("click", "starting_keys_list_selected")
def validate_group_limits(evt):
    """Raise an error if a group of items had too many of its members placed."""
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
    # Add in starting Kongs, which also count toward the totals.
    startingKongs = js.document.getElementById("plando_starting_kongs_selected")
    for kong in startingKongs.selectedOptions:
        if kong.value == "":
            continue
        selectedKong = PlandoItems[kong.value.capitalize()]
        if selectedKong in count_dict:
            # Add in None, so we don't attempt to mark a nonexistent element.
            count_dict[selectedKong].append(None)
        else:
            count_dict[selectedKong] = [None]
    # Check to see if any groups exceeded their limits.
    groupTypeNameMap = {
        PlandoItems.RandomKong: "Kongs",
        PlandoItems.RandomMove: "moves",
        PlandoItems.RandomKongMove: "Kong moves",
        PlandoItems.RandomSharedMove: "shared moves",
        PlandoItems.RandomKey: "keys",
        PlandoItems.RandomItem: "collectibles",
    }
    for plandoGroup, groupItems in PlandoGroupMap.items():
        # For each group, add up the number of times the "random" item was
        # placed, and all of the items in that group. If it exceeds the limit,
        # that's an error.
        groupLocations = count_dict[plandoGroup] if plandoGroup in count_dict else []
        for groupItem in groupItems:
            if groupItem in count_dict:
                groupLocations.extend(count_dict[groupItem])
        # If we're dealing with keys, add in the number of starting keys.
        if plandoGroup == PlandoItems.RandomKey:
            startingKeyCount = 0
            if js.document.getElementById("select_keys").checked:
                for _ in js.document.getElementById("starting_keys_list_selected").selectedOptions:
                    startingKeyCount += 1
            else:
                startingKeyCount = 8 - int(js.document.getElementById("krool_key_count").value)
            for _ in range(0, startingKeyCount):
                groupLocations.append(None)
        limitExceeded = len(groupLocations) > PlannableGroupLimits[plandoGroup]
        for loc in groupLocations:
            if loc is not None:
                # Throw an error if we've exceeded the limit and we've placed
                # the "random" item anywhere.
                if limitExceeded and plandoGroup in count_dict:
                    itemTypeName = groupTypeNameMap[plandoGroup]
                    maybeStartingItems = f" (This includes starting {itemTypeName}.)" if None in groupLocations else ""
                    errString = f"A total of {len(groupLocations)} {itemTypeName} have been placed, but the maximum allowed is {PlannableGroupLimits[plandoGroup]} {itemTypeName}.{maybeStartingItems}"
                    mark_option_invalid(js.document.getElementById(loc), ValidationError.exceeds_group_limits, errString)
                else:
                    mark_option_valid(js.document.getElementById(loc), ValidationError.exceeds_group_limits)


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
                    mark_option_invalid(vendor_element, ValidationError.shop_has_shared_and_solo_rewards, errString)
                else:
                    mark_option_valid(vendor_element, ValidationError.shop_has_shared_and_solo_rewards)
            if shared_location_valid:
                mark_option_valid(vendor_shared_element, ValidationError.shop_has_shared_and_solo_rewards)
            else:
                mark_option_invalid(vendor_shared_element, ValidationError.shop_has_shared_and_solo_rewards, errString)


@bindList("change", ShopLocationList, prefix="plando_", suffix="_item")
@bind("change", "smaller_shops")
def validate_smaller_shops_no_conflict(evt):
    """Disable shops if we have a conflict with Smaller Shops.

    If the user is using the Smaller Shops setting, they cannot place anything
    in the shops. This causes fill issues.
    """
    useSmallerShops = js.document.getElementById("smaller_shops").checked
    for locationName in ShopLocationList:
        # This check does not apply to Jetpac.
        if locationName == Locations.RarewareCoin.name:
            continue
        shopElem = js.document.getElementById(f"plando_{locationName}_item")
        if useSmallerShops:
            errString = 'Shop locations cannot be assigned if "Smaller Shops" is selected.'
            mark_option_disabled(shopElem, ValidationError.smaller_shops_conflict, errString)
        else:
            mark_option_enabled(shopElem, ValidationError.smaller_shops_conflict)


@bindList("change", ShopLocationList, prefix="plando_", suffix="_item")
@bind("change", "shuffle_shops")
def validate_shuffle_shops_no_conflict(evt):
    """Disable shops if the user has shuffled shops."""
    shuffleShops = js.document.getElementById("shuffle_shops").checked
    for locationName in ShopLocationList:
        # This check does not apply to Jetpac.
        if locationName == Locations.RarewareCoin.name:
            continue
        shopElem = js.document.getElementById(f"plando_{locationName}_item")
        if shuffleShops:
            errString = "Items cannot be assigned to shops when shop locations are shuffled."
            mark_option_disabled(shopElem, ValidationError.assigned_shop_when_shuffled, errString)
        else:
            mark_option_enabled(shopElem, ValidationError.assigned_shop_when_shuffled)


@bindList("change", HintLocationList, prefix="plando_", suffix="_hint")
@bindList("keyup", HintLocationList, prefix="plando_", suffix="_hint")
def validate_hint_text_binding(evt):
    """Raise an error if this target's hint contains invalid characters."""
    validate_hint_text(evt.target)


def validate_hint_text(element) -> None:
    """Raise an error if the element's hint contains invalid characters."""
    errString = hint_text_validation_fn(element.value)
    if errString is not None:
        mark_option_invalid(element, ValidationError.invalid_hint_text, errString)
    else:
        mark_option_valid(element, ValidationError.invalid_hint_text)


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
        mark_option_valid(hintElem, ValidationError.too_many_hints_with_fixed_hints)
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
            errString = "Fixed hints are incompatible with more than 5 plandomized hints."
            mark_option_invalid(hintElem, ValidationError.too_many_hints_with_fixed_hints, errString)


@bindList("change", ShopLocationList, prefix="plando_", suffix="_shop_cost")
@bindList("keyup", ShopLocationList, prefix="plando_", suffix="_shop_cost")
def validate_shop_costs_binding(evt):
    """Raise an error if this target's shop has an invalid cost."""
    validate_shop_costs(evt.target)


def validate_shop_costs(element) -> None:
    """Raise an error if this element's shop has an invalid cost."""
    shopCost = element.value
    if shopCost == "":
        mark_option_valid(element, ValidationError.invalid_shop_cost)
    elif shopCost.isdigit() and int(shopCost) >= 0 and int(shopCost) <= 255:
        mark_option_valid(element, ValidationError.invalid_shop_cost)
    else:
        errString = "Shop costs must be a whole number between 0 and 255."
        mark_option_invalid(element, ValidationError.invalid_shop_cost, errString)


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
        mark_option_valid(startingKongs, ValidationError.invalid_starting_kong_count)
    elif len(selectedKongs) > numStartingKongs or (len(selectedKongs) < numStartingKongs and "" not in selectedKongs):
        maybePluralKongText = "Kong was selected as a starting Kong" if len(selectedKongs) == 1 else "Kongs were selected as starting Kongs"
        errSuffix = "." if len(selectedKongs) > numStartingKongs else ', and "Random Kong(s)" was not chosen.'
        errString = f"The number of starting Kongs was set to {numStartingKongs}, but {len(selectedKongs)} {maybePluralKongText}{errSuffix}"
        mark_option_invalid(startingKongs, ValidationError.invalid_starting_kong_count, errString)
    else:
        mark_option_valid(startingKongs, ValidationError.invalid_starting_kong_count)


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
                mark_option_valid(selectElem, ValidationError.level_order_duplicates)
        else:
            for select in selects:
                selectElem = js.document.getElementById(select)
                errString = "The same level cannot be used twice in the level order."
                mark_option_invalid(selectElem, ValidationError.level_order_duplicates, errString)


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
                mark_option_valid(selectElem, ValidationError.krool_order_duplicates)
        else:
            for select in selects:
                selectElem = js.document.getElementById(select)
                errString = "The same Kong cannot be used twice in the K. Rool order."
                mark_option_invalid(selectElem, ValidationError.krool_order_duplicates, errString)


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
                mark_option_valid(selectElem, ValidationError.helm_order_duplicates)
        else:
            for select in selects:
                selectElem = js.document.getElementById(select)
                errString = "The same Kong cannot be used twice in the Helm order."
                mark_option_invalid(selectElem, ValidationError.helm_order_duplicates, errString)


@bind("change", "random_crates")
def validate_no_crate_items_with_shuffled_crates(evt):
    """Prevent crate items from being assigned with shuffled crates."""
    randomCrates = js.document.getElementById("random_crates")
    for location in MelonCrateLocationList:
        locElem = js.document.getElementById(f"plando_{location}_item")
        if randomCrates.checked:
            errString = "Items cannot be assigned to melon crates when melon crate locations are shuffled."
            mark_option_disabled(locElem, ValidationError.assigned_crate_when_shuffled, errString)
        else:
            mark_option_enabled(locElem, ValidationError.assigned_crate_when_shuffled)


@bind("change", "crown_placement_rando")
def validate_no_crown_items_with_shuffled_crowns(evt):
    """Prevent crown items from being assigned with shuffled crowns."""
    randomCrowns = js.document.getElementById("crown_placement_rando")
    for location in CrownLocationList:
        locElem = js.document.getElementById(f"plando_{location}_item")
        if randomCrowns.checked:
            errString = "Items cannot be assigned to battle arenas when battle arena locations are shuffled."
            mark_option_disabled(locElem, ValidationError.assigned_crown_when_shuffled, errString)
        else:
            mark_option_enabled(locElem, ValidationError.assigned_crown_when_shuffled)


@bind("change", "random_patches")
def validate_no_dirt_items_with_shuffled_patches(evt):
    """Prevent dirt patch items from being assigned with shuffled patches."""
    randomPatches = js.document.getElementById("random_patches")
    for location in DirtPatchLocationList:
        locElem = js.document.getElementById(f"plando_{location}_item")
        if randomPatches.checked:
            errString = "Items cannot be assigned to dirt patches when dirt patch locations are shuffled."
            mark_option_disabled(locElem, ValidationError.assigned_dirt_patch_when_shuffled, errString)
        else:
            mark_option_enabled(locElem, ValidationError.assigned_dirt_patch_when_shuffled)


@bind("change", "random_fairies")
def validate_no_fairy_items_with_shuffled_fairies(evt):
    """Prevent fairy items from being assigned with shuffled fairies."""
    randomFairies = js.document.getElementById("random_fairies")
    for location in FairyLocationList:
        locElem = js.document.getElementById(f"plando_{location}_item")
        if randomFairies.checked:
            errString = "Items cannot be assigned to fairies when fairies are shuffled."
            mark_option_disabled(locElem, ValidationError.assigned_fairy_when_shuffled, errString)
        else:
            mark_option_enabled(locElem, ValidationError.assigned_fairy_when_shuffled)


@bind("change", "kasplat_rando_setting")
def validate_no_kasplat_items_with_location_shuffle(evt):
    """Prevent Kasplat items from being assigned with location shuffle."""
    kasplatRandoElem = js.document.getElementById("kasplat_rando_setting")
    shuffled = kasplatRandoElem.value == KasplatRandoSetting.location_shuffle.name
    for location in KasplatLocationList:
        locElem = js.document.getElementById(f"plando_{location}_item")
        if shuffled:
            errString = "Items cannot be assigned to Kasplats when Kasplat locations are shuffled."
            mark_option_disabled(locElem, ValidationError.assigned_kasplat_when_shuffled, errString)
        else:
            mark_option_enabled(locElem, ValidationError.assigned_kasplat_when_shuffled)


@bind("click", "key_8_helm")
def lock_key_8_in_helm(evt):
    """If key 8 is locked in Helm, force that location to hold key 8."""
    key_8_locked_in_helm = js.document.getElementById("key_8_helm").checked
    end_of_helm = js.document.getElementById("plando_HelmKey_item")
    if key_8_locked_in_helm:
        # Forcibly select Key 8 for the End of Helm dropdown and disable it.
        errString = 'The "Lock Key 8 in Helm" setting has been chosen.'
        mark_option_disabled(end_of_helm, ValidationError.key_8_locked_in_helm, errString, Items.HideoutHelmKey.name)
    else:
        # Enable the End of Helm dropdown. If Key 8 is currently placed there,
        # remove it as the dropdown option.
        if end_of_helm.value == Items.HideoutHelmKey.name:
            end_of_helm.value = ""
        mark_option_enabled(end_of_helm, ValidationError.key_8_locked_in_helm)


@bind("click", "nav-plando-tab")
def validate_on_nav(evt):
    """Apply certain changes when navigating to the plandomizer tab."""
    perform_setting_conflict_validation(evt)


def perform_setting_conflict_validation(evt):
    """Perform checks that compare plando settings to other settings."""
    lock_key_8_in_helm(evt)
    validate_smaller_shops_no_conflict(evt)
    validate_shuffle_shops_no_conflict(evt)
    validate_no_crate_items_with_shuffled_crates(evt)
    validate_no_crown_items_with_shuffled_crowns(evt)
    validate_no_dirt_items_with_shuffled_patches(evt)
    validate_no_fairy_items_with_shuffled_fairies(evt)
    validate_no_kasplat_items_with_location_shuffle(evt)
    # This is a fallback for errors with Bootstrap sliders.
    validate_starting_kong_count(evt)


@bind("click", "reset_plando_settings")
def reset_plando_options(evt):
    """Return all plandomizer options to their default settings.

    Issues a prompt first, warning the user.
    """
    if js.window.confirm("Are you sure you want to reset all plandomizer settings?"):
        reset_plando_options_no_prompt()
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


def reset_plando_options_no_prompt() -> None:
    """Return all plandomizer options to their default settings."""
    # Reset general settings.

    # These settings are TBD
    # js.document.getElementById("plando_spawn_location").value = ""
    # js.document.getElementById("plando_101").value = False

    for option in level_options + kong_options:
        option_element = js.document.getElementById(option)
        option_element.value = ""
        remove_all_errors_from_option(option_element)
    kongs_element = js.document.getElementById("plando_starting_kongs_selected")
    kongs_element.options.item(0).selected = True
    for i in range(1, 6):
        kongs_element.options.item(i).selected = False
    remove_all_errors_from_option(kongs_element)

    for location in ItemLocationList + ShopLocationList:
        location_element = js.document.getElementById(f"plando_{location}_item")
        location_element.value = ""
        remove_all_errors_from_option(location_element)
    for shop in ShopLocationList:
        # Skip the Rareware Coin location, which has no price.
        if shop == "RarewareCoin":
            continue
        price_element = js.document.getElementById(f"plando_{shop}_shop_cost")
        price_element.value = ""
        remove_all_errors_from_option(price_element)
    for minigame in MinigameLocationList:
        minigame_element = js.document.getElementById(f"plando_{minigame}_minigame")
        minigame_element.value = ""
        remove_all_errors_from_option(minigame_element)
    for hint in HintLocationList:
        hint_element = js.document.getElementById(f"plando_{hint}_hint")
        hint_element.value = ""
        remove_all_errors_from_option(hint_element)

    # Perform some additional checks that may disable dropdowns.
    perform_setting_conflict_validation(None)


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

    minigames_map = {}
    for minigame in minigame_objects:
        # Extract the barrel location name.
        location_name = re.search("^plando_(.+)_minigame$", minigame.name)[1]
        location = get_plando_value(Locations[location_name])
        if minigame.value != "":
            minigames_map[location] = get_plando_value(Minigames[minigame.value])
    plando_form_data["plando_bonus_barrels"] = minigames_map

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

    # Check groups of items, using the same dictionary.
    # Add in starting Kongs, which also count toward the totals.
    startingKongCount = 0
    for kong in plando_dict["plando_starting_kongs_selected"]:
        if kong < 0:
            continue
        plandoKong = PlandoItems[Kongs(kong).name.capitalize()]
        startingKongCount += 1
        if plandoKong in count_dict:
            count_dict[plandoKong] += 1
        else:
            count_dict[plandoKong] = 1
    groupTypeNameMap = {
        PlandoItems.RandomKong: "Kongs",
        PlandoItems.RandomMove: "moves",
        PlandoItems.RandomKongMove: "Kong moves",
        PlandoItems.RandomSharedMove: "shared moves",
        PlandoItems.RandomKey: "keys",
        PlandoItems.RandomItem: "collectibles",
    }
    for plandoGroup, groupItems in PlandoGroupMap.items():
        # For each group, add up the number of times the "random" item was
        # placed, and all of the items in that group. If it exceeds the limit,
        # that's an error.
        groupCount = count_dict[plandoGroup] if plandoGroup in count_dict else 0
        for groupItem in groupItems:
            if groupItem in count_dict:
                groupCount += count_dict[groupItem]
        # If we're dealing with keys, add in the number of starting keys.
        startingKeyCount = 0
        if plandoGroup == PlandoItems.RandomKey:
            startingKeyCount = 0
            if js.document.getElementById("select_keys").checked:
                for _ in js.document.getElementById("starting_keys_list_selected").selectedOptions:
                    startingKeyCount += 1
            else:
                startingKeyCount = 8 - int(js.document.getElementById("krool_key_count").value)
            groupCount += startingKeyCount
        limitExceeded = groupCount > PlannableGroupLimits[plandoGroup]
        # Throw an error if we've exceeded the limit and we've placed
        # the "random" item anywhere.
        if limitExceeded and plandoGroup in count_dict:
            itemTypeName = groupTypeNameMap[plandoGroup]
            errString = f"A total of {groupCount} {itemTypeName} have been placed, but the maximum allowed is {PlannableGroupLimits[plandoGroup]} {itemTypeName}."
            if (plandoGroup == PlandoItems.RandomKong and startingKongCount > 0) or (plandoGroup == PlandoItems.RandomKey and startingKeyCount > 0):
                errString += f" (This includes starting {itemTypeName}.)"
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
        errString = hint_text_validation_fn(hint)
        if errString is not None:
            hintLocationName = LocationList[int(hintLocation)].name
            fullErrString = f'Error in hint for location "{hintLocationName}": {errString}'
            errList.append(fullErrString)

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
