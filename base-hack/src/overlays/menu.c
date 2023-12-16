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

static const char moves_values[] = {1,1,3,1,7,1,1,7}; // Move values for the main menu changes

void crossKongInit(void) {
	/**
	 * @brief Cross-Kong Purchases. Change code to add a variable inside the shop_paad
	 */
	// Change target kong (Progressive)
	*(int*)(0x80025EA0) = 0x90850004; // LBU 	a1, 0x4 (a0)
	// Change target kong (Bitfield)
	*(int*)(0x80025E80) = 0x90850004; // LBU 	a1, 0x4 (a0)
	// Change price deducted
	*(int*)(0x80025F70) = 0x93060005; // LBU 	a2, 0x5 (t8)
	// Change price check
	*(int*)(0x80026200) = 0x90CF0005; // LBU 	t7, 0x5 (a2)
	// Change Special Moves Text
	*(int*)(0x80027AE0) = 0x910F0004; // LBU 	t7, 0x4 (t0)
	// Change Gun Text
	*(int*)(0x80027BA0) = 0x91180004; // LBU 	t8, 0x4 (t0)
	// Change Instrument Text
	*(int*)(0x80027C14) = 0x910C0004; // LBU 	t4, 0x4 (t0)
	// Fix post-special move text
	*(int*)(0x80026C08) = 0x91790011; // LBU 	t9, 0x11 (t3)
	*(int*)(0x80026C00) = 0x916D0004; // LBU 	t5, 0x4 (t3)
}

void PatchCrankyCode(void) {
	loadSingularHook(0x800260E0, &CrankyDecouple);
	loadSingularHook(0x800260A8, &ForceToBuyMoveInOneLevel);
	*(int*)(0x80026160) = 0;
	loadSingularHook(0x80026140, &PriceKongStore);
	loadSingularHook(0x80025FC0, &CharacterCollectableBaseModify);
	loadSingularHook(0x800260F0, &SetMoveBaseBitfield);
	loadSingularHook(0x8002611C, &SetMoveBaseProgressive);
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
	loadSingularHook(0x80026924, &AlwaysCandyInstrument);
	*(short*)(0x80026072) = getHi(&CrankyMoves_New);
	*(short*)(0x8002607A) = getLo(&CrankyMoves_New);
	*(short*)(0x8002607E) = getHi(&CandyMoves_New);
	*(short*)(0x80026086) = getLo(&CandyMoves_New);
	*(short*)(0x8002608A) = getHi(&FunkyMoves_New);
	*(short*)(0x8002608E) = getLo(&FunkyMoves_New);
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

void overlay_mod_menu(void) {
	// Shops
	PatchCrankyCode(); // Change cranky code to handle an extra variable
	*(int*)(0x80025E9C) = 0x0C009751; // Change writing of move to "write bitfield move" function call
	writeJetpacMedalReq(); // Adjust medal requirement for Jetpac
	// Apply shop hints
	if (Rando.shop_hints) {
		writeFunction(0x8002661C, &getMoveHint);
		writeFunction(0x800265F0, &getMoveHint);
	}
	// Change move purchase
	writeFunction(0x80026720, &getNextMovePurchase);
	writeFunction(0x8002683C, &getNextMovePurchase);
	crossKongInit();
	// Write Modified purchase move stuff
	writeFunction(0x80027324, &purchaseMove);
	writeFunction(0x8002691C, &purchaseMove);
	writeFunction(0x800270B8, &showPostMoveText);
	writeFunction(0x80026508, &canPlayJetpac);
	*(int*)(0x80026F64) = 0; //  Disable check for whether you have a move before giving donation at shop
	*(int*)(0x80026F68) = 0; //  Disable check for whether you have a move before giving donation at shop
	if (CurrentMap == MAP_CRANKY) {
		*(short*)(0x80026FBA) = 3; // Coconut giving cutscene
		*(short*)(0x80026E6A) = 0xBD; // Cranky
		*(short*)(0x80026E8E) = 5; // Coconuts
		*(short*)(0x80026FB2) = 9999; // Change coconut gift from 6.6 coconuts to 66.6 coconuts
	}

	// Menu
	*(short*)(0x8002E266) = 7; // Enguarde Arena Movement Write
	*(short*)(0x8002F01E) = 7; // Rambi Arena Movement Write
	for (int i = 0; i < 8; i++) {
		// Main Menu moves given upon entering a boss/minigame
		MainMenuMoves[i].moves = moves_values[i];
	}
	// Main Menu visual changes
	writeFunction(0x80030604, &file_progress_screen_code); // New file progress code
	writeFunction(0x80029FE0, &wipeFileMod); // Wipe File Hook
	writeFunction(0x80028C88, &enterFileProgress); // Enter File Progress Screen Hook
	*(int*)(0x80029818) = 0; // Hide A
	*(int*)(0x80029840) = 0; // Hide B
	// *(int*)(0x80029874) = 0; // Hide GB
	int gb_x = 208;
	int gh_y = 0x9A;
	if (Rando.true_widescreen) {
		gb_x = (SCREEN_WD >> 1) + 48; 
		gh_y -= (DEFAULT_TRACKER_Y_OFFSET - getTrackerYOffset());
	}
	*(short*)(0x8002986E) = gb_x; // Move GB to right
	*(short*)(0x80029872) = gh_y; // Move GB down
	*(short*)(0x8002985A) = 0; // Change sprite mode for GB
	*(float*)(0x80033CA8) = 0.4f; // Change GB Scale

	// File Select
	*(int*)(0x80028CB0) = 0xA0600000; // SB $r0, 0x0 (v0) - Always view file index 0
	*(int*)(0x80028CC4) = 0; // Prevent file index overwrite
	*(int*)(0x80028F88) = 0; // File 2 render
	*(int*)(0x80028F60) = 0; // File 2 Opacity
	*(int*)(0x80028FCC) = 0; // File 3 render
	*(int*)(0x80028FA4) = 0; // File 3 Opacity
	writeFunction(0x80028D04, &changeFileSelectAction); // File select change action
	writeFunction(0x80028D10, &changeFileSelectAction_0); // File select change action
	*(int*)(0x80028DB8) = 0x1040000A; // BEQ $v0, $r0, 0xA - Change text signal
	*(short*)(0x80028CA6) = 5; // Change selecting orange to delete confirm screen

	*(int*)(0x80028EF8) = 0; // Joystick

	if (Rando.default_camera_mode) {
		InvertedControls = 1;
	}

	// Options
	initOptionScreen();
	// Disable Multiplayer
	*(int*)(0x800280B0) = 0; // Disable access
	*(int*)(0x80028A8C) = 0; // Lower Sprite Opacity
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