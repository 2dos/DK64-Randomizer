"""Dynamic mapper between standalone randomizer settings and Archipelago YAML options."""

import logging
import re
import os
from enum import Enum
from typing import Any, Dict, Iterable, List, Optional, Type

import yaml


class ArchipelagoMapper:
    """Maps standalone randomizer settings to Archipelago YAML format."""

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

    def __init__(self) -> None:
        self.options_metadata: Dict[str, Dict] = {}
        self.ap_to_settings_map: Dict[str, str] = {}
        self.settings_to_ap_map: Dict[str, str] = {}
        self._discover_options()
        self._build_name_mappings()

    def _discover_options(self) -> None:
        options_path = os.path.join(os.path.dirname(__file__), "..", "archipelago", "Options.py")
        try:
            with open(options_path, "r") as f:
                content = f.read()
        except Exception as e:
            logging.error(f"Could not read Options.py: {e}")
            logging.warning("Could not parse Options.py - YAML export will be limited")
            return

        dataclass_pattern = r'@dataclass\s+class\s+DK64Options\([^)]+\):\s*"""[^"]*"""\s*(.*?)(?=\n\nclass|\n\ndef|\Z)'
        match = re.search(dataclass_pattern, content, re.DOTALL)
        if not match:
            logging.error("Could not find DK64Options dataclass in Options.py")
            return

        fields_text = match.group(1)
        fields_found = re.findall(r"^\s*([a-z_0-9]+):\s*([A-Z][A-Za-z0-9]+)", fields_text, re.MULTILINE)
        logging.info(f"Discovered {len(fields_found)} DK64 options from Options.py")

        for field_name, class_name in fields_found:
            self.options_metadata[field_name] = self._parse_option_class(content, class_name, field_name)

    def _parse_option_class(self, content: str, class_name: str, field_name: str) -> Dict:
        option_info = {
            "field_name": field_name,
            "class_name": class_name,
            "display_name": field_name.replace("_", " ").title(),
            "default": None,
            "type": "unknown",
            "metadata": {},
        }

        class_pattern = rf'class\s+{class_name}\(([^)]+)\):\s*"""([^"]*?)"""(.*?)(?=\nclass\s|\Z)'
        match = re.search(class_pattern, content, re.DOTALL)
        if not match:
            return option_info

        parent_class = match.group(1).strip()
        class_body = match.group(3)

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
            option_info["default"] = int(default.group(1)) if default else (1 if "DefaultOnToggle" in parent_class else 0)

        elif "Choice" in parent_class or "TextChoice" in parent_class:
            option_info["type"] = "choice"
            choices = {m.group(1): int(m.group(2)) for m in re.finditer(r"option_([a-z_0-9]+)\s*=\s*(\d+)", class_body)}
            option_info["metadata"]["choices"] = choices
            default = re.search(r"default\s*=\s*(\d+)", class_body)
            if default:
                option_info["default"] = int(default.group(1))

        elif "OptionList" in parent_class or "ItemSet" in parent_class or "OptionSet" in parent_class:
            option_info["type"] = "list"
            list_default_match = re.search(r"default\s*=\s*(\[.*?\])", class_body, re.DOTALL)
            if list_default_match:
                try:
                    option_info["default"] = eval(list_default_match.group(1))
                except Exception:
                    pass

        elif "OptionDict" in parent_class or "ItemDict" in parent_class:
            option_info["type"] = "dict"

        display_match = re.search(r'display_name\s*=\s*["\']([^"\']+)["\']', class_body)
        if display_match:
            option_info["display_name"] = display_match.group(1)

        return option_info

    def _build_name_mappings(self) -> None:
        fillsettings_path = os.path.join(os.path.dirname(__file__), "..", "archipelago", "FillSettings.py")
        auto_mappings = {}
        try:
            with open(fillsettings_path, "r") as f:
                content = f.read()
            for m in re.finditer(r'settings_dict\["([^"]+)"\]\s*=\s*options\.([a-z_]+)(?:\.value)?', content):
                auto_mappings[m.group(2)] = m.group(1)
            logging.info(f"Extracted {len(auto_mappings)} mappings from FillSettings.py")
        except Exception as e:
            logging.warning(f"Could not parse FillSettings.py for mappings: {e}")

        manual_overrides = {
            "death_link": "death_link",
            "ring_link": "ring_link",
            "tag_link": "tag_link",
            "trap_link": "trap_link",
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
            "crown_filler_weight": "crown_filler_weight",
            "fairy_filler_weight": "fairy_filler_weight",
            "junk_filler_weight": "junk_filler_weight",
            "medal_filler_weight": "medal_filler_weight",
            "pearl_filler_weight": "pearl_filler_weight",
            "rainbowcoin_filler_weight": "rainbowcoin_filler_weight",
            "hint_style": "hint_style",
            "microhints": "microhints",
            "receive_notifications": "receive_notifications",
            "shopkeeper_hints": "shopkeeper_hints",
            "trap_fill_percentage": "trap_fill_percentage",
            "allowed_bosses": "bosses_selected",
            "harder_bosses": "hard_bosses_selected",
            "shuffled_bonus_barrels": "minigames_list_selected",
            "pregiven_keys": "krool_key_count",
            "require_beating_krool": "win_condition_spawns_ship",
            "goal": "win_condition_item",
            "goal_quantity": "win_condition_count",
            "select_starting_kong": "starting_kong",
            "maximum_snide": "most_snide_rewards",
            "enable_chaos_blockers": "blocker_selection_behavior",
            "enable_cutscenes": "more_cutscene_skips",
            "enable_shared_shops": "smaller_shops",
            "galleon_water_level": "galleon_water",
            "hard_minigames": "disable_hard_minigames",
            "krool_in_boss_pool": "krool_in_boss_pool_v2",
            "dk_portal_location_rando": "dk_portal_location_rando_v2",
            "random_starting_region": "random_starting_region_new",
            "randomize_blocker_required_amounts": "blocker_selection_behavior",
            "shop_prices": "random_prices",
            "loading_zone_rando": "level_randomization",
            "cannon_shuffle": "cannon_shuffle",
            "climbing_shuffle": "climbing_shuffle",
            "level_blockers": "blocker_text",
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
            "hints_in_item_pool": "item_rando_list_1",
            "boulders_in_pool": "item_rando_list_1",
            "dropsanity": "item_rando_list_1",
            "half_medals_in_pool": "item_rando_list_1",
            "shopowners_in_pool": "shuffle_shops",
            "snide_turnins_to_pool": "item_rando_list_1",
            "time_of_day": "item_rando_list_1",
            "kong_models": "kong_model_dk",
            "krusha_model_mode": "kong_model_dk",
            "switchsanity": "switchsanity_enabled",
            "alter_switch_allocation": "alter_switch_allocation",
            "maximize_level8_blocker": "maximize_helm_blocker",
        }

        combined_mappings = {**auto_mappings, **manual_overrides}
        for ap_name in self.options_metadata.keys():
            settings_name = combined_mappings.get(ap_name, ap_name)
            self.ap_to_settings_map[ap_name] = settings_name
            self.settings_to_ap_map[settings_name] = ap_name

    def _list_to_names(self, items: Iterable[Any], enum_class: Type[Enum], name_map: Optional[Dict[Any, str]]) -> List[str]:
        result = []
        for item in items:
            if isinstance(item, int):
                try:
                    enum_obj = enum_class(item)
                    name = name_map.get(enum_obj) if name_map else enum_obj.name
                    if name:
                        result.append(name)
                except ValueError:
                    pass
            elif hasattr(item, "value"):
                name = name_map.get(item) if name_map else item.name
                if name:
                    result.append(name)
            else:
                result.append(str(item))
        return result

    def _convert_value_to_ap(self, ap_field: str, value: Any, settings_dict: Dict) -> Any:
        if ap_field not in self.options_metadata:
            return list(value) if isinstance(value, (list, set, tuple)) else value

        option_info = self.options_metadata[ap_field]
        option_type = option_info["type"]

        if isinstance(value, (list, set, tuple)) and option_type != "list":
            option_type = "list"

        if option_type == "toggle":
            if isinstance(value, bool):
                return value
            elif isinstance(value, str):
                return value.lower() in ("true", "1", "yes", "on")
            return bool(value)

        elif option_type == "range":
            try:
                int_value = int(value)
                return max(option_info["metadata"]["min"], min(option_info["metadata"]["max"], int_value))
            except (ValueError, TypeError):
                return option_info["default"]

        elif option_type == "choice":
            choices = option_info["metadata"]["choices"]

            if ap_field == "logic_type":
                return {"nologic": "minimal", "glitch": "glitched", "glitchless": "glitchless", 0: "minimal", 1: "glitchless", 2: "glitched"}.get(value, "glitchless")

            elif ap_field == "goal":
                if isinstance(value, int):
                    try:
                        from randomizer.Enums.Settings import WinConditionComplex

                        value = WinConditionComplex(value).name
                    except (ImportError, ValueError):
                        pass
                elif hasattr(value, "name"):
                    value = value.name
                return {
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
                    "easy_random": "golden_bananas",
                    "medium_random": "golden_bananas",
                    "hard_random": "golden_bananas",
                }.get(str(value), str(value))

            elif ap_field in ("climbing_shuffle", "cannon_shuffle"):
                if hasattr(value, "name"):
                    return value.name == "shuffled"
                return value in ("shuffled", 1, True)

            elif ap_field == "loading_zone_rando":
                if hasattr(value, "name"):
                    return value.name != "none"
                return value not in ("none", 0, False)

            if hasattr(value, "name"):
                return value.name
            elif isinstance(value, str):
                return value
            elif isinstance(value, int):
                for choice_name, choice_val in choices.items():
                    if choice_val == value:
                        return choice_name
            return value

        elif option_type == "list":
            if not isinstance(value, (list, set, tuple)):
                return [value] if value else []
            try:
                if ap_field == "enemies_selected":
                    from randomizer.Enums.Enemies import Enemies

                    name_map = {
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
                    return self._list_to_names(value, Enemies, name_map)

                elif ap_field == "remove_barriers_selected":
                    from randomizer.Enums.Settings import RemovedBarriersSelected

                    name_map = {
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
                    return self._list_to_names(value, RemovedBarriersSelected, name_map)

                elif ap_field == "tricks_selected":
                    from randomizer.Enums.Settings import TricksSelected

                    name_map = {
                        TricksSelected.monkey_maneuvers: "monkey_maneuvers",
                        TricksSelected.hard_shooting: "hard_shooting",
                        TricksSelected.advanced_grenading: "advanced_grenading",
                        TricksSelected.slope_resets: "slope_resets",
                    }
                    return self._list_to_names(value, TricksSelected, name_map)

                elif ap_field == "glitches_selected":
                    from randomizer.Enums.Settings import GlitchesSelected

                    name_map = {
                        GlitchesSelected.moonkicks: "moonkicks",
                        GlitchesSelected.phase_swimming: "phase_swimming",
                        GlitchesSelected.swim_through_shores: "swim_through_shores",
                        GlitchesSelected.troff_n_scoff_skips: "troff_n_scoff_skips",
                        GlitchesSelected.moontail: "moontail",
                    }
                    return self._list_to_names(value, GlitchesSelected, name_map)

                elif ap_field == "hard_mode_selected":
                    from randomizer.Enums.Settings import HardModeSelected

                    name_map = {
                        HardModeSelected.hard_enemies: "hard_enemies",
                        HardModeSelected.shuffled_jetpac_enemies: "shuffled_jetpac_enemies",
                        HardModeSelected.strict_helm_timer: "strict_helm_timer",
                        HardModeSelected.donk_in_the_dark_world: "donk_in_the_dark_world",
                        HardModeSelected.donk_in_the_sky: "donk_in_the_sky",
                        HardModeSelected.angry_caves: "angry_caves",
                        HardModeSelected.fast_balloons: "fast_balloons",
                        HardModeSelected.lower_max_refill_amounts: "lower_max_refill_amounts",
                    }
                    return self._list_to_names(value, HardModeSelected, name_map)

                elif ap_field == "harder_bosses":
                    from randomizer.Enums.Settings import HardBossesSelected

                    name_map = {
                        HardBossesSelected.fast_mad_jack: "fast_mad_jack",
                        HardBossesSelected.alternative_mad_jack_kongs: "alternative_mad_jack_kongs",
                        HardBossesSelected.pufftoss_star_rando: "pufftoss_star_rando",
                        HardBossesSelected.pufftoss_star_raised: "pufftoss_star_raised",
                        HardBossesSelected.kut_out_phase_rando: "kut_out_phase_rando",
                        HardBossesSelected.k_rool_toes_rando: "k_rool_toes_rando",
                        HardBossesSelected.beta_lanky_phase: "beta_lanky_phase",
                    }
                    return self._list_to_names(value, HardBossesSelected, name_map)

                elif ap_field == "shuffled_bonus_barrels":
                    from randomizer.Enums.Settings import MinigamesListSelected

                    return self._list_to_names(value, MinigamesListSelected, None)

                elif ap_field == "allowed_bosses":
                    from randomizer.Enums.Maps import Maps

                    name_map = {
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
                    return self._list_to_names(value, Maps, name_map)

            except ImportError:
                return [str(x) for x in value]
            return list(value)

        elif option_type == "dict":
            if not isinstance(value, dict):
                value = {}
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
                "helm_door_item_count": {"golden_bananas": 1, "blueprints": 1, "company_coins": 1, "keys": 1, "medals": 1, "crowns": 1, "fairies": 1, "rainbow_coins": 1, "bean": 1, "pearls": 1},
                "level_blockers": {"level_1": 0, "level_2": 0, "level_3": 0, "level_4": 0, "level_5": 0, "level_6": 0, "level_7": 0, "level_8": 64},
                "alter_switch_allocation": {"level_1": "green", "level_2": "green", "level_3": "green", "level_4": "green", "level_5": "blue", "level_6": "blue", "level_7": "red", "level_8": "red"},
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
            defaults = dict_defaults.get(ap_field)
            if defaults:
                return {key: value.get(key, defaults[key]) for key in defaults}
            return value

        return value

    def _get_special_value(self, ap_field: str, settings_dict: Dict) -> Any:
        item_rando_list_1 = settings_dict.get("item_rando_list_1", [])
        item_list_checks = {
            "hints_in_item_pool": "hint",
            "boulders_in_pool": "dummyitem_boulderitem",
            "dropsanity": "dummyitem_enemies",
            "half_medals_in_pool": "dummyitem_halfmedal",
            "snide_turnins_to_pool": "blueprintbanana",
            "time_of_day": "fungitime",
        }
        if ap_field in item_list_checks:
            check_value = item_list_checks[ap_field]
            for item in item_rando_list_1:
                if hasattr(item, "name") and item.name == check_value:
                    return True
                elif isinstance(item, str) and item == check_value:
                    return True
                elif isinstance(item, int):
                    try:
                        from randomizer.Enums.Settings import ItemRandoListSelected

                        if ItemRandoListSelected(item).name == check_value:
                            return True
                    except Exception as e:
                        logging.warning(f"Error converting item {item} to ItemRandoListSelected: {e}")
            logging.info(f"{ap_field}: Looking for '{check_value}' in item_rando_list_1={item_rando_list_1}, not found")
            return False

        if ap_field == "enable_chaos_blockers":
            blocker_behavior = settings_dict.get("blocker_selection_behavior")
            if blocker_behavior is not None:
                try:
                    from randomizer.Enums.Settings import BLockerSetting

                    return blocker_behavior == BLockerSetting.chaos if hasattr(blocker_behavior, "value") else blocker_behavior == BLockerSetting.chaos.value
                except ImportError:
                    pass
            return False

        if ap_field == "enable_cutscenes":
            cutscene_skips = settings_dict.get("more_cutscene_skips")
            if cutscene_skips is not None:
                try:
                    from randomizer.Enums.Settings import ExtraCutsceneSkips

                    return cutscene_skips != ExtraCutsceneSkips.auto if hasattr(cutscene_skips, "value") else cutscene_skips != ExtraCutsceneSkips.auto.value
                except ImportError:
                    pass
            return None

        if ap_field == "enable_shared_shops":
            smaller_shops = settings_dict.get("smaller_shops")
            return bool(smaller_shops) if smaller_shops is not None else None

        if ap_field == "galleon_water_level":
            water_level = settings_dict.get("galleon_water")
            if water_level is not None:
                try:
                    from randomizer.Enums.Settings import GalleonWaterSetting

                    name = water_level.name if hasattr(water_level, "name") else GalleonWaterSetting(water_level).name
                    return name if name in ("raised", "lowered") else "raised"
                except (ImportError, ValueError):
                    pass
            return None

        if ap_field == "hard_minigames":
            disable_hard = settings_dict.get("disable_hard_minigames")
            return not bool(disable_hard) if disable_hard is not None else None

        if ap_field == "krool_in_boss_pool":
            krool_v2 = settings_dict.get("krool_in_boss_pool_v2")
            return bool(krool_v2) if krool_v2 is not None else None

        if ap_field == "dk_portal_location_rando":
            portal_v2 = settings_dict.get("dk_portal_location_rando_v2")
            if portal_v2 is not None:
                try:
                    from randomizer.Enums.Settings import DKPortalLocations

                    return (portal_v2.name if hasattr(portal_v2, "name") else DKPortalLocations(portal_v2).name).lower()
                except ImportError:
                    pass
            return None

        if ap_field == "random_starting_region":
            random_start = settings_dict.get("random_starting_region_new")
            if random_start is not None:
                try:
                    from randomizer.Enums.Settings import RandomStartingRegion

                    return (random_start.name if hasattr(random_start, "name") else RandomStartingRegion(random_start).name).lower()
                except ImportError:
                    pass
            return None

        if ap_field == "randomize_blocker_required_amounts":
            blocker_behavior = settings_dict.get("blocker_selection_behavior")
            if blocker_behavior is not None:
                try:
                    from randomizer.Enums.Settings import BLockerSetting

                    random_settings = [BLockerSetting.normal_random, BLockerSetting.easy_random, BLockerSetting.hard_random, BLockerSetting.chaos]
                    return blocker_behavior in random_settings if hasattr(blocker_behavior, "value") else blocker_behavior in [s.value for s in random_settings]
                except ImportError:
                    pass
            return False

        if ap_field == "loading_zone_rando":
            level_rand = settings_dict.get("level_randomization")
            if level_rand is not None:
                try:
                    from randomizer.Enums.Settings import LevelRandomization

                    return (level_rand.name if hasattr(level_rand, "name") else LevelRandomization(level_rand).name) == "loadingzone"
                except ImportError:
                    pass
            return False

        if ap_field in ("cannon_shuffle", "climbing_shuffle"):
            item_name = "Cannons" if ap_field == "cannon_shuffle" else "Climbing"
            try:
                from randomizer.Lists.Item import ItemList
                from randomizer.Enums.Items import Items as ItemsEnum

                for pool_num in range(1, 6):
                    for item_id in settings_dict.get(f"starting_moves_list_{pool_num}", []):
                        if isinstance(item_id, int):
                            try:
                                item_id = ItemsEnum(item_id)
                            except ValueError:
                                continue
                        item_obj = ItemList.get(item_id)
                        if item_obj is not None and item_obj.name == item_name:
                            return True
            except ImportError:
                pass
            return False

        if ap_field == "krusha_model_mode":
            try:
                krusha_kongs = []
                for kong in ["dk", "diddy", "lanky", "tiny", "chunky"]:
                    model = settings_dict.get(f"kong_model_{kong}")
                    if model is not None:
                        model_val = model.value if hasattr(model, "value") else model
                        if isinstance(model_val, int) and model_val == 2:
                            krusha_kongs.append(kong)
                return "none" if not krusha_kongs else "manual"
            except Exception:
                pass
            return None

        if ap_field == "shop_prices":
            tooie_shops = settings_dict.get("shops_dont_cost")
            if not tooie_shops:
                return "free"
            random_prices = settings_dict.get("random_prices")
            if random_prices is None:
                return "free"
            price_val = random_prices.value if hasattr(random_prices, "value") else int(random_prices)
            # RandomPrices: vanilla=0, free=1, low=2, medium=3, high=4, extreme=5
            # ShopPrices AP: free=0, low=1, medium=2, high=3
            return {0: "free", 1: "free", 2: "low", 3: "medium", 4: "high", 5: "high"}.get(price_val, "free")

        if ap_field == "maximize_level8_blocker":
            maximize = settings_dict.get("maximize_helm_blocker")
            return bool(maximize) if maximize is not None else None

        if ap_field == "kong_models":
            try:
                model_value_to_name = {0: "default", 1: "disco_chunky", 2: "krusha", 3: "krool_fight", 4: "krool_cutscene", 5: "cranky", 6: "candy", 7: "funky", 8: "disco_donkey", 9: "robokrem"}
                result = {}
                for kong in ["dk", "diddy", "lanky", "tiny", "chunky"]:
                    model = settings_dict.get(f"kong_model_{kong}")
                    model_val = (model.value if hasattr(model, "value") else model) if model is not None else 0
                    result[kong] = model_value_to_name.get(model_val, "default")
                return result
            except Exception:
                pass
            return None

        if ap_field == "goal_quantity":
            win_condition_count = settings_dict.get("win_condition_count")
            win_condition_item = settings_dict.get("win_condition_item")
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
            if win_condition_count is not None and win_condition_item is not None:
                try:
                    item_value = win_condition_item.value if hasattr(win_condition_item, "value") else int(win_condition_item)
                    goal_key = {
                        3: "golden_bananas",
                        4: "blueprints",
                        5: "company_coins",
                        6: "keys",
                        7: "medals",
                        8: "crowns",
                        9: "fairies",
                        10: "rainbow_coins",
                        12: "pearls",
                        17: "bosses",
                        18: "bonuses",
                    }.get(item_value)
                    if goal_key:
                        goal_quantity_dict[goal_key] = int(win_condition_count) if win_condition_count else goal_quantity_dict[goal_key]
                except (ValueError, TypeError):
                    pass
            return goal_quantity_dict

        if ap_field == "level_blockers":
            defaults = [0, 0, 0, 0, 0, 0, 0, 64]
            return {f"level_{i + 1}": int(settings_dict.get(f"blocker_{i}", defaults[i])) for i in range(8)}

        if ap_field == "switchsanity":
            kong_value_names = {0: "donkey", 1: "diddy", 2: "lanky", 3: "tiny", 4: "chunky", 5: "random", 6: "any"}
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
                raw = settings_dict.get(f"switchsanity_switch_{short_key}")
                if raw is None:
                    result[short_key] = "off"
                    continue
                int_val = raw.value if hasattr(raw, "value") else (int(raw) if isinstance(raw, int) else None)
                if int_val is None:
                    result[short_key] = "off"
                    continue
                result[short_key] = gone_value_names.get(int_val, "off") if short_key in gone_switches else kong_value_names.get(int_val, "off")
            return result

        if ap_field == "alter_switch_allocation":
            slam_name_map = {0: "none", 1: "green", 2: "blue", 3: "red"}
            result = {}
            for i in range(1, 9):
                raw = settings_dict.get(f"prog_slam_level_{i}")
                if raw is None:
                    result[f"level_{i}"] = "green" if i <= 4 else ("blue" if i <= 6 else "red")
                else:
                    int_val = raw.value if hasattr(raw, "value") else (int(raw) if isinstance(raw, int) else None)
                    result[f"level_{i}"] = slam_name_map.get(int_val, "green")
            return result

        if ap_field == "helm_door_item_count":
            door_item_key_map = {3: "golden_bananas", 4: "blueprints", 5: "company_coins", 6: "keys", 7: "medals", 8: "crowns", 9: "fairies", 10: "rainbow_coins", 11: "bean", 12: "pearls"}
            result = {"golden_bananas": 1, "blueprints": 1, "company_coins": 1, "keys": 1, "medals": 1, "crowns": 1, "fairies": 1, "rainbow_coins": 1, "bean": 1, "pearls": 1}
            for door_key, count_key in [("crown_door_item", "crown_door_item_count"), ("coin_door_item", "coin_door_item_count")]:
                door_item = settings_dict.get(door_key)
                if door_item is not None:
                    int_val = door_item.value if hasattr(door_item, "value") else (int(door_item) if isinstance(door_item, int) else None)
                    item_key = door_item_key_map.get(int_val)
                    if item_key:
                        result[item_key] = settings_dict.get(count_key, 1)
            return result

        _PROGRESSIVE_NAME_NORMALIZE = {
            "Progressive Slam ": "Progressive Slam",
            "Progressive Slam  ": "Progressive Slam",
            "Progressive Ammo Belt ": "Progressive Ammo Belt",
            "Progressive Instrument Upgrade ": "Progressive Instrument Upgrade",
            "Progressive Instrument Upgrade  ": "Progressive Instrument Upgrade",
        }
        for _pool_num in range(1, 6):
            if ap_field == f"starting_move_pool_{_pool_num}":
                pool_items = settings_dict.get(f"starting_moves_list_{_pool_num}")
                if pool_items is None:
                    return None
                if not pool_items:
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
                            item_names.append(_PROGRESSIVE_NAME_NORMALIZE.get(item_obj.name, item_obj.name))
                    return item_names if item_names else []
                except ImportError:
                    logging.warning(f"Could not import ItemList for starting_move_pool_{_pool_num} conversion")
                    return [str(x) for x in pool_items]

        return None

    def settings_to_yaml(self, settings_dict: Dict, player_name: str = "Player", game_version: str = "0.6.6") -> str:
        """Convert standalone settings dictionary to Archipelago YAML format."""
        if not self.options_metadata:
            return "# Error: Could not parse Archipelago options from Options.py"

        yaml_data = {"name": player_name, "game": "Donkey Kong 64", "requires": {"version": game_version}, "Donkey Kong 64": {}}
        default_options = {}

        for ap_field, settings_field in self.ap_to_settings_map.items():
            if settings_field in self.SKIP_SETTINGS:
                continue

            special_value = self._get_special_value(ap_field, settings_dict)
            value = special_value if special_value is not None else settings_dict.get(settings_field)

            using_default = False
            if value is None:
                if ap_field in self.options_metadata:
                    default_value = self.options_metadata[ap_field].get("default")
                    if default_value is not None:
                        value = default_value
                        using_default = True
                    else:
                        continue
                else:
                    continue

            converted_value = self._convert_value_to_ap(ap_field, value, settings_dict)

            if ap_field == "death_link":
                if converted_value:
                    yaml_data["Donkey Kong 64"][ap_field] = converted_value
                continue

            if converted_value is not None:
                formatted_value = ("true" if converted_value else "false") if isinstance(converted_value, bool) else converted_value
                if using_default:
                    default_options[ap_field] = formatted_value
                else:
                    yaml_data["Donkey Kong 64"][ap_field] = formatted_value

        yaml_str = yaml.dump(yaml_data, default_flow_style=False, sort_keys=False, allow_unicode=True, width=120)

        if default_options:
            yaml_str = yaml_str.rstrip("\n") + "\n"
            yaml_str += "  # Default settings (not found in form data):\n"
            for ap_field, value in sorted(default_options.items()):
                if isinstance(value, list):
                    yaml_str += f"  {ap_field}:\n"
                    for item in value:
                        yaml_str += f"  - {item}\n"
                else:
                    yaml_str += f"  {ap_field}: {value}\n"

        return "# Donkey Kong 64 Randomizer\n# Generated from https://dk64randomizer.com \n\n" + yaml_str


_mapper_instance = None


def get_mapper() -> ArchipelagoMapper:
    """Get or create the global mapper instance."""
    global _mapper_instance
    if _mapper_instance is None:
        _mapper_instance = ArchipelagoMapper()
    return _mapper_instance


def export_to_yaml(settings_dict: Dict, player_name: str = "Player", game_version: str = "0.6.6") -> str:
    """Export standalone settings to Archipelago YAML format."""
    return get_mapper().settings_to_yaml(settings_dict, player_name, game_version)
