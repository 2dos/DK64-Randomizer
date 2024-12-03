#include "../../include/common.h"

static short flag_purchase_types[] = {
	PURCHASE_FLAG,
	PURCHASE_GB,
	PURCHASE_ICEBUBBLE,
	PURCHASE_ICEREVERSE,
	PURCHASE_ICESLOW,
};

void moveTransplant(void) {
	int size = 126 * sizeof(purchase_struct);
	copyFromROM(0x1FEF800,&CrankyMoves_New[0][0].purchase_type,&size,0,0,0,0);
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
		purchase_struct* selected = getShopData(shop_owner - 0xBD, Character, world);
		if (selected) {
			int p_type = selected->purchase_type;
			int p_kong = selected->move_kong;
			int p_value = selected->purchase_value;
			if (p_kong > 4) {
				p_kong = 0;
			}
			if (p_type > -1) {
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
					case PURCHASE_ICEBUBBLE:
					case PURCHASE_ICEREVERSE:
					case PURCHASE_ICESLOW:
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
					if (inShortList(p_type, &flag_purchase_types[0], sizeof(flag_purchase_types) >> 1)) {
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
		} else if (isFlagInRange(flag, FLAG_WRINKLYVIEWED, 35)) {
			return PCLASS_HINT;
		} else if (isMedalFlag(flag)) {
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
		} else if (isIceTrapFlag(flag) == DYNFLAG_ICETRAP) {
			return PCLASS_FAKEITEM;
		} else {
			for (int i = 0; i < 8; i++) {
				if (flag == getKeyFlag(i)) {
					return PCLASS_KEY;
				}
			}
		}
	} else if ((purchase_type >= PURCHASE_ICEBUBBLE) && (purchase_type <= PURCHASE_ICESLOW)) {
		return PCLASS_FAKEITEM;
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
			} else if (isIceTrapFlag(paad->flag) == DYNFLAG_ICETRAP) {
				setFlagDuplicate(paad->flag, 1, FLAGTYPE_PERMANENT);
				queueIceTrap(ICETRAP_BUBBLE);
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
		case PURCHASE_ICEBUBBLE:
		case PURCHASE_ICEREVERSE:
		case PURCHASE_ICESLOW:
			setFlagDuplicate(paad->flag, 1, FLAGTYPE_PERMANENT);
			queueIceTrap((p_type - PURCHASE_ICEBUBBLE) + ICETRAP_BUBBLE);
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

int checkFirstMovePurchase(void) {
	if (!checkFlag(0x17F, FLAGTYPE_PERMANENT)) {
		return 0; // Training Barrels not spawned
	}
	for (int i = 0; i < 4; i++) {
		if (!checkFlag(FLAG_TBARREL_DIVE + i, FLAGTYPE_PERMANENT)) {
			return 0; // Lacking a training barrel complete
		}
	}
	if (checkFlag(0x180, FLAGTYPE_PERMANENT)) {
		return 1; // First move given
	}
	if (FirstMove_New.purchase_type == -1) {
		setFlag(0x180, 1, FLAGTYPE_PERMANENT);
		return 1; // First move is nothing
	}
	return 0;
}

void purchaseFirstMoveHandler(shop_paad* paad) {
	int purchase_type = FirstMove_New.purchase_type;
	paad->purchase_type = FirstMove_New.purchase_type;
	if ((purchase_type == PURCHASE_FLAG) || (purchase_type == PURCHASE_GB)) {
		paad->flag = FirstMove_New.purchase_value;
	} else if (purchase_type == -1) {
		CurrentActorPointer_0->control_state = 3;
		return;
	} else {
		paad->purchase_value = FirstMove_New.purchase_value;
	}
	paad->kong = FirstMove_New.move_kong;
	paad->price = 0;
	purchaseMove(paad);
}

void setLocation(purchase_struct* purchase_data) {
	int p_type = purchase_data->purchase_type;
	int bitfield_index = purchase_data->purchase_value - 1;
	int p_kong = purchase_data->move_kong;
	if (p_type != -1) {
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
		} else if ((p_type == PURCHASE_FLAG) && (isIceTrapFlag(purchase_data->purchase_value) == DYNFLAG_ICETRAP)) {
			setFlagDuplicate(purchase_data->purchase_value,1,FLAGTYPE_PERMANENT);
			queueIceTrap(ICETRAP_BUBBLE);
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
		} else if ((p_type >= PURCHASE_ICEBUBBLE) && (p_type <= PURCHASE_ICESLOW)) {
			setFlagDuplicate(purchase_data->purchase_value, 1, FLAGTYPE_PERMANENT);
			queueIceTrap((p_type - PURCHASE_ICEBUBBLE) + ICETRAP_BUBBLE);
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
	if (p_type != -1) {
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
		} else if (inShortList(p_type, &flag_purchase_types[0], sizeof(flag_purchase_types) >> 1)) {
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

Gfx* displayMoveText(Gfx* dl, actorData* actor) {
	move_overlay_paad* paad = actor->paad;
	gSPDisplayList(dl++, 0x01000118);
	gSPMatrix(dl++, 0x02000180, G_MTX_PUSH | G_MTX_LOAD | G_MTX_MODELVIEW);
	gDPPipeSync(dl++);
	gDPSetCombineLERP(dl++, 0, 0, 0, TEXEL0, TEXEL0, 0, PRIMITIVE, 0, 0, 0, 0, TEXEL0, TEXEL0, 0, PRIMITIVE, 0);
	gDPSetPrimColor(dl++, 0, 0, 0xFF, 0xFF, 0xFF, paad->opacity);
	if (paad->upper_text) {
		gSPMatrix(dl++, (int)&paad->matrix_0, G_MTX_PUSH | G_MTX_LOAD | G_MTX_MODELVIEW);
		dl = displayText(dl,1,0,0,paad->upper_text,0x80);
		gSPPopMatrix(dl++, G_MTX_MODELVIEW);
	}
	if (paad->lower_text) {
		gSPMatrix(dl++, (int)&paad->matrix_1, G_MTX_PUSH | G_MTX_LOAD | G_MTX_MODELVIEW);
		dl = displayText(dl,6,0,0,paad->lower_text,0x80);
		gSPPopMatrix(dl++, G_MTX_MODELVIEW);
	}
	return dl;
}

static char hint_displayed_text[20] = "";
static char* level_names[] = {
	"JAPES",
	"AZTEC",
	"FACTORY",
	"GALLEON",
	"FUNGI",
	"CAVES",
	"CASTLE",
};
static char* kong_names[] = {
	"DK",
	"DIDDY",
	"LANKY",
	"TINY",
	"CHUNKY",
};

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
	move_text_overlay_struct *used_overlay = &text_overlay_data[paad->index];
	if (shop_data) {
		has_data = 1;
		p_value = shop_data->purchase_value;
		p_type = shop_data->purchase_type;
		p_kong = shop_data->kong;
		p_flag = shop_data->flag;
	} else if (used_overlay->flag != 0) {
		has_data = 1;
		p_type = used_overlay->type;
		p_value = used_overlay->flag;
		p_kong = used_overlay->kong;
		p_string = used_overlay->string;
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
			used_overlay->kong = 0;
			used_overlay->flag = 0;
			used_overlay->type = 0;
			used_overlay->string = 0;
			used_overlay->used = 0;
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
			float position = start_y - (overlay_count * 100.0f); // Gap of 100.0f
			float move_x = 640.0f;
			_guTranslateF(&mtx1, move_x, position, 0.0f);
			_guMtxCatF(&mtx0, &mtx1, &mtx0);
			_guMtxF2L(&mtx0, &paad->matrix_0);
			_guTranslateF(&mtx1, 0.0f, 48.0f, 0.0f);
			_guMtxCatF(&mtx0, &mtx1, &mtx0);
			_guMtxF2L(&mtx0, &paad->matrix_1);
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
							if (p_flag == FLAG_ABILITY_CLIMBING) {
								top_item = ITEMTEXT_CLIMBING;
							} else if (isFlagInRange(p_flag, FLAG_BP_JAPES_DK_HAS, 40)) {
								// Blueprint
								int kong = (p_flag - FLAG_BP_JAPES_DK_HAS) % 5;
								top_item = ITEMTEXT_BLUEPRINT_DK + kong;
							} else if (isMedalFlag(p_flag)) {
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
							} else if (isFlagInRange(p_flag, FLAG_WRINKLYVIEWED, 35)) {
								// Hint
								top_item = ITEMTEXT_HINTITEM;
							} else if (p_flag == FLAG_COLLECTABLE_BEAN) {
								// Fungi Bean
								top_item = ITEMTEXT_BEAN;
							} else if (isFlagInRange(p_flag, FLAG_PEARL_0_COLLECTED, 5)) {
								// Galleon Pearls
								top_item = ITEMTEXT_PEARL;
							} else if (isFlagInRange(p_flag, FLAG_FAIRY_1, 20)) {
								// Banana Fairy
								top_item = ITEMTEXT_FAIRY;
							} else if (isIceTrapFlag(p_flag) == DYNFLAG_ICETRAP) {
								// Fake Item
								top_item = ITEMTEXT_FAKEITEM;
							} else if (isFlagInRange(p_flag, FLAG_ITEM_CRANKY, 4)) {
								top_item = ITEMTEXT_CRANKYITEM + (p_flag - FLAG_ITEM_CRANKY);
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
				case PURCHASE_ICEBUBBLE:
				case PURCHASE_ICEREVERSE:
				case PURCHASE_ICESLOW:
					top_item = ITEMTEXT_FAKEITEM;
					break;
				break;
			}
			if (override_string) {
				paad->upper_text = p_string;
			} else {
				if (top_item < 0) {
					paad->upper_text = (void*)0;
				} else {
					if (top_item == ITEMTEXT_HINTITEM) {
						int flag_offset = p_flag - FLAG_WRINKLYVIEWED;
						int level_index = flag_offset / 5;
						int kong_index = flag_offset % 5;
						if ((kong_index >= 0) && (kong_index < 5) && (level_index >= 0) && (level_index < 7)) {
							dk_strFormat(&hint_displayed_text, "%s %s HINT", level_names[level_index], kong_names[kong_index]);
							paad->upper_text = &hint_displayed_text;
						} else {
							paad->upper_text = getTextPointer(0x27,top_item,0);
						}
					} else {
						paad->upper_text = getTextPointer(0x27,top_item,0);
					}


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
				addDLToOverlay(&displayMoveText, CurrentActorPointer_0, 3);
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
	if (BFIMove_New.purchase_type != -1) {
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
				case PURCHASE_ICEBUBBLE:
				case PURCHASE_ICEREVERSE:
				case PURCHASE_ICESLOW:
					text_item_1 = 0x25 + 7;
					text_file = 8;
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