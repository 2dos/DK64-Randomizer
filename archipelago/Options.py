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
    default = 0


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


@dataclass
class DK64Options(PerGameCommonOptions):
    """Options for DK64R."""

    death_link: DeathLink
    receive_notifications: ReceiveNotifications
    goal: Goal
    climbing_shuffle: ClimbingShuffle
    starting_kong_count: StartingKongCount
    starting_move_count: StartingMoveCount
    trap_fill_percentage: TrapFillPercentage
    bubble_trap_weight: BubbleTrapWeight
    reverse_trap_weight: ReverseTrapWeight
    slow_trap_weight: SlowTrapWeight
