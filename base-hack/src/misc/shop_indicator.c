#include "../../include/common.h"

#define PURCHASE_MOVES 0
#define PURCHASE_SLAM 1
#define PURCHASE_GUN 2
#define PURCHASE_AMMOBELT 3
#define PURCHASE_INSTRUMENT 4
#define PURCHASE_NOTHING -1

int doesKongPossessMove(int purchase_type, int purchase_value, int kong) {
	if (purchase_type != PURCHASE_NOTHING) {
		if (purchase_value > 0) {
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
			}
		}
	}
	return 0;
};

#define MOVEBTF_DK 1
#define MOVEBTF_DIDDY 2
#define MOVEBTF_LANKY 4
#define MOVEBTF_TINY 8
#define MOVEBTF_CHUNKY 0x10
#define MOVEBTF_SHARED 0x20

#define SHOPINDEX_CRANKY 0
#define SHOPINDEX_FUNKY 1
#define SHOPINDEX_CANDY 2

int getMoveCountInShop(int shop_index) {
	int level = getWorld(CurrentMap,0);
	int possess = 0;
	int btf = 0;
	int count = 0;
	if (level < LEVEL_COUNT) {
		for (int i = 0; i < 5; i++) {
			if (shop_index == SHOPINDEX_CRANKY) {
				possess = doesKongPossessMove(CrankyMoves_New[i][level].purchase_type, CrankyMoves_New[i][level].purchase_value, CrankyMoves_New[i][level].move_kong);
			} else if (shop_index == SHOPINDEX_FUNKY) {
				possess = doesKongPossessMove(FunkyMoves_New[i][level].purchase_type, FunkyMoves_New[i][level].purchase_value, FunkyMoves_New[i][level].move_kong);
			} else if (shop_index == SHOPINDEX_CANDY) {
				possess = doesKongPossessMove(CandyMoves_New[i][level].purchase_type, CandyMoves_New[i][level].purchase_value, CandyMoves_New[i][level].move_kong);
			}
			if (possess == 1) {
				btf |= (1 << i);
				count += 1;
			} else if (possess > 1) {
				btf |= MOVEBTF_SHARED;
				count = 1;
			}
		}
	}
	CurrentActorPointer_0->rgb_mask[0] |= (count << 4);
	return btf;
}

typedef struct counter_paad {
	/* 0x000 */ void* image_slots[3];
	/* 0x00C */ behaviour_data* linked_behaviour;
} counter_paad;

#define IMG_WIDTH 32

void* loadFontTexture_Counter(void* slot, int index) {
	return loadCounterFontTexture(0x21,slot,1,index,IMG_WIDTH);
}

void updateCounterDisplay(void) {
	int kongs_btf = CurrentActorPointer_0->rgb_mask[1];
	int index = CurrentActorPointer_0->rgb_mask[2];
	int cap = CurrentActorPointer_0->rgb_mask[0] >> 4;
	counter_paad* paad = CurrentActorPointer_0->paad;
	if (kongs_btf & MOVEBTF_SHARED) {
		index = 0;
		paad->image_slots[1] = loadFontTexture_Counter(paad->image_slots[1],6);
	} else {
		int found_index = 0;
		for (int kong = 0; kong < 5; kong++) {
			if (kongs_btf & (1 << kong)) {
				if (found_index == index) {
					paad->image_slots[1] = loadFontTexture_Counter(paad->image_slots[1],kong+1);
					return;
				} else {
					found_index += 1;
					if (found_index == cap) {
						return;
					}
				}
			}
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
	int* m2location = ObjectModel2Pointer;
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
	int* m2location = ObjectModel2Pointer;
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

void newCounterCode(void) {
	counter_paad* paad = CurrentActorPointer_0->paad;
	if ((CurrentActorPointer_0->obj_props_bitfield & 0x10) == 0) {
		// Init Code
		if (CurrentMap != 0x11) {
			if (Rando.shop_indicator_on) {
				for (int i = 0; i < 3; i++) {
					paad->image_slots[i] = loadCounterFontTexture(0x21,paad->image_slots[i],i,0,IMG_WIDTH);
				}
				CurrentActorPointer_0->rot_z = 3072; // Facing vertical
				int closest_shop = getClosestShop();
				CurrentActorPointer_0->rgb_mask[0] = closest_shop;
				if (closest_shop == 3) { // Snide is closest
					deleteActorContainer(CurrentActorPointer_0);
				} else {
					CurrentActorPointer_0->rgb_mask[1] = getMoveCountInShop(CurrentActorPointer_0->rgb_mask[0] & 0xF);
					CurrentActorPointer_0->rgb_mask[2] = 0;
					updateCounterDisplay();
					if (CurrentActorPointer_0->rgb_mask[1] == 0) {
						paad->image_slots[1] = loadFontTexture_Counter(paad->image_slots[1],7);
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
					float x_r = getXRatioMovement(CurrentActorPointer_0->rot_y);
					float x_d = scale * h_factor * x_r;
					float z_d = scale * h_factor * getZRatioMovement(CurrentActorPointer_0->rot_y);
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
			for (int i = 0; i < 3; i++) {
				paad->image_slots[i] = loadCounterFontTexture(0x21,paad->image_slots[i],i,0,IMG_WIDTH);
			}
			int id = getActorSpawnerIDFromTiedActor(CurrentActorPointer_0);
			int face = Rando.k_rool_order[id - 0x100];
			CurrentActorPointer_0->rot_z = 3072; // Facing vertical
			paad->image_slots[1] = loadFontTexture_Counter(paad->image_slots[1],face+1);
		}
	} else {
		if (CurrentMap != 0x11) {
			if ((ObjectModel2Timer % 20) == 0) {
				int lim = CurrentActorPointer_0->rgb_mask[0] >> 4;
				if (lim > 1) {
					CurrentActorPointer_0->rgb_mask[2] += 1;
					if (CurrentActorPointer_0->rgb_mask[2] >= lim) {
						CurrentActorPointer_0->rgb_mask[2] = 0;
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
			if (CurrentMap == 0x1E) {
				int shop = CurrentActorPointer_0->rgb_mask[0] & 0xF;
				int* m2location = ObjectModel2Pointer;
				if (shop == 1) {
					int funky = convertIDToIndex(0x1F4);
					if (funky > -1) {
						ModelTwoData* funky_object = getObjectArrayAddr(m2location,0x90,funky);
						int funky_y = funky_object->yPos;
						CurrentActorPointer_0->yPos = funky_y + (40 * 1.12f);
					}
				} else if (shop == 2) {
					int candy = convertIDToIndex(0x36);
					if (candy > -1) {
						ModelTwoData* candy_object = getObjectArrayAddr(m2location,0x90,candy);
						int candy_y = candy_object->yPos;
						CurrentActorPointer_0->yPos = candy_y + (40 * 1.28f);
					}
				}
			}
		}
	}
	renderActor(CurrentActorPointer_0,0);
}