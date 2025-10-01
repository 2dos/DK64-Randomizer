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
        assignGIFToActor(paad, sprite_table[sprite_index], scale);
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

void KongDropCode(void) {
    /**
     * @brief Kong Actors actor code
     */
    GoldenBananaCode();
    if ((CurrentActorPointer_0->obj_props_bitfield & 0x10) == 0) {
        int kong = CurrentActorPointer_0->actorType - NEWACTOR_KONGDK;
        if (kong >= 0) {
            updateActorHandStates(CurrentActorPointer_0, kong + 2);
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

static const short shop_owner_anims[] = {
    622, // Cranky Idle
    624, // Funky Idle
    626, // Candy Idle
    628, // Snide Idle
};

void shopOwnerItemCode(void) {
    /**
     * @brief Actor code for the shop owner items
     */
    GoldenBananaCode();
    if ((CurrentActorPointer_0->obj_props_bitfield & 0x10) == 0) {
        CurrentActorPointer_0->obj_props_bitfield &= 0xFFFFEFFF; // Make color blends work
        int owner = CurrentActorPointer_0->actorType - NEWACTOR_CRANKYITEM;
        playActorAnimation(CurrentActorPointer_0, shop_owner_anims[owner]);
    }
}

#define SHOP_OWNER_WAIT_LENGTH 30

void missingShopOwnerCode(int cutscene) {
    initCharSpawnerActor();
    if ((CurrentActorPointer_0->obj_props_bitfield & 0x10) == 0) {
        Player->unk_fairycam_bitfield |= 0x20; // Freeze player input
    }
    int control_state = CurrentActorPointer_0->control_state;
    if (control_state < SHOP_OWNER_WAIT_LENGTH) {
        CurrentActorPointer_0->control_state += 1;
    } else if (control_state == SHOP_OWNER_WAIT_LENGTH) {
        if (cutscene != -1) {
            playCutscene((void*)0, cutscene, 1);
        }
        CurrentActorPointer_0->control_state += 1;
    } else if (control_state == (SHOP_OWNER_WAIT_LENGTH + 1)) {
        if (CutsceneActive == 0) {
            ExitFromBonus();
            CurrentActorPointer_0->control_state += 1;
        }
    }
}

void crankyCodeHandler(void) {
    if (checkFlag(FLAG_ITEM_CRANKY, FLAGTYPE_PERMANENT)) {
        crankyCode();
        return;
    }
    missingShopOwnerCode(7);
}

void funkyCodeHandler(void) {
    if (checkFlag(FLAG_ITEM_FUNKY, FLAGTYPE_PERMANENT)) {
        funkyCode();
        return;
    }
    missingShopOwnerCode(7);
}

void candyCodeHandler(void) {
    if (checkFlag(FLAG_ITEM_CANDY, FLAGTYPE_PERMANENT)) {
        candyCode();
        return;
    }
    missingShopOwnerCode(7);
}

float getModelTwoScale(int obj_id) {
    for (int i = 0; i < (sizeof(item_conversions) / sizeof(item_conversion_info)); i++) {
        if (item_conversions[i].model_two == obj_id) {
            return item_conversions[i].scale;
        }
    }
    return 0.25f;
}

void snideCodeHandler(void) {
    if (checkFlag(FLAG_ITEM_SNIDE, FLAGTYPE_PERMANENT)) {
        snideCode();
        return;
    }
    missingShopOwnerCode(13);
}

void FakeKeyCode(void) {
    /**
     * @brief Actor code for the fake item (commonly known as "Ice Traps") actor
     */
    BossKeyCode();
    CurrentActorPointer_0->rot_y -= 0xE4; // Spin in reverse
}
void FakeGBCode(void) {
    /**
     * @brief Actor code for the fake item (commonly known as "Ice Traps") actor
     */
    GoldenBananaCode();
    CurrentActorPointer_0->rot_y -= 0xE4; // Spin in reverse
}

void FakeFairyCode(void) {
    fairyDuplicateCode();
    CurrentActorPointer_0->rot_y -= 0xE4; // Spin in reverse
}

void mermaidCheck(void) {
    /**
     * @brief Set the mermaid control state based on the amount of pearls you have
     */
    int count = getItemCount_new(REQITEM_PEARL, 0, 0);
    if ((count == 0) && (Rando.mermaid_requirement > 0)) {
        CurrentActorPointer_0->control_state = 0x1E;
    } else if (count < Rando.mermaid_requirement) {
        CurrentActorPointer_0->control_state = 0x1F;
    } else {
        CurrentActorPointer_0->control_state = 0x27;
    }
    CurrentActorPointer_0->control_state_progress = 0;
}

int fairyQueenCutsceneInit(int start, int count, flagtypes type) {
    /**
     * @brief Set BFI Queen control state based on the amount of fairies you have
     */
    int fairies_in_possession = getItemCount_new(REQITEM_FAIRY, 0, 0);
    if (fairies_in_possession < Rando.rareware_gb_fairies) {
        // Not enough fairies
        CurrentActorPointer_0->control_state = 10;
    } else {
        CurrentActorPointer_0->control_state = 3;
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
        if ((dx * dx) + (dz * dz) < 8100.0f) {
            // In Range
            if (!checkFlag(0x79, FLAGTYPE_TEMPORARY)) {
                playCutscene(Player, 3, 1);
                CurrentActorPointer_0->control_state = 11;
                setFlag(0x79, 1, FLAGTYPE_TEMPORARY);
            }
        }
    }
    renderActor(CurrentActorPointer_0, 0);
}

void fairyQueenCheckSpeedup(void *actor, int unk) {
    unkSoundFunction(actor, unk);
    fairyQueenCutsceneInit(0x24D, 20, FLAGTYPE_PERMANENT);
}

#define STORED_COUNT 18
static int stored_maps[STORED_COUNT] = {};
static unsigned char stored_kasplat[STORED_COUNT] = {};
static unsigned char stored_enemies[ENEMY_REWARD_CACHE_SIZE][STORED_COUNT] = {};
static unsigned short stored_holdable;

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
                for (int j = 0; j < ENEMY_REWARD_CACHE_SIZE; j++) {
                    stored_enemies[j][i] = -1;
                }
            }
        }
    }
    // Store Old Bitfield
    int place_new = 1;
    for (int i = 0; i < STORED_COUNT; i++) {
        if (stored_maps[i] == PreviousMap) {
            place_new = 0;
            stored_holdable = HoldableSpawnBitfield;
            stored_kasplat[i] = KasplatSpawnBitfield;
            for (int j = 0; j < ENEMY_REWARD_CACHE_SIZE; j++) {
                stored_enemies[j][i] = enemy_rewards_spawned[j];
            }
        }
    }
    if (place_new) {
        for (int i = 0; i < STORED_COUNT; i++) {
            if (place_new) {
                if (stored_maps[i] == -1) {
                    stored_holdable = HoldableSpawnBitfield;
                    stored_kasplat[i] = KasplatSpawnBitfield;
                    for (int j = 0; j < ENEMY_REWARD_CACHE_SIZE; j++) {
                        stored_enemies[j][i] = enemy_rewards_spawned[j];
                    }
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
                for (int j = 0; j < ENEMY_REWARD_CACHE_SIZE; j++) {
                    enemy_rewards_spawned[j] = 0;
                }
            }
            HoldableSpawnBitfield = stored_holdable;
            KasplatSpawnBitfield = stored_kasplat[i];
            for (int j = 0; j < ENEMY_REWARD_CACHE_SIZE; j++) {
                enemy_rewards_spawned[j] = stored_enemies[j][i];
            }
        }
    }
    if (!in_chain) {
        KasplatSpawnBitfield = 0;
        HoldableSpawnBitfield = 0;
        for (int j = 0; j < ENEMY_REWARD_CACHE_SIZE; j++) {
            enemy_rewards_spawned[j] = 0;
        }
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
                int is_drop = inShortList(actor_type, &actor_drops, sizeof(actor_drops) >> 1);
                if (is_drop) {
                    int flag = referenced_spawner->flag;
                    if (isFlagInRange(flag, FLAG_BP_JAPES_DK_HAS, 40)) {
                        // Is Kasplat Drop
                        int kong = (flag - FLAG_BP_JAPES_DK_HAS) % 5;
                        int shift = 1 << kong;
                        KasplatSpawnBitfield &= (0xFF - shift);
                    } else if (isFlagInRange(flag, FLAG_ENEMY_KILLED_0, ENEMIES_TOTAL)) {
                        // Is Enemy Drop
                        setSpawnBitfieldFromFlag(flag, 0);
                    } else if (isFlagInRange(flag, FLAG_GRABBABLES_DESTROYED, 16)) {
                        // Is Holdable
                        HoldableSpawnBitfield |= (1 << (flag - FLAG_GRABBABLES_DESTROYED));
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

int isFlaggedWatermelon(void) {
    if (ActorSpawnerPointer) {
        actorSpawnerData* referenced_spawner = ActorSpawnerPointer;
        while (1 == 1) {
            if (referenced_spawner) {
                if (referenced_spawner->tied_actor == CurrentActorPointer_0) {
                    int flag = referenced_spawner->flag;
                    if (flag != -1) {
                        // Is flagged drop
                        return 1;
                    }
                }
                // Get Next Spawner
                if (referenced_spawner->next_spawner) {
                    referenced_spawner = referenced_spawner->next_spawner;
                } else {
                    return 0;
                }
            } else {
                return 0;
            }
        }
    }
    return 0;
}

int canItemPersist(void) {
    int actor = CurrentActorPointer_0->actorType;
    if (actor == 0x2F) {
        if (isFlaggedWatermelon()) {
            return 1;
        }
    }
    if ((actor == 0x2F) || (actor == 0x36)) {
        return isCutsceneActive();
    }
    return 1;
}
