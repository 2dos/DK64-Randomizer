"""File containing enums to represent all settings."""
from enum import IntEnum, auto

from randomizer.Enums.Items import Items
from randomizer.Lists.EnemyTypes import Enemies
from randomizer.Lists.MapsAndExits import Maps

# Each select-based setting should have its own associated enum class. The enum
# values should exactly match the input values in the HTML (not the IDs).
# Do not change the values of any enums in this file, or settings strings will
# break.

# Randomizers


class LogicType(IntEnum):
    """The logic use to place items in the seed.

    glitchless: No glitches will be required.
    glitch: Some glitches may be required.
    nologic: The seed may not be beatable.
    """

    glitchless = 1
    glitch = 2
    nologic = 3


class GlitchesSelected(IntEnum):
    """Glitch categories that can be selected for the seed logic.

    These values are tied to the GlitchSelector in randomizer.Lists.Logic. More
    details on each can be found in that file.
    """

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


class ActivateAllBananaports(IntEnum):
    """Whether bananaports should start as activated, and where.

    This enum is explicitly indexed for use in ApplyRandomizer.py. Do not
    change these enum values or seed generation will break.

    off: No bananaports will be activated.
    all: All bananaports will be activated.
    isles: Only bananaports in D.K. Isles will be activated.
    """

    off = 0
    all = 1
    isles = 2


class LevelRandomization(IntEnum):
    """Determines how entrances are randomized and placed.

    vanilla: All entrances are the same as the base game.
    level_order: Randomizes the order that the levels are in.
    loadingzone: All entrances except for Helm/Helm Lobby.
    loadingzonesdecoupled: All entrances except for Helm/Helm Lobby.
        Going back through an entrance may not take you back to where you
        just were.
    """

    vanilla = 0
    level_order = 1
    loadingzone = 2
    loadingzonesdecoupled = 3


# TODO: merge this with the Types enum.
class ItemRandoListSelected(IntEnum):
    """Item categories that may be randomized.

    These values are tied to the ItemRandoSelector in randomizer.Enums.Types.
    The presence of "beanpearl" requires a different enum from Types.
    """

    shop = 1
    banana = 2
    toughbanana = 3
    crown = 4
    blueprint = 5
    key = 6
    medal = 7
    coin = 8
    kong = 9
    fairy = 10
    rainbowcoin = 11
    beanpearl = 12
    fakeitem = 13
    junkitem = 14


class KasplatRandoSetting(IntEnum):
    """Determines if and how Kasplats are randomized.

    off: Kasplats are in their original locations with original blueprints.
    vanilla_locations: Kasplats are shuffled between the locations that exist
        in the vanilla game.
    location_shuffle: Kasplats will be shuffled between all possible locations,
        including new ones not in the vanilla game.
    """

    off = 0
    vanilla_locations = 1
    location_shuffle = 2


class MoveRando(IntEnum):
    """Determines if and how moves are randomized.

    off: Moves are in their vanilla locations.
    on: Moves will be shuffled between shops, but must still be bought by the
        original Kong.
    cross_purchase: Moves will be shuffled between shops, and can be bought by
        any Kong.
    start_with: Player starts with all moves unlocked.
    item_shuffle: Moves are shuffled into the broader item pool. (Cannot be
        selected through the web UI.)
    """

    off = 0
    on = 1
    cross_purchase = 2
    start_with = 3
    item_shuffle = 4


class TrainingBarrels(IntEnum):
    """Determines if and how training barrels are randomized.

    normal: Training barrels give the vanilla moves.
    shuffled: Training moves are shuffled into the item pool, and the training
        barrels gives four random moves.
    """

    normal = 0
    shuffled = 1


class RandomPrices(IntEnum):
    """Determines how and if shop prices are randomized.

    vanilla: Shop prices are the same as the vanilla game.
    free: All items are free.
    low: Moves cost 1-4 coins most of the time.
    medium: Moves cost 1-8 coins most of the time.
    high: Moves cost 1-12 coins most of the time.
    extreme: Moves cost 10+ coins most of the time.
    """

    vanilla = 0
    free = 1
    low = 2
    medium = 3
    high = 4
    extreme = 5


