/**
 * @file file_screen.c
 * @author Ballaam
 * @brief Changes to the file screen
 * @version 0.1
 * @date 2022-01-23
 * 
 * @copyright Copyright (c) 2022
 * 
 */
#include "../../include/common.h"

static char balanced_igt[20] = "";
static char perc_str[7] = "";
static char gb_str[5] = "";

#define LINE_GAP 0x8C
static char updated_tracker = 0;

typedef struct tracker_struct {
	/* 0x000 */ short min_x;
	/* 0x002 */ short max_x;
	/* 0x004 */ short min_y;
	/* 0x006 */ short max_y;
	/* 0x008 */ unsigned char enabled;
	/* 0x009 */ unsigned char type;
} tracker_struct;

#define TRACKER_ENABLED_DEFAULT 1

static tracker_struct tracker_info[] = {
	// Position of items on the tracker image
	{.min_x = 0, .max_x = 20, .min_y = 0, .max_y = 22, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_COCONUT}, // Coconut
	{.min_x = 0, .max_x = 20, .min_y = 22, .max_y = 42, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_BONGOS}, // Bongos
	{.min_x = 0, .max_x = 20, .min_y = 44, .max_y = 64, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_GRAB}, // Grab
	{.min_x = 0, .max_x = 20, .min_y = 66, .max_y = 86, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_BLAST}, // Blast
	{.min_x = 0, .max_x = 20, .min_y = 88, .max_y = 108, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_STRONG}, // Strong
	{.min_x = 22, .max_x = 42, .min_y = 0, .max_y = 22, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_PEANUT}, // Peanut
	{.min_x = 22, .max_x = 42, .min_y = 22, .max_y = 42, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_GUITAR}, // Guitar
	{.min_x = 22, .max_x = 42, .min_y = 44, .max_y = 64, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_CHARGE}, // Charge
	{.min_x = 22, .max_x = 42, .min_y = 66, .max_y = 86, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_SPRING}, // Spring
	{.min_x = 22, .max_x = 42, .min_y = 88, .max_y = 108, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_ROCKET}, // Rocket
	{.min_x = 44, .max_x = 64, .min_y = 0, .max_y = 22, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_GRAPE}, // Grape
	{.min_x = 44, .max_x = 64, .min_y = 22, .max_y = 42, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_TROMBONE}, // Trombone
	{.min_x = 44, .max_x = 64, .min_y = 44, .max_y = 64, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_OSTAND}, // OStand
	{.min_x = 44, .max_x = 64, .min_y = 66, .max_y = 86, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_BALLOON}, // Balloon
	{.min_x = 44, .max_x = 64, .min_y = 88, .max_y = 108, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_OSPRINT}, // OSprint
	{.min_x = 66, .max_x = 86, .min_y = 0, .max_y = 22, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_FEATHER}, // Feather
	{.min_x = 66, .max_x = 86, .min_y = 22, .max_y = 42, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_SAX}, // Sax
	{.min_x = 66, .max_x = 86, .min_y = 44, .max_y = 64, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_PTT}, // PTT
	{.min_x = 66, .max_x = 86, .min_y = 66, .max_y = 86, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_MONKEYPORT}, // Monkeyport
	{.min_x = 66, .max_x = 86, .min_y = 88, .max_y = 108, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_MINI}, // Mini
	{.min_x = 88, .max_x = 108, .min_y = 0, .max_y = 22, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_PINEAPPLE}, // Pineapple
	{.min_x = 88, .max_x = 108, .min_y = 22, .max_y = 42, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_TRIANGLE}, // Triangle
	{.min_x = 88, .max_x = 108, .min_y = 44, .max_y = 64, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_PUNCH}, // Punch
	{.min_x = 88, .max_x = 108, .min_y = 66, .max_y = 86, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_GONE}, // Gone
	{.min_x = 88, .max_x = 108, .min_y = 88, .max_y = 108, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_HUNKY}, // Hunky
	{.min_x = 156, .max_x = 172, .min_y = 64, .max_y = 84, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_KEY1}, // Key1
	{.min_x = 172, .max_x = 189, .min_y = 64, .max_y = 84, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_KEY2}, // Key2
	{.min_x = 189, .max_x = 203, .min_y = 64, .max_y = 84, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_KEY3}, // Key3
	{.min_x = 205, .max_x = 221, .min_y = 64, .max_y = 84, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_KEY4}, // Key4
	{.min_x = 157, .max_x = 172, .min_y = 86, .max_y = 105, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_KEY5}, // Key5
	{.min_x = 173, .max_x = 188, .min_y = 86, .max_y = 105, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_KEY6}, // Key6
	{.min_x = 189, .max_x = 204, .min_y = 86, .max_y = 105, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_KEY7}, // Key7
	{.min_x = 205, .max_x = 220, .min_y = 86, .max_y = 105, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_KEY8}, // Key8
	{.min_x = 136, .max_x = 150, .min_y = 0, .max_y = 20, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_CAMERA}, // Camera
	{.min_x = 130, .max_x = 152, .min_y = 22, .max_y = 42, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_SHOCKWAVE}, // Shockwave
	{.min_x = 132, .max_x = 138, .min_y = 54, .max_y = 64, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_SLAM}, // Slam
	{.min_x = 138, .max_x = 141, .min_y = 52, .max_y = 55, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_SLAM}, // Slam
	{.min_x = 138, .max_x = 146, .min_y = 60, .max_y = 63, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_SLAM}, // Slam
	{.min_x = 146, .max_x = 152, .min_y = 54, .max_y = 63, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_SLAM}, // Slam
	{.min_x = 144, .max_x = 146, .min_y = 52, .max_y = 55, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_SLAM}, // Slam
	{.min_x = 132, .max_x = 152, .min_y = 46, .max_y = 64, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_SLAM_HAS}, // Slam Has
	{.min_x = 134, .max_x = 149, .min_y = 66, .max_y = 79, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_HOMING}, // Homing
	{.min_x = 132, .max_x = 152, .min_y = 92, .max_y = 104, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_SNIPER}, // Sniper
	{.min_x = 0, .max_x = 20, .min_y = 108, .max_y = 128, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_DIVE}, // Dive
	{.min_x = 22, .max_x = 42, .min_y = 108, .max_y = 128, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_ORANGE}, // Orange
	{.min_x = 44, .max_x = 64, .min_y = 108, .max_y = 128, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_BARREL}, // Barrel
	{.min_x = 66, .max_x = 86, .min_y = 108, .max_y = 128, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_VINE}, // Vine
	{.min_x = 87, .max_x = 107, .min_y = 108, .max_y = 128, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_CLIMB}, // Climbing
	{.min_x = 176, .max_x = 192, .min_y = 0, .max_y = 18, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_MELON_2}, // Melon_2
	{.min_x = 192, .max_x = 209, .min_y = 0, .max_y = 18, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_MELON_3}, // Melon_3
	{.min_x = 218, .max_x = 238, .min_y = 0, .max_y = 18, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_INSUPG_1}, // InsUpg_1
	{.min_x = 239, .max_x = 249, .min_y = 3, .max_y = 18, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_INSUPG_2}, // InsUpg_2
	{.min_x = 220, .max_x = 235, .min_y = 22, .max_y = 36, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_BELT_1}, // Belt_1
	{.min_x = 236, .max_x = 244, .min_y = 22, .max_y = 37, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_BELT_2}, // Belt_2
	{.min_x = 135, .max_x = 149, .min_y = 108, .max_y = 128, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_CRANKY}, // Cranky
	{.min_x = 157, .max_x = 173, .min_y = 108, .max_y = 128, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_FUNKY}, // Funky
	{.min_x = 177, .max_x = 194, .min_y = 108, .max_y = 128, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_CANDY}, // Candy
	{.min_x = 199, .max_x = 217, .min_y = 113, .max_y = 123, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_SNIDE}, // Snide
};

