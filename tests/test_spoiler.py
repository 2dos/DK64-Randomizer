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
                                       CrownEnemyDifficulty, DamageAmount,
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

# For each preset in the list if settings_string is not None, add the preset to the list
valid_presets = []
valid_presets.append(("Custom", "Px+VnF6AAa/AAZggAAwwAAYoAAP9A0yAoCBgIDgYIBASCgoGBYODAiAJ1lhuAJvARwAZxAhyApzAx0A65BBMwEJxShMDTCaCBNZAK0C0S0i0y1E1U1m122W2gbbbjbqdwbzcJcBb4d5eAcQc5cYcicrcweKdAdJdUdadjdsNFMxNQki4gDrVEqAQUQKMFIClBTAQRcE9TZPlm2YhGyyn4ZCWFsBbgJGYxTSBHR8QpFmpJeixi9U6FRCwCEzCiASJHaqqsmWHJkneIoDiGV5ArGgY8ljAyAAVTPEN0EIQAC0KABaGAAlDgASiAAHVoADokABUUAAaLAAdGAAKjQADVwAFk9EsqmwVgui2PZniyDBHDAM5klgD5dgcKYqFoY4rA0FYhjWFwWk8JJ/EsQZIl0XhcEBIUFhgaHCAiJCgqLDAyNDg6PEBCREZISkxOUFJUVlhaXF5gYmRmaGq4ury/WL4AYAAwgBiAB2AH6CFXJwRCKIyFMdCVwY1z1J0QCIZCmOhKlsbBzw6R4wCHdcQZaxCC9fP4Bs8fDCaOd3Ur2VmZxTZ1bF8KcKAmEQyFMdCVLY1z4RlM/gCyAIKACYAKI8EQyFMdCVLY1z4RlOlbXxnW+d88gB7gDzFAgxSSjD0lFmGnHoYpp6KXwLAiDDkFmnIIpqrstuvwRyS1PQAfIA9QB9AD2AH2AA"))


@parameterized_class(('name', 'settings_string'), valid_presets)
class TestSpoiler(unittest.TestCase):

    def test_settings_string(self):
        """Confirm that settings strings decryption is working and generate a spoiler log with it."""
        # The settings string is defined either here or in the string above, pick your poison
        self.settings_string = "Px+YQAAEKA4WBwwDhoDDgGHgMQAYiAxICiYFFAKKgUWA4vkxgojgpGwqMiEaBY7QvQADX4ADMEAAmGAADFAAB/oGmQFAQMBAcDBAICQUFAwLBwYEQBOqWNwAN4AOAAOIAOQAOYAOgAXIAJmAhOHoEKEBgYYQaEgmsgFaBaJaRaZaiaqaza7bFs1tQ223G3U7q3m4S4C3w768K4g5y4w5E5W5g6A6S6o607G7YaIkpqTKLjAOtUSoBBRAowUgKUFMBBFwT1Nk+WbZiEbLIfp+GQllbAW4CRmMU0gQ6HxCmpJeixC2L1ToVELAITMKIBIkdqqqygYyw5Mk7xFAcryBWODzyWMDIAAFUzxDdBCEAAtCgAWhgAJQ4AEogAB1aAA6JAAVFAAGiwAHRgACo0AA1cABZPhLKqDFYLotj2Z4sgwRwwDOZJYF2BwpioWhjisDQViGIo1hcTwkhCfxLEGSJdF4RAgEgoFg0HBAIhIKBULBgMhoOB0PCAQiIRiQSiYTigUiwWi4XjAar4GBgrGI0L6sYAGXC6XmEBioZDNiAB2AH6AinAkMRkOlbHp0PEjRWeJq83vDpHjAId1xBlrEIL18/gGzx8MJo53dSvZWZnFNnVsXwpwoB4RDIZCVLY1z4RP4AsgCCgbUKI8EQyFMdCVLY1z4RlOlbXxnW+d88gZSKaiex7g9ct8isEbzDwgxSSjD0lmGnHoaXwJAiDW3EFmnIIprstuv1PQAfIA9QB9AD2AH2AA"
        settings_dict = decrypt_settings_string_enum(self.settings_string)
        settings_dict["seed"] = random.randint(0, 100000000)  # Can be fixed if you want to test a specific seed repeatedly

        # Plando testing - fill the data with a json string
        # settings_dict["enable_plandomizer"] = True
        # settings_dict["plandomizer_data"] = json.loads('{"plando_starting_exit": -1, "plando_starting_kongs_selected": [-1], "plando_kong_rescue_diddy": -1, "plando_kong_rescue_lanky": -1, "plando_kong_rescue_tiny": -1, "plando_kong_rescue_chunky": -1, "plando_level_order_0": -1, "plando_level_order_1": -1, "plando_level_order_2": -1, "plando_level_order_3": -1, "plando_level_order_4": -1, "plando_level_order_5": -1, "plando_level_order_6": -1, "plando_level_order_7": -1, "plando_krool_order_0": -1, "plando_krool_order_1": -1, "plando_krool_order_2": -1, "plando_helm_order_0": -1, "plando_helm_order_1": -1, "plando_place_fairies": false, "plando_place_arenas": false, "plando_place_patches": false, "plando_place_kasplats": false, "plando_place_crates": false, "plando_place_wrinkly": false, "plando_place_tns": false, "locations": {"156": 18}, "prices": {}, "plando_bonus_barrels": {"156": 60}, "plando_switchsanity": {}, "plando_battle_arenas": {}, "plando_dirt_patches": [], "plando_fairies": [], "plando_kasplats": {}, "plando_melon_crates": [], "plando_wrinkly_doors": {}, "plando_tns_portals": {}, "hints": {}}')

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
