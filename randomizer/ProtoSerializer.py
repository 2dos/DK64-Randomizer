"""Settings serialization to/from Protocol Buffers."""

import base64
import json
import logging
import os
import sys
from typing import Any, Dict, Iterable, List, Tuple, TYPE_CHECKING
from randomizer.Enums.Items import Items
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Settings import CrownEnemyRando, HardBossesSelected, HardModeSelected, HelmDoorItem, MiscChangesSelected, SlamRequirement
from randomizer.Enums.Types import BarrierItems

proto_gen_path = os.path.join(os.path.dirname(__file__), "proto_gen")
if proto_gen_path not in sys.path:
    sys.path.insert(0, proto_gen_path)

from randomizer.proto_gen import (
    endgame_settings_pb2,
    fill_result_pb2,
    item_settings_pb2,
    overworld_settings_pb2,
    plandomizer_settings_pb2,
    qol_settings_pb2,
    requirement_settings_pb2,
    settings_pb2,
)

if TYPE_CHECKING:
    from randomizer.Settings import Settings
    from randomizer.Spoiler import Spoiler

logger = logging.getLogger(__name__)


# =============================================================================
# Small helpers
# =============================================================================


def _enum_value(x: Any) -> Any:
    """Return x.value for enum-like objects, otherwise x unchanged."""
    return x.value if hasattr(x, "value") else x


def _enum_values(items: Iterable[Any]) -> List[Any]:
    return [_enum_value(x) for x in items]


def _to_int(val: Any, default: int = 0) -> int:
    """Coerce val to int, falling back to default on None or conversion failure."""
    if val is None:
        return default
    try:
        return int(val)
    except (TypeError, ValueError):
        return default


# =============================================================================
# How to add a new setting
# =============================================================================
#
#  NOTE: ALL SETTINGS NEED AN ENTRY HERE TO BE PICKED UP BY THE PROTO CONVERSION
#
#  To add a setting:
#  1. Find which section is the most fitting for said setting
#    - Normally it is based on what tab the setting is at on the site
#
#  2. If the setting needs a mapping (eg. Switchsanity) Make sure to add the
#     mapping in the appropriate section
#
#  3. IMPORTANT: BE SURE TO ADD THE SETTING TO BOTH "populate_x_settings" AND
#     "apply_x_settings"
#     - Without this, the setting string conversion will be incomplete
#
#  4. Additionally, any changes to fill will need to be accounted for in
#     the proto -> ProtoSerializer -> ApplyRandomizer roundtrip so that
#     patching will match the spoiler log
#
#
# =============================================================================
# Top-level Settings <-> proto conversion
# =============================================================================


def settings_to_proto(settings: "Settings") -> settings_pb2.SettingsInfo:
    """Convert a Settings object to a SettingsInfo protobuf message."""
    proto = settings_pb2.SettingsInfo()
    _populate_item_settings(settings, proto.item_settings)
    _populate_requirement_settings(settings, proto.requirement_settings)
    _populate_overworld_settings(settings, proto.overworld_settings)
    _populate_endgame_settings(settings, proto.endgame_settings)
    _populate_qol_settings(settings, proto.qol_settings)
    _populate_plandomizer_settings(settings, proto.plandomizer_settings)
    return proto


def proto_to_settings(proto: settings_pb2.SettingsInfo, settings: "Settings") -> None:
    """Apply settings from a SettingsInfo protobuf message to a Settings object."""
    _apply_item_settings(proto.item_settings, settings)
    _apply_requirement_settings(proto.requirement_settings, settings)
    _apply_overworld_settings(proto.overworld_settings, settings)
    _apply_endgame_settings(proto.endgame_settings, settings)
    _apply_qol_settings(proto.qol_settings, settings)
    _apply_plandomizer_settings(proto.plandomizer_settings, settings)


def serialize_settings_to_base64(settings: "Settings") -> str:
    """Serialize a Settings object to a URL-safe base64-encoded protobuf string."""
    proto = settings_to_proto(settings)
    return base64.urlsafe_b64encode(proto.SerializeToString()).decode("utf-8")


def deserialize_settings_from_base64(proto_string: str) -> settings_pb2.SettingsInfo:
    """Deserialize a base64-encoded protobuf string to a SettingsInfo message.

    Raises:
        ValueError: If the string cannot be decoded or parsed.
    """
    try:
        try:
            binary_data = base64.urlsafe_b64decode(proto_string)
        except Exception:
            # Fall back to standard base64 for older / non-URL-safe payloads.
            binary_data = base64.b64decode(proto_string)

        proto = settings_pb2.SettingsInfo()
        proto.ParseFromString(binary_data)
        return proto
    except Exception as e:
        raise ValueError(f"Failed to deserialize proto string: {e}")


def is_proto_settings_string(settings_string: str) -> bool:
    """Return True if the string parses as a protobuf SettingsInfo."""
    try:
        deserialize_settings_from_base64(settings_string)
        return True
    except Exception:
        return False


# =============================================================================
# Item settings
# =============================================================================
# Add a new simple setting: append one row to _ICE_TRAP_WEIGHTS or
# _ITEM_COUNT_FIELDS below, or add an explicit line in both
# _populate_item_settings and _apply_item_settings.

# (ice_traps.weights proto field, Settings attribute).
_ICE_TRAP_WEIGHTS: Tuple[Tuple[str, str], ...] = (
    ("bubble", "trap_weight_bubble"),
    ("reverse", "trap_weight_reverse"),
    ("slow", "trap_weight_slow"),
    ("disable_a", "trap_weight_disablea"),
    ("disable_b", "trap_weight_disableb"),
    ("disable_z", "trap_weight_disablez"),
    ("disable_c_up", "trap_weight_disablecu"),
    ("get_out", "trap_weight_getout"),
    ("dry", "trap_weight_dry"),
    ("flip", "trap_weight_flip"),
    ("ice_floor", "trap_weight_icefloor"),
    ("paper", "trap_weight_paper"),
    ("slip", "trap_weight_slip"),
    ("animal", "trap_weight_animal"),
    ("rockfall", "trap_weight_rockfall"),
    ("disable_tag", "trap_weight_disabletag"),
)

# (item_counts proto field, Settings attribute).
_ITEM_COUNT_FIELDS: Tuple[Tuple[str, str], ...] = (
    ("golden_bananas", "total_gbs"),
    ("banana_medals", "total_medals"),
    ("banana_fairies", "total_fairies"),
    ("battle_crowns", "total_crowns"),
    ("rainbow_coins", "total_rainbow_coins"),
    ("pearls", "total_pearls"),
)


def _populate_item_settings(settings: "Settings", proto: item_settings_pb2.ItemSettings) -> None:
    """Populate ItemSettings proto from Settings object."""
    is_decoupled = bool(settings.decouple_item_rando)
    proto.decouple_item_rando = is_decoupled

    # Always create all 10 item pools (even empty) to preserve index mapping.
    # In decoupled mode pools 5-9 contain check locations rather than items.
    for i in range(10):
        pool = proto.pools.add()
        item_list = getattr(settings, f"item_rando_list_{i}", None)
        if not item_list:
            continue
        values = _enum_values(item_list)
        if is_decoupled and i >= 5:
            pool.checks.extend(values)
        else:
            pool.items.extend(values)

    # Always create all 5 starting-move pools (even empty) to preserve index mapping.
    # Prefer the original list (pre-progressive conversion) to keep Progressive* items.
    for i in range(1, 6):
        move_pool = proto.starting_move_pools.add()
        move_list = getattr(settings, f"original_starting_moves_list_{i}", None) if hasattr(settings, f"original_starting_moves_list_{i}") else getattr(settings, f"starting_moves_list_{i}", None)
        if move_list:
            move_pool.items.extend(_enum_values(move_list))
        move_pool.count_given = getattr(settings, f"starting_moves_list_count_{i}", 0)

    if settings.filler_items_selected:
        proto.filler_items.extend(_enum_values(settings.filler_items_selected))

    # Ice trap settings
    proto.ice_traps.count = settings.ice_trap_count
    proto.ice_traps.model = settings.ice_trap_model_v2
    for proto_field, settings_attr in _ICE_TRAP_WEIGHTS:
        setattr(proto.ice_traps.weights, proto_field, getattr(settings, settings_attr))

    # Item counts
    for proto_field, settings_attr in _ITEM_COUNT_FIELDS:
        setattr(proto.item_counts, proto_field, getattr(settings, settings_attr))

    proto.max_snide_reward_requirement = settings.most_snide_rewards


def _apply_item_settings(proto: item_settings_pb2.ItemSettings, settings: "Settings") -> None:
    """Apply ItemSettings proto to Settings object."""

    is_decoupled = bool(proto.decouple_item_rando)
    settings.decouple_item_rando = is_decoupled

    # Clear all 10 item lists, then restore from the corresponding pool.
    for i in range(10):
        setattr(settings, f"item_rando_list_{i}", [])
    for i, pool in enumerate(proto.pools):
        if i >= 10:
            break
        pool_items = list(pool.checks) if (is_decoupled and i >= 5) else list(pool.items)
        setattr(settings, f"item_rando_list_{i}", pool_items)

    # Restore starting move pools (1-indexed). Items are converted back to the
    # Items enum so downstream code keeps working with enum members.
    for i, move_pool in enumerate(proto.starting_move_pools):
        if i >= 5:
            break
        list_index = i + 1
        enum_list: List[Any] = []
        for value in move_pool.items:
            try:
                enum_list.append(Items(value))
            except ValueError:
                enum_list.append(value)
        setattr(settings, f"starting_moves_list_{list_index}", enum_list)
        setattr(settings, f"starting_moves_list_count_{list_index}", move_pool.count_given)

    settings.filler_items_selected = list(proto.filler_items)

    # Ice trap settings
    settings.ice_trap_count = proto.ice_traps.count
    settings.ice_trap_model_v2 = proto.ice_traps.model
    for proto_field, settings_attr in _ICE_TRAP_WEIGHTS:
        setattr(settings, settings_attr, getattr(proto.ice_traps.weights, proto_field))

    # Item counts
    for proto_field, settings_attr in _ITEM_COUNT_FIELDS:
        setattr(settings, settings_attr, getattr(proto.item_counts, proto_field))

    settings.most_snide_rewards = proto.max_snide_reward_requirement


