from enum import IntEnum

class ActivateAllBananaports(IntEnum):
    off = 0
    all = 1
    isles = 2

class BananaportRando(IntEnum):
    off = 0
    in_level = 1
    crossmap_coupled = 2
    crossmap_decoupled = 3

class BigHeadMode(IntEnum):
    off = 0
    big = 1
    small = 2
    random = 3

class CBRando(IntEnum):
    off = 0
    on = 1
    on_with_isles = 2

class CharacterColors(IntEnum):
    vanilla = 0
    randomized = 1
    custom = 2

class ColorblindMode(IntEnum):
    off = 0
    prot = 1
    deut = 2
    trit = 3

class CrownEnemyRando(IntEnum):
    off = 0
    easy = 1
    medium = 2
    hard = 3

class DamageAmount(IntEnum):
    default = 0
    double = 1
    quad = 2
    ohko = 3

class DPadDisplays(IntEnum):
    off = 0
    on = 1
    minimal = 2

class ExcludedSongs(IntEnum):
    wrinkly = 1
    transformation = 2
    pause_music = 3
    sub_areas = 4

class ExtraCutsceneSkips(IntEnum):
    off = 0
    press = 1
    auto = 2

class FasterChecksSelected(IntEnum):
    factory_toy_monster_fight = 1
    factory_piano_game = 2
    factory_diddy_rnd = 3
    factory_arcade_round_1 = 4
    factory_car_race = 5
    galleon_seal_race = 6
    galleon_mech_fish = 7
    forest_mill_conveyor = 8
    forest_owl_race = 9
    forest_rabbit_race = 10
    caves_ice_tomato_minigame = 11
    castle_minecart = 12
    castle_car_race = 13
    jetpac = 14
    arcade = 15

class FillAlgorithm(IntEnum):
    forward = 0
    assumed = 1
    random = 2
    careful_random = 3

class FreeTradeSetting(IntEnum):
    none = 0
    not_blueprints = 1
    major_collectibles = 2

class FungiTimeSetting(IntEnum):
    day = 0
    night = 1
    random = 2
    dusk = 3
    progressive = 4

class GalleonWaterSetting(IntEnum):
    lowered = 0
    raised = 1
    random = 2

class GlitchesSelected(IntEnum):
    advanced_platforming = 1
    b_locker_skips = 2
    boulder_clips = 3
    general_clips = 4
    ledge_clips = 5
    moonkicks = 6
    phase_swimming = 7
    phase_walking = 8
    skew = 9
    spawn_snags = 10
    swim_through_shores = 11
    tag_barrel_storage = 12
    troff_n_scoff_skips = 13
    moontail = 14

class HelmDoorItem(IntEnum):
    vanilla = 0
    opened = 1
    medium_random = 2
    req_gb = 3
    req_bp = 4
    req_companycoins = 5
    req_key = 6
    req_medal = 7
    req_crown = 8
    req_fairy = 9
    req_rainbowcoin = 10
    req_bean = 11
    req_pearl = 12
    easy_random = 13
    hard_random = 14

class HelmSetting(IntEnum):
    default = 0
    skip_start = 1
    skip_all = 2

class HelmBonuses(IntEnum):
    zero = 0
    one = 1
    two = 2

class HardBossesSelected(IntEnum):
    fast_mad_jack = 1
    alternative_mad_jack_kongs = 2
    pufftoss_star_rando = 3
    pufftoss_star_raised = 4
    kut_out_phase_rando = 5

class HardModeSelected(IntEnum):
    null_option_0 = 1
    null_option_1 = 2
    hard_enemies = 3
    water_is_lava = 4
    reduced_fall_damage_threshold = 5
    shuffled_jetpac_enemies = 6
    lower_max_refill_amounts = 7
    strict_helm_timer = 8
    donk_in_the_dark_world = 9
    donk_in_the_sky = 10
    angry_caves = 11

class IceTrapFrequency(IntEnum):
    rare = 0
    mild = 1
    common = 2
    frequent = 3
    pain = 4

