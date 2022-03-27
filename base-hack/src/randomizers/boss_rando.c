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
static const unsigned char boss_maps[] = {
	8,
	197,
	154,
	111,
	83,
	196,
	199,
};
static const short normal_key_flags[] = {0x1A,0x4A,0x8A,0xA8,0xEC,0x124,0x13D};

void randomize_bosses(void) {
	for (int i = 0; i < 7; i++) {
		BossMapArray[i] = Rando.boss_map[i];
		BossKongArray[i] = Rando.boss_kong[i];
		levelIndexMapping[(int)Rando.boss_map[i]] = i;
	}
}

void alter_boss_key_flags(void) {
	if (TransitionSpeed < 0) {
		int in_boss_map = 0;
		for (int i = 0; i < 7; i++) {
			if (CurrentMap == boss_maps[i]) {
				in_boss_map = 1;
			}
		}
		if (in_boss_map) {
			for (int i = 0; i < 7; i++) {
				for (int j = 0; j < 7; j++) {
					if (Rando.boss_map[j] == boss_maps[i]) {
						*(short*)(key_flag_addresses[i]) = normal_key_flags[j];
					}
				}
			}
		}
	}
}