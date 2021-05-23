"""Data for the misc tab."""
import collections


class Misc:
    """Contains flags for the misc tab."""

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

    def unlock_all_kongs(self):
        """Response Data for form info."""
        tooltip = """This option will make all 5 kongs available from the start without freeing them.
            The golden bananas awarded when freeing specific kongs still must be collected even with this option on.
            If using Level Progression Randomizer and playing through glitchless, this option is forced on."""
        return self.response(Value=True, ToolTip=self._unindent(tooltip), Enabled="disabled")

    def generate_spoilerlog(self):
        """Response Data for form info."""
        tooltip = """This option enables spoiler log files to be created on randomizer generation."""
        return self.response(Value=True, ToolTip=self._unindent(tooltip), Enabled="")

    def unlock_all_moves(self):
        """Response Data for form info."""
        tooltip = """This option will make all moves available from the start without purchasing them.
            Includes all Cranky, all Candy, and almost all Funky purchasables.
            Does not include access to JetPac in Cranky; you will still need 15 banana medals.
            Does not include snipe scope to reduce 1st person camera lag. Is still purchasable.
            Does not include the shockwave attack from the banana fairy queen."""
        return self.response(Value=False, ToolTip=self._unindent(tooltip), Enabled="")

    def unlock_fairy_shockwave(self):
        """Response Data for form info."""
        tooltip = """This option makes the fairy camera and shockwave attack available from the start.
            Normally obtainable by visiting the Banana Fairy Queen with Tiny as Mini Monkey."""
        return self.response(Value=False, ToolTip=self._unindent(tooltip), Enabled="")

    def enable_tag_anywhere(self):
        """Response Data for form info."""
        tooltip = """This option will allow you to switch kongs almost anywhere using DPad left or DPad right.
            You will still need to unlock the kong you want if Unlock All Kongs isn't enabled.
            You cannot switch kongs in rooms or areas that would otherwise break the puzzle."""
        return self.response(Value=False, ToolTip=self._unindent(tooltip), Enabled="")

    def fast_start_beginning_of_game(self):
        """Response Data for form info."""
        tooltip = """Training Barrels complete, start with Simian Slam, spawn in DK Isles, Japes lobby entrance open."""
        return self.response(Value=True, ToolTip=self._unindent(tooltip), Enabled="")

    def fast_start_hideout_helm(self):
        """Response Data for form info."""
        tooltip = """This option will shorten the time it takes to beat Hideout Helm with the following changes:
            - You will spawn in the Blast o Matic room.
            - Opens the roman numeral doors to each Kong's room.
            - The gates in front of the music pads are gone."""
        return self.response(Value=True, ToolTip=self._unindent(tooltip), Enabled="")

    def crown_door_open(self):
        """Response Data for form info."""
        tooltip = """You do not need to collect 4 crowns to collect Key 8."""
        return self.response(Value=True, ToolTip=self._unindent(tooltip), Enabled="")

    def coin_door_open(self):
        """Response Data for form info."""
        tooltip = """You do not need to collect the Nintendo and Rareware coin to collect Key 8."""
        return self.response(Value=True, ToolTip=self._unindent(tooltip), Enabled="")

    def quality_of_life(self):
        """Response Data for form info."""
        tooltip = """This option enables the following quality of life changes to the game:
            - Removes first time text.
            - Removes first time boss cutscenes.
            - Remove cutscenes from the startup sequence.
            - Story Skip option in the main menu set to On by default."""
        return self.response(Value=True, ToolTip=self._unindent(tooltip), Enabled="")
