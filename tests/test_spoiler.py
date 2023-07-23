"""Temp file used for testing new logic system."""
import json
import random

import pytest

# from randomizer.Enums.Items import Items
import randomizer.Lists.Exceptions as Ex
from randomizer.Enums.Settings import (ActivateAllBananaports, BananaportRando,
                                       CrownEnemyRando, DamageAmount,
                                       FillAlgorithm, FreeTradeSetting,
                                       HelmDoorItem, HelmSetting,
                                       KasplatRandoSetting, KrushaUi,
                                       LevelRandomization, LogicType,
                                       MicrohintsEnabled, MoveRando,
                                       RandomPrices, SettingsMap,
                                       ShockwaveStatus, TrainingBarrels,
                                       WinCondition, WrinklyHints)
from randomizer.Fill import Generate_Spoiler
from randomizer.Settings import Settings
from randomizer.SettingStrings import decrypt_settings_string_enum
from randomizer.Spoiler import Spoiler


@pytest.fixture
def generate_lo_rando_race_settings():
    """Generate a data dictionary that mimics what the front end passes to the shuffler."""
    # PLEASE NOTE: THIS LIST OF SETTINGS IS NOT COMPREHENSIVE - use the comments as quick references, not the entire story
    # You may have to add new options as you add them or as they get added

    data = {}
    data["seed"] = random.randint(0, 100000000)  # Can be fixed if you want to test a specific seed repeatedly
    data["settings_string"] = "Vy6IURioqPw+QRGkV6mTCIW6nrGmoBFCkNQX8EoAycRkF1ls0FAXUAgwE7AIHA3cBhAI8AQJBXkChQM9AYLB3sDhgQow0ofJYpnqUtoolsvaTSocWKiLAImIoAr9sjsctd+kcDwKZKorsbokmtoSQZgQRzQgYM5kBxbLQCFxvLBZFgpLgaFAtFYqMJNGJHNJGOSAEgeAFUAfQBWAA"

    # Randomizers
    # Major Items
    data["shuffle_items"] = False  # Must be true to trigger the list selector below
    # data["item_rando_list_selected"] = ["shop", "banana", "toughbanana", "crown", "blueprint", "key", "medal", "coin", "kong", "fairy", "rainbowcoin", "beanpearl", "fakeitem", "junkitem"]  # all options
    data["move_rando"] = MoveRando.on  # usually "on" but i like "cross_purchase", rarely need to test with "start_with"
    # if start_with, training barrels and "camera and shockwave" are FORCED to be normal and vanilla respectively
    data["training_barrels"] = TrainingBarrels.normal  # usually "normal", could be "shuffled"
    data["starting_moves_count"] = 4  # 0-40

    # Shuffled Locations
    data["random_patches"] = True  # usually False
    data["cb_rando"] = False  # likely to be False?
    data["coin_rando"] = False
    data["random_fairies"] = False  # likely to be False
    data["wrinkly_location_rando"] = False  # likely to be False
    data["tns_location_rando"] = False  # likely to be False
    data["vanilla_door_rando"] = False  # unclear, likely prefer True? easier to debug when False
    data["crown_placement_rando"] = False  # usually false
    data["kasplat_rando_setting"] = KasplatRandoSetting.vanilla_locations  # usually vanilla_locations but i like location_shuffle, RARELY set to off

    # Global
    data["enemy_rando"] = True
    data["bonus_barrel_rando"] = True
    data["enemy_speed_rando"] = True
    data["boss_location_rando"] = True  # usually True
    data["kong_rando"] = True  # usually True - FORCED True if level_order shuffle
    data["puzzle_rando"] = True
    data["krool_phase_order_rando"] = True  # usually True
    data["helm_phase_order_rando"] = True
    data["boss_kong_rando"] = True  # usually True
    data["randomize_pickups"] = False
    data["shuffle_shops"] = True  # usually False
    data["random_starting_region"] = False  # likely to be False

    data["level_randomization"] = LevelRandomization.vanilla  # usually "level_order" may need to test with "loadingzone" or "loadingzonesdecoupled"
    data["random_prices"] = RandomPrices.low  # usually "medium, might need free, rarely vanilla"
    # If shuffle_items is true, shockwave_status is always shuffled_decoupled, vanilla, or start_with
    data["shockwave_status"] = ShockwaveStatus.vanilla  # usually "vanilla", could be "shuffled" or "shuffled_decoupled" or "start_with"
    data["bananaport_rando"] = BananaportRando.in_level  # usually "off", could be "in_level" "crossmap_coupled" "crossmap_decoupled"

    # Overworld
    # Global Settings
    data["bonus_barrel_auto_complete"] = False  # usually False
    data["open_lobbies"] = False
    data["open_levels"] = False  # usually False
    data["alter_switch_allocation"] = False  # likely to be True, easier to test things when false
    data["high_req"] = True  # usually True
    data["fast_gbs"] = True  # usually True
    data["helm_hurry"] = False
    data["smaller_shops"] = False  # likely to be True in item rando, many settings force it to be false

    data["logic_type"] = LogicType.glitchless  # "glitchless", "glitch", "nologic"
    data["glitches_selected"] = []
    # glitch options:
    # "advanced_platforming", "b_locker_skips", "general_clips", "ledge_clips", "moonkicks", "phase_swimming", "phase_walking", "skew", "spawn_snags", "swim_through_shores", "tag_barrel_storage", "troff_n_scoff_skips"
    data["win_condition"] = WinCondition.beat_krool  # lots of options: all_keys | get_key8 | beat_krool | all_medals | all_fairies | all_blueprints | poke_snap
    data["free_trade_setting"] = FreeTradeSetting.none  # none | not_blueprints | major_collectibles
    data["activate_all_bananaports"] = ActivateAllBananaports.isles  # usually isles, could be all or off
    data["krusha_ui"] = KrushaUi.dk

    # Difficulty
    data["no_healing"] = False
    data["no_melons"] = False
    data["hard_shooting"] = False
    data["hard_bosses"] = False
    data["perma_death"] = False
    data["disable_tag_barrels"] = False
    data["hard_blockers"] = False  # likely to be False
    data["hard_troff_n_scoff"] = False  # likely to be False
    data["hard_level_progression"] = False  # likely to be False
    data["hard_enemies"] = False

    data["damage_amount"] = DamageAmount.default
    data["crown_enemy_rando"] = CrownEnemyRando.easy

    # Progression
    # Level Requirements
    data["randomize_blocker_required_amounts"] = True  # usually True, if false set values below
    data["blocker_0"] = 1
    data["blocker_1"] = 2
    data["blocker_2"] = 3
    data["blocker_3"] = 4
    data["blocker_4"] = 5
    data["blocker_5"] = 6
    data["blocker_6"] = 7
    data["blocker_7"] = 8
    data["blocker_text"] = 40  # usually 69
    data["maximize_helm_blocker"] = True  # usually True

    data["randomize_cb_required_amounts"] = True  # usually True, if false set values below
    data["troff_0"] = 1
    data["troff_1"] = 2
    data["troff_2"] = 3
    data["troff_3"] = 4
    data["troff_4"] = 5
    data["troff_5"] = 6
    data["troff_6"] = 7
    data["troff_text"] = 300  # usually 400?

    # Banana Medal/Fairy Requirements
    data["medal_requirement"] = 15  # vanilla is 15
    data["medal_cb_req"] = 75  # vanilla is 75
    data["rareware_gb_fairies"] = 20

    data["fast_start_beginning_of_game"] = True
    data["random_medal_requirement"] = False

    # Game Length Settings
    data["krool_random"] = False  # "phase count is random" setting
    data["krool_phase_count"] = 3  # usually 3
    data["helm_random"] = False  # "room count is random" setting
    data["helm_phase_count"] = 3  # usually 3
    data["keys_random"] = False  # "key count is random" setting
    data["select_keys"] = False  # usually False, if True use below
    # data["starting_keys_list_selected"] = [Items.JungleJapesKey]  # JungleJapesKey, AngryAztecKey, etc.
    data["key_8_helm"] = False  # likely to be True in most settings
    data["krool_access"] = True  # usually True - this is the weirdly named key 8 required setting
    data["krool_key_count"] = 8  # usually 5
    data["starting_random"] = False  # "starting kong count is random" setting
    data["starting_kongs_count"] = 3  # usually 2

    data["crown_door_item"] = HelmDoorItem.opened  # opened | random | specify the item: req_xxx
    data["crown_door_item_count"] = 1  # no need to specify when random
    data["coin_door_item"] = HelmDoorItem.opened  # opened | random | specify the item: req_xxx
    data["coin_door_item_count"] = 1  # no need to specify when random

    # QoL
    # Gameplay
    data["quality_of_life"] = True
    data["misc_changes_selected"] = []  # a whole suite of things it includes
    data["shorten_boss"] = True
    data["enable_tag_anywhere"] = True
    data["enable_shop_hints"] = True
    data["shop_indicator"] = True
    data["wrinkly_available"] = False
    data["warp_to_isles"] = True
    data["fast_warps"] = True
    data["auto_keys"] = True

    data["wrinkly_hints"] = WrinklyHints.standard
    data["helm_setting"] = HelmSetting.skip_start
    data["microhints_enabled"] = MicrohintsEnabled.base  # off/base/all

    # Other
    data["fps_display"] = False
    data["portal_numbers"] = True
    data["item_reward_previews"] = True

    return data


