/**
 * @file turf.c
 * @author Ballaam
 * @version 0.1
 * @date 2026-02-06
 * 
 * @copyright Copyright (c) 2026
 * 
 */
#include "../../include/common.h"

// Holding boulder cs = 0x48 (cs func: 806da94c)
// csc = 0x37: l offset 80751ec0

typedef struct holdableDisplacementStruct {
    unsigned short actor_type;
    short displacement;
} holdableDisplacementStruct;

ROM_RODATA_NUM static const holdableDisplacementStruct holdableDisplacements[] = {
    { .actor_type = 63,  .displacement = 386 },
    { .actor_type = 64,  .displacement = 386 },
    { .actor_type = 65,  .displacement = 386 },
    { .actor_type = 66,  .displacement = 386 },
    { .actor_type = 85,  .displacement = 120 },
    { .actor_type = 130, .displacement = 334 },
    { .actor_type = 67,  .displacement = 120 },
};

float getHoldableHeightLocal(actorData *actor) {
    for (unsigned int i = 0; i < sizeof(holdableDisplacements) / sizeof(holdableDisplacementStruct); i++) {
        if (holdableDisplacements[i].actor_type == actor->actorType) {
            return holdableDisplacements[i].displacement;
        }
    }
    return 196.6f;
}

float getHoldableHeight(actorData *actor) {
    return getHoldableHeightLocal(actor) * actor->render->scale_y;
}

// int isHoldableBarrel(actorData *actor) {
//     if (actor->actorType == 85) {
//         return 1;
//     }
//     return 0;
// }

void enterTS(void) {
    if (NewlyPressedControllerInput.Buttons.l) {
        playerData *player = (playerData *)CurrentActorPointer_0;
        player->control_state = 0x84;
        player->control_state_progress = 0;
        actorData *turf = player->held_actor;
        if (isAddressActor(turf)) {
            turf->control_state = 8;
            turf->control_state_progress = 0;
            turf->xPos = Player->xPos;
            turf->yPos = Player->yPos;
            turf->zPos = Player->zPos;
            turf->yVelocity = 5.0f;
            CurrentActorPointer_0->hSpeed = 60.0f;
            player->vehicle_actor_pointer = turf;
            // if (isHoldableBarrel(turf)) {
            //     turf->rot_z = 1024;
            // }
        }
        player->held_actor = 0;
        player->held_destroy_actor = 0;
        playAnimation(player, 0x86);
    }
}

void boulderTSCode(void) {
    if (CurrentActorPointer_0->grounded & 1) {
        CurrentActorPointer_0->hSpeed -= 0.1f;
        if (CurrentActorPointer_0->hSpeed < 0.0f) {
            CurrentActorPointer_0->hSpeed = 0.0f;
        }
    }
    float x_delta = determineXRatioMovement(CurrentActorPointer_0->rot_y_copy) * 2.0f;
    float z_delta = determineZRatioMovement(CurrentActorPointer_0->rot_y_copy) * 2.0f;
    Player->xPos = CurrentActorPointer_0->xPos + x_delta;
    Player->zPos = CurrentActorPointer_0->zPos + z_delta;
    Player->yPos = CurrentActorPointer_0->yPos + getHoldableHeight(CurrentActorPointer_0);
    CurrentActorPointer_0->yVelocity -= 4.0f;
    if (CurrentActorPointer_0->grounded & 1) {
        CurrentActorPointer_0->yVelocity = 0.0f;
    }
    CurrentActorPointer_0->obj_props_bitfield |= 0x20;
    if (isBoulderMakingCollision()) {
        CurrentActorPointer_0->control_state = 4;
    }
    // Gravity Functions
    unkProjectileCode_2(CurrentActorPointer_0);
    unkProjectileCode_3(CurrentActorPointer_0, 0);
}

void TSHandler(void) {
    // unkVehicleFunc();
    playerData *player = (playerData *)CurrentActorPointer_0;
    actorData *vehicle = player->vehicle_actor_pointer;
    if (!isAddressActor(vehicle)) {
        player->control_state = 0x48;
        player->control_state_progress = 0;
        player->vehicle_actor_pointer = 0;
    } else {
        // if (isHoldableBarrel(vehicle)) {
        //     vehicle->rot_x += vehicle->hSpeed;
        // } else {
        // }
        vehicle->rot_y += vehicle->hSpeed;
        vehicle->rot_y &= 0xFFF;
        vehicle->rot_y_copy = player->facing_angle;
        controlStateControl(90);
        inVehicleMovement();
    }
    renderActor(CurrentActorPointer_0, 0);
}

void TSJump(void) {
    if (Input.Buttons.a) {
        playerData *player = (playerData *)CurrentActorPointer_0;
        actorData *vehicle = player->vehicle_actor_pointer;
        int delta = vehicle->yPos - vehicle->floor;
        if ((delta > -10) && (delta < 10)) {
            vehicle->yVelocity = 100.0f;
        }
    }
}

void TSSpeed(void) {
    if (Input.Buttons.l) {
        playerData *player = (playerData *)CurrentActorPointer_0;
        actorData *vehicle = player->vehicle_actor_pointer;
        if (vehicle->grounded & 1) {
            vehicle->hSpeed += 20.0f;
            vehicle->yVelocity = 5.0f;
            if (vehicle->hSpeed > 300.0f) {
                vehicle->hSpeed = 300.0f;
            }
            playAnimation(player, 0x86);
        }
    }
}

void TSDrop(void) {
    playerData *player = (playerData *)CurrentActorPointer_0;
    player->control_state = 0x48;
    player->control_state_progress = 0;
    actorData *turf = player->vehicle_actor_pointer;
    if (isAddressActor(turf)) {
        turf->control_state = 2;
        turf->control_state_progress = 0;
        player->vehicle_actor_pointer = 0;
        player->held_actor = turf;
        player->held_destroy_actor = turf;
        player->yPos -= getHoldableHeight(turf);
        turf->rot_x = 0;
        turf->rot_y = 0;
        turf->rot_z = 0;
    }
    playAnimation(player, 0x2C);
}