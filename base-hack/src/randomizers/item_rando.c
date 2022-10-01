#include "../../include/common.h"

int getObjectCollectability(int id, int unk1, int model2_type) {
    int index = indexOfNextObj(id);
    int* m2location = ObjectModel2Pointer;
    ModelTwoData* _object = getObjectArrayAddr(m2location,0x90,index);
    if (model2_type == 0x11) {
        // Homing
        return (MovesBase[(int)Character].weapon_bitfield & 3) == 3;
    } else if (model2_type == 0x8E) {
        // Crystal
        return crystalsUnlocked(Character);
    } else if (model2_type == 0x8F) {
        // Regular Crate
        return MovesBase[(int)Character].weapon_bitfield & 1;
    } else if (model2_type == 0x90) {
        // Medal
        if (CurrentMap == 0x11) {
            behaviour_data* behaviour = _object->behaviour_pointer;
            if (behaviour) {
                if (behaviour->unk_64 != 0xFF) {
                    return 0;
                }
            }
        }
    } else if (model2_type == 0x98) {
        // Film
        return checkFlag(FLAG_ABILITY_CAMERA,0);
    }
    int collectable_state = _object->collectable_state;
    if (((collectable_state & 8) == 0) || (Player->new_kong == 2)) {
        if (((collectable_state & 2) == 0) || (Player->new_kong == 3)) {
            if (((collectable_state & 4) == 0) || (Player->new_kong == 5)) {
                if (((collectable_state & 0x10) == 0) || (Player->new_kong == 4)) {
                    if ((collectable_state & 1) && (Player->new_kong != 6)) {
                        return 0;
                    }
                    return 1;
                }
                return 0;
            }
            return 0;
        }
        return 0;
    }
    return 0;
}

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

#define COLLISION_LIMIT 45
static collision_info object_collisions[COLLISION_LIMIT] = {};

int addCollisionInfo(int index, int type, int collectable, int kong, int actor_equivalent, int hitbox_y, int hitbox_scale) {
    object_collisions[index].type = type;
    object_collisions[index].collectable_type = collectable;
    object_collisions[index].unk4 = 0.08f;
    object_collisions[index].unk8 = 0.95f;
    object_collisions[index].intended_actor = kong + 2;
    object_collisions[index].actor_equivalent = actor_equivalent;
    object_collisions[index].hitbox_y_center = hitbox_y;
    object_collisions[index].hitbox_scale = hitbox_scale;
    return index + 1;
}

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

void initCollectableCollision(void) {
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
    index = addCollisionInfo(index, 0x00DE, COLLECTABLE_BP, KONG_DK, 0x4E, 0, 0);
    index = addCollisionInfo(index, 0x00E0, COLLECTABLE_BP, KONG_DIDDY, 0x4B, 0, 0);
    index = addCollisionInfo(index, 0x00E1, COLLECTABLE_BP, KONG_LANKY, 0x4D, 0, 0);
    index = addCollisionInfo(index, 0x00DD, COLLECTABLE_BP, KONG_TINY, 0x4F, 0, 0);
    index = addCollisionInfo(index, 0x00DF, COLLECTABLE_BP, KONG_CHUNKY, 0x4C, 0, 0);
    // Multiplayer
    index = addCollisionInfo(index, 0x00B7, COLLECTABLE_COIN, KONG_NONE, 0x8C, 0, 0); // Rainbow Coin
    index = addCollisionInfo(index, 0x01CF, COLLECTABLE_NONE, KONG_NONE, 0x78, 0, 0); // Yellow CB Powerup
    index = addCollisionInfo(index, 0x01D0, COLLECTABLE_NONE, KONG_NONE, 0x77, 0, 0); // Blue CB Powerup
    index = addCollisionInfo(index, 0x01D1, COLLECTABLE_NONE, KONG_NONE, 0x76, 0, 0); // Coin Powerup
    index = addCollisionInfo(index, 0x01D2, COLLECTABLE_COIN, KONG_NONE, 0x7A, 0, 0); // Coin Multiplayer
    // Others
    index = addCollisionInfo(index, 0x0074, COLLECTABLE_GB, KONG_NONE, 0x2D, 8, 4); // Golden Banana
    index = addCollisionInfo(index, 0x0056, COLLECTABLE_ORANGE, KONG_NONE, 0x34, 0, 0); // Orange
    index = addCollisionInfo(index, 0x008F, COLLECTABLE_AMMOBOX, KONG_NONE, 0x33, 0, 0); // Ammo Crate
    index = addCollisionInfo(index, 0x0011, COLLECTABLE_AMMOBOX, KONG_NONE, 0, 0, 0); // Homing Ammo Crate
    index = addCollisionInfo(index, 0x008E, COLLECTABLE_CRYSTAL, KONG_NONE, 0x79, 0, 0); // Crystal
    index = addCollisionInfo(index, 0x0057, COLLECTABLE_NONE, KONG_NONE, 0x2F, 0, 0); // Watermelon
    index = addCollisionInfo(index, 0x0098, COLLECTABLE_FILM, KONG_NONE, 0, 0, 0); // Film
    index = addCollisionInfo(index, 0x0090, COLLECTABLE_MEDAL, KONG_NONE, 0, 0, 0); // Medal
    index = addCollisionInfo(index, 0x00EC, COLLECTABLE_RACECOIN, KONG_NONE, 0x36, 0, 0); // Race Coin
    index = addCollisionInfo(index, 0x013C, COLLECTABLE_NONE, KONG_NONE, 0x48, 0, 0); // Boss Key
    index = addCollisionInfo(index, 0x018D, COLLECTABLE_NONE, KONG_NONE, 0x56, 0, 0); // Battle Crown
    index = addCollisionInfo(index, 0x0288, COLLECTABLE_GB, KONG_NONE, 0x7A, 8, 4); // Rareware GB
    index = addCollisionInfo(index, 0x0048, COLLECTABLE_NONE, KONG_NONE, 0, 0, 0); // Nintendo Coin
    index = addCollisionInfo(index, 0x028F, COLLECTABLE_NONE, KONG_NONE, 0, 0, 0); // Rareware Coin
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