# =============================================================================
# Requirement settings
# =============================================================================
# Add a new switchsanity location: append one row to _SWITCHSANITY_LOCATIONS.
# Other new simple settings need an explicit line in both _populate_* and
# _apply_* below.

# Switchsanity switch locations: (proto enum value, Settings attribute name).
_SWITCHSANITY_LOCATIONS: Tuple[Tuple[int, str], ...] = (
    (1, "switchsanity_switch_isles_to_kroc_top"),
    (2, "switchsanity_switch_isles_helm_lobby"),
    (3, "switchsanity_switch_isles_aztec_lobby_back_room"),
    (4, "switchsanity_switch_isles_fungi_lobby_fairy"),
    (5, "switchsanity_switch_isles_spawn_rocketbarrel"),
    (6, "switchsanity_switch_japes_free_kong"),
    (7, "switchsanity_switch_japes_to_hive"),
    (8, "switchsanity_switch_japes_to_cavern"),
    (9, "switchsanity_switch_japes_to_painting_room"),
    (10, "switchsanity_switch_japes_to_rambi"),
    (11, "switchsanity_switch_aztec_free_tiny"),
    (12, "switchsanity_switch_aztec_free_lanky"),
    (13, "switchsanity_switch_aztec_to_kasplat_room"),
    (14, "switchsanity_switch_aztec_to_connector_tunnel"),
    (15, "switchsanity_switch_aztec_llama_front"),
    (16, "switchsanity_switch_aztec_llama_side"),
    (17, "switchsanity_switch_aztec_llama_back"),
    (18, "switchsanity_switch_aztec_sand_tunnel"),
    (19, "switchsanity_switch_galleon_to_lighthouse_side"),
    (20, "switchsanity_switch_galleon_to_shipwreck_side"),
    (21, "switchsanity_switch_galleon_to_cannon_game"),
    (22, "switchsanity_switch_fungi_yellow_tunnel"),
    (23, "switchsanity_switch_fungi_green_tunnel_near"),
    (24, "switchsanity_switch_fungi_green_tunnel_far"),
    (25, "switchsanity_switch_factory_dark_grate"),
    (26, "switchsanity_switch_factory_bonus_grate"),
    (27, "switchsanity_switch_factory_monster_grate"),
    (28, "switchsanity_switch_caves_gone_cave"),
    (29, "switchsanity_switch_caves_snide_cave"),
    (30, "switchsanity_switch_caves_boulder_cave"),
    (31, "switchsanity_switch_caves_lobby_blueprint"),
    (32, "switchsanity_switch_caves_lobby_lava"),
    (33, "switchsanity_switch_aztec_gong_tower"),
    (34, "switchsanity_switch_aztec_lobby_gong"),
)


def _populate_requirement_settings(settings: "Settings", proto: requirement_settings_pb2.RequirementSettings) -> None:
    """Populate RequirementSettings proto from Settings object."""
    # B Locker / T&S / quantity-based requirements
    proto.b_locker_option.opt = settings.blocker_selection_behavior
    if settings.BLockerEntryCount:
        proto.b_locker_option.amounts.extend(settings.BLockerEntryCount)
    proto.b_locker_option.maximum = settings.blocker_max
    proto.maximize_helm_b_locker = bool(settings.maximize_helm_blocker)

    proto.tns_option.opt = settings.tns_selection_behavior
    if settings.BossBananas:
        proto.tns_option.amounts.extend(settings.BossBananas)
    proto.tns_option.maximum = settings.troff_max

    proto.medals_for_jetpac.opt = settings.medal_jetpac_behavior
    proto.medals_for_jetpac.selected_quantity = settings.medal_requirement

    proto.pearls_for_mermaid.opt = settings.pearl_mermaid_behavior
    proto.pearls_for_mermaid.selected_quantity = settings.mermaid_gb_pearls

    proto.fairies_for_fairy_queen.opt = settings.fairy_queen_behavior
    proto.fairies_for_fairy_queen.selected_quantity = settings.rareware_gb_fairies

    proto.cbs_for_medal.opt = settings.cb_medal_behavior_new
    proto.cbs_for_medal.selected_quantity = settings.medal_cb_req

    proto.open_lobbies = bool(settings.open_lobbies)

    # Switchsanity: add a SwitchAssignment for every configured location.
    proto.switchsanity.enabled = bool(settings.switchsanity_enabled)
    for location_enum, attr_name in _SWITCHSANITY_LOCATIONS:
        if not hasattr(settings, attr_name):
            continue
        switch_item = getattr(settings, attr_name)
        if switch_item is None:
            continue
        assignment = proto.switchsanity.switch_assignment.add()
        assignment.location = location_enum
        assignment.item = _enum_value(switch_item)

    proto.smaller_shops = bool(settings.smaller_shops)
    proto.tooie_style_shops = bool(settings.shops_dont_cost)
    proto.free_trade_agreement = bool(settings.free_trade_setting)

    if settings.remove_barriers_selected:
        proto.removed_barriers.extend(_enum_values(settings.remove_barriers_selected))

    proto.galleon_water = settings.galleon_water
    proto.fungi_time = settings.fungi_time
    proto.shop_prices = settings.random_prices
    proto.activate_bananaports = settings.activate_all_bananaports

    if settings.faster_checks_selected:
        proto.faster_checks.extend(_enum_values(settings.faster_checks_selected))

    proto.puzzle_rando = settings.puzzle_rando_difficulty

    # Progressive switch strength (alter_switch_allocation + prog_slam_level_1..8).
    proto.progressive_switch_strength.enabled = bool(settings.alter_switch_allocation)
    proto.progressive_switch_strength.slam_levels.extend(int(getattr(settings, f"prog_slam_level_{i}")) for i in range(1, 9))


def _apply_requirement_settings(proto: requirement_settings_pb2.RequirementSettings, settings: "Settings") -> None:
    """Apply RequirementSettings proto to Settings object."""
    settings.blocker_selection_behavior = proto.b_locker_option.opt
    settings.BLockerEntryCount = list(proto.b_locker_option.amounts)
    settings.blocker_max = proto.b_locker_option.maximum
    settings.maximize_helm_blocker = bool(proto.maximize_helm_b_locker)

    settings.tns_selection_behavior = proto.tns_option.opt
    settings.BossBananas = list(proto.tns_option.amounts)
    settings.troff_max = proto.tns_option.maximum

    settings.medal_jetpac_behavior = proto.medals_for_jetpac.opt
    settings.medal_requirement = proto.medals_for_jetpac.selected_quantity

    settings.pearl_mermaid_behavior = proto.pearls_for_mermaid.opt
    settings.mermaid_gb_pearls = proto.pearls_for_mermaid.selected_quantity

    settings.fairy_queen_behavior = proto.fairies_for_fairy_queen.opt
    settings.rareware_gb_fairies = proto.fairies_for_fairy_queen.selected_quantity

    settings.cb_medal_behavior_new = proto.cbs_for_medal.opt
    settings.medal_cb_req = proto.cbs_for_medal.selected_quantity

    settings.open_lobbies = bool(proto.open_lobbies)

    if proto.HasField("switchsanity"):
        settings.switchsanity_enabled = bool(proto.switchsanity.enabled)
        location_to_attr = {loc: attr for loc, attr in _SWITCHSANITY_LOCATIONS}
        for assignment in proto.switchsanity.switch_assignment:
            attr_name = location_to_attr.get(assignment.location)
            if attr_name:
                setattr(settings, attr_name, assignment.item)

    settings.smaller_shops = bool(proto.smaller_shops)
    settings.shops_dont_cost = bool(proto.tooie_style_shops)
    settings.free_trade_setting = bool(proto.free_trade_agreement)
    settings.remove_barriers_selected = list(proto.removed_barriers)
    settings.galleon_water = proto.galleon_water
    settings.fungi_time = proto.fungi_time
    settings.random_prices = proto.shop_prices
    settings.activate_all_bananaports = proto.activate_bananaports
    settings.faster_checks_selected = list(proto.faster_checks)
    settings.puzzle_rando_difficulty = proto.puzzle_rando
    settings.alter_switch_allocation = bool(proto.progressive_switch_strength.enabled)
    slam_levels = list(proto.progressive_switch_strength.slam_levels)
    for i in range(1, 9):
        if i - 1 < len(slam_levels):
            try:
                setattr(settings, f"prog_slam_level_{i}", SlamRequirement(int(slam_levels[i - 1])))
            except ValueError:
                setattr(settings, f"prog_slam_level_{i}", int(slam_levels[i - 1]))


# =============================================================================
# Overworld settings
# =============================================================================
# Add a new kong model / helm-hurry timer / hard-mode toggle / hard-boss
# toggle: append one row to the matching table below. Other new simple
# settings need an explicit line in both _populate_* and _apply_*.

# (kong_models proto field, Settings attribute).
_KONG_MODEL_FIELDS: Tuple[Tuple[str, str], ...] = (
    ("dk_model", "kong_model_dk"),
    ("diddy_model", "kong_model_diddy"),
    ("lanky_model", "kong_model_lanky"),
    ("tiny_model", "kong_model_tiny"),
    ("chunky_model", "kong_model_chunky"),
    ("mode", "kong_model_mode"),
)

