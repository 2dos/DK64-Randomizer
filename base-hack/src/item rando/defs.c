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

static actor_behaviour_def actor_defs[DEFS_LIMIT] = {};
void* actor_functions[ACTOR_LIMIT] = {};
health_damage_struct actor_health_damage[ACTOR_LIMIT] = {};
short actor_interactions[ACTOR_LIMIT] = {};
unsigned char actor_master_types[ACTOR_LIMIT] = {};
short* actor_extra_data_sizes[ACTOR_LIMIT] = {};
collision_data_struct actor_collisions[ACTOR_LIMIT] = {};

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

int addActorDef(int index, int actor, int model, unsigned int func_0, unsigned int func_1, int rescale, int is_custom) {
    /**
     * @brief Add actor to the actor definition table
     * 
     * @param index Index inside the definition table
     * @param actor Actor Index
     * @param model Model that the actor will have upon being spawned
     * @param func_0 Unknown function
     * @param func_1 Unknown function
     * @param rescale Rescale actor (Set to 0 to have default)
     * @param is_custom Is Custom actor, apply offset
     * 
     * @return following index
     */
    if (is_custom) {
        actor += CUSTOM_ACTORS_START;
    }
    actor_defs[index].actor_type = actor;
    actor_defs[index].model = model;
    if (rescale == 0) {
        actor_defs[index].unk4[4] = 0x02;
        actor_defs[index].unk4[5] = 0x26;
    } else {
        actor_defs[index].unk4[4] = (rescale >> 8) & 0xFF;
        actor_defs[index].unk4[5] = rescale & 0xFF;
    }
    actor_defs[index].code = (void*)func_0;
    actor_defs[index].unk10 = (void*)func_1;
    return index + 1;
}

#define MODEL_CHAIN 0x80

