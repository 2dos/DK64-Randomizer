#include "../../include/common.h"

void writeWTI(int index) {
	ExpandPauseMenu = index;
	InitialPauseHeight = 0x198 - (0x28 * index);
}

void handle_WTI(void) {
	if (isLobby(CurrentMap)) {
		writeWTI(0);
	} else if (levelIndexMapping[CurrentMap] < 7) {
		writeWTI(1);
	} else if ((CurrentMap == 0x11) && (checkFlag(FLAG_MODIFIER_HELMBOM,0))) {
		writeWTI(1);
	} else {
		writeWTI(0);
	}
}