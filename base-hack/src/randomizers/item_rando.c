#include "../../include/common.h"

int getObjectCollectability(int id, int unk1, int model2_type) {
    int index = indexOfNextObj(id);
    int* m2location = (int*)ObjectModel2Pointer;
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

#define COLLISION_LIMIT 57
#define DEFS_LIMIT 145
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
    index = addCollisionInfo(index, 0x00B7, COLLECTABLE_COIN, KONG_NONE, 0x8C, 0, 0); // Rainbow Coin
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

int addActorDef(int index, int actor, int model, unsigned int func_0, unsigned int func_1) {
    actor_defs[index].actor_type = actor;
    actor_defs[index].model = model;
    actor_defs[index].unk4[4] = 0x02;
    actor_defs[index].unk4[5] = 0x26;
    actor_defs[index].code = (void*)func_0;
    actor_defs[index].unk10 = (void*)func_1;
    return index + 1;
}

void initActorDefs(void) {
    dk_memcpy(&actor_defs[0], &ActorBehaviourTable[0], 128*sizeof(actor_behaviour_def));
    int index = addActorDef(128, 151, 0, 0x80689F80, 0x8068A10C); // Nintendo Coin
    index = addActorDef(index, 152, 0, 0x80689F80, 0x8068A10C); // Rareware Coin
    // Potions
    index = addActorDef(index, 157, 0xEE, 0x80689F80, 0x80689FEC); // DK Potion
    index = addActorDef(index, 158, 0xEF, 0x80689F80, 0x80689FEC); // Diddy Potion
    index = addActorDef(index, 159, 0xF0, 0x80689F80, 0x80689FEC); // Lanky Potion
    index = addActorDef(index, 160, 0xF1, 0x80689F80, 0x80689FEC); // Tiny Potion
    index = addActorDef(index, 161, 0xF2, 0x80689F80, 0x80689FEC); // Chunky Potion
    index = addActorDef(index, 162, 0xF3, 0x80689F80, 0x80689FEC); // Any Potion
    index = addActorDef(index, 153, 0, 0x80689F80, 0x8068A10C); // Nothing
    index = addActorDef(index, 154, 0, 0x80689F80, 0x8068A10C); // Medal
    // Kongs
    index = addActorDef(index, 141, 0x4, 0x80689F80, 0x80689FEC); // DK
    index = addActorDef(index, 142, 0x1, 0x80689F80, 0x80689FEC); // Diddy
    index = addActorDef(index, 143, 0x6, 0x80689F80, 0x80689FEC); // Lanky
    index = addActorDef(index, 144, 0x9, 0x80689F80, 0x80689FEC); // Tiny
    index = addActorDef(index, 155, 0xC, 0x80689F80, 0x80689FEC); // Chunky
    // Misc
    index = addActorDef(index, 172, 0, 0x80689F80, 0x8068A10C); // Bean
    index = addActorDef(index, 174, 0, 0x80689F80, 0x8068A10C); // Pearl
    *(unsigned short*)(0x8068926A) = getHi(&actor_defs[0].actor_type);
    *(unsigned short*)(0x8068927A) = getLo(&actor_defs[0].actor_type);
    *(unsigned short*)(0x806892D2) = getHi(&actor_defs[0].actor_type);
    *(unsigned short*)(0x806892D6) = getLo(&actor_defs[0].actor_type);
    *(unsigned short*)(0x8068945A) = getHi(&actor_defs[0].actor_type);
    *(unsigned short*)(0x80689466) = getLo(&actor_defs[0].actor_type);
    *(unsigned short*)(0x8068928A) = DEFS_LIMIT;
    *(unsigned short*)(0x80689452) = DEFS_LIMIT;
}

void spawnBonusReward(int object, int x_f, int y_f, int z_f, int unk0, int cutscene, int flag, int unk1) {
    bonus_paad* paad = CurrentActorPointer_0->paad;
    int index = paad->barrel_index;
    if ((index > 0) && (index < 95)) {
        object = bonus_data[index].spawn_actor;
    }
    if (object != 153) {
        spawnActorWithFlag(object, x_f, y_f, z_f, unk0, cutscene, flag, unk1);
    }
}

void spawnRewardAtActor(int object, int flag) {
    int index = CurrentActorPointer_0->reward_index;
    if ((index > 0) && (index < 95)) {
        object = bonus_data[index].spawn_actor;
    }
    if (object != 153) {
        spawnObjectAtActor(object, flag);
    }
}

void spawnMinecartReward(int object, int flag) {
    for (int i = 0; i < 95; i++) {
        if (bonus_data[i].flag == flag) {
            if (bonus_data[i].spawn_actor != 153) {
                spawnObjectAtActor(bonus_data[i].spawn_actor, flag);
            }
            return;
        }
    }
}

void spawnCrownReward(int object, int x_f, int y_f, int z_f, int unk0, int cutscene, int flag, int unk1) {
    int new_obj = getCrownItem(CurrentMap);
    if (new_obj != 0) {
        object = new_obj;
    }
    if (object != 153) {
        spawnActorWithFlag(object, x_f, y_f, z_f, unk0, cutscene, flag, unk1);
    }
}

void spawnBossReward(int object, int x_f, int y_f, int z_f, int unk0, int cutscene, int flag, int unk1) {
    int new_obj = getKeyItem(flag);
    if (new_obj != 0) {
        object = new_obj;
    }
    if (object != 153) {
        // Protect against null objects
        if ((ActorMasterType[object] == ACTORMASTER_SPRITE) && ((CurrentMap == 0x53) || (CurrentMap == 0xC5))) {
            // Sprite & Dogadon Fight
            cutscene = 1;
            x_f = 0x43ED8000;
            y_f = 0x43570000;
            z_f = 0x443B8000;
        } else if ((object != 72) && (CurrentMap == 0x6F)) {
            // Pufftoss - Not a key
            cutscene = 100;
        }
        if ((CurrentMap == 0x9A) || (CurrentMap == 0xC4)) {
            // AD2/MJ
            cutscene = 1;
        }
        spawnActorWithFlag(object, x_f, y_f, z_f, unk0, cutscene, flag, unk1);
        // Fix items which have short spawn ranges
        ActorSpawnerPointer->spawn_range = 4000000.0f;
    }
}

int checkFlagDuplicate(short flag, int type) {
    // Duplicate of the check flag function, for the purpose of checking a flag without referencing the lookup table
    if (flag == -1) {
        return 0;
    }
    unsigned char* fba = 0;
    if ((type == 0) || (type == 2)) {
        fba = (unsigned char*)getFlagBlockAddress(type);
    } else {
        fba = (unsigned char*)&TempFlagBlock[0];
    }
    int offset = flag >> 3;
    int shift = flag & 7;
    return (fba[offset] >> shift) & 1;
}

void setFlagDuplicate(short flag, int set, int type) {
    if (flag != -1) {
        unsigned char* fba = 0;
        if ((type == 0) || (type == 2)) {
            fba = (unsigned char*)getFlagBlockAddress(type);
        } else {
            fba = (unsigned char*)&TempFlagBlock[0];
        }
        int offset = flag >> 3;
        int shift = flag & 7;
        if (!set) {
            fba[offset] &= ~(1 << shift);
        } else {
            fba[offset] |= (1 << shift);
        }
        checkVictory_flaghook(flag);
    }
}

int countFlagsForKongFLUT(int startFlag, int start, int cap, int kong) {
    int count = 0;
    if (kong < 5) {
        for (int i = start; i <= cap; i++) {
            int check = getFlagIndex(startFlag, i, kong);
            if (check > -1) {
                count += checkFlag(check, 0);
            }
        }
    }
    return count;
}

int countFlagsDuplicate(int start, int count, int type) {
    int end = start + count;
    int amt = 0;
    for (int i = start; i < end; i++) {
        amt += checkFlagDuplicate(i, type);
    }
    return amt;
}

static short flut_cache[40] = {};
static unsigned char cache_spot = 0;
static int flut_size = -1;

void cacheFlag(int input, int output) {
    int slot = cache_spot;
    flut_cache[(2 * slot)] = input;
    flut_cache[(2 * slot) + 1] = output;
    cache_spot = (cache_spot + 1) % 20;
}

int clampFlag(int flag) {
    /*
        Clamp flag for GBs, Medals, Crowns, BPs, Nin/RW Coin, Boss Key
    */
    if ((flag >= 0x1D5) && (flag <= 0x1FC)) {
        return 1; // Blueprints
    }
    if ((flag >= 0x225) && (flag <= 0x24C)) {
        return 1; // Medal
    }
    if ((flag >= 0x261) && (flag <= 0x26A)) {
        return 1; // Crown
    }
    if (flag == 0x17B) {
        return 1; // RW Coin
    }
    if ((flag >= 0x1) && (flag <= 0x1F)) {
        return 1; // Japes GBs + Key 1
    }
    if ((flag >= 0x31) && (flag <= 0x4D)) {
        return 1; // Aztec GBs + Key 2
    }
    if ((flag >= 0x70) && (flag <= 0x8B)) {
        return 1; // Factory GBs + Key 3 + Nintendo Coin
    }
    if ((flag >= 0x9A) && (flag <= 0xA8)) {
        return 1; // Galleon GBs (Group 1) + Key 4
    }
    if ((flag >= 0xB6) && (flag <= 0xEC)) {
        return 1; // Galleon GBs (Group 2) + Fungi GBs (Group 1) + Key 5 + Pearls
    }
    if ((flag >= 0xF7) && (flag <= 0x119)) {
        return 1; // Fungi GBs (Group 2) + Caves GBs (Group 1)
    }
    if ((flag >= 0x124) && (flag <= 0x146)) {
        return 1; // Caves GBs (Group 2) + Key 6 + Castle GBs (Group 1) + Key 7 + Rareware GB
    }
    if ((flag >= 0x15E) && (flag <= 0x161)) {
        return 1; // Castle GBs (Group 2)
    }
    if ((flag == 0x17C) || (flag == 0x17D)) {
        return 1; // Key 8 + First GB
    }
    if ((flag >= 0x18E) && (flag <= 0x1AF)) {
        return 1; // Isles GBs
    }
    if (flag == 0x300) {
        return 1; // Fungi Bean
    }
    return 0;
}

void* checkMove(short* flag, void* fba, int source) {
    if (*flag & 0x8000) {
        // Is Move
        int item_kong = (*flag >> 12) & 7;
        if (item_kong > 4) {
            item_kong = 0;
        }
        int item_type = (*flag >> 8) & 15;
        int item_index = *flag & 0xFF;
        if (item_type == 7) {
            *flag = 0;
            return fba;
        } else {
            char* temp_fba = (char*)&MovesBase[item_kong];
            if (item_index == 0) {
                *flag = 0;
            } else {
                *flag = item_index - 1;
            }
            int init_val = *(char*)(temp_fba + item_type);
            if (((init_val & (1 << *flag)) == 0) && (source == 1)) {
                // Move given
                spawnActor(324,0);
                TextOverlayData.type = item_type;
                TextOverlayData.flag = item_index;
                TextOverlayData.kong = item_kong;
                if (item_type == 4) {
                    if (CollectableBase.Melons < 2) {
                        CollectableBase.Melons = 2;
                        CollectableBase.Health = CollectableBase.Melons << 2;
                    }
                }
            }
            return temp_fba + item_type;
        }
    } else {
        int flag_index = *flag;
        int spawn_overlay = 0;
        int item_type = 0;
        int item_index = 0;
        int item_kong = 0;
        if ((source == 1) && (!checkFlagDuplicate(flag_index, 0)) && (Gamemode == 6)) {
            if ((flag_index == FLAG_ITEM_SLAM_0) || (flag_index == FLAG_ITEM_SLAM_1)) {
                // Slam
                MovesBase[0].simian_slam += 1;
                item_index = MovesBase[0].simian_slam;
                for (int i = 1; i < 5; i++) {
                    MovesBase[i].simian_slam = item_index;
                }
                spawn_overlay = 1;
                item_type = 1;
            } else if ((flag_index == FLAG_ITEM_BELT_0) || (flag_index == FLAG_ITEM_BELT_1)) {
                // Belt
                MovesBase[0].ammo_belt += 1;
                item_index = MovesBase[0].ammo_belt;
                for (int i = 1; i < 5; i++) {
                    MovesBase[i].ammo_belt = item_index;
                }
                spawn_overlay = 1;
                item_type = 3;
            } else if ((flag_index >= FLAG_ITEM_INS_0) && (flag_index <= FLAG_ITEM_INS_2)) {
                // Instrument Upgrade
                item_index = 0;
                for (int i = 1; i < 4; i++) {
                    if (MovesBase[0].instrument_bitfield & (1 << i)) {
                        item_index = i;
                    }
                }
                item_index += 1;
                for (int i = 0; i < 5; i++) {
                    MovesBase[i].instrument_bitfield |= (1 << item_index);
                }
                spawn_overlay = 1;
                item_type = 4;
                if (item_index >= 2) {
                    // 3rd Melon
                    if (CollectableBase.Melons < 3) {
                        CollectableBase.Melons = 3;
                        CollectableBase.Health = CollectableBase.Melons << 2;
                    }
                } else {
                    if (CollectableBase.Melons < 2) {
                        CollectableBase.Melons = 2;
                        CollectableBase.Health = CollectableBase.Melons << 2;
                    }
                }
                item_index += 1;
            } else if ((flag_index >= FLAG_TBARREL_DIVE) && (flag_index <= FLAG_TBARREL_BARREL)) {
                spawn_overlay = 1;
                item_type = 5;
                item_index = flag_index;
            } else if ((flag_index == FLAG_ABILITY_CAMERA) || (flag_index == FLAG_ABILITY_SHOCKWAVE)) {
                spawn_overlay = 1;
                item_type = 5;
                item_index = flag_index;
            } else {
                for (int i = 0; i < 5; i++) {
                    if (flag_index == kong_flags[i]) {
                        spawn_overlay = 1;
                        item_type = 5;
                        item_index = flag_index;
                    }
                }
            }
            if (spawn_overlay) {
                spawnActor(324, 0);
                TextOverlayData.type = item_type;
                TextOverlayData.flag = item_index;
                TextOverlayData.kong = item_kong;
            }
        }
    }
    return fba;
}

void getFLUTSize(void) {
    for (int i = 0; i < 400; i++) {
        if (ItemRando_FLUT[2 * i] == -1) {
            flut_size = i;
            return;
        }
    }
}

int binarySearch(int search_item, int low, int high) {
    int lim = high - low;
    int old_dist = (high - low) + 1;
    while (low != high) {
        int mid = (low + high) / 2;
        int loc = 2 * mid;
        if (search_item == ItemRando_FLUT[loc]) {
            return mid;
        } else if (search_item > ItemRando_FLUT[loc]) {
            low = mid + 1;
        } else {
            high = mid - 1;
        }
        lim -= 1;
        if (lim == 0) {
            return -1;
        }
        if ((high - low) > old_dist) {
            // diverging
            return -1;
        }
        old_dist = (high - low);
    }
    return -1;
}

void* searchFlag(int old_flag, short* flag_write, int source, void* fba) {
    if (flut_size < 10) {
        // Plain search
        for (int i = 0; i < (flut_size * 2); i++) {
            int lookup = ItemRando_FLUT[(2 * i)];
            if (old_flag == lookup) {
                *flag_write = ItemRando_FLUT[(2 * i) + 1];
                cacheFlag(old_flag, *flag_write);
                return checkMove(flag_write, fba, source);
            } else if (lookup == -1) {
                cacheFlag(old_flag, -1);
                return fba;
            }
        }
    } else {
        // Search by halves
        int index = binarySearch(old_flag, 0, flut_size - 1);
        if (index >= -1) {
            int lookup = ItemRando_FLUT[(2 * index)];
            if (old_flag == lookup) {
                *flag_write = ItemRando_FLUT[(2 * index) + 1];
                cacheFlag(old_flag, *flag_write);
                return checkMove(flag_write, fba, source);
            }
        }
    }
    cacheFlag(old_flag, -1);
    return fba;
}

void* updateFlag(int type, short* flag, void* fba, int source) {
    if ((Rando.item_rando) && (type == 0) && (*flag != 0)) {
        if (flut_size == -1) {
            getFLUTSize();
        }
        int vanilla_flag = *flag;
        if (flut_size > 0) {
            if (clampFlag(vanilla_flag)) {
                for (int i = 0; i < 20; i++) {
                    if (flut_cache[(2 * i)] == vanilla_flag) {
                        if (flut_cache[(2 * i) + 1] != -1) {
                            *flag = flut_cache[(2 * i) + 1];
                        }
                        return checkMove(flag, fba, source);
                    }
                }
                for (int i = 0; i < flut_size; i++) {
                    int lookup = ItemRando_FLUT[(2 * i)];
                    if (vanilla_flag == lookup) {
                        *flag = ItemRando_FLUT[(2 * i) + 1];
                        if (source == 1) {
                            int give_gb = 0;
                            if ((vanilla_flag == FLAG_COLLECTABLE_NINTENDOCOIN) && (Rando.arcade_reward == 5)) {
                                give_gb = 1;
                            } else if ((vanilla_flag == FLAG_COLLECTABLE_RAREWARECOIN) && (Rando.jetpac_reward == 5)) {
                                give_gb = 1;
                            }
                            if (give_gb) {
                                if (!checkFlag(vanilla_flag, 0)) {
                                    int world = getWorld(CurrentMap, 1);
                                    if (world < 8) {
                                        MovesBase[(int)Character].gb_count[world] += 1;
                                    }
                                }
                            }
                        }
                        cacheFlag(vanilla_flag, *flag);
                        return checkMove(flag, fba, source);
                    } else if (lookup == -1) {
                        cacheFlag(vanilla_flag, -1);
                        return fba;
                    }
                }
            }
        }
    }
    return fba;
}

int getKongFromBonusFlag(int flag) {
    if ((Rando.any_kong_items & 1) == 0) {
        for (int i = 0; i < 95; i++) {
            if (bonus_data[i].flag == flag) {
                return bonus_data[i].kong_actor;
            }
        }
    }
    return 0;
}

void banana_medal_acquisition(int flag) {
    /* 
        0 - GB,
        1 - BP,
        2 - Key,
        3 - Crown,
        4 - SpecialCoin,
        5 - Medal,
        6 - Cranky,
        7 - Funky,
        8 - Candy,
        9 - Training Barrel,
        10 - Shockwave,
        11 - Kong,
        12 - Bean,
        13 - Pearl,
        14 - Nothing,
    */
    int item_type = getMedalItem(flag - FLAG_MEDAL_JAPES_DK);
    if (!checkFlag(flag, 0)) {
        // Display and play effects if you don't have item
        if (item_type < 15) {
            int kong = -1;
            short flut_flag = flag;
            updateFlag(0, (short*)&flut_flag, (void*)0, -1);
            if (item_type == 11) {
                for (int i = 0; i < 5; i++) {
                    if (flut_flag == kong_flags[i]) {
                        kong = i;
                    }
                }
            }
            if (item_type == 2) {
                // Display key text
                int key_bitfield = 0;
                for (int i = 0; i < 8; i++) {
                    if (checkFlagDuplicate(getKeyFlag(i), 0)) {
                        key_bitfield |= (1 << i);
                    }
                }
                setFlag(flag, 1, 0);
                int spawned = 0;
                for (int i = 0; i < 8; i++) {
                    if ((checkFlagDuplicate(getKeyFlag(i), 0)) && ((key_bitfield & (1 << i)) == 0)) {
                        if (!spawned) {
                            spawnActor(324, 0);
                            TextOverlayData.type = 5;
                            TextOverlayData.flag = getKeyFlag(i);
                            TextOverlayData.kong = 0;
                            spawned = 1;
                        }
                    }
                }
            } else if (item_type < 14) {
                setFlag(flag, 1, 0);
            }
            if (item_type == 0) {
                MovesBase[getKong(0)].gb_count[getWorld(CurrentMap,1)] += 1;
            }
            if (item_type < 14) {
                playSFX(0xF2);
                int used_song = 0x97;
                int kong_songs[] = {11, 10, 12, 13, 9};
                int songs[] = {18,69,18,0x97,22,115,115,115,115,115,0x97, 0, 147, 128};
                if (item_type == 11) {
                    used_song = kong_songs[kong];
                } else if (item_type < 14) {
                    used_song = songs[item_type];
                }
                playSong(used_song, 0x3F800000);
            }
            unkSpriteRenderFunc(200);
            unkSpriteRenderFunc_0();
            loadSpriteFunction(0x8071EFDC);
            int bp_sprites[] = {0x5C,0x5A,0x4A,0x5D,0x5B};
            int sprite_indexes[] = {0x3B, 0, 0x8A, 0x8B, 0, 0x3C, 0x94, 0x96, 0x93, 0x94, 0x3A, 0x8E, 0, 0x92, 0x92};
            int used_sprite = 0x3B;
            if (item_type == 1) {
                int character_val = Character;
                if (character_val > 4) {
                    character_val = 0;
                }
                used_sprite = bp_sprites[character_val];
            } else if (item_type == 4) {
                if (flut_flag == 132) {
                    // Nintendo Coin
                    used_sprite = 0x8C;
                } else {
                    // Rareware Coin
                    used_sprite = 0x8D;
                }
            } else if (item_type == 11) {
                used_sprite = 0xA9 + kong;
            } else {
                used_sprite = sprite_indexes[item_type];
            }
            void* sprite_addr = sprite_table[used_sprite];
            if (item_type == 12) {
                sprite_addr = &bean_sprite;
            } else if (item_type == 13) {
                sprite_addr = &pearl_sprite;
            }
            displaySpriteAtXYZ(sprite_addr, 0x3F800000, 160.0f, 120.0f, -10.0f);
        }
    } else {
        // No item or pre-given item
        unkSpriteRenderFunc(200);
        unkSpriteRenderFunc_0();
        loadSpriteFunction(0x8071EFDC);
        displaySpriteAtXYZ(sprite_table[0x8E], 0x3F800000, 160.0f, 120.0f, -10.0f);
    }
}

static unsigned char key_timer = 0;
static unsigned char key_index = 0;
static char key_text[] = "KEY 0";
static unsigned char old_keys = 0;

void keyGrabHook(int song, int vol) {
    playSong(song, vol);
    int val = 0;
    for (int i = 0; i < 8; i++) {
        if (checkFlagDuplicate(getKeyFlag(i), 0)) {
            val |= (1 << i);
        }
    }
    old_keys = val;
}

int getFlagIndex_Corrected(int start, int level) {
    return start + (5 * level) + getKong(0);
}

static const short boss_maps[] = {0x8,0xC5,0x9A,0x6F,0x53,0xC4,0xC7};

int itemGrabHook(int collectable_type, int obj_type, int is_homing) {
    if (Rando.item_rando) {
        if (obj_type == 0x13C) {
            for (int i = 0; i < 8; i++) {
                if (checkFlagDuplicate(getKeyFlag(i), 0)) {
                    if ((old_keys & (1 << i)) == 0) {
                        spawnActor(324,0);
                        TextOverlayData.type = 5;
                        TextOverlayData.flag = getKeyFlag(i);
                        TextOverlayData.kong = 0;
                    }
                }
            }
            auto_turn_keys();
        } else {
            for (int i = 0; i < 7; i++) {
                if (CurrentMap == boss_maps[i]) {
                    for (int j = 0; j < (sizeof(acceptable_items) / 2); j++) {
                        if (obj_type == acceptable_items[j]) {
                            setAction(0x41, 0, 0);
                        }
                    }
                }
            }
        }
        if (obj_type != 0x18D) {
            if ((CurrentMap == 0x35) || (CurrentMap == 0x49) || ((CurrentMap >= 0x9B) && (CurrentMap <= 0xA2))) {
                for (int j = 0; j < (sizeof(acceptable_items) / 2); j++) {
                    if (obj_type == acceptable_items[j]) {
                        setAction(0x42, 0, 0);
                    }
                }
            }
        }
    }
    return getCollectableOffset(collectable_type, obj_type, is_homing);
}

int* controlKeyText(int* dl) {
    if (key_timer > 0) {
        int key_opacity = 255;
        if (key_timer < 10) {
            key_opacity = 25 * key_timer;
        } else if (key_timer > 90) {
            key_opacity = 25 * (100 - key_timer);
        }
        dl = initDisplayList(dl);
        *(unsigned int*)(dl++) = 0xFCFF97FF;
	    *(unsigned int*)(dl++) = 0xFF2CFE7F;
        *(unsigned int*)(dl++) = 0xFA000000;
        *(unsigned int*)(dl++) = 0xFFFFFF00 | key_opacity;
        dk_strFormat(key_text, "KEY %d", key_index + 1);
        dl = displayText(dl,1,640,750,key_text,0x80);
        key_timer -= 1;
    }
    return dl;
}

void initKeyText(int ki) {
    key_index = ki;
    key_timer = 100;
}

void spriteCode(int sprite_index, float scale) {
    void* paad = CurrentActorPointer_0->paad;
    spriteActorGenericCode(scale);
    if ((CurrentActorPointer_0->obj_props_bitfield & 0x10) == 0) {
        assignGIFToActor(paad, sprite_table[sprite_index], 0x3F800000);
        if (CurrentActorPointer_0->control_state == 99) {
            CurrentActorPointer_0->control_state = 1;
            CurrentActorPointer_0->sub_state = 2;
        }
    }
}

void ninCoinCode(void) {
    spriteCode(0x8D, 4.5f);
}

void rwCoinCode(void) {
    spriteCode(0x8C, 4.5f);
}

void medalCode(void) {
    spriteCode(0x3C, 12.0f);
}

void beanCode(void) {
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
    deleteActorContainer(CurrentActorPointer_0);
}

void scaleBounceDrop(float scale) {
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
    GoldenBananaCode();
    scaleBounceDrop(0.15f);
    if (CurrentActorPointer_0->yVelocity > 500.0f) {
        CurrentActorPointer_0->yVelocity = 500.0f;
    }
}

void PotionCode(void) {
    GoldenBananaCode();
    if ((CurrentActorPointer_0->obj_props_bitfield & 0x10) == 0) {
        CurrentActorPointer_0->obj_props_bitfield &= 0xFFFFEFFF; // Make color blends work
    }
}

void KLumsyText(void) {
    /*
        NOTE: Re-add this once we get some text for this
        float dist_to_klumsy = *(float*)(0x807FC8D4);
        if (dist_to_klumsy < 160000.0f) {
            if ((checkFlag(FLAG_KEYIN_JAPES, 0)) && (checkFlag(FLAG_KEYHAVE_KEY8, 0)) && (Rando.item_rando)) {
                if ((!checkFlagDuplicate(FLAG_KEYHAVE_KEY8, 0)) || (1 == 1)) {
                    if (!checkFlag(0x78, 2)) {
                        getTextPointer_0(CurrentActorPointer_0, 41, 0);
                        setFlag(0x78, 1, 2);
                    }
                }
            }
        }
    */
    renderActor(CurrentActorPointer_0, 0);
}

static const unsigned char dance_skip_ban_maps[] = {
    0x0E, // Aztec Beetle
    0x1B, // Factory Car Race
    0x27, // Galleon Seal Race
    0x52, // Caves Beetle
    0xB9, // Castle Car Race
    0x08, // AD1
    0xC5, // Dog1
    0x9A, // MJ
    0x6F, // Pufftoss
    0x53, // Dog2
    0xC4, // AD2
    0xC7, // KKO
    0x35, // Japes: Crown
    0x49, // Aztec: Crown
    0x9B, // Factory: Crown
    0x9C, // Galleon: Crown
    0x9F, // Fungi: Crown
    0xA0, // Caves: Crown
    0xA1, // Castle: Crown
    0xA2, // Helm: Crown
    0x9D, // Isles: Lobby Crown
    0x9E, // Isles: Snide Crown
};

int canDanceSkip(void) {
    if (CurrentMap == 0x6F) {
        return 0;
    }
    if ((Player->yPos - Player->floor) >= 100.0f) {
        return 1;
    }
    if (Player->control_state == 99) {
        return 1;
    }
    if ((Player->grounded_bitfield & 4) && ((Player->water_floor - Player->floor) > 20.0f)) {
        return 1;
    }
    if (Rando.quality_of_life.dance_skip) {
        int is_banned_map = 0;
        for (int i = 0; i < sizeof(dance_skip_ban_maps); i++) {
            if (dance_skip_ban_maps[i] == CurrentMap) {
                is_banned_map = 1;
            }
        }
        if (!is_banned_map) {
            return 1;
        }
    }
    return 0;
}

void getItem(int object_type) {
    float pickup_volume = 1-(0.3f * *(char*)(0x80745838));
    int song = -1;
    switch(object_type) {
        case 0x0A:
        case 0x0D:
        case 0x16:
        case 0x1E:
        case 0x1F:
        case 0x1CF:
        case 0x1D0:
            // CB Single
            playSound(0x2A0, 0x7FFF, 0x427C0000, 0x3F800000, 5, 0);
            break;
        case 0x11:
        case 0x8F:
            // Homing Ammo Crate
            playSound(0x157, 0x7FFF, 0x427C0000, 0x3F800000, 5, 0);
            break;
        case 0x1C:
        case 0x1D:
        case 0x23:
        case 0x24:
        case 0x27:
            // Banana Coin
            playSong(23, *(int*)(&pickup_volume));
            break;
        case 0x48:
        case 0x28F:
            // Company Coin
            if (Rando.item_rando) {
                playSong(22, *(int*)(&pickup_volume));
            }
            break;
        case 0x56:
            // Orange
            playSound(0x147, 0x7FFF, 0x427C0000, 0x3F800000, 5, 0);
            break;
        case 0x57:
            // Melon Slice
            playSong(0x2F, *(int*)(&pickup_volume));
            break;
        case 0x59:
        case 0x5B:
        case 0x1F2:
        case 0x1F3:
        case 0x1F5:
        case 0x1F6:
            // Potion
            playSong(115, 0x3F800000);
            if (!canDanceSkip()) {
                setAction(0x29, 0, 0);
            }
            break;
        case 0x74:
        case 0x288:
            // GB
            playSong(0x12, 0x3F800000);
            if (!canDanceSkip()) {
                setAction(0x29, 0, 0);
            }
            break;
        case 0x8E:
            // Crystal
            playSong(35, *(int*)(&pickup_volume));
            break;
        case 0x90:
            // Medal
            playSong(0x12, 0x3F800000);
            BananaMedalGet();
            if (!canDanceSkip()) {
                setAction(0x29, 0, 0);
            }
            break;
        case 0x98:
            // Film
            playSound(0x263, 0x7FFF, 0x427C0000, 0x3F800000, 5, 0);
            break;
        case 0xB7:
            // Rainbow Coin
            playSong(0x91, *(int*)(&pickup_volume));
            break;
        case 0xDD:
        case 0xDE:
        case 0xDF:
        case 0xE0:
        case 0xE1:
            // Blueprint
            playSong(69, *(int*)(&pickup_volume));
            break;
        case 0xEC:
        case 0x1D2:
            // Race Coin
            playSong(32, *(int*)(&pickup_volume));
            break;
        case 0x13C:
            // Key
            keyGrabHook(0x12, 0x3F800000);
            if (!canDanceSkip()) {
                unsigned char boss_list[] = {0x08, 0xC5, 0x9A, 0x6F, 0x53, 0xC4, 0xC7};
                int action = 0;
                for (int i = 0; i < sizeof(boss_list); i++) {
                    if (CurrentMap == boss_list[i]) {
                        action = 0x41; // Key Get
                    }
                }
                if (action == 0) {
                    action = 0x29; // GB Get
                }
                setAction(action, 0, 0);
            }
            auto_turn_keys();
            break;
        case 0x18D:
            // Crown
            playSong(0x12, 0x3F800000);
            if (!canDanceSkip()) {
                setAction(0x42, 0, 0);
            }
            CrownGet();
            break;
        case 0x198:
            // Bean
            playSong(147, 0x3F800000);
            break;
        case 0x1B4:
            // Pearl
            {
                playSong(128, 0x3F800000);
                if (CurrentMap == 0x2C) { // Treasure Chest
                    int requirement = 5;
                    if (Rando.fast_gbs) {
                        requirement = 1;
                    }
                    int count = 0;
                    for (int i = 0; i < 5; i++) {
                        count += checkFlagDuplicate(FLAG_PEARL_0_COLLECTED + i, 0);
                    }
                    if (count == (requirement - 1)) {
                        playCutscene((void*)0, 1, 0);
                    }
                }
            }
            break;
        case 0x1D1:
            // Coin Powerup
            playSound(0xAE, 0x7FFF, 0x427C0000, 0x3F800000, 5, 0);
            break;
        case 0x257:
            song = 11;
        case 0x258:
            if (song == -1) {
                song = 10;
            }
        case 0x259:
            if (song == -1) {
                song = 12;
            }
        case 0x25A:
            if (song == -1) {
                song = 13;
            }
        case 0x25B:
            if (song == -1) {
                song = 9;
            }
            if (song >= 0) {
                playSong(song, 0x3F800000);
            }
            if (!canDanceSkip()) {
                setAction(0x42, 0, 0);
            }
            refreshItemVisibility();
            break;
    }
}

#define STORED_COUNT 18
static int stored_maps[STORED_COUNT] = {};
static unsigned char stored_kasplat[STORED_COUNT] = {};

int setupHook(int map) {
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
    if (ActorSpawnerPointer) {
        actorSpawnerData* referenced_spawner = ActorSpawnerPointer;
        while (1 == 1) {
            if (referenced_spawner) {
                int actor_type = referenced_spawner->actor_type + 0x10;
                int is_drop = 0;
                int i = 0;
                while (i < sizeof(actor_drops)) {
                    if (actor_type == actor_drops[i]) {
                        is_drop = 1;
                        break;
                    }
                    i++;
                }
                if (is_drop) {
                    int flag = referenced_spawner->flag;
                    if ((flag >= FLAG_BP_JAPES_DK_HAS) && (flag < (FLAG_BP_JAPES_DK_HAS + 40))) {
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

static char* text_rewards[] = {
    "GOLDEN BANANA",
    "BLUEPRINT",
    "BOSS KEY",
    "BATTLE CROWN",
    "BANANA FAIRY",
    "RAREWARE COIN",
    "NINTENDO COIN",
    "BANANA MEDAL",
    "POTION",
    "KONG",
    "BEAN",
    "PEARL",
    "RAINBOW COIN",
    "NOTHING",
};

void handleDynamicItemText(char* location, char* format, int character) {
    if (character == 0x7C) {
        // Dynamic Text
        if (TextItemName >= 14) {
            TextItemName = 0;
        }
        dk_strFormat(location, "%s", text_rewards[(int)TextItemName]);
    } else {
        dk_strFormat(location, format, character);
    }
}

void mermaidCheck(void) {
    int requirement = 5;
    if (Rando.fast_gbs) {
        requirement = 1;
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

#define GB_DICTIONARY_COUNT 119
static GBDictItem NewGBDictionary[GB_DICTIONARY_COUNT] = {};

int addDictionaryItem(int index, int map, int id, int flag, int kong) {
    NewGBDictionary[index].map = map;
    NewGBDictionary[index].model2_id = id;
    NewGBDictionary[index].flag_index = flag;
    NewGBDictionary[index].intended_kong_actor = kong + 2;
    return index + 1;
}

void initItemDictionary(void) {
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
    }
    // Add new entries
    int size = addDictionaryItem(113, 0x2C, 0, FLAG_PEARL_0_COLLECTED, -2);
    for (int i = 1; i < 5; i++) {
        size = addDictionaryItem(size, 0x2C, i, FLAG_PEARL_0_COLLECTED + i, -2);
    }
    size = addDictionaryItem(size, 0x34, 5, FLAG_COLLECTABLE_BEAN, -2);
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