@pytest.fixture
def generate_settings():
    """Asdf."""
    # Setting test settings
    data = json.load(open("static/presets/default.json"))
    data["seed"] = random.randint(0, 100000000)
    # Convert to enums
    for k, v in data.items():
        if k in SettingsMap:
            if type(v) is list:
                values = []
                for val in v:
                    values.append(SettingsMap[k][val])
                data[k] = values
            else:
                data[k] = SettingsMap[k][v]
    return data


# def test_manual_settings_dict(generate_lo_rando_race_settings):
#     """Asdf."""
#     generate_lo_rando_race_settings["algorithm"] = FillAlgorithm.forward
#     settings = Settings(generate_lo_rando_race_settings)
#     spoiler = Spoiler(settings)
#     Generate_Spoiler(spoiler)
#     print(spoiler)
#     print(spoiler.json)
#     print("all done")


def test_with_settings_string_1():
    """Confirm that settings strings decryption is working and generate a spoiler log with it."""
    # INPUT YOUR SETTINGS STRING OF CHOICE HERE:
    # This top one is always the S2 Preset (probably up to date, if it isn't go steal it from the season2.json)
    settings_string = "bKEFiRorPN5ysnPCBogPQ+qBoRDIhKlsa58B+I0eu0uXxCnLE2nBACoMgt1PX4EkAyaBkF1kssFAXQAgwE6gIHA3YBhAI7gQJBXgChQM8gYLB3oDhgQoQ08e2QpHqKhnKlMubRbwM0NjlFuCFRFgMTEUDF61xyN2q/32RQPAZiqcuUOS2EJIIvoE5IMMGY2mMHFosi0rlgVigthoTiwVCkwEwYEYkHERh0AVQA"
    # This one is for ease of testing, go wild with it
    # nasty lzr settings_string = "bKEHCRorPE1ebysnPCAMMSwVfwNywcYokPR0ixgENxBlrEIL18/gGzx8MJo53dSvZWZnFNnVsXwpwPqggEQyFMdCVLY1z4D8Ro9dpcviFmttjp0xRpgSfAoHJhQaHjBIV3AiT1+BIAImhXlMZRcZLLBQF0AIMBOoCBwN2AYQCO4ECQV4AoUDPIGCwd6A4YEBrw95BgqR6jLZ6JVLqkw4EVIWARMhQBXqqGiGQpkqWxrp2HLVfZFgExFOI65Q5LDi0WQEQRALTcWBWKC2GhOLBUUCYMCMaCKSDiaw2fwG"
    # nasty no lzr settings_string = "bKEHCRorPE1ebysnPCAMMSwVfwNywcYokPR0ixgENxBlrEIL18/gGzx8MJo53dSvZWZnFNnVsXwpwPqggEQyFMdCVLY1z4D8Ro9dpcviFmttjpyxRpgSfAoHJhQaHjBIV3AiT1+BIAImhXlMZRcZLLBQF0AIMBOoCBwN2AYQCO4ECQV4AoUDPIGCwd6A4YEBrw95BgqR6jLZ6JVLqkw4EVIWARMhQBXqqGiGQpkqWxrp2HLVfZFgExFOI65Q5LDi0WQEQRALTcWBWKC2GhOLBUUCYMCMaCKSDiaw2fwG"

    settings_dict = decrypt_settings_string_enum(settings_string)
    settings_dict["seed"] = random.randint(0, 100000000)  # Can be fixed if you want to test a specific seed repeatedly
    settings = Settings(settings_dict)
    # settings.extreme_debugging = True  # Greatly slows seed gen, use with caution
    spoiler = Spoiler(settings)
    Generate_Spoiler(spoiler)
    print(spoiler)
    print(spoiler.json)
    # printHintDistribution(spoiler)
    with open("test-result-1.json", "w") as outfile:
        outfile.write(spoiler.json)
    print("test 1 done")


