#include "../../include/common.h"

typedef struct foot_extra_data {
    /* 0x000 */ char unk_00[0x12];
    /* 0x012 */ unsigned short progress;
    /* 0x014 */ char damage_applied;
    /* 0x015 */ char unk_15[0x18-0x15];
} foot_extra_data;

typedef struct foot_toes {
    /* 0x000 */ actorData* toe[3];
} foot_toes;

void handleFootProgress(actorData* actor) {
    foot_extra_data* data = actor->paad2;
    int progress = data->progress;
    foot_toes* toes = (foot_toes*)actor->paad3;
    if ((progress == 1) || (progress == 3)) {
        // Warp Back
        playAnimation(Player,0x4A);
        setNextTransitionType(1);
        ISGActive = 1;
        initiateTransition(MAP_KROOLTINY,0);
        setFlag(FLAG_KROOL_TOE_1 + progress,1, FLAGTYPE_TEMPORARY);
        actor->control_state_progress += 1;
    } else {
        // Stay
        setFlag(FLAG_KROOL_TOE_1 + progress,1, FLAGTYPE_TEMPORARY);
        if (checkFlag(FLAG_KROOL_TOE_1, FLAGTYPE_TEMPORARY)) {
            setToeTexture(actor,4);
            actor->sub_state = 2;
            toes->toe[0]->sub_state = 1;
            data->progress = 1;
        }
        for (int i = 0; i < 2; i++) {
            if (checkFlag(FLAG_KROOL_TOE_2 + i, FLAGTYPE_TEMPORARY)) {
                setToeTexture(toes->toe[i],4);
                toes->toe[i]->sub_state = 2;
                toes->toe[i + 1]->sub_state = 1;
                data->progress = 2 + i;
            }
        }
        actor->control_state = 0x28;
        actor->control_state_progress = 2;
        data->damage_applied = 0;
        actor->takes_enemy_damage = -1;
    }
}