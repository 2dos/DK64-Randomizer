#include "../../include/common.h"

#define BTF_CRANKY 1
#define BTF_FUNKY 2
#define BTF_CANDY 4

static const unsigned char shop_maps[] = {
	0x07, // Japes
	0x26, // Aztec
	0x1A, // Factory
	0x1E, // Galleon
	0x30, // Fungi
	0x48, // Caves
	0x57, // Castle
	0xB7, // Castle: Hub
	0x97, // Castle: Tunnel
	0xB0, // Training Grounds
};

static const char shop_btf[] = {
	BTF_CRANKY | BTF_FUNKY, // Japes
	BTF_CRANKY | BTF_FUNKY | BTF_CANDY, // Aztec
	BTF_CRANKY | BTF_FUNKY | BTF_CANDY, // Factory
	BTF_CRANKY | BTF_FUNKY | BTF_CANDY, // Galleon
	BTF_CRANKY | BTF_FUNKY, // Fungi
	BTF_CRANKY | BTF_FUNKY | BTF_CANDY, // Caves
	BTF_CRANKY, // Castle
	BTF_FUNKY, // Castle: Crypt
	BTF_CANDY, // Castle: Tunnel
	BTF_CRANKY, // Training Grounds
};

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
	if (level < 7) {
		for (int i = 0; i < 5; i++) {
			if (shop_index == SHOPINDEX_CRANKY) {
				possess = doesKongPossessMove(CrankyMoves_New[i][level].purchase_type, CrankyMoves_New[i][level].purchase_value, i);
			} else if (shop_index == SHOPINDEX_FUNKY) {
				possess = doesKongPossessMove(FunkyMoves_New[i][level].purchase_type, FunkyMoves_New[i][level].purchase_value, i);
			} else if (shop_index == SHOPINDEX_CANDY) {
				possess = doesKongPossessMove(CandyMoves_New[i][level].purchase_type, CandyMoves_New[i][level].purchase_value, i);
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

void adjustGalleonShopHeights(void) {
	if (Rando.shop_indicator_on) {
		if (CurrentMap == 0x1E) {
			if (SwapObject) {
				int cam_chunk = SwapObject->chunk;
				int* m2location = ObjectModel2Pointer;
				if ((cam_chunk == 12) || (cam_chunk == 15)) {
					int candy = convertIDToIndex(0x36);
					if (candy > -1) {
						ModelTwoData* candy_object = getObjectArrayAddr(m2location,0x90,candy);
						int candy_y = candy_object->yPos;
						int candy_indicator = convertIDToIndex(0x232);
						if (candy_indicator > -1) {
							ModelTwoData* _object = getObjectArrayAddr(m2location,0x90,candy_indicator);
							model_struct* _model = _object->model_pointer;
							if (_model) {
								_model->y = candy_y;
							}
						}
					}
				} else if (cam_chunk == 13) {
					int funky = convertIDToIndex(0x1F4);
					if (funky > -1) {
						ModelTwoData* funky_object = getObjectArrayAddr(m2location,0x90,funky);
						int funky_y = funky_object->yPos + 2.693f;
						int funky_indicator = convertIDToIndex(0x231);
						if (funky_indicator > -1) {
							ModelTwoData* _object = getObjectArrayAddr(m2location,0x90,funky_indicator);
							model_struct* _model = _object->model_pointer;
							if (_model) {
								_model->y = funky_y;
							}
						}
					}
				}
			}
		}
	}
}

void displayShopIndicator(void) {
	int in_shop_container_map = -1;
	for (int i = 0; i < sizeof(shop_maps); i++) {
		if (shop_maps[i] == CurrentMap) {
			in_shop_container_map = i;
		}
	}
	if (in_shop_container_map > -1) {
		if (Rando.shop_indicator_on) {
			for (int j = 0; j < 3; j++) {
				if (shop_btf[in_shop_container_map] & (1 << j)) {
					int display_number = getMoveCountInShop(j);
					if (display_number < 0) {
						display_number = 0;
					}
					for (int i = 1; i < 4; i++) {
						displayNumberOnObject(0x230 + j,i,(((10-i) + display_number % 10) % 10) - 1, 0, 0);
						display_number /= 10;
					}
				}
			}
		} else {
			int* m2location = ObjectModel2Pointer;
			for (int j = 0; j < 3; j++) {
				int slot = convertIDToIndex(0x230 + j);
				if (slot > -1) {
					ModelTwoData* _object = getObjectArrayAddr(m2location,0x90,slot);
					model_struct* _model = _object->model_pointer;
					if (_model) {
						_model->scale = 0.0f;
					}
				}
			}
		}
	}
}

typedef struct counter_paad {
	/* 0x000 */ void* image_slots[3];
} counter_paad;

void updateCounterDisplay(void) {
	int kongs_btf = CurrentActorPointer_0->rgb_mask[1];
	int index = CurrentActorPointer_0->rgb_mask[2];
	counter_paad* paad = CurrentActorPointer_0->paad;
	if (kongs_btf & MOVEBTF_SHARED) {
		index = 0;
		paad->image_slots[1] = StoredCounterTextures[6];
	} else {
		int found_index = 0;
		int kong = 0;
		while (kong < 5) {
			if (kongs_btf & (1 << kong)) {
				paad->image_slots[1] = StoredCounterTextures[kong+1];
				return;
			}
			kong++;
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

void getClosestShop(void) {
	/*
		Cranky's: 0x73
		Funky's Hut: 0x7A
		Candy's Shop: 0x124
	*/
	unsigned int dists[3] = {0xFFFFFFFF,0xFFFFFFFF,0xFFFFFFFF};
	int* m2location = ObjectModel2Pointer;
	int found_counter = 0;
	for (int i = 0; i < ObjectModel2Count; i++) {
		if (found_counter < 3) {
			ModelTwoData* _object = getObjectArrayAddr(m2location,0x90,i);
			if (_object->object_type == 0x73) {
				dists[0] = getActorModelTwoDist(_object);
				found_counter += 1;
			} else if (_object->object_type == 0x7A) {
				dists[1] = getActorModelTwoDist(_object);
				found_counter += 1;
			} else if (_object->object_type == 0x124) {
				dists[2] = getActorModelTwoDist(_object);
				found_counter += 1;
			}
		}
	}
	if ((dists[2] < dists[1]) && (dists[2] < dists[0])) {
		return 2;
	} else if ((dists[1] < dists[0]) && (dists[1] < dists[2])) {
		return 1;
	}
	return 0;
}

void newCounterCode(void) {
	counter_paad* paad = CurrentActorPointer_0->paad;
	if ((CurrentActorPointer_0->obj_props_bitfield & 0x10) == 0) {
		// Init Code
		for (int i = 0; i < 3; i++) {
			paad->image_slots[i] = StoredCounterTextures[0];
		}
		CurrentActorPointer_0->rot_z = 3072; // Facing vertical
		CurrentActorPointer_0->rgb_mask[0] = getClosestShop();
		CurrentActorPointer_0->rgb_mask[1] = getMoveCountInShop(CurrentActorPointer_0->rgb_mask[0] & 0xF);
		updateCounterDisplay();
	}
}