#include "../../include/common.h"

static char file_percentage[5] = "";
static char golden_count[4] = "";
static char balanced_igt[20] = "";
static char bp_count_str[5] = "";
static char move_count_str[10] = "";
static short igt_h = 0;
static short igt_m = 0;
static short igt_s = 0;
static unsigned char move_count;
static unsigned char bp_count;

#define LINE_GAP 0x8C

typedef struct menu_controller_paad {
	/* 0x000 */ float screen_transition_progress;
	/* 0x004 */ float unk_4;
	/* 0x008 */ char unk_8[0x12-0x8];
	/* 0x012 */ unsigned char current_screen;
	/* 0x013 */ unsigned char next_screen;
	/* 0x014 */ char unk_14[0x16-0x14];
	/* 0x016 */ char prevent_action;
	/* 0x017 */ char selected_action;
} menu_controller_paad;

typedef enum file_screen_modes {
	/* 0x000 */ FILEMODE_NEW,
	/* 0x001 */ FILEMODE_USED,
} file_screen_modes;

int* display_images(int* dl, file_screen_modes mode) {
	int y_offset = FileScreenDLOffset - 720;
	for (int i = 0; i < 8; i++) {
		int key_there = checkFlag(FLAG_KEYIN_KEY1 + i,0);
		if (!key_there) {
			if (Rando.keys_preturned & (1 << i)) {
				key_there = 1;
			}
		}
		float divisor = (key_there ^ 1) + 1;
		if (divisor == 0) {
			divisor = 1;
		}
		float opacity_mult = 1.0f / divisor;
		float opacity_f = 255 * opacity_mult;
		int opacity_i = opacity_f;
		if (opacity_i > 255) {
			opacity_i = 255;
		}
		dl = drawImage(dl, 107 + i, RGBA16, 32, 32, 900 + (150 * (i % 2)), (520 + y_offset + (80 * (i / 2))),4.0f, 4.0f,opacity_i);
	}
	/*
		dl = drawImage(dl, 115, RGBA16, 32, 32, 200, y_offset + 450,4.0f, 4.0f,0xFF); // Cranky Head
		dl = drawImage(dl, 116, RGBA16, 32, 32, 500, y_offset + 720,3.0f, 3.0f,0xFF); // Blueprint
	*/
	return dl;
}

static file_screen_modes file_mode = FILEMODE_NEW;

int getTextIndexFromMove(purchase_struct* info) {
	if (info->purchase_type != -1) {
		switch (info->purchase_type) {
			case PURCHASE_MOVES:
				return SpecialMovesNames[(int)((info->move_kong * 4) + info->purchase_value)].name;
				break;
			case PURCHASE_SLAM:
				return SimianSlamNames[(int)info->purchase_value].name;
				break;
			case PURCHASE_GUN:
				if (info->purchase_value == 1) {
					return GunNames[(int)info->move_kong];
				} else {
					return GunUpgNames[(int)info->purchase_value];
				}
				break;
			case PURCHASE_AMMOBELT:
				return AmmoBeltNames[(int)info->purchase_value];
				break;
			case PURCHASE_INSTRUMENT:
				if (info->purchase_value == 1) {
					return InstrumentNames[(int)info->move_kong];
				} else {
					return InstrumentUpgNames[(int)info->purchase_value];
				}
				break;
			case PURCHASE_FLAG:
				{
					if (info->purchase_value == -2) {
						return 59;
					} else {
						int tied_flags[] = {FLAG_TBARREL_DIVE,FLAG_TBARREL_ORANGE,FLAG_TBARREL_BARREL,FLAG_TBARREL_VINE,FLAG_ABILITY_CAMERA,FLAG_ABILITY_SHOCKWAVE};
						for (int i = 0; i < sizeof(tied_flags) / 4; i++) {
							if (tied_flags[i] == info->purchase_value) {
								return 53 + i;
							}
						}
					}
				}
			break;
		}
	}
	return -1;
}

