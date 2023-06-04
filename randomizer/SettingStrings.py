"""Encryption and Decryption of settings strings."""
import base64
import collections
import json
from itertools import groupby

import js
from randomizer.Enums.Settings import BananaportRando, LogicType, SettingsStringDataType, SettingsStringEnum, SettingsStringIntRangeMap, SettingsStringListTypeMap, SettingsStringTypeMap

letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
index_to_letter = {i: letters[i] for i in range(64)}
letter_to_index = {letters[i]: i for i in range(len(letters))}


def int_to_bin_string(num, bytesize):
    """Convert an integer to a binary representation.

    This function is needed to handle negative numbers.
    """
    return format(num if num >= 0 else (1 << bytesize) + num, f"0{bytesize}b").zfill(bytesize)


def bin_string_to_int(bin_str, bytesize):
    """Convert a binary string to an integer.

    This function is needed to handle negative numbers.
    """
    if bin_str[0] == "1":
        return int(bin_str, 2) - (1 << bytesize)
    else:
        return int(bin_str, 2)


def get_var_int_encode_details(settingEnum):
    """Return key information needed to encode/decode a given var_int setting.

    Returns:
        int - The bit length of the int.
        bool - True if negative numbers are possible.
    """
    range = SettingsStringIntRangeMap[settingEnum]
    max_val = range["max"]
    min_val = range["min"]
    limiting_val = max_val
    negatives_possible = min_val < 0
    if negatives_possible and abs(min_val) > max_val:
        # We subtract one, to handle the edge case where the absolute value is
        # a negative power of 2.
        limiting_val = abs(min_val) - 1
    # Get the bit length of the limiting value.
    bit_len = limiting_val.bit_length()
    # If negatives are possible, add one to the bit length.
    if negatives_possible:
        bit_len += 1
    return bit_len, negatives_possible


def encode_var_int(settingEnum, num):
    """Convert a variable-size integer to a binary representation."""
    bit_len, _ = get_var_int_encode_details(settingEnum)
    return int_to_bin_string(num, bit_len)


def decode_var_int(settingEnum, bin_str):
    """Convert a binary string to a variable-size integer."""
    bit_len, negatives_possible = get_var_int_encode_details(settingEnum)
    if negatives_possible:
        return bin_string_to_int(bin_str, bit_len)
    else:
        return int(bin_str, 2)


# A map tying certain key settings to other settings that should be excluded
# from the string, if the key setting has a certain value.
settingsExclusionMap = {
    "helm_hurry": {
        False: [
            "helmhurry_list_banana_medal",
            "helmhurry_list_battle_crown",
            "helmhurry_list_bean",
            "helmhurry_list_blueprint",
            "helmhurry_list_boss_key",
            "helmhurry_list_colored_bananas",
            "helmhurry_list_company_coins",
            "helmhurry_list_fairies",
            "helmhurry_list_golden_banana",
            "helmhurry_list_ice_traps",
            "helmhurry_list_kongs",
            "helmhurry_list_move",
            "helmhurry_list_pearl",
            "helmhurry_list_rainbow_coin",
            "helmhurry_list_starting_time",
        ]
    },
    "shuffle_items": {False: ["item_rando_list_selected"]},
    "enemy_rando": {False: ["enemies_selected"]},
    "bonus_barrel_rando": {False: ["minigames_list_selected"]},
    "bananaport_rando": {BananaportRando.off: ["warp_level_list_selected"]},
    "logic_type": {LogicType.glitchless: ["glitches_selected"], LogicType.nologic: ["glitches_selected"]},
    "select_keys": {False: ["starting_keys_list_selected"], True: ["krool_key_count"]},
    "quality_of_life": {False: ["misc_changes_selected"]},
}


def prune_settings(settings_dict: dict):
    """Remove certain settings based on the values of other settings."""
    settings_to_remove = []
    for keySetting, exclusions in settingsExclusionMap.items():
        if settings_dict[keySetting] in exclusions:
            settings_to_remove.extend(exclusions[settings_dict[keySetting]])
    for pop in settings_to_remove:
        if pop in settings_dict:
            settings_dict.pop(pop)
    return settings_dict


