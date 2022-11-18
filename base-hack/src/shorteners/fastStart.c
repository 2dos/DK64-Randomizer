#include "../../include/common.h"

void applyFastStart(void) {
	if (Rando.fast_start_beginning) {
		if (MovesBase[0].simian_slam == 0) {
			for (int i = 0; i < 5; i++) {
				MovesBase[i].simian_slam = 1;
			}
		}
		for (int i = 0; i < 4; i++) {
			setLocationStatus(LOCATION_DIVE + i); // Training Barrels Complete
		}
		setPermFlag(FLAG_KEYIN_JAPES); // Japes Boulder
		setPermFlag(FLAG_ESCAPE); // Isles Escape CS
		setPermFlag(FLAG_TBARREL_SPAWNED); // Training Barrels Spawned
		setPermFlag(FLAG_ABILITY_SIMSLAM); // Cranky given SSlam
		setPermFlag(getKongFlag(Rando.starting_kong)); // Starting Kong Free
		if (Rando.camera_unlocked) {
			setFlagDuplicate(FLAG_ABILITY_SHOCKWAVE, 1, 0);
			setFlagDuplicate(FLAG_ABILITY_CAMERA, 1, 0);
		}
	}
}