#include "../../include/common.h"

#define FUNKY 1
#define CRANKY 5
#define CANDY 0x19

#define PURCHASE_MOVES 0
#define PURCHASE_SLAM 1
#define PURCHASE_GUN 2
#define PURCHASE_AMMOBELT 3
#define PURCHASE_INSTRUMENT 4
#define PURCHASE_NOTHING -1

int getMoveType(int value) {
	int ret = (value >> 0x4) & 0xF;
	if (ret == 0xF) {
		return -1;
	} else {
		return ret;
	}
}

int getMoveIndex(int value) {
	return value & 0xF;
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
		if (level >= 0 && level < 7) {
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
		for (int i = 0; i < 7; i++) {
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

void moveTransplant(void) {
	for (int i = 0; i < 7; i++) {
		CrankyMoves_New[0][i].purchase_type = getMoveType(Rando.dk_crankymoves[i]);
		CrankyMoves_New[0][i].purchase_value = getMoveIndex(Rando.dk_crankymoves[i]);
		CandyMoves_New[0][i].purchase_type = getMoveType(Rando.dk_candymoves[i]);
		CandyMoves_New[0][i].purchase_value = getMoveIndex(Rando.dk_candymoves[i]);
		FunkyMoves_New[0][i].purchase_type = getMoveType(Rando.dk_funkymoves[i]);
		FunkyMoves_New[0][i].purchase_value = getMoveIndex(Rando.dk_funkymoves[i]);

		CrankyMoves_New[1][i].purchase_type = getMoveType(Rando.diddy_crankymoves[i]);
		CrankyMoves_New[1][i].purchase_value = getMoveIndex(Rando.diddy_crankymoves[i]);
		CandyMoves_New[1][i].purchase_type = getMoveType(Rando.diddy_candymoves[i]);
		CandyMoves_New[1][i].purchase_value = getMoveIndex(Rando.diddy_candymoves[i]);
		FunkyMoves_New[1][i].purchase_type = getMoveType(Rando.diddy_funkymoves[i]);
		FunkyMoves_New[1][i].purchase_value = getMoveIndex(Rando.diddy_funkymoves[i]);

		CrankyMoves_New[2][i].purchase_type = getMoveType(Rando.lanky_crankymoves[i]);
		CrankyMoves_New[2][i].purchase_value = getMoveIndex(Rando.lanky_crankymoves[i]);
		CandyMoves_New[2][i].purchase_type = getMoveType(Rando.lanky_candymoves[i]);
		CandyMoves_New[2][i].purchase_value = getMoveIndex(Rando.lanky_candymoves[i]);
		FunkyMoves_New[2][i].purchase_type = getMoveType(Rando.lanky_funkymoves[i]);
		FunkyMoves_New[2][i].purchase_value = getMoveIndex(Rando.lanky_funkymoves[i]);

		CrankyMoves_New[3][i].purchase_type = getMoveType(Rando.tiny_crankymoves[i]);
		CrankyMoves_New[3][i].purchase_value = getMoveIndex(Rando.tiny_crankymoves[i]);
		CandyMoves_New[3][i].purchase_type = getMoveType(Rando.tiny_candymoves[i]);
		CandyMoves_New[3][i].purchase_value = getMoveIndex(Rando.tiny_candymoves[i]);
		FunkyMoves_New[3][i].purchase_type = getMoveType(Rando.tiny_funkymoves[i]);
		FunkyMoves_New[3][i].purchase_value = getMoveIndex(Rando.tiny_funkymoves[i]);

		CrankyMoves_New[4][i].purchase_type = getMoveType(Rando.chunky_crankymoves[i]);
		CrankyMoves_New[4][i].purchase_value = getMoveIndex(Rando.chunky_crankymoves[i]);
		CandyMoves_New[4][i].purchase_type = getMoveType(Rando.chunky_candymoves[i]);
		CandyMoves_New[4][i].purchase_value = getMoveIndex(Rando.chunky_candymoves[i]);
		FunkyMoves_New[4][i].purchase_type = getMoveType(Rando.chunky_funkymoves[i]);
		FunkyMoves_New[4][i].purchase_value = getMoveIndex(Rando.chunky_funkymoves[i]);
	}
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

// void getPurchaseMoveForLevel(shop_paad* shop, int level, purchase_struct* shop_data, int kong) {
// 	int purchaseable = 0;
// 	int price = 0;
// 	if (level < 7) {
// 		purchase_struct* focus = getObjectArrayAddr(shop_data,6,kong);
// 		focus = getObjectArrayAddr(focus,0x2A,level);
// 		int _type = focus->purchase_type;
// 		int sub_type = 0;
// 		int base_value = 0;
// 		int price = focus->price;
// 		if (_type > -1) {
// 			switch(_type) {
// 				case PURCHASE_MOVES:
// 					sub_type = 1;
// 					base_value = MovesBase[kong].special_moves;
// 					break;
// 				case PURCHASE_SLAM:
// 					sub_type = 0;
// 					base_value = MovesBase[kong].simian_slam;
// 					break;
// 				case PURCHASE_GUN:
// 					sub_type = 1;
// 					base_value = MovesBase[kong].weapon_bitfield;
// 					break;
// 				case PURCHASE_AMMOBELT:
// 					sub_type = 0;
// 					base_value = MovesBase[kong].ammo_belt;
// 					break;
// 				case PURCHASE_INSTRUMENT:
// 					sub_type = 1;
// 					base_value = MovesBase[kong].instrument_bitfield;
// 				break;
// 			}
// 			int p_value = focus->purchase_value;
// 			if (sub_type == 1) {
// 				// Bitfield
// 				if (p_value > 0) {
// 					int bit = 1 << (p_value - 1);
// 					if ((base_value & bit) == 0) {
// 						purchaseable = 1;
// 					}
// 				}
// 			} else {
// 				if (base_value < p_value) {
// 					purchaseable = 1;
// 				}
// 			}
// 			if (purchaseable) {
// 				shop->purchase_type = _type;
// 				*(short*)(0x80750AC8) = price;
// 				shop->price = price;
// 				shop->purchase_value = p_value;
// 			}
// 		}
// 	}
// 	if (!purchaseable) {
// 		shop->price = 0;
// 		*(short*)(0x80750AC8) = price;
// 		shop->purchase_type = -2;
// 	}
// 	shop->melons = CollectableBase.Melons;
// }

// void getRandoNextMovePurchase(shop_paad* shop_info, KongBase* moves) {
// 	int shop_type = CurrentActorPointer_0->actorType;
// 	int world = getWorld(CurrentMap,0);
// 	purchase_struct* shop_struct = (purchase_struct*)&CrankyMoves_New;
// 	if (shop_type == 0xBE) {
// 		shop_struct = (purchase_struct*)&FunkyMoves_New;
// 	} else if (shop_type == 0xBF) {
// 		shop_struct = (purchase_struct*)&CandyMoves_New;
// 	}
// 	getPurchaseMoveForLevel(shop_info,world,shop_struct,Character);
// }

/*
JAL_NewMoveFunc:
JAL 	getRandoNextMovePurchase
NOP

LUI 	t3, 0x8002
LUI 	t4, hi(JAL_NewMoveFunc)
LW 		t4, lo(JAL_NewMoveFunc) (t4)
SW 		t4, 0x6720 (t3)
SW 		t4, 0x683C (t3)
*/