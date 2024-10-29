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
	if (inTraining(CurrentMap)) {
		CollectableBase.Oranges = StoredOrangeCount;
	}
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

static unsigned char helm_entry_points[] = {0, 3, 4};

int getHelmExit(void) {
	int setting = Rando.fast_start_helm;
	if (setting > 0) {
		setPermFlag(FLAG_STORY_HELM); // Helm Story
		setFlag(FLAG_HELM_ROMANDOORS_OPEN,1,FLAGTYPE_TEMPORARY); // Roman Numeral Doors
		for (int j = 0; j < 4; j++) {
			setFlag(FLAG_HELM_GATE_0 + j,1,FLAGTYPE_TEMPORARY); // Gates knocked down
		}
		if (setting == 2) {
			setPermFlag(FLAG_MODIFIER_HELMBOM);
		}
	}
	return helm_entry_points[setting];
}

void WarpToHelm(void) {
	initiateTransition(MAP_HELM, getHelmExit());
}