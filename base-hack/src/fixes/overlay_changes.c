/**
 * @file overlay_changes.c
 * @author Ballaam
 * @brief Changes which need to be applied on overlay initialization
 * @version 0.1
 * @date 2022-01-12
 * 
 * @copyright Copyright (c) 2022
 * 
 */

#include "../../include/common.h"

#define FUNKY 1
#define CRANKY 5
#define CANDY 0x19
#define MAIN_MENU 0x50
#define SNIDE 0xF

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

static const unsigned char boss_maps[] = {0x8,0xC5,0x9A,0x6F,0x53,0xC4,0xC7,0xCB,0xCC,0xCD,0xCE,0xCF,0xD6}; // Boss Maps

void arcadeExit(void) {
	/**
	 * @brief Arcade exit procedure to fix a bug with Arcade if you have R2 Reward before R1 Reward
	 */
	if (!ArcadeExited) {
		if ((ArcadeEnableReward) && (ArcadeStoryMode)) {
			if (!checkFlag(FLAG_ARCADE_ROUND1, 0)) {
				setFlag(0x10, 1, 2); // Spawn R1 Reward
			} else if (!checkFlag(FLAG_COLLECTABLE_NINTENDOCOIN, 0)) {
				setFlag(0x11, 1, 2); // Spawn R2 Reward
			}
		}
		if (!ArcadeStoryMode) {
			initiateTransition(0x50, 0);
		} else {
			ExitFromBonus();
		}
		ArcadeExited = 1;
	}
}

int determineArcadeLevel(void) {
	/**
	 * @brief Determines the arcade level based on R1 & Nin Coin flags
	 */
	if (checkFlag(FLAG_ARCADE_ROUND1, 0)) {
		if (checkFlag(FLAG_COLLECTABLE_NINTENDOCOIN, 0)) {
			ArcadeMap = 8;
			return 0;
		}
		ArcadeMap = 4;
		return 0;
	}
	ArcadeMap = 0;
	return 0;
}

void HandleArcadeVictory(void) {
	/**
	 * @brief Determine how to handle where to send the player after beating a stage in DK Arcade
	 */
	if ((ArcadeStoryMode) && ((ArcadeMap & 3) == 0)) {
		ArcadeEnableReward = 1;
		if (ArcadeScores[4] < ArcadeCurrentScore) {
			sendToHiScorePage();
		} else {
			arcadeExit();
		}
	} else {
		sendToNextMap();
	}
}

/*
	Arcade Reward Indexes:
	0 - Nintendo Coin / No Item
	1 - Bean
	2 - Blueprint
	3 - Crown
	4 - Fairy
	5 - GB
	6 - Key
	7 - Medal
	8 - Pearl
	9 - Potion (DK)
	10 - Potion (Diddy)
	11 - Potion (Lanky)
	12 - Potion (Tiny)
	13 - Potion (Chunky)
	14 - Potion (Any)
	15 - DK
	16 - Diddy
	17 - Lanky
	18 - Tiny
	19 - Chunky
	20 - Rainbow Coin
	21 - RW Coin
	22 - Melon

	Jetpac Reward Indexes:
	0 - Rareware Coin / No Item
	1 - Bean
	2 - Blueprint
	3 - Crown
	4 - Fairy
	5 - GB
	6 - Key
	7 - Medal
	8 - Pearl
	9 - Potion
	10 - Kong
	11 - Rainbow Coin
	12 - Nintendo Coin
	13 - Melon
*/
#define ARCADE_IMAGE_COUNT 22

void* getFile(int size, int rom) {
	/**
	 * @brief Get file from ROM
	 */
	int* file_size;
	*(int*)(&file_size) = size;
	void* loc = dk_malloc(size);
	copyFromROM(rom,loc,&file_size,0,0,0,0);
	return loc;
}