int* display_text(int* dl) {
	// Display Background
	LevelStateBitfield &= 0xFFFFFFEF;
	// File Percentage
	// int y = FileScreenDLOffset - 320;
	if (CutsceneActive != 6) {
		if (ReadFile(0xD,0,0,FileIndex)) {
			file_mode = FILEMODE_USED;
		} else {
			file_mode = FILEMODE_NEW;
		}
	}
	if (file_mode == FILEMODE_USED) {
		int y_gap = 110;
		int y_start = (FileScreenDLOffset - 320) - y_gap - 144;
		int y_offset = y_start;
		// Move Count
		y_offset += y_gap;
		dk_strFormat((char*)move_count_str, "%02dl35", move_count);
		dl = printText(dl, 325, y_offset, 0.6f, (char*)move_count_str);
		// File Percentage
		y_offset += y_gap;
		dk_strFormat((char*)file_percentage, "%d%%", FilePercentage);
		int perc_x = 276;
		if (FilePercentage > 99) {
			perc_x = 310;
		} else if (FilePercentage > 9) {
			perc_x = 300;
		}
		dl = printText(dl, perc_x, y_offset, 0.6f, (char*)file_percentage);
		// GB Count
		y_offset += y_gap;
		dk_strFormat((char*)golden_count, "%03dl201",FileGBCount);
		dl = printText(dl, 375, y_offset, 0.6f, (char*)golden_count);
		// BP Count
		y_offset += y_gap;
		dk_strFormat((char*)bp_count_str, "%02dl40", bp_count);
		dl = printText(dl, 325, y_offset, 0.6f, (char*)bp_count_str);
		// Balanced IGT
		y_offset += y_gap;
		dk_strFormat((char*)balanced_igt, "%03d:%02d:%02d",igt_h,igt_m,igt_s);
		dl = printText(dl, 390, y_offset, 0.6f, (char*)balanced_igt);
	} else { // New File
		// Move List
		char* move_names[7] = {0,0,0,0,0,0,0};
		if (Rando.unlock_moves) {
			move_names[0] = "EVERYTHING";
		} else {
			move_names[0] = getTextPointer(39,SimianSlamNames[1].name,1); // Slam
			int position_index = 1;
			if (Rando.fast_start_beginning) {
				for (int i = 0; i < 4; i++) {
					if (TrainingMoves_New[i].purchase_value == -2) {
						move_names[position_index] = getTextPointer(39,57,1);
						move_names[position_index+1] = getTextPointer(39,58,1);
						position_index += 2;
					} else {
						int move_index = getTextIndexFromMove(&TrainingMoves_New[i]);
						if (move_index > -1) {
							move_names[position_index] = getTextPointer(39,move_index,1); // Training Moves
							position_index += 1;
						}
					}
				}
			}
			if (Rando.camera_unlocked) {
				move_names[position_index] = getTextPointer(39,57,1);
				move_names[position_index+1] = getTextPointer(39,58,1);
				position_index += 1;
			}
		}
		int list_start = -144;
		int y_offset = (FileScreenDLOffset - 320) - 65 + list_start;
		int x_offset = 375;
		dl = printText(dl, x_offset, y_offset, 0.6f, "STARTING MOVES:");
		for (int i = 0; i < sizeof(move_names)/4; i++) {
			if (move_names[i]) {
				y_offset = (FileScreenDLOffset - 320) + (i * 65) + list_start;
				dl = printText(dl, x_offset, y_offset, 0.6f, move_names[i]);
			}
		}
	}
	// // Move Count
	// int move_count = 1;
	// if (Rando.camera_unlocked) {
	// 	move_count += 2;
	// }
	// if (Rando.unlock_moves) {
	// 	move_count += 33; // All moves except camera and shockwave
	// 	if (!Rando.camera_unlocked) {
	// 		if (checkFlag(FLAG_ABILITY_CAMERA,0)) {
	// 			move_count += 1;
	// 		}
	// 		if (checkFlag(FLAG_ABILITY_SHOCKWAVE,0)) {
	// 			move_count += 1;
	// 		}
	// 	}
	// } else {
	// 	if ((!Rando.camera_unlocked)) {
	// 		if (checkFlag(FLAG_ABILITY_CAMERA,0)) {
	// 			move_count += 1;
	// 		}
	// 		if (checkFlag(FLAG_ABILITY_SHOCKWAVE,0)) {
	// 			move_count += 1;
	// 		}
	// 	}
	// 	if (MovesBase[0].simian_slam > 1) {
	// 		move_count += (MovesBase[0].simian_slam - 1); // Simian Slam
	// 	}
	// 	move_count += MovesBase[0].ammo_belt;
	// 	int btf_value = MovesBase[0].weapon_bitfield >> 1;
	// 	for (int i = 0; i < 2; i++) {
	// 		move_count += (btf_value & 1);
	// 		btf_value >>= 1;
	// 	}
	// 	move_count += (MovesBase[0].instrument_bitfield >> 1) & 1;
	// 	move_count += (MovesBase[0].instrument_bitfield >> 3) & 1;
	// 	for (int i = 0; i < 5; i++) {
	// 		move_count += (MovesBase[i].weapon_bitfield & 1); // Base Gun
	// 		move_count += (MovesBase[i].instrument_bitfield & 1); // Base Instrument
	// 		btf_value = MovesBase[i].special_moves;
	// 		for (int j = 0; j < 3; j++) {
	// 			move_count += btf_value & 1;
	// 			btf_value >>= 1;
	// 		}
	// 	}
	// }
	// dk_strFormat((char*)move_count_str, "%02d", move_count);
	// dl = displayText(dl,1,0x140,y,(char*)move_count_str,0x81);	
	// // GB Count
	// y += LINE_GAP;
	// dk_strFormat((char*)golden_count, "%03d", FileGBCount);
	// dl = displayText(dl,1,0x280,y,(char*)golden_count,0x81);
	// // Blueprint Count
	// y += LINE_GAP;
	// int blueprints = countFlagArray(0x1D5,40,0);
	// dk_strFormat((char*)blueprints_count, "%02d", blueprints);
	// dl = displayText(dl,1,0x280,y,(char*)blueprints_count,0x81);

	
	// Image Render
	dl = display_images(dl,file_mode);
	return dl;
}

