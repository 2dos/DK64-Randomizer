#include "../../include/common.h"

#define CASTLE_MAIN 0x57

void fixCastleAutowalk(void) {
	if (CurrentMap == CASTLE_MAIN) {
		if (CutsceneActive) {
			if (CutsceneIndex == 29) {
				if (IsAutowalking) {
					IsAutowalking = 0;
				}
			}
		}
	}
}