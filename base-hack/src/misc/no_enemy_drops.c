#include "../../include/common.h"

static const short banned_types[] = {
	0x2F, // Watermelon
	0x34, // Oranges
	0x33, // Ammo Crates
};

void no_enemy_drops(void) {
	int drop_object = 0;
	if (Rando.disable_drops) {
		for (int i = 0; i < 27; i++) {
			drop_object = EnemyDropsTable[i].dropped_object_type;
			int is_drop = 0;
			for (int j = 0; j < 3; j++) {
				if (banned_types[j] == drop_object) {
					is_drop = 1;
				}
			}
			if (is_drop) {
				EnemyDropsTable[i].source_object_type = 3; // Has to be non-zero to enable other drops. Attaching it to Diddy since he can't drop anything upon death
			}
		}
	}
}