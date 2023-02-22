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

collision_info object_collisions[COLLISION_LIMIT] = {};
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

int addCollisionInfo(int index, int type, int collectable, int kong, int actor_equivalent, int hitbox_y, int hitbox_radius, int hitbox_height, int is_custom) {
    /**
     * @brief Add an item to the collision table. This will mean that picking it up will set the flag determined by the 
     * flag mapping table in the vanilla game, as well as enabling you to pick up actors and for them to register properly.
     * 
     * @param index Index of item in the table
     * @param type Object Model 2 type
     * @param collectable Collectable Index
     * @param kong Intended kong for this item. Set to 0 if no kong
     * @param actor_equivalent Actor equivalent of the Object Model 2 type
     * @param hitbox_y Hitbox Y Offset from the actor/OM2 position, in units
     * @param hitbox_radius Hitbox Radius, in units
     * @param hitbox_height Hitbox height for cylindrical hitboxes
     * @param is_custom Is Custom object, add offset
     * 
     * @return following index
     */
    if (is_custom) {
        actor_equivalent += CUSTOM_ACTORS_START;
    }
    object_collisions[index].type = type;
    object_collisions[index].collectable_type = collectable;
    object_collisions[index].unk4 = 0.08f;
    object_collisions[index].unk8 = 0.95f;
    object_collisions[index].intended_actor = kong + 2;
    if ((Rando.any_kong_items & 2) && (collectable == COLLECTABLE_BP)) {
        // Blueprints
        object_collisions[index].intended_actor = 0;
    }
    object_collisions[index].actor_equivalent = actor_equivalent;
    object_collisions[index].hitbox_y_center = hitbox_y;
    object_collisions[index].hitbox_radius = hitbox_radius;
    object_collisions[index].hitbox_height = hitbox_height;
    return index + 1;
}

