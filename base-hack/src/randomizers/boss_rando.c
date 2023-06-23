#include "../../include/common.h"

static short* key_flag_addresses[] = {
	(short*)0x800258FA,
	(short*)0x8002C136,
	(short*)0x80035676,
	(short*)0x8002A0C2,
	(short*)0x8002B3F6,
	(short*)0x80025C4E,
	(short*)0x800327EE,
};

void randomize_bosses(void) {
	for (int i = 0; i < 7; i++) {
		BossMapArray[i] = Rando.boss_map[i];
		BossKongArray[i] = Rando.boss_kong[i];
		levelIndexMapping[(int)Rando.boss_map[i]] = i;
	}
}

void alter_boss_key_flags(void) {
	if (TransitionSpeed < 0) {
		if (inBossMap(CurrentMap, 1, 0, 0)) {
			for (int i = 0; i < 7; i++) {
				for (int j = 0; j < 7; j++) {
					if (Rando.boss_map[j] == regular_boss_maps[i]) {
						*(short*)(key_flag_addresses[i]) = normal_key_flags[j];
					}
				}
			}
		}
	}
}