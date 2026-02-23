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

int isBonus(maps map) {
	/**
	 * @brief Is map queried a bonus map
	 * 
	 * @param map Map index being queried
	 * 
	 * @return Is bonus map (bool)
	 */
	if (map == MAP_MAINMENU) {
		return 0;
	} else if (inBattleCrown(map)) {
		return 0;
	}
	level_indexes level = levelIndexMapping[map];
	return (level == LEVEL_BONUS) || (level == LEVEL_SHARED);
}

int standingOnM2Object(int index) {
	return (Player->touching_object == 1) && (Player->standing_on_index == index);
}

int checkSlamLocation(int kong, int key, int id) {
	/**
	 * @brief Check slam location
	 * 
	 * @param kong Required kong
	 * @param key Index in Object Model Two Array
	 * @param id Object ID of target
	 */
	if (Character == kong) {
		if (Player) {
			if ((Player->obj_props_bitfield & 0x2000) == 0) {
				if (standingOnM2Object(id)) {
					if (Player->standing_on_subposition == key) {
						return 1;
					}
				}
			}
		}
	}
	return 0;
}

void playSFXContainer(int id, int vanilla_sfx, int new_sfx) {
	/**
	 * @brief Container function for playing a SFX from an object
	 * 
	 * @param id Object ID
	 * @param vanilla_sfx Original SFX
	 * @param new_sfx New SFX to be played. If 0, defaults to vanilla_sfx
	 */
	int index = convertIDToIndex(id);
	if (index == -1) {
		index = 0;
	}
	int sfx_played = new_sfx;
	if (new_sfx == 0) {
		sfx_played = vanilla_sfx;
	}
	playSFXFromObject(index,sfx_played,-1,127,0,0,0.3f);
}