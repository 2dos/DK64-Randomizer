"""Hard Mode information."""


class HardModeItem:
    """Hard Mode multiselector information."""

    def __init__(self, name, shift, tooltip=""):
        """Initialize with given data."""
        self.name = name
        self.shift = shift
        self.tooltip = tooltip


HardSelector = []
# If you make changes to this list, make sure to change the corresponding
# MiscChangesSelected enum in randomizer.Enums.Settings.
HardItems = [
    HardModeItem("Hard Bosses", -1, "Boss fights are slightly harder, including allowing extra kongs the ability to fight Mad Jack."),
    HardModeItem("Extra Hard Bosses", 2, "Boss fights are even harder, including raised pufftoss stars and a faster Mad Jack."),
    HardModeItem("Hard Enemies", 3, "Enemies fight back a little harder."),
    HardModeItem("Water is Lava", 1, "All water surfaces are lava water instead, damaging you."),
    HardModeItem("Reduced Fall Damage Threshold", 0, "The amount of distance required to fall too far has been reduced by 70%."),
    HardModeItem("Shuffled Jetpac Enemies", -1, "Jetpac enemies are shuffled within jetpac."),
    HardModeItem("Lower Max Refill Amounts", -1, "Refills will have lower caps."),
    HardModeItem("Strict Helm Timer", -1, "Helm Timer starts a base time of 0 minutes instead of 10."),
    HardModeItem(
        "Donk in the Dark World",
        -1,
        "All maps are pitch black, with only a light to help you path your way to the end of the game. Mixing this with 'Donk in the Sky' will convert the challenge into 'Memory Challenge' instead.",
    ),
    HardModeItem("Donk in the Sky", -1, "Collision Geometry is disabled. Mixing this with 'Donk in the Dark World' will convert the challenge into 'Memory Challenge' instead."),
]
for item in HardItems:
    if item.name != "No Group":
        HardSelector.append({"name": item.name, "value": item.name.lower().replace(" ", "_"), "tooltip": item.tooltip, "shift": item.shift})