class ShockwaveStatus(IntEnum):
    """Determines how Banana Fairy Isle is handled.

    vanilla: Camera and Shockwave are given.
    shuffled: Camera and Shockwave are shuffled into the move pool as a single
        item. BFI has a shared or Tiny reward.
    shuffled_decoupled: Camera and Shockwave are shuffled into the move pool as
        separate items. BFI has a shared or Tiny reward.
    start_with: Player starts with Camera and Shockwave. BFI has nothing.
    """

    vanilla = 0
    shuffled = 1
    shuffled_decoupled = 2
    start_with = 3


class BananaportRando(IntEnum):
    """Determines how bananaports are shuffled.

    off: Bananaports have their vanilla locations.
    in_level: Bananaport warps are shuffled within their own levels.
    crossmap_coupled: Bananaport warps are shuffled among all bananaports in
        all levels.
    crossmap_decoupled: Same as crossmap_coupled, but going back through one
        bananaport may not take you to the same location.
    """

    off = 0
    in_level = 1
    crossmap_coupled = 2
    crossmap_decoupled = 3


# Overworld


class MinigamesListSelected(IntEnum):
    """Minigame categories used for the web selector.

    These values are tied to the MinigameSelector in randomizer.Lists.Minigame.
    More details on each can be found in that file.
    """

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


class WinCondition(IntEnum):
    """The condition needed to complete the game.

    This enum is explicitly indexed for use in ApplyRandomizer.py. Do not
    change these enum values or seed generation will break.

    beat_krool: Complete the King K. Rool boss fight.
    get_key8: Collect key 8.
    all_fairies: Collect all Banana Fairies.
    all_blueprints: Collect all blueprints.
    all_medals: Collect all Banana Medals.
    poke_snap: Capture a photograph of each enemy in the game.
    all_keys: Collect all keys.
    """

    beat_krool = 0
    get_key8 = 1
    all_fairies = 2
    all_blueprints = 3
    all_medals = 4
    poke_snap = 5
    all_keys = 6


class FreeTradeSetting(IntEnum):
    """Determines if Kongs can collect items assigned to other Kongs.

    none: Items can only be collected by their original assigned Kong.
    not_blueprints: Major items can be collected by any Kong, except for
        blueprints.
    major_collectibles: Major items can be collected by any Kong.
    """

    none = 0
    not_blueprints = 1
    major_collectibles = 2


class KrushaUi(IntEnum):
    """Which Kong model will be replaced with Krusha."""

    no_slot = 0
    dk = 1
    diddy = 2
    lanky = 3
    tiny = 4
    chunky = 5
    random = 6


class HelmDoorItem(IntEnum):
    """Items that are required to open the crown/coin doors in Helm.

    vanilla: The originally required item (crowns for door 1, company coins for
        door 2).
    opened: The door is automatically opened.
    random: The door is opened by a randomly selected item.
    req_gb: Golden Bananas.
    req_bp: Blueprints.
    req_companycoins: The Rareware and Nintendo coins.
    req_key: Keys.
    req_medal: Banana Medals.
    req_crown: Battle Browns.
    req_fairy: Banana Fairies.
    req_rainbowcoin: Rainbow Coins.
    req_bean: The bean.
    req_pearl: Pearls.
    """

    vanilla = 0
    opened = 1
    random = 2
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


# Difficulty


class DamageAmount(IntEnum):
    """The damage multipler.

    default: Normal damage.
    double: Damage is 2x normal.
    quad: Damage is 4x normal.
    ohko: Damage is 12x normal (one hit kills).
    """

    default = 0
    double = 1
    quad = 2
    ohko = 3


class CrownEnemyRando(IntEnum):
    """Determines the difficulty of enemies in Battle Arenas."""

    off = 0
    easy = 1
    medium = 2
    hard = 3


# Quality of Life


class MiscChangesSelected(IntEnum):
    """Various quality of life fixes that can be applied.

    These values are tied to the QoLSelector in randomizer.Lists.QoL. More
    details on each can be found in that file.
    """

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


class WrinklyHints(IntEnum):
    """Whether or not Wrinkly hints are replaced with useful randomizer hints.

    off: Hints are the same as the vanilla game.
    standard: Normal randomizer hints are provided.
    cryptic: Cryptic randomizer hints are provided.
    """

    off = 0
    standard = 1
    cryptic = 2


