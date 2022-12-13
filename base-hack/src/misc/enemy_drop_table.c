#include "../../include/common.h"

typedef struct drop_item {
    /* 0x000 */ short source_object;
    /* 0x002 */ short dropped_object;
    /* 0x004 */ unsigned char drop_music;
    /* 0x005 */ unsigned char drop_count;
} drop_item;

#define DROP_COUNT 29
static drop_item drops[DROP_COUNT] = {};

int addItemDrop(int source_object, int drop_object, int drop_music, int drop_count, int drop_total) {
    if (Rando.disable_drops) {
        if (source_object != 0) {
            if ((drop_object == 0x2F) || (drop_object == 0x34) || (drop_object == 0x33)) {
                source_object = 3;
            }
        }
    }
    drops[drop_total].source_object = source_object;
    drops[drop_total].dropped_object = drop_object;
    drops[drop_total].drop_music = drop_music;
    drops[drop_total].drop_count = drop_count;
    return drop_total + 1;
}

void buildItemDrops(void) {
    int drop_total = 0;
    drop_total = addItemDrop(0xB2,0x2F,0x2F,1,drop_total); // Beaver (Blue)
    drop_total = addItemDrop(0xD4,0x2F,0x2F,2,drop_total); // Beaver (Gold)
    drop_total = addItemDrop(0xCD,0x2F,0x2F,1,drop_total); // Green Klaptrap
    drop_total = addItemDrop(0xD0,0x34,0x00,3,drop_total); // Purple Klaptrap
    drop_total = addItemDrop(0xD1,0x33,0x00,1,drop_total); // Red Klaptrap
    drop_total = addItemDrop(0x03,0x35,0x00,3,drop_total); // Diddy
    drop_total = addItemDrop(0xF1,0x4E,0x4C,1,drop_total); // Kasplat (DK)
    drop_total = addItemDrop(0xF2,0x4B,0x4C,1,drop_total); // Kasplat (Diddy)
    drop_total = addItemDrop(0xF3,0x4D,0x4C,1,drop_total); // Kasplat (Lanky)
    drop_total = addItemDrop(0xF4,0x4F,0x4C,1,drop_total); // Kasplat (Tiny)
    drop_total = addItemDrop(0xF5,0x4C,0x4C,1,drop_total); // Kasplat (Chunky)
    drop_total = addItemDrop(0xBB,0x34,0x00,3,drop_total); // Klump
    drop_total = addItemDrop(0xEE,0x2F,0x2F,1,drop_total); // Kremling
    drop_total = addItemDrop(0xEB,0x2F,0x2F,2,drop_total); // Robo Kremling
    drop_total = addItemDrop(0x123,0x2F,0x2F,2,drop_total); // Kosha
    drop_total = addItemDrop(0xB7,0x2F,0x2F,1,drop_total); // Zinger
    drop_total = addItemDrop(0xCE,0x2F,0x2F,1,drop_total); // Zinger
    drop_total = addItemDrop(0x105,0x2F,0x2F,1,drop_total); // Robo-Zinger
    drop_total = addItemDrop(0x11D,0x2F,0x2F,1,drop_total); // Bat
    drop_total = addItemDrop(0x10F,0x2F,0x2F,1,drop_total); // Mr. Dice
    drop_total = addItemDrop(0x10E,0x2F,0x2F,1,drop_total); // Sir Domino
    drop_total = addItemDrop(0x10D,0x2F,0x2F,1,drop_total); // Mr. Dice
    drop_total = addItemDrop(0xE0,0x2F,0x2F,1,drop_total); // Mushroom Man
    drop_total = addItemDrop(0x106,0x2F,0x2F,1,drop_total); // Krossbones
    drop_total = addItemDrop(0x121,0x2F,0x2F,1,drop_total); // Ghost
    drop_total = addItemDrop(0xB6,0x2F,0x2F,1,drop_total); // Klobber
    drop_total = addItemDrop(0xAF,0x2F,0x2F,1,drop_total); // Kaboom
    drop_total = addItemDrop(0x103,0x79,0x0,1,drop_total); // Guard
    drop_total = addItemDrop(0,0,0,0,drop_total);
}

