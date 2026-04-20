"""Options for DK64R."""

from dataclasses import dataclass
import numbers
import typing

from BaseClasses import PlandoOptions
from Options import Choice, PerGameCommonOptions, Range, Option, OptionDict, OptionError, OptionList, Toggle, DeathLink, DefaultOnToggle, OptionGroup, TextChoice
from typing import List
from randomizer.Enums.Settings import SettingsStringEnum
from randomizer.Enums.Settings import SettingsStringTypeMap
from randomizer.Enums.Settings import SettingsStringDataType
from randomizer.Enums.Settings import SettingsMap as DK64RSettingsMap
from worlds.AutoWorld import World

# DK64_TODO: Get Options from DK64R


class Goal(Choice):
    """Determines the goal of the seed.

    Options:
    - acquire_keys_3_and_8: Acquire both Keys 3 and Key 8 to win.
    - acquire_key_8: Win by obtaining Key 8, which is normally found at the end of Hideout Helm.
    - kremling_kapture: Take a picture of every enemy to win.
    - dk_rap: Obtain all items mentioned in the DK Rap to win.
    - golden_bananas: Find a certain number of Golden Bananas to win. See goal_quantity option for more info.
    - blueprints: Find a certain number of Blueprints to win. See goal_quantity option for more info.
    - company_coins: Find the Nintendo and/or Rareware Coin to win. See goal_quantity option for more info.
    - keys: Find a certain number of Boss Keys to win. See goal_quantity option for more info.
    - medals: Find a certain number of Banana Medals to win. See goal_quantity option for more info.
    - crowns: Find a certain number of Battle Crowns to win. See goal_quantity option for more info.
    - fairies: Find a certain number of Banana Fairies to win. See goal_quantity option for more info.
    - rainbow_coins: Find a certain number of Rainbow Coins to win. See goal_quantity option for more info.
    - bean: Find The Bean to win.
    - pearls: Find a certain number of Pearls to win. See goal_quantity option for more info.
    - bosses: Defeat a certain number of bosses to win. See goal_quantity option for more info.
    - bonuses: Complete a certain number of Bonus Barrels to win. Automatically disables auto_complete_bonus_barrels if set. See goal_quantity option for more info.
    - treasure_hurry: Run down the timer by collecting treasure! You win when the timer reaches 0. If you beat Helm, the wincon automatically changes to beating K. Rool.
    - krools_challenge: K. Rool's ship does not spawn until you collect All keys, Defeat All bosses, Play all Bonus Barrels, and collect All Blueprints.
    - kill_the_rabbit: Kill the rabbit in Chunky's igloo in Caves. Turn it to Ash. Simple as that.
    """

    display_name = "Goal"
    option_acquire_keys_3_and_8 = 0
    option_acquire_key_8 = 1
    option_kremling_kapture = 2
    option_dk_rap = 3
    option_golden_bananas = 4
    option_blueprints = 5
    option_company_coins = 6
    option_keys = 7
    option_medals = 8
    option_crowns = 9
    option_fairies = 10
    option_rainbow_coins = 11
    option_bean = 12
    option_pearls = 13
    option_bosses = 14
    option_bonuses = 15
    option_treasure_hurry = 16
    option_krools_challenge = 17
    option_kill_the_rabbit = 18
    default = 7


class GoalQuantity(OptionDict):
    """Determines how many of a particular item you need to goal.

    You can set multiple values to account for any win conditions above, but it will only use the one that matches the win condition.
    (i.e. if you set your win condition to "blueprints", the "keys" field will be ignored) This is useful in case you randomize your win condition.

    Valid Keys:
    - "golden_bananas"
    - "blueprints"
    - "company_coins"
    - "keys"
    - "medals"
    - "crowns"
    - "fairies"
    - "rainbow_coins"
    - "pearls"
    - "bosses"
    - "bonuses"

    Valid Values:
    - a number from 1 to the maximum value for the key type
    - "random", which will pick a random valid value for you
    - a range in the form "x-y", which will pick a random valid value between x and y
    """

    min = 1
    max_values_dict: dict[str, int] = {
        "golden_bananas": 201,
        "blueprints": 40,
        "company_coins": 2,
        "keys": 8,
        "medals": 40,
        "crowns": 10,
        "fairies": 20,
        "rainbow_coins": 16,
        "pearls": 5,
        "bosses": 7,
        "bonuses": 53,
    }

    def verify(self, world: type[World], player_name: str, plando_options: PlandoOptions) -> None:
        """Verify Goal Quantity."""
        super(GoalQuantity, self).verify(world, player_name, plando_options)

        for key in self.value.keys():
            if key not in self.max_values_dict.keys():
                raise OptionError(f"{key} is not a valid key for goal_quantity.")

        accumulated_errors = []

        for key, value in self.value.items():
            print(f"Checking {key}: {value}")
            max = self.max_values_dict[key]
            if isinstance(value, numbers.Integral):
                value = int(value)
                if value > max:
                    accumulated_errors.append(f"{key}: {value} is higher than maximum allowed value {max}")
                elif value < self.min:
                    accumulated_errors.append(f"{key}: {value} is lower than minimum allowed value {self.min}")
            else:
                if value == "random":
                    continue
                split = value.split("-")
                if len(split) != 2:
                    accumulated_errors.append(f'{key}: {value} is not an integer or range, nor is it "random".')
                else:
                    for bound in split:
                        try:
                            bound = int(bound)
                        except (ValueError, TypeError):
                            accumulated_errors.append(f'{key}: {value} is not an integer or range, nor is it "random".')
                            continue
                        if bound > max:
                            accumulated_errors.append(f"{key}: Upper edge of range {bound} is higher than maximum allowed value {max}")
                        elif bound < self.min:
                            accumulated_errors.append(f"{key}: Lower edge of range {bound} is lower than minimum allowed value {self.min}")
        print("\n".join(accumulated_errors))
        if accumulated_errors:
            raise OptionError("Found errors with option goal_quantity:\n" + "\n".join(accumulated_errors))

    default = {"golden_bananas": 100, "blueprints": 20, "company_coins": 2, "keys": 8, "medals": 15, "crowns": 5, "fairies": 15, "rainbow_coins": 10, "pearls": 3, "bosses": 7, "bonuses": 15}


class OpenLobbies(Toggle):
    """Determines whether or not all lobbies are preopened."""

    display_name = "Open Lobbies"


class ClimbingShuffle(Toggle):
    """Whether or not you shuffle the Climbing ability into the world(s)."""

    display_name = "Climbing Shuffle"


class CannonShuffle(Toggle):
    """Whether or not you shuffle the Cannon ability into the world(s)."""

    display_name = "Cannon Shuffle"


class StartingKongCount(Range):
    """Determines how many Kongs you start with."""

    display_name = "Starting Kong Count"
    range_start = 1
    range_end = 5
    default = 1


_STARTING_MOVE_VALID_KEYS = frozenset(
    {
        # Training barrel basics
        "Vines",
        "Diving",
        "Oranges",
        "Barrels",
        # Kong abilities
        "Baboon Balloon",
        "Baboon Blast",
        "Chimpy Charge",
        "Gorilla Gone",
        "Gorilla Grab",
        "Hunky Chunky",
        "Mini Monkey",
        "Monkeyport",
        "Orangstand",
        "Orangstand Sprint",
        "Pony Tail Twirl",
        "Primate Punch",
        "Rocketbarrel Boost",
        "Simian Spring",
        "Strong Kong",
        # Weapons
        "Coconut",
        "Feather",
        "Grape",
        "Homing Ammo",
        "Peanut",
        "Pineapple",
        "Sniper Sight",
        # Instruments
        "Bongos",
        "Guitar",
        "Saxophone",
        "Triangle",
        "Trombone",
        # Progressive upgrades (can appear multiple times in a pool list for multiple copies)
        "Progressive Ammo Belt",
        "Progressive Instrument Upgrade",
        "Progressive Slam",
        # Shockwave
        "Camera and Shockwave",
        "Fairy Camera",
        "Shockwave",
        # Special moves
        "Climbing",
        "Cannons",
        # Shopkeepers
        "Cranky",
        "Funky",
        "Candy",
        "Snide",
        # Keys
        "Key 1",
        "Key 2",
        "Key 3",
        "Key 4",
        "Key 5",
        "Key 6",
        "Key 7",
        "Key 8",
        # Time of day
        "Day",
        "Night",
    }
)


