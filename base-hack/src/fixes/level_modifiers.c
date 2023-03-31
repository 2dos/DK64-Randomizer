/**
 * @file level_modifiers.c
 * @author Ballaam
 * @brief Modify level behaviour so that key level attributes work when spawning into the world from differing locations.
 * @version 0.1
 * @date 2022-01-30
 * 
 * @copyright Copyright (c) 2022
 * 
 */

#include "../../include/common.h"

#define TORCH_ALT 0xC7

void load_object_script(int obj_instance_id) {
	/**
	 * @brief Load an object script into the script cache
	 */
	scriptLoadsAttempted += 1;
	int script_index = scriptsLoaded;
	if (script_index != 0x46) {
		scriptsLoaded = script_index + 1;
		scriptLoadedArray[script_index] = obj_instance_id;
		int obj_idx = convertIDToIndex(obj_instance_id);
		int* m2location = (int*)ObjectModel2Pointer;
		ModelTwoData* _object = getObjectArrayAddr(m2location,0x90,obj_idx);
		int* behav = _object->behaviour_pointer;
		updateObjectScript(behav);
		executeBehaviourScript(behav, _object->sub_id);
	}
}

void adjust_level_modifiers(void) {
	/**
	 * @brief Adjust level modifiers on map load
	 */
	if (ObjectModel2Timer < 5) {
		if (CurrentMap == MAP_GALLEON) {
			// Water Level
			load_object_script(0); // Up Switch
			load_object_script(1); // Down Switch
			if (checkFlag(FLAG_MODIFIER_GALLEONWATER,FLAGTYPE_PERMANENT)) {
				// Adjust water height in all chunks if water is raised
				for (int i = 0; i < 20; i++) {
					setWaterHeight(i,55.0f,1000.0f);
				}
			}
		} else if (CurrentMap == MAP_AZTEC) {
			// Sandstorm Effect
			load_object_script(0xC1);
		} else if (CurrentMap == MAP_CAVES) {
			// Giant Kosha Timer
			load_object_script(0x31);
		} else if (CurrentMap == MAP_FUNGI) {
			// Daytime/Nighttime
			load_object_script(0x4);
		}
	}
}