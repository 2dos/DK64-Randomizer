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
	} else if (CurrentMap == MAIN_MENU) {
		*(short*)(0x8002E266) = 7; // Enguarde Arena Movement Write
		*(short*)(0x8002F01E) = 7; // Rambi Arena Movement Write
		for (int i = 0; i < 8; i++) {
			MainMenuMoves[i].moves = moves_values[i];
		}
		int func_call = 0x0C000000 | (((int)&displayHeadTexture & 0xFFFFFF) >> 2);
		*(int*)(0x800292B8) = func_call;
		*(int*)(0x800292D4) = func_call;
		// Menu Stuff
		*(short*)(0x800281AA) = 3; // Set "adventure" destination to the file progress screen
		*(short*)(0x8002A05A) = 3; // Set B button action in delete confirm to file progress
		*(short*)(0x8002A05A) = 3; // Set B button action in delete confirm to file progress
		*(short*)(0x8002A02A) = 3; // Set B button action in delete confirm to file progress
		*(short*)(0x80029fea) = 3; // Set A button action in delete confirm to file progress
		*(int*)(0x80030604) = 0x0C000000 | (((int)&file_progress_screen_code & 0xFFFFFF) >> 2); // New file progress code
		*(int*)(0x80029760) = 0x0C000000 | (((int)&displayTopText & 0xFFFFFF) >> 2); // New file progress top text code
		*(int*)(0x80030614) = 0x0C000000 | (((int)&FileProgressInit & 0xFFFFFF) >> 2); // New file progress init code
		*(int*)(0x8002999C) = 0;
	} else if (CurrentMap == SNIDE) {
		*(int*)(0x8002402C) = 0x240E000C; // No extra contraption cutscenes
		*(int*)(0x80024054) = 0x24080001; // 1 GB Turn in
	} else if (CurrentMap == 0x11) {
		HelmInit(0);
	}
	if ((CurrentMap >= 0xCB) && (CurrentMap <= 0xCF)) {
		int phase = CurrentMap - 0xCB;
		initKRool(phase);
	}
	if (Rando.short_bosses) {
		if ((CurrentMap == 8) || (DestMap == 8)) {
			*(short*)(0x8074D3A8) = 4; // Dillo Health - AD1
		} else if ((CurrentMap == 0xC4) || (CurrentMap == 0xC4)) {
			*(short*)(0x8074D3A8) = 3; // Dillo Health - AD2
		}
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
	}
	int in_boss = 0;
	for (int i = 0; i < sizeof(boss_maps); i++) {
		if (CurrentMap == boss_maps[i]) {
			in_boss = 1;
		}
	}
	if (in_boss) {
		PatchKRoolCode();
		if (Rando.quality_of_life) {
			*(short*)(0x800359A6) = 3;
		}
	}
	if ((CurrentMap == 0x65) || ((CurrentMap >= 0x8D) && (CurrentMap <= 0x8F))) {
		PatchBonusCode();
		// Adjust Krazy KK Flicker Speeds
		// Defaults: 48/30. Start: 60. Flicker Thresh: -30. Scaling: 2.3
		*(unsigned short*)(0x800293E6) = 110; // V Easy
		*(unsigned short*)(0x800293FA) = 110; // Easy
		*(unsigned short*)(0x8002940E) = 69; // Medium
		*(unsigned short*)(0x80029422) = 69; // Hard
		*(unsigned short*)(0x800295D2) = 138; // Start
		*(unsigned short*)(0x800297D8) = 0x916B; // LB -> LBU
		*(short*)(0x800297CE) = -69; // Flicker Threshold
		if (Rando.disco_chunky) {
			*(short*)(0x8002D8D0) = 0xE; // Change to disco chunky model
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
