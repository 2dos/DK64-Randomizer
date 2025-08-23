#include "../../include/common.h"

StartingItemsStruct starting_item_data = {
	.others = {
		.flag_moves = {
			.barrels = 1,
			.diving = 1,
			.oranges = 1,
			.vines = 1,
		}
	},
	.melons = 1,
	.slam = 1,
};

static const unsigned short fast_start_flags[] = {
	FLAG_TBARREL_DIVE,
	FLAG_TBARREL_ORANGE,
	FLAG_TBARREL_BARREL,
	FLAG_TBARREL_VINE,
	FLAG_ABILITY_SIMSLAM,
};

void unlockMoves(void) {
	CollectableBase.Oranges = 15;
	CollectableBase.Crystals = 1500;
	CollectableBase.StandardAmmo = 100;
	CollectableBase.Film = 5;
	if (Rando.quality_of_life.global_instrument) {
		CollectableBase.InstrumentEnergy = 12;
	} else {
		
	}
	CollectableBase.Melons = starting_item_data.melons;
	CollectableBase.Health = starting_item_data.melons << 2;
	for (int i = 0; i < 5; i++) {
		StartingItemsKongwiseStruct *kong = &starting_item_data.kongs[i];
		MovesBase[i].ammo_belt = starting_item_data.belt;
		MovesBase[i].instrument_bitfield = kong->instrument;
		MovesBase[i].simian_slam = starting_item_data.slam;
		MovesBase[i].special_moves = kong->special_moves;
		MovesBase[i].weapon_bitfield = kong->gun;
		MovesBase[i].instrument_energy = 12;
		if (Rando.fast_start_beginning) {
			setPermFlag(fast_start_flags[i]);
		}
	}
	*ItemInventory = starting_item_data.others;
	if (starting_item_data.climbing) {
		setPermFlag(FLAG_ABILITY_CLIMBING);
	}
	auto_turn_keys();
}