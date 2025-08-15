"""Options for DK64R."""

from dataclasses import dataclass
import typing

from Options import Choice, PerGameCommonOptions, Range, Option, Toggle, DeathLink, DefaultOnToggle, OptionList

from randomizer.Enums.Settings import SettingsStringEnum
from randomizer.Enums.Settings import SettingsStringTypeMap
from randomizer.Enums.Settings import SettingsStringDataType
from randomizer.Enums.Settings import SettingsMap as DK64RSettingsMap


# DK64_TODO: Get Options from DK64R


class Goal(Choice):
    """Determines the goal of the seed."""

    display_name = "Goal"
    option_krool = 0
    option_all_keys = 1
    option_dk_rap = 2
    default = 0


class OpenLobbies(Toggle):
    """Determines whether or not all lobbies are preopened."""

    display_name = "Open Lobbies"


class ClimbingShuffle(Toggle):
    """Whether or not you shuffle the Climbing ability into the world(s)."""

    display_name = "Climbing Shuffle"


class StartingKongCount(Range):
    """Determines how many Kongs you start with."""

    display_name = "Starting Kong Count"
    range_start = 1
    range_end = 5
    default = 1


class StartingMoveCount(Range):
    """Determines how many additional random moves you start with. If you choose more moves than are available, you will start with all moves."""

    display_name = "Starting Move Count"
    range_start = 0
    range_end = 50
    default = 0


class KroolInBossPool(Toggle):
    """Whether or not K. Rool can be fightable in T&S Bosses and vice versa."""

    display_name = "K. Rool In Boss Pool"


class TrapFillPercentage(Range):
    """Replace a percentage of junk items in the item pool with random traps."""

    display_name = "Trap Fill Percentage"
    range_start = 0
    range_end = 100
    default = 0


class BaseTrapWeight(Choice):
    """Base Class for Trap Weights."""

    option_none = 0
    option_low = 1
    option_medium = 2
    option_high = 4
    default = 2


class ReceiveNotifications(Choice):
    """Determines if the player will receive notifications about item sends.

    Options:
    - display_all_speedup (1): If we have more than 5 items queued, we will speed up the display based on the percentage.
    - display_all_discard_extra (2): If we have more than 5 items queued, we will speed up the display based on percentage, but discard any non progression items.
    - display_all_fast (3): Displays ALL items at the fastest speed.
    - display_extra_fast (4): Displays Progression items at the default speed, and non progression items at a faster speed.
    - display_extra_items (5): Displays extra items and progression items at standard speed.
    - display_only_progression (6): Progression only, no speed changes.
    """

    display_name = "Receive Notifications Type"

    option_display_all_speedup = 1
    option_display_all_discard_extra = 2
    option_display_all_fast = 3
    option_display_extra_fast = 4
    option_display_extra_items = 5
    option_display_only_progression = 6
    option_display_nothing = 7
    default = 1


class BubbleTrapWeight(BaseTrapWeight):
    """Likelihood of receiving a trap which freezes the player."""

    display_name = "Bubble Trap Weight"


class ReverseTrapWeight(BaseTrapWeight):
    """Likelihood of receiving a trap which reverses controls."""

    display_name = "Reverse Trap Weight"


class SlowTrapWeight(BaseTrapWeight):
    """Likelihood of receiving a trap which slows the player."""

    display_name = "Slow Trap Weight"


class DisableAWeight(BaseTrapWeight):
    """Likelihood of receiving a trap which disables your A button."""

    display_name = "Disable A Trap"


class DisableBWeight(BaseTrapWeight):
    """Likelihood of receiving a trap which disables your B button."""

    display_name = "Disable B Trap"


class DisableZWeight(BaseTrapWeight):
    """Likelihood of receiving a trap which disables your Z button."""

    display_name = "Disable Z Trap"


class DisableCWeight(BaseTrapWeight):
    """Likelihood of receiving a trap which disables your C buttons."""

    display_name = "Disable C Trap"


class KroolPhaseCount(Range):
    """Pick how many phases are in the final battle against K. Rool."""

    display_name = "K. Rool Phase Count"
    range_start = 1
    range_end = 5
    default = 3


