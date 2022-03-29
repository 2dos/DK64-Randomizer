#include "../../include/common.h"

#define GLOOMY_GALLEON 0x1E
#define ANGRY_AZTEC 0x26
#define FUNGI_FOREST 0x30
#define CASTLE_BALLROOM 0x58
#define CASTLE_MUSEUM 0x71
#define JUNGLE_JAPES 0x7
#define FRANTIC_FACTORY 0x1A
#define CRYSTAL_CAVES 0x48
#define CREEPY_CASTLE 0x57

#define FUNGI_MINECART_GRATE 0x22
#define SEASICK_SHIP 0x27
#define AZTEC_BEETLE_GRATE 0x1E
#define BALLROOM_MONKEYPORT 0x5
#define MUSEUM_WARP_MONKEYPORT 0x8
#define JAPES_BBLAST 0xA3
#define FACTORY_BBLAST 0x4D
#define CAVES_BBLAST 0x20
#define CASTLE_BBLAST 0x1F
#define AZTEC_BBLAST 0x2E
#define GALLEON_BBLAST 0x34
#define FUNGI_BBLAST 0x4C

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
	} else if ((CurrentMap == CASTLE_BALLROOM) && (id == BALLROOM_MONKEYPORT)) {
		if (Rando.randomize_more_loading_zones) {
			createCollisionObjInstance(COLLISION_MAPWARP,(Rando.ballroom_to_museum >> 8 & 0xFF), Rando.ballroom_to_museum & 0xFF);
		} else {
			createCollisionObjInstance(COLLISION_MAPWARP,113,2);
		}
	} else if ((CurrentMap == CASTLE_MUSEUM) && (id == MUSEUM_WARP_MONKEYPORT)) {
		if (Rando.randomize_more_loading_zones) {
			createCollisionObjInstance(COLLISION_MAPWARP,(Rando.museum_to_ballroom >> 8 & 0xFF), Rando.museum_to_ballroom & 0xFF);
		} else {
			createCollisionObjInstance(COLLISION_MAPWARP,88,1);
		}
	}
	InstanceScriptParams[1] = id;
	InstanceScriptParams[2] = index;
	InstanceScriptParams[3] = param2;
}