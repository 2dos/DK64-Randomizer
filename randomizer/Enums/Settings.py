"""File containing enums to represent all settings."""
from enum import IntEnum, auto

from randomizer.Enums.Items import Items
from randomizer.Lists.EnemyTypes import Enemies
from randomizer.Lists.MapsAndExits import Maps

# Each select-based setting should have its own associated enum class. The enum
# values should exactly match the input values in the HTML (not the IDs).

# Randomizers


class LogicType(IntEnum):
    """The logic use to place items in the seed.

    glitchless: No glitches will be required.
    glitch: Some glitches may be required.
    nologic: The seed may not be beatable.
    """

    glitchless = auto()
    glitch = auto()
    nologic = auto()


class GlitchesSelected(IntEnum):
    """Glitch categories that can be selected for the seed logic.

    These values are tied to the GlitchSelector in randomizer.Lists.Logic. More
    details on each can be found in that file.
    """

    advanced_platforming = auto()
    b_locker_skips = auto()
    boulder_clips = auto()
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


class ActivateAllBananaports(IntEnum):
    """Whether bananaports should start as activated, and where.

    This enum is explicitly indexed for use in ApplyRandomizer.py. Do not
    change these enum values.

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

    vanilla = auto()
    level_order = auto()
    loadingzone = auto()
    loadingzonesdecoupled = auto()


# TODO: merge this with the Types enum.
class ItemRandoListSelected(IntEnum):
    """Item categories that may be randomized.

    These values are tied to the ItemRandoSelector in randomizer.Enums.Types.
    The presence of "beanpearl" requires a different enum from Types.
    """

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
    """Determines if and how Kasplats are randomized.

    off: Kasplats are in their original locations with original blueprints.
    vanilla_locations: Kasplats are shuffled between the locations that exist
        in the vanilla game.
    location_shuffle: Kasplats will be shuffled between all possible locations,
        including new ones not in the vanilla game.
    """

    off = auto()
    vanilla_locations = auto()
    location_shuffle = auto()


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

    off = auto()
    on = auto()
    cross_purchase = auto()
    start_with = auto()
    item_shuffle = auto()


class TrainingBarrels(IntEnum):
    """Determines if and how training barrels are randomized.

    normal: Training barrels give the vanilla moves.
    shuffled: Training moves are shuffled into the item pool, and the training
        barrels gives four random moves.
    """

    normal = auto()
    shuffled = auto()


class RandomPrices(IntEnum):
    """Determines how and if shop prices are randomized.

    vanilla: Shop prices are the same as the vanilla game.
    free: All items are free.
    low: Moves cost 1-4 coins most of the time.
    medium: Moves cost 1-8 coins most of the time.
    high: Moves cost 1-12 coins most of the time.
    extreme: Moves cost 10+ coins most of the time.
    """

    vanilla = auto()
    free = auto()
    low = auto()
    medium = auto()
    high = auto()
    extreme = auto()


class ShockwaveStatus(IntEnum):
    """Determines how Banana Fairy Isle is handled.

    vanilla: Camera and Shockwave are given.
    shuffled: Camera and Shockwave are shuffled into the move pool as a single
        item. BFI has a shared or Tiny reward.
    shuffled_decoupled: Camera and Shockwave are shuffled into the move pool as
        separate items. BFI has a shared or Tiny reward.
    start_with: Player starts with Camera and Shockwave. BFI has nothing.
    """

    vanilla = auto()
    shuffled = auto()
    shuffled_decoupled = auto()
    start_with = auto()


class BananaportRando(IntEnum):
    """Determines how bananaports are shuffled.

    off: Bananaports have their vanilla locations.
    in_level: Bananaport warps are shuffled within their own levels.
    crossmap_coupled: Bananaport warps are shuffled among all bananaports in
        all levels.
    crossmap_decoupled: Same as crossmap_coupled, but going back through one
        bananaport may not take you to the same location.
    """

    off = auto()
    in_level = auto()
    crossmap_coupled = auto()
    crossmap_decoupled = auto()


# Overworld


class MinigamesListSelected(IntEnum):
    """Minigame categories used for the web selector.

    These values are tied to the MinigameSelector in randomizer.Lists.Minigame.
    More details on each can be found in that file.
    """

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


class WinCondition(IntEnum):
    """The condition needed to complete the game.

    This enum is explicitly indexed for use in ApplyRandomizer.py. Do not
    change these enum values.

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

    none = auto()
    not_blueprints = auto()
    major_collectibles = auto()


class KrushaUi(IntEnum):
    """Which Kong model will be replaced with Krusha."""

    no_slot = auto()
    dk = auto()
    diddy = auto()
    lanky = auto()
    tiny = auto()
    chunky = auto()
    random = auto()


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
    """The damage multipler.

    default: Normal damage.
    double: Damage is 2x normal.
    quad: Damage is 4x normal.
    ohko: Damage is 12x normal (one hit kills).
    """

    default = auto()
    double = auto()
    quad = auto()
    ohko = auto()


class CrownEnemyRando(IntEnum):
    """Determines the difficulty of enemies in Battle Arenas."""

    off = auto()
    easy = auto()
    medium = auto()
    hard = auto()


# Quality of Life


class MiscChangesSelected(IntEnum):
    """Various quality of life fixes that can be applied.

    These values are tied to the QoLSelector in randomizer.Lists.QoL. More
    details on each can be found in that file.
    """

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
    """Whether or not Wrinkly hints are replaced with useful randomizer hints.

    off: Hints are the same as the vanilla game.
    standard: Normal randomizer hints are provided.
    cryptic: Cryptic randomizer hints are provided.
    """

    off = auto()
    standard = auto()
    cryptic = auto()


class HelmSetting(IntEnum):
    """Determines where the player starts when entering Hideout Helm.

    This enum is explicitly indexed for use in ApplyRandomizer.py. Do not
    change these enum values.

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
    change these enum values.

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

    off: Normal colors.
    prot: Setting for protanomaly/protanopia (red/green color blindness,
        biased toward red).
    deut: Setting for deuteranomaly/deuteranopia (red/green color blindness,
        biased toward green).
    trit: Setting for tritanomaly/tritanopia (blue/yellow color blindness).
    """

    off = auto()
    prot = auto()
    deut = auto()
    trit = auto()


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
