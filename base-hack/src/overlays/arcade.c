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
	if ((ArcadeStoryMode) && ((ArcadeMap & 3) == 0)) {
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

/*
	Arcade Reward Indexes:
	0 - Nintendo Coin / No Item
	1 - Bean
	2 - Blueprint
	3 - Crown
	4 - Fairy
	5 - GB
	6 - Key
	7 - Medal
	8 - Pearl
	9 - Potion (DK)
	10 - Potion (Diddy)
	11 - Potion (Lanky)
	12 - Potion (Tiny)
	13 - Potion (Chunky)
	14 - Potion (Any)
	15 - DK
	16 - Diddy
	17 - Lanky
	18 - Tiny
	19 - Chunky
	20 - Rainbow Coin
	21 - RW Coin
	22 - Melon

	Jetpac Reward Indexes:
	0 - Rareware Coin / No Item
	1 - Bean
	2 - Blueprint
	3 - Crown
	4 - Fairy
	5 - GB
	6 - Key
	7 - Medal
	8 - Pearl
	9 - Potion
	10 - Kong
	11 - Rainbow Coin
	12 - Nintendo Coin
	13 - Melon
*/

void initArcade(void) {
	/**
	 * @brief Initialize DK Arcade Changes
	 */
	// Address of Nintendo Coin Image write: 0x8002E8B4/0x8002E8C0
	*(int*)(0x80024F10) = 0x240E0005; // ADDIU $t6, $r0, 0x5
	*(short*)(0x80024F2A) = 0xC71B;
	*(int*)(0x80024F2C) = 0xA0CEC71B; // SB $t6, 0xC71B ($a2)
	writeFunction(0x80024D5C, &arcadeExit);
	writeFunction(0x800257B4, &arcadeExit);
	writeFunction(0x8002B6D4, &arcadeExit);
	writeFunction(0x8002FA58, &arcadeExit);
	// Fix arcade level setting logic
	writeFunction(0x80024F34, &determineArcadeLevel); // Change log
	*(int*)(0x80024F70) = 0; // Prevent level set
	*(int*)(0x80024F50) = 0; // Prevent level set
	// Arcade Level Order Rando
	for (int i = 0; i < 4; i++) {
		ArcadeBackgrounds[i] = Rando.arcade_order[i];
	}
	writeFunction(0x8002F7BC, &HandleArcadeVictory);
	writeFunction(0x8002FA68, &HandleArcadeVictory);
	*(short*)(0x8002FA24) = 0x1000;
	// Load Arcade Sprite
	if ((*(unsigned short*)(0x8002E8B6) == 0x8004) && (*(unsigned short*)(0x8002E8BA) == 0xAE58) && (Rando.arcade_reward > 0)) {
		// Change Arcade Reward Sprite
		// Ensure code is only run once
		void* addr = getPointerFile(6, Rando.arcade_reward - 1);
		*(unsigned short*)(0x8002E8B6) = getHi(addr);
		*(unsigned short*)(0x8002E8BA) = getLo(addr);
	}
}