"""Turn the website's settings into an Archipelago player YAML for DK64.

How a setting gets into the YAML
--------------------------------
Every AP option has one line in the SETTINGS dict that says where its value
comes from on the website:

    "helm_key_lock": "key_8_helm",                                # copy a website setting
    "hard_minigames": opposite("disable_hard_minigames"),         # flip a checkbox
    "tricks_selected": names("tricks_selected", TricksSelected),  # list of enum names
    "goal": goal,                                                 # anything else: a function
    "hint_style": AP_ONLY,                                        # the website has no such setting

Adding a setting
----------------
1. Add the option to archipelago/Options.py as usual.
2. Add one line for it to SETTINGS, in the section for its option group.
"""

from __future__ import annotations

import ast
import logging
import os
from dataclasses import dataclass, field
from enum import Enum
from functools import lru_cache
from typing import Any, Callable, Dict, List, Optional, Type, Union

import yaml

from randomizer.Enums.Items import Items
from randomizer.Enums.Maps import Maps
from randomizer.Enums.Settings import (
    BLockerSetting,
    CustomMinigamesSelected,
    DKPortalRando,
    Enemies,
    ExtraCutsceneSkips,
    FreeTradeSetting,
    GalleonWaterSetting,
    GlitchesSelected,
    HardBossesSelected,
    HardModeSelected,
    HelmDoorItem,
    ItemRandoFiller,
    ItemRandoListSelected,
    KongModels,
    LevelRandomization,
    LogicType,
    MinigamesListSelected,
    RandomPrices,
    RandomStartingRegion,
    RemovedBarriersSelected,
    SlamRequirement,
    SwitchsanityGone,
    SwitchsanityKong,
    TricksSelected,
    TroffSetting,
    WinConditionComplex,
)
from randomizer.Lists.Item import ItemList

Rule = Union[str, Callable[["WebsiteSettings"], Any]]

#: For AP options the website doesn't have. The yaml always uses their AP default.
AP_ONLY = None


def opposite(key: str) -> Rule:
    """Flip a website checkbox, for example "disable hard minigames" -> hard_minigames."""

    def rule(website: WebsiteSettings) -> Optional[bool]:
        return None if website.get(key) is None else not website.flag(key)

    return rule


def names(key: str, enum: Type[Enum], rename: Optional[Dict[str, str]] = None) -> Rule:
    """List the enum names picked in a website multi-select, renaming any that AP spells differently."""
    rename = rename or {}

    def rule(website: WebsiteSettings) -> List[str]:
        return [rename.get(name, name) for name in website.names(key, enum)]

    return rule


def in_item_pool(item: str) -> Rule:
    """Check whether the website's shuffled item pool has this ItemRandoListSelected entry."""
    return lambda website: item in website.shuffled_items()


def trap_weight(key: str) -> Rule:
    """Turn a website trap weight (0, 1, 2, 3 or more) into none, low, medium or high.

    Every trap weight is "none" when ice traps aren't in the website's filler items.
    """

    def rule(website: WebsiteSettings) -> Optional[str]:
        if "icetraps" not in website.names("filler_items_selected", ItemRandoFiller):
            return "none"
        weight = website.number(key)
        if weight is None:
            return None
        if weight <= 0:
            return "none"
        return {1: "low", 2: "medium"}.get(weight, "high")

    return rule


def starting_moves(pool: int) -> Rule:
    """Turn a website starting move pool (a list of item numbers) into a list of item names."""

    def rule(website: WebsiteSettings) -> Optional[List[str]]:
        items = website.get(f"starting_moves_list_{pool}")
        if items is None:
            return None
        moves = []
        for item in items or []:
            if isinstance(item, int):
                try:
                    item = Items(item)
                except ValueError:
                    continue
            if item in ItemList:
                moves.append(ItemList[item].name.strip())  # some progressive item names end in spaces
        return moves

    return rule


# Victory Conditions

GOAL_NAMES = {
    "beat_krool": "treasure_hurry",
    "get_key8": "acquire_key_8",
    "get_keys_3_and_8": "acquire_keys_3_and_8",
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
}

