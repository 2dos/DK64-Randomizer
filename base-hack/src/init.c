#include "../include/common.h"

void initHack(void) {
	if ((LoadedHooks == 0) && (CurrentMap == 0x28)) {
		DebugInfoOn = 1;
		*(int*)(0x80731F78) = 0; // Debug 1 Column
		*(int*)(0x8060E04C) = 0; // Prevent moves overwrite
		*(short*)(0x8060DDAA) = 0; // Writes readfile data to moves
		loadExtraHooks();
		LoadedHooks = 1;
	}
}