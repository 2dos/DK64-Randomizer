/**
 * @file switches.c
 * @author Ballaam
 * @brief Functions related to switches
 * @version 0.1
 * @date 2023-10-23
 * 
 * @copyright Copyright (c) 2023
 * 
 */

#include "../../include/common.h"

int getPressedRandoSwitch(behaviour_data* behaviour_pointer, int setting, int vanilla_bullet_type, int ID) {
	int bullet = vanilla_bullet_type;
	if (setting != 0) {
		if (setting == 6) {
			// Any kong switch
			int valid = 0;
			for (int i = 0; i < 5; i++) {
				valid |= getPressedSwitch(behaviour_pointer, kong_pellets[i], ID);
			}
			return valid;
		}
		bullet = kong_pellets[setting - 1];
	}
	return getPressedSwitch(behaviour_pointer, bullet, ID);
}

int hasChunkyPhaseSlam(void) {
	return MovesBase[KONG_CHUNKY].simian_slam >= Rando.chunky_phase_krool_slam_req;
}