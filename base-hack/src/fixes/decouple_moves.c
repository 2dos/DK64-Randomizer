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
	// Change price check
	*(int*)(0x80026200) = 0x90CF0005; // LBU 	t7, 0x5 (a2)
	// Change Special Moves Text
	*(int*)(0x80027AE0) = 0x910F0004; // LBU 	t7, 0x4 (t0)
	// Change Gun Text
	*(int*)(0x80027BA0) = 0x91180004; // LBU 	t8, 0x4 (t0)
	// Change Instrument Text
	*(int*)(0x80027C14) = 0x910C0004; // LBU 	t4, 0x4 (t0)
}

void decouple_moves_fixes(void) {
	if ((CurrentMap == CRANKY) || (CurrentMap == CANDY) || (CurrentMap == FUNKY)) {
		PatchCrankyCode();
		*(int*)(0x80025E9C) = 0x0C009751; // Change writing of move to "write bitfield move" function call
		writeJetpacMedalReq(); // Adjust medal requirement for Jetpac
		if (Rando.shop_hints) {
			int func_call = 0x0C000000 | (((int)&getMoveHint & 0xFFFFFF) >> 2);
			*(int*)(0x8002661C) = func_call;
			*(int*)(0x800265F0) = func_call;
		}
		int func_call = 0x0C000000 | (((int)&getNextMovePurchase & 0xFFFFFF) >> 2);
		*(int*)(0x80026720) = func_call;
		*(int*)(0x8002683C) = func_call;
		crossKongInit();
	} else if (CurrentMap == MAIN_MENU) {
		*(short*)(0x8002E266) = 7; // Enguarde Arena Movement Write
		*(short*)(0x8002F01E) = 7; // Rambi Arena Movement Write
		for (int i = 0; i < 8; i++) {
			MainMenuMoves[i].moves = moves_values[i];
		}
	} else if (CurrentMap == SNIDE) {
		*(int*)(0x8002402C) = 0x240E000C; // No extra contraption cutscenes
		*(int*)(0x80024054) = 0x24080001; // 1 GB Turn in
	}
	writeCoinRequirements(1);
	if ((*(int*)(0x807FBB64) << 1) & 0x80000000) {
		// Menu Overlay - Candy's Shop Glitch
		*(short*)(0x80027678) = 0x1000;
		*(short*)(0x8002769C) = 0x1000;
	}
	if ((CurrentMap >= 0xCB) && (CurrentMap <= 0xCF)) {
		PatchKRoolCode();
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
	}
	if (CurrentMap == 0x9A) {
		*(short*)(0x80033B26) = 0x41F0; // Jumping Around
		*(short*)(0x800331AA) = 0x41F0; // Random Square
		*(short*)(0x800339EE) = 0x41F0; // Stationary
		// *(float*)(0x80036C40) = 3.0f; // Phase 1 Jump speed
		// *(float*)(0x80036C44) = 3.0f; // Phase 2
		// *(float*)(0x80036C48) = 3.0f; // ...
		// *(float*)(0x80036C4C) = 3.0f;
		// *(float*)(0x80036C50) = 3.0f;
	}
}