# (helm_hurry_mode proto field, Settings attribute).
_HELM_HURRY_FIELDS: Tuple[Tuple[str, str], ...] = (
    ("starting_time", "helmhurry_list_starting_time"),
    ("golden_banana_time", "helmhurry_list_golden_banana"),
    ("blueprint_time", "helmhurry_list_blueprint"),
    ("company_coin_time", "helmhurry_list_company_coins"),
    ("move_time", "helmhurry_list_move"),
    ("banana_medal_time", "helmhurry_list_banana_medal"),
    ("rainbow_coin_time", "helmhurry_list_rainbow_coin"),
    ("boss_key_time", "helmhurry_list_boss_key"),
    ("battle_crown_time", "helmhurry_list_battle_crown"),
    ("bean_time", "helmhurry_list_bean"),
    ("pearl_time", "helmhurry_list_pearl"),
    ("kong_time", "helmhurry_list_kongs"),
    ("fairy_time", "helmhurry_list_fairy"),
    ("cb_time", "helmhurry_list_colored_bananas"),
    ("trap_time", "helmhurry_list_ice_traps"),
)

# Proto bool fields on hard_mode. Each name must match a HardModeSelected
# enum member (proto field name == enum member name).
_HARD_MODE_FIELDS: Tuple[str, ...] = (
    "hard_enemies",
    "water_is_lava",
    "reduced_fall_damage_threshold",
    "shuffled_jetpac_enemies",
    "lower_max_refill_amounts",
    "strict_helm_timer",
    "donk_in_the_dark_world",
    "donk_in_the_sky",
    "angry_caves",
    "fast_balloons",
)

# Proto bool fields on hard_bosses. Each name must match a HardBossesSelected
# enum member.
_HARD_BOSSES_FIELDS: Tuple[str, ...] = (
    "fast_mad_jack",
    "alternative_mad_jack_kongs",
    "pufftoss_star_rando",
    "pufftoss_star_raised",
    "kut_out_phase_rando",
    "k_rool_toes_rando",
    "beta_lanky_phase",
)


def _populate_overworld_settings(settings: "Settings", proto: overworld_settings_pb2.OverworldSettings) -> None:
    """Populate OverworldSettings proto from Settings object."""

    # World navigation
    proto.entrance_randomizer = settings.level_randomization
    proto.shuffle_helm_location = bool(settings.shuffle_helm_location)
    proto.cross_map_bananaports = settings.bananaport_rando
    proto.random_starting_region = settings.random_starting_region_new

    # Kong models
    for proto_field, settings_attr in _KONG_MODEL_FIELDS:
        setattr(proto.kong_models, proto_field, getattr(settings, settings_attr))

    # Location randomizers. Dirt patches / fairies / crates are derived from
    # whether their matching enum value appears in item_rando_list_selected.
    item_rando_values = {_enum_value(x) for x in (settings.item_rando_list_selected or [])}
    proto.dirt_patch_randomizer = 0 in item_rando_values
    proto.banana_coin_randomizer = bool(settings.coin_rando)
    proto.banana_fairy_randomizer = 2 in item_rando_values
    proto.melon_crate_randomizer = 3 in item_rando_values
    proto.battle_crown_randomizer = bool(settings.crown_placement_rando)
    proto.race_coin_randomizer = bool(settings.race_coin_rando)
    proto.randomize_pickups = bool(settings.randomize_pickups)
    proto.shuffle_shop_locations = bool(settings.shuffle_shops)

    # CB randomizer
    proto.cb_randomizer.enabled = bool(settings.cb_rando_enabled)
    if settings.cb_rando_list_selected:
        proto.cb_randomizer.cb_randomized_levels.extend(_enum_values(settings.cb_rando_list_selected))

    proto.kasplat_randomizer = settings.kasplat_rando_setting

    # Bananaport randomizer (Settings does not keep a placement list, only the opt).
    proto.bananaport_randomizer.opt = settings.bananaport_placement_rando

    proto.wrinky_door_randomizer = bool(settings.wrinkly_location_rando)
    proto.tns_portal_randomizer = bool(settings.tns_location_rando)
    proto.vanilla_door_shuffle = bool(settings.vanilla_door_rando)
    proto.dos_doors = bool(settings.dos_door_rando)
    proto.dk_portal_randomizer = settings.dk_portal_location_rando_v2

    # Bosses
    proto.shuffle_boss_location = bool(settings.boss_location_rando)
    proto.krool_in_boss_pool = settings.krool_in_boss_pool_v2
    if settings.bosses_selected:
        proto.bosses_selected.extend(_enum_values(settings.bosses_selected))
    proto.ship_location_rando = bool(settings.ship_location_rando)

    # Enemies
    if settings.enemies_selected:
        proto.shuffled_enemies.extend(_enum_values(settings.enemies_selected))
    proto.crown_enemies = settings.crown_enemy_difficulty
    proto.random_enemy_speed = bool(settings.enemy_speed_rando)
    proto.random_enemy_size = bool(settings.randomize_enemy_sizes)

    # Bonus barrels
    if settings.minigames_list_selected:
        proto.shuffled_bonus_barrels.extend(_enum_values(settings.minigames_list_selected))
    proto.disable_hard_minigames = bool(settings.disable_hard_minigames)
    proto.auto_complete_bonus_barrels = bool(settings.bonus_barrel_auto_complete)
    proto.alternate_minecart_mayhem = bool(settings.alt_minecart_mayhem)

    # Difficulty
    proto.no_heals = bool(settings.no_healing)
    proto.no_melon_slice_drops = bool(settings.no_melons)
    proto.ice_traps_damage_player = bool(settings.ice_traps_damage)
    proto.mirror_mode = bool(settings.mirror_mode)
    proto.tag_barrels_disabled = bool(settings.disable_tag_barrels)

    # Helm hurry
    proto.helm_hurry_mode.enabled = bool(settings.helm_hurry)
    if settings.helm_hurry:
        for proto_field, settings_attr in _HELM_HURRY_FIELDS:
            setattr(proto.helm_hurry_mode, proto_field, getattr(settings, settings_attr))

    proto.no_consumable_upgrades = bool(settings.no_consumable_upgrades)

    # Hard mode / hard bosses: each proto bool field is named identically to
    # its corresponding selected-list enum member.
    if settings.hard_mode_selected:
        for field in _HARD_MODE_FIELDS:
            setattr(proto.hard_mode, field, HardModeSelected[field] in settings.hard_mode_selected)
    if settings.hard_bosses_selected:
        for field in _HARD_BOSSES_FIELDS:
            setattr(proto.hard_bosses, field, HardBossesSelected[field] in settings.hard_bosses_selected)

    proto.damage = settings.damage_amount


def _apply_overworld_settings(proto: overworld_settings_pb2.OverworldSettings, settings: "Settings") -> None:
    """Apply OverworldSettings proto to Settings object."""

    settings.level_randomization = proto.entrance_randomizer
    settings.shuffle_helm_location = bool(proto.shuffle_helm_location)
    settings.bananaport_rando = proto.cross_map_bananaports
    settings.random_starting_region_new = proto.random_starting_region

    for proto_field, settings_attr in _KONG_MODEL_FIELDS:
        setattr(settings, settings_attr, getattr(proto.kong_models, proto_field))

    settings.coin_rando = bool(proto.banana_coin_randomizer)
    settings.crown_placement_rando = bool(proto.battle_crown_randomizer)
    settings.race_coin_rando = bool(proto.race_coin_randomizer)
    settings.randomize_pickups = bool(proto.randomize_pickups)
    settings.shuffle_shops = bool(proto.shuffle_shop_locations)

    settings.cb_rando_enabled = bool(proto.cb_randomizer.enabled)
    settings.cb_rando_list_selected = list(proto.cb_randomizer.cb_randomized_levels)

    settings.kasplat_rando_setting = proto.kasplat_randomizer
    settings.bananaport_placement_rando = proto.bananaport_randomizer.opt

    settings.wrinkly_location_rando = bool(proto.wrinky_door_randomizer)
    settings.tns_location_rando = bool(proto.tns_portal_randomizer)
    settings.vanilla_door_rando = bool(proto.vanilla_door_shuffle)
    settings.dos_door_rando = bool(proto.dos_doors)
    settings.dk_portal_location_rando_v2 = proto.dk_portal_randomizer

    settings.boss_location_rando = bool(proto.shuffle_boss_location)
    settings.krool_in_boss_pool_v2 = proto.krool_in_boss_pool
    settings.bosses_selected = list(proto.bosses_selected)
    settings.ship_location_rando = bool(proto.ship_location_rando)

    settings.enemies_selected = list(proto.shuffled_enemies)
    settings.crown_enemy_difficulty = proto.crown_enemies
    settings.enemy_speed_rando = bool(proto.random_enemy_speed)
    settings.randomize_enemy_sizes = bool(proto.random_enemy_size)

    settings.minigames_list_selected = list(proto.shuffled_bonus_barrels)
    settings.disable_hard_minigames = bool(proto.disable_hard_minigames)
    settings.bonus_barrel_auto_complete = bool(proto.auto_complete_bonus_barrels)
    settings.alt_minecart_mayhem = bool(proto.alternate_minecart_mayhem)

    settings.no_healing = bool(proto.no_heals)
    settings.no_melons = bool(proto.no_melon_slice_drops)
    settings.ice_traps_damage = bool(proto.ice_traps_damage_player)
    settings.mirror_mode = bool(proto.mirror_mode)
    settings.disable_tag_barrels = bool(proto.tag_barrels_disabled)

    settings.helm_hurry = bool(proto.helm_hurry_mode.enabled)
    if settings.helm_hurry:
        for proto_field, settings_attr in _HELM_HURRY_FIELDS:
            setattr(settings, settings_attr, getattr(proto.helm_hurry_mode, proto_field))

    settings.no_consumable_upgrades = bool(proto.no_consumable_upgrades)

    # Rebuild selected-lists from the booleans on hard_mode / hard_bosses.
    settings.hard_mode_selected = [HardModeSelected[field] for field in _HARD_MODE_FIELDS if getattr(proto.hard_mode, field)]
    settings.hard_bosses_selected = [HardBossesSelected[field] for field in _HARD_BOSSES_FIELDS if getattr(proto.hard_bosses, field)]

    settings.damage_amount = proto.damage


