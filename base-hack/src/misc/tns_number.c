#include "../../include/common.h"

void displayNumberOnObject(int id, int param2, int imageindex, int param4, int subtype) {
	int* m2location = ObjectModel2Pointer;
	int slot = convertIDToIndex(id);
	ModelTwoData* _object = getObjectArrayAddr(m2location,0x90,slot);
	model_struct* _model = _object->model_pointer;
	if (_model) {
		if (subtype == 0) {
			drawNumberObject(_model->unk_B8,param2,imageindex,param4);
		} else {
			drawNumberObject(_model->unk_50,param2,imageindex,param4);
		}
	}
}

void shiftBrokenJapesPortal(void) {
	if (CurrentMap == 7) {
		int* m2location = ObjectModel2Pointer;
		int slot = convertIDToIndex(0x220);
		ModelTwoData* _object = getObjectArrayAddr(m2location,0x90,slot);
		model_struct* _model = _object->model_pointer;
		if (_model) {
			_model->x = 722.473f;
			_model->z = 2386.608f;
		}
	}
}

static const unsigned char tns_maps[] = {
	0x7, // Japes
	0x1A, // Factory
	0x1E, // Galleon
	0x26, // Aztec
	0x30, // Fungi
	0x48, // Caves
	0x57, // Castle
	0x97, // Castle Dungeon Tunnel
	0xB7, // Castle Crypt
};

static const unsigned char tns_count[] = {
	3,
	5,
	5,
	5,
	5,
	4,
	3,
	1,
	1,
};

static const short tns_flags[] = {
	46, // Japes
	108, // Aztec
	152, // Factory
	203, // Galleon
	258, // Fungi
	302, // Caves
	352, // Castle
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
			if (checkFlag(tns_flags[world_index],0) == 0) {
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
				int* m2location = ObjectModel2Pointer;
				for (int j = 0; j < tns_count[in_tns_map]; j++) {
					int slot = convertIDToIndex(0x220 + j);
					ModelTwoData* _object = getObjectArrayAddr(m2location,0x90,slot);
					model_struct* _model = _object->model_pointer;
					if (_model) {
						_model->scale = 0.0f;
					}
				}
			}
		}
	}
}