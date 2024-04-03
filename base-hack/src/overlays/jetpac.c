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

static char jetpacRewardText[] = "REWARD COLLECTED";

void initJetpac(void) {
	/**
	 * @brief Initialize Jetpac Changes.
	 */
	if ((*(int*)(0x8002D9F8) == 0x8002D868) && (Rando.jetpac_reward > 0)) {
		// Change Jetpac Reward Sprite
		// Ensure code is only run once
		*(int*)(0x8002D9F8) = (int)getPointerFile(6, Rando.jetpac_reward - 1 + ARCADE_IMAGE_COUNT);
	}
	if (Rando.item_rando) {
		*(short*)(0x80024D8E) = getHi(&jetpacRewardText);
		*(short*)(0x80024D96) = getLo(&jetpacRewardText);
	}
	if (Rando.faster_checks.jetpac) {
		*(short*)(0x80027DCA) = 2500; // Jetpac score requirement
	}
	// Jetpac Enemy Rando
	int enable_jetpac_enemy_rando = 0;
	for (int i = 0; i < 8; i++) {
		if (Rando.jetpac_enemy_order[i] != 0) {
			enable_jetpac_enemy_rando = 1;
		}
	}
	if (enable_jetpac_enemy_rando) {
		void* jetpac_functions[8] = {};
		for (int i = 0; i < 8; i++) {
			jetpac_functions[i] = JetpacEnemyFunctions[i];
		}
		for (int i = 0; i < 8; i++) {
			JetpacEnemyFunctions[i] = jetpac_functions[Rando.jetpac_enemy_order[i]];
		}
	}
}