class ItemRandoListSelected(IntEnum):
    shop = 1
    banana = 2
    toughbanana = 3
    crown = 4
    blueprint = 5
    key = 6
    medal = 7
    nintendocoin = 8
    kong = 9
    fairy = 10
    rainbowcoin = 11
    beanpearl = 12
    fakeitem = 13
    junkitem = 14
    crateitem = 15
    rarewarecoin = 16
    shopowners = 17
    hint = 18

class KasplatRandoSetting(IntEnum):
    off = 0
    vanilla_locations = 1
    location_shuffle = 2

class RandomModels(IntEnum):
    off = 0
    random = 1
    extreme = 2

class KrushaUi(IntEnum):
    no_slot = 0
    dk = 1
    diddy = 2
    lanky = 3
    tiny = 4
    chunky = 5
    random = 6

class KongModels(IntEnum):
    default = 0
    disco_chunky = 1
    krusha = 2
    krool_fight = 3
    krool_cutscene = 4
    cranky = 5
    candy = 6
    funky = 7

class LevelRandomization(IntEnum):
    vanilla = 0
    level_order = 1
    loadingzone = 2
    loadingzonesdecoupled = 3
    level_order_complex = 4

class LogicType(IntEnum):
    glitchless = 1
    glitch = 2
    nologic = 3

class MicrohintsEnabled(IntEnum):
    off = 0
    base = 1
    all = 2

class MinigameBarrels(IntEnum):
    normal = 0
    skip = 1
    random = 2
    selected = 3

class MinigamesListSelected(IntEnum):
    batty_barrel_bandit = 1
    big_bug_bash = 2
    busy_barrel_barrage = 3
    mad_maze_maul = 4
    minecart_mayhem = 5
    beaver_bother = 6
    teetering_turtle_trouble = 7
    stealthy_snoop = 8
    stash_snatch = 9
    splish_splash_salvage = 10
    speedy_swing_sortie = 11
    krazy_kong_klamour = 12
    searchlight_seek = 13
    kremling_kosh = 14
    peril_path_panic = 15
    helm_minigames = 16
    arenas = 17
    training_minigames = 18

class MiscChangesSelected(IntEnum):
    auto_dance_skip = 1
    fast_boot = 2
    calm_caves = 3
    animal_buddies_grab_items = 4
    reduced_lag = 5
    remove_extraneous_cutscenes = 6
    hint_textbox_hold = 7
    remove_wrinkly_puzzles = 8
    fast_picture_taking = 9
    hud_hotkey = 10
    ammo_swap = 11
    homing_balloons = 12
    fast_transform_animation = 13
    troff_n_scoff_audio_indicator = 14
    lowered_aztec_lobby_bonus = 15
    quicker_galleon_star = 16
    vanilla_bug_fixes = 17
    save_k_rool_progress = 18
    small_bananas_always_visible = 19
    fast_hints = 20
    brighten_mad_maze_maul_enemies = 21
    raise_fungi_dirt_patch = 22
    global_instrument = 23
    fast_pause_transitions = 24
    cannon_game_better_control = 25
    better_fairy_camera = 26
    remove_enemy_cabin_timer = 27
    remove_galleon_ship_timers = 28
    japes_bridge_permanently_extended = 29

class MoveRando(IntEnum):
    off = 0
    on = 1
    cross_purchase = 2
    start_with = 3
    item_shuffle = 4

class MusicFilters(IntEnum):
    length = 1
    location = 2

class PuzzleRando(IntEnum):
    off = 0
    easy = 1
    medium = 2
    hard = 3
    chaos = 4

class RandomPrices(IntEnum):
    vanilla = 0
    free = 1
    low = 2
    medium = 3
    high = 4
    extreme = 5

class RemovedBarriersSelected(IntEnum):
    japes_coconut_gates = 1
    japes_shellhive_gate = 2
    aztec_tunnel_door = 3
    aztec_5dtemple_switches = 4
    aztec_llama_switches = 5
    factory_production_room = 6
    factory_testing_gate = 7
    galleon_lighthouse_gate = 8
    galleon_shipyard_area_gate = 9
    castle_crypt_doors = 10
    galleon_seasick_ship = 11
    forest_green_tunnel = 12
    forest_yellow_tunnel = 13
    caves_igloo_pads = 14
    caves_ice_walls = 15
    galleon_treasure_room = 16
    aztec_tiny_temple_ice = 17

