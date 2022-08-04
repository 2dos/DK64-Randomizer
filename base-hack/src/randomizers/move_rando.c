#include "../../include/common.h"

#define FUNKY 1
#define CRANKY 5
#define CANDY 0x19

#define PURCHASE_MOVES 0
#define PURCHASE_SLAM 1
#define PURCHASE_GUN 2
#define PURCHASE_AMMOBELT 3
#define PURCHASE_INSTRUMENT 4
#define PURCHASE_FLAG 5
#define PURCHASE_GB 6
#define PURCHASE_NOTHING -1

int getMoveType(int value) {
	int ret = (value >> 5) & 7;
	if (ret == 7) {
		return -1;
	} else {
		return ret;
	}
}

int getMoveIndex(int value) {
	return ((value >> 3) & 3) + 1;
}

int getMoveKong(int value) {
	return value & 7; 
}

static char stored_slam_level = 0;
static char stored_belt_level = 0;
static char stored_instrument_level = 0;
static char stored_melons = 0;

void checkProgressive(
		char* previous_storage,
		char* current_storage,
		unsigned char* eep_storage,
		int lower_threshold,
		int upper_threshold,
		int level,
		int purchase_type,
		int purchase_level,
		int is_bitfield,
		int progressive_floor) {
	int pass = 0;
	if (is_bitfield) {
		if ((!(*previous_storage & (1 << lower_threshold))) && (*current_storage & (1 << lower_threshold))) {
			pass = 1;
		}
	} else {
		if ((*previous_storage <= lower_threshold) && (*current_storage >= upper_threshold)) {
			pass = 1;
		}
	}
	if (pass) {
		// Just purchased Move
		int purchased = 0;
		if (level >= 0 && level < LEVEL_COUNT) {
			purchased = 1;
		}
		int shop = 0;
		if (CurrentMap == FUNKY) {
			shop = 1;
		} else if (CurrentMap == CANDY) {
			shop = 2;
		}
		*eep_storage = (level << 4) | (purchased << 2) | shop;
		SaveToGlobal();
	}
	pass = 0;
	if (is_bitfield) {
		if (*current_storage & (1 << lower_threshold)) {
			pass = 1;
		}
	} else {
		if (*current_storage > lower_threshold) {
			pass = 1;
		}
	}
	if (pass) {
		int encoded_sss_location = *eep_storage;
		int shop = encoded_sss_location & 3;
		int purchased = (encoded_sss_location >> 2) & 1;
		int level = (encoded_sss_location >> 4) & 7;
		for (int i = 0; i < LEVEL_COUNT; i++) {
			for (int j = 0; j < 5; j++) {
				if (CrankyMoves_New[j][i].purchase_type == purchase_type) {
					if ((purchased) && (shop == 0) && (level == i)) {
						CrankyMoves_New[j][i].purchase_type = PURCHASE_NOTHING;
					} else {
						if (CrankyMoves_New[j][i].purchase_value > progressive_floor) {
							CrankyMoves_New[j][i].purchase_value = purchase_level;
						}
					}
				}
				if (CandyMoves_New[j][i].purchase_type == purchase_type) {
					if ((purchased) && (shop == 2) && (level == i)) {
						CandyMoves_New[j][i].purchase_type = PURCHASE_NOTHING;
					} else {
						if (CandyMoves_New[j][i].purchase_value > progressive_floor) {
							CandyMoves_New[j][i].purchase_value = purchase_level;
						}
					}
				}
				if (FunkyMoves_New[j][i].purchase_type == purchase_type) {
					if ((purchased) && (shop == 1) && (level == i)) {
						FunkyMoves_New[j][i].purchase_type = PURCHASE_NOTHING;
					} else {
						if (FunkyMoves_New[j][i].purchase_value > progressive_floor) {
							FunkyMoves_New[j][i].purchase_value = purchase_level;
						}
					}
				}
			}
		}
	}
	*previous_storage = *current_storage;
}

void updateProgressive(void) {
	if (Rando.move_rando_on) {
		int level = getWorld(CurrentMap,0);
		checkProgressive(
			&stored_slam_level,
			&MovesBase[0].simian_slam,
			&StoredSettings.file_extra[(int)FileIndex].location_sss_purchased,
			1,
			2,
			level,
			PURCHASE_SLAM,
			3,
			0,
			0
		);
		checkProgressive(
			&stored_belt_level,
			&MovesBase[0].ammo_belt,
			&StoredSettings.file_extra[(int)FileIndex].location_ab1_purchased,
			0,
			1,
			level,
			PURCHASE_AMMOBELT,
			2,
			0,
			0
		);
		checkProgressive(
			&stored_instrument_level,
			&MovesBase[0].instrument_bitfield,
			&StoredSettings.file_extra[(int)FileIndex].location_ug1_purchased,
			1,
			1,
			level,
			PURCHASE_INSTRUMENT,
			3,
			1,
			1
		);
		checkProgressive(
			&stored_melons,
			&CollectableBase.Melons,
			&StoredSettings.file_extra[(int)FileIndex].location_mln_purchased,
			2,
			3,
			level,
			PURCHASE_INSTRUMENT,
			4,
			0,
			1
		);
	}
}

