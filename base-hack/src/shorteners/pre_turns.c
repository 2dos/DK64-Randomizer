#include "../../include/common.h"

void pre_turn_keys(void) {
	int check = 1;
	if (ObjectModel2Timer < 5) {
		if (Rando.keys_preturned) {
			for (int i = 0; i < 8; i++) {
				if (Rando.keys_preturned & check) {
					setPermFlag(444 + i);
				}
				check <<= 1;
			}
		}
	}
}