GOAL_QUANTITY_DEFAULTS = {
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

HELM_DOOR_ITEMS = {
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
}


def goal(website: WebsiteSettings) -> Optional[str]:
    """Return Treasure Hurry when Helm Hurry is on, otherwise the website's win condition."""
    if website.flag("helm_hurry"):
        return "treasure_hurry"
    win_condition = website.name("win_condition_item", WinConditionComplex)
    return GOAL_NAMES.get(win_condition, win_condition)


def goal_quantity(website: WebsiteSettings) -> Dict[str, int]:
    """Return the amount every quantity goal needs. Only the picked goal's amount comes from the website."""
    quantities = dict(GOAL_QUANTITY_DEFAULTS)
    win_condition = website.name("win_condition_item", WinConditionComplex) or ""
    amount = website.number("win_condition_count")
    if win_condition.startswith("req_") and win_condition in GOAL_NAMES and amount:
        quantities[GOAL_NAMES[win_condition]] = amount
    return quantities


def helm_door_item_count(website: WebsiteSettings) -> Dict[str, int]:
    """Return how many of each item a Helm door needs. The website sets the amounts for its two doors' items."""
    counts = {item: 1 for item in HELM_DOOR_ITEMS.values()}
    for door in ("crown_door_item", "coin_door_item"):
        item = HELM_DOOR_ITEMS.get(website.name(door, HelmDoorItem))
        if item:
            counts[item] = website.number(f"{door}_count", 1)
    return counts


# B. Locker Settings


def randomize_blockers(website: WebsiteSettings) -> bool:
    """Check whether the website uses a random B. Locker mode (easy, normal, hard or chaos)."""
    return website.name("blocker_selection_behavior", BLockerSetting) in ("easy_random", "normal_random", "hard_random", "chaos")


def chaos_blockers(website: WebsiteSettings) -> bool:
    """Check whether the website's B. Locker mode is chaos."""
    return website.name("blocker_selection_behavior", BLockerSetting) == "chaos"


def level_blockers(website: WebsiteSettings) -> Dict[str, int]:
    """Return the B. Locker amounts for levels 1-8 (website settings blocker_0 to blocker_7)."""
    defaults = [0, 0, 0, 0, 0, 0, 0, 64]
    return {f"level_{level + 1}": website.number(f"blocker_{level}", defaults[level]) for level in range(8)}


# Troff n Scoff Settings


def randomize_troff(website: WebsiteSettings) -> bool:
    """Check whether the Troff 'n' Scoff amounts are random. Only a pre-selected website mode turns this off."""
    if website.get("tns_selection_behavior") is None:
        return True
    return website.name("tns_selection_behavior", TroffSetting) in ("normal_random", "hard_random")


def troff_max(website: WebsiteSettings) -> int:
    """Return the Troff 'n' Scoff maximum. The website has a text box for it; anything but a number means 150."""
    return website.number("troff_text", 150)


def level_troff(website: WebsiteSettings) -> Dict[str, int]:
    """Return the Troff 'n' Scoff amounts for levels 1-8 (website settings troff_0 to troff_7)."""
    return {f"level_{level + 1}": website.number(f"troff_{level}", 0) for level in range(8)}


# Item Pool

# item pool entry
ITEM_POOL_CATEGORIES = {
    "crown": "crowns",
    "blueprint": "blueprints",
    "medal": "medals",
    "nintendocoin": "company_coins",
    "rarewarecoin": "company_coins",
    "fairy": "fairies",
    "rainbowcoin": "rainbow_coins",
    "bean": "bean",
    "pearl": "pearls",
    "crateitem": "crates",
    "hint": "hints",
    "shopowners": "shopkeepers",
    "dummyitem_halfmedal": "half_medals",
    "blueprintbanana": "snide_turnins",
    "fungitime": "time_of_day",
    "dummyitem_boulderitem": "boulders",
    "dummyitem_balloon": "balloons",
    "dummyitem_breakable": "breakables",
    "dummyitem_enemies": "dropsanity",
}


def item_pool(website: WebsiteSettings) -> List[str]:
    """Return the AP item pool categories found in the website's shuffled pools.

    Moves, Golden Bananas, shops, Kongs and keys are always in the AP pool, so they have no category.
    """
    return sorted({ITEM_POOL_CATEGORIES[item] for item in website.shuffled_items() if item in ITEM_POOL_CATEGORIES})


# Shops

#: Website price setting -> AP shop_prices.
SHOP_PRICES = {"vanilla": "free", "free": "free", "low": "low", "medium": "medium", "high": "high", "extreme": "high"}


def shop_prices(website: WebsiteSettings) -> str:
    """Return free unless Tooie-style shops (shops_dont_cost) are on; then follow the website's prices."""
    if not website.flag("shops_dont_cost"):
        return "free"
    return SHOP_PRICES.get(website.name("random_prices", RandomPrices), "free")


#: Every switch, in the order the YAML lists them.
SWITCHES = [
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


def switchsanity(website: WebsiteSettings) -> Dict[str, str]:
    """Return each switch's Kong, or for the Helm lobby switch its pad. Missing switches are off."""
    result = {}
    for switch in SWITCHES:
        options = SwitchsanityGone if switch == "isles_helm_lobby" else SwitchsanityKong
        result[switch] = website.name(f"switchsanity_switch_{switch}", options) or "off"
    return result


def loading_zone_rando(website: WebsiteSettings) -> str:
    """Return yes when the website shuffles loading zones (coupled), otherwise no."""
    return "yes" if website.name("level_randomization", LevelRandomization) == "loadingzone" else "no"


def galleon_water_level(website: WebsiteSettings) -> str:
    """Return raised or lowered. The website's random water level becomes raised."""
    water = website.name("galleon_water", GalleonWaterSetting)
    return water if water in ("raised", "lowered") else "raised"


def random_starting_region(website: WebsiteSettings) -> str:
    """Return the website's random starting region, or off if AP doesn't have it."""
    region = website.name("random_starting_region_new", RandomStartingRegion)
    return region if region in ap_choices("random_starting_region") else "off"


#: Website DK portal mode -> AP dk_portal_location_rando, where the names differ.
DK_PORTAL_MODES = {"on": "all", "on_underwater": "all_underwater"}


def dk_portal_location_rando(website: WebsiteSettings) -> str:
    """Return the DK portal rando mode, or off if AP doesn't have it."""
    mode = website.name("dk_portal_location_rando_v2", DKPortalRando)
    mode = DK_PORTAL_MODES.get(mode, mode)
    return mode if mode in ap_choices("dk_portal_location_rando") else "off"


# Logic

#: Website logic -> AP logic_type
LOGIC_TYPES = {"advanced_glitchless": "advanced_glitchless", "glitchless": "glitchless", "glitch": "glitched", "minimal": "minimal"}

#: Kong model settings
KONGS = ["dk", "diddy", "lanky", "tiny", "chunky"]

#: Website boss map -> AP allowed_bosses name.
BOSS_NAMES = {
    "JapesBoss": "Armydillo 1",
    "AztecBoss": "Dogadon 1",
    "FactoryBoss": "Mad Jack",
    "GalleonBoss": "Pufftoss",
    "FungiBoss": "Dogadon 2",
    "CavesBoss": "Armydillo 2",
    "CastleBoss": "Kutout",
    "KroolDonkeyPhase": "DK phase",
    "KroolDiddyPhase": "Diddy Phase",
    "KroolLankyPhase": "Lanky Phase",
    "KroolTinyPhase": "Tiny Phase",
    "KroolChunkyPhase": "Chunky Phase",
}

#: Website slam level -> AP alter_switch_allocation
SLAM_LEVELS = {"no_slam": "none", "green": "green", "blue": "blue", "red": "red"}

SLAM_DEFAULTS = {
    "level_1": "green",
    "level_2": "green",
    "level_3": "green",
    "level_4": "green",
    "level_5": "blue",
    "level_6": "blue",
    "level_7": "red",
    "level_8": "red",
}


def logic_type(website: WebsiteSettings) -> str:
    """Return the AP logic type. Anything AP doesn't have becomes glitchless."""
    return LOGIC_TYPES.get(website.name("logic_type", LogicType), "glitchless")


def krusha_model_mode(website: WebsiteSettings) -> str:
    """Return manual when any Kong uses the Krusha model, otherwise none."""
    uses_krusha = any(website.name(f"kong_model_{kong}", KongModels) == "krusha" for kong in KONGS)
    return "manual" if uses_krusha else "none"


def kong_models(website: WebsiteSettings) -> Dict[str, str]:
    """Return each Kong's model."""
    return {kong: website.name(f"kong_model_{kong}", KongModels) or "default" for kong in KONGS}


def allowed_bosses(website: WebsiteSettings) -> List[str]:
    """Return the bosses the website allows. None picked means all of them."""
    bosses = [BOSS_NAMES[boss] for boss in website.names("bosses_selected", Maps) if boss in BOSS_NAMES]
    return bosses or list(BOSS_NAMES.values())


def alter_switch_allocation(website: WebsiteSettings) -> Dict[str, str]:
    """Return the slam level each level's switches need."""
    result = {}
    for level, default in SLAM_DEFAULTS.items():
        key = f"prog_slam_{level}"
        result[level] = default if website.get(key) is None else SLAM_LEVELS.get(website.name(key, SlamRequirement), "green")
    return result


def free_trade_cbs(website: WebsiteSettings) -> Optional[bool]:
    """Check whether the website's Free Trade Agreement includes CBs. AP always lets any Kong collect items."""
    if website.get("free_trade_setting") is None:
        return None
    return website.name("free_trade_setting", FreeTradeSetting) == FreeTradeSetting.all_cbs.name


# Enemies

#: Website enemy name -> AP enemies_selected name
ENEMY_NAMES = {
    "Guard": "Kop",
    "GuardDisableA": "DisableAKop",
    "GuardDisableZ": "DisableZKop",
    "GuardTag": "DisableTaggingKop",
    "GuardGetOut": "GetOutKop",
    "KasplatChunky": "ChunkyKasplat",
    "KasplatDK": "DKKasplat",
    "KasplatDiddy": "DiddyKasplat",
    "KasplatLanky": "LankyKasplat",
    "KasplatTiny": "TinyKasplat",
    "KlaptrapGreen": "GreenKlaptrap",
    "KlaptrapPurple": "PurpleKlaptrap",
    "KlaptrapRed": "RedKlaptrap",
    "MrDice0": "GreenDice",
    "MrDice1": "RedDice",
}


# Quality of Life


def enable_cutscenes(website: WebsiteSettings) -> Optional[bool]:
    """Check whether cutscenes play, which is unless the website skips them automatically."""
    if website.get("more_cutscene_skips") is None:
        return None
    return website.name("more_cutscene_skips", ExtraCutsceneSkips) != "auto"


# ---------------------------------------------------------------------------
# SETTINGS: every AP option, and where its value comes from on the website.
# Sections and order follow the option groups in archipelago/Options.py.
# ALL AP SETTINGS NEEDS AN ENTRY HERE
# ---------------------------------------------------------------------------

SETTINGS: Dict[str, Optional[Rule]] = {
    # Victory Conditions
    "goal": goal,
    "require_beating_krool": "win_condition_spawns_ship",
    "goal_quantity": goal_quantity,
    "pregiven_keys": "krool_key_count",
    "helm_phase_count": "helm_phase_count",
    "crown_door_item": "crown_door_item",
    "coin_door_item": "coin_door_item",
    "helm_door_item_count": helm_door_item_count,
    "krool_phase_count": "krool_phase_count",
    "krool_in_boss_pool": "krool_in_boss_pool_v2",
    # B. Locker Settings
    "randomize_blocker_required_amounts": randomize_blockers,
    "blocker_max": "blocker_text",
    "enable_chaos_blockers": chaos_blockers,
    "maximize_level8_blocker": "maximize_helm_blocker",
    "chaos_ratio": "blocker_text",  # the website uses one box for both the maximum and the chaos ratio
    "level_blockers": level_blockers,
    # Troff n Scoff Settings
    "randomize_troff": randomize_troff,
    "troff_max": troff_max,
    "level_troff": level_troff,
    # Item Pool
    "starting_kong_count": "starting_kongs_count",
    "select_starting_kong": "starting_kong",
    "starting_move_pool_1": starting_moves(1),
    "starting_move_pool_1_count": "starting_moves_list_count_1",
    "starting_move_pool_2": starting_moves(2),
    "starting_move_pool_2_count": "starting_moves_list_count_2",
    "starting_move_pool_3": starting_moves(3),
    "starting_move_pool_3_count": "starting_moves_list_count_3",
    "starting_move_pool_4": starting_moves(4),
    "starting_move_pool_4_count": "starting_moves_list_count_4",
    "starting_move_pool_5": starting_moves(5),
    "starting_move_pool_5_count": "starting_moves_list_count_5",
    "helm_key_lock": "key_8_helm",
    "item_pool": item_pool,
    "half_medals_in_pool": in_item_pool("halfmedal"),
    "half_medal_percentage": "half_medal_percentage",
    "maximum_snide": "most_snide_rewards",
    # Shops
    "shop_prices": shop_prices,
    "smaller_shops": "smaller_shops",
    "enable_shared_shops": "smaller_shops",  # on the website, smaller shops also turns on shared shops
    # Levels/Barriers
    "shuffle_helm_level_order": "shuffle_helm_location",
    "open_lobbies": "open_lobbies",
    "switchsanity": switchsanity,
    "remove_barriers_selected": names("remove_barriers_selected", RemovedBarriersSelected),
    "loading_zone_rando": loading_zone_rando,
    "galleon_water_level": galleon_water_level,
    "random_starting_region": random_starting_region,
    "dk_portal_location_rando": dk_portal_location_rando,
    # Logic
    "logic_type": logic_type,
    "tricks_selected": names("tricks_selected", TricksSelected),
    "glitches_selected": names("glitches_selected", GlitchesSelected),
    "cbs_required_for_medal": "medal_cb_req",
    "medal_distribution": "cb_medal_behavior_new",
    "pearls_required_for_mermaid": "mermaid_gb_pearls",
    "fairies_required_for_bfi": "rareware_gb_fairies",
    "jetpac_requirement": "medal_requirement",
    "puzzle_rando": "puzzle_rando_difficulty",
    "krusha_model_mode": krusha_model_mode,
    "kong_models": kong_models,
    "allowed_bosses": allowed_bosses,
    "alter_switch_allocation": alter_switch_allocation,
    "free_trade_cbs": free_trade_cbs,
    # Bonus Barrels
    "shuffled_bonus_barrels": names("minigames_list_selected", MinigamesListSelected),
    "hard_minigames": opposite("disable_hard_minigames"),
    "auto_complete_bonus_barrels": "bonus_barrel_auto_complete",
    "helm_room_bonus_count": "helm_room_bonus_count",
    "alternate_minecart_mayhem": "alt_minecart_mayhem",
    "custom_arcade_minigames": "custom_minigames_enabled",
    "dk_arcade_minigame_pool": names("arcade_minigame_pool_selected", CustomMinigamesSelected),
    "jetpac_minigame_pool": names("jetpac_minigame_pool_selected", CustomMinigamesSelected),
    # Hard Mode
    "hard_mode_selected": names("hard_mode_selected", HardModeSelected),
    "harder_bosses": names("hard_bosses_selected", HardBossesSelected),
    "mirror_mode": "mirror_mode",
    # Enemies
    "enemies_selected": names("enemies_selected", Enemies, rename=ENEMY_NAMES),
    # Hints
    "hint_style": AP_ONLY,
    "shopkeeper_hints": AP_ONLY,
    "microhints": AP_ONLY,
    # Filler Weights
    "junk_filler_weight": AP_ONLY,
    "banana_filler_weight": AP_ONLY,
    "crown_filler_weight": AP_ONLY,
    "fairy_filler_weight": AP_ONLY,
    "medal_filler_weight": AP_ONLY,
    "pearl_filler_weight": AP_ONLY,
    "rainbowcoin_filler_weight": AP_ONLY,
    # Trap Weights
    "trap_fill_percentage": "ice_trap_count",
    "bubble_trap_weight": trap_weight("trap_weight_bubble"),
    "slow_trap_weight": trap_weight("trap_weight_slow"),
    "reverse_trap_weight": trap_weight("trap_weight_reverse"),
    "disable_a_trap_weight": trap_weight("trap_weight_disablea"),
    "disable_b_trap_weight": trap_weight("trap_weight_disableb"),
    "disable_c_trap_weight": trap_weight("trap_weight_disablecu"),
    "disable_z_trap_weight": trap_weight("trap_weight_disablez"),
    "get_out_trap_weight": trap_weight("trap_weight_getout"),
    "dry_trap_weight": trap_weight("trap_weight_dry"),
    "flip_trap_weight": trap_weight("trap_weight_flip"),
    "ice_floor_weight": trap_weight("trap_weight_icefloor"),
    "paper_weight": trap_weight("trap_weight_paper"),
    "slip_weight": trap_weight("trap_weight_slip"),
    "animal_trap_weight": trap_weight("trap_weight_animal"),
    "rockfall_trap_weight": trap_weight("trap_weight_rockfall"),
    "disabletag_trap_weight": trap_weight("trap_weight_disabletag"),
    # Links
    "tag_link": AP_ONLY,
    "ring_link": AP_ONLY,
    "trap_link": AP_ONLY,
    "damage_link": AP_ONLY,
    "knockback_link": AP_ONLY,
    "death_link": AP_ONLY,
    # Quality of Life
    "enable_cutscenes": enable_cutscenes,
    "remove_bait_potions": "no_consumable_upgrades",
    "receive_notifications": AP_ONLY,
}


class WebsiteSettings:
    """The settings dict the website sent, with helpers that accept any form a value arrives in."""

    def __init__(self, settings: Dict[str, Any]) -> None:
        """Wrap the website's settings dict."""
        self.settings = settings

    def get(self, key: str) -> Any:
        """Return the raw value, or None if the website didn't send it."""
        return self.settings.get(key)

    def flag(self, key: str) -> bool:
        """Return a checkbox as True or False. A missing checkbox is False."""
        return to_bool(self.get(key))

    def number(self, key: str, otherwise: Optional[int] = None) -> Optional[int]:
        """Return the value as a whole number, or `otherwise` if it's missing or not a number."""
        try:
            return int(self.get(key))
        except (TypeError, ValueError):
            return otherwise

    def name(self, key: str, enum: Type[Enum]) -> Optional[str]:
        """Return the enum name picked in a single-choice setting, or None."""
        return enum_name(self.get(key), enum)

    def names(self, key: str, enum: Type[Enum]) -> List[str]:
        """Return the enum names picked in a multi-select. A missing setting means none."""
        values = self.get(key)
        if values is None:
            return []
        if not isinstance(values, (list, set, tuple)):
            values = [values]
        return [name for name in (enum_name(value, enum) for value in values) if name is not None]

    def shuffled_items(self) -> List[str]:
        """Return the ItemRandoListSelected names in every shuffled item and check pool."""
        # Pools 1-4 hold items and 6-9 hold checks. Pools 0 and 5 are the "not shuffled" lists.
        return [item for pool in (1, 2, 3, 4, 6, 7, 8, 9) for item in self.names(f"item_rando_list_{pool}", ItemRandoListSelected)]


def enum_name(value: Any, enum: Type[Enum]) -> Optional[str]:
    """Return the name for an enum member or its number. Strings are taken to be names already."""
    if isinstance(value, str):
        return value
    if isinstance(value, Enum):
        return value.name
    if isinstance(value, int):
        try:
            return enum(value).name
        except ValueError:
            return None
    return None


def to_bool(value: Any) -> bool:
    """Read a checkbox value. The strings "true", "1", "yes" and "on" count as True."""
    if isinstance(value, str):
        return value.lower() in ("true", "1", "yes", "on")
    return bool(value)


OPTIONS_FILE = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "archipelago", "Options.py"))

