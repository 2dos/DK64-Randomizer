"""Settings class and functions."""
import hashlib
import inspect
import json
import random
import sys

from randomizer.ShuffleBosses import ShuffleBosses, ShuffleBossKongs, ShuffleKutoutKongs
from randomizer.Enums.Events import Events
from randomizer.Enums.Kongs import Kongs, GetKongs
from randomizer.Enums.Locations import Locations
from randomizer.Prices import RandomizePrices, VanillaPrices
from random import randint


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
        self.blocker_max = self.blocker_text if self.blocker_text else 50
        self.troff_max = self.troff_text if self.troff_text else 270
        self.troff_min = round(self.troff_max / 3)
        # Always start with training barrels currently
        # training_barrels: str
        # normal
        # shuffled
        # startwith
        self.training_barrels = "startwith"

        # currently just set to moves by shop_location_rando
        # shuffle_items: str
        # none
        # moves
        # all (currently only theoretical)
        self.shuffle_items = "none"

        # Pointless with just move rando, maybe have it once full rando
        # progressive_upgrades: bool
        self.progressive_upgrades = False

        self.prices = VanillaPrices.copy()
        self.resolve_settings()

    def update_progression_totals(self):
        """Update the troff and blocker totals if we're randomly setting them."""
        # Assign weights to Troff n Scoff based on level order if not shuffling loading zones
        self.troff_weight_0 = 0.5
        self.troff_weight_1 = 0.55
        self.troff_weight_2 = 0.6
        self.troff_weight_3 = 0.7
        self.troff_weight_4 = 0.8
        self.troff_weight_5 = 0.9
        self.troff_weight_6 = 1.0
        if self.level_randomization in ("loadingzone", "loadingzonesdecoupled"):
            self.troff_weight_0 = 1
            self.troff_weight_1 = 1
            self.troff_weight_2 = 1
            self.troff_weight_3 = 1
            self.troff_weight_4 = 1
            self.troff_weight_5 = 1
            self.troff_weight_6 = 1

        if self.randomize_cb_required_amounts:
            randomlist = random.sample(range(self.troff_min, self.troff_max), 7)
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
            b_lockers.append(1)
            if self.shuffle_loading_zones == "all":
                random.shuffle(b_lockers)
            else:
                b_lockers.sort()
            self.blocker_0 = b_lockers[0]
            self.blocker_1 = b_lockers[1]
            self.blocker_2 = b_lockers[2]
            self.blocker_3 = b_lockers[3]
            self.blocker_4 = b_lockers[4]
            self.blocker_5 = b_lockers[5]
            self.blocker_6 = b_lockers[6]
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
        self.shop_location_rando = None
        self.random_prices = None
        self.boss_location_rando = None
        self.boss_kong_rando = None
        self.kasplat_rando = None

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
        # start_with_moves: bool
        self.unlock_all_moves = None
        # crown_door_open: bool
        self.crown_door_open = None
        # coin_door_open: bool
        self.coin_door_open = None
        # unlock_fairy_shockwave: bool
        self.unlock_fairy_shockwave = None
        # krool_phase_count: int, [1-5]
        self.krool_phase_count = 5
        self.krool_random = False
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
        self.gnawty_barrels = False

        # hard_shooting: bool
        self.hard_shooting = False

        # hard_mad_jack: bool
        self.hard_mad_jack = False

        # damage multiplier
        self.damage_amount = "default"

        # shuffle_loading_zones: str
        # none
        # levels
        # all
        self.shuffle_loading_zones = "none"

        # decoupled_loading_zones: bool
        self.decoupled_loading_zones = False

        #  Music
        self.music_bgm = None
        self.music_fanfares = None
        self.music_events = None

        #  Color
        self.dk_colors = None
        self.diddy_colors = None
        self.lanky_colors = None
        self.tiny_colors = None
        self.chunky_colors = None

        #  Misc
        self.generate_spoilerlog = None
        self.fast_start_beginning_of_game = None
        self.helm_setting = None
        self.quality_of_life = None
        self.enable_tag_anywhere = None
        self.krool_phase_order_rando = None
        self.krool_access = False
        self.open_lobbies = None
        self.random_medal_requirement = True
        self.bananaport_rando = False
        self.shop_indicator = False
        self.randomize_cb_required_amounts = False
        self.randomize_blocker_required_amounts = False
        self.perma_death = False
        self.disable_tag_barrels = False
        self.level_randomization = "none"
        self.kong_rando = False
        self.kongs_for_progression = False
        self.wrinkly_hints = "off"

    def resolve_settings(self):
        """Resolve settings which are not directly set through the UI."""
        kongs = GetKongs()

        # Price Rando
        if self.random_prices != "vanilla":
            self.prices = RandomizePrices(self.random_prices)

        # B Locker and Troff n Scoff amounts Rando
        self.update_progression_totals()

        # Handle K. Rool Phases
        self.krool_donkey = False
        self.krool_diddy = False
        self.krool_lanky = False
        self.krool_tiny = False
        self.krool_chunky = True

        phases = [x for x in kongs if x != Kongs.chunky]
        if self.krool_phase_order_rando:
            random.shuffle(phases)
        if self.krool_random:
            self.krool_phase_count = randint(1, 5)
        if isinstance(self.krool_phase_count, str) is True:
            self.krool_phase_count = 5
        if self.krool_phase_count < 5:
            phases = random.sample(phases, self.krool_phase_count - 1)
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
        orderedPhases.append(Kongs.chunky)
        self.krool_order = orderedPhases

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
        if self.keys_random:
            required_key_count = randint(0, 8)
        else:
            required_key_count = self.krool_key_count
        if self.krool_access:
            # If helm guaranteed, make sure it's added and included in the key count
            self.krool_keys_required.append(Events.HelmKeyTurnedIn)
            key_list.remove(Events.HelmKeyTurnedIn)
            required_key_count -= 1
        random.shuffle(key_list)
        for x in range(required_key_count):
            self.krool_keys_required.append(key_list[x])

        # Banana medals
        if self.random_medal_requirement:
            # Range roughly from 4 to 15, average around 10
            self.BananaMedalsRequired = round(random.normalvariate(10, 1.5))
        else:
            self.BananaMedalsRequired = 15

        # Boss Rando
        self.boss_maps = ShuffleBosses(self.boss_location_rando)
        self.boss_kongs = ShuffleBossKongs(self)
        self.kutout_kongs = ShuffleKutoutKongs(self.boss_maps, self.boss_kongs, self.boss_kong_rando)

        # Bonus Barrel Rando
        if self.bonus_barrel_auto_complete:
            self.bonus_barrels = "skip"
        elif self.bonus_barrel_rando:
            self.bonus_barrels = "random"
        elif self.gnawty_barrels:
            self.bonus_barrels = "all_beaver_bother"
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
            # Kong locations are adjusted in the fill, set all possible for now
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

        # Kongs needed for level progression
        if self.starting_kongs_count < 5 and (self.shuffle_loading_zones == "levels" or self.shuffle_loading_zones == "none"):
            self.kongs_for_progression = True

        # Move Location Rando
        if self.shop_location_rando:
            self.shuffle_items = "moves"

    def SelectKongLocations(self):
        """Select which random kong locations to use depending on number of starting kongs."""
        # First determine which kong cages will have a kong to free
        kongCageLocations = [
            Locations.DiddyKong,
            Locations.LankyKong,
            Locations.TinyKong,
            Locations.ChunkyKong,
        ]
        # Randomly decide which kong cages will not have kongs in them
        for i in range(0, self.starting_kongs_count - 1):
            kongLocation = random.choice(kongCageLocations)
            kongCageLocations.remove(kongLocation)
            # In case diddy is the only kong to free, he can't be in the llama temple since it's behind guitar door
        if self.starting_kongs_count == 4 and Kongs.diddy not in self.starting_kong_list and Locations.LankyKong in kongCageLocations:
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
        hash_value = []
        files = []
        files.append(inspect.getsource(Settings))
        files.append(inspect.getsource(__import__("randomizer.Spoiler")))
        files.append(inspect.getsource(__import__("randomizer.Fill")))
        files.append(inspect.getsource(__import__("randomizer.BackgroundRandomizer")))
        try:
            files.append(inspect.getsource(__import__("version")))
        except Exception:  # Fails if running python by itself
            pass
        for file in sorted(files):
            hash_value.append(hashlib.md5(file.encode("utf-8")).hexdigest())
        return "".join(hash_value)

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
