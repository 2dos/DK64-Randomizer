"""Temp file used for testing new logic system."""
import json
import os
import random
import unittest
from unittest import mock

from parameterized import parameterized_class

# from randomizer.Enums.Items import Items
from randomizer.Enums.HintType import HintType
import randomizer.Lists.Exceptions as Ex
import randomizer.Patching.ApplyRandomizer as ApplyRandomizer
from randomizer.Enums.Settings import (ActivateAllBananaports, BananaportRando, CBRando,
                                       CrownEnemyDifficulty, DamageAmount,
                                       ExtraCutsceneSkips, FillAlgorithm,
                                       FreeTradeSetting, HelmDoorItem, HelmBonuses,
                                       HelmSetting, KasplatRandoSetting,
                                       KrushaUi, LevelRandomization, LogicType,
                                       MicrohintsEnabled, MoveRando, ProgressiveHintAlgorithm,
                                       RandomPrices, SettingsMap,
                                       ShockwaveStatus, SpoilerHints,
                                       TrainingBarrels, WinConditionComplex,
                                       WrinklyHints)
from randomizer.Fill import Generate_Spoiler
from randomizer.Settings import Settings
from randomizer.ProtoSerializer import settings_string_to_form_data
from randomizer.Spoiler import Spoiler

# For each preset in the list if settings_string is not None, add the preset to the list
valid_presets = []
valid_presets.append(("Custom", "eNqVkj1MFEEUx_f_Zvd2du5rbrmDZe-DveXrOL6OBcwFI54daoPix5mgkBiVSg02VIZYUZKYGENFJ4WFsaI0BuP3R6wsLY2VpaWzc5AYO2eyv8zMe2_eznt_8RVuUjiTY1Ph0PD0bM11hSRmOaI6UvFL3V4-5WZdQ8-yKMJMjE80eDKdkbmuQk9vsdwX9A9EM4P10UMnwx8SIXeEdnHzhW6v1y-VK0E17B8YHBqujYyNT0w2ZiXz08JJjU7NrDzFE5K2bwu2fPWaJN8SrB5N-0YI1Acl_CpnknksQA0NNNHCAi1Sm1Zpjd3FBjZBUZq_hax5-UDUZMNq1tx9EhlOLgedNq2Ezb3Iz3K43Dgc3iOEJCt1kohIJuZIRmdSsQPUIGLs_AHU1uSQliJJrqh-Q9HUtCQpJrTV1idcxv6OInGhVkltSykST6tVRluyaiV1bE5FEXfV16V2eR1dkKZit7b36Fs9fdKr6WsWNUuaZc2KZp9moO-paoYSa1hPIsdM20mmsm7XBqlqbYFtg-0gC2K6OKpZqXQmuwvaQ-Tf52adGlg3HoA4toBt4DGwC-yBXqLAX2EHd5YO8Brv8QEf8Qmf8Q79143q7eXgxiV56sT8yVax0pdwzt06fuHylbGbzaXpi-0Vq_QF-Ab87GROHOWVuV_AJuE5Gb_JCu8JW1WeMTLdY6rA3EMYP_Q_6CsF-zQ3Hyi9hKYkz6jnFRErKIpbGtOSrYhzdHRVfwhxNjZ0nA5lhkW0sapq2JHZP7XAM2AfeAG8ATov-w78ANRrjrL9fZFqxUQsKZWEOrY53_WUTJJeMnBqTsNuWi17gS3abWuVtaitIv8AXRRpeQ"))


