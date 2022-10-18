#include "../../include/common.h"

#define FUNKY 1
#define CRANKY 5
#define CANDY 0x19

int getMoveType(int value) {
	int ret = (value >> 5) & 7;
	if (ret == 7) {
		return -1;
	} else {
		return ret;
	}
}

int getMoveIndex(move_rom_item* item) {
	int item_type = getMoveType(item->move_master_data);
	if ((item_type == PURCHASE_FLAG) || (item_type == PURCHASE_GB)) {
		return item->flag;
	}
	return ((item->move_master_data >> 3) & 3) + 1;
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
	if (pass && ((CurrentMap != 0x22) && (CurrentMap != 0x50))) {
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
					if ((purchase_type != PURCHASE_INSTRUMENT) || (CrankyMoves_New[j][i].purchase_value != 1)) {
						if ((purchased) && (shop == 0) && (level == i)) {
							CrankyMoves_New[j][i].purchase_type = PURCHASE_NOTHING;
						} else {
							if (CrankyMoves_New[j][i].purchase_value > progressive_floor) {
								CrankyMoves_New[j][i].purchase_value = purchase_level;
							}
						}
					}
				}
				if (CandyMoves_New[j][i].purchase_type == purchase_type) {
					if ((purchase_type != PURCHASE_INSTRUMENT) || (CandyMoves_New[j][i].purchase_value != 1)) {
						if ((purchased) && (shop == 2) && (level == i)) {
							CandyMoves_New[j][i].purchase_type = PURCHASE_NOTHING;
						} else {
							if (CandyMoves_New[j][i].purchase_value > progressive_floor) {
								CandyMoves_New[j][i].purchase_value = purchase_level;
							}
						}
					}
				}
				if (FunkyMoves_New[j][i].purchase_type == purchase_type) {
					if ((purchase_type != PURCHASE_INSTRUMENT) || (FunkyMoves_New[j][i].purchase_value != 1)) {
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
	}
	*previous_storage = *current_storage;
}

void updateProgressive(void) {
	if (Rando.move_rando_on) {
		int level = getWorld(CurrentMap,0);
		checkProgressive(
			&stored_slam_level,
			&MovesBase[0].simian_slam,
			&StoredSettings.file_extra.location_sss_purchased,
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
			&StoredSettings.file_extra.location_ab1_purchased,
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
			&StoredSettings.file_extra.location_ug1_purchased,
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
			&StoredSettings.file_extra.location_mln_purchased,
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
				CrankyMoves_New[j][i].purchase_value = getMoveIndex((move_rom_item *)&move_data->cranky_moves[j][i]);

				CandyMoves_New[j][i].purchase_type = getMoveType(move_data->candy_moves[j][i].move_master_data);
				CandyMoves_New[j][i].move_kong = getMoveKong(move_data->candy_moves[j][i].move_master_data);
				CandyMoves_New[j][i].purchase_value = getMoveIndex((move_rom_item *)&move_data->candy_moves[j][i]);

				FunkyMoves_New[j][i].purchase_type = getMoveType(move_data->funky_moves[j][i].move_master_data);
				FunkyMoves_New[j][i].move_kong = getMoveKong(move_data->funky_moves[j][i].move_master_data);
				FunkyMoves_New[j][i].purchase_value = getMoveIndex((move_rom_item *)&move_data->funky_moves[j][i]);
			}
		}
		for (int i = 0; i < 4; i++) {
			TrainingMoves_New[i].purchase_type = getMoveType(move_data->training_moves[i].move_master_data);
			TrainingMoves_New[i].move_kong = getMoveKong(move_data->training_moves[i].move_master_data);
			TrainingMoves_New[i].purchase_value = getMoveIndex((move_rom_item *)&move_data->training_moves[i]);
		}
		BFIMove_New.purchase_type = getMoveType(move_data->bfi_move.move_master_data);
		BFIMove_New.move_kong = getMoveKong(move_data->bfi_move.move_master_data);
		BFIMove_New.purchase_value = getMoveIndex((move_rom_item *)&move_data->bfi_move);
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
	int p_index = 0;
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
							has_purchase = 1 ^ (checkFlag(FLAG_ABILITY_CAMERA,0) & checkFlag(FLAG_ABILITY_SHOCKWAVE,0));
						} else {
							has_purchase = 1 ^ checkFlag(p_value,0);
						}
					break;
				}
				if (has_purchase) {
					paad->purchase_type = p_type;
					int p_price = selected->price;
					textParameter = p_price;
					paad->price = p_price;
					if ((p_type == PURCHASE_GB) || (p_type == PURCHASE_FLAG)) {
						paad->flag = p_value;
						paad->purchase_value = p_index;
					} else {
						paad->purchase_value = p_value;
					}
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

void purchaseMove(shop_paad* paad) {
	int item_given = -1;
	int crystals_unlocked = crystalsUnlocked(paad->kong);
	int p_type = paad->purchase_type;
	switch(p_type) {
		case PURCHASE_MOVES:
			setMoveBitfield(paad, paad->kong);
			break;
		case PURCHASE_SLAM:
		case PURCHASE_AMMOBELT:
			setMovesForAllKongs(paad, 0);
			break;
		case PURCHASE_GUN:
		case PURCHASE_INSTRUMENT:
			if (paad->purchase_value == 1) {
				setMoveBitfield(paad, paad->kong);
			} else {
				setMovesForAllKongs(paad, 1);
			}
			break;
		case PURCHASE_GB:
			MovesBase[(int)paad->kong].gb_count[getWorld(CurrentMap,1)] += 1;
		case PURCHASE_FLAG:
			setPermFlag(paad->flag);
		break;
	}
	if (p_type == PURCHASE_INSTRUMENT) {
		int melon_cap = MelonArray[(int)paad->purchase_value];
		if (CollectableBase.Melons < melon_cap) {
			CollectableBase.Melons = melon_cap;
			refillHealth(0);
			SwapObject->unk_2e2 |= 0x11;
		}
	}
	if (p_type == PURCHASE_MOVES) {
		if ((!crystals_unlocked) && (crystalsUnlocked(paad->kong))) {
			item_given = 5;
		}
	} else if ((p_type == PURCHASE_GUN) || (p_type == PURCHASE_AMMOBELT)) {
		item_given = 2;
	} else if ((p_type == PURCHASE_INSTRUMENT)) {
		item_given = 7;
	}
	changeCollectableCount(1, 0, (0 - paad->price));
	if (item_given > -1) {
		changeCollectableCount(item_given, 0, 9999);
	}
	save();
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
					for (int kong = 0; kong < 5; kong++) {
						if (MovesBase[kong].simian_slam < purchase_data->purchase_value) {
							MovesBase[kong].simian_slam = purchase_data->purchase_value;
						}
					}
					break;
				case PURCHASE_GUN:
					if (bitfield_index > 0) {
						for (int kong = 0; kong < 5; kong++) {
							MovesBase[kong].weapon_bitfield |= (1 << bitfield_index);
						}
					} else {
						MovesBase[p_kong].weapon_bitfield |= (1 << bitfield_index);
					}
					break;
				case PURCHASE_AMMOBELT:
					for (int kong = 0; kong < 5; kong++) {
						if (MovesBase[kong].ammo_belt < purchase_data->purchase_value) {
							MovesBase[kong].ammo_belt = purchase_data->purchase_value;
						}
					}
					break;
				case PURCHASE_INSTRUMENT:
					if (bitfield_index > 0) {
						for (int kong = 0; kong < 5; kong++) {
							MovesBase[kong].instrument_bitfield |= (1 << bitfield_index);
						}
					} else {
						MovesBase[p_kong].instrument_bitfield |= (1 << bitfield_index);
					}
					if (CollectableBase.Melons < 2) {
						CollectableBase.Melons = 2;
					} else if ((CollectableBase.Melons < 3) && (bitfield_index > 1)) {
						CollectableBase.Melons = 3;
					}
				break;
			}
		} else if ((p_type == PURCHASE_FLAG) && (purchase_data->purchase_value == -2)) {
			// BFI Coupled Moves
			setFlagDuplicate(FLAG_ABILITY_SHOCKWAVE,1,0);
			setFlagDuplicate(FLAG_ABILITY_CAMERA,1,0);
		} else if (p_type == PURCHASE_FLAG) {
			// IsFlag
			setFlagDuplicate(purchase_data->purchase_value,1,0);
		} else if (p_type == PURCHASE_GB) {
			// IsFlag + GB Update
			setFlagDuplicate(purchase_data->purchase_value,1,0);
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
			return checkFlagDuplicate(FLAG_ABILITY_CAMERA,0) & checkFlagDuplicate(FLAG_ABILITY_SHOCKWAVE,0);
		} else if ((p_type == PURCHASE_FLAG) || (p_type == PURCHASE_GB)) {
			// IsFlag
			return checkFlagDuplicate(purchase_data->purchase_value,0);
		}
	}
	return 0;
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
	return 0;
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

