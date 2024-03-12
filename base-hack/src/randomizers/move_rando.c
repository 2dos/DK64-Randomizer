#include "../../include/common.h"

static unsigned short slam_flag = FLAG_SHOPMOVE_SLAM_0;
static unsigned short belt_flag = FLAG_SHOPMOVE_BELT_0;
static unsigned short ins_flag = FLAG_SHOPMOVE_INS_0;

int getMoveType(int value) {
	int ret = (value >> 5) & 7;
	if (ret == 7) {
		return -1;
	} else {
		if (ret == PURCHASE_INSTRUMENT) {
			int index = ((value >> 3) & 3) + 1;
			if (index > 1) {
				return PURCHASE_FLAG;
			}
		} else if ((ret == PURCHASE_SLAM) || (ret == PURCHASE_AMMOBELT)) {
			return PURCHASE_FLAG;
		}
		return ret;
	}
}

int getMoveIndex(move_rom_item* item) {
	int item_type = getMoveType(item->move_master_data);
	int index = ((item->move_master_data >> 3) & 3) + 1;
	int original_item_type = ((item->move_master_data) >> 5) & 7;
	if (original_item_type == PURCHASE_SLAM) {
		slam_flag += 1;
		return slam_flag - 1;
	} else if (original_item_type == PURCHASE_AMMOBELT) {
		belt_flag += 1;
		return belt_flag - 1;
	} else if (original_item_type == PURCHASE_INSTRUMENT) {
		if (index > 1) {
			ins_flag += 1;
			return ins_flag - 1;
		}
	}
	if ((item_type == PURCHASE_FLAG) || (item_type == PURCHASE_GB)) {
		return item->flag;
	}
	return index;
}

int getMoveKong(int value) {
	return value & 7; 
}

move_block* getMoveBlock(void) {
	return getFile(0x200, 0x1FEF000);
}

