/**
 * @file cannon_game.c
 * @author Ballaam
 * @brief Changes related to the cannon game in Galleon
 * @version 0.1
 * @date 2023-12-16
 * 
 * @copyright Copyright (c) 2023
 * 
 */

#include "../../include/common.h"

typedef struct cannon_game_paad {
    /* 0x000 */ char unk_00[8];
    /* 0x008 */ short h_angle;
} cannon_game_paad;

void handleCannonGameReticle(void) {
    if (CurrentMap == MAP_GALLEON) {
        float size = 1.0f;
        if (Rando.quality_of_life.cannon_game_speed) {
            if (ControllerInput.Buttons.a) {
                size = 0.2f;
            }
        }
        float y_value = size;
        if (InvertedControls) {
            y_value = -size;
        }
        *(float*)(0x8074E7F8) = size;
        *(float*)(0x8074E800) = y_value;
    }
}

void resetCannonGameState(actorData* actor) {
    if (actor->control_state == 0) {
        cannon_game_paad* paad = actor->paad;
        paad->h_angle = 0;
        *(float*)(0x8074E804) = 0;
    }
    renderActor(actor, 0);
}