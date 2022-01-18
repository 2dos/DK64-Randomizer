#include "../../include/common.h"

static const short* krool_write_locations[] = {
	(short*)0x8002DBCE, // DK > Diddy
	(short*)0x8002E71A, // Diddy > Lanky
	(short*)0x8002F04E, // Lanky > Tiny
	(short*)0x8002FAF2, // Tiny > Chunky
};

void determine_krool_order(void) {
	int containing = 0;
	int destination = 0;
	int current_phase = 0;
	if (TransitionSpeed < 0) {
		if (CurrentMap >= 0xCB) {
			if (CurrentMap <= 0xCF) {
				current_phase = CurrentMap - 0xCB;
				if (Character != current_phase) {
					tagKong(current_phase + 2);
				}
				for (int i = 0; i < 4; i++) {
					containing = Rando.k_rool_order[i];
					destination = Rando.k_rool_order[i + 1];
					if (containing > -1) {
						*(short*)(krool_write_locations[containing]) = 0xCB + destination;
					}
				}
			}
		}
	}
}