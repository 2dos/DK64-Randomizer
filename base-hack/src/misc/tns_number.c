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

void shiftBrokenJapesPortal(void) {
	if (CurrentMap == MAP_JAPES) {
		int slot = convertIDToIndex(0x220);
		model_struct* _model = ObjectModel2Pointer[slot].model_pointer;
		if (_model) {
			_model->x = 722.473f;
			_model->z = 2386.608f;
		}
	}
}

static const unsigned char tns_maps[] = {
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

static const unsigned char tns_count[] = {
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

void displayNumberOnTns(void) {
	int in_tns_map = -1;
	for (int i = 0; i < 9; i++) {
		if (tns_maps[i] == CurrentMap) {
			in_tns_map = i;
		}
	}
	if (in_tns_map > -1) {
		int world_index = getWorld(CurrentMap, 0);
		if (world_index <= 7) {
			if (checkFlag(tnsportal_flags[world_index], FLAGTYPE_PERMANENT) == 0) {
				for (int j = 0; j < tns_count[in_tns_map]; j++) {
					int display_number = TroffNScoffReqArray[world_index] - TroffNScoffTurnedArray[world_index];
					if (display_number < 0) {
						display_number = 0;
					}
					for (int i = 1; i < 4; i++) {
						displayNumberOnObject(0x220 + j,i,(((10-i) + display_number % 10) % 10) - 1, 0, 0);
						display_number /= 10;
					}
				}
			} else {
				for (int j = 0; j < tns_count[in_tns_map]; j++) {
					int slot = convertIDToIndex(0x220 + j);
					model_struct* _model = ObjectModel2Pointer[slot].model_pointer;
					if (_model) {
						_model->scale = 0.0f;
					}
				}
			}
		}
	}
}