"""Settings serialization to/from Protocol Buffers."""

import base64
import json
import logging
import sys
import os
from typing import Any, Dict, Optional, TYPE_CHECKING

proto_gen_path = os.path.join(os.path.dirname(__file__), 'proto_gen')
if proto_gen_path not in sys.path:
    sys.path.insert(0, proto_gen_path)
from randomizer.proto_gen import settings_pb2
from randomizer.proto_gen import item_settings_pb2
from randomizer.proto_gen import requirement_settings_pb2
from randomizer.proto_gen import overworld_settings_pb2
from randomizer.proto_gen import endgame_settings_pb2
from randomizer.proto_gen import qol_settings_pb2
from randomizer.proto_gen import plandomizer_settings_pb2
from randomizer.proto_gen import fill_result_pb2

if TYPE_CHECKING:
    from randomizer.Settings import Settings
    from randomizer.Spoiler import Spoiler

logger = logging.getLogger(__name__)


def settings_to_proto(settings: "Settings") -> settings_pb2.SettingsInfo:
    """Convert a Settings object to a SettingsInfo protobuf message."""
    proto = settings_pb2.SettingsInfo()
    
    # Convert each settings category
    _populate_item_settings(settings, proto.item_settings)
    _populate_requirement_settings(settings, proto.requirement_settings)
    _populate_overworld_settings(settings, proto.overworld_settings)
    _populate_endgame_settings(settings, proto.endgame_settings)
    _populate_qol_settings(settings, proto.qol_settings)
    _populate_plandomizer_settings(settings, proto.plandomizer_settings)
    
    return proto


def proto_to_settings(proto: settings_pb2.SettingsInfo, settings: "Settings") -> None:
    """Apply settings from a SettingsInfo protobuf message to a Settings object.
    
    Args:
        proto: SettingsInfo protobuf message
        settings: Settings object to update
    """
    _apply_item_settings(proto.item_settings, settings)
    _apply_requirement_settings(proto.requirement_settings, settings)
    _apply_overworld_settings(proto.overworld_settings, settings)
    _apply_endgame_settings(proto.endgame_settings, settings)
    _apply_qol_settings(proto.qol_settings, settings)
    _apply_plandomizer_settings(proto.plandomizer_settings, settings)


def serialize_settings_to_base64(settings: "Settings") -> str:
    """Serialize a Settings object to a base64-encoded protobuf string.
    
    This creates a compact, copy-paste friendly representation of settings.
    Uses URL-safe base64 encoding to avoid issues with JSON transmission.
    
    Args:
        settings: Settings object to serialize
        
    Returns:
        URL-safe base64-encoded protobuf string
    """
    proto = settings_to_proto(settings)
    binary_data = proto.SerializeToString()
    return base64.urlsafe_b64encode(binary_data).decode('utf-8')


def deserialize_settings_from_base64(proto_string: str) -> settings_pb2.SettingsInfo:
    """Deserialize a base64-encoded protobuf string to a SettingsInfo message.
    
    Args:
        proto_string: URL-safe base64-encoded protobuf string
        
    Returns:
        SettingsInfo protobuf message
        
    Raises:
        ValueError: If the string cannot be decoded or parsed
    """
    try:
        try:
            binary_data = base64.urlsafe_b64decode(proto_string)
        except Exception:
            binary_data = base64.b64decode(proto_string)
        
        proto = settings_pb2.SettingsInfo()
        proto.ParseFromString(binary_data)
        return proto
    except Exception as e:
        raise ValueError(f"Failed to deserialize proto string: {e}")


def is_proto_settings_string(settings_string: str) -> bool:
    """Detect if a settings string is in protobuf format.
    
    Attempts to distinguish between the old custom base64 format and
    the new protobuf format by trying to parse as protobuf.
    
    Args:
        settings_string: Settings string to check
        
    Returns:
        True if the string appears to be a valid protobuf, False otherwise
    """
    try:
        deserialize_settings_from_base64(settings_string)
        return True
    except:
        return False


# Helper functions to populate proto messages from Settings
def _populate_item_settings(settings: "Settings", proto: item_settings_pb2.ItemSettings) -> None:
    """Populate ItemSettings proto from Settings object."""
    proto.decouple_item_rando = bool(settings.decouple_item_rando)
    is_decoupled = bool(settings.decouple_item_rando)
    
    # ItemPool - create one pool for each of the 10 lists to preserve exact distribution
    # Always create all 10 pools (even if empty) to maintain index mapping
    for i in range(10):
        pool = proto.pools.add()
        list_attr = f"item_rando_list_{i}"
        if hasattr(settings, list_attr):
            item_list = getattr(settings, list_attr)
            if item_list:
                # Extract .value from enums if they exist
                items = [x.value if hasattr(x, 'value') else x for x in item_list]
                
                # For decoupled mode, lists 0-4 are items, 5-9 are checks
                # For coupled mode, all lists are items
                if is_decoupled and i >= 5:
                    pool.checks.extend(items)
                else:
                    pool.items.extend(items)
    
    # StartingMovePool - multiple pools with items and count_given
    # Always create all 5 pools (even if empty) to maintain index mapping
    # Read from individual starting_moves_list_1 through _5 fields (not the combined lists)
    for i in range(1, 6):  # 1-5 inclusive
        move_pool = proto.starting_move_pools.add()
        # Use original lists (before progressive item conversion)
        # This preserves ProgressiveSlam2/3, ProgressiveAmmoBelt2, ProgressiveInstrumentUpgrade2/3
        original_list_attr = f"original_starting_moves_list_{i}"
        list_attr = f"starting_moves_list_{i}"
        count_attr = f"starting_moves_list_count_{i}"
        
        # Prefer original list if it exists, otherwise fall back to current list
        if hasattr(settings, original_list_attr):
            move_list = getattr(settings, original_list_attr)
        elif hasattr(settings, list_attr):
            move_list = getattr(settings, list_attr)
        else:
            move_list = None
            
        if move_list:
            items_with_values = [x.value if hasattr(x, 'value') else x for x in move_list]
            move_pool.items.extend(items_with_values)
        
        if hasattr(settings, count_attr):
            count_val = getattr(settings, count_attr)
            move_pool.count_given = count_val
        else:
            move_pool.count_given = 0
    
    # Filler items
    if settings.filler_items_selected:
        proto.filler_items.extend([x.value if hasattr(x, 'value') else x for x in settings.filler_items_selected])
    
    # Ice trap settings
    proto.ice_traps.count = settings.ice_trap_count
    proto.ice_traps.model = settings.ice_trap_model_v2
    proto.ice_traps.weights.bubble = settings.trap_weight_bubble
    proto.ice_traps.weights.reverse = settings.trap_weight_reverse
    proto.ice_traps.weights.slow = settings.trap_weight_slow
    proto.ice_traps.weights.disable_a = settings.trap_weight_disablea
    proto.ice_traps.weights.disable_b = settings.trap_weight_disableb
    proto.ice_traps.weights.disable_z = settings.trap_weight_disablez
    proto.ice_traps.weights.disable_c_up = settings.trap_weight_disablecu
    proto.ice_traps.weights.get_out = settings.trap_weight_getout
    proto.ice_traps.weights.dry = settings.trap_weight_dry
    proto.ice_traps.weights.flip = settings.trap_weight_flip
    proto.ice_traps.weights.ice_floor = settings.trap_weight_icefloor
    proto.ice_traps.weights.paper = settings.trap_weight_paper
    proto.ice_traps.weights.slip = settings.trap_weight_slip
    proto.ice_traps.weights.animal = settings.trap_weight_animal
    proto.ice_traps.weights.rockfall = settings.trap_weight_rockfall
    proto.ice_traps.weights.disable_tag = settings.trap_weight_disabletag
    
    # Item counts
    proto.item_counts.golden_bananas = settings.total_gbs
    proto.item_counts.banana_medals = settings.total_medals
    proto.item_counts.banana_fairies = settings.total_fairies
    proto.item_counts.battle_crowns = settings.total_crowns
    proto.item_counts.rainbow_coins = settings.total_rainbow_coins
    proto.item_counts.pearls = settings.total_pearls
    
    # Max snide reward requirement
    proto.max_snide_reward_requirement = settings.most_snide_rewards

