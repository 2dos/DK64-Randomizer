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
    if (sub_id == 0) {
        if (Rando.switchsanity.isles.monkeyport == 0) {
            return MovesBase[KONG_TINY].special_moves & MOVECHECK_MONKEYPORT;
        } else if (Rando.switchsanity.isles.monkeyport == 2) {
            return MovesBase[KONG_LANKY].special_moves & MOVECHECK_BALLOON;
        }
    } else if (sub_id == 1) {
        if (Rando.switchsanity.isles.gone == 0) {
            return MovesBase[KONG_CHUNKY].special_moves & MOVECHECK_GONE;
        } else {
            return MovesBase[Rando.switchsanity.isles.gone - 1].instrument_bitfield & 1;
        }
    }
    return 0;
}

int hasEnoughGBsMicrohint(int level_cap) {
    int gb_count = getTotalGBs();
    int max_gbs = 0;
    for (int level = 0; level < level_cap; level++) {
        if (BLockerDefaultArray[level] > max_gbs) {
            max_gbs = BLockerDefaultArray[level];
        }
    }
    return (gb_count >= max_gbs) && (Rando.microhints != MICROHINTS_NONE); 
}

int ableToUseMonkeyport(int id) {
    if (Player) {
        if ((Player->obj_props_bitfield & 0x2000) == 0) {
            if (Player->touching_object == 1) {
                if (Player->standing_on_index == id) {
                    int mport_kong = Rando.switchsanity.isles.monkeyport;
                    if (mport_kong == 0) {
                        // Set Monkeyport thing
                        return (Player->characterID == 5) || (Rando.perma_lose_kongs);
                    } else {
                        if ((Player->characterID == monkeyport_kongs[mport_kong] + 2) || (Rando.perma_lose_kongs)) {
                            if (mport_kong == 1) {
                                // Blast
                                // fun_80608528 - sfx player
                                Player->control_state = 0x18;
                                Player->control_state_progress = 0;
                                Player->noclip = 1;
                                Player->blast_y_velocity = 200.0f;
                                Player->ostand_value = 0x28;
                                playAnimation(Player, 0x22);
                            } else if (mport_kong == 2) {
                                // Balloon
                                createCollisionObjInstance(COLLISION_BABOON_BALLOON, 80, 200);	
                            }
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
            behaviour_pointer->unk_60 = 1;
            behaviour_pointer->unk_62 = 70;
            behaviour_pointer->unk_66 = 255;
            behaviour_pointer->next_state = 5;
        } else {
            setScriptRunState(behaviour_pointer, 3, 300);
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
                    setScriptRunState(tied_behaviour,1,0);
                }
            }
        }
    } else if (current_state == 5) {
        if (hasEnoughGBsMicrohint(7)) {
            if (Player->touching_object == 1) {
                if (Player->standing_on_index == index) {
                    PlayCutsceneFromModelTwoScript(behaviour_pointer, 24, 1, 0);
                    behaviour_pointer->next_state = 6;
                }
            }
        }
    } else if (current_state == 6) {
        if (Player->touching_object == 1) {
            if (Player->standing_on_index == index) {
                if (CutsceneActive != 1) {
                    behaviour_pointer->next_state = 5;
                }
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

void HelmLobbyGoneCode(behaviour_data* behaviour_pointer, int index) {
    int current_state = behaviour_pointer->current_state;
    int sub_type = Rando.switchsanity.isles.gone;
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
            behaviour_pointer->unk_60 = 1;
            behaviour_pointer->unk_62 = 70;
            behaviour_pointer->unk_66 = 255;
            behaviour_pointer->next_state = 5;
        } else {
            setScriptRunState(behaviour_pointer, 3, 300);
            behaviour_pointer->next_state = 1;
        }
    }
    if (current_state == 1) {
        if (Player->characterID == getHelmLobbyGoneReqKong()) {
            if (Player->touching_object == 1) {
                if (Player->standing_on_index == index) {
                    if (hasHelmProgMove(HELMPROG_GONE)) {
                        if (sub_type == 0) {
                            createCollisionObjInstance(COLLISION_GORILLA_GONE, -1, 0);
                        } else if (Player->control_state == 103) {
                            setScriptRunState(behaviour_pointer, 1, 0);
                            behaviour_pointer->next_state = 7;
                        }
                        
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
        if (hasEnoughGBsMicrohint(8)) {
            if (Player->touching_object == 1) {
                if (Player->standing_on_index == index) {
                    PlayCutsceneFromModelTwoScript(behaviour_pointer, 3, 1, 0);
                    behaviour_pointer->next_state = 6;
                }
            }
        }
    } else if (current_state == 6) {
        if (Player->touching_object == 1) {
            if (Player->standing_on_index == index) {
                if (CutsceneActive != 1) {
                    behaviour_pointer->next_state = 5;
                }
            }
        }
    } else if (current_state == 7) {
        // Instrument specific stuff
        if (CutsceneActive != 1) {
            // Show Vines
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
            behaviour_pointer->timer = 15;
            behaviour_pointer->next_state = 2;
        }
    }
}

void initHelmLobbyBonusChange(void) {
    if (Rando.switchsanity.isles.gone != 0) {
        *(short*)(0x80680E3A) = getHi(&bonus_shown);
        *(int*)(0x80680E3C) = 0x91EF0000 | getLo(&bonus_shown); // lbu $t7, lo(bonus_shown) ($t7)
        *(int*)(0x80680E48) = 0; // nop
        *(int*)(0x80680E54) = 0x51E00009; // beql $t7, $zero, 0x9
    }
}