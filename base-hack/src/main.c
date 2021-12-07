#include "../include/common.h"

#define MAIN_MENU 0x50
#define NINTENDO_LOGO 0x28

void cFuncLoop(void) {
	initHack();
	unlockKongs();
	tagAnywhere();
	islesSpawn();
	fixCastleAutowalk();
	level_order_rando_funcs();
	qualityOfLife_fixes();
	qualityOfLife_shorteners();
	if (CurrentMap == NINTENDO_LOGO) {
		if (TransitionSpeed > 0) {
			CutsceneFadeActive = 0;
			DestExit = 16;
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