def _populate_requirement_settings(settings: "Settings", proto: requirement_settings_pb2.RequirementSettings) -> None:
    """Populate RequirementSettings proto from Settings object."""
    # B Locker option
    proto.b_locker_option.opt = settings.blocker_selection_behavior
    if settings.BLockerEntryCount:
        proto.b_locker_option.amounts.extend(settings.BLockerEntryCount)
    proto.b_locker_option.maximum = settings.blocker_max
    proto.maximize_helm_b_locker = bool(settings.maximize_helm_blocker)
    
    # Troff'n'Scoff option
    proto.tns_option.opt = settings.tns_selection_behavior
    if settings.BossBananas:
        proto.tns_option.amounts.extend(settings.BossBananas)
    proto.tns_option.maximum = settings.troff_max
    
    # Medals for Jetpac
    proto.medals_for_jetpac.opt = settings.medal_jetpac_behavior
    proto.medals_for_jetpac.selected_quantity = settings.medal_requirement
    
    # Pearls for Mermaid
    proto.pearls_for_mermaid.opt = settings.pearl_mermaid_behavior
    proto.pearls_for_mermaid.selected_quantity = settings.mermaid_gb_pearls
    
    # Fairies for Fairy Queen
    proto.fairies_for_fairy_queen.opt = settings.fairy_queen_behavior
    proto.fairies_for_fairy_queen.selected_quantity = settings.rareware_gb_fairies
    
    # CBs for Medal
    proto.cbs_for_medal.opt = settings.cb_medal_behavior_new
    proto.cbs_for_medal.selected_quantity = settings.medal_cb_req
    
    # Open lobbies
    proto.open_lobbies = bool(settings.open_lobbies)
    
    # Switchsanity
    proto.switchsanity.enabled = bool(settings.switchsanity_enabled)
    
    # Map individual switchsanity_switch_* attributes to proto switch assignments
    # Mapping: settings attribute name -> proto SwitchLocation enum value
    switch_location_map = {
        'switchsanity_switch_isles_to_kroc_top': 1,  # SWITCH_LOCATION_ISLES_TO_TOP_OF_KREM_ISLE
        'switchsanity_switch_isles_helm_lobby': 2,  # SWITCH_LOCATION_ISLES_IN_HELM_LOBBY
        'switchsanity_switch_isles_aztec_lobby_back_room': 3,  # SWITCH_LOCATION_ISLES_BACK_OF_AZTEC_LOBBY
        'switchsanity_switch_isles_fungi_lobby_fairy': 4,  # SWITCH_LOCATION_ISLES_FOREST_LOBBY_FAIRY
        'switchsanity_switch_isles_spawn_rocketbarrel': 5,  # SWITCH_LOCATION_ISLES_CABIN_ISLE_ROCKET
        'switchsanity_switch_japes_free_kong': 6,  # SWITCH_LOCATION_JAPES_FREE_KONG
        'switchsanity_switch_japes_to_hive': 7,  # SWITCH_LOCATION_JAPES_HIVE_AREA
        'switchsanity_switch_japes_to_cavern': 8,  # SWITCH_LOCATION_JAPES_STARTING_TUNNEL
        'switchsanity_switch_japes_to_painting_room': 9,  # SWITCH_LOCATION_JAPES_PAINTING_ROOM
        'switchsanity_switch_japes_to_rambi': 10,  # SWITCH_LOCATION_JAPES_RAMBI
        'switchsanity_switch_aztec_free_tiny': 11,  # SWITCH_LOCATION_AZTEC_TINY_TEMPLE_FREE_KONG
        'switchsanity_switch_aztec_free_lanky': 12,  # SWITCH_LOCATION_AZTEC_LLAMA_TEMPLE_FREE_KONG
        'switchsanity_switch_aztec_to_kasplat_room': 13,  # SWITCH_LOCATION_AZTEC_STARTING_TUNNEL_KASPLAT
        'switchsanity_switch_aztec_to_connector_tunnel': 14,  # SWITCH_LOCATION_AZTEC_OASIS_DOOR
        'switchsanity_switch_aztec_llama_front': 15,  # SWITCH_LOCATION_AZTEC_LLAMA_TEMPLE_FRONT
        'switchsanity_switch_aztec_llama_side': 16,  # SWITCH_LOCATION_AZTEC_LLAMA_TEMPLE_SIDE
        'switchsanity_switch_aztec_llama_back': 17,  # SWITCH_LOCATION_AZTEC_LLAMA_TEMPLE_BACK
        'switchsanity_switch_aztec_sand_tunnel': 18,  # SWITCH_LOCATION_AZTEC_SAND_TUNNEL
        'switchsanity_switch_galleon_to_lighthouse_side': 19,  # SWITCH_LOCATION_GALLEON_LIGHTHOUSE_AREA
        'switchsanity_switch_galleon_to_shipwreck_side': 20,  # SWITCH_LOCATION_GALLEON_SHIPYARD_AREA
        'switchsanity_switch_galleon_to_cannon_game': 21,  # SWITCH_LOCATION_GALLEON_CANNON_GAME
        'switchsanity_switch_fungi_yellow_tunnel': 22,  # SWITCH_LOCATION_FOREST_YELLOW_TUNNEL
        'switchsanity_switch_fungi_green_tunnel_near': 23,  # SWITCH_LOCATION_FOREST_GREEN_TUNNEL_CLOCK_SIDE
        'switchsanity_switch_fungi_green_tunnel_far': 24,  # SWITCH_LOCATION_FOREST_GREEN_TUNNEL_BEAN_SIDE
        'switchsanity_switch_factory_dark_grate': 25,
        'switchsanity_switch_factory_bonus_grate': 26,
        'switchsanity_switch_factory_monster_grate': 27,
        'switchsanity_switch_caves_gone_cave': 28,
        'switchsanity_switch_caves_snide_cave': 29,
        'switchsanity_switch_caves_boulder_cave': 30,
        'switchsanity_switch_caves_lobby_blueprint': 31,
        'switchsanity_switch_caves_lobby_lava': 32,
        'switchsanity_switch_aztec_gong_tower': 33,
        'switchsanity_switch_aztec_lobby_gong': 34,
    }
    
    for attr_name, location_enum in switch_location_map.items():
        if hasattr(settings, attr_name):
            switch_item = getattr(settings, attr_name)
            if switch_item is not None:
                switch_assignment = proto.switchsanity.switch_assignment.add()
                switch_assignment.location = location_enum
                # Convert the switch item to proto enum value (extract .value if enum)
                switch_assignment.item = switch_item.value if hasattr(switch_item, 'value') else switch_item
    
    # Smaller shops
    proto.smaller_shops = bool(settings.smaller_shops)
    
    # Tooie style shops and free trade agreement
    proto.tooie_style_shops = bool(settings.shops_dont_cost)
    proto.free_trade_agreement = bool(settings.free_trade_setting)
    
    # Removed barriers
    if settings.remove_barriers_selected:
        proto.removed_barriers.extend([x.value if hasattr(x, 'value') else x for x in settings.remove_barriers_selected])
    
    # Galleon water
    proto.galleon_water = settings.galleon_water
    
    # Fungi time
    proto.fungi_time = settings.fungi_time
    
    # Shop prices
    proto.shop_prices = settings.random_prices
    
    # Activate bananaports
    proto.activate_bananaports = settings.activate_all_bananaports
    
    # Faster checks
    if settings.faster_checks_selected:
        proto.faster_checks.extend([x.value if hasattr(x, 'value') else x for x in settings.faster_checks_selected])
    
    # Puzzle rando
    proto.puzzle_rando = settings.puzzle_rando_difficulty


def _populate_overworld_settings(settings: "Settings", proto: overworld_settings_pb2.OverworldSettings) -> None:
    """Populate OverworldSettings proto from Settings object."""
    # World Navigation
    proto.entrance_randomizer = settings.level_randomization
    proto.shuffle_helm_location = bool(settings.shuffle_helm_location)
    proto.cross_map_bananaports = settings.bananaport_rando
    proto.random_starting_region = settings.random_starting_region_new
    
    # Kong models
    proto.kong_models.dk_model = settings.kong_model_dk
    proto.kong_models.diddy_model = settings.kong_model_diddy
    proto.kong_models.lanky_model = settings.kong_model_lanky
    proto.kong_models.tiny_model = settings.kong_model_tiny
    proto.kong_models.chunky_model = settings.kong_model_chunky
    proto.kong_models.mode = settings.kong_model_mode
    
    # Location Randomizers
    proto.dirt_patch_randomizer = bool(settings.item_rando_list_selected and any(x.value == 0 for x in settings.item_rando_list_selected))
    proto.banana_coin_randomizer = bool(settings.coin_rando)
    proto.banana_fairy_randomizer = bool(settings.item_rando_list_selected and any(x.value == 2 for x in settings.item_rando_list_selected))
    proto.melon_crate_randomizer = bool(settings.item_rando_list_selected and any(x.value == 3 for x in settings.item_rando_list_selected))
    proto.battle_crown_randomizer = bool(settings.crown_placement_rando)
    proto.race_coin_randomizer = bool(settings.race_coin_rando)
    proto.randomize_pickups = bool(settings.randomize_pickups)
    proto.shuffle_shop_locations = bool(settings.shuffle_shops)
    
    # CB randomizer
    proto.cb_randomizer.enabled = bool(settings.cb_rando_enabled)
    if settings.cb_rando_list_selected:
        proto.cb_randomizer.cb_randomized_levels.extend([x.value if hasattr(x, 'value') else x for x in settings.cb_rando_list_selected])
    
    proto.kasplat_randomizer = settings.kasplat_rando_setting
    
    # Bananaport randomizer
    proto.bananaport_randomizer.opt = settings.bananaport_placement_rando
    # Note: Settings doesn't have a bananaport_placement_list attribute
    # Only has bananaport_placement_rando (enum) and useful_bananaport_placement (bool)
    
    proto.wrinky_door_randomizer = bool(settings.wrinkly_location_rando)
    proto.tns_portal_randomizer = bool(settings.tns_location_rando)
    proto.vanilla_door_shuffle = bool(settings.vanilla_door_rando)
    proto.dos_doors = bool(settings.dos_door_rando)
    proto.dk_portal_randomizer = settings.dk_portal_location_rando_v2
    
    # Bosses
    proto.shuffle_boss_location = bool(settings.boss_location_rando)
    proto.krool_in_boss_pool = settings.krool_in_boss_pool_v2
    if settings.boss_maps:
        proto.bosses_selected.extend([x.value if hasattr(x, 'value') else x for x in settings.boss_maps])
    proto.ship_location_rando = bool(settings.ship_location_rando)
    
    # Enemies
    if settings.enemies_selected:
        proto.shuffled_enemies.extend([x.value if hasattr(x, 'value') else x for x in settings.enemies_selected])
    proto.crown_enemies = settings.crown_enemy_difficulty
    proto.random_enemy_speed = bool(settings.enemy_speed_rando)
    proto.random_enemy_size = bool(settings.randomize_enemy_sizes)
    
    # Bonus Barrels
    if settings.minigames_list_selected:
        proto.shuffled_bonus_barrels.extend([x.value if hasattr(x, 'value') else x for x in settings.minigames_list_selected])
    proto.disable_hard_minigames = bool(settings.disable_hard_minigames)
    proto.auto_complete_bonus_barrels = bool(settings.bonus_barrel_auto_complete)
    proto.alternate_minecart_mayhem = bool(settings.alt_minecart_mayhem)
    
    # Difficulty
    proto.no_heals = bool(settings.no_healing)
    proto.no_melon_slice_drops = bool(settings.no_melons)
    proto.ice_traps_damage_player = bool(settings.ice_traps_damage)
    proto.mirror_mode = bool(settings.mirror_mode)
    proto.tag_barrels_disabled = bool(settings.disable_tag_barrels)
    
    # Helm Hurry
    proto.helm_hurry_mode.enabled = bool(settings.helm_hurry)
    if settings.helm_hurry:
        proto.helm_hurry_mode.starting_time = settings.helmhurry_list_starting_time
        proto.helm_hurry_mode.golden_banana_time = settings.helmhurry_list_golden_banana
        proto.helm_hurry_mode.blueprint_time = settings.helmhurry_list_blueprint
        proto.helm_hurry_mode.company_coin_time = settings.helmhurry_list_company_coins
        proto.helm_hurry_mode.move_time = settings.helmhurry_list_move
        proto.helm_hurry_mode.banana_medal_time = settings.helmhurry_list_banana_medal
        proto.helm_hurry_mode.rainbow_coin_time = settings.helmhurry_list_rainbow_coin
        proto.helm_hurry_mode.boss_key_time = settings.helmhurry_list_boss_key
        proto.helm_hurry_mode.battle_crown_time = settings.helmhurry_list_battle_crown
        proto.helm_hurry_mode.bean_time = settings.helmhurry_list_bean
        proto.helm_hurry_mode.pearl_time = settings.helmhurry_list_pearl
        proto.helm_hurry_mode.kong_time = settings.helmhurry_list_kongs
        proto.helm_hurry_mode.fairy_time = settings.helmhurry_list_fairy
        proto.helm_hurry_mode.cb_time = settings.helmhurry_list_colored_bananas
        proto.helm_hurry_mode.trap_time = settings.helmhurry_list_ice_traps
    
    proto.no_consumable_upgrades = bool(settings.no_consumable_upgrades)
    
    # Hard mode
    from randomizer.Enums.Settings import HardModeSelected
    if settings.hard_mode_selected:
        proto.hard_mode.hard_enemies = HardModeSelected.hard_enemies in settings.hard_mode_selected
        proto.hard_mode.water_is_lava = HardModeSelected.water_is_lava in settings.hard_mode_selected
        proto.hard_mode.reduced_fall_damage_threshold = HardModeSelected.reduced_fall_damage_threshold in settings.hard_mode_selected
        proto.hard_mode.shuffled_jetpac_enemies = HardModeSelected.shuffled_jetpac_enemies in settings.hard_mode_selected
        proto.hard_mode.lower_max_refill_amounts = HardModeSelected.lower_max_refill_amounts in settings.hard_mode_selected
        proto.hard_mode.strict_helm_timer = HardModeSelected.strict_helm_timer in settings.hard_mode_selected
        proto.hard_mode.donk_in_the_dark_world = HardModeSelected.donk_in_the_dark_world in settings.hard_mode_selected
        proto.hard_mode.donk_in_the_sky = HardModeSelected.donk_in_the_sky in settings.hard_mode_selected
        proto.hard_mode.angry_caves = HardModeSelected.angry_caves in settings.hard_mode_selected
        proto.hard_mode.fast_balloons = HardModeSelected.fast_balloons in settings.hard_mode_selected
    
    # Hard bosses
    from randomizer.Enums.Settings import HardBossesSelected
    if settings.hard_bosses_selected:
        proto.hard_bosses.fast_mad_jack = HardBossesSelected.fast_mad_jack in settings.hard_bosses_selected
        proto.hard_bosses.alternative_mad_jack_kongs = HardBossesSelected.alternative_mad_jack_kongs in settings.hard_bosses_selected
        proto.hard_bosses.pufftoss_star_rando = HardBossesSelected.pufftoss_star_rando in settings.hard_bosses_selected
        proto.hard_bosses.pufftoss_star_raised = HardBossesSelected.pufftoss_star_raised in settings.hard_bosses_selected
        proto.hard_bosses.kut_out_phase_rando = HardBossesSelected.kut_out_phase_rando in settings.hard_bosses_selected
        proto.hard_bosses.k_rool_toes_rando = HardBossesSelected.k_rool_toes_rando in settings.hard_bosses_selected
        proto.hard_bosses.beta_lanky_phase = HardBossesSelected.beta_lanky_phase in settings.hard_bosses_selected
    
    proto.damage = settings.damage_amount


