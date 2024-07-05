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

void loadJetpacSprites_handler(void) {
	loadJetpacSprites();
	*(unsigned char*)(0x8002F060) = Rando.jetman_rgb[0];
	*(unsigned char*)(0x8002F061) = Rando.jetman_rgb[1];
	*(unsigned char*)(0x8002F062) = Rando.jetman_rgb[2];
}

void initJetpac(void) {
	/**
	 * @brief Initialize Jetpac Changes.
	 */
	if (Rando.item_rando) {
		*(short*)(0x80024D8E) = getHi(&jetpacRewardText);
		*(short*)(0x80024D96) = getLo(&jetpacRewardText);
	}
}