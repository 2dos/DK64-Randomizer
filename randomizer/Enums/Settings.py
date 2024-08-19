"""File containing enums to represent all settings."""

from __future__ import annotations

from enum import IntEnum, auto
from typing import TYPE_CHECKING

from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Items import Items
from randomizer.Lists.EnemyTypes import Enemies
from randomizer.Enums.Maps import Maps

# Each select-based setting should have its own associated enum class. The enum
# values should exactly match the input values in the HTML (not the IDs).
# Do not change the values of any enums in this file, or settings strings will
# break.


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


class BigHeadMode(IntEnum):
    """Determines which big head mode setting is used.

    This enum is explicitly indexed for use in ApplyRandomizer.py. Do not
    change these enum values or seed generation will break.

    off: Normal head size.
    big: Very big heads.
    small: Very small heads.
    """

    off = 0
    big = 1
    small = 2


class CBRando(IntEnum):
    """Determines the level of CB Rando utilized.

    off: CB Rando is disabled.
    on: CB Rando is on in the main 7 levels.
    on_with_isles: Same as "on", but expanded to include isles.
    """

    off = auto()
    on = auto()
    on_with_isles = auto()


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


class CrownEnemyRando(IntEnum):
    """Determines the difficulty of enemies in Battle Arenas."""

    off = 0
    easy = 1
    medium = 2
    hard = 3


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


class DPadDisplays(IntEnum):
    """Varying methods of displaying the dpad.

    off: display isn't rendered.
    on: display is rendered including all elements.
    minimal: only the medal is rendered.
    """

    off = 0
    on = 1
    minimal = 2


class ExcludedSongs(IntEnum):
    """Determines the types of songs excluded."""

    wrinkly = 1
    transformation = 2
    pause_music = 3
    sub_areas = 4
    # shops = 5
    # events = 6


class ExtraCutsceneSkips(IntEnum):
    """Controls how extra cutscenes are handled.

    This enum is explicitly indexed for use in ApplyRandomizer.py. Do not
    change these enum values or seed generation will break.

    off: Extra Cutscenes can't be skipped.
    press: Cutscenes can be skipped by pressing start.
    auto: Cutscenes are skipped automatically.
    """

    off = 0
    press = 1
    auto = 2


class FasterChecksSelected(IntEnum):
    """Various faster check changes that can be applied.

    These values are tied to the FasterCheckSelector in randomizer.Lists.Multiselectors. More
    details on each can be found in that file.
    """

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
    """The algorithm used for placing items.

    This enum does not correspond to any website setting.

    forward: Places items in locations that are available with what's already
        been placed. Faster than assumed.
    assumed: Attempts to place items in locations under the assumption that
        those locations will be valid. More likely to place items deeper into
        a seed.
    random: Places items with no regard for logic.
    careful_random: Places items with no regard for anything except coin logic. Probably.
    """

    forward = auto()
    assumed = auto()
    random = auto()
    careful_random = auto()


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


class FungiTimeSetting(IntEnum):
    """Determines the starting time of day.

    day: Start at daytime.
    night: Start at nighttime.
    random: Random starting time.
    dusk: All time-specific gates are removed.
    progressive: Time of day progresses naturally when in Fungi.
    """

    day = auto()
    night = auto()
    random = auto()
    dusk = auto()
    progressive = auto()


class GalleonWaterSetting(IntEnum):
    """Determines the starting water level.

    lowered: Start lowered.
    raised: Start raised.
    random: Random level.
    """

    lowered = auto()
    raised = auto()
    random = auto()


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
    moontail = 14


class HelmDoorItem(IntEnum):
    """Items that are required to open the crown/coin doors in Helm.

    vanilla: The originally required item (crowns for door 1, company coins for
        door 2).
    opened: The door is automatically opened.
    medium_random: The door is opened by a randomly selected item (Medium difficulty).
    req_gb: Golden Bananas.
    req_bp: Blueprints.
    req_companycoins: The Rareware and Nintendo coins.
    req_key: Keys.
    req_medal: Banana Medals.
    req_crown: Battle Crowns.
    req_fairy: Banana Fairies.
    req_rainbowcoin: Rainbow Coins.
    req_bean: The bean.
    req_pearl: Pearls.
    easy_random: The door is opened by a randomly selected item (Easy difficulty).
    hard_random: The door is opened by a randomly selected item (Hard difficulty).
    """

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