def _populate_endgame_settings(settings: "Settings", proto: endgame_settings_pb2.EndgameSettings) -> None:
    """Populate EndgameSettings proto from Settings object."""
    # Logic
    proto.logic.type = settings.logic_type
    if settings.glitches_selected:
        proto.logic.glitches.extend([x.value if hasattr(x, 'value') else x for x in settings.glitches_selected])
    if settings.tricks_selected:
        proto.logic.tricks.extend([x.value if hasattr(x, 'value') else x for x in settings.tricks_selected])
    
    # Win Condition
    proto.win_condition.type = settings.win_condition_item
    proto.win_condition.quantity = settings.win_condition_count
    proto.win_condition.spawns_ship = bool(settings.win_condition_spawns_ship)
    
    # Required Keys
    proto.required_keys.random_quantity = bool(settings.select_keys)
    proto.required_keys.specified_quantity = settings.krool_key_count
    if settings.starting_keys_list_selected:
        proto.required_keys.specified_starting_keys.extend([x.value if hasattr(x, 'value') else x for x in settings.starting_keys_list_selected])
    proto.required_keys.helm_key_lock = bool(settings.key_8_helm)
    proto.required_keys.key_8_required = bool(settings.k_rool_vanilla_requirement)
    
    # Starting Kongs
    proto.starting_kongs.random_quantity = bool(settings.kong_rando)
    proto.starting_kongs.specified_quantity = settings.starting_kongs_count
    proto.starting_kongs.specified_starting_kong = settings.starting_kong
    
    # Helm Settings
    proto.helm_settings.random_length = bool(settings.helm_barrels == 1)  # MinigameBarrels.random
    proto.helm_settings.specified_length = settings.helm_setting if settings.helm_setting else 0
    proto.helm_settings.shuffle_helm_rooms = bool(settings.helm_phase_order_rando)
    proto.helm_settings.helm_start_location = settings.helm_setting
    proto.helm_settings.helm_room_bonus_count = settings.helm_room_bonus_count
    
    # Helm door requirements
    if settings.crown_door_item:
        door_req = proto.helm_settings.helm_door_requirements.add()
        door_req.type = settings.crown_door_item
        door_req.specified_quantity = settings.crown_door_item_count

    if settings.coin_door_item:
        door_req = proto.helm_settings.helm_door_requirements.add()
        door_req.type = settings.coin_door_item
        door_req.specified_quantity = settings.coin_door_item_count
    
    # K.Rool Settings
    proto.k_rool_settings.shuffle_k_rool_phases = bool(settings.krool_phase_order_rando)
    proto.k_rool_settings.random_phase_amount = bool(settings.krool_random)
    proto.k_rool_settings.specified_phase_amount = settings.krool_phase_count
    proto.k_rool_settings.dk_phase_requires_blast = bool(settings.cannons_require_blast)
    proto.k_rool_settings.chunky_phase_slam_requirement = settings.chunky_phase_slam_req


def _populate_qol_settings(settings: "Settings", proto: qol_settings_pb2.QualityOfLifeSettings) -> None:
    """Populate QualityOfLifeSettings proto from Settings object."""    
    from randomizer.Enums.Settings import MiscChangesSelected, CrownEnemyRando, MicrohintsEnabled
    
    # Basic boolean toggles
    proto.tag_anywhere = bool(settings.enable_tag_anywhere)
    proto.fast_warps = bool(settings.fast_warps)
    proto.portal_numbers = bool(settings.portal_numbers)
    proto.item_reward_previews = bool(settings.item_reward_previews)
    proto.auto_key_turn_ins = bool(settings.auto_keys)
    proto.warp_to_isles = bool(settings.warp_to_isles)
    proto.shorten_boss_fights = bool(settings.shorten_boss)
    proto.shop_indicator = bool(settings.shop_indicator)
    proto.enemy_kill_crown_timer = bool(settings.enemy_kill_crown_timer != CrownEnemyRando.off)
    proto.disable_racing_patches = bool(settings.disable_racing_patches)
    proto.less_fragile_boulders = bool(settings.less_fragile_boulders)
    
    # Enum fields - proto enums are the source of truth
    proto.cutscene_skips = settings.more_cutscene_skips
    
    # MiscChanges - check each enum value in misc_changes_selected list
    proto.misc_changes.auto_dance_skip = MiscChangesSelected.auto_dance_skip in settings.misc_changes_selected
    proto.misc_changes.fast_boot = MiscChangesSelected.fast_boot in settings.misc_changes_selected
    proto.misc_changes.calm_caves = MiscChangesSelected.calm_caves in settings.misc_changes_selected
    proto.misc_changes.animal_buddies_grab_items = MiscChangesSelected.animal_buddies_grab_items in settings.misc_changes_selected
    proto.misc_changes.reduced_lag = MiscChangesSelected.reduced_lag in settings.misc_changes_selected
    proto.misc_changes.remove_extraneous_cutscenes = MiscChangesSelected.remove_extraneous_cutscenes in settings.misc_changes_selected
    proto.misc_changes.hint_textbox_hold = MiscChangesSelected.hint_textbox_hold in settings.misc_changes_selected
    proto.misc_changes.remove_wrinkly_puzzles = MiscChangesSelected.remove_wrinkly_puzzles in settings.misc_changes_selected
    proto.misc_changes.fast_picture_taking = MiscChangesSelected.fast_picture_taking in settings.misc_changes_selected
    proto.misc_changes.hud_hotkey = MiscChangesSelected.hud_hotkey in settings.misc_changes_selected
    proto.misc_changes.ammo_swap = MiscChangesSelected.ammo_swap in settings.misc_changes_selected
    proto.misc_changes.homing_balloons = MiscChangesSelected.homing_balloons in settings.misc_changes_selected
    proto.misc_changes.fast_transform_animation = MiscChangesSelected.fast_transform_animation in settings.misc_changes_selected
    proto.misc_changes.troff_n_scoff_audio_indicator = MiscChangesSelected.troff_n_scoff_audio_indicator in settings.misc_changes_selected
    proto.misc_changes.lowered_aztec_lobby_bonus = MiscChangesSelected.lowered_aztec_lobby_bonus in settings.misc_changes_selected
    proto.misc_changes.quicker_galleon_star = MiscChangesSelected.quicker_galleon_star in settings.misc_changes_selected
    proto.misc_changes.vanilla_bug_fixes = MiscChangesSelected.vanilla_bug_fixes in settings.misc_changes_selected
    proto.misc_changes.save_k_rool_progress = MiscChangesSelected.save_k_rool_progress in settings.misc_changes_selected
    proto.misc_changes.small_bananas_always_visible = MiscChangesSelected.small_bananas_always_visible in settings.misc_changes_selected
    proto.misc_changes.fast_hints = MiscChangesSelected.fast_hints in settings.misc_changes_selected
    proto.misc_changes.brighten_mad_maze_maul_enemies = MiscChangesSelected.brighten_mad_maze_maul_enemies in settings.misc_changes_selected
    proto.misc_changes.raise_fungi_dirt_patch = MiscChangesSelected.raise_fungi_dirt_patch in settings.misc_changes_selected
    proto.misc_changes.global_instrument = MiscChangesSelected.global_instrument in settings.misc_changes_selected
    proto.misc_changes.fast_pause_transitions = MiscChangesSelected.fast_pause_transitions in settings.misc_changes_selected
    proto.misc_changes.cannon_game_better_control = MiscChangesSelected.cannon_game_better_control in settings.misc_changes_selected
    proto.misc_changes.better_fairy_camera = MiscChangesSelected.better_fairy_camera in settings.misc_changes_selected
    proto.misc_changes.remove_enemy_cabin_timer = MiscChangesSelected.remove_enemy_cabin_timer in settings.misc_changes_selected
    proto.misc_changes.remove_galleon_ship_timers = MiscChangesSelected.remove_galleon_ship_timers in settings.misc_changes_selected
    proto.misc_changes.japes_bridge_permanently_extended = MiscChangesSelected.japes_bridge_permanently_extended in settings.misc_changes_selected
    proto.misc_changes.move_spring_cabin_rocketbarrel = MiscChangesSelected.move_spring_cabin_rocketbarrel in settings.misc_changes_selected
    
    # HintSettings
    proto.hints.wrinkly_hints = settings.wrinkly_hints
    proto.hints.shop_hints = bool(settings.enable_shop_hints)
    proto.hints.dim_solved_hints = bool(settings.dim_solved_hints)
    proto.hints.no_joke_hints = bool(settings.serious_hints)
    proto.hints.kongless_hint_doors = bool(settings.microhints_enabled != MicrohintsEnabled.off)
    proto.hints.extra_hints = settings.microhints_enabled
    
    # Progressive hints
    proto.hints.progressive_hints.item = settings.progressive_hint_item
    proto.hints.progressive_hints.count_for_35th_hint = int(settings.progressive_hint_count)
    proto.hints.progressive_hints.hint_curve = settings.progressive_hint_algorithm
    
    # Spoiler hints configuration
    proto.hints.spoiler_hints.type = settings.spoiler_hints
    proto.hints.spoiler_hints.include_woth_count = bool(settings.spoiler_include_woth_count)
    proto.hints.spoiler_hints.include_level_order = bool(settings.spoiler_include_level_order)
    
    # Spoiler hints points
    proto.hints.spoiler_hints.points.kongs = int(settings.points_list_kongs)
    proto.hints.spoiler_hints.points.keys = int(settings.points_list_keys)
    proto.hints.spoiler_hints.points.shopkeepers = int(settings.points_list_shopkeepers)
    proto.hints.spoiler_hints.points.guns = int(settings.points_list_guns)
    proto.hints.spoiler_hints.points.instruments = int(settings.points_list_instruments)
    proto.hints.spoiler_hints.points.training_moves = int(settings.points_list_training_moves)
    proto.hints.spoiler_hints.points.important_shared = int(settings.points_list_important_shared)
    proto.hints.spoiler_hints.points.fairy_moves = int(settings.points_list_fairy_moves)
    proto.hints.spoiler_hints.points.pad_moves = int(settings.points_list_pad_moves)
    proto.hints.spoiler_hints.points.barrel_moves = int(settings.points_list_barrel_moves)
    proto.hints.spoiler_hints.points.active_moves = int(settings.points_list_active_moves)
    proto.hints.spoiler_hints.points.bean = int(settings.points_list_bean)


