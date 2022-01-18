#include "../../include/common.h"

void randomize_bosses(void) {
	for (int i = 0; i < 7; i++) {
		BossMapArray[i] = Rando.boss_map[i];
		BossKongArray[i] = Rando.boss_kong[i];
	}
}