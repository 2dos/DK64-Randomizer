#include "../../include/common.h"

void apply_key(int index, int remove_troff) {
	setPermFlag(FLAG_KEYIN_KEY1 + index);
	if (index < 7) {
		if (Rando.level_order_rando_on) {
			giveItem(REQITEM_KEY, index, 0);
			if (remove_troff) {
				for (int j = 0; j < 7; j++) {
					if (normal_key_flags[j] == normal_key_flags[index]) {
						setPermFlag(tnsportal_flags[j]);
					}
				}
			}
		} else {
			giveItem(REQITEM_KEY, index, 0);
			if (remove_troff) {
				setPermFlag(tnsportal_flags[index]);
			}
		}
	} else {
		giveItem(REQITEM_KEY, 7, 0);
	}
}

void pre_turn_keys(void) {
	if (Rando.keys_preturned) {
		for (int i = 0; i < 8; i++) {
			if (Rando.keys_preturned & (1 << i)) {
				apply_key(i,1);
			}
		}
	}
}

void auto_turn_keys(void) {
	if (Rando.auto_keys) {
		for (int i = 0; i < 8; i++) {
			if (getItemCount_new(REQITEM_KEY, i, 0)) {
				setPermFlag(FLAG_KEYIN_KEY1 + i);
			}
		}
	}
}