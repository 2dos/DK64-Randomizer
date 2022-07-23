"""Temp file used for testing new logic system."""
import random
from copy import deepcopy

import pytest

import randomizer.Lists.Exceptions as Ex
from randomizer.Fill import Generate_Spoiler  # , Generate_Spoiler_pass_or_crash
from randomizer.Lists import Exceptions
from randomizer.Logic import LogicVariables
from randomizer.Settings import Settings
from randomizer.Spoiler import Spoiler


@pytest.fixture
def generate_lo_rando_race_settings():
    """Asdf."""
    # Setting test settings
    data = {}
    data["seed"] = random.randint(0, 100000000)

    data["name"] = "Level Order Rando Race"
    data["description"] = "Preset for racing DK64 Level Order Randomizer"
    data["fast_start_beginning_of_game"] = True
    data["enemy_rando"] = True
    data["crown_enemy_rando"] = True
    data["enemy_speed_rando"] = True
    data["krool_phase_order_rando"] = True
    data["boss_kong_rando"] = True
    data["boss_location_rando"] = True
    data["random_medal_requirement"] = False
    data["bananaport_rando"] = False
    data["kasplat_rando"] = True
    data["kong_rando"] = True
    data["move_rando"] = "on"  # usually "on"
    data["random_prices"] = "medium"  # usually "medium"
    data["randomize_blocker_required_amounts"] = True
    data["randomize_cb_required_amounts"] = True
    data["blocker_text"] = 69
    data["troff_text"] = 400
    data["level_randomization"] = "level_order"  # usually "level_order"
    data["maximize_helm_blocker"] = True
    data["damage_amount"] = "default"
    data["no_healing"] = False
    data["no_melons"] = False
    data["hard_shooting"] = False
    data["hard_mad_jack"] = False
    data["perma_death"] = False
    data["unlock_fairy_shockwave"] = False
    data["crown_door_open"] = True
    data["coin_door_open"] = True
    data["bonus_barrel_rando"] = True
    data["gnawty_barrels"] = False
    data["bonus_barrel_auto_complete"] = False
    data["open_lobbies"] = False
    data["open_levels"] = False
    data["randomize_pickups"] = False
    data["krool_random"] = False
    data["krool_phase_count"] = 3
    data["krool_access"] = True
    data["keys_random"] = False
    data["krool_key_count"] = 4
    data["starting_random"] = False
    data["starting_kongs_count"] = 1  # usually 2
    data["quality_of_life"] = True
    data["enable_tag_anywhere"] = True
    data["wrinkly_hints"] = "standard"
    data["disable_shop_hints"] = False
    data["warp_to_isles"] = True
    data["helm_setting"] = "skip_start"
    data["portal_numbers"] = True
    data["shop_indicator"] = True
    data["puzzle_rando"] = True
    data["fast_gbs"] = True

    # data["no_logic"] = True  # CURSED - DO NOT DO LOGIC TESTING WITH THIS GUY HERE

    return data


