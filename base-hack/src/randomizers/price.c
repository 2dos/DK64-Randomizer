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

void alter_price(int purchase_type, int purchase_value, int kong, int level) {
	int write = 0;
	if (purchase_type > PURCHASE_NOTHING) {
		switch(purchase_type) {
			case PURCHASE_MOVES:
				CrankyMoves[kong][level].price = Rando.special_move_prices[kong][purchase_value - 1];
				break;
			case PURCHASE_SLAM:
				CrankyMoves[kong][level].price = Rando.slam_prices[purchase_value - 2];
				break;
			case PURCHASE_GUN:
				if (purchase_value == 1) {
					write = Rando.gun_prices[kong];
				} else {
					write = Rando.gun_upgrade_prices[purchase_value - 2];
				}
				FunkyMoves[kong][level].price = write;
				break;
			case PURCHASE_AMMOBELT:
				FunkyMoves[kong][level].price = Rando.ammo_belt_prices[purchase_value - 1];
				break;
			case PURCHASE_INSTRUMENT:
				if (purchase_value == 1) {
					write = Rando.instrument_prices[kong];
				} else {
					write = Rando.instrument_upgrade_prices[purchase_value - 2];
				}
				CandyMoves[kong][level].price = write;
			break;
		}
	}
}

void price_rando(void) {
	if (Rando.price_rando_on) {
		if (CurrentMap == CRANKY) {
			for (int kong = 0; kong < 5; kong++) {
				for (int level = 0; level < 7; level++) {
					alter_price(CrankyMoves[kong][level].purchase_type,CrankyMoves[kong][level].purchase_value,kong,level);
				}
			}
		} else if (CurrentMap == CANDY) {
			for (int kong = 0; kong < 5; kong++) {
				for (int level = 0; level < 7; level++) {
					alter_price(CandyMoves[kong][level].purchase_type,CandyMoves[kong][level].purchase_value,kong,level);
				}
			}
		} else if (CurrentMap == FUNKY) {
			for (int kong = 0; kong < 5; kong++) {
				for (int level = 0; level < 7; level++) {
					alter_price(FunkyMoves[kong][level].purchase_type,FunkyMoves[kong][level].purchase_value,kong,level);
				}
			}
		}
	}
}