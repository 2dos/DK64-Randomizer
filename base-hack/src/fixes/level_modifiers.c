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

#define FUNGI_TOD_LENGTH 4500 // 2.5 * 60 * 30 (2.5 minutes)
#define FUNGI_SEG_LENGTH 1500
static short progressive_time_of_day = FUNGI_SEG_LENGTH;
static float subseg_brightnesses[6] = {
	0.77f,
	1.00f, // Peak Daytime
	0.77f,
	0.53f,
	0.30f, // Peak Nighttime
	0.53f,
};

void handleTimeOfDay(time_of_day_calls call) {
	fungi_time time = Rando.fungi_time_of_day_setting;
	if (time == TIME_NIGHT) {
		if (call == TODCALL_INITFILE) {
			setFlag(FLAG_MODIFIER_FUNGINIGHT, 1, FLAGTYPE_PERMANENT);
		}
	} else if (time == TIME_PROGRESSIVE) {
		if (call == TODCALL_FUNGIACTIVE) {
			// Increment Timer
			int force_update = ObjectModel2Timer < 2;
			int was_night = progressive_time_of_day >= FUNGI_TOD_LENGTH;
			int prev_tod_subseg = progressive_time_of_day / FUNGI_SEG_LENGTH;
			progressive_time_of_day += 1;
			if (progressive_time_of_day >= FUNGI_TOD_LENGTH * 2) {
				progressive_time_of_day = 0;
			}
			int is_night = progressive_time_of_day >= FUNGI_TOD_LENGTH;
			int tod_subseg = progressive_time_of_day / FUNGI_SEG_LENGTH;
			if ((was_night != is_night) || (force_update)) {
				// Handle objects
				setFlag(FLAG_MODIFIER_FUNGINIGHT, is_night, FLAGTYPE_PERMANENT);
				if (Player) {
					if (is_night) {
						Player->strong_kong_ostand_bitfield |= FUNGI_NIGHT_CHECK;
					} else {
						Player->strong_kong_ostand_bitfield &= ~FUNGI_NIGHT_CHECK;
					}
				}
			}
			if ((prev_tod_subseg != tod_subseg) || (force_update)) {
				if (tod_subseg < 6) {
					// Handle skylight
					float brightness = subseg_brightnesses[tod_subseg];
					float blueness = 1.0f - ((1.0f - brightness) / 2);
					for (int i = 0; i < chunk_count; i++) {
						setChunkLighting(brightness, brightness, blueness, i);
					}
				}
			}
		}
	}
}