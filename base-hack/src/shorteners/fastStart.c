#include "../../include/common.h"

void islesSpawn(void) {
	if (Rando.fast_start_beginning) {
		*(int*)(0x80714540) = 0;
	}
}

static const short kong_flags[] = {385,6,70,66,117};

void applyFastStart(void) {
	if (Rando.fast_start_beginning) {
		for (int i = 0; i < 4; i++) {
			setPermFlag(386 + i); // Training Barrels Complete
		}
		setPermFlag(0x1BB); // Japes Boulder
		setPermFlag(0x186); // Isles Escape CS
		setPermFlag(0x17F); // Training Barrels Spawned
		setPermFlag(0x180); // Cranky given SSlam
		setPermFlag(kong_flags[(int)Rando.starting_kong]); // Starting Kong Free
		if (Rando.camera_unlocked) {
			setPermFlag(0x179);
		}
		if (MovesBase[0].simian_slam == 0) {
			for (int i = 0; i < 5; i++) {
				MovesBase[i].simian_slam = 1;
			}
		}
	}
}