void wipeTrackerCache(void) {
	/**
	 * @brief Wipe image cache for all images that are being cached
	 */
	for (int i = 0; i < 32; i++) {
		if ((ImageCache[i].image_index == IMAGE_TRACKER) && (ImageCache[i].image_state != 0)) {
			ImageCache[i].image_state = 0;
			if (ImageCache[i].image_pointer) {
				complex_free(ImageCache[i].image_pointer);
			}
			return;
		}
	}
}

static unsigned char slam_screen_level = 0;
static unsigned char belt_screen_level = 0;
static unsigned char ins_screen_level = 0;

typedef struct passMapping {
	short button_required;
	unsigned char btf_val;
	char text_char;
} passMapping;

typedef enum passEnum {
	PASSKEY_NULL,
	PASSKEY_DU,
	PASSKEY_DD,
	PASSKEY_DL,
	PASSKEY_DR,
	PASSKEY_Z,
	PASSKEY_S,
} passEnum;

#define L_Button 0x0020
#define D_Up 0x0800
#define D_Down 0x0400
#define D_Left 0x0200
#define D_Right 0x0100
#define B_Button 0x4000
#define A_Button 0x8000
#define Z_Button 0x2000
#define R_Button 0x0010
#define Start_Button 0x1000
#define C_Up 0x0008
#define C_Down 0x0004
#define C_Left 0x0002
#define C_Right 0x0001

static char passwordProgress = 0;
static char acceptPassInput = 0;
static char inputtedPass[8];
static passMapping button_mapping_password[] = {
	{.button_required = D_Up | C_Up, .btf_val = PASSKEY_DU, .text_char='U'},
	{.button_required = D_Down | C_Down, .btf_val = PASSKEY_DD, .text_char='D'},
	{.button_required = D_Left | C_Left, .btf_val = PASSKEY_DL, .text_char='L'},
	{.button_required = D_Right | C_Right, .btf_val = PASSKEY_DR, .text_char='R'},
	{.button_required = Z_Button, .btf_val = PASSKEY_Z, .text_char='Z'},
	{.button_required = Start_Button, .btf_val = PASSKEY_S, .text_char='S'},
};
static char passTextDisplay[9];

