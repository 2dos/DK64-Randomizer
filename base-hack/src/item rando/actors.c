/**
 * @file actors.c
 * @author Ballaam
 * @brief Item Rando changes pertaining to actors
 * @version 0.1
 * @date 2023-01-17
 * 
 * @copyright Copyright (c) 2023
 * 
 */

#include "../../include/common.h"

void spriteCode(int sprite_index, float scale) {
    /**
     * @brief Generic sprite code for actors
     * 
     * @param sprite_index Sprite Index inside the Sprite Table
     * @param scale Scale of the item which will be spawned
     */
    void* paad = CurrentActorPointer_0->paad;
    spriteActorGenericCode(4.5f);
    if ((CurrentActorPointer_0->obj_props_bitfield & 0x10) == 0) {
        assignGIFToActor(paad, sprite_table[sprite_index], *(int*)(&scale));
        if (CurrentActorPointer_0->control_state == 99) {
            CurrentActorPointer_0->control_state = 1;
            CurrentActorPointer_0->sub_state = 2;
        }
    }
}

void ninCoinCode(void) {
    /**
     * @brief Nintendo Coin Actor Code
     */
    spriteCode(0x8D, 1.0f);
}

void rwCoinCode(void) {
    /**
     * @brief Rareware Coin Actor Code
     */
    spriteCode(0x8C, 1.0f);
}

void medalCode(void) {
    /**
     * @brief Medal Actor Code
     */
    spriteCode(0x3C, 2.0f);
}

void beanCode(void) {
    /**
     * @brief Bean Actor Code
     */
    void* paad = CurrentActorPointer_0->paad;
    spriteActorGenericCode(12.0f);
    if ((CurrentActorPointer_0->obj_props_bitfield & 0x10) == 0) {
        assignGIFToActor(paad, &bean_sprite, 0x3F800000);
        if (CurrentActorPointer_0->control_state == 99) {
            CurrentActorPointer_0->control_state = 1;
            CurrentActorPointer_0->sub_state = 2;
        }
    }
}

void pearlCode(void) {
    /**
     * @brief Pearl Actor Code
     */
    void* paad = CurrentActorPointer_0->paad;
    spriteActorGenericCode(12.0f);
    if ((CurrentActorPointer_0->obj_props_bitfield & 0x10) == 0) {
        assignGIFToActor(paad, &pearl_sprite, 0x3F800000);
        if (CurrentActorPointer_0->control_state == 99) {
            CurrentActorPointer_0->control_state = 1;
            CurrentActorPointer_0->sub_state = 2;
        }
    }
}

void NothingCode(void) {
    /**
     * @brief Null Item Actor Code
     */
    deleteActorContainer(CurrentActorPointer_0);
}

void scaleBounceDrop(float scale) {
    /**
     * @brief Change the visual scale of a bounce drop
     * 
     * @param scale New Scale of the object
     */
    if ((CurrentActorPointer_0->obj_props_bitfield & 0x10) == 0) {
        renderingParamsData* render = CurrentActorPointer_0->render;
        if (render) {
            render->scale_x = scale;
            render->scale_y = scale;
            render->scale_z = scale;
        }
    }
}

void KongDropCode(void) {
    /**
     * @brief Kong Actors actor code
     */
    GoldenBananaCode();
    scaleBounceDrop(0.15f);
    if (CurrentActorPointer_0->yVelocity > 500.0f) {
        CurrentActorPointer_0->yVelocity = 500.0f;
    }
    if ((CurrentActorPointer_0->obj_props_bitfield & 0x10) == 0) {
        int current_type = CurrentActorPointer_0->actorType - CUSTOM_ACTORS_START;
        int kong = current_type - NEWACTOR_KONGDK;
        if (kong >= 0) {
            handleCutsceneKong(CurrentActorPointer_0, kong + 2);
            playActorAnimation(CurrentActorPointer_0, AnimationTable1[(0x8B * 7) + kong]);
        }
    }
}

void PotionCode(void) {
    /**
     * @brief Actor code for the potion actors
     */
    GoldenBananaCode();
    if ((CurrentActorPointer_0->obj_props_bitfield & 0x10) == 0) {
        CurrentActorPointer_0->obj_props_bitfield &= 0xFFFFEFFF; // Make color blends work
    }
}

void fairyDuplicateCode(void) {
    /**
     * @brief Actor code for the fairy pickup duplicate
     */
    GoldenBananaCode();
    if ((CurrentActorPointer_0->obj_props_bitfield & 0x10) == 0) {
        CurrentActorPointer_0->obj_props_bitfield &= 0xFFFFEFFF; // Make color blends work
    }
    playActorAnimation(CurrentActorPointer_0, 0x2B5);
}

void FakeGBCode(void) {
    /**
     * @brief Actor code for the fake item (commonly known as "Ice Traps") actor
     */
    GoldenBananaCode();
    scaleBounceDrop(0.10f);
    if (CurrentActorPointer_0->yVelocity > 500.0f) {
        CurrentActorPointer_0->yVelocity = 500.0f;
    }
    CurrentActorPointer_0->rot_y -= 0xE4; // Spin in reverse
}

