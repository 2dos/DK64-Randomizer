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

typedef struct collision_info {
    /* 0x000 */ unsigned short type;
    /* 0x002 */ char collectable_type;
    /* 0x003 */ char unk3;
    /* 0x004 */ float unk4;
    /* 0x008 */ float unk8;
    /* 0x00C */ short intended_actor;
    /* 0x00E */ short actor_equivalent;
    /* 0x010 */ short hitbox_y_center;
    /* 0x012 */ short hitbox_scale;
} collision_info;

#define COLLISION_LIMIT 59
#define DEFS_LIMIT 147
static collision_info object_collisions[COLLISION_LIMIT] = {};
static actor_behaviour_def actor_defs[DEFS_LIMIT] = {};

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

int addCollisionInfo(int index, int type, int collectable, int kong, int actor_equivalent, int hitbox_y, int hitbox_scale) {
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
     * @param hitbox_scale Hitbox Radius, in units
     * 
     * @return following index
     */
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
    object_collisions[index].hitbox_scale = hitbox_scale;
    return index + 1;
}

void initCollectableCollision(void) {
    /**
     * @brief Initialize all collectable collisions
     */
    // Single
    int index = addCollisionInfo(0, 0x000D, COLLECTABLE_CB, KONG_DK, 0, 0, 0);
    index = addCollisionInfo(index, 0x000A, COLLECTABLE_CB, KONG_DIDDY, 0, 0, 0);
    index = addCollisionInfo(index, 0x001F, COLLECTABLE_CB, KONG_CHUNKY, 0, 0, 0);
    index = addCollisionInfo(index, 0x001E, COLLECTABLE_CB, KONG_LANKY, 0, 0, 0);
    index = addCollisionInfo(index, 0x0016, COLLECTABLE_CB, KONG_TINY, 0, 0, 0);
    // Coin
    index = addCollisionInfo(index, 0x0024, COLLECTABLE_COIN, KONG_DIDDY, 0, 0, 0);
    index = addCollisionInfo(index, 0x0023, COLLECTABLE_COIN, KONG_LANKY, 0x35, 0, 0);
    index = addCollisionInfo(index, 0x0027, COLLECTABLE_COIN, KONG_CHUNKY, 0, 0, 0);
    index = addCollisionInfo(index, 0x001C, COLLECTABLE_COIN, KONG_TINY, 0, 0, 0);
    index = addCollisionInfo(index, 0x001D, COLLECTABLE_COIN, KONG_DK, 0, 0, 0);
    // Bunch
    index = addCollisionInfo(index, 0x002B, COLLECTABLE_CB, KONG_DK, 0, 0, 0);
    index = addCollisionInfo(index, 0x0208, COLLECTABLE_CB, KONG_DIDDY, 0, 0, 0);
    index = addCollisionInfo(index, 0x0206, COLLECTABLE_CB, KONG_CHUNKY, 0x6E, 0, 0);
    index = addCollisionInfo(index, 0x0205, COLLECTABLE_CB, KONG_LANKY, 0, 0, 0);
    index = addCollisionInfo(index, 0x0207, COLLECTABLE_CB, KONG_TINY, 0, 0, 0);
    // Pellets
    index = addCollisionInfo(index, 0x0091, COLLECTABLE_AMMOPELLET, KONG_NONE, 0, 0, 0); // Peanut
    index = addCollisionInfo(index, 0x015D, COLLECTABLE_AMMOPELLET, KONG_NONE, 0, 0, 0); // Feather
    index = addCollisionInfo(index, 0x015E, COLLECTABLE_AMMOPELLET, KONG_NONE, 0, 0, 0); // Grape
    index = addCollisionInfo(index, 0x015F, COLLECTABLE_AMMOPELLET, KONG_NONE, 0, 0, 0); // Pineapple
    index = addCollisionInfo(index, 0x0160, COLLECTABLE_AMMOPELLET, KONG_NONE, 0, 0, 0); // Coconut
    // Blueprint
    index = addCollisionInfo(index, 0x00DE, COLLECTABLE_BP, KONG_DK, 0x4E, 8, 4);
    index = addCollisionInfo(index, 0x00E0, COLLECTABLE_BP, KONG_DIDDY, 0x4B, 8, 4);
    index = addCollisionInfo(index, 0x00E1, COLLECTABLE_BP, KONG_LANKY, 0x4D, 8, 4);
    index = addCollisionInfo(index, 0x00DD, COLLECTABLE_BP, KONG_TINY, 0x4F, 8, 4);
    index = addCollisionInfo(index, 0x00DF, COLLECTABLE_BP, KONG_CHUNKY, 0x4C, 8, 4);
    // Multiplayer
    index = addCollisionInfo(index, 0x00B7, COLLECTABLE_COIN, KONG_NONE, 0x8C, 8, 4); // Rainbow Coin
    index = addCollisionInfo(index, 0x01CF, COLLECTABLE_NONE, KONG_NONE, 0x78, 0, 0); // Yellow CB Powerup
    index = addCollisionInfo(index, 0x01D0, COLLECTABLE_NONE, KONG_NONE, 0x77, 0, 0); // Blue CB Powerup
    index = addCollisionInfo(index, 0x01D1, COLLECTABLE_NONE, KONG_NONE, 0x76, 0, 0); // Coin Powerup
    index = addCollisionInfo(index, 0x01D2, COLLECTABLE_COIN, KONG_NONE, 0x7A, 0, 0); // Coin Multiplayer
    // Potions
    index = addCollisionInfo(index, 0x005B, COLLECTABLE_NONE, KONG_NONE, 157, 8, 4); // Potion DK
    index = addCollisionInfo(index, 0x01F2, COLLECTABLE_NONE, KONG_NONE, 158, 8, 4); // Potion Diddy
    index = addCollisionInfo(index, 0x0059, COLLECTABLE_NONE, KONG_NONE, 159, 8, 4); // Potion Lanky
    index = addCollisionInfo(index, 0x01F3, COLLECTABLE_NONE, KONG_NONE, 160, 8, 4); // Potion Tiny
    index = addCollisionInfo(index, 0x01F5, COLLECTABLE_NONE, KONG_NONE, 161, 8, 4); // Potion Chunky
    index = addCollisionInfo(index, 0x01F6, COLLECTABLE_NONE, KONG_NONE, 162, 8, 4); // Potion Any
    // Kongs
    index = addCollisionInfo(index, 0x0257, COLLECTABLE_NONE, KONG_NONE, 141, 8, 4); // DK
    index = addCollisionInfo(index, 0x0258, COLLECTABLE_NONE, KONG_NONE, 142, 8, 4); // Diddy
    index = addCollisionInfo(index, 0x0259, COLLECTABLE_NONE, KONG_NONE, 143, 8, 4); // Lanky
    index = addCollisionInfo(index, 0x025A, COLLECTABLE_NONE, KONG_NONE, 144, 8, 4); // Tiny
    index = addCollisionInfo(index, 0x025B, COLLECTABLE_NONE, KONG_NONE, 155, 8, 4); // Chunky
    // Others
    index = addCollisionInfo(index, 0x0074, COLLECTABLE_GB, KONG_NONE, 0x2D, 8, 4); // Golden Banana
    index = addCollisionInfo(index, 0x0056, COLLECTABLE_ORANGE, KONG_NONE, 0x34, 0, 0); // Orange
    index = addCollisionInfo(index, 0x008F, COLLECTABLE_AMMOBOX, KONG_NONE, 0x33, 0, 0); // Ammo Crate
    index = addCollisionInfo(index, 0x0011, COLLECTABLE_AMMOBOX, KONG_NONE, 0, 0, 0); // Homing Ammo Crate
    index = addCollisionInfo(index, 0x008E, COLLECTABLE_CRYSTAL, KONG_NONE, 0x79, 0, 0); // Crystal
    index = addCollisionInfo(index, 0x0057, COLLECTABLE_NONE, KONG_NONE, 0x2F, 0, 0); // Watermelon
    index = addCollisionInfo(index, 0x0098, COLLECTABLE_FILM, KONG_NONE, 0, 0, 0); // Film
    index = addCollisionInfo(index, 0x0090, COLLECTABLE_MEDAL, KONG_NONE, 154, 8, 4); // Medal
    index = addCollisionInfo(index, 0x00EC, COLLECTABLE_RACECOIN, KONG_NONE, 0x36, 0, 0); // Race Coin
    index = addCollisionInfo(index, 0x013C, COLLECTABLE_NONE, KONG_NONE, 0x48, 8, 4); // Boss Key
    index = addCollisionInfo(index, 0x018D, COLLECTABLE_NONE, KONG_NONE, 0x56, 8, 4); // Battle Crown
    index = addCollisionInfo(index, 0x0288, COLLECTABLE_GB, KONG_NONE, 0x2D, 8, 4); // Rareware GB
    index = addCollisionInfo(index, 0x0048, COLLECTABLE_NONE, KONG_NONE, 151, 8, 4); // Nintendo Coin
    index = addCollisionInfo(index, 0x028F, COLLECTABLE_NONE, KONG_NONE, 152, 8, 4); // Rareware Coin
    index = addCollisionInfo(index, 0x0198, COLLECTABLE_NONE, KONG_NONE, 172, 8, 4); // Bean
    index = addCollisionInfo(index, 0x01B4, COLLECTABLE_NONE, KONG_NONE, 174, 8, 4); // Pearl
    index = addCollisionInfo(index, 0x025C, COLLECTABLE_NONE, KONG_NONE, 88, 8, 4); // Fairy
    index = addCollisionInfo(index, 0x025D, COLLECTABLE_NONE, KONG_NONE, 217, 8, 4); // Fake Item
    
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
}