int isMovePregiven(int index) {
	/**
	 * @brief Get the tracker move initial state (Empty File)
	 * 
	 * @param index Tracker item index
	 * 
	 * @return State
	 */
	switch(index) {
		case TRACKER_TYPE_COCONUT:
		case TRACKER_TYPE_PEANUT:
		case TRACKER_TYPE_GRAPE:
		case TRACKER_TYPE_FEATHER:
		case TRACKER_TYPE_PINEAPPLE:
			return initFile_hasGun(index / 5);
		case TRACKER_TYPE_BONGOS:
		case TRACKER_TYPE_GUITAR:
		case TRACKER_TYPE_TROMBONE:
		case TRACKER_TYPE_SAX:
		case TRACKER_TYPE_TRIANGLE:
			return initFile_hasInstrument((index - 1) / 5);
		case TRACKER_TYPE_GRAB:
			return Rando.moves_pregiven.grab || initFile_checkTraining(PURCHASE_MOVES, 0, 3);
		case TRACKER_TYPE_BLAST:
			return Rando.moves_pregiven.blast || initFile_checkTraining(PURCHASE_MOVES, 0, 1);
		case TRACKER_TYPE_STRONG:
			return Rando.moves_pregiven.strong_kong || initFile_checkTraining(PURCHASE_MOVES, 0, 2);
		case TRACKER_TYPE_CHARGE:
			return Rando.moves_pregiven.charge || initFile_checkTraining(PURCHASE_MOVES, 1, 1);
		case TRACKER_TYPE_SPRING:
			return Rando.moves_pregiven.spring || initFile_checkTraining(PURCHASE_MOVES, 1, 3);
		case TRACKER_TYPE_ROCKET:
			return Rando.moves_pregiven.rocketbarrel || initFile_checkTraining(PURCHASE_MOVES, 1, 2);
		case TRACKER_TYPE_OSTAND:
			return Rando.moves_pregiven.ostand || initFile_checkTraining(PURCHASE_MOVES, 2, 1);
		case TRACKER_TYPE_BALLOON:
			return Rando.moves_pregiven.balloon || initFile_checkTraining(PURCHASE_MOVES, 2, 2);
		case TRACKER_TYPE_OSPRINT:
			return Rando.moves_pregiven.osprint || initFile_checkTraining(PURCHASE_MOVES, 2, 3);
		case TRACKER_TYPE_PTT:
			return Rando.moves_pregiven.twirl || initFile_checkTraining(PURCHASE_MOVES, 3, 2);
		case TRACKER_TYPE_MONKEYPORT:
			return Rando.moves_pregiven.monkeyport || initFile_checkTraining(PURCHASE_MOVES, 3, 3);
		case TRACKER_TYPE_MINI:
			return Rando.moves_pregiven.mini || initFile_checkTraining(PURCHASE_MOVES, 3, 1);
		case TRACKER_TYPE_PUNCH:
			return Rando.moves_pregiven.punch || initFile_checkTraining(PURCHASE_MOVES, 4, 2);
		case TRACKER_TYPE_GONE:
			return Rando.moves_pregiven.gone || initFile_checkTraining(PURCHASE_MOVES, 4, 3);
		case TRACKER_TYPE_HUNKY:
			return Rando.moves_pregiven.hunky || initFile_checkTraining(PURCHASE_MOVES, 4, 1);
		case TRACKER_TYPE_CAMERA:
			return Rando.moves_pregiven.camera || initFile_checkTraining(PURCHASE_FLAG, -1, FLAG_ABILITY_CAMERA) || initFile_checkTraining(PURCHASE_FLAG, -1, -2);
		case TRACKER_TYPE_SHOCKWAVE:
			return Rando.moves_pregiven.shockwave || initFile_checkTraining(PURCHASE_FLAG, -1, FLAG_ABILITY_SHOCKWAVE) || initFile_checkTraining(PURCHASE_FLAG, -1, -2);
		case TRACKER_TYPE_SLAM:
		case TRACKER_TYPE_SLAM_HAS:
			return initFile_getSlamLevel(1);
		case TRACKER_TYPE_HOMING:
			return Rando.moves_pregiven.homing || initFile_checkTraining(PURCHASE_GUN, -1, 2);
		case TRACKER_TYPE_SNIPER:
			return Rando.moves_pregiven.sniper || initFile_checkTraining(PURCHASE_GUN, -1, 3);
		case TRACKER_TYPE_CLIMB:
			return Rando.moves_pregiven.climbing || initFile_checkTraining(PURCHASE_FLAG, -1, FLAG_ABILITY_CLIMBING);
		case TRACKER_TYPE_DIVE:
			return Rando.moves_pregiven.dive || initFile_checkTraining(PURCHASE_FLAG, -1, FLAG_TBARREL_DIVE);
		case TRACKER_TYPE_ORANGE:
			return Rando.moves_pregiven.oranges || initFile_checkTraining(PURCHASE_FLAG, -1, FLAG_TBARREL_ORANGE);
		case TRACKER_TYPE_BARREL:
			return Rando.moves_pregiven.barrels || initFile_checkTraining(PURCHASE_FLAG, -1, FLAG_TBARREL_BARREL);
		case TRACKER_TYPE_VINE:
			return Rando.moves_pregiven.vines || initFile_checkTraining(PURCHASE_FLAG, -1, FLAG_TBARREL_VINE);
		case TRACKER_TYPE_MELON_2:
			if (initFile_getInsUpgradeLevel(1) >= 1) {
				return 1;
			}
			for (int i = 0; i < 5; i++) {
				if (initFile_hasInstrument(i)) {
					return 1;
				}
			}
			return 0;
		case TRACKER_TYPE_MELON_3:
			return initFile_getInsUpgradeLevel(1) >= 2;
		case TRACKER_TYPE_INSUPG_1:
			return initFile_getInsUpgradeLevel(1) >= 1;
		case TRACKER_TYPE_INSUPG_2:
			return initFile_getInsUpgradeLevel(1) >= 3;
		case TRACKER_TYPE_BELT_1:
			return initFile_getBeltLevel(1) >= 1;
		case TRACKER_TYPE_BELT_2:
			return initFile_getBeltLevel(1) >= 2;
		case TRACKER_TYPE_AMMOBELT:
			return initFile_getBeltLevel(1);
		case TRACKER_TYPE_INSTRUMENT_UPG:
			if (initFile_getInsUpgradeLevel(1) >= 3) {
				return 2;
			} else if (initFile_getInsUpgradeLevel(1) >= 1) {
				return 1;
			}
			return 0;
		case TRACKER_TYPE_KEY1:
		case TRACKER_TYPE_KEY2:
		case TRACKER_TYPE_KEY3:
		case TRACKER_TYPE_KEY4:
		case TRACKER_TYPE_KEY5:
		case TRACKER_TYPE_KEY6:
		case TRACKER_TYPE_KEY7:
		case TRACKER_TYPE_KEY8:
			if (Rando.keys_preturned & (1 << (index - TRACKER_TYPE_KEY1))) {
				return 1;
			}
			return 0;
		case TRACKER_TYPE_CRANKY:
		case TRACKER_TYPE_FUNKY:
		case TRACKER_TYPE_CANDY:
		case TRACKER_TYPE_SNIDE:
			if (Rando.check_shop_flags & (0x80 >> (index - TRACKER_TYPE_CRANKY))) {
				return 1;
			}
			return 0;
		default:
			break;
	}
	return 0;
}

