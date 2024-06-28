#include "../../include/common.h"

void alter_price(purchase_struct* data) {
	// int purchase_type, int purchase_value, int kong, int level, vendors shop_index
	if (!data) {
		return;
	}
	int write = -1;
	if (data->purchase_type == PURCHASE_FLAG) {
		int subtype = getMoveProgressiveFlagType(data->purchase_value);
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
		data->price = write;
	}
}

void priceTransplant(void) {
	for (int kong = 0; kong < 5; kong++) {
		for (int level = 0; level < 8; level++) {
			for (int vendor = 0; vendor < 3; vendor++) {
				purchase_struct* data = getShopData(vendor, kong, level);
				alter_price(data);	
			}
		}
	}
}