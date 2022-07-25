#include "../../include/common.h"

static char warp_timer = 0;
static unsigned char bad_guard_states[] = {
    0x18, // BBlast Pad
    0x52, // Bananaport
    0x53, // Monkeyport
    0x54, // MP Bananaport
    0x67, // Instrument
};

typedef struct guard_paad {
    /* 0x000 */ char unk_00[0xA];
    /* 0x00A */ short x_something;
    /* 0x00C */ char unk_0C[0x2];
    /* 0x00E */ short z_something;
    /* 0x010 */ char unk_10[0x1A-0x10];
    /* 0x01A */ short unk_1A;
} guard_paad;

int isBadMovementState(void) {
    if (Player) {
        int control_state = Player->control_state;
        for (int i = 0; i < sizeof(bad_guard_states); i++) {
            if (control_state == bad_guard_states[i]) {
                return 1;
            }
        }
        return 0;
    }
    return 1;
}

void guardCatch(void) {
    if (Player) {
        if ((warp_timer == 0) && (TransitionSpeed == 0) && (!isBadMovementState()) && (CutsceneActive == 0)) {
            warp_timer = 80;
            tagKong(Player->new_kong);
            Player->noclip = 1;
            if (Player->control_state != 0x7D) {
                if ((Player->grounded_bitfield & 4) == 0) {
                    if ((Player->grounded_bitfield & 2) == 0) {
                        playAnimation(Player,0x5D);
                    }
                } else {
                    playAnimation(Player,0x34);
                }
            }
            Player->control_state = 0x70;
            Player->control_state_progress = 0;
            Player->yVelocity = 0;
            Player->hSpeed = 0;
            playSong(42,0x3F800000);
        }
    }
}

void catchWarpHandle(void) {
    if (warp_timer > 0) {
        if ((warp_timer == 1) && (TransitionSpeed == 0)) {
            if ((CurrentMap == 0x11) && (Rando.fast_start_helm > 0)) {
                if (Rando.fast_start_helm == 1) {
                    initiateTransition(0x11,3);
                } else if (Rando.fast_start_helm == 2) {
                    initiateTransition(0x11,4);
                } else {
                    voidWarp();
                }
            } else {
                voidWarp();
            }
        }
        warp_timer -= 1;
    }
    if (TransitionSpeed != 0) {
        warp_timer = 0;
    }
}

