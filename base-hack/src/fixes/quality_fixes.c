#include "../../include/common.h"

#define JAPES_MAIN 7
#define MODE_DKTV 3

void qualityOfLife_fixes(void) {
	if (Rando.quality_of_life) {
		*(unsigned char*)(0x807132BF) = JAPES_MAIN;
		*(unsigned char*)(0x807132CB) = MODE_DKTV;
		if (Gamemode != 0) {
			StorySkip = 1;
		}
		setPermFlag(0x309); // Cranky FTT
		setPermFlag(0x17F); // Training Barrels Spawned
	}
}