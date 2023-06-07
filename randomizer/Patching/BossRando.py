"""Apply Boss Locations."""
from randomizer.Patching.Patcher import ROM
from randomizer.Spoiler import Spoiler


def randomize_bosses(spoiler: Spoiler):
    """Apply Boss locations based on boss_maps from spoiler."""
    varspaceOffset = spoiler.settings.rom_data
    bossMapOffset = 0x097
    # /* 0x097 */ char boss_kong[7]; // Array of kongs used to fight the boss, in order of vanilla level sequence. If no changes are made, supply the vanilla values
    # /* 0x09E */ unsigned char boss_map[7]; // Array of boss maps, in order of vanilla level sequence. If no changes are made, supply the vanilla values
    ROM().seek(varspaceOffset + bossMapOffset)
    ROM().writeBytes(bytearray(spoiler.settings.boss_kongs))
    ROM().writeBytes(bytearray(spoiler.settings.boss_maps))
    # /* 0x111 */ char kut_out_kong_order[5]; // Value of item: 0 = DK, 1 = Diddy, 2 = Lanky, 3 = Tiny, 4 = Chunky. Kongs can be repeated
    kutoutOffset = 0x120
    ROM().seek(varspaceOffset + kutoutOffset)
    ROM().writeBytes(bytearray(spoiler.settings.kutout_kongs))
