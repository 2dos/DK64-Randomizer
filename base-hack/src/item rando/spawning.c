/**
 * @file spawning.c
 * @author Ballaam
 * @brief Item Rando elements pertaining to the spawning process of items
 * @version 0.1
 * @date 2023-01-17
 * 
 * @copyright Copyright (c) 2023
 * 
 */
#include "../../include/common.h"

void spawnBonusReward(int object, int x_f, int y_f, int z_f, int unk0, int cutscene, int flag, int unk1) {
    /**
     * @brief Spawn bonus reward
     * 
     * @param object Actor Index
     * @param x_f X Position (Float in int form)
     * @param y_f Y Position (Float in int form)
     * @param z_f Z Position (Float in int form)
     * @param unk0 Unknown
     * @param cutscene Spawning Condition
     * @param flag Tied flag
     * @param unk1 Unknown
     */
    bonus_paad* paad = CurrentActorPointer_0->paad;
    int index = paad->barrel_index;
    if ((index > 0) && (index < 95)) {
        object = bonus_data[index].spawn_actor;
    }
    if (object != (CUSTOM_ACTORS_START + NEWACTOR_NULL)) {
        spawnActorWithFlag(object, x_f, y_f, z_f, unk0, cutscene, flag, unk1);
    }
}

void spawnRewardAtActor(int object, int flag) {
    /**
     * @brief Spawns a reward at the position as an actor, based on the bonus reward table
     * 
     * @param object Actor Index
     * @param flag Flag Index
     */
    int index = CurrentActorPointer_0->reward_index;
    if ((index > 0) && (index < 95)) {
        object = bonus_data[index].spawn_actor;
    }
    if (object != (CUSTOM_ACTORS_START + NEWACTOR_NULL)) {
        if (!checkFlag(flag, FLAGTYPE_PERMANENT)) {
            spawnObjectAtActor(object, flag);
        }
    }
}

void spawnMinecartReward(int object, int flag) {
    /**
     * @brief Spawns a minecart reward at an actor
     * 
     * @param object Actor Index
     * @param flag Flag Index
     */
    for (int i = 0; i < 95; i++) {
        if (bonus_data[i].flag == flag) {
            if (bonus_data[i].spawn_actor != (CUSTOM_ACTORS_START + NEWACTOR_NULL)) {
                int x_f = *(int*)(&Player->xPos);
                int y_f = *(int*)(&Player->yPos);
                int z_f = *(int*)(&Player->zPos);
                spawnActorWithFlag(bonus_data[i].spawn_actor, x_f, y_f, z_f, 0, 0, flag, 0);
                // spawnObjectAtActor(bonus_data[i].spawn_actor, flag); // Causes some interesting side-effects with collision
            }
            return;
        }
    }
}

void spawnCrownReward(int object, int x_f, int y_f, int z_f, int unk0, int cutscene, int flag, int unk1) {
    /**
     * @brief Spawn Crown Reward
     * 
     * @param object Actor Index
     * @param x_f X Position (Float in int form)
     * @param y_f Y Position (Float in int form)
     * @param z_f Z Position (Float in int form)
     * @param unk0 Unknown
     * @param cutscene Spawning Condition
     * @param flag Tied flag
     * @param unk1 Unknown
     */
    int new_obj = getCrownItem(CurrentMap);
    if (new_obj != 0) {
        object = new_obj;
    }
    if (object != (CUSTOM_ACTORS_START + NEWACTOR_NULL)) {
        spawnActorWithFlag(object, x_f, y_f, z_f, unk0, cutscene, flag, unk1);
    }
}

