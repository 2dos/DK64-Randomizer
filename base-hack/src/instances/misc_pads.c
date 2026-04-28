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

typedef enum helm_prog_enum {
    /* 0 */ HELMPROG_MONKEYPORT,
    /* 1 */ HELMPROG_GONE,
} helm_prog_enum;

ROM_DATA static kongs monkeyport_kongs[] = {KONG_TINY, KONG_DK, KONG_LANKY, KONG_TINY, KONG_TINY}; // Kongs used for the switchsanity setting for lower monkeyport in Isles

int hasHelmProgMove(helm_prog_enum sub_id) {
    // 0 = Monkeyport pad, 1 = Gone Pad
    if (sub_id == HELMPROG_MONKEYPORT) {
        if (Rando.switchsanity_monkeyport == 0) {
            return MovesBase[KONG_TINY].special_moves & MOVECHECK_MONKEYPORT;
        } else if (Rando.switchsanity_monkeyport == 1) {
            return MovesBase[KONG_DK].special_moves & MOVECHECK_BLAST;
        } else if (Rando.switchsanity_monkeyport == 2) {
            return MovesBase[KONG_LANKY].special_moves & MOVECHECK_BALLOON;
        }
    } else if (sub_id == HELMPROG_GONE) {
        if (Rando.switchsanity_gone == 0) {
            return MovesBase[KONG_CHUNKY].special_moves & MOVECHECK_GONE;
        } else if (Rando.switchsanity_gone == 6) {
            return MovesBase[KONG_DK].special_moves & MOVECHECK_GRAB;
        } else if (Rando.switchsanity_gone == 7) {
            return MovesBase[KONG_DIDDY].special_moves & MOVECHECK_CHARGE;
        } else {
            return MovesBase[Rando.switchsanity_gone - 1].instrument_bitfield & 1;
        }
    }
    return 0;
}

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

int ableToUseMonkeyport(int id) {
    if (Player) {
        if ((Player->obj_props_bitfield & 0x2000) == 0) {
            if (standingOnM2Object(id)) {
                int mport_kong = Rando.switchsanity_monkeyport;
                if (mport_kong == 0) {
                    // Set Monkeyport thing
                    return Player->characterID == KONG_TINY;
                } else {
                    if (((unsigned int)Player->characterID == monkeyport_kongs[mport_kong] + 2)) {
                        if (mport_kong == 1) {
                            // Blast
                            createCollisionObjInstance(COLLISION_BBLAST, MAP_ISLES, 0);
                        } else if (mport_kong == 2) {
                            // Balloon
                            createCollisionObjInstance(COLLISION_BABOON_BALLOON, 15, 0);	
                        }
                    }
                }
            }
        }
    }
    return 0;
}

void IslesMonkeyportCode(behaviour_data* behaviour_pointer, int index) {
    int current_state = behaviour_pointer->current_state;
    if (current_state == 0) {
        if (!hasHelmProgMove(HELMPROG_MONKEYPORT)) {
            setObjectOpacity(behaviour_pointer, 70);
            behaviour_pointer->next_state = 5;
        } else {
            setScriptRunState(behaviour_pointer, RUNSTATE_DISTANCERUN, 300);
            behaviour_pointer->next_state = 1;
        }
    } else if (current_state == 1) {
        // Use the move
        if (ableToUseMonkeyport(index)) {
            setObjectScriptState(55, 20, 0);
            int tied_index = convertIDToIndex(55);
            if (tied_index > -1) {
                behaviour_data* tied_behaviour = ObjectModel2Pointer[tied_index].behaviour_pointer;
                if (tied_behaviour) {
                    setScriptRunState(tied_behaviour, RUNSTATE_RUNNING, 0);
                }
            }
        }
    } else if (current_state == 5) {
        if (hasHelmProgMove(HELMPROG_MONKEYPORT)) {
            setObjectOpacity(behaviour_pointer, 255);
            setScriptRunState(behaviour_pointer, RUNSTATE_DISTANCERUN, 300);
            behaviour_pointer->next_state = 1;
        } else {
            if (canOpenXBlockers(7)) {
                if (standingOnM2Object(index)) {
                    PlayCutsceneFromModelTwoScript(behaviour_pointer, 24, 1, 0);
                    behaviour_pointer->next_state = 6;
                }
            }
        }
    } else if (current_state == 6) {
        if (!standingOnM2Object(index)) {
            if (CutsceneActive != 1) {
                behaviour_pointer->next_state = 5;
            }
        }
    } else if (current_state == 20) {
        createCollision(0, Player, COLLISION_MONKEYPORT_WARP, 0, 0, *(int*)(0x807F621C),*(int*)(0x807F6220),*(int*)(0x807F6224));
        behaviour_pointer->next_state = 0;
    }
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