void initActorDefs(void) {
    /**
     * @brief Initialize actor definitions table
     */
    if (Rando.seasonal_changes == SEASON_HALLOWEEN) {
        ActorBehaviourTable[12].model = MODEL_CHAIN;
        ActorBehaviourTable[49].model = MODEL_CHAIN;
    }
    dk_memcpy(&actor_defs[0], &ActorBehaviourTable[0], 128*sizeof(actor_behaviour_def));
    int index = addActorDef(128, NEWACTOR_NINTENDOCOIN, 0x10B, 0x80689F80, 0x80689FEC, 0, 1); // Nintendo Coin
    index = addActorDef(index, NEWACTOR_RAREWARECOIN, 0x10D, 0x80689F80, 0x80689FEC, 0, 1); // Rareware Coin
    // Potions
    index = addActorDef(index, NEWACTOR_POTIONDK, 0xEE, 0x80689F80, 0x80689FEC, 0, 1); // DK Potion
    index = addActorDef(index, NEWACTOR_POTIONDIDDY, 0xEF, 0x80689F80, 0x80689FEC, 0, 1); // Diddy Potion
    index = addActorDef(index, NEWACTOR_POTIONLANKY, 0xF0, 0x80689F80, 0x80689FEC, 0, 1); // Lanky Potion
    index = addActorDef(index, NEWACTOR_POTIONTINY, 0xF1, 0x80689F80, 0x80689FEC, 0, 1); // Tiny Potion
    index = addActorDef(index, NEWACTOR_POTIONCHUNKY, 0xF2, 0x80689F80, 0x80689FEC, 0, 1); // Chunky Potion
    index = addActorDef(index, NEWACTOR_POTIONANY, 0xF3, 0x80689F80, 0x80689FEC, 0, 1); // Any Potion
    // Kongs
    index = addActorDef(index, NEWACTOR_KONGDK, 0xFE, 0x80689F80, 0x80689FEC, 0, 1); // DK
    index = addActorDef(index, NEWACTOR_KONGDIDDY, 0xFF, 0x80689F80, 0x80689FEC, 0, 1); // Diddy
    index = addActorDef(index, NEWACTOR_KONGLANKY, 0x100, 0x80689F80, 0x80689FEC, 0, 1); // Lanky
    index = addActorDef(index, NEWACTOR_KONGTINY, 0x101, 0x80689F80, 0x80689FEC, 0, 1); // Tiny
    index = addActorDef(index, NEWACTOR_KONGCHUNKY, 0x102, 0x80689F80, 0x80689FEC, 0, 1); // Chunky
    // Shop Owners
    index = addActorDef(index, NEWACTOR_CRANKYITEM, 0x10F, 0x80689F80, 0x80689FEC, 0, 1); // Cranky
    index = addActorDef(index, NEWACTOR_FUNKYITEM, 0x110, 0x80689F80, 0x80689FEC, 0, 1); // Funky
    index = addActorDef(index, NEWACTOR_CANDYITEM, 0x111, 0x80689F80, 0x80689FEC, 0, 1); // Candy
    index = addActorDef(index, NEWACTOR_SNIDEITEM, 0x112, 0x80689F80, 0x80689FEC, 0, 1); // Snide
    // Misc
    index = addActorDef(index, NEWACTOR_BEAN, 0x105, 0x80689F80, 0x80689FEC, 0, 1); // Bean
    index = addActorDef(index, NEWACTOR_PEARL, 0x107, 0x80689F80, 0x80689FEC, 0, 1); // Pearl
    index = addActorDef(index, NEWACTOR_FAIRY, 0xFC, 0x80689F80, 0x80689FEC, 0, 1); // Fairy
    index = addActorDef(index, NEWACTOR_NULL, 0, 0x80689F80, 0x8068A10C, 0, 1); // Nothing
    index = addActorDef(index, NEWACTOR_MEDAL, 0x109, 0x80689F80, 0x80689FEC, 0, 1); // Medal
    index = addActorDef(index, NEWACTOR_ICETRAPBUBBLE, 0xFD, 0x80689F80, 0x80689FEC, 0, 1); // Fake Item
    index = addActorDef(index, NEWACTOR_ICETRAPREVERSE, 0xFD, 0x80689F80, 0x80689FEC, 0, 1); // Fake Item
    index = addActorDef(index, NEWACTOR_ICETRAPSLOW, 0xFD, 0x80689F80, 0x80689FEC, 0, 1); // Fake Item
    index = addActorDef(index, NEWACTOR_HINTITEM, 0x11A, 0x80689F80, 0x80689FEC, 0, 1); // Hint Item
    *(unsigned short*)(0x8068926A) = getHi(&actor_defs[0].actor_type);
    *(unsigned short*)(0x8068927A) = getLo(&actor_defs[0].actor_type);
    *(unsigned short*)(0x806892D2) = getHi(&actor_defs[0].actor_type);
    *(unsigned short*)(0x806892D6) = getLo(&actor_defs[0].actor_type);
    *(unsigned short*)(0x8068945A) = getHi(&actor_defs[0].actor_type);
    *(unsigned short*)(0x80689466) = getLo(&actor_defs[0].actor_type);
    *(unsigned short*)(0x8068928A) = DEFS_LIMIT;
    *(unsigned short*)(0x80689452) = DEFS_LIMIT;
}

void changeFeatherToSprite(void) {
    actor_defs[24].model = 0;
    actor_master_types[43] = ACTORMASTER_SPRITE;
}

void setActorDamage(int actor, int new_damage) {
    actor_health_damage[actor].damage_applied = new_damage;
}

