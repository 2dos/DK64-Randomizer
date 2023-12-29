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
	if (Rando.model_swaps.beetle_is_rabbit) {
		*(short*)(0x8075ECD2) = 0x47; // Model
		*(short*)(0x8075ECD4) = 0x309;
		*(short*)(0x80024ADE) = 0x305;
		*(short*)(0x80025006) = 0x305;
		*(short*)(0x800241E6) = 0x303;
		if (CurrentMap == MAP_CAVESBEETLERACE) {
			*(short*)(0x8002421A) = 2; // Fixes a bug just before 2nd ramp where rabbit gets stuck
		}
		*(short*)(0x800251B2) = 0x307;
		*(short*)(0x80025246) = 0x308;
		// Fix spinning
		*(short*)(0x80025112) = 0xEE;
		*(int*)(0x80025114) = 0x0140C021;
	}
}