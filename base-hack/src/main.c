#include "../include/common.h"

#define MAIN_MENU 0x50
#define NINTENDO_LOGO 0x28
#define JAPES_MAIN 7

void cFuncLoop(void) {
	initHack();
	unlockKongs();
	tagAnywhere();
	islesSpawn();
	//fixCastleAutowalk();
	level_order_rando_funcs();
	qualityOfLife_fixes();
	qualityOfLife_shorteners();
	if (Rando.quality_of_life) {
		// DKTVKong = 0;
		// if (CurrentMap == NINTENDO_LOGO) {
		// 	if (TransitionSpeed > 0) {
		// 		CutsceneFadeActive = 0;
		// 		DestExit = 16;
		// 	}
		// }
		if (Gamemode == 3) {
			if (TransitionSpeed < 0) {
				TransitionType = 1;
			}
		}
	}
	if (CurrentMap == MAIN_MENU) {
		if (CutsceneActive == 6) {
			if (!checkFlag(0x346,0)) {
				unlockMoves();
				applyFastStart();
				openCrownDoor();
				openCoinDoor();
				setPermFlag(0x346);
			}
		}
	}
};