move_block* getMoveBlock(void) {
	int size = 0x200;
	move_block* write_space = dk_malloc(size);
	int* file_size;
	*(int*)(&file_size) = size;
	copyFromROM(0x1FEF000,write_space,&file_size,0,0,0,0);
	return write_space;
}

void moveTransplant(void) {
	move_block* move_data = getMoveBlock();
	if (move_data) {
		for (int i = 0; i < LEVEL_COUNT; i++) {
			for (int j = 0; j < 5; j++) {
				CrankyMoves_New[j][i].purchase_type = getMoveType(move_data->cranky_moves[j][i].move_master_data);
				CrankyMoves_New[j][i].move_kong = getMoveKong(move_data->cranky_moves[j][i].move_master_data);
				CrankyMoves_New[j][i].purchase_value = getMoveIndex(move_data->cranky_moves[j][i].move_master_data);

				CandyMoves_New[j][i].purchase_type = getMoveType(move_data->candy_moves[j][i].move_master_data);
				CandyMoves_New[j][i].move_kong = getMoveKong(move_data->candy_moves[j][i].move_master_data);
				CandyMoves_New[j][i].purchase_value = getMoveIndex(move_data->candy_moves[j][i].move_master_data);

				FunkyMoves_New[j][i].purchase_type = getMoveType(move_data->funky_moves[j][i].move_master_data);
				FunkyMoves_New[j][i].move_kong = getMoveKong(move_data->funky_moves[j][i].move_master_data);
				FunkyMoves_New[j][i].purchase_value = getMoveIndex(move_data->funky_moves[j][i].move_master_data);
			}
		}
		for (int i = 0; i < 4; i++) {
			TrainingMoves_New[i].purchase_type = getMoveType(move_data->training_moves[i].move_master_data);
			TrainingMoves_New[i].move_kong = getMoveKong(move_data->training_moves[i].move_master_data);
			TrainingMoves_New[i].purchase_value = getMoveIndex(move_data->training_moves[i].move_master_data);
		}
		BFIMove_New.purchase_type = getMoveType(move_data->bfi_move.move_master_data);
		BFIMove_New.move_kong = getMoveKong(move_data->bfi_move.move_master_data);
		BFIMove_New.purchase_value = getMoveIndex(move_data->bfi_move.move_master_data);
	}
	complex_free(move_data);
}

void replace_moves(void) {
	if (Rando.move_rando_on) {
		moveTransplant();
		updateProgressive();
	}
}

void cancelMoveSoftlock(void) {
	if (Rando.move_rando_on) {
		if (CurrentMap == CRANKY) {
			if ((TBVoidByte & 0x30) != 0) {
				if ((CutsceneActive) && (CutsceneIndex == 2) && (CutsceneTimer == 80)) {
					//cancelPausedCutscene();
				}
			}
		} else if ((CurrentMap == FUNKY) || (CurrentMap == CANDY)) {
			// int* potion = findActorWithType(320);
			// if (potion) {
			// 	if ((TBVoidByte & 0x30) == 0) {
			// 		if ((CutsceneActive) && (CutsceneIndex == 2) && (CutsceneTimer == 80)) {
			// 			pauseCutscene();
			// 		}
			// 	} else {
			// 		cancelPausedCutscene();
			// 		TBVoidByte |= 0x30;
			// 	}
			// }
		}
	}
}

