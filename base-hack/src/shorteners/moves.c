#include "../../include/common.h"

int initFile_checkTraining(int type_check, int kong_check, int value_check) {
	for (int i = 0; i < 4; i++) {
		if (TrainingMoves_New[i].purchase_type == type_check) {
			if ((kong_check == -1) || (TrainingMoves_New[i].move_kong == kong_check)) {
				if (TrainingMoves_New[i].purchase_value == value_check) {
					return 1;
				}
			}
		}
	}
	return 0;
}

int initFile_hasGun(int kong) {
	int guns[] = {Rando.moves_pregiven.coconut, Rando.moves_pregiven.peanut, Rando.moves_pregiven.grape, Rando.moves_pregiven.feather, Rando.moves_pregiven.pineapple};
	return (guns[kong] != 0) || (initFile_checkTraining(PURCHASE_GUN, kong, 1));
}

int initFile_hasInstrument(int kong) {
	int instruments[] = {Rando.moves_pregiven.bongos, Rando.moves_pregiven.guitar, Rando.moves_pregiven.trombone, Rando.moves_pregiven.sax, Rando.moves_pregiven.triangle};
	return (instruments[kong] != 0) || (initFile_checkTraining(PURCHASE_INSTRUMENT, kong, 1));
}

int initFile_getBeltLevel(void) {
	int belts[] = {Rando.moves_pregiven.belt_upgrade_0, Rando.moves_pregiven.belt_upgrade_1};
	int belt_flags[] = {FLAG_ITEM_BELT_0, FLAG_ITEM_BELT_1};
	int belt_level = 0;
	for (int i = 0; i < 2; i++) {
		if (belts[i]) {
			belt_level += 1;
			setFlagDuplicate(FLAG_ITEM_BELT_0 + i, 1, 0);
		}
		if (initFile_checkTraining(PURCHASE_FLAG, -1, belt_flags[i])) {
			belt_level += 1;
		}
	}
	return belt_level;
}

int initFile_getInsUpgradeLevel(void) {
	int instrument_upgrades[] = {Rando.moves_pregiven.ins_upgrade_0, Rando.moves_pregiven.ins_upgrade_1, Rando.moves_pregiven.ins_upgrade_2};
	int ins_upg_flags[] = {FLAG_ITEM_INS_0, FLAG_ITEM_INS_1, FLAG_ITEM_INS_2};
	int instrument_upgrade_level = 0;
	for (int i = 0; i < 3; i++) {
		if (instrument_upgrades[i]) {
			instrument_upgrade_level += 1;
			setFlagDuplicate(FLAG_ITEM_INS_0 + i, 1, 0);
		}
		if (initFile_checkTraining(PURCHASE_FLAG, -1, ins_upg_flags[i])) {
			instrument_upgrade_level += 1;
		}
	}
	return instrument_upgrade_level;
}

#define DEFAULT_SLAM_LEVEL 1
int initFile_getSlamLevel(void) {
	int slams[] = {Rando.moves_pregiven.slam_upgrade_0, Rando.moves_pregiven.slam_upgrade_1, Rando.moves_pregiven.slam_upgrade_2};
	int slam_flags[] = {FLAG_ITEM_SLAM_0, FLAG_ITEM_SLAM_1};
	int slam_level = DEFAULT_SLAM_LEVEL;
	for (int i = DEFAULT_SLAM_LEVEL; i < 3; i++) {
		if (slams[i]) {
			slam_level += 1;
			setFlagDuplicate(FLAG_ITEM_SLAM_0 + i, 1, 0);
		}
		if (initFile_checkTraining(PURCHASE_FLAG, -1, slam_flags[i-DEFAULT_SLAM_LEVEL])) {
			slam_level += 1;
		}
	}
	return slam_level;
}

int initFile_getKongPotionBitfield(int kong) {
	int potions[5][3] = {
		{Rando.moves_pregiven.blast, Rando.moves_pregiven.strong_kong, Rando.moves_pregiven.grab},
		{Rando.moves_pregiven.charge, Rando.moves_pregiven.rocketbarrel, Rando.moves_pregiven.spring},
		{Rando.moves_pregiven.ostand, Rando.moves_pregiven.balloon, Rando.moves_pregiven.osprint},
		{Rando.moves_pregiven.mini, Rando.moves_pregiven.twirl, Rando.moves_pregiven.monkeyport},
		{Rando.moves_pregiven.hunky, Rando.moves_pregiven.punch, Rando.moves_pregiven.gone},
	};
	int bitfield = 0;
	for (int i = 0; i < 3; i++) {
		if (potions[kong][i]) {
			bitfield |= (1 << i);
		}
		if (initFile_checkTraining(PURCHASE_MOVES, kong, i+1)) {
			bitfield |= (1 << i);
		}
	}
	return bitfield;
}

void unlockMoves(void) {
	// Evaluate progressives
	int has_instrument = 0;
	for (int i = 0; i < 5; i++) {
		if (initFile_hasInstrument(i)) {
			has_instrument = 1;
		}
	}
	CollectableBase.Oranges = 15;
	CollectableBase.Crystals = 1500;
	int slam_level = initFile_getSlamLevel();
	int belt_level = initFile_getBeltLevel();
	int base_gun_bitfield = 0;
	int base_ins_bitfield = ((1 << initFile_getInsUpgradeLevel()) - 1) << 1;
	if ((Rando.moves_pregiven.homing) || (initFile_checkTraining(PURCHASE_GUN, -1, 2))) {
		base_gun_bitfield |= 2;
	}
	if ((Rando.moves_pregiven.sniper) || (initFile_checkTraining(PURCHASE_GUN, -1, 3))) {
		base_gun_bitfield |= 4;
	}
	for (int i = 0; i < 5; i++) {
		int has_kong_instrument = initFile_hasInstrument(i);
		int has_kong_gun = initFile_hasGun(i);
		MovesBase[i].special_moves = initFile_getKongPotionBitfield(i);
		MovesBase[i].simian_slam = slam_level;
		MovesBase[i].weapon_bitfield = base_gun_bitfield | (has_kong_gun != 0);
		MovesBase[i].ammo_belt = belt_level;
		MovesBase[i].instrument_bitfield = base_ins_bitfield | (has_kong_instrument != 0);
		if (has_kong_instrument) {
			MovesBase[i].instrument_energy = 12;
			has_instrument = 1;
		}
		if (has_kong_gun) {
			CollectableBase.StandardAmmo = 100;
		}
	}
	if (initFile_getInsUpgradeLevel() >= 2) {
		CollectableBase.Melons = 3;
		CollectableBase.Health = 12;
	} else {
		if (has_instrument) {
			CollectableBase.Melons = 2;
			CollectableBase.Health = 8;
		}
	}
	if (Rando.fast_start_beginning) {
		for (int i = 0; i < 4; i++) {
			setLocationStatus(LOCATION_DIVE + i);
		}
	}
	if ((Rando.moves_pregiven.camera) || (initFile_checkTraining(PURCHASE_FLAG, -1, FLAG_ABILITY_CAMERA) || (initFile_checkTraining(PURCHASE_FLAG, -1, -2)))) {
		setFlagDuplicate(FLAG_ABILITY_CAMERA, 1, 0);
		CollectableBase.Film = 5;
	}
	if ((Rando.moves_pregiven.shockwave) || (initFile_checkTraining(PURCHASE_FLAG, -1, FLAG_ABILITY_SHOCKWAVE) || (initFile_checkTraining(PURCHASE_FLAG, -1, -2)))) {
		setFlagDuplicate(FLAG_ABILITY_SHOCKWAVE, 1, 0);
	}
}