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

void spawnBonusReward(int object, float x, float y, float z, int unk0, int cutscene, int flag, int unk1) {
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
    if ((index > 0) && (index < BONUS_DATA_COUNT)) {
        object = bonus_data[index].spawn_actor;
    }
    if (object != (CUSTOM_ACTORS_START + NEWACTOR_NULL)) {
        spawnActorWithFlag(object, x, y, z, unk0, cutscene, flag, unk1);
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
    if ((index > 0) && (index < BONUS_DATA_COUNT)) {
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
    for (int i = 0; i < BONUS_DATA_COUNT; i++) {
        if (bonus_data[i].flag == flag) {
            if (bonus_data[i].spawn_actor != (CUSTOM_ACTORS_START + NEWACTOR_NULL)) {
                spawnActorWithFlag(bonus_data[i].spawn_actor, Player->xPos, Player->yPos, Player->zPos, 0, 0, flag, 0);
                // spawnObjectAtActor(bonus_data[i].spawn_actor, flag); // Causes some interesting side-effects with collision
            }
            return;
        }
    }
}

void spawnCrownReward(int object, float x, float y, float z, int unk0, int cutscene, int flag, int unk1) {
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
        spawnActorWithFlag(object, x, y, z, unk0, cutscene, flag, unk1);
    }
}

void spawnBossReward(int object, float x, float y, float z, int unk0, int cutscene, int flag, int unk1) {
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
            x = 475.0f;
            y = 215.0f;
            z = 750.0f;
        } else if ((object != 72) && (CurrentMap == MAP_GALLEONPUFFTOSS)) {
            // Pufftoss - Not a key
            cutscene = 100;
        }
        if ((CurrentMap == MAP_FACTORYJACK) || (CurrentMap == MAP_CAVESDILLO)) {
            // AD2/MJ
            cutscene = 1;
        }
        spawnActorWithFlag(object, x, y, z, unk0, cutscene, flag, unk1);
        // Fix items which have short spawn ranges
        ActorSpawnerPointer->spawn_range = 4000000.0f;
    }
}

void spawnDirtPatchReward(int object, float x, float y, float z, int unk0, int cutscene, int flag, int unk1) {
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
        if (isBounceObject(object)) {
            cutscene = 2;
        }
        spawnActorWithFlag(object, x, y, z, unk0, cutscene, flag, unk1);
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
            | Fake Item      | ----                       | True   | 0x103         |
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
                if ((model >= -4) && (model <= -2)) {
                    model = 0x103;
                }
            }
        }
        spawnActor(actor, model);
    } else {
        spawnActor(actor, CharSpawnerActorData[spawner->alt_enemy_value].model);
    }
}

void melonCrateItemHandler(behaviour_data* behaviour_pointer, int index, int p1, int p2) {
    int id = ObjectModel2Pointer[convertSubIDToIndex(index)].object_id;
    int flag = getCrateFlag(id);
    int spawn_count = 1;
    int object = getCrateItem(flag);
    int cutscene = 1;
    if (object == 0x2F) {
        // Junk Item. Set flag as we're spawning 4 unflagged melons and we want it to update check screen
        setFlag(flag, 1, FLAGTYPE_PERMANENT);
    }
    if (checkFlag(flag, FLAGTYPE_PERMANENT) || (object == (CUSTOM_ACTORS_START + NEWACTOR_NULL))) {
        spawn_count = 4;
        flag = -1;
        object = 0x2F;
        cutscene = 1;
    } else if (isBounceObject(object)) {
        cutscene = 2;
    }
    float x = collisionPos[0];
    float y = collisionPos[1] + 15.0f;
    float z = collisionPos[2];
    for (int i = 0; i < spawn_count; i++) {
        spawnActorWithFlag(object, x, y, z, 0x400 * i, cutscene, flag, 0);
    }
    unkSpriteRenderFunc_1(1);
    displaySpriteAtXYZ(sprite_table[31], 2.5f, x, y + 15.0f, z);
}