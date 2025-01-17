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
    off = 1
    on = 2
    on_with_isles = 3

class CharacterColors(IntEnum):
    vanilla = 1
    randomized = 2
    custom = 3

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

class CrownEnemyDifficulty(IntEnum):
    vanilla = 0
    easy = 1
    medium = 2
    hard = 3
    progressive = 4

class DamageAmount(IntEnum):
    default = 0
    double = 1
    quad = 2
    ohko = 3

class DPadDisplays(IntEnum):
    off = 0
    on = 1
    minimal = 2

class DKPortalRando(IntEnum):
    off = 0
    main_only = 1
    on = 2

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
    forward = 1
    assumed = 2
    random = 3
    careful_random = 4

class FreeTradeSetting(IntEnum):
    none = 0
    not_blueprints = 1
    major_collectibles = 2

class FungiTimeSetting(IntEnum):
    day = 1
    night = 2
    random = 3
    dusk = 4
    progressive = 5

class GalleonWaterSetting(IntEnum):
    lowered = 1
    raised = 2
    random = 3

class ClimbingStatus(IntEnum):
    normal = 0
    shuffled = 1

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
    phasefall = 15

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
    k_rool_toes_rando = 6
    beta_lanky_phase = 7

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
    shockwave = 19

class KasplatRandoSetting(IntEnum):
    off = 0
    vanilla_locations = 1
    location_shuffle = 2

class RandomModels(IntEnum):
    off = 1
    random = 2
    extreme = 3

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
    normal = 1
    skip = 2
    random = 3
    selected = 4

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

class ProgressiveHintItem(IntEnum):
    off = 0
    req_gb = 1
    req_bp = 2
    req_key = 3
    req_medal = 4
    req_crown = 5
    req_fairy = 6
    req_rainbowcoin = 7
    req_bean = 8
    req_pearl = 9
    req_cb = 10

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
    off = 1
    vanilla_only = 2
    half_vanilla = 3
    on = 4

