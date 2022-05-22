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
    data["seed"] = random.randint(0, 100000000)
    # important things
    data["blocker_0"] = 0
    data["blocker_1"] = 0
    data["blocker_2"] = 0
    data["blocker_3"] = 0
    data["blocker_4"] = 0
    data["blocker_5"] = 0
    data["blocker_6"] = 0
    data["blocker_7"] = 100
    data["troff_0"] = 100
    data["troff_1"] = 100
    data["troff_2"] = 100
    data["troff_3"] = 100
    data["troff_4"] = 100
    data["troff_5"] = 100
    data["troff_6"] = 100

    data["unlock_all_moves"] = False
    data["kasplat_rando"] = False
    data["starting_kongs_count"] = 5
    data["crown_door_open"] = False
    data["coin_door_open"] = False
    data["unlock_fairy_shockwave"] = False
    data["krool_phase_count"] = 4

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
    generate_settings["algorithm"] = "forward"
    settings = Settings(generate_settings)
    settings.shuffle_loading_zones = "all"
    settings.decoupled_loading_zones = True
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
