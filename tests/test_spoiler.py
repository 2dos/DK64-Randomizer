"""Temp file used for testing new logic system."""
import json
import os
import random
import unittest

from parameterized import parameterized_class

# from randomizer.Enums.Items import Items
from randomizer.Enums.HintType import HintType
import randomizer.Lists.Exceptions as Ex
from randomizer.Enums.Settings import (ActivateAllBananaports, BananaportRando, CBRando,
                                       CrownEnemyRando, DamageAmount,
                                       ExtraCutsceneSkips, FillAlgorithm,
                                       FreeTradeSetting, HelmDoorItem, HelmBonuses,
                                       HelmSetting, KasplatRandoSetting,
                                       KrushaUi, LevelRandomization, LogicType,
                                       MicrohintsEnabled, MoveRando,
                                       RandomPrices, SettingsMap,
                                       ShockwaveStatus, SpoilerHints,
                                       TrainingBarrels, WinConditionComplex,
                                       WrinklyHints)
from randomizer.Fill import Generate_Spoiler
from randomizer.Settings import Settings
from randomizer.SettingStrings import decrypt_settings_string_enum
from randomizer.Spoiler import Spoiler

# Get the preset_files.json file from static/presets
with open("static/presets/preset_files.json", "r") as file:
    preset_files = json.load(file)
    # For each preset in the list if settings_string is not None, add the preset to the list
    valid_presets = [(preset.get("name"), preset.get("settings_string")) for preset in preset_files if preset.get("settings_string")]

# Add a custom preset for testing
# If we're not running on github actions, add the custom preset
if not os.environ.get("GITHUB_ACTIONS"):
    valid_presets.append(("Custom", "bKEHhEMhTHSpbGufFWUIGiA9HSLGAQ3EGWsQgvXz+AbPHwwmjnd1K9lZmcU2dWxfCnA+qBoRDIhKlsa58B+I0eu0uXxCnLE2nBCgKPSA6K01fAUgt1PX4EkAyaKE0SMgusllgoA6AEGAHUBA4A7AMIAHcCBIA8AUKAHkDBYA9AcMAFCGnj2yFI9RUM5alpTLm0W8DODo9Rbgp+iuiwCJ6KAK9a45G7Vf77IoHMWIoAzZ5EkWABMYABMaAA8cAA8eAAsgAAsiAAckAAcmAAcoAAanLlDkuFTphCSCL6BOSDDCVU5mNpjBxaFpXLArQ5bDQnFgqVBgJgwIxIUxxTSeRSZEalAFUAlwEMnAA"))


@parameterized_class(('name', 'settings_string'), valid_presets)
class TestSpoiler(unittest.TestCase):

    def test_settings_string(self):
        """Confirm that settings strings decryption is working and generate a spoiler log with it."""
        # The settings string is defined from the preset_files.json file
        self.settings_string = "bKEJBEMhTHRBKlsa58ZKyuxCAIgJI9D6oHBEMiEqWxrnwjTx+I0ely+IU4sTvU04IUBR6QICMhjoW4CkFup7fAvwEkgGoTRVUKsVgrRXAZBdZLLBQB0AIMAOoCBwB2AYQAO4ECQB4AoUAPIGCwB6A4YAKENQHtkW4AMqRKitZyVJSnZbMlySWaLeBHJ2i0i4KfoqIsAiYigEvWuORu1X++yKByHczFr6IoAzWbMrHEkWABMYABMaAA8cAA8eAAtqAA8gAAsiAAckAAcmAAcoAAdsABanLlDkuFTphQRfQJyWCDDCVXBmNpjWgOLQtK5YXgrQ4oLYaVAnFhgJgwIymOKeRSZEYdAKUAugBVAJcICAkKCwwNKjE"
        settings_dict = decrypt_settings_string_enum(self.settings_string)
        settings_dict["seed"] = random.randint(0, 100000000)  # Can be fixed if you want to test a specific seed repeatedly

        # Plando testing - fill the data with a json string
        # settings_dict["enable_plandomizer"] = True
        # settings_dict["plandomizer_data"] = '{"plando_starting_kongs_selected": [0], "plando_kong_rescue_diddy": -1, "plando_kong_rescue_lanky": -1, "plando_kong_rescue_tiny": -1, "plando_kong_rescue_chunky": -1, "plando_level_order_0": 4, "plando_level_order_1": 2, "plando_level_order_2": 5, "plando_level_order_3": 3, "plando_level_order_4": 6, "plando_level_order_5": 1, "plando_level_order_6": 0, "plando_krool_order_0": -1, "plando_krool_order_1": -1, "plando_krool_order_2": -1, "plando_krool_order_3": -1, "plando_krool_order_4": -1, "plando_helm_order_0": -1, "plando_helm_order_1": -1, "plando_helm_order_2": -1, "plando_helm_order_3": -1, "plando_helm_order_4": -1, "locations": {"42": 26, "537": 50, "594": 47, "72": 25, "67": 49, "83": 16, "88": 23, "125": 30, "164": 29, "159": 21, "166": 9, "194": 24, "210": 39, "211": 28, "212": 32, "213": 8, "214": 39, "245": 4, "224": 19, "243": 12, "244": 45, "222": 35, "231": 18, "255": 31, "251": 27, "261": 6, "252": 48, "312": 3, "296": 5, "299": 22, "286": 17, "310": 10, "287": 7, "539": 34, "331": 10, "332": 39, "326": 38, "327": 37, "328": 36, "329": 14, "330": 11, "369": 15, "443": 2, "447": 20}, "prices": {}, "plando_bonus_barrels": {"231": 13, "296": 59, "299": 70, "310": 39}, "hints": {}}'

        settings = Settings(settings_dict)
        # settings.extreme_debugging = True  # Greatly slows seed gen, use with caution
        spoiler = Spoiler(settings)
        Generate_Spoiler(spoiler)
        print(spoiler)
        print(spoiler.json)
        # self.printHintDistribution(spoiler)
        # self.printDesiredOutput(spoiler)
        with open(f"test-result-{self.name}.json", "w") as outfile:
            outfile.write(spoiler.json)
        print(f"test {self.name} done")

    def printHintDistribution(self, spoiler: Spoiler):
        """Print the hint distribution for the given spoiler log."""
        types = ""
        values = ""
        for key, value in spoiler.hint_distribution.items():
            types += (key.name + ", ")
            values += (str(value) + ", ")
        print(types)
        print(values)


def printDesiredOutput(self, spoiler: Spoiler):
    """Print any desired output from the spoiler. Customize to your heart's desire."""
    print("# of path hints: " + str(spoiler.hint_distribution[HintType.Multipath]) + " | woth length: " + str(len(spoiler.woth_locations) - 2))
    print()
