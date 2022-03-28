#include "../../include/common.h"

/*
	actor_spawner->float_0x40 = 2;
*/

#define MODE_DKTV 3

void resolve_barrels(void) {
	if (ObjectModel2Timer < 5) {
		if (Gamemode != MODE_DKTV) {
			if (Rando.resolve_bonus) {
				actorSpawnerData* spawner = ActorSpawnerPointer;
				if (spawner) {
					int pass = 1;
					while (pass) {
						if ((spawner->actor_type == 0xC) && (Rando.resolve_bonus & 1)) {
							spawner->barrel_resolved = 2.0f;
						} else if ((spawner->actor_type == 91) && (Rando.resolve_bonus & 2)) {
							spawner->barrel_resolved = 2.0f;
						}

						if (spawner->next_spawner) {
							spawner = (actorSpawnerData*)(spawner->next_spawner);
						} else {
							pass = 0;
							break;
						}
					}
				}
			}
		}
	}
}