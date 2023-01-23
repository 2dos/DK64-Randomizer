/**
 * @file guardCatch.c
 * @author Ballaam
 * @brief All functions associated with the guard actor normally present in Stealthy Snoop
 * @version 0.1
 * @date 2022-07-07
 * 
 * @copyright Copyright (c) 2022
 * 
 */
#include "../../include/common.h"

static char warp_timer = 0; // Global variable for a warp timer upon getting caught by a guard
static unsigned char bad_guard_states[] = {
    // Control States that you can't be caught in
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
    /**
     * @brief Check if you're in a bad control state
     */
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
    /**
     * @brief Catch Code for a guard
     */
    if (Player) {
        if ((warp_timer == 0) && (TransitionSpeed == 0) && (!isBadMovementState()) && (CutsceneActive == 0)) {
            /*
                Only activates in the following conditions:
                - Not caught by a guard at all (warp_timer == 0)
                - Not in a transition process (TransitionSpeed == 0)
                - Not in a bad movement state (!isBadMovementState())
                - Not in a cutscene (CutsceneActive == 0)
            */
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
    /**
     * @brief Handles the warp procedure for guards, voiding and death
     */
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
    /**
     * @brief Handle the catch procedure for a guard
     */
    if (warp_timer > 0) {
        if ((warp_timer == 1) && (TransitionSpeed == 0)) {
            // Warp on the final frame if not in a transition already
            WarpHandle();
        }
        warp_timer -= 1;
    }
    if (TransitionSpeed != 0) {
        // Protect against warping if in a transition, which can cause a warp to an invalid map
        warp_timer = 0;
    }
}

void newGuardCode(void) {
    /**
     * @brief Guard Actor Code
     */
    unsigned int level_state = *(unsigned int*)(0x807FBB64);
    if (CurrentActorPointer_0->control_state <= 0x35) {
        if (Player) {
            if ((Player->strong_kong_ostand_bitfield & 0x60) == 0) { // No GGone / OSprint
                // Guard detection can't happen if being damaged or dying, or ggone/osprint
                handleGuardDetection(40.0f,70.0f);
            }
        }
    }
    if ((collisionType == 4) || (collisionType == 9) || (collisionActive)) { // If being damaged
        if ((level_state & 0x104000) == 0) { // If not in SSnoop
            // Hit by ammo/oranges
            if ((CurrentActorPointer_0->health <= 0) || (collisionActive)) { // If being attacked and with zero/negative health
                // Death procedure
                CurrentActorPointer_0->health = 0;
                playActorAnimation(CurrentActorPointer_0,0x201);
                CurrentActorPointer_0->control_state = 0x42;
                CurrentActorPointer_0->control_state_progress = 0;
                CurrentActorPointer_0->noclip_byte = 1;
            } else {
                // Damage procedure
                playActorAnimation(CurrentActorPointer_0,0x1FF);
                CurrentActorPointer_0->control_state = 0x41;
                CurrentActorPointer_0->control_state_progress = 0;
            }
        }
    }
    int control_state = CurrentActorPointer_0->control_state;
    if (control_state > 0x35) {
        if (control_state == 0x37) {
            // Spawn Enemy Drops
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