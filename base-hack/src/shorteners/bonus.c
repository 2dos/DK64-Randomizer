#include "../../include/common.h"

#define DISREGARD_TANGIBILITY 0

void destroyBonus(actorData* bonus) {
    bonus->control_state = 0xC;
    bonus->control_state_progress = 0;
    bonus->noclip_byte = 1;
    bonus_paad* paad = (bonus_paad*)(bonus->paad);
    paad->destroy_timer = 3;
}

void completeBonus(actorData* actor) {
    unkBonusFunction(actor);
    int control_state = actor->control_state;
    if ((control_state == 0) || (control_state == 0x15) || ((DISREGARD_TANGIBILITY) && ((actor->obj_props_bitfield & 0x10) == 0))) {
        if (Gamemode != GAMEMODE_DKTV) {
            if ((Rando.resolve_bonus & 1) && (actor->actorType == 0x1C)) {
                // Regular Bonus
                destroyBonus(actor);
            }
            if ((Rando.resolve_bonus & 2) && (actor->actorType == 0x6B)) {
                // Helm Bonus
                destroyBonus(actor);
            }
        }
    }
}