# =============================================================================
# Endgame settings
# =============================================================================


# HelmDoorItem <-> proto HelmDoorRequirementType. The two enums do NOT share
# numeric values, so raw int copies produce mismatches (e.g. vanilla=0 round-
# trips as UNSPECIFIED=0 which is fine, but medium_random=2 would decode as
# RANDOM_EASY=2). Explicit map required both directions.
_HELM_DOOR_ITEM_TO_PROTO: Dict[int, int] = {
    0: 0,  # vanilla       -> VANILLA
    1: 1,  # opened        -> OPEN
    2: 3,  # medium_random -> RANDOM_MEDIUM
    3: 5,  # req_gb        -> GOLDEN_BANANAS
    4: 6,  # req_bp        -> BLUEPRINTS
    5: 7,  # req_companycoins -> COMPANY_COINS
    6: 8,  # req_key       -> KEYS
    7: 9,  # req_medal     -> MEDALS
    8: 10,  # req_crown     -> CROWNS
    9: 11,  # req_fairy     -> FAIRIES
    10: 12,  # req_rainbowcoin -> RAINBOW_COINS
    11: 13,  # req_bean      -> BEAN
    12: 14,  # req_pearl     -> PEARLS
    13: 2,  # easy_random   -> RANDOM_EASY
    14: 4,  # hard_random   -> RANDOM_HARD
}
_PROTO_TO_HELM_DOOR_ITEM: Dict[int, int] = {v: k for k, v in _HELM_DOOR_ITEM_TO_PROTO.items()}


# Kongs (donkey=0..chunky=4, any=5) <-> proto KongId (UNSPECIFIED=0,
# DONKEY=1..CHUNKY=5). Kongs.any maps to UNSPECIFIED.
_KONG_TO_PROTO: Dict[int, int] = {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 0}
_PROTO_TO_KONG: Dict[int, int] = {v: k for k, v in _KONG_TO_PROTO.items()}


_BARRIER_TO_HELM_DOOR_ITEM_COMMON: Dict[int, int] = {
    0: 1,  # Nothing -> opened
    3: 3,  # GoldenBanana -> req_gb
    4: 4,  # Blueprint -> req_bp
    5: 9,  # Fairy -> req_fairy
    6: 6,  # Key -> req_key
    9: 7,  # Medal -> req_medal
    10: 11,  # Bean -> req_bean
    11: 12,  # Pearl -> req_pearl
    12: 10,  # RainbowCoin -> req_rainbowcoin
}


def _barrier_to_helm_door_item(value: Any, is_coin_door: bool) -> int:
    """Convert a stored crown/coin door value back to its HelmDoorItem int."""
    if value is None:
        return 0  # vanilla
    ival = int(value)

    if isinstance(value, HelmDoorItem):
        return ival
    if isinstance(value, BarrierItems):
        if is_coin_door and ival == int(BarrierItems.CompanyCoin):
            return 0  # vanilla
        if not is_coin_door and ival == int(BarrierItems.Crown):
            return 0  # vanilla
        if is_coin_door and ival == int(BarrierItems.Crown):
            return 8  # req_crown
        if not is_coin_door and ival == int(BarrierItems.CompanyCoin):
            return 5  # req_companycoins
        return _BARRIER_TO_HELM_DOOR_ITEM_COMMON.get(ival, 0)
    # Bare int fallback: assume pre-resolve HelmDoorItem value.
    return ival


def _populate_endgame_settings(settings: "Settings", proto: endgame_settings_pb2.EndgameSettings) -> None:
    """Populate EndgameSettings proto from Settings object."""
    # Logic
    proto.logic.type = settings.logic_type
    if settings.glitches_selected:
        proto.logic.glitches.extend(_enum_values(settings.glitches_selected))
    if settings.tricks_selected:
        proto.logic.tricks.extend(_enum_values(settings.tricks_selected))

    # Win condition
    proto.win_condition.type = settings.win_condition_item
    proto.win_condition.quantity = settings.win_condition_count
    proto.win_condition.spawns_ship = bool(settings.win_condition_spawns_ship)

    # Required keys
    proto.required_keys.random_quantity = bool(settings.select_keys)
    proto.required_keys.specified_quantity = settings.krool_key_count
    if settings.starting_keys_list_selected:
        proto.required_keys.specified_starting_keys.extend(_enum_values(settings.starting_keys_list_selected))
    proto.required_keys.helm_key_lock = bool(settings.key_8_helm)
    proto.required_keys.key_8_required = bool(settings.k_rool_vanilla_requirement)
    proto.required_keys.random_quantity = bool(settings.keys_random)

    # Starting Kongs
    proto.starting_kongs.random_quantity = bool(settings.kong_rando)
    proto.starting_kongs.specified_quantity = settings.starting_kongs_count
    proto.starting_kongs.specified_starting_kong = _KONG_TO_PROTO.get(int(settings.starting_kong), 0)
    proto.starting_kongs.random_quantity = bool(settings.starting_random)

    # Helm settings. helm_setting serves double duty as both specified length
    # and helm start location.
    proto.helm_settings.random_length = bool(settings.helm_barrels == 1)  # MinigameBarrels.random
    proto.helm_settings.specified_length = settings.helm_setting if settings.helm_setting else 0
    proto.helm_settings.shuffle_helm_rooms = bool(settings.helm_phase_order_rando)
    proto.helm_settings.helm_start_location = settings.helm_setting
    proto.helm_settings.helm_room_bonus_count = settings.helm_room_bonus_count
    proto.helm_settings.random_length = bool(settings.helm_random)

    # Always emit exactly two entries so index [0] = crown door, [1] = coin door.
    crown_req = proto.helm_settings.helm_door_requirements.add()
    crown_req.type = _HELM_DOOR_ITEM_TO_PROTO.get(_barrier_to_helm_door_item(settings.crown_door_item, is_coin_door=False), 0)
    crown_req.specified_quantity = settings.crown_door_item_count
    coin_req = proto.helm_settings.helm_door_requirements.add()
    coin_req.type = _HELM_DOOR_ITEM_TO_PROTO.get(_barrier_to_helm_door_item(settings.coin_door_item, is_coin_door=True), 0)
    coin_req.specified_quantity = settings.coin_door_item_count

    # K. Rool settings
    proto.k_rool_settings.shuffle_k_rool_phases = bool(settings.krool_phase_order_rando)
    proto.k_rool_settings.random_phase_amount = bool(settings.krool_random)
    proto.k_rool_settings.specified_phase_amount = settings.krool_phase_count
    proto.k_rool_settings.dk_phase_requires_blast = bool(settings.cannons_require_blast)
    proto.k_rool_settings.chunky_phase_slam_requirement = settings.chunky_phase_slam_req


def _apply_endgame_settings(proto: endgame_settings_pb2.EndgameSettings, settings: "Settings") -> None:
    """Apply EndgameSettings proto to Settings object."""
    settings.logic_type = proto.logic.type
    settings.glitches_selected = list(proto.logic.glitches)
    settings.tricks_selected = list(proto.logic.tricks)

    settings.win_condition_item = proto.win_condition.type
    settings.win_condition_count = proto.win_condition.quantity
    settings.win_condition_spawns_ship = bool(proto.win_condition.spawns_ship)

    settings.select_keys = bool(proto.required_keys.random_quantity)
    settings.krool_key_count = proto.required_keys.specified_quantity
    settings.starting_keys_list_selected = list(proto.required_keys.specified_starting_keys)
    settings.key_8_helm = bool(proto.required_keys.helm_key_lock)
    settings.k_rool_vanilla_requirement = bool(proto.required_keys.key_8_required)
    settings.keys_random = bool(proto.required_keys.random_quantity)

    settings.kong_rando = bool(proto.starting_kongs.random_quantity)
    settings.starting_kongs_count = proto.starting_kongs.specified_quantity
    settings.starting_kong = Kongs(_PROTO_TO_KONG.get(int(proto.starting_kongs.specified_starting_kong), 5))
    settings.starting_random = bool(proto.starting_kongs.random_quantity)

    if proto.helm_settings.random_length:
        settings.helm_barrels = 1  # MinigameBarrels.random
    settings.helm_setting = proto.helm_settings.helm_start_location if proto.helm_settings.helm_start_location else proto.helm_settings.specified_length
    settings.helm_phase_order_rando = bool(proto.helm_settings.shuffle_helm_rooms)
    settings.helm_room_bonus_count = proto.helm_settings.helm_room_bonus_count
    settings.helm_random = bool(proto.helm_settings.random_length)

    reqs = proto.helm_settings.helm_door_requirements
    if len(reqs) > 0:
        settings.crown_door_item = HelmDoorItem(_PROTO_TO_HELM_DOOR_ITEM.get(int(reqs[0].type), 0))
        settings.crown_door_item_count = reqs[0].specified_quantity
    if len(reqs) > 1:
        settings.coin_door_item = HelmDoorItem(_PROTO_TO_HELM_DOOR_ITEM.get(int(reqs[1].type), 0))
        settings.coin_door_item_count = reqs[1].specified_quantity

    settings.krool_phase_order_rando = bool(proto.k_rool_settings.shuffle_k_rool_phases)
    settings.krool_random = bool(proto.k_rool_settings.random_phase_amount)
    settings.krool_phase_count = proto.k_rool_settings.specified_phase_amount
    settings.cannons_require_blast = bool(proto.k_rool_settings.dk_phase_requires_blast)
    settings.chunky_phase_slam_req = proto.k_rool_settings.chunky_phase_slam_requirement