void* getPointerFile(int table, int file) {
	/**
	 * @brief Get a pointer table file without using getMapData for instances where getMapData will crash the game.
	 */
	int ptr_offset = 0x101C50;
	int* ptr_table = getFile(32*4, ptr_offset);
	int table_addr = ptr_table[table] + ptr_offset;
	int* table_loc = getFile(8, table_addr + (file * 4));
	int file_start = table_loc[0] + ptr_offset;
	int file_end = table_loc[1] + ptr_offset;
	int file_size = file_end - file_start;
	return getFile(file_size, file_start);
}

void initArcade(void) {
	/**
	 * @brief Initialize DK Arcade Changes
	 */
	// Address of Nintendo Coin Image write: 0x8002E8B4/0x8002E8C0
	*(int*)(0x80024F10) = 0x240E0005; // ADDIU $t6, $r0, 0x5
	*(short*)(0x80024F2A) = 0xC71B;
	*(int*)(0x80024F2C) = 0xA0CEC71B; // SB $t6, 0xC71B ($a2)
	*(int*)(0x80024D5C) = 0x0C000000 | (((int)&arcadeExit & 0xFFFFFF) >> 2);
	*(int*)(0x800257B4) = 0x0C000000 | (((int)&arcadeExit & 0xFFFFFF) >> 2);
	*(int*)(0x8002B6D4) = 0x0C000000 | (((int)&arcadeExit & 0xFFFFFF) >> 2);
	*(int*)(0x8002FA58) = 0x0C000000 | (((int)&arcadeExit & 0xFFFFFF) >> 2);
	// Fix arcade level setting logic
	*(int*)(0x80024F34) = 0x0C000000 | (((int)&determineArcadeLevel & 0xFFFFFF) >> 2); // Change log
	*(int*)(0x80024F70) = 0; // Prevent level set
	*(int*)(0x80024F50) = 0; // Prevent level set
	// Arcade Level Order Rando
	for (int i = 0; i < 4; i++) {
		ArcadeBackgrounds[i] = Rando.arcade_order[i];
	}
	*(int*)(0x8002F7BC) = 0x0C000000 | (((int)&HandleArcadeVictory & 0xFFFFFF) >> 2);
	*(int*)(0x8002FA68) = 0x0C000000 | (((int)&HandleArcadeVictory & 0xFFFFFF) >> 2);
	*(short*)(0x8002FA24) = 0x1000;
	// Load Arcade Sprite
	if ((*(unsigned short*)(0x8002E8B6) == 0x8004) && (*(unsigned short*)(0x8002E8BA) == 0xAE58) && (Rando.arcade_reward > 0)) {
		// Change Arcade Reward Sprite
		// Ensure code is only run once
		void* addr = getPointerFile(6, Rando.arcade_reward - 1);
		*(unsigned short*)(0x8002E8B6) = getHi(addr);
		*(unsigned short*)(0x8002E8BA) = getLo(addr);
	}
}

static char jetpacRewardText[] = "REWARD COLLECTED";

void initJetpac(void) {
	/**
	 * @brief Initialize Jetpac Changes.
	 */
	if ((*(int*)(0x8002D9F8) == 0x8002D868) && (Rando.jetpac_reward > 0)) {
		// Change Jetpac Reward Sprite
		// Ensure code is only run once
		*(int*)(0x8002D9F8) = (int)getPointerFile(6, Rando.jetpac_reward - 1 + ARCADE_IMAGE_COUNT);
	}
	if (Rando.item_rando) {
		*(short*)(0x80024D8E) = getHi(&jetpacRewardText);
		*(short*)(0x80024D96) = getLo(&jetpacRewardText);
	}
	if (Rando.fast_gbs) {
		*(short*)(0x80027DCA) = 2500; // Jetpac score requirement
	}
}

