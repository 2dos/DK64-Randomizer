#include "../../include/common.h"

#define PURCHASE_MOVES 0
#define PURCHASE_SLAM 1
#define PURCHASE_GUN 2
#define PURCHASE_AMMOBELT 3
#define PURCHASE_INSTRUMENT 4
#define PURCHASE_NOTHING -1

void alter_price(int purchase_type, int purchase_value, int kong, int level, vendors shop_index) {
	int write = -1;
	if (purchase_type == PURCHASE_FLAG) {
		int subtype = getMoveProgressiveFlagType(purchase_value);
		if (subtype == 0) {
			// Slam
			write = Rando.slam_prices[MovesBase[0].simian_slam - 1];
		} else if (subtype == 1) {
			// Belt
			write = Rando.ammo_belt_prices[(int)MovesBase[0].ammo_belt];
		} else if (subtype == 2) {
			// Ins Upgrade
			int level = 0;
			if (MovesBase[0].instrument_bitfield & 4) {
				level = 2;
			} else if (MovesBase[0].instrument_bitfield & 2) {
				level = 1;
			}
			write = Rando.instrument_upgrade_prices[level];
		}
	}
	if (write > -1) {
		switch (shop_index) {
			case SHOP_CRANKY:
				CrankyMoves_New[kong][level].price = write;
				break;
			case SHOP_FUNKY:
				FunkyMoves_New[kong][level].price = write;
				break;
			case SHOP_CANDY:
				CandyMoves_New[kong][level].price = write;
				break;
			case SHOP_SNIDE:
				break;
			break;
		}
	}
}

void priceTransplant(void) {
	for (int kong = 0; kong < 5; kong++) {
		for (int level = 0; level < LEVEL_COUNT; level++) {
			alter_price(CrankyMoves_New[kong][level].purchase_type,CrankyMoves_New[kong][level].purchase_value,kong,level,SHOP_CRANKY);
			alter_price(CandyMoves_New[kong][level].purchase_type,CandyMoves_New[kong][level].purchase_value,kong,level,SHOP_CANDY);
			alter_price(FunkyMoves_New[kong][level].purchase_type,FunkyMoves_New[kong][level].purchase_value,kong,level,SHOP_FUNKY);
		}
	}
}