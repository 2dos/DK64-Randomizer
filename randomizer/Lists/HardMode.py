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
]
for item in HardItems:
    if item.name != "No Group":
        HardSelector.append({"name": item.name, "value": item.name.lower().replace(" ", "_"), "tooltip": item.tooltip, "shift": item.shift})
