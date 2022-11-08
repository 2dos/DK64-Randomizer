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
					if ((containing > -1) && (destination > -1) && (containing < 4)) {
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

void initKRool(int phase) {
	int is_last = 0;
	int next_phase = -1;
	int found_phase = 0;
	int found_next = 0;
	int microbuffer_cutscenes[] = {4,3,5,3,4};
	for (int i = 0; i < 5; i++) {
		if (Rando.k_rool_order[i] == phase) {
			found_phase = 1;
		} else {
			if ((found_phase) && (!found_next)) {
				if (Rando.k_rool_order[i] == -1) {
					is_last = 1;
				} else {
					next_phase = Rando.k_rool_order[i];
				}
				found_next = 1;
			}
		}
	}
	if ((found_phase) && (!found_next)) {
		// If phase length is 5 phases
		is_last = 1;
	}
	if (phase == 4) {
		if (!is_last) {
			modifyCutsceneItem(0, 7, 8, 12, 0); // Set to Kremlings Running Out Cutscene
			modifyCutsceneItem(0, 8, 0x29, 0xCB + next_phase, microbuffer_cutscenes[next_phase]); // Set to Kremlings Running Out Cutscene
			modifyCutscenePoint(0, 22, 40, 7); // Overwrite playsong call with change of cutscene
			modifyCutscenePoint(0, 12, 22, 8); // End of cutscene 12 should bring you to next phase
		}
	} else {
		if (is_last) {
			int phase_items[] = {134,102,111,174};
			modifyCutsceneItem(0, phase_items[phase], 0x29, 0x22, 29);
		}
	}
}