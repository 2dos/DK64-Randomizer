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
	*/
	unsigned int dists[3] = {0xFFFFFFFF,0xFFFFFFFF,0xFFFFFFFF};
	int* m2location = ObjectModel2Pointer;
	int found_counter = 0;
	behaviour_data* behavs[3] = {};
	counter_paad* paad = CurrentActorPointer_0->paad;
	for (int i = 0; i < ObjectModel2Count; i++) {
		if (found_counter < 3) {
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
			}
		}
	}
	int closest_index = 0;
	if ((dists[2] < dists[1]) && (dists[2] < dists[0])) {
		paad->linked_behaviour = behavs[2];
		closest_index = 2;
	} else if ((dists[1] < dists[0]) && (dists[1] < dists[2])) {
		paad->linked_behaviour = behavs[1];
		closest_index = 1;
	}
	if (found_counter > 0) {
		paad->linked_behaviour = behavs[closest_index];
	}
	return closest_index;
}

void newCounterCode(void) {
	counter_paad* paad = CurrentActorPointer_0->paad;
	if ((CurrentActorPointer_0->obj_props_bitfield & 0x10) == 0) {
		// Init Code
		if (Rando.shop_indicator_on) {
			for (int i = 0; i < 3; i++) {
				paad->image_slots[i] = loadCounterFontTexture(0x21,paad->image_slots[i],i,0,IMG_WIDTH);
			}
			CurrentActorPointer_0->rot_z = 3072; // Facing vertical
			CurrentActorPointer_0->rgb_mask[0] = getClosestShop();
			CurrentActorPointer_0->rgb_mask[1] = getMoveCountInShop(CurrentActorPointer_0->rgb_mask[0] & 0xF);
			CurrentActorPointer_0->rgb_mask[2] = 0;
			updateCounterDisplay();
			if (CurrentActorPointer_0->rgb_mask[1] == 0) {
				paad->image_slots[1] = loadFontTexture_Counter(paad->image_slots[1],7);
			}
		} else {
			deleteActorContainer(CurrentActorPointer_0);
		}
	} else {
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
	renderActor(CurrentActorPointer_0,0);
}