class ShockwaveStatus(IntEnum):
    vanilla = 0
    shuffled = 1
    shuffled_decoupled = 2
    start_with = 3

class ShuffleLoadingZones(IntEnum):
    none = 0
    levels = 1
    all = 2

class ShufflePortLocations(IntEnum):
    off = 0
    vanilla_only = 1
    half_vanilla = 2
    on = 3

class SlamRequirement(IntEnum):
    green = 0
    blue = 1
    red = 2
    random = 3

class SoundType(IntEnum):
    stereo = 0
    mono = 1
    surround = 2

class SwitchsanityLevel(IntEnum):
    off = 0
    helm_access = 1
    all = 2

class TrainingBarrels(IntEnum):
    normal = 0
    shuffled = 1

class WinCondition(IntEnum):
    beat_krool = 0
    get_key8 = 1
    all_fairies = 2
    all_blueprints = 3
    all_medals = 4
    poke_snap = 5
    all_keys = 6

class WinConditionComplex(IntEnum):
    beat_krool = 0
    get_key8 = 1
    krem_kapture = 2
    req_gb = 3
    req_bp = 4
    req_companycoins = 5
    req_key = 6
    req_medal = 7
    req_crown = 8
    req_fairy = 9
    req_rainbowcoin = 10
    req_bean = 11
    req_pearl = 12
    easy_random = 13
    medium_random = 14
    hard_random = 15
    dk_rap_items = 16

class WrinklyHints(IntEnum):
    off = 0
    standard = 1
    cryptic = 2
    fixed_racing = 3
    item_hinting = 4
    item_hinting_advanced = 5

class SpoilerHints(IntEnum):
    off = 0
    vial_colors = 1
    points = 2

