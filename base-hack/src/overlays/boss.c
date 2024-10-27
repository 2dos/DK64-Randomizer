/**
 * @file boss.c
 * @author Ballaam
 * @brief Changes within the boss overlay
 * @version 0.1
 * @date 2023-12-16
 * 
 * @copyright Copyright (c) 2023
 * 
 */

#include "../../include/common.h"

void overlay_mod_boss(void) {
	// Add chunky phase microhint
	if ((Rando.microhints != MICROHINTS_NONE) && (!hasChunkyPhaseSlam())) {
		*(short*)(0x800359A8) = 14; // Microhint Cutscene
		*(int*)(0x80028D54) = 0; // Delete flag set
	}
	
	// Change Dillo Health based on map
	if (Rando.short_bosses) {
		if ((CurrentMap == MAP_JAPESDILLO) || (DestMap == MAP_JAPESDILLO)) {
			actor_health_damage[185].init_health = 4; // Dillo Health - AD1
		} else if ((CurrentMap == MAP_CAVESDILLO) || (CurrentMap == MAP_CAVESDILLO)) {
			actor_health_damage[185].init_health = 3; // Dillo Health - AD2
		}
	}

	// Shoe
	if (Rando.quality_of_life.vanilla_fixes) {
		if (!(MovesBase[KONG_TINY].weapon_bitfield & 1)) {
			*(int*)(0x8002FFE0) = 0; // Control State patch
			*(int*)(0x8002FFE8) = 0; // Control State progress patch
		}
	}
	if (Rando.music_rando_on) {
		// Lower Crowd SFX Volume
		*(short*)(0x80028F3E) = CROWD_VOLUME;
		*(short*)(0x8002904E) = CROWD_VOLUME;
	}
}