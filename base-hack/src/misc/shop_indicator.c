#include "../../include/common.h"

static short flag_purchase_types[] = {
	PURCHASE_FLAG,
	PURCHASE_GB,
	PURCHASE_ICEBUBBLE,
	PURCHASE_ICEREVERSE,
	PURCHASE_ICESLOW,
};

int doesKongPossessMove(int purchase_type, int purchase_value, int kong) {
	if (kong > 4) {
		kong = 0;
	}
	if (purchase_type != -1) {
		if (purchase_value != 0) {
			if (purchase_type == PURCHASE_MOVES) {
				if (MovesBase[kong].special_moves & (1 << (purchase_value - 1))) {
					return 0;
				} else {
					return 1;
				}
			} else if (purchase_type == PURCHASE_SLAM) {
				if (MovesBase[kong].simian_slam >= purchase_value) {
					return 0;
				} else {
					return 2;
				}
			} else if (purchase_type == PURCHASE_GUN) {
				if (MovesBase[kong].weapon_bitfield & (1 << (purchase_value - 1))) {
					return 0;
				} else {
					if (purchase_value == 1) {
						return 1;
					} else {
						return 3;
					}
				}
			} else if (purchase_type == PURCHASE_AMMOBELT) {
				if (MovesBase[kong].ammo_belt >= purchase_value) {
					return 0;
				} else {
					return 4;
				}
			} else if (purchase_type == PURCHASE_INSTRUMENT) {
				if (MovesBase[kong].instrument_bitfield & (1 << (purchase_value - 1))) {
					return 0;
				} else {
					if (purchase_value == 1) {
						return 1;
					} else {
						return 5;
					}
				}
			} else if (inShortList(purchase_type, &flag_purchase_types[0], sizeof(flag_purchase_types) >> 1)) {
				if (purchase_value == -2) { // Shockwave & Camera Combo
					if ((!checkFlagDuplicate(FLAG_ABILITY_CAMERA, FLAGTYPE_PERMANENT)) || (!checkFlagDuplicate(FLAG_ABILITY_SHOCKWAVE, FLAGTYPE_PERMANENT))) {
						return 6;
					}
				} else {
					if (!checkFlagDuplicate(purchase_value, FLAGTYPE_PERMANENT)) {
						int is_shared = 0;
						int tied_flags[] = {FLAG_TBARREL_DIVE,FLAG_TBARREL_ORANGE,FLAG_TBARREL_BARREL,FLAG_TBARREL_VINE,FLAG_ABILITY_CLIMBING, FLAG_ABILITY_CAMERA,FLAG_ABILITY_SHOCKWAVE};
						for (int i = 0; i < (sizeof(tied_flags) / 4); i++) {
							if (purchase_value == tied_flags[i]) {
								is_shared = 1;
							}
						}
						if (getMoveProgressiveFlagType(purchase_value) > -1) {
							is_shared = 1;
						}
						if (is_shared) {
							return 6;
						}
						return 1;
					}
				}
			}
		}
	}
	return 0;
}

#define MOVEBTF_DK 1
#define MOVEBTF_DIDDY 2
#define MOVEBTF_LANKY 4
#define MOVEBTF_TINY 8
#define MOVEBTF_CHUNKY 0x10
#define MOVEBTF_SHARED 0x20

#define SHOPINDEX_CRANKY 0
#define SHOPINDEX_FUNKY 1
#define SHOPINDEX_CANDY 2

int isSharedMove(vendors shop_index, int level) {
	purchase_struct* targ = getShopData(shop_index, 0, level);
	if (!targ) {
		return 1;
	}
	for (int i = 1; i < 5; i++) {
		purchase_struct* src = getShopData(shop_index, i, level);
		if (src) {
			if (targ->move_kong != src->move_kong) {
				return 0;
			}
			if (targ->purchase_type != src->purchase_type) {
				return 0;
			}
			if (targ->purchase_value != src->purchase_value) {
				return 0;
			}
		}
	}
	return 1;
}

typedef struct counter_paad {
	/* 0x000 */ void* image_slots[3];
	/* 0x00C */ behaviour_data* linked_behaviour;
	/* 0x010 */ unsigned char kong_images[5];
	/* 0x015 */ unsigned char item_images[5];
	/* 0x016 */ unsigned char use_item_display;
	/* 0x017 */ unsigned char cap;
	/* 0x018 */ unsigned char current_slot;
	/* 0x019 */ unsigned char shop;
} counter_paad;

