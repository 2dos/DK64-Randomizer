#include "../../include/common.h"

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
			unsigned char *src_arr = &src->item;
			unsigned char *targ_arr = &targ->item;
			for (int j = 0; j < 4; j++) {
				if (src_arr[j] != targ_arr[j]) {
					return 0;
				}
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

int getCounterItem(vendors shop_index, int kong, int level) {
	purchase_struct* data = getShopData(shop_index, kong, level);
	if (data) {
		return getShopSkinIndex(&data->item);
	}
	return SKIN_NULL;
}

int getMoveCountInShop(counter_paad* paad, vendors shop_index) {
	int level = getWorld(CurrentMap,0);
	int count = 0;
	if (level < LEVEL_COUNT) {
		for (int i = 0; i < 5; i++) {
			if (!isShopEmpty(shop_index, level, i)) {
				// Shop is some item
				if (isSharedMove(shop_index, level)) {
					paad->kong_images[0] = SKIN_SHARED;
					paad->item_images[0] = getCounterItem(shop_index, i, level);
					return 1;
				} else {
					paad->kong_images[count] = i + 1;
					paad->item_images[count] = getCounterItem(shop_index, i, level);
					count++;
				}
			}
		}
	}
	return count;
}

#define IMG_WIDTH 32

static void* texture_data[SKIN_TERMINATOR] = {};
static unsigned char texture_load[SKIN_TERMINATOR] = {};

void wipeCounterImageCache(void) {
	for (int i = 0; i < SKIN_TERMINATOR; i++) {
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

/*
	Cranky's: 0x73
	Funky's Hut: 0x7A
	Candy's Shop: 0x124
	Snide's HQ: 0x79
*/
static short shop_objects[] = {0x73, 0x7A, 0x124, 0x79};

int getClosestShop(void) {
	counter_paad* paad = CurrentActorPointer_0->paad;
	int closest_dist = -1;
	int closest_shop_index = -1;
	paad->linked_behaviour = 0;
	for (int i = 0; i < ObjectModel2Count; i++) {
		ModelTwoData* _object = &ObjectModel2Pointer[i];
		int local_idx = -1;
		for (int j = 0; j < 4; j++) {
			if (_object->object_type == shop_objects[j]) {
				local_idx = j;
			}
		}
		if (local_idx > -1) {
			int temp_dist = getActorModelTwoDist(_object);
			if ((closest_dist == -1) || (temp_dist < closest_dist)) {
				closest_dist = temp_dist;
				closest_shop_index = local_idx;
				paad->linked_behaviour = _object->behaviour_pointer;
			}
		}
	}
	return closest_shop_index;
}

typedef struct ModelData {
	/* 0x000 */ float pos[3];
	/* 0x00C */ float scale;
} ModelData;

float getShopScale(int index) {
	for (int i = 0; i < ObjectModel2Count; i++) {
		ModelTwoData* _object = &ObjectModel2Pointer[i];
		if (_object) {
			if (_object->object_type == shop_objects[index]) {
				ModelData* model = _object->model_pointer;
				if (model) {
					if (index == SHOP_SNIDE) {
						return model->scale * 1.4f;
					}
					return model->scale;
				}
			}
		}
	}
	return 1.0f;
}

static const short float_ids[] = {0x1F4, 0x36};
static const float float_offsets[] = {51.0f, 45.0f, 45.0f, 47.5f};
static const float h_factors[] = {60.0f, 60.0f, 62.0f, 120.6f};

void newCounterCode(void) {
	counter_paad* paad = CurrentActorPointer_0->paad;
	if ((CurrentActorPointer_0->obj_props_bitfield & 0x10) == 0) {
		// Init Code
		if (Rando.shop_indicator_on) {
			if (Rando.shop_indicator_on == 2) {
				paad->use_item_display = 1;
			} else {
				paad->use_item_display = 0;
			}
			// Initialize slots
			for (int i = 0; i < 3; i++) {
				paad->image_slots[i] = loadFontTexture_Counter(paad->image_slots[i], SKIN_NULL, i);
			}
			CurrentActorPointer_0->rot_z = 3072; // Facing vertical
			int closest_shop = getClosestShop();
			if (closest_shop == SHOP_SNIDE) {
				if (!Rando.snide_has_rewards) {
					deleteActorContainer(CurrentActorPointer_0);
					return;
				}
				setActorModel(CurrentActorPointer_0, 0x139);
			} else {
				setActorModel(CurrentActorPointer_0, 0xA4);
			}
			paad->shop = closest_shop;
			// Update Position depending on scale
			float scale = getShopScale(closest_shop);
			int rot_y = CurrentActorPointer_0->rot_y;
			int rot_y_offset = 2048;
			float y_factor = 40.0f;
			if (closest_shop == SHOP_SNIDE) {
				rot_y -= 445;
				rot_y_offset = 2048 + 423;
				y_factor = 44.3f;
			}
			float h_factor = h_factors[closest_shop];
			float x_d = scale * h_factor * determineXRatioMovement(rot_y);
			float z_d = scale * h_factor * determineZRatioMovement(rot_y);
			float y_d = scale * y_factor;
			CurrentActorPointer_0->xPos += x_d;
			CurrentActorPointer_0->yPos += y_d;
			CurrentActorPointer_0->zPos += z_d;
			CurrentActorPointer_0->rot_y = (CurrentActorPointer_0->rot_y + rot_y_offset) % 4096;
			renderingParamsData* render = CurrentActorPointer_0->render;
			if (render) {
				render->scale_x = 0.0375f * scale;
				render->scale_z = 0.0375f * scale;
			}
			paad->current_slot = 0;
			if (closest_shop == SHOP_SNIDE) { // Snide is closest
				// Rules for Snide
				int snide_index = getTurnedCount(-1);
				if (snide_index > 39) {
					deleteActorContainer(CurrentActorPointer_0);
					return;
				}
				for (int i = 0; i < 3; i++) {
					if ((snide_index + i) < 40) {
						int img_idx = getShopSkinIndex(&snide_rewards[snide_index + i].item);
						paad->image_slots[i] = loadFontTexture_Counter(paad->image_slots[i], img_idx, i);
					}
				}
				paad->cap = 1;
			} else {
				paad->cap = getMoveCountInShop(paad, paad->shop);
				updateCounterDisplay();
				if (paad->cap == 0) {
					paad->kong_images[0] = SKIN_SOLDOUT;
					paad->image_slots[1] = loadFontTexture_Counter(paad->image_slots[1], SKIN_SOLDOUT, 1);
					paad->cap = 1;
					paad->use_item_display = 0;
				}
				
			}
		} else {
			deleteActorContainer(CurrentActorPointer_0);
		}
		return;
	}
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
		for (int i = 0; i < 2; i++) {
			int float_slot = convertIDToIndex(float_ids[i]);
			if (float_slot > -1) {
				ModelTwoData* float_slot_object = &ObjectModel2Pointer[float_slot];
				int float_slot_obj_type = float_slot_object->object_type;
				for (int j = 0; j < 3; j++) {
					if (shop_objects[j] == float_slot_obj_type) {
						if (j == shop) {
							CurrentActorPointer_0->yPos = float_slot_object->yPos + float_offsets[shop];
						}
					}
				}
			}
		}
	}
	renderActor(CurrentActorPointer_0, 0);
}