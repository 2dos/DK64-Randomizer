#include "../../include/common.h"

void clearVultureCutscene(int unk0, int unk1, int unk2) {
    modifyCharSpawnerAttributes(unk0,unk1,unk2);
    cancelCutscene(0);
}