class HelmSetting(IntEnum):
    """Determines where the player starts when entering Hideout Helm.

    This enum is explicitly indexed for use in ApplyRandomizer.py. Do not
    change these enum values or seed generation will break.

    default: Player starts at the entrance to Helm.
    skip_start: Player starts in the Blast-O-Matic room, with the roman numeral
        doors opened and no gates blocking the music pads.
    skip_all: Player starts at the crown door.
    """

    default = 0
    skip_start = 1
    skip_all = 2


class MicrohintsEnabled(IntEnum):
    """Adds some additional hints for late-game-required items.

    This enum is explicitly indexed for use in ApplyRandomizer.py. Do not
    change these enum values or seed generation will break.

    off: No extra hints are added.
    base: Monkeyport and Gorilla Gone hints are added to the Krem Isle pads if
        the user is otherwise able to access the Hideout Helm lobby.
    all: Same as base, but the instrument pads in Hideout Helm will provide
        hints as to their locations.
    """

    off = 0
    base = 1
    all = 2


# Cosmetics


class MusicCosmetics(IntEnum):
    """Determines how BGM, fanfare or event music is shuffled.

    default: Music is not shuffled.
    randomized: Music is shuffled.
    chaos: All D.K. Rap, all the time.
    uploaded: Use music files provided by the user.
    """

    default = auto()
    randomized = auto()
    chaos = auto()
    uploaded = auto()


class KlaptrapModel(IntEnum):
    """Determines which model is used for Klaptrap in Beaver Bother."""

    green = auto()
    purple = auto()
    red = auto()
    random_klap = auto()
    random_model = auto()


class CharacterColors(IntEnum):
    """Determines the colors for the Kongs, Rambi and Enguarde.

    vanilla: The character uses vanilla colors.
    randomized: The character uses a random color.
    custom: The character uses a user-provided color.
    """

    vanilla = auto()
    randomized = auto()
    custom = auto()


class ColorblindMode(IntEnum):
    """Determines which colorblind mode setting is used.

    This enum is explicitly indexed for use in ApplyRandomizer.py. Do not
    change these enum values or seed generation will break.

    off: Normal colors.
    prot: Setting for protanomaly/protanopia (red/green color blindness,
        biased toward red).
    deut: Setting for deuteranomaly/deuteranopia (red/green color blindness,
        biased toward green).
    trit: Setting for tritanomaly/tritanopia (blue/yellow color blindness).
    """

    off = 0
    prot = 1
    deut = 2
    trit = 3


# Additional enums not currently shown on the web site.


class FillAlgorithm(IntEnum):
    """The algorithm used for placing items.

    forward: Places items in locations that are available with what's already
        been placed. Faster than assumed.
    assumed: Attempts to place items in locations under the assumption that
        those locations will be valid. More likely to place items deeper into
        a seed.
    random: Places items with no regard for logic.
    """

    forward = auto()
    assumed = auto()
    random = auto()


class ShuffleLoadingZones(IntEnum):
    """Determines how loading zones are shuffled.

    none: No loading zones are shuffled.
    levels: Only level entrances are shuffled.
    all: All loading zones are shuffled.
    """

    none = auto()
    levels = auto()
    all = auto()


class MinigameBarrels(IntEnum):
    """Determines how the minigames are shuffled between barrels.

    normal: Minigames are the same as in the vanilla game.
    skip: Minigames are auto-completed.
    random: Minigames are shuffled randomly.
    selected: Minigames are shuffled among the selections made by the user.
    """

    normal = auto()
    skip = auto()
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
    "helm_barrels": MinigameBarrels,
}


