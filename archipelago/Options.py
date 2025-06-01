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

    display_name = "Krool In Boss Pool"


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
    """Determines what type of logic is needed to beat the seed."""

    display_name = "Logic Type"

    option_glitchless = 1
    option_glitched = 2
    default = 1


class GlitchesSelected(OptionList):
    """Determines what glitches are enabled if logic_type is set to Glitched.

    Valid Keys:
    "advanced_platforming": Platforming techniques that don't require any glitches but might be too tough for some players.
    "moonkicks": A trick that allows Donkey to ascend by interrupting his aerial attack with a kick.
    "phase_swimming": Formerly known as STVW, a trick to go through a significant amount of walls in the game whilst underwater.
    "swim_through_shores": A trick that allows you to swim into a sloped shoreline to get out of bounds.
    "troff_n_scoff_skips": Any skip that allows you to bypass the kong and small banana requirement in order to fight a boss.
    "moontail": A trick that allows the player to gain extra height with Diddy.
    """

    display_name = "Glitched Logic"
    valid_keys = {
        "advanced_platforming",
        "moonkicks",
        "phase_swimming",
        "swim_through_shores",
        "troff_n_scoff_skips",
        "moontail",
    }


class RingLink(Toggle):
    """Determines if the Ring Link is enabled.

    The easier waty to say this is Ammo link.
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
    medal_cb_req: MedalColorBananaRequirement
    mermaid_gb_pearls: MermaidRequirement
    medal_requirement: JetpacRequirement
    rareware_gb_fairies: RarewareGBRequirement
    open_lobbies: OpenLobbies
    switchsanity: SwitchSanity
    climbing_shuffle: ClimbingShuffle
    starting_kong_count: StartingKongCount
    starting_move_count: StartingMoveCount
    logic_type: LogicType
    glitches_selected: GlitchesSelected
    trap_fill_percentage: TrapFillPercentage
    bubble_trap_weight: BubbleTrapWeight
    reverse_trap_weight: ReverseTrapWeight
    slow_trap_weight: SlowTrapWeight
    receive_notifications: ReceiveNotifications