class HelmBonuses(IntEnum):
    """Determines how many barrels are necessary to beat in order to defeat a helm room.

    This enum is explicitly indexed for use in ApplyRandomizer.py. Do not
    change these enum values or seed generation will break.

    zero: Room is completed upon playing the instrument pad.
    one: Room is completed upon beating the left-most barrel in each room.
    two: Both barrels are required to complete the room.
    """

    zero = 0
    one = 1
    two = 2


class HardBossesSelected(IntEnum):
    """Various hard boss changes that can be applied.

    These values are tied to the HardBossSelector in randomizer.Lists.HardMode. More
    details on each can be found in that file.
    """

    fast_mad_jack = 1
    alternative_mad_jack_kongs = 2
    pufftoss_star_rando = 3
    pufftoss_star_raised = 4
    kut_out_phase_rando = 5


class HardModeSelected(IntEnum):
    """Various hard mode changes that can be applied.

    These values are tied to the HardSelector in randomizer.Lists.HardMode. More
    details on each can be found in that file.
    """

    null_option_0 = 1  # Used to be hard bosses
    null_option_1 = 2  # Used to be extra hard bosses
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
    """The attempted frequency of ice traps in the seed.

    Placing ice traps into the seed will take away from junk items
    rare: 4 ice traps
    mild: 10 ice traps.
    common: 32 ice traps.
    frequent: 64 ice traps.
    pain: 100 ice traps.
    """

    rare = 0
    mild = 1
    common = 2
    frequent = 3
    pain = 4


# TODO: merge this with the Types enum.
class ItemRandoListSelected(IntEnum):
    """Item categories that may be randomized.

    These values are tied to the ItemRandoSelector in randomizer.Enums.Types.
    The presence of "beanpearl" and "shopowners" requires a different enum from Types.
    """

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


class RandomModels(IntEnum):
    """Determines the random model level."""

    off = auto()
    random = auto()
    extreme = auto()


class KrushaUi(IntEnum):
    """Which Kong model will be replaced with Krusha."""

    no_slot = 0
    dk = 1
    diddy = 2
    lanky = 3
    tiny = 4
    chunky = 5
    random = 6


class KongModels(IntEnum):
    """Models for each kong."""

    default = 0
    disco_chunky = 1
    krusha = 2
    krool_fight = 3
    krool_cutscene = 4
    cranky = 5
    candy = 6
    funky = 7


class LevelRandomization(IntEnum):
    """Determines how entrances are randomized and placed.

    vanilla: All entrances are the same as the base game.
    level_order: Randomizes the order that the levels are in.
    loadingzone: All entrances except for Helm/Helm Lobby.
    loadingzonesdecoupled: All entrances except for Helm/Helm Lobby.
        Going back through an entrance may not take you back to where you
        just were.
    level_order_complex: Level order setting, but with complex order.
    """

    vanilla = 0
    level_order = 1
    loadingzone = 2
    loadingzonesdecoupled = 3
    level_order_complex = 4


class LogicType(IntEnum):
    """The logic use to place items in the seed.

    glitchless: No glitches will be required.
    glitch: Some glitches may be required.
    nologic: The seed may not be beatable.
    """

    glitchless = 1
    glitch = 2
    nologic = 3


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


class MinigameBarrels(IntEnum):
    """Determines how the minigames are shuffled between barrels.

    This enum does not correspond to any website setting.

    normal: Minigames are the same as in the vanilla game.
    skip: Minigames are auto-completed.
    random: Minigames are shuffled randomly.
    selected: Minigames are shuffled among the selections made by the user.
    """

    normal = auto()
    skip = auto()
    random = auto()
    selected = auto()


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
    arenas = 17
    training_minigames = 18


