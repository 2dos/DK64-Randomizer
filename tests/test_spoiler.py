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
    valid_presets.append(("Custom", "bKEHBEMpjoglS2OerK7MIGiAk4BHofVA4IhkQlS2Nc+EaePxGj0uXxCnFid6mnBCgKPSBIYjIY6FuApBbqe3wL8BJIBqE0VVCrFYK0VwGQXWSywUBdACDATqAgcDdgGEAjuBAkFeAKFAzyBgsHegOGBGCCFCGoD2yLcAGVIlRWs5KkpTstmS5JLNFvAjk7RaRcFP0VEWARMRQBXrXHI3ar/fZFA5DuZi19EUAZrNmVjiSLAAuMAAuNAAmOAAmPAAe1AAeQAAWRAAOSAAeTAAWUAAO2AAtTlyhyXCp0woIvoE5LBBhhKrgzG0xrQHFoWlcsLwVocUFsNKgTiwwEwYEZTHFPIpMiM+AA6AUoBdACqAS4GGlRjOAA"))


@parameterized_class(('name', 'settings_string'), valid_presets)
class TestSpoiler(unittest.TestCase):

    def test_settings_string(self):
        """Confirm that settings strings decryption is working and generate a spoiler log with it."""
        # The settings string is defined from the preset_files.json file
        # self.settings_string = "bKEIhEMhTHRBKlsa58Z2rK7MIEw4Kv3LYRjK0SEvAI9HRDHuIQXr5/ADCaLinVCnA+PxGj0uXxDcWa206MSvY04IUFR6QHCQx4OUBSCnt8C/ASSAahlE1QqxWCtFcBkF5kssFAXQAgwE6gIHA3YBhAI7gQJBXgChQM8gYLB3oDhgRgggNMnsyVG3ACZSAUVDOKpSU7LZouaS6RcFPgVsWARMBQCXrXHI3ar/fZFA5DuZi19EUAZrNnk9scSRYAFxgAFxoAExwAEx4AD2oADyAACyIAByQADyYACygAB2wAFqcuUOS4VAoNTmNaA4tC03FcsLwVocUFsNFATiwwEwYEY0EVTHFFJkRnwAVAClALoAbwBVAJcFCgwNIyycAA"
        settings_dict = decrypt_settings_string_enum(self.settings_string)
        settings_dict["seed"] = random.randint(0, 100000000)  # Can be fixed if you want to test a specific seed repeatedly

        # Plando testing - fill the data with a json string
        # settings_dict["enable_plandomizer"] = True
        # settings_dict["plandomizer_data"] = json.loads('{"plando_starting_exit": -1, "plando_starting_kongs_selected": [-1], "plando_kong_rescue_diddy": -1, "plando_kong_rescue_lanky": -1, "plando_kong_rescue_tiny": -1, "plando_kong_rescue_chunky": -1, "plando_level_order_0": -1, "plando_level_order_1": -1, "plando_level_order_2": -1, "plando_level_order_3": -1, "plando_level_order_4": -1, "plando_level_order_5": -1, "plando_level_order_6": -1, "plando_level_order_7": -1, "plando_krool_order_0": -1, "plando_krool_order_1": -1, "plando_krool_order_2": -1, "plando_helm_order_0": -1, "plando_helm_order_1": -1, "plando_helm_order_2": -1, "plando_place_fairies": false, "plando_place_arenas": false, "plando_place_patches": false, "plando_place_kasplats": false, "plando_place_crates": false, "plando_place_wrinkly": false, "plando_place_tns": false, "locations": {"51": 52}, "prices": {}, "plando_bonus_barrels": {}, "plando_switchsanity": {"1": {"kong": 0}, "2": {"kong": 4, "switch_type": 1}}, "plando_battle_arenas": {}, "plando_dirt_patches": [], "plando_fairies": [], "plando_kasplats": {}, "plando_melon_crates": [], "plando_wrinkly_doors": {}, "plando_tns_portals": {}, "hints": {}}')

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
