#include "../../include/common.h"

typedef enum KeySubtitleEnum {
	KEYSUB_K1,
	KEYSUB_K2,
	KEYSUB_K4,
	KEYSUB_K5,
	KEYSUB_K67,
	KEYSUB_K38,
} KeySubtitleEnum;

ROM_RODATA_PTR static const char *key_subtitles[] = {
	"OPENS LEVEL 2",
	"OPENS LEVELS 3 & 4",
	"OPENS LEVEL 5",
	"OPENS LEVELS 6 & 7",
	"HELPS OPEN LEVEL 8",
	"HELPS OPEN K. ROOL",
};

ROM_RODATA_NUM static const unsigned char key_subtitle_indexes[] = {
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
				return Rando.slam_prices[(int)MovesBase[0].simian_slam];
			case 7:
				return Rando.ammo_belt_prices[(int)MovesBase[0].ammo_belt];
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
	if (has_entered_level) {
		purchase_struct* selected = getShopData(shop_owner - 0xBD, Character, world);
		if (selected) {
			item_packet *item_data = &selected->item;
			has_purchase = isShopEmpty(shop_owner - 0xBD, world, Character) == 0;
			if (has_purchase) {
				paad->item_type = item_data->item_type;
				paad->item_level = item_data->level;
				paad->kong = item_data->kong;
				int p_price = getPrice(selected);
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

ROM_RODATA_NUM static const short flag_location_series[] = {
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

ROM_DATA static char hint_displayed_text[20] = "";
ROM_RODATA_PTR static const char* level_names[] = {
	"JAPES",
	"AZTEC",
	"FACTORY",
	"GALLEON",
	"FUNGI",
	"CAVES",
	"CASTLE",
};
ROM_RODATA_PTR static const char* kong_names[] = {
	"DK",
	"DIDDY",
	"LANKY",
	"TINY",
	"CHUNKY",
};

typedef struct text_match_struct {
	unsigned char req_item;
	char kong;
	char level;
	unsigned char text_item;
} text_match_struct;

ROM_RODATA_NUM static const text_match_struct TextMatchInfo[] = {
	{.req_item = REQITEM_MOVE, .level = 10, .kong = 0, .text_item = ITEMTEXT_DIVE},
	{.req_item = REQITEM_MOVE, .level = 10, .kong = 1, .text_item = ITEMTEXT_ORANGE},
	{.req_item = REQITEM_MOVE, .level = 10, .kong = 2, .text_item = ITEMTEXT_BARREL},
	{.req_item = REQITEM_MOVE, .level = 10, .kong = 3, .text_item = ITEMTEXT_VINE},
	{.req_item = REQITEM_MOVE, .level = 11, .kong = -1, .text_item = ITEMTEXT_CLIMBING},
	{.req_item = REQITEM_MOVE, .level = 12, .kong = -1, .text_item = ITEMTEXT_CAMERACOMBO},
	{.req_item = REQITEM_MOVE, .level = 13, .kong = -1, .text_item = ITEMTEXT_CANNONS},
	{.req_item = REQITEM_GOLDENBANANA, .level = -1, .kong = -1, .text_item = ITEMTEXT_BANANA},
	{.req_item = REQITEM_BLUEPRINT, .level = -1, .kong = 0, .text_item = ITEMTEXT_BLUEPRINT_DK},
	{.req_item = REQITEM_BLUEPRINT, .level = -1, .kong = 1, .text_item = ITEMTEXT_BLUEPRINT_DIDDY},
	{.req_item = REQITEM_BLUEPRINT, .level = -1, .kong = 2, .text_item = ITEMTEXT_BLUEPRINT_LANKY},
	{.req_item = REQITEM_BLUEPRINT, .level = -1, .kong = 3, .text_item = ITEMTEXT_BLUEPRINT_TINY},
	{.req_item = REQITEM_BLUEPRINT, .level = -1, .kong = 4, .text_item = ITEMTEXT_BLUEPRINT_CHUNKY},
	{.req_item = REQITEM_MEDAL, .level = -1, .kong = -1, .text_item = ITEMTEXT_MEDAL},
	{.req_item = REQITEM_COMPANYCOIN, .level = -1, .kong = 0, .text_item = ITEMTEXT_NINTENDO},
	{.req_item = REQITEM_COMPANYCOIN, .level = -1, .kong = 1, .text_item = ITEMTEXT_RAREWARE},
	{.req_item = REQITEM_CROWN, .level = -1, .kong = -1, .text_item = ITEMTEXT_CROWN},
	{.req_item = REQITEM_HINT, .level = -1, .kong = -1, .text_item = ITEMTEXT_HINTITEM},
	{.req_item = REQITEM_BEAN, .level = -1, .kong = -1, .text_item = ITEMTEXT_BEAN},
	{.req_item = REQITEM_PEARL, .level = -1, .kong = -1, .text_item = ITEMTEXT_PEARL},
	{.req_item = REQITEM_FAIRY, .level = -1, .kong = -1, .text_item = ITEMTEXT_FAIRY},
	{.req_item = REQITEM_ICETRAP, .level = -1, .kong = -1, .text_item = ITEMTEXT_FAKEITEM},
	{.req_item = REQITEM_SHOPKEEPER, .level = -1, .kong = 0, .text_item = ITEMTEXT_CRANKYITEM},
	{.req_item = REQITEM_SHOPKEEPER, .level = -1, .kong = 1, .text_item = ITEMTEXT_FUNKYITEM},
	{.req_item = REQITEM_SHOPKEEPER, .level = -1, .kong = 2, .text_item = ITEMTEXT_CANDYITEM},
	{.req_item = REQITEM_SHOPKEEPER, .level = -1, .kong = 3, .text_item = ITEMTEXT_SNIDEITEM},
	{.req_item = REQITEM_KONG, .level = -1, .kong = 0, .text_item = ITEMTEXT_KONG_DK},
	{.req_item = REQITEM_KONG, .level = -1, .kong = 1, .text_item = ITEMTEXT_KONG_DIDDY},
	{.req_item = REQITEM_KONG, .level = -1, .kong = 2, .text_item = ITEMTEXT_KONG_LANKY},
	{.req_item = REQITEM_KONG, .level = -1, .kong = 3, .text_item = ITEMTEXT_KONG_TINY},
	{.req_item = REQITEM_KONG, .level = -1, .kong = 4, .text_item = ITEMTEXT_KONG_CHUNKY},
	{.req_item = REQITEM_RAINBOWCOIN, .level = -1, .kong = -1, .text_item = ITEMTEXT_RAINBOWCOIN},
	{.req_item = REQITEM_FUNGITIME, .level = -1, .kong = 0, .text_item = ITEMTEXT_DAY},
	{.req_item = REQITEM_FUNGITIME, .level = -1, .kong = 1, .text_item = ITEMTEXT_NIGHT},
};

char *getTextFromTextEntry(int entry) {
	return getTextPointer(0x27, entry, 0);
}

void getTextForMove(char **top, char **bottom, int purchase_type, int purchase_value, int purchase_kong) {
	*top = NULL;
	*bottom = NULL;
	for (unsigned int di = 0; di < sizeof(TextMatchInfo) / sizeof(text_match_struct); di++) {
		const text_match_struct *tm_data = &TextMatchInfo[di];
		if (tm_data->req_item == purchase_type) {
			if ((tm_data->level == -1) || (tm_data->level == purchase_value)) {
				if ((tm_data->kong == -1) || (tm_data->kong == purchase_kong)) {
					if (tm_data->text_item == ITEMTEXT_HINTITEM) {
						dk_strFormat((char*)&hint_displayed_text, "%s %s HINT", level_names[purchase_value], kong_names[purchase_kong]); // TODO: Make this not reference a static addr
						*top = &hint_displayed_text[0];
						return;
					}
					*top = getTextFromTextEntry(tm_data->text_item);
					return;
				}
			}
		}
	}
	if (purchase_type == REQITEM_MOVE) {
		switch (purchase_value) {
			case 0:
			case 1:
			case 2:
				{
					int move_index = (purchase_kong * 4) + purchase_value + 1;
					*top = getTextFromTextEntry(SpecialMovesNames[move_index].name);
					*bottom = getTextFromTextEntry(SpecialMovesNames[move_index].latin);
				}
				break;
			case 3:
				{
					int slam_level = MovesBase[0].simian_slam;
					*top = getTextFromTextEntry(SimianSlamNames[slam_level].name);
					*bottom = getTextFromTextEntry(SimianSlamNames[slam_level].latin);
				}
				break;
			case 4:
				*top = getTextFromTextEntry(GunNames[purchase_kong]);
				break;
			case 5:
			case 6:
				*top = getTextFromTextEntry(GunUpgNames[purchase_value - 3]);
				break;
			case 7:
				{
					int belt_level = MovesBase[0].ammo_belt;
					*top = getTextFromTextEntry(AmmoBeltNames[belt_level]);
				}
				break;
			case 8:
				*top = getTextFromTextEntry(InstrumentNames[purchase_kong]);
				break;
			case 9:
				{
					int lvl = getInstrumentLevel();
					*top = getTextFromTextEntry(InstrumentUpgNames[lvl + 1]);
				}
				break;
		}
		return;
	}
	if (purchase_type == REQITEM_KEY) {
		*top = getTextFromTextEntry(ITEMTEXT_KEY1 + purchase_value);
		*bottom = (char*)key_subtitles[key_subtitle_indexes[purchase_value]];
	}
}

void getNextMoveText(void) {
	move_overlay_paad* paad = CurrentActorPointer_0->paad;
	int overlay_count = 0;
	if ((CurrentActorPointer_0->obj_props_bitfield & 0x10) == 0) {
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
		mtx_item mtx0;
		mtx_item mtx1;
		_guScaleF(&mtx0, 0x3F19999A, 0x3F19999A, 0x3F800000);
		int position = 800 - (overlay_count * 100); // Gap of 100
		_guTranslateF(&mtx1, 640.0f, position, 0.0f);
		_guMtxCatF(&mtx0, &mtx1, &mtx0);
		_guMtxF2L(&mtx0, &paad->matrix_0);
		_guTranslateF(&mtx1, 0.0f, 48.0f, 0.0f);
		_guMtxCatF(&mtx0, &mtx1, &mtx0);
		_guMtxF2L(&mtx0, &paad->matrix_1);
	}
	paad->timer--;
	if (paad->timer == 0) {
		if (paad->upper_text) {
			complex_free(paad->upper_text);
		}
		if (paad->lower_text) {
			complex_free(paad->lower_text);
		}
		deleteActorContainer(CurrentActorPointer_0);
		return;
	}
	if (paad->timer == paad->fade_out) {
		CurrentActorPointer_0->control_state = 2;
	} else if (paad->timer == paad->fade_in) {
		CurrentActorPointer_0->control_state = 1;
	}
	int opacity = paad->opacity;
	if (CurrentActorPointer_0->control_state == 1) {
		opacity += paad->fade_rate;
		if (opacity > 0xFF) {
			opacity = 0xFF;
		}
		paad->opacity = opacity;
	} else if (CurrentActorPointer_0->control_state == 2) {
		opacity -= paad->fade_rate;
		if (opacity < 0) {
			opacity = 0;
		}
		paad->opacity = opacity;
	}
	if (CurrentActorPointer_0->control_state != 0) {
		addDLToOverlay(&displayMoveText, CurrentActorPointer_0, 3);
	}
	if (CurrentActorPointer_0->actorType == 0x140) {
		renderActor(CurrentActorPointer_0,0);
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

ROM_RODATA_NUM static const unsigned char Explanation_Special[] = {
	0x00, 0x0B, 0x0F, 0x14, // DK
	0x00, 0x0C, 0x10, 0x15, // Diddy
	0x00, 0x0E, 0x13, 0x16, // Lanky
	0x00, 0x0D, 0x11, 0x17, // Tiny
	0x00, 0x0D, 0x12, 0x18, // Chunky - Is Item 2 a bug?
};

ROM_RODATA_NUM static const unsigned char Explanation_Slam[] = {0x0, 0x19, 0x1A, 0x1B};
ROM_RODATA_NUM static const unsigned char Explanation_Gun[] = {0x0, 0x12, 0x13, 0x14};

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