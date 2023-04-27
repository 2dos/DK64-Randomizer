"""Module used to handle setting and randomizing kasplats."""
import random

import js
import randomizer.Fill as Fill
import randomizer.Lists.Exceptions as Ex
import randomizer.Logic as Logic
from randomizer.Enums.Items import Items
from randomizer.Enums.Kongs import GetKongs, Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Types import Types
from randomizer.Lists.KasplatLocations import KasplatLocationList
from randomizer.Lists.Location import Location
from randomizer.Lists.MapsAndExits import Maps
from randomizer.LogicClasses import LocationLogic

shufflable = {
    Locations.IslesKasplatHelmLobby: Kongs.donkey,
    Locations.IslesKasplatCastleLobby: Kongs.diddy,
    Locations.IslesKasplatCavesLobby: Kongs.lanky,
    Locations.IslesKasplatFactoryLobby: Kongs.tiny,
    Locations.IslesKasplatGalleonLobby: Kongs.chunky,
    Locations.JapesKasplatLeftTunnelNear: Kongs.donkey,
    Locations.JapesKasplatNearPaintingRoom: Kongs.diddy,
    Locations.JapesKasplatNearLab: Kongs.lanky,
    Locations.JapesKasplatLeftTunnelFar: Kongs.tiny,
    Locations.AztecKasplatSandyBridge: Kongs.donkey,
    Locations.AztecKasplatLlamaTemple: Kongs.lanky,
    Locations.AztecKasplatNearLab: Kongs.tiny,
    Locations.FactoryKasplatProductionTop: Kongs.donkey,
    Locations.FactoryKasplatProductionBottom: Kongs.diddy,
    Locations.FactoryKasplatRandD: Kongs.lanky,
    Locations.FactoryKasplatStorage: Kongs.tiny,
    Locations.FactoryKasplatBlocks: Kongs.chunky,
    Locations.GalleonKasplatGoldTower: Kongs.donkey,
    Locations.GalleonKasplatLighthouseArea: Kongs.diddy,
    Locations.GalleonKasplatCannons: Kongs.lanky,
    Locations.GalleonKasplatNearLab: Kongs.tiny,
    Locations.GalleonKasplatNearSub: Kongs.chunky,
    Locations.ForestKasplatNearBarn: Kongs.donkey,
    Locations.ForestKasplatInsideMushroom: Kongs.diddy,
    Locations.ForestKasplatOwlTree: Kongs.lanky,
    Locations.ForestKasplatLowerMushroomExterior: Kongs.tiny,
    Locations.ForestKasplatUpperMushroomExterior: Kongs.chunky,
    Locations.CavesKasplatNearLab: Kongs.donkey,
    Locations.CavesKasplatPillar: Kongs.lanky,
    Locations.CavesKasplatNearCandy: Kongs.tiny,
    Locations.CavesKasplatOn5DI: Kongs.chunky,
    Locations.CastleKasplatCrypt: Kongs.diddy,
    Locations.CastleKasplatHalfway: Kongs.lanky,
    Locations.CastleKasplatLowerLedge: Kongs.tiny,
    Locations.CastleKasplatNearCandy: Kongs.chunky,
}

constants = {
    # Must be chunky since need to shoot pineapple to lower vines and they don't stay lowered
    Locations.JapesKasplatUnderground: Kongs.chunky,
    # Need jetpack to reach so must be diddy
    Locations.AztecKasplatOnTinyTemple: Kongs.diddy,
    # Pineapple doors don't stay open, so need to be chunky
    Locations.AztecKasplatChunky5DT: Kongs.chunky,
    # Need to jetpack to the warp pad to get to the kasplat... can technically fall onto it but seems awful
    Locations.CavesKasplatNearFunky: Kongs.diddy,
    # Coconut gate doesn't stay open
    Locations.CastleKasplatTree: Kongs.donkey,
}


def FindLevel(location):
    """Find the level given a location."""
    for region in Logic.Regions.values():
        for loc in region.locations:
            if loc.id == location:
                return region.level


def GetBlueprintItemForKongAndLevel(level, kong):
    """For the Level and Kong enum values, return the Blueprint Item enum tied to it."""
    baseOffset = int(Items.JungleJapesDonkeyBlueprint)  # Japes/Donkey is the first Blueprint item and they're all grouped together
    levelOffset = int(level)
    # Other levels are 0-6 but Helm is 7, DK Isles is 8, and I'm too scared to change it so it's accounted for here
    if levelOffset > 7:
        levelOffset = 7
    return Items(baseOffset + (5 * levelOffset) + int(kong))


