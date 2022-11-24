"""Settings class and functions."""
import hashlib
import inspect
import json
import random
from version import whl_hash
from random import randint

from randomizer.Enums.Events import Events
from randomizer.Enums.Items import Items
from randomizer.Enums.Kongs import GetKongs, Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Regions import Regions
from randomizer.Enums.Types import Types
import randomizer.ItemPool as ItemPool
from randomizer.Lists.Item import ItemList
from randomizer.Lists.Location import ChunkyMoveLocations, DiddyMoveLocations, DonkeyMoveLocations, LankyMoveLocations, LocationList, SharedShopLocations, TinyMoveLocations, TrainingBarrelLocations
from randomizer.Lists.ShufflableExit import ShufflableExits
from randomizer.Lists.MapsAndExits import GetMapId, GetExitId, RegionMapList
from randomizer.Prices import CompleteVanillaPrices, RandomizePrices, VanillaPrices
from randomizer.ShuffleBosses import ShuffleBosses, ShuffleBossKongs, ShuffleKKOPhaseOrder, ShuffleKutoutKongs
import randomizer.LogicFiles.DKIsles
import randomizer.LogicFiles.JungleJapes
import randomizer.LogicFiles.AngryAztec
import randomizer.LogicFiles.FranticFactory
import randomizer.LogicFiles.GloomyGalleon
import randomizer.LogicFiles.FungiForest
import randomizer.LogicFiles.CrystalCaves
import randomizer.LogicFiles.CreepyCastle


