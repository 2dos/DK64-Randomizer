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
static short past_crystals = 0;

void giveCollectables(void) {
	int mult = 1;
	if (MovesBase[0].ammo_belt > 0) {
		mult = 2 * MovesBase[0].ammo_belt;
	}
	CollectableBase.StandardAmmo = 25 * mult;
	CollectableBase.Oranges = 10;
	CollectableBase.Crystals = 1500;
	CollectableBase.Film = 5;
}

void cFuncLoop(void) {
	DataIsCompressed[18] = 0;
	unlockKongs();
	int crystal_count = CollectableBase.Crystals;
	tagAnywhere(past_crystals);
	past_crystals = crystal_count;
	islesSpawn();
	initHack();
	//fixCastleAutowalk();
	level_order_rando_funcs();
	qualityOfLife_fixes();
	qualityOfLife_shorteners();
	decouple_moves_fixes();
	replace_zones(0);
	alter_boss_key_flags();
	if (ObjectModel2Timer <= 2) {
		shiftBrokenJapesPortal();
	}
	displayNumberOnTns();
	if (Rando.music_rando_on) {
		if (CurrentMap == 0x28) {
			if (ObjectModel2Timer == 5) {
				preventSongPlaying = 0;
			}
		}
	}
	if (CurrentMap == 0x50) {
		colorMenuSky();
	}
	cancelMoveSoftlock();
	fixDKFreeSoftlock();
	callParentMapFilter();
	recolorKongControl();
	spawnCannonWrapper();
	setCrusher();
	if (Rando.perma_lose_kongs) {
		preventBossCheese();
		kong_has_died();
		forceBossKong();
	} else {
		if (CurrentMap == 0xC7) {
			if (TransitionSpeed > 0.0f) {
				if (LZFadeoutProgress == 30.0f) {
					for (int i = 0; i < 7; i++) {
						if (BossMapArray[i] == 0xC7) {
							Character = BossKongArray[i];
						}
					}
				}
			}
		}
	}
	changeHelmLZ();
	if (Rando.fast_start_helm == 2) {
		if (TransitionSpeed > 0) {
			if ((DestMap == 0x11) && (CurrentMap == 0xAA)) {
				setPermFlag(770);
			}
		}
	}
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
				giveCollectables();
				setPermFlag(0x346);
				Character = Rando.starting_kong;
				StoredSettings.file_extra[(int)FileIndex].location_sss_purchased = 0;
				StoredSettings.file_extra[(int)FileIndex].location_ab1_purchased = 0;
				StoredSettings.file_extra[(int)FileIndex].location_ug1_purchased = 0;
				StoredSettings.file_extra[(int)FileIndex].location_mln_purchased = 0;
				SaveToGlobal();
			} else {
				// Used File
				Character = Rando.starting_kong;
				determineStartKong_PermaLossMode();
				giveCollectables();
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
	if (ObjectModel2Timer == 2) {
		updateProgressive();
		price_rando();
		setFlag(0x5D,1,2); // DK Phase Intro
		setFlag(0x58,1,2); // Tiny Phase Intro
		if (CurrentMap == 0x22) {
			KRoolRound = 0;
			for (int i = 0; i < 4; i++) {
				setFlag(0x51 + i,0,2); // Clear Toes
			}
		}
	}
	if (CurrentMap == 1) {
		if ((CutsceneActive) && (CutsceneIndex == 2)) {
			CutsceneBarState = 20;
		}
	}
	if ((CurrentMap == 5) || (CurrentMap == 1) || (CurrentMap == 0x19)) {
		if ((CutsceneActive) && (CutsceneIndex == 2)) {
			updateProgressive();
		}
	}
	if (CurrentMap == 0x6F) { // Pufftoss
		if ((CutsceneActive) && (CutsceneIndex == 20) && (CutsceneTimer == 2)) { // Short Intro Cutscene
			if (Rando.music_rando_on) {
				MusicTrackChannels[0] = 0; // Disables boss intro music
			}
		}
	}
	// Cutscene DK Code
	if ((CurrentMap == 0x28) || (CurrentMap == 0x4C)) {
		*(int*)(0x8074C3B0) = 0x806C1640;
	} else {
		*(int*)(0x8074C3B0) = (int)&cutsceneDKCode;
	}
	write_kutoutorder();
	remove_blockers();
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
static char bp_numerator = 0;
static char bp_denominator = 0;
static char bpStr[10] = "";
static char hud_timer = 0;
#define HERTZ 60
#define ACTOR_MAINMENUCONTROLLER 0x146
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
		if (HUD) {
			int hud_st = HUD->item[0xC].hud_state;
			if (hud_st) {
				if (hud_st == 1) {
					bp_numerator = 0;
					bp_denominator = 0;
					for (int i = 0; i < 8; i++) {
						int bp_has = checkFlag(469 + (i * 5) + Character,0);
						int bp_turn = checkFlag(509 + (i * 5) + Character,0);
						if ((bp_has) && (!bp_turn)) {
							bp_numerator += 1;
						}
						if (!bp_turn) {
							bp_denominator += 1;
						}
					}
					hud_timer += 1;
				} else if (hud_st == 3) {
					hud_timer -= 1;
					if (hud_timer < 0) {
						hud_timer = 0;
					}
				}
				dk_strFormat((char *)bpStr, "%dl%d", bp_numerator, bp_denominator);
				float opacity = 255 * hud_timer;
				opacity /= 12;
				dl = drawText(dl, 1, 355.0f, 480.f + ((12 - hud_timer) * 4), bpStr, 0xFF, 0xFF, 0xFF, opacity);
			} else {
				hud_timer = 0;
			}
		}
	}
	return dl;
};