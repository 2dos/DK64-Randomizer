#include "../../include/common.h"

static const short normal_key_flags[] = {
	FLAG_KEYHAVE_KEY1,
	FLAG_KEYHAVE_KEY2,
	FLAG_KEYHAVE_KEY3,
	FLAG_KEYHAVE_KEY4,
	FLAG_KEYHAVE_KEY5,
	FLAG_KEYHAVE_KEY6,
	FLAG_KEYHAVE_KEY7,
	FLAG_KEYHAVE_KEY8
};
static const short tnsportal_flags[] = {
	FLAG_PORTAL_JAPES,
	FLAG_PORTAL_AZTEC,
	FLAG_PORTAL_FACTORY,
	FLAG_PORTAL_GALLEON,
	FLAG_PORTAL_FUNGI,
	FLAG_PORTAL_CAVES,
	FLAG_PORTAL_CASTLE,
};

void apply_key(int index, int remove_troff, int set_key) {
	if (set_key) {
		setPermFlag(FLAG_KEYIN_KEY1 + index);
	}
	if (index < 7) {
		if (Rando.level_order_rando_on) {
			if (set_key) {
				setFlagDuplicate(Rando.key_flags[index],1,0);
			}
			if (remove_troff) {
				for (int j = 0; j < 7; j++) {
					if (normal_key_flags[j] == Rando.key_flags[index]) {
						setPermFlag(tnsportal_flags[j]);
					}
				}
			}
		} else {
			if (set_key) {
				setFlagDuplicate(normal_key_flags[index],1,0);
			}
			if (remove_troff) {
				setPermFlag(tnsportal_flags[index]);
			}
		}
	} else {
		if (set_key) {
			setFlagDuplicate(normal_key_flags[7],1,0); // Set Key 8
		}
	}
}

void pre_turn_keys(void) {
	int check = 1;
	if (Rando.keys_preturned) {
		for (int i = 0; i < 8; i++) {
			if (Rando.keys_preturned & check) {
				apply_key(i,!Rando.item_rando,1);
			}
			check <<= 1;
		}
	}
	if (Rando.item_rando) {
		for (int i = 0; i < 7; i++) {
			if (checkFlag(getKeyFlag(i), 0)) {
				setFlagDuplicate(tnsportal_flags[i], 1, 0);
			}
		}
	}
}

void writeKeyFlags(int index) {
	setPermFlag(FLAG_KEYIN_KEY1 + index);
}

void auto_turn_keys(void) {
	if (ObjectModel2Timer < 5) {
		for (int i = 0; i < 8; i++) {
			if (Rando.level_order_rando_on) {
				if (i < 7) {
					if (checkFlagDuplicate(Rando.key_flags[i],0)) {
						writeKeyFlags(i);
					}
				}
				if (checkFlagDuplicate(normal_key_flags[7],0)) {
					writeKeyFlags(7);
				}
			} else {
				if (checkFlagDuplicate(normal_key_flags[i],0)) {
					writeKeyFlags(i);
				}
			}
		}
	}
}