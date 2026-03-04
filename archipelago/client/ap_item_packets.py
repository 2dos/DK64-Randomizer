"""AP Item Packet mappings - converts items to giveItem parameters."""

from typing import Dict, Any, Optional

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

# Config flag bitfield values
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
    """Represents an AP item packet for sending to the C code."""

    def __init__(self, item_type: int, level: int = 0, kong: int = 0, config_flags: int = 0):
        """Initialize an AP item packet.
        
        Args:
            item_type: requirement_item enum value
            level: Level/tier parameter for giveItem
            kong: Kong index or other context parameter
            config_flags: Packed giveItemConfig bitfield
        """
        self.item_type = item_type
        self.level = level
        self.kong = kong
        self.config_flags = config_flags

    def to_bytes(self) -> bytes:
        """Convert the packet to 4 bytes for writing to memory (little-endian)."""
        return bytes([self.item_type, self.level, self.kong, self.config_flags])

    def to_u32(self) -> int:
        """Convert the packet to a 32-bit integer for writing to memory."""
        return (self.item_type << 24) | (self.level << 16) | (self.kong << 8) | self.config_flags


def get_item_packet(count_data: Dict[str, Any]) -> Optional[APItemPacket]:
    """Convert count_data to an APItemPacket.
    
    This function maps the count_id data structure to the generic packet format
    that the C code expects.
    
    Args:
        count_data: The count_id dictionary from item_ids
        
    Returns:
        APItemPacket or None if this item should not use the fed system
    """
    if not isinstance(count_data, dict):
        return None

    # Default config: display=0, helm_hurry=1 (most items)
    config = CONFIG_APPLY_HELM_HURRY

    # Check for ice trap
    if "ice_trap_type" in count_data:
        trap_type = count_data.get("ice_trap_type", "bubble")
        trap_kong = ICE_TRAP_TYPES.get(trap_type, 1)  # Default to bubble
        return APItemPacket(
            item_type=REQITEM_ICETRAP,
            level=0,
            kong=trap_kong,
            config_flags=CONFIG_APPLY_ICE_TRAP  # Ice traps should have ice trap flag
        )

    # Handle items with specific item/level structure (moves, slams, etc.)
    if "item" in count_data and "level" in count_data:
        item_id = count_data.get("item")
        level = count_data.get("level")
        kong = count_data.get("kong", 0)  # Some moves have kong parameter
        
        # These items are typically moves that come via AP fed system
        # The item_id here is actually a move index that we need to map
        # For now, items with item/level structure should continue using CountStruct
        # as they are already handled properly there
        return None
    
    # Items with just "item" field
    if "item" in count_data and "level" not in count_data:
        # These should also stay in CountStruct
        return None

    # Default: items without these structures should use CountStruct
    return None


