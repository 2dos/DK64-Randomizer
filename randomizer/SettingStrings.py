"""Encryption and Decryption of settings strings."""
import base64
import collections
import json
from itertools import groupby

import js

from randomizer.Enums.Settings import (
    SettingsStringDataType,
    SettingsStringEnum,
    SettingsStringListTypeMap,
    SettingsStringTypeMap,
)

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
        "lanky_colors",
        "lanky_custom_color",
        "rambi_colors",
        "rambi_custom_color",
        "random_colors",
        "random_music",
        "music_bgm",
        "music_events",
        "music_fanfares",
        "tiny_colors",
        "tiny_custom_color",
        "override_cosmetics",
        "remove_water_oscillation",
        "colorblind_mode",
        "search",
        "holiday_mode",
        "homebrew_header",
    ]:
        if pop in dict_data:
            dict_data.pop(pop)
    bitstring = ""
    for key in dict_data:
        value = dict_data[key]
        # At this time, all strings represent ints, so just convert.
        if type(value) == str:
            value = int(value)
        key_enum = SettingsStringEnum[key]
        key_data_type = SettingsStringTypeMap[key_enum]
        # Encode the key.
        bitstring += bin(key_enum)[2:].zfill(8)
        if key_data_type == SettingsStringDataType.bool:
            bitstring += "1" if value else "0"
        elif key_data_type == SettingsStringDataType.int4:
            bitstring += int_to_bin_string(value, 4)
        elif key_data_type == SettingsStringDataType.int8:
            bitstring += int_to_bin_string(value, 8)
        elif key_data_type == SettingsStringDataType.int16:
            bitstring += int_to_bin_string(value, 16)
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
                else:
                    enum_values = [member.value for member in key_list_data_type]
                    index = enum_values.index(item.value)
                    bitstring += format(index, f"0{len(enum_values).bit_length()}b")
        else:
            enum_values = [member.value for member in key_data_type]
            index = enum_values.index(value.value)
            bitstring += format(index, f"0{len(enum_values).bit_length()}b")

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
    # If there are fewer than nine characters left in our bitstring, we have
    # hit the padding. (Nine characters is the minimum needed for a key and a
    # value.)
    while bit_index < (bitstring_length - 9):
        # Consume the next key.
        key = int(bitstring[bit_index : bit_index + 8], 2)
        bit_index += 8
        key_enum = SettingsStringEnum(key)
        key_name = key_enum.name
        key_data_type = SettingsStringTypeMap[key_enum]
        if key_data_type == SettingsStringDataType.bool:
            settings_dict[key_name] = True if bitstring[bit_index] == "1" else False
            bit_index += 1
        elif key_data_type == SettingsStringDataType.int4:
            settings_dict[key_name] = bin_string_to_int(bitstring[bit_index : bit_index + 4], 4)
            bit_index += 4
        elif key_data_type == SettingsStringDataType.int8:
            settings_dict[key_name] = bin_string_to_int(bitstring[bit_index : bit_index + 8], 8)
            bit_index += 8
        elif key_data_type == SettingsStringDataType.int16:
            settings_dict[key_name] = bin_string_to_int(bitstring[bit_index : bit_index + 16], 16)
            bit_index += 16
        elif key_data_type == SettingsStringDataType.list:
            list_length = int(bitstring[bit_index : bit_index + 8], 2)
            bit_index += 8
            settings_dict[key_name] = []
            key_list_data_type = SettingsStringListTypeMap[key_enum]
            for _ in range(list_length):
                if key_list_data_type == SettingsStringDataType.bool:
                    settings_dict[key_name].append(True if bitstring[bit_index] == "1" else False)
                    bit_index += 1
                elif key_list_data_type == SettingsStringDataType.int4:
                    settings_dict[key_name] = bin_string_to_int(bitstring[bit_index : bit_index + 4], 4)
                    bit_index += 4
                elif key_list_data_type == SettingsStringDataType.int8:
                    settings_dict[key_name] = bin_string_to_int(bitstring[bit_index : bit_index + 8], 8)
                    bit_index += 8
                elif key_list_data_type == SettingsStringDataType.int16:
                    settings_dict[key_name] = bin_string_to_int(bitstring[bit_index : bit_index + 16], 16)
                    bit_index += 16
                else:
                    enum_values = [member.value for member in key_list_data_type]
                    index = int(bitstring[bit_index : bit_index + len(enum_values).bit_length()], 2)
                    settings_dict[key_name].append(key_list_data_type(index))
                    bit_index += len(enum_values).bit_length()
        else:
            enum_values = [member.value for member in key_data_type]
            index = int(bitstring[bit_index : bit_index + len(enum_values).bit_length()], 2)
            settings_dict[key_name] = key_data_type(index)
            bit_index += len(enum_values).bit_length()
    return settings_dict