int getEnabledState(int index) {
	/**
	 * @brief Get the enabled state of a tracker item
	 * 
	 * @param index Tracker item index
	 * 
	 * @return State
	 */
	int file_empty = 0;
	if (CurrentMap == MAP_MAINMENU) {
		file_empty = isFileEmpty(0);
	}
	if (file_empty) { // Empty file check
		return isMovePregiven(index);
	}
	switch(index) {
		case TRACKER_TYPE_COCONUT:
		case TRACKER_TYPE_PEANUT:
		case TRACKER_TYPE_GRAPE:
		case TRACKER_TYPE_FEATHER:
		case TRACKER_TYPE_PINEAPPLE:
			{
				int kong = index / 5;
				return MovesBase[kong].weapon_bitfield & 1;
			}
		case TRACKER_TYPE_BONGOS:
		case TRACKER_TYPE_GUITAR:
		case TRACKER_TYPE_TROMBONE:
		case TRACKER_TYPE_SAX:
		case TRACKER_TYPE_TRIANGLE:
			{
				int kong = index / 5;
				return MovesBase[kong].instrument_bitfield & 1;
			}
		case TRACKER_TYPE_GRAB:
			return MovesBase[KONG_DK].special_moves & MOVECHECK_GRAB;
		case TRACKER_TYPE_BLAST:
			return MovesBase[KONG_DK].special_moves & MOVECHECK_BLAST;
		case TRACKER_TYPE_STRONG:
			return MovesBase[KONG_DK].special_moves & MOVECHECK_STRONG;
		case TRACKER_TYPE_CHARGE:
			return MovesBase[KONG_DIDDY].special_moves & MOVECHECK_CHARGE;
		case TRACKER_TYPE_SPRING:
			return MovesBase[KONG_DIDDY].special_moves & MOVECHECK_SPRING;
		case TRACKER_TYPE_ROCKET:
			return MovesBase[KONG_DIDDY].special_moves & MOVECHECK_ROCKETBARREL;
		case TRACKER_TYPE_OSTAND:
			return MovesBase[KONG_LANKY].special_moves & MOVECHECK_OSTAND;
		case TRACKER_TYPE_BALLOON:
			return MovesBase[KONG_LANKY].special_moves & MOVECHECK_BALLOON;
		case TRACKER_TYPE_OSPRINT:
			return MovesBase[KONG_LANKY].special_moves & MOVECHECK_OSPRINT;
		case TRACKER_TYPE_PTT:
			return MovesBase[KONG_TINY].special_moves & MOVECHECK_TWIRL;
		case TRACKER_TYPE_MONKEYPORT:
			return MovesBase[KONG_TINY].special_moves & MOVECHECK_MONKEYPORT;
		case TRACKER_TYPE_MINI:
			return MovesBase[KONG_TINY].special_moves & MOVECHECK_MINI;
		case TRACKER_TYPE_PUNCH:
			return MovesBase[KONG_CHUNKY].special_moves & MOVECHECK_PUNCH;
		case TRACKER_TYPE_GONE:
			return MovesBase[KONG_CHUNKY].special_moves & MOVECHECK_GONE;
		case TRACKER_TYPE_HUNKY:
			return MovesBase[KONG_CHUNKY].special_moves & MOVECHECK_HUNKY;
		case TRACKER_TYPE_CAMERA:
			return checkFlagDuplicate(FLAG_ABILITY_CAMERA, FLAGTYPE_PERMANENT);
		case TRACKER_TYPE_SHOCKWAVE:
			return checkFlagDuplicate(FLAG_ABILITY_SHOCKWAVE, FLAGTYPE_PERMANENT);
		case TRACKER_TYPE_SLAM:
		case TRACKER_TYPE_SLAM_HAS:
			return MovesBase[KONG_DK].simian_slam;
		case TRACKER_TYPE_HOMING:
			return MovesBase[KONG_DK].weapon_bitfield & MOVECHECK_HOMING;
		case TRACKER_TYPE_SNIPER:
			return MovesBase[KONG_DK].weapon_bitfield & MOVECHECK_SNIPER;
		case TRACKER_TYPE_CLIMB:
			return checkFlagDuplicate(FLAG_ABILITY_CLIMBING, FLAGTYPE_PERMANENT);
		case TRACKER_TYPE_DIVE:
			return checkFlagDuplicate(FLAG_TBARREL_DIVE, FLAGTYPE_PERMANENT);
		case TRACKER_TYPE_ORANGE:
			return checkFlagDuplicate(FLAG_TBARREL_ORANGE, FLAGTYPE_PERMANENT);
		case TRACKER_TYPE_BARREL:
			return checkFlagDuplicate(FLAG_TBARREL_BARREL, FLAGTYPE_PERMANENT);
		case TRACKER_TYPE_VINE:
			return checkFlagDuplicate(FLAG_TBARREL_VINE, FLAGTYPE_PERMANENT);
		case TRACKER_TYPE_MELON_2:
			for (int i = 0; i < 5; i++) {
				if (MovesBase[i].instrument_bitfield != 0) {
					return 1;
				}
			}
			return 0;
		case TRACKER_TYPE_MELON_3:
			return MovesBase[KONG_DK].instrument_bitfield & MOVECHECK_THIRDMELON;
		case TRACKER_TYPE_INSUPG_1:
			return MovesBase[KONG_DK].instrument_bitfield & MOVECHECK_UPGRADE1;
		case TRACKER_TYPE_INSUPG_2:
			return MovesBase[KONG_DK].instrument_bitfield & MOVECHECK_UPGRADE2;
		case TRACKER_TYPE_BELT_1:
			return MovesBase[KONG_DK].ammo_belt >= 1;
		case TRACKER_TYPE_BELT_2:
			return MovesBase[KONG_DK].ammo_belt >= 2;
		case TRACKER_TYPE_AMMOBELT:
			return MovesBase[KONG_DK].ammo_belt;
		case TRACKER_TYPE_INSTRUMENT_UPG:
			if (MovesBase[KONG_DK].instrument_bitfield & MOVECHECK_UPGRADE2) {
				return 2;
			} else if (MovesBase[KONG_DK].instrument_bitfield & MOVECHECK_UPGRADE1) {
				return 1;
			}
			return 0;
		case TRACKER_TYPE_KEY1:
		case TRACKER_TYPE_KEY2:
		case TRACKER_TYPE_KEY3:
		case TRACKER_TYPE_KEY4:
		case TRACKER_TYPE_KEY5:
		case TRACKER_TYPE_KEY6:
		case TRACKER_TYPE_KEY7:
		case TRACKER_TYPE_KEY8:
			{
				// Keys in
				int key_index = index - TRACKER_TYPE_KEY1;
				int key_there = has_key(key_index);
				if (!key_there) {
					if (Rando.keys_preturned & (1 << key_index)) {
						key_there = 1;
					}
				}
				return key_there;
			}
		case TRACKER_TYPE_CRANKY:
		case TRACKER_TYPE_FUNKY:
		case TRACKER_TYPE_CANDY:
		case TRACKER_TYPE_SNIDE:
			return checkFlagDuplicate(FLAG_ITEM_CRANKY + (index - TRACKER_TYPE_CRANKY), FLAGTYPE_PERMANENT);
		default:
			break;
	}
	return 0;
}