# =============================================================================
# Quality of life settings
# =============================================================================
# Add a new simple bool toggle: append a row to _QOL_BOOL_FIELDS.
# Add a new MiscChanges bool (proto field name matches enum member):
# append the name to _MISC_CHANGES_FIELDS.
# Add a new spoiler-hint points category: append a row to
# _SPOILER_POINTS_FIELDS. Anything else needs explicit lines in
# _populate_qol_settings and _apply_qol_settings.

# (QoL proto bool, Settings attribute) pairs for simple passthroughs.
_QOL_BOOL_FIELDS: Tuple[Tuple[str, str], ...] = (
    ("tag_anywhere", "enable_tag_anywhere"),
    ("fast_warps", "fast_warps"),
    ("portal_numbers", "portal_numbers"),
    ("item_reward_previews", "item_reward_previews"),
    ("auto_key_turn_ins", "auto_keys"),
    ("warp_to_isles", "warp_to_isles"),
    ("shorten_boss_fights", "shorten_boss"),
    ("shop_indicator", "shop_indicator"),
    ("disable_racing_patches", "disable_racing_patches"),
    ("less_fragile_boulders", "less_fragile_boulders"),
)

# Proto bool fields on misc_changes. Each name must match a
# MiscChangesSelected enum member.
_MISC_CHANGES_FIELDS: Tuple[str, ...] = (
    "auto_dance_skip",
    "fast_boot",
    "calm_caves",
    "animal_buddies_grab_items",
    "reduced_lag",
    "remove_extraneous_cutscenes",
    "hint_textbox_hold",
    "remove_wrinkly_puzzles",
    "fast_picture_taking",
    "hud_hotkey",
    "ammo_swap",
    "homing_balloons",
    "fast_transform_animation",
    "troff_n_scoff_audio_indicator",
    "lowered_aztec_lobby_bonus",
    "quicker_galleon_star",
    "vanilla_bug_fixes",
    "save_k_rool_progress",
    "small_bananas_always_visible",
    "fast_hints",
    "brighten_mad_maze_maul_enemies",
    "raise_fungi_dirt_patch",
    "global_instrument",
    "fast_pause_transitions",
    "cannon_game_better_control",
    "better_fairy_camera",
    "remove_enemy_cabin_timer",
    "remove_galleon_ship_timers",
    "japes_bridge_permanently_extended",
    "move_spring_cabin_rocketbarrel",
)

# (spoiler_hints.points proto field, Settings attribute).
_SPOILER_POINTS_FIELDS: Tuple[Tuple[str, str], ...] = (
    ("kongs", "points_list_kongs"),
    ("keys", "points_list_keys"),
    ("shopkeepers", "points_list_shopkeepers"),
    ("guns", "points_list_guns"),
    ("instruments", "points_list_instruments"),
    ("training_moves", "points_list_training_moves"),
    ("important_shared", "points_list_important_shared"),
    ("fairy_moves", "points_list_fairy_moves"),
    ("pad_moves", "points_list_pad_moves"),
    ("barrel_moves", "points_list_barrel_moves"),
    ("active_moves", "points_list_active_moves"),
    ("bean", "points_list_bean"),
)


def _populate_qol_settings(settings: "Settings", proto: qol_settings_pb2.QualityOfLifeSettings) -> None:
    """Populate QualityOfLifeSettings proto from Settings object."""

    for proto_field, settings_attr in _QOL_BOOL_FIELDS:
        setattr(proto, proto_field, bool(getattr(settings, settings_attr)))
    proto.enemy_kill_crown_timer = bool(settings.enemy_kill_crown_timer != CrownEnemyRando.off)

    proto.cutscene_skips = settings.more_cutscene_skips

    # MiscChanges: each proto bool mirrors an enum member of MiscChangesSelected.
    for field in _MISC_CHANGES_FIELDS:
        setattr(proto.misc_changes, field, MiscChangesSelected[field] in settings.misc_changes_selected)

    # Hints
    proto.hints.wrinkly_hints = settings.wrinkly_hints
    proto.hints.shop_hints = bool(settings.enable_shop_hints)
    proto.hints.dim_solved_hints = bool(settings.dim_solved_hints)
    proto.hints.no_joke_hints = bool(settings.serious_hints)
    proto.hints.kongless_hint_doors = bool(settings.wrinkly_available)
    proto.hints.extra_hints = settings.microhints_enabled

    proto.hints.progressive_hints.item = settings.progressive_hint_item
    proto.hints.progressive_hints.count_for_35th_hint = int(settings.progressive_hint_count)
    proto.hints.progressive_hints.hint_curve = settings.progressive_hint_algorithm

    proto.hints.spoiler_hints.type = settings.spoiler_hints
    proto.hints.spoiler_hints.include_woth_count = bool(settings.spoiler_include_woth_count)
    proto.hints.spoiler_hints.include_level_order = bool(settings.spoiler_include_level_order)

    for proto_field, settings_attr in _SPOILER_POINTS_FIELDS:
        setattr(proto.hints.spoiler_hints.points, proto_field, int(getattr(settings, settings_attr)))


def _apply_qol_settings(proto: qol_settings_pb2.QualityOfLifeSettings, settings: "Settings") -> None:
    """Apply QualityOfLifeSettings proto to Settings object."""

    for proto_field, settings_attr in _QOL_BOOL_FIELDS:
        setattr(settings, settings_attr, bool(getattr(proto, proto_field)))
    settings.enemy_kill_crown_timer = bool(proto.enemy_kill_crown_timer)

    settings.more_cutscene_skips = proto.cutscene_skips

    settings.misc_changes_selected = [MiscChangesSelected[field] for field in _MISC_CHANGES_FIELDS if getattr(proto.misc_changes, field)]

    settings.wrinkly_hints = proto.hints.wrinkly_hints
    settings.enable_shop_hints = bool(proto.hints.shop_hints)
    settings.dim_solved_hints = bool(proto.hints.dim_solved_hints)
    settings.serious_hints = bool(proto.hints.no_joke_hints)
    settings.wrinkly_available = bool(proto.hints.kongless_hint_doors)
    settings.microhints_enabled = proto.hints.extra_hints

    settings.progressive_hint_item = proto.hints.progressive_hints.item
    settings.progressive_hint_count = int(proto.hints.progressive_hints.count_for_35th_hint)
    settings.progressive_hint_algorithm = proto.hints.progressive_hints.hint_curve

    settings.spoiler_hints = proto.hints.spoiler_hints.type
    settings.spoiler_include_woth_count = bool(proto.hints.spoiler_hints.include_woth_count)
    settings.spoiler_include_level_order = bool(proto.hints.spoiler_hints.include_level_order)

    for proto_field, settings_attr in _SPOILER_POINTS_FIELDS:
        setattr(settings, settings_attr, int(getattr(proto.hints.spoiler_hints.points, proto_field)))


# =============================================================================
# Plandomizer settings (not yet implemented)
# =============================================================================


def _populate_plandomizer_settings(settings: "Settings", proto: plandomizer_settings_pb2.PlandomizerSettings) -> None:
    """Populate PlandomizerSettings proto from Settings object.

    TODO: Map the complex plandomizer_dict structure (plando_starting_exit,
    plando_starting_kongs_selected, plando_*_order_N, plando_dirt_patches,
    plando_melon_crates, plando_battle_arenas, item/minigame/hint/shop
    assignments, custom_location_assignments, ...) into proto fields.
    """
    pass


def _apply_plandomizer_settings(proto: plandomizer_settings_pb2.PlandomizerSettings, settings: "Settings") -> None:
    """Apply PlandomizerSettings proto to Settings object (not yet implemented)."""
    pass


# =============================================================================
# Fill Result serialization
# =============================================================================


def fill_result_to_proto(spoiler: "Spoiler") -> fill_result_pb2.FillResult:
    """Convert a post-Fill Spoiler object to a FillResult protobuf message.

    Serializes everything the ROM patcher needs that is not already captured
    in SettingsInfo.
    """
    proto = fill_result_pb2.FillResult()
    _populate_location_assignments(spoiler, proto.location_assignments)
    _populate_move_shop_data(spoiler, proto.move_shop_data)
    _populate_shuffle_data(spoiler, proto.shuffle_data)
    _populate_placement_data(spoiler, proto.placement_data)
    _populate_hint_data(spoiler, proto.hint_data)
    _populate_path_data(spoiler, proto.path_data)
    _populate_misc_patching_data(spoiler, proto.misc_data)
    return proto


# -----------------------------------------------------------------------------
# Location assignments
# -----------------------------------------------------------------------------


def _populate_location_assignments(spoiler: "Spoiler", proto: fill_result_pb2.LocationAssignments) -> None:
    """Populate LocationAssignments from spoiler.LocationList."""
    for location_id, location in spoiler.LocationList.items():
        if location.item is not None:
            proto.assignments[int(location_id)] = int(location.item)


# -----------------------------------------------------------------------------
# Move shop data
# -----------------------------------------------------------------------------

# (move_type string, MoveEntry submessage name). The field names are all the
# move_type with "_move" appended, so we key off move_type directly.
_MOVE_ENTRY_TYPES: Tuple[str, ...] = (
    "special",
    "slam",
    "gun",
    "ammo_belt",
    "instrument",
)


def _populate_move_entry(move_dict: Any, proto: fill_result_pb2.MoveEntry) -> None:
    """Populate a single MoveEntry from a move dictionary."""
    if not isinstance(move_dict, dict):
        proto.empty_move.CopyFrom(fill_result_pb2.EmptyMove())
        return

    move_type = move_dict.get("move_type")
    if move_type is None:
        proto.empty_move.CopyFrom(fill_result_pb2.EmptyMove())
    elif move_type == "flag":
        proto.flag_move.flag = move_dict.get("flag", "")
        proto.flag_move.price = move_dict.get("price", 0)
    elif move_type in _MOVE_ENTRY_TYPES:
        sub = getattr(proto, f"{move_type}_move")
        sub.move_lvl = move_dict.get("move_lvl", 0)
        sub.move_kong = move_dict.get("move_kong", 0)
        sub.price = move_dict.get("price", 0)


