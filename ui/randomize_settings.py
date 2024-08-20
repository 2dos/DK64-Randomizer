"""Function to randomize settings and store them in a dictionary."""

import math
import random

import js
from randomizer.Enums.Settings import ShufflePortLocations, LogicType, SettingsStringDataType, SettingsStringEnum, SettingsStringListTypeMap, SettingsStringTypeMap


def random_bool_setting(weight: float) -> bool:
    """Generate a random value for a boolean setting."""
    return random.uniform(0, 1) <= weight


def random_list_setting(weights: dict, settingEnum: SettingsStringEnum) -> list[str]:
    """Generate a random list of values for a list-based setting."""
    settingListType = SettingsStringListTypeMap[settingEnum]
    settingList = []
    for settingOption, optionWeight in weights.items():
        typedOption = settingListType[settingOption]
        randValue = random.uniform(0, 1)
        if randValue <= optionWeight:
            settingList.append(typedOption.name)
    return settingList


def get_random_normal_value(mean: float, sdev: float) -> float:
    """Return a random number using the Box-Muller transform algorithm."""
    u1 = random.uniform(0, 1)
    u2 = random.uniform(0, 1)
    while u1 == 0:
        u1 = random.uniform(0, 1)
    while u2 == 0:
        u2 = random.uniform(0, 1)
    r = math.sqrt(-2.0 * math.log(u1))
    theta = 2.0 * math.pi * u2
    u0 = r * math.cos(theta)
    return mean + (sdev * u0)


def random_numeric_setting(weights: dict) -> int:
    """Generate a random value for a numeric setting.

    If there is a provided mean, the resulting number will be biased toward the
    mean, but can range all the way from the min to the max. If there is no
    mean, the number will be pulled from a uniform distribution.
    """
    min = weights["min"]
    max = weights["max"]

    # If the min equals the max, return that number.
    if min == max:
        return min

    # If there is no mean, obtain a random number between the min and max,
    # equally distributed.
    if "mean" not in weights:
        return round(random.uniform(min, max))

    mean = weights["mean"]

    # Determine the standard deviation. This will be 1/3 of the difference
    # between the mean and the min, or the mean and the max, whichever is
    # larger.
    minDiff = mean - min
    maxDiff = max - mean
    minBased = minDiff >= maxDiff
    sdev = minDiff / 3 if minBased else maxDiff / 3
    # We need to determine the scale difference between the minDiff and the
    # maxdiff, since we will use that to adjust numbers outside the range.
    oppositeScale = maxDiff / minDiff if minBased else minDiff / maxDiff

    # Obtain a normally-distributed random number.
    randNum = get_random_normal_value(mean, sdev)

    # If we're min-based and our number is larger than the mean, or if we're
    # max-based and our number is smaller than the mean, we need to adjust the
    # number so it fits into the different scale of the opposite side.
    if (minBased and randNum > mean) or (not minBased and randNum < mean):
        randNum = ((randNum - mean) * oppositeScale) + mean

    # Trim the number so it falls within our bounds.
    if randNum < min:
        randNum = min
    elif randNum > max:
        randNum = max

    # Round to the nearest integer.
    return round(randNum)


def random_enum_setting(weights: dict, settingEnum: SettingsStringEnum):
    """Generate a randomly selected value for an enum setting."""
    enumType = SettingsStringTypeMap[settingEnum]
    # Generate our buckets.
    buckets = []
    bucketCeiling = 0
    for enumOptionName, enumWeight in weights.items():
        enumOption = enumType[enumOptionName]
        bucketCeiling += enumWeight
        buckets.append({"option": enumOption, "ceiling": bucketCeiling})
    # The random value is multiplied by the sum of all the weights, to ensure
    # an even distribution even if all the weights don't add up to 1.
    randValue = random.uniform(0, 1) * bucketCeiling
    for bucket in buckets:
        if randValue < bucket["ceiling"]:
            return bucket["option"]
    # This should never happen.
    return None


def assign_list_setting(settingName: str, valueList: list[str]):
    """Assign a list of values to a list-based setting."""
    listElem = js.document.getElementsByName(settingName).item(0)
    for i in range(listElem.options.length):
        optElem = listElem.options.item(i)
        optElem.selected = optElem.value in valueList


def randomize_settings():
    """Assign random values to all of the non-cosmetic settings."""
    # Generate random settings based on the selected weights.
    weightsElem = js.document.getElementById("random-weights")
    weightData = None
    for val in js.random_settings_presets:
        if val.get("name") == weightsElem.value:
            weightData = val
    # If we somehow have no selection, just return.
    if weightData is None:
        return

    numTypes = set([SettingsStringDataType.int16, SettingsStringDataType.u16, SettingsStringDataType.int4, SettingsStringDataType.int8, SettingsStringDataType.var_int])
    randSettings = dict()

    # Start by generating random values and placing them in the dictionary.
    for settingName, weights in weightData.items():
        if settingName == "name" or settingName == "description":
            continue
        settingEnum = SettingsStringEnum[settingName]
        settingType = SettingsStringTypeMap[settingEnum]

        # For a bool setting, generate a random number and see if it's below
        # the provided weight.
        if settingType is SettingsStringDataType.bool:
            randomValue = random_bool_setting(weights)
            randSettings[settingName] = randomValue
        # For a list setting, generate a random number for every possible value
        # and add that value if it's above the provided weight.
        elif settingType is SettingsStringDataType.list:
            randomList = random_list_setting(weights, settingEnum)
            randSettings[settingName] = randomList
        # For a numeric setting, generate a random number from a distribution
        # based on the provided values.
        elif settingType in numTypes:
            randomValue = random_numeric_setting(weights)
            randSettings[settingName] = randomValue
        # For an enum setting, generate a random number and see which bucket
        # the number falls into. That bucket's value is chosen.
        else:
            randomValue = random_enum_setting(weights, settingEnum)
            randSettings[settingName] = randomValue

    # If logic isn't glitched logic, remove selected glitches.
    if randSettings["logic_type"] != LogicType.glitch:
        randSettings["glitches_selected"] = []
    # Only enable individual hard mode settings if hard mode is enabled.
    if not randSettings["hard_mode"]:
        randSettings["hard_mode_selected"] = []
    # Remove all selected minigames if they aren't being randomized.
    if not randSettings["bonus_barrel_rando"]:
        randSettings["minigames_list_selected"] = []
    # Remove all selected enemies if they aren't being randomized.
    if not randSettings["enemy_rando"]:
        randSettings["enemies_selected"] = []
    # Ignore the warp level list if bananaports are not shuffled.
    if randSettings["bananaport_placement_rando"] == ShufflePortLocations.off:
        randSettings["warp_level_list_selected"] = []

    # Now we assign the random values to the HTML settings.
    for settingName, settingValue in randSettings.items():
        # These two settings are ignored, at this time.
        if settingName in ["random_starting_move_list_selected", "starting_move_list_selected"]:
            continue

        settingEnum = SettingsStringEnum[settingName]
        settingType = SettingsStringTypeMap[settingEnum]

        if settingType is SettingsStringDataType.bool:
            elem = js.document.getElementsByName(settingName).item(0)
            elem.checked = settingValue
        elif settingType is SettingsStringDataType.list:
            assign_list_setting(settingName, settingValue)
        elif settingType in numTypes:
            elem = js.document.getElementsByName(settingName).item(0)
            elem.value = settingValue
        else:
            elem = js.document.getElementsByName(settingName).item(0)
            elem.value = settingValue.name
