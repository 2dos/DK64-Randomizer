#include "../../include/common.h"

void fixkey8(void) {
	if (CurrentMap == 0x11) { // Hideout Helm
		if (checkFlag(FLAG_KEYHAVE_KEY8,0) == 0) { // Doesn't have Key 8
			if (touchingModel2Object(0x5A)) {
				setPermFlag(FLAG_KEYHAVE_KEY8); // Give Key 8
			}
		}
	}
}