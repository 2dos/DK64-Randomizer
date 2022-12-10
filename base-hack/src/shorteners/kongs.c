#include "../../include/common.h"

void unlockKongs(void) {
	if (Rando.unlock_kongs) {
		for (int i = 0; i < 5; i++) {
			if (Rando.unlock_kongs & (1 << i)) {
				if (i == 0) {
					setPermFlag(FLAG_KONG_DK);
				} else {
					setPermFlag(KongFlagArray[i - 1]);
				}
			}
		}
	}
}

void initKongRando(void) {
	changeCharSpawnerFlag(0x14, 2, 93); // Tie llama spawn to lanky help me cutscene flag
	changeCharSpawnerFlag(0x7, 1, getKongFlag(Rando.free_target_japes));
	changeCharSpawnerFlag(0x10, 0x13, getKongFlag(Rando.free_target_ttemple));
	changeCharSpawnerFlag(0x14, 1, getKongFlag(Rando.free_target_llama));
	changeCharSpawnerFlag(0x1A, 1, getKongFlag(Rando.free_target_factory));
	alterGBKong(0x22, 0x4, Rando.starting_kong); // First GB
	alterGBKong(0x7, 0x69, Rando.free_source_japes); // Front of Diddy Cage GB
	alterGBKong(0x7, 0x48, Rando.free_source_japes); // In Diddy's Cage
	alterGBKong(0x10, 0x5B, Rando.free_source_ttemple); // In Tiny's Cage
	alterGBKong(0x14, 0x6C, Rando.free_source_llama); // Free Lanky GB
	alterGBKong(0x1A, 0x78, Rando.free_source_factory); // Free Chunky GB
}