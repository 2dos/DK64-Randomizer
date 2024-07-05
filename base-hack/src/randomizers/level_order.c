#include "../../include/common.h"

void swapRequirements() {
	if (TransitionSpeed < 0) {
		for (int i = 0; i < 7; i++) {
			CheckmarkKeyArray[i] = normal_key_flags[i];
		}
	}
}

void level_order_rando_funcs(void) {
	if (Rando.level_order_rando_on) {
		swapRequirements();
	}
}