#define GB_DICTIONARY_COUNT 120
static GBDictItem NewGBDictionary[GB_DICTIONARY_COUNT] = {};

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
    // Initialize addresses
    *(short*)(0x8073150A) = getHi(&NewGBDictionary[0].map);
    *(short*)(0x8073151E) = getLo(&NewGBDictionary[0].map);
    *(short*)(0x8073151A) = GB_DICTIONARY_COUNT;
    *(short*)(0x807315EA) = getHi(&NewGBDictionary[0].map);
    *(short*)(0x807315FE) = getLo(&NewGBDictionary[0].map);
    *(short*)(0x807315FA) = GB_DICTIONARY_COUNT;
    *(short*)(0x80731666) = getHi(&NewGBDictionary[0].map);
    *(short*)(0x80731676) = getLo(&NewGBDictionary[0].map);
    *(short*)(0x80731672) = GB_DICTIONARY_COUNT;
}

void initActorExpansion(void) {
    /**
     * @brief Initialize the Actor Slot Expansion
     */
    // Actor Functions
    dk_memcpy(&actor_functions[0], &ActorFunctions[0], ACTOR_VANILLA_LIMIT*4);
    *(short*)(0x806788F2) = getHi(&actor_functions[0]);
    *(short*)(0x8067890E) = getLo(&actor_functions[0]);
    *(short*)(0x80678A3E) = getHi(&actor_functions[0]);
    *(short*)(0x80678A52) = getLo(&actor_functions[0]);
    *(int*)(0x8076152C) = (int)&actor_functions[0];
    *(int*)(0x80764768) = (int)&actor_functions[0];
    // Actor Collisions
    dk_memcpy(&actor_collisions[0].collision_info, &ActorCollisionArray[0].collision_info, ACTOR_VANILLA_LIMIT*8);
    *(short*)(0x8067586A) = getHi(&actor_collisions[0].collision_info);
    *(short*)(0x80675876) = getLo(&actor_collisions[0].collision_info);
    *(short*)(0x806759F2) = getHi(&actor_collisions[0].unk_4);
    *(short*)(0x80675A02) = getLo(&actor_collisions[0].unk_4);
    *(short*)(0x8067620E) = getHi(&actor_collisions[0].unk_4);
    *(short*)(0x8067621E) = getLo(&actor_collisions[0].unk_4);
    // Actor Health/Damage
    dk_memcpy(&actor_health_damage[0].init_health, &ActorHealthArray[0].init_health, ACTOR_VANILLA_LIMIT*4);
    *(short*)(0x806761D6) = getHi(&actor_health_damage[0].init_health);
    *(short*)(0x806761E2) = getLo(&actor_health_damage[0].init_health);
    *(short*)(0x806761F2) = getHi(&actor_health_damage[0].damage_applied);
    *(short*)(0x806761FE) = getLo(&actor_health_damage[0].damage_applied);
    // Actor Interactions
    dk_memcpy(&actor_interactions[0], &ActorInteractionArray[0], ACTOR_VANILLA_LIMIT*2);
    *(short*)(0x806781BA) = getHi(&actor_interactions[0]);
    *(short*)(0x8067820A) = getLo(&actor_interactions[0]);
    *(short*)(0x8067ACCA) = getHi(&actor_interactions[0]);
    *(short*)(0x8067ACDA) = getLo(&actor_interactions[0]);
    // Actor Master Types
    dk_memcpy(&actor_master_types[0], &ActorMasterType[0], ACTOR_VANILLA_LIMIT);
    *(short*)(0x80677EF6) = getHi(&actor_master_types[0]);
    *(short*)(0x80677F02) = getLo(&actor_master_types[0]);
    *(short*)(0x80677FCA) = getHi(&actor_master_types[0]);
    *(short*)(0x80677FD2) = getLo(&actor_master_types[0]);
    *(short*)(0x80678CDA) = getHi(&actor_master_types[0]);
    *(short*)(0x80678CE6) = getLo(&actor_master_types[0]);
    // Actor Extra Data Sizes
    dk_memcpy(&actor_extra_data_sizes[0], &ActorPaadDefs[0], ACTOR_VANILLA_LIMIT*4);
    *(short*)(0x8067805E) = getHi(&actor_extra_data_sizes[0]);
    *(short*)(0x80678062) = getLo(&actor_extra_data_sizes[0]);
}