int addActorDef(int index, int actor, int model, unsigned int func_0, unsigned int func_1, int rescale) {
    /**
     * @brief Add actor to the actor definition table
     * 
     * @param index Index inside the definition table
     * @param actor Actor Index
     * @param model Model that the actor will have upon being spawned
     * @param func_0 Unknown function
     * @param func_1 Unknown function
     * @param rescale Rescale actor (Set to 0 to have default)
     * 
     * @return following index
     */
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
    int index = addActorDef(128, 151, 0, 0x80689F80, 0x8068A10C, 0); // Nintendo Coin
    index = addActorDef(index, 152, 0, 0x80689F80, 0x8068A10C, 0); // Rareware Coin
    // Potions
    index = addActorDef(index, 157, 0xEE, 0x80689F80, 0x80689FEC, 0); // DK Potion
    index = addActorDef(index, 158, 0xEF, 0x80689F80, 0x80689FEC, 0); // Diddy Potion
    index = addActorDef(index, 159, 0xF0, 0x80689F80, 0x80689FEC, 0); // Lanky Potion
    index = addActorDef(index, 160, 0xF1, 0x80689F80, 0x80689FEC, 0); // Tiny Potion
    index = addActorDef(index, 161, 0xF2, 0x80689F80, 0x80689FEC, 0); // Chunky Potion
    index = addActorDef(index, 162, 0xF3, 0x80689F80, 0x80689FEC, 0); // Any Potion
    // Kongs
    index = addActorDef(index, 141, 0x4, 0x80689F80, 0x80689FEC, 0); // DK
    index = addActorDef(index, 142, 0x1, 0x80689F80, 0x80689FEC, 0); // Diddy
    index = addActorDef(index, 143, 0x6, 0x80689F80, 0x80689FEC, 0); // Lanky
    index = addActorDef(index, 144, 0x9, 0x80689F80, 0x80689FEC, 0); // Tiny
    index = addActorDef(index, 155, 0xC, 0x80689F80, 0x80689FEC, 0); // Chunky
    // Misc
    index = addActorDef(index, 172, 0, 0x80689F80, 0x8068A10C, 0); // Bean
    index = addActorDef(index, 174, 0, 0x80689F80, 0x8068A10C, 0); // Pearl
    index = addActorDef(index, 88, 0xFC, 0x80689F80, 0x80689FEC, 0); // Fairy
    index = addActorDef(index, 153, 0, 0x80689F80, 0x8068A10C, 0); // Nothing
    index = addActorDef(index, 154, 0, 0x80689F80, 0x8068A10C, 0); // Medal
    index = addActorDef(index, 217, 0x10E, 0x80689F80, 0x80689FEC, 0); // Fake Item
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