@parameterized_class(('name', 'settings_string'), valid_presets)
class TestSpoiler(unittest.TestCase):

    def test_settings_string(self):
        """Confirm that settings strings decryption is working and generate a spoiler log with it."""
        # The settings string is defined either here or in the string above, pick your poison
        self.settings_string = "eNqVkj1MFEEUx_f_Zvd2du5rbrmDZe-DveXrOL6OBcwFI54daoPix5mgkBiVSg02VIZYUZKYGENFJ4WFsaI0BuP3R6wsLY2VpaWzc5AYO2eyv8zMe2_eznt_8RVuUjiTY1Ph0PD0bM11hSRmOaI6UvFL3V4-5WZdQ8-yKMJMjE80eDKdkbmuQk9vsdwX9A9EM4P10UMnwx8SIXeEdnHzhW6v1y-VK0E17B8YHBqujYyNT0w2ZiXz08JJjU7NrDzFE5K2bwu2fPWaJN8SrB5N-0YI1Acl_CpnknksQA0NNNHCAi1Sm1Zpjd3FBjZBUZq_hax5-UDUZMNq1tx9EhlOLgedNq2Ezb3Iz3K43Dgc3iOEJCt1kohIJuZIRmdSsQPUIGLs_AHU1uSQliJJrqh-Q9HUtCQpJrTV1idcxv6OInGhVkltSykST6tVRluyaiV1bE5FEXfV16V2eR1dkKZit7b36Fs9fdKr6WsWNUuaZc2KZp9moO-paoYSa1hPIsdM20mmsm7XBqlqbYFtg-0gC2K6OKpZqXQmuwvaQ-Tf52adGlg3HoA4toBt4DGwC-yBXqLAX2EHd5YO8Brv8QEf8Qmf8Q79143q7eXgxiV56sT8yVax0pdwzt06fuHylbGbzaXpi-0Vq_QF-Ab87GROHOWVuV_AJuE5Gb_JCu8JW1WeMTLdY6rA3EMYP_Q_6CsF-zQ3Hyi9hKYkz6jnFRErKIpbGtOSrYhzdHRVfwhxNjZ0nA5lhkW0sapq2JHZP7XAM2AfeAG8ATov-w78ANRrjrL9fZFqxUQsKZWEOrY53_WUTJJeMnBqTsNuWi17gS3abWuVtaitIv8AXRRpeQ"
        settings_dict = settings_string_to_form_data(self.settings_string)
        settings_dict["seed"] = random.randint(0, 100000000)  # Can be fixed if you want to test a specific seed repeatedly

        # Plando testing - fill the data with a json string
        # settings_dict["enable_plandomizer"] = True
        # settings_dict["plandomizer_data"] = json.loads('{"plando_starting_exit": -1, "plando_starting_kongs_selected": [-1], "plando_kong_rescue_diddy": -1, "plando_kong_rescue_lanky": -1, "plando_kong_rescue_tiny": -1, "plando_kong_rescue_chunky": -1, "plando_level_order_0": -1, "plando_level_order_1": -1, "plando_level_order_2": -1, "plando_level_order_3": -1, "plando_level_order_4": -1, "plando_level_order_5": -1, "plando_level_order_6": -1, "plando_level_order_7": -1, "plando_krool_order_0": -1, "plando_krool_order_1": -1, "plando_krool_order_2": -1, "plando_helm_order_0": -1, "plando_helm_order_1": -1, "plando_place_fairies": false, "plando_place_arenas": false, "plando_place_patches": false, "plando_place_kasplats": false, "plando_place_crates": false, "plando_place_wrinkly": false, "plando_place_tns": false, "locations": {"156": 18}, "prices": {}, "plando_bonus_barrels": {"156": 60}, "plando_switchsanity": {}, "plando_battle_arenas": {}, "plando_dirt_patches": [], "plando_fairies": [], "plando_kasplats": {}, "plando_melon_crates": [], "plando_wrinkly_doors": {}, "plando_tns_portals": {}, "hints": {}}')

        settings = Settings(settings_dict)
        settings.progressive_hint_algorithm = ProgressiveHintAlgorithm.medium
        # settings.extreme_debugging = True  # Greatly slows seed gen, use with caution
        spoiler = Spoiler(settings)
        # Skip the server ROM patch (TODO: Find Proper fix)
        with mock.patch.object(ApplyRandomizer, "patching_response", return_value=(b"", None)):
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
