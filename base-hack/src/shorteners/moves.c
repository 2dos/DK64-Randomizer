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
			setPermFlag(i  + 0x182);
		}
	}
	if (Rando.camera_unlocked) {
		setPermFlag(0x179);
	}
}