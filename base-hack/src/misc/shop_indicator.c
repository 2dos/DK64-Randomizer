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
					return 1;
				}
			} else if (purchase_type == PURCHASE_SLAM) {
				if (MovesBase[kong].simian_slam >= purchase_value) {
					return 2;
				}
			} else if (purchase_type == PURCHASE_GUN) {
				if (MovesBase[kong].weapon_bitfield & (1 << (purchase_value - 1))) {
					if (purchase_value == 1) {
						return 1;
					} else {
						return 3;
					}
				}
			} else if (purchase_type == PURCHASE_AMMOBELT) {
				if (MovesBase[kong].ammo_belt >= purchase_value) {
					return 4;
				}
			} else if (purchase_type == PURCHASE_INSTRUMENT) {
				if (MovesBase[kong].instrument_bitfield & (1 << (purchase_value - 1))) {
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

int getMoveCountInShop(int shop_index) {
	/* 
		0 = Cranky
		1 = Funky
		2 = Candy
	*/
	int count = 0;
	int level = getWorld(CurrentMap,0);
	int has_shared[] = {0,0,0,0};
	int possess = 0;
	if (level < 7) {
		for (int i = 0; i < 5; i++) {
			if (shop_index == 0) {
				possess = doesKongPossessMove(CrankyMoves_New[i][level].purchase_type, CrankyMoves_New[i][level].purchase_value, i);
			} else if (shop_index == 1) {
				possess = doesKongPossessMove(FunkyMoves_New[i][level].purchase_type, FunkyMoves_New[i][level].purchase_value, i);
			} else if (shop_index == 2) {
				possess = doesKongPossessMove(CandyMoves_New[i][level].purchase_type, CandyMoves_New[i][level].purchase_value, i);
			}
			if (possess == 1) {
				count += 1;
			} else if (possess > 1) {
				has_shared[possess - 2] = 1;
			}
		}
	}
	for (int i = 0; i < 4; i++) {
		count += has_shared[i];
	}
	return count;
}

void displayShopIndicator(void) {
	if (Rando.shop_indicator_on) {
		int in_shop_container_map = -1;
		for (int i = 0; i < 9; i++) {
			if (shop_maps[i] == CurrentMap) {
				in_shop_container_map = i;
			}
		}
		if (in_shop_container_map > -1) {
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
		}
	}
}