void spawnBossReward(int object, int x_f, int y_f, int z_f, int unk0, int cutscene, int flag, int unk1) {
    /**
     * @brief Spawn boss reward
     * 
     * @param object Actor Index
     * @param x_f X Position (Float in int form)
     * @param y_f Y Position (Float in int form)
     * @param z_f Z Position (Float in int form)
     * @param unk0 Unknown
     * @param cutscene Spawning Condition
     * @param flag Tied flag
     * @param unk1 Unknown
     */
    int new_obj = getKeyItem(flag);
    if (new_obj != 0) {
        object = new_obj;
    }
    if (object != (CUSTOM_ACTORS_START + NEWACTOR_NULL)) {
        // Protect against null objects
        if ((actor_master_types[object] == ACTORMASTER_SPRITE) && ((CurrentMap == MAP_FUNGIDOGADON) || (CurrentMap == MAP_AZTECDOGADON))) {
            // Sprite & Dogadon Fight
            cutscene = 1;
            x_f = 0x43ED8000;
            y_f = 0x43570000;
            z_f = 0x443B8000;
        } else if ((object != 72) && (CurrentMap == MAP_GALLEONPUFFTOSS)) {
            // Pufftoss - Not a key
            cutscene = 100;
        }
        if ((CurrentMap == MAP_FACTORYJACK) || (CurrentMap == MAP_CAVESDILLO)) {
            // AD2/MJ
            cutscene = 1;
        }
        spawnActorWithFlag(object, x_f, y_f, z_f, unk0, cutscene, flag, unk1);
        // Fix items which have short spawn ranges
        ActorSpawnerPointer->spawn_range = 4000000.0f;
    }
}

void spawnDirtPatchReward(int object, int x_f, int y_f, int z_f, int unk0, int cutscene, int flag, int unk1) {
    /**
     * @brief Spawn dirt patch reward
     * 
     * @param object Actor Index
     * @param x_f X Position (Float in int form)
     * @param y_f Y Position (Float in int form)
     * @param z_f Z Position (Float in int form)
     * @param unk0 Unknown
     * @param cutscene Spawning Condition
     * @param flag Tied flag
     * @param unk1 Unknown
     */
    int new_obj = getRainbowCoinItem(flag);
    if (new_obj != 0) {
        object = new_obj;
    }
    if (object != (CUSTOM_ACTORS_START + NEWACTOR_NULL)) {
        for (int i = 0; i < (int)(sizeof(bounce_objects)/2); i++) {
            if (object == bounce_objects[i]) {
                cutscene = 2;
            }
        }
        spawnActorWithFlag(object, x_f, y_f, z_f, unk0, cutscene, flag, unk1);
    }
}

void spawnCharSpawnerActor(int actor, SpawnerInfo* spawner) {
    /**
     * @brief Change Character Spawner Information to account for Fairy Rando
     * 
     * @param actor Actor index of the spawned item
     * @param spawner Spawner Object for the spawned item
     */
    /*
        INFORMATION:
            +----------------+----------------------------+--------+---------------+
            |   Model Name   |         Base Model         | Tested |   New Model   |
            +----------------+----------------------------+--------+---------------+
            | Golden Banana  | 0x69                       | True   | See Left      |
            | Boss Key       | 0xA5                       | True   | 0xF5          |
            | Crown          | 0xAF                       | True   | 0xF4          |
            | Fake Item      | ----                       | ----   | 0x10F         |
            | Potions        | 0xEE-0xF3                  | True   | 0xF6-0xFB     |
            | Kong Items     | 4, 1, 6, 9, 0xC, 0xE, 0xDB | True   | See Left      |
            +----------------+----------------------------+--------+---------------+
            Some items are excluded because when they're actors, they are sprites which can't easily be rendered with the fairy stuff. I might have a way around this,
            but we'll have to wait and see for probably a secondary update after the first push.
    */
    if (actor == 248) {
        // Fairy
        int model = 0x3D;
        for (int i = 0; i < 31; i++) {
            if ((charspawnerflags[i].map == CurrentMap) && (charspawnerflags[i].spawner_id == spawner->spawn_trigger)) {
                model = getFairyModel(charspawnerflags[i].tied_flag);
            }
        }
        spawnActor(actor, model);
    } else {
        spawnActor(actor, CharSpawnerActorData[spawner->alt_enemy_value].model);
    }
}

typedef struct packet_extra_data {
    /* 0x000 */ char unk_00[0xA];
    /* 0x00A */ short index;
} packet_extra_data;

