"""Class for level data."""
import collections


class Randomizers:
    """Level progression information."""

    def __init__(self):
        """Set up Response named tuples."""
        self.response = collections.namedtuple("Response", ["Value", "ToolTip", "Enabled"])

    @staticmethod
    def _unindent(string):
        """Un indent tool tip data.

        Args:
            string (str): Tool Tip info.

        Returns:
            str: Un indented text.
        """
        return "".join(map(str.lstrip, string.splitlines(1)))

    def randomize_progression(self):
        """Response Data for form info."""
        tooltip = """This option will randomize the order the levels appear in.
            Specifically the level lobby entrances are randomized.
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
