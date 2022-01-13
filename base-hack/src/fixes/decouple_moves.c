#include "../../include/common.h"

#define CRANKY 5
#define MAIN_MENU 0x50

static const char moves_values[] = {1,1,3,1,7,1,1,7};

void decouple_moves_fixes(void) {
	if (TransitionSpeed < 0) {
		if (CurrentMap == CRANKY) {
			PatchCrankyCode();
			*(int*)(0x80025E9C) = 0x0C009751; // Change writing of move to "write bitfield move" function call
		} else if (CurrentMap == MAIN_MENU) {
			*(short*)(0x8002E266) = 7; // Enguarde Arena Movement Write
			*(short*)(0x8002F01E) = 7; // Rambi Arena Movement Write
			for (int i = 0; i < 8; i++) {
				MainMenuMoves[i].moves = moves_values[i];
			}
		}
	}
}