def _populate_plandomizer_settings(settings: "Settings", proto: plandomizer_settings_pb2.PlandomizerSettings) -> None:
    """Populate PlandomizerSettings proto from Settings object."""
    # Plandomizer uses a complex dictionary structure (settings.plandomizer_dict)
    # Keys include: plando_starting_exit, plando_starting_kongs_selected, 
    # plando_krool_order_N, plando_boss_order_N, plando_helm_order_N,
    # plando_dirt_patches, plando_melon_crates, plando_battle_arenas, etc.
    # 
    # TODO: Implement plandomizer dictionary serialization
    # This will require mapping the dictionary structure to the proto fields:
    # - starting_exit: int -> optional int32
    # - starting_kongs: list -> repeated KongId
    # - place_* booleans
    # - level_order, krool_order, boss_order, helm_order maps
    # - item_assignments, minigame_assignments, hint_assignments, shop_assignments
    # - custom_location_assignments (dirt patches, crates, arenas, kasplats, wrinkly, tns)
    pass


# Helper functions to apply proto messages to Settings
def _apply_item_settings(proto: item_settings_pb2.ItemSettings, settings: "Settings") -> None:
    """Apply ItemSettings proto to Settings object."""
    # Decouple item rando
    settings.decouple_item_rando = bool(proto.decouple_item_rando)
    is_decoupled = bool(proto.decouple_item_rando)
    
    # ItemPool - restore each pool to its corresponding list (preserves exact distribution)
    # Clear all individual lists first
    for i in range(10):
        setattr(settings, f"item_rando_list_{i}", [])
    
    # Apply each pool to its corresponding list
    for i, pool in enumerate(proto.pools):
        if i >= 10:
            break  # Safety check - only process up to 10 lists
        
        # In decoupled mode, lists 0-4 have items, lists 5-9 have checks
        # In coupled mode, all lists have items only
        if is_decoupled and i >= 5:
            # This is a checks list (item_rando_list_5 through _9) - use pool.checks
            pool_items = list(pool.checks)
        else:
            # This is an items list (item_rando_list_0 through _4 in decoupled, or all in coupled) - use pool.items
            pool_items = list(pool.items)
        
        setattr(settings, f"item_rando_list_{i}", pool_items)
    
    # StartingMovePool - extract multiple pools (restores each pool to its corresponding list)
    # Write to individual starting_moves_list_1 through _5 fields (not the combined lists)
    # Convert integer values back to Items enum objects
    from randomizer.Enums.Items import Items
    for i, move_pool in enumerate(proto.starting_move_pools):
        if i >= 5:
            break  # Safety check - only process up to 5 lists
        
        list_index = i + 1  # Convert 0-based to 1-based (starting_moves_list_1, _2, etc.)
        move_list = list(move_pool.items)
        
        # Convert integer values back to Items enum objects
        enum_list = []
        for item_value in move_list:
            try:
                enum_obj = Items(item_value)
                enum_list.append(enum_obj)
            except ValueError:
                # If conversion fails, keep the integer value
                enum_list.append(item_value)
        
        setattr(settings, f"starting_moves_list_{list_index}", enum_list)
        setattr(settings, f"starting_moves_list_count_{list_index}", move_pool.count_given)
    
    # Filler items
    settings.filler_items_selected = list(proto.filler_items)
    
    # Ice trap settings
    settings.ice_trap_count = proto.ice_traps.count
    settings.ice_trap_model_v2 = proto.ice_traps.model
    settings.trap_weight_bubble = proto.ice_traps.weights.bubble
    settings.trap_weight_reverse = proto.ice_traps.weights.reverse
    settings.trap_weight_slow = proto.ice_traps.weights.slow
    settings.trap_weight_disablea = proto.ice_traps.weights.disable_a
    settings.trap_weight_disableb = proto.ice_traps.weights.disable_b
    settings.trap_weight_disablez = proto.ice_traps.weights.disable_z
    settings.trap_weight_disablecu = proto.ice_traps.weights.disable_c_up
    settings.trap_weight_getout = proto.ice_traps.weights.get_out
    settings.trap_weight_dry = proto.ice_traps.weights.dry
    settings.trap_weight_flip = proto.ice_traps.weights.flip
    settings.trap_weight_icefloor = proto.ice_traps.weights.ice_floor
    settings.trap_weight_paper = proto.ice_traps.weights.paper
    settings.trap_weight_slip = proto.ice_traps.weights.slip
    settings.trap_weight_animal = proto.ice_traps.weights.animal
    settings.trap_weight_rockfall = proto.ice_traps.weights.rockfall
    settings.trap_weight_disabletag = proto.ice_traps.weights.disable_tag
    
    # Item counts
    settings.total_gbs = proto.item_counts.golden_bananas
    settings.total_medals = proto.item_counts.banana_medals
    settings.total_fairies = proto.item_counts.banana_fairies
    settings.total_crowns = proto.item_counts.battle_crowns
    settings.total_rainbow_coins = proto.item_counts.rainbow_coins
    settings.total_pearls = proto.item_counts.pearls
    
    # Max snide reward requirement
    settings.most_snide_rewards = proto.max_snide_reward_requirement


def _apply_requirement_settings(proto: requirement_settings_pb2.RequirementSettings, settings: "Settings") -> None:
    """Apply RequirementSettings proto to Settings object."""
    # B Locker option
    settings.blocker_selection_behavior = proto.b_locker_option.opt
    settings.BLockerEntryCount = list(proto.b_locker_option.amounts)
    settings.blocker_max = proto.b_locker_option.maximum
    settings.maximize_helm_blocker = bool(proto.maximize_helm_b_locker)
    
    # Troff'n'Scoff option
    settings.tns_selection_behavior = proto.tns_option.opt
    settings.BossBananas = list(proto.tns_option.amounts)
    settings.troff_max = proto.tns_option.maximum
    
    # Medals for Jetpac
    settings.medal_jetpac_behavior = proto.medals_for_jetpac.opt
    settings.medal_requirement = proto.medals_for_jetpac.selected_quantity
    
    # Pearls for Mermaid
    settings.pearl_mermaid_behavior = proto.pearls_for_mermaid.opt
    settings.mermaid_gb_pearls = proto.pearls_for_mermaid.selected_quantity
    
    # Fairies for Fairy Queen
    settings.fairy_queen_behavior = proto.fairies_for_fairy_queen.opt
    settings.rareware_gb_fairies = proto.fairies_for_fairy_queen.selected_quantity
    
    # CBs for Medal
    settings.cb_medal_behavior_new = proto.cbs_for_medal.opt
    settings.medal_cb_req = proto.cbs_for_medal.selected_quantity
    
    # Open lobbies
    settings.open_lobbies = bool(proto.open_lobbies)
    
    # Switchsanity
    if proto.HasField('switchsanity'):
        settings.switchsanity_enabled = bool(proto.switchsanity.enabled)
        
        # Reverse mapping: proto SwitchLocation enum value -> settings attribute name
        location_to_attr_map = {
            1: 'switchsanity_switch_isles_to_kroc_top',
            2: 'switchsanity_switch_isles_helm_lobby',
            3: 'switchsanity_switch_isles_aztec_lobby_back_room',
            4: 'switchsanity_switch_isles_fungi_lobby_fairy',
            5: 'switchsanity_switch_isles_spawn_rocketbarrel',
            6: 'switchsanity_switch_japes_free_kong',
            7: 'switchsanity_switch_japes_to_hive',
            8: 'switchsanity_switch_japes_to_cavern',
            9: 'switchsanity_switch_japes_to_painting_room',
            10: 'switchsanity_switch_japes_to_rambi',
            11: 'switchsanity_switch_aztec_free_tiny',
            12: 'switchsanity_switch_aztec_free_lanky',
            13: 'switchsanity_switch_aztec_to_kasplat_room',
            14: 'switchsanity_switch_aztec_to_connector_tunnel',
            15: 'switchsanity_switch_aztec_llama_front',
            16: 'switchsanity_switch_aztec_llama_side',
            17: 'switchsanity_switch_aztec_llama_back',
            18: 'switchsanity_switch_aztec_sand_tunnel',
            19: 'switchsanity_switch_galleon_to_lighthouse_side',
            20: 'switchsanity_switch_galleon_to_shipwreck_side',
            21: 'switchsanity_switch_galleon_to_cannon_game',
            22: 'switchsanity_switch_fungi_yellow_tunnel',
            23: 'switchsanity_switch_fungi_green_tunnel_near',
            24: 'switchsanity_switch_fungi_green_tunnel_far',
            25: 'switchsanity_switch_factory_dark_grate',
            26: 'switchsanity_switch_factory_bonus_grate',
            27: 'switchsanity_switch_factory_monster_grate',
            28: 'switchsanity_switch_caves_gone_cave',
            29: 'switchsanity_switch_caves_snide_cave',
            30: 'switchsanity_switch_caves_boulder_cave',
            31: 'switchsanity_switch_caves_lobby_blueprint',
            32: 'switchsanity_switch_caves_lobby_lava',
            33: 'switchsanity_switch_aztec_gong_tower',
            34: 'switchsanity_switch_aztec_lobby_gong',
        }
        
        # Apply each switch assignment from proto to settings
        for switch_assignment in proto.switchsanity.switch_assignment:
            attr_name = location_to_attr_map.get(switch_assignment.location)
            if attr_name:
                setattr(settings, attr_name, switch_assignment.item)
    
    # Smaller shops
    settings.smaller_shops = bool(proto.smaller_shops)
    
    # Tooie style shops and free trade agreement
    settings.shops_dont_cost = bool(proto.tooie_style_shops)
    settings.free_trade_setting = bool(proto.free_trade_agreement)
    
    # Removed barriers
    settings.remove_barriers_selected = list(proto.removed_barriers)
    
    # Galleon water
    settings.galleon_water = proto.galleon_water
    
    # Fungi time
    settings.fungi_time = proto.fungi_time
    
    # Shop prices
    settings.random_prices = proto.shop_prices
    
    # Activate bananaports
    settings.activate_all_bananaports = proto.activate_bananaports
    
    # Faster checks
    settings.faster_checks_selected = list(proto.faster_checks)
    
    # Puzzle rando
    settings.puzzle_rando_difficulty = proto.puzzle_rando


