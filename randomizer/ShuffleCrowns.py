"""Shuffle Crown picks, excluding helm."""

import random
from randomizer.Enums.Levels import Levels
from randomizer.Lists.CrownLocations import CrownLocations


def ShuffleCrowns(crown_selection, human_crowns):
    """Generate Crown Placement Assortment."""
    for level in CrownLocations:
        level_lst = CrownLocations[level]
        index_lst = list(range(len(level_lst)))
        pick_count = 1
        if level == Levels.DKIsles:
            pick_count = 2
        crowns = random.sample(index_lst, pick_count)
        crown_selection[level] = crowns.copy()
        for crown_index, crown in enumerate(crowns):
            crown_name = level.name
            if level == Levels.DKIsles:
                crown_name = f"{level.name} ({crown_index + 1})"
            human_crowns[crown_name] = level_lst[crown].name
