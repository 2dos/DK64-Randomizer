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
	if ((Rando.microhints != MICROHINTS_NONE) && (MovesBase[0].simian_slam < 2)) {
		*(short*)(0x800359A8) = 14; // Microhint Cutscene
		*(int*)(0x80028D54) = 0; // Delete flag set
	}
	if (DAMAGE_MASKING) {
		writeFunction(0x80031524, &applyDamageMask);
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
	if (Rando.randomize_toes) {
		for (int i = 0; i < 5; i++) {
			ToeSet1[(4 * i) + 2] = Rando.k_rool_toes[i];
			ToeSet2[(4 * i) + 2] = Rando.k_rool_toes[5 + i];
		}
	}
	if (Rando.quality_of_life.vanilla_fixes) {
		if (!(MovesBase[KONG_TINY].weapon_bitfield & 1)) {
			*(int*)(0x8002FFE0) = 0; // Control State patch
			*(int*)(0x8002FFE8) = 0; // Control State progress patch
		}
	}

	writeFunction(0x8002D20C, &SpiderBossExtraCode); // Handle preventing spider boss being re-fightable

	if (Rando.item_rando) {
		writeFunction(0x80028650, &spawnBossReward); // Key Spawn
	}
	PatchKRoolCode();

	if (Rando.music_rando_on) {
		// Lower Crowd SFX Volume
		*(short*)(0x80028F3E) = CROWD_VOLUME;
		*(short*)(0x8002904E) = CROWD_VOLUME;
	}
}