void updateEnabledStates(void) {
	/**
	 * @brief Update all tracker item enabled states
	 */
	slam_screen_level = 0;
	belt_screen_level = 0;
	ins_screen_level = 0;
	if (Rando.fast_start_beginning) {
		for (int i = 0; i < 5; i++) {
			int subtype = -1;
			if (i < 4) {
				// Training Moves
				if (TrainingMoves_New[i].purchase_type == PURCHASE_FLAG) {
					subtype = getMoveProgressiveFlagType(TrainingMoves_New[i].purchase_value);
				}
			} else if (i == 4) {
				// First Move
				if (FirstMove_New.purchase_type == PURCHASE_FLAG) {
					subtype = getMoveProgressiveFlagType(FirstMove_New.purchase_value);
				}
			}
			if (subtype == 0) {
				slam_screen_level += 1;
			} else if (subtype == 1) {
				belt_screen_level += 1;
			} else if (subtype == 2) {
				ins_screen_level += 1;
			}
			
		}
	}
	for (int i = 0; i < (int)(sizeof(tracker_info) / sizeof(tracker_struct)); i++) {
		tracker_info[i].enabled = getEnabledState(tracker_info[i].type);
	}
}

#define TRACKER_INIT 2
#define TRACKER_WIDTH 254
#define TRACKER_HEIGHT 128

void initTracker(void) {
	/**
	 * @brief Initialize tracker
	 */
	updated_tracker = 0;
}

void resetTracker(void) {
	/**
	 * @brief Reset tracker
	 */
	updated_tracker = 0;
	WipeImageCache();
}

#define TRACKER_FADE 0.3f

void modifyTrackerImage(int dl_offset) {
	/**
	 * @brief Modify the tracker image based on the items in your inventory
	 * 
	 * @param dl_offset y_offset
	 */
	// Check if tracker needs updating
	if (updated_tracker == (TRACKER_INIT + 3)) {
		return;
	}
	updated_tracker += 1;
	if (updated_tracker == TRACKER_INIT) {
		// wipeTrackerCache();
		updateEnabledStates();
	}
	if (updated_tracker == (TRACKER_INIT + 3)) {
		// Load Tracker Image into cache
		short* image = getPtr14Texture(IMAGE_TRACKER);
		// Manipulate cached image
		int width = TRACKER_WIDTH;
		for (int i = 0; i < (int)(sizeof(tracker_info) / sizeof(tracker_struct)); i++) {
			int enabled = tracker_info[i].enabled;
			for (int x = tracker_info[i].min_x; x < tracker_info[i].max_x; x++) {
				for (int y = tracker_info[i].min_y; y < tracker_info[i].max_y; y++) {
					unsigned short init_rgba = *(short*)(image + (y * width) + x);
					if (init_rgba & 1) {
						// Has Alpha
						unsigned short new_rgba = 1;
						int update = 0;
						if (tracker_info[i].type == TRACKER_TYPE_SLAM) {
							if (enabled) {
								/*
									If slam is illuminated, but white, that means that
									the calculated slam count is higher than slam 3.
									As a result, should be fixed
								*/
								int subdue[] = {0,0,0};
								if (enabled == 1) {
									subdue[0] = 1; // B
									subdue[1] = 3; // G
									subdue[2] = 1; // R
									update = 1;
								} else if (enabled == 2) {
									subdue[0] = 3; // B
									subdue[1] = 2; // G
									subdue[2] = 0; // R
									update = 1;
								} else if (enabled == 3) {
									subdue[0] = 0; // B
									subdue[1] = 0; // G
									subdue[2] = 3; // R
									update = 1;
								}
								for (int c = 0; c < 3; c++) {
									int shift = (5 * c) + 1;
									float channel = (init_rgba >> shift) & 31;
									if (subdue[c] == 0) {
										channel = 0;
									} else if (subdue[c] == 1) {
										channel *= 0.19f;
									} else if (subdue[c] == 2) {
										channel *= 0.5f;
									}
									new_rgba |= (((int)(channel) & 31) << shift);
								}
							}
						} else if ((tracker_info[i].type == TRACKER_TYPE_INSUPG_2) || (tracker_info[i].type == TRACKER_TYPE_BELT_2)) {
							if (!enabled) {
								update = 1;
								new_rgba = 0;
							}
						} else {
							if (!enabled) {
								for (int c = 0; c < 3; c++) {
									int shift = (5 * c) + 1;
									float channel = (init_rgba >> shift) & 31;
									channel *= TRACKER_FADE; // Depreciation
									new_rgba |= (((int)(channel) & 31) << shift);
								}
								update = 1;
							}
						}
						if (update) {
							*(short*)(image + (y * width) + x) = new_rgba;
						}
					}
				}
			}
		}
	}
}

