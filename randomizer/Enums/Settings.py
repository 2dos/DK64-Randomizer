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
# Find where "seed" is being changed back to a string
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

# Used for settings.shuffle_loading_zones
class ShuffleLoadingZones(IntEnum):
    none = auto()
    levels = auto()
    all = auto()

# Used for settings.bonus_barrels and settings.helm_barrels
class MinigameBarrels(IntEnum):
    skip = auto()
    normal = auto()
    random = auto()
    selected = auto()

# An enum that lists all settings options provided in the HTML form. The names
# of each enum value must exactly match the HTML name of the associated
# select/checkbox/etc.
class FormSettings(IntEnum):
    # Randomizers

    # Global Randomizers
    enemy_rando = auto()
    enemies_selected = auto()
    enemy_speed_rando = auto()
    puzzle_rando = auto()
    krool_phase_order_rando = auto()
    helm_phase_order_rando = auto()
    boss_kong_rando = auto()
    logic_type = auto()
    glitches_selected = auto()
    activate_all_bananaports = auto()
    level_randomization = auto()
    # Location Randomizers
    boss_location_rando = auto()
    kong_rando = auto()
    random_patches = auto()
    shuffle_shops = auto()
    cb_rando = auto()
    shuffle_items = auto()
    item_rando_list_selected = auto()
    random_fairies = auto()
    kasplat_rando_setting = auto()
    move_rando = auto()
    training_barrels = auto()
    random_prices = auto()
    shockwave_status = auto()
    bananaport_rando = auto()
    warp_level_list_selected = auto()

    # Overworld

    # Global Settings
    bonus_barrel_auto_complete = auto()
    bonus_barrel_rando = auto()
    minigames_list_selected = auto()
    open_lobbies = auto()
    open_levels = auto()
    randomize_pickups = auto()
    alter_switch_allocation = auto()
    wrinkly_location_rando = auto()
    tns_location_rando = auto()
    crown_placement_rando = auto()
    high_req = auto()
    fast_gbs = auto()
    helm_hurry = auto()
    # Helm Hurry settings
    helmhurry_list_starting_time = auto()
    helmhurry_list_golden_banana = auto()
    helmhurry_list_blueprint = auto()
    helmhurry_list_company_coins = auto()
    helmhurry_list_move = auto()
    helmhurry_list_banana_medal = auto()
    helmhurry_list_rainbow_coin = auto()
    helmhurry_list_boss_key = auto()
    helmhurry_list_battle_crown = auto()
    helmhurry_list_bean = auto()
    helmhurry_list_pearl = auto()
    helmhurry_list_kongs = auto()
    helmhurry_list_fairies = auto()
    helmhurry_list_colored_bananas = auto()
    helmhurry_list_ice_traps = auto()
    # End Helm Hurry settings
    random_starting_region = auto()
    win_condition = auto()
    free_trade_setting = auto()
    krusha_ui = auto()
    random_medal_requirement = auto()
    medal_requirement = auto()
    medal_cb_req = auto()
    rareware_gb_fairies = auto()
    # Game Length Settings
    krool_random = auto()
    krool_phase_count = auto()
    helm_random = auto()
    helm_phase_count = auto()
    keys_random = auto()
    select_keys = auto()
    starting_keys_list_selected = auto()
    key_8_helm = auto()
    krool_access = auto()
    krool_key_count = auto()
    starting_random = auto()
    starting_kongs_count = auto()
    crown_door_item = auto()
    crown_door_item_count = auto()
    coin_door_item = auto()
    coin_door_item_count = auto()

    # Difficulty

    # Progression
    randomize_blocker_required_amounts = auto()
    blocker_0 = auto()
    blocker_1 = auto()
    blocker_2 = auto()
    blocker_3 = auto()
    blocker_4 = auto()
    blocker_5 = auto()
    blocker_6 = auto()
    blocker_7 = auto()
    randomize_cb_required_amounts = auto()
    troff_0 = auto()
    troff_1 = auto()
    troff_2 = auto()
    troff_3 = auto()
    troff_4 = auto()
    troff_5 = auto()
    troff_6 = auto()
    maximize_helm_blocker = auto()
    blocker_text = auto()
    troff_text = auto()
    # Difficulty
    no_healing = auto()
    no_melons = auto()
    hard_shooting = auto()
    hard_bosses = auto()
    perma_death = auto()
    disable_tag_barrels = auto()
    hard_blockers = auto()
    hard_troff_n_scoff = auto()
    hard_level_progression = auto()
    hard_enemies = auto()
    smaller_shops = auto()
    damage_amount = auto()
    crown_enemy_rando = auto()

    # Quality of Life

    fast_start_beginning_of_game = auto()
    quality_of_life = auto()
    misc_changes_selected = auto()
    shorten_boss = auto()
    enable_tag_anywhere = auto()
    enable_shop_hints = auto()
    fps_display = auto()
    wrinkly_available = auto()
    wrinkly_hints = auto()
    helm_setting = auto()
    microhints_enabled = auto()
    warp_to_isles = auto()
    portal_numbers = auto()
    shop_indicator = auto()
    fast_warps = auto()
    dpad_display = auto()
    auto_keys = auto()
    item_reward_previews = auto()

    # Cosmetics

    override_cosmetics = auto()
    # Music Rando
    random_music = auto()
    music_bgm = auto()
    music_fanfares = auto()
    music_events = auto()
    # Custom Music
    music_file = auto()
    # Miscellaneous
    klaptrap_model = auto()
    misc_cosmetics = auto()
    disco_chunky = auto()
    holiday_mode = auto()
    # Colors
    random_colors = auto()
    dk_colors = auto()
    dk_custom_color = auto()
    diddy_colors = auto()
    diddy_custom_color = auto()
    lanky_colors = auto()
    lanky_custom_color = auto()
    tiny_colors = auto()
    tiny_custom_color = auto()
    chunky_colors = auto()
    chunky_custom_color = auto()
    rambi_colors = auto()
    rambi_custom_color = auto()
    enguarde_colors = auto()
    enguarde_custom_color = auto()
    # Accessibility
    remove_water_oscillation = auto()
    colorblind_mode = auto()

    # Seed Generation

    seed = auto()
    settings_string = auto()
    generate_spoilerlog = auto()
    download_patch_file = auto()

