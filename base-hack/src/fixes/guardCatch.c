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

void WarpHandle(void) {
    if (CurrentMap == 0x11) {
        if (Rando.fast_start_helm == 2) { // Skip All
            initiateTransition(0x11,4); // Crown Door
        } else if (checkFlag(FLAG_HELM_ROMANDOORS_OPEN,2) || checkFlag(FLAG_MODIFIER_HELMBOM,0)) { // Roman Doors Open or BoM off
            initiateTransition(0x11,3); // Lever
        } else {
            initiateTransition(0x11,0); // Start
        }
        setFlag(0x50,0,2); // Prevent Helm Door hardlock
    } else {
        voidWarp();
    }
}

void catchWarpHandle(void) {
    if (warp_timer > 0) {
        if ((warp_timer == 1) && (TransitionSpeed == 0)) {
            WarpHandle();
        }
        warp_timer -= 1;
    }
    if (TransitionSpeed != 0) {
        warp_timer = 0;
    }
}

void newGuardCode(void) {
    unsigned int level_state = *(unsigned int*)(0x807FBB64);
    if (CurrentActorPointer_0->control_state <= 0x35) {
        handleGuardDetection(40.0f,70.0f);
    }
    if ((collisionType == 4) || (collisionType == 9) || (collisionActive)) {
        if ((level_state & 0x104000) == 0) {
            // Hit by ammo/oranges
            if ((CurrentActorPointer_0->health <= 0) || (collisionActive)) {
                CurrentActorPointer_0->health = 0;
                playActorAnimation(CurrentActorPointer_0,0x201);
                CurrentActorPointer_0->control_state = 0x42;
                CurrentActorPointer_0->control_state_progress = 0;
                CurrentActorPointer_0->noclip_byte = 1;
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
            spawnEnemyDrops(CurrentActorPointer_0);
        } else {
            handleGuardDefaultAnimation();
            switch(control_state) {
                case 0x41:
                    // Damage
                    if (CurrentActorPointer_0->control_state_progress < 0xC) {
                        CurrentActorPointer_0->control_state_progress += 1;
                    } else {
                        setActorAnimation(0x2C1);
                    }
                    break;
                case 0x42:
                    // Death
                    if (CurrentActorPointer_0->control_state_progress < 0x20) {
                        CurrentActorPointer_0->control_state_progress += 1;
                    } else {
                        CurrentActorPointer_0->control_state = 0x37;
                        CurrentActorPointer_0->control_state_progress = 1;
                    }
                break;
            }
        }
    }
}