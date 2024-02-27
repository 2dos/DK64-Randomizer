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