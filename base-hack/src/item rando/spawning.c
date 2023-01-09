#include "../../include/common.h"

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
        if (!checkFlag(flag, 0)) {
            spawnObjectAtActor(object, flag);
        }
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

void spawnDirtPatchReward(int object, int x_f, int y_f, int z_f, int unk0, int cutscene, int flag, int unk1) {
    /*
        TODO:
        Add to item dictionaries
        Add to logic
        Update writer to place rainbow coins
        Add to shop indicator
        Ensure keys/moves works with it, displaying the text and turning in the keys
        Add Rainbow Coins to check screen
    */
    int new_obj = getRainbowCoinItem(flag);
    if (new_obj != 0) {
        object = new_obj;
    }
    if (object != 153) {
        for (int i = 0; i < sizeof(bounce_objects); i++) {
            if (object == bounce_objects[i]) {
                cutscene = 2;
            }
        }
        spawnActorWithFlag(object, x_f, y_f, z_f, unk0, cutscene, flag, unk1);
    }
}

void spawnCharSpawnerActor(int actor, SpawnerInfo* spawner) {
    // Change Character Spawner Information account for fairy rando
    /*
        INFORMATION:
            +----------------+----------------------------+--------+---------------+
            |   Model Name   |         Base Model         | Tested |   New Model   |
            +----------------+----------------------------+--------+---------------+
            | Golden Banana  | 0x69                       | True   | See Left      |
            | Boss Key       | 0xA5                       | True   | 0xF5          |
            | Crown          | 0xAF                       | True   | 0xF4          |
            | Fake Item      | ----                       | ----   | 0x10E         |
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

static unsigned char master_copy[345] = {};

typedef struct packet_extra_data {
    /* 0x000 */ char unk_00[0xA];
    /* 0x00A */ short index;
} packet_extra_data;

int getBarrelModel(int index) {
    if (index < 95) {
        int actor = bonus_data[index].spawn_actor;
        switch (actor) {
            case 78:
            case 75:
            case 77:
            case 79:
            case 76:
                return 0x102; // Blueprint
            case 151:
                return 0x103; // Nintendo Coin
            case 152:
                return 0x104; // Rareware Coin
            case 72:
                return 0x105; // Key
            case 86:
                return 0x106; // Crown
            case 154:
                return 0x107; // Medal
            case 157:
            case 158:
            case 159:
            case 160:
            case 161:
            case 162:
                return 0x108; // Potion
            case 141:
            case 142:
            case 143:
            case 144:
                return 0xFD + (actor - 141); // DK-Tiny
            case 155:
                return 0x101; // Chunky
            case 172:
                return 0x109; // Bean
            case 174:
                return 0x10A; // Pearl
            case 88:
                return 0x10B; // Fairy
            case 140:
                return 0x10C; // Rainbow Coin
            case 217:
                return 0x10D; // Fake Item
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
    for (int i = 0; i < 345; i++) {
        master_copy[i] = ActorMasterType[i];
    }
    master_copy[0x1C] = 5;
    *(short*)(0x80677EF6) = getHi(&master_copy[0]);
    *(short*)(0x80677F02) = getLo(&master_copy[0]);
    *(int*)(0x8074DA44) = (int)&SpawnBarrel;
    *(int*)(0x80689368) = 0x0C000000 | (((int)&SpawnPreSpawnedBarrel & 0xFFFFFF) >> 2); // Change model if barrel is being reloaded
}