class SlamRequirement(IntEnum):
    green = 1
    blue = 2
    red = 3
    random = 4

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
    hard_shooting = 41
    hard_troff_n_scoff = 42
    helm_hurry = 43
    helm_phase_count = 44
    helm_phase_order_rando = 45
    helm_random = 46
    helm_setting = 47
    helmhurry_list_banana_medal = 48
    helmhurry_list_battle_crown = 49
    helmhurry_list_bean = 50
    helmhurry_list_blueprint = 51
    helmhurry_list_boss_key = 52
    helmhurry_list_colored_bananas = 53
    helmhurry_list_company_coins = 54
    helmhurry_list_fairies = 55
    helmhurry_list_golden_banana = 56
    helmhurry_list_ice_traps = 57
    helmhurry_list_kongs = 58
    helmhurry_list_move = 59
    helmhurry_list_pearl = 60
    helmhurry_list_rainbow_coin = 61
    helmhurry_list_starting_time = 62
    item_rando_list_selected = 63
    item_reward_previews = 64
    kasplat_rando_setting = 65
    key_8_helm = 66
    keys_random = 67
    kong_rando = 68
    krool_access = 69
    krool_key_count = 70
    krool_phase_count = 71
    krool_phase_order_rando = 72
    krool_random = 73
    level_randomization = 74
    logic_type = 75
    maximize_helm_blocker = 76
    medal_cb_req = 77
    medal_requirement = 78
    microhints_enabled = 79
    minigames_list_selected = 80
    misc_changes_selected = 81
    move_rando = 82
    no_healing = 83
    no_melons = 84
    open_lobbies = 85
    perma_death = 86
    portal_numbers = 87
    quality_of_life = 88
    random_fairies = 89
    random_medal_requirement = 90
    random_patches = 91
    random_prices = 92
    random_starting_region = 93
    randomize_blocker_required_amounts = 94
    randomize_cb_required_amounts = 95
    randomize_pickups = 96
    rareware_gb_fairies = 97
    select_keys = 98
    shockwave_status = 99
    shop_indicator = 100
    shorten_boss = 101
    shuffle_items = 102
    shuffle_shops = 103
    smaller_shops = 104
    starting_keys_list_selected = 105
    starting_kongs_count = 106
    starting_random = 107
    tns_location_rando = 108
    training_barrels = 109
    troff_0 = 110
    troff_1 = 111
    troff_2 = 112
    troff_3 = 113
    troff_4 = 114
    troff_5 = 115
    troff_6 = 116
    troff_text = 117
    warp_level_list_selected = 118
    warp_to_isles = 119
    wrinkly_available = 120
    wrinkly_hints = 121
    wrinkly_location_rando = 122
    coin_rando = 123
    vanilla_door_rando = 124
    starting_moves_count = 125
    enable_plandomizer = 126
    hard_mode_selected = 127
    hard_mode = 128
    more_cutscene_skips = 129
    spoiler_hints = 130
    spoiler_include_woth_count = 131
    points_list_kongs = 132
    points_list_keys = 133
    points_list_guns = 134
    points_list_instruments = 135
    points_list_training_moves = 136
    points_list_important_shared = 137
    points_list_pad_moves = 138
    points_list_barrel_moves = 139
    points_list_active_moves = 140
    points_list_bean = 141
    random_crates = 142
    starting_move_list_selected = 143
    start_with_slam = 144
    spoiler_include_level_order = 145
    enable_progressive_hints = 146
    progressive_hint_text = 147
    random_starting_move_list_selected = 148
    enemy_drop_rando = 149
    dim_solved_hints = 150
    starting_kong = 151
    switchsanity = 152
    fungi_time = 153
    galleon_water = 154
    remove_barriers_enabled = 155
    remove_barriers_selected = 156
    faster_checks_selected = 157
    k_rool_vanilla_requirement = 158
    disable_hard_minigames = 159
    chaos_blockers = 160
    mermaid_gb_pearls = 161
    kong_model_dk = 162
    kong_model_diddy = 163
    kong_model_lanky = 164
    kong_model_tiny = 165
    kong_model_chunky = 166
    helm_room_bonus_count = 167
    dk_portal_location_rando = 168
    serious_hints = 169
    cannons_require_blast = 170
    chunky_phase_slam_req = 171
    shuffle_helm_location = 172
    points_list_fairy_moves = 173
    points_list_shopkeepers = 174
    chaos_ratio = 175
    krool_in_boss_pool = 176
    enemy_kill_crown_timer = 177
    hard_bosses_selected = 178
    ice_trap_frequency = 179
    ice_traps_damage = 180
    puzzle_rando_difficulty = 181
    win_condition_item = 182
    win_condition_count = 183
    bananaport_placement_rando = 184
    troff_7 = 185
    has_password = 186
    randomize_enemy_sizes = 187
    starting_moves_list_1 = 188
    starting_moves_list_count_1 = 189
    starting_moves_list_2 = 190
    starting_moves_list_count_2 = 191
    starting_moves_list_3 = 192
    starting_moves_list_count_3 = 193
    starting_moves_list_4 = 194
    starting_moves_list_count_4 = 195
    starting_moves_list_5 = 196
    starting_moves_list_count_5 = 197
    progressive_hint_item = 198
    mirror_mode = 199
    progressive_hint_count = 200
    cb_rando_enabled = 201
    cb_rando_list_selected = 202
    crown_enemy_difficulty = 203
    dk_portal_location_rando_v2 = 204
    dos_door_rando = 205

class SettingsStringDataType(IntEnum):
    bool = 1
    int4 = 2
    int8 = 3
    int16 = 4
    var_int = 5
    str = 6
    list = 7
    u16 = 8