class _BaseStartingMovePool(OptionList):
    """Base class for starting move pool item lists."""

    valid_keys = _STARTING_MOVE_VALID_KEYS


class StartingMovePool1(_BaseStartingMovePool):
    """Items available in starting move Pool 1. A random selection of this pool will be given at game start.

    Progressive items (Progressive Slam, Progressive Ammo Belt, Progressive Instrument Upgrade)
    can be listed multiple times to include multiple copies.
    """

    display_name = "Starting Move Pool 1 Items"
    default = [
        "Vines",
        "Diving",
        "Oranges",
        "Barrels",
        "Baboon Balloon",
        "Baboon Blast",
        "Chimpy Charge",
        "Gorilla Gone",
        "Gorilla Grab",
        "Hunky Chunky",
        "Mini Monkey",
        "Monkeyport",
        "Orangstand",
        "Orangstand Sprint",
        "Pony Tail Twirl",
        "Primate Punch",
        "Rocketbarrel Boost",
        "Simian Spring",
        "Strong Kong",
        "Coconut",
        "Feather",
        "Grape",
        "Homing Ammo",
        "Peanut",
        "Pineapple",
        "Sniper Sight",
        "Bongos",
        "Guitar",
        "Saxophone",
        "Triangle",
        "Trombone",
        "Progressive Slam",
        "Progressive Slam",
        "Camera and Shockwave",
        "Shockwave",
        "Cannons",
    ]


class StartingMovePool1Count(Range):
    """How many items to randomly give from Starting Move Pool 1 at game start.

    Values larger than the pool size will give all items in the pool.
    """

    display_name = "Starting Move Pool 1 Count"
    range_start = 0
    range_end = 999
    default = 3


class StartingMovePool2(_BaseStartingMovePool):
    """Items available in starting move Pool 2. A selection of this pool will be given at game start.

    By default contains bait potions, Fairy Camera, Snide, and one Progressive Slam.
    Count defaults to 999 (give all items).
    """

    display_name = "Starting Move Pool 2 Items"
    default = [
        "Climbing",
        "Progressive Ammo Belt",
        "Progressive Instrument Upgrade",
        "Fairy Camera",
        "Snide",
        "Progressive Slam",
    ]


class StartingMovePool2Count(Range):
    """How many items to give from Starting Move Pool 2 at game start.

    Defaults to 999 (give all items in pool).
    """

    display_name = "Starting Move Pool 2 Count"
    range_start = 0
    range_end = 999
    default = 999


class StartingMovePool3(_BaseStartingMovePool):
    """Items available in starting move Pool 3. A selection of this pool will be given at game start.

    By default contains the shopkeepers (Cranky, Funky, Candy).
    """

    display_name = "Starting Move Pool 3 Items"
    default = ["Cranky", "Funky", "Candy"]


class StartingMovePool3Count(Range):
    """How many items to give from Starting Move Pool 3 at game start."""

    display_name = "Starting Move Pool 3 Count"
    range_start = 0
    range_end = 999
    default = 2


class StartingMovePool4(_BaseStartingMovePool):
    """Items available in starting move Pool 4. A selection of this pool will be given at game start.

    By default contains extra bait potion copies (one Ammo Belt + two Instrument Upgrades).
    """

    display_name = "Starting Move Pool 4 Items"
    default = [
        "Progressive Ammo Belt",
        "Progressive Instrument Upgrade",
        "Progressive Instrument Upgrade",
    ]


class StartingMovePool4Count(Range):
    """How many items to give from Starting Move Pool 4 at game start."""

    display_name = "Starting Move Pool 4 Count"
    range_start = 0
    range_end = 999
    default = 0


class StartingMovePool5(_BaseStartingMovePool):
    """Items available in starting move Pool 5. A selection of this pool will be given at game start.

    Empty by default. Use this as a custom pool for any additional starting moves.
    """

    display_name = "Starting Move Pool 5 Items"
    default = []


class StartingMovePool5Count(Range):
    """How many items to give from Starting Move Pool 5 at game start."""

    display_name = "Starting Move Pool 5 Count"
    range_start = 0
    range_end = 999
    default = 0


class KroolShuffle(Choice):
    """Whether or not K. Rool can be fightable in T&S Bosses and vice versa.

    "off": K. Rool can only appear in the final fight.
    "krool_only": K. Rool can appear in T&S bosses, but T&S can't appear in the final fight.
    "full_shuffle": K. Rool and T&S bosses can be shuffled between eachother.
    """

    display_name = "K. Rool In Boss Pool"

    option_off = 0
    option_krool_only = 1
    option_full_shuffle = 2

    default = 0


