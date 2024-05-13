/**
 * @file arcade.c
 * @author Ballaam
 * @brief Changes within the Arcade Overlay
 * @version 0.1
 * @date 2023-12-16
 * 
 * @copyright Copyright (c) 2023
 * 
 */

#include "../../include/common.h"

void arcadeExit(void) {
	/**
	 * @brief Arcade exit procedure to fix a bug with Arcade if you have R2 Reward before R1 Reward
	 */
	if (!ArcadeExited) {
		if ((ArcadeEnableReward) && (ArcadeStoryMode)) {
			if (!checkFlag(FLAG_ARCADE_ROUND1, FLAGTYPE_PERMANENT)) {
				setFlag(0x10, 1, FLAGTYPE_TEMPORARY); // Spawn R1 Reward
			} else if (!checkFlag(FLAG_COLLECTABLE_NINTENDOCOIN, FLAGTYPE_PERMANENT)) {
				setFlag(0x11, 1, FLAGTYPE_TEMPORARY); // Spawn R2 Reward
			}
		}
		if (!ArcadeStoryMode) {
			initiateTransition(MAP_MAINMENU, 0);
		} else {
			ExitFromBonus();
		}
		ArcadeExited = 1;
	}
}

int determineArcadeLevel(void) {
	/**
	 * @brief Determines the arcade level based on R1 & Nin Coin flags
	 */
	if (checkFlag(FLAG_ARCADE_ROUND1, FLAGTYPE_PERMANENT)) {
		if (checkFlag(FLAG_COLLECTABLE_NINTENDOCOIN, FLAGTYPE_PERMANENT)) {
			ArcadeMap = 8;
			return 0;
		}
		ArcadeMap = 4;
		return 0;
	}
	ArcadeMap = 0;
	return 0;
}

void HandleArcadeVictory(void) {
	/**
	 * @brief Determine how to handle where to send the player after beating a stage in DK Arcade
	 */
	int threshold = 4;
	if (Rando.faster_checks.arcade_second_round) {
		threshold = 2;
	}
	if ((ArcadeStoryMode) && ((ArcadeMap & 3) == (threshold & 3))) {
		ArcadeEnableReward = 1;
		if (ArcadeScores[4] < ArcadeCurrentScore) {
			sendToHiScorePage();
		} else {
			arcadeExit();
		}
	} else {
		sendToNextMap();
	}
}