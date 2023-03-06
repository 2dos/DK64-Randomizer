"""Temp file used for testing new logic system."""
import json
import random

import pytest

from randomizer.Enums.Settings import (
    SettingsMap,
    ActivateAllBananaports,
    BananaportRando,
    DamageAmount,
    FreeTradeSetting,
    HelmDoorItem,
    HelmSetting,
    KasplatRandoSetting,
    LevelRandomization,
    LogicType,
    MicrohintsEnabled,
    MoveRando,
    RandomPrices,
    ShockwaveStatus,
    TrainingBarrels,
    WinCondition,
    WrinklyHints,
    FillAlgorithm
)
# from randomizer.Enums.Items import Items
import randomizer.Lists.Exceptions as Ex
from randomizer.Fill import Generate_Spoiler
from randomizer.Settings import Settings
from randomizer.Spoiler import Spoiler


@pytest.fixture
def generate_lo_rando_race_settings():
    """Generate a data dictionary that mimics what the front end passes to the shuffler."""
    # PLEASE NOTE: THIS LIST OF SETTINGS IS NOT COMPREHENSIVE - use the comments as quick references, not the entire story
    # You may have to add new options as you add them or as they get added

    data = {}
    data["seed"] = random.randint(0, 100000000)  # Can be fixed if you want to test a specific seed repeatedly

    data["fast_start_beginning_of_game"] = True
    data["enemy_rando"] = True
    data["crown_enemy_rando"] = True
    data["enemy_speed_rando"] = True
    data["boss_kong_rando"] = True  # usually True
    data["boss_location_rando"] = True  # usually True
    data["random_medal_requirement"] = False
    data["medal_requirement"] = 15  # vanilla is 15
    data["medal_cb_req"] = 75  # vanilla is 75
    data["kasplat_rando_setting"] = KasplatRandoSetting.vanilla_locations  # usually vanilla_locations but i like location_shuffle, RARELY set to off
    data["kong_rando"] = True  # usually True - FORCED True if level_order shuffle

    data["bananaport_rando"] = BananaportRando.off  # usually "off", could be "in_level" "crossmap_coupled" "crossmap_decoupled"
    data["activate_all_bananaports"] = ActivateAllBananaports.isles  # usually isles, could be all or off

    # item shuffler options here
    data["move_rando"] = MoveRando.on  # usually "on" but i like "cross_purchase", rarely need to test with "start_with"
    # if start_with, next two are FORCED to be normal and vanilla
    data["training_barrels"] = TrainingBarrels.shuffled  # usually "normal", could be "shuffled"
    data["shockwave_status"] = ShockwaveStatus.shuffled_decoupled  # usually "vanilla", could be "shuffled" or "shuffled_decoupled" or "start_with"
    # If true, the above is always decoupled or vanilla
    data["shuffle_items"] = True  # Must be true to trigger the list selector below
    # data["item_rando_list_selected"] = ["shop", "banana", "toughbanana", "crown", "blueprint", "key", "medal", "coin", "kong", "fairy", "rainbowcoin", "beanpearl", "fakeitem", "junkitem"]  # all options

    data["random_prices"] = RandomPrices.low  # usually "medium, might need free, rarely vanilla"
    data["randomize_blocker_required_amounts"] = True  # usually True, if false set values below
    data["blocker_0"] = 0
    data["blocker_1"] = 0
    data["blocker_2"] = 0
    data["blocker_3"] = 0
    data["blocker_4"] = 0
    data["blocker_5"] = 0
    data["blocker_6"] = 0
    data["blocker_7"] = 50
    data["blocker_text"] = 69  # usually 69
    data["maximize_helm_blocker"] = True  # usually True

    data["randomize_cb_required_amounts"] = True  # usually True, if false set values below
    data["troff_0"] = 500
    data["troff_1"] = 500
    data["troff_2"] = 500
    data["troff_3"] = 500
    data["troff_4"] = 500
    data["troff_5"] = 500
    data["troff_6"] = 500
    data["troff_text"] = 400  # usually 400?

    data["level_randomization"] = LevelRandomization.level_order  # usually "level_order" may need to test with "loadingzone" or "loadingzonesdecoupled"

    data["damage_amount"] = DamageAmount.default
    data["no_healing"] = False
    data["no_melons"] = False
    data["hard_shooting"] = False
    # data["hard_mad_jack"] = False
    data["perma_death"] = False
    data["crown_door_item"] = HelmDoorItem.random  # opened | random | specify the item: req_xxx
    data["crown_door_item_count"] = 1  # no need to specify when random
    data["coin_door_item"] = HelmDoorItem.random  # opened | random | specify the item: req_xxx
    data["coin_door_item_count"] = 1  # no need to specify when random
    data["bonus_barrel_rando"] = True
    # data["gnawty_barrels"] = False
    data["bonus_barrel_auto_complete"] = False  # usually False
    data["open_lobbies"] = False
    data["open_levels"] = False  # usually False
    data["randomize_pickups"] = True

    data["krool_phase_order_rando"] = True  # usually True
    data["krool_random"] = False  # "phase count is random" setting
    data["krool_phase_count"] = 3  # usually 3
    data["helm_random"] = False  # "room count is random" setting
    data["helm_phase_count"] = 3  # usually 3
    data["krool_access"] = True  # usually True - this is the weirdly named key 8 required setting
    data["keys_random"] = False  # "key count is random" setting
    data["krool_key_count"] = 8  # usually 5
    data["select_keys"] = False  # usually False, if True use below
    # data["starting_keys_list_selected"] = [Items.JungleJapesKey]  # JungleJapesKey, AngryAztecKey, etc.
    data["starting_random"] = False  # "starting kong count is random" setting
    data["starting_kongs_count"] = 2  # usually 2

    data["quality_of_life"] = True
    data["enable_tag_anywhere"] = True
    data["wrinkly_hints"] = WrinklyHints.standard
    # data["disable_shop_hints"] = False
    data["warp_to_isles"] = True
    data["helm_setting"] = HelmSetting.skip_start
    data["portal_numbers"] = True
    data["shop_indicator"] = True
    data["puzzle_rando"] = True
    data["fast_gbs"] = True  # usually True
    data["high_req"] = True  # usually True
    data["random_patches"] = False  # usually False
    data["shuffle_shops"] = False  # usually False

    data["free_trade_setting"] = FreeTradeSetting.not_blueprints  # none | not_blueprints | major_collectibles
    data["crown_placement_rando"] = False  # usually false
    data["hard_blockers"] = False  # likely to be False
    data["hard_troff_n_scoff"] = False  # likely to be False
    data["cb_rando"] = True  # likely to be False?
    data["win_condition"] = WinCondition.beat_krool  # lots of options: all_keys | get_key8 | beat_krool | all_medals | all_fairies | all_blueprints | poke_snap
    data["wrinkly_location_rando"] = False  # likely to be False
    data["tns_location_rando"] = False  # likely to be False
    data["vanilla_door_rando"] = True  # unclear, likely prefer True? easier to debug when False
    data["key_8_helm"] = True  # likely to be True in most settings
    data["misc_changes_selected"] = []  # a whole suite of things it includes

    data["hard_level_progression"] = False  # likely to be False

    data["logic_type"] = LogicType.glitchless  # "glitchless", "glitch", "nologic"
    # glitch options:
    # "advanced_platforming", "b_locker_skips", "general_clips", "ledge_clips", "moonkicks", "phase_swimming", "phase_walking", "skew", "spawn_snags", "swim_through_shores", "tag_barrel_storage", "troff_n_scoff_skips"
    data["glitches_selected"] = []
    data["microhints_enabled"] = MicrohintsEnabled.all  # off/base/all
    data["smaller_shops"] = True  # likely to be True in item rando, many settings force it to be false
    data["alter_switch_allocation"] = False  # likely to be True, easier to test things when false
    data["random_starting_region"] = False  # likely to be False
    data["random_fairies"] = False  # likely to be False

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


def test_forward_fill(generate_lo_rando_race_settings):
    """Asdf."""
    generate_lo_rando_race_settings["algorithm"] = FillAlgorithm.forward
    settings = Settings(generate_lo_rando_race_settings)
    spoiler = Spoiler(settings)
    Generate_Spoiler(spoiler)
    print(spoiler)
    print(spoiler.json)
    asdf = 1 / 0
    print(asdf)
    raise Exception