class HelmPhaseCount(Range):
    """Pick how many rooms needed to complete Helm."""

    display_name = "Helm Phase Count"
    range_start = 1
    range_end = 5
    default = 2


class MedalColorBananaRequirement(Range):
    """Determines how many CBs are needed to acquire Banana Medal."""

    display_name = "Medal CB Requirements"
    range_start = 1
    range_end = 100
    default = 40


class RarewareGBRequirement(Range):
    """Determines how many Fairies are needed to unlock the Rareware Door."""

    display_name = "Rareware GB Requirment"
    range_start = 1
    range_end = 20
    default = 4


class JetpacRequirement(Range):
    """Determines how many medals are needed to play Jetpac."""

    display_name = "Jetpac Requirement"
    range_start = 1
    range_end = 40
    default = 9


class MermaidRequirement(Range):
    """Determines how many pearls are needed to satisfy the mermaid."""

    display_name = "Mermaid Requirement"
    range_start = 1
    range_end = 5
    default = 1


class KeysRequiredToBeatKrool(Range):
    """Determines how many keys are needed to spawn Krool's Ship.

    Choosing a value of 0 means you start with all 8 keys.
    Choosing a value of 8 means you start with no keys.
    """

    display_name = "Keys Required to Beat Krool"
    range_start = 0
    range_end = 8
    default = 8


class SwitchSanity(Choice):
    """Determines if the pads leading to helm are randomized.

    Options:
    off: Switchsanity is Off
    helm_access: Monkeyport pad and Gorilla Gone Pad are randomized
    all: Most switches across the game are randomized.
    """

    display_name = "Switchsanity"

    option_off = 0
    option_helm_access = 1
    option_all = 2
    default = 0


class LogicType(Choice):
    """Determines what type of logic is needed to beat the seed.

    Options:
    glitchless: Logic is designed to be completed without glitches, mostly as intended by the developers.
    advanced_glitchless: Logic is designed to be completed without glitches, but allows for advanced techniques. Add tricks you want to put in logic in tricks_selected.
    glitched: Logic is designed to be completed with glitches. Add tricks you want to put in logic in tricks_selected, AND add glitches you want to put in logic in glitches_selected.
    """

    display_name = "Logic Type"

    option_glitchless = 1
    option_advanced_glitchless = 0
    option_glitched = 2
    default = 1


class TricksSelected(OptionList):
    """Determines what tricks are enabled if logic_type is set to Advanced Glitchless or Glitched.

    Valid Keys:
    "monkey_maneuvers": Platforming techniques that don't require any glitches but might be too tough for some players.
    "hard_shooting": Certain shooting checks that are harder will not require shooting aids, such as Homing Ammo and Sniper Scope.
    "advanced_grenading": Certain checks can be done with oranges (DK 5 Door Cabin, Japes Painting Room). In addition, change Fungi time of day with oranges.
    "slope_resets": Use kong ground attacks to climb steep slopes.
    """

    display_name = "Tricks Selected"
    valid_keys = {"monkey_maneuvers", "hard_shooting", "advanced_grenading", "slope_resets"}


class GlitchesSelected(OptionList):
    """Determines what glitches are enabled if logic_type is set to Glitched.

    Valid Keys:
    "moonkicks": A trick that allows Donkey to ascend by interrupting his aerial attack with a kick.
    "phase_swimming": Formerly known as STVW, a trick to go through a significant amount of walls in the game whilst underwater.
    "swim_through_shores": A trick that allows you to swim into a sloped shoreline to get out of bounds.
    "troff_n_scoff_skips": Any skip that allows you to bypass the kong and small banana requirement in order to fight a boss.
    "moontail": A trick that allows the player to gain extra height with Diddy.
    """

    display_name = "Glitches Selected"
    valid_keys = {
        "moonkicks",
        "phase_swimming",
        "swim_through_shores",
        "troff_n_scoff_skips",
        "moontail",
    }


class RingLink(Toggle):
    """Determines if the Ring Link is enabled.

    The easier way to say this is Ammo link.
    If enabled, all ammo types are shared between players.

    Currently for Film and Crystal Coconuts if you gain any above the base amount from ringlink, we will not provide more.
    But you can still gain more ammo from the world, and it will be shared.
    """

    display_name = "Ring Link"