def test_with_settings_string_2():
    """Confirm that settings strings decryption is working and generate a spoiler log with it."""
    # INPUT YOUR SETTINGS STRING OF CHOICE HERE:
    # non-item rando seed
    settings_string = "Vi5oQVEE4Yi0gIJ+/AkAETQMguAoC6DwGBXU8A4e7MgIHnd9BJk8SwKQXmvBag9ZAMZFCGnj2yFI9Rls9Eql1SKSjgRUBYEEwFAJejlqvsigeADEUxcktsMISQRfQJyQYYDwPD4RI5dJYvCBmNpjBxaLICIIgFpuK5YFYoLYaE4sFQpMhlMBMGBGNBFOJrDZ/EZDKoA"

    settings_dict = decrypt_settings_string_enum(settings_string)
    settings_dict["seed"] = random.randint(0, 100000000)  # Can be fixed if you want to test a specific seed repeatedly
    settings = Settings(settings_dict)
    spoiler = Spoiler(settings)
    Generate_Spoiler(spoiler)
    # print(spoiler)
    # print(spoiler.json)
    # printHintDistribution(spoiler)
    with open("test-result-2.json", "w") as outfile:
        outfile.write(spoiler.json)
    print("test 2 done")


def test_with_settings_string_3():
    """Confirm that settings strings decryption is working and generate a spoiler log with it."""
    # INPUT YOUR SETTINGS STRING OF CHOICE HERE:
    # S2
    settings_string = "bKEFiRorPN5ysnPCBogPQ+qBoRDIhKlsa58B+I0eu0uXxCnLE2nBACoMgt1PX4EkAyaBkF1kssFAXQAgwE6gIHA3YBhAI7gQJBXgChQM8gYLB3oDhgQoQ08e2QpHqKhnKlMubRbwM0NjlFuCFRFgMTEUDF61xyN2q/32RQPAZiqcuUOS2EJIIvoE5IMMGY2mMHFosi0rlgVigthoTiwVCkwEwYEYkHERh0AVQA"

    settings_dict = decrypt_settings_string_enum(settings_string)
    settings_dict["seed"] = random.randint(0, 100000000)  # Can be fixed if you want to test a specific seed repeatedly
    settings = Settings(settings_dict)
    spoiler = Spoiler(settings)
    Generate_Spoiler(spoiler)
    # print(spoiler)
    # print(spoiler.json)
    # printHintDistribution(spoiler)
    with open("test-result-3.json", "w") as outfile:
        outfile.write(spoiler.json)
    print("test 3 done")


