/**
 * @file quality_fixes.c
 * @author Ballaam
 * @brief Quality of life fixes to the game
 * @version 0.1
 * @date 2021-12-07
 * 
 * @copyright Copyright (c) 2021
 * 
 */
#include "../../include/common.h"

#define MODE_DKTV 3

void qualityOfLife_fixes(void) {
	/**
	 * @brief Quality of life fixes to the game
	 */
	if (Rando.quality_of_life.remove_cutscenes) {
		// Upon ROM Boot, set "Story Skip" to on
		if (Gamemode == GAMEMODE_NINTENDOLOGO) {
			StorySkip = 1;
		}
	}
	if (Rando.quality_of_life.vanilla_fixes) {
		// Set some flags in-game
		setPermFlag(FLAG_FTT_CRANKY); // Cranky FTT
		fixkey8();
		// Prevent a bug where detransforming from Rambi shortly before getting hit will keep you locked as Rambi
		if (CurrentMap == MAP_JAPES) {
			if (Player) {
				if (Character == 6) { // Rambi
					if (Player->detransform_timer == 0) {
						Player->rambi_enabled = 1;
					}
				}
			}
		} else if (CurrentMap == MAP_CAVESROTATINGROOM) {
			if (Player) {
				if (Player->yPos < 50.0f) {
					Player->xPos = 317.0f;
					Player->yPos = 124.0f;
					Player->zPos = 295.0f;
					displaySpriteAtXYZ(sprite_table[19], 0x3F800000, Player->xPos, Player->yPos, Player->zPos);
				}
			}
		} else {
			int is_beaver_bother = CurrentMap == MAP_BBOTHER_EASY ||
				CurrentMap == MAP_BBOTHER_HARD ||
				CurrentMap == MAP_BBOTHER_NORMAL;
			if (is_beaver_bother) {
				if (Player) {
					int control_state = Player->control_state;
					int good_state = control_state == 0x7D || // Klaptrap
						control_state == 0x73 || // Failure
						control_state == 0x74; // Victory
					if (!good_state) {
						Player->control_state = 0x7D;
					}
				}
			}
		}
	}
}

void checkNinWarp(void) {
	/**
	 * @brief Change the warp destination upon booting the game
	 */
	if (Rando.quality_of_life.fast_boot) {
		WarpToDKTV();
		TransitionType = 0;
	} else {
		initiateTransitionFade(MAP_DKRAP,0,2); // DK Rap
	}
}

int CanDive_WithCheck(void) {
	if (ObjectModel2Timer < 5) {
		return 1;
	}
	return CanDive();
}

static unsigned short previous_total_cbs = 0xFFFF;
static unsigned char previous_world = 0xFF;

static const short tnsportal_flags[] = {
	// Troff n Scoff portal clear flags
	FLAG_PORTAL_JAPES,
	FLAG_PORTAL_AZTEC,
	FLAG_PORTAL_FACTORY,
	FLAG_PORTAL_GALLEON,
	FLAG_PORTAL_FUNGI,
	FLAG_PORTAL_CAVES,
	FLAG_PORTAL_CASTLE,
};

typedef struct sprite_info {
	/* 0x000 */ char unk_00[0x358];
	/* 0x358 */ int timer;
	/* 0x35C */ char unk_35C[0x360-0x35C];
	/* 0x360 */ float scale_x;
	/* 0x364 */ float scale_z;
	/* 0x368 */ char unk_368[0x36A-0x368];
	/* 0x36A */ unsigned char red;
	/* 0x36B */ unsigned char green;
	/* 0x36C */ unsigned char blue;
	/* 0x36D */ unsigned char alpha;
} sprite_info;

#define SPRITE_ALPHA_IN 8
#define SPRITE_ALPHA_OUT 44
#define SPRITE_ALPHA_END 52

void playCBDing(void) {
	/**
	 * @brief Play Bell Ding sound effect
	 */
	playSFX(Bell);
}