int getBarrelModel(int index) {
    /**
     * @brief Get barrel model based on the contents inside the bonus barrel
     * 
     * @param index Bonus Barrel's tied reward index
     * 
     * @return Model Index
     */
    if (index < 95) {
        int actor = bonus_data[index].spawn_actor;
        switch (actor) {
            case 78:
            case 75:
            case 77:
            case 79:
            case 76:
                return 0x102; // Blueprint
            case CUSTOM_ACTORS_START + NEWACTOR_NINTENDOCOIN:
                return 0x103; // Nintendo Coin
            case CUSTOM_ACTORS_START + NEWACTOR_RAREWARECOIN:
                return 0x104; // Rareware Coin
            case 72:
                return 0x105; // Key
            case 86:
                return 0x106; // Crown
            case CUSTOM_ACTORS_START + NEWACTOR_MEDAL:
                return 0x107; // Medal
            case CUSTOM_ACTORS_START + NEWACTOR_POTIONDK:
            case CUSTOM_ACTORS_START + NEWACTOR_POTIONDIDDY:
            case CUSTOM_ACTORS_START + NEWACTOR_POTIONLANKY:
            case CUSTOM_ACTORS_START + NEWACTOR_POTIONTINY:
            case CUSTOM_ACTORS_START + NEWACTOR_POTIONCHUNKY:
            case CUSTOM_ACTORS_START + NEWACTOR_POTIONANY:
                return 0x108; // Potion
            case CUSTOM_ACTORS_START + NEWACTOR_KONGDK:
            case CUSTOM_ACTORS_START + NEWACTOR_KONGDIDDY:
            case CUSTOM_ACTORS_START + NEWACTOR_KONGLANKY:
            case CUSTOM_ACTORS_START + NEWACTOR_KONGTINY:
            case CUSTOM_ACTORS_START + NEWACTOR_KONGCHUNKY:
                return 0xFD + (actor - (CUSTOM_ACTORS_START + NEWACTOR_KONGDK)); // Kong Pickup Actors
            case CUSTOM_ACTORS_START + NEWACTOR_BEAN:
                return 0x109; // Bean
            case CUSTOM_ACTORS_START + NEWACTOR_PEARL:
                return 0x10A; // Pearl
            case CUSTOM_ACTORS_START + NEWACTOR_FAIRY:
                return 0x10B; // Fairy
            case 140:
                return 0x10C; // Rainbow Coin
            case CUSTOM_ACTORS_START + NEWACTOR_FAKEITEM:
                return 0x10D; // Fake Item
            case 0x2F:
                return 0x10E; // Junk Item
        }
    }
    return 0x76;
}

typedef struct spawnerExtraInfo {
    /* 0x000 */ char unk_0[8];
    /* 0x008 */ int index;
} spawnerExtraInfo;

int SpawnPreSpawnedBarrel(
        float x, float y, int z, int unk0,
        int sp10, int sp14, int sp18, int sp1c,
        int sp20, int sp24, int sp28, actorSpawnerData* spawner,
        int sp30, int sp34, int sp38, int sp3c,
        int sp40, int sp44, spawnerExtraInfo* extra_data
    ) {
        /**
         * @brief Spawn a barrel and alter the referenced model.
         * Only for barrels that have been spawned before and need it's model reassigning correctly.
         */
    if (Rando.item_rando) {
        if (spawner) {
            if ((spawner->actor_type + 0x10) == 0x1C) {
                int index = extra_data->index;
                if (index < 95) {
                    int model = getBarrelModel(index);
                    if (model != 0) {
                        spawner->model = model;
                    }
                }
            }
        }
    }
    return getChunk(x, y, z, unk0);
}

void SpawnBarrel(spawnerPacket* packet) {
    /**
     * @brief Spawn a barrel and alter the referenced model.
     * Only for barrels that have NOT been spawned before.
     */
    if ((Rando.item_rando)) {
        packet_extra_data* data = (packet_extra_data*)packet->extra_data;
        if (data) {
            int index = data->index;
            if (index < 95) {
                int model = getBarrelModel(index);
                if (model != 0) {
                    packet->model = model;
                }
            }
        }
    }
    spawn3DActor(packet);
}

void initBarrelChange(void) {
    /**
     * @brief Initialize the changes necessary for bonus barrels to match contents
     */
    actor_master_types[0x1C] = 5;
    *(int*)(0x8074DA44) = (int)&SpawnBarrel;
    writeFunction(0x80689368, &SpawnPreSpawnedBarrel); // Change model if barrel is being reloaded
}