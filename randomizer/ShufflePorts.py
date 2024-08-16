"""Shuffle Bananaport Locations."""

import random
import randomizer.LogicFiles.AngryAztec
import randomizer.LogicFiles.CreepyCastle
import randomizer.LogicFiles.CrystalCaves
import randomizer.LogicFiles.DKIsles
import randomizer.LogicFiles.FranticFactory
import randomizer.LogicFiles.FungiForest
import randomizer.LogicFiles.GloomyGalleon
import randomizer.LogicFiles.JungleJapes
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Events import Events
from randomizer.Enums.Maps import Maps
from randomizer.Enums.Regions import Regions
from randomizer.Enums.Settings import ShufflePortLocations, KasplatRandoSetting
from randomizer.Lists.CustomLocations import CustomLocation, CustomLocations, LocationTypes
from randomizer.Lists.Warps import BananaportVanilla
from randomizer.LogicClasses import Event

def addPort(spoiler, warp: CustomLocation, event_enum: Events):
    """Add bananaport to relevant Logic Region."""
    spoiler.RegionList[warp.logic_region].events.append(Event(event_enum, warp.logic))
    for k in BananaportVanilla:
        if BananaportVanilla[k].event == event_enum:
            BananaportVanilla[k].region_id = warp.logic_region

def getBannedWarps(spoiler) -> list[Events]:
    """Get list of banned warp events based on settings"""
    lst = [
        # All of these float on water, lets make these static
        Events.GalleonW2bTagged,
        Events.GalleonW4bTagged,
        Events.GalleonW5bTagged,
        # Only way to ensure 2 hidden warps don't link to eachother
        Events.CavesW3bTagged,
        Events.CavesW4bTagged,
        Events.CavesW5aTagged,
        # Locations with extra logic
        Events.JapesW5bTagged,
        Events.AztecW5bTagged,
        Events.GalleonW4aTagged,
    ]
    WARP_SHUFFLE_SETTING = spoiler.settings.bananaport_placement_rando
    KASPLAT_LOCATION_RANDO = spoiler.settings.kasplat_rando_setting == KasplatRandoSetting.location_shuffle
    if (not KASPLAT_LOCATION_RANDO and WARP_SHUFFLE_SETTING == ShufflePortLocations.on) or WARP_SHUFFLE_SETTING == ShufflePortLocations.half_vanilla:
        # Access to the Lanky Kasplat
        lst.append(Events.LlamaW2bTagged)
    if WARP_SHUFFLE_SETTING == ShufflePortLocations.half_vanilla:
        lst.extend([
            # Japes
            Events.JapesW1aTagged,  # W1 Portal
            Events.JapesW2aTagged,  # W2 Entrance
            Events.JapesW3aTagged,  # W3 Painting
            Events.JapesW4aTagged,  # W4 Tunnel
            # Aztec
            Events.AztecW1aTagged,  # W1 Portal
            Events.AztecW2aTagged,  # W2 Oasis
            Events.AztecW3aTagged,  # W3 Totem
            Events.AztecW4aTagged,  # W4 Totem
            # Llama
            Events.LlamaW1aTagged,  # W1 Near Entrance
            # Factory
            Events.FactoryW1aTagged,  # W1 Lobby
            Events.FactoryW2aTagged,  # W2 Lobby
            Events.FactoryW3aTagged,  # W3 Lobby
            Events.FactoryW4aTagged,  # W4 Prod Bottom
            Events.FactoryW5bTagged,  # W5 Funky
            # Galleon
            Events.GalleonW1aTagged,  # W1 Main Area
            Events.GalleonW3aTagged,  # W3 Main Area
            # Fungi
            Events.ForestW1aTagged,  # W1 Clock
            Events.ForestW2aTagged,  # W2 Clock
            Events.ForestW3aTagged,  # W3 Clock
            Events.ForestW4aTagged,  # W4 Clock
            Events.ForestW5bTagged,  # W5 Low
            # Caves
            Events.CavesW1aTagged,  # W1 Start
            Events.CavesW2aTagged,  # W2 Start
            # Castle
            Events.CastleW1aTagged,  # W1 Start
            Events.CastleW2aTagged,  # W2 Start
            Events.CastleW3aTagged,  # W3 Start
            Events.CastleW4aTagged,  # W4 Start
            Events.CastleW5aTagged,  # W5 Start
            # Crypt
            Events.CryptW1aTagged,  # W1 Start
            Events.CryptW2aTagged,  # W2 Start
            Events.CryptW3aTagged,  # W3 Start
            # Isles
            Events.IslesW1aTagged,  # W1 Ring
            Events.IslesW2aTagged,  # W2 Ring
            Events.IslesW3aTagged,  # W3 Ring
            Events.IslesW4aTagged,  # W4 Ring
            Events.IslesW5aTagged,  # W5 Ring
        ])
    return lst


