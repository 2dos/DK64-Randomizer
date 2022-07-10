#include "../../include/common.h"

#define JAPES_MAIN 7
#define MODE_DKTV 3

void qualityOfLife_fixes(void) {
	if (Rando.quality_of_life) {
		if (Gamemode == 0) {
			StorySkip = 1;
		}
		setPermFlag(0x309); // Cranky FTT
		setPermFlag(0x17F); // Training Barrels Spawned
		setPermFlag(300); // Giant Kosha Dead
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