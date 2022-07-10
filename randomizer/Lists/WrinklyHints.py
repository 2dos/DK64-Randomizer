"""Hint location data for Wrinkly hints."""
from randomizer.Enums.WrinklyKong import WrinklyKong, WrinklyLocation


class Hint:
    """Hint object for Wrinkly hint data locations."""

    def __init__(self, name, kong: WrinklyKong, location: WrinklyLocation, hint):
        """Create wrinkly hint object.

        Args:
            name (str): Location/String name of wrinkly.
            kong (WrinklyKong): What kong the hint is for.
            location (WrinklyLocation): What lobby the hint is in.
            hint (str): Hint to be written to ROM
        """
        self.name = name
        self.kong = kong
        self.location = location
        self.hint = hint


hints = [
    Hint("First Time Talk", WrinklyKong.ftt, WrinklyLocation.ftt, "WELCOME TO THE DONKEY KONG 64 RANDOMIZER. MADE BY 2DOS, BALLAAM, KILLKLLI, SHADOWSHINE, CFOX, BISMUTH AND ZNERNICUS"),
    Hint("Japes DK", WrinklyKong.dk, WrinklyLocation.japes, ""),
    Hint("Japes Diddy", WrinklyKong.diddy, WrinklyLocation.japes, ""),
    Hint("Japes Lanky", WrinklyKong.lanky, WrinklyLocation.japes, ""),
    Hint("Japes Tiny", WrinklyKong.tiny, WrinklyLocation.japes, ""),
    Hint("Japes Chunky", WrinklyKong.chunky, WrinklyLocation.japes, ""),
    Hint("Aztec DK", WrinklyKong.dk, WrinklyLocation.aztec, ""),
    Hint("Aztec Diddy", WrinklyKong.diddy, WrinklyLocation.aztec, ""),
    Hint("Aztec Lanky", WrinklyKong.lanky, WrinklyLocation.aztec, ""),
    Hint("Aztec Tiny", WrinklyKong.tiny, WrinklyLocation.aztec, ""),
    Hint("Aztec Chunky", WrinklyKong.chunky, WrinklyLocation.aztec, ""),
    Hint("Factory DK", WrinklyKong.dk, WrinklyLocation.factory, ""),
    Hint("Factory Diddy", WrinklyKong.diddy, WrinklyLocation.factory, ""),
    Hint("Factory Lanky", WrinklyKong.lanky, WrinklyLocation.factory, ""),
    Hint("Factory Tiny", WrinklyKong.tiny, WrinklyLocation.factory, ""),
    Hint("Factory Chunky", WrinklyKong.chunky, WrinklyLocation.factory, ""),
    Hint("Galleon DK", WrinklyKong.dk, WrinklyLocation.galleon, ""),
    Hint("Galleon Diddy", WrinklyKong.diddy, WrinklyLocation.galleon, ""),
    Hint("Galleon Lanky", WrinklyKong.lanky, WrinklyLocation.galleon, ""),
    Hint("Galleon Tiny", WrinklyKong.tiny, WrinklyLocation.galleon, ""),
    Hint("Galleon Chunky", WrinklyKong.chunky, WrinklyLocation.galleon, ""),
    Hint("Fungi DK", WrinklyKong.dk, WrinklyLocation.fungi, ""),
    Hint("Fungi Diddy", WrinklyKong.diddy, WrinklyLocation.fungi, ""),
    Hint("Fungi Lanky", WrinklyKong.lanky, WrinklyLocation.fungi, ""),
    Hint("Fungi Tiny", WrinklyKong.tiny, WrinklyLocation.fungi, ""),
    Hint("Fungi Chunky", WrinklyKong.chunky, WrinklyLocation.fungi, ""),
    Hint("Caves DK", WrinklyKong.dk, WrinklyLocation.caves, ""),
    Hint("Caves Diddy", WrinklyKong.diddy, WrinklyLocation.caves, ""),
    Hint("Caves Lanky", WrinklyKong.lanky, WrinklyLocation.caves, ""),
    Hint("Caves Tiny", WrinklyKong.tiny, WrinklyLocation.caves, ""),
    Hint("Caves Chunky", WrinklyKong.chunky, WrinklyLocation.caves, ""),
    Hint("Castle DK", WrinklyKong.dk, WrinklyLocation.castle, ""),
    Hint("Castle Diddy", WrinklyKong.diddy, WrinklyLocation.castle, ""),
    Hint("Castle Lanky", WrinklyKong.lanky, WrinklyLocation.castle, ""),
    Hint("Castle Tiny", WrinklyKong.tiny, WrinklyLocation.castle, ""),
    Hint("Castle Chunky", WrinklyKong.chunky, WrinklyLocation.castle, ""),
]
