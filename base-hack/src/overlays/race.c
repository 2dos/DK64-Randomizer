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
	if (Rando.model_swaps.beetle_is_rabbit) {
		if (CurrentMap == MAP_CAVESBEETLERACE) {
			*(short*)(0x8002421A) = 2; // Fixes a bug just before 2nd ramp where rabbit gets stuck
		}
	}
}