void CBDing(void) {
	/**
	 * @brief Check if T&S Threshold has been met
	 */
	if (Rando.quality_of_life.cb_indicator) {
		int world = getWorld(CurrentMap, 1);
		int total_cbs = 0;
		if (world < 7) {
			total_cbs = CBTurnedInArray[world];
			for (int kong = 0; kong < 5; kong++) {
				total_cbs += MovesBase[kong].cb_count[world];
			}
			int req_cbs = TroffNScoffReqArray[world];
			if ((previous_total_cbs < req_cbs) && (total_cbs >= req_cbs) && (previous_world == world) && (CurrentMap != MAP_TROFFNSCOFF)) { // Ban in T&S because of delayed update to turn in array
				if (!checkFlag(tnsportal_flags[world],FLAGTYPE_PERMANENT)) {
					playCBDing();
				}
			}
		}
		previous_world = world;
		previous_total_cbs = total_cbs;
	}
}

void fixRBSlowTurn(void) {
	/**
	 * @brief Fix the Rocketbarrel Slow Turn glitch
	 * This occurs if you standing ground attack before jumping into a Rocketbarrel Barrel
	 */
	controlStateControl(0x1B);
	if (Player) {
		Player->turn_speed = 0x190;
	}
}

void postKRoolSaveCheck(void) {
	/**
	 * @brief Prevent the game saving on the transition from Chunky Phase to the K. Rool launch cutscene
	 */
	if ((CurrentMap != MAP_ISLES) || (!CutsceneFadeActive) || (CutsceneFadeIndex != 29)) {
		save();
	}
}

void tagBarrelBackgroundKong(int kong_actor) {
	/**
	 * @brief Alter the tag function to also change the background kong.
	 * This prevents a bug with tagging from a tag barrel where it doesn't update the background kong.
	 * This can result in a weird tag when getting caught by a guard or other situations
	 */
	tagKong(kong_actor);
	Player->new_kong = kong_actor;
}

void preventMedalHUD(int item, int unk0, int unk1) {
	/**
	 * @brief Prevent Medal HUD from showing
	 */
	if (item != 0xA) {
		displayItemOnHUD(item, unk0, unk1);
	}
}

void initHUDDirection(placementData* hud_data, int item) {
	/**
	 * @brief Modified initialization of HUD Direction function to account for new medal changes.
	 */
	int x_direction = 0;
	int y_direction = 0;
	hud_data->unk_0C = 0;
	switch(item) {
		case 0x0: // CB
		case 0xD: // CB T&S
		case 0xE: // Move Cost
			x_direction = -1;
			break;
		case 0x9: // GBs
		case 0xC: // Blueprint
			y_direction = 1;
			break;
		default:
			x_direction = 1;
		break;
	}
	hud_data->x_direction = x_direction * 0x30;
	hud_data->y_direction = y_direction * 0x30;
}

void* getHUDSprite_HUD(int item) {
	/**
	 * @brief Override HUD Sprite for Medals to be a MultiBunch
	 * @return Sprite Address
	 */
	if (item == 0xA) {
		return sprite_table[0xA8];
	} else {
		return getHUDSprite(item);
	}
}

void updateMultibunchCount(void) {
	/**
	 * @brief Get the total amount of colored bananas for a level.
	 * Used in the multibunch display
	 */
	int world = getWorld(CurrentMap,1);
	int count = 0;
	if (world < 7) {
		count = CBTurnedInArray[world];
		for (int kong = 0; kong < 5; kong++) {
			count += MovesBase[kong].cb_count[world];
		}
	}
	MultiBunchCount = count;
	if (HUD) {
		HUD->item[0xA].visual_item_count = count;
	}
}

