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
static char good_eeprom = 0;
static char new_picture = 0;

void cFuncLoop(void) {
	DataIsCompressed[18] = 0;
	unlockKongs();
	int crystal_count = CollectableBase.Crystals;
	tagAnywhere(past_crystals);
	past_crystals = crystal_count;
	initHack(0);
	//fixCastleAutowalk();
	level_order_rando_funcs();
	qualityOfLife_fixes();
	qualityOfLife_shorteners();
	decouple_moves_fixes();
	replace_zones(0);
	alter_boss_key_flags();
	if (ObjectModel2Timer <= 2) {
		setFlag(0x78, 0, 2); // Clear K. Lumsy temp flag
		if (!Rando.tns_portal_rando_on) {
			shiftBrokenJapesPortal();
		}
		openCoinDoor();
		priceTransplant();
		if (CurrentMap == 0x50) {
			good_eeprom = EEPROMType == 2;
		} else if (CurrentMap == 0xE) {
			TextItemName = Rando.aztec_beetle_reward;
		} else if (CurrentMap == 0x52) {
			TextItemName = Rando.caves_beetle_reward;
		}
	}
	if (Rando.item_rando) {
		if (TransitionSpeed > 0) {
			if (LZFadeoutProgress == 30.0f) {
				CheckKasplatSpawnBitfield();
			}
		}
	}
	// displayNumberOnTns();
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
	fixDKFreeSoftlock();
	callParentMapFilter();
	recolorKongControl();
	spawnCannonWrapper();
	setCrusher();
	if (Rando.win_condition == GOAL_POKESNAP) {
		int picture_bitfield = 0;
		if (Player) {
			int control_state = Player->control_state;
			EnemyInView = 0;
			if ((control_state == 4) || (control_state == 5)) {
				EnemyInView = isSnapEnemyInRange();
			}
			if (Player->strong_kong_ostand_bitfield & 0x8000) {
				picture_bitfield = 1;
				if (!new_picture) {
					pokemonSnapMode();
				}
			}
		}
		new_picture = picture_bitfield;
	}
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
	handleSFXCache();
	if (Rando.fast_start_helm == 2) {
		if (TransitionSpeed > 0) {
			if ((DestMap == 0x11) && (CurrentMap == 0xAA)) {
				setPermFlag(FLAG_MODIFIER_HELMBOM);
			}
		}
	}
	handleDPadFunctionality();
	if (Rando.quality_of_life.fast_boot) {
		if (Gamemode == 3) {
			if (TransitionSpeed < 0) {
				TransitionType = 1;
			}
		}
	}
	if (Rando.helm_hurry_mode) {
		checkTotalCache();
	}
	// if (Rando.item_rando) {
	// 	controlKeyText();
	// }
	if (CurrentMap == 0x11) {
		if ((CutsceneActive == 1) && ((CutsceneStateBitfield & 4) != 0)) {
			if ((CutsceneIndex == 0) || (CutsceneIndex == 4) || (CutsceneIndex == 7) || (CutsceneIndex == 8) || (CutsceneIndex == 9)) {
				if (checkFlag(FLAG_MODIFIER_HELMBOM,0)) {
					setFlag(0x50,0,2); // Prevent Helm Door hardlock
				}
			}
		}
	} else if ((CurrentMap == 0xAA) && (ObjectModel2Timer < 5)) {
		if (checkFlag(FLAG_MODIFIER_HELMBOM,0)) {
			setFlag(0x50,0,2); // Prevent Helm Door hardlock
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
}

void earlyFrame(void) {
	if (ObjectModel2Timer == 2) {
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
		if (CurrentMap == 0x11) {
			HelmInit(1);
		}
		if (CurrentMap == 0x40) {
			// Adjust Giant Mushroom Void
			MapVoid_MinX = -259;
			MapVoid_MinZ = -227;
			MapVoid_MaxX = 1210;
			MapVoid_MaxZ = 1239;
		} else if (CurrentMap == 13) {
			// Adjust Painting Void
			MapVoid_MinX = -284;
			MapVoid_MinZ = -320;
			MapVoid_MaxX = 703;
			MapVoid_MaxZ = 757;
		}
		if ((Rando.helm_hurry_mode) && (QueueHelmTimer)) {
			if (HelmTimerShown == 0) {
				initHelmTimer();
			}
			QueueHelmTimer = 0;
		}
	}
	if (CurrentMap == 0x6F) { // Pufftoss
		if ((CutsceneActive) && (CutsceneIndex == 20) && (CutsceneTimer == 2)) { // Short Intro Cutscene
			if (Rando.music_rando_on) {
				MusicTrackChannels[0] = 0; // Disables boss intro music
			}
		}
	} else if (CurrentMap == 0x6E) { // Factory BBlast
		if (Rando.fast_gbs) {
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
	} else if (CurrentMap == 0x9A) {
		if ((CutsceneActive == 1) && ((CutsceneStateBitfield & 4) == 0)) {
			if ((CutsceneIndex == 8) || (CutsceneIndex == 2) || (CutsceneIndex == 16) || (CutsceneIndex == 18) || (CutsceneIndex == 17)) {
				// Falling off Mad Jack
				if (Player) {
					Player->control_state = 0xC;
					Player->hSpeed = 0;
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
	fastWarpShockwaveFix();
	catchWarpHandle();
	write_kutoutorder();
	remove_blockers();
	determine_krool_order();
	disable_krool_health_refills();
	CBDing();
	if (ObjectModel2Timer < 5) {
		auto_turn_keys();
	}
	if (Rando.item_rando) {
		int has_sniper = 0;
		int has_homing = 0;
		for (int i = 0; i < 5; i++) {
			int weap_val = MovesBase[i].weapon_bitfield;
			if (weap_val & 2) {
				has_homing = 1;
			}
			if (weap_val & 4) {
				has_sniper = 1;
			}
		}
		for (int i = 0; i < 5; i++) {
			if (has_homing) {
				MovesBase[i].weapon_bitfield |= 2;
			}
			if (has_sniper) {
				MovesBase[i].weapon_bitfield |= 4;
			}
		}
	}
	handle_WTI();
	adjust_galleon_water();
	finalizeBeatGame();
	for (int kong = 0; kong < 5; kong++) {
		for (int level = 0; level < 7; level++) {
			MovesBase[kong].cb_count[level] &= 0xFF;
			MovesBase[kong].tns_cb_count[level] &= 0xFF;
		}
	}
	if ((CurrentMap == MAIN_MENU) && (ObjectModel2Timer < 5)) {
		FileScreenDLCode_Write();
		initTracker();
	}
	if (CurrentMap == NFR_SCREEN) {
		if (ObjectModel2Timer == 5) {
			preventSongPlaying = 0;
		}
		int loaded = *(char*)(0x807F01A6);
		if ((loaded) || (ObjectModel2Timer > 800)) {
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
static char pkmnStr[10] = "";
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
static unsigned char ammo_hud_timer = 0;

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
			dl = drawScreenRect(dl, left, 475, right, 485, *(unsigned char*)(address + 0), *(unsigned char*)(address + 1), *(unsigned char*)(address + 2), *(unsigned char*)(address + 3));
			dl = drawPixelTextContainer(dl, wait_x_offsets[(int)wait_progress_master], 130, (char*)wait_texts[(int)wait_progress_master], 0xFF, 0xFF, 0xFF, 0xFF, 1);
			dl = drawPixelTextContainer(dl, 110, 150, "PLEASE WAIT", 0xFF, 0xFF, 0xFF, 0xFF, 1);
		} else if (CurrentMap == MAIN_MENU) {
			if (!good_eeprom) {
				dl = drawPixelTextContainer(dl, 0x52, 0x66, "BAD EEPROM SETTINGS.", 0xFF, 0xFF, 0xFF, 0xFF, 1);
				dl = drawPixelTextContainer(dl, 0x3E, 0x6F, "YOUR GAME WILL NOT SAVE.", 0xFF, 0, 0, 0xFF, 1);
				dl = drawPixelTextContainer(dl, 0x3E, 0x87, "CHECK THE SETUP GUIDE IN", 0xFF, 0xFF, 0xFF, 0xFF, 1);
				dl = drawPixelTextContainer(dl, 0x34, 0x92, "THE WIKI TO FIX THIS ERROR.", 0xFF, 0xFF, 0xFF, 0xFF, 1);
			}
		} else {
			if (Rando.item_rando) {
				dl = controlKeyText(dl);
			}
			if (Rando.fps_on) {
				float fps = HERTZ;
				if (current_avg_lag != 0) {
					fps = HERTZ / current_avg_lag;
				}
				int fps_int = fps;
				dk_strFormat((char *)fpsStr, "FPS %d", fps_int);
				dl = drawPixelTextContainer(dl, 250, 210, fpsStr, 0xFF, 0xFF, 0xFF, 0xFF, 1);
			}
			if (Rando.dpad_visual_enabled) {
				dl = drawDPad(dl);
			}
			if (ammo_hud_timer) {
				int ammo_x = 150;
				int ammo_default_y = 850;
				int ammo_y = ammo_default_y;
				float ammo_o = 255.0f;
				if (ammo_hud_timer > 40) {
					ammo_y = ammo_default_y + (5 * (ammo_hud_timer - 40));
					ammo_o = (50 - ammo_hud_timer) * 25.5f;
				} else if (ammo_hud_timer < 10) {
					ammo_y = ammo_default_y + (5 * (10 - ammo_hud_timer));
					ammo_o = ammo_hud_timer * 25.5f;
				}
				dl = drawImage(dl, IMAGE_AMMO_START + (1 ^ ForceStandardAmmo), RGBA16, 32, 32, ammo_x, ammo_y, 4.0f, 4.0f, (int)ammo_o);
				ammo_hud_timer -= 1;
			}
			if (HUD) {
				int hud_st = HUD->item[0xC].hud_state;
				if (hud_st) {
					if (hud_st == 1) {
						bp_numerator = 0;
						bp_denominator = 0;
						for (int i = 0; i < 8; i++) {
							int bp_has = checkFlagDuplicate(FLAG_BP_JAPES_DK_HAS + (i * 5) + Character,0);
							int bp_turn = checkFlagDuplicate(FLAG_BP_JAPES_DK_TURN + (i * 5) + Character,0);
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
			if (Rando.win_condition == GOAL_POKESNAP) {
				int pkmn_f = 0;
				int pkmn_n = 0;
				int pkmn_d = 0;
				if (getPkmnSnapData(&pkmn_f, &pkmn_n, &pkmn_d)) {
					dk_strFormat((char *)pkmnStr, "%dl%d", pkmn_n, pkmn_d);
					float opacity = 255.0f;
					if (pkmn_f < 12) {
						opacity = pkmn_f * 255;
						opacity /= 12;
					} else if (pkmn_f > 38) {
						int diff = 12 - (pkmn_f - 38);
						opacity = diff * 255;
						opacity /= 12;
					}
					if (opacity > 255) {
						opacity = 255;
					} else if (opacity < 0) {
						opacity = 0;
					}
					dl = drawText(dl, 1, 290, 370, pkmnStr, 0xFF, 0xFF, 0xFF, opacity);
				}
			}
		}
	}
	return dl;
}

void toggleStandardAmmo(void) {
	if (Gamemode == 6) {
		if (NewlyPressedControllerInput.Buttons & D_Down) {
			if (MovesBase[(int)Character].weapon_bitfield & 2) {
				if (CollectableBase.HomingAmmo > 0) {
					ForceStandardAmmo = 1 ^ ForceStandardAmmo;
					if (ammo_hud_timer == 0) {
						ammo_hud_timer = 50;
					}
				}
            }
		}
	}
}