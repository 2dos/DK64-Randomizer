#include "../../include/common.h"

static const short normal_key_flags[] = {0x1A,0x4A,0x8A,0xA8,0xEC,0x124,0x13D};
static const short tnsportal_flags[] = {46,108,152,203,258,302,352};

void apply_key(int index, int remove_troff, int set_key) {
	setPermFlag(444 + index);
	if (index < 7) {
		if (Rando.level_order_rando_on) {
			if (set_key) {
				setPermFlag(Rando.key_flags[index]);
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
				setPermFlag(normal_key_flags[index]);
			}
			if (remove_troff) {
				setPermFlag(tnsportal_flags[index]);
			}
		}
	} else {
		if (set_key) {
			setPermFlag(normal_key_flags[7]); // Set Key 8
		}
	}
}

void pre_turn_keys(void) {
	int check = 1;
	if (ObjectModel2Timer < 5) {
		if (Rando.keys_preturned) {
			for (int i = 0; i < 8; i++) {
				if (Rando.keys_preturned & check) {
					apply_key(i,1,1);
				}
				check <<= 1;
			}
		}
	}
}

void auto_turn_keys(void) {
	if (ObjectModel2Timer < 5) {
		for (int i = 0; i < 8; i++) {
			if (checkFlag(normal_key_flags[i],0)) {
				apply_key(i,0,0);
			}
		}
	}
}