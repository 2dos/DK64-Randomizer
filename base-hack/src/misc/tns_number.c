#include "../../include/common.h"

typedef struct model_struct {
	/* 0x000 */ char unk_00[0x50];
	/* 0x050 */ int unk_50;
	/* 0x054 */ char unk_54[0xB8-0x54];
	/* 0X0B8 */ int unk_B8;
} model_struct;

void displayNumberOnObject(int id, int param2, int imageindex, int param4) {
	int* m2location = ObjectModel2Pointer;
	int slot = convertIDToIndex(id);
	ModelTwoData* _object = getObjectArrayAddr(m2location,0x90,slot);
	model_struct* _model = _object->model_pointer;
	if (_model) {
		drawNumberObject(_model->unk_B8,param2,imageindex,param4);
	}
}

void displayNumberOnTns(void) {
	if (CurrentMap == 0x26) {
		int world_index = getWorld(CurrentMap, 0);
		if (world_index > 7) {
			world_index = 7;
		}
		int display_number = TroffNScoffReqArray[world_index];
		if (display_number < 0) {
			display_number = 0;
		}
		for (int i = 1; i < 4; i++) {
			displayNumberOnObject(0x302,i,((10-i) + display_number % 10) % 10, 0);
			display_number /= 10;
		}
	}
}