void moveTransplant(void) {
	slam_flag = FLAG_SHOPMOVE_SLAM_0;
	belt_flag = FLAG_SHOPMOVE_BELT_0;
	ins_flag = FLAG_SHOPMOVE_INS_0;
	move_block* move_data = getMoveBlock();
	if (move_data) {
		for (int i = 0; i < LEVEL_COUNT; i++) {
			int stored_slam = slam_flag;
			int stored_belt = belt_flag;
			int stored_ins = ins_flag;
			int cranky_type = (move_data->cranky_moves[0][i].move_master_data >> 5) & 7;
			int funky_type = (move_data->funky_moves[0][i].move_master_data >> 5) & 7;
			int candy_type = (move_data->candy_moves[0][i].move_master_data >> 5) & 7;
			int cranky_shared = 1;
			int funky_shared = 1;
			int candy_shared = 1;
			if ((cranky_type > 2) && (cranky_type < 5)) {
				cranky_shared = cranky_type - 1;
			} else if (cranky_type != 1) {
				cranky_shared = 0;
			}
			if ((funky_type > 2) && (funky_type < 5)) {
				funky_shared = funky_type - 1;
			} else if (funky_type != 1) {
				funky_shared = 0;
			}
			if ((candy_type > 2) && (candy_type < 5)) {
				candy_shared = candy_type - 1;
			} else if (candy_type != 1) {
				candy_shared = 0;
			}
			int cranky_targ_data = move_data->cranky_moves[0][i].move_master_data & 0xF8;
			int cranky_targ_flag = move_data->cranky_moves[0][i].flag;
			int funky_targ_data = move_data->funky_moves[0][i].move_master_data & 0xF8;
			int funky_targ_flag = move_data->funky_moves[0][i].flag;
			int candy_targ_data = move_data->candy_moves[0][i].move_master_data & 0xF8;
			int candy_targ_flag = move_data->candy_moves[0][i].flag;
			for (int j = 1; j < 5; j++) {
				if (((move_data->cranky_moves[j][i].move_master_data & 0xF8) != cranky_targ_data) || (move_data->cranky_moves[j][i].flag != cranky_targ_flag)) {
					cranky_shared = 0;
				}
				if (((move_data->funky_moves[j][i].move_master_data & 0xF8) != funky_targ_data) || (move_data->funky_moves[j][i].flag != funky_targ_flag)) {
					funky_shared = 0;
				}
				if (((move_data->candy_moves[j][i].move_master_data & 0xF8) != candy_targ_data) || (move_data->candy_moves[j][i].flag != candy_targ_flag)) {
					candy_shared = 0;
				}
			}
			for (int j = 0; j < 5; j++) {
				if ((cranky_shared == 1) || (funky_shared == 1) || (candy_shared == 1)) {
					slam_flag = stored_slam;
				}
				if ((cranky_shared == 2) || (funky_shared == 2) || (candy_shared == 2)) {
					belt_flag = stored_belt;
				}
				if ((cranky_shared == 3) || (funky_shared == 3) || (candy_shared == 3)) {
					ins_flag = stored_ins;
				}
				CrankyMoves_New[j][i].purchase_type = getMoveType(move_data->cranky_moves[j][i].move_master_data);
				CrankyMoves_New[j][i].move_kong = getMoveKong(move_data->cranky_moves[j][i].move_master_data);
				CrankyMoves_New[j][i].purchase_value = getMoveIndex((move_rom_item *)&move_data->cranky_moves[j][i]);
				CrankyMoves_New[j][i].price = move_data->cranky_moves[j][i].price;
				CrankyMoves_New[j][i].price = move_data->cranky_moves[j][i].price;

				CandyMoves_New[j][i].purchase_type = getMoveType(move_data->candy_moves[j][i].move_master_data);
				CandyMoves_New[j][i].move_kong = getMoveKong(move_data->candy_moves[j][i].move_master_data);
				CandyMoves_New[j][i].purchase_value = getMoveIndex((move_rom_item *)&move_data->candy_moves[j][i]);
				CandyMoves_New[j][i].price = move_data->candy_moves[j][i].price;

				FunkyMoves_New[j][i].purchase_type = getMoveType(move_data->funky_moves[j][i].move_master_data);
				FunkyMoves_New[j][i].move_kong = getMoveKong(move_data->funky_moves[j][i].move_master_data);
				FunkyMoves_New[j][i].purchase_value = getMoveIndex((move_rom_item *)&move_data->funky_moves[j][i]);
				FunkyMoves_New[j][i].price = move_data->funky_moves[j][i].price;
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
		FirstMove_New.purchase_type = getMoveType(move_data->first_move.move_master_data);
		FirstMove_New.move_kong = getMoveKong(move_data->first_move.move_master_data);
		FirstMove_New.purchase_value = getMoveIndex((move_rom_item *)&move_data->first_move);
	}
	complex_free(move_data);
}

void progressiveChange(int flag) {
	if (!checkFlagDuplicate(flag, FLAGTYPE_PERMANENT)) {
		int subtype = getMoveProgressiveFlagType(flag);
		if (subtype == 0) {
			// Slam
			giveSlamLevel();
		} else if (subtype == 1) {
			// Belt
			int belt_level = MovesBase[0].ammo_belt + 1;
			for (int i = 0; i < 5; i++) {
				MovesBase[i].ammo_belt = belt_level;
			}
		} else if (subtype == 2) {
			// Instrument upgrade
			int ins_level = 0;
			for (int i = 1; i < 4; i++) {
				if (MovesBase[0].instrument_bitfield & (1 << i)) {
					ins_level = i;
				}
			}
			if (ins_level > 0) {
				if (CollectableBase.Melons < 3) {
					CollectableBase.Melons = 3;
					CollectableBase.Health = CollectableBase.Melons << 2;
				}
			} else {
				if (CollectableBase.Melons < 2) {
					CollectableBase.Melons = 2;
					CollectableBase.Health = CollectableBase.Melons << 2;
				}
			}
			for (int i = 0; i < 5; i++) {
				MovesBase[i].instrument_bitfield |= (1 << (ins_level + 1));
			}
		}
	}
}

int getMoveProgressiveFlagType(int flag) {
	if (isSlamFlag(flag)) {
		return 0;
	} else if (isBeltFlag(flag)) {
		return 1;
	} else if (isInstrumentUpgradeFlag(flag)) {
		return 2;
	}
	return -1;
}

int writeProgressiveText(int flag, int* top_text, int* bottom_text) {
	int subtype = getMoveProgressiveFlagType(flag);
	if (subtype == 0) {
		// Slam
		*top_text = SimianSlamNames[(int)MovesBase[0].simian_slam].name;
		*bottom_text = SimianSlamNames[(int)MovesBase[0].simian_slam].latin;
		return 1;
	} else if (subtype == 1) {
		// Belt
		*top_text = AmmoBeltNames[(int)MovesBase[0].ammo_belt];
		return 1;
	} else if (subtype == 2) {
		// Instrument upgrade
		int level = 2;
		if (MovesBase[0].instrument_bitfield & 8) {
			level = 4;
		} else if (MovesBase[0].instrument_bitfield & 4) {
			level = 3;
		}
		*top_text = InstrumentUpgNames[level];
		return 1;
	}
	return 0;
}

void getNextMovePurchase(shop_paad* paad, KongBase* movedata) {
	int has_purchase = 0;
	int latest_level_entered = 0;
	int has_entered_level = 1; // Set to 0 forcing level entry requirement
	for (int i = 0; i < 7; i++) {
		if (checkFlag((FLAG_STORY_JAPES + i), FLAGTYPE_PERMANENT)) {
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
			if (p_kong > 4) {
				p_kong = 0;
			}
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
							has_purchase = 1 ^ (checkFlagDuplicate(FLAG_ABILITY_CAMERA, FLAGTYPE_PERMANENT) & checkFlagDuplicate(FLAG_ABILITY_SHOCKWAVE, FLAGTYPE_PERMANENT));
						} else {
							has_purchase = 1 ^ checkFlagDuplicate(p_value, FLAGTYPE_PERMANENT);
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

purchase_classification getPurchaseClassification(int purchase_type, int flag) {
	if ((purchase_type == PURCHASE_MOVES) || (purchase_type == PURCHASE_SLAM)) {
		return PCLASS_MOVE;
	} else if ((purchase_type == PURCHASE_AMMOBELT) || (purchase_type == PURCHASE_GUN)) {
		return PCLASS_GUN;
	} else if (purchase_type == PURCHASE_INSTRUMENT) {
		return PCLASS_INSTRUMENT;
	} else if (purchase_type == PURCHASE_GB) {
		return PCLASS_GB;
	} else if (purchase_type == PURCHASE_FLAG) {
		int subtype = getMoveProgressiveFlagType(flag);
		if (subtype == 0) {
			return PCLASS_MOVE;
		} else if (subtype == 1) {
			return PCLASS_GUN;
		} else if (subtype == 2) {
			return PCLASS_INSTRUMENT;
		}
		if (flag == -2) {
			return PCLASS_CAMSHOCK;
		} else if (isTBarrelFlag(flag)) {
			return PCLASS_MOVE;
		} else if (flag == FLAG_ABILITY_CAMERA) {
			return PCLASS_CAMERA;
		} else if (flag == FLAG_ABILITY_SHOCKWAVE) {
			return PCLASS_SHOCKWAVE;
		} else if (isFlagInRange(flag, FLAG_BP_JAPES_DK_HAS, 40)) {
			return PCLASS_BLUEPRINT;
		} else if (isFlagInRange(flag, FLAG_MEDAL_JAPES_DK, 40)) {
			return PCLASS_MEDAL;
		} else if ((flag == FLAG_COLLECTABLE_NINTENDOCOIN) || (flag == FLAG_COLLECTABLE_RAREWARECOIN)) {
			return PCLASS_COMPANYCOIN;
		} else if (isFlagInRange(flag, FLAG_CROWN_JAPES, 10)) {
			return PCLASS_CROWN;
		} else if (flag == FLAG_COLLECTABLE_BEAN) {
			return PCLASS_BEAN;
		} else if (isFlagInRange(flag, FLAG_PEARL_0_COLLECTED, 5)) {
			return PCLASS_PEARL;
		} else if (isFlagInRange(flag, FLAG_FAIRY_1, 20)) {
			return PCLASS_FAIRY;
		} else if (isFlagInRange(flag, FLAG_FAKEITEM, 0x10)) {
			return PCLASS_FAKEITEM;
		} else {
			for (int i = 0; i < 8; i++) {
				if (flag == getKeyFlag(i)) {
					return PCLASS_KEY;
				}
			}
		}
	}
	return PCLASS_NOTHING;
}

static helm_hurry_items hh_item_list[] = {
	HHITEM_NOTHING, // PCLASS_NOTHING,
	HHITEM_MOVE, // PCLASS_MOVE,
	HHITEM_MOVE, // PCLASS_INSTRUMENT,
	HHITEM_MOVE, // PCLASS_GUN,
	HHITEM_MOVE, // PCLASS_CAMERA,
	HHITEM_MOVE, // PCLASS_SHOCKWAVE,
	HHITEM_MOVE, // PCLASS_CAMSHOCK,
	HHITEM_NOTHING, // PCLASS_GB, - Handled separately
	HHITEM_BLUEPRINT, // PCLASS_BLUEPRINT,
	HHITEM_COMPANYCOIN, // PCLASS_COMPANYCOIN,
	HHITEM_MEDAL, // PCLASS_MEDAL,
	HHITEM_RAINBOWCOIN, // PCLASS_RAINBOWCOIN,
	HHITEM_KEY, // PCLASS_KEY,
	HHITEM_CROWN, // PCLASS_CROWN,
	HHITEM_BEAN, // PCLASS_BEAN,
	HHITEM_PEARL, // PCLASS_PEARL,
	HHITEM_KONG, // PCLASS_KONG,
	HHITEM_FAIRY, // PCLASS_FAIRY,
	HHITEM_FAKEITEM, // PCLASS_FAKEITEM,
};

void addHelmHurryPurchaseTime(int purchase_type, int flag) {
	purchase_classification pclass = getPurchaseClassification(purchase_type, flag);
	helm_hurry_items hh_item = hh_item_list[(int)pclass];
	if (hh_item != HHITEM_NOTHING) {
		addHelmTime(hh_item, 1);
	}
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
			giveGB(Character, getWorld(CurrentMap, 1));
		case PURCHASE_FLAG:
			progressiveChange(paad->flag);
			if (paad->flag == -2) {
				setFlagDuplicate(FLAG_ABILITY_CAMERA, 1, FLAGTYPE_PERMANENT);
				setFlagDuplicate(FLAG_ABILITY_SHOCKWAVE, 1, FLAGTYPE_PERMANENT);
				if (CollectableBase.Film < 10) {
					CollectableBase.Film = 10;
				}
				if (CollectableBase.Crystals < (10*150)) {
					CollectableBase.Crystals = 10*150;
				}
			} else if ((paad->flag >= FLAG_FAKEITEM) && (paad->flag < (FLAG_FAKEITEM + 0x10))) {
				setFlagDuplicate(paad->flag, 1, FLAGTYPE_PERMANENT);
				queueIceTrap();
			} else {
				setFlagDuplicate(paad->flag, 1, FLAGTYPE_PERMANENT);
				if (paad->flag == FLAG_ABILITY_CAMERA) {
                    if (CollectableBase.Film < 10) {
						CollectableBase.Film = 10;
					}
                } else if (paad->flag == FLAG_ABILITY_SHOCKWAVE) {
                    if (CollectableBase.Crystals < (10*150)) {
						CollectableBase.Crystals = 10*150;
					}
                }
			}
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
	addHelmHurryPurchaseTime(paad->purchase_type, paad->flag);
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
						CollectableBase.Health = CollectableBase.Melons << 2;
					} else if ((CollectableBase.Melons < 3) && (bitfield_index > 1)) {
						CollectableBase.Melons = 3;
						CollectableBase.Health = CollectableBase.Melons << 2;
					}
				break;
			}
		} else if ((p_type == PURCHASE_FLAG) && (purchase_data->purchase_value == -2)) {
			// BFI Coupled Moves
			setFlagDuplicate(FLAG_ABILITY_SHOCKWAVE,1,FLAGTYPE_PERMANENT);
			setFlagDuplicate(FLAG_ABILITY_CAMERA,1,FLAGTYPE_PERMANENT);
			if (CollectableBase.Film < 10) {
				CollectableBase.Film = 10;
			}
			if (CollectableBase.Crystals < (10*150)) {
				CollectableBase.Crystals = 10*150;
			}
		} else if ((p_type == PURCHASE_FLAG) && (isFlagInRange(purchase_data->purchase_value, FLAG_FAKEITEM, 0x10))) {
			setFlagDuplicate(purchase_data->purchase_value,1,FLAGTYPE_PERMANENT);
			queueIceTrap();
		} else if (p_type == PURCHASE_FLAG) {
			// IsFlag
			progressiveChange(purchase_data->purchase_value);
			setFlagDuplicate(purchase_data->purchase_value,1,FLAGTYPE_PERMANENT);
			if (purchase_data->purchase_value == FLAG_ABILITY_CAMERA) {
				if (CollectableBase.Film < 10) {
					CollectableBase.Film = 10;
				}
			} else if (purchase_data->purchase_value == FLAG_ABILITY_SHOCKWAVE) {
				if (CollectableBase.Crystals < (10*150)) {
					CollectableBase.Crystals = 10*150;
				}
			}
		} else if (p_type == PURCHASE_GB) {
			// IsFlag + GB Update
			if (!checkFlagDuplicate(purchase_data->purchase_value, FLAGTYPE_PERMANENT)) {
				setFlagDuplicate(purchase_data->purchase_value,1,FLAGTYPE_PERMANENT);
				int world = getWorld(CurrentMap,1);
				if (world > 7) {
					world = 7;
				}
				giveGB(p_kong, world);
			}
		}
		addHelmHurryPurchaseTime(p_type, purchase_data->purchase_value);
	}
}

int getLocation(purchase_struct* purchase_data) {
	int p_type = purchase_data->purchase_type;
	int bitfield_index = purchase_data->purchase_value - 1;
	int p_kong = purchase_data->move_kong;
	if (p_kong > 4) {
		p_kong = 0;
	}
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
			return checkFlagDuplicate(FLAG_ABILITY_CAMERA, FLAGTYPE_PERMANENT) & checkFlagDuplicate(FLAG_ABILITY_SHOCKWAVE, FLAGTYPE_PERMANENT);
		} else if ((p_type == PURCHASE_FLAG) || (p_type == PURCHASE_GB)) {
			// IsFlag
			return checkFlagDuplicate(purchase_data->purchase_value, FLAGTYPE_PERMANENT);
		}
	}
	return 1;
}