void getNextMovePurchase(shop_paad* paad, KongBase* movedata) {
	int has_purchase = 0;
	int latest_level_entered = 0;
	int has_entered_level = 1; // Set to 0 forcing level entry requirement
	for (int i = 0; i < 7; i++) {
		if (checkFlag((FLAG_STORY_JAPES + i),0)) {
			latest_level_entered = i;
			has_entered_level = 1;
		}
	}
	latest_level_entered += has_entered_level;
	int world = getWorld(CurrentMap,0);
	paad->level = world;
	int shop_owner = CurrentActorPointer_0->actorType;
	if (has_entered_level) {
		purchase_struct* selected = 0;
		if (shop_owner == 0xBD) { // Cranky
			selected = &CrankyMoves_New[(int)Character][world];
		} else if (shop_owner == 0xBE) { // Funky
			selected = &FunkyMoves_New[(int)Character][world];
		} else if (shop_owner == 0xBF) { // Candy
			selected = &CandyMoves_New[(int)Character][world];
		}
		if (selected) {
			int p_type = selected->purchase_type;
			int p_kong = selected->move_kong;
			int p_value = selected->purchase_value;
			if (p_type > PURCHASE_NOTHING) {
				switch (p_type) {
					case PURCHASE_MOVES:
						if ((MovesBase[p_kong].special_moves & (1 << (p_value - 1))) == 0) {
							has_purchase = 1;
						}
						break;
					case PURCHASE_GUN:
						if ((MovesBase[p_kong].weapon_bitfield & (1 << (p_value - 1))) == 0) {
							has_purchase = 1;
						}
						break;
					case PURCHASE_INSTRUMENT:
						if ((MovesBase[p_kong].instrument_bitfield & (1 << (p_value - 1))) == 0) {
							has_purchase = 1;
						}
						break;
					case PURCHASE_SLAM:
						if (MovesBase[p_kong].simian_slam < p_value) {
							has_purchase = 1;
						}
						break;
					case PURCHASE_AMMOBELT:
						if (MovesBase[p_kong].ammo_belt < p_value) {
							has_purchase = 1;
						}
					case PURCHASE_GB:
					case PURCHASE_FLAG:
						if (p_value == -2) {
							has_purchase = checkFlag(FLAG_ABILITY_CAMERA,0) & checkFlag(FLAG_ABILITY_SHOCKWAVE,0);
						} else {
							has_purchase = checkFlag(p_value,0);
						}
					break;
				}
				if (has_purchase) {
					paad->purchase_type = p_type;
					int p_price = selected->price;
					textParameter = p_price;
					paad->price = p_price;
					paad->purchase_value = p_value;
					paad->kong = p_kong;
				}
			}
		}
	}
	if (!has_purchase) {
		paad->price = 0;
		textParameter = 0;
		paad->purchase_type = -1;
		if (latest_level_entered > 6) {
			paad->purchase_type = -2;
		}
		paad->kong = Character;
	}
	paad->melons = CollectableBase.Melons;
}

void setLocation(purchase_struct* purchase_data) {
	int p_type = purchase_data->purchase_type;
	int bitfield_index = purchase_data->purchase_value - 1;
	int p_kong = purchase_data->move_kong;
	if (p_type != PURCHASE_NOTHING) {
		if (p_type < PURCHASE_FLAG) {
			switch(p_type) {
				case PURCHASE_MOVES:
					MovesBase[p_kong].special_moves |= (1 << bitfield_index);
					break;
				case PURCHASE_SLAM:
					MovesBase[p_kong].simian_slam = purchase_data->purchase_value;
					break;
				case PURCHASE_GUN:
					MovesBase[p_kong].weapon_bitfield |= (1 << bitfield_index);
					break;
				case PURCHASE_AMMOBELT:
					MovesBase[p_kong].ammo_belt = purchase_data->purchase_value;
					break;
				case PURCHASE_INSTRUMENT:
					MovesBase[p_kong].instrument_bitfield |= (1 << bitfield_index);
				break;
			}
		} else if ((p_type == PURCHASE_FLAG) && (purchase_data->purchase_value == -2)) {
			// BFI Coupled Moves
			setPermFlag(FLAG_ABILITY_SHOCKWAVE);
			setPermFlag(FLAG_ABILITY_CAMERA);
		} else if (p_type == PURCHASE_FLAG) {
			// IsFlag
			setPermFlag(purchase_data->purchase_value);
		} else if (p_type == PURCHASE_GB) {
			// IsFlag + GB Update
			setPermFlag(purchase_data->purchase_value);
			MovesBase[p_kong].gb_count[getWorld(CurrentMap,1)] += 1;
		}
	}
}

int getLocation(purchase_struct* purchase_data) {
	int p_type = purchase_data->purchase_type;
	int bitfield_index = purchase_data->purchase_value - 1;
	int p_kong = purchase_data->move_kong;
	if (p_type != PURCHASE_NOTHING) {
		if (p_type < PURCHASE_FLAG) {
			switch(p_type) {
				case PURCHASE_MOVES:
					return (MovesBase[p_kong].special_moves & (1 << bitfield_index)) != 0;
					break;
				case PURCHASE_SLAM:
					return MovesBase[p_kong].simian_slam >= purchase_data->purchase_value;
					break;
				case PURCHASE_GUN:
					return (MovesBase[p_kong].weapon_bitfield & (1 << bitfield_index)) != 0;
					break;
				case PURCHASE_AMMOBELT:
					return MovesBase[p_kong].ammo_belt >= purchase_data->purchase_value;
					break;
				case PURCHASE_INSTRUMENT:
					return (MovesBase[p_kong].instrument_bitfield & (1 << bitfield_index)) != 0;
				break;
			}
		} else if ((p_type == PURCHASE_FLAG) && (purchase_data->purchase_value == -2)) {
			// BFI Coupled Moves
			return checkFlag(FLAG_ABILITY_CAMERA) & checkFlag(FLAG_ABILITY_SHOCKWAVE,0);
		} else if ((p_type == PURCHASE_FLAG) || (p_type == PURCHASE_GB)) {
			// IsFlag
			return checkFlag(purchase_data->purchase_value,0);
		}
	}
}

