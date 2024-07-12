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

/*
#define TRASHCAN_BUG_ANIM_0 0x30A
#define TRASHCAN_BUG_ANIM_1 0x30B
#define TRASHCAN_BUG_ANIM_2 0x30C
#define TRASHCAN_BUG_ANIM_3 0x30D
#define TRASHCAN_BUG_ANIM_4 0x30E
*/

/*
    Known bug anims
    (Maybe 0x32F)
    0x331
*/

typedef struct fly_paad_0 {
    /* 0x000 */ float x;
    /* 0x004 */ float y;
    /* 0x008 */ float z;
    /* 0x00C */ float y_0;
    /* 0x010 */ short counter_10;
    /* 0x012 */ short counter;
} fly_paad_0;

void handleBugEnemy(void) {
    if (CurrentMap == MAP_CASTLETRASH) {
        trashCanBugCode();
        return;
    }
    /*
    fly_paad_0* paad_178 = CurrentActorPointer_0->paad2;
    initCharSpawnerActor();
    int control_state = CurrentActorPointer_0->control_state;
    if ((control_state != 0x37) && (control_state != 0x40)) {
        if ((collisionType == 9) || (collisionActive)) {
            // 80605314
            playActorAnimation(CurrentActorPointer_0, 0x331);
            CurrentActorPointer_0->control_state = 0x37;
            CurrentActorPointer_0->control_state_progress = 0;
            unkProjectileCode_4(Player, 0x16, 0xFF, 0x7F, 0x1E);
        }
    }
    if ((CurrentActorPointer_0->obj_props_bitfield & 0x10) == 0) {
        CurrentActorPointer_0->hSpeed = 40.0f;
        CurrentActorPointer_0->control_state = 0x23;
        CurrentActorPointer_0->control_state_progress = 0;
        CurrentActorPointer_0->unk_EC = ((getRNGLower31() >> 0xF) & 7) + 0xF;
        paad_178->x = CurrentActorPointer_0->xPos;
        paad_178->y = CurrentActorPointer_0->yPos;
        paad_178->z = CurrentActorPointer_0->zPos;
        paad_178->y_0 = paad_178->y;
        paad_178->counter_10 = 1;
        paad_178->counter = (getRNGLower31() & 0xFF) + 0x78;
    }
    if ((CurrentActorPointer_0->control_state != 0x37) && (CurrentActorPointer_0->sound_slot != -1)) {
        unkLightFunc_0(CurrentActorPointer_0, 0x10E, 0, 0, 0, 0xFF, 1.0f, 0);
    }
    control_state = CurrentActorPointer_0->control_state;
    if (control_state == 0x26) {
        paad_178->x = Player->xPos;
        paad_178->y = Player->yPos;
        paad_178->z = Player->zPos;
        paad_178->counter = (getRNGLower31() & 0xFF) + 0x78;
    } else {
        if (control_state == 0x37) {
            CurrentActorPointer_0->obj_props_bitfield &= 0xFFFF7FFF;
            CurrentActorPointer_0->shadow_intensity -= 8;
            CurrentActorPointer_0->yPos -= 8.0f;
            if (CurrentActorPointer_0->shadow_intensity < 0) {
                CurrentActorPointer_0->shadow_intensity = 0;
                CurrentActorPointer_0->control_state = 0x40;
                CurrentActorPointer_0->control_state_progress = 0;
                CurrentActorPointer_0->noclip_byte = 1;
            }
        } else if (control_state != 0x23) {
            handleGuardDefaultAnimation(0x32F);
        }
        if (control_state != 0x23) {
            renderActor(CurrentActorPointer_0, 0);
            return;
        }
    }
    int angle = getAngleBetweenPoints(CurrentActorPointer_0->xPos, CurrentActorPointer_0->zPos, paad_178->x, paad_178->z);
    angle = getPauseWheelRotationProgress(angle + 0x800, CurrentActorPointer_0->rot_y);
    CurrentActorPointer_0->rot_y -= (angle >> 4);
    if (paad_178->counter_10-- < 1) {
        paad_178->counter_10 = (getRNGLower31() & 0x3F) + 0xF;
        angle = getAngleBetweenPoints(TiedCharacterSpawner->xPos, TiedCharacterSpawner->zPos, paad_178->x, paad_178->z);
        short new_angle = angle + ((getRNGLower31() & 7) * 0x100) + 0x400;
        float magnitude = getRNGAsFloat() * 180.0f;
        paad_178->y = paad_178->y_0;
        paad_178->x = TiedCharacterSpawner->xPos + (magnitude * determineXRatioMovement(new_angle));
        paad_178->z = TiedCharacterSpawner->zPos + (magnitude * determineZRatioMovement(new_angle));
        CurrentActorPointer_0->control_state = 0x23;
    }
    if (CurrentActorPointer_0->control_state == 0x23) {
        if (paad_178->counter-- < 1) {
            paad_178->counter_10 = 0x3C;
            CurrentActorPointer_0->control_state = 0x26;
        }
    }
    float delta_y = paad_178->y - (CurrentActorPointer_0->yPos * 0.0625f);
    if (delta_y > 8.0f) {
        delta_y = 8.0f;
    } else if (delta_y < -8.0f) {
        delta_y = -8.0f;
    }
    CurrentActorPointer_0->xPos += (8.0f * determineXRatioMovement(CurrentActorPointer_0->rot_y));
    CurrentActorPointer_0->yPos += delta_y;
    float lim = TiedCharacterSpawner->yPos + 200.0f;
    if (CurrentActorPointer_0->yPos > lim) {
        CurrentActorPointer_0->yPos = lim;
    }
    CurrentActorPointer_0->zPos += (8.0f * determineZRatioMovement(CurrentActorPointer_0->rot_y));
    renderActor(CurrentActorPointer_0, 0);

    /*
    if ((CurrentActorPointer_0->obj_props_bitfield & 0x10) == 0) {
        modifyCharSpawnerAttributes(TRASHCAN_BUG_ANIM_2, TRASHCAN_BUG_ANIM_1, TRASHCAN_BUG_ANIM_3); // TODO: Figure out anim indexes
        CurrentActorPointer_0->obj_props_bitfield &= 0xFFFF7FFF;
    }
    void* func = 0;
    if (ObjectModel2Timer & 1) {
        func = (void*)0x806B3F3C;
    } else {
        func = (void*)0x806B3E7C;
    }
    flyingEnemyHandler(func, TRASHCAN_BUG_ANIM_4, TRASHCAN_BUG_ANIM_1, 0x10E);
    */

    initCharSpawnerActor();
    int control_state = CurrentActorPointer_0->control_state;
    if ((control_state != 0x37) && (control_state != 0x40)) {
        if ((collisionType == 9) || (collisionActive)) {
            // 80605314
            playActorAnimation(CurrentActorPointer_0, 0x331);
            CurrentActorPointer_0->control_state = 0x37;
            CurrentActorPointer_0->control_state_progress = 0;
            unkProjectileCode_4(Player, 0x16, 0xFF, 0x7F, 0x1E);
        }
    }
    flyingEnemyHandler((void*)0x806B3E7C, 0x331, 0x32F, 0x10E);
    // 8072881C
    if (CurrentActorPointer_0->control_state == 0x37) {
        CurrentActorPointer_0->obj_props_bitfield &= 0xFFFF7FFF;
        CurrentActorPointer_0->shadow_intensity -= 8;
        CurrentActorPointer_0->yPos -= 8.0f;
        if (CurrentActorPointer_0->shadow_intensity < 0) {
            CurrentActorPointer_0->shadow_intensity = 0;
            CurrentActorPointer_0->control_state = 0x40;
            CurrentActorPointer_0->control_state_progress = 0;
            CurrentActorPointer_0->noclip_byte = 1;
            spawnEnemyDrops(CurrentActorPointer_0);
        }
    }
}