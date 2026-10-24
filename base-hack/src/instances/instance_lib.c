/**
 * @file instance_lib.c
 * @author Ballaam
 * @brief Library functions for instance scripts
 * @version 0.1
 * @date 2023-10-23
 * 
 * @copyright Copyright (c) 2023
 * 
 */

#include "../../include/common.h"

void setObjectOpacity(behaviour_data* behaviour_pointer, int opacity) {
	behaviour_pointer->unk_60 = 1;
	behaviour_pointer->unk_62 = opacity;
	behaviour_pointer->unk_66 = 255;
}

void hideObject(behaviour_data* behaviour_pointer) {
	/**
	 * @brief Hide object model 2 item and make it intangible
	 * 
	 * @param behaviour_pointer Behaviour Pointer of Object
	 */
	setObjectOpacity(behaviour_pointer, 0);
	behaviour_pointer->unk_70 = 0;
	behaviour_pointer->unk_71 = 0;
	setScriptRunState(behaviour_pointer, RUNSTATE_PAUSED, 0);
}

int standingOnM2Object(int index) {
	return (Player->touching_object == 1) && (Player->standing_on_index == index);
}