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
char k_rool_text[9] = "& K.ROOL";

#define LINE_GAP 0x8C
static char updated_tracker = 0;

typedef struct tracker_struct {
	/* 0x000 */ short min_x;
	/* 0x002 */ short max_x;
	/* 0x004 */ short min_y;
	/* 0x006 */ short max_y;
	/* 0x008 */ unsigned char enabled;
	/* 0x009 */ unsigned char type;
	/* 0x00A */ unsigned char item;
	/* 0x00B */ char level;
	/* 0x00C */ char kong;
} tracker_struct;

#define TRACKER_ENABLED_DEFAULT 1

static tracker_struct tracker_info[] = {
	// Position of items on the tracker image
	{
		// Coconut
		.min_x = 0, .max_x = 20,
		.min_y = 0, .max_y = 22,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_COCONUT,
		.item = REQITEM_MOVE,
		.level = 4,
		.kong = KONG_DK,
	},
	{
		// Bongos
		.min_x = 0, .max_x = 20,
		.min_y = 22, .max_y = 42,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_BONGOS,
		.item = REQITEM_MOVE,
		.level = 8,
		.kong = KONG_DK,
	},
	{
		// Grab
		.min_x = 0, .max_x = 20,
		.min_y = 44, .max_y = 64,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_GRAB,
		.item = REQITEM_MOVE,
		.level = 2,
		.kong = KONG_DK,
	},
	{
		// Blast
		.min_x = 0, .max_x = 20,
		.min_y = 66, .max_y = 86,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_BLAST,
		.item = REQITEM_MOVE,
		.level = 0,
		.kong = KONG_DK,
	},
	{
		// Strong
		.min_x = 0, .max_x = 20,
		.min_y = 88, .max_y = 108,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_STRONG,
		.item = REQITEM_MOVE,
		.level = 1,
		.kong = KONG_DK,
	},
	{
		// Peanut
		.min_x = 22, .max_x = 42,
		.min_y = 0, .max_y = 22,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_PEANUT,
		.item = REQITEM_MOVE,
		.level = 4,
		.kong = KONG_DIDDY,
	},
	{
		// Guitar
		.min_x = 22, .max_x = 42,
		.min_y = 22, .max_y = 42,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_GUITAR,
		.item = REQITEM_MOVE,
		.level = 8,
		.kong = KONG_DIDDY,
	},
	{
		// Charge
		.min_x = 22, .max_x = 42,
		.min_y = 44, .max_y = 64,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_CHARGE,
		.item = REQITEM_MOVE,
		.level = 0,
		.kong = KONG_DIDDY,
	},
	{
		// Spring
		.min_x = 22, .max_x = 42,
		.min_y = 66, .max_y = 86,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_SPRING,
		.item = REQITEM_MOVE,
		.level = 2,
		.kong = KONG_DIDDY,
	},
	{
		// Rocket
		.min_x = 22, .max_x = 42,
		.min_y = 88, .max_y = 108,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_ROCKET,
		.item = REQITEM_MOVE,
		.level = 1,
		.kong = KONG_DIDDY,
	},
	{
		// Grape
		.min_x = 44, .max_x = 64,
		.min_y = 0, .max_y = 22,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_GRAPE,
		.item = REQITEM_MOVE,
		.level = 4,
		.kong = KONG_LANKY,
	},
	{
		// Trombone
		.min_x = 44, .max_x = 64,
		.min_y = 22, .max_y = 42,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_TROMBONE,
		.item = REQITEM_MOVE,
		.level = 8,
		.kong = KONG_LANKY,
	},
	{
		// OStand
		.min_x = 44, .max_x = 64,
		.min_y = 44, .max_y = 64,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_OSTAND,
		.item = REQITEM_MOVE,
		.level = 0,
		.kong = KONG_LANKY,
	},
	{
		// Balloon
		.min_x = 44, .max_x = 64,
		.min_y = 66, .max_y = 86,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_BALLOON,
		.item = REQITEM_MOVE,
		.level = 1,
		.kong = KONG_LANKY,
	},
	{
		// OSprint
		.min_x = 44, .max_x = 64,
		.min_y = 88, .max_y = 108,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_OSPRINT,
		.item = REQITEM_MOVE,
		.level = 2,
		.kong = KONG_LANKY,
	},
	{
		// Feather
		.min_x = 66, .max_x = 86,
		.min_y = 0, .max_y = 22,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_FEATHER,
		.item = REQITEM_MOVE,
		.level = 4,
		.kong = KONG_TINY,
	},
	{
		// Sax
		.min_x = 66, .max_x = 86,
		.min_y = 22, .max_y = 42,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_SAX,
		.item = REQITEM_MOVE,
		.level = 8,
		.kong = KONG_TINY,
	},
	{
		// PTT
		.min_x = 66, .max_x = 86,
		.min_y = 44, .max_y = 64,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_PTT,
		.item = REQITEM_MOVE,
		.level = 1,
		.kong = KONG_TINY,
	},
	{
		// Monkeyport
		.min_x = 66, .max_x = 86,
		.min_y = 66, .max_y = 86,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_MONKEYPORT,
		.item = REQITEM_MOVE,
		.level = 2,
		.kong = KONG_TINY,
	},
	{
		// Mini
		.min_x = 66, .max_x = 86,
		.min_y = 88, .max_y = 108,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_MINI,
		.item = REQITEM_MOVE,
		.level = 0,
		.kong = KONG_TINY,
	},
	{
		// Pineapple
		.min_x = 88, .max_x = 108,
		.min_y = 0, .max_y = 22,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_PINEAPPLE,
		.item = REQITEM_MOVE,
		.level = 4,
		.kong = KONG_CHUNKY,
	},
	{
		// Triangle
		.min_x = 88, .max_x = 108,
		.min_y = 22, .max_y = 42,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_TRIANGLE,
		.item = REQITEM_MOVE,
		.level = 8,
		.kong = KONG_CHUNKY,
	},
	{
		// Punch
		.min_x = 88, .max_x = 108,
		.min_y = 44, .max_y = 64,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_PUNCH,
		.item = REQITEM_MOVE,
		.level = 1,
		.kong = KONG_CHUNKY,
	},
	{
		// Gone
		.min_x = 88, .max_x = 108,
		.min_y = 66, .max_y = 86,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_GONE,
		.item = REQITEM_MOVE,
		.level = 2,
		.kong = KONG_CHUNKY,
	},
	{
		// Hunky
		.min_x = 88, .max_x = 108,
		.min_y = 88, .max_y = 108,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_HUNKY,
		.item = REQITEM_MOVE,
		.level = 0,
		.kong = KONG_CHUNKY,
	},
	{
		// Key1
		.min_x = 156, .max_x = 172,
		.min_y = 64, .max_y = 84,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_KEY1,
		.item = REQITEM_KEY,
		.level = 0,
	},
	{
		// Key2
		.min_x = 172, .max_x = 189,
		.min_y = 64, .max_y = 84,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_KEY2,
		.item = REQITEM_KEY,
		.level = 1,
	},
	{
		// Key3
		.min_x = 189, .max_x = 203,
		.min_y = 64, .max_y = 84,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_KEY3,
		.item = REQITEM_KEY,
		.level = 2,
	},
	{
		// Key4
		.min_x = 205, .max_x = 221,
		.min_y = 64, .max_y = 84,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_KEY4,
		.item = REQITEM_KEY,
		.level = 3,
	},
	{
		// Key5
		.min_x = 157, .max_x = 172,
		.min_y = 86, .max_y = 105,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_KEY5,
		.item = REQITEM_KEY,
		.level = 4,
	},
	{
		// Key6
		.min_x = 173, .max_x = 188,
		.min_y = 86, .max_y = 105,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_KEY6,
		.item = REQITEM_KEY,
		.level = 5,
	},
	{
		// Key7
		.min_x = 189, .max_x = 204,
		.min_y = 86, .max_y = 105,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_KEY7,
		.item = REQITEM_KEY,
		.level = 6,
	},
	{
		// Key8
		.min_x = 205, .max_x = 220,
		.min_y = 86, .max_y = 105,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_KEY8,
		.item = REQITEM_KEY,
		.level = 7,
	},
	{
		// Camera
		.min_x = 136, .max_x = 150,
		.min_y = 0, .max_y = 20,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_CAMERA,
		.item = REQITEM_MOVE,
		.level = 10,
		.kong = 4,
	},
	{
		// Shockwave
		.min_x = 130, .max_x = 152,
		.min_y = 22, .max_y = 42,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_SHOCKWAVE,
		.item = REQITEM_MOVE,
		.level = 10,
		.kong = 5,
	},
	{
		// Slam
		.min_x = 132, .max_x = 138,
		.min_y = 54, .max_y = 64,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_SLAM,
		.item = REQITEM_MOVE,
		.level = 3,
	},
	{
		// Slam
		.min_x = 138, .max_x = 141,
		.min_y = 52, .max_y = 55,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_SLAM,
		.item = REQITEM_MOVE,
		.level = 3,
	},
	{
		// Slam
		.min_x = 138, .max_x = 146,
		.min_y = 60, .max_y = 63,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_SLAM,
		.item = REQITEM_MOVE,
		.level = 3,
	},
	{
		// Slam
		.min_x = 146, .max_x = 152,
		.min_y = 54, .max_y = 63,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_SLAM,
		.item = REQITEM_MOVE,
		.level = 3,
	},
	{
		// Slam
		.min_x = 144, .max_x = 146,
		.min_y = 52, .max_y = 55,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_SLAM,
		.item = REQITEM_MOVE,
	},
	{
		 //Slam Has
		.min_x = 132, .max_x = 152,
		.min_y = 46, .max_y = 64,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_SLAM_HAS,
		.item = REQITEM_MOVE,
		.level = 3,
	},
	{
		// Homing
		.min_x = 134, .max_x = 149,
		.min_y = 66, .max_y = 79,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_HOMING,
		.item = REQITEM_MOVE,
		.level = 5,
	},
	{
		// Sniper
		.min_x = 132, .max_x = 152,
		.min_y = 92, .max_y = 104,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_SNIPER,
		.item = REQITEM_MOVE,
		.level = 6,
	},
	{
		// Dive
		.min_x = 0, .max_x = 20,
		.min_y = 108, .max_y = 128,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_DIVE,
		.item = REQITEM_MOVE,
		.level = 10,
		.kong = 0,
	},
	{
		// Orange
		.min_x = 22, .max_x = 42,
		.min_y = 108, .max_y = 128,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_ORANGE,
		.item = REQITEM_MOVE,
		.level = 10,
		.kong = 1,
	},
	{
		// Barrel
		.min_x = 44, .max_x = 64,
		.min_y = 108, .max_y = 128,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_BARREL,
		.item = REQITEM_MOVE,
		.level = 10,
		.kong = 2,
	},
	{
		// Vine
		.min_x = 66, .max_x = 86,
		.min_y = 108, .max_y = 128,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_VINE,
		.item = REQITEM_MOVE,
		.level = 10,
		.kong = 3,
	},
	{
		// Climbing
		.min_x = 87, .max_x = 107,
		.min_y = 108, .max_y = 128,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_CLIMB,
		.item = REQITEM_MOVE,
		.level = 11,
	},
	{
		// Melon_2
		.min_x = 176, .max_x = 192,
		.min_y = 0, .max_y = 18,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_MELON_2,
	},
	{
		// Melon_3
		.min_x = 192, .max_x = 209,
		.min_y = 0, .max_y = 18,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_MELON_3,
	},
	{
		// InsUpg_1
		.min_x = 218, .max_x = 238,
		.min_y = 0, .max_y = 18,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_INSUPG_1,
	},
	{
		// InsUpg_2
		.min_x = 239, .max_x = 249,
		.min_y = 3, .max_y = 18,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_INSUPG_2,
	},
	{
		// Belt_1
		.min_x = 220, .max_x = 235,
		.min_y = 22, .max_y = 36,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_BELT_1,
	},
	{
		// Belt_2
		.min_x = 236, .max_x = 244,
		.min_y = 22, .max_y = 37,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_BELT_2,
	},
	{
		// Cranky
		.min_x = 135, .max_x = 149,
		.min_y = 108, .max_y = 128,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_CRANKY,
		.item = REQITEM_SHOPKEEPER,
		.kong = 0,
	},
	{
		// Funky
		.min_x = 157, .max_x = 173,
		.min_y = 108, .max_y = 128,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_FUNKY,
		.item = REQITEM_SHOPKEEPER,
		.kong = 1,
	},
	{
		// Candy
		.min_x = 177, .max_x = 194,
		.min_y = 108, .max_y = 128,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_CANDY,
		.item = REQITEM_SHOPKEEPER,
		.kong = 2,
	},
	{
		// Snide
		.min_x = 199, .max_x = 217,
		.min_y = 113, .max_y = 123,
		.enabled = TRACKER_ENABLED_DEFAULT,
		.type = TRACKER_TYPE_SNIDE,
		.item = REQITEM_SHOPKEEPER,
		.kong = 3,
	},
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
unsigned char pregiven_status[] = {
	0, // 0  = TRACKER_TYPE_COCONUT
	0, // 1  = TRACKER_TYPE_BONGOS
	0, // 2  = TRACKER_TYPE_GRAB
	0, // 3  = TRACKER_TYPE_STRONG
	0, // 4  = TRACKER_TYPE_BLAST
	0, // 5  = TRACKER_TYPE_PEANUT
	0, // 6  = TRACKER_TYPE_GUITAR
	0, // 7  = TRACKER_TYPE_CHARGE
	0, // 8  = TRACKER_TYPE_ROCKET
	0, // 9  = TRACKER_TYPE_SPRING
	0, // 10 = TRACKER_TYPE_GRAPE
	0, // 11 = TRACKER_TYPE_TROMBONE
	0, // 12 = TRACKER_TYPE_OSTAND
	0, // 13 = TRACKER_TYPE_OSPRINT
	0, // 14 = TRACKER_TYPE_BALLOON
	0, // 15 = TRACKER_TYPE_FEATHER
	0, // 16 = TRACKER_TYPE_SAX
	0, // 17 = TRACKER_TYPE_PTT
	0, // 18 = TRACKER_TYPE_MINI
	0, // 19 = TRACKER_TYPE_MONKEYPORT
	0, // 20 = TRACKER_TYPE_PINEAPPLE
	0, // 21 = TRACKER_TYPE_TRIANGLE
	0, // 22 = TRACKER_TYPE_PUNCH
	0, // 23 = TRACKER_TYPE_HUNKY
	0, // 24 = TRACKER_TYPE_GONE
	0, // 25 = TRACKER_TYPE_SLAM
	0, // 26 = TRACKER_TYPE_SLAM_HAS
	0, // 27 = TRACKER_TYPE_HOMING
	0, // 28 = TRACKER_TYPE_SNIPER
	0, // 29 = TRACKER_TYPE_AMMOBELT
	0, // 30 = TRACKER_TYPE_INSTRUMENT_UPG
	1, // 31 = TRACKER_TYPE_DIVE
	1, // 32 = TRACKER_TYPE_ORANGE
	1, // 33 = TRACKER_TYPE_BARREL
	1, // 34 = TRACKER_TYPE_VINE
	0, // 35 = TRACKER_TYPE_CAMERA
	0, // 36 = TRACKER_TYPE_SHOCKWAVE
	0, // 37 = TRACKER_TYPE_KEY1
	0, // 38 = TRACKER_TYPE_KEY2
	0, // 39 = TRACKER_TYPE_KEY3
	0, // 40 = TRACKER_TYPE_KEY4
	0, // 41 = TRACKER_TYPE_KEY5
	0, // 42 = TRACKER_TYPE_KEY6
	0, // 43 = TRACKER_TYPE_KEY7
	0, // 44 = TRACKER_TYPE_KEY8
	0, // 45 = TRACKER_TYPE_MELON_2
	0, // 46 = TRACKER_TYPE_MELON_3
	0, // 47 = TRACKER_TYPE_INSUPG_1
	0, // 48 = TRACKER_TYPE_INSUPG_2
	0, // 49 = TRACKER_TYPE_BELT_1
	0, // 50 = TRACKER_TYPE_BELT_2
	1, // 51 = TRACKER_TYPE_CRANKY
	1, // 52 = TRACKER_TYPE_FUNKY
	1, // 53 = TRACKER_TYPE_CANDY
	1, // 54 = TRACKER_TYPE_SNIDE
	1, // 55 = TRACKER_TYPE_CLIMB
};

int getEnabledState(tracker_struct *segment) {
	/**
	 * @brief Get the enabled state of a tracker item
	 * 
	 * @param index Tracker item index
	 * 
	 * @return State
	 */
	int file_empty = 0;
	int index = segment->type;
	if (CurrentMap == MAP_MAINMENU) {
		file_empty = isFileEmpty(0);
	}
	if (file_empty) { // Empty file check
		return pregiven_status[index];
	}
	if ((index == TRACKER_TYPE_MELON_2) || (index == TRACKER_TYPE_MELON_3)) {
		return CollectableBase.Melons >= (2 + (index - TRACKER_TYPE_MELON_2));
	} else if (index == TRACKER_TYPE_INSUPG_1) {
		return MovesBase[0].instrument_bitfield & 2;
	} else if (index == TRACKER_TYPE_INSUPG_2) {
		return MovesBase[0].instrument_bitfield & 8;
	} else if ((index == TRACKER_TYPE_BELT_1) || (index == TRACKER_TYPE_BELT_2)) {
		return MovesBase[0].ammo_belt > (index - TRACKER_TYPE_BELT_1);
	} else {
		return getItemCount_new(segment->item, segment->level, segment->kong);
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
				if (TrainingMoves_New[i].item.item_type == REQITEM_MOVE) {
					subtype = TrainingMoves_New[i].item.level;
				}
			} else if (i == 4) {
				// First Move
				if (FirstMove_New.item.item_type == REQITEM_MOVE) {
					subtype = FirstMove_New.item.level;
				}
			}
			if (subtype == 3) {
				slam_screen_level += 1;
			} else if (subtype == 7) {
				belt_screen_level += 1;
			} else if (subtype == 9) {
				ins_screen_level += 1;
			}
			
		}
	}
	for (int i = 0; i < (int)(sizeof(tracker_info) / sizeof(tracker_struct)); i++) {
		tracker_info[i].enabled = getEnabledState(&tracker_info[i]);
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
	dl = drawImage(dl, IMAGE_TRACKER, RGBA16, TRACKER_WIDTH, TRACKER_HEIGHT, tracker_x, y_offset + DEFAULT_TRACKER_Y_OFFSET,1.0f, 1.0f,0xFF);
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
static char *flag_strings[] = {
	"PLANDOMIZER",
	"SPOILER GENNED",
	"LOCKED",
	"ARCHIPELAGO",
};

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
	int andi = 0x80;
	int rom_flags = *(unsigned char*)(&Rando.rom_flags);
	for (int i = 0; i < 4; i++) {
		if (rom_flags & andi) {
			dl = displayCenteredText(dl, info_y / 4, flag_strings[i], 1);
			info_y += INFO_Y_DIFF;
		}
		andi >>= 1;
	}
	return dl;
}