class AllowedBosses(OptionList):
    """Determines which bosses are in the pool. If not enough bosses are selected, it will fill the pool with duplicate bosses."""

    display_name = "Allowed Bosses"

    valid_keys: {"Armydillo 1", "Dogadon 1", "Mad Jack", "Pufftoss", "Dogadon 2", "Armydillo 2", "Kutout", "DK phase", "Diddy Phase", "Lanky Phase", "Tiny Phase", "Chunky Phase"}
    default = ["Armydillo 1", "Dogadon 1", "Mad Jack", "Pufftoss", "Dogadon 2", "Armydillo 2", "Kutout", "DK phase", "Diddy Phase", "Lanky Phase", "Tiny Phase", "Chunky Phase"]


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
    - display_all_fast: Displays ALL items at the fastest speed.
    - display_only_progression: Displays only progression items at the fastest speed.
    - display_nothing: No item notifications.
    """

    display_name = "Receive Notifications Type"

    option_display_all_fast = 1
    option_display_only_progression = 2
    option_display_nothing = 3
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

    display_name = "Disable A Trap Weight"


class DisableBWeight(BaseTrapWeight):
    """Likelihood of receiving a trap which disables your B button."""

    display_name = "Disable B Trap Weight"


class DisableZWeight(BaseTrapWeight):
    """Likelihood of receiving a trap which disables your Z button."""

    display_name = "Disable Z Trap Weight"


class DisableCWeight(BaseTrapWeight):
    """Likelihood of receiving a trap which disables your C buttons."""

    display_name = "Disable C Trap Weight"


class GetOutTrapWeight(BaseTrapWeight):
    """Likelihood of receiving a trap which tells you to Get Out."""

    display_name = "Get Out Trap Weight"


class DryTrapWeight(BaseTrapWeight):
    """Likelihood of receiving a trap which removes all of your consumables."""

    display_name = "Dry Trap Weight"


class FlipTrapWeight(BaseTrapWeight):
    """Likelihood of receiving a trap which flips the camera."""

    display_name = "Flip Trap Weight"


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


class MedalDistribution(Choice):
    """Determines how the CB requirement is determined.

    Options:
    pre_selected: Player chooses a specific value for CB requirements
    easy_random: Random values are chosen with an easier progression curve
    medium_random: Random values are chosen with a medium progression curve
    hard_random: Random values are chosen with a hard progression curve
    progressive: CB requirements increase progressively through levels depending on your medal_cb_requirement.
    """

    display_name = "CB Requirement Setting"
    option_pre_selected = 0
    option_easy_random = 1
    option_medium_random = 2
    option_hard_random = 3
    option_progressive = 4
    default = 0


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


class NumberOfStartingKeys(Range):
    """Determines how many keys are pregiven.

    Choosing a value of 0 means you start with 0 keys.
    Choosing a value of 8 means you start with all 8 keys.
    """

    display_name = "Amount of Pregiven Keys"
    range_start = 0
    range_end = 8
    default = 0


class RequireBeatingKrool(DefaultOnToggle):
    """Require defeating K. Rool in addition to the win condition requirements.

    K. Rool's ship will not spawn until you meet your win condition requirements, and you must defeat K. Rool to win.
    Automatically enabled for Krool's Challenge. Automatically disabled for Kill the Rabbit.
    """

    display_name = "Require Beating K. Rool"


class SwitchsanityOptions(OptionDict):
    """Customizes each Switchsanity switch individually.

    Set each switch to the kong that controls it, or "off" to leave it at its vanilla assignment.

    Kong switches accept: "off", "donkey", "diddy", "lanky", "tiny", "chunky", "random", "any"
    The isles_helm_lobby switch (Gorilla Gone pad) also accepts:
        "bongos", "guitar", "trombone", "sax", "triangle", "lever", "gong", "gone_pad"

    Switch keys (one per switch across all levels):
    - isles_to_kroc_top, isles_helm_lobby, isles_aztec_lobby_back_room
    - isles_fungi_lobby_fairy, isles_spawn_rocketbarrel
    - japes_to_hive, japes_to_rambi, japes_to_painting_room, japes_to_cavern, japes_free_kong
    - aztec_to_kasplat_room, aztec_llama_front, aztec_llama_side, aztec_llama_back
    - aztec_sand_tunnel, aztec_to_connector_tunnel, aztec_free_lanky, aztec_free_tiny
    - aztec_gong_tower, aztec_lobby_gong
    - factory_free_kong, factory_dark_grate, factory_bonus_grate, factory_monster_grate
    - galleon_to_lighthouse_side, galleon_to_shipwreck_side, galleon_to_cannon_game
    - fungi_yellow_tunnel, fungi_green_tunnel_near, fungi_green_tunnel_far
    - caves_gone_cave, caves_snide_cave, caves_boulder_cave, caves_lobby_blueprint, caves_lobby_lava
    """

    display_name = "Switchsanity"

    KONG_SWITCHES = frozenset(
        [
            "isles_to_kroc_top",
            "isles_aztec_lobby_back_room",
            "isles_fungi_lobby_fairy",
            "isles_spawn_rocketbarrel",
            "japes_to_hive",
            "japes_to_rambi",
            "japes_to_painting_room",
            "japes_to_cavern",
            "japes_free_kong",
            "aztec_to_kasplat_room",
            "aztec_llama_front",
            "aztec_llama_side",
            "aztec_llama_back",
            "aztec_sand_tunnel",
            "aztec_to_connector_tunnel",
            "aztec_free_lanky",
            "aztec_free_tiny",
            "aztec_gong_tower",
            "aztec_lobby_gong",
            "factory_free_kong",
            "factory_dark_grate",
            "factory_bonus_grate",
            "factory_monster_grate",
            "galleon_to_lighthouse_side",
            "galleon_to_shipwreck_side",
            "galleon_to_cannon_game",
            "fungi_yellow_tunnel",
            "fungi_green_tunnel_near",
            "fungi_green_tunnel_far",
            "caves_gone_cave",
            "caves_snide_cave",
            "caves_boulder_cave",
            "caves_lobby_blueprint",
            "caves_lobby_lava",
        ]
    )
    GONE_SWITCHES = frozenset(["isles_helm_lobby"])
    valid_keys = KONG_SWITCHES | GONE_SWITCHES

    KONG_VALUES = frozenset(["off", "donkey", "diddy", "lanky", "tiny", "chunky", "random", "any"])
    GONE_VALUES = frozenset(["off", "bongos", "guitar", "trombone", "sax", "triangle", "lever", "gong", "gone_pad", "random"])

    default = {
        "isles_to_kroc_top": "off",
        "isles_helm_lobby": "off",
        "isles_aztec_lobby_back_room": "off",
        "isles_fungi_lobby_fairy": "off",
        "isles_spawn_rocketbarrel": "off",
        "japes_to_hive": "off",
        "japes_to_rambi": "off",
        "japes_to_painting_room": "off",
        "japes_to_cavern": "off",
        "japes_free_kong": "off",
        "aztec_to_kasplat_room": "off",
        "aztec_llama_front": "off",
        "aztec_llama_side": "off",
        "aztec_llama_back": "off",
        "aztec_sand_tunnel": "off",
        "aztec_to_connector_tunnel": "off",
        "aztec_free_lanky": "off",
        "aztec_free_tiny": "off",
        "aztec_gong_tower": "off",
        "aztec_lobby_gong": "off",
        "factory_free_kong": "off",
        "factory_dark_grate": "off",
        "factory_bonus_grate": "off",
        "factory_monster_grate": "off",
        "galleon_to_lighthouse_side": "off",
        "galleon_to_shipwreck_side": "off",
        "galleon_to_cannon_game": "off",
        "fungi_yellow_tunnel": "off",
        "fungi_green_tunnel_near": "off",
        "fungi_green_tunnel_far": "off",
        "caves_gone_cave": "off",
        "caves_snide_cave": "off",
        "caves_boulder_cave": "off",
        "caves_lobby_blueprint": "off",
        "caves_lobby_lava": "off",
    }

    def verify(self, world, player_name: str, plando_options) -> None:
        """Verify all switch keys and values are valid."""
        super().verify(world, player_name, plando_options)
        for key, value in self.value.items():
            if key not in self.valid_keys:
                raise OptionError(f"Invalid switchsanity key '{key}'. Must be one of the documented switch names.")
            if key in self.GONE_SWITCHES:
                if value not in self.GONE_VALUES:
                    raise OptionError(f"Invalid value '{value}' for switch '{key}'. " f"Must be one of: {', '.join(sorted(self.GONE_VALUES))}")
            else:
                if value not in self.KONG_VALUES:
                    raise OptionError(f"Invalid value '{value}' for switch '{key}'. " f"Must be one of: {', '.join(sorted(self.KONG_VALUES))}")


class CrownPlacementRando(Toggle):
    """Randomizes the locations of Battle Arena crown pads to alternate positions throughout the levels."""

    display_name = "Crown Placement Randomization"


class RandomCrates(Toggle):
    """Randomizes the locations of Melon Crates to alternate positions throughout the levels."""

    display_name = "Random Melon Crates"


class RandomPatches(Toggle):
    """Randomizes the locations of Dirt Patches (Rainbow Coins) to alternate positions throughout the levels."""

    display_name = "Random Dirt Patches"


# TODO: Figure this out
# class CBRando(Toggle):
#     """Randomizes the locations of Colored Bananas throughout the levels.

#     This does NOT make individual bananas checks - they remain collectibles that count toward medals.
#     """

#     display_name = "Colored Banana Randomization"


class LogicType(Choice):
    """Determines what type of logic is needed to beat the seed.

    Options:
    glitchless: Logic is designed to be completed without glitches, mostly as intended by the developers.
    advanced_glitchless: Logic is designed to be completed without glitches, but allows for advanced techniques. Add tricks you want to put in logic in tricks_selected.
    glitched: Logic is designed to be completed with glitches. Add tricks you want to put in logic in tricks_selected, AND add glitches you want to put in logic in glitches_selected.
    minimal: Simplified logic with basic item placement rules. Key 5 won't be in level 7, Kongs won't be in their own shops/medals, and DK won't be in blast-locked locations.
    """

    display_name = "Logic Type"

    option_glitchless = 1
    option_advanced_glitchless = 0
    option_glitched = 2
    option_minimal = 4
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


class TrapLink(Toggle):
    """Determines if the Trap Link is enabled.

    If enabled, your received Traps will link to other players with Trap Link enabled, and their received traps will link to you
    """

    display_name = "Trap Link"


class MirrorMode(Toggle):
    """Determines whether the game will be horizontally Mirrored."""

    display_name = "Mirror Mode"


