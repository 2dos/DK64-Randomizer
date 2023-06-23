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
	} else if ((CurrentMap == MAP_HELM) && (checkFlag(FLAG_MODIFIER_HELMBOM, FLAGTYPE_PERMANENT))) {
		// Helm (Only if BoM is off)
		writeWTI(1);
	} else if ((CurrentMap == MAP_ISLES) || (CurrentMap == MAP_FAIRYISLAND) || (CurrentMap == MAP_KLUMSY) || (CurrentMap == MAP_ISLES_SNIDEROOM)) {
		// Isles, BFI, K. Lumsy, Snide Room
		writeWTI(1);
	} else if ((checkFlagDuplicate(FLAG_ESCAPE, FLAGTYPE_PERMANENT)) && ((CurrentMap == MAP_TRAININGGROUNDS) || (CurrentMap == MAP_TREEHOUSE))) {
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