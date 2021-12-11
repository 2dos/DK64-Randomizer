"""Settings class and functions."""
import json


class Settings:
    """Class used to store settings for seed generation."""

    def __init__(self, form_data: dict):
        """Init all the settings using the form data to set the flags.

        Args:
            form_data (dict): Post data from the html form.
        """
        self.algorithm = None
        self.generate_main()
        self.generate_progression()
        self.generate_misc()
        for k, v in form_data.items():
            setattr(self, k, v)

    def generate_main(self):
        """Set Default items on main page."""
        self.randomize_progression = None
        self.seed = None
        self.download_json = None

    def generate_progression(self):
        """Set default items on progression page."""
        self.blocker_selected = None
        self.troff_selected = None
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
        self.unlock_all_moves = None
        self.generate_spoilerlog = None
        self.unlock_all_kongs = None
        self.fast_start_beginning_of_game = None
        self.fast_start_hideout_helm = None
        self.crown_door_open = None
        self.coin_door_open = None
        self.quality_of_life = None
        self.unlock_fairy_shockwave = None
        self.enable_tag_anywhere = None

    def __repr__(self):
        """Return printable version of the object as json.

        Returns:
            str: Json string of the dict.
        """
        return json.dumps(self.__dict__)
