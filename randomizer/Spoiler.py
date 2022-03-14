"""Spoiler class and functions."""

import json
from typing import OrderedDict

from randomizer import Logic
from randomizer.Enums.Items import Items
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Types import Types
from randomizer.Enums.MoveTypes import MoveTypes
from randomizer.Lists.Item import ItemFromKong, ItemList
from randomizer.Lists.Location import LocationList
from randomizer.Lists.Minigame import MinigameAssociations, MinigameRequirements
from randomizer.Lists.Songs import Song
from randomizer.MapsAndExits import GetExitId, GetMapId
from randomizer.Settings import Settings
from randomizer.ShuffleExits import ShufflableExits


class Spoiler:
    """Class which contains all spoiler data passed into and out of randomizer."""

    def __init__(self, settings):
        """Initialize spoiler just with settings."""
        self.settings: Settings = settings
        self.playthrough = {}
        self.shuffled_barrel_data = {}
        self.shuffled_exit_data = {}
        self.shuffled_exit_instructions = []
        self.music_bgm_data = {}
        self.music_fanfare_data = {}
        self.music_event_data = {}
        self.location_data = {}

        self.move_data = []
        # 0: Cranky, 1: Funky, 2: Candy
        for i in range(3):
            moves = []
            # One for each kong
            for j in range(5):
                kongmoves = []
                # One for each level
                for k in range(7):
                    kongmoves.append(0)
                moves.append(kongmoves)
            self.move_data.append(moves)

    def toJson(self):
        """Convert spoiler to JSON."""
        # Verify we match our hash
        self.settings.verify_hash()
        # We want to convert raw spoiler data into the important bits and in human-readable formats.
        humanspoiler = OrderedDict()

        # Settings data
        settings = OrderedDict()
        settings["seed"] = self.settings.seed
        settings["algorithm"] = self.settings.algorithm
        settings["shuffle_items"] = self.settings.shuffle_items
        settings["shuffle_loading_zones"] = self.settings.shuffle_loading_zones
        settings["decoupled_loading_zones"] = self.settings.decoupled_loading_zones
        settings["unlock_all_moves"] = self.settings.unlock_all_moves
        settings["unlock_all_kongs"] = self.settings.unlock_all_kongs
        settings["starting_kong"] = ItemList[ItemFromKong(self.settings.starting_kong)].name
        settings["crown_door_open"] = self.settings.crown_door_open
        settings["coin_door_open"] = self.settings.coin_door_open
        settings["unlock_fairy_shockwave"] = self.settings.unlock_fairy_shockwave
        settings["krool_phases"] = self.settings.krool_order
        settings["music_bgm"] = self.settings.music_bgm
        settings["music_fanfares"] = self.settings.music_fanfares
        settings["music_events"] = self.settings.music_events
        settings["fast_start_beginning_of_game"] = self.settings.fast_start_beginning_of_game
        settings["fast_start_hideout_helm"] = self.settings.fast_start_hideout_helm
        settings["quality_of_life"] = self.settings.quality_of_life
        settings["enable_tag_anywhere"] = self.settings.enable_tag_anywhere
        settings["blocker_golden_bananas"] = self.settings.EntryGBs
        settings["troff_n_scoff_bananas"] = self.settings.BossBananas
        humanspoiler["Settings"] = settings

        if self.settings.shuffle_items != "none":
            # Playthrough data
            humanspoiler["Playthrough"] = self.playthrough

            # Item location data
            locations = OrderedDict()
            for location, item in self.location_data.items():
                if not LocationList[location].constant:
                    locations[LocationList[location].name] = ItemList[item].name
            humanspoiler["Locations"] = locations

        if self.settings.shuffle_loading_zones != "none":
            # Shuffled exit data
            shuffled_exits = OrderedDict()
            for exit, dest in self.shuffled_exit_data.items():
                shuffled_exits[ShufflableExits[exit].name] = Logic.Regions[dest.regionId].name + " " + dest.name
            humanspoiler["Shuffled Exits"] = shuffled_exits

        if self.settings.bonus_barrels == "random":
            shuffled_barrels = OrderedDict()
            for location, minigame in self.shuffled_barrel_data.items():
                shuffled_barrels[LocationList[location].name] = MinigameRequirements[minigame].name
            humanspoiler["Shuffled Bonus Barrels"] = shuffled_barrels

        if self.settings.music_bgm == "randomized":
            humanspoiler["Shuffled Music (BGM)"] = self.music_bgm_data
        if self.settings.music_fanfares == "randomized":
            humanspoiler["Shuffled Music Fanfares"] = self.music_fanfare_data
        if self.settings.music_events == "randomized":
            humanspoiler["Shuffled Music Events"] = self.music_event_data

        return json.dumps(humanspoiler, indent=4)

    def UpdateBarrels(self):
        """Update list of shuffled barrel minigames."""
        self.shuffled_barrel_data = {}
        for location, minigame in MinigameAssociations.items():
            self.shuffled_barrel_data[location] = minigame

    def UpdateExits(self):
        """Update list of shuffled exits."""
        self.shuffled_exit_data = {}
        containerMaps = {}
        for key, exit in ShufflableExits.items():
            if exit.shuffled:
                try:
                    vanillaBack = exit.back
                    shuffledBack = ShufflableExits[exit.shuffledId].back
                    self.shuffled_exit_data[key] = shuffledBack
                    containerMapId = GetMapId(exit.region)
                    if containerMapId not in containerMaps:
                        containerMaps[containerMapId] = {
                            "container_map": containerMapId,  # DK Isles
                            "zones": [],
                        }
                    loading_zone_mapping = {}
                    loading_zone_mapping["vanilla_map"] = GetMapId(vanillaBack.regionId)
                    loading_zone_mapping["vanilla_exit"] = GetExitId(vanillaBack)
                    loading_zone_mapping["new_map"] = GetMapId(shuffledBack.regionId)
                    loading_zone_mapping["new_exit"] = GetExitId(shuffledBack)
                    containerMaps[containerMapId]["zones"].append(loading_zone_mapping)
                except Exception as ex:
                    print(ex)
        for key, containerMap in containerMaps.items():
            self.shuffled_exit_instructions.append(containerMap)

    def UpdateLocations(self, locations):
        """Update location list for what was produced by the fill."""
        self.location_data = {}
        for id, location in locations.items():
            if location.item is not None:
                self.location_data[id] = location.item
                if location.type == Types.Shop:
                    # Get indices from the location
                    shop_index = 0  # cranky
                    if location.movetype in [MoveTypes.Guns, MoveTypes.AmmoBelt]:
                        shop_index = 1  # funky
                    elif location.movetype == MoveTypes.Instruments:
                        shop_index = 2  # candy
                    kong_indices = [location.kong]
                    if location.kong == Kongs.any:
                        kong_indices = [Kongs.donkey, Kongs.diddy, Kongs.lanky, Kongs.tiny, Kongs.chunky]
                    level_index = location.level
                    # Use the item to find the data to write
                    data = (ItemList[location.item].movetype << 4) | ItemList[location.item].index
                    for kong_index in kong_indices:
                        self.move_data[shop_index][kong_index][level_index] = data
            # Uncomment for more verbose spoiler with all locations
            # else:
            #     self.location_data[id] = Items.NoItem

    def UpdatePlaythrough(self, locations, playthroughLocations):
        """Write playthrough as a list of dicts of location/item pairs."""
        self.playthrough = {}
        i = 0
        for sphere in playthroughLocations:
            newSphere = {}
            for locationId in sphere:
                location = locations[locationId]
                newSphere[location.name] = ItemList[location.item].name
            self.playthrough[i] = newSphere
            i += 1
