#include "../../include/common.h"

static const short normal_key_flags[] = {0x1A,0x4A,0x8A,0xA8,0xEC,0x124,0x13D};
static const short tnsportal_flags[] = {46,108,152,203,258,302,352};

void pre_turn_keys(void) {
	int check = 1;
	if (ObjectModel2Timer < 5) {
		if (Rando.keys_preturned) {
			for (int i = 0; i < 8; i++) {
				if (Rando.keys_preturned & check) {
					setPermFlag(444 + i);
					if (i < 7) {
						if (Rando.level_order_rando_on) {
							setPermFlag(Rando.key_flags[i]);
							for (int j = 0; j < 7; j++) {
								if (normal_key_flags[j] == Rando.key_flags[i]) {
									setPermFlag(tnsportal_flags[j]);
								}
							}
						} else {
							setPermFlag(normal_key_flags[i]);
							setPermFlag(tnsportal_flags[i]);
						}
					} else {
						setPermFlag(normal_key_flags[7]); // Set Key 8
					}
				}
				check <<= 1;
			}
		}
	}
}