def _populate_move_shop_data(spoiler: "Spoiler", proto: fill_result_pb2.MoveShopData) -> None:
    """Populate MoveShopData from spoiler.move_data.

    ``move_data`` layout: [shop_moves (4-deep nested), training_barrels, bfi_moves].
    """
    move_data = spoiler.move_data

    # Index 0: Shop moves, structure shop_type -> shop_index -> kong -> move.
    if len(move_data) > 0 and isinstance(move_data[0], list):
        for shop_type_data in move_data[0]:
            shop_type_proto = proto.shop_types.add()
            for shop_index_data in shop_type_data:
                shop_index_proto = shop_type_proto.shop_indices.add()
                for kong_moves_data in shop_index_data:
                    kong_moves_proto = shop_index_proto.kong_moves.add()
                    for move_entry in kong_moves_data:
                        _populate_move_entry(move_entry, kong_moves_proto.moves.add())

    # Index 1: Training barrels.
    if len(move_data) > 1 and isinstance(move_data[1], list):
        for move_entry in move_data[1]:
            _populate_move_entry(move_entry, proto.training_barrels.add())

    # Index 2: BFI moves.
    if len(move_data) > 2 and isinstance(move_data[2], list):
        for move_entry in move_data[2]:
            _populate_move_entry(move_entry, proto.bfi_moves.add())


# -----------------------------------------------------------------------------
# Shuffle data
# -----------------------------------------------------------------------------


def _populate_shuffle_data(spoiler: "Spoiler", proto: fill_result_pb2.ShuffleData) -> None:
    """Populate ShuffleData from spoiler shuffle dictionaries."""
    # Shuffled exits. TransitionFront exposes .dest/.exit; TransitionBack
    # exposes .regionId/.name - handle both shapes.
    for exit_id, exit_dest in spoiler.shuffled_exit_data.items():
        exit_proto = proto.shuffled_exits[int(exit_id)]
        if hasattr(exit_dest, "dest"):
            exit_proto.destination_region = int(exit_dest.dest)
            exit_proto.exit_name = getattr(exit_dest, "exit", "")
        elif hasattr(exit_dest, "regionId"):
            exit_proto.destination_region = int(exit_dest.regionId)
            exit_proto.exit_name = getattr(exit_dest, "name", "")
        else:
            exit_proto.destination_region = int(getattr(exit_dest, "dest", getattr(exit_dest, "regionId", 0)))
            exit_proto.exit_name = getattr(exit_dest, "exit", getattr(exit_dest, "name", ""))
        reverse = getattr(exit_dest, "reverse", None)
        exit_proto.reverse_transition = int(reverse) if reverse is not None else 0
        exit_proto.spoiler_name = getattr(exit_dest, "spoilerName", "")

    # Shuffled barrels (may be a MinigameLocationData wrapper or a raw enum).
    for location_id, minigame_data in spoiler.shuffled_barrel_data.items():
        value = minigame_data.minigame if hasattr(minigame_data, "minigame") else minigame_data
        proto.shuffled_barrels[int(location_id)] = int(value)

    # Shuffled doors. Each level maps to a list of tuples whose shape varies by
    # door type; downstream (DoorPlacer.place_door_locations) reads them by
    # positional index, so we preserve tuple contents verbatim.
    for level, door_list in spoiler.shuffled_door_data.items():
        shuffle_proto = proto.shuffled_doors.add()
        shuffle_proto.level = int(level)
        for entry in door_list:
            door_proto = shuffle_proto.doors.add()
            door_proto.door_location = int(entry[0])
            door_proto.door_type = str(int(entry[1]))
            if len(entry) > 2 and entry[2] is not None:
                door_proto.kong_assignee = int(entry[2])

    for instruction in spoiler.shuffled_exit_instructions:
        serializable = {
            "container_map": int(instruction["container_map"]),
            "zones": [{k: int(v) for k, v in zone.items()} for zone in instruction.get("zones", [])],
        }
        proto.exit_instructions.append(json.dumps(serializable))

    # Port connections
    if hasattr(spoiler, "port_connections"):
        for port_id, connection in spoiler.port_connections.items():
            port_proto = proto.port_connections[int(port_id)]
            if hasattr(connection, "dest"):
                port_proto.destination_region = int(connection.dest)
            if hasattr(connection, "map"):
                port_proto.destination_map = int(connection.map)
            if hasattr(connection, "exit"):
                port_proto.destination_exit = int(connection.exit)

    # Human-readable warps
    if hasattr(spoiler, "warp_data"):
        for warp in spoiler.warp_data:
            warp_proto = proto.warp_data.add()
            warp_proto.from_location = warp.get("from", "")
            warp_proto.to = warp.get("to", "")

    # Crown arenas – crown_locations is {Levels: {crown_index: subindex}}
    if hasattr(spoiler, "crown_locations") and spoiler.crown_locations:
        for level, crown_data in spoiler.crown_locations.items():
            for crown_index, subindex in crown_data.items():
                crown_proto = proto.crown_placements.add()
                crown_proto.level = int(_enum_value(level))
                crown_proto.crown_index = int(crown_index)
                crown_proto.subindex = int(subindex)

    # Dirt patches – each entry is {"name", "map", "level" (Levels enum), ...}
    if hasattr(spoiler, "dirt_patch_placement"):
        for patch in spoiler.dirt_patch_placement:
            patch_proto = proto.patch_placements.add()
            patch_proto.map_id = int(patch.get("map", 0))
            patch_proto.level = int(_enum_value(patch.get("level", 0)))
            patch_proto.name = str(patch.get("name", ""))

    # Melon crates – attribute is meloncrate_placement
    if hasattr(spoiler, "meloncrate_placement"):
        for crate in spoiler.meloncrate_placement:
            crate_proto = proto.crate_placements.add()
            crate_proto.map_id = int(crate.get("map", 0))
            crate_proto.level = int(_enum_value(crate.get("level", 0)))
            crate_proto.name = str(crate.get("name", ""))

    # Shop location shuffles – {Levels: {old_shop_region: new_shop_region}}
    if hasattr(spoiler, "shuffled_shop_locations") and spoiler.shuffled_shop_locations:
        for level, shop_map in spoiler.shuffled_shop_locations.items():
            shuffle_proto = proto.shuffled_shop_locations.add()
            shuffle_proto.level = int(_enum_value(level))
            for old_shop, new_shop in shop_map.items():
                assign = shuffle_proto.assignments.add()
                assign.old_shop = int(_enum_value(old_shop))
                assign.new_shop = int(_enum_value(new_shop))

    # Kasplat location shuffles – {name: kong_index}
    if hasattr(spoiler, "shuffled_kasplat_map") and spoiler.shuffled_kasplat_map:
        for name, kong in spoiler.shuffled_kasplat_map.items():
            proto.shuffled_kasplat_map[str(name)] = int(kong)

    # Fairy locations – {Levels: [fairy_indexes]}
    if hasattr(spoiler, "fairy_locations") and spoiler.fairy_locations:
        for level, indexes in spoiler.fairy_locations.items():
            fairy_proto = proto.fairy_locations.add()
            fairy_proto.level = int(_enum_value(level))
            fairy_proto.fairy_indexes.extend([int(i) for i in indexes])

    # Fairy data table – list of 20 dicts (or None)
    if hasattr(spoiler, "fairy_data_table") and spoiler.fairy_data_table:
        for entry in spoiler.fairy_data_table:
            entry_proto = proto.fairy_data_table.add()
            if entry is not None:
                entry_proto.present = True
                entry_proto.fairy_index = int(entry.get("fairy_index", 0))
                entry_proto.level = int(_enum_value(entry.get("level", 0)))
                entry_proto.flag = int(entry.get("flag", 0))
                entry_proto.id = int(entry.get("id", 0))
                entry_proto.shift = int(entry.get("shift", 0))
                entry_proto.script_id = int(entry.get("script_id", 0))
                entry_proto.map_id = int(entry.get("map_id", 0))
            else:
                entry_proto.present = False

    # Bananaport replacements – [(new_pad_index, visual_type)]
    if hasattr(spoiler, "bananaport_replacements") and spoiler.bananaport_replacements:
        for pad_index, visual_type in spoiler.bananaport_replacements:
            bp_proto = proto.bananaport_replacements.add()
            bp_proto.new_pad_index = int(pad_index)
            bp_proto.visual_type = int(visual_type)

    # Warp locations – {warp_id: custom_location_id}
    if hasattr(spoiler, "warp_locations") and spoiler.warp_locations:
        for warp_id, loc_id in spoiler.warp_locations.items():
            proto.warp_locations[int(warp_id)] = int(loc_id)


# -----------------------------------------------------------------------------
# Placement data
# -----------------------------------------------------------------------------


def _populate_cb_location(loc: Any, loc_proto: Any) -> None:
    """Copy a CB spawn location (dict or 5-tuple) into its proto."""
    if isinstance(loc, dict):
        loc_proto.amount = int(loc.get("amount", 1))
        loc_proto.scale = float(loc.get("scale", 1.0))
        loc_proto.x = float(loc.get("x", 0))
        loc_proto.y = float(loc.get("y", 0))
        loc_proto.z = float(loc.get("z", 0))
    elif isinstance(loc, (list, tuple)) and len(loc) >= 5:
        loc_proto.amount = int(loc[0])
        loc_proto.scale = float(loc[1])
        loc_proto.x = float(loc[2])
        loc_proto.y = float(loc[3])
        loc_proto.z = float(loc[4])


