#include "../../include/common.h"

void remove_blockers(void) {
	int bitfield_check = 1;
	if (ObjectModel2Timer < 5) {
		for (int i = 0; i < 8; i++) {
			if (Rando.remove_blockers & bitfield_check) {
				setPermFlag(FLAG_BLOCKER_JAPES + i);
			}
			bitfield_check <<= 1;
		}
	}
}