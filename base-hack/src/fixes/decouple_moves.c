#include "../../include/common.h"

#define FUNKY 1
#define CRANKY 5
#define CANDY 0x19
#define MAIN_MENU 0x50
#define SNIDE 0xF

static const char moves_values[] = {1,1,3,1,7,1,1,7};

void crossKongInit(void) {
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

static const unsigned char boss_maps[] = {0x8,0xC5,0x9A,0x6F,0x53,0xC4,0xC7,0xCB,0xCC,0xCD,0xCE,0xCF,0xD6};

void arcadeExit(void) {
	if (!ArcadeExited) {
		if ((ArcadeEnableReward) && (ArcadeStoryMode)) {
			if (!checkFlag(FLAG_ARCADE_ROUND1, 0)) {
				setFlag(0x10, 1, 2);
			} else if (!checkFlag(FLAG_COLLECTABLE_NINTENDOCOIN, 0)) {
				setFlag(0x11, 1, 2);
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

void initArcade(void) {
	*(int*)(0x80024F10) = 0x240E0005; // ADDIU $t6, $r0, 0x5
	*(short*)(0x80024F2A) = 0xC71B;
	*(int*)(0x80024F2C) = 0xA0CEC71B; // SB $t6, 0xC71B ($a2)
	*(int*)(0x80024D5C) = 0x0C000000 | (((int)&arcadeExit & 0xFFFFFF) >> 2);
	*(int*)(0x800257B4) = 0x0C000000 | (((int)&arcadeExit & 0xFFFFFF) >> 2);
	*(int*)(0x8002B6D4) = 0x0C000000 | (((int)&arcadeExit & 0xFFFFFF) >> 2);
	*(int*)(0x8002FA58) = 0x0C000000 | (((int)&arcadeExit & 0xFFFFFF) >> 2);
	*(short*)(0x80024F32) = 0x82; // Swap flags
	*(short*)(0x80024F56) = 0x84; // Swap flags
	*(short*)(0x80024F4A) = 4; // Swap levels
	*(short*)(0x80024F6E) = 8; // Swap levels
	for (int i = 0; i < 4; i++) {
		ArcadeBackgrounds[i] = Rando.arcade_order[i];
	}
}


void decouple_moves_fixes(void) {
	if ((CurrentMap == CRANKY) || (CurrentMap == CANDY) || (CurrentMap == FUNKY)) {
		PatchCrankyCode();
		*(int*)(0x80025E9C) = 0x0C009751; // Change writing of move to "write bitfield move" function call
		writeJetpacMedalReq(); // Adjust medal requirement for Jetpac
		int func_call = 0;
		if (Rando.shop_hints) {
			func_call = 0x0C000000 | (((int)&getMoveHint & 0xFFFFFF) >> 2);
			*(int*)(0x8002661C) = func_call;
			*(int*)(0x800265F0) = func_call;
		}
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
	} else if (CurrentMap == MAIN_MENU) {
		*(short*)(0x8002E266) = 7; // Enguarde Arena Movement Write
		*(short*)(0x8002F01E) = 7; // Rambi Arena Movement Write
		for (int i = 0; i < 8; i++) {
			MainMenuMoves[i].moves = moves_values[i];
		}
		// int func_call = 0x0C000000 | (((int)&displayHeadTexture & 0xFFFFFF) >> 2);
		// *(int*)(0x800292B8) = func_call;
		// *(int*)(0x800292D4) = func_call;
		// Menu Stuff
		// *(short*)(0x800281AA) = 3; // Set "adventure" destination to the file progress screen
		
		*(int*)(0x80030604) = 0x0C000000 | (((int)&file_progress_screen_code & 0xFFFFFF) >> 2); // New file progress code
		*(int*)(0x80029FE0) = 0x0C000000 | (((int)&wipeFileMod & 0xFFFFFF) >> 2); // Wipe File Hook
		*(int*)(0x80028C88) = 0x0C000000 | (((int)&enterFileProgress & 0xFFFFFF) >> 2); // Enter File Progress Screen Hook
		// *(int*)(0x80029760) = 0x0C000000 | (((int)&displayTopText & 0xFFFFFF) >> 2); // New file progress top text code
		// // *(int*)(0x80030614) = 0x0C000000 | (((int)&FileProgressInit & 0xFFFFFF) >> 2); // New file progress init code
		// *(int*)(0x80029894) = 0x0C000000 | (((int)&FileProgressInitSub & 0xFFFFFF) >> 2); // New file progress init code
		// *(int*)(0x8002999C) = 0;
		*(int*)(0x80029874) = 0; // Hide GB
		*(int*)(0x80029818) = 0; // Hide A
		*(int*)(0x80029840) = 0; // Hide B
		// File Select
		// *(short*)(0x80028D16) = 2; // Cap to 2 options
		// *(short*)(0x80028D0A) = 2; // Cap to 2 options
		// *(short*)(0x80028C96) = 1; // Target Delete Index
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
			*(int*)(0x80024CF0) = 0x0C000000 | (((int)&countFlagsDuplicate & 0xFFFFFF) >> 2); // File select change action
			*(int*)(0x80024854) = 0x0C000000 | (((int)&checkFlagDuplicate & 0xFFFFFF) >> 2); // File select change action
			*(int*)(0x80024880) = 0x0C000000 | (((int)&checkFlagDuplicate & 0xFFFFFF) >> 2); // File select change action
			*(int*)(0x800248B0) = 0x0C000000 | (((int)&setFlagDuplicate & 0xFFFFFF) >> 2); // File select change action
		}
	} else if (CurrentMap == 0x11) {
		HelmInit(0);
	}
	if ((CurrentMap == 0x35) || (CurrentMap == 0x49) || ((CurrentMap >= 0x9B) && (CurrentMap <= 0xA2))) {
		if (Rando.item_rando) {
			*(int*)(0x8002501C) = 0x0C000000 | (((int)&spawnCrownReward & 0xFFFFFF) >> 2); // Crown Spawn
		}
	}
	if (Rando.short_bosses) {
		if ((CurrentMap == 8) || (DestMap == 8)) {
			*(short*)(0x8074D3A8) = 4; // Dillo Health - AD1
		} else if ((CurrentMap == 0xC4) || (CurrentMap == 0xC4)) {
			*(short*)(0x8074D3A8) = 3; // Dillo Health - AD2
		}
	}
	if (ObjectModel2Timer < 2) {
		WarpData = 0;
	}
	if (CurrentMap == 2) {
		initArcade();
	}
	writeCoinRequirements(1);
	fixTBarrelsAndBFI(0);
	if ((*(int*)(0x807FBB64) << 1) & 0x80000000) {
		// Menu Overlay - Candy's Shop Glitch
		*(short*)(0x80027678) = 0x1000;
		*(short*)(0x8002769C) = 0x1000;
	} else if (*(int*)(0x807FBB64) & 0x104000) {
		*(short*)(0x80024266) = 1; // Set Minigame oranges as infinite
	}
	if (CurrentMap == 0xBD) {
		*(int*)(0x80028080) = 0x0C000000 | (((int)&displayBFIMoveText & 0xFFFFFF) >> 2); // BFI Text Display
		if (Rando.rareware_gb_fairies > 0) {
			*(int*)(0x80027E70) = 0x2C410000 | Rando.rareware_gb_fairies; // SLTIU $at, $v0, count
			*(short*)(0x80027E74) = 0x1420; // BNEZ $at, 0x6
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
			*(short*)(0x800359A6) = 3;
		}
	}
	if (Rando.misc_cosmetic_on) {
		if ((CurrentMap >= 0x90) && (CurrentMap <= 0x93)) {
			// PPPanic
			*(short*)(0x8002A55E) = 0x21 + Rando.pppanic_klaptrap_color;
		}
		if ((CurrentMap == 0x67) || ((CurrentMap >= 0x8A) && (CurrentMap <= 0x8C))) {
			// SSeek
			*(short*)(0x8002C22E) = 0x21 + Rando.sseek_klaptrap_color;
		}
	}
	if ((CurrentMap == 0x65) || ((CurrentMap >= 0x8D) && (CurrentMap <= 0x8F))) {
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
	if (CurrentMap == 0x9A) {
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
			*(short*)(0x8002D03A) = 0x0001; //1 Lap
		}

		if(CurrentMap == 0xB9) { //Castle Car Race
			*(short*)(0x8002D096) = 0x0001; //1 Lap
		}

		if(CurrentMap == 0x27) { //Seal Race
			*(short*)(0x8002D0E2) = 0x0001; //1 Lap
		}
	}
}

void parseCutsceneData(void) {
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