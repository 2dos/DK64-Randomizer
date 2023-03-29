#include "../../include/common.h"

#define TRIGGER_ELEMENT_SIZE 0x3A
#define LOBBY_COUNT 7

static const unsigned char lobbies[] = {
	MAP_JAPESLOBBY,
	MAP_AZTECLOBBY,
	MAP_FACTORYLOBBY,
	MAP_GALLEONLOBBY,
	MAP_FUNGILOBBY,
	MAP_CAVESLOBBY,
	MAP_CASTLELOBBY
};
static const unsigned char lobbyexits[] = {2,3,4,5,6,10,11};

void randomizeLevelOrder(void) {
	if (ObjectModel2Timer == 2) {
		if (TriggerArray) {
			for (int i = 0; i < TriggerSize; i++) {
				if (TriggerArray[i].type == 9) {
					if (CurrentMap == MAP_ISLES) {
						// Change Map
						int j = 0;
						while (j < LOBBY_COUNT) {
							if (lobbies[j] == TriggerArray[i].map) {
								TriggerArray[i].map = lobbies[(int)Rando.level_order[j]];
								break;
							}
							j++;
						}
					} else if (TriggerArray[i].map == MAP_ISLES) {
						// Change Exit
						int k = 0;
						while (k < LOBBY_COUNT) {
							if (lobbies[k] == CurrentMap) { // Get Current Lobby Index
								int a = 0;
								while (a < LOBBY_COUNT) {
									if (k == Rando.level_order[a]) {
										TriggerArray[i].exit = lobbyexits[a];
										break;
									}
									a++;
								}
								break;
							}
							k++;
						}
					}
				}
			}
		}
		if (CurrentMap == MAP_ISLES) {
			if (isRDRAM(CastleCannonPointer)) {
				if (CastleCannonPointer->source_map == MAP_ISLES) {
					CastleCannonPointer->destination_map = lobbies[(int)Rando.level_order[6]];
				}
			}
		}
	}
}

void swapRequirements(int key_swap) {
	if (TransitionSpeed < 0) {
		for (int i = 0; i < 8; i++) {
			if (i < 7) {
				if (Rando.troff_scoff_count[i] > 0) {
					TroffNScoffReqArray[i] = Rando.troff_scoff_count[i];
				} else {
					TroffNScoffReqArray[i] = 1;
					CBTurnedInArray[i] = 1;
				}
			}
			BLockerDefaultArray[i] = Rando.blocker_normal_count[i];
			BLockerCheatArray[i].gb_count = Rando.blocker_normal_count[i];
			if ((key_swap) && (i < 7)) {
				if (levelIndexMapping[CurrentMap] == 7) {
					// In Isles
					CheckmarkKeyArray[i] = Rando.key_flags[i];
				} else {
					CheckmarkKeyArray[i] = normal_key_flags[i];
				}
			}
			
		}
	}
}

void level_order_rando_funcs(void) {
	if (Rando.level_order_rando_on) {
		randomizeLevelOrder();
		swapRequirements(1);
	} else {
		swapRequirements(0);
	}
}