#include "../../include/common.h"

static short flag_purchase_types[] = {
	PURCHASE_FLAG,
	PURCHASE_GB,
	PURCHASE_ICEBUBBLE,
	PURCHASE_ICEREVERSE,
	PURCHASE_ICESLOW,
	PURCHASE_ARCHIPELAGO,
	PURCHASE_MEDAL,
	PURCHASE_CROWN,
	PURCHASE_RAINBOWCOIN,
	PURCHASE_FAIRY,
	PURCHASE_NINTENDOCOIN,
	PURCHASE_RAREWARECOIN,
	PURCHASE_BEAN,
	PURCHASE_PEARL,
	PURCHASE_HINT,
	PURCHASE_BLUEPRINT,
	PURCHASE_KEY,
	PURCHASE_KONG,
};

typedef enum KeySubtitleEnum {
	KEYSUB_K1,
	KEYSUB_K2,
	KEYSUB_K4,
	KEYSUB_K5,
	KEYSUB_K67,
	KEYSUB_K38,
} KeySubtitleEnum;

static char *key_subtitles[] = {
	"OPENS LEVEL 2",
	"OPENS LEVELS 3 AND 4",
	"OPENS LEVEL 5",
	"OPENS LEVELS 6 AND 7",
	"HELPS OPEN LEVEL 8",
	"HELPS OPEN K. ROOL",
};

static unsigned char key_subtitle_indexes[] = {
	KEYSUB_K1,
	KEYSUB_K2,
	KEYSUB_K38,
	KEYSUB_K4,
	KEYSUB_K5,
	KEYSUB_K67,
	KEYSUB_K67,
	KEYSUB_K38,
};

