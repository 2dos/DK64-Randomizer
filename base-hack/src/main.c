#include "../include/common.h"

#define MAIN_MENU 0x50
#define NINTENDO_LOGO 0x28
#define JAPES_MAIN 7

#define LAG_CAP 10
static short past_lag[LAG_CAP] = {};
static char lag_counter = 0;
static float current_avg_lag = 0;

void cFuncLoop(void) {
	DataIsCompressed[18] = 0;
	initHack();
	unlockKongs();
	tagAnywhere();
	islesSpawn();
	//fixCastleAutowalk();
	level_order_rando_funcs();
	qualityOfLife_fixes();
	qualityOfLife_shorteners();
	decouple_moves_fixes();
	determine_krool_order();
	replace_zones(0);
	krool_order_indicator();
	alter_boss_key_flags();
	displayNumberOnTns();
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
	past_lag[(int)(lag_counter % LAG_CAP)] = StoredLag;
	lag_counter = (lag_counter + 1) % LAG_CAP;
	int lag_sum = 0;
	for (int i = 0; i < LAG_CAP; i++) {
		lag_sum += past_lag[i];
	}
	current_avg_lag = lag_sum;
	current_avg_lag /= LAG_CAP;
};

void earlyFrame(void) {
	decouple_moves_fixes();
	replace_moves();
	price_rando();
	write_kutoutorder();
	remove_blockers();
	resolve_barrels();
}

static char fpsStr[15] = "";
#define HERTZ 60
int* displayListModifiers(int* dl) {
	if (CurrentMap != NINTENDO_LOGO) {
		if (Rando.fps_on) {
			float fps = HERTZ;
			if (current_avg_lag != 0) {
				fps = HERTZ / current_avg_lag;
			}
			int fps_int = fps;
			dk_strFormat((char *)fpsStr, "FPS %d", fps_int);
			dl = drawPixelTextContainer(dl, 250, 210, fpsStr, 0xFF, 0xFF, 0xFF, 0xFF, 1);
		}
	}
	return dl;
};