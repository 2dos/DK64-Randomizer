#include "../../include/common.h"

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
	"OPENS LEVELS 3 & 4",
	"OPENS LEVEL 5",
	"OPENS LEVELS 6 & 7",
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
	copyFromROM(0x1FEF000,&CrankyMoves_New[0][0],&size,0,0,0,0);
}

int isShopEmpty(vendors vendor, int level, int kong) {
	int flag = getShopFlag(vendor, level, kong);
	if (checkFlag(flag, FLAGTYPE_PERMANENT)) {
		return 1;
	}
	purchase_struct *shop_data = getShopData(vendor, kong, level);
	if (shop_data->item.item_type == REQITEM_NONE) {
		return 1;
	}
	return 0;
}

int getInstrumentLevel(void) {
	int val = MovesBase[0].instrument_bitfield;
	if (val & 8) {
		return 3;
	} else if (val & 4) {
		return 2;
	} else if (val & 2) {
		return 1;
	}
	return 0;
}

int getPrice(purchase_struct *shop_data) {
	if (shop_data->item.item_type == REQITEM_MOVE) {
		switch (shop_data->item.level) {
			case 3:
				if (MovesBase[0].simian_slam > 0) {
					return Rando.slam_prices[MovesBase[0].simian_slam - 1]; // Indexing error
				}
			case 7:
				return Rando.ammo_belt_prices[MovesBase[0].ammo_belt];
			case 9:
				{
					int level = getInstrumentLevel();
					return Rando.instrument_upgrade_prices[level];
				}
		}
	}
	return shop_data->price;
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
			item_packet *item_data = &selected->item;
			has_purchase = isShopEmpty(shop_owner - 0xBD, world, Character) == 0;
			if (has_purchase) {
				paad->item_type = item_data->item_type;
				paad->item_level = item_data->level;
				paad->kong = item_data->kong;
				int p_price = selected->price;
				textParameter = p_price;
				paad->price = p_price;
			}
		}
	}
	if (!has_purchase) {
		paad->price = 0;
		textParameter = 0;
		paad->item_type = -1;
		if (latest_level_entered > 6) {
			paad->item_type = -2;
		}
		paad->kong = Character;
	}
	paad->melons = CollectableBase.Melons;
}

void purchaseMove(shop_paad* paad) {
	int item_given = -1;
	int crystals_unlocked = crystalsUnlocked(paad->kong);
	int p_kong = paad->kong;
	giveItem(paad->item_type, paad->item_level, paad->kong, (giveItemConfig){.display_item_text = 0, .apply_helm_hurry = 1, .apply_ice_trap = 1});
	vendors vendor = CurrentActorPointer_0->actorType - 0xBD;
	int world = getWorld(CurrentMap, 0);
	int shop_flag_dk = getShopFlag(vendor, world, KONG_DK);
	if (isSharedMove(vendor, world)) {
		for (int i = 0; i < 5; i++) {
			setPermFlag(shop_flag_dk + i);
		}
	} else {
		setPermFlag(shop_flag_dk + Character);
	}
	if (paad->item_type == REQITEM_MOVE) {
		int item_level = paad->item_level;
		if (item_level < 4) {
			// Special Move / Slam
			if ((!crystals_unlocked) && (crystalsUnlocked(paad->kong))) {
				item_given = 5;
			}
		} else if (item_level < 8) {
			// Guns/homing/sniper/belt
			item_given = 2;
		} else if (item_level < 10) {
			// Instruments/upgrades
			item_given = 7;
		}
	}

	if ((!Rando.shops_dont_cost) && (!isAPEnabled())) {
			changeCollectableCount(1, 0, (0 - paad->price));
	}
	if (item_given > -1) {
		changeCollectableCount(item_given, 0, 9999);
	}
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
	if (FirstMove_New.item.item_type) {
		setPermFlag(0x180);
		return 1; // First move is nothing
	}
	return 0;
}

void purchaseFirstMoveHandler(shop_paad* paad) {
	paad->item_type = FirstMove_New.item.item_type;
	if (paad->item_type == -1) {
		CurrentActorPointer_0->control_state = 3;
		return;
	}
	paad->item_level = FirstMove_New.item.level;
	paad->kong = FirstMove_New.item.kong;
	paad->price = 0;
	purchaseMove(paad);
}