# Legacy fed_id mappings for reference (these will be replaced by packet data)
# This dict maps old fed_id values to their packet equivalents
LEGACY_FED_ID_TO_PACKET = {
    # Golden Banana
    0x000: APItemPacket(REQITEM_GOLDENBANANA, 0, 0, CONFIG_APPLY_HELM_HURRY),
    
    # Rainbow Coin
    0x001: APItemPacket(REQITEM_RAINBOWCOIN, 0, 0, CONFIG_APPLY_HELM_HURRY | CONFIG_GIVE_COINS),
    
    # Special Moves (Baboon Blast through Gorilla Gone)
    # DK (0-2)
    0x019: APItemPacket(REQITEM_MOVE, 0, 0, CONFIG_APPLY_HELM_HURRY),  # Baboon Blast
    0x01A: APItemPacket(REQITEM_MOVE, 1, 0, CONFIG_APPLY_HELM_HURRY),  # Strong Kong
    0x01B: APItemPacket(REQITEM_MOVE, 2, 0, CONFIG_APPLY_HELM_HURRY),  # Gorilla Grab
    # Diddy (3-5)
    0x01C: APItemPacket(REQITEM_MOVE, 0, 1, CONFIG_APPLY_HELM_HURRY),  # Chimpy Charge
    0x01D: APItemPacket(REQITEM_MOVE, 1, 1, CONFIG_APPLY_HELM_HURRY),  # Rocketbarrel Boost
    0x01E: APItemPacket(REQITEM_MOVE, 2, 1, CONFIG_APPLY_HELM_HURRY),  # Simian Spring
    # Lanky (6-8)
    0x01F: APItemPacket(REQITEM_MOVE, 0, 2, CONFIG_APPLY_HELM_HURRY),  # Orangstand
    0x020: APItemPacket(REQITEM_MOVE, 1, 2, CONFIG_APPLY_HELM_HURRY),  # Baboon Balloon
    0x021: APItemPacket(REQITEM_MOVE, 2, 2, CONFIG_APPLY_HELM_HURRY),  # Orangstand Sprint
    # Tiny (9-11)
    0x022: APItemPacket(REQITEM_MOVE, 0, 3, CONFIG_APPLY_HELM_HURRY),  # Mini Monkey
    0x023: APItemPacket(REQITEM_MOVE, 1, 3, CONFIG_APPLY_HELM_HURRY),  # Pony Tail Twirl
    0x024: APItemPacket(REQITEM_MOVE, 2, 3, CONFIG_APPLY_HELM_HURRY),  # Monkeyport
    # Chunky (12-14)
    0x025: APItemPacket(REQITEM_MOVE, 0, 4, CONFIG_APPLY_HELM_HURRY),  # Hunky Chunky
    0x026: APItemPacket(REQITEM_MOVE, 1, 4, CONFIG_APPLY_HELM_HURRY),  # Primate Punch
    0x027: APItemPacket(REQITEM_MOVE, 2, 4, CONFIG_APPLY_HELM_HURRY),  # Gorilla Gone
    
    # Instruments (level 8)
    0x028: APItemPacket(REQITEM_MOVE, 8, 0, CONFIG_APPLY_HELM_HURRY),  # Bongos
    0x029: APItemPacket(REQITEM_MOVE, 8, 1, CONFIG_APPLY_HELM_HURRY),  # Guitar
    0x02A: APItemPacket(REQITEM_MOVE, 8, 2, CONFIG_APPLY_HELM_HURRY),  # Trombone
    0x02B: APItemPacket(REQITEM_MOVE, 8, 3, CONFIG_APPLY_HELM_HURRY),  # Sax
    0x02C: APItemPacket(REQITEM_MOVE, 8, 4, CONFIG_APPLY_HELM_HURRY),  # Triangle
    
    # Guns (level 4)
    0x02D: APItemPacket(REQITEM_MOVE, 4, 0, CONFIG_APPLY_HELM_HURRY),  # Coconut
    0x02E: APItemPacket(REQITEM_MOVE, 4, 1, CONFIG_APPLY_HELM_HURRY),  # Peanut
    0x02F: APItemPacket(REQITEM_MOVE, 4, 2, CONFIG_APPLY_HELM_HURRY),  # Grape
    0x030: APItemPacket(REQITEM_MOVE, 4, 3, CONFIG_APPLY_HELM_HURRY),  # Feather
    0x031: APItemPacket(REQITEM_MOVE, 4, 4, CONFIG_APPLY_HELM_HURRY),  # Pineapple
    
    # Shared upgrades
    0x032: APItemPacket(REQITEM_MOVE, 5, 0, CONFIG_APPLY_HELM_HURRY),  # Homing Ammo
    0x033: APItemPacket(REQITEM_MOVE, 10, 0, CONFIG_APPLY_HELM_HURRY),  # Slam (level 10 = slam upgrade)
    0x034: APItemPacket(REQITEM_MOVE, 6, 0, CONFIG_APPLY_HELM_HURRY),  # Sniper Sight
    0x035: APItemPacket(REQITEM_MOVE, 7, 0, CONFIG_APPLY_HELM_HURRY),  # Ammo Belt
    0x036: APItemPacket(REQITEM_MOVE, 9, 0, CONFIG_APPLY_HELM_HURRY),  # Instrument Upgrade
}


def get_packet_from_fed_id(fed_id: int) -> Optional[APItemPacket]:
    """Get an AP packet from a legacy fed_id value.
    
    This is for backward compatibility during the transition.
    
    Args:
        fed_id: The old archipelago_items enum value
        
    Returns:
        APItemPacket or None if not found
    """
    return LEGACY_FED_ID_TO_PACKET.get(fed_id)
