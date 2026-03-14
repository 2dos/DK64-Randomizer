"""Dynamic mapper between standalone randomizer settings and Archipelago YAML options."""

import logging
import re
import os
from typing import Any, Dict, List, Optional, Set, Tuple
import yaml


class ArchipelagoMapper:
    """Maps standalone randomizer settings to Archipelago YAML format."""

    # Cosmetic/music settings to skip (not supported in Archipelago)
    SKIP_SETTINGS = {
        "music_bgm_randomized",
        "music_majoritems_randomized",
        "music_minoritems_randomized",
        "music_events_randomized",
        "random_music",
        "music_rando_enabled",
        "music_is_custom",
        "music_vanilla_locations",
        "music_disable_reverb",
        "isles_cool_musical",
        "music_selection_dict",
        "music_selections",
        "bgm_songs_selected",
        "majoritems_songs_selected",
        "minoritems_songs_selected",
        "events_songs_selected",
        "kong_model",
        "random_models",
        "color_palettes",
        "randomize_pickups",
        "randomize_enemies",
        "krool_model",
        "misc_model_changes",
        "texture_rando",
        "disable_tag_barrels",
        "fps_display",
        "enemy_rando",
        "colorblind_mode",
        "disco_chunky",
        "krusha_mode",
        "crown_mode",
        "puzzle_mode",
        "kasplat_rando",
        "enemy_drop_list",
    }

    def __init__(self):
        """Initialize the mapper and discover all Archipelago options."""
        self.options_metadata = {}
        self.ap_to_settings_map = {}
        self.settings_to_ap_map = {}

        self._discover_options()
        self._build_name_mappings()

    def _parse_options_file(self) -> str:
        """Read and return the content of archipelago/Options.py."""
        options_path = os.path.join(os.path.dirname(__file__), "..", "archipelago", "Options.py")

        try:
            with open(options_path, "r") as f:
                return f.read()
        except Exception as e:
            logging.error(f"Could not read Options.py: {e}")
            return ""

    def _discover_options(self):
        """Parse archipelago/Options.py to discover all options without importing."""
        content = self._parse_options_file()
        if not content:
            logging.warning("Could not parse Options.py - YAML export will be limited")
            return

        # Find the DK64Options dataclass definition
        dataclass_pattern = r'@dataclass\s+class\s+DK64Options\([^)]+\):\s*"""[^"]*"""\s*(.*?)(?=\n\nclass|\n\ndef|\Z)'
        match = re.search(dataclass_pattern, content, re.DOTALL)

        if not match:
            logging.error("Could not find DK64Options dataclass in Options.py")
            return

        fields_text = match.group(1)

        # Parse field definitions (e.g., "starting_kong_count: StartingKongCount")
        field_pattern = r"^\s*([a-z_0-9]+):\s*([A-Z][A-Za-z0-9]+)"
        fields_found = re.findall(field_pattern, fields_text, re.MULTILINE)

        logging.info(f"Discovered {len(fields_found)} DK64 options from Options.py")

        # For each field, try to find the class definition to get type info
        for field_name, class_name in fields_found:
            option_info = self._parse_option_class(content, class_name, field_name)
            self.options_metadata[field_name] = option_info

    def _parse_option_class(self, content: str, class_name: str, field_name: str) -> Dict:
        """Parse a specific option class definition to extract metadata."""
        option_info = {"field_name": field_name, "class_name": class_name, "display_name": field_name.replace("_", " ").title(), "default": None, "type": "unknown", "metadata": {}}

        # Find the class definition
        class_pattern = rf'class\s+{class_name}\(([^)]+)\):\s*"""([^"]*?)"""(.*?)(?=\nclass\s|\Z)'
        match = re.search(class_pattern, content, re.DOTALL)

        if not match:
            return option_info

        parent_class = match.group(1).strip()
        class_body = match.group(3)

        # Determine type based on parent class
        if "Range" in parent_class or "NamedRange" in parent_class:
            option_info["type"] = "range"
            range_start = re.search(r"range_start\s*=\s*(\d+)", class_body)
            range_end = re.search(r"range_end\s*=\s*(\d+)", class_body)
            default = re.search(r"default\s*=\s*(\d+)", class_body)

            if range_start and range_end:
                option_info["metadata"] = {"min": int(range_start.group(1)), "max": int(range_end.group(1))}
            if default:
                option_info["default"] = int(default.group(1))

        elif "Toggle" in parent_class:
            option_info["type"] = "toggle"
            option_info["metadata"]["default_on"] = "DefaultOnToggle" in parent_class
            default = re.search(r"default\s*=\s*(\d+)", class_body)
            if default:
                option_info["default"] = int(default.group(1))
            else:
                option_info["default"] = 1 if "DefaultOnToggle" in parent_class else 0

        elif "Choice" in parent_class or "TextChoice" in parent_class:
            option_info["type"] = "choice"
            # Find all option_* attributes
            choices = {}
            for match in re.finditer(r"option_([a-z_0-9]+)\s*=\s*(\d+)", class_body):
                choice_name = match.group(1)
                choice_value = int(match.group(2))
                choices[choice_name] = choice_value
            option_info["metadata"]["choices"] = choices

            default = re.search(r"default\s*=\s*(\d+)", class_body)
            if default:
                option_info["default"] = int(default.group(1))

        elif "OptionList" in parent_class or "ItemSet" in parent_class or "OptionSet" in parent_class:
            option_info["type"] = "list"
            # Extract list default if present (e.g. default = ["Vines", "Diving", ...])
            list_default_match = re.search(r"default\s*=\s*(\[.*?\])", class_body, re.DOTALL)
            if list_default_match:
                try:
                    option_info["default"] = eval(list_default_match.group(1))  # Safe: list of string literals
                except Exception:
                    pass

        elif "OptionDict" in parent_class or "ItemDict" in parent_class:
            option_info["type"] = "dict"

        # Extract display_name if present
        display_match = re.search(r'display_name\s*=\s*["\']([^"\']+)["\']', class_body)
        if display_match:
            option_info["display_name"] = display_match.group(1)

        return option_info

    def _parse_fillsettings_mappings(self) -> Dict[str, str]:
        """Parse FillSettings.py to extract Archipelago option to standalone setting mappings."""
        fillsettings_path = os.path.join(os.path.dirname(__file__), "..", "archipelago", "FillSettings.py")

        mappings = {}

        try:
            with open(fillsettings_path, "r") as f:
                content = f.read()

            # Find patterns like: settings_dict["standalone_name"] = options.archipelago_name.value
            # This matches the common pattern in fillsettings function
            pattern = r'settings_dict\["([^"]+)"\]\s*=\s*options\.([a-z_]+)(?:\.value)?'

            for match in re.finditer(pattern, content):
                standalone_name = match.group(1)
                archipelago_name = match.group(2)
                mappings[archipelago_name] = standalone_name

            logging.info(f"Extracted {len(mappings)} mappings from FillSettings.py")

        except Exception as e:
            logging.warning(f"Could not parse FillSettings.py for mappings: {e}")

        return mappings

    def _build_name_mappings(self):
        """Build bidirectional name mappings by parsing FillSettings.py and adding overrides."""
        # Start with mappings extracted from FillSettings.py
        auto_mappings = self._parse_fillsettings_mappings()

        # Manual overrides for special cases that don't follow the standard pattern
        # Most mappings are now auto-discovered from FillSettings.py!
        manual_overrides = {
            # Archipelago name -> Standalone name
            # Link options (Archipelago-specific, will use defaults)
            "death_link": "death_link",
            "ring_link": "ring_link",
            "tag_link": "tag_link",
            "trap_link": "trap_link",
            # Trap weights (Archipelago-specific, will use defaults)
            "animal_trap_weight": "animal_trap_weight",
            "banana_filler_weight": "banana_filler_weight",
            "bubble_trap_weight": "bubble_trap_weight",
            "disable_a_trap_weight": "disable_a_trap_weight",
            "disable_b_trap_weight": "disable_b_trap_weight",
            "disable_c_trap_weight": "disable_c_trap_weight",
            "disable_z_trap_weight": "disable_z_trap_weight",
            "disabletag_trap_weight": "disabletag_trap_weight",
            "dry_trap_weight": "dry_trap_weight",
            "flip_trap_weight": "flip_trap_weight",
            "get_out_trap_weight": "get_out_trap_weight",
            "ice_floor_weight": "ice_floor_weight",
            "paper_weight": "paper_weight",
            "reverse_trap_weight": "reverse_trap_weight",
            "rockfall_trap_weight": "rockfall_trap_weight",
            "slip_weight": "slip_weight",
            "slow_trap_weight": "slow_trap_weight",
            # Filler weights (Archipelago-specific, will use defaults)
            "crown_filler_weight": "crown_filler_weight",
            "fairy_filler_weight": "fairy_filler_weight",
            "junk_filler_weight": "junk_filler_weight",
            "medal_filler_weight": "medal_filler_weight",
            "pearl_filler_weight": "pearl_filler_weight",
            "rainbowcoin_filler_weight": "rainbowcoin_filler_weight",
            # Archipelago-specific defaults
            "hint_style": "hint_style",
            "microhints": "microhints",
            "receive_notifications": "receive_notifications",
            "shopkeeper_hints": "shopkeeper_hints",
            "trap_fill_percentage": "trap_fill_percentage",
            # Direct mappings with different names
            "allowed_bosses": "bosses_selected",
            "harder_bosses": "hard_bosses_selected",
            "shuffled_bonus_barrels": "minigames_list_selected",
            "pregiven_keys": "krool_key_count",
            "require_beating_krool": "win_condition_spawns_ship",
            "goal": "win_condition_item",
            "goal_quantity": "win_condition_count",
            "select_starting_kong": "starting_kong",
            "maximum_snide": "most_snide_rewards",
            # Settings that need special handling (handled in _get_special_value)
            "enable_chaos_blockers": "blocker_selection_behavior",
            "enable_cutscenes": "more_cutscene_skips",
            "enable_shared_shops": "smaller_shops",
            "galleon_water_level": "GalleonWaterLevel",
            "hard_minigames": "disable_hard_minigames",
            "krool_in_boss_pool": "krool_in_boss_pool_v2",
            "dk_portal_location_rando": "dk_portal_location_rando_v2",
            "random_starting_region": "random_starting_region_new",
            "randomize_blocker_required_amounts": "blocker_selection_behavior",
            "shop_prices": "random_prices",
            "loading_zone_rando": "LevelRandomization",
            "cannon_shuffle": "cannon_shuffle",
            "climbing_shuffle": "climbing_shuffle",
            "level_blockers": "blocker_text",  # Complex blocker handling
            # Starting move pools — each maps to starting_moves_list_N / starting_moves_list_count_N
            # Actual values are reconstructed via _get_special_value
            "starting_move_pool_1": "starting_moves_list_1",
            "starting_move_pool_1_count": "starting_moves_list_count_1",
            "starting_move_pool_2": "starting_moves_list_2",
            "starting_move_pool_2_count": "starting_moves_list_count_2",
            "starting_move_pool_3": "starting_moves_list_3",
            "starting_move_pool_3_count": "starting_moves_list_count_3",
            "starting_move_pool_4": "starting_moves_list_4",
            "starting_move_pool_4_count": "starting_moves_list_count_4",
            "starting_move_pool_5": "starting_moves_list_5",
            "starting_move_pool_5_count": "starting_moves_list_count_5",
            # Options that control item_rando_list_1 rather than direct settings
            # These are handled specially in _get_special_value()
            "hints_in_item_pool": "item_rando_list_1",
            "boulders_in_pool": "item_rando_list_1",
            "dropsanity": "item_rando_list_1",
            "half_medals_in_pool": "item_rando_list_1",
            "shopowners_in_pool": "shuffle_shops",  # Also adds to item_rando_list_1
            "snide_turnins_to_pool": "item_rando_list_1",
            "time_of_day": "item_rando_list_1",  # Adds day/night items, not forest_time_of_day
            # Complex conversions that need special handling beyond simple assignment
            "kong_models": "kong_model_dk",  # Converted to dict in special handler
            "krusha_model_mode": "kong_model_dk",  # Converted via match statement
            # switchsanity is an OptionDict - each key maps to a standalone switchsanity_switch_* key
            "switchsanity": "switchsanity_enabled",  # Presence tracked via special handler
            # alter_switch_allocation is an OptionDict - per-level data lives in prog_slam_level_1..8
            "alter_switch_allocation": "alter_switch_allocation",  # Reconstructed via special handler
        }

        # Combine auto-discovered mappings with manual overrides
        # Manual overrides take precedence
        combined_mappings = {**auto_mappings, **manual_overrides}

        # Build the bidirectional mappings
        for ap_name in self.options_metadata.keys():
            if ap_name in combined_mappings:
                settings_name = combined_mappings[ap_name]
            else:
                # Try exact match as fallback
                settings_name = ap_name

            self.ap_to_settings_map[ap_name] = settings_name
            self.settings_to_ap_map[settings_name] = ap_name

    def _convert_value_to_ap(self, ap_field: str, value: Any, settings_dict: Dict) -> Any:
        """Convert a standalone value to Archipelago format."""
        if ap_field not in self.options_metadata:
            # No metadata - just try to handle lists
            if isinstance(value, (list, set, tuple)):
                return self._convert_list_value(ap_field, value)
            return value

        option_info = self.options_metadata[ap_field]
        option_type = option_info["type"]

        # Override type detection for lists
        if isinstance(value, (list, set, tuple)) and option_type != "list":
            option_type = "list"

        # Handle different option types
        if option_type == "toggle":
            # Convert various boolean representations
            if isinstance(value, bool):
                return value
            elif isinstance(value, str):
                return value.lower() in ("true", "1", "yes", "on")
            elif isinstance(value, int):
                return bool(value)
            return bool(value)

        elif option_type == "range":
            # Ensure it's an integer within range
            try:
                int_value = int(value)
                min_val = option_info["metadata"]["min"]
                max_val = option_info["metadata"]["max"]
                return max(min_val, min(max_val, int_value))
            except (ValueError, TypeError):
                return option_info["default"]

        elif option_type == "choice":
            # Convert enum or string to choice name
            choices = option_info["metadata"]["choices"]

            # Special handling for specific fields
            if ap_field == "logic_type":
                logic_map = {
                    "nologic": "minimal",
                    "glitch": "glitched",
                    "glitchless": "glitchless",
                    0: "minimal",
                    1: "glitchless",
                    2: "glitched",
                }
                return logic_map.get(value, "glitchless")

            elif ap_field == "goal":
                # Convert standalone win_condition_item to Archipelago goal
                # First convert from enum integer if needed
                if isinstance(value, int):
                    try:
                        from randomizer.Enums.Settings import WinConditionComplex

                        value = WinConditionComplex(value).name
                    except (ImportError, ValueError):
                        pass
                elif hasattr(value, "name"):
                    value = value.name
                return self._convert_goal_from_standalone(str(value))

            elif ap_field == "shop_prices":
                # Convert shops_dont_cost bool to price setting
                if isinstance(value, bool):
                    return "free" if value else "medium"
                return value

            elif ap_field == "climbing_shuffle" or ap_field == "cannon_shuffle":
                # Convert status enum to bool
                if hasattr(value, "name"):
                    return value.name == "shuffled"
                return value in ("shuffled", 1, True)

            elif ap_field == "loading_zone_rando":
                # Convert ShuffleLoadingZones enum to bool
                if hasattr(value, "name"):
                    return value.name != "none"
                return value not in ("none", 0, False)

            # Try to match by name or value
            if hasattr(value, "name"):
                return value.name
            elif isinstance(value, str):
                return value
            elif isinstance(value, int):
                # Find choice name by value
                for choice_name, choice_val in choices.items():
                    if choice_val == value:
                        return choice_name

            return value

        elif option_type == "list":
            return self._convert_list_value(ap_field, value)

        elif option_type == "dict":
            # Ensure all keys are populated for OptionDict types (Archipelago expects all keys)
            if isinstance(value, dict):
                return self._populate_dict_keys(ap_field, value)
            return self._populate_dict_keys(ap_field, {})

        return value

    def _convert_list_value(self, ap_field: str, value: Any) -> list:
        """Convert a list value with special enum handling."""
        # Ensure it's a list
        if isinstance(value, (list, set, tuple)):
            # Special handling for enemies_selected - convert enum IDs to names
            if ap_field == "enemies_selected":
                return self._convert_enemy_ids_to_names(value)
            # Special handling for remove_barriers_selected
            elif ap_field == "remove_barriers_selected":
                return self._convert_barriers_to_names(value)
            # Special handling for tricks_selected
            elif ap_field == "tricks_selected":
                return self._convert_tricks_to_names(value)
            # Special handling for glitches_selected
            elif ap_field == "glitches_selected":
                return self._convert_glitches_to_names(value)
            # Special handling for hard_mode_selected
            elif ap_field == "hard_mode_selected":
                return self._convert_hard_mode_to_names(value)
            # Special handling for harder_bosses
            elif ap_field == "harder_bosses":
                return self._convert_hard_bosses_to_names(value)
            # Special handling for shuffled_bonus_barrels
            elif ap_field == "shuffled_bonus_barrels":
                return self._convert_minigames_to_names(value)
            # Special handling for allowed_bosses
            elif ap_field == "allowed_bosses":
                return self._convert_allowed_bosses_to_names(value)
            return list(value)
        elif value:
            return [value]
        return []

    def _populate_dict_keys(self, ap_field: str, value: dict) -> dict:
        """Ensure all expected keys are populated in OptionDict values."""
        # Define expected keys and defaults for each OptionDict type
        dict_defaults = {
            "goal_quantity": {
                "golden_bananas": 100,
                "blueprints": 20,
                "company_coins": 2,
                "keys": 8,
                "medals": 15,
                "crowns": 5,
                "fairies": 15,
                "rainbow_coins": 10,
                "pearls": 3,
                "bosses": 7,
                "bonuses": 15,
            },
            "helm_door_item_count": {
                "golden_bananas": 1,
                "blueprints": 1,
                "company_coins": 1,
                "keys": 1,
                "medals": 1,
                "crowns": 1,
                "fairies": 1,
                "rainbow_coins": 1,
                "bean": 1,
                "pearls": 1,
            },
            "level_blockers": {
                "level_1": 0,
                "level_2": 0,
                "level_3": 0,
                "level_4": 0,
                "level_5": 0,
                "level_6": 0,
                "level_7": 0,
                "level_8": 64,
            },
            "alter_switch_allocation": {
                "level_1": "green",
                "level_2": "green",
                "level_3": "green",
                "level_4": "green",
                "level_5": "blue",
                "level_6": "blue",
                "level_7": "red",
                "level_8": "red",
            },
            "switchsanity": {
                "isles_to_kroc_top": "off",
                "isles_helm_lobby": "off",
                "isles_aztec_lobby_back_room": "off",
                "isles_fungi_lobby_fairy": "off",
                "isles_spawn_rocketbarrel": "off",
                "japes_to_hive": "off",
                "japes_to_rambi": "off",
                "japes_to_painting_room": "off",
                "japes_to_cavern": "off",
                "japes_free_kong": "off",
                "aztec_to_kasplat_room": "off",
                "aztec_llama_front": "off",
                "aztec_llama_side": "off",
                "aztec_llama_back": "off",
                "aztec_sand_tunnel": "off",
                "aztec_to_connector_tunnel": "off",
                "aztec_free_lanky": "off",
                "aztec_free_tiny": "off",
                "aztec_gong_tower": "off",
                "aztec_lobby_gong": "off",
                "factory_free_kong": "off",
                "factory_dark_grate": "off",
                "factory_bonus_grate": "off",
                "factory_monster_grate": "off",
                "galleon_to_lighthouse_side": "off",
                "galleon_to_shipwreck_side": "off",
                "galleon_to_cannon_game": "off",
                "fungi_yellow_tunnel": "off",
                "fungi_green_tunnel_near": "off",
                "fungi_green_tunnel_far": "off",
                "caves_gone_cave": "off",
                "caves_snide_cave": "off",
                "caves_boulder_cave": "off",
                "caves_lobby_blueprint": "off",
                "caves_lobby_lava": "off",
            },
        }

        # Get the default values for this field
        if ap_field in dict_defaults:
            defaults = dict_defaults[ap_field]
            # Create a new dict with all keys populated
            result = {}
            for key in defaults.keys():
                if key in value:
                    result[key] = value[key]
                else:
                    result[key] = defaults[key]
            return result

        # For unknown dict types, just return the value as-is
        return value

    def _convert_enemy_ids_to_names(self, enemy_ids: list) -> list:
        """Convert enemy enum IDs to their string names for Archipelago."""
        try:
            from randomizer.Enums.Enemies import Enemies

            # Reverse mapping from FillSettings.py enemy_mapping
            enemies_reverse_map = {
                Enemies.Bat: "Bat",
                Enemies.BeaverBlue: "BeaverBlue",
                Enemies.BeaverGold: "BeaverGold",
                Enemies.Bug: "Bug",
                Enemies.FireballGlasses: "FireballGlasses",
                Enemies.GetOut: "GetOut",
                Enemies.Ghost: "Ghost",
                Enemies.Gimpfish: "Gimpfish",
                Enemies.Kaboom: "Kaboom",
                Enemies.KasplatChunky: "ChunkyKasplat",
                Enemies.KasplatDK: "DKKasplat",
                Enemies.KasplatDiddy: "DiddyKasplat",
                Enemies.KasplatLanky: "LankyKasplat",
                Enemies.KasplatTiny: "TinyKasplat",
                Enemies.KlaptrapGreen: "GreenKlaptrap",
                Enemies.KlaptrapPurple: "PurpleKlaptrap",
                Enemies.KlaptrapRed: "RedKlaptrap",
                Enemies.Klobber: "Klobber",
                Enemies.Klump: "Klump",
                Enemies.Guard: "Kop",
                Enemies.Kosha: "Kosha",
                Enemies.Kremling: "Kremling",
                Enemies.Krossbones: "Krossbones",
                Enemies.MrDice0: "GreenDice",
                Enemies.MrDice1: "RedDice",
                Enemies.MushroomMan: "MushroomMan",
                Enemies.Pufftup: "Pufftup",
                Enemies.RoboKremling: "RoboKremling",
                Enemies.ZingerRobo: "ZingerRobo",
                Enemies.Ruler: "Ruler",
                Enemies.Shuri: "Shuri",
                Enemies.SirDomino: "SirDomino",
                Enemies.SpiderSmall: "SpiderSmall",
                Enemies.ZingerCharger: "ZingerCharger",
                Enemies.ZingerLime: "ZingerLime",
                Enemies.GuardDisableA: "DisableAKop",
                Enemies.GuardDisableZ: "DisableZKop",
                Enemies.GuardTag: "DisableTaggingKop",
                Enemies.GuardGetOut: "GetOutKop",
            }

            enemy_names = []
            for enemy_id in enemy_ids:
                if isinstance(enemy_id, int):
                    try:
                        enemy_enum = Enemies(enemy_id)
                        enemy_name = enemies_reverse_map.get(enemy_enum)
                        if enemy_name:
                            enemy_names.append(enemy_name)
                        else:
                            logging.warning(f"Unknown enemy enum: {enemy_enum}")
                    except ValueError:
                        logging.warning(f"Unknown enemy ID: {enemy_id}")
                elif hasattr(enemy_id, "value"):
                    # Already an enum
                    enemy_name = enemies_reverse_map.get(enemy_id)
                    if enemy_name:
                        enemy_names.append(enemy_name)
                else:
                    # Already a string
                    enemy_names.append(str(enemy_id))
            return enemy_names
        except ImportError:
            logging.warning("Could not import Enemies enum for conversion")
            return [str(x) for x in enemy_ids]

    def _convert_barriers_to_names(self, barrier_ids: list) -> list:
        """Convert barrier enum IDs to their string names for Archipelago."""
        try:
            from randomizer.Enums.Settings import RemovedBarriersSelected

            # Reverse mapping from FillSettings.py barrier match cases
            barriers_reverse_map = {
                RemovedBarriersSelected.japes_coconut_gates: "japes_coconut_gates",
                RemovedBarriersSelected.japes_shellhive_gate: "japes_shellhive_gate",
                RemovedBarriersSelected.aztec_tunnel_door: "aztec_tunnel_door",
                RemovedBarriersSelected.aztec_5dtemple_switches: "aztec_5dtemple_switches",
                RemovedBarriersSelected.aztec_llama_switches: "aztec_llama_switches",
                RemovedBarriersSelected.aztec_tiny_temple_ice: "aztec_tiny_temple_ice",
                RemovedBarriersSelected.factory_testing_gate: "factory_testing_gate",
                RemovedBarriersSelected.factory_production_room: "factory_production_room",
                RemovedBarriersSelected.galleon_lighthouse_gate: "galleon_lighthouse_gate",
                RemovedBarriersSelected.galleon_shipyard_area_gate: "galleon_shipyard_area_gate",
                RemovedBarriersSelected.castle_crypt_doors: "castle_crypt_doors",
                RemovedBarriersSelected.galleon_seasick_ship: "galleon_seasick_ship",
                RemovedBarriersSelected.forest_green_tunnel: "forest_green_tunnel",
                RemovedBarriersSelected.forest_yellow_tunnel: "forest_yellow_tunnel",
                RemovedBarriersSelected.caves_igloo_pads: "caves_igloo_pads",
                RemovedBarriersSelected.caves_ice_walls: "caves_ice_walls",
                RemovedBarriersSelected.galleon_treasure_room: "galleon_treasure_room",
                RemovedBarriersSelected.helm_star_gates: "helm_star_gates",
                RemovedBarriersSelected.helm_punch_gates: "helm_punch_gates",
            }

            barrier_names = []
            for barrier_id in barrier_ids:
                if isinstance(barrier_id, int):
                    try:
                        barrier_enum = RemovedBarriersSelected(barrier_id)
                        barrier_name = barriers_reverse_map.get(barrier_enum)
                        if barrier_name:
                            barrier_names.append(barrier_name)
                    except ValueError:
                        logging.warning(f"Unknown barrier ID: {barrier_id}")
                elif hasattr(barrier_id, "value"):
                    barrier_name = barriers_reverse_map.get(barrier_id)
                    if barrier_name:
                        barrier_names.append(barrier_name)
                else:
                    barrier_names.append(str(barrier_id))
            return barrier_names
        except ImportError:
            logging.warning("Could not import RemovedBarriersSelected enum")
            return [str(x) for x in barrier_ids]

    def _convert_tricks_to_names(self, trick_ids: list) -> list:
        """Convert tricks enum IDs to their string names for Archipelago."""
        try:
            from randomizer.Enums.Settings import TricksSelected

            tricks_reverse_map = {
                TricksSelected.monkey_maneuvers: "monkey_maneuvers",
                TricksSelected.hard_shooting: "hard_shooting",
                TricksSelected.advanced_grenading: "advanced_grenading",
                TricksSelected.slope_resets: "slope_resets",
            }

            trick_names = []
            for trick_id in trick_ids:
                if isinstance(trick_id, int):
                    try:
                        trick_enum = TricksSelected(trick_id)
                        trick_name = tricks_reverse_map.get(trick_enum)
                        if trick_name:
                            trick_names.append(trick_name)
                    except ValueError:
                        logging.warning(f"Unknown trick ID: {trick_id}")
                elif hasattr(trick_id, "value"):
                    trick_name = tricks_reverse_map.get(trick_id)
                    if trick_name:
                        trick_names.append(trick_name)
                else:
                    trick_names.append(str(trick_id))
            return trick_names
        except ImportError:
            return [str(x) for x in trick_ids]

    def _convert_glitches_to_names(self, glitch_ids: list) -> list:
        """Convert glitches enum IDs to their string names for Archipelago."""
        try:
            from randomizer.Enums.Settings import GlitchesSelected

            glitches_reverse_map = {
                GlitchesSelected.moonkicks: "moonkicks",
                GlitchesSelected.phase_swimming: "phase_swimming",
                GlitchesSelected.swim_through_shores: "swim_through_shores",
                GlitchesSelected.troff_n_scoff_skips: "troff_n_scoff_skips",
                GlitchesSelected.moontail: "moontail",
            }

            glitch_names = []
            for glitch_id in glitch_ids:
                if isinstance(glitch_id, int):
                    try:
                        glitch_enum = GlitchesSelected(glitch_id)
                        glitch_name = glitches_reverse_map.get(glitch_enum)
                        if glitch_name:
                            glitch_names.append(glitch_name)
                    except ValueError:
                        logging.warning(f"Unknown glitch ID: {glitch_id}")
                elif hasattr(glitch_id, "value"):
                    glitch_name = glitches_reverse_map.get(glitch_id)
                    if glitch_name:
                        glitch_names.append(glitch_name)
                else:
                    glitch_names.append(str(glitch_id))
            return glitch_names
        except ImportError:
            return [str(x) for x in glitch_ids]

    def _convert_hard_mode_to_names(self, hard_mode_ids: list) -> list:
        """Convert hard mode enum IDs to their string names for Archipelago."""
        try:
            from randomizer.Enums.Settings import HardModeSelected

            hard_mode_reverse_map = {
                HardModeSelected.hard_enemies: "hard_enemies",
                HardModeSelected.shuffled_jetpac_enemies: "shuffled_jetpac_enemies",
                HardModeSelected.strict_helm_timer: "strict_helm_timer",
                HardModeSelected.donk_in_the_dark_world: "donk_in_the_dark_world",
                HardModeSelected.donk_in_the_sky: "donk_in_the_sky",
                HardModeSelected.angry_caves: "angry_caves",
                HardModeSelected.fast_balloons: "fast_balloons",
                HardModeSelected.lower_max_refill_amounts: "lower_max_refill_amounts",
            }

            hard_mode_names = []
            for hm_id in hard_mode_ids:
                if isinstance(hm_id, int):
                    try:
                        hm_enum = HardModeSelected(hm_id)
                        hm_name = hard_mode_reverse_map.get(hm_enum)
                        if hm_name:
                            hard_mode_names.append(hm_name)
                    except ValueError:
                        logging.warning(f"Unknown hard mode ID: {hm_id}")
                elif hasattr(hm_id, "value"):
                    hm_name = hard_mode_reverse_map.get(hm_id)
                    if hm_name:
                        hard_mode_names.append(hm_name)
                else:
                    hard_mode_names.append(str(hm_id))
            return hard_mode_names
        except ImportError:
            return [str(x) for x in hard_mode_ids]

    def _convert_hard_bosses_to_names(self, hard_boss_ids: list) -> list:
        """Convert hard boss enum IDs to their string names for Archipelago."""
        try:
            from randomizer.Enums.Settings import HardBossesSelected

            hard_bosses_reverse_map = {
                HardBossesSelected.fast_mad_jack: "fast_mad_jack",
                HardBossesSelected.alternative_mad_jack_kongs: "alternative_mad_jack_kongs",
                HardBossesSelected.pufftoss_star_rando: "pufftoss_star_rando",
                HardBossesSelected.pufftoss_star_raised: "pufftoss_star_raised",
                HardBossesSelected.kut_out_phase_rando: "kut_out_phase_rando",
                HardBossesSelected.k_rool_toes_rando: "k_rool_toes_rando",
                HardBossesSelected.beta_lanky_phase: "beta_lanky_phase",
            }

            hard_boss_names = []
            for hb_id in hard_boss_ids:
                if isinstance(hb_id, int):
                    try:
                        hb_enum = HardBossesSelected(hb_id)
                        hb_name = hard_bosses_reverse_map.get(hb_enum)
                        if hb_name:
                            hard_boss_names.append(hb_name)
                    except ValueError:
                        logging.warning(f"Unknown hard boss ID: {hb_id}")
                elif hasattr(hb_id, "value"):
                    hb_name = hard_bosses_reverse_map.get(hb_id)
                    if hb_name:
                        hard_boss_names.append(hb_name)
                else:
                    hard_boss_names.append(str(hb_id))
            return hard_boss_names
        except ImportError:
            return [str(x) for x in hard_boss_ids]

    def _convert_minigames_to_names(self, minigame_ids: list) -> list:
        """Convert minigame enum IDs to their string names for Archipelago."""
        try:
            from randomizer.Enums.Settings import MinigamesListSelected

            # Archipelago uses the enum names directly
            minigame_names = []
            for mg_id in minigame_ids:
                if isinstance(mg_id, int):
                    try:
                        mg_enum = MinigamesListSelected(mg_id)
                        minigame_names.append(mg_enum.name)
                    except ValueError:
                        logging.warning(f"Unknown minigame ID: {mg_id}")
                elif hasattr(mg_id, "name"):
                    minigame_names.append(mg_id.name)
                else:
                    minigame_names.append(str(mg_id))
            return minigame_names
        except ImportError:
            return [str(x) for x in minigame_ids]

    def _convert_allowed_bosses_to_names(self, boss_ids: list) -> list:
        """Convert boss Map enum IDs to their string names for Archipelago."""
        try:
            from randomizer.Enums.Maps import Maps

            # Reverse mapping from FillSettings.py boss_mapping
            bosses_reverse_map = {
                Maps.JapesBoss: "Armydillo 1",
                Maps.AztecBoss: "Dogadon 1",
                Maps.FactoryBoss: "Mad Jack",
                Maps.GalleonBoss: "Pufftoss",
                Maps.FungiBoss: "Dogadon 2",
                Maps.CavesBoss: "Armydillo 2",
                Maps.CastleBoss: "Kutout",
                Maps.KroolDonkeyPhase: "DK phase",
                Maps.KroolDiddyPhase: "Diddy Phase",
                Maps.KroolLankyPhase: "Lanky Phase",
                Maps.KroolTinyPhase: "Tiny Phase",
                Maps.KroolChunkyPhase: "Chunky Phase",
            }

            boss_names = []
            for boss_id in boss_ids:
                if isinstance(boss_id, int):
                    try:
                        boss_enum = Maps(boss_id)
                        boss_name = bosses_reverse_map.get(boss_enum)
                        if boss_name:
                            boss_names.append(boss_name)
                    except ValueError:
                        logging.warning(f"Unknown boss ID: {boss_id}")
                elif hasattr(boss_id, "value"):
                    boss_name = bosses_reverse_map.get(boss_id)
                    if boss_name:
                        boss_names.append(boss_name)
                else:
                    boss_names.append(str(boss_id))
            return boss_names
        except ImportError:
            return [str(x) for x in boss_ids]

    def _convert_enum_id_to_name(self, field_name: str, enum_id: int) -> str:
        """Convert an enum ID to its string name for various option types."""
        # For now, just convert to string - this can be enhanced later
        # with specific enum mappings for each field type
        return str(enum_id)

    def _get_special_value(self, ap_field: str, settings_dict: Dict) -> Any:
        """
        Get special values that don't have a direct standalone setting mapping.

        For example, some Archipelago options control what items go into item_rando_list_1
        rather than having their own dedicated setting.
        """
        # Handle options that check item_rando_list_1
        item_rando_list_1 = settings_dict.get("item_rando_list_1", [])

        # Map AP field to the ItemRandoListSelected value to check for
        item_list_checks = {
            "hints_in_item_pool": "hint",  # ItemRandoListSelected.hint = 34
            "boulders_in_pool": "dummyitem_boulderitem",  # ItemRandoListSelected.dummyitem_boulderitem = 39
            "dropsanity": "dummyitem_enemies",  # ItemRandoListSelected.dummyitem_enemies = 38
            "half_medals_in_pool": "dummyitem_halfmedal",  # ItemRandoListSelected.dummyitem_halfmedal = 44
            "snide_turnins_to_pool": "blueprintbanana",  # ItemRandoListSelected.blueprintbanana
            "time_of_day": "fungitime",  # ItemRandoListSelected.fungitime - adds day/night items
        }

        if ap_field in item_list_checks:
            check_value = item_list_checks[ap_field]
            # Check if the item is in the list (could be enum or string)
            for item in item_rando_list_1:
                if hasattr(item, "name") and item.name == check_value:
                    return True
                elif isinstance(item, str) and item == check_value:
                    return True
                elif isinstance(item, int):
                    # Try to convert to enum name
                    try:
                        from randomizer.Enums.Settings import ItemRandoListSelected

                        enum_obj = ItemRandoListSelected(item)
                        if enum_obj.name == check_value:
                            return True
                    except Exception as e:
                        logging.warning(f"Error converting item {item} to ItemRandoListSelected: {e}")
            # Log if we didn't find it
            logging.info(f"{ap_field}: Looking for '{check_value}' in item_rando_list_1={item_rando_list_1}, not found")
            return False

        # enable_chaos_blockers: True if blocker_selection_behavior == BLockerSetting.chaos
        if ap_field == "enable_chaos_blockers":
            blocker_behavior = settings_dict.get("blocker_selection_behavior")
            if blocker_behavior is not None:
                try:
                    from randomizer.Enums.Settings import BLockerSetting

                    if hasattr(blocker_behavior, "value"):
                        return blocker_behavior == BLockerSetting.chaos
                    elif isinstance(blocker_behavior, int):
                        return blocker_behavior == BLockerSetting.chaos.value
                except ImportError:
                    pass
            return False

        # enable_cutscenes: False if more_cutscene_skips is ExtraCutsceneSkips.auto
        if ap_field == "enable_cutscenes":
            cutscene_skips = settings_dict.get("more_cutscene_skips")
            if cutscene_skips is not None:
                try:
                    from randomizer.Enums.Settings import ExtraCutsceneSkips

                    if hasattr(cutscene_skips, "value"):
                        return cutscene_skips != ExtraCutsceneSkips.auto
                    elif isinstance(cutscene_skips, int):
                        return cutscene_skips != ExtraCutsceneSkips.auto.value
                except ImportError:
                    pass
            return None

        # enable_shared_shops: True if smaller_shops is enabled
        if ap_field == "enable_shared_shops":
            smaller_shops = settings_dict.get("smaller_shops")
            if smaller_shops is not None:
                return bool(smaller_shops)
            return None

        # galleon_water_level: Convert GalleonWaterLevel enum
        if ap_field == "galleon_water_level":
            water_level = settings_dict.get("GalleonWaterLevel")
            if water_level is not None:
                try:
                    from randomizer.Enums.Settings import GalleonWaterLevel

                    if hasattr(water_level, "name"):
                        return water_level.name.lower()
                    elif isinstance(water_level, int):
                        return GalleonWaterLevel(water_level).name.lower()
                except ImportError:
                    pass
            return None

        # hard_minigames: Opposite of disable_hard_minigames
        if ap_field == "hard_minigames":
            disable_hard = settings_dict.get("disable_hard_minigames")
            if disable_hard is not None:
                return not bool(disable_hard)
            return None

        # krool_in_boss_pool: Based on krool_in_boss_pool_v2
        if ap_field == "krool_in_boss_pool":
            krool_v2 = settings_dict.get("krool_in_boss_pool_v2")
            if krool_v2 is not None:
                return bool(krool_v2)
            return None

        # dk_portal_location_rando: Convert dk_portal_location_rando_v2 enum
        if ap_field == "dk_portal_location_rando":
            portal_v2 = settings_dict.get("dk_portal_location_rando_v2")
            if portal_v2 is not None:
                try:
                    from randomizer.Enums.Settings import DKPortalLocations

                    if hasattr(portal_v2, "name"):
                        return portal_v2.name.lower()
                    elif isinstance(portal_v2, int):
                        return DKPortalLocations(portal_v2).name.lower()
                except ImportError:
                    pass
            return None

        # random_starting_region: Convert random_starting_region_new enum
        if ap_field == "random_starting_region":
            random_start = settings_dict.get("random_starting_region_new")
            if random_start is not None:
                try:
                    from randomizer.Enums.Settings import RandomStartingRegion

                    if hasattr(random_start, "name"):
                        return random_start.name.lower()
                    elif isinstance(random_start, int):
                        return RandomStartingRegion(random_start).name.lower()
                except ImportError:
                    pass
            return None

        # randomize_blocker_required_amounts: True if behavior is normal_random, easy_random, or hard_random
        if ap_field == "randomize_blocker_required_amounts":
            blocker_behavior = settings_dict.get("blocker_selection_behavior")
            if blocker_behavior is not None:
                try:
                    from randomizer.Enums.Settings import BLockerSetting

                    random_settings = [BLockerSetting.normal_random, BLockerSetting.easy_random, BLockerSetting.hard_random]
                    if hasattr(blocker_behavior, "value"):
                        return blocker_behavior in random_settings
                    elif isinstance(blocker_behavior, int):
                        return blocker_behavior in [s.value for s in random_settings]
                except ImportError:
                    pass
            return False

        # shop_prices: Convert random_prices enum
        if ap_field == "shop_prices":
            random_prices = settings_dict.get("random_prices")
            if random_prices is not None:
                return int(random_prices) if isinstance(random_prices, (int, float)) else 0
            return None

        # loading_zone_rando: Check if LevelRandomization is loadingzone
        if ap_field == "loading_zone_rando":
            level_rand = settings_dict.get("LevelRandomization")
            if level_rand is not None:
                try:
                    from randomizer.Enums.Settings import LevelRandomization

                    if hasattr(level_rand, "name"):
                        return level_rand.name == "loadingzone"
                    elif isinstance(level_rand, int):
                        return LevelRandomization(level_rand).name == "loadingzone"
                except ImportError:
                    pass
            return False

        # cannon_shuffle: True if the Cannons item appears in any starting move pool (1-5)
        if ap_field == "cannon_shuffle":
            try:
                from randomizer.Lists.Item import ItemList
                from randomizer.Enums.Items import Items as ItemsEnum

                for pool_num in range(1, 6):
                    pool_items = settings_dict.get(f"starting_moves_list_{pool_num}", [])
                    for item_id in pool_items:
                        if isinstance(item_id, int):
                            try:
                                item_id = ItemsEnum(item_id)
                            except ValueError:
                                continue
                        item_obj = ItemList.get(item_id)
                        if item_obj is not None and item_obj.name == "Cannons":
                            return True
            except ImportError:
                pass
            return False

        # climbing_shuffle: True if the Climbing item appears in any starting move pool (1-5)
        if ap_field == "climbing_shuffle":
            try:
                from randomizer.Lists.Item import ItemList
                from randomizer.Enums.Items import Items as ItemsEnum

                for pool_num in range(1, 6):
                    pool_items = settings_dict.get(f"starting_moves_list_{pool_num}", [])
                    for item_id in pool_items:
                        if isinstance(item_id, int):
                            try:
                                item_id = ItemsEnum(item_id)
                            except ValueError:
                                continue
                        item_obj = ItemList.get(item_id)
                        if item_obj is not None and item_obj.name == "Climbing":
                            return True
            except ImportError:
                pass
            return False

        # krusha_model_mode: Check which kongs have krusha model (specifically model type 2)
        if ap_field == "krusha_model_mode":
            try:
                from randomizer.Enums.Settings import KongModels

                krusha_kongs = []
                for kong in ["dk", "diddy", "lanky", "tiny", "chunky"]:
                    model = settings_dict.get(f"kong_model_{kong}")
                    if model is not None:
                        # Check if it's specifically the krusha model (value 2)
                        # Ignore other cosmetic models (disco_chunky, krool_fight, cranky, etc.)
                        if hasattr(model, "value"):
                            if model.value == 2:  # KongModels.krusha
                                krusha_kongs.append(kong)
                        elif isinstance(model, int):
                            if model == 2:  # KongModels.krusha value
                                krusha_kongs.append(kong)

                # Return mode based on how many krushas
                if len(krusha_kongs) == 0:
                    return "off"
                else:
                    # Default to manual mode if any krushas are set
                    return "manual"
            except ImportError:
                pass
            return None

        # kong_models: Export as a dict mapping kong names to their model values
        if ap_field == "kong_models":
            try:
                from randomizer.Enums.Settings import KongModels as KongModelsEnum

                kong_models_dict = {}

                # Map enum values to their string names
                model_value_to_name = {
                    0: "default",
                    1: "disco_chunky",
                    2: "krusha",
                    3: "krool_fight",
                    4: "krool_cutscene",
                    5: "cranky",
                    6: "candy",
                    7: "funky",
                    8: "disco_donkey",
                    9: "robokrem",
                }

                # Always include all 5 kongs (Archipelago expects all keys for OptionDict)
                for kong in ["dk", "diddy", "lanky", "tiny", "chunky"]:
                    model = settings_dict.get(f"kong_model_{kong}")
                    if model is not None:
                        # Get the model value
                        model_value = model.value if hasattr(model, "value") else model
                        model_name = model_value_to_name.get(model_value, "default")
                        kong_models_dict[kong] = model_name
                    else:
                        # Default to "default" if not found
                        kong_models_dict[kong] = "default"

                return kong_models_dict
            except ImportError:
                pass
            return None

        # goal_quantity: Convert win_condition_count (single value) to dict with all goal types
        if ap_field == "goal_quantity":
            win_condition_count = settings_dict.get("win_condition_count")
            win_condition_item = settings_dict.get("win_condition_item")

            # Create full dict with all goal types
            goal_quantity_dict = {
                "golden_bananas": 100,
                "blueprints": 20,
                "company_coins": 2,
                "keys": 8,
                "medals": 15,
                "crowns": 5,
                "fairies": 15,
                "rainbow_coins": 10,
                "pearls": 3,
                "bosses": 7,
                "bonuses": 15,
            }

            # If we have a win_condition_count, set it for the appropriate goal type
            if win_condition_count is not None and win_condition_item is not None:
                # Map win_condition_item to goal_quantity key
                try:
                    from randomizer.Enums.Settings import WinConditionComplex

                    if hasattr(win_condition_item, "value"):
                        item_value = win_condition_item.value
                    else:
                        item_value = int(win_condition_item)

                    # Map WinConditionComplex enum to goal_quantity keys
                    goal_type_map = {
                        3: "golden_bananas",  # WinConditionComplex.req_gb
                        4: "blueprints",  # WinConditionComplex.req_bp
                        5: "company_coins",  # WinConditionComplex.req_companycoins
                        6: "keys",  # WinConditionComplex.req_key
                        7: "medals",  # WinConditionComplex.req_medal
                        8: "crowns",  # WinConditionComplex.req_crown
                        9: "fairies",  # WinConditionComplex.req_fairy
                        10: "rainbow_coins",  # WinConditionComplex.req_rainbowcoin
                        12: "pearls",  # WinConditionComplex.req_pearl
                        17: "bosses",  # WinConditionComplex.req_bosses
                        18: "bonuses",  # WinConditionComplex.req_bonuses
                    }

                    goal_key = goal_type_map.get(item_value)
                    if goal_key:
                        goal_quantity_dict[goal_key] = int(win_condition_count) if win_condition_count else goal_quantity_dict[goal_key]
                except (ImportError, ValueError, TypeError):
                    pass

            return goal_quantity_dict

        # level_blockers: Convert blocker_text (single value or complex) to dict with all 8 levels
        if ap_field == "level_blockers":
            blocker_text = settings_dict.get("blocker_text")

            # Create full dict with all 8 levels
            level_blockers_dict = {
                "level_1": 0,
                "level_2": 0,
                "level_3": 0,
                "level_4": 0,
                "level_5": 0,
                "level_6": 0,
                "level_7": 0,
                "level_8": 64,
            }

            # If blocker_text is a simple number, set all levels to that value
            if blocker_text is not None:
                if isinstance(blocker_text, (int, float)):
                    # Single value - set all levels to this
                    value = int(blocker_text)
                    for i in range(1, 9):
                        level_blockers_dict[f"level_{i}"] = value
                elif isinstance(blocker_text, str):
                    # Could be a string representation of numbers
                    try:
                        value = int(blocker_text)
                        for i in range(1, 9):
                            level_blockers_dict[f"level_{i}"] = value
                    except ValueError:
                        pass

            return level_blockers_dict

        # switchsanity: Read individual switchsanity_switch_* standalone settings
        # and build the OptionDict with short key names
        if ap_field == "switchsanity":
            # Kong switches: SwitchsanityKong enum (0=donkey,1=diddy,2=lanky,3=tiny,4=chunky,5=random,6=any)
            kong_value_names = {0: "donkey", 1: "diddy", 2: "lanky", 3: "tiny", 4: "chunky", 5: "random", 6: "any"}
            # Gone switch (isles_helm_lobby): SwitchsanityGone enum (0=bongos...7=gone_pad,8=random)
            gone_value_names = {0: "bongos", 1: "guitar", 2: "trombone", 3: "sax", 4: "triangle", 5: "lever", 6: "gong", 7: "gone_pad", 8: "random"}

            gone_switches = {"isles_helm_lobby"}
            all_switches = [
                "isles_to_kroc_top",
                "isles_helm_lobby",
                "isles_aztec_lobby_back_room",
                "isles_fungi_lobby_fairy",
                "isles_spawn_rocketbarrel",
                "japes_to_hive",
                "japes_to_rambi",
                "japes_to_painting_room",
                "japes_to_cavern",
                "japes_free_kong",
                "aztec_to_kasplat_room",
                "aztec_llama_front",
                "aztec_llama_side",
                "aztec_llama_back",
                "aztec_sand_tunnel",
                "aztec_to_connector_tunnel",
                "aztec_free_lanky",
                "aztec_free_tiny",
                "aztec_gong_tower",
                "aztec_lobby_gong",
                "factory_free_kong",
                "factory_dark_grate",
                "factory_bonus_grate",
                "factory_monster_grate",
                "galleon_to_lighthouse_side",
                "galleon_to_shipwreck_side",
                "galleon_to_cannon_game",
                "fungi_yellow_tunnel",
                "fungi_green_tunnel_near",
                "fungi_green_tunnel_far",
                "caves_gone_cave",
                "caves_snide_cave",
                "caves_boulder_cave",
                "caves_lobby_blueprint",
                "caves_lobby_lava",
            ]

            result = {}
            for short_key in all_switches:
                full_key = f"switchsanity_switch_{short_key}"
                raw = settings_dict.get(full_key)
                if raw is None:
                    result[short_key] = "off"
                    continue
                # Resolve enum to int if needed
                int_val = raw.value if hasattr(raw, "value") else (int(raw) if isinstance(raw, int) else None)
                if int_val is None:
                    result[short_key] = "off"
                    continue
                if short_key in gone_switches:
                    result[short_key] = gone_value_names.get(int_val, "off")
                else:
                    result[short_key] = kong_value_names.get(int_val, "off")
            return result

        # alter_switch_allocation: reconstruct the OptionDict from the per-level prog_slam_level_* standalone settings.
        # In standalone, alter_switch_allocation is a boolean and prog_slam_level_1..8 are SlamRequirement enums.
        # SlamRequirement: no_slam=0 ("none"), green=1, blue=2, red=3
        if ap_field == "alter_switch_allocation":
            slam_name_map = {0: "none", 1: "green", 2: "blue", 3: "red"}
            result = {}
            for i in range(1, 9):
                raw = settings_dict.get(f"prog_slam_level_{i}")
                if raw is None:
                    # Fall back to AlterSwitchAllocation defaults: levels 1-4 green, 5-6 blue, 7-8 red
                    result[f"level_{i}"] = "green" if i <= 4 else ("blue" if i <= 6 else "red")
                else:
                    int_val = raw.value if hasattr(raw, "value") else (int(raw) if isinstance(raw, int) else None)
                    result[f"level_{i}"] = slam_name_map.get(int_val, "green")
            return result

        # helm_door_item_count: reconstruct the OptionDict from the per-door standalone settings.
        # In standalone settings there is no single helm_door_item_count key; instead
        # crown_door_item / crown_door_item_count and coin_door_item / coin_door_item_count
        # record which item type each door requires and how many of that item is needed.
        # We build the full OptionDict (one count per item type) from those four fields.
        if ap_field == "helm_door_item_count":
            # HelmDoorItem int value → helm_door_item_count dict key
            door_item_key_map = {
                3: "golden_bananas",  # req_gb
                4: "blueprints",  # req_bp
                5: "company_coins",  # req_companycoins
                6: "keys",  # req_key
                7: "medals",  # req_medal
                8: "crowns",  # req_crown
                9: "fairies",  # req_fairy
                10: "rainbow_coins",  # req_rainbowcoin
                11: "bean",  # req_bean
                12: "pearls",  # req_pearl
            }
            result = {
                "golden_bananas": 1,
                "blueprints": 1,
                "company_coins": 1,
                "keys": 1,
                "medals": 1,
                "crowns": 1,
                "fairies": 1,
                "rainbow_coins": 1,
                "bean": 1,
                "pearls": 1,
            }
            for door_key, count_key in [("crown_door_item", "crown_door_item_count"), ("coin_door_item", "coin_door_item_count")]:
                door_item = settings_dict.get(door_key)
                if door_item is not None:
                    int_val = door_item.value if hasattr(door_item, "value") else (int(door_item) if isinstance(door_item, int) else None)
                    item_key = door_item_key_map.get(int_val)
                    if item_key:
                        result[item_key] = settings_dict.get(count_key, 1)
            return result

        # starting_move_pool_N: Convert item IDs from starting_moves_list_N to AP string names.
        # The standalone stores integer Items enum values in starting_moves_list_N (set by the
        # form's <select id="starting_moves_list_N"> elements via serialize_settings).
        # AP expects a list of display-name strings matching _STARTING_MOVE_VALID_KEYS.
        # Note: ProgressiveSlam2/3, ProgressiveAmmoBelt2, ProgressiveInstrumentUpgrade2/3
        # are dummy items used only for the modal UI and have names with trailing spaces —
        # these must be normalized to the canonical base name (matching FillSettings.py logic).
        _PROGRESSIVE_NAME_NORMALIZE = {
            "Progressive Slam ": "Progressive Slam",
            "Progressive Slam  ": "Progressive Slam",
            "Progressive Ammo Belt ": "Progressive Ammo Belt",
            "Progressive Instrument Upgrade ": "Progressive Instrument Upgrade",
            "Progressive Instrument Upgrade  ": "Progressive Instrument Upgrade",
        }
        for _pool_num in range(1, 6):
            if ap_field == f"starting_move_pool_{_pool_num}":
                # Use sentinel to distinguish "key absent" (use AP defaults) from "key present but empty"
                pool_items = settings_dict.get(f"starting_moves_list_{_pool_num}")
                if pool_items is None:
                    # Key absent — return None so settings_to_yaml falls back to AP class defaults
                    return None
                if not pool_items:
                    # Key present but the pool was deliberately left empty
                    return []
                try:
                    from randomizer.Lists.Item import ItemList
                    from randomizer.Enums.Items import Items as ItemsEnum

                    item_names = []
                    for item_id in pool_items:
                        if isinstance(item_id, int):
                            try:
                                item_id = ItemsEnum(item_id)
                            except ValueError:
                                continue
                        item_obj = ItemList.get(item_id)
                        if item_obj is not None:
                            name = _PROGRESSIVE_NAME_NORMALIZE.get(item_obj.name, item_obj.name)
                            item_names.append(name)
                    return item_names if item_names else []
                except ImportError:
                    logging.warning(f"Could not import ItemList for starting_move_pool_{_pool_num} conversion")
                    return [str(x) for x in pool_items]

        # No special handling needed
        return None

    def _convert_goal_from_standalone(self, win_condition_item: str) -> str:
        """Convert standalone win_condition_item to Archipelago goal format."""
        # Mapping from standalone win_condition values to Archipelago goal values
        goal_mapping = {
            "get_keys_3_and_8": "acquire_keys_3_and_8",
            "get_key8": "acquire_key_8",
            "krem_kapture": "kremling_kapture",
            "dk_rap_items": "dk_rap",
            "req_gb": "golden_bananas",
            "req_bp": "blueprints",
            "req_companycoins": "company_coins",
            "req_key": "keys",
            "req_medal": "medals",
            "req_crown": "crowns",
            "req_fairy": "fairies",
            "req_rainbowcoin": "rainbow_coins",
            "req_bean": "bean",
            "req_pearl": "pearls",
            "req_bosses": "bosses",
            "req_bonuses": "bonuses",
            "beat_krool": "treasure_hurry",
            "krools_challenge": "krools_challenge",
            "kill_the_rabbit": "kill_the_rabbit",
            # Also handle some alternate forms
            "easy_random": "golden_bananas",  # Default to golden bananas for random
            "medium_random": "golden_bananas",
            "hard_random": "golden_bananas",
        }

        return goal_mapping.get(win_condition_item, win_condition_item)

    def settings_to_yaml(self, settings_dict: Dict, player_name: str = "Player", game_version: str = "0.6.6") -> str:
        """
        Convert standalone settings dictionary to Archipelago YAML format.

        Args:
            settings_dict: Dictionary of standalone randomizer settings
            player_name: Player name for the YAML
            game_version: Required Archipelago version

        Returns:
            YAML string ready to be saved to a file
        """
        if not self.options_metadata:
            return "# Error: Could not parse Archipelago options from Options.py"

        # Build the YAML structure
        yaml_data = {"name": player_name, "game": "Donkey Kong 64", "requires": {"version": game_version}, "Donkey Kong 64": {}}

        # Convert each Archipelago option
        default_options = {}  # Store options that used defaults

        for ap_field, settings_field in self.ap_to_settings_map.items():
            # Skip cosmetic settings
            if settings_field in self.SKIP_SETTINGS:
                continue

            # Check for special value handling first
            special_value = self._get_special_value(ap_field, settings_dict)
            if special_value is not None:
                value = special_value
            else:
                # Get value from settings - if not present, use the Archipelago default
                value = settings_dict.get(settings_field)

            # Track if we're using a default value
            using_default = False
            if value is None:
                if ap_field in self.options_metadata:
                    default_value = self.options_metadata[ap_field].get("default")
                    if default_value is not None:
                        value = default_value
                        using_default = True
                    else:
                        # Skip options with no value and no default
                        continue
                else:
                    continue

            # Convert the value to AP format
            converted_value = self._convert_value_to_ap(ap_field, value, settings_dict)

            # Special handling for specific options
            if ap_field == "death_link":
                # Only add if enabled
                if converted_value:
                    yaml_data["Donkey Kong 64"][ap_field] = converted_value
                continue

            # Add to YAML (use string format for better readability)
            if converted_value is not None:
                # Convert booleans to strings for YAML readability
                if isinstance(converted_value, bool):
                    formatted_value = "true" if converted_value else "false"
                else:
                    formatted_value = converted_value

                # Store in appropriate dict
                if using_default:
                    default_options[ap_field] = formatted_value
                else:
                    yaml_data["Donkey Kong 64"][ap_field] = formatted_value

        # Generate YAML string with nice formatting
        yaml_str = yaml.dump(yaml_data, default_flow_style=False, sort_keys=False, allow_unicode=True, width=120)

        # Add default settings section if any
        if default_options:
            # Remove the closing line and add default settings
            yaml_str = yaml_str.rstrip("\n") + "\n"
            yaml_str += "  # Default settings (not found in form data):\n"
            for ap_field, value in sorted(default_options.items()):
                if isinstance(value, list):
                    yaml_str += f"  {ap_field}:\n"
                    for item in value:
                        yaml_str += f"  - {item}\n"
                else:
                    yaml_str += f"  {ap_field}: {value}\n"

        # Add a comment header
        header = "# Donkey Kong 64 Randomizer\n" "# Generated from https://dk64randomizer.com \n" "\n"

        return header + yaml_str

    def generate_triggers(self, settings_dict: Dict) -> List[Dict]:
        """
        Generate Archipelago triggers based on standalone settings.

        Triggers add items to start_inventory based on certain conditions.
        For example, if starting with 5 kongs, add all kongs to start_inventory.

        Args:
            settings_dict: Dictionary of standalone randomizer settings

        Returns:
            List of trigger dictionaries
        """
        triggers = []

        # Example: Starting Kongs trigger
        starting_kongs_count = settings_dict.get("starting_kongs_count", 1)
        if starting_kongs_count > 1:
            kong_names = ["Diddy", "Lanky", "Tiny", "Chunky"]
            start_inventory = {}

            # Add kongs based on count (Donkey is always available)
            for i in range(min(starting_kongs_count - 1, 4)):
                start_inventory[kong_names[i]] = 1

            triggers.append(
                {"option_category": "Donkey Kong 64", "option_name": "starting_kong_count", "option_result": starting_kongs_count, "options": {"Donkey Kong 64": {"+start_inventory": start_inventory}}}
            )

        # Example: Starting Moves trigger
        starting_moves_count = settings_dict.get("starting_moves_count", 0)
        if starting_moves_count > 0:
            # This would need more complex logic to determine which moves
            # For now, just note that moves were requested
            pass

        return triggers


