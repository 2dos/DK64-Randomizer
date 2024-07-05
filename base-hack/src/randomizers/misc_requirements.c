#include "../../include/common.h"

Gfx* writeHUDAmount(char* str_location, char* format, int value, int item_index, Gfx* dl) {
	int found = 0;
	int amt = -1;
	if (item_index == 0xB) {
		switch(CurrentMap) {
			case MAP_AZTECBEETLE:
				amt = Rando.coinreq_aztecbeetle;
				break;
			case MAP_JAPESMINECART:
				amt = Rando.coinreq_japescart;
				break;
			case MAP_FUNGIMINECART:
				amt = Rando.coinreq_fungicart;
				break;
			case MAP_CAVESBEETLERACE:
				amt = Rando.coinreq_cavesbeetle;
				break;
			case MAP_FACTORYCARRACE:
				amt = Rando.coinreq_factorycar;
				break;
			case MAP_CASTLECARRACE:
				amt = Rando.coinreq_castlecar;
				break;
			case MAP_GALLEONSEALRACE:
				amt = Rando.coinreq_sealrace;
				break;
			case MAP_CASTLEMINECART:
				amt = Rando.coinreq_castlecart;
				break;
			default:
			break;
		}
		if (amt > -1) {
			found = 1;
		}
	}
	if (found) {
		dk_strFormat(str_location,"%dl%d",value,amt);
		gSPMatrix(dl++, (int)&style6Mtx[0], G_MTX_NOPUSH | G_MTX_LOAD | G_MTX_MODELVIEW);
	} else {
		dk_strFormat(str_location,"%d",value);
	}
	return dl;
}