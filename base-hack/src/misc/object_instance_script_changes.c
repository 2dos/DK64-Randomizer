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
#define LLAMA_TEMPLE 0x14
#define JAPES_MOUNTAIN 0x4
#define MILL_FRONT 0x3D
#define MILL_REAR 0x3E
#define FUNGI_GMUSH 0x40

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
#define AZTEC_SNOOPDOOR 0x26
#define LLAMA_SNOOPPAD 0x2C
#define JAPES_DKCAGEGB 0x43
#define JAPES_DKCAGESWITCH 0x40
#define JAPES_MOUNTAINGB 0x51
#define JAPES_MOUNTAINGBSWITCH 0xB
#define FACTORY_DIDDYPRODGB 0x2C
#define FACTORY_DIDDYPRODSWITCH 0x31
#define MILL_WARNINGLIGHTS 0xC
#define MILL_CRUSHER 0x8
#define MILL_TRIANGLEPAD 0x0
#define GMUSH_BOARD 0xB
#define CAVES_GBDOME 0x27
#define CAVES_BOULDERDOME 0x2B
#define CAVES_SMALLBOULDERPAD 0x2E
#define CAVES_BIGBOULDERPAD 0x2F


#define ISLES_JAPESBOULDER 0x19
#define ISLES_AZTECDOOR 0x02
#define ISLES_FACTORYPLATFORM 0x04
#define ISLES_FACTORYDOOR 0x05
#define ISLES_GALLEONBARS 0x03
#define ISLES_FUNGIBOULDER 0x20
#define ISLES_CAVESBOULDER 0x1A
#define ISLES_CASTLEROCK 0x33
#define ISLES_HELMJAW 0x1B

#define MILL_CRUSHER_PROGRESS 1

void hideObject(behaviour_data* behaviour_pointer) {
	behaviour_pointer->unk_60 = 1;
	behaviour_pointer->unk_62 = 0;
	behaviour_pointer->unk_66 = 255;
	behaviour_pointer->unk_70 = 0;
	behaviour_pointer->unk_71 = 0;
	setScriptRunState(behaviour_pointer,2,0);
}