class HardModeSelected(OptionList):
    """Determines which Hard Mode settings are enabled.

    Valid Keys:
    "hard_enemies": Enemies Fight Back a little harder.
    "shuffled_jetpac_enemies": Jetpac enemies are shuffled within Jetpac.
    "strict_helm_timer": Helm Timer starts at 0:00 requiring blueprints to turn in
    "donk_in_the_dark_world: All maps are pitch black, with only a light to help you path your way to the end of the game. Mixing this with 'Donk in the Sky' will convert the challenge into 'Memory Challenge' instead.
    "donk_in_the_sky": Collision Geometry is disabled. Mixing this with 'Donk in the Dark World' will convert the challenge into 'Memory Challenge' instead.
    "faster_balloons": Balloons will now move at super speed.
    "angry_caves": Stalactites will rain down upon you in Caves at super speed.
    "lower_max_refill_amount": Halves your replenishable items.
    """

    display_name = "Hard Mode Options"

    valid_keys = {
        "hard_enemies",
        "shuffled_jetpac_enemies",
        "strict_helm_timer",
        "donk_in_the_dark_world",
        "donk_in_the_sky",
        "faster_balloons",
        "angry_caves",
        "lower_max_refill_amount",
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
    "helm_star_gates"
    "helm_punch_gates"
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
        "helm_star_gates",
        "helm_punch_gates",
    }

    default = [
        "japes_coconut_gates",
        "aztec_tunnel_door",
        "aztec_5dtemple_switches",
        "aztec_tiny_temple_ice",
        "factory_testing_gate",
        "factory_production_room",
        "galleon_lighthouse_gate",
        "galleon_seasick_ship",
        "caves_igloo_pads",
        "helm_star_gates",
        "helm_punch_gates",
    ]


_ITEM_POOL_VALID_KEYS = frozenset(
    [
        "crowns",
        "blueprints",
        "medals",
        "company_coins",
        "fairies",
        "rainbow_coins",
        "bean",
        "pearls",
        "crates",
        "battle_arenas",
        "hints",
        "shopkeepers",
        "half_medals",
        "snide_turnins",
        "time_of_day",
        "boulders",
        "balloons",
        "breakables",
        "dropsanity",
    ]
)


class ItemPool(OptionList):
    """Determines which item categories are shuffled into the Archipelago item pool.

    Moves, Golden Bananas, Shops, Kongs, Keys, Races, Training Moves, and Shockwave are always included and cannot be disabled.

    Valid Keys:
    - "crowns": Battle Arena Crowns
    - "blueprints": Kong Blueprints
    - "medals": Banana Medals
    - "company_coins": Nintendo & Rareware Coins
    - "fairies": Banana Fairies
    - "rainbow_coins": Rainbow Coins (dirt patches)
    - "bean": The Bean
    - "pearls": Mermaid Pearls
    - "crates": Melon Crates
    - "battle_arenas": Banana rewards from Battle Arenas (Gauntlets)
    - "hints": Wrinkly Hint items
    - "shopkeepers": Cranky/Funky/Candy/Snide themselves (shops locked until collected)
    - "half_medals": Half Medal items granted at partial CB requirements
    - "snide_turnins": Blueprint turn-in rewards
    - "time_of_day": Fungi Forest Time of Day
    - "boulders": Throwable boulder/barrel checks
    - "balloons": Balloon checks
    - "breakables": Breakable object checks (pots, etc.)
    - "dropsanity": Enemy drop checks
    """

    display_name = "Item Pool"
    valid_keys = _ITEM_POOL_VALID_KEYS
    default = [
        "crowns",
        "blueprints",
        "medals",
        "company_coins",
        "fairies",
        "rainbow_coins",
        "bean",
        "pearls",
        "crates",
        "battle_arenas",
    ]

    def verify(self, world, player_name: str, plando_options) -> None:
        """Verify all keys are valid."""
        super().verify(world, player_name, plando_options)
        invalid = [k for k in self.value if k not in self.valid_keys]
        if invalid:
            raise OptionError(f"Invalid item_pool keys: {', '.join(invalid)}. Must be one of: {', '.join(sorted(self.valid_keys))}")


class RandomizeBlockers(Toggle):
    """Determines if B. Locker values are randomized."""

    display_name = "Randomize B. Lockers"
    default = True


class MaximumBLocker(Range):
    """Determines the Maximum Value for B. Lockers if Randomize B.Lockers are enabled."""

    display_name = "Maximum B. Locker"
    range_start = 0
    range_end = 201
    default = 64


class ChaosBLockers(Toggle):
    """If Randomize B. Lockers is also enabled, determines if B. Lockers may require non-Golden Banana collectibles."""

    display_name = "Chaos B. Lockers"


class MaximizeHelmBLocker(Toggle):
    """Ensures that Level 8's B. Locker will always be at the maximum value."""

    display_name = "Maximize Helm B. Locker"


class LevelBlockers(OptionDict):
    """Determines the B. Locker values for each level if Randomize B. Lockers are turned off.

    Valid Keys:
    - "level_1"
    - "level_2"
    - "level_3"
    - "level_4"
    - "level_5"
    - "level_6"
    - "level_7"
    - "level_8"

    Valid Values:
    - a number from 0 to 201
    - "random", which will pick a random valid value for you
    - a range in the form "x-y", which will pick a random valid value between x and y
    """

    display_name = "Level B. Lockers"

    min = 0
    max = 201
    default = {
        "level_1": 0,
        "level_2": 0,
        "level_3": 0,
        "level_4": 0,
        "level_5": 0,
        "level_6": 0,
        "level_7": 0,
        "level_8": 64,
    }


class RandomizeTroff(Toggle):
    """Determines if Troff n Scoff banana values are randomized."""

    display_name = "Randomize Troff n Scoff"
    default = True


class MaximumTroff(Range):
    """Determines the Maximum Value for Troff n Scoff if Randomize Troff n Scoff is enabled."""

    display_name = "Maximum Troff n Scoff"
    range_start = 0
    range_end = 500
    default = 150


class LevelTroff(OptionDict):
    """Determines the Troff n Scoff banana values for each level if Randomize Troff n Scoff is turned off.

    Valid Keys:
    - "level_1"
    - "level_2"
    - "level_3"
    - "level_4"
    - "level_5"
    - "level_6"
    - "level_7"
    - "level_8"

    Valid Values:
    - a number from 0 to 500
    - "random", which will pick a random valid value for you
    - a range in the form "x-y", which will pick a random valid value between x and y
    """

    display_name = "Level Troff n Scoff"

    min = 0
    max = 500
    default = {
        "level_1": 0,
        "level_2": 0,
        "level_3": 0,
        "level_4": 0,
        "level_5": 0,
        "level_6": 0,
        "level_7": 0,
        "level_8": 0,
    }


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


class ShopPrices(Choice):
    """Determines the cost of shop purchases.

    Shops uses the standalone Tooie Shops settings making it so purchases don't deduct your coins when making purchases.
    Prices are randomized within difficulty-based budgets calculated from each kong's total available coins.

    Difficulty Percentages:
    - free (0%): All shops cost 0 coins
    - low (35%): Lower coin requirements, casual gameplay
    - medium (55%): Moderate coin requirements, balanced difficulty
    - high (85%): High coin requirements, requires collecting most coins
    """

    display_name = "Shop Prices"
    option_free = 0
    option_low = 1
    option_medium = 2
    option_high = 3
    default = 0


class HelmKeyLock(DefaultOnToggle):
    """Determines if a key will be locked at the end of Helm."""

    display_name = "Lock Helm Key"


class ShuffleHelmLevel(Toggle):
    """Determined if Helm is shuffled into the level order."""

    display_name = "Shuffle Helm"


class ShopkeeperHints(DefaultOnToggle):
    """Determines if entering a shop with Shopkeepers in the pool will give you a hint on where the shopkeeper is."""

    display_name = "Shopkeeper Hint"


