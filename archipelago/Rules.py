"""Rules for Archipelago."""

from BaseClasses import MultiWorld
from worlds.AutoWorld import LogicMixin
from worlds.generic.Rules import add_rule, set_rule
from randomizer.Enums.Settings import WinConditionComplex


def set_rules(world: MultiWorld, player: int, dk64_world):
    """Set the rules for the given player's world."""
    # DK64_TODO: Get location access rules from DK64R

    # Set completion condition based on win condition
    if dk64_world.spoiler.settings.win_condition_item == WinConditionComplex.krools_challenge:
        # For K. Rool's Challenge, use the custom win condition logic
        def krools_challenge_complete(state):
            # Check all requirements for K. Rool's Challenge
            return (state.has("Banana Hoard", player) and  # Can access K. Rool fight
                    state.has("Jungle Japes Key", player) and
                    state.has("Angry Aztec Key", player) and
                    state.has("Frantic Factory Key", player) and
                    state.has("Gloomy Galleon Key", player) and
                    state.has("Fungi Forest Key", player) and
                    state.has("Crystal Caves Key", player) and
                    state.has("Creepy Castle Key", player) and
                    state.has("Hideout Helm Key", player) and
                    state.has_from_list_unique([f"DK Isles Lanky Blueprint", f"DK Isles Tiny Blueprint", f"DK Isles Diddy Blueprint", f"DK Isles Chunky Blueprint", f"DK Isles DK Blueprint"], player, 40) and
                    state.has_from_list_unique(["Boss Defeated - Jungle Japes", "Boss Defeated - Angry Aztec", "Boss Defeated - Frantic Factory", 
                                               "Boss Defeated - Gloomy Galleon", "Boss Defeated - Fungi Forest", "Boss Defeated - Crystal Caves", 
                                               "Boss Defeated - Creepy Castle"], player, 7) and
                    state.has_from_list_unique([f"Bonus Completed - {i}" for i in range(1, 44)], player, 43))
        
        world.completion_condition[player] = krools_challenge_complete
    else:
        # Default completion condition for other win conditions
        world.completion_condition[player] = lambda state: state.has("Banana Hoard", player)
