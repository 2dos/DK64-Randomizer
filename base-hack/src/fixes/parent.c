#include "../../include/common.h"

#define PARENT_FILTER_THRESHOLD 14
#define LOCK_STACK_THRESHOLD 28

// void wipeParentSlot(int index) {
// 	if (SubmapData[index].slot_populated) {
// 		wipeStoredSetup(&SubmapData[index].setup);
// 		complex_free(SubmapData[index].setup);
// 		if (SubmapData[index].uses_extra_setup) {
// 			wipeStoredSetup(&SubmapData[index].setup2);
// 			complex_free(SubmapData[index].setup2);
// 		}
// 		SubmapData[index].slot_populated = 0;
// 	}
// }

// void shuffleParents(void) {
// 	for (int i = 1; i < 0x12; i++) {
// 		if (SubmapData[i].slot_populated) {
// 			// Shuffle
// 			int vacant = -1;
// 			for (int j = 0; j < i; j++) {
// 				if ((SubmapData[j].slot_populated == 0) && (SubmapData[j].parent_map != CurrentMap)) {
// 					vacant = j;
// 					wipeParentSlot(j);
// 				}
// 			}
// 			if (vacant > -1) {
// 				// Has previous vacant slot
// 				dk_memcpy(&SubmapData[vacant].slot_populated, &SubmapData[i].slot_populated, 0xC0);
// 				wipeMemory(&SubmapData[i].slot_populated,0xC0);
// 			}
// 		}
// 	}
// }

// static const unsigned char main_levels[] = {0x7,0x26,0x1A,0x1E,0x30,0x48,0x57,0x11};
// static const unsigned char boss_maps[] = {0x8,0xC5,0x9A,0x6F,0x53,0xC4,0xC7};
// #define CUSTOM_CHAIN_LENGTH 0x12
// static unsigned char custom_map_chain[CUSTOM_CHAIN_LENGTH] = {};
// static char chain_index = -1;

// void parentFilter(void) {
// 	int used = 0;
// 	for (int i = 0; i < 0x12; i++) {
// 		if (SubmapData[i].slot_populated) {
// 			used += 1;
// 		}
// 	}
// 	if ((used > PARENT_FILTER_THRESHOLD) || (LockStackCount >= LOCK_STACK_THRESHOLD)) {
// 		for (int i = 0; i < 0x12; i++) {
// 			if (SubmapData[i].slot_populated) {
// 				int good_map = 0;
// 				int curr_map = SubmapData[i].parent_map;
// 				for (int j = 0; j < sizeof(main_levels); j++) {
// 					if (curr_map == main_levels[j]) {
// 						good_map = 1; // 8
// 					}
// 				}
// 				// 1
// 				if ((curr_map == 5) && ((CurrentMap == 9) || (DestMap == 9))) {
// 					good_map = 1;
// 				}
// 				if (curr_map == custom_map_chain[chain_index - 1]) {
// 					good_map = 1;
// 				}
// 				// 1
// 				if (curr_map == 61) {
// 					// Grinder
// 					good_map = 1;
// 				}
// 				// 1
// 				for (int j = 0; j < sizeof(boss_maps); j++) {
// 					if ((curr_map == 0x2A) && ((CurrentMap == boss_maps[j]) || (DestMap == boss_maps[j]))) {
// 						good_map = 1;
// 					}
// 				}
// 				// 4
// 				for (int j = 0; j < CUSTOM_CHAIN_LENGTH; j++) {
// 					if ((custom_map_chain[j] == 5) || (custom_map_chain[j] == 15) || (custom_map_chain[j] == 0x2A) || (custom_map_chain[j] == 1)) {
// 						if (j > 0) {
// 							if (curr_map == (custom_map_chain[j - 1])) {
// 								good_map = 1;
// 							}
// 						}
// 					}
// 				}
// 				if (!good_map) {
// 					wipeParentSlot(i);
// 				}
// 			}
// 		}
// 	}
// }

// void pushToCustomChain(int map) {
// 	int pop = 0;
// 	for (int i = 0; i < CUSTOM_CHAIN_LENGTH; i++) {
// 		if (pop) {
// 			custom_map_chain[i] = 0;
// 		} else if (custom_map_chain[i] == map) {
// 			pop = 1;
// 			chain_index = i;
// 		}
// 	}
// 	chain_index += 1;
// 	if (chain_index < CUSTOM_CHAIN_LENGTH) {
// 		custom_map_chain[(int)chain_index] = map;
// 	} else {
// 		// Shift
// 		for (int i = 0; i < (CUSTOM_CHAIN_LENGTH - 1); i++) {
// 			custom_map_chain[i] = custom_map_chain[i + 1];
// 		}
// 		chain_index = CUSTOM_CHAIN_LENGTH - 1;
// 		custom_map_chain[(int)chain_index] = map;
// 	}
// }

// static const unsigned char banned_filter_non_boss_maps[] = {
// 	1, // Funky's
// 	2, // Arcade
// 	5, // Cranky's
// 	9, // Jetpac
// 	15, // Snide's
// 	0x19, // Candy's
// 	0x2A, // T&S
// 	0x33, // Mech Fish
// };

// void callParentMapFilter(void) {
// 	if (ObjectModel2Timer == 2) {
// 		*(int*)(0x807FF708) = (int)&custom_map_chain[0];
// 		pushToCustomChain(CurrentMap);
// 		int curr = CurrentMap;
// 		int banned = 0;
// 		for (int i = 0; i < sizeof(banned_filter_non_boss_maps); i++) {
// 			if (curr == banned_filter_non_boss_maps[i]) {
// 				banned = 1;
// 			}
// 		}
// 		for (int i = 0; i < sizeof(boss_maps); i++) {
// 			if (curr == boss_maps[i]) {
// 				banned = 1;
// 			}
// 		}
// 		if ((levelIndexMapping[curr] == 9) || (levelIndexMapping[curr] == 0xD)) {
// 			banned = 1;
// 		}
// 		if (!banned) {
// 			parentFilter();
// 			//shuffleParents();
// 		}
// 	}
// }

static const unsigned char banned_filter_maps[] = {
	1, // Funky's
	2, // Arcade
	5, // Cranky's
	9, // Jetpac
	15, // Snide's
	0x19, // Candy's
	0x2A, // T&S
	0x33, // Mech FIsh
	0x8, // Japes Dillo
	0xC5, // Aztec Dog
	0x9A, // MJ
	0x6F, // Pufftoss
	0x53, // Fungi Dog
	0xC4, // Caves Dillo
	0xC7, // KKO
	61, // Mill Front
	62, // Mill Rear
	0x14, // Llama Temple
	0x26, // Angry Aztec
	0x30, // Fungi Forest
	0x4, // Mountain
	0x29, // Aztec BBlast
	0x36, // Galleon BBlast
	0x6E, // Factory BBlast
	0xBB, // Castle BBlast
	0x7, // Japes
	0x25, // Japes BBlast
};

void callParentMapFilter(void) {
	if (Rando.randomize_more_loading_zones) {
		if (ObjectModel2Timer == 2) {
			int curr = CurrentMap;
			int level = levelIndexMapping[curr];
			if (level < 7) {
				setPermFlag(453 + level);
			}
			int banned = 0;
			for (int i = 0; i < sizeof(banned_filter_maps); i++) {
				if (banned_filter_maps[i] == curr) {
					banned = 1;
				}
			}
			if ((level == 9) || (level == 0xD)) {
				banned = 1;
			}
			if (!banned) {
				resetMapContainer();
			}
		} else if (ObjectModel2Timer < 2) {
			correctDKPortal();
		}
	}
}