def _apply_overworld_settings(proto: overworld_settings_pb2.OverworldSettings, settings: "Settings") -> None:
    """Apply OverworldSettings proto to Settings object."""
    # World Navigation
    settings.level_randomization = proto.entrance_randomizer
    settings.shuffle_helm_location = bool(proto.shuffle_helm_location)
    settings.bananaport_rando = proto.cross_map_bananaports
    settings.random_starting_region_new = proto.random_starting_region
    
    # Kong models
    settings.kong_model_dk = proto.kong_models.dk_model
    settings.kong_model_diddy = proto.kong_models.diddy_model
    settings.kong_model_lanky = proto.kong_models.lanky_model
    settings.kong_model_tiny = proto.kong_models.tiny_model
    settings.kong_model_chunky = proto.kong_models.chunky_model
    settings.kong_model_mode = proto.kong_models.mode
    
    # Location Randomizers
    settings.coin_rando = bool(proto.banana_coin_randomizer)
    settings.crown_placement_rando = bool(proto.battle_crown_randomizer)
    settings.race_coin_rando = bool(proto.race_coin_randomizer)
    settings.randomize_pickups = bool(proto.randomize_pickups)
    settings.shuffle_shops = bool(proto.shuffle_shop_locations)
    
    # CB randomizer
    settings.cb_rando_enabled = bool(proto.cb_randomizer.enabled)
    settings.cb_rando_list_selected = list(proto.cb_randomizer.cb_randomized_levels)
    
    settings.kasplat_rando_setting = proto.kasplat_randomizer
    
    # Bananaport randomizer
    settings.bananaport_placement_rando = proto.bananaport_randomizer.opt
    
    settings.wrinkly_location_rando = bool(proto.wrinky_door_randomizer)
    settings.tns_location_rando = bool(proto.tns_portal_randomizer)
    settings.vanilla_door_rando = bool(proto.vanilla_door_shuffle)
    settings.dos_door_rando = bool(proto.dos_doors)
    settings.dk_portal_location_rando_v2 = proto.dk_portal_randomizer
    
    # Bosses
    settings.boss_location_rando = bool(proto.shuffle_boss_location)
    settings.krool_in_boss_pool_v2 = proto.krool_in_boss_pool
    settings.boss_maps = list(proto.bosses_selected)
    settings.ship_location_rando = bool(proto.ship_location_rando)
    
    # Enemies
    settings.enemies_selected = list(proto.shuffled_enemies)
    settings.crown_enemy_difficulty = proto.crown_enemies
    settings.enemy_speed_rando = bool(proto.random_enemy_speed)
    settings.randomize_enemy_sizes = bool(proto.random_enemy_size)
    
    # Bonus Barrels
    settings.minigames_list_selected = list(proto.shuffled_bonus_barrels)
    settings.disable_hard_minigames = bool(proto.disable_hard_minigames)
    settings.bonus_barrel_auto_complete = bool(proto.auto_complete_bonus_barrels)
    settings.alt_minecart_mayhem = bool(proto.alternate_minecart_mayhem)
    
    # Difficulty
    settings.no_healing = bool(proto.no_heals)
    settings.no_melons = bool(proto.no_melon_slice_drops)
    settings.ice_traps_damage = bool(proto.ice_traps_damage_player)
    settings.mirror_mode = bool(proto.mirror_mode)
    settings.disable_tag_barrels = bool(proto.tag_barrels_disabled)
    
    # Helm Hurry
    settings.helm_hurry = bool(proto.helm_hurry_mode.enabled)
    if settings.helm_hurry:
        settings.helmhurry_list_starting_time = proto.helm_hurry_mode.starting_time
        settings.helmhurry_list_golden_banana = proto.helm_hurry_mode.golden_banana_time
        settings.helmhurry_list_blueprint = proto.helm_hurry_mode.blueprint_time
        settings.helmhurry_list_company_coins = proto.helm_hurry_mode.company_coin_time
        settings.helmhurry_list_move = proto.helm_hurry_mode.move_time
        settings.helmhurry_list_banana_medal = proto.helm_hurry_mode.banana_medal_time
        settings.helmhurry_list_rainbow_coin = proto.helm_hurry_mode.rainbow_coin_time
        settings.helmhurry_list_boss_key = proto.helm_hurry_mode.boss_key_time
        settings.helmhurry_list_battle_crown = proto.helm_hurry_mode.battle_crown_time
        settings.helmhurry_list_bean = proto.helm_hurry_mode.bean_time
        settings.helmhurry_list_pearl = proto.helm_hurry_mode.pearl_time
        settings.helmhurry_list_kongs = proto.helm_hurry_mode.kong_time
        settings.helmhurry_list_fairy = proto.helm_hurry_mode.fairy_time
        settings.helmhurry_list_colored_bananas = proto.helm_hurry_mode.cb_time
        settings.helmhurry_list_ice_traps = proto.helm_hurry_mode.trap_time
    
    settings.no_consumable_upgrades = bool(proto.no_consumable_upgrades)
    
    # Hard mode - rebuild list from booleans
    from randomizer.Enums.Settings import HardModeSelected
    settings.hard_mode_selected = []
    if proto.hard_mode.hard_enemies:
        settings.hard_mode_selected.append(HardModeSelected.hard_enemies)
    if proto.hard_mode.water_is_lava:
        settings.hard_mode_selected.append(HardModeSelected.water_is_lava)
    if proto.hard_mode.reduced_fall_damage_threshold:
        settings.hard_mode_selected.append(HardModeSelected.reduced_fall_damage_threshold)
    if proto.hard_mode.shuffled_jetpac_enemies:
        settings.hard_mode_selected.append(HardModeSelected.shuffled_jetpac_enemies)
    if proto.hard_mode.lower_max_refill_amounts:
        settings.hard_mode_selected.append(HardModeSelected.lower_max_refill_amounts)
    if proto.hard_mode.strict_helm_timer:
        settings.hard_mode_selected.append(HardModeSelected.strict_helm_timer)
    if proto.hard_mode.donk_in_the_dark_world:
        settings.hard_mode_selected.append(HardModeSelected.donk_in_the_dark_world)
    if proto.hard_mode.donk_in_the_sky:
        settings.hard_mode_selected.append(HardModeSelected.donk_in_the_sky)
    if proto.hard_mode.angry_caves:
        settings.hard_mode_selected.append(HardModeSelected.angry_caves)
    if proto.hard_mode.fast_balloons:
        settings.hard_mode_selected.append(HardModeSelected.fast_balloons)
    
    # Hard bosses - rebuild list from booleans
    from randomizer.Enums.Settings import HardBossesSelected
    settings.hard_bosses_selected = []
    if proto.hard_bosses.fast_mad_jack:
        settings.hard_bosses_selected.append(HardBossesSelected.fast_mad_jack)
    if proto.hard_bosses.alternative_mad_jack_kongs:
        settings.hard_bosses_selected.append(HardBossesSelected.alternative_mad_jack_kongs)
    if proto.hard_bosses.pufftoss_star_rando:
        settings.hard_bosses_selected.append(HardBossesSelected.pufftoss_star_rando)
    if proto.hard_bosses.pufftoss_star_raised:
        settings.hard_bosses_selected.append(HardBossesSelected.pufftoss_star_raised)
    if proto.hard_bosses.kut_out_phase_rando:
        settings.hard_bosses_selected.append(HardBossesSelected.kut_out_phase_rando)
    if proto.hard_bosses.k_rool_toes_rando:
        settings.hard_bosses_selected.append(HardBossesSelected.k_rool_toes_rando)
    if proto.hard_bosses.beta_lanky_phase:
        settings.hard_bosses_selected.append(HardBossesSelected.beta_lanky_phase)
    
    settings.damage_amount = proto.damage


def _apply_endgame_settings(proto: endgame_settings_pb2.EndgameSettings, settings: "Settings") -> None:
    """Apply EndgameSettings proto to Settings object."""
    # Logic
    settings.logic_type = proto.logic.type
    settings.glitches_selected = list(proto.logic.glitches)
    settings.tricks_selected = list(proto.logic.tricks)
    
    # Win Condition
    settings.win_condition_item = proto.win_condition.type
    settings.win_condition_count = proto.win_condition.quantity
    settings.win_condition_spawns_ship = bool(proto.win_condition.spawns_ship)
    
    # Required Keys
    settings.select_keys = bool(proto.required_keys.random_quantity)
    settings.krool_key_count = proto.required_keys.specified_quantity
    settings.starting_keys_list_selected = list(proto.required_keys.specified_starting_keys)
    settings.key_8_helm = bool(proto.required_keys.helm_key_lock)
    settings.k_rool_vanilla_requirement = bool(proto.required_keys.key_8_required)
    
    # Starting Kongs
    settings.kong_rando = bool(proto.starting_kongs.random_quantity)
    settings.starting_kongs_count = proto.starting_kongs.specified_quantity
    settings.starting_kong = proto.starting_kongs.specified_starting_kong
    
    # Helm Settings
    if proto.helm_settings.random_length:
        settings.helm_barrels = 1  # MinigameBarrels.random
    # helm_setting serves dual purpose: specified_length and helm_start_location use the same value
    settings.helm_setting = proto.helm_settings.helm_start_location if proto.helm_settings.helm_start_location else proto.helm_settings.specified_length
    settings.helm_phase_order_rando = bool(proto.helm_settings.shuffle_helm_rooms)
    settings.helm_room_bonus_count = proto.helm_settings.helm_room_bonus_count
    
    # Helm door requirements
    if proto.helm_settings.helm_door_requirements:
        door_req = proto.helm_settings.helm_door_requirements[0]
        settings.crown_door_item = door_req.type
        settings.crown_door_item_count = door_req.specified_quantity
        settings.coin_door_item = door_req.type
        settings.coin_door_item_coint = door_req.specified_quantity
    
    # K.Rool Settings
    settings.krool_phase_order_rando = bool(proto.k_rool_settings.shuffle_k_rool_phases)
    settings.krool_random = bool(proto.k_rool_settings.random_phase_amount)
    settings.chunky_phase_slam_req = proto.k_rool_settings.chunky_phase_slam_requirement


