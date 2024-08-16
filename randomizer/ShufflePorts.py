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
from randomizer.Enums.Settings import MiscChangesSelected, ShufflePortLocations, CBRando, KasplatRandoSetting
from randomizer.Lists.CustomLocations import CustomLocation, CustomLocations, LocationTypes
from randomizer.Lists.Warps import BananaportVanilla
from randomizer.LogicClasses import Event
from randomizer.Patching.Lib import IsItemSelected

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
    ]
    WARP_SHUFFLE_SETTING = spoiler.settings.bananaport_placement_rando
    JAPES_BRIDGE_PERM = IsItemSelected(spoiler.settings.quality_of_life, spoiler.settings.misc_changes_selected, MiscChangesSelected.japes_bridge_permanently_extended)
    COIN_RANDO = spoiler.settings.coin_rando
    CB_RANDO = spoiler.settings.cb_rando != CBRando.off
    KASPLAT_LOCATION_RANDO = spoiler.settings.kasplat_rando_setting == KasplatRandoSetting.location_shuffle
    if (not JAPES_BRIDGE_PERM) or WARP_SHUFFLE_SETTING in (ShufflePortLocations.vanilla_only, ShufflePortLocations.half_vanilla):
        # Access to top of mountain region if the QoL setting isn't enabled
        lst.append(Events.JapesW5bTagged)
    if (not COIN_RANDO) or (not CB_RANDO) or WARP_SHUFFLE_SETTING in (ShufflePortLocations.vanilla_only, ShufflePortLocations.half_vanilla):
        # Access to the Chunky coins with vanilla coins, Diddy CBs
        lst.append(Events.AztecW5bTagged)
    if (not KASPLAT_LOCATION_RANDO and WARP_SHUFFLE_SETTING == ShufflePortLocations.on) or WARP_SHUFFLE_SETTING == ShufflePortLocations.half_vanilla:
        # Access to the Lanky Kasplat
        lst.append(Events.LlamaW2bTagged)
    if (not KASPLAT_LOCATION_RANDO) or WARP_SHUFFLE_SETTING in (ShufflePortLocations.vanilla_only, ShufflePortLocations.half_vanilla):
        # Access to the DK Kasplat with vanilla/vanilla shuffle kasplats
        lst.append(Events.GalleonW4aTagged)
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


def removePorts(spoiler):
    """Remove all bananaports from Logic regions."""
    level_logic_regions = [
        randomizer.LogicFiles.DKIsles.LogicRegions,
        randomizer.LogicFiles.JungleJapes.LogicRegions,
        randomizer.LogicFiles.AngryAztec.LogicRegions,
        randomizer.LogicFiles.FranticFactory.LogicRegions,
        randomizer.LogicFiles.GloomyGalleon.LogicRegions,
        randomizer.LogicFiles.FungiForest.LogicRegions,
        randomizer.LogicFiles.CrystalCaves.LogicRegions,
        randomizer.LogicFiles.CreepyCastle.LogicRegions,
    ]
    BANNED_PORT_SHUFFLE_EVENTS = getBannedWarps(spoiler)
    for level in level_logic_regions:
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

def ShufflePorts(spoiler, port_selection, human_ports):
    """Shuffle the location of bananaports."""
    removePorts(spoiler)
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
    BANNED_PORT_SHUFFLE_EVENTS = getBannedWarps(spoiler)
    for level in levels_to_check:
        level_lst = CustomLocations[level]
        index_lst = list(range(len(level_lst)))
        for map in PortShufflerData:
            if PortShufflerData[map]["level"] == level:
                index_lst = [x for x in index_lst if (not level_lst[x].selected) and (LocationTypes.Bananaport not in level_lst[x].banned_types) and (level_lst[x].map == map)]
                global_count = PortShufflerData[map]["global_warp_count"]
                start_event = PortShufflerData[map]["starting_warp"]
                end_event = start_event + PortShufflerData[map]["global_warp_count"]
                pick_count = global_count - len([x for x in BANNED_PORT_SHUFFLE_EVENTS if x >= start_event and x < end_event])
                if len(index_lst) < pick_count:
                    print(f"Lowering pick count for {map.name} from {pick_count} to {len(index_lst)}")
                pick_count = min(pick_count, len(index_lst))
                warps = random.sample(index_lst, pick_count)
                idx_selection = 0
                if pick_count > 0:
                    for k in BananaportVanilla:
                        event_id = BananaportVanilla[k].event
                        if event_id >= start_event and event_id < end_event and event_id not in BANNED_PORT_SHUFFLE_EVENTS:
                            selected_port = warps[idx_selection]
                            port_selection[k] = selected_port
                            print(k.name, level_lst[selected_port].name)
                            addPort(spoiler, level_lst[selected_port], event_id)
                            CustomLocations[level][selected_port].setCustomLocation(True)
                            human_ports[event_id.name] = level_lst[selected_port].name
                            idx_selection += 1
                            if idx_selection >= pick_count:
                                break