#include "../../include/common.h"

static const int krool_write_locations[] = {
	0x8002DBCE, // DK > Diddy
	0x8002E716, // Diddy > Lanky
	0x8002F04E, // Lanky > Tiny
	0x8002FAF2, // Tiny > Chunky
};

#define ISLES_OVERWORLD 0x22

void determine_krool_order(void) {
	int containing = 0;
	int destination = 0;
	int current_phase = 0;
	if (ObjectModel2Timer < 5) {
		if (CurrentMap >= 0xCB) {
			if (CurrentMap <= 0xCF) {
				current_phase = CurrentMap - 0xCB;
				if (Character != current_phase) {
					tagKong(current_phase + 2);
				}
				for (int i = 0; i < 4; i++) {
					containing = Rando.k_rool_order[i];
					destination = Rando.k_rool_order[i + 1];
					if ((containing > -1) && (destination > -1)) {
						*(short*)(*(int*)((int)&krool_write_locations[containing])) = 0xCB + destination;
					}
				}
			}
		}
	}
}

void disable_krool_health_refills(void) {
	if (ObjectModel2Timer < 5) {
		if (Rando.no_health_refill) {
			if (CurrentMap >= 0xCB) {
				if (CurrentMap <= 0xCF) {
					*(int*)(0x800289B0) = 0; // Between Phases
				}
			}
		}
	}
}