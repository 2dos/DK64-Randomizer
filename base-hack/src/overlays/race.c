/**
 * @file race.c
 * @author Ballaam
 * @brief Changes within the Race Overlay
 * @version 0.1
 * @date 2023-12-16
 * 
 * @copyright Copyright (c) 2023
 * 
 */

#include "../../include/common.h"

void overlay_mod_race(void) {
	writeCoinRequirements(1);

	if (Rando.faster_checks.factory_car) {
		*(short*)(0x8002D03A) = 0x0001; // Fac Car Race 1 Lap
	}
	if (Rando.faster_checks.castle_car) {
		*(short*)(0x8002D096) = 0x0001; // Cas Car Race 1 Lap
	}
	if (Rando.faster_checks.seal_race) {
		*(short*)(0x8002D0E2) = 0x0001; // Seal Race 1 Lap
	}
}