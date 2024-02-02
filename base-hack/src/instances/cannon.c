/**
 * @file cannon.c
 * @author Ballaam
 * @brief Instance functions related to cannons
 * @version 0.1
 * @date 2023-10-23
 * 
 * @copyright Copyright (c) 2023
 * 
 */

#include "../../include/common.h"

void spawnCannon(actorData* cannon) {
	/**
	 * @brief Set correct cannon data
	 * 
	 * @param cannon Actor Pointer for referenced cannon
	 */
	cannon->shadow_intensity = 0xFF;
	cannon->obj_props_bitfield |= 0x8000;
	cannon->control_state = 0;
	cannon->noclip_byte = 2;
}

int spawnCannonWrapper(void) {
	/**
	 * @brief Container function for spawning a cannon
	 * 
	 * @return Cannon is being spawned
	 */
	if (CurrentMap == MAP_ISLES) {
		int spawner_id = getActorSpawnerIDFromTiedActor(LastSpawnedActor);
		if (spawner_id == 8) { // Castle Cannon
			if (Rando.lobbies_open_bitfield & 0x40) {
				return 1;
			}
		} else if (spawner_id == 18) { // Fungi Cannon
			if (Rando.lobbies_open_bitfield & 0x10) {
				return 1;
			}
		} 
	}
	return 0;
}