SettingsMap: dict = {
    "activate_all_bananaports": ActivateAllBananaports,
    "bananaport_placement_rando": ShufflePortLocations,
    "bananaport_rando": BananaportRando,
    "big_head_mode": BigHeadMode,
    "bonus_barrels": MinigameBarrels,
    "cb_rando": CBRando,
    "chunky_colors": CharacterColors,
    "coin_door_item": HelmDoorItem,
    "colorblind_mode": ColorblindMode,
    "crown_door_item": HelmDoorItem,
    "crown_enemy_rando": CrownEnemyRando,
    "crown_enemy_difficulty": CrownEnemyDifficulty,
    "damage_amount": DamageAmount,
    "dk_portal_location_rando_v2": DKPortalRando,
    "diddy_colors": CharacterColors,
    "dk_colors": CharacterColors,
    "dpad_display": DPadDisplays,
    "enemies_selected": Enemies,
    "enguarde_colors": CharacterColors,
    "excluded_songs_selected": ExcludedSongs,
    "free_trade_setting": FreeTradeSetting,
    "fungi_time": FungiTimeSetting,
    "galleon_water": GalleonWaterSetting,
    "gb_colors": CharacterColors,
    "glitches_selected": GlitchesSelected,
    "hard_bosses_selected": HardBossesSelected,
    "hard_mode_selected": HardModeSelected,
    "helm_barrels": MinigameBarrels,
    "helm_room_bonus_count": HelmBonuses,
    "helm_setting": HelmSetting,
    "ice_trap_frequency": IceTrapFrequency,
    "item_rando_list_selected": ItemRandoListSelected,
    "kasplat_rando_setting": KasplatRandoSetting,
    "krusha_ui": KrushaUi,
    "lanky_colors": CharacterColors,
    "level_randomization": LevelRandomization,
    "logic_type": LogicType,
    "microhints_enabled": MicrohintsEnabled,
    "minigames_list_selected": MinigamesListSelected,
    "cb_rando_list_selected": Levels,
    "misc_changes_selected": MiscChangesSelected,
    "more_cutscene_skips": ExtraCutsceneSkips,
    "move_rando": MoveRando,
    "music_filtering_selected": MusicFilters,
    "rambi_colors": CharacterColors,
    "random_models": RandomModels,
    "random_prices": RandomPrices,
    "shockwave_status": ShockwaveStatus,
    "shuffle_loading_zones": ShuffleLoadingZones,
    "sound_type": SoundType,
    "starting_keys_list_selected": Items,
    "starting_move_list_selected": Items,
    "switchsanity": SwitchsanityLevel,
    "random_starting_move_list_selected": Items,
    "tiny_colors": CharacterColors,
    "training_barrels": TrainingBarrels,
    "warp_level_list_selected": Maps,
    "win_condition": WinCondition,
    "win_condition_item": WinConditionComplex,
    "wrinkly_hints": WrinklyHints,
    "spoiler_hints": SpoilerHints,
    "starting_kong": Kongs,
    "remove_barriers_selected": RemovedBarriersSelected,
    "faster_checks_selected": FasterChecksSelected,
    "kong_model_dk": KongModels,
    "kong_model_diddy": KongModels,
    "kong_model_lanky": KongModels,
    "kong_model_tiny": KongModels,
    "kong_model_chunky": KongModels,
    "chunky_phase_slam_req": SlamRequirement,
    "puzzle_rando_difficulty": PuzzleRando,
    "progressive_hint_item": ProgressiveHintItem,
    "starting_moves_list_1": Items,
    "starting_moves_list_2": Items,
    "starting_moves_list_3": Items,
    "starting_moves_list_4": Items,
    "starting_moves_list_5": Items,
}