@pytest.fixture
def generate_2dos_special_settings():
    """Asdf."""
    # Setting test settings
    data = {}
    data["seed"] = random.randint(0, 100000000)

    data["name"] = "The 2dos Special"
    data["description"] = "Coupled LZR with 2dos's preferred settings."
    data["fast_start_beginning_of_game"] = True
    data["enemy_rando"] = True
    data["crown_enemy_rando"] = True
    data["enemy_speed_rando"] = True
    data["krool_phase_order_rando"] = True
    data["boss_kong_rando"] = True
    data["boss_location_rando"] = True
    data["random_medal_requirement"] = False
    data["bananaport_rando"] = False
    data["kasplat_rando"] = True
    data["kong_rando"] = True
    data["move_rando"] = "on"
    data["random_prices"] = "medium"
    data["level_randomization"] = "loadingzone"
    data["randomize_blocker_required_amounts"] = False
    data["randomize_cb_required_amounts"] = True
    data["troff_text"] = 150
    data["blocker_0"] = 0
    data["blocker_1"] = 0
    data["blocker_2"] = 0
    data["blocker_3"] = 0
    data["blocker_4"] = 0
    data["blocker_5"] = 0
    data["blocker_6"] = 0
    data["blocker_7"] = 50
    data["damage_amount"] = "double"
    data["no_healing"] = True
    data["no_melons"] = True
    data["hard_shooting"] = True
    data["hard_mad_jack"] = True
    data["perma_death"] = False
    data["disable_tag_barrels"] = True
    data["unlock_fairy_shockwave"] = False
    data["crown_door_open"] = True
    data["coin_door_open"] = True
    data["bonus_barrel_rando"] = True
    data["gnawty_barrels"] = False
    data["bonus_barrel_auto_complete"] = False
    data["open_lobbies"] = True
    data["open_levels"] = False
    data["krool_random"] = False
    data["krool_phase_count"] = 3
    data["krool_access"] = True
    data["keys_random"] = False
    data["krool_key_count"] = 5
    data["starting_random"] = False
    data["starting_kongs_count"] = 2
    data["quality_of_life"] = True
    data["enable_tag_anywhere"] = True
    data["wrinkly_hints"] = "standard"
    data["disable_shop_hints"] = False
    data["warp_to_isles"] = True
    data["helm_setting"] = "skip_all"
    data["portal_numbers"] = True
    data["shop_indicator"] = True
    return data


@pytest.fixture
def the_miracle_settings():
    """Asdf."""
    # Setting test settings
    data = {}
    data["seed"] = 681570
    return data


@pytest.fixture
def generate_settings():
    """Asdf."""
    # Setting test settings
    data = {}
    data["seed"] = random.randint(0, 100000000)
    # important things
    data["blocker_0"] = 0
    data["blocker_1"] = 0
    data["blocker_2"] = 0
    data["blocker_3"] = 0
    data["blocker_4"] = 0
    data["blocker_5"] = 0
    data["blocker_6"] = 1
    data["blocker_7"] = 50
    data["troff_0"] = 100
    data["troff_1"] = 100
    data["troff_2"] = 100
    data["troff_3"] = 100
    data["troff_4"] = 100
    data["troff_5"] = 100
    data["troff_6"] = 100

    data["unlock_all_moves"] = False
    data["kasplat_rando"] = True
    data["starting_kongs_count"] = 1
    data["crown_door_open"] = False
    data["coin_door_open"] = False
    data["unlock_fairy_shockwave"] = False
    data["krool_phase_count"] = 4
    data["random_prices"] = "low"
    data["move_rando"] = "on"  # vanilla does not work right now, must be "on"/"on_shared"/"start_with"

    data["kong_rando"] = True

    # not important things
    data["download_patch_file"] = True

    data["music_bgm"] = True
    data["music_fanfares"] = True
    data["music_events"] = True

    data["generate_spoilerlog"] = True
    data["fast_start_beginning_of_game"] = False
    data["helm_setting"] = "default"
    data["quality_of_life"] = True
    data["enable_tag_anywhere"] = False
    data["krool_phase_order_rando"] = True
    return data


def test_forward(generate_settings):
    """Asdf."""
    generate_settings["algorithm"] = "forward"
    settings = Settings(generate_settings)
    settings.shuffle_loading_zones = "all"
    settings.decoupled_loading_zones = False
    spoiler = Spoiler(settings)
    Generate_Spoiler(spoiler)
    print(spoiler)
    print(spoiler.toJson())
    asdf = 1 / 0
    print(asdf)
    raise Exception


def test_forward_lo_race(generate_lo_rando_race_settings):
    """Asdf."""
    generate_lo_rando_race_settings["algorithm"] = "forward"
    settings = Settings(generate_lo_rando_race_settings)
    spoiler = Spoiler(settings)
    Generate_Spoiler(spoiler)
    print(spoiler)
    print(spoiler.toJson())
    asdf = 1 / 0
    print(asdf)
    raise Exception


