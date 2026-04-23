"""Fill settings module for DK64 randomizer.

This module contains all the settings configuration logic
that was previously in the generate_early method.
"""

from typing import Any
from random import Random

from BaseClasses import MultiWorld
from randomizer.Settings import Settings
from randomizer.Enums.Settings import (
    ActivateAllBananaports,
    BananaportRando,
    BLockerSetting,
    CBRequirement,
    CrownEnemyDifficulty,
    DamageAmount,
    DKPortalRando,
    ExtraCutsceneSkips,
    FasterChecksSelected,
    FungiTimeSetting,
    GalleonWaterSetting,
    GlitchesSelected,
    HardBossesSelected,
    HardModeSelected,
    HelmBonuses,
    HelmDoorItem,
    HelmSetting,
    ItemRandoFiller,
    ItemRandoListSelected,
    KasplatRandoSetting,
    KongModels,
    LevelRandomization,
    LogicType,
    MicrohintsEnabled,
    MinigamesListSelected,
    MiscChangesSelected,
    ProgressiveHintItem,
    PuzzleRando,
    RandomStartingRegion,
    RandomRequirement,
    RemovedBarriersSelected,
    ShufflePortLocations,
    SlamRequirement,
    SpoilerHints,
    SwitchsanityGone,
    SwitchsanityKong,
    TricksSelected,
    TroffSetting,
    WrinklyHints,
    KroolInBossPool,
)
from randomizer.Enums.Items import Items as DK64RItems
from randomizer.Enums.Types import Types
from randomizer.Enums.Maps import Maps
from randomizer.Enums.Enemies import Enemies
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.SwitchTypes import SwitchType
from randomizer.Enums.Switches import Switches
from randomizer.Lists.Switches import SwitchInfo
from archipelago.Options import (
    Goal,
    SwitchsanityOptions,
    SelectStartingKong,
    GalleonWaterLevel,
    KrushaRandom,
    KroolShuffle,
    DKPortalLocationRando,
    RandomStartingLocation,
    DK64Options,
)
from archipelago.Goals import GOAL_MAPPING, QUANTITY_GOALS, calculate_quantity
from archipelago.Logic import logic_item_name_to_id


