#include "../../include/common.h"

void writeWTI(int index) {
	ExpandPauseMenu = index;
	int init_y = 0x198;
	InitialPauseHeight = init_y - (0x28 * index);
}

static unsigned char isles_maps[] = {
	MAP_ISLES,
	MAP_FAIRYISLAND,
	MAP_KLUMSY,
	MAP_ISLES_SNIDEROOM,
	MAP_TRAININGGROUNDS,
	MAP_TREEHOUSE,
};

void handle_WTI(void) {
	if (!checkFlagDuplicate(FLAG_ESCAPE, FLAGTYPE_PERMANENT)) {
		writeWTI(0);
		return;
	}
	if (isLobby(CurrentMap)) {
		// Lobbies
		writeWTI(1);
	} else if (levelIndexMapping[CurrentMap] < LEVEL_ISLES) {
		// Any Map explicitly in first 7 worlds
		writeWTI(1);
	} else if ((CurrentMap == MAP_HELM) && (checkFlag(FLAG_MODIFIER_HELMBOM, FLAGTYPE_PERMANENT))) {
		// Helm (Only if BoM is off)
		writeWTI(1);
	} else if (inU8List(CurrentMap, &isles_maps, sizeof(isles_maps))) {
		// Isles, BFI, K. Lumsy, Snide Room
		writeWTI(1);
	} else {
		writeWTI(0);
	}
}

void warpToIsles(void) {
	int exit = Rando.starting_exit;
	if (Rando.starting_map == MAP_HELM) {
		exit = getHelmExit();
	}
	initiateTransition(Rando.starting_map, exit);
	fixHelmTimerCorrection();
}