#: Archipelago option base class
AP_CLASSES = {
    "Toggle": "toggle",
    "DeathLink": "toggle",
    "DefaultOnToggle": "default_on_toggle",
    "Choice": "choice",
    "TextChoice": "text_choice",
    "Range": "range",
    "NamedRange": "range",
    "OptionList": "list",
    "OptionSet": "list",
    "ItemSet": "list",
    "OptionDict": "dict",
    "ItemDict": "dict",
}


@dataclass
class APOption:
    """What the YAML needs to know about one AP option class."""

    kind: str = "unknown"
    default: Any = None
    choices: Dict[str, int] = field(default_factory=dict)
    range_start: Optional[int] = None
    range_end: Optional[int] = None

    def choice_name(self, number: int) -> Optional[str]:
        """Return the name of the choice with this number."""
        return next((name for name, value in self.choices.items() if value == number), None)


@lru_cache(maxsize=None)
def read_ap_options() -> Dict[str, APOption]:
    """Read the DK64Options fields from archipelago/Options.py, in order."""
    try:
        with open(OPTIONS_FILE, "r") as file:
            tree = ast.parse(file.read())
    except (OSError, SyntaxError) as error:
        logging.error("ArchipelagoMapper: could not read %s: %s", OPTIONS_FILE, error)
        return {}
    classes = {node.name: node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)}
    if "DK64Options" not in classes:
        logging.error("ArchipelagoMapper: DK64Options not found in %s", OPTIONS_FILE)
        return {}
    options = {}
    for line in classes["DK64Options"].body:
        # Each field looks like `goal: Goal`.
        if isinstance(line, ast.AnnAssign) and isinstance(line.target, ast.Name) and isinstance(line.annotation, ast.Name):
            options[line.target.id] = read_option_class(line.annotation.id, classes)
    missing = [name for name in options if name not in SETTINGS]
    unknown = [name for name in SETTINGS if name not in options]
    if missing:
        logging.warning("ArchipelagoMapper: add these AP options to SETTINGS (they get their AP default for now): %s", ", ".join(missing))
    if unknown:
        logging.warning("ArchipelagoMapper: SETTINGS has options that archipelago/Options.py doesn't: %s", ", ".join(unknown))
    return options


