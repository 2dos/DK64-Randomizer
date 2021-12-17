#include "../include/common.h"

void initHack(void) {
	if ((LoadedHooks == 0) && (CurrentMap == 0x28)) {
		DebugInfoOn = 1;
		*(int*)(0x80731F78) = 0; // Debug 1 Column
		loadExtraHooks();
		LoadedHooks = 1;
	}
}