/**
 * @file enemies.c
 * @author Ballaam
 * @brief Any changes relevant for enemies
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

typedef struct crown_timer_reduction {
    /* 0x000 */ short target_actor;
    /* 0x002 */ short timer_change;
} crown_timer_reduction;

static const crown_timer_reduction actor_crown_timer_changes[] = {
    {.target_actor = 285, .timer_change = -3}, // Bat
    {.target_actor = 178, .timer_change = -1}, // Beaver (Blue)
    {.target_actor = 212, .timer_change = -2}, // Beaver (Gold)
    {.target_actor = 273, .timer_change = -1}, // Fireball
    {.target_actor = 210, .timer_change = 0}, // Get Out Guy
    {.target_actor = 289, .timer_change = -1}, // Ghost
    {.target_actor = 175, .timer_change = -3}, // Kaboom
    {.target_actor = 241, .timer_change = -4}, // Kasplat (DK)
    {.target_actor = 242, .timer_change = -4}, // Kasplat (Diddy)
    {.target_actor = 243, .timer_change = -4}, // Kasplat (Lanky)
    {.target_actor = 244, .timer_change = -4}, // Kasplat (Tiny)
    {.target_actor = 245, .timer_change = -4}, // Kasplat (Chunky)
    {.target_actor = 205, .timer_change = -1}, // Klaptrap (Green)
    {.target_actor = 208, .timer_change = -3}, // Klaptrap (Purple)
    {.target_actor = 209, .timer_change = -3}, // Klaptrap (Red)
    {.target_actor = 182, .timer_change = -3}, // Klobber
    {.target_actor = 291, .timer_change = -5}, // Kosha
    {.target_actor = 238, .timer_change = -1}, // Kremling
    {.target_actor = 262, .timer_change = -1}, // Krossbones
    {.target_actor = 269, .timer_change = -1}, // Mr. Dice
    {.target_actor = 271, .timer_change = -1}, // Mr. Dice
    {.target_actor = 224, .timer_change = -1}, // Mushroom Man
    {.target_actor = 235, .timer_change = -3}, // Robo Kremling
    {.target_actor = 230, .timer_change = -1}, // Ruler
    {.target_actor = 270, .timer_change = -1}, // Sir Domino
    {.target_actor = 276, .timer_change = -2}, // Spider
    {.target_actor = 261, .timer_change = -4}, // Zinger (Robo)
    {.target_actor = 183, .timer_change = -3}, // Zinger (Charger)
    {.target_actor = 206, .timer_change = -4}, // Zinger (Lime Thrower)
};

typedef struct timer_paad {
    /* 0x000 */ int start_timestamp_major;
    /* 0x004 */ int start_timestamp_minor;
    /* 0x008 */ int time_elapsed;
    /* 0x00C */ int timer_cap;
} timer_paad;

typedef struct general_enemy_paad_crowns {
    /* 0x000 */ char unk_00[0x47];
    /* 0x047 */ char killed;
} general_enemy_paad_crowns;

void handleCrownTimerInternal(void) {
    if (!inBattleCrown(CurrentMap)) {
        return;
    }
    int actor_type = CurrentActorPointer_0->actorType;
    for (int i = 0; i < sizeof(actor_crown_timer_changes)/sizeof(crown_timer_reduction); i++) {
        if (actor_crown_timer_changes[i].target_actor == actor_type) {
            int change = -1;
            if (Player->control_state != 0x2D) { // Not shockwaving
                change = actor_crown_timer_changes[i].timer_change;
            }
            general_enemy_paad_crowns* enemy_paad = CurrentActorPointer_0->paad;
            if (enemy_paad->killed) {
                return;
            }
            actorData* controller = findActorWithType(297);
            if (!controller) {
                return;
            }
            actorData* timer = controller->parent;
            if (!timer) {
                return;
            }
            timer_paad* paad = timer->paad;
            // Protections around setting timer cap fixes some crashes
            if ((paad->timer_cap - paad->time_elapsed) >= 1) {
                paad->timer_cap += change;
                if ((paad->timer_cap - paad->time_elapsed) < 1) {
                    paad->timer_cap = paad->time_elapsed + 1;
                }
            }
            enemy_paad->killed = 1;
            return;
        }
    }
}

void handleCrownTimer(actorData* actor) {
    if ((actor->control_state == 0x37) && (actor->control_state_progress == 0)) {
        handleCrownTimerInternal();
    }
    actor->unk_6C = actor->grounded;
}