def removePorts(spoiler, permitted_levels: list[Levels]):
    """Remove all bananaports from Logic regions."""
    level_logic_regions = {
        Levels.DKIsles: randomizer.LogicFiles.DKIsles.LogicRegions,
        Levels.JungleJapes: randomizer.LogicFiles.JungleJapes.LogicRegions,
        Levels.AngryAztec: randomizer.LogicFiles.AngryAztec.LogicRegions,
        Levels.FranticFactory: randomizer.LogicFiles.FranticFactory.LogicRegions,
        Levels.GloomyGalleon: randomizer.LogicFiles.GloomyGalleon.LogicRegions,
        Levels.FungiForest: randomizer.LogicFiles.FungiForest.LogicRegions,
        Levels.CrystalCaves: randomizer.LogicFiles.CrystalCaves.LogicRegions,
        Levels.CreepyCastle: randomizer.LogicFiles.CreepyCastle.LogicRegions,
    }
    BANNED_PORT_SHUFFLE_EVENTS = getBannedWarps(spoiler)
    for level_id in level_logic_regions:
        if level_id in permitted_levels:
            level = level_logic_regions[level_id]
            for region in level:
                region_data = spoiler.RegionList[region]
                region_data.events = [x for x in region_data.events if x.name < Events.JapesW1aTagged or x.name > Events.IslesW5bTagged or x.name in BANNED_PORT_SHUFFLE_EVENTS]

PortShufflerData = {
    Maps.JungleJapes: {
        "level": Levels.JungleJapes,
        "starting_warp": Events.JapesW1aTagged,
        "global_warp_count": 10,
    },
    Maps.AngryAztec: {
        "level": Levels.AngryAztec,
        "starting_warp": Events.AztecW1aTagged,
        "global_warp_count": 10,
    },
    Maps.FranticFactory: {
        "level": Levels.FranticFactory,
        "starting_warp": Events.FactoryW1aTagged,
        "global_warp_count": 10,
    },
    Maps.GloomyGalleon: {
        "level": Levels.GloomyGalleon,
        "starting_warp": Events.GalleonW1aTagged,
        "global_warp_count": 10,
    },
    Maps.FungiForest: {
        "level": Levels.FungiForest,
        "starting_warp": Events.ForestW1aTagged,
        "global_warp_count": 10,
    },
    Maps.CrystalCaves: {
        "level": Levels.CrystalCaves,
        "starting_warp": Events.CavesW1aTagged,
        "global_warp_count": 10,
    },
    Maps.CreepyCastle: {
        "level": Levels.CreepyCastle,
        "starting_warp": Events.CastleW1aTagged,
        "global_warp_count": 10,
    },
    Maps.Isles: {
        "level": Levels.DKIsles,
        "starting_warp": Events.IslesW1aTagged,
        "global_warp_count": 10,
    },
    Maps.AztecLlamaTemple: {
        "level": Levels.AngryAztec,
        "starting_warp": Events.LlamaW1aTagged,
        "global_warp_count": 4,
    },
    Maps.CastleCrypt: {
        "level": Levels.CreepyCastle,
        "starting_warp": Events.CryptW1aTagged,
        "global_warp_count": 6,
    },
}

def ResetPorts():
    """Reset all bananaports to their vanilla state."""
    for k in BananaportVanilla:
        BananaportVanilla[k].reset()

# TODO: Add Llama, Factory->Castle warps to CustomLocations (boring)

def isCustomLocationValid(spoiler, location: CustomLocation, map_id: Maps, level: Levels) -> bool:
    """Determines whether a custom location is valid for a warp pad."""
    if location.map != map_id:
        # Has to be in the right map
        return False
    BANNED_PORT_SHUFFLE_EVENTS = getBannedWarps(spoiler)
    if location.tied_warp_event in BANNED_PORT_SHUFFLE_EVENTS:
        # Disable all locked warp locations
        return False
    if spoiler.settings.enable_plandomizer:
        if location.name in spoiler.settings.plandomizer_dict["reserved_custom_locations"][level]:
            return False
    return location.isValidLocation(LocationTypes.Bananaport)

