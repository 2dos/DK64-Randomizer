"""Select CB Location selection."""
import random

import js
import randomizer.CollectibleLogicFiles.AngryAztec
import randomizer.CollectibleLogicFiles.CreepyCastle
import randomizer.CollectibleLogicFiles.CrystalCaves
import randomizer.CollectibleLogicFiles.FranticFactory
import randomizer.CollectibleLogicFiles.FungiForest
import randomizer.CollectibleLogicFiles.GloomyGalleon
import randomizer.CollectibleLogicFiles.JungleJapes
import randomizer.Fill as Fill
import randomizer.Lists.CBLocations.AngryAztecCBLocations
import randomizer.Lists.CBLocations.CreepyCastleCBLocations
import randomizer.Lists.CBLocations.CrystalCavesCBLocations
import randomizer.Lists.CBLocations.FranticFactoryCBLocations
import randomizer.Lists.CBLocations.FungiForestCBLocations
import randomizer.Lists.CBLocations.GloomyGalleonCBLocations
import randomizer.Lists.CBLocations.JungleJapesCBLocations
import randomizer.Lists.Exceptions as Ex
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Logic import CollectibleRegions
from randomizer.LogicClasses import Collectible
from randomizer.Spoiler import Spoiler

from .Enums.Collectibles import Collectibles

max_balloons = 105
max_singles = 780  # 793 Singles in Vanilla, under-representing this to help with the calculation formula
max_bunches = 790 - max_balloons * 2 - round(max_singles / 5)  # 334 bunches in vanilla, biasing this for now to help with calculation formula

level_data = {
    Levels.JungleJapes: {
        "cb": randomizer.Lists.CBLocations.JungleJapesCBLocations.ColoredBananaGroupList,
        "balloons": randomizer.Lists.CBLocations.JungleJapesCBLocations.BalloonList,
    },
    Levels.AngryAztec: {
        "cb": randomizer.Lists.CBLocations.AngryAztecCBLocations.ColoredBananaGroupList,
        "balloons": randomizer.Lists.CBLocations.AngryAztecCBLocations.BalloonList,
    },
    Levels.FranticFactory: {
        "cb": randomizer.Lists.CBLocations.FranticFactoryCBLocations.ColoredBananaGroupList,
        "balloons": randomizer.Lists.CBLocations.FranticFactoryCBLocations.BalloonList,
    },
    Levels.GloomyGalleon: {
        "cb": randomizer.Lists.CBLocations.GloomyGalleonCBLocations.ColoredBananaGroupList,
        "balloons": randomizer.Lists.CBLocations.GloomyGalleonCBLocations.BalloonList,
    },
    Levels.FungiForest: {
        "cb": randomizer.Lists.CBLocations.FungiForestCBLocations.ColoredBananaGroupList,
        "balloons": randomizer.Lists.CBLocations.FungiForestCBLocations.BalloonList,
    },
    Levels.CrystalCaves: {
        "cb": randomizer.Lists.CBLocations.CrystalCavesCBLocations.ColoredBananaGroupList,
        "balloons": randomizer.Lists.CBLocations.CrystalCavesCBLocations.BalloonList,
    },
    Levels.CreepyCastle: {
        "cb": randomizer.Lists.CBLocations.CreepyCastleCBLocations.ColoredBananaGroupList,
        "balloons": randomizer.Lists.CBLocations.CreepyCastleCBLocations.BalloonList,
    },
}


