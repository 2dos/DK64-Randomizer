/**
 * @file helm.c
 * @author Ballaam
 * @brief Fixes any glitches in Hideout Helm
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
	if (CurrentMap == MAP_HELM) { // Hideout Helm
		if (checkFlag(FLAG_KEYHAVE_KEY8,FLAGTYPE_PERMANENT) == 0) { // Doesn't have Key 8
			if (touchingModel2Object(0x5A)) {
				setPermFlag(FLAG_KEYHAVE_KEY8); // Give Key 8
			}
		}
	}
}

void fixHelmTimerCorrection(void) {
	/**
	 * @brief Fix a bug where pausing and then doing something other than unpausing that takes you out of the pause menu will not perform the helm timer correction
	 * 
	 */
	if (HelmTimerShown) {
		unsigned long long current_timestamp = getTimestamp();
		unsigned int minor = current_timestamp & 0xFFFFFFFF;
		unsigned int major = (current_timestamp >> 32) & 0xFFFFFFFF;
		unsigned int diff_major = (major - PauseTimestampMajor) - (minor < PauseTimestampMinor);
		unsigned int diff_minor = minor - PauseTimestampMinor;
		HelmStartTimestampMinor += diff_minor;
		HelmStartTimestampMajor = (HelmStartTimestampMinor < diff_minor) + HelmStartTimestampMajor + diff_major;
	}
}

void helmTime_restart(void) {
	/**
	 * @brief Instance of the correction code which overwrites the instruction to warp to the same map for the restart
	 * 
	 */
	initiateTransition(CurrentMap, 0);
	fixHelmTimerCorrection();
}

void helmTime_exitBonus(void) {
	/**
	 * @brief Instance of the correction code which overwrites the instruction to exit out of a bonus minigame
	 * 
	 */
	ExitFromBonus();
	fixHelmTimerCorrection();
}

void helmTime_exitRace(void) {
	/**
	 * @brief Instance of the correction code which overwrites the instruction to exit out of a race
	 * 
	 */
	ExitRace();
	fixHelmTimerCorrection();
}

void helmTime_exitLevel(void) {
	/**
	 * @brief Instance of the correction code which overwrites the instruction to exit out of a level
	 * 
	 */
	ExitFromLevel();
	fixHelmTimerCorrection();
}

void helmTime_exitBoss(void) {
	/**
	 * @brief Instance of the correction code which overwrites the instruction to exit out of a boss
	 * 
	 */
	initiateTransition(MAP_TROFFNSCOFF, 2);
	fixHelmTimerCorrection();
}

void helmTime_exitKRool(void) {
	/**
	 * @brief Instance of the correction code which overwrites the instruction to exit out of K. Rool
	 * 
	 */
	initiateTransition(MAP_ISLES, 12);
	fixHelmTimerCorrection();
}