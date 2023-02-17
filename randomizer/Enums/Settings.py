"""File containing enums to represent all settings."""
from enum import IntEnum, auto

from randomizer.Enums.Items import Items
from randomizer.Lists.EnemyTypes import Enemies
from randomizer.Lists.MapsAndExits import Maps

# Each select-based setting should have its own associated enum class. The enum
# values should exactly match the input values in the HTML (not the IDs).

# Settings to double-check:
# ActivateAllBananaports
# EnemySelector
# HelmSetting
# MicrohintsEnabled
# WinCondition
# Search for IsGlitchEnabled
# Search for DoorItemCheck
# static/presets/default.json needs to be reworked

# Randomizers

class LogicType(IntEnum):
    glitchless = auto()
    glitch = auto()
    nologic = auto()

# These values are tied to the GlitchSelector in randomizer.Lists.Logic.
class GlitchesSelected(IntEnum):
    advanced_platforming = auto()
    b_locker_skips = auto()
    general_clips = auto()
    ledge_clips = auto()
    moonkicks = auto()
    phase_swimming = auto()
    phase_walking = auto()
    skew = auto()
    spawn_snags = auto()
    swim_through_shores = auto()
    tag_barrel_storage = auto()
    troff_n_scoff_skips = auto()

# This enum is explicitly indexed for use in ApplyRandomizer.py.
class ActivateAllBananaports(IntEnum):
    off = 0
    all = 1
    isles = 2

class LevelRandomization(IntEnum):
    level_order = auto()
    loadingzone = auto()
    loadingzonesdecoupled = auto()
    vanilla = auto()

# These values are tied to the ItemRandoSelector in randomizer.Enums.Types.
# The presence of "beanpearl" requires a different enum from Types.
# TODO: merge this with the Types enum.
class ItemRandoListSelected(IntEnum):
    shop = auto()
    banana = auto()
    toughbanana = auto()
    crown = auto()
    blueprint = auto()
    key = auto()
    medal = auto()
    coin = auto()
    kong = auto()
    fairy = auto()
    rainbowcoin = auto()
    beanpearl = auto()
    fakeitem = auto()
    junkitem = auto()

class KasplatRandoSetting(IntEnum):
    off = auto()
    vanilla_locations = auto()
    location_shuffle = auto()

class MoveRando(IntEnum):
    off = auto()
    on = auto()
    cross_purchase = auto()
    start_with = auto()

class TrainingBarrels(IntEnum):
    normal = auto()
    shuffled = auto()

class RandomPrices(IntEnum):
    vanilla = auto()
    free = auto()
    low = auto()
    medium = auto()
    high = auto()
    extreme = auto()

class ShockwaveStatus(IntEnum):
    vanilla = auto()
    shuffled = auto()
    shuffled_decoupled = auto()
    start_with = auto()

class BananaportRando(IntEnum):
    off = auto()
    in_level = auto()
    crossmap_coupled = auto()
    crossmap_decoupled = auto()

# Overworld

# These values are tied to the MinigameSelector in randomizer.Lists.Minigame.
class MinigamesListSelected(IntEnum):
    batty_barrel_bandit = auto()
    big_bug_bash = auto()
    busy_barrel_barrage = auto()
    mad_maze_maul = auto()
    minecart_mayhem = auto()
    beaver_bother = auto()
    teetering_turtle_trouble = auto()
    stealthy_snoop = auto()
    stash_snatch = auto()
    splish_splash_salvage = auto()
    speedy_swing_sortie = auto()
    krazy_kong_klamour = auto()
    searchlight_seek = auto()
    kremling_kosh = auto()
    peril_path_panic = auto()
    helm_minigames = auto()

# This enum is explicitly indexed for use in ApplyRandomizer.py.
class WinCondition(IntEnum):
    beat_krool = 0
    get_key8 = 1
    all_fairies = 2
    all_blueprints = 3
    all_medals = 4
    poke_snap = 5
    all_keys = 6

class FreeTradeSetting(IntEnum):
    none = auto()
    not_blueprints = auto()
    major_collectibles = auto()

class KrushaUi(IntEnum):
    no_slot = auto()
    dk = auto()
    diddy = auto()
    lanky = auto()
    tiny = auto()
    chunky = auto()
    random = auto()

class HelmDoorItem(IntEnum):
    vanilla = auto()
    opened = auto()
    random = auto()
    req_gb = auto()
    req_bp = auto()
    req_companycoins = auto()
    req_key = auto()
    req_medal = auto()
    req_crown = auto()
    req_fairy = auto()
    req_rainbowcoin = auto()
    req_bean = auto()
    req_pearl = auto()