def GetBlueprintLocationForKongAndLevel(level, kong):
    """For the Level and Kong enum values, return the generic Blueprint Location enum tied to it."""
    baseOffset = int(Locations.JapesDonkeyKasplatRando)  # Japes/Donkey is the first generic Blueprint location and they're all grouped together
    levelOffset = int(level)
    # Other levels are 0-6 but Helm is 7, DK Isles is 8, and I'm too scared to change it so it's accounted for here
    if levelOffset > 7:
        levelOffset = 7
    return Locations(baseOffset + (5 * levelOffset) + int(kong))


def ShuffleKasplatsAndLocations(spoiler, LogicVariables):
    """Shuffle the location and kong assigned to each kasplat. This should replace ShuffleKasplats if all goes well."""
    # Cull all locations for vanilla kasplats so they don't get in the way or have items shuffled into them
    spoiler.shuffled_kasplat_map = {}
    LogicVariables.kasplat_map = {}
    for location in shufflable:
        Logic.LocationList[location].inaccessible = True
    for location in constants:
        Logic.LocationList[location].inaccessible = True
    # Fill kasplats level by level
    for level in KasplatLocationList:
        kasplats = KasplatLocationList[level]
        # Fill kasplats kong by kong
        kongs = GetKongs()
        random.shuffle(kongs)
        for kong in kongs:
            available_for_kong = []
            # Pick a random unselected kasplat from available ones for this kong
            for kasplat in kasplats:
                if not kasplat.selected and kong in kasplat.kong_lst:
                    available_for_kong.append(kasplat.name)
            selected_kasplat = random.choice(available_for_kong)
            # Loop through kasplats until we find the relevant one
            for kasplat in kasplats:
                if kasplat.name == selected_kasplat:
                    kasplat.setKasplat()
                    # Figure out what blueprint should be placed where
                    item_id = GetBlueprintItemForKongAndLevel(level, kong)
                    location_id = GetBlueprintLocationForKongAndLevel(level, kong)
                    # Assemble the Location object
                    location = Location(level, kasplat.name, item_id, Types.Blueprint, kong, [kasplat.map])
                    Logic.LocationList[location_id] = location
                    # Insert the Location into the Region
                    kasplatRegion = Logic.Regions[kasplat.region_id]
                    kasplatRegion.locations.append(LocationLogic(location_id, kasplat.additional_logic))
                    # Update logic variables for remainder of the Fill
                    LogicVariables.kasplat_map[location_id] = kong
                    spoiler.shuffled_kasplat_map[kasplat.name] = int(kong)
                    break


def ShuffleKasplatsInVanillaLocations(spoiler, LogicVariables):
    """Shuffles the kong assigned to each kasplat, restricted to their vanilla locations."""
    spoiler.shuffled_kasplat_map = {}
    LogicVariables.kasplat_map = {}
    for location in shufflable:
        Logic.LocationList[location].inaccessible = True
    for location in constants:
        Logic.LocationList[location].inaccessible = True
    # Place by level
    for level in KasplatLocationList:
        availableKongs = GetKongs().copy()
        five_vanilla_kasplats = [kasplat for kasplat in KasplatLocationList[level] if kasplat.vanilla]
        five_vanilla_kasplats.sort(key=lambda l: len(l.kong_lst))  # Make sure kasplats with fewer possible kongs get placed first
        # We go by location in this method because it will guarantee a fill
        for kasplat in five_vanilla_kasplats:
            chosenKong = random.choice([kong for kong in kasplat.kong_lst if kong in availableKongs])
            # Figure out what blueprint should be placed where
            item_id = GetBlueprintItemForKongAndLevel(level, chosenKong)
            rando_location_id = GetBlueprintLocationForKongAndLevel(level, chosenKong)
            # Assemble the Location object
            location = Location(level, kasplat.name, item_id, Types.Blueprint, chosenKong, [kasplat.map])
            Logic.LocationList[rando_location_id] = location
            # Insert the rando Location into the Region
            kasplatRegion = Logic.Regions[kasplat.region_id]
            kasplatRegion.locations.append(LocationLogic(rando_location_id, kasplat.additional_logic))
            LogicVariables.kasplat_map[rando_location_id] = chosenKong
            spoiler.shuffled_kasplat_map[kasplat.name] = int(chosenKong)
            availableKongs.remove(chosenKong)