class Settings:
    """Class used to store settings for seed generation."""

    def __init__(self, form_data: dict):
        """Init all the settings using the form data to set the flags.

        Args:
            form_data (dict): Post data from the html form.
        """
        self.__hash = self.__get_hash()
        self.public_hash = self.__get_hash()
        self.algorithm = "forward"
        self.generate_main()
        self.generate_progression()
        self.generate_misc()
        self.rom_data = 0x1FED020
        self.move_location_data = 0x1FEF000

        for k, v in form_data.items():
            setattr(self, k, v)
        self.seed_id = str(self.seed)
        self.seed = str(self.seed) + self.__hash
        self.set_seed()
        self.seed_hash = [random.randint(0, 9) for i in range(5)]
        self.krool_keys_required = []
        # Settings which are not yet implemented on the web page

        # B Locker and T&S max values
        # Shorter: 20 GB
        # Short: 35 GB
        # Medium: 50 GB
        # Long: 65 GB
        # Longer: 80 GB\
        self.blocker_max = int(self.blocker_text) if self.blocker_text else 50
        self.troff_max = int(self.troff_text) if self.troff_text else 270
        self.troff_min = [0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55]  # Weights for the minimum value of troff
        if self.hard_troff_n_scoff:
            self.troff_min = [0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75]  # Add 20% to the minimum for hard T&S
        # In hard level progression we go through levels in a random order, so we set every level's troff min weight to the largest weight
        if self.hard_level_progression:
            self.troff_min = [self.troff_min[-1] for x in self.troff_min]

        # set to true if move_rando set to start_with
        self.unlock_all_moves = False

        # Pointless with just move rando, maybe have it once full rando
        # progressive_upgrades: bool
        self.progressive_upgrades = False

        CompleteVanillaPrices()
        self.prices = VanillaPrices.copy()
        self.level_order = {1: Levels.JungleJapes, 2: Levels.AngryAztec, 3: Levels.FranticFactory, 4: Levels.GloomyGalleon, 5: Levels.FungiForest, 6: Levels.CrystalCaves, 7: Levels.CreepyCastle}

        # Used by hints in level order rando
        # By default (and in LZR) assume you have access to everything everywhere so hints are unrestricted
        self.owned_kongs_by_level = {
            Levels.JungleJapes: GetKongs().copy(),
            Levels.AngryAztec: GetKongs().copy(),
            Levels.FranticFactory: GetKongs().copy(),
            Levels.GloomyGalleon: GetKongs().copy(),
            Levels.FungiForest: GetKongs().copy(),
            Levels.CrystalCaves: GetKongs().copy(),
            Levels.CreepyCastle: GetKongs().copy(),
        }
        self.owned_moves_by_level = {
            Levels.JungleJapes: ItemPool.AllKongMoves().copy(),
            Levels.AngryAztec: ItemPool.AllKongMoves().copy(),
            Levels.FranticFactory: ItemPool.AllKongMoves().copy(),
            Levels.GloomyGalleon: ItemPool.AllKongMoves().copy(),
            Levels.FungiForest: ItemPool.AllKongMoves().copy(),
            Levels.CrystalCaves: ItemPool.AllKongMoves().copy(),
            Levels.CreepyCastle: ItemPool.AllKongMoves().copy(),
        }

        self.resolve_settings()
        self.update_valid_locations()

    def update_progression_totals(self):
        """Update the troff and blocker totals if we're randomly setting them."""
        # Assign weights to Troff n Scoff based on level order if not shuffling loading zones
        # Hard level shuffling makes these weights meaningless, as you'll be going into levels in a random order
        self.troff_weight_0 = 0.5
        self.troff_weight_1 = 0.55
        self.troff_weight_2 = 0.6
        self.troff_weight_3 = 0.7
        self.troff_weight_4 = 0.8
        self.troff_weight_5 = 0.9
        self.troff_weight_6 = 1.0
        if self.level_randomization in ("loadingzone", "loadingzonesdecoupled") or self.hard_level_progression:
            self.troff_weight_0 = 1
            self.troff_weight_1 = 1
            self.troff_weight_2 = 1
            self.troff_weight_3 = 1
            self.troff_weight_4 = 1
            self.troff_weight_5 = 1
            self.troff_weight_6 = 1

        if self.randomize_cb_required_amounts:
            randomlist = []
            for min_percentage in self.troff_min:
                randomlist.append(random.randint(round(self.troff_max * min_percentage), self.troff_max))
            cbs = randomlist
            self.troff_0 = round(min(cbs[0] * self.troff_weight_0, 500))
            self.troff_1 = round(min(cbs[1] * self.troff_weight_1, 500))
            self.troff_2 = round(min(cbs[2] * self.troff_weight_2, 500))
            self.troff_3 = round(min(cbs[3] * self.troff_weight_3, 500))
            self.troff_4 = round(min(cbs[4] * self.troff_weight_4, 500))
            self.troff_5 = round(min(cbs[5] * self.troff_weight_5, 500))
            self.troff_6 = round(min(cbs[6] * self.troff_weight_6, 500))
        if self.randomize_blocker_required_amounts:
            randomlist = random.sample(range(1, self.blocker_max), 7)
            b_lockers = randomlist
            if self.shuffle_loading_zones == "all" or self.hard_level_progression:
                b_lockers.append(random.randint(1, self.blocker_max))
                random.shuffle(b_lockers)
            else:
                b_lockers.append(1)
                b_lockers.sort()
            self.blocker_0 = b_lockers[0]
            self.blocker_1 = b_lockers[1]
            self.blocker_2 = b_lockers[2]
            self.blocker_3 = b_lockers[3]
            self.blocker_4 = b_lockers[4]
            self.blocker_5 = b_lockers[5]
            self.blocker_6 = b_lockers[6]
            if self.maximize_helm_blocker:
                self.blocker_7 = self.blocker_max
            else:
                self.blocker_7 = b_lockers[7]

        # Store banana values in array
        self.EntryGBs = [self.blocker_0, self.blocker_1, self.blocker_2, self.blocker_3, self.blocker_4, self.blocker_5, self.blocker_6, self.blocker_7]
        self.BossBananas = [self.troff_0, self.troff_1, self.troff_2, self.troff_3, self.troff_4, self.troff_5, self.troff_6]

    def generate_main(self):
        """Set Default items on main page."""
        self.seed = None
        self.download_patch_file = None
        self.bonus_barrel_rando = None
        self.loading_zone_coupled = None
        self.move_rando = "off"
        self.random_patches = None
        self.random_prices = None
        self.boss_location_rando = None
        self.boss_kong_rando = None
        self.kasplat_rando_setting = None
        self.puzzle_rando = None
        self.shuffle_shops = None

        # The major setting for item randomization
        self.shuffle_items = True

        # In item rando, can any Kong collect any item?
        # free_trade_setting: str
        # none
        # not_blueprints - this excludes blueprints and lesser collectibles like cbs and coins
        # major_collectibles - includes blueprints, does not include lesser collectibles like cbs and coins
        self.free_trade_setting = "none"

    def set_seed(self):
        """Forcibly re-set the random seed to the seed set in the config."""
        random.seed(self.seed)

    def generate_progression(self):
        """Set default items on progression page."""
        self.blocker_0 = None
        self.blocker_1 = None
        self.blocker_2 = None
        self.blocker_3 = None
        self.blocker_4 = None
        self.blocker_5 = None
        self.blocker_6 = None
        self.blocker_7 = None
        self.troff_0 = None
        self.troff_1 = None
        self.troff_2 = None
        self.troff_3 = None
        self.troff_4 = None
        self.troff_5 = None
        self.troff_6 = None
        self.troff_min = None
        self.troff_max = None
        self.blocker_text = None
        self.troff_text = None

    def generate_misc(self):
        """Set default items on misc page."""
        #  Settings which affect logic
        # crown_door_open: bool
        self.crown_door_open = None
        # coin_door_open: bool
        self.coin_door_open = None
        # krool_phase_count: int, [1-5]
        self.krool_phase_count = 5
        self.krool_random = False
        # helm_phase_count: int, [1-5]
        self.helm_phase_count = 3
        self.helm_random = False
        # krool_key_count: int, [0-8]
        self.krool_key_count = 8
        self.keys_random = False
        # starting_kongs_count: int, [1-5]
        self.starting_kongs_count = 5
        self.starting_random = False

        # bonus_barrels: str
        # skip (auto-completed)
        # normal
        # random
        self.bonus_barrels = "normal"
        # helm_barrels: str
        # skip (helm skip all)
        # normal
        # random
        self.helm_barrels = "normal"
        self.bonus_barrel_auto_complete = False

        # hard_shooting: bool
        self.hard_shooting = False

        # hard_bosses: bool
        self.hard_bosses = False

        # damage multiplier
        self.damage_amount = "default"

        # no_logic: bool
        self.no_logic = False

        # shuffle_loading_zones: str
        # none
        # levels
        # all
        self.shuffle_loading_zones = "none"

        # decoupled_loading_zones: bool
        self.decoupled_loading_zones = False

        # Always start with training barrels currently
        # training_barrels: str
        # normal
        # shuffled
        self.training_barrels = "normal"

        # The status of camera & shockwave: str
        # vanilla - both located at Banana Fairy Isle
        # shuffled - located in a random valid location
        # shuffled_decoupled - camera and shockwave are separate upgrades and can be anywhere
        # start_with - start with camera and shockwave
        self.shockwave_status = "vanilla"

        #  Music
        self.music_bgm = "default"
        self.music_fanfares = "default"
        self.music_events = "default"
        self.random_music = False

        #  Color
        self.colors = {}
        self.color_palettes = {}
        self.klaptrap_model = "green"
        self.klaptrap_model_index = 0x21
        self.dk_colors = "vanilla"
        self.dk_custom_color = "#000000"
        self.diddy_colors = "vanilla"
        self.diddy_custom_color = "#000000"
        self.lanky_colors = "vanilla"
        self.lanky_custom_color = "#000000"
        self.tiny_colors = "vanilla"
        self.tiny_custom_color = "#000000"
        self.chunky_colors = "vanilla"
        self.chunky_custom_color = "#000000"
        self.rambi_colors = "vanilla"
        self.rambi_custom_color = "#000000"
        self.enguarde_colors = "vanilla"
        self.enguarde_custom_color = "#000000"
        self.disco_chunky = False
        self.krusha_slot = "no_slot"
        self.misc_cosmetics = False
        self.remove_water_oscillation = False

        #  Misc
        self.generate_spoilerlog = None
        self.fast_start_beginning_of_game = None
        self.helm_setting = None
        self.quality_of_life = None
        self.shorten_boss = False
        self.enable_tag_anywhere = None
        self.krool_phase_order_rando = None
        self.krool_access = False
        self.helm_phase_order_rando = None
        self.open_lobbies = None
        self.open_levels = None
        self.randomize_pickups = False
        self.random_medal_requirement = False
        self.medal_requirement = 15
        self.medal_cb_req = 75
        self.rareware_gb_fairies = 20
        self.bananaport_rando = "off"
        self.activate_all_bananaports = "off"
        self.shop_indicator = False
        self.randomize_cb_required_amounts = False
        self.randomize_blocker_required_amounts = False
        self.maximize_helm_blocker = False
        self.perma_death = False
        self.disable_tag_barrels = False
        self.level_randomization = "none"
        self.kong_rando = False
        self.kongs_for_progression = False
        self.wrinkly_hints = "off"
        self.fast_warps = False
        self.dpad_display = False
        self.high_req = False
        self.fast_gbs = False
        self.auto_keys = False
        self.kko_phase_order = [0, 0, 0]
        self.enemy_rando = False
        self.crown_enemy_rando = "off"
        self.enemy_speed_rando = False
        self.cb_rando = False
        self.crown_placement_rando = False
        self.override_cosmetics = False
        self.random_colors = False
        self.hard_level_progression = False
        self.hard_blockers = False
        self.hard_troff_n_scoff = False
        self.hard_enemies = False
        self.wrinkly_location_rando = False
        self.tns_location_rando = False
        self.minigames_list_selected = []
        self.item_rando_list_selected = []
        self.misc_changes_selected = []
        self.enemies_selected = []
        self.starting_keys_list_selected = []
        self.select_keys = False
        self.helm_hurry = False
        self.colorblind_mode = "off"
        self.win_condition = "beat_krool"
        self.key_8_helm = False
        self.random_starting_region = False
        self.starting_region = {}

    def shuffle_prices(self):
        """Price randomization. Reuseable if we need to reshuffle prices."""
        # Price Rando
        if self.random_prices != "vanilla":
            self.prices = RandomizePrices(self.random_prices)

    def resolve_settings(self):
        """Resolve settings which are not directly set through the UI."""
        kongs = GetKongs()

        self.shuffled_location_types = []
        if self.shuffle_items:
            if not self.item_rando_list_selected:
                self.shuffled_location_types = [Types.Shop, Types.Banana, Types.Crown, Types.Blueprint, Types.Key, Types.Medal, Types.Coin]
            else:
                for item in self.item_rando_list_selected:
                    for type in Types:
                        if type.name == item.capitalize():
                            self.shuffled_location_types.append(type)
            if Types.Shop in self.shuffled_location_types:
                if self.move_rando != "start_with":
                    self.move_rando = "item_shuffle"
                if self.shockwave_status not in ("vanilla", "start_with"):
                    self.shuffled_location_types.append(Types.Shockwave)
                if self.training_barrels != "normal":
                    self.shuffled_location_types.append(Types.TrainingBarrel)
            # DEBUG CODE for testing, put it in the list selector when it's completed
            # Uncomment the next line if you want Kongs in the item rando location pool
            # self.shuffled_location_types.append(Types.Kong)
        self.shuffle_prices()

        # B Locker and Troff n Scoff amounts Rando
        self.update_progression_totals()

        # Handle K. Rool Phases
        self.krool_donkey = False
        self.krool_diddy = False
        self.krool_lanky = False
        self.krool_tiny = False
        self.krool_chunky = False

        phases = kongs.copy()
        if self.krool_phase_order_rando:
            random.shuffle(phases)
        if self.krool_random:
            self.krool_phase_count = randint(1, 5)
        if isinstance(self.krool_phase_count, str) is True:
            self.krool_phase_count = 5
        if self.krool_phase_count < 5:
            phases = random.sample(phases, self.krool_phase_count)
        orderedPhases = []
        for kong in phases:
            if kong == Kongs.donkey:
                self.krool_donkey = True
                orderedPhases.append(Kongs.donkey)
            if kong == Kongs.diddy:
                self.krool_diddy = True
                orderedPhases.append(Kongs.diddy)
            if kong == Kongs.lanky:
                self.krool_lanky = True
                orderedPhases.append(Kongs.lanky)
            if kong == Kongs.tiny:
                self.krool_tiny = True
                orderedPhases.append(Kongs.tiny)
            if kong == Kongs.chunky:
                self.krool_chunky = True
                orderedPhases.append(Kongs.chunky)
        self.krool_order = orderedPhases

        # Helm Order
        self.helm_donkey = False
        self.helm_diddy = False
        self.helm_lanky = False
        self.helm_tiny = False
        self.helm_chunky = False

        rooms = [Kongs.donkey, Kongs.chunky, Kongs.tiny, Kongs.lanky, Kongs.diddy]
        if self.helm_phase_order_rando:
            random.shuffle(rooms)
        if self.helm_random:
            self.helm_phase_count = randint(1, 5)
        if isinstance(self.helm_phase_count, str) is True:
            self.helm_phase_count = 5
        if self.helm_phase_count < 5:
            rooms = random.sample(rooms, self.helm_phase_count)
        orderedRooms = []
        for kong in rooms:
            if kong == Kongs.donkey:
                orderedRooms.append(0)
                self.helm_donkey = True
            elif kong == Kongs.diddy:
                self.helm_diddy = True
                orderedRooms.append(4)
            elif kong == Kongs.lanky:
                self.helm_lanky = True
                orderedRooms.append(3)
            elif kong == Kongs.tiny:
                self.helm_tiny = True
                orderedRooms.append(2)
            elif kong == Kongs.chunky:
                self.helm_chunky = True
                orderedRooms.append(1)
        self.helm_order = orderedRooms

        # Start Region
        if self.random_starting_region:
            region_data = [
                randomizer.LogicFiles.DKIsles.LogicRegions,
                randomizer.LogicFiles.JungleJapes.LogicRegions,
                randomizer.LogicFiles.AngryAztec.LogicRegions,
                randomizer.LogicFiles.FranticFactory.LogicRegions,
                randomizer.LogicFiles.GloomyGalleon.LogicRegions,
                randomizer.LogicFiles.FungiForest.LogicRegions,
                randomizer.LogicFiles.CrystalCaves.LogicRegions,
                randomizer.LogicFiles.CreepyCastle.LogicRegions,
            ]
            selected_region_world = random.choice(region_data)
            valid_starting_regions = []
            for region in selected_region_world:
                region_data = selected_region_world[region]
                transitions = [
                    x.exitShuffleId for x in region_data.exits if x.exitShuffleId is not None and x.exitShuffleId in ShufflableExits and ShufflableExits[x.exitShuffleId].back.reverse is not None
                ]
                if region in RegionMapList:
                    # Has tied map
                    tied_map = GetMapId(region)
                    for transition in transitions:
                        relevant_transition = ShufflableExits[transition].back.reverse
                        tied_exit = GetExitId(ShufflableExits[relevant_transition].back)
                        valid_starting_regions.append(
                            {"region": region, "map": tied_map, "exit": tied_exit, "region_name": region_data.name, "exit_name": ShufflableExits[relevant_transition].back.name}
                        )
            self.starting_region = random.choice(valid_starting_regions)
            for x in range(2):
                randomizer.LogicFiles.DKIsles.LogicRegions[Regions.GameStart].exits[x + 1].dest = self.starting_region["region"]

        # Set keys required for KRool
        KeyEvents = [
            Events.JapesKeyTurnedIn,
            Events.AztecKeyTurnedIn,
            Events.FactoryKeyTurnedIn,
            Events.GalleonKeyTurnedIn,
            Events.ForestKeyTurnedIn,
            Events.CavesKeyTurnedIn,
            Events.CastleKeyTurnedIn,
            Events.HelmKeyTurnedIn,
        ]
        key_list = KeyEvents.copy()
        required_key_count = 0
        if self.keys_random:
            required_key_count = randint(0, 8)
        if self.select_keys:
            self.krool_keys_required = KeyEvents.copy()
            for key in self.starting_keys_list_selected:
                if key == "key1":
                    self.krool_keys_required.remove(key_list[0])
                if key == "key2":
                    self.krool_keys_required.remove(key_list[1])
                if key == "key3":
                    self.krool_keys_required.remove(key_list[2])
                if key == "key4":
                    self.krool_keys_required.remove(key_list[3])
                if key == "key5":
                    self.krool_keys_required.remove(key_list[4])
                if key == "key6":
                    self.krool_keys_required.remove(key_list[5])
                if key == "key7":
                    self.krool_keys_required.remove(key_list[6])
                if key == "key8":
                    self.krool_keys_required.remove(key_list[7])
        else:
            required_key_count = self.krool_key_count
        if self.krool_access or self.win_condition == "get_key8":
            # If helm is guaranteed or the win condition, make sure it's added and included in the key count
            self.krool_keys_required.append(Events.HelmKeyTurnedIn)
            key_list.remove(Events.HelmKeyTurnedIn)
            required_key_count -= 1
        if not self.select_keys:
            random.shuffle(key_list)
            for x in range(required_key_count):
                self.krool_keys_required.append(key_list[x])
        if Events.JapesKeyTurnedIn not in self.krool_keys_required:
            ItemList[Items.JungleJapesKey].playthrough = False
        if Events.AztecKeyTurnedIn not in self.krool_keys_required:
            ItemList[Items.AngryAztecKey].playthrough = False
        if Events.FactoryKeyTurnedIn not in self.krool_keys_required:
            ItemList[Items.FranticFactoryKey].playthrough = False
        if Events.GalleonKeyTurnedIn not in self.krool_keys_required:
            ItemList[Items.GloomyGalleonKey].playthrough = False
        if Events.ForestKeyTurnedIn not in self.krool_keys_required:
            ItemList[Items.FungiForestKey].playthrough = False
        if Events.CavesKeyTurnedIn not in self.krool_keys_required:
            ItemList[Items.CrystalCavesKey].playthrough = False
        if Events.CastleKeyTurnedIn not in self.krool_keys_required:
            ItemList[Items.CreepyCastleKey].playthrough = False
        if Events.HelmKeyTurnedIn not in self.krool_keys_required:
            ItemList[Items.HideoutHelmKey].playthrough = False

        # Banana medals
        if self.random_medal_requirement:
            # Range roughly from 4 to 15, average around 10
            self.medal_requirement = round(random.normalvariate(10, 1.5))

        # Boss Rando
        self.boss_maps = ShuffleBosses(self.boss_location_rando)
        self.boss_kongs = ShuffleBossKongs(self)
        self.kutout_kongs = ShuffleKutoutKongs(self.boss_maps, self.boss_kongs, self.boss_kong_rando)
        self.kko_phase_order = ShuffleKKOPhaseOrder(self)

        # Bonus Barrel Rando
        if self.bonus_barrel_auto_complete:
            self.bonus_barrels = "skip"
        elif self.bonus_barrel_rando and not self.minigames_list_selected:
            self.bonus_barrels = "random"
        elif self.bonus_barrel_rando and self.minigames_list_selected:
            self.bonus_barrels = "selected"
        # Helm Barrel Rando
        if self.helm_setting == "skip_all":
            self.helm_barrels = "skip"
        elif self.bonus_barrel_rando:
            self.helm_barrels = "random"

        # Loading Zone Rando
        if self.level_randomization == "level_order":
            self.shuffle_loading_zones = "levels"
        elif self.level_randomization == "loadingzone":
            self.shuffle_loading_zones = "all"
        elif self.level_randomization == "loadingzonesdecoupled":
            self.shuffle_loading_zones = "all"
            self.decoupled_loading_zones = True
        elif self.level_randomization == "vanilla":
            self.shuffle_loading_zones = "none"

        # Kong rando
        # Temp until Slider UI binding gets fixed
        if self.starting_random:
            self.starting_kongs_count = randint(1, 5)
        if self.starting_kongs_count == 5:
            self.kong_rando = False
        if self.kong_rando:
            self.starting_kong_list = random.sample(kongs, self.starting_kongs_count)
            self.starting_kong = random.choice(self.starting_kong_list)
            # Kong freers are decided in the fill, set as any kong for now
            self.diddy_freeing_kong = Kongs.any
            self.lanky_freeing_kong = Kongs.any
            self.tiny_freeing_kong = Kongs.any
            self.chunky_freeing_kong = Kongs.any
            if self.shuffle_items and Types.Kong in self.shuffled_location_types:
                self.kong_locations = [Locations.DiddyKong, Locations.LankyKong, Locations.TinyKong, Locations.ChunkyKong]
            else:
                self.kong_locations = self.SelectKongLocations()
        else:
            self.possible_kong_list = kongs.copy()
            self.possible_kong_list.remove(0)
            self.starting_kong_list = random.sample(self.possible_kong_list, self.starting_kongs_count - 1)
            self.starting_kong_list.append(Kongs.donkey)
            self.starting_kong = Kongs.donkey
            self.diddy_freeing_kong = Kongs.donkey
            self.lanky_freeing_kong = Kongs.donkey
            self.tiny_freeing_kong = Kongs.diddy
            self.chunky_freeing_kong = Kongs.lanky
            # Set up kong locations with vanilla kongs in them, removing any kongs we start with
            self.kong_locations = [Locations.DiddyKong, Locations.LankyKong, Locations.TinyKong, Locations.ChunkyKong]
            if Kongs.diddy in self.starting_kong_list:
                self.kong_locations.remove(Locations.DiddyKong)
            if Kongs.lanky in self.starting_kong_list:
                self.kong_locations.remove(Locations.LankyKong)
            if Kongs.tiny in self.starting_kong_list:
                self.kong_locations.remove(Locations.TinyKong)
            if Kongs.chunky in self.starting_kong_list:
                self.kong_locations.remove(Locations.ChunkyKong)

        # Designate the Rock GB as a location for the starting kong
        LocationList[Locations.IslesDonkeyJapesRock].kong = self.starting_kong

        # Kongs needed for level progression
        if self.starting_kongs_count < 5 and (self.shuffle_loading_zones == "levels" or self.shuffle_loading_zones == "none") and not self.no_logic:
            self.kongs_for_progression = True

        # Move Location Rando
        if self.move_rando == "start_with":
            self.unlock_all_moves = True

        # Kasplat Rando
        self.kasplat_rando = False
        self.kasplat_location_rando = False
        if self.kasplat_rando_setting == "vanilla_locations":
            self.kasplat_rando = True
        if self.kasplat_rando_setting == "location_shuffle":
            self.kasplat_rando = True
            self.kasplat_location_rando = True

        # Some settings (mostly win conditions) require modification of items in order to better generate the spoiler log
        if self.win_condition == "all_fairies":
            ItemList[Items.BananaFairy].playthrough = True
        if self.win_condition == "all_blueprints":
            for item_index in ItemList:
                if ItemList[item_index].type == Types.Blueprint:
                    ItemList[item_index].playthrough = True
        if self.win_condition == "all_medals":
            ItemList[Items.BananaMedal].playthrough = True
        if not self.crown_door_open:
            ItemList[Items.BattleCrown].playthrough = True

        self.free_trade_items = self.free_trade_setting != "none"
        self.free_trade_blueprints = self.free_trade_setting == "major_collectibles"

    def update_valid_locations(self):
        """Calculate (or recalculate) valid locations for items by type."""
        self.valid_locations = {}
        self.valid_locations[Types.Kong] = self.kong_locations.copy()
        # If shops are not shuffled into the larger pool, calculate shop locations for shop-bound moves
        if self.move_rando not in ("off", "item_shuffle"):
            self.valid_locations[Types.Shop] = {}
            self.valid_locations[Types.Shop][Kongs.donkey] = []
            self.valid_locations[Types.Shop][Kongs.diddy] = []
            self.valid_locations[Types.Shop][Kongs.lanky] = []
            self.valid_locations[Types.Shop][Kongs.tiny] = []
            self.valid_locations[Types.Shop][Kongs.chunky] = []
            if self.move_rando == "on":
                self.valid_locations[Types.Shop][Kongs.donkey] = DonkeyMoveLocations.copy()
                self.valid_locations[Types.Shop][Kongs.diddy] = DiddyMoveLocations.copy()
                self.valid_locations[Types.Shop][Kongs.lanky] = LankyMoveLocations.copy()
                self.valid_locations[Types.Shop][Kongs.tiny] = TinyMoveLocations.copy()
                self.valid_locations[Types.Shop][Kongs.chunky] = ChunkyMoveLocations.copy()
            elif self.move_rando == "cross_purchase":
                allKongMoveLocations = DonkeyMoveLocations.copy()
                allKongMoveLocations.update(DiddyMoveLocations.copy())
                allKongMoveLocations.update(TinyMoveLocations.copy())
                allKongMoveLocations.update(ChunkyMoveLocations.copy())
                allKongMoveLocations.update(LankyMoveLocations.copy())
                if self.training_barrels == "shuffled" and Types.TrainingBarrel not in self.shuffled_location_types:
                    allKongMoveLocations.update(TrainingBarrelLocations.copy())
                if self.shockwave_status in ("vanilla", "start_with") and Types.Shockwave not in self.shuffled_location_types:
                    allKongMoveLocations.remove(Locations.CameraAndShockwave)
                self.valid_locations[Types.Shop][Kongs.donkey] = allKongMoveLocations
                self.valid_locations[Types.Shop][Kongs.diddy] = allKongMoveLocations
                self.valid_locations[Types.Shop][Kongs.lanky] = allKongMoveLocations
                self.valid_locations[Types.Shop][Kongs.tiny] = allKongMoveLocations
                self.valid_locations[Types.Shop][Kongs.chunky] = allKongMoveLocations
            self.valid_locations[Types.Shop][Kongs.any] = SharedShopLocations.copy()
            if self.shockwave_status not in ("vanilla", "start_with") and Types.Shockwave not in self.shuffled_location_types:
                self.valid_locations[Types.Shop][Kongs.any].add(Locations.CameraAndShockwave)
            elif Locations.CameraAndShockwave in self.valid_locations[Types.Shop][Kongs.tiny]:
                self.valid_locations[Types.Shop][Kongs.tiny].remove(Locations.CameraAndShockwave)
            if self.training_barrels == "shuffled" and Types.TrainingBarrel not in self.shuffled_location_types:
                for kong in Kongs:
                    self.valid_locations[Types.Shop][kong].update(TrainingBarrelLocations.copy())
            self.valid_locations[Types.Shockwave] = self.valid_locations[Types.Shop][Kongs.any]
            self.valid_locations[Types.TrainingBarrel] = self.valid_locations[Types.Shop][Kongs.any]

        if self.shuffle_items and any(self.shuffled_location_types):
            # All shuffled locations are valid except for Kong locations (the Kong inside the cage, not the GB) - those can only be Kongs
            shuffledLocations = [location for location in LocationList if LocationList[location].type in self.shuffled_location_types and LocationList[location].type != Types.Kong]
            if Types.Shop in self.shuffled_location_types:
                self.valid_locations[Types.Shop] = {}
                # Cross-kong acquisition is assumed in full item rando, calculate the list of all Kong-specific shops
                allKongMoveLocations = DonkeyMoveLocations.copy()
                allKongMoveLocations.update(DiddyMoveLocations.copy())
                allKongMoveLocations.update(TinyMoveLocations.copy())
                allKongMoveLocations.update(ChunkyMoveLocations.copy())
                allKongMoveLocations.update(LankyMoveLocations.copy())
                # Generate a list of all valid locations EXCEPT the Kong-specific shops - these are valid locations for shared moves
                locations_excluding_kong_shops = [location for location in shuffledLocations if location not in allKongMoveLocations]
                self.valid_locations[Types.Shop][Kongs.any] = locations_excluding_kong_shops
                # Shockwave and Training Barrels can only be shuffled if shops are shuffled and their valid locations are non-Kong-specific shops
                if Types.Shockwave in self.shuffled_location_types:
                    locations_excluding_kong_shops.append(Locations.CameraAndShockwave)
                    self.valid_locations[Types.Shockwave] = locations_excluding_kong_shops
                if Types.TrainingBarrel in self.shuffled_location_types:
                    self.valid_locations[Types.TrainingBarrel] = locations_excluding_kong_shops
                # Kong-specific moves can go in any non-shared shop location
                locations_excluding_shared_shops = [location for location in shuffledLocations if location not in SharedShopLocations]
                self.valid_locations[Types.Shop][Kongs.donkey] = locations_excluding_shared_shops
                self.valid_locations[Types.Shop][Kongs.diddy] = locations_excluding_shared_shops
                self.valid_locations[Types.Shop][Kongs.lanky] = locations_excluding_shared_shops
                self.valid_locations[Types.Shop][Kongs.tiny] = locations_excluding_shared_shops
                self.valid_locations[Types.Shop][Kongs.chunky] = locations_excluding_shared_shops
            if Types.Blueprint in self.shuffled_location_types:
                # Blueprints are banned from Key or Crown locations
                blueprintValidTypes = [typ for typ in self.shuffled_location_types if typ not in (Types.Crown, Types.Key)]
                # These locations do not have a set Kong assigned to them and can't have blueprints
                badBPLocations = (
                    Locations.IslesDonkeyJapesRock,
                    Locations.JapesDonkeyFrontofCage,
                    Locations.JapesDonkeyFreeDiddy,
                    Locations.AztecDiddyFreeTiny,
                    Locations.AztecDonkeyFreeLanky,
                    Locations.FactoryLankyFreeChunky,
                )
                blueprintLocations = [location for location in LocationList if location not in badBPLocations and LocationList[location].type in blueprintValidTypes]
                self.valid_locations[Types.Blueprint] = {}
                self.valid_locations[Types.Blueprint][Kongs.donkey] = [location for location in blueprintLocations if LocationList[location].kong == Kongs.donkey]
                self.valid_locations[Types.Blueprint][Kongs.diddy] = [location for location in blueprintLocations if LocationList[location].kong == Kongs.diddy]
                self.valid_locations[Types.Blueprint][Kongs.lanky] = [location for location in blueprintLocations if LocationList[location].kong == Kongs.lanky]
                self.valid_locations[Types.Blueprint][Kongs.tiny] = [location for location in blueprintLocations if LocationList[location].kong == Kongs.tiny]
                self.valid_locations[Types.Blueprint][Kongs.chunky] = [location for location in blueprintLocations if LocationList[location].kong == Kongs.chunky]
            if Types.Banana in self.shuffled_location_types:
                self.valid_locations[Types.Banana] = shuffledLocations
            if Types.Crown in self.shuffled_location_types:
                # Banned for technical reasons
                banned_crown_locations = (
                    Locations.HelmDonkeyMedal,
                    Locations.HelmDiddyMedal,
                    Locations.HelmLankyMedal,
                    Locations.HelmTinyMedal,
                    Locations.HelmChunkyMedal,
                    Locations.JapesDiddyMinecarts,
                    Locations.CastleDonkeyMinecarts,
                    Locations.ForestChunkyMinecarts,
                    Locations.IslesDonkeyInstrumentPad,
                    Locations.IslesDiddyInstrumentPad,
                    Locations.IslesLankyInstrumentPad,
                    Locations.IslesTinyInstrumentPad,
                    Locations.IslesChunkyInstrumentPad,
                )
                self.valid_locations[Types.Crown] = [location for location in shuffledLocations if location not in banned_crown_locations]
            if Types.Key in self.shuffled_location_types:
                self.valid_locations[Types.Key] = shuffledLocations
            if Types.Medal in self.shuffled_location_types:
                self.valid_locations[Types.Medal] = shuffledLocations
            if Types.Coin in self.shuffled_location_types:
                self.valid_locations[Types.Coin] = shuffledLocations
            if Types.Kong in self.shuffled_location_types:
                # Banned because it defeats the purpose of starting with X Kongs
                banned_kong_locations = (
                    Locations.IslesSwimTrainingBarrel,
                    Locations.IslesVinesTrainingBarrel,
                    Locations.IslesBarrelsTrainingBarrel,
                    Locations.IslesOrangesTrainingBarrel,
                    Locations.IslesDonkeyJapesRock,
                )
                self.valid_locations[Types.Kong].extend([loc for loc in shuffledLocations if loc not in banned_kong_locations])  # No items can be in Kong cages but Kongs can be in all other locations

    def GetValidLocationsForItem(self, item_id):
        """Return the valid locations the input item id can be placed in."""
        item_obj = ItemList[item_id]
        valid_locations = []
        # Some types of items have restrictions on valid locations based on their kong
        if item_obj.type in (Types.Shop, Types.Blueprint):
            valid_locations = self.valid_locations[item_obj.type][item_obj.kong]
        else:
            valid_locations = self.valid_locations[item_obj.type]
        return valid_locations

    def SelectKongLocations(self):
        """Select which random kong locations to use depending on number of starting kongs."""
        # First determine which kong cages will have a kong to free
        kongCageLocations = [Locations.DiddyKong, Locations.LankyKong, Locations.TinyKong, Locations.ChunkyKong]
        # Randomly decide which kong cages will not have kongs in them
        for i in range(0, self.starting_kongs_count - 1):
            kongLocation = random.choice(kongCageLocations)
            kongCageLocations.remove(kongLocation)

        # The following cases do not apply if you could bypass the Guitar door without Diddy
        bypass_guitar_door = self.open_levels or self.activate_all_bananaports == "all"
        # In case both Diddy and Chunky need to be freed but only Aztec locations are available
        # This would be impossible, as one of them must free the Tiny location and Diddy is needed for the Lanky location
        if (
            not bypass_guitar_door
            and self.starting_kongs_count == 3
            and Kongs.diddy not in self.starting_kong_list
            and Kongs.chunky not in self.starting_kong_list
            and Locations.TinyKong in kongCageLocations
            and Locations.LankyKong in kongCageLocations
        ):
            # Move a random location to a non-Aztec location
            kongCageLocations.pop()
            kongCageLocations.append(random.choice(Locations.DiddyKong, Locations.ChunkyKong))
        # In case Diddy is the only kong to free, he can't be in the Llama Temple since it's behind the Guitar door
        if not bypass_guitar_door and self.starting_kongs_count == 4 and Kongs.diddy not in self.starting_kong_list and Locations.LankyKong in kongCageLocations:
            # Move diddy kong from llama temple to another cage randomly chosen
            kongCageLocations.remove(Locations.LankyKong)
            kongCageLocations.append(random.choice(Locations.DiddyKong, Locations.TinyKong, Locations.ChunkyKong))
        return kongCageLocations

    def __repr__(self):
        """Return printable version of the object as json.

        Returns:
            str: Json string of the dict.
        """
        return json.dumps(self.__dict__)

    @staticmethod
    def __get_hash():
        """Get the hash value of all of the source code loaded."""
        return whl_hash

    def compare_hash(self, hash):
        """Compare our hash with a passed hash value."""
        if self.__hash != hash:
            raise Exception("Error: Comparison failed, Hashes do not match.")

    def verify_hash(self):
        """Verify our hash files match our existing code."""
        try:
            if self.__hash == self.__get_hash():
                return True
            else:
                raise Exception("Error: Hashes do not match")
        except Exception:
            return False

    def __setattr__(self, name, value):
        """Set an attributes value but only after verifying our hash."""
        self.verify_hash()
        super().__setattr__(name, value)

    def __delattr__(self, name):
        """Delete an attribute if its not our settings hash or if the code has been modified."""
        self.verify_hash()
        if name == "_Settings__hash":
            raise Exception("Error: Attempted deletion of race hash.")
        super().__delattr__(name)