void change_object_scripts(behaviour_data* behaviour_pointer, int id, int index, int param2) {
	switch(CurrentMap) {
		case GLOOMY_GALLEON:
			if (id == SEASICK_SHIP) {
				if (Rando.randomize_more_loading_zones) {
					initiateTransition_0((Rando.seasick_ship_enter >> 8) & 0xFF, Rando.seasick_ship_enter & 0xFF, 0, 0);
				} else {
					initiateTransition_0(31, 0, 0, 0);
				}
			}
			break;
		case ANGRY_AZTEC:
			if (id == AZTEC_BEETLE_GRATE) {
				if (Rando.randomize_more_loading_zones) {
					initiateTransition_0((Rando.aztec_beetle_enter >> 8) & 0xFF, Rando.aztec_beetle_enter & 0xFF, 0, 0);
				} else {
					initiateTransition_0(14, 0, 0, 0);
				}
			} else if (id == AZTEC_SNOOPDOOR) {
				if (index == 0) {
					// Flag Check
					if (checkFlag(SNOOPDOOR_OPEN,0)) {
						behaviour_pointer->next_state = 40;
						behaviour_pointer->current_state = 40;
					}
				} else if (index == 1) {
					// Flag Set
					setPermFlag(SNOOPDOOR_OPEN);
					setNextTransitionType(0);
				}
			}
			break;
		case FUNGI_FOREST:
			if (id == FUNGI_MINECART_GRATE) {
				if (Rando.randomize_more_loading_zones) {
					initiateTransition_0((Rando.fungi_minecart_enter >> 8) & 0xFF, Rando.fungi_minecart_enter & 0xFF, 0, 0);
				} else {
					initiateTransition_0(55, 0, 0, 0);
				}
			}
			break;
		case CASTLE_BALLROOM:
			if (id == BALLROOM_MONKEYPORT) {
				if (Rando.randomize_more_loading_zones) {
					createCollisionObjInstance(COLLISION_MAPWARP,(Rando.ballroom_to_museum >> 8 & 0xFF), Rando.ballroom_to_museum & 0xFF);
				} else {
					createCollisionObjInstance(COLLISION_MAPWARP,113,2);
				}
			}
			break;
		case CASTLE_MUSEUM:
			if (id == MUSEUM_WARP_MONKEYPORT) {
				if (Rando.randomize_more_loading_zones) {
					createCollisionObjInstance(COLLISION_MAPWARP,(Rando.museum_to_ballroom >> 8 & 0xFF), Rando.museum_to_ballroom & 0xFF);
				} else {
					createCollisionObjInstance(COLLISION_MAPWARP,88,1);
				}
			}
			break;
		case DK_ISLES:
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
				// TestVariable = (int)behaviour_pointer;
				// *(int*)(0x807FF700) = id;
			}
			break;
		case LLAMA_TEMPLE:
			if (id == LLAMA_SNOOPPAD) {
				if (checkFlag(SNOOPDOOR_OPEN,0)) {
					behaviour_pointer->current_state = 20;
					behaviour_pointer->next_state = 20;
				}
			}
			break;
		case JUNGLE_JAPES:
			if (id == JAPES_DKCAGEGB) {
				if (index == 0) {
					if (checkFlag(DKJAPESCAGEGB_OPEN,0)) {
						behaviour_pointer->current_state = 6;
						behaviour_pointer->next_state = 6;
						behaviour_pointer->unk_38 = unkObjFunction3(0,2,1,2,*(int*)(0x807F6220),*(int*)(0x807F6224),*(int*)(0x807F621C));
						unkObjFunction4(behaviour_pointer->unk_38,1);
						unkObjFunction5(behaviour_pointer->unk_38,1);
						unkObjFunction6(behaviour_pointer->unk_38,5);
					}
				} else if (index == 1) {
					setPermFlag(DKJAPESCAGEGB_OPEN);
				}
			} else if (id == JAPES_DKCAGESWITCH) {
				if (checkFlag(DKJAPESCAGEGB_OPEN,0)) {
					behaviour_pointer->current_state = 20;
					behaviour_pointer->next_state = 20;
				}
			} else if (id == JAPES_MOUNTAINGB) {
				if (index == 0) {
					if (checkFlag(JAPESMOUNTAINSPAWNED,0)) {
						behaviour_pointer->current_state = 20;
						behaviour_pointer->next_state = 20;
					}
				} else if (index == 1) {
					setPermFlag(JAPESMOUNTAINSPAWNED);
				}
			}
			break;
		case JAPES_MOUNTAIN:
			if (id == JAPES_MOUNTAINGBSWITCH) {
				if (checkFlag(JAPESMOUNTAINSPAWNED,0)) {
					behaviour_pointer->current_state = 20;
					behaviour_pointer->next_state = 20;
				}
			}
			break;
		case FRANTIC_FACTORY:
			if (id == FACTORY_DIDDYPRODGB) {
				if (index == 0) {
					if (checkFlag(FACTORYDIDDYPRODSPAWNED,0)) {
						behaviour_pointer->current_state = 11;
						behaviour_pointer->next_state = 11;
					}
				} else if (index == 1) {
					setPermFlag(FACTORYDIDDYPRODSPAWNED);
				}
			} else if (id == FACTORY_DIDDYPRODSWITCH) {
				if (checkFlag(FACTORYDIDDYPRODSPAWNED,0)) {
					behaviour_pointer->current_state = 20;
					behaviour_pointer->next_state = 20;
				}
			}
			break;
		case MILL_FRONT:
			if (id == MILL_WARNINGLIGHTS) {
				if (checkFlag(FUNGICRUSHERON,0)) {
					//behaviour_pointer->current_state = MILL_CRUSHER_PROGRESS * 2;
					//behaviour_pointer->next_state = MILL_CRUSHER_PROGRESS * 2;
				}
			} else if (id == MILL_CRUSHER) {
				if (index == 0) {
					if (checkFlag(FUNGICRUSHERON,0)) {
						if (!checkFlag(221,0)) { // If GB not acquired
							if (behaviour_pointer->counter == 0) {
								// behaviour_pointer->counter = MILL_CRUSHER_PROGRESS;
								behaviour_pointer->current_state = 12;
								behaviour_pointer->next_state = 12;
								unkObjFunction1(id,1,8);
								unkObjFunction2(id,1,65535);
							}
						}
					}
				} else if (index == 1) {
					setPermFlag(FUNGICRUSHERON);
					behaviour_pointer->counter = MILL_CRUSHER_PROGRESS;
				}
			}
			break;
		case MILL_REAR:
			if (id == MILL_TRIANGLEPAD) {
				if (checkFlag(FUNGICRUSHERON,0)) {
					behaviour_pointer->current_state = 3;
					behaviour_pointer->next_state = 3;
				}
			}
			break;
		case FUNGI_GMUSH:
			if (id == GMUSH_BOARD) {
				int switch_count = 0;
				for (int i = 0; i < 5; i++) {
					switch_count += checkFlag(0xE6 + i,0);
				}
				if (switch_count == 5) {
					behaviour_pointer->current_state = 6;
					behaviour_pointer->next_state = 6;
					behaviour_pointer->timer = 465;
				}
			}
			break;
		case CRYSTAL_CAVES:
			if (id == CAVES_GBDOME) {
				if (index == 0) {
					if (checkFlag(CAVESGBDOME_DESTROYED,0)) {
						hideObject(behaviour_pointer);
						behaviour_pointer->current_state = 11;
						behaviour_pointer->next_state = 11;
					}
				} else if (index == 1) {
					setPermFlag(CAVESGBDOME_DESTROYED);
				}
			} else if (id == CAVES_SMALLBOULDERPAD) {
				if (checkFlag(CAVESBOULDERDOME_DESTROYED,0)) {
					behaviour_pointer->current_state = 20;
					behaviour_pointer->next_state = 20;
				}
			} else if (id == CAVES_BOULDERDOME) {
				if (index == 0) {
					if (checkFlag(CAVESBOULDERDOME_DESTROYED,0)) {
						hideObject(behaviour_pointer);
						behaviour_pointer->current_state = 11;
						behaviour_pointer->next_state = 11;
					}
				} else if (index == 1) {
					setPermFlag(CAVESBOULDERDOME_DESTROYED);
				}
			} else if (id == CAVES_BIGBOULDERPAD) {
				if (checkFlag(CAVESBOULDERDOME_DESTROYED,0)) {
					if (checkFlag(CAVESGBDOME_DESTROYED,0)) {
						hideObject(behaviour_pointer);
						behaviour_pointer->current_state = 20;
						behaviour_pointer->next_state = 20;
					} else {
						behaviour_pointer->current_state = 10;
						behaviour_pointer->next_state = 10;
					}
				}
			}
		break;
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