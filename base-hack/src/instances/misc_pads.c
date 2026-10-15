/**
 * @file misc_pads.c
 * @author Ballaam
 * @brief Functions related to miscellaneous pads, namely Isles Port & Helm Lobby Gone
 * @version 0.1
 * @date 2023-10-23
 * 
 * @copyright Copyright (c) 2023
 * 
 */

#include "../../include/common.h"

int canOpenSpecificBLocker(int level) {
    ItemRequirement req = {.count = BLockerDefaultArray[level], .item = Rando.b_locker_requirements[level]};
    if (!isItemRequirementSatisfied(&req)) {
        return 0;
    }
    return Rando.microhints != MICROHINTS_NONE;
}

int canOpenXBlockers(int count) {
    int openable = 8;
    for (int level = 0; level < 8; level++) {
        ItemRequirement req = {.count = BLockerDefaultArray[level], .item = Rando.b_locker_requirements[level]};
        if (!isItemRequirementSatisfied(&req)) {
            openable--;
        }
    }
    if (openable < count) {
        return 0;
    }
    return Rando.microhints != MICROHINTS_NONE; 
}

void activateGonePad(void) {
    actorSpawnerData* spawner = ActorSpawnerPointer;
    if (spawner) {
        while (spawner) {
            if (spawner->id < 9) { // Vine
                spawner->can_hide_vine = 0;
            }
            spawner = spawner->next_spawner;
            if (!spawner) {
                break;
            }
        }
    }
    bonus_shown = 1;
}