"""Function to randomize settings and store them in a dictionary."""
import json
import math
import random

import js
from randomizer.Enums.Settings import ItemRandoListSelected, MoveRando, SettingsStringDataType, SettingsStringEnum, SettingsStringListTypeMap, SettingsStringTypeMap


def random_bool_setting(weight: float) -> bool:
    """Generate a random value for a boolean setting."""
    return random.uniform(0, 1) <= weight


def random_list_setting(weights: dict, settingEnum: SettingsStringEnum) -> list:
    """Generate a random list of values for a list-based setting."""
    settingListType = SettingsStringListTypeMap[settingEnum]
    settingList = []
    for settingOption, optionWeight in weights.items():
        typedOption = settingListType[settingOption]
        randValue = random.uniform(0, 1)
        if randValue <= optionWeight:
            settingList.append(typedOption)
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
    
    The resulting number will be biased toward the mean, but can range all the
    way from the min to the max.
    """
    min = weights["min"]
    max = weights["max"]
    mean = weights["mean"]

    # If the min equals the max, return that number.
    if min == max:
        return min
    
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

    if minBased:
        # If our number fell on the lower side of the mean, make sure our
        # number isn't below our actual minimum. If it is, return the actual
        # minimum. (This should only happen 0.15% of the time.)
        if randNum <= mean:
            if randNum < min:
                randNum = min
        else:
            # If our number fell on the higher side of the mean, we need to
            # adjust the number so it fits into the different scale of the max
            # side.
            randNum = ((randNum - mean) * oppositeScale) + mean
            # Then trim the number by the actual max.
            if randNum > max:
                randNum = max
    else:
        # If our number fell on the higher side of the mean, make sure our
        # number isn't above our actual maximum. If it is, return the actual
        # maximum. (This should only happen 0.15% of the time.)
        if randNum >= mean:
            if randNum > max:
                randNum = max
        else:
            # If our number fell on the lower side of the mean, we need to
            # adjust the number so it fits into the different scale of the min
            # side.
            randNum = ((randNum - mean) * oppositeScale) + mean
            # Then trim the number by the actual min.
            if randNum < min:
                randNum = min
    
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


def randomize_settings(existingSettings: dict) -> dict:
    """Generate random settings based on provided weight.
    
    Args:
        existingSettings (dict): The serialized settings based on chosen web
            options. Much of this will be overwritten.
    Returns:
        dict: The settings dictionary, with random settings applied.
    """
    # Erase certain settings from the existing dictionary.
    existingSettings["enemies_selected"] = []
    existingSettings["minigames_list_selected"] = []
    existingSettings["warp_level_list_selected"] = []
    existingSettings["glitches_selected"] = []
    existingSettings["starting_keys_list_selected"] = []
    existingSettings["starting_move_list_selected"] = []
    existingSettings["random_starting_move_list_selected"] = []

    # Generate random settings based on the given weights.
    weightData = js.random_settings_presets[0]
    randomizedSettings = dict()
    numTypes = set([SettingsStringDataType.int16, SettingsStringDataType.int4, SettingsStringDataType.int8, SettingsStringDataType.var_int])
    for settingName, weights in weightData.items():
        settingEnum = SettingsStringEnum[settingName]
        settingType = SettingsStringTypeMap[settingEnum]

        # For a bool setting, generate a random number and see if it's below
        # the provided weight.
        if settingType is SettingsStringDataType.bool:
            randomizedSettings[settingName] = random_bool_setting(weights)
        # For a list setting, generate a random number for every possible value
        # and add that value if it's above the provided weight.
        elif settingType is SettingsStringDataType.list:
            randomizedSettings[settingName] = random_list_setting(weights, settingEnum)
        # For a numeric setting, generate a random number from a distribution
        # based on the provided values.
        elif settingType in numTypes:
            randomizedSettings[settingName] = random_numeric_setting(weights)
        # For an enum setting, generate a random number and see which bucket
        # the number falls into. That bucket's value is chosen.
        else:
            randomizedSettings[settingName] = random_enum_setting(weights, settingEnum)
    
    # If tag anywhere is off, tag barrels must be enabled.
    if not randomizedSettings["enable_tag_anywhere"]:
        randomizedSettings["disable_tag_barrels"] = False
    # Only enable individual hard mode settings if hard mode is enabled.
    if not randomizedSettings["hard_mode"]:
        randomizedSettings["hard_mode_selected"] = []
    # If shops are shuffled in the item randomizer, move_rando is overridden.
    if ItemRandoListSelected.shop in randomizedSettings["item_rando_list_selected"]:
        randomizedSettings["move_rando"] = MoveRando.cross_purchase
    
    # Apply the random settings to the previous dictionary and return.
    existingSettings.update(randomizedSettings)
    return existingSettings