def test_2dos_special(generate_2dos_special_settings):
    """Asdf."""
    generate_2dos_special_settings["algorithm"] = "forward"
    settings = Settings(generate_2dos_special_settings)
    spoiler = Spoiler(settings)
    Generate_Spoiler(spoiler)
    print(spoiler)
    print(spoiler.toJson())
    asdf = 1 / 0
    print(asdf)
    raise Exception


def test_shuffles(generate_settings):
    """Asdf."""
    generate_settings["algorithm"] = "forward"
    settings = Settings(generate_settings)
    duped = deepcopy(settings)
    duped.training_barrels = True
    duped.unlock_all_moves = True
    duped.starting_kongs_count = 5
    duped.unlock_fairy_shockwave = True
    duped.shuffle_items = "moves"
    duped.shuffle_loading_zones = "all"
    duped.decoupled_loading_zones = True
    spoiler = Spoiler(duped)
    # TODO: We know this exception is a bit overkill, and will be replaced in the future, we are expecting failures
    try:
        Generate_Spoiler(spoiler)
        spoiler.toJson()
    except Exception:
        pass


def test_assumed(generate_settings):
    """Asdf."""
    generate_settings["algorithm"] = "assumed"
    settings = Settings(generate_settings)
    spoiler = Spoiler(settings)
    # TODO: We know this exception is a bit overkill, and will be replaced in the future, we are expecting failures
    try:
        Generate_Spoiler(spoiler)
        spoiler.toJson()
    except Exception:
        pass


def test_level_shuffle_bias(generate_settings):
    """Asdf."""
    generate_settings["algorithm"] = "forward"

    successes = 0
    failures = 0
    crashes = 0
    for i in range(100):
        try:
            generate_settings["seed"] = random.randint(0, 100000000)
            settings = Settings(generate_settings)
            settings.shuffle_loading_zones = "levels"
            settings.decoupled_loading_zones = False
            spoiler = Spoiler(settings)
            yay = True  # Generate_Spoiler_pass_or_crash(spoiler)
            if yay:
                successes += 1
            else:
                failures += 1
        except Exception:
            crashes += 1
    print(successes)
    print(failures)
    print(crashes)


# doesn't work because something about restarting seed gen not properly clearing every variable (don't know who the offenders are though)
def test_indefinite_shuffling(generate_lo_rando_race_settings):
    """*Using LO Race preset."""
    successes = 0
    codeCrashes = 0
    whatthefuckcrashes = 0
    fillCrashes = 0
    kongPlacementCrashes = 0
    itemPlacementCrashes = 0
    coinLogicCrashes = 0
    whatthefuckcrasheslevelorders = []

    for i in range(100):
        try:
            settingsTemplate = deepcopy(generate_lo_rando_race_settings)
            settingsTemplate["seed"] = random.randint(0, 100000000)
            settingsTemplate["algorithm"] = "forward"
            settings = Settings(settingsTemplate)
            spoiler = Spoiler(settings)
            asdf = spoiler.toJson()
            Generate_Spoiler(spoiler)
            successes += 1

        except Ex.GameNotBeatableException as ex:
            print(settings)
            coinLogicCrashes += 1
            fillCrashes += 1
        except Ex.ItemPlacementException as ex:
            print(settings)
            if "kong" in ex.args[0]:
                kongPlacementCrashes += 1
            itemPlacementCrashes += 1
            fillCrashes += 1
        except Ex.FillException as ex:
            print(settings)
            fillCrashes += 1
        except Ex.KasplatPlacementException as ex:
            print(settings)
            # whatthefuckcrasheslevelorders.append(settings.level_order)
            whatthefuckcrashes += 1
        except Exception as ex:
            codeCrashes += 1
    asdf = 1 / 0
    print(asdf)
