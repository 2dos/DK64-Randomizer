/**
 * @file critter.c
 * @author Ballaam
 * @brief Changes within the critter/water overlay
 * @version 0.1
 * @date 2023-12-16
 * 
 * @copyright Copyright (c) 2023
 * 
 */

#include "../../include/common.h"

void overlay_mod_critter(void) {
	// Prevent Helm Lobby B. Locker requiring Chunky
	*(short*)(0x80027970) = 0x1000;

	// Training
	*(int*)(0x80029610) = 0; // Disable set flag
	writeFunction(0x80029638, &warpOutOfTraining);
	*(int*)(0x80029644) = 0;
	*(short*)(0x8002968E) = 1; // Set timer to 1
	//*(int*)(0x80029314) = 0x2406000A; // Set ticking timer to 10s

	writeFunction(0x80028080, &displayBFIMoveText); // BFI Text Display
	if (Rando.rareware_gb_fairies > 0) {
		*(int*)(0x80027E70) = 0x2C410000 | Rando.rareware_gb_fairies; // SLTIU $at, $v0, count
		*(short*)(0x80027E74) = 0x1420; // BNEZ $at, 0x6
	}
	if (Rando.item_rando) {
		writeFunction(0x80027E68, &fairyQueenCutsceneInit); // BFI, Init Cutscene Setup
		writeFunction(0x80028104, &fairyQueenCutsceneCheck); // BFI, Cutscene Play
	}
}