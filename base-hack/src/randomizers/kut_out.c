#include "../../include/common.h"

void write_kutoutorder(void) {
	if (ObjectModel2Timer < 5) {
		if (CurrentMap == MAP_CASTLEKUTOUT) {
			for (int i = 0; i < 5; i++) {
				KutOutKongArray[i] = Rando.kut_out_kong_order[i] % 5;
			}
		}
	}
}