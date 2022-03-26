#include "../include/common.h"

#define MAIN_MENU 0x50
#define NINTENDO_LOGO 0x28
#define JAPES_MAIN 7
#define ADVENTURE_MODE 6
#define SNIDES_BONUS_GAMES 13

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
	replace_zones(0);
	krool_order_indicator();
	alter_boss_key_flags();
	if (ObjectModel2Timer <= 2) {
		shiftBrokenJapesPortal();
	}
	displayNumberOnTns();
	cancelMoveSoftlock();
	callParentMapFilter();
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
				// New File
				unlockMoves();
				applyFastStart();
				openCrownDoor();
				openCoinDoor();
				setPermFlag(0x346);
				StoredSettings.file_extra[(int)FileIndex].location_sss_purchased = 0;
				SaveToGlobal();
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
	if ((Gamemode == ADVENTURE_MODE) || (Gamemode == SNIDES_BONUS_GAMES)) {
		BalancedIGT += 1;
	}
};

void earlyFrame(void) {
	decouple_moves_fixes();
	replace_moves();
	price_rando();
	write_kutoutorder();
	remove_blockers();
	resolve_barrels();
	determine_krool_order();
	disable_krool_health_refills();
	pre_turn_keys();
	handle_WTI();
	adjust_galleon_water();
	if ((CurrentMap == MAIN_MENU) && (ObjectModel2Timer < 5)) {
		FileScreenDLCode_Write();
	}
}

static char fpsStr[15] = "";
#define HERTZ 60
#define ACTOR_MAINMENUCONTROLLER 0x146
static unsigned char hash_textures[] = {48,49,50,51,55,62,63,64,65,76};
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
	if (CurrentMap == MAIN_MENU) {
		int j = 0;
		while (j < LoadedActorCount) {
			if (LoadedActorArray[j].actor) {
				if (LoadedActorArray[j].actor->actorType == ACTOR_MAINMENUCONTROLLER) {
					int screen = *(char*)((int)(LoadedActorArray[j].actor) + 0x18A);
					//int next_screen = *(char*)((int)(LoadedActorArray[i].actor) + 0x18B);
					if ((screen <= 5) && (screen != 3)) {
						dl = drawTextContainer(dl, 1, 25, 500, "SEED HASH", 0xFF, 0xFF, 0xFF, 0xFF, 0);
						for (int i = 0; i < 5; i++) {
							int hash_index = Rando.hash[i] % 10;
							dl = drawImage(dl, hash_textures[hash_index], RGBA16, 32, 32, 125 + (100 * i), 850, 3.0f, 3.0f, 0xFF);
						}
					}
					break;
				}
			}
			j++;
		}
	}
	return dl;
};