def _apply_qol_settings(proto: qol_settings_pb2.QualityOfLifeSettings, settings: "Settings") -> None:
    """Apply QualityOfLifeSettings proto to Settings object."""
    from randomizer.Enums.Settings import MiscChangesSelected, CrownEnemyRando, MicrohintsEnabled
    
    # Basic boolean toggles
    settings.enable_tag_anywhere = bool(proto.tag_anywhere)
    settings.fast_warps = bool(proto.fast_warps)
    settings.portal_numbers = bool(proto.portal_numbers)
    settings.item_reward_previews = bool(proto.item_reward_previews)
    settings.auto_keys = bool(proto.auto_key_turn_ins)
    settings.warp_to_isles = bool(proto.warp_to_isles)
    settings.shorten_boss = bool(proto.shorten_boss_fights)
    settings.shop_indicator = bool(proto.shop_indicator)
    settings.disable_racing_patches = bool(proto.disable_racing_patches)
    settings.less_fragile_boulders = bool(proto.less_fragile_boulders)
    
    # Enemy kill crown timer - reverse the check
    settings.enemy_kill_crown_timer = bool(proto.enemy_kill_crown_timer)
    
    # Enum fields
    settings.more_cutscene_skips = proto.cutscene_skips
    
    # MiscChanges - rebuild list from booleans
    settings.misc_changes_selected = []
    if proto.misc_changes.auto_dance_skip:
        settings.misc_changes_selected.append(MiscChangesSelected.auto_dance_skip)
    if proto.misc_changes.fast_boot:
        settings.misc_changes_selected.append(MiscChangesSelected.fast_boot)
    if proto.misc_changes.calm_caves:
        settings.misc_changes_selected.append(MiscChangesSelected.calm_caves)
    if proto.misc_changes.animal_buddies_grab_items:
        settings.misc_changes_selected.append(MiscChangesSelected.animal_buddies_grab_items)
    if proto.misc_changes.reduced_lag:
        settings.misc_changes_selected.append(MiscChangesSelected.reduced_lag)
    if proto.misc_changes.remove_extraneous_cutscenes:
        settings.misc_changes_selected.append(MiscChangesSelected.remove_extraneous_cutscenes)
    if proto.misc_changes.hint_textbox_hold:
        settings.misc_changes_selected.append(MiscChangesSelected.hint_textbox_hold)
    if proto.misc_changes.remove_wrinkly_puzzles:
        settings.misc_changes_selected.append(MiscChangesSelected.remove_wrinkly_puzzles)
    if proto.misc_changes.fast_picture_taking:
        settings.misc_changes_selected.append(MiscChangesSelected.fast_picture_taking)
    if proto.misc_changes.hud_hotkey:
        settings.misc_changes_selected.append(MiscChangesSelected.hud_hotkey)
    if proto.misc_changes.ammo_swap:
        settings.misc_changes_selected.append(MiscChangesSelected.ammo_swap)
    if proto.misc_changes.homing_balloons:
        settings.misc_changes_selected.append(MiscChangesSelected.homing_balloons)
    if proto.misc_changes.fast_transform_animation:
        settings.misc_changes_selected.append(MiscChangesSelected.fast_transform_animation)
    if proto.misc_changes.troff_n_scoff_audio_indicator:
        settings.misc_changes_selected.append(MiscChangesSelected.troff_n_scoff_audio_indicator)
    if proto.misc_changes.lowered_aztec_lobby_bonus:
        settings.misc_changes_selected.append(MiscChangesSelected.lowered_aztec_lobby_bonus)
    if proto.misc_changes.quicker_galleon_star:
        settings.misc_changes_selected.append(MiscChangesSelected.quicker_galleon_star)
    if proto.misc_changes.vanilla_bug_fixes:
        settings.misc_changes_selected.append(MiscChangesSelected.vanilla_bug_fixes)
    if proto.misc_changes.save_k_rool_progress:
        settings.misc_changes_selected.append(MiscChangesSelected.save_k_rool_progress)
    if proto.misc_changes.small_bananas_always_visible:
        settings.misc_changes_selected.append(MiscChangesSelected.small_bananas_always_visible)
    if proto.misc_changes.fast_hints:
        settings.misc_changes_selected.append(MiscChangesSelected.fast_hints)
    if proto.misc_changes.brighten_mad_maze_maul_enemies:
        settings.misc_changes_selected.append(MiscChangesSelected.brighten_mad_maze_maul_enemies)
    if proto.misc_changes.raise_fungi_dirt_patch:
        settings.misc_changes_selected.append(MiscChangesSelected.raise_fungi_dirt_patch)
    if proto.misc_changes.global_instrument:
        settings.misc_changes_selected.append(MiscChangesSelected.global_instrument)
    if proto.misc_changes.fast_pause_transitions:
        settings.misc_changes_selected.append(MiscChangesSelected.fast_pause_transitions)
    if proto.misc_changes.cannon_game_better_control:
        settings.misc_changes_selected.append(MiscChangesSelected.cannon_game_better_control)
    if proto.misc_changes.better_fairy_camera:
        settings.misc_changes_selected.append(MiscChangesSelected.better_fairy_camera)
    if proto.misc_changes.remove_enemy_cabin_timer:
        settings.misc_changes_selected.append(MiscChangesSelected.remove_enemy_cabin_timer)
    if proto.misc_changes.remove_galleon_ship_timers:
        settings.misc_changes_selected.append(MiscChangesSelected.remove_galleon_ship_timers)
    if proto.misc_changes.japes_bridge_permanently_extended:
        settings.misc_changes_selected.append(MiscChangesSelected.japes_bridge_permanently_extended)
    if proto.misc_changes.move_spring_cabin_rocketbarrel:
        settings.misc_changes_selected.append(MiscChangesSelected.move_spring_cabin_rocketbarrel)
    
    # HintSettings
    settings.wrinkly_hints = proto.hints.wrinkly_hints
    settings.enable_shop_hints = bool(proto.hints.shop_hints)
    settings.dim_solved_hints = bool(proto.hints.dim_solved_hints)
    settings.serious_hints = bool(proto.hints.no_joke_hints)
    settings.microhints_enabled = proto.hints.extra_hints
    
    # Progressive hints
    settings.progressive_hint_item = proto.hints.progressive_hints.item
    settings.progressive_hint_count = int(proto.hints.progressive_hints.count_for_35th_hint)
    settings.progressive_hint_algorithm = proto.hints.progressive_hints.hint_curve
    
    # Spoiler hints configuration
    settings.spoiler_hints = proto.hints.spoiler_hints.type
    settings.spoiler_include_woth_count = bool(proto.hints.spoiler_hints.include_woth_count)
    settings.spoiler_include_level_order = bool(proto.hints.spoiler_hints.include_level_order)
    
    # Spoiler hints points
    settings.points_list_kongs = int(proto.hints.spoiler_hints.points.kongs)
    settings.points_list_keys = int(proto.hints.spoiler_hints.points.keys)
    settings.points_list_shopkeepers = int(proto.hints.spoiler_hints.points.shopkeepers)
    settings.points_list_guns = int(proto.hints.spoiler_hints.points.guns)
    settings.points_list_instruments = int(proto.hints.spoiler_hints.points.instruments)
    settings.points_list_training_moves = int(proto.hints.spoiler_hints.points.training_moves)
    settings.points_list_important_shared = int(proto.hints.spoiler_hints.points.important_shared)
    settings.points_list_fairy_moves = int(proto.hints.spoiler_hints.points.fairy_moves)
    settings.points_list_pad_moves = int(proto.hints.spoiler_hints.points.pad_moves)
    settings.points_list_barrel_moves = int(proto.hints.spoiler_hints.points.barrel_moves)
    settings.points_list_active_moves = int(proto.hints.spoiler_hints.points.active_moves)
    settings.points_list_bean = int(proto.hints.spoiler_hints.points.bean)


def _apply_plandomizer_settings(proto: plandomizer_settings_pb2.PlandomizerSettings, settings: "Settings") -> None:
    """Apply PlandomizerSettings proto to Settings object."""
    # TODO: Map proto fields to settings attributes
    pass


# =============================================================================
# Fill Result Serialization
# =============================================================================

def fill_result_to_proto(spoiler: "Spoiler") -> fill_result_pb2.FillResult:
    """Convert a Spoiler object (post-Fill) to a FillResult protobuf message.
    
    This serializes all the results of the Fill algorithm that are needed
    for patching the ROM.
    
    Args:
        spoiler: Spoiler object after Fill has completed
        
    Returns:
        FillResult protobuf message
    """
    proto = fill_result_pb2.FillResult()
    
    # Populate each section
    _populate_location_assignments(spoiler, proto.location_assignments)
    _populate_move_shop_data(spoiler, proto.move_shop_data)
    _populate_shuffle_data(spoiler, proto.shuffle_data)
    _populate_placement_data(spoiler, proto.placement_data)
    _populate_hint_data(spoiler, proto.hint_data)
    _populate_path_data(spoiler, proto.path_data)
    _populate_misc_patching_data(spoiler, proto.misc_data)
    
    return proto


def _populate_location_assignments(spoiler: "Spoiler", proto: fill_result_pb2.LocationAssignments) -> None:
    """Populate LocationAssignments from spoiler.LocationList."""
    for location_id, location in spoiler.LocationList.items():
        if location.item is not None:
            proto.assignments[int(location_id)] = int(location.item)


def _populate_move_shop_data(spoiler: "Spoiler", proto: fill_result_pb2.MoveShopData) -> None:
    """Populate MoveShopData from spoiler.move_data."""
    # move_data is a 3-element list: [shop_moves, training_barrels, bfi_moves]
    
    # Index 0: Shop moves (3D structure)
    if len(spoiler.move_data) > 0 and isinstance(spoiler.move_data[0], list):
        for shop_type_data in spoiler.move_data[0]:
            shop_type_proto = proto.shop_types.add()
            for shop_index_data in shop_type_data:
                shop_index_proto = shop_type_proto.shop_indices.add()
                for kong_moves_data in shop_index_data:
                    kong_moves_proto = shop_index_proto.kong_moves.add()
                    for move_entry in kong_moves_data:
                        _populate_move_entry(move_entry, kong_moves_proto.moves.add())
    
    # Index 1: Training barrels
    if len(spoiler.move_data) > 1 and isinstance(spoiler.move_data[1], list):
        for move_entry in spoiler.move_data[1]:
            _populate_move_entry(move_entry, proto.training_barrels.add())
    
    # Index 2: BFI moves
    if len(spoiler.move_data) > 2 and isinstance(spoiler.move_data[2], list):
        for move_entry in spoiler.move_data[2]:
            _populate_move_entry(move_entry, proto.bfi_moves.add())


def _populate_move_entry(move_dict: Any, proto: fill_result_pb2.MoveEntry) -> None:
    """Populate a single MoveEntry from a move dictionary."""
    # Handle non-dict types (might be string or other)
    if not isinstance(move_dict, dict):
        proto.empty_move.CopyFrom(fill_result_pb2.EmptyMove())
        return
    
    move_type = move_dict.get("move_type")
    
    if move_type is None:
        proto.empty_move.CopyFrom(fill_result_pb2.EmptyMove())
    elif move_type == "flag":
        proto.flag_move.flag = move_dict.get("flag", "")
        proto.flag_move.price = move_dict.get("price", 0)
    elif move_type == "special":
        proto.special_move.move_lvl = move_dict.get("move_lvl", 0)
        proto.special_move.move_kong = move_dict.get("move_kong", 0)
        proto.special_move.price = move_dict.get("price", 0)
    elif move_type == "slam":
        proto.slam_move.move_lvl = move_dict.get("move_lvl", 0)
        proto.slam_move.move_kong = move_dict.get("move_kong", 0)
        proto.slam_move.price = move_dict.get("price", 0)
    elif move_type == "gun":
        proto.gun_move.move_lvl = move_dict.get("move_lvl", 0)
        proto.gun_move.move_kong = move_dict.get("move_kong", 0)
        proto.gun_move.price = move_dict.get("price", 0)
    elif move_type == "ammo_belt":
        proto.ammo_belt_move.move_lvl = move_dict.get("move_lvl", 0)
        proto.ammo_belt_move.move_kong = move_dict.get("move_kong", 0)
        proto.ammo_belt_move.price = move_dict.get("price", 0)
    elif move_type == "instrument":
        proto.instrument_move.move_lvl = move_dict.get("move_lvl", 0)
        proto.instrument_move.move_kong = move_dict.get("move_kong", 0)
        proto.instrument_move.price = move_dict.get("price", 0)