typedef enum counter_items {
	/* 0x000 */ COUNTER_NO_ITEM,
	/* 0x001 */ COUNTER_DK_FACE,
	/* 0x002 */ COUNTER_DIDDY_FACE,
	/* 0x003 */ COUNTER_LANKY_FACE,
	/* 0x004 */ COUNTER_TINY_FACE,
	/* 0x005 */ COUNTER_CHUNKY_FACE,
	/* 0x006 */ COUNTER_SHARED_FACE,
	/* 0x007 */ COUNTER_SOLDOUT,
	/* 0x008 */ COUNTER_GB,
	/* 0x009 */ COUNTER_BP,
	/* 0x00A */ COUNTER_CROWN,
	/* 0x00B */ COUNTER_KEY,
	/* 0x00C */ COUNTER_MEDAL,
	/* 0x00D */ COUNTER_POTION,
	/* 0x00E */ COUNTER_NINCOIN,
	/* 0x00F */ COUNTER_RWCOIN,
	/* 0x010 */ COUNTER_BEAN,
	/* 0x011 */ COUNTER_PEARL,
	/* 0x012 */ COUNTER_FAIRY,
	/* 0x013 */ COUNTER_RAINBOWCOIN,
	/* 0x014 */ COUNTER_FAKEITEM,
	/* 0x015 */ COUNTER_HINT,
	/* 0x016 */ COUNTER_DILLO1,
	/* 0x017 */ COUNTER_DOG1,
	/* 0x018 */ COUNTER_MJ,
	/* 0x019 */ COUNTER_PUFFTOSS,
	/* 0x01A */ COUNTER_DOG2,
	/* 0x01B */ COUNTER_DILLO2,
	/* 0x01C */ COUNTER_KKO,
} counter_items;

int getCounterItem(vendors shop_index, int kong, int level) {
	purchase_struct* data = getShopData(shop_index, kong, level);
	if (data) {
		switch(data->purchase_type) {
			case PURCHASE_MOVES:
			case PURCHASE_SLAM:
			case PURCHASE_GUN:
			case PURCHASE_AMMOBELT:
			case PURCHASE_INSTRUMENT:
				return COUNTER_POTION;
				break;
			case PURCHASE_FLAG:
				{
					int flag = data->purchase_value;
					if (isFlagInRange(flag, FLAG_BP_JAPES_DK_HAS, 40)) {
						return COUNTER_BP;
					} else if (isMedalFlag(flag)) {
						return COUNTER_MEDAL;
					} else if (isFlagInRange(flag, FLAG_CROWN_JAPES, 10)) {
						return COUNTER_CROWN;
					} else if (flag == FLAG_COLLECTABLE_NINTENDOCOIN) {
						return COUNTER_NINCOIN;
					} else if (flag == FLAG_COLLECTABLE_RAREWARECOIN) {
						return COUNTER_RWCOIN;
					} else if (flag == FLAG_COLLECTABLE_BEAN) {
						return COUNTER_BEAN;
					} else if (isFlagInRange(flag, FLAG_PEARL_0_COLLECTED, 5)) {
						return COUNTER_PEARL;
					} else if (isFlagInRange(flag, FLAG_FAIRY_1, 20)) {
						return COUNTER_FAIRY;
					} else if (isFlagInRange(flag, FLAG_WRINKLYVIEWED, 35)) {
						return COUNTER_HINT;
					} else if (isFlagInRange(flag, FLAG_RAINBOWCOIN_0, 16)) {
						return COUNTER_RAINBOWCOIN;
					} else if (isIceTrapFlag(flag) == DYNFLAG_ICETRAP) {
						return COUNTER_FAKEITEM;
					} else {
						if (isTBarrelFlag(flag)) {
							return COUNTER_POTION;
						}
						if (isFairyFlag(flag)) {
							return COUNTER_POTION;
						}
						if (flag == FLAG_ABILITY_CLIMBING) {
							return COUNTER_POTION;
						}
						int subtype = getMoveProgressiveFlagType(flag);
						if (subtype >= 0) {
							return COUNTER_POTION;
						}
						for (int i = 0; i < 8; i++) {
							if (flag == getKeyFlag(i)) {
								return COUNTER_KEY;
							}
						}
						for (int i = 0; i < 5; i++) {
							if (flag == getKongFlag(i)) {
								return COUNTER_DK_FACE + i;
							}
						}
					}
				}
				break;
			case PURCHASE_GB:
				return COUNTER_GB;
			case PURCHASE_ICEBUBBLE:
			case PURCHASE_ICEREVERSE:
			case PURCHASE_ICESLOW:
				return COUNTER_FAKEITEM;
			break;
		}
	}
	return COUNTER_NO_ITEM;
}