def read_option_class(class_name: str, classes: Dict[str, ast.ClassDef]) -> APOption:
    """Read one option class, including what it inherits from DK64's own option classes."""
    # The class itself, then its DK64 parents (e.g. BubbleTrapWeight -> BaseTrapWeight).
    lineage: List[ast.ClassDef] = []
    while class_name in classes and classes[class_name] not in lineage:
        lineage.append(classes[class_name])
        class_name = next((base.id for base in lineage[-1].bases if isinstance(base, ast.Name) and base.id in classes), "")

    option = APOption(kind=option_kind(lineage, classes))
    attributes: Dict[str, Any] = {}
    for node in reversed(lineage):  # parents first, so the class's own values win
        for line in node.body:
            if isinstance(line, ast.Assign):
                for target in line.targets:
                    if isinstance(target, ast.Name) and target.id.startswith("option_"):
                        number = literal(line.value)
                        if isinstance(number, int):
                            option.choices[target.id[len("option_") :]] = number
                if len(line.targets) == 1 and isinstance(line.targets[0], ast.Name):
                    value = literal(line.value)
                    if value is not None or isinstance(line.value, (ast.Set, ast.List, ast.Dict, ast.Tuple)):
                        attributes[line.targets[0].id] = value
            elif isinstance(line, ast.AnnAssign) and isinstance(line.target, ast.Name) and line.value is not None:
                value = literal(line.value)
                if value is not None:
                    attributes[line.target.id] = value

    option.default = attributes.get("default")
    if option.default is None and option.kind in ("toggle", "default_on_toggle"):
        option.default = option.kind == "default_on_toggle"
    if option.kind == "range":
        option.range_start = attributes.get("range_start")
        option.range_end = attributes.get("range_end")
    return option