class SettingsStringEnum(IntEnum):
    """Maps setting names to key values, for use in the ssettings string.

    Changing any of the existing values will cause generated settings strings
        to break. Only add new values.

    Next available value: 132
    """

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
    dpad_display = 27
    enable_shop_hints = 28
    enable_tag_anywhere = 29
    enemies_selected = 30
    enemy_rando = 31
    enemy_speed_rando = 32
    fast_gbs = 33
    fast_start_beginning_of_game = 34
    fast_warps = 35
    fps_display = 36
    free_trade_setting = 37
    generate_spoilerlog = 38
    glitches_selected = 39
    hard_blockers = 40
    hard_bosses = 41
    hard_enemies = 42
    hard_level_progression = 43
    hard_shooting = 44
    hard_troff_n_scoff = 45
    helm_hurry = 46
    helm_phase_count = 47
    helm_phase_order_rando = 48
    helm_random = 49
    helm_setting = 50
    helmhurry_list_banana_medal = 51
    helmhurry_list_battle_crown = 52
    helmhurry_list_bean = 53
    helmhurry_list_blueprint = 54
    helmhurry_list_boss_key = 55
    helmhurry_list_colored_bananas = 56
    helmhurry_list_company_coins = 57
    helmhurry_list_fairies = 58
    helmhurry_list_golden_banana = 59
    helmhurry_list_ice_traps = 60
    helmhurry_list_kongs = 61
    helmhurry_list_move = 62
    helmhurry_list_pearl = 63
    helmhurry_list_rainbow_coin = 64
    helmhurry_list_starting_time = 65
    high_req = 66
    item_rando_list_selected = 67
    item_reward_previews = 68
    kasplat_rando_setting = 69
    key_8_helm = 70
    keys_random = 71
    kong_rando = 72
    krool_access = 73
    krool_key_count = 74
    krool_phase_count = 75
    krool_phase_order_rando = 76
    krool_random = 77
    krusha_ui = 78
    level_randomization = 79
    logic_type = 80
    maximize_helm_blocker = 81
    medal_cb_req = 82
    medal_requirement = 83
    microhints_enabled = 84
    minigames_list_selected = 85
    misc_changes_selected = 86
    move_rando = 87
    no_healing = 88
    no_melons = 89
    open_levels = 90
    open_lobbies = 91
    perma_death = 92
    portal_numbers = 93
    puzzle_rando = 94
    quality_of_life = 95
    random_fairies = 96
    random_medal_requirement = 97
    random_patches = 98
    random_prices = 99
    random_starting_region = 100
    randomize_blocker_required_amounts = 101
    randomize_cb_required_amounts = 102
    randomize_pickups = 103
    rareware_gb_fairies = 104
    select_keys = 105
    shockwave_status = 106
    shop_indicator = 107
    shorten_boss = 108
    shuffle_items = 109
    shuffle_shops = 110
    smaller_shops = 111
    starting_keys_list_selected = 112
    starting_kongs_count = 113
    starting_random = 114
    tns_location_rando = 115
    training_barrels = 116
    troff_0 = 117
    troff_1 = 118
    troff_2 = 119
    troff_3 = 120
    troff_4 = 121
    troff_5 = 122
    troff_6 = 123
    troff_text = 124
    warp_level_list_selected = 125
    warp_to_isles = 126
    win_condition = 127
    wrinkly_available = 128
    wrinkly_hints = 129
    wrinkly_location_rando = 130
    coin_rando = 131


class SettingsStringDataType(IntEnum):
    """Enum for mapping settings to data types for encryption/decryption."""

    bool = auto()
    # Can represent up to 16 values (-8 to 7).
    int4 = auto()
    # Can represent up to 256 values (-128 to 127).
    int8 = auto()
    # Can represent up to 65,536 values (-32,768 to 32,767).
    int16 = auto()
    str = auto()
    list = auto()