void initCollectableCollision(void) {
    /**
     * @brief Initialize all collectable collisions
     */
    // Single
    int index = addCollisionInfo(0, 0x000D, COLLECTABLE_CB, KONG_DK, 0, 0, 0, 0, 0);
    index = addCollisionInfo(index, 0x000A, COLLECTABLE_CB, KONG_DIDDY, 0, 0, 0, 0, 0);
    index = addCollisionInfo(index, 0x001F, COLLECTABLE_CB, KONG_CHUNKY, 0, 0, 0, 0, 0);
    index = addCollisionInfo(index, 0x001E, COLLECTABLE_CB, KONG_LANKY, 0, 0, 0, 0, 0);
    index = addCollisionInfo(index, 0x0016, COLLECTABLE_CB, KONG_TINY, 0, 0, 0, 0, 0);
    // Coin
    index = addCollisionInfo(index, 0x0024, COLLECTABLE_COIN, KONG_DIDDY, 0, 0, 0, 0, 0);
    index = addCollisionInfo(index, 0x0023, COLLECTABLE_COIN, KONG_LANKY, 0x35, 0, 0, 0, 0);
    index = addCollisionInfo(index, 0x0027, COLLECTABLE_COIN, KONG_CHUNKY, 0, 0, 0, 0, 0);
    index = addCollisionInfo(index, 0x001C, COLLECTABLE_COIN, KONG_TINY, 0, 0, 0, 0, 0);
    index = addCollisionInfo(index, 0x001D, COLLECTABLE_COIN, KONG_DK, 0, 0, 0, 0, 0);
    // Bunch
    index = addCollisionInfo(index, 0x002B, COLLECTABLE_CB, KONG_DK, 0, 0, 0, 0, 0);
    index = addCollisionInfo(index, 0x0208, COLLECTABLE_CB, KONG_DIDDY, 0, 0, 0, 0, 0);
    index = addCollisionInfo(index, 0x0206, COLLECTABLE_CB, KONG_CHUNKY, 0x6E, 0, 0, 0, 0);
    index = addCollisionInfo(index, 0x0205, COLLECTABLE_CB, KONG_LANKY, 0, 0, 0, 0, 0);
    index = addCollisionInfo(index, 0x0207, COLLECTABLE_CB, KONG_TINY, 0, 0, 0, 0, 0);
    // Pellets
    index = addCollisionInfo(index, 0x0091, COLLECTABLE_AMMOPELLET, KONG_NONE, 0, 0, 0, 0, 0); // Peanut
    index = addCollisionInfo(index, 0x015D, COLLECTABLE_AMMOPELLET, KONG_NONE, 0, 0, 0, 0, 0); // Feather
    index = addCollisionInfo(index, 0x015E, COLLECTABLE_AMMOPELLET, KONG_NONE, 0, 0, 0, 0, 0); // Grape
    index = addCollisionInfo(index, 0x015F, COLLECTABLE_AMMOPELLET, KONG_NONE, 0, 0, 0, 0, 0); // Pineapple
    index = addCollisionInfo(index, 0x0160, COLLECTABLE_AMMOPELLET, KONG_NONE, 0, 0, 0, 0, 0); // Coconut
    // Blueprint
    index = addCollisionInfo(index, 0x00DE, COLLECTABLE_BP, KONG_DK, 0x4E, 8, 4, 13, 0);
    index = addCollisionInfo(index, 0x00E0, COLLECTABLE_BP, KONG_DIDDY, 0x4B, 8, 4, 13, 0);
    index = addCollisionInfo(index, 0x00E1, COLLECTABLE_BP, KONG_LANKY, 0x4D, 8, 4, 13, 0);
    index = addCollisionInfo(index, 0x00DD, COLLECTABLE_BP, KONG_TINY, 0x4F, 8, 4, 13, 0);
    index = addCollisionInfo(index, 0x00DF, COLLECTABLE_BP, KONG_CHUNKY, 0x4C, 8, 4, 13, 0);
    // Multiplayer
    index = addCollisionInfo(index, 0x00B7, COLLECTABLE_COIN, KONG_NONE, 0x8C, 8, 4, 13, 0); // Rainbow Coin
    index = addCollisionInfo(index, 0x01CF, COLLECTABLE_NONE, KONG_NONE, 0x78, 0, 0, 0, 0); // Yellow CB Powerup
    index = addCollisionInfo(index, 0x01D0, COLLECTABLE_NONE, KONG_NONE, 0x77, 0, 0, 0, 0); // Blue CB Powerup
    index = addCollisionInfo(index, 0x01D1, COLLECTABLE_NONE, KONG_NONE, 0x76, 0, 0, 0, 0); // Coin Powerup
    index = addCollisionInfo(index, 0x01D2, COLLECTABLE_COIN, KONG_NONE, 0x7A, 0, 0, 0, 0); // Coin Multiplayer
    // Potions
    index = addCollisionInfo(index, 0x005B, COLLECTABLE_NONE, KONG_NONE, NEWACTOR_POTIONDK, 8, 4, 13, 1); // Potion DK
    index = addCollisionInfo(index, 0x01F2, COLLECTABLE_NONE, KONG_NONE, NEWACTOR_POTIONDIDDY, 8, 4, 13, 1); // Potion Diddy
    index = addCollisionInfo(index, 0x0059, COLLECTABLE_NONE, KONG_NONE, NEWACTOR_POTIONLANKY, 8, 4, 13, 1); // Potion Lanky
    index = addCollisionInfo(index, 0x01F3, COLLECTABLE_NONE, KONG_NONE, NEWACTOR_POTIONTINY, 8, 4, 13, 1); // Potion Tiny
    index = addCollisionInfo(index, 0x01F5, COLLECTABLE_NONE, KONG_NONE, NEWACTOR_POTIONCHUNKY, 8, 4, 13, 1); // Potion Chunky
    index = addCollisionInfo(index, 0x01F6, COLLECTABLE_NONE, KONG_NONE, NEWACTOR_POTIONANY, 8, 4, 13, 1); // Potion Any
    // Kongs
    index = addCollisionInfo(index, 0x0257, COLLECTABLE_NONE, KONG_NONE, NEWACTOR_KONGDK, 8, 4, 13, 1); // DK
    index = addCollisionInfo(index, 0x0258, COLLECTABLE_NONE, KONG_NONE, NEWACTOR_KONGDIDDY, 8, 4, 13, 1); // Diddy
    index = addCollisionInfo(index, 0x0259, COLLECTABLE_NONE, KONG_NONE, NEWACTOR_KONGLANKY, 8, 4, 13, 1); // Lanky
    index = addCollisionInfo(index, 0x025A, COLLECTABLE_NONE, KONG_NONE, NEWACTOR_KONGTINY, 8, 4, 13, 1); // Tiny
    index = addCollisionInfo(index, 0x025B, COLLECTABLE_NONE, KONG_NONE, NEWACTOR_KONGCHUNKY, 8, 4, 13, 1); // Chunky
    // Others
    index = addCollisionInfo(index, 0x0074, COLLECTABLE_GB, KONG_NONE, 0x2D, 8, 4, 13, 0); // Golden Banana
    index = addCollisionInfo(index, 0x0056, COLLECTABLE_ORANGE, KONG_NONE, 0x34, 0, 0, 0, 0); // Orange
    index = addCollisionInfo(index, 0x008F, COLLECTABLE_AMMOBOX, KONG_NONE, 0x33, 0, 0, 0, 0); // Ammo Crate
    index = addCollisionInfo(index, 0x0011, COLLECTABLE_AMMOBOX, KONG_NONE, 0, 0, 0, 0, 0); // Homing Ammo Crate
    index = addCollisionInfo(index, 0x008E, COLLECTABLE_CRYSTAL, KONG_NONE, 0x79, 0, 0, 0, 0); // Crystal
    index = addCollisionInfo(index, 0x0057, COLLECTABLE_NONE, KONG_NONE, 0x2F, 0, 0, 0, 0); // Watermelon
    index = addCollisionInfo(index, 0x025E, COLLECTABLE_NONE, KONG_NONE, 0, 8, 4, 13, 0); // Watermelon - Duplicate
    index = addCollisionInfo(index, 0x0098, COLLECTABLE_FILM, KONG_NONE, 0, 0, 0, 0, 0); // Film
    index = addCollisionInfo(index, 0x0090, COLLECTABLE_MEDAL, KONG_NONE, NEWACTOR_MEDAL, 8, 4, 13, 1); // Medal
    index = addCollisionInfo(index, 0x00EC, COLLECTABLE_RACECOIN, KONG_NONE, 0x36, 0, 0, 0, 0); // Race Coin
    index = addCollisionInfo(index, 0x013C, COLLECTABLE_NONE, KONG_NONE, 0x48, 8, 4, 13, 0); // Boss Key
    index = addCollisionInfo(index, 0x018D, COLLECTABLE_NONE, KONG_NONE, 0x56, 8, 4, 13, 0); // Battle Crown
    index = addCollisionInfo(index, 0x0288, COLLECTABLE_GB, KONG_NONE, 0x2D, 8, 4, 13, 0); // Rareware GB
    index = addCollisionInfo(index, 0x0048, COLLECTABLE_NONE, KONG_NONE, NEWACTOR_NINTENDOCOIN, 8, 4, 13, 1); // Nintendo Coin
    index = addCollisionInfo(index, 0x028F, COLLECTABLE_NONE, KONG_NONE, NEWACTOR_RAREWARECOIN, 8, 4, 13, 1); // Rareware Coin
    index = addCollisionInfo(index, 0x0198, COLLECTABLE_NONE, KONG_NONE, NEWACTOR_BEAN, 8, 4, 13, 1); // Bean
    index = addCollisionInfo(index, 0x01B4, COLLECTABLE_NONE, KONG_NONE, NEWACTOR_PEARL, 8, 4, 13, 1); // Pearl
    index = addCollisionInfo(index, 0x025C, COLLECTABLE_NONE, KONG_NONE, NEWACTOR_FAIRY, 8, 4, 13, 1); // Fairy
    index = addCollisionInfo(index, 0x025D, COLLECTABLE_NONE, KONG_NONE, NEWACTOR_FAKEITEM, 8, 4, 13, 1); // Fake Item
    
    // Write new table to ROM
    int hi = getHi(&object_collisions[0].type);
    int lo = getLo(&object_collisions[0].type);
    *(unsigned short*)(0x806F48D2) = hi;
    *(unsigned short*)(0x806F48D6) = lo;
    *(unsigned short*)(0x806F4A8E) = index;
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
    *(unsigned short*)(0x806F7996) = getHi(&object_collisions[index].type);
    *(unsigned short*)(0x806F799A) = getLo(&object_collisions[index].type);
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

void initActorDefs(void) {
    /**
     * @brief Initialize actor definitions table
     */
    dk_memcpy(&actor_defs[0], &ActorBehaviourTable[0], 128*sizeof(actor_behaviour_def));
    int index = addActorDef(128, NEWACTOR_NINTENDOCOIN, 0, 0x80689F80, 0x8068A10C, 0, 1); // Nintendo Coin
    index = addActorDef(index, NEWACTOR_RAREWARECOIN, 0, 0x80689F80, 0x8068A10C, 0, 1); // Rareware Coin
    // Potions
    index = addActorDef(index, NEWACTOR_POTIONDK, 0xEE, 0x80689F80, 0x80689FEC, 0, 1); // DK Potion
    index = addActorDef(index, NEWACTOR_POTIONDIDDY, 0xEF, 0x80689F80, 0x80689FEC, 0, 1); // Diddy Potion
    index = addActorDef(index, NEWACTOR_POTIONLANKY, 0xF0, 0x80689F80, 0x80689FEC, 0, 1); // Lanky Potion
    index = addActorDef(index, NEWACTOR_POTIONTINY, 0xF1, 0x80689F80, 0x80689FEC, 0, 1); // Tiny Potion
    index = addActorDef(index, NEWACTOR_POTIONCHUNKY, 0xF2, 0x80689F80, 0x80689FEC, 0, 1); // Chunky Potion
    index = addActorDef(index, NEWACTOR_POTIONANY, 0xF3, 0x80689F80, 0x80689FEC, 0, 1); // Any Potion
    // Kongs
    index = addActorDef(index, NEWACTOR_KONGDK, 0x4, 0x80689F80, 0x80689FEC, 0, 1); // DK
    index = addActorDef(index, NEWACTOR_KONGDIDDY, 0x1, 0x80689F80, 0x80689FEC, 0, 1); // Diddy
    index = addActorDef(index, NEWACTOR_KONGLANKY, 0x6, 0x80689F80, 0x80689FEC, 0, 1); // Lanky
    index = addActorDef(index, NEWACTOR_KONGTINY, 0x9, 0x80689F80, 0x80689FEC, 0, 1); // Tiny
    index = addActorDef(index, NEWACTOR_KONGCHUNKY, 0xC, 0x80689F80, 0x80689FEC, 0, 1); // Chunky
    // Misc
    index = addActorDef(index, NEWACTOR_BEAN, 0, 0x80689F80, 0x8068A10C, 0, 1); // Bean
    index = addActorDef(index, NEWACTOR_PEARL, 0, 0x80689F80, 0x8068A10C, 0, 1); // Pearl
    index = addActorDef(index, NEWACTOR_FAIRY, 0xFC, 0x80689F80, 0x80689FEC, 0, 1); // Fairy
    index = addActorDef(index, NEWACTOR_NULL, 0, 0x80689F80, 0x8068A10C, 0, 1); // Nothing
    index = addActorDef(index, NEWACTOR_MEDAL, 0, 0x80689F80, 0x8068A10C, 0, 1); // Medal
    index = addActorDef(index, NEWACTOR_FAKEITEM, 0x10F, 0x80689F80, 0x80689FEC, 0, 1); // Fake Item
    *(unsigned short*)(0x8068926A) = getHi(&actor_defs[0].actor_type);
    *(unsigned short*)(0x8068927A) = getLo(&actor_defs[0].actor_type);
    *(unsigned short*)(0x806892D2) = getHi(&actor_defs[0].actor_type);
    *(unsigned short*)(0x806892D6) = getLo(&actor_defs[0].actor_type);
    *(unsigned short*)(0x8068945A) = getHi(&actor_defs[0].actor_type);
    *(unsigned short*)(0x80689466) = getLo(&actor_defs[0].actor_type);
    *(unsigned short*)(0x8068928A) = DEFS_LIMIT;
    *(unsigned short*)(0x80689452) = DEFS_LIMIT;
}

#define GB_DICTIONARY_COUNT 120
static GBDictItem NewGBDictionary[GB_DICTIONARY_COUNT] = {};

int addDictionaryItem(int index, int map, int id, int flag, int kong) {
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
        if ((map == 0x22) && (id == 4)) {
            kong = Rando.starting_kong;
        } else if ((map == 0x7) && ((id == 0x69) || (id == 0x48))) {
            kong = Rando.free_source_japes;
        } else if ((map == 0x10) && (id == 0x5B)) {
            kong = Rando.free_source_ttemple;
        } else if ((map == 0x14) && (id == 0x6C)) {
            kong = Rando.free_source_llama;
        } else if ((map == 0x1A) && (id == 0x78)) {
            kong = Rando.free_source_factory;
        } else if ((map == 0x11) && (id == 0x5E)) {
            flag = 0x24C;
        } else if ((map == 0x11) && (id == 0x61)) {
            flag = 0x249;
        }
        NewGBDictionary[i].intended_kong_actor = kong + 2;
        NewGBDictionary[i].flag_index = flag;
        if ((flag == FLAG_ARCADE_ROUND1) && (Rando.fast_gbs)) {
            NewGBDictionary[i].map = 0x6E;
            NewGBDictionary[i].model2_id = 0;
        }
    }
    // Add new entries
    int size = addDictionaryItem(113, 0x2C, 0, FLAG_PEARL_0_COLLECTED, -2);
    for (int i = 1; i < 5; i++) {
        size = addDictionaryItem(size, 0x2C, i, FLAG_PEARL_0_COLLECTED + i, -2);
    }
    size = addDictionaryItem(size, 0x34, 5, FLAG_COLLECTABLE_BEAN, -2);
    if (Rando.quality_of_life.vanilla_fixes) {
        size = addDictionaryItem(size, 0x11, 0x5A, FLAG_KEYHAVE_KEY8, -2); // Fake Key backup fix
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