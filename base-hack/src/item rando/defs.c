/**
 * @file defs.c
 * @author Ballaam
 * @brief Definitions for item rando
 * @version 0.1
 * @date 2023-01-17
 * 
 * @copyright Copyright (c) 2023
 * 
 */
#include "../../include/common.h"

const collision_tree_struct fixed_shockwave_collision[3] = {
    {.actor_interaction = -1, .target_interaction=COLBTF_SHOCKWAVE, .collision_type=1, .unk9=2, .force_break=1}, // If you're shockwaving, treat as immune
    {.actor_interaction = -1, .target_interaction=-1, .function=(void*)0x80676C10, .collision_type=1, .unk9=2, .force_break=2},
    {.actor_interaction = -1, .target_interaction=-1, .collision_type=4, .unk9=5},
};

const collision_tree_struct fixed_scarab_collision[4] = {
    {.actor_interaction = -1, .target_interaction=COLBTF_RAMBI_ENGUARDEBATTACK, .collision_type=6, .unk9=10, .force_break=2}, // Rambi kills enemy
    {.actor_interaction=0x1, .target_interaction=0xFE8, .collision_type=0x4, .force_break=0x2},
    {.actor_interaction=0x2, .target_interaction=-1, .function=&stompHandler, .collision_type=0x9, .unk9=0x3, .force_break=0x2},
    {.actor_interaction=-1, .target_interaction=-1, .collision_type=0x1, .unk9=0x5},
};

const collision_tree_struct fixed_dice_collision[12] = {
    {.actor_interaction = 1, .target_interaction=COLBTF_RAMBI_ENGUARDEBATTACK, .collision_type=6, .unk9=10, .force_break=2}, // Rambi kills enemy
    {.actor_interaction=0x1, .target_interaction=0xa00, .function=(void*)0x8067641c, .collision_type=0x6, .unk9=0x2, .force_break=0x2},
    {.actor_interaction=0x1, .target_interaction=0x80, .function=(void*)0x806764d8, .collision_type=0x6, .unk9=0x2, .force_break=0x2},
    {.actor_interaction=0x1, .target_interaction=0x4, .function=(void*)0x80676540, .collision_type=0x6, .unk9=0x3, .force_break=0x2},
    {.actor_interaction=0x1, .target_interaction=0x420, .collision_type=0x6, .unk9=0x2, .force_break=0x2},
    {.actor_interaction=0x1, .target_interaction=0xb48, .function=(void*)0x8067641c, .collision_type=0x6, .unk9=0x2, .force_break=0x2},
    {.actor_interaction=0x2, .target_interaction=-1, .collision_type=0x2, .unk9=0x2, .force_break=0x2},
    {.actor_interaction=0x4, .target_interaction=-1, .collision_type=0x1, .unk9=0x5, .force_break=0x2},
    {.actor_interaction=0x8, .target_interaction=0xe60, .collision_type=0x4, .unk9=0x2, .force_break=0x2},
    {.actor_interaction=0x8, .target_interaction=-1, .collision_type=0x2, .unk9=0x2, .force_break=0x2},
    {.actor_interaction=-1, .target_interaction=-1, .function=(void*)0x80676c10, .collision_type=0x1, .unk9=0x2, .force_break=0x2},
    {.actor_interaction=-1, .target_interaction=-1, .collision_type=0x1, .unk9=0x5},
};

const collision_tree_struct fixed_klap_collision[8] = {
    {.actor_interaction = 1, .target_interaction=COLBTF_RAMBI_ENGUARDEBATTACK, .collision_type=6, .unk9=10, .force_break=2}, // Rambi kills enemy
    {.actor_interaction=-1, .target_interaction=0x4, .function=(void*)0x80676540, .collision_type=0x6, .unk9=0x3, .force_break=0x2},
    {.actor_interaction=-1, .target_interaction=0x8, .collision_type=0x6, .unk9=0x8, .force_break=0x2},
    {.actor_interaction=-1, .target_interaction=0x400, .collision_type=0x9, .force_break=0x2},
    {.actor_interaction=-1, .target_interaction=0xa00, .function=(void*)0x8067641c, .collision_type=0x6, .unk9=0x2, .force_break=0x2},
    {.actor_interaction=-1, .target_interaction=0x1e8, .collision_type=0x6, .unk9=0x8, .force_break=0x2},
    {.actor_interaction=-1, .target_interaction=-1, .function=(void*)0x80676c10, .collision_type=0x1, .unk9=0x2, .force_break=0x2},
    {.actor_interaction=-1, .target_interaction=-1, .collision_type=0x1, .unk9=0x5},
};

const collision_tree_struct fixed_bug_collision[2] = {
    {.actor_interaction = -1, .target_interaction=COLBTF_SHOCKWAVE, .collision_type=1, .unk9=2, .force_break=1}, // If you're shockwaving, treat as immune
    {.actor_interaction=-1, .target_interaction=-1, .collision_type=0x1, .unk9=0x5},
};

#define MODEL_CHAIN 0x80

void initActorDefs(void) {
    /**
     * @brief Initialize actor definitions table
     */
    if (Rando.seasonal_changes == SEASON_HALLOWEEN) {
        actor_defs[12].model = MODEL_CHAIN;
        actor_defs[49].model = MODEL_CHAIN;
    }
}

void setActorDamage(int actor, int new_damage) {
    actor_health_damage[actor].damage_applied = new_damage;
}

static unsigned char kremling_krossbone_maps[] = {
    MAP_BARRAGE_EASY,
    MAP_BARRAGE_NORMAL,
    MAP_BARRAGE_HARD,
    MAP_HELMBARREL_RANDOMKREMLING,
    MAP_HELMBARREL_HIDDENKREMLING,
};

void swapKremlingModel(void) {
    if (Rando.seasonal_changes != SEASON_HALLOWEEN) {
        return;
    }
    int kremling_model = 0x31;
    if (inU8List(CurrentMap, &kremling_krossbone_maps, sizeof(kremling_krossbone_maps))) {
        kremling_model = 0x42;
    }
    CharSpawnerActorData[59].model = kremling_model;
}

void getBPCountStats(int kong, unsigned char *has, unsigned char *turned) {
    *has = getItemCount_new(REQITEM_BLUEPRINT, 0, kong);
    *turned = ItemInventory->turned_in_bp_count[kong];
}

int getTurnedCount(int kong) {
    int count = 0;
    for (int i = 0; i < 5; i++) {
        if ((kong == i) || (kong == -1)) {
            count += ItemInventory->turned_in_bp_count[i];
        }
    }
    return count;
}

int getFirstEmptySnideReward(int offset) {
    for (int i = 0; i < 40; i++) {
        if (!checkFlag(FLAG_SNIDE_REWARD + i, FLAGTYPE_PERMANENT)) {
            return i + offset;
        }
    }
    return -1;
}