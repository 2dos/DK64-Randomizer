"""Quality of life information."""


class QoLItem:
    """Quality of life multiselector information."""

    def __init__(self, name, shift, tooltip=""):
        """Initialize with given data."""
        self.name = name
        self.shift = shift
        self.tooltip = tooltip


QoLSelector = []
QoLItems = [
    QoLItem("Auto Dance Skip", 4, "Dances upon picking up some collectables, notably Golden Bananas, are removed (with some exceptions)."),
    QoLItem("Fast Boot", 5, "The boot sequence is dramatically sped up."),
    QoLItem("Calm Caves", 12, "Crystal Caves will no longer rain rocks down periodically."),
    QoLItem("Animal Buddies grab Items", 13, "Rambi and Enguarde will be able to pick up DK's and Lanky's Items respectively."),
    QoLItem("Reduced Lag", 0, "Lag is reduced where possible without hindering gameplay."),
    QoLItem("Remove Extraneous Cutscenes", 1, "A lot of cutscenes are removed, enabling a fast-paced game."),
    QoLItem("Hint Textbox Hold", 11, "Hint Textboxes will not close automatically upon the game reaching the end of the text, requiring B to be pressed."),
    QoLItem("Remove Wrinkly Puzzles", -1, "Removes the Wrinkly Puzzles from the Angry Aztec, Fungi Forest and Crystal Caves lobbies"),
    QoLItem("Fast Picture Taking", 2, "The picture taking sequence is heavily sped up, with lag being significantly reduced on BizHawk."),
    QoLItem("HUD Hotkey", 14, "Pressing D-Pad Up will show the total amount of colored bananas acquired in the level, as well as the blueprint count for that Kong."),
    QoLItem("Ammo Swap", 7, "Homing Ammo and Standard ammo can be swapped between (upon having Homing Ammo) by pressing D-Pad Down."),
    QoLItem("Homing Balloons", 15, "Homing Ammo homes in on Banana Balloons."),
    QoLItem("Fast Transform Animation", 6, "Transform barrels will not go through the morphing animation."),
    QoLItem("Troff n Scoff Audio Indicator", 8, "A bell ding will play upon collecting enough colored bananas to unlock the level's boss."),
    QoLItem("Lowered Aztec Lobby Bonus", 3, "The bonus barrel in Aztec Lobby is lowered to make it easier to reach."),
    QoLItem("Quicker Galleon Star", 9, "The star in Gloomy Galleon now only requires Enguarde to go through it once to open the Gold Tower Gate."),
    QoLItem("Vanilla Bug Fixes", 10, "Various bugs in the vanilla game have been fixed."),
]
for item in QoLItems:
    if item.name != "No Group":
        QoLSelector.append({"name": item.name, "value": item.name.lower().replace(" ", "_"), "tooltip": item.tooltip, "shift": item.shift})