def _populate_placement_data(spoiler: "Spoiler", proto: fill_result_pb2.PlacementData) -> None:
    """Populate PlacementData from spoiler placement lists."""
    # CB placements
    for cb_data in spoiler.cb_placements:
        cb_proto = proto.cb_placements.add()
        cb_proto.id = cb_data.get("id", 0)
        cb_proto.name = cb_data.get("name", "")
        cb_proto.kong = int(cb_data.get("kong", 0))
        cb_proto.level = int(cb_data.get("level", 0))
        cb_proto.type = cb_data.get("type", "")
        cb_proto.map = int(cb_data.get("map", 0))
        locations = cb_data.get("locations")
        if isinstance(locations, list):
            for loc in locations:
                _populate_cb_location(loc, cb_proto.locations.add())

    # Balloon placements
    for balloon_data in spoiler.balloon_placement:
        balloon_proto = proto.balloon_placements.add()
        balloon_proto.id = balloon_data.get("id", 0)
        balloon_proto.name = balloon_data.get("name", "")
        balloon_proto.kong = int(balloon_data.get("kong", 0))
        balloon_proto.level = int(balloon_data.get("level", 0))
        balloon_proto.map = int(balloon_data.get("map", 0))
        balloon_proto.score = balloon_data.get("score", 0)

    # Enemy replacements (kasplat swaps)
    for enemy_data in spoiler.enemy_replacements:
        enemy_proto = proto.enemy_replacements.add()
        enemy_proto.container_map = int(enemy_data.get("container_map", 0))
        for swap in enemy_data.get("kasplat_swaps", []):
            swap_proto = enemy_proto.kasplat_swaps.add()
            swap_proto.vanilla_location = int(swap.get("vanilla_location", 0))
            swap_proto.replace_with = int(swap.get("replace_with", 0))

    # Coin requirements
    for map_id, coin_count in spoiler.coin_requirements.items():
        proto.coin_requirements[int(map_id)] = int(coin_count)

    # Coin placements
    if hasattr(spoiler, "coin_placements"):
        for coin_data in spoiler.coin_placements:
            coin_proto = proto.coin_placements.add()
            coin_proto.level = int(_enum_value(coin_data.get("level", 0)))
            coin_proto.map = int(coin_data.get("map", 0))
            coin_proto.kong = int(_enum_value(coin_data.get("kong", 0)))
            coin_proto.type = coin_data.get("type", "")
            coin_proto.name = coin_data.get("name", "")
            for loc in coin_data.get("locations", []):
                loc_proto = coin_proto.locations.add()
                loc_proto.scale = float(loc[0])
                loc_proto.x = float(loc[1])
                loc_proto.y = float(loc[2])
                loc_proto.z = float(loc[3])

    # Race coin placements
    if hasattr(spoiler, "race_coin_placements"):
        for coin_data in spoiler.race_coin_placements:
            coin_proto = proto.race_coin_placements.add()
            coin_proto.map = int(coin_data.get("map", 0))
            coin_proto.level = int(_enum_value(coin_data.get("level", 0)))
            coin_proto.name = coin_data.get("name", "")
            for loc in coin_data.get("locations", []):
                loc_proto = coin_proto.locations.add()
                loc_proto.scale = float(loc[0])
                loc_proto.x = float(loc[1])
                loc_proto.y = float(loc[2])
                loc_proto.z = float(loc[3])

    # Pokemon Snap enemy data (for Krem Kapture win condition)
    if hasattr(spoiler, "pkmn_snap_data"):
        for spawned in spoiler.pkmn_snap_data:
            proto.pkmn_snap_data.append(bool(spawned))

    # Enemy rando data: map_id -> list of {enemy, speeds, id, location}.
    # Populated during Fill and consumed by randomize_enemies at patch time.
    enemy_rando_data = getattr(spoiler, "enemy_rando_data", None) or {}
    for map_id, entries in enemy_rando_data.items():
        map_proto = proto.enemy_rando_data[int(map_id)]
        for entry in entries or []:
            entry_proto = map_proto.entries.add()
            entry_proto.enemy = _to_int(entry.get("enemy", 0))
            for speed in entry.get("speeds") or []:
                try:
                    entry_proto.speeds.append(int(speed))
                except (TypeError, ValueError):
                    continue
            entry_proto.spawner_id = _to_int(entry.get("id", 0))
            entry_proto.location = str(entry.get("location", "") or "")


# -----------------------------------------------------------------------------
# Hint data
# -----------------------------------------------------------------------------


def _populate_hint_data(spoiler: "Spoiler", proto: fill_result_pb2.HintData) -> None:
    """Populate HintData from spoiler hint structures."""
    if hasattr(spoiler, "hintset"):
        proto.hint_set.max_hints = spoiler.hintset.hint_cap
        for hint in spoiler.hintset.hints:
            hint_proto = proto.hint_set.hints.add()
            hint_proto.location_id = int(hint.location) if hasattr(hint, "location") else 0
            hint_proto.hint_text = getattr(hint, "hint", "")
            hint_proto.important = getattr(hint, "important", False)
            hint_proto.priority = getattr(hint, "priority", 0)

    for hint_name, flag_value in spoiler.tied_hint_flags.items():
        proto.tied_hint_flags[hint_name] = int(flag_value)
    for region in spoiler.tied_hint_regions:
        proto.tied_hint_regions.append(int(region))

    microhints = getattr(spoiler, "microhints", None)
    if microhints:
        for item_name, hint_text in microhints.items():
            proto.microhints[str(item_name)] = str(hint_text)

    if hasattr(spoiler, "level_spoiler"):
        for level_id, level_hints in spoiler.level_spoiler.items():
            level_proto = proto.level_spoiler_hints[int(level_id)]
            if hasattr(level_hints, "vial_colors"):
                level_proto.vial_colors.extend(level_hints.vial_colors)
            if hasattr(level_hints, "points"):
                level_proto.points = level_hints.points
            if hasattr(level_hints, "woth_count"):
                level_proto.woth_count = level_hints.woth_count
            if hasattr(level_hints, "level_items"):
                for item_entry in level_hints.level_items:
                    item_proto = level_proto.level_items.add()
                    item_proto.item = int(_enum_value(item_entry.get("item", 0)))
                    item_proto.points = int(item_entry.get("points", 0))
                    item_proto.flag = int(item_entry.get("flag", 0))

    if hasattr(spoiler, "level_spoiler_human_readable"):
        for level_name, hint_text in spoiler.level_spoiler_human_readable.items():
            proto.level_spoiler_human_readable[level_name] = hint_text


# -----------------------------------------------------------------------------
# Path data
# -----------------------------------------------------------------------------


def _fill_int_path_map(src_dict: Any, dst_map: Any, key_cast: Any = int) -> None:
    """Copy {key: [loc_ids]} into a proto ``map<key, Path>`` field."""
    for key, path_locations in src_dict.items():
        path_proto = dst_map[key_cast(key)]
        for loc_id in path_locations:
            path_proto.locations.append(int(loc_id))


def _populate_path_data(spoiler: "Spoiler", proto: fill_result_pb2.PathData) -> None:
    """Populate PathData from spoiler path structures."""
    if hasattr(spoiler, "woth_locations"):
        for location_id in spoiler.woth_locations:
            proto.woth_locations.append(int(location_id))

    _fill_int_path_map(spoiler.woth_paths, proto.woth_paths, key_cast=int)
    _fill_int_path_map(spoiler.krool_paths, proto.krool_paths, key_cast=str)
    _fill_int_path_map(spoiler.rap_win_con_paths, proto.rap_win_con_paths, key_cast=str)
    _fill_int_path_map(spoiler.other_paths, proto.other_paths, key_cast=int)

    for location_id in spoiler.rabbit_path:
        proto.rabbit_path.append(int(location_id))

    # Playthrough (list of spheres, each sphere is {location_id: item_id}).
    if hasattr(spoiler, "playthrough") and isinstance(spoiler.playthrough, list):
        for sphere_dict in spoiler.playthrough:
            sphere_proto = proto.playthrough.add()
            for location_id, item_id in sphere_dict.items():
                loc_proto = sphere_proto.locations.add()
                loc_proto.location_id = int(location_id)
                loc_proto.item_id = int(item_id)

    if hasattr(spoiler, "majorItems"):
        for item_id in spoiler.majorItems:
            proto.major_items.append(int(item_id))
    if hasattr(spoiler, "foolish_region_names"):
        proto.foolish_region_names.extend([str(name) for name in spoiler.foolish_region_names])
    if hasattr(spoiler, "pathless_moves"):
        for item_id in spoiler.pathless_moves:
            proto.pathless_moves.append(int(item_id))

    # region_hintable_count: region -> item_name -> {plural, count, shuffled_locations[]}
    # shuffled_locations may hold ints or Location objects; reverse-lookup
    # Location objects via spoiler.LocationList to emit a plain id.
    if hasattr(spoiler, "region_hintable_count"):
        # Build an identity-keyed reverse lookup (Location object -> location id)
        # once up front. The previous implementation scanned spoiler.LocationList
        # linearly for every Location object, producing O(regions * items * locs
        # * len(LocationList)) behavior and a 20-30s hang before patching.
        loc_obj_to_id: Dict[int, int] = {}
        if hasattr(spoiler, "LocationList"):
            for loc_id, loc_obj in spoiler.LocationList.items():
                loc_obj_to_id[id(loc_obj)] = int(loc_id)

        for region_name, items_dict in spoiler.region_hintable_count.items():
            region_counts_proto = proto.region_hintable_count[str(region_name)]
            for item_name, item_data in items_dict.items():
                item_data_proto = region_counts_proto.items[item_name]
                item_data_proto.plural = item_data.get("plural", "")
                item_data_proto.count = item_data.get("count", 0)
                for loc in item_data.get("shuffled_locations", []):
                    if isinstance(loc, int):
                        item_data_proto.shuffled_locations.append(loc)
                    else:
                        mapped_id = loc_obj_to_id.get(id(loc))
                        if mapped_id is not None:
                            item_data_proto.shuffled_locations.append(mapped_id)

    if hasattr(spoiler, "accessible_hints_for_location"):
        for location_id, hints in spoiler.accessible_hints_for_location.items():
            hints_proto = proto.accessible_hints_for_location[int(location_id)]
            if isinstance(hints, list):
                hints_proto.hint_names.extend([str(h) for h in hints])