void overlay_changes(void) {
	/**
	 * @brief All changes upon loading an overlay
	 */
	if ((CurrentMap == CRANKY) || (CurrentMap == CANDY) || (CurrentMap == FUNKY)) {
		PatchCrankyCode(); // Change cranky code to handle an extra variable
		*(int*)(0x80025E9C) = 0x0C009751; // Change writing of move to "write bitfield move" function call
		writeJetpacMedalReq(); // Adjust medal requirement for Jetpac
		// Apply shop hints
		int func_call = 0;
		if (Rando.shop_hints) {
			func_call = 0x0C000000 | (((int)&getMoveHint & 0xFFFFFF) >> 2);
			*(int*)(0x8002661C) = func_call;
			*(int*)(0x800265F0) = func_call;
		}
		// Change move purchase
		func_call = 0x0C000000 | (((int)&getNextMovePurchase & 0xFFFFFF) >> 2);
		*(int*)(0x80026720) = func_call;
		*(int*)(0x8002683C) = func_call;
		crossKongInit();
		// Write Modified purchase move stuff
		func_call = 0x0C000000 | (((int)&purchaseMove & 0xFFFFFF) >> 2);
		*(int*)(0x80027324) = func_call;
		*(int*)(0x8002691C) = func_call;
		*(int*)(0x800270B8) = 0x0C000000 | (((int)&showPostMoveText & 0xFFFFFF) >> 2);
		*(int*)(0x80026508) = 0x0C000000 | (((int)&canPlayJetpac & 0xFFFFFF) >> 2);
		*(int*)(0x80026F64) = 0; //  Disable check for whether you have a move before giving donation at shop
		*(int*)(0x80026F68) = 0; //  Disable check for whether you have a move before giving donation at shop
		if (CurrentMap == CRANKY) {
			*(short*)(0x80026FBA) = 3; // Coconut giving cutscene
			*(short*)(0x80026E6A) = 0xBD; // Cranky
			*(short*)(0x80026E8E) = 5; // Coconuts
			*(short*)(0x80026FB2) = 9999; // Change coconut gift from 6.6 coconuts to 66.6 coconuts
		}
	} else if (CurrentMap == MAIN_MENU) {
		*(short*)(0x8002E266) = 7; // Enguarde Arena Movement Write
		*(short*)(0x8002F01E) = 7; // Rambi Arena Movement Write
		for (int i = 0; i < 8; i++) {
			// Main Menu moves given upon entering a boss/minigame
			MainMenuMoves[i].moves = moves_values[i];
		}
		// Main Menu visual changes
		*(int*)(0x80030604) = 0x0C000000 | (((int)&file_progress_screen_code & 0xFFFFFF) >> 2); // New file progress code
		*(int*)(0x80029FE0) = 0x0C000000 | (((int)&wipeFileMod & 0xFFFFFF) >> 2); // Wipe File Hook
		*(int*)(0x80028C88) = 0x0C000000 | (((int)&enterFileProgress & 0xFFFFFF) >> 2); // Enter File Progress Screen Hook
		*(int*)(0x80029874) = 0; // Hide GB
		*(int*)(0x80029818) = 0; // Hide A
		*(int*)(0x80029840) = 0; // Hide B
		// File Select
		*(int*)(0x80028CB0) = 0xA0600000; // SB $r0, 0x0 (v0) - Always view file index 0
		*(int*)(0x80028CC4) = 0; // Prevent file index overwrite
		*(int*)(0x80028F88) = 0; // File 2 render
		*(int*)(0x80028F60) = 0; // File 2 Opacity
		*(int*)(0x80028FCC) = 0; // File 3 render
		*(int*)(0x80028FA4) = 0; // File 3 Opacity
		*(int*)(0x80028D04) = 0x0C000000 | (((int)&changeFileSelectAction & 0xFFFFFF) >> 2); // File select change action
		*(int*)(0x80028D10) = 0x0C000000 | (((int)&changeFileSelectAction_0 & 0xFFFFFF) >> 2); // File select change action
		*(int*)(0x80028DB8) = 0x1040000A; // BEQ $v0, $r0, 0xA - Change text signal
		*(short*)(0x80028CA6) = 5; // Change selecting orange to delete confirm screen
		// Options
		initOptionScreen();
	} else if (CurrentMap == SNIDE) {
		*(int*)(0x8002402C) = 0x240E000C; // No extra contraption cutscenes
		*(int*)(0x80024054) = 0x24080001; // 1 GB Turn in
		if (Rando.item_rando) {		
			*(int*)(0x80024CF0) = 0x0C000000 | (((int)&countFlagsDuplicate & 0xFFFFFF) >> 2); // Flag change to FLUT
			*(int*)(0x80024854) = 0x0C000000 | (((int)&checkFlagDuplicate & 0xFFFFFF) >> 2); // Flag change to FLUT
			*(int*)(0x80024880) = 0x0C000000 | (((int)&checkFlagDuplicate & 0xFFFFFF) >> 2); // Flag change to FLUT
			*(int*)(0x800248B0) = 0x0C000000 | (((int)&setFlagDuplicate & 0xFFFFFF) >> 2); // Flag change to FLUT
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
	} else if (CurrentMap == 0x11) {
		// Initialize Helm
		HelmInit(0);
	} else if ((CurrentMap == 0xAA) && (Rando.perma_lose_kongs)) {
		// Prevent Helm Lobby B. Locker requiring Chunky
		*(short*)(0x80027970) = 0x1000;
	}
	if ((CurrentMap == 0x35) || (CurrentMap == 0x49) || ((CurrentMap >= 0x9B) && (CurrentMap <= 0xA2))) {
		// Change crown spawn
		if (Rando.item_rando) {
			*(int*)(0x8002501C) = 0x0C000000 | (((int)&spawnCrownReward & 0xFFFFFF) >> 2); // Crown Spawn
		}
	}
	// Change Dillo Health based on map
	if (Rando.short_bosses) {
		if ((CurrentMap == 8) || (DestMap == 8)) {
			actor_health_damage[185].init_health = 4; // Dillo Health - AD1
		} else if ((CurrentMap == 0xC4) || (CurrentMap == 0xC4)) {
			actor_health_damage[185].init_health = 3; // Dillo Health - AD2
		}
	}
	if (ObjectModel2Timer < 2) {
		// Wipe warp data pointer to prevent pointing to free memory
		WarpData = 0;
		wipeHintCache();
	}
	if (CurrentMap == 2) { // Arcade
		initArcade();
	} else if (CurrentMap == 9) { // Jetpac
		initJetpac();
	}
	writeCoinRequirements(1);
	fixTBarrelsAndBFI(0);
	if ((*(int*)(0x807FBB64) << 1) & 0x80000000) {
		// Menu Overlay - Candy's Shop Glitch
		*(short*)(0x80027678) = 0x1000;
		*(short*)(0x8002769C) = 0x1000;
	} else if (*(int*)(0x807FBB64) & 0x104000) { // Minigames
		*(short*)(0x80024266) = 1; // Set Minigame oranges as infinite
	}
	if (CurrentMap == 0xBD) { // BFI
		*(int*)(0x80028080) = 0x0C000000 | (((int)&displayBFIMoveText & 0xFFFFFF) >> 2); // BFI Text Display
		if (Rando.rareware_gb_fairies > 0) {
			*(int*)(0x80027E70) = 0x2C410000 | Rando.rareware_gb_fairies; // SLTIU $at, $v0, count
			*(short*)(0x80027E74) = 0x1420; // BNEZ $at, 0x6
		}
		if (Rando.item_rando) {
			*(int*)(0x80027E68) = 0x0C000000 | (((int)&fairyQueenCutsceneInit & 0xFFFFFF) >> 2); // BFI, Init Cutscene Setup
			*(int*)(0x80028104) = 0x0C000000 | (((int)&fairyQueenCutsceneCheck & 0xFFFFFF) >> 2); // BFI, Cutscene Play
		}
	}
	if (CurrentMap == 0xD6) {
		// Shoe
		if (Rando.randomize_toes) {
			for (int i = 0; i < 5; i++) {
				ToeSet1[(4 * i) + 2] = Rando.k_rool_toes[i];
				ToeSet2[(4 * i) + 2] = Rando.k_rool_toes[5 + i];
			}
		}
	}
	int in_boss = 0;
	for (int i = 0; i < sizeof(boss_maps); i++) {
		if (CurrentMap == boss_maps[i]) {
			in_boss = 1;
		}
	}
	if (in_boss) {
		if (Rando.item_rando) {
			*(int*)(0x80028650) = 0x0C000000 | (((int)&spawnBossReward & 0xFFFFFF) >> 2); // Key Spawn
		}
		PatchKRoolCode();
		if (Rando.quality_of_life.vanilla_fixes) {
			*(short*)(0x800359A6) = 3; // Fix cutscene bug
		}
	}
	if (Rando.misc_cosmetic_on) {
		if ((CurrentMap >= 0x90) && (CurrentMap <= 0x93)) {
			// PPPanic
			*(short*)(0x8002A55E) = 0x21 + Rando.pppanic_klaptrap_color; // PPPanic Klaptrap Color
		}
		if ((CurrentMap == 0x67) || ((CurrentMap >= 0x8A) && (CurrentMap <= 0x8C))) {
			// SSeek
			*(short*)(0x8002C22E) = 0x21 + Rando.sseek_klaptrap_color; // SSeek Klaptrap Color
		}
	}
	if ((CurrentMap == 0x65) || ((CurrentMap >= 0x8D) && (CurrentMap <= 0x8F))) {
		// Krazy Kong Klamour - Adjsut flicker speeds
		PatchBonusCode();
		// Adjust Krazy KK Flicker Speeds
		// Defaults: 48/30. Start: 60. Flicker Thresh: -30. Scaling: 2.7
		*(unsigned short*)(0x800293E6) = 130; // V Easy
		*(unsigned short*)(0x800293FA) = 130; // Easy
		*(unsigned short*)(0x8002940E) = 81; // Medium
		*(unsigned short*)(0x80029422) = 81; // Hard
		*(unsigned short*)(0x800295D2) = 162; // Start
		*(unsigned short*)(0x800297D8) = 0x916B; // LB -> LBU
		*(short*)(0x800297CE) = -81; // Flicker Threshold
		if (Rando.disco_chunky) {
			KrazyKKModels[4] = 0xE; // Change to disco chunky model
		}
		if (Rando.krusha_slot != -1) {
			KrazyKKModels[(int)Rando.krusha_slot] = 0xDB; // Change to krusha model
		}
	}
	if (CurrentMap == 0x9A) { // Mad Jack
		// Change phase reset differential to 40.0f units
		*(short*)(0x80033B26) = 0x4220; // Jumping Around
		*(short*)(0x800331AA) = 0x4220; // Random Square
		*(short*)(0x800339EE) = 0x4220; // Stationary
		// *(float*)(0x80036C40) = 3.0f; // Phase 1 Jump speed
		// *(float*)(0x80036C44) = 3.0f; // Phase 2
		// *(float*)(0x80036C48) = 3.0f; // ...
		// *(float*)(0x80036C4C) = 3.0f;
		// *(float*)(0x80036C50) = 3.0f;
	}

	if (Rando.fast_gbs) {
		if (CurrentMap == 0x1B) { // Factory Car Race
			*(short*)(0x8002D03A) = 0x0001; // 1 Lap
		}
		if(CurrentMap == 0xB9) { //Castle Car Race
			*(short*)(0x8002D096) = 0x0001; // 1 Lap
		}
		if(CurrentMap == 0x27) { //Seal Race
			*(short*)(0x8002D0E2) = 0x0001; // 1 Lap
		}
	}
}

void parseCutsceneData(void) {
	/**
	 * @brief Handle Cutscene Data
	 */
	wipeCounterImageCache();
	if ((CurrentMap >= 0xCB) && (CurrentMap <= 0xCF)) {
		int phase = CurrentMap - 0xCB;
		initKRool(phase);
	}
	if (Rando.quality_of_life.remove_cutscenes) {
		updateSkippableCutscenes();
	}
	loadDKTVData(); // Has to be last
}