void guardCode(void) {
    initCharSpawnerActor();
    guard_paad* paad = CurrentActorPointer_0->paad;
    int update_state = 1;
    int p = 0;
    unsigned int level_state = *(unsigned int*)(0x807FBB64);
    if ((CurrentActorPointer_0->obj_props_bitfield & 0x10) == 0) {
        modifyCharSpawnerAttributes(0x2C0,0x2C1,0x2C1);
        unkCutsceneKongFunction_0(0xE,1);
        paad->unk_1A |= 0x800;
        CurrentActorPointer_0->obj_props_bitfield |= 0x400;
    }
    handleGuardDetection(40.0f,70.0f);
    TestVariable = collisionType;
    *(int*)(0x807FF700) = collisionActive;
    if ((collisionType == 4) || (collisionType == 9) || (collisionActive)) {
        if ((level_state & 0x104000) == 0) {
            // Hit by ammo/oranges
            if (CurrentActorPointer_0->health <= 0) {
                playActorAnimation(CurrentActorPointer_0,0x201);
                CurrentActorPointer_0->control_state = 0x42;
                CurrentActorPointer_0->control_state_progress = 0;
                // CurrentActorPointer_0->yVelocity = 150.0f;
                // CurrentActorPointer_0->yAccel = -20.0f;
            } else {
                playActorAnimation(CurrentActorPointer_0,0x1FF);
                CurrentActorPointer_0->control_state = 0x41;
                CurrentActorPointer_0->control_state_progress = 0;
            }
        }
    }
    int control_state = CurrentActorPointer_0->control_state;
    if (control_state > 0x35) {
        if (control_state == 0x37) {
            CurrentActorPointer_0->control_state = 0x40;
            CurrentActorPointer_0->control_state_progress = 0;
        } else if (control_state < 0x41) {
            handleGuardDefaultAnimation();
        } else {
            switch(control_state) {
                case 0x41:
                    // Damage
                    if (CurrentActorPointer_0->control_state_progress < 0x10) {
                        CurrentActorPointer_0->control_state_progress += 1;
                    } else {
                        CurrentActorPointer_0->control_state = 0x1;
                        CurrentActorPointer_0->control_state_progress = 0;
                    }
                    break;
                case 0x42:
                    // Death
                    if (CurrentActorPointer_0->control_state_progress < 0x10) {
                        CurrentActorPointer_0->control_state_progress += 1;
                    } else {
                        CurrentActorPointer_0->control_state = 0x37;
                        CurrentActorPointer_0->control_state_progress = 1;
                    }
                break;
            }
        }
    }
    if (control_state < 0x12) {
        switch(control_state) {
            case 1:
                if (guardShouldMove()) {
                    CurrentActorPointer_0->control_state = 0x11;
                    CurrentActorPointer_0->control_state_progress = 0;
                }
                p = 0;
                if (CurrentActorPointer_0->control_state == 1) {
                    p = 2;
                }
                guardUnkFunction(p);
                generalActorHandle(CurrentActorPointer_0->control_state, *(int*)(&PlayerPointer_0->xPos), *(int*)(&PlayerPointer_0->zPos), 0, 0.0f);
                break;
            case 2:
            case 3:
            case 7:
                p = 3;
                if (control_state == 0x35) {
                    p = 2;
                }
                guardUnkFunction(p);
                generalActorHandle(CurrentActorPointer_0->control_state, paad->x_something, paad->z_something, 0, 0.0f);
                break;
            case 0x11:
                guardUnkFunction(2);
                int csp = CurrentActorPointer_0->control_state_progress;
                if (csp == 0) {
                    setActorSpeed(CurrentActorPointer_0,0);
                    playActorAnimation(CurrentActorPointer_0,0x2C0);
                    CurrentActorPointer_0->control_state_progress += 1;
                } else {
                    if (csp == 1) {
                        generalActorHandle(CurrentActorPointer_0->control_state, *(int*)(&PlayerPointer_0->xPos), *(int*)(&PlayerPointer_0->zPos), 0, 0.0f);
                        if (CurrentActorPointer_0->hSpeed >= 1.0f) {
                            control_state = CurrentActorPointer_0->control_state;
                        } else {
                            CurrentActorPointer_0->control_state_progress += 1;
                        }
                    } else if (csp == 2) {
                        actorUnkFunction();
                        int rng = getRNGLower31();
                        int rng_subset = (rng >> 0xF) & 1000;
                        if (rng_subset > 995) {
                            setActorAnimation(0x2C1);
                        }
                    } else {
                        control_state = CurrentActorPointer_0->control_state;
                    }
                }
                break;
            default:
                handleGuardDefaultAnimation();
            break;
        }
    } else {
        if (control_state != 0x35) {
            handleGuardDefaultAnimation();
        } else if (control_state < 0x41) {
            p = 3;
            if (control_state == 0x35) {
                p = 2;
            }
            guardUnkFunction(p);
            generalActorHandle(CurrentActorPointer_0->control_state, paad->x_something, paad->z_something, 0, 0.0f);
        }
    }
    if (update_state == 1) {
        control_state = CurrentActorPointer_0->control_state;
    }
    if ((control_state == 2) || (control_state == 3)) {
        actorUnkFunction_0(control_state,1);
    }
    renderActor(CurrentActorPointer_0,0);
    
    // if ((level_state & 0x104000) == 0) {
    //     if ((CurrentActorPointer_0->control_state == 0x16) || ((CurrentActorPointer_0->health <= 0) && (CurrentActorPointer_0->control_state < 0x35))) {
    //         CurrentActorPointer_0->control_state = 0x37;
    //         CurrentActorPointer_0->control_state_progress = 1;
    //         spawnSparkles(CurrentActorPointer_0->xPos, CurrentActorPointer_0->yPos, CurrentActorPointer_0->zPos, 20);
    //         playSFX(493);
    //     } else if (CurrentActorPointer_0->control_state == 0x37) {
    //         CurrentActorPointer_0->control_state = 0x40;
    //         CurrentActorPointer_0->control_state_progress = 0;
    //     }
    // }
}