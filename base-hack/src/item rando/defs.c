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

#define COLLECTABLE_AMMOBOX -2
#define COLLECTABLE_NONE -1
#define COLLECTABLE_CB 0
#define COLLECTABLE_COIN 1
#define COLLECTABLE_AMMOPELLET 2
#define COLLECTABLE_ORANGE 4
#define COLLECTABLE_CRYSTAL 5
#define COLLECTABLE_FILM 6
#define COLLECTABLE_GB 8
#define COLLECTABLE_MEDAL 10
#define COLLECTABLE_RACECOIN 11
#define COLLECTABLE_BP 12

#define KONG_NONE -2

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

void initCollectableCollision(void) {
    /**
     * @brief Initialize all collectable collisions
     */
    if (Rando.any_kong_items.blueprints) {
        for (int i = 0; i < COLLISION_LIMIT; i++) {
            if (object_collisions[i].collectable_type == COLLECTABLE_BP) {
                // Blueprints
                object_collisions[i].intended_actor = 0;
            }
        }
    }

    // Write new table to ROM
    int hi = getHi(&object_collisions[0].type);
    int lo = getLo(&object_collisions[0].type);
    *(unsigned short*)(0x806F48D2) = hi;
    *(unsigned short*)(0x806F48D6) = lo;
    *(unsigned short*)(0x806F4A8E) = COLLISION_LIMIT;
    *(unsigned short*)(0x806F4E7E) = hi;
    *(unsigned short*)(0x806F4E8E) = lo;
    *(unsigned short*)(0x806F51C2) = getHi(&object_collisions[0].intended_actor);
    *(unsigned short*)(0x806F51CE) = getLo(&object_collisions[0].intended_actor);
    *(unsigned short*)(0x806F5556) = getHi(&object_collisions[0].collectable_type);
    *(unsigned short*)(0x806F5562) = getLo(&object_collisions[0].collectable_type);
    *(unsigned short*)(0x806F626E) = hi;
    *(unsigned short*)(0x806F627A) = lo;
    *(unsigned short*)(0x806F6AC6) = hi;
    *(unsigned short*)(0x806F6ACE) = lo;
    *(unsigned short*)(0x806F742A) = hi;
    *(unsigned short*)(0x806F744A) = lo;
    *(unsigned short*)(0x806F7996) = getHi(&object_collisions[COLLISION_LIMIT].type);
    *(unsigned short*)(0x806F799A) = getLo(&object_collisions[COLLISION_LIMIT].type);
    // Change new sizes
    *(unsigned short*)(0x806F4A92) = sizeof(collision_info);
    *(unsigned short*)(0x806F4EAA) = sizeof(collision_info);
    *(int*)(0x806F51B4) = 0x240A0000 | sizeof(collision_info); // addiu $t2, $zero (sizeof(collision_info))
    *(int*)(0x806F51B8) = 0x01420019; // multu $t2, $v0
    *(int*)(0x806F51BC) = 0x00004812; // mflo $t1
    *(int*)(0x806F5548) = 0x240A0000 | sizeof(collision_info); // addiu $t2, $zero (sizeof(collision_info))
    *(int*)(0x806F554C) = 0x01420019; // multu $t2, $v0
    *(int*)(0x806F5550) = 0x00005012; // mflo $t2
    *(unsigned short*)(0x806F6282) = sizeof(collision_info);
    *(unsigned short*)(0x806F6ABE) = sizeof(collision_info);
    *(unsigned short*)(0x806F799E) = sizeof(collision_info);

}

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

void changeFeatherToSprite(void) {
    actor_defs[24].model = 0;
    actor_master_types[43] = ACTORMASTER_SPRITE;
}

void setActorDamage(int actor, int new_damage) {
    actor_health_damage[actor].damage_applied = new_damage;
}

GBDictItem NewGBDictionary[GB_DICTIONARY_COUNT];

