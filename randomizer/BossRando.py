"""Apply Boss Locations."""
from randomizer.Patcher import ROM
from randomizer.Spoiler import Spoiler

def randomize_bosses(spoiler: Spoiler):
    """Apply Boss locations based on boss_maps from spoiler."""
    varspaceOffset = 0x1FED020  # TODO: Define this as constant in a more global place
    bossMapOffset = 0x097
    # /* 0x097 */ char boss_kong[7]; // Array of kongs used to fight the boss, in order of vanilla level sequence. If no changes are made, supply the vanilla values
    # /* 0x09E */ unsigned char boss_map[7]; // Array of boss maps, in order of vanilla level sequence. If no changes are made, supply the vanilla values
    ROM().seek(varspaceOffset + bossMapOffset)
    ROM().writeBytes(bytearray(spoiler.settings.boss_kongs))
    ROM().writeBytes(bytearray(spoiler.settings.boss_maps))
