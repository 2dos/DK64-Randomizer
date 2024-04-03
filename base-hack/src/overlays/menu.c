/**
 * @file menu.c
 * @author Ballaam
 * @brief Changes within the menu overlay
 * @version 0.1
 * @date 2023-12-16
 * 
 * @copyright Copyright (c) 2023
 * 
 */

#include "../../include/common.h"

void PatchCrankyCode(void) {
	if (CurrentMap == MAP_CRANKY) {
		int timer = 300;
		*(short*)(0x80027B72) = timer;
		*(short*)(0x80027BCA) = timer;
		*(short*)(0x80027BFA) = timer;
		loadSingularHook(0x80026EFC, &CrankyCoconutDonation);
	} else {
		loadSingularHook(0x80027AE8, &FixInvisibleText_0);
		loadSingularHook(0x80027B30, &FixInvisibleText_1);
	}
}

int give_all_blueprints(int flag, int level, int kong_p) {
	int given_bp = 0;
	for (int kong = 0; kong < 5; kong++) {
		int offset = (level*5) + kong;
		if (checkFlagDuplicate(FLAG_BP_JAPES_DK_HAS + offset, FLAGTYPE_PERMANENT)) {
			int gb_flag = FLAG_BP_JAPES_DK_TURN + offset;
			if (!checkFlag(gb_flag, FLAGTYPE_PERMANENT)) {
				given_bp = 1;
				MovesBase[kong].gb_count[level] += 1;
				setFlag(gb_flag, 1, FLAGTYPE_PERMANENT);
			}
		}
	}
	return given_bp;
}

void gbUpdateHandler(void) {
	updateGBCountHUD(0);
	handleProgressiveIndicator();
}

void overlay_mod_menu(void) {
	// Shops
	PatchCrankyCode(); // Change cranky code to handle an extra variable
	if (CurrentMap == MAP_CRANKY) {
		*(short*)(0x80026FBA) = 3; // Coconut giving cutscene
		*(short*)(0x80026E6A) = 0xBD; // Cranky
		*(short*)(0x80026E8E) = 5; // Coconuts
		*(short*)(0x80026FB2) = 9999; // Change coconut gift from 6.6 coconuts to 66.6 coconuts
	}

	// Menu
	if (Rando.default_camera_mode) {
		InvertedControls = 1;
	}

	// Options
	if (ENABLE_FILENAME) {
		initFilename();
	}

	// Force enable cheats
	*(short*)(0x800280DC) = 0x1000; // Force access to mystery menu
	*(short*)(0x80028A40) = 0x1000; // Force opaqueness
	*(short*)(0x8002EA7C) = 0x1000; // Disable Cutscene Menu
	*(short*)(0x8002EAF8) = 0x1000; // Disable Minigames Menu
	*(short*)(0x8002EB70) = 0x1000; // Disable Bosses Menu
	*(int*)(0x8002EBE8) = 0; // Disable Krusha Menu
	*(short*)(0x8002EC18) = 0x1000; // Enable Cheats Menu
	*(int*)(0x8002E8D8) = 0x240E0004; // Force cheats menu to start on page 4
	*(short*)(0x8002E8F4) = 0x1000; // Disable edge cases
	*(int*)(0x8002E074) = 0xA06F0000; // overflow loop to 1
	*(int*)(0x8002E0F0) = 0x5C400004; // underflow loop from 1
	*(short*)(0x8002EA3A) = 0xFFFE; // Disable option 1 load
	*(int*)(0x8002EA4C) = 0xA0600003; // Force Krusha to 0
	*(int*)(0x8002EA64) = 0xA64B0008; // Disable option 1 write

	// Snide
	*(int*)(0x8002402C) = 0x240E000C; // No extra contraption cutscenes
	*(int*)(0x80024054) = 0x24080001; // 1 GB Turn in
	if (Rando.item_rando) {		
		writeFunction(0x80024CF0, &countFlagsDuplicate); // Flag change to FLUT
		writeFunction(0x80024854, &checkFlagDuplicate); // Flag change to FLUT
		writeFunction(0x80024880, &checkFlagDuplicate); // Flag change to FLUT
		writeFunction(0x800248B0, &setFlagDuplicate); // Flag change to FLUT
		if (Rando.quality_of_life.blueprint_compression) {
			writeFunction(0x80024840, &give_all_blueprints); // Change initial check
			*(int*)(0x80024850) = 0xAFA90040; // SW $t1, 0x40 ($sp)
			*(int*)(0x80024854) = 0; // NOP
			*(short*)(0x8002485C) = 0x1000; // Force Branch
		}
	}
	if (Rando.colorblind_mode != COLORBLIND_OFF) {
		int colorblind_offset = 5 * (Rando.colorblind_mode - 1);
		for (int i = 0; i < 16; i++) {
			int mapping = i / 3;
			if (mapping == 5) {
				mapping = 4;
			}
			rgb color = colorblind_colors[colorblind_offset + mapping];
			BlueprintLargeImageColors[i].red = color.red;
			BlueprintLargeImageColors[i].green = color.green;
			BlueprintLargeImageColors[i].blue = color.blue;
		}
	}

	// Menu Overlay - Candy's Shop Glitch
	*(short*)(0x80027678) = 0x1000;
	*(short*)(0x8002769C) = 0x1000;
}