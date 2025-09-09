"""Options for DK64R."""

from dataclasses import dataclass
import numbers
import typing

from BaseClasses import PlandoOptions
from Options import Choice, PerGameCommonOptions, Range, Option, OptionDict, OptionError, OptionList, Toggle, DeathLink, DefaultOnToggle, OptionGroup
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
    - beat_k_rool: Defeat K. Rool! K. Rool can be fought by finding all 8 keys, then entering the ship that appears at the back of DK Isle.
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
    - treasure_hurry: Run down the timer by collecting treasure! You win when the timer reaches 0.
    """

    display_name = "Goal"
    option_beat_k_rool = 0
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
    default = 0


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


class TrapLink(Toggle):
    """Determines if the Trap Link is enabled.

    If enabled, your received Traps will link to other players with Trap Link enabled, and their received traps will link to you
    """

    display_name = "Trap Link"


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


class Level1Blocker(Range):
    """Determines the value of Level 1's B. Locker if Randomize B. Lockers are turned off."""

    display_name = "Level 1 B. Locker"

    range_start = 0
    range_end = 201
    default = 0


class Level2Blocker(Range):
    """Determines the value of Level 2's B. Locker if Randomize B. Lockers are turned off."""

    display_name = "Level 2 B. Locker"

    range_start = 0
    range_end = 201
    default = 0


class Level3Blocker(Range):
    """Determines the value of Level 3's B. Locker if Randomize B. Lockers are turned off."""

    display_name = "Level 3 B. Locker"

    range_start = 0
    range_end = 201
    default = 0


class Level4Blocker(Range):
    """Determines the value of Level 4's B. Locker if Randomize B. Lockers are turned off."""

    display_name = "Level 4 B. Locker"

    range_start = 0
    range_end = 201
    default = 0


class Level5Blocker(Range):
    """Determines the value of Level 5's B. Locker if Randomize B. Lockers are turned off."""

    display_name = "Level 5 B. Locker"

    range_start = 0
    range_end = 201
    default = 0


class Level6Blocker(Range):
    """Determines the value of Level 6's B. Locker if Randomize B. Lockers are turned off."""

    display_name = "Level 6 B. Locker"

    range_start = 0
    range_end = 201
    default = 0


class Level7Blocker(Range):
    """Determines the value of Level 7's B. Locker if Randomize B. Lockers are turned off."""

    display_name = "Level 7 B. Locker"

    range_start = 0
    range_end = 201
    default = 0


class Level8Blocker(Range):
    """Determines the value of Level 8's B. Locker if Randomize B. Lockers are turned off."""

    display_name = "Level 8 B. Locker"

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


class HalfMedals(Toggle):
    """Determines if Half Medals are added to the pool.

    If medal_cb_req is set to 50, you will get a check at 25 Colored Bananas.
    """

    display_name = "Half Medals in Pool"

    default = False


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

    Select "any" if you want your starting kong to be randomly determined."""

    display_name = "Select Starting Kong"
    option_donkey = 0
    option_diddy = 1
    option_lanky = 2
    option_tiny = 3
    option_chunky = 4
    option_any = 5

    default = 5


@dataclass
class DK64Options(PerGameCommonOptions):
    """Options for DK64R."""

    death_link: DeathLink
    ring_link: RingLink
    tag_link: TagLink
    trap_link: TrapLink
    goal: Goal
    krool_key_count: KeysRequiredToBeatKrool
    helm_key_lock: HelmKeyLock
    shuffle_helm_level_order: ShuffleHelmLevel
    krool_phase_count: KroolPhaseCount
    helm_phase_count: HelmPhaseCount
    krool_in_boss_pool: KroolInBossPool
    remove_barriers_selected: RemoveBarriers
    medal_cb_req: MedalColorBananaRequirement
    medal_distribution: MedalDistribution
    mermaid_gb_pearls: MermaidRequirement
    jetpac_requirement: JetpacRequirement
    rareware_gb_fairies: RarewareGBRequirement
    randomize_blocker_required_amounts: RandomizeBlockers
    blocker_max: MaximumBLocker
    enable_chaos_blockers: ChaosBLockers
    maximize_helm_blocker: MaximizeHelmBLocker
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
    half_medals_in_pool: HalfMedals
    glitches_selected: GlitchesSelected
    hard_mode: HardModeEnabled
    hard_mode_selected: HardModeSelected
    mirror_mode: MirrorMode
    hints_in_item_pool: HintItemRandomization
    boulders_in_pool: BouldersInPool
    dropsanity: Dropsanity
    shopkeeper_hints: ShopkeeperHints
    microhints: MicroHints
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
    smaller_shops: SmallerShops
    harder_bosses: HardBosses
    puzzle_rando: PuzzleRando
    goal_quantity: GoalQuantity
    select_starting_kong: SelectStartingKong


dk64_option_groups: List[OptionGroup] = [
    OptionGroup(
        "Victory Conditions",
        [
            Goal,
            GoalQuantity,
            KeysRequiredToBeatKrool,
            HelmPhaseCount,
            KroolPhaseCount,
            KroolInBossPool,
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
            Level1Blocker,
            Level2Blocker,
            Level3Blocker,
            Level4Blocker,
            Level5Blocker,
            Level6Blocker,
            Level7Blocker,
            Level8Blocker,
        ],
    ),
    OptionGroup(
        "Item Pool",
        [
            StartingKongCount,
            SelectStartingKong,
            StartingMoveCount,
            HelmKeyLock,
            ClimbingShuffle,
            ShopKeepers,
            BouldersInPool,
            Dropsanity,
            HintItemRandomization,
            HalfMedals,
            SmallerShops,
        ],
    ),
    OptionGroup(
        "Levels/Barriers",
        [
            ShuffleHelmLevel,
            OpenLobbies,
            SwitchSanity,
            RemoveBarriers,
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
        ],
    ),
    OptionGroup(
        "Bonus Barrels",
        [
            ShuffledBonusBarrels,
            HardMinigames,
            AutoCompleteBonusBarrels,
            HelmRoomBonusCount,
        ],
    ),
    OptionGroup(
        "Hard Mode",
        [
            HardModeEnabled,
            HardModeSelected,
            HardBosses,
            MirrorMode,
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
    OptionGroup("Notifications", [ReceiveNotifications]),
]
