/**
 * @file bonus.c
 * @author Ballaam
 * @brief Changes within the Bonus Overlay
 * @version 0.1
 * @date 2023-12-16
 * 
 * @copyright Copyright (c) 2023
 * 
 */

#include "../../include/common.h"

void overlay_mod_bonus(void) {
	// Change crown spawn
	if (Rando.item_rando) {
		writeFunction(0x8002501C, &spawnCrownReward); // Crown Spawn
	}
	*(short*)(0x80024266) = 1; // Set Minigame oranges as infinite

	writeFunction(0x8002D6A8, &warpOutOfArenas); // Enable the two arenas to be minigames
	writeFunction(0x8002D31C, &ArenaTagKongCode); // Tag Rambi/Enguarde Instantly
	writeFunction(0x8002D6DC, &ArenaEarlyCompletionCheck); // Check completion
	if (!isGamemode(GAMEMODE_DKBONUS, 0)) {
		*(int*)(0x8002D628) = 0x016FC022; // sub $t8, $t3, $t7 - Rambi Arena
		*(int*)(0x8002D658) = 0x03224822; // sub $t1, $t9, $v0 - Enguarde Arena
	}

	*(short*)(0x8002A55E) = 0x21 + Rando.pppanic_klaptrap_color; // PPPanic Klaptrap Color
	*(short*)(0x8002C22E) = 0x21 + Rando.sseek_klaptrap_color; // SSeek Klaptrap Color
	if (Rando.pppanic_fairy_model) {
		*(short*)(0x8002A656) = Rando.pppanic_fairy_model;
	}
	if (Rando.tttrouble_turtle_model) {
		*(short*)(0x80028776) = Rando.tttrouble_turtle_model;
	}

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

	if (Rando.music_rando_on) {
		// Lower Crowd SFX Volume
		*(short*)(0x80025192) = CROWD_VOLUME;
		*(short*)(0x80025166) = CROWD_VOLUME;
		*(short*)(0x80025112) = CROWD_VOLUME;
	}
}