void getMoveCountInShop(counter_paad* paad, vendors shop_index) {
	int level = getWorld(CurrentMap,0);
	int possess = 0;
	int count = 0;
	int slot = 0;
	if (level < LEVEL_COUNT) {
		for (int i = 0; i < 5; i++) {
			purchase_struct* data = getShopData(shop_index, i, level);
			if (data) {
				possess = doesKongPossessMove(data->purchase_type, data->purchase_value, data->move_kong);
			}
			if ((possess == 1) && (isSharedMove(shop_index, level))) {
				possess = 7;
			}
			if (possess == 1) {
				paad->kong_images[slot] = i + 1;
				paad->item_images[slot] = getCounterItem(shop_index, i, level);
				slot += 1;
				count += 1;
			} else if (possess > 1) {
				paad->kong_images[0] = COUNTER_SHARED_FACE;
				paad->item_images[0] = getCounterItem(shop_index, i, level);
				paad->cap = 1;
				return;
			}
		}
	}
	paad->cap = count;
}

#define IMG_WIDTH 32

#define COUNTER_CACHE_SIZE 32
static void* texture_data[COUNTER_CACHE_SIZE] = {};
static unsigned char texture_load[COUNTER_CACHE_SIZE] = {};

void wipeCounterImageCache(void) {
	for (int i = 0; i < COUNTER_CACHE_SIZE; i++) {
		texture_data[i] = 0;
		texture_load[i] = 0;
	}
}

void* loadInternalTexture(int texture_start, int texture_offset) {
	if (texture_load[texture_offset] == 0) {
		texture_data[texture_offset] = getMapData(TABLE_TEXTURES, texture_start + texture_offset, 1, 1);
	}
	texture_load[texture_offset] = 3;
	return texture_data[texture_offset];
}

void* loadFontTexture_Counter(void* slot, int index, int slot_index) {
	void* texture = loadInternalTexture(196, index); // Load texture
	if (slot) {
		wipeTextureSlot(slot);
	}
	void* location = dk_malloc(IMG_WIDTH << 7);
	copyImage(location, texture, IMG_WIDTH);
	blink(CurrentActorPointer_0, slot_index, 0xFFFF);
	applyImageToActor(CurrentActorPointer_0, slot_index, 0);
	writeImageSlotToActor(CurrentActorPointer_0, slot_index, 0, location);
	return location;
}

void updateCounterDisplay(void) {
	counter_paad* paad = CurrentActorPointer_0->paad;
	int index = paad->current_slot;
	if (paad->cap > 0) {
		int kong_image = paad->kong_images[index];
		int item_image = paad->item_images[index];
		if ((kong_image < 0) || (kong_image > 0x15)) {
			kong_image = 0;
		}
		if ((item_image < 0) || (item_image > 0x15)) {
			item_image = 0;
		}
		if (paad->use_item_display) {
			paad->image_slots[0] = loadFontTexture_Counter(paad->image_slots[0], kong_image, 0);
			paad->image_slots[2] = loadFontTexture_Counter(paad->image_slots[2], item_image, 2);
		} else {
			paad->image_slots[1] = loadFontTexture_Counter(paad->image_slots[1], kong_image, 1);
		}
	}
}

unsigned int getActorModelTwoDist(ModelTwoData* _object) {
	int ax = CurrentActorPointer_0->xPos;
	int ay = CurrentActorPointer_0->yPos;
	int az = CurrentActorPointer_0->zPos;
	int mx = _object->xPos;
	int my = _object->yPos;
	int mz = _object->zPos;
	int dx = ax - mx;
	int dy = ay - my;
	int dz = az - mz;
	return (dx * dx) + (dy * dy) + (dz * dz);
}