def get_default_settings() -> dict[str, Any]:
    """Get the default settings dictionary."""
    return {
        "activate_all_bananaports": ActivateAllBananaports.isles,
        "alter_switch_allocation": True,
        "auto_keys": True,
        "bananaport_placement_rando": ShufflePortLocations.off,
        "bananaport_rando": BananaportRando.off,
        "blocker_0": 1,
        "blocker_1": 2,
        "blocker_2": 3,
        "blocker_3": 4,
        "blocker_4": 5,
        "blocker_5": 6,
        "blocker_6": 7,
        "blocker_7": 8,
        "blocker_selection_behavior": BLockerSetting.normal_random,
        "blocker_text": 60,
        "bosses_selected": [
            Maps.JapesBoss,
            Maps.AztecBoss,
            Maps.FactoryBoss,
            Maps.GalleonBoss,
            Maps.FungiBoss,
            Maps.CavesBoss,
            Maps.CastleBoss,
            Maps.KroolDonkeyPhase,
            Maps.KroolDiddyPhase,
            Maps.KroolLankyPhase,
            Maps.KroolTinyPhase,
            Maps.KroolChunkyPhase,
        ],
        "bonus_barrel_auto_complete": False,
        "boss_location_rando": True,
        "cannons_require_blast": True,
        "cb_medal_behavior_new": CBRequirement.pre_selected,
        "chunky_phase_slam_req": SlamRequirement.green,
        "coin_door_item": HelmDoorItem.opened,
        "coin_door_item_count": 1,
        "coin_rando": False,
        "crown_door_item": HelmDoorItem.opened,
        "crown_door_item_count": 1,
        "crown_enemy_difficulty": CrownEnemyDifficulty.easy,
        "damage_amount": DamageAmount.default,
        "decouple_item_rando": False,
        "dim_solved_hints": False,
        "disable_hard_minigames": True,
        "disable_racing_patches": False,
        "disable_tag_barrels": False,
        "dk_portal_location_rando_v2": DKPortalRando.off,
        "dos_door_rando": False,
        "enable_shop_hints": True,
        "enable_tag_anywhere": True,
        "enemies_selected": [],
        "enemy_kill_crown_timer": True,
        "enemy_speed_rando": False,
        "fairy_queen_behavior": RandomRequirement.pre_selected,
        "fast_start_beginning_of_game_dummy": False,
        "fast_warps": True,
        "faster_checks_selected": [
            FasterChecksSelected.factory_toy_monster_fight,
            FasterChecksSelected.factory_piano_game,
            FasterChecksSelected.factory_diddy_rnd,
            FasterChecksSelected.factory_arcade_round_1,
            FasterChecksSelected.factory_car_race,
            FasterChecksSelected.galleon_seal_race,
            FasterChecksSelected.galleon_mech_fish,
            FasterChecksSelected.forest_mill_conveyor,
            FasterChecksSelected.forest_owl_race,
            FasterChecksSelected.forest_rabbit_race,
            FasterChecksSelected.caves_ice_tomato_minigame,
            FasterChecksSelected.castle_minecart,
            FasterChecksSelected.castle_car_race,
            FasterChecksSelected.jetpac,
            FasterChecksSelected.arcade,
        ],
        "filler_items_selected": [ItemRandoFiller.junkitem],
        "free_trade_setting": True,
        "fungi_time": FungiTimeSetting.dusk,
        "generate_spoilerlog": True,
        "hard_bosses_selected": [],
        "hard_mode_selected": [],
        "has_password": False,
        "helm_hurry": False,
        "helm_phase_count": 2,
        "helm_phase_order_rando": True,
        "helm_random": False,
        "helm_room_bonus_count": HelmBonuses.zero,
        "helm_setting": HelmSetting.skip_start,
        "ice_trap_count": 10,
        "ice_traps_damage": False,
        "item_rando_list_0": [],
        "item_rando_list_1": [],
        "item_rando_list_2": [],
        "item_rando_list_3": [],
        "item_rando_list_4": [],
        "item_rando_list_5": [],
        "item_rando_list_6": [
            ItemRandoListSelected.wrinkly,
            ItemRandoListSelected.gauntletbanana,
            ItemRandoListSelected.racebanana,
            ItemRandoListSelected.sniderewards,
            ItemRandoListSelected.arenas,
            ItemRandoListSelected.halfmedal,
            ItemRandoListSelected.enemies,
            ItemRandoListSelected.boulderitem,
            ItemRandoListSelected.breakable,
            ItemRandoListSelected.balloon,
            ItemRandoListSelected.shop,
            ItemRandoListSelected.bfi_gift,
            ItemRandoListSelected.banana_checks,
            ItemRandoListSelected.jetpac,
            ItemRandoListSelected.kasplat,
            ItemRandoListSelected.bosses,
            ItemRandoListSelected.endofhelm,
            ItemRandoListSelected.medal_checks,
            ItemRandoListSelected.medal_checks_helm,
            ItemRandoListSelected.arcade,
            ItemRandoListSelected.fairy_checks,
            ItemRandoListSelected.dirt_patches,
            ItemRandoListSelected.clams,
            ItemRandoListSelected.anthillreward,
            ItemRandoListSelected.kong_cages,
            ItemRandoListSelected.crateitem,
            ItemRandoListSelected.trainingbarrels,
        ],
        "item_rando_list_7": [],
        "item_rando_list_8": [],
        "item_rando_list_9": [],
        "item_reward_previews": True,
        "k_rool_vanilla_requirement": False,
        "kasplat_rando_setting": KasplatRandoSetting.off,
        "key_8_helm": True,
        "keys_random": False,
        "kong_model_chunky": KongModels.default,
        "kong_model_diddy": KongModels.default,
        "kong_model_dk": KongModels.default,
        "kong_model_lanky": KongModels.default,
        "kong_model_tiny": KongModels.default,
        "krool_access": False,
        "krool_in_boss_pool": False,
        "krool_key_count": 0,
        "krool_phase_count": 3,
        "krool_phase_order_rando": True,
        "krool_random": False,
        "less_fragile_boulders": True,
        "logic_type": LogicType.glitchless,
        "maximize_helm_blocker": True,
        "medal_cb_req": 40,
        "medal_jetpac_behavior": RandomRequirement.pre_selected,
        "medal_requirement": 9,
        "mermaid_gb_pearls": 1,
        "microhints_enabled": MicrohintsEnabled.all,
        "mirror_mode": False,
        "misc_changes_selected": [
            MiscChangesSelected.auto_dance_skip,
            MiscChangesSelected.fast_boot,
            MiscChangesSelected.calm_caves,
            MiscChangesSelected.animal_buddies_grab_items,
            MiscChangesSelected.reduced_lag,
            MiscChangesSelected.remove_extraneous_cutscenes,
            MiscChangesSelected.hint_textbox_hold,
            MiscChangesSelected.remove_wrinkly_puzzles,
            MiscChangesSelected.fast_picture_taking,
            MiscChangesSelected.hud_hotkey,
            MiscChangesSelected.ammo_swap,
            MiscChangesSelected.homing_balloons,
            MiscChangesSelected.fast_transform_animation,
            MiscChangesSelected.troff_n_scoff_audio_indicator,
            MiscChangesSelected.lowered_aztec_lobby_bonus,
            MiscChangesSelected.quicker_galleon_star,
            MiscChangesSelected.vanilla_bug_fixes,
            MiscChangesSelected.save_k_rool_progress,
            MiscChangesSelected.small_bananas_always_visible,
            MiscChangesSelected.fast_hints,
            MiscChangesSelected.brighten_mad_maze_maul_enemies,
            MiscChangesSelected.raise_fungi_dirt_patch,
            MiscChangesSelected.global_instrument,
            MiscChangesSelected.fast_pause_transitions,
            MiscChangesSelected.cannon_game_better_control,
            MiscChangesSelected.better_fairy_camera,
            MiscChangesSelected.remove_enemy_cabin_timer,
            MiscChangesSelected.remove_galleon_ship_timers,
            MiscChangesSelected.japes_bridge_permanently_extended,
            MiscChangesSelected.move_spring_cabin_rocketbarrel,
        ],
        "more_cutscene_skips": ExtraCutsceneSkips.auto,
        "no_healing": False,
        "no_melons": False,
        "open_lobbies": False,
        "pearl_mermaid_behavior": RandomRequirement.pre_selected,
        "perma_death": False,
        "portal_numbers": True,
        "prog_slam_level_1": SlamRequirement.green,
        "prog_slam_level_2": SlamRequirement.green,
        "prog_slam_level_3": SlamRequirement.green,
        "prog_slam_level_4": SlamRequirement.green,
        "prog_slam_level_5": SlamRequirement.blue,
        "prog_slam_level_6": SlamRequirement.blue,
        "prog_slam_level_7": SlamRequirement.red,
        "prog_slam_level_8": SlamRequirement.red,
        "progressive_hint_count": 1,
        "progressive_hint_item": ProgressiveHintItem.off,
        "puzzle_rando_difficulty": PuzzleRando.medium,
        "race_coin_rando": False,
        "random_fairies": False,
        "random_starting_region": False,
        "random_starting_region_new": RandomStartingRegion.off,
        "randomize_enemy_sizes": False,
        "randomize_pickups": False,
        "rareware_gb_fairies": 6,
        "remove_barriers_selected": [],
        "select_keys": False,
        "serious_hints": True,
        "shop_indicator": True,
        "shorten_boss": True,
        "shops_dont_cost": True,
        "shuffle_helm_location": False,
        "shuffle_shops": False,
        "smaller_shops": False,
        "spoiler_hints": SpoilerHints.off,
        "spoiler_include_level_order": False,
        "spoiler_include_woth_count": False,
        "starting_keys_list_selected": [],
        "starting_moves_list_1": [],
        "starting_moves_list_2": [],
        "starting_moves_list_3": [],
        "starting_moves_list_4": [],
        "starting_moves_list_5": [],
        "starting_moves_list_count_1": 0,
        "starting_moves_list_count_2": 0,
        "starting_moves_list_count_3": 0,
        "starting_moves_list_count_4": 0,
        "starting_moves_list_count_5": 0,
        "starting_random": False,
        "tns_location_rando": False,
        "tns_selection_behavior": TroffSetting.normal_random,
        "troff_0": 0,
        "troff_1": 0,
        "troff_2": 0,
        "troff_3": 0,
        "troff_4": 0,
        "troff_5": 0,
        "troff_6": 0,
        "troff_7": 0,
        "troff_text": 150,
        "vanilla_door_rando": False,
        "warp_level_list_selected": [],
        "warp_to_isles": True,
        "win_condition_count": 1,
        "wrinkly_available": True,
        "wrinkly_hints": WrinklyHints.standard,
        "wrinkly_location_rando": False,
        "cb_rando_enabled": False,
        "cb_rando_list_selected": [],
    }