REGION_KLUMPS = {
    # A way to bias against zones of a map with a lot of logic regions
    # Any entries in the list will sort regarding region dict based on the key rather than the normal value
    Regions.IslesMainUpper: [Regions.IslesEar, Regions.IslesHill],
    Regions.KremIsleBeyondLift: [Regions.KremIsleMouth, Regions.KremIsleTopLevel],
    Regions.CabinIsle: [Regions.IslesAboveWaterfall],
    Regions.JungleJapesMain: [Regions.JapesTnSAlcove],
    Regions.JapesHill: [Regions.JapesHillTop, Regions.JapesCannonPlatform, Regions.JapesTopOfMountain],
    Regions.JapesBeyondCoconutGate2: [Regions.JapesLankyCave],
    Regions.AztecTunnelBeforeOasis: [Regions.AngryAztecStart, Regions.BetweenVinesByPortal],
    Regions.LlamaTemple: [Regions.LlamaTempleBack],
    Regions.RandD: [Regions.RandDUpper],
    Regions.MiddleCore: [Regions.SpinningCore, Regions.UpperCore],
    Regions.MushroomLowerExterior: [Regions.MushroomNightExterior, Regions.MushroomUpperExterior, Regions.MushroomUpperMidExterior],
    Regions.MillArea: [Regions.ForestTopOfMill, Regions.ForestVeryTopOfMill],
    Regions.CrystalCavesMain: [Regions.CavesBlueprintPillar, Regions.CavesBananaportSpire, Regions.CavesBonusCave]
}

def ShufflePorts(spoiler, port_selection, human_ports):
    """Shuffle the location of bananaports."""
    levels_to_check = [
        # We can change this based on Jacob's multiselector
        Levels.JungleJapes,
        Levels.AngryAztec,
        Levels.FranticFactory,
        Levels.GloomyGalleon,
        Levels.FungiForest,
        Levels.CrystalCaves,
        Levels.CreepyCastle,
        Levels.DKIsles,
    ]
    removePorts(spoiler, levels_to_check)
    BANNED_PORT_SHUFFLE_EVENTS = getBannedWarps(spoiler)
    for level in levels_to_check:
        level_lst = CustomLocations[level]
        for map in PortShufflerData:
            if PortShufflerData[map]["level"] == level:
                index_lst = list(range(len(level_lst)))
                index_lst = [x for x in index_lst if isCustomLocationValid(spoiler, level_lst[x], map, level)]
                global_count = PortShufflerData[map]["global_warp_count"]
                start_event = PortShufflerData[map]["starting_warp"]
                end_event = start_event + PortShufflerData[map]["global_warp_count"]
                pick_count = global_count - len([x for x in BANNED_PORT_SHUFFLE_EVENTS if x >= start_event and x < end_event])
                if len(index_lst) < pick_count:
                    print(f"Lowering pick count for {map.name} from {pick_count} to {len(index_lst)}")
                pick_count = min(pick_count, len(index_lst))
                warps = []
                if spoiler.settings.useful_bananaport_placement:
                    random.shuffle(index_lst)
                    # Populate the region dict with custom locations in each region
                    region_dict = {}
                    for x in index_lst:
                        region = level_lst[x].logic_region
                        # Calculate the region based on klumping
                        for prop_region in REGION_KLUMPS:
                            if region in REGION_KLUMPS[prop_region]:
                                region = prop_region
                                break
                        # Populate dict
                        if region not in region_dict:
                            region_dict[region] = []
                        region_dict[region].append(x)
                    # For all regions, push the first location in each region. Loop through regions repeatedly until warp list is filled
                    counter = pick_count
                    while counter > 0:
                        region_lst = [x for xi, x in enumerate(list(region_dict.keys())) if xi < counter]
                        for region in region_lst:
                            selected_warp = region_dict[region].pop(0)
                            warps.append(selected_warp)
                            counter -= 1
                        del_lst = []
                        for region in region_dict:
                            if len(region_dict[region]) == 0:  # delete any empty region
                                del_lst.append(region)
                        for region in del_lst:
                            del region_dict[region]
                else:
                    warps = random.sample(index_lst, pick_count)
                idx_selection = 0
                if pick_count > 0:
                    for k in BananaportVanilla:
                        event_id = BananaportVanilla[k].event
                        if event_id >= start_event and event_id < end_event and event_id not in BANNED_PORT_SHUFFLE_EVENTS:
                            selected_port = warps[idx_selection]
                            port_selection[k] = selected_port
                            addPort(spoiler, level_lst[selected_port], event_id)
                            CustomLocations[level][selected_port].setCustomLocation(True)
                            human_ports[event_id.name] = level_lst[selected_port].name
                            idx_selection += 1
                            if idx_selection >= pick_count:
                                break