int getClosestShop(void) {
	/*
		Cranky's: 0x73
		Funky's Hut: 0x7A
		Candy's Shop: 0x124
		Snide's HQ: 0x79
	*/
	unsigned int dists[4] = {0xFFFFFFFF,0xFFFFFFFF,0xFFFFFFFF,0xFFFFFFFF};
	int* m2location = (int*)ObjectModel2Pointer;
	int found_counter = 0;
	behaviour_data* behavs[4] = {};
	counter_paad* paad = CurrentActorPointer_0->paad;
	for (int i = 0; i < ObjectModel2Count; i++) {
		if (found_counter < 4) {
			ModelTwoData* _object = getObjectArrayAddr(m2location,0x90,i);
			if (_object->object_type == 0x73) {
				dists[0] = getActorModelTwoDist(_object);
				behavs[0] = _object->behaviour_pointer;
				found_counter += 1;
			} else if (_object->object_type == 0x7A) {
				dists[1] = getActorModelTwoDist(_object);
				behavs[1] = _object->behaviour_pointer;
				found_counter += 1;
			} else if (_object->object_type == 0x124) {
				dists[2] = getActorModelTwoDist(_object);
				behavs[2] = _object->behaviour_pointer;
				found_counter += 1;
			} else if (_object->object_type == 0x79) {
				dists[3] = getActorModelTwoDist(_object);
				behavs[3] = _object->behaviour_pointer;
				found_counter += 1;
			}
		}
	}
	int closest_index = 0;
	if ((dists[2] < dists[1]) && (dists[2] < dists[0]) && (dists[2] < dists[3])) {
		paad->linked_behaviour = behavs[2];
		closest_index = 2;
	} else if ((dists[3] < dists[1]) && (dists[3] < dists[0]) && (dists[3] < dists[2])) {
		paad->linked_behaviour = behavs[3];
		closest_index = 3;
	} else if ((dists[1] < dists[0]) && (dists[1] < dists[2]) && (dists[1] < dists[3])) {
		paad->linked_behaviour = behavs[1];
		closest_index = 1;
	} else if ((dists[0] < dists[1]) && (dists[0] < dists[2]) && (dists[0] < dists[3])) {
		paad->linked_behaviour = behavs[0];
		closest_index = 0;
	}
	if (found_counter > 0) {
		paad->linked_behaviour = behavs[closest_index];
	}
	return closest_index;
}

typedef struct ModelData {
	/* 0x000 */ float pos[3];
	/* 0x00C */ float scale;
} ModelData;

float getShopScale(int index) {
	int* m2location = (int*)ObjectModel2Pointer;
	for (int i = 0; i < ObjectModel2Count; i++) {
		ModelTwoData* _object = getObjectArrayAddr(m2location,0x90,i);
		if (_object) {
			if (index == 0) { // Crankys
				if (_object->object_type == 0x73) {
					ModelData* model = _object->model_pointer;
					if (model) {
						return model->scale;
					}
				}
			} else if (index == 1) { // Funkys
				if (_object->object_type == 0x7A) {
					ModelData* model = _object->model_pointer;
					if (model) {
						return model->scale;
					}
				}
			} else if (index == 2) { // Candys
				if (_object->object_type == 0x124) {
					ModelData* model = _object->model_pointer;
					if (model) {
						return model->scale;
					}
				}
			} else if (index == 3) { // Snide
				return 1.0f;
			}
		}
	}
	return 1.0f;
}

typedef struct krool_head {
	/* 0x000 */ unsigned char map;
	/* 0x001 */ unsigned char texture_offset;
} krool_head;

static const krool_head helm_heads[] = {
	{.map = MAP_JAPESDILLO, .texture_offset=COUNTER_DILLO1},
	{.map = MAP_AZTECDOGADON, .texture_offset=COUNTER_DOG1},
	{.map = MAP_FACTORYJACK, .texture_offset=COUNTER_MJ},
	{.map = MAP_GALLEONPUFFTOSS, .texture_offset=COUNTER_PUFFTOSS},
	{.map = MAP_FUNGIDOGADON, .texture_offset=COUNTER_DOG2},
	{.map = MAP_CAVESDILLO, .texture_offset=COUNTER_DILLO2},
	{.map = MAP_CASTLEKUTOUT, .texture_offset=COUNTER_KKO},
	{.map = MAP_KROOLDK, .texture_offset=COUNTER_DK_FACE},
	{.map = MAP_KROOLDIDDY, .texture_offset=COUNTER_DIDDY_FACE},
	{.map = MAP_KROOLLANKY, .texture_offset=COUNTER_LANKY_FACE},
	{.map = MAP_KROOLTINY, .texture_offset=COUNTER_TINY_FACE},
	{.map = MAP_KROOLCHUNKY, .texture_offset=COUNTER_CHUNKY_FACE},
	{.map = 0xFF, .texture_offset=COUNTER_NO_ITEM},
};

static const short float_ids[] = {0x1F4, 0x36};
static const short shop_obj_types[] = {0x73, 0x7A, 0x124};
static const float float_offsets[] = {51.0f, 51.0f, 45.0f};

