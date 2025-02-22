#include "../../include/common.h"

typedef struct coinHUDStruct {
	/* 0x000 */ maps map_id;
	/* 0x004 */ unsigned char *addr;
} coinHUDStruct;

static coinHUDStruct CoinHUDElements[] = {
	{.map_id = MAP_AZTECBEETLE, .addr = &Rando.coinreq_aztecbeetle},
	{.map_id = MAP_JAPESMINECART, .addr = &Rando.coinreq_japescart},
	{.map_id = MAP_FUNGIMINECART, .addr = &Rando.coinreq_fungicart},
	{.map_id = MAP_CAVESBEETLERACE, .addr = &Rando.coinreq_cavesbeetle},
	{.map_id = MAP_FACTORYCARRACE, .addr = &Rando.coinreq_factorycar},
	{.map_id = MAP_CASTLECARRACE, .addr = &Rando.coinreq_castlecar},
	{.map_id = MAP_GALLEONSEALRACE, .addr = &Rando.coinreq_sealrace},
	{.map_id = MAP_CASTLEMINECART, .addr = &Rando.coinreq_castlecart},
};

Gfx* writeHUDAmount(char* str_location, char* format, int value, int item_index, Gfx* dl) {
	if (item_index == 0xB) {
		for (int i = 0; i < 8; i++) {
			if (CoinHUDElements[i].map_id == CurrentMap) {
				dk_strFormat(str_location,"%dl%d", value, *CoinHUDElements[i].addr);
				gSPMatrix(dl++, (int)&style6Mtx[0], G_MTX_NOPUSH | G_MTX_LOAD | G_MTX_MODELVIEW);
				return dl;
			}
		}
	}
	dk_strFormat(str_location,"%d",value);
	return dl;
}