def encrypt_settings_string_enum(dict_data: dict):
    """Take a dictionary and return an enum-based encrypted string.

    Args:
        dict_data (dict): Posted JSON data from the form.

    Returns:
        str: Returns an encrypted string.
    """
    for pop in [
        "download_patch_file",
        "seed",
        "settings_string",
        "chunky_colors",
        "chunky_custom_color",
        "diddy_colors",
        "diddy_custom_color",
        "dk_colors",
        "dk_custom_color",
        "enguarde_colors",
        "enguarde_custom_color",
        "klaptrap_model",
        "misc_cosmetics",
        "disco_chunky",
        "dark_mode_textboxes",
        "lanky_colors",
        "lanky_custom_color",
        "rambi_colors",
        "rambi_custom_color",
        "random_colors",
        "random_music",
        "music_bgm_randomized",
        "music_events_randomized",
        "music_majoritems_randomized",
        "music_minoritems_randomized",
        "tiny_colors",
        "tiny_custom_color",
        "override_cosmetics",
        "remove_water_oscillation",
        "head_balloons",
        "colorblind_mode",
        "search",
        "holiday_setting",
        "homebrew_header",
        "dpad_display",
        "camera_is_follow",
        "sfx_volume",
        "music_volume",
        "camera_is_widescreen",
        "camera_is_not_inverted",
        "sound_type",
    ]:
        if pop in dict_data:
            dict_data.pop(pop)
    dict_data = prune_settings(dict_data)
    bitstring = ""
    for key in dict_data:
        value = dict_data[key]
        # At this time, all strings represent ints, so just convert.
        if type(value) == str:
            value = int(value)
        key_enum = SettingsStringEnum[key]
        key_data_type = SettingsStringTypeMap[key_enum]
        # Encode the key.
        key_size = max([member.value for member in SettingsStringEnum]).bit_length()
        bitstring += bin(key_enum)[2:].zfill(key_size)
        if key_data_type == SettingsStringDataType.bool:
            bitstring += "1" if value else "0"
        elif key_data_type == SettingsStringDataType.int4:
            bitstring += int_to_bin_string(value, 4)
        elif key_data_type == SettingsStringDataType.int8:
            bitstring += int_to_bin_string(value, 8)
        elif key_data_type == SettingsStringDataType.int16:
            bitstring += int_to_bin_string(value, 16)
        elif key_data_type == SettingsStringDataType.var_int:
            bitstring += encode_var_int(key_enum, value)
        elif key_data_type == SettingsStringDataType.list:
            bitstring += f"{len(value):08b}"
            key_list_data_type = SettingsStringListTypeMap[key_enum]
            for item in value:
                if type(item) == str:
                    item = int(item)
                if key_list_data_type == SettingsStringDataType.bool:
                    bitstring += "1" if item else "0"
                elif key_list_data_type == SettingsStringDataType.int4:
                    bitstring += int_to_bin_string(item, 4)
                elif key_list_data_type == SettingsStringDataType.int8:
                    bitstring += int_to_bin_string(item, 8)
                elif key_list_data_type == SettingsStringDataType.int16:
                    bitstring += int_to_bin_string(item, 16)
                elif key_list_data_type == SettingsStringDataType.var_int:
                    bitstring += encode_var_int(key_enum, item)
                else:
                    # The value is an enum.
                    max_value = max([member.value for member in key_list_data_type])
                    bitstring += format(item.value, f"0{max_value.bit_length()}b")
        else:
            # The value is an enum.
            max_value = max([member.value for member in key_data_type])
            bitstring += format(value.value, f"0{max_value.bit_length()}b")

    # Pad the bitstring with zeroes until the length is divisible by 6.
    remainder = len(bitstring) % 6
    if remainder > 0:
        for _ in range(0, 6 - remainder):
            bitstring += "0"

    # Split the bitstring into 6-bit chunks and look up the corresponding
    # letters.
    letter_string = ""
    for i in range(0, len(bitstring), 6):
        chunk = int(bitstring[i : i + 6], 2)
        letter_string += letters[chunk]
    return letter_string


