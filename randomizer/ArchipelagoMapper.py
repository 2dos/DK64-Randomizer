"""Convert standalone DK64R settings dicts into Archipelago YAML.

Architecture
------------
The Archipelago framework is **not importable** from this process, so we cannot
`import archipelago.Options` directly. Instead, archipelago/Options.py is parsed
as text via Python's `ast` module to discover the AP option classes and their
metadata (defaults, choices, etc).

Each AP field is then converted to its YAML value either by a registered
converter (`@converter("ap_field")`) when its settings-dict shape needs custom
logic, or by a generic fallthrough that handles the common cases (toggle ↔ bool,
choice ↔ enum-name, range ↔ int, list ↔ list-of-names).

Adding a new AP option
----------------------
1. Add the option class + dataclass field in archipelago/Options.py.
2. If the AP field name does NOT match the settings-dict key, or the value
   needs reshaping, add ONE `@converter` function below. Otherwise nothing
   else is needed — the fallthrough handles it.
"""

from __future__ import annotations

import ast
import logging
import os
from dataclasses import dataclass, field as dc_field
from typing import Any, Callable, Dict, Iterable, List, Optional

import yaml


# ---------------------------------------------------------------------------
# Static config
# ---------------------------------------------------------------------------

#: settings_dict keys that should never be exported to AP YAML
SKIP_SETTINGS = frozenset(
    {
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
)

#: Default goal_quantity dict, used both as fallback and as the base when
#: round-tripping (we only know the user's count for the *active* win condition).
GOAL_QUANTITY_DEFAULTS: Dict[str, int] = {
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

#: Default helm_door_item_count dict.
HELM_DOOR_COUNT_DEFAULTS: Dict[str, int] = {
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

#: HelmDoorItem enum value → AP item-key (matches AP HelmDoor1Item / HelmDoor2Item names).
HELM_DOOR_ITEM_KEY: Dict[int, str] = {
    3: "golden_bananas",
    4: "blueprints",
    5: "company_coins",
    6: "keys",
    7: "medals",
    8: "crowns",
    9: "fairies",
    10: "rainbow_coins",
    11: "bean",
    12: "pearls",
}

#: WinConditionComplex enum-name → AP Goal option-name.
WIN_CONDITION_TO_GOAL_NAME: Dict[str, str] = {
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
    "krools_challenge": "krools_challenge",
    "kill_the_rabbit": "kill_the_rabbit",
}

#: Inverse — AP Goal option-name → WinConditionComplex enum-name (for goal_quantity lookups).
GOAL_NAME_TO_WIN_KEY: Dict[str, str] = {
    "golden_bananas": "golden_bananas",
    "blueprints": "blueprints",
    "company_coins": "company_coins",
    "keys": "keys",
    "medals": "medals",
    "crowns": "crowns",
    "fairies": "fairies",
    "rainbow_coins": "rainbow_coins",
    "pearls": "pearls",
    "bosses": "bosses",
    "bonuses": "bonuses",
}

#: AP LogicType integer → AP option-name. (LogicType uses non-sequential ints.)
LOGIC_TYPE_INT_TO_NAME: Dict[Any, str] = {
    0: "advanced_glitchless",
    1: "glitchless",
    2: "glitched",
    4: "minimal",
    "glitchless": "glitchless",
    "glitch": "glitched",
    "nologic": "minimal",
}

#: KongModels enum integer → AP kong_models value-name.
KONG_MODEL_NAMES: Dict[int, str] = {
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
    10: "rabbit",
}

#: Standalone RandomPrices enum-int → AP shop_prices choice-name.
SHOP_PRICE_NAMES: Dict[int, str] = {
    0: "free",
    1: "free",
    2: "low",
    3: "medium",
    4: "high",
    5: "high",
}

#: SlamRequirement enum-int → AP alter_switch_allocation value-name.
SLAM_NAMES: Dict[int, str] = {0: "none", 1: "green", 2: "blue", 3: "red"}

#: Default alter_switch_allocation dict.
SLAM_DEFAULTS: Dict[str, str] = {
    "level_1": "green",
    "level_2": "green",
    "level_3": "green",
    "level_4": "green",
    "level_5": "blue",
    "level_6": "blue",
    "level_7": "red",
    "level_8": "red",
}

#: SwitchsanityKong enum-int → AP switchsanity value-name (for kong-controlled switches).
SWITCHSANITY_KONG_NAMES: Dict[int, str] = {0: "donkey", 1: "diddy", 2: "lanky", 3: "tiny", 4: "chunky", 5: "random", 6: "any"}

#: SwitchsanityGone enum-int → AP switchsanity value-name (for the gone-pad switch).
SWITCHSANITY_GONE_NAMES: Dict[int, str] = {0: "bongos", 1: "guitar", 2: "trombone", 3: "sax", 4: "triangle", 5: "lever", 6: "gong", 7: "gone_pad", 8: "random"}

#: Switches that use SwitchsanityGone (everything else uses SwitchsanityKong).
SWITCHSANITY_GONE_KEYS = frozenset({"isles_helm_lobby"})

#: Canonical switchsanity switch keys, in display order.
SWITCHSANITY_SWITCH_KEYS: List[str] = [
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

#: ItemRandoListSelected enum-name → AP item_pool option-key.
#: (Some standalone enums have no AP equivalent and are dropped — moves, banana,
#: shop, kong, key, racebanana, trainingmoves, shockwave are forced-on and not
#: exposed as toggleable item_pool keys.)
ITEM_POOL_ENUM_TO_KEY: Dict[str, str] = {
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

#: Boolean derivative AP fields → ItemRandoListSelected enum-name to look for
#: in the item pool. Each is a yes/no shortcut for "is this category in the pool?".
ITEM_POOL_PRESENCE_CHECKS: Dict[str, str] = {
    "hints_in_item_pool": "hint",
    "boulders_in_pool": "boulderitem",
    "dropsanity": "enemies",
    "half_medals_in_pool": "halfmedal",
    "snide_turnins_to_pool": "blueprintbanana",
    "time_of_day": "fungitime",
}

#: AP `enemies_selected` accepts these names; standalone Enemies enum-names need
#: to be remapped where they differ.
ENEMY_NAME_REMAP: Dict[str, str] = {
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
    "FireballGlasses": "FireballGlasses",
}

#: Maps enum-name → AP allowed_bosses display name.
BOSS_MAP_NAME_TO_AP: Dict[str, str] = {
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

#: Progressive starting-move names get a trailing-space variant in some sources;
#: normalize when we encounter one.
_PROGRESSIVE_NAME_NORMALIZE: Dict[str, str] = {
    "Progressive Slam ": "Progressive Slam",
    "Progressive Slam  ": "Progressive Slam",
    "Progressive Ammo Belt ": "Progressive Ammo Belt",
    "Progressive Instrument Upgrade ": "Progressive Instrument Upgrade",
    "Progressive Instrument Upgrade  ": "Progressive Instrument Upgrade",
}

#: AP fields whose settings-dict key differs from the AP field name AND that do
#: NOT have a custom converter (i.e. simple-value renames). All other rename
#: cases are encoded directly inside their converter.
_FALLTHROUGH_NAME_OVERRIDES: Dict[str, str] = {
    "select_starting_kong": "starting_kong",
    "maximum_snide": "most_snide_rewards",
    "starting_kong_count": "starting_kongs_count",
    "alternate_minecart_mayhem": "alt_minecart_mayhem",
    "cbs_required_for_medal": "medal_cb_req",
    "jetpac_requirement": "medal_requirement",
    "fairies_required_for_bfi": "rareware_gb_fairies",
    "helm_key_lock": "key_8_helm",
    "shuffle_helm_level_order": "shuffle_helm_location",
    "pearls_required_for_mermaid": "mermaid_gb_pearls",
    "puzzle_rando": "puzzle_rando_difficulty",
    "remove_bait_potions": "no_consumable_upgrades",
    "pregiven_keys": "krool_key_count",
    "starting_move_pool_1_count": "starting_moves_list_count_1",
    "starting_move_pool_2_count": "starting_moves_list_count_2",
    "starting_move_pool_3_count": "starting_moves_list_count_3",
    "starting_move_pool_4_count": "starting_moves_list_count_4",
    "starting_move_pool_5_count": "starting_moves_list_count_5",
    "trap_fill_percentage": "ice_trap_count",
    "auto_complete_bonus_barrels": "bonus_barrel_auto_complete"
    # Trap weights are handled by a dedicated converter (see TRAP_WEIGHT_FIELDS
    # below) — the standalone stores 0/1/2/3 but AP's BaseTrapWeight uses
    # option_high=4, so direct int passthrough would mis-map "high".
}

#: AP trap-weight field → standalone settings_dict key. The standalone's int
#: value 0/1/2/3 maps directly to the AP choice names none/low/medium/high.
TRAP_WEIGHT_FIELDS: Dict[str, str] = {
    "bubble_trap_weight": "trap_weight_bubble",
    "reverse_trap_weight": "trap_weight_reverse",
    "slow_trap_weight": "trap_weight_slow",
    "disable_a_trap_weight": "trap_weight_disablea",
    "disable_b_trap_weight": "trap_weight_disableb",
    "disable_c_trap_weight": "trap_weight_disablecu",
    "disable_z_trap_weight": "trap_weight_disablez",
    "get_out_trap_weight": "trap_weight_getout",
    "dry_trap_weight": "trap_weight_dry",
    "flip_trap_weight": "trap_weight_flip",
    "ice_floor_weight": "trap_weight_icefloor",
    "paper_weight": "trap_weight_paper",
    "slip_weight": "trap_weight_slip",
    "animal_trap_weight": "trap_weight_animal",
    "rockfall_trap_weight": "trap_weight_rockfall",
    "disabletag_trap_weight": "trap_weight_disabletag",
}

#: Standalone trap-weight integer → AP choice name. Standalone values are
#: arbitrary ints, bucketed: 0→none, 1→low, 2→medium, >=3→high. Done as a
#: bucket rather than a dict lookup because (a) the standalone field is a
#: free-form int, and (b) AP's BaseTrapWeight uses option_high=4, so a blind
#: int passthrough would silently fall back to default for any "high" weight.
def _trap_weight_int_to_name(int_val: int) -> str:
    if int_val <= 0:
        return "none"
    if int_val == 1:
        return "low"
    if int_val == 2:
        return "medium"
    return "high"


# ---------------------------------------------------------------------------
# OptionDef — parsed metadata for a single AP option class
# ---------------------------------------------------------------------------


@dataclass
class OptionDef:
    """Parsed metadata for one AP option (one DK64Options dataclass field)."""

    field: str  # dataclass field name, e.g. "krool_in_boss_pool"
    class_name: str  # option class name, e.g. "KroolShuffle"
    kind: str  # "toggle" | "default_on_toggle" | "choice" | "text_choice" | "range" | "list" | "dict" | "unknown"
    display_name: str
    default: Any = None
    choices: Dict[str, int] = dc_field(default_factory=dict)  # choice/text_choice
    valid_keys: List[str] = dc_field(default_factory=list)  # list/dict
    range_min: Optional[int] = None
    range_max: Optional[int] = None


# ---------------------------------------------------------------------------
# AST-based parser for archipelago/Options.py
# ---------------------------------------------------------------------------

_TOGGLE_BASES = {"Toggle", "DefaultOnToggle", "DeathLink"}
_CHOICE_BASES = {"Choice"}
_TEXT_CHOICE_BASES = {"TextChoice"}
_RANGE_BASES = {"Range", "NamedRange"}
_LIST_BASES = {"OptionList", "OptionSet", "ItemSet"}
_DICT_BASES = {"OptionDict", "ItemDict"}


def _literal(node: ast.AST) -> Any:
    """Best-effort literal evaluation; returns None if not a constant."""
    try:
        return ast.literal_eval(node)
    except Exception:
        return None


def parse_options_file(path: str) -> Dict[str, OptionDef]:
    """Parse archipelago/Options.py via AST and return {ap_field → OptionDef}.

    Walks every ClassDef (recording each class' parent + body), then walks the
    DK64Options dataclass fields to pair `field_name` with its option class.
    Inheritance is resolved one level (e.g. BubbleTrapWeight inherits from
    BaseTrapWeight which inherits from Choice — we resolve that chain).
    """
    try:
        with open(path, "r") as f:
            source = f.read()
    except OSError as exc:
        logging.error("ArchipelagoMapper: could not read %s: %s", path, exc)
        return {}

    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        logging.error("ArchipelagoMapper: could not parse %s: %s", path, exc)
        return {}

    # First pass: collect every class -> (bases, body)
    classes: Dict[str, ast.ClassDef] = {}
    dk64_options: Optional[ast.ClassDef] = None
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            classes[node.name] = node
            if node.name == "DK64Options":
                dk64_options = node

    if dk64_options is None:
        logging.error("ArchipelagoMapper: DK64Options dataclass not found in %s", path)
        return {}

    # Walk DK64Options fields: each is an `AnnAssign` like `goal: Goal`.
    metadata: Dict[str, OptionDef] = {}
    for stmt in dk64_options.body:
        if not isinstance(stmt, ast.AnnAssign) or not isinstance(stmt.target, ast.Name):
            continue
        if not isinstance(stmt.annotation, ast.Name):
            continue
        ap_field = stmt.target.id
        class_name = stmt.annotation.id
        opt_def = _build_option_def(ap_field, class_name, classes)
        if opt_def is not None:
            metadata[ap_field] = opt_def

    return metadata


def _resolve_kind(class_name: str, classes: Dict[str, ast.ClassDef]) -> tuple[str, bool]:
    """Walk parent classes to find the top-level Archipelago base type.

    Returns ("toggle"|"choice"|… , default_on) where default_on is True only for
    DefaultOnToggle.
    """
    seen: set[str] = set()
    cur = class_name
    while cur and cur not in seen:
        seen.add(cur)
        node = classes.get(cur)
        if node is None:
            break
        for base in node.bases:
            if isinstance(base, ast.Name):
                bname = base.id
                if bname in _TOGGLE_BASES:
                    return ("toggle", bname == "DefaultOnToggle")
                if bname in _CHOICE_BASES:
                    return ("choice", False)
                if bname in _TEXT_CHOICE_BASES:
                    return ("text_choice", False)
                if bname in _RANGE_BASES:
                    return ("range", False)
                if bname in _LIST_BASES:
                    return ("list", False)
                if bname in _DICT_BASES:
                    return ("dict", False)
                # Continue up the chain if it's another user class.
                if bname in classes:
                    cur = bname
                    break
        else:
            break
    return ("unknown", False)


def _build_option_def(ap_field: str, class_name: str, classes: Dict[str, ast.ClassDef]) -> Optional[OptionDef]:
    """Construct an OptionDef by reading attributes off `class_name` (and parents)."""
    kind, default_on = _resolve_kind(class_name, classes)

    # Walk the inheritance chain bottom-up, collecting attribute assignments.
    # Subclass attributes win over parent ones.
    chain: List[ast.ClassDef] = []
    cur = class_name
    seen: set[str] = set()
    while cur and cur not in seen and cur in classes:
        seen.add(cur)
        chain.append(classes[cur])
        # Walk to first user-defined parent (skip Archipelago bases).
        next_parent: Optional[str] = None
        for base in classes[cur].bases:
            if isinstance(base, ast.Name) and base.id in classes:
                next_parent = base.id
                break
        cur = next_parent or ""

    attrs: Dict[str, Any] = {}
    choices: Dict[str, int] = {}
    valid_keys: List[str] = []
    docstring: Optional[str] = None

    for cls_node in reversed(chain):  # Parent-first so subclass overrides.
        if docstring is None:
            docstring = ast.get_docstring(cls_node)
        for stmt in cls_node.body:
            if isinstance(stmt, ast.Assign):
                # `option_xxx = N` for choice options
                for target in stmt.targets:
                    if isinstance(target, ast.Name) and target.id.startswith("option_"):
                        val = _literal(stmt.value)
                        if isinstance(val, int):
                            choices[target.id[len("option_") :]] = val
                # Other named assignments (display_name, default, range_*, valid_keys)
                if len(stmt.targets) == 1 and isinstance(stmt.targets[0], ast.Name):
                    name = stmt.targets[0].id
                    val = _literal(stmt.value)
                    if val is not None or isinstance(stmt.value, (ast.Set, ast.List, ast.Dict, ast.Tuple)):
                        attrs[name] = val
                        if name == "valid_keys" and isinstance(val, (set, frozenset, list, tuple)):
                            valid_keys = sorted(str(x) for x in val)
            elif isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name):
                # `valid_keys = {...}` is sometimes mistakenly written as
                # `valid_keys: {...}` (a type annotation with no assignment).
                # We try to recover the literal anyway.
                if stmt.value is not None:
                    val = _literal(stmt.value)
                    if val is not None:
                        attrs[stmt.target.id] = val
                        if stmt.target.id == "valid_keys" and isinstance(val, (set, frozenset, list, tuple)):
                            valid_keys = sorted(str(x) for x in val)

    display_name = attrs.get("display_name") or ap_field.replace("_", " ").title()

    default = attrs.get("default")
    if default is None and kind == "toggle":
        default = bool(default_on)

    range_min = attrs.get("range_start") if kind == "range" else None
    range_max = attrs.get("range_end") if kind == "range" else None

    return OptionDef(
        field=ap_field,
        class_name=class_name,
        kind="default_on_toggle" if default_on else kind,
        display_name=display_name,
        default=default,
        choices=choices,
        valid_keys=valid_keys,
        range_min=range_min,
        range_max=range_max,
    )


# ---------------------------------------------------------------------------
# Generic helpers
# ---------------------------------------------------------------------------


def _name_of(value: Any) -> Optional[str]:
    """Extract the .name attribute of an enum-like value, else str/None."""
    if value is None:
        return None
    if hasattr(value, "name"):
        return value.name
    if isinstance(value, str):
        return value
    return None


def _enum_name(value: Any, opt: OptionDef, *, name_map: Optional[Dict[str, str]] = None) -> Optional[str]:
    """Resolve a settings_dict value (enum / int / str) to an AP choice-name.

    Validates the result against opt.choices when available — invalid names
    log a warning and fall back to the option's default name.
    """
    name = _name_of(value)
    if name is None and isinstance(value, int):
        # Last-ditch: look up the int in the option's choices.
        for cname, cval in opt.choices.items():
            if cval == value:
                name = cname
                break
    if name is None:
        return None
    if name_map and name in name_map:
        name = name_map[name]
    if opt.choices and name not in opt.choices:
        logging.debug("ArchipelagoMapper: %r is not a valid choice for %s; passing through anyway", name, opt.field)
    return name


def _to_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ("true", "1", "yes", "on")
    return bool(value)


def _iter_item_pool_entries(settings_dict: Dict[str, Any]) -> Iterable[str]:
    """Yield each ItemRandoListSelected enum-name across all *shuffled* pools.

    DK64R uses pools 0..4 for items and 5..9 for checks; pools 0 and 5 are
    "unshuffled" and excluded so user-parked items don't leak into AP exports.
    """
    for pool in range(10):
        if pool in (0, 5):
            continue
        for item in settings_dict.get(f"item_rando_list_{pool}", []) or []:
            name = _name_of(item)
            if name is None and isinstance(item, int):
                try:
                    from randomizer.Enums.Settings import ItemRandoListSelected

                    name = ItemRandoListSelected(item).name
                except Exception:
                    continue
            if name is not None:
                yield name


def _enum_int(value: Any) -> Optional[int]:
    """Return the integer value of an enum-like or int, else None."""
    if hasattr(value, "value"):
        try:
            return int(value.value)
        except (TypeError, ValueError):
            return None
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    return None


# ---------------------------------------------------------------------------
# Converter registry
# ---------------------------------------------------------------------------

#: Each converter receives (settings_dict, option_def) and returns the AP-shaped
#: value, or None to indicate "no override — fall through to defaults".
Converter = Callable[[Dict[str, Any], OptionDef], Any]

CONVERTERS: Dict[str, Converter] = {}


def converter(*ap_fields: str) -> Callable[[Converter], Converter]:
    """Register a function to handle one or more AP field names."""

    def deco(fn: Converter) -> Converter:
        for f in ap_fields:
            CONVERTERS[f] = fn
        return fn

    return deco


# ---------- Goals & win condition --------------------------------------------------


@converter("goal")
def _conv_goal(settings: Dict[str, Any], opt: OptionDef) -> Any:
    # helm_hurry overrides win_condition_item: it's a separate site toggle that,
    # when on, forces the AP goal to "treasure_hurry" regardless of the wincon.
    if _to_bool(settings.get("helm_hurry")):
        return "treasure_hurry"
    raw = settings.get("win_condition_item")
    name = _name_of(raw)
    if name is None and isinstance(raw, int):
        try:
            from randomizer.Enums.Settings import WinConditionComplex

            name = WinConditionComplex(raw).name
        except Exception:
            return None
    if name is None:
        return None
    return WIN_CONDITION_TO_GOAL_NAME.get(name, name)


@converter("goal_quantity")
def _conv_goal_quantity(settings: Dict[str, Any], opt: OptionDef) -> Dict[str, int]:
    result = dict(GOAL_QUANTITY_DEFAULTS)
    count = settings.get("win_condition_count")
    item = settings.get("win_condition_item")
    int_val = _enum_int(item)
    if int_val is None:
        return result
    name = HELM_DOOR_ITEM_KEY.get(int_val)
    if name is None:
        try:
            from randomizer.Enums.Settings import WinConditionComplex

            ap_name = WIN_CONDITION_TO_GOAL_NAME.get(WinConditionComplex(int_val).name)
            name = GOAL_NAME_TO_WIN_KEY.get(ap_name) if ap_name else None
        except Exception:
            name = None
    if name and count:
        try:
            result[name] = int(count)
        except (TypeError, ValueError):
            pass
    return result


@converter("require_beating_krool")
def _conv_require_beating_krool(settings: Dict[str, Any], opt: OptionDef) -> bool:
    return _to_bool(settings.get("win_condition_spawns_ship"))


@converter("pregiven_keys")
def _conv_pregiven_keys(settings: Dict[str, Any], opt: OptionDef) -> Optional[int]:
    raw = settings.get("krool_key_count")
    return int(raw) if raw is not None else None


# ---------- Boss pool / K. Rool ---------------------------------------------------


@converter("krool_in_boss_pool")
def _conv_krool_in_boss_pool(settings: Dict[str, Any], opt: OptionDef) -> Optional[str]:
    """K. Rool boss pool: emit the choice name (off / krool_only / full_shuffle).

    Bug fixed here: previously this was `bool(...)`, collapsing 3 values to 2.
    """
    raw = settings.get("krool_in_boss_pool_v2")
    if raw is None:
        return None
    name = _enum_name(raw, opt)
    if name is None and isinstance(raw, int):
        try:
            from randomizer.Enums.Settings import KroolInBossPool

            name = KroolInBossPool(raw).name
        except Exception:
            return None
    return name


@converter("allowed_bosses")
def _conv_allowed_bosses(settings: Dict[str, Any], opt: OptionDef) -> List[str]:
    bosses = settings.get("bosses_selected") or []
    if not isinstance(bosses, (list, set, tuple)):
        bosses = [bosses]
    out: List[str] = []
    try:
        from randomizer.Enums.Maps import Maps  # noqa: F401
    except ImportError:
        Maps = None  # type: ignore[assignment]
    for boss in bosses:
        name = _name_of(boss)
        if name is None and isinstance(boss, int) and Maps is not None:
            try:
                name = Maps(boss).name
            except Exception:
                continue
        if name and name in BOSS_MAP_NAME_TO_AP:
            out.append(BOSS_MAP_NAME_TO_AP[name])
    # Default to all bosses if the standalone settings didn't specify any.
    return out or list(BOSS_MAP_NAME_TO_AP.values())


@converter("harder_bosses")
def _conv_harder_bosses(settings: Dict[str, Any], opt: OptionDef) -> List[str]:
    return _names_from_settings(settings.get("hard_bosses_selected"), "HardBossesSelected")


# ---------- Item pool & derived presence checks -----------------------------------


@converter("item_pool")
def _conv_item_pool(settings: Dict[str, Any], opt: OptionDef) -> List[str]:
    keys: set[str] = set()
    for enum_name in _iter_item_pool_entries(settings):
        mapped = ITEM_POOL_ENUM_TO_KEY.get(enum_name)
        if mapped:
            keys.add(mapped)
    return sorted(keys)


# Boolean derivatives (hints_in_item_pool, dropsanity, etc.) only make sense
# if the corresponding AP option exists in DK64Options. They're emitted from
# this single helper so all six stay consistent.
def _make_pool_presence_converter(target_enum_name: str) -> Converter:
    def _conv(settings: Dict[str, Any], opt: OptionDef) -> bool:
        return any(name == target_enum_name for name in _iter_item_pool_entries(settings))

    return _conv


for _ap_field, _enum_n in ITEM_POOL_PRESENCE_CHECKS.items():
    CONVERTERS[_ap_field] = _make_pool_presence_converter(_enum_n)


# ---------- Lists with enum→name mapping ------------------------------------------


def _names_from_settings(value: Any, enum_class_name: str) -> List[str]:
    """Generic enum-list → list-of-names. Tolerates ints, enums, and strings."""
    if value is None:
        return []
    if not isinstance(value, (list, set, tuple)):
        value = [value]
    out: List[str] = []
    enum_class = None
    for item in value:
        name = _name_of(item)
        if name is None and isinstance(item, int):
            if enum_class is None:
                try:
                    from importlib import import_module

                    enum_class = getattr(import_module("randomizer.Enums.Settings"), enum_class_name, None)
                except Exception:
                    enum_class = None
            if enum_class is not None:
                try:
                    name = enum_class(item).name  # type: ignore[misc]
                except Exception:
                    continue
        if name is not None:
            out.append(name)
    return out


@converter("tricks_selected")
def _conv_tricks(settings: Dict[str, Any], opt: OptionDef) -> List[str]:
    return _names_from_settings(settings.get("tricks_selected"), "TricksSelected")


@converter("glitches_selected")
def _conv_glitches(settings: Dict[str, Any], opt: OptionDef) -> List[str]:
    return _names_from_settings(settings.get("glitches_selected"), "GlitchesSelected")


@converter("hard_mode_selected")
def _conv_hard_mode(settings: Dict[str, Any], opt: OptionDef) -> List[str]:
    return _names_from_settings(settings.get("hard_mode_selected"), "HardModeSelected")


@converter("remove_barriers_selected")
def _conv_remove_barriers(settings: Dict[str, Any], opt: OptionDef) -> List[str]:
    return _names_from_settings(settings.get("remove_barriers_selected"), "RemovedBarriersSelected")


@converter("shuffled_bonus_barrels")
def _conv_shuffled_bonus_barrels(settings: Dict[str, Any], opt: OptionDef) -> List[str]:
    return _names_from_settings(settings.get("minigames_list_selected"), "MinigamesListSelected")


@converter("enemies_selected")
def _conv_enemies(settings: Dict[str, Any], opt: OptionDef) -> List[str]:
    raw_names = _names_from_settings(settings.get("enemies_selected"), "Enemies")
    return [ENEMY_NAME_REMAP.get(n, n) for n in raw_names]


# ---------- Logic & misc choices --------------------------------------------------


@converter("logic_type")
def _conv_logic_type(settings: Dict[str, Any], opt: OptionDef) -> str:
    raw = settings.get("logic_type")
    int_val = _enum_int(raw)
    if int_val is not None and int_val in LOGIC_TYPE_INT_TO_NAME:
        return LOGIC_TYPE_INT_TO_NAME[int_val]
    name = _name_of(raw)
    if name and name in LOGIC_TYPE_INT_TO_NAME:
        return LOGIC_TYPE_INT_TO_NAME[name]
    return "glitchless"


@converter("loading_zone_rando")
def _conv_loading_zone_rando(settings: Dict[str, Any], opt: OptionDef) -> str:
    """Loading-zone rando: 'yes' iff level_randomization == loadingzone, else 'no'.

    Bug fixed here: previously returned bool, but AP TextChoice expects 'yes'/'no'.
    """
    raw = settings.get("level_randomization")
    name = _name_of(raw)
    if name is None and isinstance(raw, int):
        try:
            from randomizer.Enums.Settings import LevelRandomization

            name = LevelRandomization(raw).name
        except Exception:
            return "no"
    return "yes" if name == "loadingzone" else "no"


@converter("galleon_water_level")
def _conv_galleon_water_level(settings: Dict[str, Any], opt: OptionDef) -> str:
    raw = settings.get("galleon_water")
    name = _name_of(raw)
    if name is None and isinstance(raw, int):
        try:
            from randomizer.Enums.Settings import GalleonWaterSetting

            name = GalleonWaterSetting(raw).name
        except Exception:
            return "raised"
    return name if name in ("raised", "lowered") else "raised"


@converter("dk_portal_location_rando")
def _conv_dk_portal(settings: Dict[str, Any], opt: OptionDef) -> str:
    raw = settings.get("dk_portal_location_rando_v2")
    name = _name_of(raw)
    if name is None and isinstance(raw, int):
        try:
            from randomizer.Enums.Settings import DKPortalRando

            name = DKPortalRando(raw).name
        except Exception:
            return "off"
    # Standalone uses "on" for full rando; AP option is "all".
    if name == "on":
        return "all"
    return name if name in opt.choices else "off"


@converter("random_starting_region")
def _conv_random_starting_region(settings: Dict[str, Any], opt: OptionDef) -> str:
    raw = settings.get("random_starting_region_new")
    name = _name_of(raw)
    if name is None and isinstance(raw, int):
        try:
            from randomizer.Enums.Settings import RandomStartingRegion

            name = RandomStartingRegion(raw).name
        except Exception:
            return "off"
    return name if name in opt.choices else "off"


# ---------- Blocker / Troff behavior ----------------------------------------------


def _is_chaos_blocker(settings: Dict[str, Any]) -> Optional[bool]:
    raw = settings.get("blocker_selection_behavior")
    if raw is None:
        return None
    int_val = _enum_int(raw)
    return int_val == 4  # BLockerSetting.chaos


def _is_random_blocker(settings: Dict[str, Any]) -> Optional[bool]:
    raw = settings.get("blocker_selection_behavior")
    if raw is None:
        return None
    int_val = _enum_int(raw)
    # easy_random=1, normal_random=2, hard_random=3, chaos=4
    return int_val in (1, 2, 3, 4)


@converter("enable_chaos_blockers")
def _conv_enable_chaos_blockers(settings: Dict[str, Any], opt: OptionDef) -> Optional[bool]:
    val = _is_chaos_blocker(settings)
    return False if val is None else val


@converter("randomize_blocker_required_amounts")
def _conv_randomize_blockers(settings: Dict[str, Any], opt: OptionDef) -> Optional[bool]:
    val = _is_random_blocker(settings)
    return False if val is None else val


@converter("randomize_troff")
def _conv_randomize_troff(settings: Dict[str, Any], opt: OptionDef) -> bool:
    raw = settings.get("tns_selection_behavior")
    int_val = _enum_int(raw)
    if int_val is None:
        return True
    return int_val in (1, 2)  # normal_random or hard_random


@converter("troff_max")
def _conv_troff_max(settings: Dict[str, Any], opt: OptionDef) -> int:
    raw = settings.get("troff_text")
    try:
        return int(raw) if raw is not None else 150
    except (TypeError, ValueError):
        return 150


@converter("level_blockers")
def _conv_level_blockers(settings: Dict[str, Any], opt: OptionDef) -> Dict[str, int]:
    defaults = [0, 0, 0, 0, 0, 0, 0, 64]
    return {f"level_{i + 1}": int(settings.get(f"blocker_{i}", defaults[i])) for i in range(8)}


@converter("level_troff")
def _conv_level_troff(settings: Dict[str, Any], opt: OptionDef) -> Dict[str, int]:
    return {f"level_{i + 1}": int(settings.get(f"troff_{i}", 0)) for i in range(8)}


@converter("maximize_level8_blocker")
def _conv_maximize_helm_blocker(settings: Dict[str, Any], opt: OptionDef) -> Optional[bool]:
    raw = settings.get("maximize_helm_blocker")
    return None if raw is None else _to_bool(raw)


# ---------- Cutscenes / shops / minigames -----------------------------------------


@converter("enable_cutscenes")
def _conv_enable_cutscenes(settings: Dict[str, Any], opt: OptionDef) -> Optional[bool]:
    raw = settings.get("more_cutscene_skips")
    if raw is None:
        return None
    int_val = _enum_int(raw)
    if int_val is None:
        name = _name_of(raw)
        return None if name is None else name != "auto"
    # ExtraCutsceneSkips.auto = 2 → cutscenes NOT enabled
    return int_val != 2


@converter("enable_shared_shops")
def _conv_enable_shared_shops(settings: Dict[str, Any], opt: OptionDef) -> Optional[bool]:
    raw = settings.get("smaller_shops")
    return None if raw is None else _to_bool(raw)


@converter("hard_minigames")
def _conv_hard_minigames(settings: Dict[str, Any], opt: OptionDef) -> Optional[bool]:
    raw = settings.get("disable_hard_minigames")
    return None if raw is None else not _to_bool(raw)


@converter("shop_prices")
def _conv_shop_prices(settings: Dict[str, Any], opt: OptionDef) -> str:
    if not _to_bool(settings.get("shops_dont_cost")):
        return "free"
    raw = settings.get("random_prices")
    int_val = _enum_int(raw)
    if int_val is None:
        return "free"
    return SHOP_PRICE_NAMES.get(int_val, "free")


# ---------- Helm doors -----------------------------------------------------------


@converter("helm_door_item_count")
def _conv_helm_door_item_count(settings: Dict[str, Any], opt: OptionDef) -> Dict[str, int]:
    result = dict(HELM_DOOR_COUNT_DEFAULTS)
    for door_key, count_key in (("crown_door_item", "crown_door_item_count"), ("coin_door_item", "coin_door_item_count")):
        item_int = _enum_int(settings.get(door_key))
        if item_int is None:
            continue
        item_key = HELM_DOOR_ITEM_KEY.get(item_int)
        if item_key:
            try:
                result[item_key] = int(settings.get(count_key, 1))
            except (TypeError, ValueError):
                result[item_key] = 1
    return result


# ---------- Trap weights ---------------------------------------------------------


def _ice_traps_enabled(settings: Dict[str, Any]) -> bool:
    """True iff ItemRandoFiller.icetraps (value 2) is in filler_items_selected.

    When ice traps aren't in the filler pool, no traps will ever be sent, so
    every individual trap weight should report as 'none' regardless of what
    its trap_weight_<short> integer is set to.
    """
    for entry in settings.get("filler_items_selected", []) or []:
        if _name_of(entry) == "icetraps" or _enum_int(entry) == 2:
            return True
    return False


def _make_trap_weight_converter(settings_key: str) -> Converter:
    def _conv(settings: Dict[str, Any], opt: OptionDef) -> Optional[str]:
        if not _ice_traps_enabled(settings):
            return "none"
        int_val = _enum_int(settings.get(settings_key))
        if int_val is None:
            return None
        return _trap_weight_int_to_name(int_val)

    return _conv


for _ap_field, _settings_key in TRAP_WEIGHT_FIELDS.items():
    CONVERTERS[_ap_field] = _make_trap_weight_converter(_settings_key)


# ---------- Switchsanity / kong models / starting moves ---------------------------


@converter("switchsanity")
def _conv_switchsanity(settings: Dict[str, Any], opt: OptionDef) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for key in SWITCHSANITY_SWITCH_KEYS:
        raw = settings.get(f"switchsanity_switch_{key}")
        if raw is None:
            out[key] = "off"
            continue
        int_val = _enum_int(raw)
        if int_val is None:
            out[key] = "off"
            continue
        if key in SWITCHSANITY_GONE_KEYS:
            out[key] = SWITCHSANITY_GONE_NAMES.get(int_val, "off")
        else:
            out[key] = SWITCHSANITY_KONG_NAMES.get(int_val, "off")
    return out


@converter("alter_switch_allocation")
def _conv_alter_switch_allocation(settings: Dict[str, Any], opt: OptionDef) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for i in range(1, 9):
        raw = settings.get(f"prog_slam_level_{i}")
        if raw is None:
            out[f"level_{i}"] = SLAM_DEFAULTS[f"level_{i}"]
        else:
            int_val = _enum_int(raw)
            out[f"level_{i}"] = SLAM_NAMES.get(int_val if int_val is not None else -1, "green")
    return out


@converter("kong_models")
def _conv_kong_models(settings: Dict[str, Any], opt: OptionDef) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for kong in ("dk", "diddy", "lanky", "tiny", "chunky"):
        int_val = _enum_int(settings.get(f"kong_model_{kong}"))
        out[kong] = KONG_MODEL_NAMES.get(int_val if int_val is not None else 0, "default")
    return out


@converter("krusha_model_mode")
def _conv_krusha(settings: Dict[str, Any], opt: OptionDef) -> str:
    """If any kong was assigned the 'krusha' model, report 'manual'; else 'none'."""
    for kong in ("dk", "diddy", "lanky", "tiny", "chunky"):
        if _enum_int(settings.get(f"kong_model_{kong}")) == 2:  # KongModels.krusha
            return "manual"
    return "none"


def _make_starting_move_pool_converter(pool_num: int) -> Converter:
    def _conv(settings: Dict[str, Any], opt: OptionDef) -> Optional[List[str]]:
        items = settings.get(f"starting_moves_list_{pool_num}")
        if items is None:
            return None
        if not items:
            return []
        try:
            from randomizer.Enums.Items import Items as ItemsEnum
            from randomizer.Lists.Item import ItemList
        except ImportError:
            return [str(x) for x in items]
        names: List[str] = []
        for item_id in items:
            if isinstance(item_id, int):
                try:
                    item_id = ItemsEnum(item_id)
                except ValueError:
                    continue
            item_obj = ItemList.get(item_id)
            if item_obj is not None:
                names.append(_PROGRESSIVE_NAME_NORMALIZE.get(item_obj.name, item_obj.name))
        return names

    return _conv


for _i in range(1, 6):
    CONVERTERS[f"starting_move_pool_{_i}"] = _make_starting_move_pool_converter(_i)


# ---------------------------------------------------------------------------
# Mapper
# ---------------------------------------------------------------------------


class ArchipelagoMapper:
    """Convert standalone DK64R settings dicts into Archipelago YAML."""

    def __init__(self, options_path: Optional[str] = None) -> None:
        if options_path is None:
            options_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "archipelago", "Options.py"))
        self.options_metadata: Dict[str, OptionDef] = parse_options_file(options_path)
        if not self.options_metadata:
            logging.warning("ArchipelagoMapper: no options parsed; YAML export will be empty")
        self.fallthrough_settings_key: Dict[str, str] = self._build_fallthrough_name_map()

    # ---- discovery -------------------------------------------------------

    def _build_fallthrough_name_map(self) -> Dict[str, str]:
        """Build the AP-name → settings-key map for options *without* a converter.

        Reads `settings_dict["X"] = options.Y.value` patterns from FillSettings.py
        (single source of truth for simple round-trips) and overlays the small
        manual table in `_FALLTHROUGH_NAME_OVERRIDES`.
        """
        path = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "archipelago", "FillSettings.py"))
        auto: Dict[str, str] = {}
        try:
            with open(path, "r") as f:
                source = f.read()
        except OSError:
            source = ""
        if source:
            try:
                tree = ast.parse(source)
            except SyntaxError:
                tree = None
            if tree is not None:
                for node in ast.walk(tree):
                    if not isinstance(node, ast.Assign):
                        continue
                    if len(node.targets) != 1:
                        continue
                    target = node.targets[0]
                    if not (isinstance(target, ast.Subscript) and isinstance(target.value, ast.Name) and target.value.id == "settings_dict"):
                        continue
                    key = _literal(target.slice)
                    if not isinstance(key, str):
                        continue
                    # Only match `options.<name>.value` or `options.<name>` RHS.
                    rhs = node.value
                    ap_name: Optional[str] = None
                    if isinstance(rhs, ast.Attribute) and rhs.attr == "value" and isinstance(rhs.value, ast.Attribute) and isinstance(rhs.value.value, ast.Name) and rhs.value.value.id == "options":
                        ap_name = rhs.value.attr
                    elif isinstance(rhs, ast.Attribute) and isinstance(rhs.value, ast.Name) and rhs.value.id == "options":
                        ap_name = rhs.attr
                    if ap_name:
                        auto[ap_name] = key
        return {**auto, **_FALLTHROUGH_NAME_OVERRIDES}

    def get_exported_settings_keys(self) -> List[str]:
        """Return a sorted list of every standalone settings_dict key the mapper
        consumes when producing AP YAML.

        Used by the UI to filter the settings form to "AP-exportable only".
        Built from three sources: the fallthrough name map (auto + manual),
        explicit converter inputs, and trap-weight settings keys.
        """
        keys: set[str] = set(self.fallthrough_settings_key.values())
        keys.update(TRAP_WEIGHT_FIELDS.values())
        keys.update(_CONVERTER_INPUT_KEYS)
        keys -= SKIP_SETTINGS
        return sorted(keys)

    # ---- value conversion ----------------------------------------------

    def _convert(self, ap_field: str, settings: Dict[str, Any]) -> Any:
        """Run the converter (if any) else fall through to a generic converter."""
        opt = self.options_metadata.get(ap_field)
        if opt is None:
            return None

        fn = CONVERTERS.get(ap_field)
        if fn is not None:
            return fn(settings, opt)

        # Generic fallthrough by option kind.
        settings_key = self.fallthrough_settings_key.get(ap_field, ap_field)
        raw = settings.get(settings_key)
        if raw is None:
            return None

        if opt.kind in ("toggle", "default_on_toggle"):
            return _to_bool(raw)

        if opt.kind == "range":
            try:
                int_val = int(raw if not hasattr(raw, "value") else raw.value)
            except (TypeError, ValueError):
                return opt.default
            lo = opt.range_min if opt.range_min is not None else int_val
            hi = opt.range_max if opt.range_max is not None else int_val
            return max(lo, min(hi, int_val))

        if opt.kind in ("choice", "text_choice"):
            return _enum_name(raw, opt)

        if opt.kind == "list":
            if isinstance(raw, (list, set, tuple)):
                return [_name_of(x) or str(x) for x in raw]
            return [_name_of(raw) or str(raw)]

        if opt.kind == "dict":
            return raw if isinstance(raw, dict) else None

        return raw

    # ---- yaml -----------------------------------------------------------

    def _format_default(self, opt: OptionDef) -> Any:
        """Convert opt.default (raw class attribute value) to its AP-shaped form."""
        default = opt.default
        if default is None:
            return None
        if opt.kind in ("toggle", "default_on_toggle"):
            return _to_bool(default)
        if opt.kind in ("choice", "text_choice"):
            if isinstance(default, str):
                return default
            if isinstance(default, int) and opt.choices:
                for cname, cval in opt.choices.items():
                    if cval == default:
                        return cname
            return default
        if opt.kind == "list":
            return list(default) if isinstance(default, (list, set, tuple, frozenset)) else default
        if opt.kind == "dict":
            return dict(default) if isinstance(default, dict) else default
        return default

    def settings_to_yaml(self, settings_dict: Dict[str, Any], player_name: str = "Player", game_version: str = "0.6.7") -> str:
        """Convert a standalone settings_dict into Archipelago YAML."""
        if not self.options_metadata:
            return "# Error: Could not parse Archipelago options from Options.py"

        yaml_data: Dict[str, Any] = {
            "name": player_name,
            "game": "Donkey Kong 64",
            "requires": {"version": game_version},
            "Donkey Kong 64": {},
        }
        defaults_block: Dict[str, Any] = {}

        for ap_field, opt in self.options_metadata.items():
            settings_key = self.fallthrough_settings_key.get(ap_field, ap_field)
            if settings_key in SKIP_SETTINGS:
                continue

            value = self._convert(ap_field, settings_dict)
            using_default = False
            if value is None:
                if opt.default is None:
                    continue
                value = self._format_default(opt)
                if value is None:
                    continue
                using_default = True

            # Special-case death_link: only emit when truthy (matches prior behavior).
            if ap_field == "death_link":
                if value:
                    yaml_data["Donkey Kong 64"][ap_field] = value
                continue

            formatted = ("true" if value else "false") if isinstance(value, bool) else value
            if using_default:
                defaults_block[ap_field] = formatted
            else:
                yaml_data["Donkey Kong 64"][ap_field] = formatted

        body = yaml.dump(yaml_data, default_flow_style=False, sort_keys=False, allow_unicode=True, width=120)
        if defaults_block:
            body = body.rstrip("\n") + "\n  # Default settings (not found in form data):\n"
            for ap_field, value in sorted(defaults_block.items()):
                if isinstance(value, list):
                    body += f"  {ap_field}:\n"
                    for item in value:
                        body += f"  - {item}\n"
                else:
                    body += f"  {ap_field}: {value}\n"

        return "# Donkey Kong 64 Randomizer\n# Generated from https://dk64randomizer.com \n\n" + body


# ---------------------------------------------------------------------------
# Module-level singleton + entry points (preserve existing import surface)
# ---------------------------------------------------------------------------

_mapper_instance: Optional[ArchipelagoMapper] = None


def get_mapper() -> ArchipelagoMapper:
    """Get or create the global mapper instance."""
    global _mapper_instance
    if _mapper_instance is None:
        _mapper_instance = ArchipelagoMapper()
    return _mapper_instance


def export_to_yaml(settings_dict: Dict[str, Any], player_name: str = "Player", game_version: str = "0.6.7") -> str:
    """Export standalone settings to Archipelago YAML format."""
    return get_mapper().settings_to_yaml(settings_dict, player_name=player_name, game_version=game_version)
