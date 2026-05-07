#include "../../include/common.h"

coinHUDStruct CoinHUDElements[8] = {
	{.map_id = MAP_AZTECBEETLE, .requirement = 50},
	{.map_id = MAP_JAPESMINECART, .requirement = 50},
	{.map_id = MAP_FUNGIMINECART, .requirement = 50},
	{.map_id = MAP_CAVESBEETLERACE, .requirement = 50},
	{.map_id = MAP_FACTORYCARRACE, .requirement = 10},
	{.map_id = MAP_CASTLECARRACE, .requirement = 10},
	{.map_id = MAP_GALLEONSEALRACE, .requirement = 10},
	{.map_id = MAP_CASTLEMINECART, .requirement = 25},
};

Gfx* writeHUDAmount(char* str_location, char* format, int value, int item_index, Gfx* dl) {
	if (item_index == 0xB) {
		for (int i = 0; i < 8; i++) {
			if (CoinHUDElements[i].map_id == CurrentMap) {
				dk_strFormat(str_location,"%dl%d", value, CoinHUDElements[i].requirement);
				gSPMatrix(dl++, (int)&style6Mtx[0], G_MTX_NOPUSH | G_MTX_LOAD | G_MTX_MODELVIEW);
				return dl;
			}
		}
	}
	dk_strFormat(str_location,"%d",value);
	return dl;
}