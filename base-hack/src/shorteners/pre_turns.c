#include "../../include/common.h"

void auto_turn_keys(void) {
	if (Rando.auto_keys) {
		for (int i = 0; i < 8; i++) {
			if (getItemCount_new(REQITEM_KEY, i, 0)) {
				setPermFlag(FLAG_KEYIN_KEY1 + i);
			}
		}
	}
}