void setLocation(purchase_struct* purchase_data, int force_text) {
	if (purchase_data->item.item_type) {
		giveItemFromPacket(&purchase_data->item, force_text);
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
		setLocation(&TrainingMoves_New[location_int], 0);
	} else if (location_index == LOCATION_BFI) {
		// BFI
		setLocation(&BFIMove_New, 1);
	} else if (location_index == LOCATION_FIRSTMOVE) {
		// First Move (Normally Slam 1)
		setLocation(&FirstMove_New, 0);
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
	int is_jetpac = CurrentActorPointer_0->actorType == NEWACTOR_JETPACITEMOVERLAY;
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
	char* p_string = 0;
	char* p_subtitle = 0;
	int has_data = 0;
	move_text_overlay_struct *used_overlay = &text_overlay_data[paad->index];
	if (shop_data) {
		has_data = 1;
		p_value = shop_data->item_level;
		p_type = shop_data->item_type;
		p_kong = shop_data->kong;
	} else {
		has_data = 1;
		p_type = used_overlay->type;
		p_value = used_overlay->level;
		p_kong = used_overlay->kong;
		p_string = used_overlay->string;
		p_subtitle = used_overlay->subtitle;
	}
	int override_string = isAPEnabled() && p_type == REQITEM_AP;
	if ((has_data) || (paad->upper_text) || (paad->lower_text)) {
		if ((CurrentActorPointer_0->obj_props_bitfield & 0x10) == 0) {
			used_overlay->kong = 0;
			used_overlay->level = 0;
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
			if (p_type == REQITEM_AP) {
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
				case REQITEM_MOVE:
					switch (p_value) {
						case 0:
						case 1:
						case 2:
							{
								int move_index = (p_kong * 4) + p_value + 1;
								top_item = SpecialMovesNames[move_index].name;
								bottom_item = SpecialMovesNames[move_index].latin;
							}
							break;
						case 3:
							{
								int slam_level = MovesBase[0].simian_slam;
								top_item = SimianSlamNames[slam_level].name;
								bottom_item = SimianSlamNames[slam_level].latin;
							}
							break;
						case 4:
							top_item = GunNames[p_kong];
							break;
						case 5:
						case 6:
							top_item = GunUpgNames[p_value - 3];
							break;
						case 7:
							{
								int belt_level = MovesBase[0].ammo_belt;
								top_item = AmmoBeltNames[belt_level];
							}
							break;
						case 8:
							top_item = InstrumentNames[p_kong];
							break;
						case 9:
							{
								int lvl = getInstrumentLevel();
								top_item = InstrumentUpgNames[lvl + 1];
							}
							break;
						case 10:
							top_item = ITEMTEXT_DIVE + p_kong;
							break;
						case 11:
							top_item = ITEMTEXT_CLIMBING;
							break;
						case 12:
							top_item = ITEMTEXT_CAMERACOMBO;
							break;
					}
					break;
				case REQITEM_GOLDENBANANA:
					top_item = ITEMTEXT_BANANA;
					break;
				case REQITEM_BLUEPRINT:
					top_item = ITEMTEXT_BLUEPRINT_DK + p_kong;
					break;
				case REQITEM_MEDAL:
					top_item = ITEMTEXT_MEDAL;
					break;
				case REQITEM_COMPANYCOIN:
					top_item = ITEMTEXT_NINTENDO + p_kong;
					break;
				case REQITEM_CROWN:
					top_item = ITEMTEXT_CROWN;
					break;
				case REQITEM_HINT:
					top_item = ITEMTEXT_HINTITEM;
					break;
				case REQITEM_BEAN:
					top_item = ITEMTEXT_BEAN;
					break;
				case REQITEM_PEARL:
					top_item = ITEMTEXT_PEARL;
					break;
				case REQITEM_FAIRY:
					top_item = ITEMTEXT_FAIRY;
					break;
				case REQITEM_ICETRAP:
					top_item = ITEMTEXT_FAKEITEM;
					break;
				case REQITEM_SHOPKEEPER:
					top_item = ITEMTEXT_CRANKYITEM + p_kong;
					break;
				case REQITEM_KEY:
					top_item = ITEMTEXT_KEY1 + p_value;
					break;
				case REQITEM_KONG:
					top_item = ITEMTEXT_KONG_DK + p_kong;
					break;
				case REQITEM_RAINBOWCOIN:
					top_item = ITEMTEXT_RAINBOWCOIN;
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
						if ((p_kong >= 0) && (p_kong < 5) && (p_value >= 0) && (p_value < 7)) {
							dk_strFormat(&hint_displayed_text, "%s %s HINT", level_names[p_value], kong_names[p_kong]);
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
		}
		int timer = paad->timer;
		paad->timer = timer - 1;
		if (timer == 1) {
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
	if ((BFIMove_New.item.item_type == REQITEM_MOVE) && (BFIMove_New.item.level == 10) && (BFIMove_New.item.kong == 4)) {
		// Camera
		displayItemOnHUD(6,0,0);
	}
	if (BFIMove_New.item.item_type != REQITEM_NONE) {
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
			if (paad->item_type == REQITEM_MOVE) {
				switch (paad->item_level) {
					case 0:
					case 1:
					case 2:
						text_item_1 = Explanation_Special[(paad->kong * 4) + paad->item_level + 1];
						text_file = 8;
						break;
					case 3:
						text_item_1 = Explanation_Slam[paad->item_level];
						text_file = 8;
						break;
					case 4:
					case 5:
					case 6:
						text_item_1 = Explanation_Gun[paad->item_level - 3];
						text_file = 7;
						break;
					case 7:
						textParameter = getRefillCount(2,0);
						text_item_1 = 0x15;
						text_file = 7;
						break;
					case 8:
						text_item_1 = 0x12;
						if (!doAllKongsHaveMove(paad,1)) {
							text_item_0 = 0x15;
						}
						text_file = 9;
						break;
					case 9:
						text_item_1 = 0x13;
						text_file = 9;
						if ((paad->melons + 1) == CollectableBase.Melons) {
							text_item_1 = 0x14;
						} else {
							text_file = 9;
						}
						break;
					case 10:
						text_item_1 = 0x25 + paad->kong;
						text_file = 8;
						break;
					// NOTE TO SELF
					// WAS FINISHING UP THIS SWITCH CASE
				}
			} else {
				text_item_1 = 0x25 + 7;
				text_file = 8;
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