"""Apply Boss Locations."""

from randomizer.Patching.Patcher import LocalROM


def randomize_bosses(spoiler):
    """Apply Boss locations based on boss_maps from spoiler."""
    varspaceOffset = spoiler.settings.rom_data
    ROM_COPY = LocalROM()
    # /* 0x111 */ char kut_out_kong_order[5]; // Value of item: 0 = DK, 1 = Diddy, 2 = Lanky, 3 = Tiny, 4 = Chunky. Kongs can be repeated
    kutoutOffset = 0x120
    ROM_COPY.seek(varspaceOffset + kutoutOffset)
    ROM_COPY.writeBytes(bytearray(spoiler.settings.kutout_kongs))
