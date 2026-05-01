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

void getModelTwoItemFromActor(int actor, short* item, float* scale) {
	/**
	 * @brief Converts actor into it's model two equivalent
	 * 
	 * @param actor Actor Index
	 * @param item Address to store item model two index
	 * @param scale Address to store item scale
	 */
	for (unsigned int i = 0; i < (sizeof(item_conversions) / sizeof(item_conversion_info)); i++) {
		if (actor == item_conversions[i].actor) {
			*item = item_conversions[i].model_two;
			*scale = item_conversions[i].scale;
			return;
		}	
	}
}

int standingOnM2Object(int index) {
	return (Player->touching_object == 1) && (Player->standing_on_index == index);
}