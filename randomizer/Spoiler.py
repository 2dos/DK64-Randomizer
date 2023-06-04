"""Spoiler class and functions."""

import json
from email.policy import default
from typing import OrderedDict

import randomizer.ItemPool as ItemPool
from randomizer.Enums.Events import Events
from randomizer.Enums.Items import Items
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.MoveTypes import MoveTypes
from randomizer.Enums.Regions import Regions
from randomizer.Enums.Settings import BananaportRando, GlitchesSelected, HelmDoorItem, LogicType, MinigameBarrels, RandomPrices, ShockwaveStatus, ShuffleLoadingZones, TrainingBarrels, WinCondition
from randomizer.Enums.Transitions import Transitions
from randomizer.Enums.Types import Types
from randomizer.Lists.Item import ItemFromKong, ItemList, KongFromItem, NameFromKong
from randomizer.Lists.Location import LocationList, PreGivenLocations
from randomizer.Lists.Logic import GlitchLogicItems
from randomizer.Lists.MapsAndExits import GetExitId, GetMapId, Maps
from randomizer.Lists.Minigame import BarrelMetaData, HelmMinigameLocations, MinigameRequirements
from randomizer.Prices import ProgressiveMoves
from randomizer.Settings import Settings
from randomizer.ShuffleExits import ShufflableExits