class SettingsStringEnum(IntEnum):
    activate_all_bananaports = 1
    alter_switch_allocation = 2
    auto_keys = 3
    bananaport_rando = 4
    blocker_0 = 5
    blocker_1 = 6
    blocker_2 = 7
    blocker_3 = 8
    blocker_4 = 9
    blocker_5 = 10
    blocker_6 = 11
    blocker_7 = 12
    blocker_text = 13
    bonus_barrel_auto_complete = 14
    bonus_barrel_rando = 15
    boss_kong_rando = 16
    boss_location_rando = 17
    cb_rando = 18
    coin_door_item = 19
    coin_door_item_count = 20
    crown_door_item = 21
    crown_door_item_count = 22
    crown_enemy_rando = 23
    crown_placement_rando = 24
    damage_amount = 25
    disable_tag_barrels = 26
    enable_shop_hints = 27
    enable_tag_anywhere = 28
    enemies_selected = 29
    enemy_rando = 30
    enemy_speed_rando = 31
    faster_checks_enabled = 32
    fast_start_beginning_of_game = 33
    fast_warps = 34
    fps_display = 35
    free_trade_setting = 36
    generate_spoilerlog = 37
    glitches_selected = 38
    hard_blockers = 39
    hard_bosses = 40
    hard_enemies = 41
    hard_level_progression = 42
    hard_shooting = 43
    hard_troff_n_scoff = 44
    helm_hurry = 45
    helm_phase_count = 46
    helm_phase_order_rando = 47
    helm_random = 48
    helm_setting = 49
    helmhurry_list_banana_medal = 50
    helmhurry_list_battle_crown = 51
    helmhurry_list_bean = 52
    helmhurry_list_blueprint = 53
    helmhurry_list_boss_key = 54
    helmhurry_list_colored_bananas = 55
    helmhurry_list_company_coins = 56
    helmhurry_list_fairies = 57
    helmhurry_list_golden_banana = 58
    helmhurry_list_ice_traps = 59
    helmhurry_list_kongs = 60
    helmhurry_list_move = 61
    helmhurry_list_pearl = 62
    helmhurry_list_rainbow_coin = 63
    helmhurry_list_starting_time = 64
    high_req = 65
    item_rando_list_selected = 66
    item_reward_previews = 67
    kasplat_rando_setting = 68
    key_8_helm = 69
    keys_random = 70
    kong_rando = 71
    krool_access = 72
    krool_key_count = 73
    krool_phase_count = 74
    krool_phase_order_rando = 75
    krool_random = 76
    krusha_ui = 77
    level_randomization = 78
    logic_type = 79
    maximize_helm_blocker = 80
    medal_cb_req = 81
    medal_requirement = 82
    microhints_enabled = 83
    minigames_list_selected = 84
    misc_changes_selected = 85
    move_rando = 86
    no_healing = 87
    no_melons = 88
    open_levels = 89
    open_lobbies = 90
    perma_death = 91
    portal_numbers = 92
    puzzle_rando = 93
    quality_of_life = 94
    random_fairies = 95
    random_medal_requirement = 96
    random_patches = 97
    random_prices = 98
    random_starting_region = 99
    randomize_blocker_required_amounts = 100
    randomize_cb_required_amounts = 101
    randomize_pickups = 102
    rareware_gb_fairies = 103
    select_keys = 104
    shockwave_status = 105
    shop_indicator = 106
    shorten_boss = 107
    shuffle_items = 108
    shuffle_shops = 109
    smaller_shops = 110
    starting_keys_list_selected = 111
    starting_kongs_count = 112
    starting_random = 113
    tns_location_rando = 114
    training_barrels = 115
    troff_0 = 116
    troff_1 = 117
    troff_2 = 118
    troff_3 = 119
    troff_4 = 120
    troff_5 = 121
    troff_6 = 122
    troff_text = 123
    warp_level_list_selected = 124
    warp_to_isles = 125
    win_condition = 126
    wrinkly_available = 127
    wrinkly_hints = 128
    wrinkly_location_rando = 129
    coin_rando = 130
    vanilla_door_rando = 131
    starting_moves_count = 132
    enable_plandomizer = 133
    hard_mode_selected = 134
    hard_mode = 135
    more_cutscene_skips = 136
    spoiler_hints = 137
    spoiler_include_woth_count = 138
    points_list_kongs = 139
    points_list_keys = 140
    points_list_guns = 141
    points_list_instruments = 142
    points_list_training_moves = 143
    points_list_important_shared = 144
    points_list_pad_moves = 145
    points_list_barrel_moves = 146
    points_list_active_moves = 147
    points_list_bean = 148
    random_crates = 149
    choose_starting_moves = 150
    starting_move_list_selected = 151
    start_with_slam = 152
    spoiler_include_level_order = 153
    enable_progressive_hints = 154
    progressive_hint_text = 155
    random_starting_move_list_selected = 156
    enemy_drop_rando = 157
    dim_solved_hints = 158
    starting_kong = 159
    switchsanity = 160
    fungi_time = 161
    galleon_water = 162
    remove_barriers_enabled = 163
    remove_barriers_selected = 164
    faster_checks_selected = 165
    k_rool_vanilla_requirement = 166
    disable_hard_minigames = 167
    chaos_blockers = 168
    mermaid_gb_pearls = 169
    kong_model_dk = 170
    kong_model_diddy = 171
    kong_model_lanky = 172
    kong_model_tiny = 173
    kong_model_chunky = 174
    helm_room_bonus_count = 175
    dk_portal_location_rando = 176
    serious_hints = 177
    cannons_require_blast = 178
    chunky_phase_slam_req = 179
    shuffle_helm_location = 180
    points_list_fairy_moves = 181
    points_list_shopkeepers = 182
    chaos_ratio = 183
    krool_in_boss_pool = 184
    enemy_kill_crown_timer = 185
    hard_bosses_selected = 186
    ice_trap_frequency = 187
    ice_traps_damage = 188
    puzzle_rando_difficulty = 189
    win_condition_item = 190
    win_condition_count = 191
    bananaport_placement_rando = 192
    troff_7 = 193

class SettingsStringDataType(IntEnum):
    bool = 0
    int4 = 1
    int8 = 2
    int16 = 3
    var_int = 4
    str = 5
    list = 6
    u16 = 7
