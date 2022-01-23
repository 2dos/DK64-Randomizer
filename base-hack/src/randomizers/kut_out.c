#include "../../include/common.h"

#define KUT_OUT 0xC7

void write_kutoutorder(void) {
	if (ObjectModel2Timer < 5) {
		if (CurrentMap == KUT_OUT) {
			for (int i = 0; i < 5; i++) {
				KutOutKongArray[i] = Rando.kut_out_kong_order[i] % 5;
			}
		}
	}
}