void moveTransplant(void) {
	int size = 126 * sizeof(purchase_struct);
	copyFromROM(0x1FEF800,&CrankyMoves_New[0][0].purchase_type,&size,0,0,0,0);
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
				int shop_flag = getShopFlag(shop_owner - 0xBD, world, Character);
				has_purchase = checkFlag(shop_flag, FLAGTYPE_PERMANENT) == 0;
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

helm_hurry_items getHelmHurryFromPurchase(int purchase_type, int flag) {
	switch (purchase_type) {
		case PURCHASE_MOVES:
		case PURCHASE_SLAM:
		case PURCHASE_GUN:
		case PURCHASE_AMMOBELT:
		case PURCHASE_INSTRUMENT:
			return HHITEM_MOVE;
		case PURCHASE_GB:
			return HHITEM_GB;
		case PURCHASE_FLAG:
			{
				int subtype = getMoveProgressiveFlagType(flag);
				if ((subtype >= 0) && (subtype <= 2)) {
					return HHITEM_MOVE;
				}
				if (flag == -2) {
					return HHITEM_MOVE;
				} else if (isTBarrelFlag(flag)) {
					return HHITEM_MOVE;
				} else if (flag == FLAG_ABILITY_CAMERA) {
					return HHITEM_MOVE;
				} else if (flag == FLAG_ABILITY_SHOCKWAVE) {
					return HHITEM_MOVE;
				}
			}
			break;
		case PURCHASE_BLUEPRINT:
			return HHITEM_BLUEPRINT;
		// case PURCHASE_HINT:
		// 	return HHITEM_NOTHING;
		case PURCHASE_MEDAL:
			return HHITEM_MEDAL;
		case PURCHASE_NINTENDOCOIN:
		case PURCHASE_RAREWARECOIN:
			return HHITEM_COMPANYCOIN;
		case PURCHASE_CROWN:
			return HHITEM_CROWN;
		case PURCHASE_BEAN:
			return HHITEM_BEAN;
		case PURCHASE_PEARL:
			return HHITEM_PEARL;
		case PURCHASE_FAIRY:
			return HHITEM_FAIRY;
		case PURCHASE_ICEBUBBLE:
		case PURCHASE_ICEREVERSE:
		case PURCHASE_ICESLOW:
			return HHITEM_FAKEITEM;
		case PURCHASE_KEY:
			return HHITEM_KEY;
	}
	return HHITEM_NOTHING;
}

void addHelmHurryPurchaseTime(int purchase_type, int flag) {
	helm_hurry_items hh_item = getHelmHurryFromPurchase(purchase_type, flag);
	if (hh_item != HHITEM_NOTHING) {
		addHelmTime(hh_item, 1);
	}
}

void giveItemFromShop(int p_type, int p_kong, int p_value, int flag) {
	unsigned char *base;
	switch(p_type) {
		case PURCHASE_MOVES:
			MovesBase[p_kong].special_moves |= (1 << p_value);
			break;
		case PURCHASE_SLAM:
		case PURCHASE_AMMOBELT:
			for (int i = 0; i < 5; i++) {
				base = &MovesBase[i];
				base[p_type]++;
			}
			break;
		case PURCHASE_GUN:
		case PURCHASE_INSTRUMENT:
			if (p_value == 1) {
				base = &MovesBase[p_kong];
				base[p_type] |= (1 << p_value);
			} else {
				for (int i = 0; i < 5; i++) {
					base = &MovesBase[i];
					base[p_type]++;
				}
			}
			break;
		case PURCHASE_GB:
			giveGB();
		case PURCHASE_FLAG:
			if (flag == -2) {
				setFlagMove(FLAG_ABILITY_CAMERA);
				setFlagMove(FLAG_ABILITY_SHOCKWAVE);
				if (CollectableBase.Film < 10) {
					CollectableBase.Film = 10;
				}
				if (CollectableBase.Crystals < (10*150)) {
					CollectableBase.Crystals = 10*150;
				}
			} else {
				setFlagMove(flag);
				if (flag == FLAG_ABILITY_CAMERA) {
                    if (CollectableBase.Film < 10) {
						CollectableBase.Film = 10;
					}
                } else if (flag == FLAG_ABILITY_SHOCKWAVE) {
                    if (CollectableBase.Crystals < (10*150)) {
						CollectableBase.Crystals = 10*150;
					}
                }
			}
			break;
		case PURCHASE_ICEBUBBLE:
		case PURCHASE_ICEREVERSE:
		case PURCHASE_ICESLOW:
			giveItem(REQITEM_ICETRAP, 0, 0);
			queueIceTrap((p_type - PURCHASE_ICEBUBBLE) + ICETRAP_BUBBLE);
			break;
		case PURCHASE_MEDAL:
			giveItem(REQITEM_MEDAL, 0, 0);
			break;
		case PURCHASE_CROWN:
			giveItem(REQITEM_CROWN, 0, 0);
			break;
		case PURCHASE_RAINBOWCOIN:
			giveItem(REQITEM_RAINBOWCOIN, 0, 0);
            for (int i = 0; i < 5; i++) {
				MovesBase[i].coins += 5;
			}
			break;
		case PURCHASE_FAIRY:
			giveItem(REQITEM_FAIRY, 0, 0);
			break;
		case PURCHASE_NINTENDOCOIN:
			giveItem(REQITEM_COMPANYCOIN, 0, 0);
			break;
		case PURCHASE_RAREWARECOIN:
			giveItem(REQITEM_COMPANYCOIN, 0, 1);
			break;
		case PURCHASE_BEAN:
			giveItem(REQITEM_BEAN, 0, 0);
			break;
		case PURCHASE_PEARL:
			giveItem(REQITEM_PEARL, 0, 0);
			break;
		case PURCHASE_HINT:
			giveItem(REQITEM_HINT, p_value / 5, p_value % 5);
			break;
		case PURCHASE_BLUEPRINT:
			giveItem(REQITEM_BLUEPRINT, p_value / 5, p_value % 5);
			break;
		case PURCHASE_KEY:
			giveItem(REQITEM_KEY, p_value, 0);
			break;
		case PURCHASE_KONG:
			giveItem(REQITEM_KONG, 0, p_value);
			break;
		break;
	}
	if (p_type == PURCHASE_INSTRUMENT) {
		int melon_cap = MelonArray[p_value];
		if (CollectableBase.Melons < melon_cap) {
			CollectableBase.Melons = melon_cap;
			refillHealth(0);
			SwapObject->unk_2e2 |= 0x11;
		}
	}
}

void purchaseMove(shop_paad* paad) {
	int item_given = -1;
	int crystals_unlocked = crystalsUnlocked(paad->kong);
	int p_type = paad->purchase_type;
	int bitfield_index = paad->purchase_value;
	int p_kong = paad->kong;
	giveItemFromShop(paad->purchase_type, paad->kong, paad->purchase_value, paad->flag);
	int world = getWorld(CurrentMap, 0);
	int shop_flag = getShopFlag(CurrentActorPointer_0->actorType - 0xBD, world, Character);
	setPermFlag(shop_flag);
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
		setPermFlag(0x180);
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
		giveItemFromShop(purchase_data->purchase_type, purchase_data->move_kong, purchase_data->purchase_value, purchase_data->purchase_value);
		addHelmHurryPurchaseTime(p_type, purchase_data->purchase_value);
	}
}