typedef struct move_overlay_paad {
	/* 0x000 */ void* upper_text;
	/* 0x004 */ void* lower_text;
	/* 0x008 */ unsigned char opacity;
	/* 0x009 */ char unk_09[0x10-0x9];
	/* 0x010 */ mtx_item unk_10;
	/* 0x050 */ mtx_item unk_50;
	/* 0x090 */ int timer;
	/* 0x094 */ actorData* shop_owner;
} move_overlay_paad;

unsigned int* displayMoveText(unsigned int* dl, actorData* actor) {
	move_overlay_paad* paad = actor->paad;
	*(unsigned int*)(dl++) = 0xDE000000;
	*(unsigned int*)(dl++) = 0x01000118;
	*(unsigned int*)(dl++) = 0xDA380002;
	*(unsigned int*)(dl++) = 0x02000180;
	*(unsigned int*)(dl++) = 0xE7000000;
	*(unsigned int*)(dl++) = 0x00000000;
	*(unsigned int*)(dl++) = 0xFCFF97FF;
	*(unsigned int*)(dl++) = 0xFF2CFE7F;
	*(unsigned int*)(dl++) = 0xFA000000;
	*(unsigned int*)(dl++) = 0xFFFFFF00 | paad->opacity;
	if (paad->upper_text) {
		*(unsigned int*)(dl++) = 0xDA380002;
		*(unsigned int*)(dl++) = (int)&paad->unk_10;
		dl = (unsigned int*)displayText((int*)dl,1,0,0,paad->upper_text,0x80);
		*(unsigned int*)(dl++) = 0xD8380002;
		*(unsigned int*)(dl++) = 0x00000040;
	}
	if (paad->lower_text) {
		*(unsigned int*)(dl++) = 0xDA380002;
		*(unsigned int*)(dl++) = (int)&paad->unk_50;
		dl = (unsigned int*)displayText((int*)dl,6,0,0,paad->lower_text,0x80);
		*(unsigned int*)(dl++) = 0xD8380002;
		*(unsigned int*)(dl++) = 0x00000040;
	}
	return dl;
}