void correctKongFaces(void) {
	/**
	 * @brief Alter the kong faces on the file screen to handle pre-given kongs
	 */
	for (int i = 0; i < 5; i++) {
		int has_kong = getItemCount_new(REQITEM_KONG, 0, i);
		KongUnlockedMenuArray[i] = has_kong;
		if (!has_kong) {
			// If you don't have the kong, check the starting moves data
			KongUnlockedMenuArray[i] = (starting_item_data.others.kong_bitfield >> i) & 1;
		}
	}
	if (!getItemCount_new(REQITEM_KONG, 0, KONG_DK)) {
		if ((starting_item_data.others.kong_bitfield & 1) == 0) {
			KongUnlockedMenuArray[0] = 0;
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
	int ins_level = getInstrumentLevel();
	int max = 15 + ((ins_level - 1) * 5); //giving instrument power even if no instrument is unlocked
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
		giveCollectables();
		if (checkFlag(FLAG_COLLECTABLE_LLAMAGB, FLAGTYPE_PERMANENT)) {
			setPermFlag(FLAG_MODIFIER_LLAMAFREE); // No item check
		}
		Character = Rando.starting_kong;
		setFlag(FLAG_HELM_HURRY_DISABLED, 0, FLAGTYPE_PERMANENT);
		if (checkFlag(FLAG_ARCADE_ROUND1, FLAGTYPE_PERMANENT)) {
			setPermFlag(FLAG_ARCADE_LEVER);
		}
		for (int i = 0; i < 7; i++) {
			if (checkFlag(normal_key_flags[i], FLAGTYPE_PERMANENT)) {
				setPermFlag(tnsportal_flags[i]);
			}
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
	initAPCounter();
	resetProgressive();
	updateBarrierCounts();
	if ((Rando.helm_hurry_mode) && (!checkFlag(FLAG_HELM_HURRY_DISABLED, FLAGTYPE_PERMANENT))) {
		QueueHelmTimer = 1;
	}
	setKongIgt();
	ForceStandardAmmo = 0;
}

int testPasswordSequence(void) {
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
	saveAPCounter();
	saveHelmHurryTime();
	saveItemsToFile();
	int new_igt = getNewSaveTime();
	if (canSaveHelmHurry()) {
		int sum = 0;
		for (int i = 0; i < 9; i++) {
			int value = ReadFile(DATA_IGT_JAPES + i, 0, 0, FileIndex);
			sum += value; 
		}
		int diff = new_igt - sum;
		int world = getWorld(previous_map_save, 1);
		if (world < 9) {
			int old = ReadFile(DATA_IGT_JAPES + world, 0, 0, FileIndex);
			SaveToFile(DATA_IGT_JAPES + world, 0, 0, FileIndex, old + diff);
		}
	}
	previous_map_save = CurrentMap;
	updatePercentageKongStat();
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