class Spoiler:
    """Class which contains all spoiler data passed into and out of randomizer."""

    def __init__(self, settings):
        """Initialize spoiler just with settings."""
        self.settings: Settings = settings
        self.playthrough = {}
        self.woth = {}
        self.woth_locations = {}
        self.woth_paths = {}
        self.krool_paths = {}
        self.shuffled_barrel_data = {}
        self.shuffled_exit_data = {}
        self.shuffled_exit_instructions = []
        self.music_bgm_data = {}
        self.music_majoritem_data = {}
        self.music_minoritem_data = {}
        self.music_event_data = {}
        self.location_data = {}
        self.enemy_replacements = []

        self.debug_human_item_assignment = None  # Kill this as soon as the spoiler is better

        self.move_data = []
        # 0: Cranky, 1: Funky, 2: Candy
        for move_master_type in range(3):
            master_moves = []
            if move_master_type == 0:
                # Shop
                for shop_index in range(3):
                    moves = []
                    # One for each kong
                    for kong_index in range(5):
                        kongmoves = []
                        # One for each level
                        for level_index in range(8):
                            kongmoves.append({"move_type": None})
                        moves.append(kongmoves)
                    master_moves.append(moves)
            elif move_master_type == 1:
                # Training Barrels
                if self.settings.training_barrels == TrainingBarrels.normal:
                    for tbarrel_type in ["dive", "orange", "barrel", "vine"]:
                        master_moves.append({"move_type": "flag", "flag": tbarrel_type, "price": 0})
                else:
                    for tbarrel_type in ["dive", "orange", "barrel", "vine"]:
                        master_moves.append({"move_type": None})
            elif move_master_type == 2:
                # BFI
                if self.settings.shockwave_status == ShockwaveStatus.vanilla:
                    master_moves = [{"move_type": "flag", "flag": "camera_shockwave", "price": 0}]
                else:
                    master_moves = [{"move_type": None}]
            self.move_data.append(master_moves)

        self.hint_list = {}

    def getItemGroup(self, item):
        """Get item group from item."""
        if item is None:
            item = Items.NoItem
        if item == Items.NoItem:
            return "Empty"
        item_type = ItemList[item].type
        type_dict = {
            Types.Kong: "Kongs",
            Types.Shop: "Moves",
            Types.Shockwave: "Moves",
            Types.TrainingBarrel: "Moves",
            Types.Banana: "Golden Bananas",
            Types.Blueprint: "Blueprints",
            Types.Fairy: "Fairies",
            Types.Key: "Keys",
            Types.Crown: "Crowns",
            Types.Medal: "Medals",
            Types.Coin: "Coins",
            Types.Bean: "Miscellaneous Items",
            Types.Pearl: "Miscellaneous Items",
            Types.RainbowCoin: "Rainbow Coins",
            Types.FakeItem: "Ice Traps",
            Types.JunkItem: "Junk Items",
        }
        if item_type in type_dict:
            return type_dict[item_type]
        return "Unknown"

    def createJson(self):
        """Convert spoiler to JSON and save it."""
        # Verify we match our hash
        self.settings.verify_hash()
        # We want to convert raw spoiler data into the important bits and in human-readable formats.
        humanspoiler = OrderedDict()

        # Settings data
        settings = OrderedDict()
        settings["Seed"] = self.settings.seed_id
        # settings["algorithm"] = self.settings.algorithm # Don't need this for now, probably
        logic_types = {LogicType.nologic: "No Logic", LogicType.glitch: "Glitched Logic", LogicType.glitchless: "Glitchless Logic"}
        if self.settings.logic_type in logic_types:
            settings["Logic Type"] = logic_types[self.settings.logic_type]
        else:
            settings["Logic Type"] = self.settings.logic_type
        if self.settings.logic_type == LogicType.glitch:
            settings["Glitches Enabled"] = ", ".join(
                [x.name for x in GlitchLogicItems if GlitchesSelected[x.shorthand] in self.settings.glitches_selected or len(self.settings.glitches_selected) == 0]
            )
        settings["Shuffle Enemies"] = self.settings.enemy_rando
        settings["Move Randomization type"] = self.settings.move_rando.name
        settings["Loading Zones Shuffled"] = self.settings.shuffle_loading_zones.name
        settings["Decoupled Loading Zones"] = self.settings.decoupled_loading_zones
        startKongList = []
        for x in self.settings.starting_kong_list:
            startKongList.append(x.name.capitalize())
        settings["Hard B Lockers"] = self.settings.hard_blockers
        if self.settings.randomize_blocker_required_amounts:
            settings["Maximum B Locker"] = self.settings.blocker_text
        settings["Hard Troff N Scoff"] = self.settings.hard_troff_n_scoff
        if self.settings.randomize_cb_required_amounts:
            settings["Maximum Troff N Scoff"] = self.settings.troff_text
        settings["Open Lobbies"] = self.settings.open_lobbies
        settings["Open Levels"] = self.settings.open_levels
        settings["Auto Complete Bonus Barrels"] = self.settings.bonus_barrel_auto_complete
        settings["Complex Level Order"] = self.settings.hard_level_progression
        settings["Progressive Switch Strength"] = self.settings.alter_switch_allocation
        settings["Hard Bosses"] = self.settings.hard_bosses
        settings["Hard Shooting"] = self.settings.hard_shooting
        settings["Free Trade Agreement"] = self.settings.free_trade_setting.name
        settings["Randomize Pickups"] = self.settings.randomize_pickups
        settings["Randomize Patches"] = self.settings.random_patches
        settings["Randomize CB Locations"] = self.settings.cb_rando
        settings["Randomize Coin Locations"] = self.settings.coin_rando
        settings["Puzzle Randomization"] = self.settings.puzzle_rando
        settings["Crown Door Open"] = self.settings.crown_door_item == HelmDoorItem.opened
        settings["Coin Door Open"] = self.settings.coin_door_item == HelmDoorItem.opened
        settings["Shockwave Shuffle"] = self.settings.shockwave_status.name
        settings["Random Jetpac Medal Requirement"] = self.settings.random_medal_requirement
        settings["Bananas Required for Medal"] = self.settings.medal_cb_req
        settings["Fairies Required for Rareware GB"] = self.settings.rareware_gb_fairies
        settings["Random Shop Prices"] = self.settings.random_prices.name
        settings["Banana Port Randomization"] = self.settings.bananaport_rando.name
        settings["Activated Warps"] = self.settings.activate_all_bananaports.name
        settings["Shuffle Shop Locations"] = self.settings.shuffle_shops
        settings["Shuffle Kasplats"] = self.settings.kasplat_rando_setting.name

        settings["Key 8 Required"] = self.settings.krool_access
        settings["Key 8 in Helm"] = self.settings.key_8_helm
        settings["Select Starting Keys"] = self.settings.select_keys
        if not self.settings.keys_random:
            settings["Number of Keys Required"] = self.settings.krool_key_count
        settings["Starting Moves Count"] = self.settings.starting_moves_count
        settings["Fast Start"] = self.settings.fast_start_beginning_of_game
        settings["Helm Setting"] = self.settings.helm_setting.name
        settings["Quality of Life"] = self.settings.quality_of_life
        settings["Tag Anywhere"] = self.settings.enable_tag_anywhere
        settings["Kongless Hint Doors"] = self.settings.wrinkly_available
        settings["Fast GBs"] = self.settings.fast_gbs
        settings["High Requirements"] = self.settings.high_req
        settings["Win Condition"] = self.settings.win_condition.name
        if self.settings.helm_hurry:
            settings["Game Mode"] = "Helm Hurry"
        humanspoiler["Settings"] = settings
        humanspoiler["Cosmetics"] = {}
        humanspoiler["Requirements"] = {}
        if self.settings.random_starting_region:
            humanspoiler["Game Start"] = {}
            humanspoiler["Game Start"]["Starting Kong List"] = startKongList
            humanspoiler["Game Start"]["Starting Region"] = self.settings.starting_region["region_name"]
            humanspoiler["Game Start"]["Starting Exit"] = self.settings.starting_region["exit_name"]
        # GB Counts
        gb_counts = {}
        level_list = ["Jungle Japes", "Angry Aztec", "Frantic Factory", "Gloomy Galleon", "Fungi Forest", "Crystal Caves", "Creepy Castle", "Hideout Helm"]
        for level_index, amount in enumerate(self.settings.EntryGBs):
            gb_counts[level_list[level_index]] = amount
        humanspoiler["Requirements"]["B Locker GBs"] = gb_counts
        # CB Counts
        cb_counts = {}
        for level_index, amount in enumerate(self.settings.BossBananas):
            cb_counts[level_list[level_index]] = amount
        humanspoiler["Requirements"]["Troff N Scoff Bananas"] = cb_counts
        humanspoiler["Requirements"]["Miscellaneous"] = {}
        humanspoiler["Kongs"] = {}
        humanspoiler["Kongs"]["Starting Kong List"] = startKongList
        humanspoiler["Kongs"]["Japes Kong Puzzle Solver"] = ItemList[ItemFromKong(self.settings.diddy_freeing_kong)].name
        humanspoiler["Kongs"]["Tiny Temple Puzzle Solver"] = ItemList[ItemFromKong(self.settings.tiny_freeing_kong)].name
        humanspoiler["Kongs"]["Llama Temple Puzzle Solver"] = ItemList[ItemFromKong(self.settings.lanky_freeing_kong)].name
        humanspoiler["Kongs"]["Factory Kong Puzzle Solver"] = ItemList[ItemFromKong(self.settings.chunky_freeing_kong)].name
        humanspoiler["Requirements"]["Miscellaneous"]["Jetpac Medal Requirement"] = self.settings.medal_requirement
        humanspoiler["End Game"] = {}
        humanspoiler["End Game"]["Keys Required for K Rool"] = self.GetKroolKeysRequired(self.settings.krool_keys_required)
        krool_order = []
        for phase in self.settings.krool_order:
            krool_order.append(ItemList[ItemFromKong(phase)].name.capitalize())
        humanspoiler["End Game"]["K Rool Phases"] = krool_order

        helm_default_order = [Kongs.donkey, Kongs.chunky, Kongs.tiny, Kongs.lanky, Kongs.diddy]
        helm_new_order = []
        for room in self.settings.helm_order:
            helm_new_order.append(helm_default_order[room].name.capitalize())
        humanspoiler["End Game"]["Helm Rooms"] = helm_new_order
        if self.settings.crown_door_item != HelmDoorItem.opened:
            humanspoiler["End Game"]["Crown Door Item"] = self.settings.crown_door_item.name
            humanspoiler["End Game"]["Crown Door Item Amount"] = self.settings.crown_door_item_count
        if self.settings.coin_door_item != HelmDoorItem.opened:
            humanspoiler["End Game"]["Coin Door Item"] = self.settings.coin_door_item.name
            humanspoiler["End Game"]["Coin Door Item Amount"] = self.settings.coin_door_item_count
        if self.settings.shuffle_items:
            humanspoiler["Item Pool"] = list(set([enum.name for enum in self.settings.shuffled_location_types]))
        humanspoiler["Items"] = {
            "Kongs": {},
            "Shops": {},
            "DK Isles": {},
            "Jungle Japes": {},
            "Angry Aztec": {},
            "Frantic Factory": {},
            "Gloomy Galleon": {},
            "Fungi Forest": {},
            "Crystal Caves": {},
            "Creepy Castle": {},
            "Hideout Helm": {},
            "Special": {},
        }
        sorted_item_name = "Items (Sorted by Item)"
        humanspoiler[sorted_item_name] = {
            "Kongs": {},
            "Moves": {},
            "Golden Bananas": {},
            "Blueprints": {},
            "Fairies": {},
            "Keys": {},
            "Crowns": {},
            "Coins": {},
            "Medals": {},
            "Miscellaneous Items": {},
            "Rainbow Coins": {},
            "Ice Traps": {},
            "Junk Items": {},
            "Empty": {},
            "Unknown": {},
        }

        # Playthrough data
        humanspoiler["Playthrough"] = self.playthrough

        # Woth data
        humanspoiler["Way of the Hoard"] = self.woth
        # Paths for Woth items - does not show up on the site, just for debugging
        humanspoiler["Paths"] = {}
        wothSlams = 0
        for loc, path in self.woth_paths.items():
            destination_item = ItemList[LocationList[loc].item]
            path_dict = {}
            for path_loc_id in path:
                path_location = LocationList[path_loc_id]
                path_item = ItemList[path_location.item]
                path_dict[path_location.name] = path_item.name
            extra = ""
            if LocationList[loc].item == Items.ProgressiveSlam:
                wothSlams += 1
                extra = " " + str(wothSlams)
            humanspoiler["Paths"][destination_item.name + extra] = path_dict
        # Paths for K. Rool phases - also do not show up on the site, just for debugging
        for kong, path in self.krool_paths.items():
            path_dict = {}
            for path_loc_id in path:
                path_location = LocationList[path_loc_id]
                path_item = ItemList[path_location.item]
                path_dict[path_location.name] = path_item.name
            phase_name = "K. Rool Donkey Phase"
            if kong == Kongs.diddy:
                phase_name = "K. Rool Diddy Phase"
            elif kong == Kongs.lanky:
                phase_name = "K. Rool Lanky Phase"
            elif kong == Kongs.tiny:
                phase_name = "K. Rool Tiny Phase"
            elif kong == Kongs.chunky:
                phase_name = "K. Rool Chunky Phase"
            humanspoiler["Paths"][phase_name] = path_dict

        self.pregiven_items = []
        for location_id, location in LocationList.items():
            # No need to spoiler constants or hints
            if location.type == Types.Constant or location.type == Types.Hint or location.inaccessible:
                continue
            if location_id in PreGivenLocations:
                self.pregiven_items.append(location.item)
            # Prevent weird null issues but get the item at the location
            if location.item is None:
                item = Items.NoItem
            else:
                item = ItemList[location.item]
            # Empty PreGiven locations don't really exist and shouldn't show up in the spoiler log
            if location.type == Types.PreGivenMove and location.item in (None, Items.NoItem):
                continue
            # Separate Kong locations
            if location.type == Types.Kong:
                humanspoiler["Items"]["Kongs"][location.name] = item.name
                humanspoiler[sorted_item_name][self.getItemGroup(location.item)][location.name] = item.name
            # Separate Shop locations
            elif location.type == Types.Shop:
                # Ignore shop locations with no items
                if location.item is None or location.item == Items.NoItem:
                    continue
                # Gotta dig up the price - progressive moves look a little weird in the spoiler
                price = ""
                if location.item in ProgressiveMoves.keys():
                    if location.item == Items.ProgressiveSlam:
                        price = f"{self.settings.prices[Items.ProgressiveSlam][0]}->{self.settings.prices[Items.ProgressiveSlam][1]}"
                    elif location.item == Items.ProgressiveAmmoBelt:
                        price = f"{self.settings.prices[Items.ProgressiveAmmoBelt][0]}->{self.settings.prices[Items.ProgressiveAmmoBelt][1]}"
                    elif location.item == Items.ProgressiveInstrumentUpgrade:
                        price = f"{self.settings.prices[Items.ProgressiveInstrumentUpgrade][0]}->{self.settings.prices[Items.ProgressiveInstrumentUpgrade][1]}->{self.settings.prices[Items.ProgressiveInstrumentUpgrade][2]}"
                # Vanilla prices are by item, not by location
                elif self.settings.random_prices == RandomPrices.vanilla:
                    price = str(self.settings.prices[location.item])
                else:
                    price = str(self.settings.prices[location_id])
                humanspoiler["Items"]["Shops"][location.name] = item.name + f" ({price})"
                humanspoiler[sorted_item_name][self.getItemGroup(location.item)][location.name] = item.name
            # Filter everything else by level - each location conveniently contains a level-identifying bit in their name
            else:
                level = "Special"
                if "Isles" in location.name or location.type == Types.PreGivenMove:
                    level = "DK Isles"
                elif "Japes" in location.name:
                    level = "Jungle Japes"
                elif "Aztec" in location.name:
                    level = "Angry Aztec"
                elif "Factory" in location.name:
                    level = "Frantic Factory"
                elif "Galleon" in location.name:
                    level = "Gloomy Galleon"
                elif "Forest" in location.name:
                    level = "Fungi Forest"
                elif "Caves" in location.name:
                    level = "Crystal Caves"
                elif "Castle" in location.name:
                    level = "Creepy Castle"
                elif "Helm" in location.name:
                    level = "Hideout Helm"
                humanspoiler["Items"][level][location.name] = item.name
                humanspoiler[sorted_item_name][self.getItemGroup(location.item)][location.name] = item.name

        if self.settings.shuffle_loading_zones == ShuffleLoadingZones.levels:
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
        elif self.settings.shuffle_loading_zones != ShuffleLoadingZones.none:
            # Show full shuffled_exits data if more than just levels are shuffled
            shuffled_exits = OrderedDict()
            level_starts = {
                "DK Isles": [
                    "DK Isles",
                    "Japes Lobby",
                    "Aztec Lobby",
                    "Factory Lobby",
                    "Galleon Lobby",
                    "Fungi Lobby",
                    "Caves Lobby",
                    "Castle Lobby",
                    "Snide's Room",
                    "Training Grounds",
                    "Banana Fairy Isle",
                    "DK's Treehouse",
                ],
                "Jungle Japes": ["Jungle Japes"],
                "Angry Aztec": ["Angry Aztec"],
                "Frantic Factory": ["Frantic Factory"],
                "Gloomy Galleon": ["Gloomy Galleon"],
                "Fungi Forest": ["Fungi Forest"],
                "Crystal Caves": ["Crystal Caves"],
                "Creepy Castle": ["Creepy Castle"],
            }
            level_data = {"Other": {}}
            for level in level_starts:
                level_data[level] = {}
            for exit, dest in self.shuffled_exit_data.items():
                level_name = "Other"
                for level in level_starts:
                    for search_name in level_starts[level]:
                        if dest.spoilerName.find(search_name) == 0:
                            level_name = level
                shuffled_exits[ShufflableExits[exit].name] = dest.spoilerName
                level_data[level_name][ShufflableExits[exit].name] = dest.spoilerName
            humanspoiler["Shuffled Exits"] = shuffled_exits
            humanspoiler["Shuffled Exits (Sorted by destination)"] = level_data
        if self.settings.alter_switch_allocation:
            humanspoiler["Level Switch Strength"] = {
                "Jungle Japes": self.settings.switch_allocation[Levels.JungleJapes],
                "Angry Aztec": self.settings.switch_allocation[Levels.AngryAztec],
                "Frantic Factory": self.settings.switch_allocation[Levels.FranticFactory],
                "Gloomy Galleon": self.settings.switch_allocation[Levels.GloomyGalleon],
                "Fungi Forest": self.settings.switch_allocation[Levels.FungiForest],
                "Crystal Caves": self.settings.switch_allocation[Levels.CrystalCaves],
                "Creepy Castle": self.settings.switch_allocation[Levels.CreepyCastle],
            }
        humanspoiler["Bosses"] = {}
        if self.settings.boss_location_rando:
            shuffled_bosses = OrderedDict()
            boss_names = {
                "JapesBoss": "Army Dillo 1",
                "AztecBoss": "Dogadon 1",
                "FactoryBoss": "Mad Jack",
                "GalleonBoss": "Pufftoss",
                "FungiBoss": "Dogadon 2",
                "CavesBoss": "Army Dillo 2",
                "CastleBoss": "King Kut Out",
            }
            for i in range(7):
                shuffled_bosses["".join(map(lambda x: x if x.islower() else " " + x, Levels(i).name)).strip()] = boss_names[Maps(self.settings.boss_maps[i]).name]
            humanspoiler["Bosses"]["Shuffled Boss Order"] = shuffled_bosses

        humanspoiler["Bosses"]["King Kut Out Properties"] = {}
        if self.settings.boss_kong_rando:
            shuffled_boss_kongs = OrderedDict()
            for i in range(7):
                shuffled_boss_kongs["".join(map(lambda x: x if x.islower() else " " + x, Levels(i).name)).strip()] = Kongs(self.settings.boss_kongs[i]).name.capitalize()
            humanspoiler["Bosses"]["Shuffled Boss Kongs"] = shuffled_boss_kongs
            kutout_order = ""
            for kong in self.settings.kutout_kongs:
                kutout_order = kutout_order + Kongs(kong).name.capitalize() + ", "
            humanspoiler["Bosses"]["King Kut Out Properties"]["Shuffled Kutout Kong Order"] = kutout_order

        if self.settings.hard_bosses:
            phase_names = []
            for phase in self.settings.kko_phase_order:
                phase_names.append(f"Phase {phase+1}")
            humanspoiler["Bosses"]["King Kut Out Properties"]["Shuffled Kutout Phases"] = ", ".join(phase_names)

        if self.settings.bonus_barrels == MinigameBarrels.selected and len(self.settings.minigames_list_selected) > 0:
            selected_minigames = []
            for minigame in self.settings.minigames_list_selected:
                selected_minigames.append(minigame.name)
            humanspoiler["Selected Minigames"] = selected_minigames
        if self.settings.bonus_barrels in (MinigameBarrels.random, MinigameBarrels.selected) or self.settings.helm_barrels == MinigameBarrels.random:
            shuffled_barrels = OrderedDict()
            for location, minigame in self.shuffled_barrel_data.items():
                if location in HelmMinigameLocations and self.settings.helm_barrels == MinigameBarrels.skip:
                    continue
                if location not in HelmMinigameLocations and self.settings.bonus_barrels == MinigameBarrels.skip:
                    continue
                shuffled_barrels[LocationList[location].name] = MinigameRequirements[minigame].name
            if len(shuffled_barrels) > 0:
                humanspoiler["Shuffled Bonus Barrels"] = shuffled_barrels

        if self.settings.kasplat_rando:
            humanspoiler["Shuffled Kasplats"] = self.human_kasplats
        if self.settings.random_fairies:
            humanspoiler["Shuffled Banana Fairies"] = self.fairy_locations_human
        if self.settings.random_patches:
            humanspoiler["Shuffled Dirt Patches"] = self.human_patches
        if self.settings.bananaport_rando != BananaportRando.off:
            shuffled_warp_levels = [x.name for x in self.settings.warp_level_list_selected]
            humanspoiler["Shuffled Bananaport Levels"] = shuffled_warp_levels
            humanspoiler["Shuffled Bananaports"] = self.human_warp_locations
        if len(self.microhints) > 0:
            human_microhints = {}
            for name, hint in self.microhints.items():
                filtered_hint = hint.replace("\x04", "")
                filtered_hint = filtered_hint.replace("\x05", "")
                filtered_hint = filtered_hint.replace("\x06", "")
                filtered_hint = filtered_hint.replace("\x07", "")
                filtered_hint = filtered_hint.replace("\x08", "")
                filtered_hint = filtered_hint.replace("\x09", "")
                filtered_hint = filtered_hint.replace("\x0a", "")
                filtered_hint = filtered_hint.replace("\x0b", "")
                filtered_hint = filtered_hint.replace("\x0c", "")
                filtered_hint = filtered_hint.replace("\x0d", "")
                human_microhints[name] = filtered_hint
            humanspoiler["Direct Item Hints"] = human_microhints
        if len(self.hint_list) > 0:
            human_hint_list = {}
            # Here it filters out the coloring from the hints to make it actually readable in the spoiler log
            for name, hint in self.hint_list.items():
                filtered_hint = hint.replace("\x04", "")
                filtered_hint = filtered_hint.replace("\x05", "")
                filtered_hint = filtered_hint.replace("\x06", "")
                filtered_hint = filtered_hint.replace("\x07", "")
                filtered_hint = filtered_hint.replace("\x08", "")
                filtered_hint = filtered_hint.replace("\x09", "")
                filtered_hint = filtered_hint.replace("\x0a", "")
                filtered_hint = filtered_hint.replace("\x0b", "")
                filtered_hint = filtered_hint.replace("\x0c", "")
                filtered_hint = filtered_hint.replace("\x0d", "")
                human_hint_list[name] = filtered_hint
            humanspoiler["Wrinkly Hints"] = human_hint_list
        if self.settings.wrinkly_location_rando:
            humanspoiler["Wrinkly Door Locations"] = self.human_hint_doors
        if self.settings.tns_location_rando:
            humanspoiler["T&S Portal Locations"] = self.human_portal_doors
        if self.settings.crown_placement_rando:
            humanspoiler["Battle Arena Locations"] = self.human_crowns
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
        if self.settings.shuffle_shops:
            shop_location_dict = {}
            for level in self.shuffled_shop_locations:
                level_name = "Unknown Level"

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
        for spoiler_dict in ("Items", "Bosses"):
            is_empty = True
            for y in humanspoiler[spoiler_dict]:
                if humanspoiler[spoiler_dict][y] != {}:
                    is_empty = False
            if is_empty:
                del humanspoiler[spoiler_dict]

        if self.settings.cb_rando:
            human_cb_type_map = {"cb": " Bananas", "balloons": " Balloons"}
            humanspoiler["Colored Banana Locations"] = {}
            cb_levels = ["Japes", "Aztec", "Factory", "Galleon", "Fungi", "Caves", "Castle"]
            cb_kongs = ["Donkey", "Diddy", "Lanky", "Tiny", "Chunky"]
            for lvl in cb_levels:
                for kng in cb_kongs:
                    humanspoiler["Colored Banana Locations"][f"{lvl} {kng}"] = {"Balloons": [], "Bananas": []}
            for group in self.cb_placements:
                lvl_name = level_dict[group["level"]]
                idx = 1
                if group["level"] == Levels.FungiForest:
                    idx = 0
                map_name = "".join(map(lambda x: x if x.islower() else " " + x, Maps(group["map"]).name)).strip()
                join_combos = ["2 D Ship", "5 D Ship", "5 D Temple"]
                for combo in join_combos:
                    if combo in map_name:
                        map_name = map_name.replace(combo, combo.replace(" ", ""))
                humanspoiler["Colored Banana Locations"][f"{lvl_name.split(' ')[idx]} {NameFromKong(group['kong'])}"][human_cb_type_map[group["type"]].strip()].append(
                    f"{map_name.strip()}: {group['name']}"
                )
        if self.settings.coin_rando:
            humanspoiler["Coin Locations"] = {}
            coin_levels = ["Japes", "Aztec", "Factory", "Galleon", "Fungi", "Caves", "Castle", "Isles"]
            coin_kongs = ["Donkey", "Diddy", "Lanky", "Tiny", "Chunky"]
            for lvl in coin_levels:
                for kng in coin_kongs:
                    humanspoiler["Coin Locations"][f"{lvl} {kng}"] = []
            for group in self.coin_placements:
                lvl_name = level_dict[group["level"]]
                idx = 1
                if group["level"] == Levels.FungiForest:
                    idx = 0
                map_name = "".join(map(lambda x: x if x.islower() else " " + x, Maps(group["map"]).name)).strip()
                join_combos = ["2 D Ship", "5 D Ship", "5 D Temple"]
                for combo in join_combos:
                    if combo in map_name:
                        map_name = map_name.replace(combo, combo.replace(" ", ""))
                humanspoiler["Coin Locations"][f"{lvl_name.split(' ')[idx]} {NameFromKong(group['kong'])}"].append(f"{map_name.strip()}: {group['name']}")

        self.json = json.dumps(humanspoiler, indent=4)

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
                    print("Exit Update Error with:")
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
            # (There must be an item here) AND (It must not be a constant item expected to be here) AND (It must be in a location not handled by the full item rando shuffler)
            if location.item is not None and location.item is not Items.NoItem and not location.constant and location.type not in self.settings.shuffled_location_types:
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
                    updated_item = ItemList[location.item]
                    move_type = updated_item.movetype
                    # Determine Price
                    price = 0
                    if id in self.settings.prices:
                        price = self.settings.prices[id]
                    # Vanilla prices are by item, not by location
                    if self.settings.random_prices == RandomPrices.vanilla:
                        price = self.settings.prices[location.item]
                    # Moves that are set with a single flag (e.g. training barrels, shockwave) are handled differently
                    if move_type == MoveTypes.Flag:
                        for kong_index in kong_indices:
                            self.move_data[0][shop_index][kong_index][level_index] = {"move_type": "flag", "flag": updated_item.flag, "price": price}
                    # This is for every other move typically purchased in a shop
                    else:
                        move_level = updated_item.index - 1
                        move_kong = updated_item.kong
                        for kong_index in kong_indices:
                            # print(f"Shop {shop_index}, Kong {kong_index}, Level {level_index} | Move: {move_type} lvl {move_level} for kong {move_kong}")
                            if (
                                move_type == MoveTypes.Slam
                                or move_type == MoveTypes.AmmoBelt
                                or (move_type == MoveTypes.Guns and move_level > 0)
                                or (move_type == MoveTypes.Instruments and move_level > 0)
                            ):
                                move_kong = kong_index
                            self.move_data[0][shop_index][kong_index][level_index] = {
                                "move_type": ["special", "slam", "gun", "ammo_belt", "instrument"][move_type],
                                "move_lvl": move_level,
                                "move_kong": move_kong,
                                "price": price,
                            }
                elif location.type == Types.Kong:
                    self.WriteKongPlacement(id, location.item)
                elif location.type == Types.TrainingBarrel and self.settings.training_barrels != TrainingBarrels.normal:
                    # Use the item to find the data to write
                    updated_item = ItemList[location.item]
                    move_type = updated_item.movetype
                    # Determine Price to be zero because this is a training barrel
                    price = 0
                    # Moves that are set with a single flag (e.g. training barrels, shockwave) are handled differently
                    if move_type == MoveTypes.Flag:
                        self.move_data[1].append({"move_type": "flag", "flag": updated_item.flag, "price": price})
                    # This is for every other move typically purchased in a shop
                    else:
                        move_level = updated_item.index - 1
                        move_kong = updated_item.kong
                        self.move_data[1].append(
                            {
                                "move_type": ["special", "slam", "gun", "ammo_belt", "instrument"][move_type],
                                "move_lvl": move_level,
                                "move_kong": move_kong % 5,  # Shared moves are 5 but should be 0
                                "price": price,
                            }
                        )
                elif location.type == Types.Shockwave and self.settings.shockwave_status != ShockwaveStatus.vanilla:
                    # Use the item to find the data to write
                    updated_item = ItemList[location.item]
                    move_type = updated_item.movetype
                    # Determine Price to be zero because BFI is free
                    price = 0
                    # Moves that are set with a single flag (e.g. training barrels, shockwave) are handled differently
                    if move_type == MoveTypes.Flag:
                        self.move_data[2] = [{"move_type": "flag", "flag": updated_item.flag, "price": price}]
                    # This is for every other move typically purchased in a shop
                    else:
                        move_level = updated_item.index - 1
                        move_kong = updated_item.kong
                        self.move_data[2] = [
                            {
                                "move_type": ["special", "slam", "gun", "ammo_belt", "instrument"][move_type],
                                "move_lvl": move_level,
                                "move_kong": move_kong % 5,  # Shared moves are 5 but should be 0
                                "price": price,
                            }
                        ]
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
            sphereLocations.sort(key=self.ScoreLocations)
            for location in sphereLocations:
                newSphere[location.name] = ItemList[location.item].name
            self.playthrough[i] = newSphere
            i += 1

    def UpdateWoth(self, locations, wothLocations):
        """Write woth locations as a dict of location/item pairs."""
        self.woth = {}
        self.woth_locations = wothLocations
        for locationId in wothLocations:
            location = locations[locationId]
            self.woth[location.name] = ItemList[location.item].name

    def ScoreLocations(self, location):
        """Score a location with the given settings for sorting the Playthrough."""
        # The Banana Hoard is likely in its own sphere but if it's not put it last
        if location == Locations.BananaHoard:
            return 250
        # GBs go last, there's a lot of them but they arent important
        if ItemList[location.item].type == Types.Banana:
            return 100
        # Win condition items are more important than GBs but less than moves
        elif self.settings.win_condition == WinCondition.all_fairies and ItemList[location.item].type == Types.Fairy:
            return 10
        elif self.settings.win_condition == WinCondition.all_blueprints and ItemList[location.item].type == Types.Blueprint:
            return 10
        elif self.settings.win_condition == WinCondition.all_medals and ItemList[location.item].type == Types.Medal:
            return 10
        # Kongs are most the single most important thing and should be at the top of spheres
        elif ItemList[location.item].type == Types.Kong:
            return 0
        # Keys are best put first
        elif ItemList[location.item].type == Types.Key:
            return 1
        # Moves are pretty important
        elif ItemList[location.item].type == Types.Shop:
            return 2
        # Everything else here is probably something unusual so it's likely important
        else:
            return 3

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
