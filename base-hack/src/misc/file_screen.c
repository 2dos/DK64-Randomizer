#include "../../include/common.h"

static char file_percentage[5] = "";
// static char golden_count[4] = "";
static char balanced_igt[20] = "";
// static char blueprints_count[5] = "";
// static char move_count_str[10] = "";

#define LINE_GAP 0x8C

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
	// File Percentage
	int y = FileScreenDLOffset - 320;
	if (CutsceneActive != 6) {
		if (ReadFile(0xD,0,0,FileIndex)) {
			file_mode = FILEMODE_USED;
		} else {
			file_mode = FILEMODE_NEW;
		}
	}
	if (file_mode == FILEMODE_USED) {
		// File Percentage
		dk_strFormat((char*)file_percentage, "%d%%", FilePercentage);
		dl = displayText(dl,1,0x280,y,(char*)file_percentage,0x81);
		// Balanced IGT
		y += LINE_GAP;
		int secs = IGT % 60;
		float secsf = secs;
		secsf /= 60;
		int hm = IGT / 60;
		int minutes = hm % 60;
		int hours = hm / 60;
		dk_strFormat((char*)balanced_igt, "%03d:%02d:%02d",hours,minutes,secs);
		dl = displayText(dl,1,0x280,y,(char*)balanced_igt,0x81);
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
void correctKongFaces(void) {
	if (Rando.unlock_kongs) {
		for (int i = 0; i < 5; i++) {
			int flag = checkFlag(kong_flags[i],0);
			KongUnlockedMenuArray[i] = flag;
			if (!flag) {
				KongUnlockedMenuArray[i] = (Rando.unlock_kongs & (1 << i)) != 0;
			}
		}
		if (!checkFlag(FLAG_KONG_DK,0)) {
			if ((Rando.unlock_kongs & 1) == 0) {
				KongUnlockedMenuArray[0] = 0;
			}
		}
	} else {
		for (int i = 0; i < 5; i++) {
			KongUnlockedMenuArray[i] = checkFlag(kong_flags[i],0);
		}
		KongUnlockedMenuArray[(int)Rando.starting_kong] = 1;
		if (Rando.starting_kong != 0) {
			if (!checkFlag(FLAG_KONG_DK,0)) {
				KongUnlockedMenuArray[0] = 0;
			}
		}
	}
}