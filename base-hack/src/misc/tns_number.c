#include "../../include/common.h"

void displayNumberOnObject(int id, int param2, int imageindex, int param4, int subtype) {
	int slot = convertIDToIndex(id);
	model_struct* _model = ObjectModel2Pointer[slot].model_pointer;
	if (_model) {
		if (subtype == 0) {
			drawNumberObject(_model->unk_B8,param2,imageindex,param4);
		} else {
			drawNumberObject(_model->unk_50,param2,imageindex,param4);
		}
	}
}

ROM_RODATA_NUM static const unsigned char tns_maps[] = {
	MAP_JAPES, // Japes
	MAP_FACTORY, // Factory
	MAP_GALLEON, // Galleon
	MAP_AZTEC, // Aztec
	MAP_FUNGI, // Fungi
	MAP_CAVES, // Caves
	MAP_CASTLE, // Castle
	MAP_CASTLEDUNGEON, // Castle Dungeon Tunnel
	MAP_CASTLECRYPT, // Castle Crypt
};

ROM_RODATA_NUM static const unsigned char tns_count[] = {
	3,
	5,
	5,
	5,
	5,
	5,
	3,
	1,
	1,
};