int getTrackerYOffset(void) {
	float y_temp = DEFAULT_TRACKER_Y_OFFSET;
	return y_temp;
}

Gfx* display_file_images(Gfx* dl, int y_offset) {
	/**
	 * @brief Display images on the file screen
	 * 
	 * @param dl Display List Address
	 * @param y_offfset Y Offset of the tracker image
	 * 
	 * @return New Display List Address
	 */
	int tracker_x = 160;
	dl = drawImage(dl, IMAGE_TRACKER, RGBA16, TRACKER_WIDTH, TRACKER_HEIGHT, tracker_x, y_offset + getTrackerYOffset(),1.0f, 1.0f,0xFF);
	modifyTrackerImage(y_offset);
	if (CurrentMap == MAP_MAINMENU) {
		int opacity = 0x80;
		if (checkFlag(FLAG_GAME_BEATEN, FLAGTYPE_PERMANENT)) {
			opacity = 0xFF;
		}
		dl = drawImage(dl, 195, RGBA16, 32, 32, 1110, y_offset + 690, 4.0f, 4.0f, opacity);
	}
	return dl;
}

Gfx* display_text(Gfx* dl) {
	/**
	 * @brief Display Text on the file screen
	 * 
	 * @param dl Display List Address
	 * 
	 * @return New Display List Address
	 */
	int y = FileScreenDLOffset - 402;
	// Balanced IGT
	// y += LINE_GAP;
	int secs = IGT % 60;
	float secsf = secs;
	secsf /= 60;
	int hm = IGT / 60;
	int minutes = hm % 60;
	int hours = hm / 60;
	float stat_x = 385.0f;
	dk_strFormat((char*)balanced_igt, "%03d:%02d:%02d",hours,minutes,secs);
	dl = drawText(dl, 1, stat_x, y + 80, (char*)balanced_igt, 0xFF, 0xFF, 0xFF, 0xFF);
	// Percentage Counter
	dk_strFormat((char*)perc_str, "%d%%", FilePercentage);
	dl = drawText(dl, 1, stat_x, y + 50, (char*)perc_str, 0xFF, 0xFF, 0xFF, 0xFF);
	// GB Count
	dk_strFormat((char*)gb_str, "%03d", *(int*)(0x8003380C));
	dl = drawText(dl, 1, stat_x + 25.0f, y + 20, (char*)gb_str, 0xFF, 0xFF, 0xFF, 0xFF);
	dl = display_file_images(dl, FileScreenDLOffset - 720);
	return dl;
}

static unsigned char hash_textures[] = {48,49,50,51,55,62,63,64,65,76};
#define INFO_Y_DIFF 50

Gfx* displayHash(Gfx* dl, int y_offset) {
	/**
	 * @brief Display seed hash on the file screen
	 * 
	 * @param dl Display List Address
	 * @param y_offset Y Offset for the hash images
	 * 
	 * @return New Display List Address
	 */
	for (int i = 0; i < 5; i++) {
		int hash_index = Rando.hash[i] % 10;
		int starting_x = 440.0f;
		int hash_y = 920;
		dl = drawImage(dl, hash_textures[hash_index], RGBA16, 32, 32, starting_x + (100 * i), hash_y - y_offset, 3.0f, 3.0f, 0xFF);
	}
	int info_y = 480 - y_offset;
	if (Rando.rom_flags.plando) {
		dl = displayCenteredText(dl, info_y / 4, "PLANDOMIZER", 1);
		info_y += INFO_Y_DIFF;
	}
	if (Rando.rom_flags.spoiler) {
		dl = displayCenteredText(dl, info_y / 4, "SPOILER GENNED", 1);
		info_y += INFO_Y_DIFF;
	}
	if (Rando.rom_flags.pass_locked) {
		dl = displayCenteredText(dl, info_y / 4, "LOCKED", 1);
		info_y += INFO_Y_DIFF;
	}
	return dl;
}

void correctKongFaces(void) {
	/**
	 * @brief Alter the kong faces on the file screen to handle pre-given kongs
	 */
	if (Rando.unlock_kongs) {
		for (int i = 0; i < 5; i++) {
			int flag = checkFlag(kong_flags[i], FLAGTYPE_PERMANENT);
			KongUnlockedMenuArray[i] = flag;
			if (!flag) {
				KongUnlockedMenuArray[i] = (Rando.unlock_kongs & (1 << i)) != 0;
			}
		}
		if (!checkFlag(FLAG_KONG_DK, FLAGTYPE_PERMANENT)) {
			if ((Rando.unlock_kongs & 1) == 0) {
				KongUnlockedMenuArray[0] = 0;
			}
		}
	} else {
		for (int i = 0; i < 5; i++) {
			KongUnlockedMenuArray[i] = checkFlag(kong_flags[i], FLAGTYPE_PERMANENT);
		}
		KongUnlockedMenuArray[(int)Rando.starting_kong] = 1;
		if (Rando.starting_kong != 0) {
			if (!checkFlag(FLAG_KONG_DK, FLAGTYPE_PERMANENT)) {
				KongUnlockedMenuArray[0] = 0;
			}
		}
	}
}

void wipeFileMod(int file, int will_save) {
	/**
	 * @brief Modification of the wipe file function
	 * 
	 * @param file File Index
	 * @param will_save Wiping will save to file
	 */
	resetTracker();
	WipeFile(file, will_save);
}

void enterFileProgress(int sfx) {
	/**
	 * @brief Modification of the enter "File Progress" screen function
	 * 
	 * @param sfx Sound effect played upon entering the file progress screen
	 */
	resetTracker();
	playSFX(sfx);
}

