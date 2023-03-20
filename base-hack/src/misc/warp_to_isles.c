#include "../../include/common.h"

void writeWTI(int index) {
	ExpandPauseMenu = index;
	InitialPauseHeight = 0x198 - (0x28 * index);
}

void handle_WTI(void) {
	if (isLobby(CurrentMap)) {
		// Lobbies
		writeWTI(1);
	} else if (levelIndexMapping[CurrentMap] < 7) {
		// Any Map explicitly in first 7 worlds
		writeWTI(1);
	} else if ((CurrentMap == 0x11) && (checkFlag(FLAG_MODIFIER_HELMBOM,0))) {
		// Helm (Only if BoM is off)
		writeWTI(1);
	} else if ((CurrentMap == 0x22) || (CurrentMap == 0xBD) || (CurrentMap == 0x61) || (CurrentMap == 0xC3)) {
		// Isles, BFI, K. Lumsy, Snide Room
		writeWTI(1);
	} else if ((checkFlagDuplicate(FLAG_ESCAPE, 0)) && ((CurrentMap == 0xB0) || (CurrentMap == 0xAB))) {
		// TGrounds & Treehouse (Only if escaped from Isles)
		writeWTI(1);
	} else {
		writeWTI(0);
	}
}

void warpToIsles(void) {
	initiateTransition(Rando.starting_map, Rando.starting_exit);
	fixHelmTimerCorrection();
}