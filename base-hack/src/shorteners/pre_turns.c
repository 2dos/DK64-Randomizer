#include "../../include/common.h"

void pre_turn_keys(void) {
	if (Rando.keys_preturned) {
		for (int i = 0; i < 8; i++) {
			if (Rando.keys_preturned & (1 << i)) {
				giveItem(REQITEM_KEY, i, 0, (giveItemConfig){.display_item_text = 0, .apply_helm_hurry = 0});
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