void giveCollectables(void) {
	/**
	 * @brief Give collectables based on file progress
	 */
	int max = 10; //giving instrument power even if no instrument is unlocked
	for (int i = 1; i < 4; i++) {
		if (MovesBase[0].instrument_bitfield & (1 << i)) {
			max += 5;
		}
	}
	int energy = max/2;
	if (Rando.quality_of_life.global_instrument) {
		CollectableBase.InstrumentEnergy = energy;
	} else {
		for (int instrument_kong = 0; instrument_kong < 5; instrument_kong++) {
			MovesBase[instrument_kong].instrument_energy = energy;
		}
	}
	CollectableBase.Health = CollectableBase.Melons * 4;
	CollectableBase.StandardAmmo = 25 * (1 << MovesBase[0].ammo_belt);
	CollectableBase.Oranges = 10;
	CollectableBase.Crystals = 1500;
	CollectableBase.Film = 5;
}

void wipeFileStats(void) {
	for (int i = 0; i < 9; i++) {
		ResetExtraData(EGD_LEVELIGT, i);
	}
	for (int i = 0; i < STAT_TERMINATOR; i++) {
		// Reset Statistics
		ResetExtraData(EGD_BONUSSTAT, i);
	}
	for (int i = 0; i < 5; i++) {
		ResetExtraData(EGD_KONGIGT, i);
	}
	ResetExtraData(EGD_HELMHURRYIGT, 0);
	ResetExtraData(EGD_HELMHURRYDISABLE, 0);
}

void setAllDefaultFlags(void) {
	short* data = getFile(0x800, 0x1FFD800);
	for (int i = 0; i < 0x400; i++) {
		short flag = data[i];
		if (flag == -1) {
			return;
		} else {
			setPermFlag(flag);
		}
	}
}

void startFile(void) {
	lockInput(1);
	int file_empty = isFileEmpty(0);
	fileStart(0);
	if (file_empty) {
		// New File
		setAllDefaultFlags();
		unlockMoves();
		applyFastStart();
		openCrownDoor();
		giveCollectables();
		if (checkFlag(FLAG_COLLECTABLE_LLAMAGB, FLAGTYPE_PERMANENT)) {
			setPermFlag(FLAG_MODIFIER_LLAMAFREE); // No item check
		}
		pre_turn_keys();
		Character = Rando.starting_kong;
		wipeFileStats();
		if (checkFlag(FLAG_ARCADE_ROUND1, FLAGTYPE_PERMANENT)) {
			setPermFlag(FLAG_ARCADE_LEVER);
		}
		SaveToGlobal();
		for (int i = 0; i < 4; i++) {
			if (Rando.check_shop_flags & (0x80 >> i)) {
				setPermFlag(FLAG_ITEM_CRANKY + i);
			}
		}
		handleTimeOfDay(TODCALL_INITFILE);
	} else {
		// Dirty File
		Character = Rando.starting_kong;
		determineStartKong_PermaLossMode();
		giveCollectables();
	}
	resetProgressive();
	updateBarrierCounts();
	if ((Rando.helm_hurry_mode) && (!ReadFile(DATA_HELMHURRYOFF, 0, 0, 0))) {
		QueueHelmTimer = 1;
	}
	setKongIgt();
	ForceStandardAmmo = 0;
}

int testPasswordSequence(void) {
	if (Rando.password == 0) {
		return 1; // Any password will work, we'll remove this once we get some stuff working
	}
	return encPass(&inputtedPass, &Rando.hash) == Rando.password;
}

void wipePassword(void) {
	passwordProgress = 0;
	for (int i = 0; i < 8; i++) {
		inputtedPass[i] == PASSKEY_NULL;
		passTextDisplay[i] = 0;
	}
}

void handlePassword(void) {
	short button_btf = *(short*)(&NewlyPressedControllerInput.Buttons);
	if (button_btf == 0) {
		acceptPassInput = 1;
	} else if (acceptPassInput) {
		if (passwordProgress >= 8) {
			return;
		}
		int has_button = 0;
		int button_sent = 0;
		for (int i = 0; i < sizeof(button_mapping_password) >> 2; i++) {
			if (button_mapping_password[i].button_required & button_btf) {
				inputtedPass[passwordProgress] = button_mapping_password[i].btf_val;
				passTextDisplay[passwordProgress++] = button_mapping_password[i].text_char;
				acceptPassInput = 0;
				playSFX(64); // Arcade walk
				return;
			}
		}
	}
}

void password_screen_code(actorData* actor, int buttons) {
	menu_controller_paad* paad = actor->paad;
	if (paad->screen_transition_progress == 0.0f) {
		if (paad->unk_4 == 0.0f) {
			if (buttons & 1) {
				// A
				if (passwordProgress == 8) {
					if (testPasswordSequence()) {
						playSFX(459); // Success
						paad->prevent_action = 0;
						paad->next_screen = 3; // file progress
					} else {
						playSFX(83); // Grunt
						wipePassword();
					}
				}
			} else if (buttons & 2) {
				// B
				playSFX(0x2C9);
				paad->prevent_action = 0;
				paad->next_screen = 2; // file select
			} else {
				// Inputting sequence
				handlePassword();
			}
		}
		initMenuBackground(paad,4);
	}
	updateMenuController(actor,paad,1);
}

void password_screen_init(actorData* actor) {
	menu_controller_paad* paad = actor->paad;
	displayMenuSprite(paad, (void*)0x80720CF0, 0x122, 0xD2, 0.75f, 2, 0); // A
	displayMenuSprite(paad, (void*)0x80720D14, 0x23, 0xD2, 0.75f, 2, 0); // B
	passwordProgress = 0;
	wipePassword();
}

