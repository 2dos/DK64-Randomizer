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

#define TRACKER_TYPE_COCONUT 0
#define TRACKER_TYPE_BONGOS 1
#define TRACKER_TYPE_GRAB 2
#define TRACKER_TYPE_STRONG 3
#define TRACKER_TYPE_BLAST 4

#define TRACKER_TYPE_PEANUT 5
#define TRACKER_TYPE_GUITAR 6
#define TRACKER_TYPE_CHARGE 7
#define TRACKER_TYPE_ROCKET 8
#define TRACKER_TYPE_SPRING 9

#define TRACKER_TYPE_GRAPE 10
#define TRACKER_TYPE_TROMBONE 11
#define TRACKER_TYPE_OSTAND 12
#define TRACKER_TYPE_OSPRINT 13
#define TRACKER_TYPE_BALLOON 14

#define TRACKER_TYPE_FEATHER 15
#define TRACKER_TYPE_SAX 16
#define TRACKER_TYPE_PTT 17
#define TRACKER_TYPE_MINI 18
#define TRACKER_TYPE_MONKEYPORT 19

#define TRACKER_TYPE_PINEAPPLE 20
#define TRACKER_TYPE_TRIANGLE 21
#define TRACKER_TYPE_PUNCH 22
#define TRACKER_TYPE_HUNKY 23
#define TRACKER_TYPE_GONE 24

#define TRACKER_TYPE_SLAM 25
#define TRACKER_TYPE_HOMING 26
#define TRACKER_TYPE_SNIPER 27
#define TRACKER_TYPE_AMMOBELT 28
#define TRACKER_TYPE_INSTRUMENT_UPG 29

#define TRACKER_TYPE_DIVE 30
#define TRACKER_TYPE_ORANGE 31
#define TRACKER_TYPE_BARREL 32
#define TRACKER_TYPE_VINE 33

#define TRACKER_TYPE_CAMERA 34
#define TRACKER_TYPE_SHOCKWAVE 35

#define TRACKER_TYPE_KEY1 36
#define TRACKER_TYPE_KEY2 37
#define TRACKER_TYPE_KEY3 38
#define TRACKER_TYPE_KEY4 39
#define TRACKER_TYPE_KEY5 40
#define TRACKER_TYPE_KEY6 41
#define TRACKER_TYPE_KEY7 42
#define TRACKER_TYPE_KEY8 43

