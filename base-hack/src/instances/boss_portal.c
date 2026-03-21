/**
 * @file boss_portal.c
 * @author Ballaam
 * @brief Functions related to T&S Portals
 * @version 0.1
 * @date 2023-10-23
 * 
 * @copyright Copyright (c) 2023
 * 
 */

#include "../../include/common.h"
#define PORTAL_DELTA 40

void TNSIndicatorGenericCode(behaviour_data* behaviour, int index, int id) {
	/**
	 * @brief Generic code for a T&S Portal Indicator
	 * 
	 * @param behaviour Behaviour Pointer for Object
	 * @param index Index of Object in Model Two Array
	 * @param id T&S Portal ID
	 */
	int world = getWorld(CurrentMap, 0);
	int display_number = TroffNScoffReqArray[world] - TroffNScoffTurnedArray[world];
	if (display_number < 0) {
		display_number = 0;
	}
	for (int i = 1; i < 4; i++) {
		int tex = (((10-i) + display_number % 10) % 10) - 1;
		if (CurrentMap == MAP_TROFFNSCOFF) {
			tex = 10;
		}
		displayNumberOnObject(id, 4 + i, tex, 0, 0);
		display_number /= 10;
	}
}