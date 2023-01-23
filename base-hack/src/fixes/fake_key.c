/**
 * @file fake_key.c
 * @author Ballaam
 * @brief Fixes the fake key glitch
 * @version 0.1
 * @date 2022-03-30
 * 
 * @copyright Copyright (c) 2022
 * 
 */
#include "../../include/common.h"

void fixkey8(void) {
	/**
	 * @brief Fixes Fake Key at the end of Hideout Helm
	 * 
	 */
	if (CurrentMap == 0x11) { // Hideout Helm
		if (checkFlag(FLAG_KEYHAVE_KEY8,0) == 0) { // Doesn't have Key 8
			if (touchingModel2Object(0x5A)) {
				setPermFlag(FLAG_KEYHAVE_KEY8); // Give Key 8
			}
		}
	}
}