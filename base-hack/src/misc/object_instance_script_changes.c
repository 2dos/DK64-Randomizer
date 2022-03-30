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
#define DK_ISLES 0x22

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

#define ISLES_JAPESBOULDER 0x19
#define ISLES_AZTECDOOR 0x02
#define ISLES_FACTORYPLATFORM 0x04
#define ISLES_FACTORYDOOR 0x05
#define ISLES_GALLEONBARS 0x03
#define ISLES_FUNGIBOULDER 0x20
#define ISLES_CAVESBOULDER 0x1A
#define ISLES_CASTLEROCK 0x33
#define ISLES_HELMJAW 0x1B

void hideObject(behaviour_data* behaviour_pointer) {
	behaviour_pointer->unk_60 = 1;
	behaviour_pointer->unk_62 = 0;
	behaviour_pointer->unk_66 = 255;
	behaviour_pointer->unk_70 = 0;
	behaviour_pointer->unk_71 = 0;
	setScriptRunState(behaviour_pointer,2,0);
}

void change_object_scripts(behaviour_data* behaviour_pointer, int id, int index, int param2) {
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
	} else if (CurrentMap == DK_ISLES) {
		if (id == ISLES_JAPESBOULDER) {
			if (Rando.lobbies_open_bitfield & 1) {
				hideObject(behaviour_pointer);
			}
		} else if (id == ISLES_AZTECDOOR) {
			if (Rando.lobbies_open_bitfield & 2) {
				hideObject(behaviour_pointer);
			}
		} else if (id == ISLES_FACTORYPLATFORM) {
			if (Rando.lobbies_open_bitfield & 4) {
				behaviour_pointer->next_state = 5;
				unkObjFunction0(id,1,0);
				unkObjFunction1(id,1,5);
				unkObjFunction2(id,1,1);
			}
		} else if (id == ISLES_FACTORYDOOR) {
			if (Rando.lobbies_open_bitfield & 4) {
				hideObject(behaviour_pointer);
			}
		} else if (id == ISLES_GALLEONBARS) {
			if (Rando.lobbies_open_bitfield & 8) {
				hideObject(behaviour_pointer);
			}
		} else if (id == ISLES_FUNGIBOULDER) {
			if (Rando.lobbies_open_bitfield & 0x10) {
				hideObject(behaviour_pointer);
			}
		} else if (id == ISLES_CAVESBOULDER) {
			if (Rando.lobbies_open_bitfield & 0x20) {
				hideObject(behaviour_pointer);
			}
		} else if (id == ISLES_CASTLEROCK) {
			if (Rando.lobbies_open_bitfield & 0x40) {
				hideObject(behaviour_pointer);
			}
		} else if (id == ISLES_HELMJAW) {
			if (Rando.lobbies_open_bitfield & 0x80) {
				behaviour_pointer->current_state = 100;
				behaviour_pointer->next_state = 100;
				unkObjFunction1(id,2,25);
				unkObjFunction2(id,2,1);
				unkObjFunction2(id,3,1);
			}
		} else {
			TestVariable = (int)behaviour_pointer;
			*(int*)(0x807FF700) = id;
		}
	}
	InstanceScriptParams[1] = id;
	InstanceScriptParams[2] = index;
	InstanceScriptParams[3] = param2;
}

void spawnCannon(actorData* cannon) {
	cannon->shadow_intensity = 0xFF;
	cannon->obj_props_bitfield |= 0x8000;
	cannon->control_state = 0;
	cannon->noclip_byte = 2;
}

int spawnCannonWrapper(void) {
	if (CurrentMap == DK_ISLES) {
		int spawner_id = getActorSpawnerIDFromTiedActor(CurrentActorPointer);
		if (spawner_id == 8) { // Castle Cannon
			if (Rando.lobbies_open_bitfield & 0x40) {
				return 1;
			}
		} else if (spawner_id == 18) { // Fungi Cannon
			if (Rando.lobbies_open_bitfield & 0x10) {
				return 1;
			}
		} 
	}
	return 0;
}