class HintStyle(Choice):
    """Choose the style of Wrinkly hints you'd like to play with. These do not affect shopkeeper or microhints.

    - off: No in-game hints at all.
    - no_woth: Hints can tell you about your K. Rool phases, and directly hint important items and hard locations.
    - woth: Same as no_woth, but Way of the Hoard hints can appear, which will tell you a location is required but not what item is at that location. Increases gen time significantly, especially in larger multiworlds.
    """

    display_name = "Hint Style"

    option_off = 0
    option_no_woth = 1
    option_woth = 2
    default = 1


class MicroHints(Choice):
    """Extra hints are placed in late-game to provide extra information if you are stuck on where an item is.

    - Monkeyport will be hinted upon touching the lower Monkeyport pad in Isles with the B. Locker requirements to enter all of the first 7 levels.
    - Gorilla Gone will be hinted upon touching the pad inside Helm Lobby with the B. Locker requirement to enter Helm.
    - Instruments will be hinted upon touching their pad in Helm.
    """

    display_name = "Micro Hints"

    option_Off = 0
    option_some = 1
    option_all = 2
    default = 2


class ShuffledBonusBarrels(OptionList):
    """Determines which minigames are shuffled into the barrel pool.

    Valid Keys:
    "batty_barrel_bandit"
    "big_bug_bash"
    "busy_barrel_barrage"
    "mad_maze_maul"
    "minecart_mayhem"
    "beaver_bother"
    "teetering_turtle_trouble"
    "stealthy_snoop"
    "stash_snatch"
    "splish_splash_salvage"
    "speedy_swing_sortie"
    "krazy_kong_klamour"
    "searchlight_seek"
    "kremling_kosh"
    "peril_path_panic"
    "helm_minigames"
    "arenas"
    "training_minigames"
    "arcade"
    """

    display_name = "Shuffled Bonus Barrels"

    valid_keys = {
        "batty_barrel_bandit",
        "big_bug_bash",
        "busy_barrel_barrage",
        "mad_maze_maul",
        "minecart_mayhem",
        "beaver_bother",
        "teetering_turtle_trouble",
        "stealthy_snoop",
        "stash_snatch",
        "splish_splash_salvage",
        "speedy_swing_sortie",
        "krazy_kong_klamour",
        "searchlight_seek",
        "kremling_kosh",
        "peril_path_panic",
        "helm_minigames",
        "arenas",
        "training_minigames",
        "arcade",
    }

    default = [
        "batty_barrel_bandit",
        "big_bug_bash",
        "busy_barrel_barrage",
        "mad_maze_maul",
        "minecart_mayhem",
        "beaver_bother",
        "teetering_turtle_trouble",
        "stealthy_snoop",
        "stash_snatch",
        "splish_splash_salvage",
        "speedy_swing_sortie",
        "krazy_kong_klamour",
        "searchlight_seek",
        "kremling_kosh",
        "peril_path_panic",
        "helm_minigames",
        "arenas",
        "training_minigames",
        "arcade",
    ]


class HardMinigames(Toggle):
    """Determines if hard minigames are shuffled into the barrel pool."""

    display_name = "Hard Minigames"


class AutoCompleteBonusBarrels(Toggle):
    """If turned on, bonus barrels will instantly spawn their reward instead of requiring a minigame to complete.

    This option does NOT autocomplete Helm barrels! Use the helm_room_bonus_count option.
    """

    display_name = "Auto Complete Bonus Barrels"


class HelmRoomBonusCount(Range):
    """Determines how many bonus barrels need to be done in each Helm room.

    If set to 0, there will be no bonus barrels and Blast-O-Matic sections will turn off immediately upon playing the instrument pad to open the room.
    """

    display_name = "Helm Room Bonus Count"

    range_start = 0
    range_end = 2
    default = 0


class HelmDoor1Item(Choice):
    """Determines what item is required to open the first door in Hideout Helm (Crown Door).

    Options:
    - vanilla: Requires Battle Crowns (as in the original game).
    - opened: The door is automatically opened.
    - golden_bananas: Requires Golden Bananas.
    - blueprints: Requires Blueprints.
    - company_coins: Requires Company Coins.
    - keys: Requires Boss Keys.
    - medals: Requires Banana Medals.
    - fairies: Requires Banana Fairies.
    - rainbow_coins: Requires Rainbow Coins.
    - bean: Requires The Bean.
    - pearls: Requires Pearls.
    - easy_random: Random item (easier items).
    - medium_random: Random item (medium difficulty).
    - hard_random: Random item (harder items).
    """

    display_name = "Crown Door Item"
    option_vanilla = 0
    option_opened = 1
    option_medium_random = 2
    option_golden_bananas = 3
    option_blueprints = 4
    option_company_coins = 5
    option_keys = 6
    option_medals = 7
    option_crowns = 8
    option_fairies = 9
    option_rainbow_coins = 10
    option_bean = 11
    option_pearls = 12
    option_easy_random = 13
    option_hard_random = 14
    default = 1


class HelmDoorItemCount(OptionDict):
    """Determines how many of a particular item you need to open Helm doors.

    You can set multiple values to account for different door item requirements.
    (i.e. if you set crown_door_item to "blueprints", the "keys" field will be ignored)

    Valid Keys:
    - "golden_bananas"
    - "blueprints"
    - "company_coins"
    - "keys"
    - "medals"
    - "crowns"
    - "fairies"
    - "rainbow_coins"
    - "bean"
    - "pearls"

    Valid Values:
    - a number from 0 to the maximum value for the key type
    - "random", which will pick a random valid value for you
    - a range in the form "x-y", which will pick a random valid value between x and y
    """

    min = 1
    max_values_dict: dict[str, int] = {
        "golden_bananas": 201,
        "blueprints": 40,
        "company_coins": 2,
        "keys": 8,
        "medals": 40,
        "crowns": 10,
        "fairies": 20,
        "rainbow_coins": 16,
        "bean": 1,
        "pearls": 5,
    }

    def verify(self, world: type[World], player_name: str, plando_options: PlandoOptions) -> None:
        """Verify Helm Door Item Count."""
        super(HelmDoorItemCount, self).verify(world, player_name, plando_options)

        for key in self.value.keys():
            if key not in self.max_values_dict.keys():
                raise OptionError(f"{key} is not a valid key for helm_door_item_count.")

        accumulated_errors = []

        for key, value in self.value.items():
            max = self.max_values_dict[key]
            if isinstance(value, numbers.Integral):
                value = int(value)
                if value > max:
                    accumulated_errors.append(f"{key}: {value} is higher than maximum allowed value {max}")
                elif value < self.min:
                    accumulated_errors.append(f"{key}: {value} is lower than minimum allowed value {self.min}")
            else:
                if value == "random":
                    continue
                split = value.split("-")
                if len(split) != 2:
                    accumulated_errors.append(f'{key}: {value} is not an integer or range, nor is it "random".')
                else:
                    for bound in split:
                        try:
                            bound = int(bound)
                        except (ValueError, TypeError):
                            accumulated_errors.append(f'{key}: {value} is not an integer or range, nor is it "random".')
                            continue
                        if bound > max:
                            accumulated_errors.append(f"{key}: Upper edge of range {bound} is higher than maximum allowed value {max}")
                        elif bound < self.min:
                            accumulated_errors.append(f"{key}: Lower edge of range {bound} is lower than minimum allowed value {self.min}")
        if accumulated_errors:
            raise OptionError("Found errors with option helm_door_item_count:\n" + "\n".join(accumulated_errors))

    default = {
        "golden_bananas": 1,
        "blueprints": 1,
        "company_coins": 1,
        "keys": 1,
        "medals": 1,
        "crowns": 1,
        "fairies": 1,
        "rainbow_coins": 1,
        "bean": 1,
        "pearls": 1,
    }