def handle_fake_generation_settings(settings: Settings, multiworld: MultiWorld) -> None:
    """Handle settings for fake generation (UT mode)."""
    if hasattr(multiworld, "generation_is_fake"):
        settings.is_ut_generation = True
        if hasattr(multiworld, "re_gen_passthrough"):
            if "Donkey Kong 64" in multiworld.re_gen_passthrough:
                passthrough = multiworld.re_gen_passthrough["Donkey Kong 64"]
                settings.level_order = passthrough["LevelOrder"]

                # Switch logic lifted out of level shuffle due to static levels for UT
                if settings.alter_switch_allocation:
                    for x in range(8):
                        settings.switch_allocation[x] = passthrough["SlamLevels"][x]

                settings.starting_kong_list = passthrough["StartingKongs"]
                settings.starting_kong = settings.starting_kong_list[0]  # fake a starting kong so that we don't force a different kong
                settings.medal_requirement = passthrough["JetpacReq"]
                settings.rareware_gb_fairies = passthrough["FairyRequirement"]
                settings.BLockerEntryItems = passthrough["BLockerEntryItems"]
                settings.BLockerEntryCount = passthrough["BLockerEntryCount"]
                settings.medal_cb_req = passthrough["MedalCBRequirement"]
                settings.medal_cb_req_level = [settings.medal_cb_req] * 8

                for level, value in enumerate(passthrough["MedalCBRequirementLevel"]):
                    settings.medal_cb_req_level[Levels(level)] = int(value)

                settings.mermaid_gb_pearls = passthrough["MermaidPearls"]
                settings.BossBananas = passthrough["BossBananas"]
                settings.boss_maps = passthrough["BossMaps"]
                settings.boss_kongs = passthrough["BossKongs"]
                settings.lanky_freeing_kong = passthrough["LankyFreeingKong"]
                settings.helm_order = passthrough["HelmOrder"]

                # Krusha kong models
                if "KongModels" in passthrough:
                    kong_models = passthrough["KongModels"]
                    settings.kong_model_dk = KongModels[kong_models.get("DK", "default")]
                    settings.kong_model_diddy = KongModels[kong_models.get("Diddy", "default")]
                    settings.kong_model_lanky = KongModels[kong_models.get("Lanky", "default")]
                    settings.kong_model_tiny = KongModels[kong_models.get("Tiny", "default")]
                    settings.kong_model_chunky = KongModels[kong_models.get("Chunky", "default")]
                settings.logic_type = LogicType[passthrough["LogicType"]]
                settings.tricks_selected = passthrough["TricksSelected"]
                settings.glitches_selected = passthrough["GlitchesSelected"]
                settings.open_lobbies = passthrough["OpenLobbies"]
                settings.starting_key_list = passthrough["StartingKeyList"]
                settings.galleon_water = GalleonWaterSetting[passthrough["GalleonWater"]]
                settings.galleon_water_internal = GalleonWaterSetting[passthrough["GalleonWater"]]

                # There's multiple sources of truth for helm order.
                settings.helm_donkey = 0 in settings.helm_order
                settings.helm_diddy = 4 in settings.helm_order
                settings.helm_lanky = 3 in settings.helm_order
                settings.helm_tiny = 2 in settings.helm_order
                settings.helm_chunky = 1 in settings.helm_order

                # Switchsanity
                for switch, data in passthrough["SwitchSanity"].items():
                    needed_kong = Kongs[data["kong"]]
                    switch_type = SwitchType[data["type"]]
                    settings.switchsanity_data[Switches[switch]] = SwitchInfo(switch, needed_kong, switch_type, 0, 0, [])

                if passthrough.get("Shopkeepers") or "shopkeepers" in (passthrough.get("ItemPool") or []):
                    settings.shuffled_location_types.append(Types.Cranky)
                    settings.shuffled_location_types.append(Types.Funky)
                    settings.shuffled_location_types.append(Types.Candy)
                    settings.shuffled_location_types.append(Types.Snide)

                # Restore starting region
                if passthrough.get("StartingRegion"):
                    from randomizer.Enums.Regions import Regions
                    from randomizer.Enums.Maps import Maps as DK64Maps

                    starting_region_data = passthrough["StartingRegion"]
                    # Ensure all fields exist and are not None
                    if all(key in starting_region_data and starting_region_data[key] is not None for key in ["region", "map", "exit", "region_name", "exit_name"]):
                        try:
                            settings.starting_region = {
                                "region": Regions[starting_region_data["region"]],
                                "map": DK64Maps[starting_region_data["map"]],
                                "exit": starting_region_data["exit"],
                                "region_name": starting_region_data["region_name"],
                                "exit_name": starting_region_data["exit_name"],
                            }
                        except (KeyError, TypeError) as e:
                            # If there's an error converting the data, just skip it
                            pass

                # Store DK Portal locations for later restoration (after spoiler is created)
                if passthrough.get("DKPortalLocations"):
                    settings.ut_dk_portal_locations = passthrough["DKPortalLocations"]


