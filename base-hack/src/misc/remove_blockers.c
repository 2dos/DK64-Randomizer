#include "../../include/common.h"

void remove_blockers(void) {
	int bitfield_check = 1;
	if (ObjectModel2Timer < 5) {
		for (int i = 0; i < 8; i++) {
			if (Rando.remove_blockers & bitfield_check) {
				setPermFlag(461 + i);
			}
			bitfield_check <<= 1;
		}
	}
}