# Global instance
_mapper_instance = None


def get_mapper() -> ArchipelagoMapper:
    """Get or create the global mapper instance."""
    global _mapper_instance
    if _mapper_instance is None:
        _mapper_instance = ArchipelagoMapper()
    return _mapper_instance


def export_to_yaml(settings_dict: Dict, player_name: str = "Player", include_triggers: bool = True, game_version: str = "0.6.6") -> str:
    """
    Export standalone settings to Archipelago YAML format.

    Args:
        settings_dict: Dictionary of standalone randomizer settings
        player_name: Player name for the YAML
        include_triggers: Whether to generate and include triggers
        game_version: Required Archipelago version

    Returns:
        Complete YAML string
    """
    mapper = get_mapper()
    yaml_str = mapper.settings_to_yaml(settings_dict, player_name, game_version)

    if include_triggers:
        triggers = mapper.generate_triggers(settings_dict)
        if triggers:
            # Parse the YAML, add triggers, and re-dump
            yaml_dict = yaml.safe_load(yaml_str.split("\n\n", 1)[1])  # Skip header comments
            yaml_dict["triggers"] = triggers

            # Regenerate YAML with triggers
            yaml_str_with_triggers = yaml.dump(yaml_dict, default_flow_style=False, sort_keys=False, allow_unicode=True, width=120)

            # Add header back
            header = "# Donkey Kong 64 Randomizer Settings\n" "# Generated from standalone randomizer web interface\n" "# https://dk64randomizer.com\n\n"
            yaml_str = header + yaml_str_with_triggers

    return yaml_str