def option_kind(lineage: List[ast.ClassDef], classes: Dict[str, ast.ClassDef]) -> str:
    """Find the Archipelago base class."""
    for node in lineage:
        for base in node.bases:
            if isinstance(base, ast.Name):
                if base.id in AP_CLASSES:
                    return AP_CLASSES[base.id]
                if base.id in classes:
                    break
        else:
            return "unknown"
    return "unknown"


def literal(node: ast.AST) -> Any:
    """Return the value of a constant in Options.py, or None if it isn't a plain constant."""
    try:
        return ast.literal_eval(node)
    except Exception:
        return None


def ap_choices(option_name: str) -> Dict[str, int]:
    """Return the choices of an AP option."""
    option = read_ap_options().get(option_name)
    return option.choices if option else {}


def export_to_yaml(settings_dict: Dict[str, Any], player_name: str = "Player", game_version: str = "0.6.7") -> str:
    """Build the Archipelago player YAML."""
    ap_options = read_ap_options()
    if not ap_options:
        return "# Error: Could not parse Archipelago options from Options.py"

    website = WebsiteSettings(settings_dict)
    chosen: Dict[str, Any] = {}
    defaults: Dict[str, Any] = {}
    for name, option in ap_options.items():
        rule = SETTINGS.get(name)
        if rule is None:
            value = None
        elif isinstance(rule, str):
            value = convert_by_type(website.get(rule), option)
        else:
            value = rule(website)

        if value is not None:
            chosen[name] = yaml_value(value)
            continue
        value = ap_default(option)
        if value is not None:  # no readable default (e.g. death_link) means leave the option out
            defaults[name] = yaml_value(value)

    data = {"name": player_name, "game": "Donkey Kong 64", "requires": {"version": game_version}, "Donkey Kong 64": chosen}
    text = yaml.dump(data, default_flow_style=False, sort_keys=False, allow_unicode=True, width=120)
    if defaults:
        text = text.rstrip("\n") + "\n  # Default settings (not found in form data):\n"
        for name, value in sorted(defaults.items()):
            if isinstance(value, list):
                text += f"  {name}:\n" + "".join(f"  - {item}\n" for item in value)
            else:
                text += f"  {name}: {value}\n"
    return "# Donkey Kong 64 Randomizer\n# Generated from https://dk64randomizer.com \n\n" + text


