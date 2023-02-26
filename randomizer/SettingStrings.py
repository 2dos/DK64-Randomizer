"""Encryption and Decryption of settings strings."""
import base64
import collections
import json
from itertools import groupby

import js

from randomizer.Enums.Settings import SettingsMap, SettingsStringDataType, SettingsStringEnum, SettingsStringListTypeMap, SettingsStringTypeMap

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
        # If this key is in the SettingsMap, convert the value to enum.
        convert_to_enum = key_name in SettingsMap
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
                else:
                    enum_values = [member.value for member in key_list_data_type]
                    index = int(bitstring[bit_index : bit_index + len(enum_values).bit_length()], 2)
                    list_val = key_list_data_type(index)
                    bit_index += len(enum_values).bit_length()
                # Convert to enum, if necessary.
                if convert_to_enum:
                    list_val = SettingsMap[key_name](list_val)
                val.append(list_val)
        else:
            enum_values = [member.value for member in key_data_type]
            index = int(bitstring[bit_index : bit_index + len(enum_values).bit_length()], 2)
            settings_dict[key_name] = key_data_type(index)
            bit_index += len(enum_values).bit_length()
        # Convert to enum, if necessary.
        if convert_to_enum and key_data_type != SettingsStringDataType.list:
            val = SettingsMap[key_name](val)
        settings_dict[key_name] = val
    return settings_dict


def encrypt_settings_string(dict_data: dict):
    """Take a dictionary and return an encrypted string.

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
        dict_data.pop(pop)
    ordered_dict = collections.OrderedDict(sorted(dict_data.items()))
    original_dict = collections.OrderedDict(sorted(default_dict.items()))
    strdata = ""
    for item in ordered_dict:
        if original_dict[item] == ordered_dict[item]:
            strdata += ","
        elif type(ordered_dict[item]) == bool:
            if ordered_dict[item] is True:
                strdata += "x1,"
            else:
                strdata += "x0,"
        else:
            strdata += str(ordered_dict[item]) + ","
    base64_encoded_string = str(base64.b64encode(strdata.encode("ascii"))).replace("b'", "").replace("'", "")
    split_strings = []
    for index in range(0, len(base64_encoded_string), 4):
        split_strings.append(base64_encoded_string[index : index + 4])

    def encode_list(s_list):
        return [[len(list(group)), key] for key, group in groupby(s_list)]

    new_string = ""
    for item in encode_list(split_strings):
        new_string += "|" + str(item[0]) + ":" + item[1]
    return new_string


def decrypt_setting_string(encrypted_string: str):
    """Take an encrypted string and return a dictionary.

    Args:
        encrypted_string (str): Passed settings string.

    Returns:
        dict: Returns the decrypted set of data.
    """
    expanded = ""
    for item in encrypted_string.split("|"):
        if item:
            if ":" in item:
                count, key = item.split(":")
                expanded += key * int(count)
            else:
                expanded += item

    new_dict = {}
    index = 0
    array = False
    value = []
    original_dict = collections.OrderedDict(sorted(default_dict.items()))
    for item in base64.b64decode(expanded).decode("ascii").split(","):
        if "[" in item:
            array = True
            new_str = item.replace("[", "").replace("'", "").replace(" ", "")
            value.append(new_str)
        elif "]" in item:
            array = False
            new_str = item.replace("]", "").replace("'", "").replace(" ", "")
            value.append(new_str)
            new_dict[list(original_dict.items())[index][0]] = value
            index += 1
            value = []
        elif array:
            new_str = item.replace("'", "").replace(" ", "")
            value.append(new_str)
        else:
            if index < len(list(original_dict.items())):
                if item == "x1":
                    new_item = True
                elif item == "x0":
                    new_item = False
                elif item == "":
                    new_item = list(original_dict.items())[index][1]
                else:
                    new_item = item
                if isinstance(new_item, str) and new_item.isnumeric():
                    new_item = int(new_item)
                new_dict[list(original_dict.items())[index][0]] = new_item
            index += 1
    return new_dict


# Default settings
resp = js.getFile("./static/presets/default.json")
default_dict = json.loads(resp)