# This maps settings to the data types that will be used to encode them in the
# settings string. Any enum-based settings should use that enum as their data
# type, to shrink the payload as much as possible.
SettingsStringTypeMap = {
    SettingsStringEnum.activate_all_bananaports: ActivateAllBananaports,
    SettingsStringEnum.alter_switch_allocation: SettingsStringDataType.bool,
    SettingsStringEnum.auto_keys: SettingsStringDataType.bool,
    SettingsStringEnum.bananaport_rando: BananaportRando,
    SettingsStringEnum.blocker_0: SettingsStringDataType.int16,
    SettingsStringEnum.blocker_1: SettingsStringDataType.int16,
    SettingsStringEnum.blocker_2: SettingsStringDataType.int16,
    SettingsStringEnum.blocker_3: SettingsStringDataType.int16,
    SettingsStringEnum.blocker_4: SettingsStringDataType.int16,
    SettingsStringEnum.blocker_5: SettingsStringDataType.int16,
    SettingsStringEnum.blocker_6: SettingsStringDataType.int16,
    SettingsStringEnum.blocker_7: SettingsStringDataType.int16,
    SettingsStringEnum.blocker_text: SettingsStringDataType.int16,
    SettingsStringEnum.bonus_barrel_auto_complete: SettingsStringDataType.bool,
    SettingsStringEnum.bonus_barrel_rando: SettingsStringDataType.bool,
    SettingsStringEnum.boss_kong_rando: SettingsStringDataType.bool,
    SettingsStringEnum.boss_location_rando: SettingsStringDataType.bool,
    SettingsStringEnum.cb_rando: SettingsStringDataType.bool,
    SettingsStringEnum.coin_door_item: HelmDoorItem,
    SettingsStringEnum.coin_door_item_count: SettingsStringDataType.int16,
    SettingsStringEnum.crown_door_item: HelmDoorItem,
    SettingsStringEnum.crown_door_item_count: SettingsStringDataType.int16,
    SettingsStringEnum.crown_enemy_rando: CrownEnemyRando,
    SettingsStringEnum.crown_placement_rando: SettingsStringDataType.bool,
    SettingsStringEnum.coin_rando: SettingsStringDataType.bool,
    SettingsStringEnum.damage_amount: DamageAmount,
    SettingsStringEnum.disable_tag_barrels: SettingsStringDataType.bool,
    SettingsStringEnum.dpad_display: SettingsStringDataType.bool,
    SettingsStringEnum.enable_shop_hints: SettingsStringDataType.bool,
    SettingsStringEnum.enable_tag_anywhere: SettingsStringDataType.bool,
    SettingsStringEnum.enemies_selected: SettingsStringDataType.list,
    SettingsStringEnum.enemy_rando: SettingsStringDataType.bool,
    SettingsStringEnum.enemy_speed_rando: SettingsStringDataType.bool,
    SettingsStringEnum.fast_gbs: SettingsStringDataType.bool,
    SettingsStringEnum.fast_start_beginning_of_game: SettingsStringDataType.bool,
    SettingsStringEnum.fast_warps: SettingsStringDataType.bool,
    SettingsStringEnum.fps_display: SettingsStringDataType.bool,
    SettingsStringEnum.free_trade_setting: FreeTradeSetting,
    SettingsStringEnum.generate_spoilerlog: SettingsStringDataType.bool,
    SettingsStringEnum.glitches_selected: SettingsStringDataType.list,
    SettingsStringEnum.hard_blockers: SettingsStringDataType.bool,
    SettingsStringEnum.hard_bosses: SettingsStringDataType.bool,
    SettingsStringEnum.hard_enemies: SettingsStringDataType.bool,
    SettingsStringEnum.hard_level_progression: SettingsStringDataType.bool,
    SettingsStringEnum.hard_shooting: SettingsStringDataType.bool,
    SettingsStringEnum.hard_troff_n_scoff: SettingsStringDataType.bool,
    SettingsStringEnum.helm_hurry: SettingsStringDataType.bool,
    SettingsStringEnum.helm_phase_count: SettingsStringDataType.int4,
    SettingsStringEnum.helm_phase_order_rando: SettingsStringDataType.bool,
    SettingsStringEnum.helm_random: SettingsStringDataType.bool,
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
    SettingsStringEnum.helmhurry_list_starting_time: SettingsStringDataType.int16,
    SettingsStringEnum.high_req: SettingsStringDataType.bool,
    SettingsStringEnum.item_rando_list_selected: SettingsStringDataType.list,
    SettingsStringEnum.item_reward_previews: SettingsStringDataType.bool,
    SettingsStringEnum.kasplat_rando_setting: KasplatRandoSetting,
    SettingsStringEnum.key_8_helm: SettingsStringDataType.bool,
    SettingsStringEnum.keys_random: SettingsStringDataType.bool,
    SettingsStringEnum.kong_rando: SettingsStringDataType.bool,
    SettingsStringEnum.krool_access: SettingsStringDataType.bool,
    SettingsStringEnum.krool_key_count: SettingsStringDataType.int8,
    SettingsStringEnum.krool_phase_count: SettingsStringDataType.int4,
    SettingsStringEnum.krool_phase_order_rando: SettingsStringDataType.bool,
    SettingsStringEnum.krool_random: SettingsStringDataType.bool,
    SettingsStringEnum.krusha_ui: KrushaUi,
    SettingsStringEnum.level_randomization: LevelRandomization,
    SettingsStringEnum.logic_type: LogicType,
    SettingsStringEnum.maximize_helm_blocker: SettingsStringDataType.bool,
    SettingsStringEnum.medal_cb_req: SettingsStringDataType.int16,
    SettingsStringEnum.medal_requirement: SettingsStringDataType.int16,
    SettingsStringEnum.microhints_enabled: MicrohintsEnabled,
    SettingsStringEnum.minigames_list_selected: SettingsStringDataType.list,
    SettingsStringEnum.misc_changes_selected: SettingsStringDataType.list,
    SettingsStringEnum.move_rando: MoveRando,
    SettingsStringEnum.no_healing: SettingsStringDataType.bool,
    SettingsStringEnum.no_melons: SettingsStringDataType.bool,
    SettingsStringEnum.open_levels: SettingsStringDataType.bool,
    SettingsStringEnum.open_lobbies: SettingsStringDataType.bool,
    SettingsStringEnum.perma_death: SettingsStringDataType.bool,
    SettingsStringEnum.portal_numbers: SettingsStringDataType.bool,
    SettingsStringEnum.puzzle_rando: SettingsStringDataType.bool,
    SettingsStringEnum.quality_of_life: SettingsStringDataType.bool,
    SettingsStringEnum.random_fairies: SettingsStringDataType.bool,
    SettingsStringEnum.random_medal_requirement: SettingsStringDataType.bool,
    SettingsStringEnum.random_patches: SettingsStringDataType.bool,
    SettingsStringEnum.random_prices: RandomPrices,
    SettingsStringEnum.random_starting_region: SettingsStringDataType.bool,
    SettingsStringEnum.randomize_blocker_required_amounts: SettingsStringDataType.bool,
    SettingsStringEnum.randomize_cb_required_amounts: SettingsStringDataType.bool,
    SettingsStringEnum.randomize_pickups: SettingsStringDataType.bool,
    SettingsStringEnum.rareware_gb_fairies: SettingsStringDataType.int8,
    SettingsStringEnum.select_keys: SettingsStringDataType.bool,
    SettingsStringEnum.shockwave_status: ShockwaveStatus,
    SettingsStringEnum.shop_indicator: SettingsStringDataType.bool,
    SettingsStringEnum.shorten_boss: SettingsStringDataType.bool,
    SettingsStringEnum.shuffle_items: SettingsStringDataType.bool,
    SettingsStringEnum.shuffle_shops: SettingsStringDataType.bool,
    SettingsStringEnum.smaller_shops: SettingsStringDataType.bool,
    SettingsStringEnum.starting_keys_list_selected: SettingsStringDataType.list,
    SettingsStringEnum.starting_kongs_count: SettingsStringDataType.int4,
    SettingsStringEnum.starting_random: SettingsStringDataType.bool,
    SettingsStringEnum.tns_location_rando: SettingsStringDataType.bool,
    SettingsStringEnum.training_barrels: TrainingBarrels,
    SettingsStringEnum.troff_0: SettingsStringDataType.int16,
    SettingsStringEnum.troff_1: SettingsStringDataType.int16,
    SettingsStringEnum.troff_2: SettingsStringDataType.int16,
    SettingsStringEnum.troff_3: SettingsStringDataType.int16,
    SettingsStringEnum.troff_4: SettingsStringDataType.int16,
    SettingsStringEnum.troff_5: SettingsStringDataType.int16,
    SettingsStringEnum.troff_6: SettingsStringDataType.int16,
    SettingsStringEnum.troff_text: SettingsStringDataType.int16,
    SettingsStringEnum.warp_level_list_selected: SettingsStringDataType.list,
    SettingsStringEnum.warp_to_isles: SettingsStringDataType.bool,
    SettingsStringEnum.win_condition: WinCondition,
    SettingsStringEnum.wrinkly_available: SettingsStringDataType.bool,
    SettingsStringEnum.wrinkly_hints: WrinklyHints,
    SettingsStringEnum.wrinkly_location_rando: SettingsStringDataType.bool,
}

# Another map for list settings, for the underlying data type of the list.
SettingsStringListTypeMap = {
    SettingsStringEnum.enemies_selected: Enemies,
    SettingsStringEnum.glitches_selected: GlitchesSelected,
    SettingsStringEnum.item_rando_list_selected: ItemRandoListSelected,
    SettingsStringEnum.minigames_list_selected: MinigamesListSelected,
    SettingsStringEnum.misc_changes_selected: MiscChangesSelected,
    SettingsStringEnum.starting_keys_list_selected: Items,
    SettingsStringEnum.warp_level_list_selected: Maps,
}
