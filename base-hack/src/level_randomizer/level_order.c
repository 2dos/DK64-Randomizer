#include "../../include/common.h"

#define TRIGGER_ELEMENT_SIZE 0x3A
#define LOBBY_COUNT 7
#define ISLES_OVERWORLD 0x22

static const unsigned char lobbies[] = {0xA9,0xAD,0xAF,0xAE,0xB2,0xC2,0xC1,0xAA};
static const unsigned char lobbyexits[] = {2,3,4,5,6,10,11,7};
static const short normal_key_flags[] = {0x1A,0x4A,0x8A,0xA8,0xEC,0x124,0x13D};

void randomizeLevelOrder(void) {
	if (ObjectModel2Timer == 2) {
		if (TriggerArray) {
			for (int i = 0; i < TriggerSize; i++) {
				trigger* focused_trigger = getObjectArrayAddr(TriggerArray,TRIGGER_ELEMENT_SIZE,i);
				if (focused_trigger->type == 9) {
					if (CurrentMap == ISLES_OVERWORLD) {
						// Change Map
						int j = 0;
						do {
							if (lobbies[j] == focused_trigger->map) {
								focused_trigger->map = lobbies[(int)Rando.level_order[j]];
								break;
							}
						} while (j++ < LOBBY_COUNT);
					} else if (focused_trigger->map == ISLES_OVERWORLD) {
						// Change Exit
						int k = 0;
						do {
							if (lobbies[k] == CurrentMap) { // Get Current Lobby Index
								int a = 0;
								do {
									if (k == Rando.level_order[a]) {
										focused_trigger->exit = lobbyexits[a];
										break;
									}
								} while (a++ < LOBBY_COUNT);
								break;
							}
						} while (k++ < LOBBY_COUNT);
					}
				}
			}
		}
		if (CurrentMap == ISLES_OVERWORLD) {
			if (isRDRAM(CastleCannonPointer)) {
				if (CastleCannonPointer->source_map == ISLES_OVERWORLD) {
					CastleCannonPointer->destination_map = lobbies[(int)Rando.level_order[6]];
				}
			}
		}
	}
}

void swapRequirements(void) {
	if (TransitionSpeed < 0) {
		for (int i = 0; i < 8; i++) {
			if (i < 7) {
				TroffNScoffReqArray[i] = Rando.troff_scoff_count[i];
			}
			BLockerDefaultArray[i] = Rando.blocker_normal_count[i];
			BLockerCheatArray[i].gb_count = Rando.blocker_cheat_count[i];
			if (levelIndexMapping[CurrentMap] == 7) {
				// In Isles
				CheckmarkKeyArray[i] = Rando.key_flags[i];
			} else {
				CheckmarkKeyArray[i] = normal_key_flags[i];
			}
			
		}
	}
}

void level_order_rando_funcs(void) {
	if (Rando.level_order_rando_on) {
		randomizeLevelOrder();
		swapRequirements();
	}
}