class MiscChangesSelected(IntEnum):
    """Various quality of life fixes that can be applied.

    These values are tied to the QoLSelector in randomizer.Lists.Multiselectors. More
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


class MusicFilters(IntEnum):
    """Determine how music is filtered."""

    length = 1
    location = 2


class PuzzleRando(IntEnum):
    """Determines the difficulty of puzzle rando.

    off: Puzzle Solutions are NOT randomized.
    easy: Easy boundaries, no castle car race.
    medium: Medium boundaries, no castle car race.
    hard: Hard boundaries.
    chaos: Any value in the easy, medium or hard bounds
    """

    off = 0
    easy = 1
    medium = 2
    hard = 3
    chaos = 4


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


class RemovedBarriersSelected(IntEnum):
    """Various barriers that can be removed that can be applied.

    These values are tied to the RemovedBarrierSelector in randomizer.Lists.Multiselectors. More
    details on each can be found in that file.
    """

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


class ShuffleLoadingZones(IntEnum):
    """Determines how loading zones are shuffled.

    This enum does not correspond to any website setting.

    none: No loading zones are shuffled.
    levels: Only level entrances are shuffled.
    all: All loading zones are shuffled.
    """

    none = auto()
    levels = auto()
    all = auto()


class ShufflePortLocations(IntEnum):
    """Determines how bananaports are shuffled.

    off = No shuffling
    vanilla_only = Only reference a pool of vanilla locations
    half_vanilla = For each pair, 1 of them is vanilla. Probably won't obey those rules with other bananaport shuffles
    on = full shuffle. Maximum mayhem. Maximum pain. Minimal chance of your favorite streamer keeping it off their restrictions.
    """

    off = auto()
    vanilla_only = auto()
    half_vanilla = auto()
    on = auto()


class SlamRequirement(IntEnum):
    """Determines the slam requirement for a switch, currently only chunky phase.

    green: Green Slam (Simian Slam).
    blue: Blue Slam (Super Simian Slam).
    red: Red Slam (Super Duper Simian Slam).
    random: Random slam color from the above.
    """

    green = auto()
    blue = auto()
    red = auto()
    random = auto()


class SoundType(IntEnum):
    """Determines the default sound mode.

    stereo: Default.
    surround: Dolby Surround.
    mono: Mono audio type.
    """

    stereo = 0
    mono = 1
    surround = 2


class SwitchsanityLevel(IntEnum):
    """Determines what switches are shuffled in switchsanity.

    none: No switches are altered.
    helm_access: Only the monkeyport pad and the gorilla gone pad on the path to Helm are shuffled.
    all: All switches are shuffled.
    """

    off = 0
    helm_access = auto()
    all = auto()


class TrainingBarrels(IntEnum):
    """Determines if and how training barrels are randomized.

    normal: Training barrels give the vanilla moves.
    shuffled: Training moves are shuffled into the item pool, and the training
        barrels gives four random moves.
    """

    normal = 0
    shuffled = 1


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


class WinConditionComplex(IntEnum):
    """The condition needed to complete the game.

    This enum is an iteration on the WinCondition enum.

    beat_krool: Complete the King K. Rool boss fight.
    get_key8: Collect Key 8. Mostly legacy.
    krem_kapture: Capture a photograph of each enemy in the game.
    req_gb: Golden Bananas.
    req_bp: Blueprints.
    req_companycoins: The Rareware and Nintendo coins.
    req_key: Keys.
    req_medal: Banana Medals.
    req_crown: Battle Crowns.
    req_fairy: Banana Fairies.
    req_rainbowcoin: Rainbow Coins.
    req_bean: The bean.
    req_pearl: Pearls.
    easy_random: The game is beaten by obtaining a random amount of a randomly selected item (Easy difficulty).
    medium_random: The game is beaten by obtaining a random amount of a randomly selected item (Medium difficulty).
    hard_random: The game is beaten by obtaining a random amount of a randomly selected item (Hard difficulty).
    """

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
    """Whether or not Wrinkly hints are replaced with useful randomizer hints.

    off: Hints are the same as the vanilla game.
    standard: Normal randomizer hints are provided.
    cryptic: Cryptic randomizer hints are provided.
    fixed_racing: Fixed distribution - this one is for the S2 racing preset.
    item_hinting: All Kongs, Keys, and as many moves as possible are hinted, prioritizing WotH moves.
    item_hinting_advanced: Same as previous, but intentionally more vague.
    """

    off = 0
    standard = 1
    cryptic = 2
    fixed_racing = 3
    item_hinting = 4
    item_hinting_advanced = 5


class SpoilerHints(IntEnum):
    """Whether or not spoiler-style hints are generated within the spoiler log for external trackers to use.

    off: No hints are generated.
    vial_colors: The keys, kongs, and non-junk vials with their color will be hinted for each level. Includes K. Rool and Helm order.
    points: Assign a number of points to each level based on the items that level contains. Point values per item can be specified. Includes K. Rool and Helm order.
    """

    off = 0
    vial_colors = 1
    points = 2


# ALL SELECT-BASED SETTINGS NEED AN ENTRY HERE!
# A dictionary that maps setting names to the associated enum for that specific setting.
# The key for each enum must exactly match the HTML name of the associated select.
SettingsMap = {
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
    "damage_amount": DamageAmount,
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
}


class SettingsStringEnum(IntEnum):
    """Maps setting names to key values, for use in the settings string.

    Changing any of the existing values will cause generated settings strings
        to break. Only add new values.

    Do not delete settings from this enum. Instead, add an entry to the
        DeprecatedSettings set below. This will be cleaned up with every major
        release.

    ALL SETTINGS NEED AN ENTRY HERE!
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


