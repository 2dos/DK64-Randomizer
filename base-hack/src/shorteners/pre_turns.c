#include "../../include/common.h"

void apply_key(int index, int remove_troff) {
	setPermFlag(FLAG_KEYIN_KEY1 + index);
	if (index < 7) {
		if (Rando.level_order_rando_on) {
			setFlagDuplicate(normal_key_flags[index],1,FLAGTYPE_PERMANENT);
			if (remove_troff) {
				for (int j = 0; j < 7; j++) {
					if (normal_key_flags[j] == normal_key_flags[index]) {
						setPermFlag(tnsportal_flags[j]);
					}
				}
			}
		} else {
			setFlagDuplicate(normal_key_flags[index],1,FLAGTYPE_PERMANENT);
			if (remove_troff) {
				setPermFlag(tnsportal_flags[index]);
			}
		}
	} else {
		setFlagDuplicate(normal_key_flags[7],1,FLAGTYPE_PERMANENT); // Set Key 8
	}
}

void pre_turn_keys(void) {
	int keys_in_item_pool = 0;
	if (Rando.item_rando) {
		for (int i = 0; i < 7; i++) {
			int j = 0;
			while (j < flut_size) {
				int vanilla_flag = ItemRando_FLUT[2 * j];
				if (normal_key_flags[i] == vanilla_flag) {
					keys_in_item_pool = 1;
					int new_flag = ItemRando_FLUT[(2 * j) + 1];
					if (checkFlagDuplicate(new_flag, FLAGTYPE_PERMANENT)) {
						setPermFlag(tnsportal_flags[i]);
					}
				} else if (vanilla_flag == -1) {
					break;
				}
				j++;
			}
		}
	}
	int check = 1;
	if (Rando.keys_preturned) {
		for (int i = 0; i < 8; i++) {
			if (Rando.keys_preturned & check) {
				apply_key(i,!keys_in_item_pool);
			}
			check <<= 1;
		}
	}
	if ((Rando.item_rando) && (keys_in_item_pool)) {
		for (int i = 0; i < 7; i++) {
			int j = 0;
			while (j < 400) {
				int vanilla_flag = ItemRando_FLUT[2 * j];
				if (normal_key_flags[i] == vanilla_flag) {
					int new_flag = ItemRando_FLUT[(2 * j) + 1];
					if (checkFlagDuplicate(new_flag, FLAGTYPE_PERMANENT)) {
						setPermFlag(tnsportal_flags[i]);
					}
				} else if (vanilla_flag == -1) {
					break;
				}
				j++;
			}
		}
	}
}

void writeKeyFlags(int index) {
	setPermFlag(FLAG_KEYIN_KEY1 + index);
}

void auto_turn_keys(void) {
	if (Rando.auto_keys) {
		for (int i = 0; i < 8; i++) {
			if (checkFlagDuplicate(normal_key_flags[i], FLAGTYPE_PERMANENT)) {
				writeKeyFlags(i);
			}
		}
	}
}