void setLocationStatus(location_list location_index) {
	int location_int = (int)location_index;
	if (location_int < 4) {
		// TBarrels
		setLocation((purchase_struct*)&TrainingMoves_New[location_int]);
	} else if (location_index == LOCATION_BFI) {
		// BFI
		setLocation((purchase_struct*)&BFIMove_New);
	} else if (location_index == LOCATION_FIRSTMOVE) {
		// First Move (Normally Slam 1)
		setLocation((purchase_struct*)&FirstMove_New);
	}
}

int getLocationStatus(location_list location_index) {
	int location_int = (int)location_index;
	if (location_int < 4) {
		// TBarrels
		return getLocation(&TrainingMoves_New[location_int]);
	} else if (location_index == LOCATION_BFI) {
		// BFI
		return getLocation(&BFIMove_New);
	} else if (location_index == LOCATION_FIRSTMOVE) {
		// First Move (Normally Slam 1)
		return getLocation(&FirstMove_New);
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
		writeFunction(0x80681D38, &getLocationStatus); // Get TBarrels Move
		// All Barrels Complete check
		*(short*)(0x80681C8A) = (short)LOCATION_DIVE;
		writeFunction(0x80681C98, &getLocationStatus); // Get TBarrels Move
	} else {
		unsigned char tbarrel_bfi_maps[] = {
			MAP_TRAININGGROUNDS, // TGrounds
			MAP_TBARREL_DIVE, // Dive
			MAP_TBARREL_ORANGE, // Orange
			MAP_TBARREL_BARREL, // Barrel
			MAP_TBARREL_VINE, // Vine
			MAP_FAIRYISLAND, // BFI
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
			writeFunction(0x80029610, &setLocationStatus); // Set TBarrels Move
			// BFI
			*(short*)(0x80027F2A) = (short)LOCATION_BFI;
			*(short*)(0x80027E1A) = (short)LOCATION_BFI;
			writeFunction(0x80027F24, &setLocationStatus); // Set BFI Move
			writeFunction(0x80027E20, &getLocationStatus); // Get BFI Move
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
	int is_jetpac = CurrentActorPointer_0->actorType == getCustomActorIndex(NEWACTOR_JETPACITEMOVERLAY);
	if (!is_jetpac) {
		if ((shop_owner == 0) && (inShop(CurrentMap, 0))) {
			shop_owner = getSpawnerTiedActor(1,0);
			paad->shop_owner = shop_owner;
		}
		if ((paad->shop_owner) && (inShop(CurrentMap, 0))) {
			shop_data = shop_owner->paad2;
		}
	}
	int p_value = 0;
	int p_type = 0;
	int p_kong = 0;
	int p_flag = 0;
	char* p_string = 0;
	int has_data = 0;
	if (shop_data) {
		has_data = 1;
		p_value = shop_data->purchase_value;
		p_type = shop_data->purchase_type;
		p_kong = shop_data->kong;
		p_flag = shop_data->flag;
	} else if (TextOverlayData.flag != 0) {
		has_data = 1;
		p_type = TextOverlayData.type;
		p_value = TextOverlayData.flag;
		p_kong = TextOverlayData.kong;
		p_string = TextOverlayData.string;
		p_flag = p_value;
	} else if (CurrentMap == MAP_FAIRYISLAND) {
		has_data = 1;
		p_type = BFIMove_New.purchase_type;
		p_value = BFIMove_New.purchase_value;
		p_kong = BFIMove_New.move_kong;
		p_flag = p_value;
	} else {
		unsigned char tbarrel_maps[] = {MAP_TBARREL_DIVE,MAP_TBARREL_ORANGE,MAP_TBARREL_BARREL,MAP_TBARREL_VINE};
		for (int i = 0; i < sizeof(tbarrel_maps); i++) {
			if ((CurrentMap == tbarrel_maps[i]) && (!has_data)) {
				has_data = 1;
				p_type = TrainingMoves_New[i].purchase_type;
				p_value = TrainingMoves_New[i].purchase_value;
				p_kong = TrainingMoves_New[i].move_kong;
				p_flag = p_value;
			}
		}
	}
	int override_string = Rando.archipelago && p_type == 8;
	if ((has_data) || (paad->upper_text) || (paad->lower_text)) {
		if ((CurrentActorPointer_0->obj_props_bitfield & 0x10) == 0) {
			TextOverlayData.kong = 0;
			TextOverlayData.flag = 0;
			TextOverlayData.type = 0;
			TextOverlayData.string = 0;
			int overlay_count = 0;
			for (int i = 0; i < LoadedActorCount; i++) {
				actorData* actor = (actorData*)LoadedActorArray[i].actor;
				if (actor) {
					if ((actor->actorType == 0x140) || (actor->actorType == 0x144)) {
						if (actor != CurrentActorPointer_0) {
							overlay_count += 1;
						}
					}
				}
			}
			int top_item = -1;
			int bottom_item = -1;
			mtx_item mtx0;
			mtx_item mtx1;
			_guScaleF(&mtx0, 0x3F19999A, 0x3F19999A, 0x3F800000);
			float start_y = 800.0f;
			if (Rando.true_widescreen) {
				start_y = (4 * SCREEN_HD_FLOAT) - 160.0f;
			}
			float position = start_y - (overlay_count * 100.0f); // Gap of 100.0f
			float move_x = 640.0f;
			if (Rando.true_widescreen) {
				move_x = SCREEN_WD_FLOAT * 2;
			}
			_guTranslateF(&mtx1, move_x, position, 0.0f);
			_guMtxCatF(&mtx0, &mtx1, &mtx0);
			_guMtxF2L(&mtx0, &paad->unk_10);
			_guTranslateF(&mtx1, 0.0f, 48.0f, 0.0f);
			_guMtxCatF(&mtx0, &mtx1, &mtx0);
			_guMtxF2L(&mtx0, &paad->unk_50);
			paad->timer = 0x82;
			if ((CurrentMap == MAP_CRANKY) && (!is_jetpac)) {
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
							top_item = ITEMTEXT_CAMERACOMBO;
						} else {
							if (!writeProgressiveText(p_flag, &top_item, &bottom_item)) {
								int tied_flags[] = {FLAG_TBARREL_DIVE,FLAG_TBARREL_ORANGE,FLAG_TBARREL_BARREL,FLAG_TBARREL_VINE,FLAG_ABILITY_CAMERA,FLAG_ABILITY_SHOCKWAVE};
								for (int i = 0; i < sizeof(tied_flags) / 4; i++) {
									if (tied_flags[i] == p_flag) {
										top_item = ITEMTEXT_DIVE + i;
									}
								}
							}
						}
						if (top_item == -1) {
							if (isFlagInRange(p_flag, FLAG_BP_JAPES_DK_HAS, 40)) {
								// Blueprint
								int kong = (p_flag - FLAG_BP_JAPES_DK_HAS) % 5;
								top_item = ITEMTEXT_BLUEPRINT_DK + kong;
							} else if (isFlagInRange(p_flag, FLAG_MEDAL_JAPES_DK, 40)) {
								// Medal
								top_item = ITEMTEXT_MEDAL;
							} else if (p_flag == FLAG_COLLECTABLE_NINTENDOCOIN) {
								// Nintendo Coin
								top_item = ITEMTEXT_NINTENDO;
							} else if (p_flag == FLAG_COLLECTABLE_RAREWARECOIN) {
								// Rareware Coin
								top_item = ITEMTEXT_RAREWARE;
							} else if (isFlagInRange(p_flag, FLAG_CROWN_JAPES, 10)) {
								// Crown
								top_item = ITEMTEXT_CROWN;
							} else if (p_flag == FLAG_COLLECTABLE_BEAN) {
								// Fungi Bean
								top_item = ITEMTEXT_BEAN;
							} else if (isFlagInRange(p_flag, FLAG_PEARL_0_COLLECTED, 5)) {
								// Galleon Pearls
								top_item = ITEMTEXT_PEARL;
							} else if (isFlagInRange(p_flag, FLAG_FAIRY_1, 20)) {
								// Banana Fairy
								top_item = ITEMTEXT_FAIRY;
							} else if (isFlagInRange(p_flag, FLAG_FAKEITEM, 0x10)) {
								// Fake Item
								top_item = ITEMTEXT_FAKEITEM;
							} else {
								// Key Number
								for (int i = 0; i < 8; i++) {
									if (p_flag == getKeyFlag(i)) {
										top_item = ITEMTEXT_KEY1 + i;
									}
								}
								// Kongs
								if (top_item == -1) {
									for (int i = 0; i < 5; i++) {
										if (p_flag == kong_flags[i]) {
											top_item = ITEMTEXT_KONG_DK + i;
										}
									}
								}
								if (top_item == -1) {
									// Default to GB
									top_item = ITEMTEXT_BANANA;
								}
							}
						}
					}
				break;
			}
			if (override_string) {
				paad->upper_text = p_string;
			} else {
				if (top_item < 0) {
					paad->upper_text = (void*)0;
				} else {
					paad->upper_text = getTextPointer(0x27,top_item,0);
				}
			}
			if (bottom_item < 0) {
				paad->lower_text = (void*)0;
			} else {
				paad->lower_text = getTextPointer(0x27,bottom_item,0);
			}
			priceTransplant();
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
						int explanation_start = 0x25;
						for (int i = 0; i < sizeof(move_flags)/4; i++) {
							if (move_flags[i] == paad->flag) {
								text_item_1 = explanation_start + i;
							}
						}
						int subtype = getMoveProgressiveFlagType(paad->flag);
						if (subtype == 0) {
							// Slam
							text_item_1 = Explanation_Slam[(int)MovesBase[0].simian_slam];
							text_file = 8;
						} else if (subtype == 1) {
							// Belt
							textParameter = getRefillCount(2,0);
							text_item_1 = 0x15;
							text_file = 7;
						} else if (subtype == 2) {
							// Shop upgrade
							text_item_1 = 0x13;
							text_file = 9;
							if ((paad->melons + 1) == CollectableBase.Melons) {
								text_item_1 = 0x14;
							} else {
								text_file = 9;
							}
						} else {
							text_item_1 = explanation_start + 7;
							text_file = 8;
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