void getNextMoveText(void) {
	move_overlay_paad* paad = CurrentActorPointer_0->paad;
	int start_hiding = 0;
	actorData* shop_owner = paad->shop_owner;
	shop_paad* shop_data = 0;
	if ((shop_owner == 0) && ((CurrentMap == CRANKY) || (CurrentMap == FUNKY) || (CurrentMap == CANDY))) {
		shop_owner = getSpawnerTiedActor(1,0);
		paad->shop_owner = shop_owner;
	}
	if ((paad->shop_owner) && ((CurrentMap == CRANKY) || (CurrentMap == FUNKY) || (CurrentMap == CANDY))) {
		shop_data = shop_owner->paad2;
	}
	int p_value = 0;
	int p_type = 0;
	int p_kong = 0;
	int p_flag = 0;
	int has_data = 0;
	if (shop_data) {
		has_data = 1;
		p_value = shop_data->purchase_value;
		p_type = shop_data->purchase_type;
		p_kong = shop_data->kong;
		p_flag = shop_data->flag;
	} else if (CurrentMap == 0xBD) {
		has_data = 1;
		p_type = BFIMove_New.purchase_type;
		p_value = BFIMove_New.purchase_value;
		p_kong = BFIMove_New.move_kong;
		p_flag = p_value;
	} else {
		unsigned char tbarrel_maps[] = {0xB1,0xB4,0xB5,0xB6};
		for (int i = 0; i < sizeof(tbarrel_maps); i++) {
			if ((CurrentMap == tbarrel_maps[i]) && (!has_data)) {
				has_data = 1;
				p_type = TrainingMoves_New[i].purchase_type;
				p_value = TrainingMoves_New[i].purchase_value;
				p_kong = TrainingMoves_New[i].move_kong;
				p_flag = p_value;
			}
		}
		if (!has_data) {
			has_data = 1;
			p_type = TextOverlayData[0];
			p_value = TextOverlayData[1];
			p_kong = TextOverlayData[2];
			p_flag = p_value;
		}
	}
	if (has_data) {
		if ((CurrentActorPointer_0->obj_props_bitfield & 0x10) == 0) {
			int top_item = -1;
			int bottom_item = -1;
			mtx_item mtx0;
			mtx_item mtx1;
			_guScaleF(&mtx0, 0x3F19999A, 0x3F19999A, 0x3F800000);
			_guTranslateF(&mtx1, 0x44200000, 0x44480000, 0x0);
			_guMtxCatF(&mtx0, &mtx1, &mtx0);
			_guMtxF2L(&mtx0, &paad->unk_10);
			_guTranslateF(&mtx1, 0, 0x42400000, 0);
			_guMtxCatF(&mtx0, &mtx1, &mtx0);
			_guMtxF2L(&mtx0, &paad->unk_50);
			paad->timer = 0x82;
			if (CurrentMap == CRANKY) {
				paad->timer = 300;
			}
			switch(p_type) {
				case PURCHASE_MOVES:
					{
						int move_index = (p_kong * 4) + p_value;
						top_item = SpecialMovesNames[move_index].name;
						bottom_item = SpecialMovesNames[move_index].latin;
					}
					break;
				case PURCHASE_SLAM:
					top_item = SimianSlamNames[(int)p_value].name;
					bottom_item = SimianSlamNames[(int)p_value].latin;
					break;
				case PURCHASE_GUN:
					if (p_value < 2) {
						top_item = GunNames[p_kong];
					} else {
						top_item = GunUpgNames[p_value];
					}
					break;
				case PURCHASE_AMMOBELT:
					top_item = AmmoBeltNames[p_value];
					break;
				case PURCHASE_INSTRUMENT:
					if (p_value == 1) {
						top_item = InstrumentNames[p_kong];
					} else {
						top_item = InstrumentUpgNames[p_value];
					}
					break;
				case PURCHASE_GB:
				case PURCHASE_FLAG:
					{
						if (p_flag == -2) {
							top_item = 59;
						} else {
							int tied_flags[] = {FLAG_TBARREL_DIVE,FLAG_TBARREL_ORANGE,FLAG_TBARREL_BARREL,FLAG_TBARREL_VINE,FLAG_ABILITY_CAMERA,FLAG_ABILITY_SHOCKWAVE};
							for (int i = 0; i < sizeof(tied_flags) / 4; i++) {
								if (tied_flags[i] == p_flag) {
									top_item = 53 + i;
								}
							}
						}
					}
				break;
			}
			if (top_item < 0) {
				paad->upper_text = (void*)0;
			} else {
				paad->upper_text = getTextPointer(0x27,top_item,0);
			}
			if (bottom_item < 0) {
				paad->lower_text = (void*)0;
			} else {
				paad->lower_text = getTextPointer(0x27,bottom_item,0);
			}
		}
		int timer = paad->timer;
		paad->timer = timer - 1;
		if ((timer > 0) && (paad->timer == 0)) {
			start_hiding = 1;
		}
		timer = paad->timer;
		if (timer == 0x1E) {
			CurrentActorPointer_0->control_state = 2;
		} else if (timer == 0x78) {
			CurrentActorPointer_0->control_state = 1;
		}
		if (CurrentActorPointer_0->control_state == 1) {
			int opacity_diff = 0xFF - paad->opacity;
			int trunc_diff = opacity_diff;
			if (opacity_diff > 0x10) {
				trunc_diff = 0x10;
			}
			paad->opacity += trunc_diff;
		} else if (CurrentActorPointer_0->control_state == 2) {
			int opacity_0 = paad->opacity;
			int trunc_opacity = opacity_0;
			if (opacity_0 > 0x10) {
				trunc_opacity = 0x10;
			}
			paad->opacity = opacity_0 - trunc_opacity;
		}
		if (start_hiding == 0) {
			if (CurrentActorPointer_0->control_state != 0) {
				addDLToOverlay((int)&displayMoveText, CurrentActorPointer_0, 3);
			}
			if (CurrentActorPointer_0->actorType == 0x140) {
				renderActor(CurrentActorPointer_0,0);
			}
		} else {
			deleteActorContainer(CurrentActorPointer_0);
		}
	}
}

