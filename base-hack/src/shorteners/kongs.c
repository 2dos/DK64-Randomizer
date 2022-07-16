#include "../../include/common.h"

void unlockKongs(void) {
	if (Rando.unlock_kongs) {
		for (int i = 0; i < 5; i++) {
			if (Rando.unlock_kongs & (1 << i)) {
				if (i == 0) {
					setPermFlag(FLAG_KONG_DK);
				} else {
					setPermFlag(KongFlagArray[i - 1]);
				}
			}
		}
	}
}