void newCounterCode(void) {
	counter_paad* paad = CurrentActorPointer_0->paad;
	if ((CurrentActorPointer_0->obj_props_bitfield & 0x10) == 0) {
		// Init Code
		if (CurrentMap != MAP_HELM) {
			if (Rando.shop_indicator_on) {
				if (Rando.shop_indicator_on == 2) {
					paad->use_item_display = 1;
				} else {
					paad->use_item_display = 0;
				}
				// Initialize slots
				for (int i = 0; i < 3; i++) {
					paad->image_slots[i] = loadFontTexture_Counter(paad->image_slots[i], 0, i);
				}
				CurrentActorPointer_0->rot_z = 3072; // Facing vertical
				int closest_shop = getClosestShop();
				paad->shop = closest_shop;
				if (closest_shop == 3) { // Snide is closest
					deleteActorContainer(CurrentActorPointer_0);
				} else {
					getMoveCountInShop(paad, paad->shop);
					paad->current_slot = 0;
					updateCounterDisplay();
					if (paad->cap == 0) {
						paad->kong_images[0] = COUNTER_SOLDOUT;
						paad->image_slots[1] = loadFontTexture_Counter(paad->image_slots[1], 7, 1);
						paad->cap = 1;
						paad->use_item_display = 0;
					}
					// Update Position depending on scale
					float h_factor = 1.0f;
					float y_factor = 1.0f;
					if (closest_shop == 0) { // Cranky
						h_factor = 60.0f;
						y_factor = 40.0f;
					} else if (closest_shop == 1) { // Funky
						h_factor = 60.0f;
						y_factor = 40.0f;
					} else if (closest_shop == 2) { // Candy
						h_factor = 62.0f;
						y_factor = 40.0f;
					}
					float scale = getShopScale(closest_shop);
					float x_r = determineXRatioMovement(CurrentActorPointer_0->rot_y);
					float x_d = scale * h_factor * x_r;
					float z_d = scale * h_factor * determineZRatioMovement(CurrentActorPointer_0->rot_y);
					float y_d = scale * y_factor;
					CurrentActorPointer_0->xPos += x_d;
					CurrentActorPointer_0->yPos += y_d;
					CurrentActorPointer_0->zPos += z_d;
					CurrentActorPointer_0->rot_y = (CurrentActorPointer_0->rot_y + 2048) % 4096;
					renderingParamsData* render = CurrentActorPointer_0->render;
					if (render) {
						render->scale_x = 0.0375f * scale;
						render->scale_z = 0.0375f * scale;
					}
				}
			} else {
				deleteActorContainer(CurrentActorPointer_0);
			}
		} else {
			// Helm Indicator
			for (int i = 0; i < 3; i++) {
				paad->image_slots[i] = loadFontTexture_Counter(paad->image_slots[i], 0, i);
			}
			int id = getActorSpawnerIDFromTiedActor(CurrentActorPointer_0);
			int face_map = Rando.k_rool_order[id - 0x100];
			int face_img = COUNTER_NO_ITEM;
			for (int i = 0; i < sizeof(helm_heads)/sizeof(krool_head); i++) {
				if (helm_heads[i].map == face_map) {
					face_img = helm_heads[i].texture_offset;
				}
			}
			CurrentActorPointer_0->rot_z = 3072; // Facing vertical
			paad->image_slots[1] = loadFontTexture_Counter(paad->image_slots[1], face_img, 1);
		}
	} else {
		if (CurrentMap != MAP_HELM) {
			if ((ObjectModel2Timer % 20) == 0) {
				int lim = paad->cap;
				if (lim > 1) {
					paad->current_slot += 1;
					if (paad->current_slot >= lim) {
						paad->current_slot = 0;
					}
					updateCounterDisplay();
				}
			}
			if (paad->linked_behaviour) {
				if (paad->linked_behaviour->current_state == 0xC) {
					CurrentActorPointer_0->obj_props_bitfield |= 0x4;
				} else {
					CurrentActorPointer_0->obj_props_bitfield &= 0xFFFFFFFB;
				}
			}
			if (CurrentMap == MAP_GALLEON) {
				int shop = paad->shop;
				int* m2location = (int*)ObjectModel2Pointer;
				int is_float = 0;
				float float_y = 0.0f;
				for (int i = 0; i < 2; i++) {
					int float_id = float_ids[i];
					int float_slot = convertIDToIndex(float_id);
					if (float_slot > -1) {
						ModelTwoData* float_slot_object = getObjectArrayAddr(m2location,0x90,float_slot);
						int float_slot_obj_type = float_slot_object->object_type;
						for (int j = 0; j < 3; j++) {
							if (shop_obj_types[j] == float_slot_obj_type) {
								if (j == shop) {
									is_float = 1;
									float_y = float_slot_object->yPos;
								}
							}
						}
					}
				}
				if (is_float) {
					CurrentActorPointer_0->yPos = float_y + float_offsets[shop];
				}
			}
		}
	}
	renderActor(CurrentActorPointer_0,0);
}