# If a setting needs to be removed, add it to this set instead of removing it
# from the enum above.
DeprecatedSettings = {
    SettingsStringEnum.hard_enemies,
    SettingsStringEnum.choose_starting_moves,
    SettingsStringEnum.open_levels,
    SettingsStringEnum.high_req,
    SettingsStringEnum.krusha_ui,
    SettingsStringEnum.hard_level_progression,
    SettingsStringEnum.puzzle_rando,
    SettingsStringEnum.win_condition,
}


class SettingsStringDataType(IntEnum):
    """Enum for mapping settings to data types for encryption/decryption."""

    bool = auto()
    # Can represent up to 16 values (-8 to 7).
    int4 = auto()
    # Can represent up to 256 values (-128 to 127).
    int8 = auto()
    # Can represent up to 65,536 values (-32,768 to 32,767).
    int16 = auto()
    # Will be shrunk down to the smallest possible size.
    var_int = auto()
    str = auto()
    list = auto()
    # Can represent up to 65,536 values (0 to 65535)
    u16 = auto()


# ALL SETTINGS NEED AN ENTRY HERE!
# This maps settings to the data types that will be used to encode them in the
# settings string. Any enum-based settings should use that enum as their data
# type, to shrink the payload as much as possible.
#
# When adding an int setting, make sure to use the smallest int possible.
# This will reduce the characters added to the settings string. See the above
# enum for valid int values.
#
# If you are using the var_int type, you must use the addSettingIntRange()
# function below to specify the valid int range.
SettingsStringTypeMap = {
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
    SettingsStringEnum.coin_rando: SettingsStringDataType.bool,
    SettingsStringEnum.damage_amount: DamageAmount,
    SettingsStringEnum.disable_tag_barrels: SettingsStringDataType.bool,
    SettingsStringEnum.dk_portal_location_rando: SettingsStringDataType.bool,
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
    SettingsStringEnum.hard_enemies: SettingsStringDataType.bool,
    SettingsStringEnum.hard_level_progression: SettingsStringDataType.bool,
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
    SettingsStringEnum.high_req: SettingsStringDataType.bool,
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
    SettingsStringEnum.krusha_ui: KrushaUi,
    SettingsStringEnum.level_randomization: LevelRandomization,
    SettingsStringEnum.logic_type: LogicType,
    SettingsStringEnum.maximize_helm_blocker: SettingsStringDataType.bool,
    SettingsStringEnum.medal_cb_req: SettingsStringDataType.var_int,
    SettingsStringEnum.medal_requirement: SettingsStringDataType.var_int,
    SettingsStringEnum.microhints_enabled: MicrohintsEnabled,
    SettingsStringEnum.minigames_list_selected: SettingsStringDataType.list,
    SettingsStringEnum.misc_changes_selected: SettingsStringDataType.list,
    SettingsStringEnum.more_cutscene_skips: ExtraCutsceneSkips,
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
    SettingsStringEnum.troff_text: SettingsStringDataType.var_int,
    SettingsStringEnum.vanilla_door_rando: SettingsStringDataType.bool,
    SettingsStringEnum.warp_level_list_selected: SettingsStringDataType.list,
    SettingsStringEnum.warp_to_isles: SettingsStringDataType.bool,
    SettingsStringEnum.win_condition: WinCondition,
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
    SettingsStringEnum.choose_starting_moves: SettingsStringDataType.bool,
    SettingsStringEnum.starting_move_list_selected: SettingsStringDataType.list,
    SettingsStringEnum.start_with_slam: SettingsStringDataType.bool,
    SettingsStringEnum.spoiler_include_level_order: SettingsStringDataType.bool,
    SettingsStringEnum.enable_progressive_hints: SettingsStringDataType.bool,
    SettingsStringEnum.progressive_hint_text: SettingsStringDataType.var_int,
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
    SettingsStringEnum.puzzle_rando_difficulty: PuzzleRando,
}

