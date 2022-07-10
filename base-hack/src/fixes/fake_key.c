#include "../../include/common.h"

void fixkey8(void) {
	if (CurrentMap == 0x11) { // Hideout Helm
		if (checkFlag(380,0) == 0) { // Doesn't have Key 8
			if (touchingModel2Object(0x5A)) {
				setPermFlag(380); // Give Key 8
			}
		}
	}
}