# -----------------------------------------------------------------------------
# Misc patching data
# -----------------------------------------------------------------------------


def _signed_int(val: Any, default: int = 0) -> int:
    """Coerce possibly-None / enum values to int for sint32 fields (-1 sentinel for None)."""
    if val is None:
        return -1
    try:
        return int(val)
    except (TypeError, ValueError):
        return default


def _populate_item_assignment(item_assign: Any, assign_proto: Any) -> None:
    """Copy a single LocationSelection onto its ItemAssignment proto."""
    assign_proto.old_type = _signed_int(getattr(item_assign, "old_type", None), -1)
    assign_proto.old_flag = _signed_int(getattr(item_assign, "old_flag", None), -1)
    assign_proto.old_item = _signed_int(getattr(item_assign, "old_item", None), -1)
    assign_proto.old_kong = _signed_int(getattr(item_assign, "old_kong", None), -1)

    # dict[map_id, actor_id]. Older code used the attribute name
    # "maps_to_actor_ids"; accept either.
    placement_map = getattr(item_assign, "placement_data", None)
    if placement_map is None:
        placement_map = getattr(item_assign, "maps_to_actor_ids", None)
    if placement_map:
        for map_id, actor_id in placement_map.items():
            try:
                assign_proto.maps_to_actor_ids[int(map_id)] = int(actor_id)
            except (TypeError, ValueError):
                continue

    location = getattr(item_assign, "location", None)
    assign_proto.location = int(location) if location is not None else 0
    assign_proto.new_flag = _signed_int(getattr(item_assign, "new_flag", None), -1)
    assign_proto.new_type = _signed_int(getattr(item_assign, "new_type", None), -1)
    assign_proto.new_item = _signed_int(getattr(item_assign, "new_item", None), -1)
    assign_proto.new_kong = _signed_int(getattr(item_assign, "new_kong", None), -1)
    assign_proto.shared = bool(getattr(item_assign, "shared", False))

    # placement_index is a list in LocationSelection (shared shop items write
    # to multiple slots); negative values are meaningful sentinels.
    pidx = getattr(item_assign, "placement_index", None)
    if isinstance(pidx, (list, tuple)):
        for v in pidx:
            try:
                assign_proto.placement_index.append(int(v))
            except (TypeError, ValueError):
                pass
    elif pidx is not None:
        try:
            assign_proto.placement_index.append(int(pidx))
        except (TypeError, ValueError):
            pass

    assign_proto.placement_subindex = int(getattr(item_assign, "placement_subindex", 0) or 0)
    assign_proto.is_reward_point = bool(getattr(item_assign, "reward_spot", False))
    assign_proto.is_shop = bool(getattr(item_assign, "is_shop", False))

    price = getattr(item_assign, "price", 0)
    if isinstance(price, (list, tuple)):
        assign_proto.price = int(price[0]) if price else 0
    else:
        try:
            assign_proto.price = int(price or 0)
        except (TypeError, ValueError):
            assign_proto.price = 0

    assign_proto.can_have_item = bool(getattr(item_assign, "can_have_item", True))
    assign_proto.can_place_item = bool(getattr(item_assign, "can_place_item", True))
    assign_proto.shop_locked = bool(getattr(item_assign, "shop_locked", False))
    assign_proto.order = int(getattr(item_assign, "order", 0) or 0)
    assign_proto.name = str(getattr(item_assign, "name", "") or "")
    assign_proto.move_name = str(getattr(item_assign, "move_name", "") or "")


def _populate_fill_time_settings(spoiler_settings: Any, proto: fill_result_pb2.MiscPatchingData) -> None:
    """Emit Fill-time-resolved Settings fields that the patcher reads directly.

    Many of these are rerolled during Fill (B.Locker/T&S chaos mode, starting
    Kongs resolution, K.Rool key randomization), so a fresh browser-side
    Settings rebuild would diverge from the spoiler log without this
    roundtrip.
    """
    # Per-level DK portal destinations. assignDKPortal sets exit=-1 to mean
    # "use map default entry"; sint32 preserves that.
    for entry in getattr(spoiler_settings, "level_portal_destinations", []) or []:
        dest_proto = proto.level_portal_destinations.add()
        dest_proto.map = int(entry["map"])
        dest_proto.exit = int(entry["exit"])
    for map_id in getattr(spoiler_settings, "level_void_maps", []) or []:
        proto.level_void_maps.append(int(map_id))

    # Fill-time resolved starting Kongs (concrete list/lead Kong chosen at Fill).
    for kong in getattr(spoiler_settings, "starting_kong_list", None) or []:
        try:
            proto.starting_kong_list.append(int(kong))
        except (TypeError, ValueError):
            continue
    resolved_starting_kong = getattr(spoiler_settings, "starting_kong", None)
    if resolved_starting_kong is not None:
        try:
            proto.resolved_starting_kong = int(resolved_starting_kong)
        except (TypeError, ValueError):
            pass

    # B.Locker / T&S arrays rolled/reordered during Fill.
    for count in getattr(spoiler_settings, "BLockerEntryCount", []) or []:
        try:
            proto.blocker_entry_counts.append(int(count))
        except (TypeError, ValueError):
            proto.blocker_entry_counts.append(0)
    for item in getattr(spoiler_settings, "BLockerEntryItems", []) or []:
        try:
            proto.blocker_entry_items.append(int(item))
        except (TypeError, ValueError):
            proto.blocker_entry_items.append(0)
    for count in getattr(spoiler_settings, "BossBananas", []) or []:
        try:
            proto.boss_bananas.append(int(count))
        except (TypeError, ValueError):
            proto.boss_bananas.append(0)

    # Switchsanity
    if getattr(spoiler_settings, "switchsanity_enabled", False):
        proto.switchsanity_enabled = True
    switchsanity_data = getattr(spoiler_settings, "switchsanity_data", None) or {}
    for switch_enum, info in switchsanity_data.items():
        kong = getattr(info, "kong", None)
        switch_type = getattr(info, "switch_type", None)
        if kong is None or switch_type is None:
            continue
        assignment = proto.switchsanity_data.add()
        assignment.switch = int(_enum_value(switch_enum))
        assignment.kong = int(_enum_value(kong))
        assignment.switch_type = int(_enum_value(switch_type))


def _populate_misc_patching_data(spoiler: "Spoiler", proto: fill_result_pb2.MiscPatchingData) -> None:
    """Populate MiscPatchingData from spoiler miscellaneous data."""
    # Item assignments (LocationSelection has many fields ItemRando reads directly).
    for item_assign in spoiler.item_assignment:
        _populate_item_assignment(item_assign, proto.item_assignments.add())

    for item_id in spoiler.valid_photo_items:
        proto.valid_photo_items.append(int(item_id))

    if getattr(spoiler, "arcade_item_reward", None) is not None:
        proto.arcade_item_reward = int(spoiler.arcade_item_reward)
    if getattr(spoiler, "jetpac_item_reward", None) is not None:
        proto.jetpac_item_reward = int(spoiler.jetpac_item_reward)

    # Music data
    for key, value in spoiler.music_bgm_data.items():
        proto.music_bgm_data[int(key)] = int(value)
    for key, value in spoiler.music_majoritem_data.items():
        proto.music_majoritem_data[int(key)] = int(value)
    for key, value in spoiler.music_minoritem_data.items():
        proto.music_minoritem_data[int(key)] = int(value)
    for key, value in spoiler.music_event_data.items():
        proto.music_event_data[int(key)] = int(value)

    # Text file changes are JSON-encoded per entry (dict shape varies).
    if hasattr(spoiler, "text_changes"):
        for file_id, changes_list in spoiler.text_changes.items():
            text_changes_proto = proto.text_file_changes[int(file_id)]
            for change_dict in changes_list:
                text_changes_proto.changes.append(json.dumps(change_dict))

    # Fill-time Settings fields the patcher reads directly from spoiler.settings.
    settings = getattr(spoiler, "settings", None)
    if settings is not None:
        _populate_fill_time_settings(settings, proto)

    for item_id in getattr(spoiler, "pregiven_items", None) or []:
        try:
            proto.pregiven_items.append(int(item_id))
        except (TypeError, ValueError):
            continue

    first_move_item = getattr(spoiler, "first_move_item", None)
    if first_move_item is not None:
        try:
            proto.first_move_item = int(first_move_item)
        except (TypeError, ValueError):
            pass

    # Archipelago flag + slot name are only meaningful when archipelago=True;
    # the patcher stamps the ROM header with player_name in that case.
    if settings is not None and getattr(settings, "archipelago", False):
        proto.archipelago = True
        player_name = getattr(settings, "player_name", None)
        if player_name:
            proto.player_name = str(player_name)

    # Fill-time K.Rool key requirement list (rerolled in Settings.__init__).
    krool_keys_required = getattr(settings, "krool_keys_required", None) if settings is not None else None
    if krool_keys_required:
        proto.krool_keys_required.extend([int(_enum_value(k)) for k in krool_keys_required])

    ship_location_index = getattr(spoiler, "ship_location_index", None)
    if ship_location_index is not None:
        try:
            proto.ship_location_index = int(ship_location_index)
        except (TypeError, ValueError):
            pass
    ship_name = getattr(spoiler, "ship_name", None)
    if ship_name:
        proto.ship_name = str(ship_name)

    # Switch allocation
    switch_allocation = getattr(settings, "switch_allocation", None) if settings is not None else None
    if switch_allocation:
        proto.switch_allocation.extend([int(_enum_value(x)) for x in switch_allocation])
