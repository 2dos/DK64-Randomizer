#include "../../include/common.h"

void clearVultureCutscene(void) {
    cutsceneKongGenericCode();
    if (CurrentActorPointer_0->control_state == 0xF) {
        CurrentActorPointer_0->control_state = 0x30;
        cancelCutscene(0);
    }
}