def convert_by_type(value: Any, option: APOption) -> Any:
    """Convert a website value to the AP option's type. None means "use the AP default"."""
    if value is None:
        return None
    if option.kind in ("toggle", "default_on_toggle"):
        return to_bool(value)
    if option.kind == "range":
        try:
            number = int(getattr(value, "value", value))
        except (TypeError, ValueError):
            return option.default
        low = number if option.range_start is None else option.range_start
        high = number if option.range_end is None else option.range_end
        return max(low, min(high, number))
    if option.kind in ("choice", "text_choice"):
        if isinstance(value, (str, Enum)):
            return value if isinstance(value, str) else value.name
        return option.choice_name(value) if isinstance(value, int) else None
    if option.kind == "list":
        values = value if isinstance(value, (list, set, tuple)) else [value]
        return [item.name if isinstance(item, Enum) else str(item) for item in values]
    if option.kind == "dict":
        return value if isinstance(value, dict) else None
    return value


def ap_default(option: APOption) -> Any:
    """Return the option's default from Options.py, shaped like a YAML value."""
    default = option.default
    if default is None:
        return None
    if option.kind in ("toggle", "default_on_toggle"):
        return to_bool(default)
    if option.kind in ("choice", "text_choice") and isinstance(default, int):
        return option.choice_name(default) or default
    if option.kind == "list" and isinstance(default, (list, set, tuple, frozenset)):
        return list(default)
    if option.kind == "dict" and isinstance(default, dict):
        return dict(default)
    return default


def yaml_value(value: Any) -> Any:
    """Write True and False as the strings "true" and "false", like the AP templates do."""
    if isinstance(value, bool):
        return "true" if value else "false"
    return value
