"""Settings class and functions."""
import hashlib
import inspect
import json
import random
import sys

from randomizer.BossShuffle import ShuffleBosses, ShuffleBossKongs, ShuffleKutoutKongs
from randomizer.Enums.Events import Events
from randomizer.Enums.Kongs import Kongs
from randomizer.Prices import RandomizePrices, VanillaPrices


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
        self.update_progression_totals()
        self.seed_id = str(self.seed)
        self.seed = str(self.seed) + self.__hash
        self.set_seed()
        # Store banana values in array
        self.EntryGBs = [
            self.blocker_0,
            self.blocker_1,
            self.blocker_2,
            self.blocker_3,
            self.blocker_4,
            self.blocker_5,
            self.blocker_6,
            self.blocker_7,
        ]
        self.BossBananas = [
            self.troff_0,
            self.troff_1,
            self.troff_2,
            self.troff_3,
            self.troff_4,
            self.troff_5,
            self.troff_6,
        ]
        self.seed_hash = [random.randint(0, 9) for i in range(5)]
        # Settings which are not yet implemented on the web page

        # Waiting on price branch
        # random_prices: str
        # vanilla
        # low
        # medium
        # high
        self.random_prices = "vanilla"

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

        # Not yet implemented
        # starting_kong: Kongs enum
        self.starting_kong = Kongs.donkey

        # Pointless with just move rando, maybe have it once full rando
        # progressive_upgrades: bool
        self.progressive_upgrades = False

        # Waiting for UI branch
        # open_lobbies: bool
        self.open_lobbies = True

        # Waiting for UI branch
        # krool_access: str
        # vanilla (Keys 3 and 8)
        # all (All keys)
        # random (Each key has 50% chance of being required)
        # random_helm (Same as random but helm is guaranteed)
        # open (Ship is there from start)
        self.krool_access = "random_helm"
        self.krool_keys_required = []

        self.prices = VanillaPrices.copy()
        self.resolve_settings()

    def update_progression_totals(self):
        """Update the troff and blocker totals if we're randomly setting them."""
        if self.randomize_cb_required_amounts:
            randomlist = random.sample(range(0, 260), 7)
            cbs = randomlist
            self.troff_0 = cbs[0]
            self.troff_1 = cbs[1]
            self.troff_2 = cbs[2]
            self.troff_3 = cbs[3]
            self.troff_4 = cbs[4]
            self.troff_5 = cbs[5]
            self.troff_6 = cbs[6]
        if self.randomize_blocker_required_amounts:
            randomlist = random.sample(range(0, 70), 7)
            b_lockers = randomlist
            b_lockers.append(1)
            random.shuffle(b_lockers)
            self.blocker_0 = b_lockers[0]
            self.blocker_1 = b_lockers[1]
            self.blocker_2 = b_lockers[2]
            self.blocker_3 = b_lockers[3]
            self.blocker_4 = b_lockers[4]
            self.blocker_5 = b_lockers[5]
            self.blocker_6 = b_lockers[6]
            self.blocker_7 = b_lockers[7]

    def generate_main(self):
        """Set Default items on main page."""
        self.seed = None
        self.download_patch_file = None
        self.bonus_barrel_rando = None
        self.shuffle_levels = None
        self.loading_zone_rando = None
        self.loading_zone_coupled = None
        self.shop_location_rando = None
        self.shop_price_rando = None
        self.boss_location_rando = None
        self.boss_kong_rando = None
        self.kasplat = None

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

    def generate_misc(self):
        """Set default items on misc page."""
        #  Settings which affect logic
        # start_with_moves: bool
        self.unlock_all_moves = None
        # unlock_all_kongs: bool
        self.unlock_all_kongs = None
        # crown_door_open: bool
        self.crown_door_open = None
        # coin_door_open: bool
        self.coin_door_open = None
        # unlock_fairy_shockwave: bool
        self.unlock_fairy_shockwave = None
        # krool_phase_count: int, [1-5]
        self.krool_phase_count = 5

        # bonus_barrels: str
        # skip - NOT IMPLEMENTED YET
        # normal
        # random
        self.bonus_barrels = "normal"

        # hard_shooting: bool
        self.hard_shooting = False

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

        #  Misc
        self.generate_spoilerlog = None
        self.fast_start_beginning_of_game = None
        self.fast_start_hideout_helm = None
        self.quality_of_life = None
        self.enable_tag_anywhere = None
        self.random_krool_phase_order = None
        self.random_medal_requirement = True
        self.bananaport_rando = False
        self.shop_indicator = False
        self.randomize_cb_required_amounts = False
        self.randomize_blocker_required_amounts = False
        self.kasplat_rando = False
        self.perma_death = False
        self.disable_tag_barrels = False
        self.level_randomization = "none"

    def resolve_settings(self):
        """Resolve settings which are not directly set through the UI."""
        # Price Rando
        if self.shop_price_rando:
            self.random_prices = "medium"  # TODO Make a UI option to set price difficulty

        if self.random_prices != "vanilla":
            self.prices = RandomizePrices(self.random_prices)

        # Handle K. Rool Phases
        self.krool_donkey = False
        self.krool_diddy = False
        self.krool_lanky = False
        self.krool_tiny = False
        self.krool_chunky = True

        phases = ["donkey", "diddy", "lanky", "tiny"]
        if self.random_krool_phase_order:
            random.shuffle(phases)
        if self.krool_phase_count < 5:
            phases = random.sample(phases, self.krool_phase_count - 1)
        orderedPhases = []
        for kong in phases:
            if kong == "donkey":
                self.krool_donkey = True
                orderedPhases.append(0)
            if kong == "diddy":
                self.krool_diddy = True
                orderedPhases.append(1)
            if kong == "lanky":
                self.krool_lanky = True
                orderedPhases.append(2)
            if kong == "tiny":
                self.krool_tiny = True
                orderedPhases.append(3)
        orderedPhases.append(4)
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
        if self.krool_access == "vanilla":
            self.krool_keys_required.extend([Events.FactoryKeyTurnedIn, Events.HelmKeyTurnedIn])
        elif self.krool_access == "all":
            self.krool_keys_required.extend(KeyEvents)
        elif self.krool_access == "random" or self.krool_access == "random_helm":
            for event in KeyEvents:
                if random.randint(1, 2) == 2:
                    self.krool_keys_required.append(event)
        if self.krool_access == "random_helm" and Events.HelmKeyTurnedIn not in self.krool_keys_required:
            self.krool_keys_required.append(Events.HelmKeyTurnedIn)

        # Banana medals
        if self.random_medal_requirement:
            # Range roughly from 4 to 15, average around 10
            self.BananaMedalsRequired = round(random.normalvariate(10, 0.15))
        else:
            self.BananaMedalsRequired = 15

        # Boss Rando
        self.boss_maps = ShuffleBosses(self.boss_location_rando)
        self.boss_kongs = ShuffleBossKongs(self.boss_maps, self.boss_kong_rando)
        self.kutout_kongs = ShuffleKutoutKongs(self.boss_maps, self.boss_kongs, self.boss_kong_rando)

        # Bonus Barrel Rando
        if self.bonus_barrel_rando:
            self.bonus_barrels = "random"

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

        # Move Location Rando
        if self.shop_location_rando:
            self.shuffle_items = "moves"

    def __repr__(self):
        """Return printable version of the object as json.

        Returns:
            str: Json string of the dict.
        """
        return json.dumps(self.__dict__)

    def __get_hash(self):
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
