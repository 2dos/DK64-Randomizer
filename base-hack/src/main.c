#include "../include/common.h"

#define MAIN_MENU 0x50
#define NINTENDO_LOGO 0x28
#define JAPES_MAIN 7
#define ADVENTURE_MODE 6
#define SNIDES_BONUS_GAMES 13
#define NFR_SCREEN 0x51

#define LAG_CAP 10
static short past_lag[LAG_CAP] = {};
static char lag_counter = 0;
static float current_avg_lag = 0;
static short past_crystals = 0;
static char has_loaded = 0;

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
	initHack(0);
	//fixCastleAutowalk();
	level_order_rando_funcs();
	qualityOfLife_fixes();
	qualityOfLife_shorteners();
	decouple_moves_fixes();
	replace_zones(0);
	alter_boss_key_flags();
	if (ObjectModel2Timer <= 2) {
		shiftBrokenJapesPortal();
		openCoinDoor();
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
				setPermFlag(FLAG_MODIFIER_HELMBOM);
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
			if (!checkFlag(FLAG_WATERFALL,0)) {
				// New File
				unlockMoves();
				applyFastStart();
				openCrownDoor();
				giveCollectables();
				setPermFlag(FLAG_WATERFALL);
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
		setFlag(FLAG_KROOL_INTRO_DK,1,2); // DK Phase Intro
		setFlag(FLAG_KROOL_INTRO_TINY,1,2); // Tiny Phase Intro
		if (CurrentMap == 0x22) {
			KRoolRound = 0;
			for (int i = 0; i < 4; i++) {
				setFlag(FLAG_KROOL_TOE_1 + i,0,2); // Clear Toes
			}
		}
		int boat_speed = 5000 << (CurrentMap == 0x6F);
		for (int i = 0; i < 2; i++) {
			BoatSpeeds[i] = boat_speed;
		}
		PauseText = 0;
		if (isLobby(CurrentMap)) {
			PauseText = 1;
		} else if ((CurrentMap == 1) || (CurrentMap == 5) || (CurrentMap == 0x19)) {
			PauseText = 1;
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
	} else if (CurrentMap == 0x6E) { // Factory BBlast
		if (Rando.skip_arcade_round1) {
			if (!checkFlag(FLAG_ARCADE_LEVER,0)) {
				if (checkFlag(FLAG_ARCADE_ROUND1,0)) {
					if (TransitionSpeed > 0) {
						if (DestMap == 0x1A) {
							delayedObjectModel2Change(0x1A,45,10);
						}
						setPermFlag(FLAG_ARCADE_LEVER);
					}
				}
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
	if (Rando.auto_keys) {
		auto_turn_keys();
	}
	handle_WTI();
	adjust_galleon_water();
	if ((CurrentMap == MAIN_MENU) && (ObjectModel2Timer < 5)) {
		FileScreenDLCode_Write();
	}
	if (CurrentMap == NFR_SCREEN) {
		if (ObjectModel2Timer == 5) {
			preventSongPlaying = 0;
		}
		int loaded = *(char*)(0x807F01A6);
		if ((loaded) || (FrameLag > 800)) {
			if (has_loaded == 0) {
				initiateTransitionFade(0x50, 0, 5);
				has_loaded = 1;
			}
		}
	}
}

static char fpsStr[15] = "";
static char bp_numerator = 0;
static char bp_denominator = 0;
static char bpStr[10] = "";
static char hud_timer = 0;
static char wait_progress_master = 0;
static char wait_progress_timer = 0;

static const char* wait_texts[] = {
	"BOOTING UP THE RANDOMIZER",
	"REMOVING LANKY KONG",
	"TELLING 2DOS TO PLAY DK64",
	"LOCKING K. LUMSY IN A CAGE",
	"STEALING THE BANANA HOARD"
};
static const char wait_x_offsets[] = {55, 85, 55, 53, 55};

#define HERTZ 60
#define ACTOR_MAINMENUCONTROLLER 0x146


#define LOADBAR_START 350
#define LOADBAR_FINISH 900
#define LOADBAR_MAXWIDTH 200
#define LOADBAR_DIVISOR 35
int* displayListModifiers(int* dl) {
	if (CurrentMap != NINTENDO_LOGO) {
		if (CurrentMap == NFR_SCREEN) {
			wait_progress_timer += 1;
			if (wait_progress_timer > LOADBAR_DIVISOR) {
				wait_progress_timer = 0;
				wait_progress_master += 1;
				if (wait_progress_master > 4) {
					wait_progress_master = 0;
				}
			}
			int address = 0x8075054C + (4 * wait_progress_master);
			float left_f = (((LOADBAR_FINISH - LOADBAR_START) + LOADBAR_MAXWIDTH) / LOADBAR_DIVISOR) * wait_progress_timer;
			left_f += LOADBAR_START;
			left_f -= LOADBAR_MAXWIDTH;
			int left = left_f;
			int right = left + LOADBAR_MAXWIDTH;
			if (left < LOADBAR_START) {
				left = LOADBAR_START;
			}
			if (left > LOADBAR_FINISH) {
				left = LOADBAR_FINISH;
			}
			if (right > LOADBAR_FINISH) {
				right = LOADBAR_FINISH;
			}
			if (right < LOADBAR_START) {
				right = LOADBAR_START;
			}
			*(int*)(0x807FF700) = left;
			*(int*)(0x807FF704) = right;
			dl = drawScreenRect(dl, left, 475, right, 485, *(unsigned char*)(address + 0), *(unsigned char*)(address + 1), *(unsigned char*)(address + 2), *(unsigned char*)(address + 3));
			dl = drawPixelTextContainer(dl, wait_x_offsets[(int)wait_progress_master], 130, (char*)wait_texts[(int)wait_progress_master], 0xFF, 0xFF, 0xFF, 0xFF, 1);
			dl = drawPixelTextContainer(dl, 110, 150, "PLEASE WAIT", 0xFF, 0xFF, 0xFF, 0xFF, 1);
		} else {
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
							int bp_has = checkFlag(FLAG_BP_JAPES_DK_HAS + (i * 5) + Character,0);
							int bp_turn = checkFlag(FLAG_BP_JAPES_DK_TURN + (i * 5) + Character,0);
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
	}
	return dl;
};