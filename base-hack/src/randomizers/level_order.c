#include "../../include/common.h"

void swapRequirements(int key_swap) {
	if (TransitionSpeed < 0) {
		for (int i = 0; i < 7; i++) {
			if (key_swap) {
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