void setLocationStatus(location_list location_index) {
	int location_int = (int)location_index;
	if (location_int < 4) {
		// TBarrels
		setLocation((purchase_struct*)&TrainingMoves_New[location_int]);
	} else if (location_index == LOCATION_BFI) {
		// BFI
		setLocation((purchase_struct*)&BFIMove_New);
	}
}

int getLocationStatus(location_list location_index) {
	int location_int = (int)location_index;
	if (location_int < 4) {
		// TBarrels
		return getLocation((purchase_struct*)&TrainingMoves_New[location_int]);
	} else if (location_index == LOCATION_BFI) {
		// BFI
		return getLocation((purchase_struct*)&BFIMove_New);
	}
}

void fixTBarrelsAndBFI(int init) {
	if (init) {
		// Individual Barrel Checks
		*(short*)(0x80681CE2) = (short)LOCATION_DIVE;
		*(short*)(0x80681CFA) = (short)LOCATION_ORANGE;
		*(short*)(0x80681D06) = (short)LOCATION_BARREL;
		*(short*)(0x80681D12) = (short)LOCATION_VINE;
		*(int*)(0x80681D38) = 0x0C000000 | (((int)&getLocationStatus & 0xFFFFFF) >> 2); // Get TBarrels Move
		// All Barrels Complete check
		*(short*)(0x80681C8A) = (short)LOCATION_DIVE;
		*(int*)(0x80681C98) = 0x0C000000 | (((int)&getLocationStatus & 0xFFFFFF) >> 2); // Get TBarrels Move
	} else {
		unsigned char tbarrel_bfi_maps[] = {
			0xB0, // TGrounds
			0xB1, // Dive
			0xB4, // Orange
			0xB5, // Barrel
			0xB6, // Vine
			0xBD, // BFI
		};
		int is_in_tbarrel_bfi = 0;
		for (int i = 0; i < sizeof(tbarrel_bfi_maps); i++) {
			if (tbarrel_bfi_maps[i] == CurrentMap) {
				is_in_tbarrel_bfi = 1;
			}
		}
		if (is_in_tbarrel_bfi) {
			// TBarrels
			*(short*)(0x800295F6) = (short)LOCATION_DIVE;
			*(short*)(0x80029606) = (short)LOCATION_ORANGE;
			*(short*)(0x800295FE) = (short)LOCATION_VINE;
			*(short*)(0x800295DA) = (short)LOCATION_BARREL;
			*(int*)(0x80029610) = 0x0C000000 | (((int)&setLocationStatus & 0xFFFFFF) >> 2); // Set TBarrels Move
			// BFI
			*(short*)(0x80027F2A) = (short)LOCATION_BFI;
			*(short*)(0x80027E1A) = (short)LOCATION_BFI;
			*(int*)(0x80027F24) = 0x0C000000 | (((int)&setLocationStatus & 0xFFFFFF) >> 2); // Set BFI Move
			*(int*)(0x80027E20) = 0x0C000000 | (((int)&getLocationStatus & 0xFFFFFF) >> 2); // Get BFI Move
		}
	}
}

// SetFlag Functions
	// Training Barrels
		// DBarrel Flag: 0x800295F4
		// OBarrel Flag: 0x80029604
		// VBarrel Flag: 0x800295FC
		// BBarrel Flag: 0x800295D8
		// TBarrel SetFlag: 0x80029610
		// BFI Camera/Shockwave: 0x80027F28

// CheckFlag Functions
	// Training Barrels
		// DBarrel Flag: 0x80681CE0
		// OBarrel Flag: 0x80681CF8
		// BBarrel Flag: 0x80681D04
		// VBarrel Flag: 0x80681D10
		// TBarrel CheckFlag: 0x80681D38
		// All TBarrels Complete call: 0x80681C98
		// Camera:
			// Usage: 0x806E9814
			// Isles Fairies Display: 0x806AB0F8
			// Other Fairies Display: 0x806AAFB8
			// Film Display: 0x806AA764
			// Film Refill: 0x8060D988

// Other
	// Simian Slam: 0x80027318