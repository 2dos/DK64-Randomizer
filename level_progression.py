"""Class for level data."""
import collections


class LevelProgression:
    """Level progression information."""

    def __init__(self):
        """Set up Response named tuples."""
        self.response = collections.namedtuple("Response", ["Value", "ToolTip", "Enabled"])

    def _unindent(self, string):
        """Un indent tool tip data.

        Args:
            string (str): Tool Tip info.

        Returns:
            str: Un indented text.
        """
        return "".join(map(str.lstrip, string.splitlines(1)))

    def randomize_progression(self):
        """Response Data for form info."""
        tooltip = """This option will randomize the level lobby entrances.
            The level will match the B Locker and Troff n Scoff requirements of the slot that it falls in.
            Hideout Helm will always be the final level."""
        return self.response(Value=True, ToolTip=self._unindent(tooltip), Enabled="")

    def generate_seed_tooltip(self):
        """Response Data for form info."""
        tooltip = """You can either manually enter a 6 digit number or click the button to the right to pick one for you.
            This program will generate the game based off the number entered."""
        return self._unindent(tooltip)

    def generate_seed_button_tooltip(self):
        """Response Data for form info."""
        tooltip = """Click this button to randomly generate a 6 digit number to base the seed on."""
        return self._unindent(tooltip)

    def return_key(self, option):
        """Return first key from dict.

        Args:
            option (dict): The dict to parse.

        Returns:
            object: The key name found first.
        """
        return list(option.keys())[0]

    def return_value(self, option):
        """Return first value from dict.

        Args:
            option (dict): The dict to parse.

        Returns:
            object: The first value to return.
        """
        return option[list(option.keys())[0]]

    def blocker_presets(self):
        """Response Data for form info."""
        tooltip = """Select the B Locker progression of the game generated.
            Vanilla: 1-5-15-30-50-65-80-100
            Steady: 1-10-20-30-40-50-60-75
            Half: 1-5-10-15-20-30-40-50
            Hell: 1-10-25-50-75-100-125-150"""
        input_tooltip = self._unindent(
            """You can adjust each individual B Locker amount to any number between 0-200.
            Note that you could make it impossible to beat the game glitchless if certain levels are set too high,
            as the program does not validate if a game is beatable glitchless with adjusted B Locker settings.
            If you are unsure what to adjust the level values to, use the presets dropdown instead.
        """
        )
        options = {
            "Vanilla": [
                self.response(Value=1, ToolTip=input_tooltip, Enabled=""),
                self.response(Value=5, ToolTip=input_tooltip, Enabled=""),
                self.response(Value=15, ToolTip=input_tooltip, Enabled=""),
                self.response(Value=30, ToolTip=input_tooltip, Enabled=""),
                self.response(Value=50, ToolTip=input_tooltip, Enabled=""),
                self.response(Value=65, ToolTip=input_tooltip, Enabled=""),
                self.response(Value=80, ToolTip=input_tooltip, Enabled=""),
                self.response(Value=100, ToolTip=input_tooltip, Enabled=""),
            ],
            "Steady": [
                self.response(Value=1, ToolTip=input_tooltip, Enabled=""),
                self.response(Value=10, ToolTip=input_tooltip, Enabled=""),
                self.response(Value=20, ToolTip=input_tooltip, Enabled=""),
                self.response(Value=30, ToolTip=input_tooltip, Enabled=""),
                self.response(Value=40, ToolTip=input_tooltip, Enabled=""),
                self.response(Value=50, ToolTip=input_tooltip, Enabled=""),
                self.response(Value=60, ToolTip=input_tooltip, Enabled=""),
                self.response(Value=75, ToolTip=input_tooltip, Enabled=""),
            ],
            "Half": [
                self.response(Value=1, ToolTip=input_tooltip, Enabled=""),
                self.response(Value=5, ToolTip=input_tooltip, Enabled=""),
                self.response(Value=10, ToolTip=input_tooltip, Enabled=""),
                self.response(Value=15, ToolTip=input_tooltip, Enabled=""),
                self.response(Value=20, ToolTip=input_tooltip, Enabled=""),
                self.response(Value=30, ToolTip=input_tooltip, Enabled=""),
                self.response(Value=40, ToolTip=input_tooltip, Enabled=""),
                self.response(Value=50, ToolTip=input_tooltip, Enabled=""),
            ],
            "Hell": [
                self.response(Value=1, ToolTip=input_tooltip, Enabled=""),
                self.response(Value=10, ToolTip=input_tooltip, Enabled=""),
                self.response(Value=25, ToolTip=input_tooltip, Enabled=""),
                self.response(Value=50, ToolTip=input_tooltip, Enabled=""),
                self.response(Value=75, ToolTip=input_tooltip, Enabled=""),
                self.response(Value=100, ToolTip=input_tooltip, Enabled=""),
                self.response(Value=125, ToolTip=input_tooltip, Enabled=""),
                self.response(Value=150, ToolTip=input_tooltip, Enabled=""),
            ],
        }

        return self.response(Value=options, ToolTip=self._unindent(tooltip), Enabled="")

    def troff_presets(self):
        """Response Data for form info."""
        tooltip = """Select the Troff n Scoff progression of the game generated.
            Vanilla: 60-120-200-250-300-350-400
            Steady: All doors set to 150
            Half: 50-75-100-125-150-175-200
            Hell: 150-200-250-300-350-400-450"""
        input_tooltip = self._unindent(
            """You can adjust each individual Troff n Scoff amount to any number between 1-500.
            Note that you could make it impossible to beat the game glitchless if early levels are set too high,
            as the program does not validate if a game is beatable glitchless with adjusted Troff n Scoff settings.
            If you are unsure what to adjust the level values to, use the presets dropdown instead."""
        )
        options = {
            "Vanilla": [
                self.response(Value=60, ToolTip=input_tooltip, Enabled=""),
                self.response(Value=120, ToolTip=input_tooltip, Enabled=""),
                self.response(Value=200, ToolTip=input_tooltip, Enabled=""),
                self.response(Value=250, ToolTip=input_tooltip, Enabled=""),
                self.response(Value=300, ToolTip=input_tooltip, Enabled=""),
                self.response(Value=350, ToolTip=input_tooltip, Enabled=""),
                self.response(Value=400, ToolTip=input_tooltip, Enabled=""),
            ],
            "Steady": [
                self.response(Value=150, ToolTip=input_tooltip, Enabled=""),
                self.response(Value=150, ToolTip=input_tooltip, Enabled=""),
                self.response(Value=150, ToolTip=input_tooltip, Enabled=""),
                self.response(Value=150, ToolTip=input_tooltip, Enabled=""),
                self.response(Value=150, ToolTip=input_tooltip, Enabled=""),
                self.response(Value=150, ToolTip=input_tooltip, Enabled=""),
                self.response(Value=150, ToolTip=input_tooltip, Enabled=""),
            ],
            "Half": [
                self.response(Value=50, ToolTip=input_tooltip, Enabled=""),
                self.response(Value=75, ToolTip=input_tooltip, Enabled=""),
                self.response(Value=100, ToolTip=input_tooltip, Enabled=""),
                self.response(Value=125, ToolTip=input_tooltip, Enabled=""),
                self.response(Value=150, ToolTip=input_tooltip, Enabled=""),
                self.response(Value=175, ToolTip=input_tooltip, Enabled=""),
                self.response(Value=200, ToolTip=input_tooltip, Enabled=""),
            ],
            "Hell": [
                self.response(Value=150, ToolTip=input_tooltip, Enabled=""),
                self.response(Value=200, ToolTip=input_tooltip, Enabled=""),
                self.response(Value=250, ToolTip=input_tooltip, Enabled=""),
                self.response(Value=300, ToolTip=input_tooltip, Enabled=""),
                self.response(Value=350, ToolTip=input_tooltip, Enabled=""),
                self.response(Value=400, ToolTip=input_tooltip, Enabled=""),
                self.response(Value=450, ToolTip=input_tooltip, Enabled=""),
            ],
        }

        return self.response(Value=options, ToolTip=self._unindent(tooltip), Enabled="")