# Difficulty

class DamageAmount(IntEnum):
    default = auto()
    ohko = auto()
    double = auto()
    quad = auto()

class CrownEnemyRando(IntEnum):
    off = auto()
    easy = auto()
    medium = auto()
    hard = auto()

# Quality of Life

# These values are tied to the QoLSelector in randomizer.Lists.QoL.
class MiscChangesSelected(IntEnum):
    auto_dance_skip = auto()
    fast_boot = auto()
    calm_caves = auto()
    animal_buddies_grab_items = auto()
    reduced_lag = auto()
    remove_extraneous_cutscenes = auto()
    hint_textbox_hold = auto()
    remove_wrinkly_puzzles = auto()
    fast_picture_taking = auto()
    hud_hotkey = auto()
    ammo_swap = auto()
    homing_balloons = auto()
    fast_transform_animation = auto()
    troff_n_scoff_audio_indicator = auto()
    lowered_aztec_lobby_bonus = auto()
    quicker_galleon_star = auto()
    vanilla_bug_fixes = auto()

class WrinklyHints(IntEnum):
    standard = auto()
    cryptic = auto()
    off = auto()

# This enum is explicitly indexed for use in ApplyRandomizer.py.
class HelmSetting(IntEnum):
    default = 0
    skip_start = 1
    skip_all = 2

# This enum is explicitly indexed for use in ApplyRandomizer.py.
class MicrohintsEnabled(IntEnum):
    off = 0
    base = 1
    all = 2

# Cosmetics

class MusicCosmetics(IntEnum):
    default = auto()
    randomized = auto()
    chaos = auto()
    uploaded = auto()

class KlaptrapModel(IntEnum):
    green = auto()
    purple = auto()
    red = auto()
    random_klap = auto()
    random_model = auto()

class CharacterColors(IntEnum):
    vanilla = auto()
    randomized = auto()
    custom = auto()

class ColorblindMode(IntEnum):
    off = auto()
    prot = auto()
    deut = auto()
    trit = auto()

# Additional enums not currently shown on the web site.

class ShuffleLoadingZones(IntEnum):
    none = auto()
    levels = auto()
    all = auto()

class MinigameBarrels(IntEnum):
    skip = auto()
    normal = auto()
    random = auto()
    selected = auto()

# A dictionary that maps setting names to the associated enum for that specific
# setting. This only applies to select-based settings. The key for each enum
# must exactly match the HTML name of the associated select.
SettingsMap = {
    # Randomizer
    "enemies_selected": Enemies,
    "logic_type": LogicType,
    "glitches_selected": GlitchesSelected,
    "activate_all_bananaports": ActivateAllBananaports,
    "level_randomization": LevelRandomization,
    "item_rando_list_selected": ItemRandoListSelected,
    "kasplat_rando_setting": KasplatRandoSetting,
    "move_rando": MoveRando,
    "training_barrels": TrainingBarrels,
    "random_prices": RandomPrices,
    "shockwave_status": ShockwaveStatus,
    "bananaport_rando": BananaportRando,
    "warp_level_list_selected": Maps,
    # Overworld
    "minigames_list_selected": MinigamesListSelected,
    "win_condition": WinCondition,
    "free_trade_setting": FreeTradeSetting,
    "krusha_ui": KrushaUi,
    "starting_keys_list_selected": Items,
    "crown_door_item": HelmDoorItem,
    "coin_door_item": HelmDoorItem,
    # Difficulty
    "damage_amount": DamageAmount,
    "crown_enemy_rando": CrownEnemyRando,
    # Quality of Life
    "misc_changes_selected": MiscChangesSelected,
    "wrinkly_hints": WrinklyHints,
    "helm_setting": HelmSetting,
    "microhints_enabled": MicrohintsEnabled,
    # Cosmetics
    "music_bgm": MusicCosmetics,
    "music_fanfares": MusicCosmetics,
    "music_events": MusicCosmetics,
    "klaptrap_model": KlaptrapModel,
    "dk_colors": CharacterColors,
    "diddy_colors": CharacterColors,
    "lanky_colors": CharacterColors,
    "tiny_colors": CharacterColors,
    "chunky_colors": CharacterColors,
    "rambi_colors": CharacterColors,
    "enguarde_colors": CharacterColors,
    "colorblind_mode": ColorblindMode,
    # Other
    "shuffle_loading_zones": ShuffleLoadingZones,
    "bonus_barrels": MinigameBarrels,
    "helm_barrels": MinigameBarrels
}