class HelmDoor2Item(Choice):
    """Determines what item is required to open the second door in Hideout Helm (Coin Door).

    Options:
    - vanilla: Requires Company Coins (as in the original game).
    - opened: The door is automatically opened.
    - golden_bananas: Requires Golden Bananas.
    - blueprints: Requires Blueprints.
    - keys: Requires Boss Keys.
    - medals: Requires Banana Medals.
    - crowns: Requires Battle Crowns.
    - fairies: Requires Banana Fairies.
    - rainbow_coins: Requires Rainbow Coins.
    - bean: Requires The Bean.
    - pearls: Requires Pearls.
    - easy_random: Random item (easier items).
    - medium_random: Random item (medium difficulty).
    - hard_random: Random item (harder items).
    """

    display_name = "Coin Door Item"
    option_vanilla = 0
    option_opened = 1
    option_medium_random = 2
    option_golden_bananas = 3
    option_blueprints = 4
    option_keys = 6
    option_medals = 7
    option_crowns = 8
    option_fairies = 9
    option_rainbow_coins = 10
    option_bean = 11
    option_pearls = 12
    option_easy_random = 13
    option_hard_random = 14
    default = 1


class SmallerShops(Toggle):
    """If enabled, shops would have a max of 3 items to sell."""

    default = True
    display_name = "Smaller Shops"


class HardBosses(OptionList):
    """Determines which bosses are harder.

    Valid Keys:
    "fast_mad_jack": Mad Jack will move at quantum speeds.
    "alternative_mad_jack_kongs": Logic can expect Donkey, Chunky, or Tiny without twirl to fight Mad Jack.
    "pufftoss_star_rando": The stars in the Pufftoss fight are now in random locations.
    "pufftoss_star_raised": The stars in the Pufftoss fight are now slightly raised to require you to jump to activate the stars.
    "kut_out_phase_rando": Kutout phases are now in random order and also a chance to see the secret 4th phase.
    "k_rool_toes_rando": The toes in Tiny phase K. Rool now attack in a random order.
    "beta_lanky_phase": K. Rool is now distracted by shooting a balloon rather than playing an instrument.
    """

    display_name = "Hard Bosses"

    valid_keys: {"fast_mad_jack", "alternative_mad_jack_kongs", "pufftoss_star_rando", "pufftoss_star_raised", "kut_out_phase_rando", "k_rool_toes_rando", "beta_lanky_phase"}


class PuzzleRando(Choice):
    """Determines the difficulty of puzzle randomization.

    off: Puzzle solutions are NOT randomized.
    easy: Easy boundaries.
    medium: Medium boundaries.
    hard: Hard boundaries, Castle Car Race is randomized.
    chaos: Any value in the easy, medium, or hard bounds.
    """

    display_name = "Puzzle Randomization"
    option_off = 0
    option_easy = 1
    option_medium = 2
    option_hard = 3
    option_chaos = 4
    default = 2


class SelectStartingKong(Choice):
    """Determines which Kong you will start with. This is the Kong that will walk out onto DK Isle at the beginning of the game.

    Select "any" if you want your starting kong to be randomly determined.
    """

    display_name = "Select Starting Kong"
    option_donkey = 0
    option_diddy = 1
    option_lanky = 2
    option_tiny = 3
    option_chunky = 4
    option_any = 5

    default = 5


class KrushaRandom(Choice):
    """Determines which random kong is chosen to be Krusha.

    This will overwrite whatever's chosen in kong_models.
    "none": Kongs will be their vanilla model
    "manual": Use kong_models to plando your Kong Model
    "random_1": One Kong will be randomly replaced with Krusha
    "sometimes_1": Maybe one Kong will be randomly replaced with Krusha
    "random_all": Each Kong has a chance to be replaced with Krusha
    """

    display_name = "Random Krusha"

    option_none = 0
    option_manual = 1
    option_random_1 = 2
    option_sometimes_1 = 3
    option_random_all = 4


class KongModels(OptionDict):
    """Choose character models for each Kong.

    Valid Keys: "dk", "diddy", "lanky", "tiny", "chunky"

    Valid Values (varies by kong):
    - "default": Normal Kong (all kongs)
    - "krusha": Krusha (all kongs)
    - "krool_fight": K. Rool fight model (all kongs)
    - "krool_cutscene": K. Rool cutscene model (all kongs)
    - "cranky": Cranky Kong (DK only)
    - "candy": Candy Kong (Tiny only)
    - "funky": Funky Kong (Diddy only)
    - "rabbit": Rabbit (Diddy only)
    - "robokrem": Robo Kremling (Lanky only)

    Example: {"dk": "krusha", "tiny": "candy"}
    """

    display_name = "Kong Models"

    valid_keys = frozenset(["dk", "diddy", "lanky", "tiny", "chunky"])

    # Models available to all kongs
    common_models = {"default", "krusha", "krool_fight", "krool_cutscene"}

    # Kong-specific models
    kong_specific_models = {
        "dk": {"cranky"},
        "diddy": {"funky", "rabbit"},
        "lanky": {"robokrem"},
        "tiny": {"candy"},
        "chunky": set(),
    }

    default = {"dk": "default", "diddy": "default", "lanky": "default", "tiny": "default", "chunky": "default"}

    def verify(self, world: type[World], player_name: str, plando_options: PlandoOptions) -> None:
        """Verify that each kong has a valid model assigned."""
        super(KongModels, self).verify(world, player_name, plando_options)

        accumulated_errors = []

        for kong, model in self.value.items():
            if kong not in self.valid_keys:
                accumulated_errors.append(f"Invalid kong '{kong}'. Must be one of: {', '.join(sorted(self.valid_keys))}")
                continue

            # Check if model is valid for this kong
            valid_models = self.common_models | self.kong_specific_models.get(kong, set())

            # Chunky cannot be krool_cutscene
            if kong == "chunky" and model == "krool_cutscene":
                accumulated_errors.append(f"Chunky cannot use the 'krool_cutscene' model")
                continue

            if model not in valid_models:
                accumulated_errors.append(f"Invalid model '{model}' for {kong}. Valid models for {kong}: {', '.join(sorted(valid_models))}")

        if accumulated_errors:
            raise OptionError("Found errors with option kong_models:\n" + "\n".join(accumulated_errors))


class IceFloorWeight(BaseTrapWeight):
    """Likelihood of receiving a trap which turns the floor slippery."""

    display_name = "Ice Floor Weight"


class PaperTrapWeight(BaseTrapWeight):
    """Likelihood of receiving a trap which turns Kongs into Paper."""

    display_name = "Paper Trap Weight"


class SlipTrapWeight(BaseTrapWeight):
    """Likelihood of receiving a trap which slips a kong on a banana peel."""

    display_name = "Slip Trap Weight"


class EnableCutscenes(Toggle):
    """Enabling this will re-add skippable cutscenes to your seed."""

    display_name = "Re-Enable Cutscenes"


class SnideMaximum(Range):
    """Determines the maximum reward for Snide Turnins to have progression."""

    display_name = "Snide Maximum"

    range_start = 0
    range_end = 40
    default = 20


class SharedShops(Toggle):
    """If enabled, makes 10 random shops shared removing 20 locations from the pool."""

    display_name = "Shared Shops"


class AnimalTrapWeight(BaseTrapWeight):
    """Likelihood of receiving a trap which transforms you into an Animal Buddy for a short time."""

    display_name = "Animal Trap Weight"


class RockfallTrapWeight(BaseTrapWeight):
    """Likelihood of receiving a trap which spawns falling stalactites for a short time."""

    display_name = "Rockfall Trap Weight"


class DisableTagTrapWeight(BaseTrapWeight):
    """Likelihood of receiving a trap which tags to a different Kong and also disabled Tagging for 15 seconds."""

    display_name = "Disable Tag Trap Weight"


class BaseFillerWeight(Choice):
    """Base Class for Filler Weights."""

    option_none = 0
    option_low = 1
    option_medium = 2
    option_high = 4
    default = 0