def ResetShuffledKasplatLocations():
    """Reset all placed kasplat locations."""
    for level in KasplatLocationList:
        for kasplat in KasplatLocationList[level]:
            # If this kasplat was selected, we need to remove random kasplat locations from the kasplat's logic region
            # This may hit multiple kasplats in the same region at the same time, but that's okay
            if kasplat.selected:
                # Also reset the state of the kasplat, by the end of the loop we'll have no kasplats selected in preparation for the next fill attempt
                kasplat.setKasplat(state=False)
                randomKasplatRegion = Logic.Regions[kasplat.region_id]
                randomKasplatRegion.locations = [loc for loc in randomKasplatRegion.locations if loc.id < Locations.JapesDonkeyKasplatRando or loc.id > Locations.IslesChunkyKasplatRando]


def ShuffleKasplats(LogicVariables):
    """Shuffles the kong assigned to each kasplat."""
    # Make sure only 1 of each kasplat per level, set up array to track that
    level_kongs = []
    kongs = GetKongs()
    # Add a list of kongs for each level
    # Excludes Shops level, but will include a useless Helm level
    for i in range(len(Levels) - 1):
        level_kongs.append(kongs.copy())
    # Remove constants
    for loc, kong in constants.items():
        level = FindLevel(loc)
        level_kongs[level].remove(kong)
    # Set up kasplat map
    LogicVariables.kasplat_map = {}
    # Make all shufflable kasplats initially accessible as anyone
    for location in shufflable.keys():
        LogicVariables.kasplat_map[location] = Kongs.any
    LogicVariables.kasplat_map.update(constants)
    # Do the shuffling
    shuffle_locations = list(shufflable.keys())
    random.shuffle(shuffle_locations)
    while len(shuffle_locations) > 0:
        location = shuffle_locations.pop()
        # Get this location's level and available kongs for this level
        level = FindLevel(location)
        kongs = level_kongs[level]
        random.shuffle(kongs)
        # Check each kong to see if placing it here produces a valid world
        success = False
        for kong in kongs:
            LogicVariables.kasplat_map[location] = kong
            # Assuming Successful placement, remove kong
            level_kongs[level].remove(kong)
            success = True
            break
        if not success:
            raise Ex.KasplatOutOfKongs


def KasplatShuffle(spoiler, LogicVariables):
    """Facilitate the shuffling of kasplat types."""
    # If these were ever set at any prior point (likely only relevant running locally) then reset them - the upcoming methods will handle this TODO: maybe do this on other shufflers
    for location in shufflable:
        Logic.LocationList[location].inaccessible = False
    for location in constants:
        Logic.LocationList[location].inaccessible = False
    if spoiler.settings.kasplat_rando:
        retries = 0
        while True:
            try:
                # Shuffle kasplats
                if spoiler.settings.kasplat_location_rando:
                    ShuffleKasplatsAndLocations(spoiler, LogicVariables)
                else:
                    ShuffleKasplatsInVanillaLocations(spoiler, LogicVariables)
                # Verify world by assuring all locations are still reachable
                Fill.Reset()
                if not Fill.VerifyWorld(spoiler.settings):
                    if retries < 10:
                        raise Ex.KasplatPlacementException
                    else:
                        # This is the first VerifyWorld check, and serves as the canary in the coal mine
                        # If we get to this point in the code, the world itself is likely unstable from some combination of settings or bugs
                        js.postMessage("Settings combination is likely unstable.")
                        raise Ex.SettingsIncompatibleException
                return
            except Ex.KasplatPlacementException:
                retries += 1
                js.postMessage("Kasplat placement failed. Retrying. Tries: " + str(retries))
                # We've added logic in kasplat location rando, now we need to remove it
                if spoiler.settings.kasplat_location_rando:
                    ResetShuffledKasplatLocations()


def InitKasplatMap(LogicVariables):
    """Initialize kasplat_map in logic variables with default values."""
    # Just use default kasplat associations.
    LogicVariables.kasplat_map = {}
    LogicVariables.kasplat_map.update(shufflable)
    LogicVariables.kasplat_map.update(constants)
