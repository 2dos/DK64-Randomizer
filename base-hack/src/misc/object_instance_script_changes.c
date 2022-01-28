#include "../../include/common.h"

#define GLOOMY_GALLEON 0x1E
#define ANGRY_AZTEC 0x26
#define FUNGI_FOREST 0x30

#define FUNGI_MINECART_GRATE 0x22
#define SEASICK_SHIP 0x27
#define AZTEC_BEETLE_GRATE 0x1E

void change_object_scripts(int code_pointer, int id, int index, int param2) {
	if ((CurrentMap == GLOOMY_GALLEON) && (id == SEASICK_SHIP)) {
		if (Rando.randomize_more_loading_zones) {
			initiateTransition_0((Rando.seasick_ship_enter >> 8) & 0xFF, Rando.seasick_ship_enter & 0xFF, 0, 0);
		} else {
			initiateTransition_0(31, 0, 0, 0);
		}
	} else if ((CurrentMap == ANGRY_AZTEC) && (id == AZTEC_BEETLE_GRATE)) {
		if (Rando.randomize_more_loading_zones) {
			initiateTransition_0((Rando.aztec_beetle_enter >> 8) & 0xFF, Rando.aztec_beetle_enter & 0xFF, 0, 0);
		} else {
			initiateTransition_0(14, 0, 0, 0);
		}
	} else if ((CurrentMap == FUNGI_FOREST) && (id == FUNGI_MINECART_GRATE)) {
		if (Rando.randomize_more_loading_zones) {
			initiateTransition_0((Rando.fungi_minecart_enter >> 8) & 0xFF, Rando.fungi_minecart_enter & 0xFF, 0, 0);
		} else {
			initiateTransition_0(55, 0, 0, 0);
		}
	} else {
		InstanceScriptParams[1] = id;
		InstanceScriptParams[2] = index;
		InstanceScriptParams[3] = param2;
	}
}