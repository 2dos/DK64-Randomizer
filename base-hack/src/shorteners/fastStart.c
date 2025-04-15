#include "../../include/common.h"

void applyFastStart(void) {
	if (Rando.fast_start_beginning) {
		setLocationStatus(LOCATION_FIRSTMOVE);
		for (int i = 0; i < 4; i++) {
			setLocationStatus(LOCATION_DIVE + i); // Training Barrels Complete
		}
		if (Rando.moves_pregiven.camera) {
			setFlagMove(FLAG_ABILITY_CAMERA);
		}
		if (Rando.moves_pregiven.shockwave) {
			setFlagMove(FLAG_ABILITY_SHOCKWAVE);
		}
	}
}