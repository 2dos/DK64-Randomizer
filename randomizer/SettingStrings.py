"""Encryption and Decryption of settings strings."""
import base64
import collections
import json
from itertools import groupby

import js


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
        "krusha_slot",
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
