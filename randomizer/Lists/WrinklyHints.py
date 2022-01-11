"""Hint location data for Wrinkly hints."""
from randomizer.Enums.WrinklyKong import WrinklyKong, WrinklyLocation


class Hint:
    """Hint object for Wrinkly hint data locations."""

    def __init__(self, name, kong: WrinklyKong, length: int, location: WrinklyLocation, address: int):
        """Create wrinkly hint object.

        Args:
            name (str): Location/String name of wrinkly.
            kong (WrinklyKong): What kong the hint is for.
            length (int): Length of characters we can/have to write.
            location (WrinklyLocation): What lobby the hint is in.
            address (int): The in ROM location of the hint.
        """
        self.name = name
        self.kong = kong
        self.length = length
        self.location = location
        self.address = address


hints = [
    Hint("First Time Talk", WrinklyKong.ftt, 455, WrinklyLocation.ftt, 0x23F),
    Hint("Japes DK", WrinklyKong.dk, 81, WrinklyLocation.japes, 0x3B9),
    Hint("Japes Diddy", WrinklyKong.diddy, 87, WrinklyLocation.japes, 0x40C),
    Hint("Japes Lanky", WrinklyKong.lanky, 95, WrinklyLocation.japes, 0x464),
    Hint("Japes Tiny", WrinklyKong.tiny, 79, WrinklyLocation.japes, 0x4C3),
    Hint("Japes Chunky", WrinklyKong.chunky, 69, WrinklyLocation.japes, 0x512),
    Hint("Aztec DK", WrinklyKong.dk, 59, WrinklyLocation.aztec, 0x557),
    Hint("Aztec Diddy", WrinklyKong.diddy, 71, WrinklyLocation.aztec, 0x591),
    Hint("Aztec Lanky", WrinklyKong.lanky, 66, WrinklyLocation.aztec, 0x5D6),
    Hint("Aztec Tiny", WrinklyKong.tiny, 70, WrinklyLocation.aztec, 0x614),
    Hint("Aztec Chunky", WrinklyKong.chunky, 81, WrinklyLocation.aztec, 0x657),
    Hint("Factory DK", WrinklyKong.dk, 79, WrinklyLocation.factory, 0x6A4),
    Hint("Factory Diddy", WrinklyKong.diddy, 77, WrinklyLocation.factory, 0x6F3),
    Hint("Factory Lanky", WrinklyKong.lanky, 68, WrinklyLocation.factory, 0x740),
    Hint("Factory Tiny", WrinklyKong.tiny, 53, WrinklyLocation.factory, 0x781),
    Hint("Factory Chunky", WrinklyKong.chunky, 67, WrinklyLocation.factory, 0x7B1),
    Hint("Galleon DK", WrinklyKong.dk, 72, WrinklyLocation.galleon, 0x7EF),
    Hint("Galleon Diddy", WrinklyKong.diddy, 68, WrinklyLocation.galleon, 0x836),
    Hint("Galleon Lanky", WrinklyKong.lanky, 81, WrinklyLocation.galleon, 0x87A),
    Hint("Galleon Tiny", WrinklyKong.tiny, 80, WrinklyLocation.galleon, 0x8BB),
    Hint("Galleon Chunky", WrinklyKong.chunky, 65, WrinklyLocation.galleon, 0x907),
    Hint("Fungi DK", WrinklyKong.dk, 44, WrinklyLocation.fungi, 0x947),
    Hint("Fungi Diddy", WrinklyKong.diddy, 64, WrinklyLocation.fungi, 0x973),
    Hint("Fungi Lanky", WrinklyKong.lanky, 86, WrinklyLocation.fungi, 0x9B3),
    Hint("Fungi Tiny", WrinklyKong.tiny, 63, WrinklyLocation.fungi, 0xA11),
    Hint("Fungi Chunky", WrinklyKong.chunky, 106, WrinklyLocation.fungi, 0xA4B),
    Hint("Caves DK", WrinklyKong.dk, 51, WrinklyLocation.caves, 0xA84),
    Hint("Caves Diddy", WrinklyKong.diddy, 67, WrinklyLocation.caves, 0xAB7),
    Hint("Caves Lanky", WrinklyKong.lanky, 77, WrinklyLocation.caves, 0xAF7),
    Hint("Caves Tiny", WrinklyKong.tiny, 97, WrinklyLocation.caves, 0xB40),
    Hint("Caves Chunky", WrinklyKong.chunky, 57, WrinklyLocation.caves, 0xB8C),
    Hint("Castle DK", WrinklyKong.dk, 132, WrinklyLocation.castle, 0xBC0),
    Hint("Castle Diddy", WrinklyKong.diddy, 61, WrinklyLocation.castle, 0xC1D),
    Hint("Castle Lanky", WrinklyKong.lanky, 100, WrinklyLocation.castle, 0xC56),
    Hint("Castle Tiny", WrinklyKong.tiny, 75, WrinklyLocation.castle, 0xC9A),
    Hint("Castle Chunky", WrinklyKong.chunky, 66, WrinklyLocation.castle, 0xCD8),
]
