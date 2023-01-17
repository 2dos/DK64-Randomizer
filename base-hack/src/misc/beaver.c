/**
 * @file beaver.c
 * @author Ballaam
 * @brief Any changes relevant for beavers
 * @version 0.1
 * @date 2022-07-24
 * 
 * @copyright Copyright (c) 2023
 * 
 */

#include "../../include/common.h"

void beaverExtraHitHandle(void) {
    /**
     * @brief Handle the extra hit detection for gold beavers in Beaver Bother
     */
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