SettingsStringTypeMap: dict = {
    SettingsStringEnum.activate_all_bananaports: ActivateAllBananaports,
    SettingsStringEnum.alter_switch_allocation: SettingsStringDataType.bool,
    SettingsStringEnum.auto_keys: SettingsStringDataType.bool,
    SettingsStringEnum.bananaport_placement_rando: ShufflePortLocations,
    SettingsStringEnum.bananaport_rando: BananaportRando,
    SettingsStringEnum.blocker_0: SettingsStringDataType.var_int,
    SettingsStringEnum.blocker_1: SettingsStringDataType.var_int,
    SettingsStringEnum.blocker_2: SettingsStringDataType.var_int,
    SettingsStringEnum.blocker_3: SettingsStringDataType.var_int,
    SettingsStringEnum.blocker_4: SettingsStringDataType.var_int,
    SettingsStringEnum.blocker_5: SettingsStringDataType.var_int,
    SettingsStringEnum.blocker_6: SettingsStringDataType.var_int,
    SettingsStringEnum.blocker_7: SettingsStringDataType.var_int,
    SettingsStringEnum.blocker_text: SettingsStringDataType.var_int,
    SettingsStringEnum.bonus_barrel_auto_complete: SettingsStringDataType.bool,
    SettingsStringEnum.bonus_barrel_rando: SettingsStringDataType.bool,
    SettingsStringEnum.boss_kong_rando: SettingsStringDataType.bool,
    SettingsStringEnum.boss_location_rando: SettingsStringDataType.bool,
    SettingsStringEnum.cb_rando: CBRando,
    SettingsStringEnum.coin_door_item: HelmDoorItem,
    SettingsStringEnum.coin_door_item_count: SettingsStringDataType.var_int,
    SettingsStringEnum.random_crates: SettingsStringDataType.bool,
    SettingsStringEnum.crown_placement_rando: SettingsStringDataType.bool,
    SettingsStringEnum.crown_door_item: HelmDoorItem,
    SettingsStringEnum.crown_door_item_count: SettingsStringDataType.var_int,
    SettingsStringEnum.crown_enemy_rando: CrownEnemyRando,
    SettingsStringEnum.crown_enemy_difficulty: CrownEnemyDifficulty,
    SettingsStringEnum.coin_rando: SettingsStringDataType.bool,
    SettingsStringEnum.damage_amount: DamageAmount,
    SettingsStringEnum.disable_tag_barrels: SettingsStringDataType.bool,
    SettingsStringEnum.dk_portal_location_rando: SettingsStringDataType.bool,
    SettingsStringEnum.dk_portal_location_rando_v2: DKPortalRando,
    SettingsStringEnum.enable_plandomizer: SettingsStringDataType.bool,
    SettingsStringEnum.enable_shop_hints: SettingsStringDataType.bool,
    SettingsStringEnum.enable_tag_anywhere: SettingsStringDataType.bool,
    SettingsStringEnum.enemies_selected: SettingsStringDataType.list,
    SettingsStringEnum.enemy_rando: SettingsStringDataType.bool,
    SettingsStringEnum.enemy_speed_rando: SettingsStringDataType.bool,
    SettingsStringEnum.faster_checks_enabled: SettingsStringDataType.bool,
    SettingsStringEnum.fast_start_beginning_of_game: SettingsStringDataType.bool,
    SettingsStringEnum.fast_warps: SettingsStringDataType.bool,
    SettingsStringEnum.fps_display: SettingsStringDataType.bool,
    SettingsStringEnum.free_trade_setting: FreeTradeSetting,
    SettingsStringEnum.generate_spoilerlog: SettingsStringDataType.bool,
    SettingsStringEnum.glitches_selected: SettingsStringDataType.list,
    SettingsStringEnum.hard_mode: SettingsStringDataType.bool,
    SettingsStringEnum.hard_mode_selected: SettingsStringDataType.list,
    SettingsStringEnum.hard_blockers: SettingsStringDataType.bool,
    SettingsStringEnum.hard_bosses: SettingsStringDataType.bool,
    SettingsStringEnum.hard_bosses_selected: SettingsStringDataType.list,
    SettingsStringEnum.hard_shooting: SettingsStringDataType.bool,
    SettingsStringEnum.hard_troff_n_scoff: SettingsStringDataType.bool,
    SettingsStringEnum.helm_hurry: SettingsStringDataType.bool,
    SettingsStringEnum.helm_phase_count: SettingsStringDataType.var_int,
    SettingsStringEnum.helm_phase_order_rando: SettingsStringDataType.bool,
    SettingsStringEnum.helm_random: SettingsStringDataType.bool,
    SettingsStringEnum.helm_room_bonus_count: HelmBonuses,
    SettingsStringEnum.helm_setting: HelmSetting,
    SettingsStringEnum.helmhurry_list_banana_medal: SettingsStringDataType.int16,
    SettingsStringEnum.helmhurry_list_battle_crown: SettingsStringDataType.int16,
    SettingsStringEnum.helmhurry_list_bean: SettingsStringDataType.int16,
    SettingsStringEnum.helmhurry_list_blueprint: SettingsStringDataType.int16,
    SettingsStringEnum.helmhurry_list_boss_key: SettingsStringDataType.int16,
    SettingsStringEnum.helmhurry_list_colored_bananas: SettingsStringDataType.int16,
    SettingsStringEnum.helmhurry_list_company_coins: SettingsStringDataType.int16,
    SettingsStringEnum.helmhurry_list_fairies: SettingsStringDataType.int16,
    SettingsStringEnum.helmhurry_list_golden_banana: SettingsStringDataType.int16,
    SettingsStringEnum.helmhurry_list_ice_traps: SettingsStringDataType.int16,
    SettingsStringEnum.helmhurry_list_kongs: SettingsStringDataType.int16,
    SettingsStringEnum.helmhurry_list_move: SettingsStringDataType.int16,
    SettingsStringEnum.helmhurry_list_pearl: SettingsStringDataType.int16,
    SettingsStringEnum.helmhurry_list_rainbow_coin: SettingsStringDataType.int16,
    SettingsStringEnum.helmhurry_list_starting_time: SettingsStringDataType.u16,
    SettingsStringEnum.item_rando_list_selected: SettingsStringDataType.list,
    SettingsStringEnum.item_reward_previews: SettingsStringDataType.bool,
    SettingsStringEnum.kasplat_rando_setting: KasplatRandoSetting,
    SettingsStringEnum.key_8_helm: SettingsStringDataType.bool,
    SettingsStringEnum.keys_random: SettingsStringDataType.bool,
    SettingsStringEnum.kong_model_dk: KongModels,
    SettingsStringEnum.kong_model_diddy: KongModels,
    SettingsStringEnum.kong_model_lanky: KongModels,
    SettingsStringEnum.kong_model_tiny: KongModels,
    SettingsStringEnum.kong_model_chunky: KongModels,
    SettingsStringEnum.kong_rando: SettingsStringDataType.bool,
    SettingsStringEnum.krool_access: SettingsStringDataType.bool,
    SettingsStringEnum.krool_key_count: SettingsStringDataType.var_int,
    SettingsStringEnum.krool_phase_count: SettingsStringDataType.var_int,
    SettingsStringEnum.krool_phase_order_rando: SettingsStringDataType.bool,
    SettingsStringEnum.krool_random: SettingsStringDataType.bool,
    SettingsStringEnum.level_randomization: LevelRandomization,
    SettingsStringEnum.logic_type: LogicType,
    SettingsStringEnum.maximize_helm_blocker: SettingsStringDataType.bool,
    SettingsStringEnum.medal_cb_req: SettingsStringDataType.var_int,
    SettingsStringEnum.medal_requirement: SettingsStringDataType.var_int,
    SettingsStringEnum.microhints_enabled: MicrohintsEnabled,
    SettingsStringEnum.minigames_list_selected: SettingsStringDataType.list,
    SettingsStringEnum.cb_rando_enabled: SettingsStringDataType.bool,
    SettingsStringEnum.cb_rando_list_selected: SettingsStringDataType.list,
    SettingsStringEnum.misc_changes_selected: SettingsStringDataType.list,
    SettingsStringEnum.more_cutscene_skips: ExtraCutsceneSkips,
    SettingsStringEnum.move_rando: MoveRando,
    SettingsStringEnum.no_healing: SettingsStringDataType.bool,
    SettingsStringEnum.no_melons: SettingsStringDataType.bool,
    SettingsStringEnum.open_lobbies: SettingsStringDataType.bool,
    SettingsStringEnum.perma_death: SettingsStringDataType.bool,
    SettingsStringEnum.portal_numbers: SettingsStringDataType.bool,
    SettingsStringEnum.quality_of_life: SettingsStringDataType.bool,
    SettingsStringEnum.random_fairies: SettingsStringDataType.bool,
    SettingsStringEnum.random_medal_requirement: SettingsStringDataType.bool,
    SettingsStringEnum.random_patches: SettingsStringDataType.bool,
    SettingsStringEnum.random_prices: RandomPrices,
    SettingsStringEnum.random_starting_region: SettingsStringDataType.bool,
    SettingsStringEnum.randomize_blocker_required_amounts: SettingsStringDataType.bool,
    SettingsStringEnum.randomize_cb_required_amounts: SettingsStringDataType.bool,
    SettingsStringEnum.randomize_pickups: SettingsStringDataType.bool,
    SettingsStringEnum.rareware_gb_fairies: SettingsStringDataType.var_int,
    SettingsStringEnum.select_keys: SettingsStringDataType.bool,
    SettingsStringEnum.shockwave_status: ShockwaveStatus,
    SettingsStringEnum.shop_indicator: SettingsStringDataType.bool,
    SettingsStringEnum.shorten_boss: SettingsStringDataType.bool,
    SettingsStringEnum.shuffle_items: SettingsStringDataType.bool,
    SettingsStringEnum.shuffle_shops: SettingsStringDataType.bool,
    SettingsStringEnum.smaller_shops: SettingsStringDataType.bool,
    SettingsStringEnum.starting_keys_list_selected: SettingsStringDataType.list,
    SettingsStringEnum.starting_kongs_count: SettingsStringDataType.var_int,
    SettingsStringEnum.starting_moves_count: SettingsStringDataType.var_int,
    SettingsStringEnum.starting_random: SettingsStringDataType.bool,
    SettingsStringEnum.tns_location_rando: SettingsStringDataType.bool,
    SettingsStringEnum.training_barrels: TrainingBarrels,
    SettingsStringEnum.troff_0: SettingsStringDataType.var_int,
    SettingsStringEnum.troff_1: SettingsStringDataType.var_int,
    SettingsStringEnum.troff_2: SettingsStringDataType.var_int,
    SettingsStringEnum.troff_3: SettingsStringDataType.var_int,
    SettingsStringEnum.troff_4: SettingsStringDataType.var_int,
    SettingsStringEnum.troff_5: SettingsStringDataType.var_int,
    SettingsStringEnum.troff_6: SettingsStringDataType.var_int,
    SettingsStringEnum.troff_7: SettingsStringDataType.var_int,
    SettingsStringEnum.troff_text: SettingsStringDataType.var_int,
    SettingsStringEnum.vanilla_door_rando: SettingsStringDataType.bool,
    SettingsStringEnum.warp_level_list_selected: SettingsStringDataType.list,
    SettingsStringEnum.warp_to_isles: SettingsStringDataType.bool,
    SettingsStringEnum.win_condition_item: WinConditionComplex,
    SettingsStringEnum.win_condition_count: SettingsStringDataType.var_int,
    SettingsStringEnum.wrinkly_available: SettingsStringDataType.bool,
    SettingsStringEnum.wrinkly_hints: WrinklyHints,
    SettingsStringEnum.wrinkly_location_rando: SettingsStringDataType.bool,
    SettingsStringEnum.spoiler_hints: SpoilerHints,
    SettingsStringEnum.spoiler_include_woth_count: SettingsStringDataType.bool,
    SettingsStringEnum.points_list_kongs: SettingsStringDataType.int16,
    SettingsStringEnum.points_list_keys: SettingsStringDataType.int16,
    SettingsStringEnum.points_list_guns: SettingsStringDataType.int16,
    SettingsStringEnum.points_list_instruments: SettingsStringDataType.int16,
    SettingsStringEnum.points_list_training_moves: SettingsStringDataType.int16,
    SettingsStringEnum.points_list_important_shared: SettingsStringDataType.int16,
    SettingsStringEnum.points_list_pad_moves: SettingsStringDataType.int16,
    SettingsStringEnum.points_list_barrel_moves: SettingsStringDataType.int16,
    SettingsStringEnum.points_list_active_moves: SettingsStringDataType.int16,
    SettingsStringEnum.points_list_bean: SettingsStringDataType.int16,
    SettingsStringEnum.starting_move_list_selected: SettingsStringDataType.list,
    SettingsStringEnum.start_with_slam: SettingsStringDataType.bool,
    SettingsStringEnum.spoiler_include_level_order: SettingsStringDataType.bool,
    SettingsStringEnum.enable_progressive_hints: SettingsStringDataType.bool,
    SettingsStringEnum.progressive_hint_text: SettingsStringDataType.var_int,
    SettingsStringEnum.progressive_hint_count: SettingsStringDataType.var_int,
    SettingsStringEnum.random_starting_move_list_selected: SettingsStringDataType.list,
    SettingsStringEnum.enemy_drop_rando: SettingsStringDataType.bool,
    SettingsStringEnum.dim_solved_hints: SettingsStringDataType.bool,
    SettingsStringEnum.starting_kong: Kongs,
    SettingsStringEnum.switchsanity: SwitchsanityLevel,
    SettingsStringEnum.fungi_time: FungiTimeSetting,
    SettingsStringEnum.galleon_water: GalleonWaterSetting,
    SettingsStringEnum.remove_barriers_enabled: SettingsStringDataType.bool,
    SettingsStringEnum.remove_barriers_selected: SettingsStringDataType.list,
    SettingsStringEnum.faster_checks_selected: SettingsStringDataType.list,
    SettingsStringEnum.k_rool_vanilla_requirement: SettingsStringDataType.bool,
    SettingsStringEnum.disable_hard_minigames: SettingsStringDataType.bool,
    SettingsStringEnum.serious_hints: SettingsStringDataType.bool,
    SettingsStringEnum.cannons_require_blast: SettingsStringDataType.bool,
    SettingsStringEnum.chaos_blockers: SettingsStringDataType.bool,
    SettingsStringEnum.mermaid_gb_pearls: SettingsStringDataType.var_int,
    SettingsStringEnum.chunky_phase_slam_req: SlamRequirement,
    SettingsStringEnum.shuffle_helm_location: SettingsStringDataType.bool,
    SettingsStringEnum.points_list_fairy_moves: SettingsStringDataType.int16,
    SettingsStringEnum.points_list_shopkeepers: SettingsStringDataType.int16,
    SettingsStringEnum.chaos_ratio: SettingsStringDataType.int16,
    SettingsStringEnum.krool_in_boss_pool: SettingsStringDataType.bool,
    SettingsStringEnum.enemy_kill_crown_timer: SettingsStringDataType.bool,
    SettingsStringEnum.ice_trap_frequency: IceTrapFrequency,
    SettingsStringEnum.ice_traps_damage: SettingsStringDataType.bool,
    SettingsStringEnum.mirror_mode: SettingsStringDataType.bool,
    SettingsStringEnum.puzzle_rando_difficulty: PuzzleRando,
    SettingsStringEnum.has_password: SettingsStringDataType.bool,
    SettingsStringEnum.randomize_enemy_sizes: SettingsStringDataType.bool,
    SettingsStringEnum.progressive_hint_item: ProgressiveHintItem,
    SettingsStringEnum.starting_moves_list_1: SettingsStringDataType.list,
    SettingsStringEnum.starting_moves_list_count_1: SettingsStringDataType.int16,
    SettingsStringEnum.starting_moves_list_2: SettingsStringDataType.list,
    SettingsStringEnum.starting_moves_list_count_2: SettingsStringDataType.int16,
    SettingsStringEnum.starting_moves_list_3: SettingsStringDataType.list,
    SettingsStringEnum.starting_moves_list_count_3: SettingsStringDataType.int16,
    SettingsStringEnum.starting_moves_list_4: SettingsStringDataType.list,
    SettingsStringEnum.starting_moves_list_count_4: SettingsStringDataType.int16,
    SettingsStringEnum.starting_moves_list_5: SettingsStringDataType.list,
    SettingsStringEnum.starting_moves_list_count_5: SettingsStringDataType.int16,
    SettingsStringEnum.dos_door_rando: SettingsStringDataType.bool,
}

