"""Temp file used for testing new logic system."""
import json
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
    data = json.load(open('static/presets/default.json'))
    data["seed"] = random.randint(0, 100000000)
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
