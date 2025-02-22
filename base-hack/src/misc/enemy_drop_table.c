/**
 * @file enemy_drop_table.c
 * @author Ballaam
 * @brief Handles the enemy drop tables and what enemies spawn what items
 * @version 0.1
 * @date 2022-07-24
 * 
 * @copyright Copyright (c) 2022
 * 
 */
#include "../../include/common.h"

static unsigned char replenlishable_drops[] = {
    0x2F, // Watermelon
    0x34, // Orange
    0x33, // Ammo Crate
    0x79, // Crystal
};

int isReplenishableDrop(int drop_object) {
    /**
     * @brief Is item that is dropped a replenishable item.
     * In other words, once a player has picked up the item, will it cause problems
     * if they pick it up again from the same instance of an enemy?
     * 
     * @param drop_object Actor index of dropped item
     * 
     * @return Is replenishable
     */
    for (int i = 0; i < sizeof(replenlishable_drops); i++) {
        if (drop_object == replenlishable_drops[i]) {
            return 1;
        }   
    }
    return 0;
}

void buildItemDrops(void) {
    /**
     * @brief Build the item drops table to handle randomizer information
     */
    if ((Rando.disable_drops) && (!Rando.enemy_item_rando)) {
        for (int i = 0; i < DROP_COUNT; i++) {
            if (drops[i].source_object != 0) {
                if (isReplenishableDrop(drops[i].dropped_object)) {
                    drops[i].source_object = 3;
                }
            }
        }
    }
}

static drop_item default_drop = {
    .dropped_object = 0x2F,
    .drop_count = 1,
    .drop_music = SONG_MELONSLICEDROP,
};

void spawnEnemyDrops(actorData* actor) {
    /**
     * @brief Handle the spawning of enemy drops. Based on a vanilla function with the same name.
     * There's a few minor modifications to handle kasplat item duplication prevention amongst a couple other things.
     */
    if (player_count > 1) {
        return;
    }
    if (MapProperties.is_bonus) {
        return;
    }
    if ((CurrentMap == MAP_CASTLEKUTOUT) && (Rando.hard_mode.lava_water)) {
        // Make sure KKO enemy always drops a melon slice
        playSong(SONG_MELONSLICEDROP, 1.0f);
        spawnActorWithFlag(0x2F, actor->xPos, actor->yPos, actor->zPos, 0xFFF, 1, -1, 0);
        return;
    }
    drop_item *item_data = 0;
    int actor_index = actor->actorType;
    for (int i = 0; i < DROP_COUNT; i++) {
        if (actor_index == drops[i].source_object) {
            item_data = &drops[i];
        }
    }
    if (!item_data) {
        return;
    }
    int song = item_data->drop_music;
    if (song > 0) {
        if (!Rando.enemy_item_rando) {
            playSong(song, 1.0f);
        }
    }
    int drop_count = item_data->drop_count;
    int drop_type = item_data->dropped_object;
    if (drop_count <= 0) {
        return;
    }
    int flag = -1;
    int drop_arg = 1;
    if ((actor_index >= 241) && (actor_index <= 245)) {
        // Is Kasplat
        int world = getWorld(CurrentMap, 1);
        flag = 469 + (5 * world) + (actor_index - 241);
        if (checkFlag(flag, FLAGTYPE_PERMANENT)) {
            return;
        } else if (Rando.item_rando) {
            drop_type = getBPItem(flag - 469);
            drop_count = 1;
            if (isBounceObject(drop_type)) {
                drop_arg = 2;
            }
            if (KasplatSpawnBitfield & (1 << (actor_index - 241))) {
                drop_count = 0;
            }
            // Not drop that despawns
            KasplatSpawnBitfield |= (1 << (actor_index - 241));
        }
    } else if (Rando.enemy_item_rando) {
        if (TiedCharacterSpawner) {
            int spawner_id = TiedCharacterSpawner->spawn_trigger;
            flag = getEnemyFlag(spawner_id);
            if ((canSpawnEnemyReward()) && (Rando.item_rando)) {
                int proposition = getEnemyItem(spawner_id);
                if ((proposition != -1) && (proposition != (CUSTOM_ACTORS_START + NEWACTOR_NULL))) {
                    drop_type = proposition;
                    drop_count = 1;
                }
                if (isBounceObject(drop_type)) {
                    drop_arg = 2;
                }
                setSpawnBitfield(spawner_id, 1);
            }
            if (!canSpawnEnemyReward()) {
                if ((drop_type == 0x2F) && (Rando.disable_drops)) {
                    return;
                }
            }
        }
    }
    float drop_rotation_divisor = 0xFFF;
    drop_rotation_divisor /= drop_count;
    for (int i = 0; i < drop_count; i++) {
        int drop_rotation = i * drop_rotation_divisor;
        spawnActorWithFlag(drop_type, actor->xPos, actor->yPos, actor->zPos, drop_rotation, drop_arg, flag, 0);
    }
}

void initItemDropTable(void) {
    /**
     * @brief Initialize the item drop data at ROM Boot
     */
    buildItemDrops();
}