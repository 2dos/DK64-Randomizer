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
    /* 0x01C */ char unk_1C[0x47-0x1C];
    /* 0x047 */ char played_uhoh;
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

void guardCatchInternal(void) {
    warp_timer = 80;
    tagKong(Player->new_kong);
    Player->noclip = 1;
    if (Player->control_state != 0x7D) {
        if ((Player->grounded_bitfield & 4) == 0) {
            playAnimation(Player,0x5D);
        } else {
            playAnimation(Player,0x34);
        }
    }
    Player->control_state = 0x70;
    Player->control_state_progress = 0;
    Player->yVelocity = 0;
    Player->hSpeed = 0;
    playSong(SONG_FAILURE, 1.0f);
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
            guardCatchInternal();
        }
    }
}

void WarpHandle(void) {
    /**
     * @brief Handles the warp procedure for guards, voiding and death
     */
    if (CurrentMap == MAP_HELM) {
        if (Rando.fast_start_helm == 2) { // Skip All
            initiateTransition(MAP_HELM,4); // Crown Door
        } else if (checkFlag(FLAG_HELM_ROMANDOORS_OPEN,FLAGTYPE_TEMPORARY) || checkFlag(FLAG_MODIFIER_HELMBOM,FLAGTYPE_PERMANENT)) { // Roman Doors Open or BoM off
            initiateTransition(MAP_HELM,3); // Lever
        } else {
            initiateTransition(MAP_HELM,0); // Start
        }
        setFlag(0x50,0,FLAGTYPE_TEMPORARY); // Prevent Helm Door hardlock
    } else if (inBossMap(CurrentMap, 1, 1, 1)) {
        exitBoss();
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

int inRabbitRace(void) {
    if (CurrentMap == MAP_FUNGI) {
        return MapProperties.unk29 != 0; // In Rabbit Race
    }
    return 0;
}

void newGuardCode(void) {
    /**
     * @brief Guard Actor Code
     */
    int in_snoop = MapProperties.is_bonus != 0;
    if (CurrentActorPointer_0->control_state <= 0x35) { // Not damaged/dying
        if (Player) {
            if ((Player->strong_kong_ostand_bitfield & 0x70) == 0) { // No GGone, OSprint, SKong
                if (!isBadMovementState()) { // Bad Movement State
                    if (!inRabbitRace()) {
                        float dist = 40.0f;
                        float radius = 70.0f;
                        if (!in_snoop) { // Not in snoop
                            if (CurrentActorPointer_0->control_state == 0x11) { // Is Idle
                                radius = 40.0f;
                                if (getAnimationTimer(CurrentActorPointer_0) > 60.0f) { // Smacking light
                                    dist = 0.0f;
                                    radius = 0.0f;
                                }
                            }
                        }
                        if (radius > 0.0f) {
                            int old_control_state = CurrentActorPointer_0->control_state;
                            handleGuardDetection(dist, radius);
                            if (old_control_state != 0) {
                                if (CurrentActorPointer_0->control_state == 0) {
                                    updateKopStat();
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    if ((collisionType == 4) || (collisionType == 9) || (collisionActive)) { // If being damaged
        if (!in_snoop) { // If not in SSnoop
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
    if (!in_snoop) { // If not in SSnoop
        guard_paad* paad = CurrentActorPointer_0->paad;
        if (CurrentActorPointer_0->grounded & 4) {
            // Touching Water
            if (paad->played_uhoh == 0) {
                playSFX(UhOh);
                spawnSparkles(CurrentActorPointer_0->xPos, CurrentActorPointer_0->yPos, CurrentActorPointer_0->zPos, 5);
            }
            paad->played_uhoh = 1;
            CurrentActorPointer_0->control_state = 0x40;
            CurrentActorPointer_0->control_state_progress = 0;
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
            handleGuardDefaultAnimation(0x2C0);
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