class TagLink(Toggle):
    """Determines if the Tag Link is enabled.

    If enabled, if you have another players kong you will tag to that kong as well.
    If you don't have that kong, you will randomly tag to another kong.
    If you only have one kong, nothing will happen.
    """

    display_name = "Tag Link"


class MirrorMode(Toggle):
    """Determines whether the game will be horizontally Mirrored."""

    display_name = "Mirror Mode"


class HardModeEnabled(Toggle):
    """Determines whether Hard Mode is enabled. Use the yaml option below this to determine which settings you want enabled."""

    display_name = "Hard Mode Enabled"


class HardModeSelected(OptionList):
    """If Hard Mode is enabled, determines which Hard Mode settings are included.

    Valid Keys:
    "hard_enemies": Enemies Fight Back a little harder.
    "shuffled_jetpac_enemies": Jetpac enemies are shuffled within Jetpac.
    "strict_helm_timer": Helm Timer starts at 0:00 requiring blueprints to turn in
    "donk_in_the_dark_world: All maps are pitch black, with only a light to help you path your way to the end of the game. Mixing this with 'Donk in the Sky' will convert the challenge into 'Memory Challenge' instead.
    "donk_in_the_sky": Collision Geometry is disabled. Mixing this with 'Donk in the Dark World' will convert the challenge into 'Memory Challenge' instead.
    """

    display_name = "Hard Mode Options"

    valid_keys = {
        "hard_enemies",
        "shuffled_jetpac_enemies",
        "strict_helm_timer",
        "donk_in_the_dark_world",
        "donk_in_the_sky",
    }


class RemoveBarriers(OptionList):
    """Determines which barriers are removed.

    Valid Keys:
    "japes_coconut_gates"
    "japes_shellhive_gates"
    "aztec_tunnel_door"
    "aztec_5dtemple_switches"
    "aztec_llama_switches"
    "aztec_tiny_temple_ice"
    "factory_testing_gate"
    "factory_production_room"
    "galleon_lighthouse_gate"
    "galleon_shipyard_area_gate"
    "galleon_seasick_ship"
    "galleon_treasure_room"
    "forest_green_tunnel"
    "forest_yellow_tunnel"
    "caves_igloo_pads"
    "caves_ice_walls"
    "castle_crypt_doors"
    """

    display_name = "Removed Barriers"

    valid_keys = {
        "japes_coconut_gates",
        "japes_shellhive_gates",
        "aztec_tunnel_door",
        "aztec_5dtemple_switches",
        "aztec_llama_switches",
        "aztec_tiny_temple_ice",
        "factory_testing_gate",
        "factory_production_room",
        "galleon_lighthouse_gate",
        "galleon_shipyard_area_gate",
        "galleon_seasick_ship",
        "galleon_treasure_room",
        "forest_green_tunnel",
        "forest_yellow_tunnel",
        "caves_igloo_pads",
        "caves_ice_walls",
        "castle_crypt_doors",
    }


class HintItemRandomization(Toggle):
    """Determines if Hints are added into the Item Pool."""

    display_name = "Randomize Hint"


class RandomizeBlockers(Toggle):
    """Determines if B. Locker values are randomized."""

    display_name = "Randomizer B. Lockers"
    default = True


class MaximumBLocker(Range):
    """Determines the Maximum Value for B. Lockers if Randomize B.Lockers are enabled."""

    display_name = "Randomizer B. Lockers"
    range_start = 0
    range_end = 201
    default = 64


class ChaosBLockers(Toggle):
    """If Randomize B. Lockers is also enabled, determines if B. Lockers may require non-Golden Banana collectibles."""

    display_name = "Chaos B. Lockers"


class Level1Blocker(Range):
    """Determines the value of Level 1's B. Locker if Randomize B. Lockers are turned off."""

    range_start = 0
    range_end = 201
    default = 0


class Level2Blocker(Range):
    """Determines the value of Level 2's B. Locker if Randomize B. Lockers are turned off."""

    range_start = 0
    range_end = 201
    default = 0


