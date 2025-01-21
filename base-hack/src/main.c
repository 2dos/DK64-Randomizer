#include "../include/common.h"

#define ADVENTURE_MODE 6
#define SNIDES_BONUS_GAMES 13

#define LAG_CAP 10
static short past_lag[LAG_CAP] = {};
static unsigned char instrument_cs_indexes[] = {0, 4, 7, 8, 9};
static char lag_counter = 0;
static float current_avg_lag = 0;
static char has_loaded = 0;
static char new_picture = 0;
int hint_pointers[35] = {};
char* itemloc_pointers[LOCATION_ITEM_COUNT] = {};
char grab_lock_timer = -1;
char tag_locked = 0;

int resetPictureStatus(void) {
	int value = *(unsigned char*)(0x807F946E);
	if ((Player->strong_kong_ostand_bitfield & 0x8000)) {
		return value;
	}
	actorData *picture = Player->vehicle_actor_pointer;
	if (picture) {
		if (picture->actorType == 0xCA) {
			return value;
		}
	}
	Player->fairy_state = 0;
	return value;
}

void cFuncLoop(void) {
	regularFrameLoop();
	cc_effect_handler();
	tagAnywhere();
	level_order_rando_funcs();
	qualityOfLife_fixes();
	qualityOfLife_shorteners();
	overlay_changes();
	replace_zones(0);
	if (ObjectModel2Timer <= 2) {
		setFlag(0x78, 0, FLAGTYPE_TEMPORARY); // Clear K. Lumsy temp flag
		setFlag(0x79, 0, FLAGTYPE_TEMPORARY); // Clear BFI Reward Cutscene temp flag
		if ((!Rando.tns_portal_rando_on) && (Rando.tns_indicator)) {
			shiftBrokenJapesPortal();
		}
		openCoinDoor();
		priceTransplant();
		if (CurrentMap == MAP_AZTECBEETLE) {
			TextItemName = Rando.aztec_beetle_reward;
		} else if (CurrentMap == MAP_CAVESBEETLERACE) {
			TextItemName = Rando.caves_beetle_reward;
		}
		if (isKrushaAdjacentModel(3)) {
			if (CurrentMap == MAP_KROOLSHOE) {
				setActorDamage(43, 1);
			} else {
				setActorDamage(43, 3);
			}
		}
		if (Rando.quality_of_life.vanilla_fixes) {
			if ((CurrentMap >= MAP_KROOLDK) && (CurrentMap <= MAP_KROOLCHUNKY)) {
				int kong_target = CurrentMap - MAP_KROOLDK;
				if (!checkFlagDuplicate(kong_flags[kong_target], FLAGTYPE_PERMANENT)) {
					exitBoss();
					Character = Rando.starting_kong;
				}
			}
		}
		handleKRoolSaveProgress();
		populateEnemyMapData();
	} else {
		setEnemyDBPopulation(0);
	}
	handleCannonGameReticle();
	if (grab_lock_timer >= 0) {
		grab_lock_timer += 1;
		if (grab_lock_timer > 10) {
			grab_lock_timer = -1;
		}
	}
	tag_locked = 0;
	if (Rando.cutscene_skip_setting == CSSKIP_PRESS) {
		clearSkipCache();
	}
	updateSkipCheck();
	if (TransitionSpeed > 0) {
		if (LZFadeoutProgress == 30.0f) {
			storeHintRegion();
		}
	}
	if (Rando.item_rando) {
		if (TransitionSpeed > 0) {
			if (LZFadeoutProgress == 30.0f) {
				CheckKasplatSpawnBitfield();
			}
		}
		callIceTrap();
	}
	// displayNumberOnTns();
	if (Rando.music_rando_on) {
		if (CurrentMap == MAP_NINTENDOLOGO) {
			if (ObjectModel2Timer == 5) {
				preventSongPlaying = 0;
			}
		}
	}
	if (isGamemode(GAMEMODE_ADVENTURE, 1)) {
		if ((CurrentMap == MAP_HELM_INTROSTORY) || (CurrentMap == MAP_ISLES_INTROSTORYROCK) || ((CurrentMap == MAP_ISLES_DKTHEATRE) && (CutsceneIndex < 8))) { // Intro Story Map
			if ((CutsceneActive) && (TransitionSpeed == 0.0f)) { // Playing a cutscene that's part of intro story
				if ((NewlyPressedControllerInput.Buttons.a) || (NewlyPressedControllerInput.Buttons.start)) {
					setIntroStoryPlaying(0);
					initiateTransition(MAP_TRAININGGROUNDS, 1);
				}
			}
		}
	}
	callParentMapFilter();
	spawnCannonWrapper();
	setCrusher();
	handleFallDamageImmunity();
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
		fixGraceCheese();
		forceBossKong();
	} else {
		if (CurrentMap == MAP_CASTLEKUTOUT) {
			if (TransitionSpeed > 0.0f) {
				if (LZFadeoutProgress == 30.0f) {
					for (int i = 0; i < 7; i++) {
						if (BossMapArray[i] == MAP_CASTLEKUTOUT) {
							Character = BossKongArray[i];
						}
					}
				}
			}
		}
	}
	handleSFXCache();
	detectSongChange();
	handleDPadFunctionality();
	if (Rando.helm_hurry_mode) {
		checkTotalCache();
	}
	// if (Rando.item_rando) {
	// 	controlKeyText();
	// }
	if (CurrentMap == MAP_HELM) {
		if ((CutsceneActive == 1) && ((CutsceneStateBitfield & 4) != 0)) {
			if (inU8List(CutsceneIndex, &instrument_cs_indexes[0], 5)) {
				if (checkFlag(FLAG_MODIFIER_HELMBOM,FLAGTYPE_PERMANENT)) {
					setFlag(0x50,0,FLAGTYPE_TEMPORARY); // Prevent Helm Door hardlock
				}
			}
		}
	} else if ((CurrentMap == MAP_HELMLOBBY) && (ObjectModel2Timer < 5)) {
		if (checkFlag(FLAG_MODIFIER_HELMBOM,FLAGTYPE_PERMANENT)) {
			setFlag(0x50,0,FLAGTYPE_TEMPORARY); // Prevent Helm Door hardlock
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

static unsigned char mj_falling_cutscenes[] = {
	8, 2, 16, 18, 17
};

void earlyFrame(void) {
	if (ObjectModel2Timer < 2) {
		setFlag(0x6A, 1, FLAGTYPE_TEMPORARY);
		swap_ending_cutscene_model();
		swapKremlingModel();
		force_enable_diving_timer = 0;
	} else if (ObjectModel2Timer == 2) {
		setFlag(FLAG_KROOL_INTRO_DK,1,FLAGTYPE_TEMPORARY); // DK Phase Intro
		setFlag(FLAG_KROOL_INTRO_TINY,1,FLAGTYPE_TEMPORARY); // Tiny Phase Intro
		if (CurrentMap == MAP_ISLES) {
			KRoolRound = 0;
			for (int i = 0; i < 4; i++) {
				setFlag(FLAG_KROOL_TOE_1 + i,0,FLAGTYPE_TEMPORARY); // Clear Toes
			}
		}
		int boat_speed = 5000 << (CurrentMap == MAP_GALLEONPUFFTOSS);
		for (int i = 0; i < 2; i++) {
			BoatSpeeds[i] = boat_speed;
		}
		PauseText = 0;
		if (isLobby(CurrentMap)) {
			PauseText = 1;
		} else if (inShop(CurrentMap, 0)) {
			PauseText = 1;
		}
		if (CurrentMap == MAP_HELM) {
			HelmInit(1);
		}
		if (CurrentMap == MAP_FUNGIGIANTMUSHROOM) {
			// Adjust Giant Mushroom Void
			MapVoid_MinX = -259;
			MapVoid_MinZ = -227;
			MapVoid_MaxX = 1210;
			MapVoid_MaxZ = 1239;
		} else if (CurrentMap == MAP_JAPESPAINTING) {
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
		if (Rando.pppanic_fairy_model) {
			int fairy_model = 0x3D;
			if ((CurrentMap == MAP_ISLES_DKTHEATRE) || (CurrentMap == MAP_TRAININGGROUNDS_ENDSEQUENCE)) {
				fairy_model = Rando.pppanic_fairy_model;
			}
			*(short*)(0x8075575C) = fairy_model;
		}
	}
	if ((CurrentMap == MAP_KROOLCHUNKY) && (CutsceneIndex == 14) && (CutsceneActive == 1)) {
		PauseText = 1;
	}
	if (CurrentMap == MAP_GALLEONPUFFTOSS) { // Pufftoss
		if ((CutsceneActive) && (CutsceneIndex == 20) && (CutsceneTimer == 2)) { // Short Intro Cutscene
			if (Rando.music_rando_on) {
				MusicTrackChannels[0] = 0; // Disables boss intro music
			}
		}
	} else if (CurrentMap == MAP_FACTORYJACK) {
		if ((CutsceneActive == 1) && ((CutsceneStateBitfield & 4) == 0)) {
			if (inU8List(CutsceneIndex, &mj_falling_cutscenes, sizeof(mj_falling_cutscenes))) {
				// Falling off Mad Jack
				if (Player) {
					Player->control_state = 0xC;
					Player->hSpeed = 0;
				}
			}
		}
	}
	// Cutscene DK Code
	if ((CurrentMap == MAP_NINTENDOLOGO) || (CurrentMap == MAP_DKRAP)) {
		actor_functions[196] = (void*)0x806C1640;
	} else {
		actor_functions[196] = &cutsceneDKCode;
	}
	if (isGamemode(GAMEMODE_ADVENTURE, 1)) {
		handleProgressiveIndicator(1);
	}
	fastWarpShockwaveFix();
	catchWarpHandle();
	CBDing();
	if (ObjectModel2Timer < 5) {
		auto_turn_keys();
		wipeHintCache();
		if (CurrentMap == MAP_MAINMENU) {
			FileScreenDLCode_Write();
			initTracker();
			if (Player) {
				// Remove DK's shadow in the main menu
				Player->unk_16E = 0;
			}
		}
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
	adjust_level_modifiers();
	finalizeBeatGame();
	for (int kong = 0; kong < 5; kong++) {
		for (int level = 0; level < 7; level++) {
			MovesBase[kong].cb_count[level] &= 0xFF;
			MovesBase[kong].tns_cb_count[level] &= 0xFF;
		}
	}
	if (CurrentMap == MAP_NFRTITLESCREEN) {
		if (ObjectModel2Timer == 5) {
			preventSongPlaying = 0;
		}
		int loaded = *(char*)(0x807F01A6);
		if ((loaded) || (ObjectModel2Timer > 800)) {
			if (has_loaded == 0) {
				maps map = MAP_DKRAP;
				gamemodes mode = GAMEMODE_RAP;
				if (Rando.quality_of_life.fast_boot) {
					map = MAP_MAINMENU;
					mode = GAMEMODE_MAINMENU;
				}
				initiateTransitionFade(map, 0, mode);
				has_loaded = 1;
			}
		}
	}
	if (Rando.archipelago) {
		handleArchipelagoFeed();
		handleArchipelagoString();
	}
	if (CurrentMap == MAP_FUNGI) {
		if ((TBVoidByte & 3) == 0) { // Not pausing
			if (CutsceneActive == 0) { // No cutscene playing
				if (Player) {
					int chunk = Player->chunk;
					if ((chunk < 12) || (chunk > 17)) { // Not in owl tree area, deemed a safe zone because of races
						handleTimeOfDay(TODCALL_FUNGIACTIVE);
					}
				}
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

#define WAIT_SIZE 64
static char wait_text_0[WAIT_SIZE] = "REMOVING LANKY KONG";
static char wait_text_1[WAIT_SIZE] = "TELLING 2DOS TO PLAY DK64";
static char wait_text_2[WAIT_SIZE] = "LOCKING K. LUMSY IN A CAGE";
static char wait_text_3[WAIT_SIZE] = "STEALING THE BANANA HOARD";
static unsigned char wait_text_lengths[] = {19, 25, 26, 25};

void insertROMMessages(void) {
	for (int i = 0; i < 4; i++) {
		unsigned char* message_write = getFile(WAIT_SIZE, 0x1FFD000 + (WAIT_SIZE * i));
		void* ptr = 0;
		if (i == 0) {
			ptr = &wait_text_0;
		} else if (i == 1) {
			ptr = &wait_text_1;
		} else if (i == 2) {
			ptr = &wait_text_2;
		} else if (i == 3) {
			ptr = &wait_text_3;
		}
		if (message_write[0] != 0) {
			dk_memcpy(ptr, message_write, WAIT_SIZE);
			wait_text_lengths[i] = 0;
			for (int j = 0; j < WAIT_SIZE; j++) {
				if ((message_write[j] == 0) && (wait_text_lengths[i] == 0)) {
					wait_text_lengths[i] = j;
				}
			}
		}
	}
}

static const char* wait_texts[] = {
	"BOOTING UP THE RANDOMIZER",
	wait_text_0,
	wait_text_1,
	wait_text_2,
	wait_text_3,
};
static unsigned char ammo_hud_timer = 0;

#define HERTZ 60

#define LOADBAR_START 350
#define LOADBAR_FINISH 900
#define LOADBAR_MAXWIDTH 200
#define LOADBAR_DIVISOR 35

#define INFO_STYLE 6
Gfx* drawInfoText(Gfx* dl, int x_offset, int y, char* str, int error) {
	int x = 93 + x_offset;
	if (x_offset == -1) {
		x = getCenter(INFO_STYLE,str);
	}
	int non_red = 0xFF;
	if (error) {
		non_red = 0;
	}
	return drawTextContainer(dl, INFO_STYLE, x, y, str, 0xFF, non_red, non_red, 255, 0);
}

typedef struct eeprom_warning_struct {
	/* 0x000 */ char* text;
	/* 0x004 */ short x_offset;
	/* 0x006 */ char error;
	/* 0x007 */ char margin_bottom;
} eeprom_warning_struct;

#define STANDARD_MARGIN_BOTTOM 14
static const eeprom_warning_struct warning_text[] = {
	{.text="WARNING", .x_offset=-10, .error=1, .margin_bottom=20},
	{.text="YOUR EMULATOR SETUP IS WRONG", .x_offset=-96, .error=0, .margin_bottom=STANDARD_MARGIN_BOTTOM},
	{.text="YOUR GAME WILL NOT SAVE!", .x_offset=-76, .error=1, .margin_bottom=STANDARD_MARGIN_BOTTOM},
	{.text="YOUR GAME WILL LIKELY", .x_offset=-88, .error=0, .margin_bottom=0},
	{.text="CRASH", .x_offset=88, .error=1, .margin_bottom=STANDARD_MARGIN_BOTTOM},
	{.text="GO TO THE WIKI", .x_offset=-32, .error=0, .margin_bottom=STANDARD_MARGIN_BOTTOM},
	{.text="OR THE DISCORD", .x_offset=-32, .error=0, .margin_bottom=STANDARD_MARGIN_BOTTOM},
	{.text="DISCORD.DK64RANDOMIZER.COM", .x_offset=-88, .error=0, .margin_bottom=STANDARD_MARGIN_BOTTOM},
	{.text="FOR HELP", .x_offset=-8, .error=0, .margin_bottom=STANDARD_MARGIN_BOTTOM},
};

typedef struct menu_paad {
	/* 0x000 */ char unk_00[0x12];
	/* 0x012 */ unsigned char screen;
} menu_paad;

Gfx* displayListModifiers(Gfx* dl) {
	if (CurrentMap != MAP_NINTENDOLOGO) {
		if (CurrentMap == MAP_NFRTITLESCREEN) {
			wait_progress_timer += 1;
			if (wait_progress_timer > LOADBAR_DIVISOR) {
				wait_progress_timer = 0;
				wait_progress_master += 1;
				if (wait_progress_master > 4) {
					wait_progress_master = 0;
				}
			}
			rgba* address = &KongRGBA[wait_progress_master];
			int left_f = (((LOADBAR_FINISH - LOADBAR_START) + LOADBAR_MAXWIDTH) / LOADBAR_DIVISOR) * wait_progress_timer;
			int left = left_f + LOADBAR_START - LOADBAR_MAXWIDTH;
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
			int bar_y = 475;
			int bar_text_y = 130;
			dl = drawScreenRect(dl, left, bar_y, right, bar_y + 10, address->red, address->green, address->blue, address->alpha);
			int wait_x_offset = 55;
			if (wait_progress_master > 0) {
				wait_x_offset = 160 - (wait_text_lengths[wait_progress_master - 1] << 2);
			}
			dl = drawPixelTextContainer(dl, wait_x_offset, bar_text_y, (char*)wait_texts[(int)wait_progress_master], 0xFF, 0xFF, 0xFF, 0xFF, 1);
			dl = drawPixelTextContainer(dl, 110, bar_text_y + 20, "PLEASE WAIT", 0xFF, 0xFF, 0xFF, 0xFF, 1);
		} else if (CurrentMap == MAP_MAINMENU) {
			if (EEPROMType != 2) {
				actorData* actor = findActorWithType(0x146);
				if (actor) {
					menu_paad* paad = (menu_paad*)actor->paad;
					if (paad->screen < 2) {
						// EEPROM Warning
						dl = drawScreenRect(dl, 250, 200, 1000, 700, 3, 3, 3, 1);
						int y_info = 130;
						for (int k = 0; k < sizeof(warning_text)/sizeof(eeprom_warning_struct); k++) {
							eeprom_warning_struct* local_warning = &warning_text[k];
							dl = drawInfoText(dl, local_warning->x_offset, y_info, local_warning->text, local_warning->error);
							y_info += local_warning->margin_bottom;
						}
					}
				}
			}
			dl = displaySongNameHandler(dl);
		} else {
			dl = drawTextPointers(dl);
			dl = displaySongNameHandler(dl);
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
				int fps_x = 250;
				int fps_y = 210;
				dl = drawPixelTextContainer(dl, fps_x, fps_y, fpsStr, 0xFF, 0xFF, 0xFF, 0xFF, 1);
			}
			dl = drawDPad(dl);
			dl = renderDingSprite(dl);
			dl = renderProgressiveSprite(dl);
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
					if ((hud_st == 1) || (hud_st == 2)) {
						bp_numerator = 0;
						bp_denominator = 0;
						for (int i = 0; i < 8; i++) {
							int bp_has = checkFlagDuplicate(FLAG_BP_JAPES_DK_HAS + (i * 5) + Character,FLAGTYPE_PERMANENT);
							int bp_turn = checkFlagDuplicate(FLAG_BP_JAPES_DK_TURN + (i * 5) + Character,FLAGTYPE_PERMANENT);
							if (!bp_turn) {
								if (bp_has) {
									bp_numerator += 1;
								}
								bp_denominator += 1;
							}
						}
						if (hud_st == 1) {
							hud_timer += 1;
						}
					} else if (hud_st == 3) {
						hud_timer -= 1;
						if (hud_timer < 0) {
							hud_timer = 0;
						}
					}
					dk_strFormat((char *)bpStr, "%dl%d", bp_numerator, bp_denominator);
					float opacity = 255 * hud_timer;
					opacity /= 12;
					float bp_x = 355.0f;
					float bp_y_start = 480.0f;
					dl = drawText(dl, 1, bp_x, bp_y_start + ((12 - hud_timer) * 4), bpStr, 0xFF, 0xFF, 0xFF, opacity);
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
	if (Gamemode == GAMEMODE_ADVENTURE) {
		if (NewlyPressedControllerInput.Buttons.d_down) {
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
