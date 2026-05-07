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
}