#define TRACKER_TYPE_MELON_2 44
#define TRACKER_TYPE_MELON_3 45
#define TRACKER_TYPE_INSUPG_1 46
#define TRACKER_TYPE_INSUPG_2 47
#define TRACKER_TYPE_BELT_1 48
#define TRACKER_TYPE_BELT_2 49

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
	{.min_x = 125, .max_x = 138, .min_y = 108, .max_y = 128, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_KEY1}, // Key1
	{.min_x = 141, .max_x = 157, .min_y = 108, .max_y = 128, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_KEY2}, // Key2
	{.min_x = 156, .max_x = 171, .min_y = 108, .max_y = 128, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_KEY3}, // Key3
	{.min_x = 173, .max_x = 189, .min_y = 108, .max_y = 128, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_KEY4}, // Key4
	{.min_x = 189, .max_x = 204, .min_y = 108, .max_y = 128, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_KEY5}, // Key5
	{.min_x = 205, .max_x = 220, .min_y = 108, .max_y = 128, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_KEY6}, // Key6
	{.min_x = 221, .max_x = 236, .min_y = 108, .max_y = 128, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_KEY7}, // Key7
	{.min_x = 237, .max_x = 252, .min_y = 108, .max_y = 128, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_KEY8}, // Key8
	{.min_x = 136, .max_x = 150, .min_y = 0, .max_y = 20, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_CAMERA}, // Camera
	{.min_x = 130, .max_x = 152, .min_y = 22, .max_y = 42, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_SHOCKWAVE}, // Shockwave
	{.min_x = 132, .max_x = 138, .min_y = 54, .max_y = 64, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_SLAM}, // Slam
	{.min_x = 138, .max_x = 141, .min_y = 52, .max_y = 55, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_SLAM}, // Slam
	{.min_x = 138, .max_x = 146, .min_y = 60, .max_y = 63, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_SLAM}, // Slam
	{.min_x = 146, .max_x = 152, .min_y = 54, .max_y = 63, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_SLAM}, // Slam
	{.min_x = 144, .max_x = 146, .min_y = 52, .max_y = 55, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_SLAM}, // Slam
	{.min_x = 134, .max_x = 149, .min_y = 66, .max_y = 79, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_HOMING}, // Homing
	{.min_x = 132, .max_x = 152, .min_y = 92, .max_y = 104, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_SNIPER}, // Sniper
	{.min_x = 0, .max_x = 20, .min_y = 108, .max_y = 128, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_DIVE}, // Dive
	{.min_x = 22, .max_x = 42, .min_y = 108, .max_y = 128, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_ORANGE}, // Orange
	{.min_x = 44, .max_x = 64, .min_y = 108, .max_y = 128, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_BARREL}, // Barrel
	{.min_x = 66, .max_x = 86, .min_y = 108, .max_y = 128, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_VINE}, // Vine
	{.min_x = 186, .max_x = 202, .min_y = 0, .max_y = 18, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_MELON_2}, // Melon_2
	{.min_x = 202, .max_x = 219, .min_y = 0, .max_y = 18, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_MELON_3}, // Melon_3
	{.min_x = 218, .max_x = 238, .min_y = 22, .max_y = 40, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_INSUPG_1}, // InsUpg_1
	{.min_x = 239, .max_x = 249, .min_y = 25, .max_y = 39, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_INSUPG_2}, // InsUpg_2
	{.min_x = 220, .max_x = 235, .min_y = 44, .max_y = 57, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_BELT_1}, // Belt_1
	{.min_x = 236, .max_x = 244, .min_y = 44, .max_y = 58, .enabled = TRACKER_ENABLED_DEFAULT, .type = TRACKER_TYPE_BELT_2}, // Belt_2
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
			return initFile_getSlamLevel(1);
		case TRACKER_TYPE_HOMING:
			return Rando.moves_pregiven.homing || initFile_checkTraining(PURCHASE_GUN, -1, 2);
		case TRACKER_TYPE_SNIPER:
			return Rando.moves_pregiven.sniper || initFile_checkTraining(PURCHASE_GUN, -1, 3);
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
			return MovesBase[KONG_DK].simian_slam;
		case TRACKER_TYPE_HOMING:
			return MovesBase[KONG_DK].weapon_bitfield & MOVECHECK_HOMING;
		case TRACKER_TYPE_SNIPER:
			return MovesBase[KONG_DK].weapon_bitfield & MOVECHECK_SNIPER;
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
				if (MovesBase[i].instrument_bitfield & 1) {
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
				int key_there = checkFlag(FLAG_KEYIN_KEY1 + key_index, FLAGTYPE_PERMANENT);
				if (!key_there) {
					if (Rando.keys_preturned & (1 << key_index)) {
						key_there = 1;
					}
				}
				return key_there;
			}
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
	for (int i = 0; i < 4; i++) {
		if (TrainingMoves_New[i].purchase_type == PURCHASE_FLAG) {
			int subtype = getMoveProgressiveFlagType(TrainingMoves_New[i].purchase_value);
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
							if (!enabled) {
								new_rgba = 0;
								update = 1;
							} else {
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
									channel *= 0.3f; // Depreciation
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

int* display_file_images(int* dl, int y_offset) {
	/**
	 * @brief Display images on the file screen
	 * 
	 * @param dl Display List Address
	 * @param y_offfset Y Offset of the tracker image
	 * 
	 * @return New Display List Address
	 */
	dl = drawImage(dl, IMAGE_TRACKER, RGBA16, TRACKER_WIDTH, TRACKER_HEIGHT, 160, y_offset + 150,1.0f, 1.0f,0xFF);
	modifyTrackerImage(y_offset);
	return dl;
}

int* display_text(int* dl) {
	/**
	 * @brief Display Text on the file screen
	 * 
	 * @param dl Display List Address
	 * 
	 * @return New Display List Address
	 */
	int y = FileScreenDLOffset - 320;
	// Balanced IGT
	// y += LINE_GAP;
	int secs = IGT % 60;
	float secsf = secs;
	secsf /= 60;
	int hm = IGT / 60;
	int minutes = hm % 60;
	int hours = hm / 60;
	dk_strFormat((char*)balanced_igt, "%03d:%02d:%02d",hours,minutes,secs);
	dl = drawText(dl, 1, 410, y + 80, (char*)balanced_igt, 0xFF, 0xFF, 0xFF, 0xFF);
	// Percentage Counter
	dk_strFormat((char*)perc_str, "%d%%", FilePercentage);
	dl = drawText(dl, 1, 410, y + 50, (char*)perc_str, 0xFF, 0xFF, 0xFF, 0xFF);
	// GB Count
	dk_strFormat((char*)gb_str, "%03d", *(int*)(0x8003380C));
	dl = drawText(dl, 1, 435, y + 20, (char*)gb_str, 0xFF, 0xFF, 0xFF, 0xFF);
	dl = display_file_images(dl, FileScreenDLOffset - 720);
	return dl;
}

static unsigned char hash_textures[] = {48,49,50,51,55,62,63,64,65,76};
int* displayHash(int* dl, int y_offset) {
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
		dl = drawImage(dl, hash_textures[hash_index], RGBA16, 32, 32, 440 + (100 * i), 920 - y_offset, 3.0f, 3.0f, 0xFF);
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
	for (int instrument_kong = 0; instrument_kong < 5; instrument_kong++) {
		MovesBase[instrument_kong].instrument_energy = energy;
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
	for (int i = 0; i < 8; i++) {
		ResetExtraData(EGD_FILENAME, i);
	}
	ResetExtraData(EGD_HELMHURRYIGT, 0);
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
				lockInput(1);
				int file_empty = isFileEmpty(0);
				fileStart(0);
				if (file_empty) {
					// New File
					setFlagDuplicate(0,1,FLAGTYPE_PERMANENT); // Set null flag as it ensures no=item stuff is actually no-item
					unlockMoves();
					applyFastStart();
					openCrownDoor();
					giveCollectables();
					activateBananaports();
					if(Rando.fast_gbs) {
						setPermFlag(FLAG_RABBIT_ROUND1); //Start race at round 2
					}
					if (Rando.quality_of_life.caves_kosha_dead) {
						setPermFlag(FLAG_MODIFIER_KOSHADEAD); // Giant Kosha Dead
					}
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
				} else {
					// Dirty File
					Character = Rando.starting_kong;
					determineStartKong_PermaLossMode();
					giveCollectables();
				}
				if (ENABLE_FILENAME) {
					writeDefaultFilename();
				}
				if ((Rando.helm_hurry_mode) && (!ReadFile(DATA_HELMHURRYOFF, 0, 0, 0))) {
					QueueHelmTimer = 1;
				}
				setKongIgt();
				ForceStandardAmmo = 0;
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

int* displayInverted(int* dl, int style, int x, int y, char* str, int unk0) {
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

void initOptionScreen(void) {
	/**
	 * @brief Initialize Options Screen
	 */
	*(char*)(0x800338FC) = 5; // 5 Options
	*(short*)(0x8002DA86) = 1; // Cap to 1
	*(short*)(0x8002DA46) = getHi(&InvertedControls); // Up/Down Edit
	*(short*)(0x8002DA4E) = getLo(&InvertedControls); // Up/Down Edit
	*(short*)(0x8002DA1E) = getHi(&InvertedControls); // Up/Down Edit
	*(short*)(0x8002DA22) = getLo(&InvertedControls); // Up/Down Edit
	*(short*)(0x8002DADE) = getHi(&InvertedControls); // Save to global
	*(short*)(0x8002DAE2) = getLo(&InvertedControls); // Save to global
	*(short*)(0x8002DA88) = 0x1000; // Prevent Language Update
	writeFunction(0x8002DEC4, &displayInverted); // Modify Function Call
}

static unsigned char previous_map_save = MAP_ISLES;

void setPrevSaveMap(void) {
	/**
	 * @brief Set Previous map where a save occurred for the in-level IGT functionality
	 */
	previous_map_save = Rando.starting_map;
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