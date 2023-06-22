#include "../../include/common.h"

void clearVultureCutscene(void) {
    cutsceneKongGenericCode();
    if (CurrentActorPointer_0->control_state == 0xF) {
        CurrentActorPointer_0->control_state = 0x30;
        cancelCutscene(0);
        CurrentActorPointer_0->draw_distance = 1000;
        TiedCharacterSpawner->unk_46 |= 0x24;
    }
}