def decrypt_settings_string_enum(encrypted_string: str):
    """Take an enum-based encrypted string and return a dictionary.

    Args:
        encrypted_string (str): Passed settings string.

    Returns:
        dict: Returns the decrypted set of data.
    """
    # Take each letter of the encrypted_string and convert it to a 6-bit binary
    # number, then use the embedded keys to get the value from the settings
    # string.
    bitstring = ""
    for letter in encrypted_string:
        index = letter_to_index[letter]
        bitstring += f"{index:06b}"
    bitstring_length = len(bitstring)
    settings_dict = {}
    bit_index = 0
    key_size = max([member.value for member in SettingsStringEnum]).bit_length()
    # If there are fewer than (key_size + 1) characters left in our bitstring,
    # we have hit the padding. (key_size + 1 characters is the minimum needed
    # for a key and a value.)
    while bit_index < (bitstring_length - (key_size + 1)):
        # Consume the next key.
        key = int(bitstring[bit_index : bit_index + key_size], 2)
        bit_index += key_size
        key_enum = SettingsStringEnum(key)
        key_name = key_enum.name
        key_data_type = SettingsStringTypeMap[key_enum]
        val = None
        if key_data_type == SettingsStringDataType.bool:
            val = True if bitstring[bit_index] == "1" else False
            bit_index += 1
        elif key_data_type == SettingsStringDataType.int4:
            val = bin_string_to_int(bitstring[bit_index : bit_index + 4], 4)
            bit_index += 4
        elif key_data_type == SettingsStringDataType.int8:
            val = bin_string_to_int(bitstring[bit_index : bit_index + 8], 8)
            bit_index += 8
        elif key_data_type == SettingsStringDataType.int16:
            val = bin_string_to_int(bitstring[bit_index : bit_index + 16], 16)
            bit_index += 16
        elif key_data_type == SettingsStringDataType.var_int:
            bit_len, _ = get_var_int_encode_details(key_enum)
            val = decode_var_int(key_enum, bitstring[bit_index : bit_index + bit_len])
            bit_index += bit_len
        elif key_data_type == SettingsStringDataType.list:
            list_length = int(bitstring[bit_index : bit_index + 8], 2)
            bit_index += 8
            val = []
            key_list_data_type = SettingsStringListTypeMap[key_enum]
            for _ in range(list_length):
                list_val = None
                if key_list_data_type == SettingsStringDataType.bool:
                    list_val = True if bitstring[bit_index] == "1" else False
                    bit_index += 1
                elif key_list_data_type == SettingsStringDataType.int4:
                    list_val = bin_string_to_int(bitstring[bit_index : bit_index + 4], 4)
                    bit_index += 4
                elif key_list_data_type == SettingsStringDataType.int8:
                    list_val = bin_string_to_int(bitstring[bit_index : bit_index + 8], 8)
                    bit_index += 8
                elif key_list_data_type == SettingsStringDataType.int16:
                    list_val = bin_string_to_int(bitstring[bit_index : bit_index + 16], 16)
                    bit_index += 16
                elif key_data_type == SettingsStringDataType.var_int:
                    bit_len, _ = get_var_int_encode_details(key_enum)
                    list_val = decode_var_int(key_enum, bitstring[bit_index : bit_index + bit_len])
                    bit_index += bit_len
                else:
                    # The value is an enum.
                    max_value = max([member.value for member in key_list_data_type])
                    int_val = int(bitstring[bit_index : bit_index + max_value.bit_length()], 2)
                    list_val = key_list_data_type(int_val)
                    bit_index += max_value.bit_length()
                val.append(list_val)
        else:
            # The value is an enum.
            max_value = max([member.value for member in key_data_type])
            int_val = int(bitstring[bit_index : bit_index + max_value.bit_length()], 2)
            val = key_data_type(int_val)
            bit_index += max_value.bit_length()
        settings_dict[key_name] = val
    return settings_dict