void RabbitRaceInfiniteCode(void) {
	/**
	 * @brief Change Rabbit Race so that upon starting the race, you get infinite Crystal Coconuts
	 * This only applies to Round 2, and will end the infinite coconuts upon the race finishing
	 */
	initCharSpawnerActor();
	if (checkFlag(FLAG_RABBIT_ROUND1,FLAGTYPE_PERMANENT)) {
		int control_state = CurrentActorPointer_0->control_state;
		if (control_state == 0x1F) {
			if (CurrentActorPointer_0->control_state_progress == 2) {
				// Start
				setHUDItemAsInfinite(5,0,1);
			}
		} else if ((control_state == 0x28) || (control_state == 0x1E)) {
			if (CurrentActorPointer_0->control_state_progress == 0) {
				// End
				resetCoconutHUD();
			}
		}
	}
}

int fixDilloTNTPads(void* actor) {
	/**
	 * @brief Fix a bug where grabbing a TNT Barrel with Tiny, then throwing it can cause the TNT Barrel to go under the pad.
	 * This exposes behaviour where the TNT spawn pad can move if it's riding another object.
	 * To fix this, we change the behaviour of the TNT Spawn pad so that it won't obey gravity and will be locked in place.
	 * The unfortunate side effect is that if the ground ripples in Army Dillo, the pad won't move with the ripple.
	 * 
	 * @param actor TNT Spawn Pad actor address
	 * 
	 * @return Does actor obey gravity
	 */
	if ((CurrentMap == MAP_JAPESDILLO) || (CurrentMap == MAP_CAVESDILLO)) {
		return 0;
	}
	return getPadGravity(actor);
}

int canPlayJetpac(void) {
	/**
	 * @brief Determine whether the player can play Jetpac.
	 * We will only enable the player to attempt Jetpac upon not having the Jetpac Reward
	 * 
	 * @return Amount of medals the player has. Set to 0 if you have the Jetpac Reward
	 */
	if (checkFlag(FLAG_COLLECTABLE_RAREWARECOIN, FLAGTYPE_PERMANENT)) {
		return 0;
	} else {
		return countFlagArray(FLAG_MEDAL_JAPES_DK, 40, 0);
	}
}

void fixCrownEntrySKong(playerData* player, int animation) {
	player->strong_kong_ostand_bitfield &= 0xFFFFFFEF;
	playAnimation(player, animation);
}

void reduceTrapBubbleLife(void) {
	Player->trap_bubble_timer -= 5;
	if (Player->trap_bubble_timer < 1) {
		Player->trap_bubble_timer = 1;
	}
}

void exitTrapBubbleController(void) {
	int x = stickX_interpretted;
	int y = stickY_interpretted;
	int threshold = 0x28;
	if (((x > threshold) || (y > threshold)) && (Player->unk_288 != 0.0f)) {
		Player->unk_288 = 1.0f;
		reduceTrapBubbleLife();
		return;
	}
	if (((x < -threshold) || (y < -threshold)) && (Player->unk_288 == 0.0f)) {
		Player->unk_288 = 0.0f;
		reduceTrapBubbleLife();
		return;
	}
	if (NewlyPressedControllerInput.Buttons.a) {
		// Perform reduction twice to counteract that this can be done once per two frames
		reduceTrapBubbleLife();
		reduceTrapBubbleLife();
		return;
	}
}

static const char test_file_name[] = "BALLAAM";

void writeDefaultFilename(void) {
	for (int i = 0; i < 8; i++) {
		SaveExtraData(EGD_FILENAME, i, test_file_name[i]);
	}
}

void fixChimpyCamBug(void) {
	/**
	 * @brief Things to be reset upon first boot of the game on PJ64 (Because PJ64 is weird)
	 */
	wipeGlobalFlags();
	SaveToFile(DATA_CAMERATYPE, 0, 0, 0, Rando.default_camera_type);
	SaveToFile(DATA_LANGUAGE, 0, 0, 0, Rando.default_camera_type);
	SaveToFile(DATA_SOUNDTYPE, 0, 0, 0, Rando.default_sound_type);
	wipeFileStats();
	if (ENABLE_FILENAME) {
		writeDefaultFilename();
	}
	SaveToGlobal();
}