void spawnEnemyDrops(actorData* actor) {
    int level_data = *(int*)(0x807FBB64);
    if ((player_count < 2) && ((level_data & 0x4000) == 0)) {
        int entry_index = -1;
        int actor_index = actor->actorType;
        for (int i = 0; i < DROP_COUNT; i++) {
            if (actor_index == drops[i].source_object) {
                entry_index = i;
            }
        }
        if (entry_index > -1) {
            int song = drops[entry_index].drop_music;
            if (song > 0) {
                playSong(song, 0x3F800000);
            }
            int drop_count = drops[entry_index].drop_count;
            int drop_type = drops[entry_index].dropped_object;
            if (drop_count > 0) {
                int flag = -1;
                int drop_arg = 1;
                if ((actor_index >= 241) && (actor_index <= 245)) {
                    int world = getWorld(CurrentMap, 1);
                    flag = 469 + (5 * world) + (actor_index - 241);
                    if (Rando.item_rando) {
                        drop_type = getBPItem(flag - 469);
                        drop_count = 1;
                        for (int i = 0; i < sizeof(bounce_objects); i++) {
                            if (drop_type == bounce_objects[i]) {
                                drop_arg = 2;
                            }
                        }
                        if (KasplatSpawnBitfield & (1 << (actor_index - 241))) {
                            drop_count = 0;
                        }
                        // Not drop that despawns
                        KasplatSpawnBitfield |= (1 << (actor_index - 241));
                        // if (((drop_type < 75) || (drop_type > 79)) && (drop_type != 151) && (drop_type != 152)) {
                        // }
                    }
                }
                for (int i = 0; i < drop_count; i++) {
                    float drop_rotation_divisor = 0xFFF;
                    drop_rotation_divisor /= drop_count;
                    int drop_rotation = i * drop_rotation_divisor;
                    spawnActorWithFlag(drop_type, *(int*)(&actor->xPos), *(int*)(&actor->yPos), *(int*)(&actor->zPos), drop_rotation, drop_arg, flag, 0);
                }
            }
        }
    }
}

void initItemDropTable(void) {
    buildItemDrops();
    *(short*)(0x806A5CA6) = getHi(&drops[0].source_object);
    *(short*)(0x806A5CB6) = getLo(&drops[0].source_object);

    *(short*)(0x806A5CBA) = getHi(&drops[0].source_object);
    *(short*)(0x806A5CBE) = getLo(&drops[0].source_object);

    *(short*)(0x806A5CD2) = getHi(&drops[0].source_object);
    *(short*)(0x806A5CD6) = getLo(&drops[0].source_object);
    // Spawn Enemy Drops function
    *(int*)(0x806AD40C) = 0x0C000000 | (((int)&spawnEnemyDrops & 0xFFFFFF) >> 2);
    *(int*)(0x806AED14) = 0x0C000000 | (((int)&spawnEnemyDrops & 0xFFFFFF) >> 2);
    *(int*)(0x806AF5A4) = 0x0C000000 | (((int)&spawnEnemyDrops & 0xFFFFFF) >> 2);
    *(int*)(0x806B0218) = 0x0C000000 | (((int)&spawnEnemyDrops & 0xFFFFFF) >> 2);
    *(int*)(0x806B0704) = 0x0C000000 | (((int)&spawnEnemyDrops & 0xFFFFFF) >> 2);
    *(int*)(0x806B0C8C) = 0x0C000000 | (((int)&spawnEnemyDrops & 0xFFFFFF) >> 2);
    *(int*)(0x806B1C88) = 0x0C000000 | (((int)&spawnEnemyDrops & 0xFFFFFF) >> 2);
    *(int*)(0x806B4744) = 0x0C000000 | (((int)&spawnEnemyDrops & 0xFFFFFF) >> 2);
    *(int*)(0x806B5B90) = 0x0C000000 | (((int)&spawnEnemyDrops & 0xFFFFFF) >> 2);
    *(int*)(0x806B61E0) = 0x0C000000 | (((int)&spawnEnemyDrops & 0xFFFFFF) >> 2);
    *(int*)(0x806B744C) = 0x0C000000 | (((int)&spawnEnemyDrops & 0xFFFFFF) >> 2);
    *(int*)(0x806B9AB4) = 0x0C000000 | (((int)&spawnEnemyDrops & 0xFFFFFF) >> 2);
}