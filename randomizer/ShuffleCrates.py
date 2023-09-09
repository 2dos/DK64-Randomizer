"""Shuffle Melon Crate Locations."""
import random

import randomizer.LogicFiles.AngryAztec
import randomizer.LogicFiles.CreepyCastle
import randomizer.LogicFiles.CrystalCaves
import randomizer.LogicFiles.DKIsles
import randomizer.LogicFiles.FranticFactory
import randomizer.LogicFiles.FungiForest
import randomizer.LogicFiles.GloomyGalleon
import randomizer.LogicFiles.JungleJapes
import randomizer.LogicFiles.HideoutHelm
from randomizer.Enums.Collectibles import Collectibles
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Lists.Location import LocationList
from randomizer.Lists.CustomLocations import CustomLocations, LocationTypes, CustomLocation
from randomizer.LogicClasses import LocationLogic
from randomizer.Spoiler import Spoiler


def addCrate(MelonCrate: CustomLocation, enum_val: int, name: str, level: Levels):
    """Add crate to relevant Logic Region."""
    level_to_enum = {
        Levels.DKIsles: randomizer.LogicFiles.DKIsles.LogicRegions,
        Levels.JungleJapes: randomizer.LogicFiles.JungleJapes.LogicRegions,
        Levels.AngryAztec: randomizer.LogicFiles.AngryAztec.LogicRegions,
        Levels.FranticFactory: randomizer.LogicFiles.FranticFactory.LogicRegions,
        Levels.GloomyGalleon: randomizer.LogicFiles.GloomyGalleon.LogicRegions,
        Levels.FungiForest: randomizer.LogicFiles.FungiForest.LogicRegions,
        Levels.CrystalCaves: randomizer.LogicFiles.CrystalCaves.LogicRegions,
        Levels.CreepyCastle: randomizer.LogicFiles.CreepyCastle.LogicRegions,
        Levels.HideoutHelm: randomizer.LogicFiles.HideoutHelm.LogicRegions,
    }
    level_to_name = {
        Levels.DKIsles: "Isles",
        Levels.JungleJapes: "Japes",
        Levels.AngryAztec: "Aztec",
        Levels.FranticFactory: "Factory",
        Levels.GloomyGalleon: "Galleon",
        Levels.FungiForest: "Forest",
        Levels.CrystalCaves: "Caves",
        Levels.CreepyCastle: "Castle",
        Levels.HideoutHelm: "Helm",
    }
    level_data = level_to_enum[level]
    level_data[MelonCrate.logic_region].locations.append(LocationLogic(enum_val, MelonCrate.logic))
    LocationList[enum_val].name = f"{level_to_name[level]} MelonCrate: {name}"
    LocationList[enum_val].default_mapid_data[0].map = MelonCrate.map
    LocationList[enum_val].level = level


def removeMelonCrate():
    """Remove all crates from Logic regions."""
    level_logic_regions = [
        randomizer.LogicFiles.DKIsles.LogicRegions,
        randomizer.LogicFiles.JungleJapes.LogicRegions,
        randomizer.LogicFiles.AngryAztec.LogicRegions,
        randomizer.LogicFiles.FranticFactory.LogicRegions,
        randomizer.LogicFiles.GloomyGalleon.LogicRegions,
        randomizer.LogicFiles.FungiForest.LogicRegions,
        randomizer.LogicFiles.CrystalCaves.LogicRegions,
        randomizer.LogicFiles.CreepyCastle.LogicRegions,
        randomizer.LogicFiles.HideoutHelm.LogicRegions,
    ]
    for level in level_logic_regions:
        for region in level:
            region_data = level[region]
            region_data.locations = [x for x in region_data.locations if x.id < Locations.MelonCrate_Location00 or x.id > Locations.MelonCrate_Location12]


def ShuffleMelonCrates(spoiler: Spoiler, human_spoiler):
    """Shuffle Melon Crate Locations."""
    removeMelonCrate()
    spoiler.meloncrate_placement = []
    total_MelonCrate_list = {
        Levels.DKIsles: [],
        Levels.JungleJapes: [],
        Levels.AngryAztec: [],
        Levels.FranticFactory: [],
        Levels.GloomyGalleon: [],
        Levels.FungiForest: [],
        Levels.CrystalCaves: [],
        Levels.CreepyCastle: [],
        Levels.HideoutHelm: [],
    }
    for key in total_MelonCrate_list:
        human_spoiler[key.name] = []  # Ensure order

    for key in total_MelonCrate_list.keys():
        for SingleMelonCrateLocation in CustomLocations[key]:
            if (SingleMelonCrateLocation.vanilla_crate or not SingleMelonCrateLocation.selected) and LocationTypes.MelonCrate not in SingleMelonCrateLocation.banned_types:
                SingleMelonCrateLocation.setCustomLocation(False)
                total_MelonCrate_list[key].append(SingleMelonCrateLocation)

    for SingleMelonCrateLocation in range(4):
        area_key = random.choice(list(total_MelonCrate_list.keys()))
        area_meloncrate = total_MelonCrate_list[area_key]
        select_random_meloncrate_from_area(area_meloncrate, 2, area_key, spoiler, human_spoiler)
        del total_MelonCrate_list[area_key]

    for area_key in total_MelonCrate_list.keys():
        area_meloncrate = total_MelonCrate_list[area_key]
        select_random_meloncrate_from_area(area_meloncrate, 1, area_key, spoiler, human_spoiler)

    sorted_MelonCrates = spoiler.meloncrate_placement.copy()
    sorted_MelonCrates = sorted(sorted_MelonCrates, key=lambda d: d["score"])
    for MelonCrate_index, MelonCrate in enumerate(sorted_MelonCrates):
        MelonCrate["enum"] = Locations.MelonCrate_Location00 + MelonCrate_index
        addCrate(MelonCrate["MelonCrate"], MelonCrate["enum"], MelonCrate["name"], MelonCrate["level"])
        MelonCrate["MelonCrate"] = None
    return human_spoiler.copy()


def select_random_meloncrate_from_area(area_meloncrate, amount, level, spoiler: Spoiler, human_spoiler):
    """Select <amount> random melon crates from <area_meloncrate>, which is a list of melon crates. Makes sure max 1 melon crate per group is selected."""
    human_spoiler[level.name] = []
    for iterations in range(amount):
        selected_crate = random.choice(area_meloncrate)  # selects a random crate from the list
        for meloncrate in CustomLocations[level]:  # enables the selected crate
            if meloncrate.name == selected_crate.name:
                meloncrate.setCustomLocation(True)
                human_spoiler[level.name].append(meloncrate.name)
                local_map_index = len([x for x in spoiler.meloncrate_placement if x["map"] == meloncrate.map])
                spoiler.meloncrate_placement.append(
                    {"name": meloncrate.name, "map": meloncrate.map, "MelonCrate": meloncrate, "level": level, "score": (meloncrate.map * 100) + local_map_index},
                )
                area_meloncrate.remove(selected_crate)
                break
        if amount > 1:  # if multiple crates are picked, remove crates from the same group, prevent them from being picked
            area_meloncrate = [crate for crate in area_meloncrate if crate.group != selected_crate.group]