class Level3Blocker(Range):
    """Determines the value of Level 3's B. Locker if Randomize B. Lockers are turned off."""

    range_start = 0
    range_end = 201
    default = 0


class Level4Blocker(Range):
    """Determines the value of Level 4's B. Locker if Randomize B. Lockers are turned off."""

    range_start = 0
    range_end = 201
    default = 0


class Level5Blocker(Range):
    """Determines the value of Level 5's B. Locker if Randomize B. Lockers are turned off."""

    range_start = 0
    range_end = 201
    default = 0


class Level6Blocker(Range):
    """Determines the value of Level 6's B. Locker if Randomize B. Lockers are turned off."""

    range_start = 0
    range_end = 201
    default = 0


class Level7Blocker(Range):
    """Determines the value of Level 7's B. Locker if Randomize B. Lockers are turned off."""

    range_start = 0
    range_end = 201
    default = 0


class Level8Blocker(Range):
    """Determines the value of Level 8's B. Locker if Randomize B. Lockers are turned off."""

    range_start = 0
    range_end = 201
    default = 64


class BouldersInPool(Toggle):
    """Determines if throwing boulders/barrels spawn a check."""

    display_name = "Boulders in Pool"


class Dropsanity(Toggle):
    """Determines if Enemy Drops are added into the pool."""

    display_name = "Dropsanity"


class ChaosRatio(Range):
    """If Chaos Blockers are enabled, determine the max percentage of collectibles than can roll onto a BLocker.

    Example:
    There are 16 Rainbow Coins in the game. With a chaos ratio of 50%, a max BLocker can have a max of 8 rainbow coins.
    Excludes Bean and Company Coins.
    """

    display_name = "Chaos Ratio"

    range_start = 1
    range_end = 100
    default = 32


class ShopKeepers(Toggle):
    """Determines if Cranky, Funky, Candy, and Snide are added into the item pool. Shops will be inaccessible unless you collect its shop keeper."""

    display_name = "Shop Keepers in Pool"


@dataclass
class DK64Options(PerGameCommonOptions):
    """Options for DK64R."""

    death_link: DeathLink
    ring_link: RingLink
    tag_link: TagLink
    goal: Goal
    krool_key_count: KeysRequiredToBeatKrool
    krool_phase_count: KroolPhaseCount
    helm_phase_count: HelmPhaseCount
    krool_in_boss_pool: KroolInBossPool
    remove_barriers_selected: RemoveBarriers
    medal_cb_req: MedalColorBananaRequirement
    mermaid_gb_pearls: MermaidRequirement
    medal_requirement: JetpacRequirement
    rareware_gb_fairies: RarewareGBRequirement
    randomize_blocker_required_amounts: RandomizeBlockers
    blocker_max: MaximumBLocker
    enable_chaos_blockers: ChaosBLockers
    chaos_ratio: ChaosRatio
    level1_blocker: Level1Blocker
    level2_blocker: Level2Blocker
    level3_blocker: Level3Blocker
    level4_blocker: Level4Blocker
    level5_blocker: Level5Blocker
    level6_blocker: Level6Blocker
    level7_blocker: Level7Blocker
    level8_blocker: Level8Blocker
    open_lobbies: OpenLobbies
    switchsanity: SwitchSanity
    climbing_shuffle: ClimbingShuffle
    starting_kong_count: StartingKongCount
    starting_move_count: StartingMoveCount
    shopowners_in_pool: ShopKeepers
    logic_type: LogicType
    tricks_selected: TricksSelected
    glitches_selected: GlitchesSelected
    hard_mode: HardModeEnabled
    hard_mode_selected: HardModeSelected
    mirror_mode: MirrorMode
    hints_in_item_pool: HintItemRandomization
    boulders_in_pool: BouldersInPool
    dropsanity: Dropsanity
    trap_fill_percentage: TrapFillPercentage
    bubble_trap_weight: BubbleTrapWeight
    reverse_trap_weight: ReverseTrapWeight
    slow_trap_weight: SlowTrapWeight
    disable_a_trap: DisableAWeight
    disable_b_trap: DisableBWeight
    disable_c_trap: DisableCWeight
    disable_z_trap: DisableZWeight
    receive_notifications: ReceiveNotifications