int addDictionaryItem(int index, maps map, int id, int flag, int kong) {
    /**
     * @brief Add flag mapping item
     * 
     * @param index Index inside the dictionary table
     * @param map Map index which houses the item
     * @param id ID of the item
     * @param flag Tied flag
     * @param kong Kong intended for the actor (set to 0 if item can be picked up by any kong)
     * 
     * @return following index
     */
    NewGBDictionary[index].map = map;
    NewGBDictionary[index].model2_id = id;
    NewGBDictionary[index].flag_index = flag;
    NewGBDictionary[index].intended_kong_actor = kong + 2;
    return index + 1;
}

void initItemDictionary(void) {
    /**
     * @brief Initialize item dictionary
     */
    // Copy old dictionary
    for (int i = 0; i < 113; i++) {
        NewGBDictionary[i].map = GBDictionary[i].map;
        NewGBDictionary[i].unk_01 = GBDictionary[i].unk_01;
        NewGBDictionary[i].model2_id = GBDictionary[i].model2_id;
        
        NewGBDictionary[i].unk_07 = GBDictionary[i].unk_07;
        // Base Dict Alterations
        int map = GBDictionary[i].map;
        int id = GBDictionary[i].model2_id;
        int kong = GBDictionary[i].intended_kong_actor - 2;
        int flag = GBDictionary[i].flag_index;
        if ((map == MAP_ISLES) && (id == 4)) {
            kong = Rando.starting_kong;
        } else if ((map == MAP_JAPES) && ((id == 0x69) || (id == 0x48))) {
            kong = Rando.free_source_japes;
        } else if ((map == MAP_AZTECTINYTEMPLE) && (id == 0x5B)) {
            kong = Rando.free_source_ttemple;
        } else if ((map == MAP_AZTECLLAMATEMPLE) && (id == 0x6C)) {
            kong = Rando.free_source_llama;
        } else if ((map == MAP_FACTORY) && (id == 0x78)) {
            kong = Rando.free_source_factory;
        } else if ((map == MAP_HELM) && (id == 0x5E)) {
            flag = 0x24C;
        } else if ((map == MAP_HELM) && (id == 0x61)) {
            flag = 0x249;
        }
        NewGBDictionary[i].intended_kong_actor = kong + 2;
        NewGBDictionary[i].flag_index = flag;
        if ((flag == FLAG_ARCADE_ROUND1) && (Rando.faster_checks.arcade_first_round)) {
            NewGBDictionary[i].map = MAP_FACTORYBBLAST;
            NewGBDictionary[i].model2_id = 0;
        }
    }
    // Add new entries
    int size = addDictionaryItem(113, MAP_GALLEONTREASURECHEST, 0, FLAG_PEARL_0_COLLECTED, -2);
    for (int i = 1; i < 5; i++) {
        size = addDictionaryItem(size, MAP_GALLEONTREASURECHEST, i, FLAG_PEARL_0_COLLECTED + i, -2);
    }
    size = addDictionaryItem(size, MAP_FUNGIANTHILL, 5, FLAG_COLLECTABLE_BEAN, -2);
    if (Rando.quality_of_life.vanilla_fixes) {
        size = addDictionaryItem(size, MAP_HELM, 0x5A, FLAG_KEYHAVE_KEY8, -2); // Fake Key backup fix
    }
    /*
        Had to disable this. Caused crashes when you would collect one version, then load the setup which contains the other version (No parent filter)
        Will look into at a future date
        size = addDictionaryItem(size, 0x3D, 0xA, FLAG_COLLECTABLE_FUNGI_DK_MILLGB, -2); // Mill GB fix
    */
}

static short kremling_krossbone_maps[] = {
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
    if (inShortList(CurrentMap, &kremling_krossbone_maps, sizeof(kremling_krossbone_maps) >> 1)) {
        kremling_model = 0x42;
    }
    CharSpawnerActorData[59].model = kremling_model;
}