def test_with_settings_string_4():
    """Confirm that settings strings decryption is working and generate a spoiler log with it."""
    # INPUT YOUR SETTINGS STRING OF CHOICE HERE:
    # all location rando
    for i in range(1, 11):
        settings_string = "bKsnPCAMMSwVfwNyjFEh6H1QQCIZCmOhKlsa58B+I0eu0uXxCzW2x05Yi0wIB1arMCoMgp8TAIv2JIBk3FcolUZBeZLLBQF0AIMBOoCBwN2AYQCO4ECQV4AoUDPIGCwd6A4YEBqM9uFgqR6ioZ0JlKpc2i3gRqbotxuFFSFgQTIUAl6qigRDIUx0JUtjXPhGdbNccjdqv99kUDwCYqnLlDkuDFpuK5YLYaE4sFJQGBGJAjIQAOgA"

        settings_dict = decrypt_settings_string_enum(settings_string)
        settings_dict["seed"] = random.randint(0, 100000000)  # Can be fixed if you want to test a specific seed repeatedly
        settings = Settings(settings_dict)
        spoiler = Spoiler(settings)
        Generate_Spoiler(spoiler)
        # print(spoiler)
        # print(spoiler.json)
        # printHintDistribution(spoiler)
        with open("test-result-4." + str(i) + ".json", "w") as outfile:
            outfile.write(spoiler.json)
        print("test 4." + str(i) + " done")


def test_with_settings_string_5():
    """Confirm that settings strings decryption is working and generate a spoiler log with it."""
    # INPUT YOUR SETTINGS STRING OF CHOICE HERE:
    # no location rando
    settings_string = "bKsnPCBoiPQ+qCARDIUx0JUtjXPgPxGj12ly+IWa205Yi0wIB1arMCoMgp6/YkgGTcVyiVRkF5kssFAXQAgwE6gIHA3YBhAI7gQJBXgChQM8gYLB3oDhgQGoz24WCpHqKhnQlIubRbwI1N0W43CipCwIJkKAS9VRQIhkKY6EqWxrnwjOtmuORu1X++yKB4BMVTlyhyWwhJBF9AnJBhgxi03FcsFsNCcWCkoEwYEYkCMhAA6AA"

    settings_dict = decrypt_settings_string_enum(settings_string)
    settings_dict["seed"] = random.randint(0, 100000000)  # Can be fixed if you want to test a specific seed repeatedly
    settings = Settings(settings_dict)
    spoiler = Spoiler(settings)
    Generate_Spoiler(spoiler)
    # print(spoiler)
    # print(spoiler.json)
    # printHintDistribution(spoiler)
    with open("test-result-5.json", "w") as outfile:
        outfile.write(spoiler.json)
    print("test 5 done")