def _populate_shuffle_data(spoiler: "Spoiler", proto: fill_result_pb2.ShuffleData) -> None:
    """Populate ShuffleData from spoiler shuffle dictionaries."""
    # Shuffled exits
    for exit_id, exit_dest in spoiler.shuffled_exit_data.items():
        exit_proto = proto.shuffled_exits[int(exit_id)]
        
        # Handle both TransitionFront and TransitionBack objects
        if hasattr(exit_dest, 'dest'):
            # TransitionFront object
            exit_proto.destination_region = int(exit_dest.dest)
            exit_proto.exit_name = exit_dest.exit if hasattr(exit_dest, 'exit') else ""
        elif hasattr(exit_dest, 'regionId'):
            # TransitionBack object
            exit_proto.destination_region = int(exit_dest.regionId)
            exit_proto.exit_name = exit_dest.name if hasattr(exit_dest, 'name') else ""
        else:
            # Unknown type, try to extract what we can
            exit_proto.destination_region = int(getattr(exit_dest, 'dest', getattr(exit_dest, 'regionId', 0)))
            exit_proto.exit_name = getattr(exit_dest, 'exit', getattr(exit_dest, 'name', ""))
        
        exit_proto.reverse_transition = int(exit_dest.reverse) if hasattr(exit_dest, 'reverse') and exit_dest.reverse is not None else 0
        exit_proto.spoiler_name = exit_dest.spoilerName if hasattr(exit_dest, 'spoilerName') else ""
    
    # Shuffled barrels
    for location_id, minigame_data in spoiler.shuffled_barrel_data.items():
        # minigame_data could be a MinigameLocationData object or just an enum
        if hasattr(minigame_data, 'minigame'):
            # MinigameLocationData object
            proto.shuffled_barrels[int(location_id)] = int(minigame_data.minigame)
        else:
            # Direct enum value
            proto.shuffled_barrels[int(location_id)] = int(minigame_data)
    
    # Shuffled doors. Each level maps to a list of tuples:
    #   (door_index, DoorType.wrinkly, kong_assignee)
    #   (door_index, DoorType.boss)
    #   (door_index, DoorType.dk_portal)
    # Downstream patching (DoorPlacer.place_door_locations) reads these by
    # positional index, so we must preserve tuple shape on the consumer side.
    for level, door_list in spoiler.shuffled_door_data.items():
        shuffle_proto = proto.shuffled_doors.add()
        shuffle_proto.level = int(level)
        for entry in door_list:
            door_proto = shuffle_proto.doors.add()
            door_proto.door_location = int(entry[0])
            door_proto.door_type = str(int(entry[1]))
            if len(entry) > 2 and entry[2] is not None:
                door_proto.kong_assignee = int(entry[2])
    
    # Exit instructions
    for instruction in spoiler.shuffled_exit_instructions:
        proto.exit_instructions.append(str(instruction))
    
    # Port connections
    if hasattr(spoiler, 'port_connections'):
        for port_id, connection in spoiler.port_connections.items():
            port_proto = proto.port_connections[int(port_id)]
            if hasattr(connection, 'dest'):
                port_proto.destination_region = int(connection.dest)
            if hasattr(connection, 'map'):
                port_proto.destination_map = int(connection.map)
            if hasattr(connection, 'exit'):
                port_proto.destination_exit = int(connection.exit)
    
    # Warp data (human readable)
    if hasattr(spoiler, 'warp_data'):
        for warp in spoiler.warp_data:
            warp_proto = proto.warp_data.add()
            warp_proto.from_location = warp.get('from', '')
            warp_proto.to = warp.get('to', '')
    
    # Crown placements
    if hasattr(spoiler, 'crown_locations'):
        for crown_loc in spoiler.crown_locations:
            crown_proto = proto.crown_placements.add()
            crown_proto.map_id = int(crown_loc.get('map', 0))
            crown_proto.arena_id = int(crown_loc.get('arena', 0))
    
    # Patch placements (dirt patches)
    if hasattr(spoiler, 'dirt_patch_placement'):
        for patch in spoiler.dirt_patch_placement:
            patch_proto = proto.patch_placements.add()
            patch_proto.map_id = int(patch.get('map', 0))
            patch_proto.patch_id = int(patch.get('id', 0))
            patch_proto.item_id = int(patch.get('item', 0))
    
    # Crate placements
    if hasattr(spoiler, 'melon_crate_placement'):
        for crate in spoiler.melon_crate_placement:
            crate_proto = proto.crate_placements.add()
            crate_proto.map_id = int(crate.get('map', 0))
            crate_proto.crate_id = int(crate.get('id', 0))
            crate_proto.item_id = int(crate.get('item', 0))


def _populate_placement_data(spoiler: "Spoiler", proto: fill_result_pb2.PlacementData) -> None:
    """Populate PlacementData from spoiler placement lists."""
    # CB placements
    for cb_data in spoiler.cb_placements:
        cb_proto = proto.cb_placements.add()
        cb_proto.id = cb_data.get('id', 0)
        cb_proto.name = cb_data.get('name', '')
        cb_proto.kong = int(cb_data.get('kong', 0))
        cb_proto.level = int(cb_data.get('level', 0))
        cb_proto.type = cb_data.get('type', '')
        cb_proto.map = int(cb_data.get('map', 0))
        
        # Locations (for CB type) - structure is [amount, scale, x, y, z]
        if 'locations' in cb_data and isinstance(cb_data['locations'], list):
            for loc in cb_data['locations']:
                loc_proto = cb_proto.locations.add()
                if isinstance(loc, dict):
                    # Dict format: {'amount': val, 'scale': val, 'x': val, 'y': val, 'z': val}
                    loc_proto.amount = int(loc.get('amount', 1))
                    loc_proto.scale = float(loc.get('scale', 1.0))
                    loc_proto.x = float(loc.get('x', 0))
                    loc_proto.y = float(loc.get('y', 0))
                    loc_proto.z = float(loc.get('z', 0))
                elif isinstance(loc, (list, tuple)) and len(loc) >= 5:
                    # List format: [amount, scale, x, y, z]
                    loc_proto.amount = int(loc[0])
                    loc_proto.scale = float(loc[1])
                    loc_proto.x = float(loc[2])
                    loc_proto.y = float(loc[3])
                    loc_proto.z = float(loc[4])
    
    # Balloon placements
    for balloon_data in spoiler.balloon_placement:
        balloon_proto = proto.balloon_placements.add()
        balloon_proto.id = balloon_data.get('id', 0)
        balloon_proto.name = balloon_data.get('name', '')
        balloon_proto.kong = int(balloon_data.get('kong', 0))
        balloon_proto.level = int(balloon_data.get('level', 0))
        balloon_proto.map = int(balloon_data.get('map', 0))
        balloon_proto.score = balloon_data.get('score', 0)
    
    # Enemy replacements
    for enemy_data in spoiler.enemy_replacements:
        enemy_proto = proto.enemy_replacements.add()
        enemy_proto.container_map = int(enemy_data.get('container_map', 0))
        
        for swap in enemy_data.get('kasplat_swaps', []):
            swap_proto = enemy_proto.kasplat_swaps.add()
            swap_proto.vanilla_location = int(swap.get('vanilla_location', 0))
            swap_proto.replace_with = int(swap.get('replace_with', 0))
    
    # Coin requirements
    for map_id, coin_count in spoiler.coin_requirements.items():
        proto.coin_requirements[int(map_id)] = int(coin_count)
    
    # Coin placements (if they exist)
    if hasattr(spoiler, 'coin_placement'):
        for coin_data in spoiler.coin_placement:
            coin_proto = proto.coin_placements.add()
            coin_proto.level = int(coin_data.get('level', 0))
            coin_proto.map = int(coin_data.get('map', 0))
            coin_proto.kong = int(coin_data.get('kong', 0))
            coin_proto.type = coin_data.get('type', '')
            coin_proto.name = coin_data.get('name', '')
    
    # Pokemon Snap enemy data (for Krem Kapture win condition)
    if hasattr(spoiler, 'pkmn_snap_data'):
        for spawned in spoiler.pkmn_snap_data:
            proto.pkmn_snap_data.append(bool(spawned))

    # Enemy rando data: map_id -> list of {enemy, speeds, id, location}.
    # Populated by randomize_enemies_0 during Fill; consumed by
    # randomize_enemies at patch time. Without serializing this the patcher
    # has an empty dict and writes no enemy swaps.
    enemy_rando_data = getattr(spoiler, 'enemy_rando_data', None) or {}
    for map_id, entries in enemy_rando_data.items():
        map_proto = proto.enemy_rando_data[int(map_id)]
        for entry in entries or []:
            entry_proto = map_proto.entries.add()
            try:
                entry_proto.enemy = int(entry.get('enemy', 0))
            except (TypeError, ValueError):
                entry_proto.enemy = 0
            for speed in (entry.get('speeds') or []):
                try:
                    entry_proto.speeds.append(int(speed))
                except (TypeError, ValueError):
                    continue
            try:
                entry_proto.spawner_id = int(entry.get('id', 0))
            except (TypeError, ValueError):
                entry_proto.spawner_id = 0
            entry_proto.location = str(entry.get('location', '') or '')

def _populate_hint_data(spoiler: "Spoiler", proto: fill_result_pb2.HintData) -> None:
    """Populate HintData from spoiler hint structures."""
    # Hint set
    if hasattr(spoiler, 'hintset'):
        proto.hint_set.max_hints = spoiler.hintset.hint_cap
        for hint in spoiler.hintset.hints:
            hint_proto = proto.hint_set.hints.add()
            hint_proto.location_id = int(hint.location) if hasattr(hint, 'location') else 0
            hint_proto.hint_text = hint.hint if hasattr(hint, 'hint') else ""
            hint_proto.important = hint.important if hasattr(hint, 'important') else False
            hint_proto.priority = hint.priority if hasattr(hint, 'priority') else 0
    
    # Tied hint flags
    for hint_name, flag_value in spoiler.tied_hint_flags.items():
        proto.tied_hint_flags[hint_name] = int(flag_value)
    
    # Tied hint regions
    for region in spoiler.tied_hint_regions:
        proto.tied_hint_regions.append(int(region))
    
    # Level spoiler hints (if they exist)
    if hasattr(spoiler, 'level_spoiler'):
        for level_id, level_hints in spoiler.level_spoiler.items():
            level_proto = proto.level_spoiler_hints[int(level_id)]
            if hasattr(level_hints, 'vial_colors'):
                level_proto.vial_colors.extend(level_hints.vial_colors)
            if hasattr(level_hints, 'points'):
                level_proto.points = level_hints.points
            if hasattr(level_hints, 'woth_count'):
                level_proto.woth_count = level_hints.woth_count
    
    # Human-readable spoiler hints
    if hasattr(spoiler, 'level_spoiler_human_readable'):
        for level_name, hint_text in spoiler.level_spoiler_human_readable.items():
            proto.level_spoiler_human_readable[level_name] = hint_text


