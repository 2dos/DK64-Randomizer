/**
 * @file hard_mode.c
 * @author Ballaam
 * @brief 
 * @version 0.1
 * @date 2023-08-01
 * 
 * @copyright Copyright (c) 2023
 * 
 */

#include "../../include/common.h"

#define DARK_WORLD_BRIGHTNESS 0.01f
#define LIGHT_BRIGHTNESS 0xFF

/*
    Misc hard mode stuff in case it comes up:
    Disable map geo rendering (donk in the sky):
    - 0x80651598 > 0xA1E00002
*/

int isDarkWorld(maps map, int chunk) {
    if ((map == MAP_MAINMENU) || (map == MAP_ISLES)) {
        return 0;
    }
    if (map == MAP_JAPES) {
        if (chunk == 3) { // Japes Main
            return 0;
        }
    }
    return 1;
}

void alterChunkLighting(int chunk) {
	loadMapChunkLighting(chunk);
	if (chunk == -1) {
		return;
	}
    if (!isDarkWorld(CurrentMap, chunk)) {
        return;
    }
	if (chunk_count > 0) {
		for (int i = 0; i < chunk_count; i++) {
            if (isDarkWorld(CurrentMap, i)) {

            }
			ChunkLighting_Red[i] = DARK_WORLD_BRIGHTNESS;
			ChunkLighting_Green[i] = DARK_WORLD_BRIGHTNESS;
			ChunkLighting_Blue[i] = DARK_WORLD_BRIGHTNESS;
		}
	}
}

void alterChunkData(void* data) {
	loadChunks(data);
	if (chunk_count > 0) {
		for (int i = 0; i < chunk_count; i++) {
			chunkArray[i].reference_dynamic_lighting = isDarkWorld(CurrentMap, i);    
		}
	}
}

#define SHINE_DISTANCE 30
#define SHINE_RADIUS 50
#define USE_POSITIONAL_SHINE 0

void shineLight(actorData* actor, int kongType) {
    genericKongCode(actor, kongType);
    playerData* player = (playerData*)actor;
    if (!isDarkWorld(CurrentMap, player->chunk)) {
        return;
    }
    if (USE_POSITIONAL_SHINE) {
        // Caused way too much lag for what it was worth
        float shine_x = determineXRatioMovement(actor->rot_y) * SHINE_DISTANCE;
        float shine_z = determineZRatioMovement(actor->rot_y) * SHINE_DISTANCE;
        shine_x += actor->xPos;
        shine_z += actor->zPos;
        renderLight(shine_x, actor->yPos + 10, shine_z, shine_x, actor->yPos + 20, shine_z, SHINE_RADIUS, 0, LIGHT_BRIGHTNESS, LIGHT_BRIGHTNESS, LIGHT_BRIGHTNESS);
    }
}

static unsigned char fall_damage_immunity = 0;

void setFallDamageImmunity(int value) {
    fall_damage_immunity = value;
}

void handleFallDamageImmunity(void) {
    if (ObjectModel2Timer > 0) {
        if (fall_damage_immunity > 0) {
            fall_damage_immunity -= 1;
        }
    }
}

void transformBarrelImmunity(void) {
    setFallDamageImmunity(60);
    DisplayExplosionSprite();
}

void fallDamageWrapper(int action, void* actor, int player_index) {
    if (ObjectModel2Timer < 100) {
        return;
    }
    if (fall_damage_immunity > 0) {
        return;
    }
    setAction(action, actor, player_index);
}