#include "../../include/common.h"

void unlockKongs(void) {
	if (Rando.unlock_kongs) {
		setPermFlag(0x181);
		for (int i = 0; i < 4; i++) {
			setPermFlag(KongFlagArray[i]);
		}
	}
}