def _populate_path_data(spoiler: "Spoiler", proto: fill_result_pb2.PathData) -> None:
    """Populate PathData from spoiler path structures."""
    # WotH locations
    if hasattr(spoiler, 'woth_locations'):
        for location_id in spoiler.woth_locations:
            proto.woth_locations.append(int(location_id))
    
    # WotH paths
    for goal_location, path_locations in spoiler.woth_paths.items():
        path_proto = proto.woth_paths[int(goal_location)]
        for loc_id in path_locations:
            path_proto.locations.append(int(loc_id))
    
    # K. Rool paths
    for phase_name, path_locations in spoiler.krool_paths.items():
        path_proto = proto.krool_paths[str(phase_name)]
        for loc_id in path_locations:
            path_proto.locations.append(int(loc_id))
    
    # Rabbit path
    for location_id in spoiler.rabbit_path:
        proto.rabbit_path.append(int(location_id))
    
    # DK Rap win con paths
    for verse_name, path_locations in spoiler.rap_win_con_paths.items():
        path_proto = proto.rap_win_con_paths[str(verse_name)]
        for loc_id in path_locations:
            path_proto.locations.append(int(loc_id))
    
    # Other paths
    for goal_location, path_locations in spoiler.other_paths.items():
        path_proto = proto.other_paths[int(goal_location)]
        for loc_id in path_locations:
            path_proto.locations.append(int(loc_id))
    
    # Playthrough
    if hasattr(spoiler, 'playthrough') and isinstance(spoiler.playthrough, list):
        for sphere_dict in spoiler.playthrough:
            sphere_proto = proto.playthrough.add()
            for location_id, item_id in sphere_dict.items():
                loc_proto = sphere_proto.locations.add()
                loc_proto.location_id = int(location_id)
                loc_proto.item_id = int(item_id)
    
    # Major items
    if hasattr(spoiler, 'majorItems'):
        for item_id in spoiler.majorItems:
            proto.major_items.append(int(item_id))
    
    # Foolish region names
    if hasattr(spoiler, 'foolish_region_names'):
        proto.foolish_region_names.extend([str(name) for name in spoiler.foolish_region_names])
    
    # Pathless moves
    if hasattr(spoiler, 'pathless_moves'):
        for item_id in spoiler.pathless_moves:
            proto.pathless_moves.append(int(item_id))
    
    # Region hintable count
    if hasattr(spoiler, 'region_hintable_count'):
        for region_name, items_dict in spoiler.region_hintable_count.items():
            region_counts_proto = proto.region_hintable_count[str(region_name)]
            for item_name, item_data in items_dict.items():
                item_data_proto = region_counts_proto.items[item_name]
                item_data_proto.plural = item_data.get('plural', '')
                item_data_proto.count = item_data.get('count', 0)
                # Handle Location objects or integers
                # Location objects need to be reverse-looked up in spoiler.LocationList to get their ID
                for loc in item_data.get('shuffled_locations', []):
                    if isinstance(loc, int):
                        item_data_proto.shuffled_locations.append(loc)
                    else:
                        # It's a Location object - find its ID in spoiler.LocationList
                        if hasattr(spoiler, 'LocationList'):
                            for loc_id, loc_obj in spoiler.LocationList.items():
                                if loc_obj is loc:
                                    item_data_proto.shuffled_locations.append(int(loc_id))
                                    break
    
    # Accessible hints for location
    if hasattr(spoiler, 'accessible_hints_for_location'):
        for location_id, hints in spoiler.accessible_hints_for_location.items():
            hints_proto = proto.accessible_hints_for_location[int(location_id)]
            if isinstance(hints, list):
                hints_proto.hint_names.extend([str(h) for h in hints])


def _populate_misc_patching_data(spoiler: "Spoiler", proto: fill_result_pb2.MiscPatchingData) -> None:
    """Populate MiscPatchingData from spoiler miscellaneous data."""
    # Item assignments. LocationSelection has many fields the patcher reads
    # directly (ItemRando.place_randomized_items); we need to preserve them
    # all faithfully - in particular placement_index (list, not scalar),
    # placement_data (actor ids per map), old_item/old_kong, and reward_spot.
    def _s(val: Any, default: int = 0) -> int:
        """Coerce possibly-None / enum values to int for sint32 fields (-1 sentinel)."""
        if val is None:
            return -1
        try:
            return int(val)
        except (TypeError, ValueError):
            return default

    for item_assign in spoiler.item_assignment:
        assign_proto = proto.item_assignments.add()
        assign_proto.old_type = _s(getattr(item_assign, 'old_type', None), -1)
        assign_proto.old_flag = _s(getattr(item_assign, 'old_flag', None), -1)
        assign_proto.old_item = _s(getattr(item_assign, 'old_item', None), -1)
        assign_proto.old_kong = _s(getattr(item_assign, 'old_kong', None), -1)

        # LocationSelection.placement_data: dict[map_id, actor_id]. Older code
        # also referred to this via the attribute "maps_to_actor_ids".
        placement_map = getattr(item_assign, 'placement_data', None)
        if placement_map is None:
            placement_map = getattr(item_assign, 'maps_to_actor_ids', None)
        if placement_map:
            for map_id, actor_id in placement_map.items():
                try:
                    assign_proto.maps_to_actor_ids[int(map_id)] = int(actor_id)
                except (TypeError, ValueError):
                    continue

        assign_proto.location = int(item_assign.location) if getattr(item_assign, 'location', None) is not None else 0
        assign_proto.new_flag = _s(getattr(item_assign, 'new_flag', None), -1)
        assign_proto.new_type = _s(getattr(item_assign, 'new_type', None), -1)
        assign_proto.new_item = _s(getattr(item_assign, 'new_item', None), -1)
        assign_proto.new_kong = _s(getattr(item_assign, 'new_kong', None), -1)
        assign_proto.shared = bool(getattr(item_assign, 'shared', False))

        # placement_index is a list in LocationSelection (shared shop items
        # write to multiple slots). Preserve the whole list; negatives are
        # meaningful (e.g. -1 sentinel for vanilla keys).
        pidx = getattr(item_assign, 'placement_index', None)
        if pidx is None:
            pass
        elif isinstance(pidx, (list, tuple)):
            for v in pidx:
                try:
                    assign_proto.placement_index.append(int(v))
                except (TypeError, ValueError):
                    pass
        else:
            try:
                assign_proto.placement_index.append(int(pidx))
            except (TypeError, ValueError):
                pass

        assign_proto.placement_subindex = int(getattr(item_assign, 'placement_subindex', 0) or 0)

        # Other LocationSelection flags consulted directly by the patcher.
        assign_proto.is_reward_point = bool(getattr(item_assign, 'reward_spot', False))
        assign_proto.is_shop = bool(getattr(item_assign, 'is_shop', False))

        price = getattr(item_assign, 'price', 0)
        if isinstance(price, (list, tuple)):
            assign_proto.price = int(price[0]) if price else 0
        else:
            try:
                assign_proto.price = int(price or 0)
            except (TypeError, ValueError):
                assign_proto.price = 0

        assign_proto.can_have_item = bool(getattr(item_assign, 'can_have_item', True))
        assign_proto.can_place_item = bool(getattr(item_assign, 'can_place_item', True))
        assign_proto.shop_locked = bool(getattr(item_assign, 'shop_locked', False))
        assign_proto.order = int(getattr(item_assign, 'order', 0) or 0)
        assign_proto.name = str(getattr(item_assign, 'name', '') or '')
        assign_proto.move_name = str(getattr(item_assign, 'move_name', '') or '')

    
    # Valid photo items
    for item_id in spoiler.valid_photo_items:
        proto.valid_photo_items.append(int(item_id))
    
    # Special items
    if hasattr(spoiler, 'arcade_item_reward') and spoiler.arcade_item_reward is not None:
        proto.arcade_item_reward = int(spoiler.arcade_item_reward)
    if hasattr(spoiler, 'jetpac_item_reward') and spoiler.jetpac_item_reward is not None:
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
    
    # Text file changes
    if hasattr(spoiler, 'text_changes'):
        for file_id, changes_list in spoiler.text_changes.items():
            text_changes_proto = proto.text_file_changes[int(file_id)]
            for change_dict in changes_list:
                # Serialize each change dict as a JSON string
                text_changes_proto.changes.append(json.dumps(change_dict))

    # Per-level DK portal destinations. These are mutated by the Fill phase
    # (e.g. assignDKPortal sets exit=-1 to indicate "use map default entry").
    # ASMPatcher reads settings.level_portal_destinations directly at patch time,
    # so we must round-trip the mutated values through the proto.
    settings = getattr(spoiler, 'settings', None)
    if settings is not None:
        for entry in getattr(settings, 'level_portal_destinations', []) or []:
            dest_proto = proto.level_portal_destinations.add()
            dest_proto.map = int(entry["map"])
            dest_proto.exit = int(entry["exit"])  # sint32; preserves -1 sentinel
        for map_id in getattr(settings, 'level_void_maps', []) or []:
            proto.level_void_maps.append(int(map_id))

        # Fill-time resolved starting Kongs. The user-input settings object
        # only carries the raw request (kong_rando flag, starting_kongs_count,
        # and possibly Kongs.any); the concrete list/lead Kong is chosen during
        # generation and must be preserved so the patched ROM matches the
        # spoiler log and the `B` in `spoiler.settings.starting_kong_list`
        # consumed by ItemRando.place_starting_moves.
        starting_kong_list = getattr(settings, 'starting_kong_list', None) or []
        for kong in starting_kong_list:
            try:
                proto.starting_kong_list.append(int(kong))
            except (TypeError, ValueError):
                continue
        resolved_starting_kong = getattr(settings, 'starting_kong', None)
        if resolved_starting_kong is not None:
            try:
                proto.resolved_starting_kong = int(resolved_starting_kong)
            except (TypeError, ValueError):
                pass

        # Fill-time resolved B.Locker / T&S arrays. These start from user
        # input but are rolled randomly in chaos mode and reordered in
        # ShuffleExits (randomizer/ShuffleExits.py). Without preserving them
        # the ROM's level access costs won't match the spoiler log.
        for count in getattr(settings, 'BLockerEntryCount', []) or []:
            try:
                proto.blocker_entry_counts.append(int(count))
            except (TypeError, ValueError):
                proto.blocker_entry_counts.append(0)
        for item in getattr(settings, 'BLockerEntryItems', []) or []:
            try:
                proto.blocker_entry_items.append(int(item))
            except (TypeError, ValueError):
                proto.blocker_entry_items.append(0)
        for count in getattr(settings, 'BossBananas', []) or []:
            try:
                proto.boss_bananas.append(int(count))
            except (TypeError, ValueError):
                proto.boss_bananas.append(0)
    for item_id in getattr(spoiler, 'pregiven_items', None) or []:
        try:
            proto.pregiven_items.append(int(item_id))
        except (TypeError, ValueError):
            continue
    first_move_item = getattr(spoiler, 'first_move_item', None)
    if first_move_item is not None:
        try:
            proto.first_move_item = int(first_move_item)
        except (TypeError, ValueError):
            pass

    # Archipelago flag. Set to True by the apworld before serialization; the
    # user-input settings restored in the browser default to False, so without
    # this roundtrip the patcher would treat AP seeds as local rando.
    if settings is not None and getattr(settings, 'archipelago', False):
        proto.archipelago = True
        # AP slot name is only meaningful when archipelago=True; the patcher
        # reads it to stamp the ROM header (ApplyRandomizer line ~1418).
        player_name = getattr(settings, 'player_name', None)
        if player_name:
            proto.player_name = str(player_name)

    # Fill-time K. Rool key requirement. Settings re-randomizes this in
    # __init__ (keys_random branch, plus starting-key-picking when
    # select_keys=False), and the browser rebuild uses a different RNG
    # state, so we must ship the exact list that the fill used.
    krool_keys_required = getattr(settings, 'krool_keys_required', None) if settings is not None else None
    if krool_keys_required:
        proto.krool_keys_required.extend([int(getattr(k, 'value', k)) for k in krool_keys_required])

    ship_location_index = getattr(spoiler, 'ship_location_index', None)
    if ship_location_index is not None:
        try:
            proto.ship_location_index = int(ship_location_index)
        except (TypeError, ValueError):
            pass
    ship_name = getattr(spoiler, 'ship_name', None)
    if ship_name:
        proto.ship_name = str(ship_name)
