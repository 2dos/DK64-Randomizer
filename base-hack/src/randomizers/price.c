#include "../../include/common.h"

#define FUNKY 1
#define CRANKY 5
#define CANDY 0x19

#define PURCHASE_MOVES 0
#define PURCHASE_SLAM 1
#define PURCHASE_GUN 2
#define PURCHASE_AMMOBELT 3
#define PURCHASE_INSTRUMENT 4
#define PURCHASE_NOTHING -1

#define SHOP_CRANKY 0
#define SHOP_FUNKY 1
#define SHOP_CANDY 2

void alter_price(int purchase_type, int purchase_value, int kong, int level, int shop_index) {
	int write = -1;
	if (purchase_type > PURCHASE_NOTHING) {
		switch(purchase_type) {
			case PURCHASE_MOVES:
				write = Rando.special_move_prices[kong][purchase_value - 1];
				break;
			case PURCHASE_SLAM:
				write = Rando.slam_prices[purchase_value - 2];
				break;
			case PURCHASE_GUN:
				if (purchase_value == 1) {
					write = Rando.gun_prices[kong];
				} else {
					write = Rando.gun_upgrade_prices[purchase_value - 2];
				}
				break;
			case PURCHASE_AMMOBELT:
				write = Rando.ammo_belt_prices[purchase_value - 1];
				break;
			case PURCHASE_INSTRUMENT:
				if (purchase_value == 1) {
					write = Rando.instrument_prices[kong];
				} else {
					write = Rando.instrument_upgrade_prices[purchase_value - 2];
				}
			break;
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
			}
		}
	}
}

void priceTransplant(void) {
	for (int kong = 0; kong < 5; kong++) {
		for (int level = 0; level < 7; level++) {
			alter_price(CrankyMoves_New[kong][level].purchase_type,CrankyMoves_New[kong][level].purchase_value,kong,level,SHOP_CRANKY);
			alter_price(CandyMoves_New[kong][level].purchase_type,CandyMoves_New[kong][level].purchase_value,kong,level,SHOP_CANDY);
			alter_price(FunkyMoves_New[kong][level].purchase_type,FunkyMoves_New[kong][level].purchase_value,kong,level,SHOP_FUNKY);
		}
	}
}

void price_rando(void) {
	if ((Rando.price_rando_on == 1) || (Rando.move_rando_on == 1)) {
		priceTransplant();
	}
}