void displayBFIMoveText(void) {
	if ((BFIMove_New.purchase_type == PURCHASE_FLAG) && ((BFIMove_New.purchase_value == -2) || (BFIMove_New.purchase_value == FLAG_ABILITY_CAMERA))) {
		displayItemOnHUD(6,0,0);
	}
	if (BFIMove_New.purchase_type != PURCHASE_NOTHING) {
		spawnActor(0x144,0);
	}
}

static const unsigned char Explanation_Special[] = {
	0x00, 0x0B, 0x0F, 0x14, // DK
	0x00, 0x0C, 0x10, 0x15, // Diddy
	0x00, 0x0E, 0x13, 0x16, // Lanky
	0x00, 0x0D, 0x11, 0x17, // Tiny
	0x00, 0x0D, 0x12, 0x18, // Chunky - Is Item 2 a bug?
};

static const unsigned char Explanation_Slam[] = {0x0, 0x19, 0x1A};
static const unsigned char Explanation_Gun[] = {0x0, 0x12, 0x13, 0x14};

void showPostMoveText(shop_paad* paad, KongBase* kong_base, int intro_flag) {
	int substate = paad->unk_0E;
	if (substate == 0) {
		if (groundContactCheck()) {
			LevelStateBitfield |= 0x10030;
			int text_item_0 = -1;
			int text_item_1 = -1;
			int text_file = 0;
			if (Player) {
				Player->obj_props_bitfield &= 0xBFFFFFFF;
			}
			groundContactSet();
			int p_type = paad->purchase_type;
			switch (p_type) {
				case PURCHASE_MOVES:
					text_item_1 = Explanation_Special[(int)((paad->kong * 4) + paad->purchase_value)];
				case PURCHASE_SLAM:
					if (text_item_1 == -1) {
						text_item_1 = Explanation_Slam[(int)paad->purchase_value];
					}
					text_file = 8;
					break;
				case PURCHASE_GUN:
					text_item_1 = Explanation_Gun[(int)paad->purchase_value];
				case PURCHASE_AMMOBELT:
					if (text_item_1 == -1) {
						textParameter = getRefillCount(2,0);
						text_item_1 = 0x15;
					}
					text_file = 7;
					break;
				case PURCHASE_INSTRUMENT:
					if (paad->purchase_value == 1) {
						text_item_1 = 0x12;
						if (!doAllKongsHaveMove(paad,1)) {
							text_item_0 = 0x15;
						}
						text_file = 9;
					} else {
						text_item_1 = 0x13;
						text_file = 9;
						if ((paad->melons + 1) == CollectableBase.Melons) {
							text_item_1 = 0x14;
						} else {
							text_file = 9;
						}
					}
				case PURCHASE_FLAG:
				case PURCHASE_GB:
					{
						int move_flags[] = {FLAG_TBARREL_DIVE, FLAG_TBARREL_ORANGE, FLAG_TBARREL_BARREL, FLAG_TBARREL_VINE, FLAG_ABILITY_CAMERA, FLAG_ABILITY_SHOCKWAVE, -2};
						text_item_1 = 0x0;
						text_file = 8;
						for (int i = 0; i < sizeof(move_flags)/4; i++) {
							if (move_flags[i] == paad->flag) {
								text_item_1 = 0x24 + i;
							}
						}
					}
				break;
			}
			if (text_item_1 == -1) {
				text_item_1 = 0;
			}
			getTextPointer_0(CurrentActorPointer_0, text_file, text_item_1);
			if (text_item_0 > -1) {
				getTextPointer_0(CurrentActorPointer_0, text_file, text_item_0);
			}
			paad->unk_0E += 1;
		}
	} else if (substate == 1) {
		if ((CurrentActorPointer_0->obj_props_bitfield << 6) > -1) {
			setPermFlag(intro_flag);
			cancelPausedCutscene();
			paad->unk_0E += 1;
		}
	} else if ((substate == 2) && (groundContactCheck())) {
		getSequentialPurchase(paad, kong_base);
	}
}