def ShuffleCBs(spoiler: Spoiler):
    """Shuffle CBs selected from location files."""
    retries = 0
    while True:
        try:
            total_balloons = 0
            total_singles = 0
            total_bunches = 0
            cb_data = []
            # First, remove all placed colored bananas
            for region_id in CollectibleRegions.keys():
                CollectibleRegions[region_id] = [
                    collectible for collectible in CollectibleRegions[region_id] if collectible.type not in [Collectibles.balloon, Collectibles.bunch, Collectibles.banana]
                ]
            for level_index, level in enumerate(level_data):
                level_placement = []
                global_divisor = 6 - level_index
                kong_specific_left = {Kongs.donkey: 100, Kongs.diddy: 100, Kongs.lanky: 100, Kongs.tiny: 100, Kongs.chunky: 100}
                # Balloons
                # Pick random amount of balloons assigned to level
                balloons_left = max_balloons - total_balloons
                balloon_lower = max(
                    int(balloons_left / (7 - level_index)) - 3, 0
                )  # Select lower bound for randomization as max between 0, and balloons left distributed amongst the remaining levels minus 3
                if global_divisor == 0:
                    # Last Level
                    balloon_upper = balloons_left
                else:
                    balloon_upper = min(int(balloons_left / (7 - level_index)) + 3, int(balloons_left / global_divisor))
                balloon_lst = level_data[level]["balloons"].copy()
                selected_balloon_count = min(random.randint(min(balloon_lower, balloon_upper), max(balloon_lower, balloon_upper)), len(balloon_lst))
                # selected_balloon_count = 22 # Test all balloon locations
                random.shuffle(balloon_lst)  # TODO: Maybe make this more advanced?
                # selects all balloons
                placed_balloons = 0
                for balloon in balloon_lst:
                    if placed_balloons < selected_balloon_count:
                        balloon_kongs = balloon.kongs.copy()
                        for kong in kong_specific_left:
                            if kong_specific_left[kong] < 10 and kong in balloon_kongs:  # Not enough Colored Bananas to place a balloon:
                                balloon_kongs.remove(kong)  # Remove kong from permitted list
                        if len(balloon_kongs) > 0:  # Has a kong who can be assigned to this balloon
                            selected_kong = random.choice(balloon_kongs)
                            kong_specific_left[selected_kong] -= 10  # Remove CBs for Balloon
                            level_placement.append({"id": balloon.id, "name": balloon.name, "kong": selected_kong, "level": level, "type": "balloons", "map": balloon.map})
                            placed_balloons += 1
                            CollectibleRegions[balloon.region].append(Collectible(Collectibles.balloon, selected_kong, balloon.logic, None, 1, name=balloon.name))
                # Model Two CBs
                bunches_left = max_bunches - total_bunches
                singles_left = max_singles - total_singles
                bunches_lower = max(int(bunches_left / (7 - level_index)) - 5, 0)
                singles_lower = max(int(singles_left / (7 - level_index)) - 10, 0)
                if global_divisor == 0:
                    bunches_upper = bunches_left
                    singles_upper = min(singles_left, int((5 * (1127 - total_bunches - total_singles) - sum(kong_specific_left)) / 4))  # Places a hard cap of 1127 total singles+bunches
                else:
                    bunches_upper = min(int(bunches_left / (7 - level_index)) + 15, int(bunches_left / global_divisor))
                    singles_upper = min(int(singles_left / (7 - level_index)) + 10, int(singles_left / global_divisor))
                groupIds = list(range(1, len(level_data[level]["cb"]) + 1))
                random.shuffle(groupIds)
                selected_bunch_count = random.randint(min(bunches_lower, bunches_upper), max(bunches_lower, bunches_upper))
                selected_single_count = random.randint(min(singles_lower, singles_upper), max(singles_lower, singles_upper))
                placed_bunches = 0
                placed_singles = 0
                for groupId in groupIds:
                    group_weight = 0
                    bunches_in_group = 0
                    singles_in_group = 0
                    colored_banana_groups = [group for group in level_data[level]["cb"] if group.group == groupId]
                    cb_kongs = list(kong_specific_left.keys())
                    for group in colored_banana_groups:
                        cb_kongs = list(set(cb_kongs) & set(group.kongs.copy()))
                        for loc in group.locations:
                            group_weight += loc[0]
                            bunches_in_group += int(loc[0] == 5)
                            singles_in_group += int(loc[0] == 1)
                    for kong in kong_specific_left:
                        if kong in cb_kongs:
                            # If this kong doesn't have space for this group, remove it. Also if this kong is close to cap, don't use this kong unless it's the last one.
                            if kong_specific_left[kong] < group_weight or (len(cb_kongs) > 1 and kong_specific_left[kong] <= 10 and (kong_specific_left[kong] - group_weight) > 0):
                                cb_kongs.remove(kong)
                    if len(cb_kongs) > 0 and selected_single_count >= placed_singles + singles_in_group and selected_bunch_count >= placed_bunches + bunches_in_group:
                        selected_kong = random.choice(cb_kongs)
                        kong_specific_left[selected_kong] -= group_weight  # Remove CBs for kong
                        # When a kong hits 0 remaining in this level, we no longer need to consider it
                        if kong_specific_left[selected_kong] == 0:
                            del kong_specific_left[selected_kong]
                        for group in colored_banana_groups:
                            # Calculate the number of bananas we have to place by lesser group so different bananas in the same group can have different logic
                            bunches_in_lesser_group = 0
                            singles_in_lesser_group = 0
                            for loc in group.locations:
                                bunches_in_lesser_group += int(loc[0] == 5)
                                singles_in_lesser_group += int(loc[0] == 1)
                            if bunches_in_lesser_group > 0:
                                CollectibleRegions[group.region].append(Collectible(Collectibles.bunch, selected_kong, group.logic, None, bunches_in_lesser_group, name=group.name))
                            if singles_in_lesser_group > 0:
                                CollectibleRegions[group.region].append(Collectible(Collectibles.banana, selected_kong, group.logic, None, singles_in_lesser_group, name=group.name))
                            level_placement.append({"group": group.group, "name": group.name, "kong": selected_kong, "level": level, "type": "cb", "map": group.map, "locations": group.locations})
                        placed_bunches += bunches_in_group
                        placed_singles += singles_in_group
                    # If all kongs have 0 unplaced, we're done here
                    if len(kong_specific_left.keys()) == 0:
                        break

                # Placement is valid
                total_balloons += placed_balloons
                total_bunches += placed_bunches
                total_singles += placed_singles
                cb_data.extend(level_placement.copy())
                for x in kong_specific_left:
                    if kong_specific_left[x] > 0:
                        print(f"WARNING: {kong_specific_left[x]} bananas unassigned for {x.name} in {level.name}")
                        raise Ex.CBFillFailureException
                    elif kong_specific_left[x] < 0:
                        print(f"WARNING: {-kong_specific_left[x]} too many bananas assigned for {x.name} in {level.name}")
                        raise Ex.CBFillFailureException
            if total_bunches + total_singles > 1127:
                print(f"WARNING: {total_bunches + total_singles} banana objects placed, exceeding cap of 1127")
                raise Ex.CBFillFailureException
            Fill.Reset()
            if not Fill.VerifyWorld(spoiler.settings):
                raise Ex.CBFillFailureException
            spoiler.cb_placements = cb_data
            return
        except Ex.CBFillFailureException:
            if retries >= 10:
                js.postMessage("CB Randomizer failed to fill. REPORT THIS TO THE DEVS!!")
                raise Ex.CBFillFailureException
            retries += 1
            js.postMessage("CB Randomizer failed to fill. Tries: " + str(retries))
