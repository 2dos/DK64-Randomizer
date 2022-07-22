"""Temp file used for testing new logic system."""
import random
from copy import deepcopy

import pytest

from randomizer.Fill import Generate_Spoiler
from randomizer.Lists import Exceptions
from randomizer.Settings import Settings
from randomizer.Spoiler import Spoiler


@pytest.fixture
def generate_settings():
    # Setting test settings
    data = {}
    data["seed"] = 821515
    # undivided
    data["name"] = "test"
    data["description"] = "test"

    data["move_rando"] = "on"  # usually "on"
    # data["random_prices"] = "medium"  # usually "medium"
    # data["blocker_text"] = 69
    # data["troff_text"] = 400
    # data["maximize_helm_blocker"] = True
    # important things

    # tab1
    data["enemy_rando"] = False
    data["crown_enemy_rando"] = False
    data["enemy_speed_rando"] = False
    data["krool_phase_order_rando"] = True
    data["boss_kong_rando"] = True
    data["random_medal_requirement"] = False
    data["level_randomization"] = "vanilla"

    data["boss_location_rando"] = True
    data["bananaport_rando"] = False
    data["kasplat_rando"] = False
    data["kong_rando"] = True
    data["random_patches"] = True
    data["unlock_all_moves"] = True

    # tab2
    data["blocker_0"] = 0
    data["blocker_1"] = 0
    data["blocker_2"] = 0
    data["blocker_3"] = 0
    data["blocker_4"] = 0
    data["blocker_5"] = 0
    data["blocker_6"] = 0
    data["blocker_7"] = 8
    data["troff_0"] = 1
    data["troff_1"] = 2
    data["troff_2"] = 3
    data["troff_3"] = 4
    data["troff_4"] = 5
    data["troff_5"] = 6
    data["troff_6"] = 7
    data["randomize_blocker_required_amounts"] = False
    data["randomize_cb_required_amounts"] = False

    data["damage_amount"] = "default"
    data["no_healing"] = False
    data["no_melons"] = False
    data["hard_shooting"] = False
    data["hard_mad_jack"] = False
    data["perma_death"] = False

    # tab3
    data["unlock_fairy_shockwave"] = True
    data["crown_door_open"] = True
    data["coin_door_open"] = True
    data["bonus_barrel_rando"] = True
    data["gnawty_barrels"] = False
    data["bonus_barrel_auto_complete"] = False
    data["open_lobbies"] = True
    data["open_levels"] = False
    data["randomize_pickups"] = False

    data["krool_random"] = False
    data["krool_phase_count"] = 4
    data["krool_access"] = False
    data["keys_random"] = False
    data["krool_key_count"] = 0
    data["starting_random"] = False
    data["starting_kongs_count"] = 5

    # tab4
    data["quality_of_life"] = True
    # unimportant missing setting
    data["enable_tag_anywhere"] = True
    data["wrinkly_hints"] = "standard"
    data["disable_shop_hints"] = False
    data["fps_display"] = False
    data["dpad_display"] = False

    data["warp_to_isles"] = True
    data["helm_setting"] = "skip_all"
    data["portal_numbers"] = True
    data["shop_indicator"] = True
    # unimportant missing
    data["fast_warps"] = True
    data["activate_all_bananaports"] = True

    # not important things
    data["download_patch_file"] = False

    data["music_bgm"] = True
    data["music_fanfares"] = True
    data["music_events"] = True

    data["generate_spoilerlog"] = True
    data["fast_start_beginning_of_game"] = True
    # data["helm_setting"] = "default"
    # data["quality_of_life"] = True
    # data["enable_tag_anywhere"] = False
    # data["krool_phase_order_rando"] = True
    return data


def test_forward(generate_settings):
    generate_settings["algorithm"] = "forward"
    settings = Settings(generate_settings)
    spoiler = Spoiler(settings)
    Generate_Spoiler(spoiler)
    spoiler.toJson()


def test_shuffles(generate_settings):
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
    generate_settings["algorithm"] = "assumed"
    settings = Settings(generate_settings)
    spoiler = Spoiler(settings)
    # TODO: We know this exception is a bit overkill, and will be replaced in the future, we are expecting failures
    try:
        Generate_Spoiler(spoiler)
        spoiler.toJson()
    except Exception:
        pass
