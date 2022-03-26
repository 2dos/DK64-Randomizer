"""Settings class and functions."""
import hashlib
import inspect
import json
import random
import sys
from randomizer.BossShuffle import ShuffleBosses

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

        # Settings which are not yet implemented on the web page

        # hard_shooting: bool
        self.hard_shooting = False

        # random_prices: str
        # vanilla
        # low
        # medium
        # high
        self.random_prices = "vanilla"

        # training_barrels: str
        # normal
        # shuffled
        # startwith
        self.training_barrels = "startwith"

        # starting_kong: Kongs enum
        self.starting_kong = Kongs.donkey

        # shuffle_items: str
        # none
        # moves
        # all (currently only theoretical)
        self.shuffle_items = "none"

        # progressive_upgrades: bool
        self.progressive_upgrades = True

        self.prices = VanillaPrices.copy()
        self.resolve_settings()

    def generate_main(self):
        """Set Default items on main page."""
        self.seed = None
        self.download_json = None
        self.bonus_barrel_rando = None
        self.loading_zone_rando = None
        self.loading_zone_coupled = None
        self.shop_location_rando = None
        self.shop_price_rando = None
        self.boss_location_rando = None
        self.boss_kong_rando = None

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

        # shuffle_loading_zones: str
        # none
        # levels
        # all
        self.shuffle_loading_zones = "none"

        # decoupled_loading_zones: bool
        self.decoupled_loading_zones = True

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

    def resolve_settings(self):
        """Resolve settings which are not directly set through the UI."""
        # Price Rando
        if self.shop_price_rando:
            self.random_prices = "medium" # TODO Make a UI option to set price difficulty

        if self.random_prices != "vanilla":
            self.prices = RandomizePrices(self.random_prices)

        # Handle K. Rool Phases
        self.krool_donkey = False
        self.krool_diddy = False
        self.krool_lanky = False
        self.krool_tiny = False
        self.krool_chunky = True

        phases = ["donkey", "diddy", "lanky", "tiny"]
        phases = random.sample(phases, self.krool_phase_count - 1)
        orderedPhases = []
        if "donkey" in phases:
            self.krool_donkey = True
            orderedPhases.append("donkey")
        if "diddy" in phases:
            self.krool_diddy = True
            orderedPhases.append("diddy")
        if "lanky" in phases:
            self.krool_lanky = True
            orderedPhases.append("lanky")
        if "tiny" in phases:
            self.krool_tiny = True
            orderedPhases.append("tiny")

        if self.random_krool_phase_order:
            random.shuffle(orderedPhases)
        orderedPhases.append("chunky")
        self.krool_order = orderedPhases

        # Boss Location Rando
        self.boss_maps = ShuffleBosses(self.boss_location_rando)

        # Bonus Barrel Rando
        if self.bonus_barrel_rando:
            self.bonus_barrels = "random"

        # Loading Zone Rando
        if self.loading_zone_rando:
            self.shuffle_loading_zones = "all"
        if self.loading_zone_coupled:
            self.decoupled_loading_zones = False

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