def fillsettings(options: DK64Options, multiworld: MultiWorld, random_obj: Random) -> Settings:
    """Fill and configure all DK64 settings."""
    # Start with default settings
    settings_dict: dict[str, Any] = get_default_settings()

    # Apply Archipelago-specific settings
    settings_dict["krool_access"] = True
    settings_dict["archipelago"] = True
    settings_dict["starting_kongs_count"] = options.starting_kong_count.value
    settings_dict["open_lobbies"] = options.open_lobbies.value
    match options.krool_in_boss_pool.value:
        case KroolShuffle.option_off:
            settings_dict["krool_in_boss_pool_v2"] = KroolInBossPool.off
        case KroolShuffle.option_krool_only:
            settings_dict["krool_in_boss_pool_v2"] = KroolInBossPool.krool_only
        case KroolShuffle.option_full_shuffle:
            settings_dict["krool_in_boss_pool_v2"] = KroolInBossPool.full_shuffle
    settings_dict["helm_phase_count"] = options.helm_phase_count.value
    settings_dict["krool_phase_count"] = options.krool_phase_count.value
    settings_dict["level_randomization"] = LevelRandomization.loadingzone if options.loading_zone_rando.value else LevelRandomization.level_order_complex
    if options.medal_distribution.value in (0, 4):  # pre_selected or progressive
        settings_dict["medal_cb_req"] = options.cbs_required_for_medal.value
    settings_dict["medal_requirement"] = options.jetpac_requirement.value
    settings_dict["rareware_gb_fairies"] = options.fairies_required_for_bfi.value
    settings_dict["mirror_mode"] = options.mirror_mode.value
    settings_dict["key_8_helm"] = options.helm_key_lock.value
    settings_dict["shuffle_helm_location"] = options.shuffle_helm_level_order.value
    settings_dict["mermaid_gb_pearls"] = options.pearls_required_for_mermaid.value
    settings_dict["cb_medal_behavior_new"] = options.medal_distribution.value
    settings_dict["smaller_shops"] = options.smaller_shops.value and not hasattr(multiworld, "generation_is_fake")
    settings_dict["puzzle_rando_difficulty"] = options.puzzle_rando.value
    if options.enable_cutscenes.value:
        settings_dict["more_cutscene_skips"] = ExtraCutsceneSkips.press
    settings_dict["alt_minecart_mayhem"] = options.alternate_minecart_mayhem.value
    match options.galleon_water_level:
        case GalleonWaterLevel.option_lowered:
            settings_dict["galleon_water"] = GalleonWaterSetting.lowered
        case GalleonWaterLevel.option_raised:
            settings_dict["galleon_water"] = GalleonWaterSetting.raised
        case _:
            settings_dict["galleon_water"] = GalleonWaterSetting.lowered
    settings_dict["no_consumable_upgrades"] = options.remove_bait_potions.value

    # Apply switch allocation settings
    slam_map = {
        "none": SlamRequirement.no_slam,
        "green": SlamRequirement.green,
        "blue": SlamRequirement.blue,
        "red": SlamRequirement.red,
    }
    if options.alter_switch_allocation.value:
        settings_dict["alter_switch_allocation"] = True
        # Convert level_1-level_8 to prog_slam_level_1 through prog_slam_level_8
        for i in range(8):
            level_key = f"level_{i + 1}"
            if level_key in options.alter_switch_allocation.value:
                slam_name = options.alter_switch_allocation.value[level_key]
                settings_dict[f"prog_slam_level_{i + 1}"] = slam_map.get(slam_name, SlamRequirement.green)

    # Apply blocker settings
    blocker_options: list[int] = [
        options.level_blockers.value.get("level_1", 0),
        options.level_blockers.value.get("level_2", 0),
        options.level_blockers.value.get("level_3", 0),
        options.level_blockers.value.get("level_4", 0),
        options.level_blockers.value.get("level_5", 0),
        options.level_blockers.value.get("level_6", 0),
        options.level_blockers.value.get("level_7", 0),
        options.level_blockers.value.get("level_8", 64),
    ]
    settings_dict["maximize_helm_blocker"] = options.maximize_level8_blocker.value
    if options.enable_chaos_blockers.value:
        settings_dict["blocker_text"] = options.chaos_ratio.value
        settings_dict["blocker_selection_behavior"] = BLockerSetting.chaos
    elif options.randomize_blocker_required_amounts.value:
        settings_dict["blocker_text"] = options.blocker_max.value
        settings_dict["blocker_selection_behavior"] = BLockerSetting.normal_random
    else:
        settings_dict["blocker_text"] = options.blocker_max.value
        settings_dict["blocker_selection_behavior"] = BLockerSetting.pre_selected
        for i, blocker in enumerate(blocker_options):
            settings_dict[f"blocker_{i}"] = blocker

    # Apply Troff n Scoff settings
    troff_options: list[int] = [
        options.level_troff.value.get("level_1", 0),
        options.level_troff.value.get("level_2", 0),
        options.level_troff.value.get("level_3", 0),
        options.level_troff.value.get("level_4", 0),
        options.level_troff.value.get("level_5", 0),
        options.level_troff.value.get("level_6", 0),
        options.level_troff.value.get("level_7", 0),
        options.level_troff.value.get("level_8", 0),
    ]
    if options.randomize_troff.value:
        settings_dict["troff_text"] = options.troff_max.value
        settings_dict["tns_selection_behavior"] = TroffSetting.normal_random
    else:
        settings_dict["troff_text"] = options.troff_max.value
        settings_dict["tns_selection_behavior"] = TroffSetting.pre_selected
        for i, troff in enumerate(troff_options):
            settings_dict[f"troff_{i}"] = troff

    # Apply item randomization settings
    # Moves, Golden Bananas, Shops, Kongs, Keys, Races, Training Moves, and Shockwave are always forced on.
    # All other categories come from the item_pool option.
    settings_dict["item_rando_list_selected"] = []
    settings_dict["item_rando_list_1"] = [
        ItemRandoListSelected.moves,
        ItemRandoListSelected.banana,
        ItemRandoListSelected.shop,
        ItemRandoListSelected.kong,
        ItemRandoListSelected.key,
        ItemRandoListSelected.racebanana,
        ItemRandoListSelected.trainingmoves,
        ItemRandoListSelected.shockwave,
    ]
    settings_dict["decouple_item_rando"] = False
    settings_dict["filler_items_selected"] = [ItemRandoFiller.junkitem]

    item_pool_selections = set(options.item_pool.value)
    item_pool_key_to_enums: dict[str, list[ItemRandoListSelected]] = {
        "crowns": [ItemRandoListSelected.crown],
        "blueprints": [ItemRandoListSelected.blueprint],
        "medals": [ItemRandoListSelected.medal],
        "company_coins": [ItemRandoListSelected.nintendocoin, ItemRandoListSelected.rarewarecoin],
        "fairies": [ItemRandoListSelected.fairy],
        "rainbow_coins": [ItemRandoListSelected.rainbowcoin],
        "bean": [ItemRandoListSelected.bean],
        "pearls": [ItemRandoListSelected.pearl],
        "crates": [ItemRandoListSelected.crateitem],
        "battle_arenas": [ItemRandoListSelected.gauntletbanana],
        "hints": [ItemRandoListSelected.hint],
        "shopkeepers": [ItemRandoListSelected.shopowners],
        "half_medals": [ItemRandoListSelected.halfmedal],
        "snide_turnins": [ItemRandoListSelected.blueprintbanana],
        "time_of_day": [ItemRandoListSelected.fungitime],
        "boulders": [ItemRandoListSelected.boulderitem],
        "balloons": [ItemRandoListSelected.balloon],
        "breakables": [ItemRandoListSelected.breakable],
        "dropsanity": [ItemRandoListSelected.enemies],
    }
    for key, enums in item_pool_key_to_enums.items():
        if key in item_pool_selections:
            for enum_value in enums:
                if enum_value not in settings_dict["item_rando_list_1"]:
                    settings_dict["item_rando_list_1"].append(enum_value)

    # Apply hard mode settings
    settings_dict["hard_mode_selected"] = []
    for hard in options.hard_mode_selected:
        match hard:
            case "hard_enemies":
                settings_dict["hard_mode_selected"].append(HardModeSelected.hard_enemies)
            case "shuffled_jetpac_enemies":
                settings_dict["hard_mode_selected"].append(HardModeSelected.shuffled_jetpac_enemies)
            case "strict_helm_timer":
                settings_dict["hard_mode_selected"].append(HardModeSelected.strict_helm_timer)
            case "donk_in_the_dark_world":
                settings_dict["hard_mode_selected"].append(HardModeSelected.donk_in_the_dark_world)
            case "donk_in_the_sky":
                settings_dict["hard_mode_selected"].append(HardModeSelected.donk_in_the_sky)
            case "angry_caves":
                settings_dict["hard_mode_selected"].append(HardModeSelected.angry_caves)
            case "fast_balloons":
                settings_dict["hard_mode_selected"].append(HardModeSelected.fast_balloons)
            case "lower_max_refill_amounts":
                settings_dict["hard_mode_selected"].append(HardModeSelected.lower_max_refill_amounts)

    # Apply Kong settings
    import random

    settings_dict["krool_key_count"] = options.pregiven_keys.value
    settings_dict["win_condition_spawns_ship"] = 1 if options.require_beating_krool.value else 0
    match options.select_starting_kong.value:
        case SelectStartingKong.option_donkey:
            settings_dict["starting_kong"] = Kongs.donkey
        case SelectStartingKong.option_diddy:
            settings_dict["starting_kong"] = Kongs.diddy
        case SelectStartingKong.option_lanky:
            settings_dict["starting_kong"] = Kongs.lanky
        case SelectStartingKong.option_tiny:
            settings_dict["starting_kong"] = Kongs.tiny
        case SelectStartingKong.option_chunky:
            settings_dict["starting_kong"] = Kongs.chunky
        case SelectStartingKong.option_any:
            settings_dict["starting_kong"] = Kongs.any

    # Apply individual kong model settings from the kong_models dict
    kong_model_mapping = {"dk": "kong_model_dk", "diddy": "kong_model_diddy", "lanky": "kong_model_lanky", "tiny": "kong_model_tiny", "chunky": "kong_model_chunky"}

    # Convert string model names to enum values if needed
    model_name_to_enum = {
        "default": 0,
        "disco_chunky": 1,
        "krusha": 2,
        "krool_fight": 3,
        "krool_cutscene": 4,
        "cranky": 5,
        "candy": 6,
        "funky": 7,
        "disco_donkey": 8,
        "robokrem": 9,
        "rabbit": 10,
    }

    for kong, setting_key in kong_model_mapping.items():
        if kong in options.kong_models.value:
            model_value = options.kong_models.value[kong]
            # Convert string to int if needed
            if isinstance(model_value, str):
                model_value = model_name_to_enum.get(model_value, 0)
            settings_dict[setting_key] = KongModels(model_value)
        else:
            settings_dict[setting_key] = KongModels.default

    # Then apply krusha settings (only if the individual model is still default)
    match options.krusha_model_mode.value:
        case KrushaRandom.option_manual:
            # Manual krusha assignment is handled via kong_models above
            pass
        case KrushaRandom.option_random_1:
            available: list[str] = [k for k, m in kong_model_mapping.items() if settings_dict[m] == KongModels.default]
            if available:
                selected = random.choice(available)
                if settings_dict[kong_model_mapping[selected]] == KongModels.default:
                    settings_dict[kong_model_mapping[selected]] = KongModels.krusha
        case KrushaRandom.option_sometimes_1:
            if random.random() < 0.5:
                available = [k for k, m in kong_model_mapping.items() if settings_dict[m] == KongModels.default]
                if available:
                    selected = random.choice(available)
                    if settings_dict[kong_model_mapping[selected]] == KongModels.default:
                        settings_dict[kong_model_mapping[selected]] = KongModels.krusha
        case KrushaRandom.option_random_all:
            for kong, model_key in kong_model_mapping.items():
                if settings_dict[model_key] == KongModels.default and random.random() < 0.5:
                    settings_dict[model_key] = KongModels.krusha

    # Apply starting region, portal, and switchsanity settings
    match options.random_starting_region.value:
        case RandomStartingLocation.option_off:
            settings_dict["random_starting_region_new"] = RandomStartingRegion.off
        case RandomStartingLocation.option_isles_only:
            settings_dict["random_starting_region_new"] = RandomStartingRegion.isles_only
        case RandomStartingLocation.option_all:
            settings_dict["random_starting_region_new"] = RandomStartingRegion.all
    match options.dk_portal_location_rando.value:
        case DKPortalLocationRando.option_off:
            settings_dict["dk_portal_location_rando_v2"] = DKPortalRando.off
        case DKPortalLocationRando.option_main_only:
            settings_dict["dk_portal_location_rando_v2"] = DKPortalRando.main_only
        case DKPortalLocationRando.option_all:
            settings_dict["dk_portal_location_rando_v2"] = DKPortalRando.on
    _kong_value_map = {
        "donkey": SwitchsanityKong.donkey,
        "diddy": SwitchsanityKong.diddy,
        "lanky": SwitchsanityKong.lanky,
        "tiny": SwitchsanityKong.tiny,
        "chunky": SwitchsanityKong.chunky,
        "random": SwitchsanityKong.random,
        "any": SwitchsanityKong.any,
    }
    _gone_value_map = {
        "bongos": SwitchsanityGone.bongos,
        "guitar": SwitchsanityGone.guitar,
        "trombone": SwitchsanityGone.trombone,
        "sax": SwitchsanityGone.sax,
        "triangle": SwitchsanityGone.triangle,
        "lever": SwitchsanityGone.lever,
        "gong": SwitchsanityGone.gong,
        "gone_pad": SwitchsanityGone.gone_pad,
        "random": SwitchsanityGone.random,
    }
    _any_switch_enabled = any(v != "off" for v in options.switchsanity.value.values())
    settings_dict["switchsanity_enabled"] = _any_switch_enabled
    if _any_switch_enabled:
        for _switch_key, _switch_value in options.switchsanity.value.items():
            if _switch_value == "off":
                continue
            _full_key = f"switchsanity_switch_{_switch_key}"
            if _switch_key in SwitchsanityOptions.GONE_SWITCHES:
                settings_dict[_full_key] = _gone_value_map.get(_switch_value, SwitchsanityGone.random)
            else:
                settings_dict[_full_key] = _kong_value_map.get(_switch_value, SwitchsanityKong.random)

    # Apply logic, barriers, glitches, and tricks settings
    settings_dict["logic_type"] = options.logic_type.value
    settings_dict["remove_barriers_selected"] = []
    for barrier in options.remove_barriers_selected:
        match barrier:
            case "japes_coconut_gates":
                settings_dict["remove_barriers_selected"].append(RemovedBarriersSelected.japes_coconut_gates)
            case "japes_shellhive_gate":
                settings_dict["remove_barriers_selected"].append(RemovedBarriersSelected.japes_shellhive_gate)
            case "aztec_tunnel_door":
                settings_dict["remove_barriers_selected"].append(RemovedBarriersSelected.aztec_tunnel_door)
            case "aztec_5dtemple_switches":
                settings_dict["remove_barriers_selected"].append(RemovedBarriersSelected.aztec_5dtemple_switches)
            case "aztec_llama_switches":
                settings_dict["remove_barriers_selected"].append(RemovedBarriersSelected.aztec_llama_switches)
            case "aztec_tiny_temple_ice":
                settings_dict["remove_barriers_selected"].append(RemovedBarriersSelected.aztec_tiny_temple_ice)
            case "factory_testing_gate":
                settings_dict["remove_barriers_selected"].append(RemovedBarriersSelected.factory_testing_gate)
            case "factory_production_room":
                settings_dict["remove_barriers_selected"].append(RemovedBarriersSelected.factory_production_room)
            case "galleon_lighthouse_gate":
                settings_dict["remove_barriers_selected"].append(RemovedBarriersSelected.galleon_lighthouse_gate)
            case "galleon_shipyard_area_gate":
                settings_dict["remove_barriers_selected"].append(RemovedBarriersSelected.galleon_shipyard_area_gate)
            case "castle_crypt_doors":
                settings_dict["remove_barriers_selected"].append(RemovedBarriersSelected.castle_crypt_doors)
            case "galleon_seasick_ship":
                settings_dict["remove_barriers_selected"].append(RemovedBarriersSelected.galleon_seasick_ship)
            case "forest_green_tunnel":
                settings_dict["remove_barriers_selected"].append(RemovedBarriersSelected.forest_green_tunnel)
            case "forest_yellow_tunnel":
                settings_dict["remove_barriers_selected"].append(RemovedBarriersSelected.forest_yellow_tunnel)
            case "caves_igloo_pads":
                settings_dict["remove_barriers_selected"].append(RemovedBarriersSelected.caves_igloo_pads)
            case "caves_ice_walls":
                settings_dict["remove_barriers_selected"].append(RemovedBarriersSelected.caves_ice_walls)
            case "galleon_treasure_room":
                settings_dict["remove_barriers_selected"].append(RemovedBarriersSelected.galleon_treasure_room)
            case "helm_star_gates":
                settings_dict["remove_barriers_selected"].append(RemovedBarriersSelected.helm_star_gates)
            case "helm_punch_gates":
                settings_dict["remove_barriers_selected"].append(RemovedBarriersSelected.helm_punch_gates)
    settings_dict["glitches_selected"] = []
    settings_dict["tricks_selected"] = []
    for trick in options.tricks_selected:
        match trick:
            case "monkey_maneuvers":
                settings_dict["tricks_selected"].append(TricksSelected.monkey_maneuvers)
            case "hard_shooting":
                settings_dict["tricks_selected"].append(TricksSelected.hard_shooting)
            case "advanced_grenading":
                settings_dict["tricks_selected"].append(TricksSelected.advanced_grenading)
            case "slope_resets":
                settings_dict["tricks_selected"].append(TricksSelected.slope_resets)
    for glitch in options.glitches_selected:
        match glitch:
            case "moonkicks":
                settings_dict["glitches_selected"].append(GlitchesSelected.moonkicks)
            case "phase_swimming":
                settings_dict["glitches_selected"].append(GlitchesSelected.phase_swimming)
            case "swim_through_shores":
                settings_dict["glitches_selected"].append(GlitchesSelected.swim_through_shores)
            case "troff_n_scoff_skips":
                settings_dict["glitches_selected"].append(GlitchesSelected.troff_n_scoff_skips)
            case "moontail":
                settings_dict["glitches_selected"].append(GlitchesSelected.moontail)

    # Apply enemy settings
    settings_dict["enemies_selected"] = []
    enemy_mapping: dict[str, Enemies] = {
        "Bat": Enemies.Bat,
        "BeaverBlue": Enemies.BeaverBlue,
        "BeaverGold": Enemies.BeaverGold,
        "Bug": Enemies.Bug,
        "FireballGlasses": Enemies.FireballGlasses,
        "GetOut": Enemies.GetOut,
        "Ghost": Enemies.Ghost,
        "Gimpfish": Enemies.Gimpfish,
        "Kaboom": Enemies.Kaboom,
        "ChunkyKasplat": Enemies.KasplatChunky,
        "DKKasplat": Enemies.KasplatDK,
        "DiddyKasplat": Enemies.KasplatDiddy,
        "LankyKasplat": Enemies.KasplatLanky,
        "TinyKasplat": Enemies.KasplatTiny,
        "GreenKlaptrap": Enemies.KlaptrapGreen,
        "PurpleKlaptrap": Enemies.KlaptrapPurple,
        "RedKlaptrap": Enemies.KlaptrapRed,
        "Klobber": Enemies.Klobber,
        "Klump": Enemies.Klump,
        "Kop": Enemies.Guard,
        "Kosha": Enemies.Kosha,
        "Kremling": Enemies.Kremling,
        "Krossbones": Enemies.Krossbones,
        "GreenDice": Enemies.MrDice0,
        "RedDice": Enemies.MrDice1,
        "MushroomMan": Enemies.MushroomMan,
        "Pufftup": Enemies.Pufftup,
        "RoboKremling": Enemies.RoboKremling,
        "ZingerRobo": Enemies.ZingerRobo,
        "Ruler": Enemies.Ruler,
        "Shuri": Enemies.Shuri,
        "SirDomino": Enemies.SirDomino,
        "SpiderSmall": Enemies.SpiderSmall,
        "ZingerCharger": Enemies.ZingerCharger,
        "ZingerLime": Enemies.ZingerLime,
        "DisableAKop": Enemies.GuardDisableA,
        "DisableZKop": Enemies.GuardDisableZ,
        "DisableTaggingKop": Enemies.GuardTag,
        "GetOutKop": Enemies.GuardGetOut,
    }
    for enemy in options.enemies_selected:
        if enemy in enemy_mapping:
            settings_dict["enemies_selected"].append(enemy_mapping[enemy])

    # Apply boss and key settings
    settings_dict["starting_keys_list_selected"] = []
    boss_mapping: dict[str, Maps] = {
        "Armydillo 1": Maps.JapesBoss,
        "Dogadon 1": Maps.AztecBoss,
        "Mad Jack": Maps.FactoryBoss,
        "Pufftoss": Maps.GalleonBoss,
        "Dogadon 2": Maps.FungiBoss,
        "Armydillo 2": Maps.CavesBoss,
        "Kutout": Maps.CastleBoss,
        "DK phase": Maps.KroolDonkeyPhase,
        "Diddy Phase": Maps.KroolDiddyPhase,
        "Lanky Phase": Maps.KroolLankyPhase,
        "Tiny Phase": Maps.KroolTinyPhase,
        "Chunky Phase": Maps.KroolChunkyPhase,
    }
    if hasattr(options, "allowed_bosses") and options.allowed_bosses.value:
        settings_dict["bosses_selected"] = []
        for boss in options.allowed_bosses.value:
            if boss in boss_mapping:
                settings_dict["bosses_selected"].append(boss_mapping[boss])
    for hardboss in options.harder_bosses:
        match hardboss:
            case "fast_mad_jack":
                settings_dict["hard_bosses_selected"].append(HardBossesSelected.fast_mad_jack)
            case "alternative_mad_jack_kongs":
                settings_dict["hard_bosses_selected"].append(HardBossesSelected.alternative_mad_jack_kongs)
            case "pufftoss_star_rando":
                settings_dict["hard_bosses_selected"].append(HardBossesSelected.pufftoss_star_rando)
            case "pufftoss_star_raised":
                settings_dict["hard_bosses_selected"].append(HardBossesSelected.pufftoss_star_raised)
            case "kut_out_phase_rando":
                settings_dict["hard_bosses_selected"].append(HardBossesSelected.kut_out_phase_rando)
            case "k_rool_toes_rando":
                settings_dict["hard_bosses_selected"].append(HardBossesSelected.k_rool_toes_rando)
            case "beta_lanky_phase":
                settings_dict["hard_bosses_selected"].append(HardBossesSelected.beta_lanky_phase)
    key_mapping: dict[str, DK64RItems] = {
        "Key 1": DK64RItems.JungleJapesKey,
        "Key 2": DK64RItems.AngryAztecKey,
        "Key 3": DK64RItems.FranticFactoryKey,
        "Key 4": DK64RItems.GloomyGalleonKey,
        "Key 5": DK64RItems.FungiForestKey,
        "Key 6": DK64RItems.CrystalCavesKey,
        "Key 7": DK64RItems.CreepyCastleKey,
        "Key 8": DK64RItems.HideoutHelmKey,
    }
    for item in options.start_inventory:
        if item in key_mapping:
            settings_dict["starting_keys_list_selected"].append(key_mapping[item])
    if settings_dict["starting_keys_list_selected"]:
        settings_dict["select_keys"] = True

    # Apply goal settings
    settings_dict["win_condition_item"] = GOAL_MAPPING[options.goal]
    if options.goal == Goal.option_krools_challenge:
        settings_dict["win_condition_spawns_ship"] = True
    if options.goal in QUANTITY_GOALS.keys():
        goal_name = QUANTITY_GOALS[options.goal]
        settings_dict["win_condition_count"] = calculate_quantity(goal_name, options.goal_quantity.value, random_obj)
    if options.goal == Goal.option_treasure_hurry:
        settings_dict.update(
            {
                "helm_hurry": True,
                "helmhurry_list_starting_time": 60000,
                "helmhurry_list_golden_banana": -60,
                "helmhurry_list_blueprint": -120,
                "helmhurry_list_company_coins": -3600,
                "helmhurry_list_move": 0,
                "helmhurry_list_banana_medal": -300,
                "helmhurry_list_rainbow_coin": 0,
                "helmhurry_list_boss_key": -900,
                "helmhurry_list_battle_crown": -1200,
                "helmhurry_list_bean": -5400,
                "helmhurry_list_pearl": -1800,
                "helmhurry_list_kongs": 0,
                "helmhurry_list_fairies": -600,
                "helmhurry_list_colored_bananas": -2,
                "helmhurry_list_ice_traps": 120,
            }
        )

    # Apply starting moves settings — pool-based system
    from randomizer.Lists import Item as DK64RItem

    _valid_move_types = {Types.Key, Types.Shop, Types.Shockwave, Types.TrainingBarrel, Types.Climbing, Types.Cannons, Types.Cranky, Types.Funky, Types.Candy, Types.Snide, Types.FungiTime}
    _shopkeeper_types = {Types.Cranky, Types.Funky, Types.Candy, Types.Snide}

    for _pool_num in range(1, 6):
        _pool_option = getattr(options, f"starting_move_pool_{_pool_num}")
        _count_option = getattr(options, f"starting_move_pool_{_pool_num}_count")
        _item_ids = []
        for _item_name in _pool_option.value:
            _item_id = logic_item_name_to_id.get(_item_name)
            if _item_id is None:
                continue
            _item_obj = DK64RItem.ItemList.get(_item_id)
            if _item_obj is None or _item_obj.type not in _valid_move_types:
                continue
            _item_ids.append(_item_id)
        settings_dict[f"starting_moves_list_{_pool_num}"] = _item_ids
        settings_dict[f"starting_moves_list_count_{_pool_num}"] = min(_count_option.value, len(_item_ids))

    # Apply hint settings
    if options.hint_style == 0:
        settings_dict["wrinkly_hints"] = WrinklyHints.off

    # Apply minigame and bonus barrel settings
    settings_dict["minigames_list_selected"] = [MinigamesListSelected[minigame] for minigame in options.shuffled_bonus_barrels]
    settings_dict["disable_hard_minigames"] = not options.hard_minigames.value
    settings_dict["bonus_barrel_auto_complete"] = options.auto_complete_bonus_barrels.value and options.goal.value != Goal.option_bonuses
    settings_dict["helm_room_bonus_count"] = HelmBonuses(options.helm_room_bonus_count.value)
    door_item_to_key: dict[HelmDoorItem, str] = {
        HelmDoorItem.req_gb: "golden_bananas",
        HelmDoorItem.req_bp: "blueprints",
        HelmDoorItem.req_companycoins: "company_coins",
        HelmDoorItem.req_key: "keys",
        HelmDoorItem.req_medal: "medals",
        HelmDoorItem.req_crown: "crowns",
        HelmDoorItem.req_fairy: "fairies",
        HelmDoorItem.req_rainbowcoin: "rainbow_coins",
        HelmDoorItem.req_bean: "bean",
        HelmDoorItem.req_pearl: "pearls",
    }
    settings_dict["crown_door_item"] = HelmDoorItem(options.crown_door_item.value)
    crown_item_key = door_item_to_key.get(settings_dict["crown_door_item"])
    settings_dict["crown_door_item_count"] = options.helm_door_item_count.value.get(crown_item_key, 1) if crown_item_key else 1
    settings_dict["coin_door_item"] = HelmDoorItem(options.coin_door_item.value)
    coin_item_key = door_item_to_key.get(settings_dict["coin_door_item"])
    settings_dict["coin_door_item_count"] = options.helm_door_item_count.value.get(coin_item_key, 1) if coin_item_key else 1
    if hasattr(multiworld, "generation_is_fake") and hasattr(multiworld, "re_gen_passthrough") and "Donkey Kong 64" in multiworld.re_gen_passthrough:
        passthrough = multiworld.re_gen_passthrough["Donkey Kong 64"]
        settings_dict["bonus_barrel_auto_complete"] = passthrough["Autocomplete"]
        settings_dict["helm_room_bonus_count"] = HelmBonuses(passthrough["HelmBarrelCount"])

    # Handle fake generation keys if needed
    if hasattr(multiworld, "generation_is_fake"):
        settings_dict["krool_key_count"] = 8

    # Create settings object
    settings = Settings(settings_dict, random_obj)
    settings.location_pool_size = 0

    # Handle fake generation additional settings
    handle_fake_generation_settings(settings, multiworld)

    return settings