SettingsStringListTypeMap: dict = {
    SettingsStringEnum.enemies_selected: Enemies,
    SettingsStringEnum.glitches_selected: GlitchesSelected,
    SettingsStringEnum.item_rando_list_selected: ItemRandoListSelected,
    SettingsStringEnum.minigames_list_selected: MinigamesListSelected,
    SettingsStringEnum.cb_rando_list_selected: Levels,
    SettingsStringEnum.misc_changes_selected: MiscChangesSelected,
    SettingsStringEnum.starting_keys_list_selected: Items,
    SettingsStringEnum.warp_level_list_selected: Maps,
    SettingsStringEnum.hard_mode_selected: HardModeSelected,
    SettingsStringEnum.starting_move_list_selected: Items,
    SettingsStringEnum.random_starting_move_list_selected: Items,
    SettingsStringEnum.remove_barriers_selected: RemovedBarriersSelected,
    SettingsStringEnum.faster_checks_selected: FasterChecksSelected,
    SettingsStringEnum.hard_bosses_selected: HardBossesSelected,
    SettingsStringEnum.starting_moves_list_1: Items,
    SettingsStringEnum.starting_moves_list_2: Items,
    SettingsStringEnum.starting_moves_list_3: Items,
    SettingsStringEnum.starting_moves_list_4: Items,
    SettingsStringEnum.starting_moves_list_5: Items,
}

