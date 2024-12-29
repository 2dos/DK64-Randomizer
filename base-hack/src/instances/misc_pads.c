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

static const kongs monkeyport_kongs[] = {KONG_TINY, KONG_DK, KONG_LANKY, KONG_TINY, KONG_TINY}; // Kongs used for the switchsanity setting for lower monkeyport in Isles

int hasHelmProgMove(helm_prog_enum sub_id) {
    // 0 = Monkeyport pad, 1 = Gone Pad
    if (sub_id == HELMPROG_MONKEYPORT) {
        if (Rando.switchsanity.isles.monkeyport == 0) {
            return MovesBase[KONG_TINY].special_moves & MOVECHECK_MONKEYPORT;
        } else if (Rando.switchsanity.isles.monkeyport == 1) {
            return MovesBase[KONG_DK].special_moves & MOVECHECK_BLAST;
        } else if (Rando.switchsanity.isles.monkeyport == 2) {
            return MovesBase[KONG_LANKY].special_moves & MOVECHECK_BALLOON;
        }
    } else if (sub_id == HELMPROG_GONE) {
        if (Rando.switchsanity.isles.gone == 0) {
            return MovesBase[KONG_CHUNKY].special_moves & MOVECHECK_GONE;
        } else if (Rando.switchsanity.isles.gone == 6) {
            return MovesBase[KONG_DK].special_moves & MOVECHECK_GRAB;
        } else if (Rando.switchsanity.isles.gone == 7) {
            return MovesBase[KONG_DIDDY].special_moves & MOVECHECK_CHARGE;
        } else {
            return MovesBase[Rando.switchsanity.isles.gone - 1].instrument_bitfield & 1;
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

int canOpenAllBLockersUntil(int level_cap) {
    for (int level = 0; level < level_cap; level++) {
        ItemRequirement req = {.count = BLockerDefaultArray[level], .item = Rando.b_locker_requirements[level]};
        if (!isItemRequirementSatisfied(&req)) {
            return 0;
        }
    }
    return Rando.microhints != MICROHINTS_NONE; 
}

int ableToUseMonkeyport(int id) {
    if (Player) {
        if ((Player->obj_props_bitfield & 0x2000) == 0) {
            if (standingOnM2Object(id)) {
                int mport_kong = Rando.switchsanity.isles.monkeyport;
                if (mport_kong == 0) {
                    // Set Monkeyport thing
                    return (Player->characterID == 5) || (Rando.perma_lose_kongs);
                } else {
                    if ((Player->characterID == monkeyport_kongs[mport_kong] + 2) || (Rando.perma_lose_kongs)) {
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
                int* m2location = (int*)ObjectModel2Pointer;
                ModelTwoData* tied_object = getObjectArrayAddr(m2location,0x90,tied_index);
                behaviour_data* tied_behaviour = (behaviour_data*)tied_object->behaviour_pointer;
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
            if (canOpenAllBLockersUntil(7)) {
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

int getHelmLobbyGoneReqKong(void) {
    int sub_type = Rando.switchsanity.isles.gone;
    if (sub_type == 0) {
        return KONG_CHUNKY + 2;
    }
    return sub_type + 1;
}

static char bonus_shown = 0;

void blastWarpContainer(maps map, int wrongCSEnabled) {
    int exit = 0;
    if (map == MAP_ISLES) {
        exit = 23;
    }
    if (wrongCSEnabled) {
        setIntroStoryPlaying(2);
        setNextTransitionType(0);
    }
    initiateTransition_0(map, exit, 0, 0);
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

#define GRAB_STATE 120

void HelmLobbyGoneLeverCode(behaviour_data* behaviour_pointer, int index) {
    int current_state = behaviour_pointer->current_state;
    if (current_state == 0) {
        bonus_shown = 0;
        behaviour_pointer->next_state = 1;
    } else if (current_state == 1) {
        unkObjFunction1(index, 1, 85);
        unkObjFunction0(index, 1, 1);
        setScriptRunState(behaviour_pointer, RUNSTATE_DISTANCERUN, 300);
        behaviour_pointer->next_state = 2;
        behaviour_pointer->unk_6F = 0;
        unkObjFunction9(index, 1, 1);
        displayImageOnObject(index, 1, 0, 0);
        unkObjFunction7(index, 1, 0);
    } else if (current_state == 2) {
        if ((Player->obj_props_bitfield & 0x2000) == 0) {
            if (Player->characterID == 2) {
                if (standingOnM2Object(index)) {
                    if (Player->standing_on_subposition == 2) {
                        if (MovesBase[KONG_DK].special_moves & MOVECHECK_GRAB) {
                            if (checkLeverAngle()) {
                                float x = 0;
                                float y = 0;
                                float z = 0;
                                getObjectPosition(index, 1, 1, &x, &y, &z);
                                Player->grab_x = x;
                                Player->grab_y = y;
                                Player->grab_z = z;
                                createCollision(0, Player, COLLISION_GRAB, 0, 0, *(int*)(0x807F621C),*(int*)(0x807F6220),*(int*)(0x807F6224));
                                behaviour_pointer->counter_next = 1;
                                behaviour_pointer->timer = 5;
                            }
                        } else {
                            // Microhints
                            behaviour_pointer->next_state = 7;
                            return;
                        }
                    }
                }
            }
        }
    }
    if (behaviour_pointer->counter == 1) {
        if (behaviour_pointer->timer == 0) {
            behaviour_pointer->counter_next = 0;
        } else {
            if (Player->control_state == GRAB_STATE) {
                setScriptRunState(behaviour_pointer, RUNSTATE_RUNNING, 0);
                behaviour_pointer->next_state = 3;
                behaviour_pointer->counter_next = 0;
            }
        }
    }
    if (current_state == 3) {
        if (getAnimationTimer(Player) > 114) {
            displayImageOnObject(index, 1, 1, 0);
            unkObjFunction2(index, 1, 1);
            playSFXFromObject(index, 459, 255, 127, 0, 0, 0.3f);
            behaviour_pointer->next_state = 4;
        }
    } else if (current_state == 4) {
        if (getAnimationTimer(Player) > 155) {
            activateGonePad();
            playSFXFromObject(index, 459, 255, 127, 0, 0, 0.3f);
            unkObjFunction2(index, 1, 1);
            behaviour_pointer->next_state = 5;
        }
    } else if (current_state == 5) {
        if (!unkObjFunction8(index, 1)) {
            displayImageOnObject(index, 1, 0, 0);
            behaviour_pointer->next_state = 6;
        }
    } else if (current_state == 6) {
        if (Player->control_state != GRAB_STATE) {
            behaviour_pointer->next_state = 11;
        }
    } else if (current_state == 7) {
        if (hasHelmProgMove(HELMPROG_GONE)) {
            setObjectOpacity(behaviour_pointer, 255);
            behaviour_pointer->next_state = 1;
        } else {
            if (canOpenSpecificBLocker(7)) {
                if ((standingOnM2Object(index)) && (Player->standing_on_subposition == 2)) {
                    PlayCutsceneFromModelTwoScript(behaviour_pointer, 3, 1, 0);
                    behaviour_pointer->next_state = 8;
                }
            }
        }
    } else if (current_state == 8) {
        if ((!standingOnM2Object(index)) || ((Player->standing_on_subposition != 2))) {
            if (CutsceneActive != 1) {
                behaviour_pointer->next_state = 7;
            }
        }
    }
    if ((current_state >= 2) && (current_state < 5)) {
        if (Player->control_state != GRAB_STATE) {
            displayImageOnObject(index, 1, 0, 0);
            unkObjFunction10(index, 1, 0, 0);
            unkObjFunction17(index, 1, 0);
            unkObjFunction1(index, 1, 0);
            unkObjFunction2(index, 1, 1);
            behaviour_pointer->next_state = 10;
        }
    } else if (current_state == 10) {
        unkObjFunction11(index, 1);
        behaviour_pointer->next_state = 1;
    }
}

int inRangeOfGong(void) {
    int dx = Player->xPos - 451;
    int dz = Player->zPos - 334;
    int dxz2 = (dx * dx) + (dz * dz);
    if (dxz2 < 400) {
        return 1;
    }
    return 0;
}

void HelmLobbyGoneGongCode(behaviour_data* behaviour_pointer, int index) {
    int current_state = behaviour_pointer->current_state;
    if (current_state == 0) {
        behaviour_pointer->unk_6F = 1;
        setScriptRunState(behaviour_pointer, RUNSTATE_DISTANCERUN, 400);
        for (int i = 0; i < 4; i++) {
            unkObjFunction7(index, i + 1, 0);
        }
        behaviour_pointer->next_state = 10;
        behaviour_pointer->current_state = 10;
        bonus_shown = 0;
    } else if (current_state == 5) {
        if (hasHelmProgMove(HELMPROG_GONE)) {
            behaviour_pointer->next_state = 10;
            behaviour_pointer->current_state = 10;
            return;
        }
        if (inRangeOfGong()) {
            if (canOpenSpecificBLocker(7)) {
                PlayCutsceneFromModelTwoScript(behaviour_pointer, 3, 1, 0);
                behaviour_pointer->next_state = 6;
                behaviour_pointer->current_state = 6;
            }
            return;
        }
    } else if (current_state == 6) {
        if (CutsceneActive != 1) {
            if (inRangeOfGong() == 0) {
                behaviour_pointer->next_state = 5;
                behaviour_pointer->current_state = 5;
                return;
            }
        }
    } else if (current_state == 10) {
        if (!hasHelmProgMove(HELMPROG_GONE)) {
            behaviour_pointer->next_state = 5;
            behaviour_pointer->current_state = 5;
            return;
        }
        if (behaviour_pointer->switch_pressed == 1) {
            if (behaviour_pointer->contact_actor_type == 3) {
                if (canHitSwitch()) {
                    setSomeTimer(0xC3);
                    if (Player->control_state == 46) {
                        if (Player->control_state_progress == 1) {
                            // Player->unk_fairycam_bitfield |= 0x20;
                            unkObjFunction1(index, 1, 200);
                            unkObjFunction10(index, 1, 0, 0);
                            unkObjFunction2(index, 1, 1);
                            behaviour_pointer->timer = 50;
                            for (int i = 0; i < 4; i++) {
                                unkObjFunction7(index, i + 1, 0);
                            }
                            unkObjFunction0(index, 1, 0);
                            playSFXFromObject(index, 165, 255, 95, 5, 60, 0.3f);
                            setScriptRunState(behaviour_pointer, RUNSTATE_RUNNING, 0);
                            behaviour_pointer->next_state = 11;
                        }
                    }
                }
            }
        }
    } else if (current_state == 11) {
        if (behaviour_pointer->timer == 10) {
            if (behaviour_pointer->unk_10 < 0) {
                behaviour_pointer->unk_10 = unkObjFunction12(index, 282, 0, 0, 100, 1, 0);
            }
            unkObjFunction1(index, 2, 3);
            unkObjFunction2(index, 2, 1);
        } else if (behaviour_pointer->timer == 0) {
            for (int i = 0; i < 4; i++) {
                unkObjFunction7(index, i + 1, 0);
            }
            // Player->unk_fairycam_bitfield &= ~0x20;
            activateGonePad();
            behaviour_pointer->next_state = 12;
        }
    } else if (current_state == 12) {
        if (unkObjFunction8(index, 2) == 0) {
            if (behaviour_pointer->unk_10 > -1) {
                unkObjFunction14(behaviour_pointer->unk_10);
                behaviour_pointer->unk_10 = -1;
            }
            behaviour_pointer->unk_60 = 1;
            behaviour_pointer->unk_62 = 0;
            behaviour_pointer->unk_66 = 255;
            behaviour_pointer->unk_70 = 0;
            setScriptRunState(behaviour_pointer, RUNSTATE_PAUSED, 0);
        }
    }
}

void HelmLobbyGoneCode(behaviour_data* behaviour_pointer, int index) {
    int sub_type = Rando.switchsanity.isles.gone;
    if (sub_type == 6) {
        HelmLobbyGoneLeverCode(behaviour_pointer, index);
        return;
    } else if (sub_type == 7) {
        HelmLobbyGoneGongCode(behaviour_pointer, index);
        return;
    }
    int current_state = behaviour_pointer->current_state;
    if (current_state == 0) {
        if (sub_type == 0) { // Is Gone
            if (isBonus(PreviousMap)) {
                *(int*)(0x807FD6F0) = -1;
                *(int*)(0x807FD6F4) = 0;
                *(int*)(0x807FD6F8) = 0;
                setAction(58, (void*)0, 0);
                behaviour_pointer->counter_next = 1;
            }
        }
        bonus_shown = 0;
        if (!hasHelmProgMove(HELMPROG_GONE)) {
            setObjectOpacity(behaviour_pointer, 70);
            behaviour_pointer->next_state = 5;
        } else {
            setScriptRunState(behaviour_pointer, RUNSTATE_DISTANCERUN, 300);
            behaviour_pointer->next_state = 1;
        }
    }
    if (current_state == 1) {
        if (Player->characterID == getHelmLobbyGoneReqKong()) {
            if (standingOnM2Object(index)) {
                if (hasHelmProgMove(HELMPROG_GONE)) {
                    if (sub_type == 0) {
                        createCollisionObjInstance(COLLISION_GORILLA_GONE, -1, 0);
                    } else if (Player->control_state == 103) {
                        setScriptRunState(behaviour_pointer, RUNSTATE_RUNNING, 0);
                        behaviour_pointer->next_state = 7;
                    }
                    
                }
            }
        }
        if (sub_type == 0) {
            if (Player->state_bitfield & 0x40) {
                behaviour_pointer->timer = 15;
                behaviour_pointer->next_state = 2;
            }
        }
    } else if (current_state == 2) {
        if (behaviour_pointer->timer == 0) {
            if (behaviour_pointer->counter == 0) {
                PlayCutsceneFromModelTwoScript(behaviour_pointer, 1, 1, 0);
                behaviour_pointer->timer = 200;
                behaviour_pointer->counter_next = 1;
                behaviour_pointer->next_state = 3;
            } else if (behaviour_pointer->counter == 1) {
                behaviour_pointer->timer = 20;
                behaviour_pointer->next_state = 3;
            }
        }
    } else if (current_state == 3) {
        if (behaviour_pointer->timer == 0) {
            behaviour_pointer->next_state = 4;
        }
    } else if (current_state == 4) {
        if (sub_type == 0) {
            if ((Player->state_bitfield & 0x40) == 0) { // Not in gone
                behaviour_pointer->next_state = 1;
            }
        }
    } else if (current_state == 5) {
        if (hasHelmProgMove(HELMPROG_GONE)) {
            setObjectOpacity(behaviour_pointer, 255);
            setScriptRunState(behaviour_pointer, RUNSTATE_DISTANCERUN, 300);
            behaviour_pointer->next_state = 1;
        } else {
            if (canOpenSpecificBLocker(7)) {
                if (standingOnM2Object(index)) {
                    PlayCutsceneFromModelTwoScript(behaviour_pointer, 3, 1, 0);
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
    } else if (current_state == 7) {
        // Instrument specific stuff
        if (CutsceneActive != 1) {
            // Show Vines
            activateGonePad();
            behaviour_pointer->timer = 15;
            behaviour_pointer->next_state = 2;
        }
    }
}

void initSwitchsanityChanges(void) {
    if (Rando.switchsanity.isles.gone != 0) {
        *(short*)(0x80680E3A) = getHi(&bonus_shown);
        *(int*)(0x80680E3C) = 0x91EF0000 | getLo(&bonus_shown); // lbu $t7, lo(bonus_shown) ($t7)
        *(int*)(0x80680E48) = 0; // nop
        *(int*)(0x80680E54) = 0x51E00009; // beql $t7, $zero, 0x9
    }
    if (Rando.switchsanity.isles.monkeyport == 1) {
        *(short*)(0x806E5A4A) = getHi(&blastWarpContainer);
        *(short*)(0x806E5A4E) = getLo(&blastWarpContainer);
    }
}