static short flag_location_series[] = {
	FLAG_TBARREL_DIVE,
	FLAG_TBARREL_ORANGE,
	FLAG_TBARREL_BARREL,
	FLAG_TBARREL_VINE,
	FLAG_ABILITY_SHOCKWAVE,
	FLAG_ABILITY_SIMSLAM,
};

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
	setPermFlag(flag_location_series[location_index]);
}

int getLocationStatus(location_list location_index) {
	return checkFlag(flag_location_series[location_index], FLAGTYPE_PERMANENT);
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
	char* p_subtitle = 0;
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
		p_subtitle = used_overlay->subtitle;
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
	int override_string = isAPEnabled() && p_type == PURCHASE_ARCHIPELAGO;
	if ((has_data) || (paad->upper_text) || (paad->lower_text)) {
		if ((CurrentActorPointer_0->obj_props_bitfield & 0x10) == 0) {
			used_overlay->kong = 0;
			used_overlay->flag = 0;
			used_overlay->type = 0;
			used_overlay->string = 0;
			used_overlay->subtitle = 0;
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
			paad->fade_in = 120;
			paad->fade_out = 30;
			paad->fade_rate = 0x10;
			paad->timer = 130;
			if ((CurrentMap == MAP_CRANKY) && (!is_jetpac)) {
				paad->timer = 300;
			}
			if (p_type == PURCHASE_ARCHIPELAGO) {
				if (APData) {
					paad->timer = APData->text_timer;
					paad->fade_in = paad->timer - 2;
					if (paad->timer < 70) {
						paad->fade_out = (paad->timer - 30) / 2;
						if (paad->fade_out < 5) {
							paad->fade_rate = 0xFF;
						} else {
							paad->fade_rate = 0x100 / (paad->fade_out - 4);
						}
					}
				}
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
								if ((top_item == -1) && (!isFlagAPItem(p_flag))) {
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
				if (p_subtitle) {
					paad->lower_text = p_subtitle;
				} else {
					paad->lower_text = 0;
				}
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
				if (bottom_item < 0) {
					paad->lower_text = (void*)0;
					if ((top_item >= ITEMTEXT_KEY1) && (top_item <= ITEMTEXT_KEY8)) {
						paad->lower_text = key_subtitles[key_subtitle_indexes[top_item - ITEMTEXT_KEY1]];
					}
				} else {
					paad->lower_text = getTextPointer(0x27,bottom_item,0);
				}
			}
			priceTransplant();
		}
		int timer = paad->timer;
		paad->timer = timer - 1;
		if ((timer > 0) && (paad->timer == 0)) {
			start_hiding = 1;
		}
		timer = paad->timer;
		if (timer == paad->fade_out) {
			CurrentActorPointer_0->control_state = 2;
		} else if (timer == paad->fade_in) {
			CurrentActorPointer_0->control_state = 1;
		}
		if (CurrentActorPointer_0->control_state == 1) {
			int opacity = paad->opacity;
			opacity += paad->fade_rate;
			if (opacity > 0xFF) {
				opacity = 0xFF;
			}
			paad->opacity = opacity;
		} else if (CurrentActorPointer_0->control_state == 2) {
			int opacity = paad->opacity;
			opacity -= paad->fade_rate;
			if (opacity < 0) {
				opacity = 0;
			}
			paad->opacity = opacity;
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