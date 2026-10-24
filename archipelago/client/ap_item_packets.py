"""AP item packet construction for the DK64 client.

Single source of truth for converting the items.py count_id schema into the
4-byte ap_item_packet that the C side reads (see base-hack/src/item rando/
archipelago.c::handleSentItem and item_handler.c::giveItem).
"""

from typing import Dict, Any, Optional, Tuple

# requirement_item enum values from common_enums.h
REQITEM_NONE = 0x00
REQITEM_KONG = 0x01
REQITEM_MOVE = 0x02
REQITEM_GOLDENBANANA = 0x03
REQITEM_BLUEPRINT = 0x04
REQITEM_FAIRY = 0x05
REQITEM_KEY = 0x06
REQITEM_CROWN = 0x07
REQITEM_COMPANYCOIN = 0x08
REQITEM_MEDAL = 0x09
REQITEM_BEAN = 0x0A
REQITEM_PEARL = 0x0B
REQITEM_RAINBOWCOIN = 0x0C
REQITEM_ICETRAP = 0x0D
REQITEM_GAMEPERCENTAGE = 0x0E
REQITEM_COLOREDBANANA = 0x0F
REQITEM_BOSSES = 0x10
REQITEM_BONUSES = 0x11
REQITEM_JUNK = 0x12
REQITEM_HINT = 0x13
REQITEM_SHOPKEEPER = 0x14
REQITEM_AP = 0x15
REQITEM_RACECOIN = 0x16

# giveItemConfig bitfield values
CONFIG_DISPLAY_ITEM_TEXT = 0x01
CONFIG_APPLY_HELM_HURRY = 0x02
CONFIG_GIVE_COINS = 0x04
CONFIG_APPLY_ICE_TRAP = 0x08
CONFIG_FORCE_DISPLAY_ITEM_TEXT = 0x10

# Ice trap type to kong parameter mapping (used as trap type in REQITEM_ICETRAP)
ICE_TRAP_TYPES = {
    "bubble": 1,
    "reverse": 2,
    "slow": 3,
    # 4 is unused (Super Bubble)
    "disable_a": 5,
    "disable_b": 6,
    "disable_z": 7,
    "disable_c_up": 8,
    "get_out": 9,
    "dry": 10,
    "flip": 11,
    "icefloor": 12,
    "paper": 13,
    # 14 is unused (Non-Instant Slip)
    "slip": 15,
    "animal": 16,
    "rockfall": 17,
    "disabletag": 18,
}


class APItemPacket:
    """4-byte packet matching the C-side ap_item_packet struct."""

    def __init__(self, item_type: int, level: int = 0, kong: int = 0, config_flags: int = 0):
        """Initialize an AP item packet.

        Args:
            item_type: requirement_item enum value
            level: Level/tier parameter for giveItem
            kong: Kong index or other context parameter (e.g. ice trap type)
            config_flags: Packed giveItemConfig bitfield
        """
        self.item_type = item_type
        self.level = level
        self.kong = kong
        self.config_flags = config_flags

    def to_u32(self) -> int:
        """Pack the packet into a big-endian 32-bit word for write_u32."""
        return (self.item_type << 24) | (self.level << 16) | (self.kong << 8) | self.config_flags


# REQITEM_MOVE (level, kong) parameters keyed by count_id["item"] from items.py.
#
# Levels match the C handler in item_handler.c::giveItem REQITEM_MOVE switch:
#   0..2 = special move bit (kong-specific)
#   3    = slam upgrade (giveSlamLevel)
#   4    = gun (kong-specific weapon bit)
#   5    = homing ammo (all kongs)
#   6    = sniper sight (all kongs)
#   7    = ammo belt (all kongs)
#   8    = instrument (kong-specific)
#   9    = progressive instrument upgrade (all kongs)
#
ITEM_ID_TO_MOVE_PARAMS: Dict[int, Tuple[int, int]] = {
    # Slam upgrade
    2: (3, 0),
    # DK special moves
    26: (0, 0),  # Baboon Blast
    27: (1, 0),  # Strong Kong
    28: (2, 0),  # Gorilla Grab
    # Diddy special moves
    29: (0, 1),  # Chimpy Charge
    30: (1, 1),  # Rocketbarrel Boost
    31: (2, 1),  # Simian Spring
    # Lanky special moves
    32: (0, 2),  # Orangstand
    33: (1, 2),  # Baboon Balloon
    34: (2, 2),  # Orangstand Sprint
    # Tiny special moves
    35: (0, 3),  # Mini Monkey
    36: (1, 3),  # Pony Tail Twirl
    37: (2, 3),  # Monkeyport
    # Chunky special moves
    38: (0, 4),  # Hunky Chunky
    39: (1, 4),  # Primate Punch
    40: (2, 4),  # Gorilla Gone
    # Instruments
    41: (8, 0),  # Bongos
    42: (8, 1),  # Guitar
    43: (8, 2),  # Trombone
    44: (8, 3),  # Saxophone
    45: (8, 4),  # Triangle
    # Guns
    46: (4, 0),  # Coconut
    47: (4, 1),  # Peanut
    48: (4, 2),  # Grape
    49: (4, 3),  # Feather
    50: (4, 4),  # Pineapple
    # Shared upgrades
    52: (5, 0),  # Homing Ammo
    53: (6, 0),  # Sniper Sight
    54: (7, 0),  # Ammo Belt
    55: (9, 0),  # Instrument Upgrade
}


def build_packet(count_data: Dict[str, Any]) -> Optional[APItemPacket]:
    """Build an APItemPacket from a count_id dict.

    Returns None for items that should not use the packet system (those are
    written directly to CountStruct by the caller).
    """
    if not isinstance(count_data, dict):
        return None

    # Ice traps: kong field carries the trap type
    if "ice_trap_type" in count_data:
        trap_kong = ICE_TRAP_TYPES.get(count_data["ice_trap_type"], 1)
        return APItemPacket(REQITEM_ICETRAP, 0, trap_kong, CONFIG_APPLY_ICE_TRAP)

    # Rainbow coins: special config flag triggers coin spawn
    if count_data.get("field") == "rainbow_coins":
        return APItemPacket(REQITEM_RAINBOWCOIN, 0, 0, CONFIG_APPLY_HELM_HURRY | CONFIG_GIVE_COINS)

    item = count_data.get("item")
    if item is None:
        return None

    # Golden Banana
    if item == 1:
        return APItemPacket(REQITEM_GOLDENBANANA, 0, 0, CONFIG_APPLY_HELM_HURRY)

    # Moves/upgrades indexed by item_id (with level field present)
    if "level" in count_data and item in ITEM_ID_TO_MOVE_PARAMS:
        level, kong = ITEM_ID_TO_MOVE_PARAMS[item]
        return APItemPacket(REQITEM_MOVE, level, kong, CONFIG_APPLY_HELM_HURRY)

    # Raw requirement_item enum (item field with no level) — defensive fallback
    if "level" not in count_data:
        return APItemPacket(item, 0, 0, CONFIG_APPLY_HELM_HURRY)

    return None
