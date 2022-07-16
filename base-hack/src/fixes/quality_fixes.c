#include "../../include/common.h"

#define JAPES_MAIN 7
#define MODE_DKTV 3

void qualityOfLife_fixes(void) {
	if (Rando.quality_of_life) {
		if (Gamemode == 0) {
			StorySkip = 1;
		}
		setPermFlag(FLAG_FTT_CRANKY); // Cranky FTT
		setPermFlag(FLAG_TBARREL_SPAWNED); // Training Barrels Spawned
		setPermFlag(FLAG_MODIFIER_KOSHADEAD); // Giant Kosha Dead
		fixkey8();
		if (CurrentMap == JAPES_MAIN) {
			if (Player) {
				if (Character == 6) { // Rambi
					if (Player->detransform_timer == 0) {
						Player->rambi_enabled = 1;
					}
				}
			}
		}
	}
}

void checkNinWarp(void) {
	if (Rando.quality_of_life) {
		WarpToDKTV();
		TransitionType = 0;
	} else {
		initiateTransitionFade(0x4C,0,2);
	}
}