class JunkFillerWeight(BaseFillerWeight):
    """Likelihood of receiving junk items as filler."""

    display_name = "Junk Filler Weight"


class BananaFillerWeight(BaseFillerWeight):
    """Likelihood of receiving golden bananas as filler."""

    display_name = "Banana Filler Weight"


class CrownFillerWeight(BaseFillerWeight):
    """Likelihood of receiving battle crowns as filler."""

    display_name = "Crown Filler Weight"


class FairyFillerWeight(BaseFillerWeight):
    """Likelihood of receiving banana fairies as filler."""

    display_name = "Fairy Filler Weight"


class MedalFillerWeight(BaseFillerWeight):
    """Likelihood of receiving banana medals as filler."""

    display_name = "Medal Filler Weight"


class PearlFillerWeight(BaseFillerWeight):
    """Likelihood of receiving pearls as filler."""

    display_name = "Pearl Filler Weight"


class RainbowCoinFillerWeight(BaseFillerWeight):
    """Likelihood of receiving rainbow coins as filler."""

    display_name = "Rainbow Coin Filler Weight"


class AlternateMinecartMayhem(Toggle):
    """If enabled, Minecart Mayhem will be a coin based bonus barrel and the timer will be removed."""

    display_name = "Alternate Minecart Mayhem"


class EnemiesSelected(OptionList):
    """Determines what Enemies are in the pool.

    Valid Keys:
    "Bat"
    "BeaverBlue"
    "BeaverGold"
    "Bug"
    "FireballGlasses"
    "Kop"
    "Ghost"
    "Gimpfish"
    "Kaboom"
    "ChunkyKasplat"
    "DKKasplat"
    "DiddyKasplat"
    "LankyKasplat"
    "TinyKasplat"
    "GreenKlaptrap"
    "PurpleKlaptrap"
    "RedKlaptrap"
    "Klobber"
    "Klump"
    "Kop"
    "Kosha"
    "Kremling"
    "Krossbones"
    "GreenDice"
    "RedDice"
    "MushroomMan"
    "Pufftup"
    "RoboKremling"
    "ZingerRobo"
    "Ruler"
    "Shuri"
    "SirDomino"
    "SpiderSmall"
    "ZingerCharger"
    "ZingerLime"
    "DisableAKop"
    "DisableZKop"
    "DisableTaggingKop"
    "GetOutKop"
    """

    display_name = "Enemies Selected"

    default = {
        "Bat",
        "BeaverBlue",
        "BeaverGold",
        "Bug",
        "FireballGlass",
        "GetOut",
        "Ghost",
        "Gimpfish",
        "Kaboom",
        "ChunkyKasplat",
        "DKKasplat",
        "DiddyKasplat",
        "LankyKasplat",
        "TinyKasplat",
        "GreenKlaptrap",
        "PurpleKlaptrap",
        "RedKlaptrap",
        "Klobber",
        "Klump",
        "Kop",
        "Kosha",
        "Kremling",
        "Krossbones",
        "GreenDice",
        "RedDice",
        "MushroomMan",
        "Pufftup",
        "RoboKremling",
        "ZingerRobo",
        "Ruler",
        "Shuri",
        "SirDomino",
        "SpiderSmall",
        "ZingerCharger",
        "ZingerLime",
        "DisableAKop",
        "DisableZKop",
        "DisableTaggingKop",
        "GetOutKop",
    }


class LoadingZoneRando(TextChoice):
    """Randomize the connections between loading zones (Loading Zone Randomizer).

    If you set this option's value to a string (ie. "LZR": 50 instead of "yes": 50), it will be used as a custom seed.
    Every player who uses the same custom seed will have the same loading zone connections.

    WARNING: LZR is not for the faint of heart. Don't turn this on UNLESS you know what you're doing.
    """

    display_name = "Loading Zone Rando"
    alias_false = 0
    alias_off = 0
    option_no = 0
    alias_true = 1
    alias_on = 1
    option_yes = 1
    default = 0


# Yes this was implemented after LZR
class GalleonWaterLevel(Choice):
    """Determines what level the water in Galleon is set to."""

    display_name = "Galleon Water Level"
    option_raised = 0
    option_lowered = 1
    default = 0


class RemoveBaitPotions(Toggle):
    """If enabled, Ammo Belts and Instrument Upgrades will not be placed in the world.

    You can still start with them.
    Only recommended to enable this with Loading Zone Rando enabled.
    """

    display_name = "Remove Bait Potions"


class AlterSwitchAllocation(OptionDict):
    """Determines the slam color requirement for colored banana switches in each level.

    Valid Keys:
    - "level_1" through "level_8"

    Valid Values:
    - "none": No slam required (White)
    - "green": Green Slam (Simian Slam)
    - "blue": Blue Slam (Super Simian Slam)
    - "red": Red Slam (Super Duper Simian Slam)
    """

    display_name = "Alter Switch Allocation"

    valid_keys = frozenset(["level_1", "level_2", "level_3", "level_4", "level_5", "level_6", "level_7", "level_8"])

    default = {
        "level_1": "green",
        "level_2": "green",
        "level_3": "green",
        "level_4": "green",
        "level_5": "blue",
        "level_6": "blue",
        "level_7": "red",
        "level_8": "red",
    }

    def verify(self, world, player_name: str, plando_options) -> None:
        """Verify switch allocation."""
        super().verify(world, player_name, plando_options)

        valid_values = {"none", "green", "blue", "red"}

        for key, value in self.value.items():
            if key not in self.valid_keys:
                raise OptionError(f"Invalid level key '{key}'. Must be one of: {', '.join(sorted(self.valid_keys))}")
            if value not in valid_values:
                raise OptionError(f"Invalid slam requirement '{value}' for {key}. Must be one of: {', '.join(sorted(valid_values))}")


class RandomStartingLocation(Choice):
    """Determines if and where the game can start you.

    - off: Start at the normal DK Isle location
    - isles_only: Start at a random location within DK Isles
    - all: Start at a random location in any level
    """

    display_name = "Random Starting Region"
    option_off = 0
    option_isles_only = 1
    option_all = 2
    default = 0


class DKPortalLocationRando(Choice):
    """Randomize the locations of DK Portals within levels.

    DK Portals are the exits that return you from a level to its lobby.

    - off: DK Portals remain in their vanilla locations
    - main_only: DK Portals can only appear in main level areas (not bonus barrels, buildings, etc.)
    - all: DK Portals can appear anywhere in the level
    """

    display_name = "DK Portal Location Rando"
    option_off = 0
    option_main_only = 1
    option_all = 2
    default = 0


