#include "../../include/common.h"

void unlockMoves(void) {
	if (Rando.unlock_moves) {
		CollectableBase.Melons = 3;
		CollectableBase.Health = 12;
		CollectableBase.StandardAmmo = 100;
		CollectableBase.Oranges = 15;
		CollectableBase.Crystals = 1500;
		CollectableBase.Film = 5;
		
		for (int i = 0; i < 5; i++) {
			MovesBase[i].special_moves = 7;
			MovesBase[i].simian_slam = 3;
			MovesBase[i].weapon_bitfield = 7;
			MovesBase[i].ammo_belt = 2;
			MovesBase[i].instrument_bitfield = 15;
			MovesBase[i].instrument_energy = 12;
		}
		
	}
	if (Rando.fast_start_beginning) {
		for (int i = 0; i < 4; i++) {
			setLocationStatus(LOCATION_DIVE + i);
		}
	}
	if (Rando.camera_unlocked) {
		setFlagDuplicate(FLAG_ABILITY_SHOCKWAVE, 1, 0);
		setFlagDuplicate(FLAG_ABILITY_CAMERA, 1, 0);
	}
}