def test_with_settings_string_6():
    """Confirm that settings strings decryption is working and generate a spoiler log with it."""
    # INPUT YOUR SETTINGS STRING OF CHOICE HERE:
    # Kamerson's settings
    settings_string = "bKEGiRorPE1ecrJzwgDDEsFX7lGKJD0Pj8Ro9dpcviFmpyxRpgRArdT4mBxJFZ7fgSICJoV5XKJPLJVKYyi+yWWCgLoAQYCdQEDgbsAwgEdwIEgrwBQoGeQMFg70BwwIUIbkPf0UqFHIz0SqXVFpMOBFQFgoTAUAl6qgxTxnWzVgExFMXKHJcCgzaYwcWiyQRALSwWw0YCYMCMaCQcTWHA2fz6IgGIw6AKgA+AA"

    settings_dict = decrypt_settings_string_enum(settings_string)
    settings_dict["seed"] = random.randint(0, 100000000)  # Can be fixed if you want to test a specific seed repeatedly
    settings = Settings(settings_dict)
    spoiler = Spoiler(settings)
    Generate_Spoiler(spoiler)
    # print(spoiler)
    # print(spoiler.json)
    # printHintDistribution(spoiler)
    with open("test-result-6.json", "w") as outfile:
        outfile.write(spoiler.json)
    print("test 6 done")


def test_with_settings_string_7():
    """Confirm that settings strings decryption is working and generate a spoiler log with it."""
    # INPUT YOUR SETTINGS STRING OF CHOICE HERE:
    # VBB
    settings_string = "Vg5oShEE4Yg0gIJ+/AkAETQMguAoC6DwGBXU8A4e7MgIHnd9BJk8SwKQXmvBag9ZAMZFCGnj2yFI9Rls9Eql1SKTDgRUBYEEwFAJejlqvsigeADEUxcktsMISQRfQJyQYYDwPD4RI5dJYvCBmNpjBxaLICIIgFpuK5YFYoLYaE4sFQpMhlMBMGBGNBFOJrDZ/EZDKoA"

    settings_dict = decrypt_settings_string_enum(settings_string)
    settings_dict["seed"] = random.randint(0, 100000000)  # Can be fixed if you want to test a specific seed repeatedly
    settings = Settings(settings_dict)
    spoiler = Spoiler(settings)
    Generate_Spoiler(spoiler)
    # print(spoiler)
    # print(spoiler.json)
    # printHintDistribution(spoiler)
    with open("test-result-7.json", "w") as outfile:
        outfile.write(spoiler.json)
    print("test 7 done")


def test_with_settings_string_8():
    """Confirm that settings strings decryption is working and generate a spoiler log with it."""
    # INPUT YOUR SETTINGS STRING OF CHOICE HERE:
    # S2
    settings_string = "bKEFiRorPN5ysnPCBogPQ+qBoRDIhKlsa58B+I0eu0uXxCnLE2nBACoMgt1PX4EkAyaBkF1kssFAXQAgwE6gIHA3YBhAI7gQJBXgChQM8gYLB3oDhgQoQ08e2QpHqKhnKlMubRbwM0NjlFuCFRFgMTEUDF61xyN2q/32RQPAZiqcuUOS2EJIIvoE5IMMGY2mMHFosi0rlgVigthoTiwVCkwEwYEYkHERh0AVQA"

    settings_dict = decrypt_settings_string_enum(settings_string)
    settings_dict["seed"] = random.randint(0, 100000000)  # Can be fixed if you want to test a specific seed repeatedly
    settings = Settings(settings_dict)
    spoiler = Spoiler(settings)
    Generate_Spoiler(spoiler)
    # print(spoiler)
    # print(spoiler.json)
    # printHintDistribution(spoiler)
    with open("test-result-8.json", "w") as outfile:
        outfile.write(spoiler.json)
    print("test 8 done")


def printHintDistribution(spoiler: Spoiler):
    """Print the hint distribution for the given spoiler log."""
    types = ""
    values = ""
    for key, value in spoiler.hint_distribution.items():
        types += (key.name + ", ")
        values += (str(value) + ", ")
    print(types)
    print(values)