# A dictionary that maps setting names to the associated enum for that specific
# setting. This only applies to select-based settings. The key for each enum
# must exactly match the HTML name of the associated select.
SettingsMap = {
    # Randomizer
    Settings.enemies_selected: Enemies,
    Settings.logic_type: LogicType,
    Settings.glitches_selected: GlitchesSelected,
    Settings.activate_all_bananaports: ActivateAllBananaports,
    Settings.level_randomization: LevelRandomization,
    Settings.item_rando_list_selected: ItemRandoListSelected,
    Settings.kasplat_rando_setting: KasplatRandoSetting,
    Settings.move_rando: MoveRando,
    Settings.training_barrels: TrainingBarrels,
    Settings.random_prices: RandomPrices,
    Settings.shockwave_status: ShockwaveStatus,
    Settings.bananaport_rando: BananaportRando,
    Settings.warp_level_list_selected: Maps,
    # Overworld
    Settings.minigames_list_selected: MinigamesListSelected,
    Settings.win_condition: WinCondition,
    Settings.free_trade_setting: FreeTradeSetting,
    Settings.krusha_ui: KrushaUi,
    Settings.starting_keys_list_selected: Items,
    Settings.crown_door_item: HelmDoorItem,
    Settings.coin_door_item: HelmDoorItem,
    # Difficulty
    Settings.damage_amount: DamageAmount,
    Settings.crown_enemy_rando: CrownEnemyRando,
    # Quality of Life
    Settings.misc_changes_selected: MiscChangesSelected,
    Settings.wrinkly_hints: WrinklyHints,
    Settings.helm_setting: HelmSetting,
    Settings.microhints_enabled: MicrohintsEnabled,
    # Cosmetics
    Settings.music_bgm: MusicCosmetics,
    Settings.music_fanfares: MusicCosmetics,
    Settings.music_events: MusicCosmetics,
    Settings.klaptrap_model: KlaptrapModel,
    Settings.dk_colors: CharacterColors,
    Settings.diddy_colors: CharacterColors,
    Settings.lanky_colors: CharacterColors,
    Settings.tiny_colors: CharacterColors,
    Settings.chunky_colors: CharacterColors,
    Settings.rambi_colors: CharacterColors,
    Settings.enguarde_colors: CharacterColors,
    Settings.colorblind_mode: ColorblindMode
}