SettingsStringIntRangeMap: dict = {
    SettingsStringEnum.blocker_0: {"max": 201, "min": 0},
    SettingsStringEnum.blocker_1: {"max": 201, "min": 0},
    SettingsStringEnum.blocker_2: {"max": 201, "min": 0},
    SettingsStringEnum.blocker_3: {"max": 201, "min": 0},
    SettingsStringEnum.blocker_4: {"max": 201, "min": 0},
    SettingsStringEnum.blocker_5: {"max": 201, "min": 0},
    SettingsStringEnum.blocker_6: {"max": 201, "min": 0},
    SettingsStringEnum.blocker_7: {"max": 201, "min": 0},
    SettingsStringEnum.blocker_text: {"max": 201, "min": 0},
    SettingsStringEnum.coin_door_item_count: {"max": 201, "min": 0},
    SettingsStringEnum.crown_door_item_count: {"max": 201, "min": 0},
    SettingsStringEnum.helm_phase_count: {"max": 5, "min": 0},
    SettingsStringEnum.krool_key_count: {"max": 8, "min": 0},
    SettingsStringEnum.krool_phase_count: {"max": 5, "min": 0},
    SettingsStringEnum.medal_cb_req: {"max": 100, "min": 0},
    SettingsStringEnum.medal_requirement: {"max": 40, "min": 0},
    SettingsStringEnum.mermaid_gb_pearls: {"max": 5, "min": 0},
    SettingsStringEnum.rareware_gb_fairies: {"max": 20, "min": 0},
    SettingsStringEnum.starting_kongs_count: {"max": 5, "min": 0},
    SettingsStringEnum.starting_moves_count: {"max": 40, "min": 0},
    SettingsStringEnum.troff_0: {"max": 500, "min": 0},
    SettingsStringEnum.troff_1: {"max": 500, "min": 0},
    SettingsStringEnum.troff_2: {"max": 500, "min": 0},
    SettingsStringEnum.troff_3: {"max": 500, "min": 0},
    SettingsStringEnum.troff_4: {"max": 500, "min": 0},
    SettingsStringEnum.troff_5: {"max": 500, "min": 0},
    SettingsStringEnum.troff_6: {"max": 500, "min": 0},
    SettingsStringEnum.troff_7: {"max": 500, "min": 0},
    SettingsStringEnum.troff_text: {"max": 500, "min": 0},
    SettingsStringEnum.progressive_hint_text: {"max": 201, "min": 0},
    SettingsStringEnum.progressive_hint_count: {"max": 3500, "min": 0},
    SettingsStringEnum.win_condition_count: {"max": 201, "min": 0},
}
