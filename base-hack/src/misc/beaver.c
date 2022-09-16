#include "../../include/common.h"

// typedef struct beaver_paad {
//     /* 0x000 */ char unk_00[0x1A];
//     /* 0x01A */ short scared_bitfield;
// } beaver_paad;

// void goldBeaverCode(void) {
//     initCharSpawnerActor();
//     if ((CurrentActorPointer_0->obj_props_bitfield & 0x10) == 0) {
//         unkCutsceneKongFunction_0(2,1);
//         modifyCharSpawnerAttributes(0x1F8,0x1F8,0x1F9);
//         if ((CurrentMap == 0x68) || (CurrentMap == 0x88) || (CurrentMap == 0x89)) {
//             CurrentActorPointer_0->subdata = 2;
//         }
//     }
//     if ((CurrentActorPointer_0->subdata == 2) && (CurrentActorPointer_0->control_state != 0x36)) {
//         actorData* klaptrap = isActorLoaded(0x11A);
//         if (klaptrap) {
//             beaver_paad* paad = klaptrap->paad;
//             if (klaptrap->control_state == 0) {
//                 // Not Barking
//                 paad->scared_bitfield &= 0x7FFF;
//             } else {
//                 if ((paad->scared_bitfield & 0x8000) == 0) {
//                     float dx = klaptrap->xPos - CurrentActorPointer_0->xPos;
//                     float dz = klaptrap->zPos - CurrentActorPointer_0->zPos;
//                     if (((dx * dx) + (dz * dz)) < 1600.0f) {
//                         int angle_sign = -1;
//                         int angle_delta = (klaptrap->rot_y  - CurrentActorPointer_0->rot_y) & 0xFFF;
//                         if (angle_delta > 0x800) {
//                             angle_sign = 1;
//                         }
//                         CurrentActorPointer_0->hSpeed = (float)(currentCharSpawner->max_aggro_speed) * 1.8f;
//                         CurrentActorPointer_0->rot_y += (angle_sign * 400);
//                         CurrentActorPointer_0->rot_y_copy = CurrentActorPointer_0->rot_y;
//                         paad->scared_bitfield |= 0x8000;
//                         CurrentActorPointer_0->control_state = 0x10;
//                         CurrentActorPointer_0->control_state_progress = 0;
//                     }
//                 }
//             }
//             if (CurrentActorPointer_0->control_state == 0x40) {
//                 EnemiesKilledCounter += 1;
//             }
//         }
//     }
//     beaverControlSwitchCase(0x1FA,0,0);
//     int p = 2;
//     if (CurrentActorPointer_0->control_state == 0x23) {
//         p = 0;
//     }
//     unkCutsceneKongFunction_1(p);
//     renderActor(CurrentActorPointer_0,0);
// }

void beaverExtraHitHandle(void) {
    if (CurrentActorPointer_0->actorType == 212) {
        // Is Gold Beaver
        if ((CurrentActorPointer_0->subdata == 2) && (CurrentActorPointer_0->control_state != 0x36)) {
            if (CurrentActorPointer_0->control_state == 0x40) { // Has been killed
                EnemiesKilledCounter += 1;
            }
        }
    }
    beaverControlSwitchCase(0x1FA,0,0);
}