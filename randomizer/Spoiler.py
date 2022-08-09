"""Spoiler class and functions."""

import json
from typing import OrderedDict

from randomizer.Enums.Events import Events
from randomizer.Enums.Items import Items
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.MoveTypes import MoveTypes
from randomizer.Enums.Transitions import Transitions
from randomizer.Enums.Regions import Regions
from randomizer.Enums.Types import Types
from randomizer.Lists.Item import ItemFromKong, NameFromKong, KongFromItem, ItemList
from randomizer.Lists.Location import LocationList
from randomizer.Lists.Minigame import BarrelMetaData, HelmMinigameLocations, MinigameRequirements
from randomizer.Lists.MapsAndExits import GetExitId, GetMapId, Maps
from randomizer.Settings import Settings
from randomizer.ShuffleExits import ShufflableExits


class Spoiler:
    """Class which contains all spoiler data passed into and out of randomizer."""

    def __init__(self, settings):
        """Initialize spoiler just with settings."""
        self.settings: Settings = settings
        self.playthrough = {}
        self.woth = {}
        self.shuffled_barrel_data = {}
        self.shuffled_exit_data = {}
        self.shuffled_exit_instructions = []
        self.music_bgm_data = {}
        self.music_fanfare_data = {}
        self.music_event_data = {}
        self.location_data = {}
        self.enemy_replacements = []

        self.move_data = []
        # 0: Cranky, 1: Funky, 2: Candy
        for i in range(3):
            moves = []
            # One for each kong
            for j in range(5):
                kongmoves = []
                # One for each level
                for k in range(8):
                    kongmoves.append(-1)
                moves.append(kongmoves)
            self.move_data.append(moves)

        self.hint_list = {}

    def toJson(self):
        """Convert spoiler to JSON."""
        # Verify we match our hash
        self.settings.verify_hash()
        # We want to convert raw spoiler data into the important bits and in human-readable formats.
        humanspoiler = OrderedDict()

        # Settings data
        settings = OrderedDict()
        settings["seed"] = self.settings.seed_id
        # settings["algorithm"] = self.settings.algorithm # Don't need this for now, probably
        settings["no_logic"] = self.settings.no_logic
        settings["move_rando"] = self.settings.move_rando
        settings["shuffle_loading_zones"] = self.settings.shuffle_loading_zones
        settings["decoupled_loading_zones"] = self.settings.decoupled_loading_zones
        settings["starting_kongs_count"] = self.settings.starting_kongs_count
        startKongList = []
        for x in self.settings.starting_kong_list:
            startKongList.append(x.name.capitalize())
        settings["starting_kong_list"] = startKongList
        settings["colors"] = self.settings.colors
        settings["diddy_freeing_kong"] = ItemList[ItemFromKong(self.settings.diddy_freeing_kong)].name
        settings["tiny_freeing_kong"] = ItemList[ItemFromKong(self.settings.tiny_freeing_kong)].name
        settings["lanky_freeing_kong"] = ItemList[ItemFromKong(self.settings.lanky_freeing_kong)].name
        settings["chunky_freeing_kong"] = ItemList[ItemFromKong(self.settings.chunky_freeing_kong)].name
        settings["open_lobbies"] = self.settings.open_lobbies
        settings["open_levels"] = self.settings.open_levels
        settings["randomize_pickups"] = self.settings.randomize_pickups
        settings["random_patches"] = self.settings.random_patches
        settings["puzzle_rando"] = self.settings.puzzle_rando
        settings["crown_door_open"] = self.settings.crown_door_open
        settings["coin_door_open"] = self.settings.coin_door_open
        settings["unlock_fairy_shockwave"] = self.settings.unlock_fairy_shockwave
        settings["random_medal_requirement"] = self.settings.random_medal_requirement
        if self.settings.coin_door_open in ["need_both", "need_rw"]:
            settings["medal_requirement"] = self.settings.medal_requirement
        settings["random_prices"] = self.settings.random_prices
        settings["bananaport_rando"] = self.settings.bananaport_rando
        settings["shuffle_shop_locations"] = self.settings.shuffle_shops
        settings["krool_phases"] = self.settings.krool_order
        settings["krool_access"] = self.settings.krool_access
        settings["krool_keys_required"] = self.GetKroolKeysRequired(self.settings.krool_keys_required)
        settings["music_bgm"] = self.settings.music_bgm
        settings["music_fanfares"] = self.settings.music_fanfares
        settings["music_events"] = self.settings.music_events
        settings["fast_start_beginning_of_game"] = self.settings.fast_start_beginning_of_game
        settings["helm_setting"] = self.settings.helm_setting
        settings["quality_of_life"] = self.settings.quality_of_life
        settings["enable_tag_anywhere"] = self.settings.enable_tag_anywhere
        settings["fast_gbs"] = self.settings.fast_gbs
        settings["high_req"] = self.settings.high_req
        settings["blocker_golden_bananas"] = self.settings.EntryGBs
        settings["troff_n_scoff_bananas"] = self.settings.BossBananas
        humanspoiler["Settings"] = settings

        if self.settings.shuffle_items != "none":
            # Playthrough data
            humanspoiler["Playthrough"] = self.playthrough

            # Woth data
            humanspoiler["Way_of_the_Hoard"] = self.woth

            # Item location data
            locations = OrderedDict()
            for location, item in self.location_data.items():
                if not LocationList[location].constant:
                    locations[LocationList[location].name] = ItemList[item].name
            humanspoiler["Locations"] = locations

        if self.settings.random_prices != "vanilla":
            prices = OrderedDict()
            for item, price in self.settings.prices.items():
                if item == Items.ProgressiveSlam:
                    prices["Super Simian Slam"] = price[0]
                    prices["Super Duper Simian Slam"] = price[1]
                elif item == Items.ProgressiveAmmoBelt:
                    prices["Ammo Belt 1"] = price[0]
                    prices["Ammo Belt 2"] = price[1]
                elif item == Items.ProgressiveInstrumentUpgrade:
                    prices["Music Upgrade 1"] = price[0]
                    prices["Third Melon"] = price[1]
                    prices["Music Upgrade 2"] = price[2]
                else:
                    prices[ItemList[item].name] = price
            humanspoiler["Prices"] = prices

        if self.settings.shuffle_loading_zones == "levels":
            # Just show level order
            shuffled_exits = OrderedDict()
            lobby_entrance_order = {
                Transitions.IslesMainToJapesLobby: Levels.JungleJapes,
                Transitions.IslesMainToAztecLobby: Levels.AngryAztec,
                Transitions.IslesMainToFactoryLobby: Levels.FranticFactory,
                Transitions.IslesMainToGalleonLobby: Levels.GloomyGalleon,
                Transitions.IslesMainToForestLobby: Levels.FungiForest,
                Transitions.IslesMainToCavesLobby: Levels.CrystalCaves,
                Transitions.IslesMainToCastleLobby: Levels.CreepyCastle,
            }
            lobby_exit_order = {
                Transitions.IslesJapesLobbyToMain: Levels.JungleJapes,
                Transitions.IslesAztecLobbyToMain: Levels.AngryAztec,
                Transitions.IslesFactoryLobbyToMain: Levels.FranticFactory,
                Transitions.IslesGalleonLobbyToMain: Levels.GloomyGalleon,
                Transitions.IslesForestLobbyToMain: Levels.FungiForest,
                Transitions.IslesCavesLobbyToMain: Levels.CrystalCaves,
                Transitions.IslesCastleLobbyToMain: Levels.CreepyCastle,
            }
            for transition, vanilla_level in lobby_entrance_order.items():
                shuffled_level = lobby_exit_order[self.shuffled_exit_data[transition].reverse]
                shuffled_exits[vanilla_level.name] = shuffled_level.name
            humanspoiler["Shuffled Level Order"] = shuffled_exits
        elif self.settings.shuffle_loading_zones != "none":
            # Show full shuffled_exits data if more than just levels are shuffled
            shuffled_exits = OrderedDict()
            for exit, dest in self.shuffled_exit_data.items():
                shuffled_exits[ShufflableExits[exit].name] = dest.spoilerName
            humanspoiler["Shuffled Exits"] = shuffled_exits

        if self.settings.boss_location_rando:
            shuffled_bosses = OrderedDict()
            for i in range(7):
                shuffled_bosses[Levels(i).name] = Maps(self.settings.boss_maps[i]).name
            humanspoiler["Shuffled Boss Order"] = shuffled_bosses

        if self.settings.boss_kong_rando:
            shuffled_boss_kongs = OrderedDict()
            for i in range(7):
                shuffled_boss_kongs[Levels(i).name] = Kongs(self.settings.boss_kongs[i]).name
            humanspoiler["Shuffled Boss Kongs"] = shuffled_boss_kongs
            kutout_order = ""
            for kong in self.settings.kutout_kongs:
                kutout_order = kutout_order + Kongs(kong).name + ", "
            humanspoiler["Shuffled Kutout Kong Order"] = kutout_order.removesuffix(", ")

        if self.settings.hard_bosses:
            phase_names = []
            for phase in self.settings.kko_phase_order:
                phase_names.append(f"Phase {phase+1}")
            humanspoiler["Shuffled Kutout Phases"] = ", ".join(phase_names)

        if self.settings.bonus_barrels in ("random", "all_beaver_bother"):
            shuffled_barrels = OrderedDict()
            for location, minigame in self.shuffled_barrel_data.items():
                if location in HelmMinigameLocations and self.settings.helm_barrels == "skip":
                    continue
                if location not in HelmMinigameLocations and self.settings.bonus_barrels == "skip":
                    continue
                shuffled_barrels[LocationList[location].name] = MinigameRequirements[minigame].name
            if len(shuffled_barrels) > 0:
                humanspoiler["Shuffled Bonus Barrels"] = shuffled_barrels

        if self.settings.music_bgm == "randomized":
            humanspoiler["Shuffled Music (BGM)"] = self.music_bgm_data
        if self.settings.music_fanfares == "randomized":
            humanspoiler["Shuffled Music Fanfares"] = self.music_fanfare_data
        if self.settings.music_events == "randomized":
            humanspoiler["Shuffled Music Events"] = self.music_event_data
        if self.settings.kasplat_rando:
            humanspoiler["Shuffled Kasplats"] = self.human_kasplats
        if self.settings.random_patches:
            humanspoiler["Shuffled Dirt Patches"] = self.human_patches
        if self.settings.bananaport_rando:
            humanspoiler["Shuffled Bananaports"] = self.human_warp_locations
        if len(self.hint_list) > 0:
            humanspoiler["Wrinkly Hints"] = self.hint_list
        if self.settings.shuffle_shops:
            shop_location_dict = {}
            for level in self.shuffled_shop_locations:
                level_name = "Unknown Level"

                level_dict = {
                    Levels.DKIsles: "DK Isles",
                    Levels.JungleJapes: "Jungle Japes",
                    Levels.AngryAztec: "Angry Aztec",
                    Levels.FranticFactory: "Frantic Factory",
                    Levels.GloomyGalleon: "Gloomy Galleon",
                    Levels.FungiForest: "Fungi Forest",
                    Levels.CrystalCaves: "Crystal Caves",
                    Levels.CreepyCastle: "Creepy Castle",
                }
                shop_dict = {Regions.CrankyGeneric: "Cranky", Regions.CandyGeneric: "Candy", Regions.FunkyGeneric: "Funky", Regions.Snide: "Snide"}
                if level in level_dict:
                    level_name = level_dict[level]
                for shop in self.shuffled_shop_locations[level]:
                    location_name = "Unknown Shop"
                    shop_name = "Unknown Shop"
                    new_shop = self.shuffled_shop_locations[level][shop]
                    if shop in shop_dict:
                        location_name = shop_dict[shop]
                    if new_shop in shop_dict:
                        shop_name = shop_dict[new_shop]
                    shop_location_dict[f"{level_name} - {location_name}"] = shop_name
            humanspoiler["Shop Locations"] = shop_location_dict

        return json.dumps(humanspoiler, indent=4)

    def UpdateKasplats(self, kasplat_map):
        """Update kasplat data."""
        for kasplat, kong in kasplat_map.items():
            # Get kasplat info
            location = LocationList[kasplat]
            mapId = location.map
            original = location.kong
            self.human_kasplats[location.name] = NameFromKong(kong)
            map = None
            # See if map already exists in enemy_replacements
            for m in self.enemy_replacements:
                if m["container_map"] == mapId:
                    map = m
                    break
            # If not, create it
            if map is None:
                map = {"container_map": mapId}
                self.enemy_replacements.append(map)
            # Create kasplat_swaps section if doesn't exist
            if "kasplat_swaps" not in map:
                map["kasplat_swaps"] = []
            # Create swap entry and add to map
            swap = {"vanilla_location": original, "replace_with": kong}
            map["kasplat_swaps"].append(swap)

    def UpdateBarrels(self):
        """Update list of shuffled barrel minigames."""
        self.shuffled_barrel_data = {}
        for location, minigame in [(key, value.minigame) for (key, value) in BarrelMetaData.items()]:
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
                        containerMaps[containerMapId] = {"container_map": containerMapId, "zones": []}  # DK Isles
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
        self.shuffled_kong_placement = {}
        # Go ahead and set starting kong
        startkong = {"kong": self.settings.starting_kong, "write": 0x151}
        trainingGrounds = {"locked": startkong}
        self.shuffled_kong_placement["TrainingGrounds"] = trainingGrounds
        # Write additional starting kongs to empty cages, if any
        emptyCages = [x for x in [Locations.DiddyKong, Locations.LankyKong, Locations.TinyKong, Locations.ChunkyKong] if x not in self.settings.kong_locations]
        for emptyCage in emptyCages:
            self.WriteKongPlacement(emptyCage, Items.NoItem)

        # Loop through locations and set necessary data
        for id, location in locations.items():
            if location.item is not None and location.item is not Items.NoItem and not location.constant:
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
                    # Isles level index is 8, but we need it to be 7 to fit it in move_data
                    if level_index == 8:
                        level_index = 7
                    # Use the item to find the data to write
                    move_type = ItemList[location.item].movetype
                    move_level = ItemList[location.item].index - 1
                    move_kong = ItemList[location.item].kong
                    for kong_index in kong_indices:
                        # print(f"Shop {shop_index}, Kong {kong_index}, Level {level_index} | Move: {move_type} lvl {move_level} for kong {move_kong}")
                        if move_type == 1 or move_type == 3 or (move_type == 2 and move_level > 0) or (move_type == 4 and move_level > 0):
                            move_kong = kong_index
                        data = (move_type << 5) | (move_level << 3) | move_kong
                        self.move_data[shop_index][kong_index][level_index] = data
                elif location.type == Types.Kong:
                    self.WriteKongPlacement(id, location.item)
            # Uncomment for more verbose spoiler with all locations
            # else:
            #     self.location_data[id] = Items.NoItem

    def WriteKongPlacement(self, locationId, item):
        """Write kong placement information for the given kong cage location."""
        locationName = "Jungle Japes"
        unlockKong = self.settings.diddy_freeing_kong
        lockedwrite = 0x152
        puzzlewrite = 0x153
        if locationId == Locations.LankyKong:
            locationName = "Llama Temple"
            unlockKong = self.settings.lanky_freeing_kong
            lockedwrite = 0x154
            puzzlewrite = 0x155
        elif locationId == Locations.TinyKong:
            locationName = "Tiny Temple"
            unlockKong = self.settings.tiny_freeing_kong
            lockedwrite = 0x156
            puzzlewrite = 0x157
        elif locationId == Locations.ChunkyKong:
            locationName = "Frantic Factory"
            unlockKong = self.settings.chunky_freeing_kong
            lockedwrite = 0x158
            puzzlewrite = 0x159
        lockedkong = {}
        lockedkong["kong"] = KongFromItem(item)
        lockedkong["write"] = lockedwrite
        puzzlekong = {"kong": unlockKong, "write": puzzlewrite}
        kongLocation = {"locked": lockedkong, "puzzle": puzzlekong}
        self.shuffled_kong_placement[locationName] = kongLocation

    def UpdatePlaythrough(self, locations, playthroughLocations):
        """Write playthrough as a list of dicts of location/item pairs."""
        self.playthrough = {}
        i = 0
        for sphere in playthroughLocations:
            newSphere = {}
            newSphere["Available GBs"] = sphere.availableGBs
            sphereLocations = list(map(lambda l: locations[l], sphere.locations))
            sphereLocations.sort(key=lambda l: l.type == Types.Banana)
            for location in sphereLocations:
                newSphere[location.name] = ItemList[location.item].name
            self.playthrough[i] = newSphere
            i += 1

    def UpdateWoth(self, locations, wothLocations):
        """Write woth locations as a dict of location/item pairs."""
        self.woth = {}
        for locationId in wothLocations:
            location = locations[locationId]
            self.woth[location.name] = ItemList[location.item].name

    @staticmethod
    def GetKroolKeysRequired(keyEvents):
        """Get key names from required key events to print in the spoiler."""
        keys = []
        if Events.JapesKeyTurnedIn in keyEvents:
            keys.append("Jungle Japes Key")
        if Events.AztecKeyTurnedIn in keyEvents:
            keys.append("Angry Aztec Key")
        if Events.FactoryKeyTurnedIn in keyEvents:
            keys.append("Frantic Factory Key")
        if Events.GalleonKeyTurnedIn in keyEvents:
            keys.append("Gloomy Galleon Key")
        if Events.ForestKeyTurnedIn in keyEvents:
            keys.append("Fungi Forest Key")
        if Events.CavesKeyTurnedIn in keyEvents:
            keys.append("Crystal Caves Key")
        if Events.CastleKeyTurnedIn in keyEvents:
            keys.append("Creepy Castle Key")
        if Events.HelmKeyTurnedIn in keyEvents:
            keys.append("Hideout Helm Key")
        return keys