static unsigned char hash_textures[] = {48,49,50,51,55,62,63,64,65,76};
int* displayHash(int* dl, int y_offset) {
	for (int i = 0; i < 5; i++) {
		int hash_index = Rando.hash[i] % 10;
		dl = drawImage(dl, hash_textures[hash_index], RGBA16, 32, 32, 440 + (100 * i), 920 - y_offset, 3.0f, 3.0f, 0xFF);
	}
	return dl;
}

int* displayHeadTexture(int* dl, int texture, float x, float y, float scale) {
	int kong_index = texture & 0x7F;
	int draw_scale = 1;
	int x_offset = 60;
	if (kong_index < 3) {
		menuHeadX[kong_index] = (x * 3) + 550 + x_offset;
		menuHeadY[kong_index] = (y * 3) + 0;
	} else {
		menuHeadX[kong_index] = (x * 2.75f) + 204 + x_offset;
		menuHeadY[kong_index] = (y * 2.75f) + 130;
	}
	menuHeadScale[kong_index] = scale * draw_scale;
	return dl;
}

static const short kong_flags[] = {FLAG_KONG_DK,FLAG_KONG_DIDDY,FLAG_KONG_LANKY,FLAG_KONG_TINY,FLAG_KONG_CHUNKY};

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

void file_progress_screen_code(actorData* actor, int buttons) {
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
					unlockMoves();
					applyFastStart();
					openCrownDoor();
					giveCollectables();
					activateBananaports();
					if(Rando.fast_gbs) {
						setPermFlag(FLAG_RABBIT_ROUND1); //Start race at round 2
					}
					setPermFlag(FLAG_ESCAPE);
					Character = Rando.starting_kong;
					StoredSettings.file_extra[(int)FileIndex].location_sss_purchased = 0;
					StoredSettings.file_extra[(int)FileIndex].location_ab1_purchased = 0;
					StoredSettings.file_extra[(int)FileIndex].location_ug1_purchased = 0;
					StoredSettings.file_extra[(int)FileIndex].location_mln_purchased = 0;
					SaveToGlobal();
				} else {
					// Dirty File
					Character = Rando.starting_kong;
					determineStartKong_PermaLossMode();
					giveCollectables();
				}
				ForceStandardAmmo = 0;
			} else if (buttons & 2) { // B
				playSFX(0x2C9);
				paad->prevent_action = 0;
				paad->next_screen = 1;
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

static char top_text[10] = "EMPTY";

int* displayTopText(int* dl, short x, short y, float scale) {
	if (isFileEmpty(0)) {
		// Display Empty Text
		dk_strFormat((char*)top_text,"%s","EMPTY");
	} else {
		// Display "Game %d" Text
		dk_strFormat((char*)top_text,"%s %d","GAME",*(char*)(0x80033F48)+1);
	}
	return printText(dl, x, y, scale, (char*)top_text);
}

void FileProgressInit(actorData* menu_controller) {
	menu_controller_paad* paad = menu_controller->paad;
	loadFile(0,0);
	if (isFileEmpty(0)) {
		// Empty
	} else {
		// Not Empty
		displayMenuSprite(paad, sprite_table[59], 35, 125, 0.6f, 2, 0); // GB
		// displayMenuSprite(paad, sprite_table[0x70], 0xA2, 0xD6, 0.75f, 2, 5); // Z - Delete
		// displayMenuSprite(paad, sprite_table[0x94], 35, 65, 0.6f, 2, 5); // Cranky Face - Moves
		int blueprint_sprite_indexes[] = {0x5C,0x5A,0x4A,0x5D,0x5B};
		// displayMenuSprite(paad, sprite_table[blueprint_sprite_indexes[0]], 35, 155, 0.75, 2, 5); // Blueprint
	}
	displayMenuSprite(paad, sprite_table[0x6F], 0x23, 0xD2, 0.75f, 2, 0); // B
	displayMenuSprite(paad, sprite_table[0x6E], 0x122, 0xD2, 0.75f, 2, 0); // A
	*(float*)(0x80033F4C) = 1600.0f;
	for (int i = 0; i < 5; i++) {
		if (Rando.unlock_kongs & (1 << i)) {
			KongUnlockedMenuArray[i] = 1;
		} else {
			KongUnlockedMenuArray[i] = 0;
		}
	}
	KongUnlockedMenuArray[(int)Rando.starting_kong] = 1;
	for (int i = 0; i < 5; i++) {
		if (checkFlag(kong_flags[i],0)) {
			KongUnlockedMenuArray[i] = 1;
		}
	}
	for (int i = 0; i < 5; i++) {
		void* sprite = sprite_table[0x92];
		if (KongUnlockedMenuArray[i]) {
			sprite = sprite_table[0xA9 + i];
		}
		displayMenuSprite(paad, sprite, i, i, 0.8f, 2, 0xF);
	}
	int gb_count = 0;
	for (int kong = 0; kong < 5; kong++) {
		for (int level = 0; level < 8; level++) {
			gb_count += MovesBase[kong].gb_count[level];
		}
	}
	int bp_count_local = 0;
	for (int i = 0; i < 40; i++) {
		bp_count_local += checkFlag(469+i,0);
	}
	int move_count_local = 0;
	if (Rando.unlock_moves) {
		move_count_local = 39; // 38 if we discount 3rd melon
	} else {
		move_count_local += MovesBase[0].simian_slam;
		move_count_local += MovesBase[0].ammo_belt;
		for (int kong = 0; kong < 5; kong++) {
			for (int level = 0; level < 3; level++) {
				if (MovesBase[kong].special_moves & (1 << level)) {
					move_count_local += 1;
				}
			}
			move_count_local += (MovesBase[kong].weapon_bitfield & 1);
			move_count_local += (MovesBase[kong].instrument_bitfield & 1);
		}
		for (int level = 0; level < 3; level++) {
			if (level < 2) {
				if (MovesBase[0].weapon_bitfield & (1 << level)) {
					move_count_local += 1;
				}
			}
			if (MovesBase[0].instrument_bitfield & (1 << level)) {
				move_count_local += 1; // Discount level == 1 if discounting 3rd melon
			}
		}
		move_count_local += checkFlag(FLAG_TBARREL_DIVE,0);
		move_count_local += checkFlag(FLAG_TBARREL_ORANGE,0);
		move_count_local += checkFlag(FLAG_TBARREL_BARREL,0);
		move_count_local += checkFlag(FLAG_TBARREL_VINE,0);
	}
	if (Rando.camera_unlocked) {
		move_count_local += 2;
	} else {
		move_count_local += checkFlag(FLAG_ABILITY_CAMERA,0);
		move_count_local += checkFlag(FLAG_ABILITY_SHOCKWAVE,0);
	}
	FileGBCount = gb_count;
	igt_h = (IGT / 60) / 60;
	igt_m = (IGT / 60) % 60;
	igt_s = IGT - (3600 * igt_h) - (60 * igt_m);
	FilePercentage = calculateFilePercentage();
	bp_count = bp_count_local;
	move_count = move_count_local;
}