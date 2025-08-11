/**
 * @file jetpac.c
 * @author Ballaam
 * @brief Changes within the Jetpac Overlay
 * @version 0.1
 * @date 2023-12-16
 * 
 * @copyright Copyright (c) 2023
 * 
 */

#include "../../include/common.h"

void loadJetpacSprites_handler(void) {
	loadJetpacSprites();
	*(unsigned char*)(0x8002F060) = Rando.jetman_rgb[0];
	*(unsigned char*)(0x8002F061) = Rando.jetman_rgb[1];
	*(unsigned char*)(0x8002F062) = Rando.jetman_rgb[2];
}

void exitJetpac(int map, int exit) {
	if (CurrentMap == MAP_JETPAC_ROCKET) {
		ExitFromBonus();
		return;
	}
	initiatetransition(map, exit);
}

void completeJetpac(void) {
	if (CurrentMap == MAP_JETPAC_ROCKET) {
		resolveBonusContainer();
		ExitFromBonus();
		return;
	}
	nextJetpacLevel();
}