# ALL LIST SETTINGS NEED AN ENTRY HERE!
# Another map for list settings, for the underlying data type of the list.
SettingsStringListTypeMap = {
    SettingsStringEnum.enemies_selected: Enemies,
    SettingsStringEnum.glitches_selected: GlitchesSelected,
    SettingsStringEnum.item_rando_list_selected: ItemRandoListSelected,
    SettingsStringEnum.minigames_list_selected: MinigamesListSelected,
    SettingsStringEnum.misc_changes_selected: MiscChangesSelected,
    SettingsStringEnum.starting_keys_list_selected: Items,
    SettingsStringEnum.warp_level_list_selected: Maps,
    SettingsStringEnum.hard_mode_selected: HardModeSelected,
    SettingsStringEnum.starting_move_list_selected: Items,
    SettingsStringEnum.random_starting_move_list_selected: Items,
    SettingsStringEnum.remove_barriers_selected: RemovedBarriersSelected,
    SettingsStringEnum.faster_checks_selected: FasterChecksSelected,
    SettingsStringEnum.hard_bosses_selected: HardBossesSelected,
}

# This map specifies the minimum and maximum values for numeric settings.
SettingsStringIntRangeMap = {}


def addSettingIntRange(settingEnum: SettingsStringEnum, maxVal: int, minVal: int = 0) -> None:
    """Add an entry to the SettingsStringIntRangeMap."""
    SettingsStringIntRangeMap[settingEnum] = {"max": maxVal, "min": minVal}


# ALL NUMERIC VAR_INT SETTINGS NEED AN ENTRY HERE!
# Minimum values only need to be supplied if they are negative.
addSettingIntRange(SettingsStringEnum.blocker_0, 201)
addSettingIntRange(SettingsStringEnum.blocker_1, 201)
addSettingIntRange(SettingsStringEnum.blocker_2, 201)
addSettingIntRange(SettingsStringEnum.blocker_3, 201)
addSettingIntRange(SettingsStringEnum.blocker_4, 201)
addSettingIntRange(SettingsStringEnum.blocker_5, 201)
addSettingIntRange(SettingsStringEnum.blocker_6, 201)
addSettingIntRange(SettingsStringEnum.blocker_7, 201)
addSettingIntRange(SettingsStringEnum.blocker_text, 201)
addSettingIntRange(SettingsStringEnum.coin_door_item_count, 201)
addSettingIntRange(SettingsStringEnum.crown_door_item_count, 201)
addSettingIntRange(SettingsStringEnum.helm_phase_count, 5)
addSettingIntRange(SettingsStringEnum.krool_key_count, 8)
addSettingIntRange(SettingsStringEnum.krool_phase_count, 5)
addSettingIntRange(SettingsStringEnum.medal_cb_req, 100)
addSettingIntRange(SettingsStringEnum.medal_requirement, 40)
addSettingIntRange(SettingsStringEnum.mermaid_gb_pearls, 5)
addSettingIntRange(SettingsStringEnum.rareware_gb_fairies, 20)
addSettingIntRange(SettingsStringEnum.starting_kongs_count, 5)
addSettingIntRange(SettingsStringEnum.starting_moves_count, 40)
addSettingIntRange(SettingsStringEnum.troff_0, 500)
addSettingIntRange(SettingsStringEnum.troff_1, 500)
addSettingIntRange(SettingsStringEnum.troff_2, 500)
addSettingIntRange(SettingsStringEnum.troff_3, 500)
addSettingIntRange(SettingsStringEnum.troff_4, 500)
addSettingIntRange(SettingsStringEnum.troff_5, 500)
addSettingIntRange(SettingsStringEnum.troff_6, 500)
addSettingIntRange(SettingsStringEnum.troff_text, 500)
addSettingIntRange(SettingsStringEnum.progressive_hint_text, 201)
addSettingIntRange(SettingsStringEnum.win_condition_count, 201)
