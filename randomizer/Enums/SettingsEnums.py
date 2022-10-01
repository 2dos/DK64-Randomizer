"""Various Enums for the settings."""
from enum import IntEnum, auto


class KasplatShuffleType(IntEnum):
    """Kasplat shuffle enum for settings."""

    Vanilla = 0
    VanillaLocations = auto()
    LocationShuffle = auto()

    @staticmethod
    def SpoilerName(value):
        """Return text the spoiler log will use for the given enum value."""
        if value == KasplatShuffleType.LocationShuffle.value:
            return "Location Shuffle"
        elif value == KasplatShuffleType.VanillaLocations.value:
            return "Vanilla Locations"
        elif value == KasplatShuffleType.Vanilla.value:
            return "Vanilla"
        else:
            return "Unknown"


# Used to map the name of the settings on the UI to the corresponding Enum for applying presets correctly
settings_enum_dict = {
    "kasplat_rando_setting": KasplatShuffleType,
}