@dataclass
class DK64Options(PerGameCommonOptions):
    """Options for DK64R."""

    death_link: DeathLink
    ring_link: RingLink
    tag_link: TagLink
    trap_link: TrapLink
    goal: Goal
    pregiven_keys: NumberOfStartingKeys
    require_beating_krool: RequireBeatingKrool
    helm_key_lock: HelmKeyLock
    shuffle_helm_level_order: ShuffleHelmLevel
    krool_phase_count: KroolPhaseCount
    helm_phase_count: HelmPhaseCount
    krool_in_boss_pool: KroolShuffle
    remove_barriers_selected: RemoveBarriers
    cbs_required_for_medal: MedalColorBananaRequirement
    medal_distribution: MedalDistribution
    pearls_required_for_mermaid: MermaidRequirement
    jetpac_requirement: JetpacRequirement
    fairies_required_for_bfi: RarewareGBRequirement
    randomize_blocker_required_amounts: RandomizeBlockers
    blocker_max: MaximumBLocker
    enable_chaos_blockers: ChaosBLockers
    maximize_level8_blocker: MaximizeHelmBLocker
    chaos_ratio: ChaosRatio
    level_blockers: LevelBlockers
    randomize_troff: RandomizeTroff
    troff_max: MaximumTroff
    level_troff: LevelTroff
    open_lobbies: OpenLobbies
    switchsanity: SwitchsanityOptions
    crown_placement_rando: CrownPlacementRando
    random_crates: RandomCrates
    random_patches: RandomPatches
    # cb_rando_enabled: CBRando
    climbing_shuffle: ClimbingShuffle
    cannon_shuffle: CannonShuffle
    starting_kong_count: StartingKongCount
    starting_move_pool_1: StartingMovePool1
    starting_move_pool_1_count: StartingMovePool1Count
    starting_move_pool_2: StartingMovePool2
    starting_move_pool_2_count: StartingMovePool2Count
    starting_move_pool_3: StartingMovePool3
    starting_move_pool_3_count: StartingMovePool3Count
    starting_move_pool_4: StartingMovePool4
    starting_move_pool_4_count: StartingMovePool4Count
    starting_move_pool_5: StartingMovePool5
    starting_move_pool_5_count: StartingMovePool5Count
    shopkeeper_hints: ShopkeeperHints
    microhints: MicroHints
    item_pool: ItemPool
    logic_type: LogicType
    tricks_selected: TricksSelected
    glitches_selected: GlitchesSelected
    hard_mode_selected: HardModeSelected
    mirror_mode: MirrorMode
    trap_fill_percentage: TrapFillPercentage
    bubble_trap_weight: BubbleTrapWeight
    reverse_trap_weight: ReverseTrapWeight
    slow_trap_weight: SlowTrapWeight
    disable_a_trap_weight: DisableAWeight
    disable_b_trap_weight: DisableBWeight
    disable_c_trap_weight: DisableCWeight
    disable_z_trap_weight: DisableZWeight
    get_out_trap_weight: GetOutTrapWeight
    dry_trap_weight: DryTrapWeight
    flip_trap_weight: FlipTrapWeight
    receive_notifications: ReceiveNotifications
    hint_style: HintStyle
    shuffled_bonus_barrels: ShuffledBonusBarrels
    hard_minigames: HardMinigames
    auto_complete_bonus_barrels: AutoCompleteBonusBarrels
    helm_room_bonus_count: HelmRoomBonusCount
    crown_door_item: HelmDoor1Item
    coin_door_item: HelmDoor2Item
    helm_door_item_count: HelmDoorItemCount
    smaller_shops: SmallerShops
    harder_bosses: HardBosses
    puzzle_rando: PuzzleRando
    goal_quantity: GoalQuantity
    select_starting_kong: SelectStartingKong
    ice_floor_weight: IceFloorWeight
    paper_weight: PaperTrapWeight
    slip_weight: SlipTrapWeight
    enable_cutscenes: EnableCutscenes
    maximum_snide: SnideMaximum
    enable_shared_shops: SharedShops
    animal_trap_weight: AnimalTrapWeight
    rockfall_trap_weight: RockfallTrapWeight
    disabletag_trap_weight: DisableTagTrapWeight
    junk_filler_weight: JunkFillerWeight
    banana_filler_weight: BananaFillerWeight
    crown_filler_weight: CrownFillerWeight
    fairy_filler_weight: FairyFillerWeight
    medal_filler_weight: MedalFillerWeight
    pearl_filler_weight: PearlFillerWeight
    rainbowcoin_filler_weight: RainbowCoinFillerWeight
    alternate_minecart_mayhem: AlternateMinecartMayhem
    enemies_selected: EnemiesSelected
    shop_prices: ShopPrices
    loading_zone_rando: LoadingZoneRando
    galleon_water_level: GalleonWaterLevel
    remove_bait_potions: RemoveBaitPotions
    alter_switch_allocation: AlterSwitchAllocation
    krusha_model_mode: KrushaRandom
    kong_models: KongModels
    allowed_bosses: AllowedBosses
    random_starting_region: RandomStartingLocation
    dk_portal_location_rando: DKPortalLocationRando


dk64_option_groups: List[OptionGroup] = [
    OptionGroup(
        "Victory Conditions",
        [
            Goal,
            RequireBeatingKrool,
            GoalQuantity,
            NumberOfStartingKeys,
            HelmPhaseCount,
            HelmDoor1Item,
            HelmDoor2Item,
            HelmDoorItemCount,
            KroolPhaseCount,
            KroolShuffle,
        ],
    ),
    OptionGroup(
        "B. Locker Settings",
        [
            RandomizeBlockers,
            MaximumBLocker,
            ChaosBLockers,
            MaximizeHelmBLocker,
            ChaosRatio,
            LevelBlockers,
        ],
    ),
    OptionGroup(
        "Troff n Scoff Settings",
        [
            RandomizeTroff,
            MaximumTroff,
            LevelTroff,
        ],
    ),
    OptionGroup(
        "Item Pool",
        [
            StartingKongCount,
            SelectStartingKong,
            StartingMovePool1,
            StartingMovePool1Count,
            StartingMovePool2,
            StartingMovePool2Count,
            StartingMovePool3,
            StartingMovePool3Count,
            StartingMovePool4,
            StartingMovePool4Count,
            StartingMovePool5,
            StartingMovePool5Count,
            HelmKeyLock,
            ClimbingShuffle,
            CannonShuffle,
            ItemPool,
            SnideMaximum,
        ],
    ),
    OptionGroup(
        "Shops",
        [
            ShopPrices,
            SmallerShops,
            SharedShops,
        ],
    ),
    OptionGroup(
        "Levels/Barriers",
        [
            ShuffleHelmLevel,
            OpenLobbies,
            SwitchsanityOptions,
            RemoveBarriers,
            LoadingZoneRando,
            GalleonWaterLevel,
            RandomStartingLocation,
            DKPortalLocationRando,
        ],
    ),
    OptionGroup(
        "Custom Locations",
        [
            CrownPlacementRando,
            RandomCrates,
            RandomPatches,
            # CBRando,
        ],
    ),
    OptionGroup(
        "Logic",
        [
            LogicType,
            TricksSelected,
            GlitchesSelected,
            MedalColorBananaRequirement,
            MedalDistribution,
            MermaidRequirement,
            RarewareGBRequirement,
            JetpacRequirement,
            PuzzleRando,
            KrushaRandom,
            KongModels,
            AllowedBosses,
            AlterSwitchAllocation,
        ],
    ),
    OptionGroup(
        "Bonus Barrels",
        [
            ShuffledBonusBarrels,
            HardMinigames,
            AutoCompleteBonusBarrels,
            HelmRoomBonusCount,
            AlternateMinecartMayhem,
        ],
    ),
    OptionGroup(
        "Hard Mode",
        [
            HardModeSelected,
            HardBosses,
            MirrorMode,
        ],
    ),
    OptionGroup(
        "Enemies",
        [
            EnemiesSelected,
        ],
    ),
    OptionGroup(
        "Hints",
        [
            HintStyle,
            ShopkeeperHints,
            MicroHints,
        ],
    ),
    OptionGroup(
        "Filler Weights",
        [
            JunkFillerWeight,
            BananaFillerWeight,
            CrownFillerWeight,
            FairyFillerWeight,
            MedalFillerWeight,
            PearlFillerWeight,
            RainbowCoinFillerWeight,
        ],
    ),
    OptionGroup(
        "Trap Weights",
        [
            TrapFillPercentage,
            BubbleTrapWeight,
            SlowTrapWeight,
            ReverseTrapWeight,
            DisableAWeight,
            DisableBWeight,
            DisableCWeight,
            DisableZWeight,
            GetOutTrapWeight,
            DryTrapWeight,
            FlipTrapWeight,
            IceFloorWeight,
            PaperTrapWeight,
            SlipTrapWeight,
            AnimalTrapWeight,
            RockfallTrapWeight,
            DisableTagTrapWeight,
        ],
    ),
    OptionGroup(
        "Links",
        [
            TagLink,
            RingLink,
            TrapLink,
            DeathLink,
        ],
    ),
    OptionGroup(
        "Quality of Life",
        [
            EnableCutscenes,
            RemoveBaitPotions,
            ReceiveNotifications,
        ],
    ),
]
