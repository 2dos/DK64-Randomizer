#include "../../include/common.h"

void swapRequirements(int key_swap) {
	if (TransitionSpeed < 0) {
		for (int i = 0; i < 8; i++) {
			if (i < 7) {
				if (Rando.troff_scoff_count[i] > 0) {
					TroffNScoffReqArray[i] = Rando.troff_scoff_count[i];
				} else {
					TroffNScoffReqArray[i] = 1;
					CBTurnedInArray[i] = 1;
				}
			}
			if ((key_swap) && (i < 7)) {
				if (levelIndexMapping[CurrentMap] == LEVEL_ISLES) {
					// In Isles
					CheckmarkKeyArray[i] = Rando.key_flags[i];
				} else {
					CheckmarkKeyArray[i] = normal_key_flags[i];
				}
			}
			
		}
	}
}

void level_order_rando_funcs(void) {
	if (Rando.level_order_rando_on) {
		swapRequirements(1);
	} else {
		swapRequirements(0);
	}
}