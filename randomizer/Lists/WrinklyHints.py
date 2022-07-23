"""Hint location data for Wrinkly hints."""
from randomizer.Enums.WrinklyKong import WrinklyLocation
from randomizer.Enums.Kongs import Kongs


class HintLocation:
    """Hint object for Wrinkly hint data locations."""

    def __init__(self, name, kong: Kongs, location: WrinklyLocation, hint, banned_keywords = []):
        """Create wrinkly hint object.

        Args:
            name (str): Location/String name of wrinkly.
            kong (Kongs): What kong the hint is for.
            location (WrinklyLocation): What lobby the hint is in.
            hint (str): Hint to be written to ROM
        """
        self.name = name
        self.kong = kong
        self.location = location
        self.hint = hint
        self.banned_keywords = banned_keywords.copy()


hints = [
    HintLocation("First Time Talk", Kongs.any, WrinklyLocation.ftt, "WELCOME TO THE DONKEY KONG 64 RANDOMIZER. MADE BY 2DOS, BALLAAM, KILLKLLI, SHADOWSHINE, CFOX, BISMUTH AND ZNERNICUS"),
    HintLocation("Japes DK", Kongs.donkey, WrinklyLocation.japes, ""),
    HintLocation("Japes Diddy", Kongs.diddy, WrinklyLocation.japes, ""),
    HintLocation("Japes Lanky", Kongs.lanky, WrinklyLocation.japes, ""),
    HintLocation("Japes Tiny", Kongs.tiny, WrinklyLocation.japes, ""),
    HintLocation("Japes Chunky", Kongs.chunky, WrinklyLocation.japes, ""),
    HintLocation("Aztec DK", Kongs.donkey, WrinklyLocation.aztec, ""),
    HintLocation("Aztec Diddy", Kongs.diddy, WrinklyLocation.aztec, ""),
    HintLocation("Aztec Lanky", Kongs.lanky, WrinklyLocation.aztec, ""),
    HintLocation("Aztec Tiny", Kongs.tiny, WrinklyLocation.aztec, ""),
    HintLocation("Aztec Chunky", Kongs.chunky, WrinklyLocation.aztec, "", banned_keywords=["Hunky Chunky","Feather Bow"]),
    HintLocation("Factory DK", Kongs.donkey, WrinklyLocation.factory, ""),
    HintLocation("Factory Diddy", Kongs.diddy, WrinklyLocation.factory, "", banned_keywords=["Gorilla Grab"]),
    HintLocation("Factory Lanky", Kongs.lanky, WrinklyLocation.factory, "", banned_keywords=["Gorilla Grab"]),
    HintLocation("Factory Tiny", Kongs.tiny, WrinklyLocation.factory, "", banned_keywords=["Gorilla Grab"]),
    HintLocation("Factory Chunky", Kongs.chunky, WrinklyLocation.factory, ""),
    HintLocation("Galleon DK", Kongs.donkey, WrinklyLocation.galleon, ""),
    HintLocation("Galleon Diddy", Kongs.diddy, WrinklyLocation.galleon, ""),
    HintLocation("Galleon Lanky", Kongs.lanky, WrinklyLocation.galleon, ""),
    HintLocation("Galleon Tiny", Kongs.tiny, WrinklyLocation.galleon, ""),
    HintLocation("Galleon Chunky", Kongs.chunky, WrinklyLocation.galleon, ""),
    HintLocation("Fungi DK", Kongs.donkey, WrinklyLocation.fungi, "", banned_keywords=["Gorilla Grab"]),
    HintLocation("Fungi Diddy", Kongs.diddy, WrinklyLocation.fungi, "", banned_keywords=["Gorilla Grab"]),
    HintLocation("Fungi Lanky", Kongs.lanky, WrinklyLocation.fungi, "", banned_keywords=["Gorilla Grab"]),
    HintLocation("Fungi Tiny", Kongs.tiny, WrinklyLocation.fungi, "", banned_keywords=["Gorilla Grab"]),
    HintLocation("Fungi Chunky", Kongs.chunky, WrinklyLocation.fungi, ""),
    HintLocation("Caves DK", Kongs.donkey, WrinklyLocation.caves, "", banned_keywords=["Primate Punch"]),
    HintLocation("Caves Diddy", Kongs.diddy, WrinklyLocation.caves, "", banned_keywords=["Primate Punch", "Rocketbarrel Boost"]),
    HintLocation("Caves Lanky", Kongs.lanky, WrinklyLocation.caves, "", banned_keywords=["Primate Punch"]),
    HintLocation("Caves Tiny", Kongs.tiny, WrinklyLocation.caves, "", banned_keywords=["Primate Punch"]),
    HintLocation("Caves Chunky", Kongs.chunky, WrinklyLocation.caves, "", banned_keywords=["Primate Punch"]),
    HintLocation("Castle DK", Kongs.donkey, WrinklyLocation.castle, ""),
    HintLocation("Castle Diddy", Kongs.diddy, WrinklyLocation.castle, ""),
    HintLocation("Castle Lanky", Kongs.lanky, WrinklyLocation.castle, ""),
    HintLocation("Castle Tiny", Kongs.tiny, WrinklyLocation.castle, ""),
    HintLocation("Castle Chunky", Kongs.chunky, WrinklyLocation.castle, ""),
]