void mermaidCheck(void) {
    /**
     * @brief Set the mermaid control state based on the amount of pearls you have
     */
    int requirement = 5;
    if (Rando.fast_gbs) {
        requirement = 1; // Fast GBs pearl requirement
    }
    int count = 0;
    for (int i = 0; i < 5; i++) {
        count += checkFlagDuplicate(FLAG_PEARL_0_COLLECTED + i, 0);
    }
    if (count == 0) {
        CurrentActorPointer_0->control_state = 0x1E;
    } else if (count < requirement) {
        CurrentActorPointer_0->control_state = 0x1F;
    } else {
        CurrentActorPointer_0->control_state = 0x27;
    }
    CurrentActorPointer_0->control_state_progress = 0;
}

int fairyQueenCutsceneInit(int start, int count, int type) {
    /**
     * @brief Set BFI Queen control state based on the amount of fairies you have
     */
    int fairies_in_possession = countFlagsDuplicate(start, count, type); 
    int fairy_limit = 20;
    if (Rando.rareware_gb_fairies > 0) {
        fairy_limit = Rando.rareware_gb_fairies;
    }
    if (fairies_in_possession < fairy_limit) {
        // Not enough fairies
        CurrentActorPointer_0->control_state = 10;
    }
    return fairies_in_possession;
}

void fairyQueenCutsceneCheck(void) {
    /**
     * @brief Check for playing the cutscene inside BFI for the rewards behind Rareware Door
     */
    if (CurrentActorPointer_0->control_state == 10) {
        float dx = CurrentActorPointer_0->xPos - Player->xPos;
        float dz = CurrentActorPointer_0->zPos - Player->zPos;
        if ((dx * dx) + (dz * dz) < 10000.0f) {
            // In Range
            if (!checkFlag(0x79, 2)) {
                playCutscene(Player, 3, 1);
                CurrentActorPointer_0->control_state = 11;
                setFlag(0x79, 1, 2);
            }
        }
    }
    renderActor(CurrentActorPointer_0, 0);
}

#define STORED_COUNT 18
static int stored_maps[STORED_COUNT] = {};
static unsigned char stored_kasplat[STORED_COUNT] = {};

int setupHook(int map) {
    /**
     * @brief Setup hook which checks the setup for whether kasplat rewards are spawned.
     * This function will alter the kasplat spawned bitfield to prevent duplication glitches with kasplat rewards
     */
    int index = getParentIndex(map);
    // Wipe array of items not in parent chain
    for (int i = 0; i < STORED_COUNT; i++) {
        if (stored_maps[i] != -1) {
            if (getParentIndex(stored_maps[i]) == -1) {
                stored_maps[i] = -1;
                stored_kasplat[i] = -1;
            }
        }
    }
    // Store Old Bitfield
    int place_new = 1;
    for (int i = 0; i < STORED_COUNT; i++) {
        if (stored_maps[i] == PreviousMap) {
            place_new = 0;
            stored_kasplat[i] = KasplatSpawnBitfield;
        }
    }
    if (place_new) {
        for (int i = 0; i < STORED_COUNT; i++) {
            if (place_new) {
                if (stored_maps[i] == -1) {
                    stored_kasplat[i] = KasplatSpawnBitfield;
                    stored_maps[i] = PreviousMap;
                    place_new = 0;
                }
            }
        }
    }
    // Place New
    int in_chain = 0;
    for (int i = 0; i < STORED_COUNT; i++) {
        if (stored_maps[i] == map) {
            in_chain = 1;
            if (index == -1) {
                // Setup refreshed
                stored_kasplat[i] = 0;
            }
            KasplatSpawnBitfield = stored_kasplat[i];
        }
    }
    if (!in_chain) {
        KasplatSpawnBitfield = 0;
    }
    return index;
}

void CheckKasplatSpawnBitfield(void) {
    /**
     * @brief Alter kasplat spawn bitfield based on the present actor spawners
     */
    if (ActorSpawnerPointer) {
        actorSpawnerData* referenced_spawner = ActorSpawnerPointer;
        while (1 == 1) {
            if (referenced_spawner) {
                int actor_type = referenced_spawner->actor_type + 0x10;
                int is_drop = 0;
                int i = 0;
                while (i < (int)(sizeof(actor_drops)/2)) {
                    if (actor_type == actor_drops[i]) {
                        is_drop = 1;
                        break;
                    }
                    i++;
                }
                if (is_drop) {
                    int flag = referenced_spawner->flag;
                    if (isFlagInRange(flag, FLAG_BP_JAPES_DK_HAS, 40)) {
                        // Is Kasplat Drop
                        int kong = (flag - FLAG_BP_JAPES_DK_HAS) % 5;
                        int shift = 1 << kong;
                        KasplatSpawnBitfield &= (0xFF - shift);
                    }
                }
                // Get Next Spawner
                if (referenced_spawner->next_spawner) {
                    referenced_spawner = referenced_spawner->next_spawner;
                } else {
                    return;
                }
            } else {
                return;
            }
        }
    }
}

int canItemPersist(void) {
    int actor = CurrentActorPointer_0->actorType;
    if ((actor == 0x2F) || (actor == 0x36)) {
        return isCutsceneActive();
    }
    return 1;
}
