#include "../../include/common.h"

#define PARENT_FILTER_THRESHOLD 14
#define LOCK_STACK_THRESHOLD 28

void wipeParentSlot(int index) {
	if (SubmapData[index].slot_populated) {
		wipeStoredSetup(&SubmapData[index].setup);
		complex_free(SubmapData[index].setup);
		if (SubmapData[index].uses_extra_setup) {
			wipeStoredSetup(&SubmapData[index].setup2);
			complex_free(SubmapData[index].setup2);
		}
		SubmapData[index].slot_populated = 0;
	}
}

static const unsigned char main_levels[] = {0x7,0x26,0x1A,0x1E,0x30,0x48,0x57,0x11};
static const unsigned char boss_maps[] = {0x8,0xC5,0x9A,0x6F,0x53,0xC4,0xC7};
#define CUSTOM_CHAIN_LENGTH 0x12
static unsigned char custom_map_chain[CUSTOM_CHAIN_LENGTH] = {};
static char chain_index = -1;

void parentFilter(void) {
	int used = 0;
	for (int i = 0; i < 0x12; i++) {
		if (SubmapData[i].slot_populated) {
			used += 1;
		}
	}
	if ((used > PARENT_FILTER_THRESHOLD) || (LockStackCount >= LOCK_STACK_THRESHOLD)) {
		for (int i = 0; i < 0x12; i++) {
			if (SubmapData[i].slot_populated) {
				int good_map = 0;
				int curr_map = SubmapData[i].parent_map;
				for (int j = 0; j < sizeof(main_levels); j++) {
					if (curr_map == main_levels[j]) {
						good_map = 1; // 8
					}
				}
				// 1
				if ((curr_map == 5) && ((CurrentMap == 9) || (DestMap == 9))) {
					good_map = 1;
				}
				if (curr_map == custom_map_chain[chain_index - 1]) {
					good_map = 1;
				}
				// 1
				if (curr_map == 61) {
					// Grinder
					good_map = 1;
				}
				// 1
				for (int j = 0; j < sizeof(boss_maps); j++) {
					if ((curr_map == 0x2A) && ((CurrentMap == boss_maps[j]) || (DestMap == boss_maps[j]))) {
						good_map = 1;
					}
				}
				// 3
				for (int j = 0; j < CUSTOM_CHAIN_LENGTH; j++) {
					if ((custom_map_chain[j] == 5) || (custom_map_chain[j] == 15) || (custom_map_chain[j] == 0x2A)) {
						if (j > 0) {
							if (curr_map == (custom_map_chain[j - 1])) {
								good_map = 1;
							}
						}
					}
				}
				if (!good_map) {
					wipeParentSlot(i);
				}
			}
		}
	}
}

void pushToCustomChain(int map) {
	int pop = 0;
	for (int i = 0; i < CUSTOM_CHAIN_LENGTH; i++) {
		if (pop) {
			custom_map_chain[i] = 0;
		} else if (custom_map_chain[i] == map) {
			pop = 1;
			chain_index = i;
		}
	}
	chain_index += 1;
	if (chain_index < CUSTOM_CHAIN_LENGTH) {
		custom_map_chain[(int)chain_index] = map;
	} else {
		// Shift
		for (int i = 0; i < (CUSTOM_CHAIN_LENGTH - 1); i++) {
			custom_map_chain[i] = custom_map_chain[i + 1];
		}
		chain_index = CUSTOM_CHAIN_LENGTH - 1;
		custom_map_chain[(int)chain_index] = map;
	}
}

void callParentMapFilter(void) {
	if (ObjectModel2Timer == 2) {
		pushToCustomChain(CurrentMap);
		parentFilter();
	}
}