Gfx* password_screen_gfx(actorData* actor, Gfx* dl) {
	float x2, y2;
	menu_controller_paad* paad = actor->paad;
	gDPSetPrimColor(dl++, 0, 0, 0xFF, 0xFF, 0xFF, 0xFF);
	handleTextScrolling(paad, 160.0f, 25.0f, &x2, &y2, 5, 0, *(float*)(0x80033CB4));
	dl = printText(dl, x2 * 4.0f, y2 * 4.0f, 0.6f, "ENTER PASSWORD");
	handleTextScrolling(paad, 160.0f, 80.0f, &x2, &y2, 5, 0, 2.0f);
	for (int i = passwordProgress; i < 8; i++) {
		passTextDisplay[i] = '?';
	}
	return printText(dl, x2 * 4.0f, y2 * 4.0f, 1.0f, &passTextDisplay);
}

void file_progress_screen_code(actorData* actor, int buttons) {
	/**
	 * @brief Handle inputs on the file progress screen
	 * 
	 * @param actor Menu Controller Actor Address
	 * @param buttons Buttons Bitfield
	 */
	/*
		Buttons:
			0001 0000 0000 - Z Button
			0000 1000 0000 - C Down
			0000 0100 0000 - C Up
			0000 0010 0000 - Default
			0000 0001 0000 - Down
			0000 0000 1000 - Right
			0000 0000 0100 - Default
			0000 0000 0010 - B Button
			0000 0000 0001 - A Button
	*/
	menu_controller_paad* paad = actor->paad;
	if (paad->screen_transition_progress == 0.0f) {
		if (paad->unk_4 == 0.0f) {
			if (buttons & 1) { // A
				startFile();
			} else if (buttons & 2) { // B
				playSFX(0x2C9);
				paad->prevent_action = 0;
				paad->next_screen = 2;
			} else if (buttons & 0x100) { // Z
				if (!isFileEmpty(0)) {
					playSFX(0x2C9);
					paad->prevent_action = 0;
					paad->next_screen = 5;
				} else {
					playSFX(Wrong);
				}
			}
		}
		initMenuBackground(paad,4);
	}
	updateMenuController(actor,paad,1);
}

static char* inverted_controls_str[] = {
	"INVERTED",
	"NON-INVERTED"
};

Gfx* displayInverted(Gfx* dl, int style, int x, int y, char* str, int unk0) {
	/**
	 * @brief Display the inverted controls text on the options screen
	 * 
	 * @param dl Display List Address
	 * @param style Text style
	 * @param x Text X Position
	 * @param y Text Y Position
	 * @param str Text String
	 * @param unk0 Unknown
	 * 
	 * @return New Display List Address
	 */
	if (InvertedControls > 1) {
		InvertedControls = 1;
	}
	return displayText(dl, style, x, y, inverted_controls_str[(int)InvertedControls], unk0);
}

static unsigned char previous_map_save = MAP_ISLES;

void setPrevSaveMap(void) {
	/**
	 * @brief Set Previous map where a save occurred for the in-level IGT functionality
	 */
	previous_map_save = Rando.starting_map;
}

void QuitGame(void) {
	save();
	LoadGameOver();
}

int updateLevelIGT(void) {
	/**
	 * @brief Update level in-game time values
	 * 
	 * @return New in-game time
	 */
	saveHelmHurryTime();
	int new_igt = getNewSaveTime();
	if (canSaveHelmHurry()) {
		int sum = 0;
		for (int i = 0; i < 9; i++) {
			int value = ReadExtraData(EGD_LEVELIGT, i);
			sum += value; 
		}
		int diff = new_igt - sum;
		int world = getWorld(previous_map_save, 1);
		if (world < 9) {
			int old = ReadExtraData(EGD_LEVELIGT, world);
			SaveExtraData(EGD_LEVELIGT, world, old + diff);
		}
	}
	previous_map_save = CurrentMap;
	updatePercentageKongStat();
	SaveToGlobal();
	return new_igt;
}

void changeFileSelectAction(menu_controller_paad* paad, int cap, int buttons) {
	/**
	 * @brief Alter file select action to account for the reduced file count
	 * 
	 * @param paad Menu Controller Paad
	 * @param cap Amount of selectable options on the file select screen
	 * @param buttons Button Bitfield
	 */
	if ((buttons & 4) == 0) {
		if (buttons & 8) {
			playSFX(0x2C9);
			*(float*)(0x80033F44) = *(float*)(0x80033D60) * 2;
			*(char*)(0x800337F0) = 0;
		}
	} else {
		playSFX(0x2C9);
		*(float*)(0x80033F44) = *(float*)(0x80033D5C) * 2;
		paad->selected_action -= 2;
		paad->unk_4 = 2.0f;
		if (paad->selected_action < 0) {
			paad->selected_action += cap;
		}
		if ((paad->selected_action % 2) == 1) {
			paad->selected_action -= 1;
		}
		*(char*)(0x800337F0) = 0;
	}
}

void changeFileSelectAction_0(menu_controller_paad* paad, int cap) {
	/**
	 * @brief Second portion of altering the actions you can perform on the file select screen to account for reduced file count
	 * 
	 * @param paad Menu Controller Paad
	 * @param cap Amount of selectable options on the file select screen
	 */
	*(char*)(0x80033F48) = 0;
	if (*(float*)(0x80033F44) > 0) {
		paad->unk_4 += *(float*)(0x80033F44);
		if (paad->unk_4 >= 2.0f) {
			paad->unk_4 = 0;
			paad->selected_action += 2;
			if (paad->selected_action >= cap) {
				paad->selected_action -= cap;
			}
			*(float*)(0x80033F44) = 0.0f;
		}
	} else if (*(float*)(0x80033F44) < 0) {
		paad->unk_4 += *(float*)(0x80033F44);
		if (paad->unk_4 <= 0.0f) {
			*(float*)(0x80033F44) = 0;
			paad->unk_4 = 0.0f;
		}
	}
}