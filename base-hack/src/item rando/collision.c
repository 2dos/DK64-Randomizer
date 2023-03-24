/**
 * @file collision.c
 * @author Ballaam
 * @brief Fixes collision issues with items to handle scaling
 * @version 0.1
 * @date 2023-01-20
 * 
 * @copyright Copyright (c) 2023
 * 
 */

#include "../../include/common.h"

#define QUAD_SIZE 100

int getCollisionSquare_New(float x, float z) {
    float size = QUAD_SIZE;
    float x_quadrant_float = x / size;
    float z_quadrant_float = z / size;
    int x_quad = x_quadrant_float;
    int z_quad = z_quadrant_float;
    if ((x >= 0.0f) && (z >= 0.0f)) {
        int x_quad_limit = *(short*)(0x807FD722);
        int z_quad_limit = *(short*)(0x807FD724);
        if ((x_quad <= x_quad_limit) && (z_quad <= z_quad_limit)) {
            return (x_quad_limit * z_quad) + x_quad;
        }
    }
    return -1;
}

void checkForValidCollision(int player_index, player_collision_info* player) {
    if (CollectableBase.Health > 0) {
        int cached_squares[] = {
            -1, -1, -1,
            -1, -1, -1,
            -1, -1, -1,
        };
        for (int i = 0; i < 9; i++) {
            int x_offset = ((i % 3) - 1) * player->scale;
            int z_offset = ((i / 3) - 1) * player->scale;
            float x = player->x + x_offset;
            if ((*(short*)(0x807FD726) + player->scale) >= x) {
                float z = player->z + z_offset;
                if ((*(short*)(0x807FD728) + player->scale) >= z) {
                    int current_collision_square = getCollisionSquare_New(x, z);
                    int permit = 1;
                    if (i > 0) {
                        int j = 0;
                        while (j < i) {
                            if (cached_squares[j] == current_collision_square) {
                                permit = 0;
                                break;
                            }
                            j++;
                        }
                    }
                    cached_squares[i] = current_collision_square;
                    if ((current_collision_square > -1) && (permit)) {
                        checkModelTwoItemCollision((*ModelTwoHitboxPointer).hitbox[current_collision_square], player_index, player);
                    }
                }
            }
        }
        checkModelTwoItemCollision(MiscHitboxPointer, player_index, player);
    }
}

void initSmallerQuadChecks(void) {
    *(short*)(0x806F4ACA) = QUAD_SIZE;

    *(int*)(0x806F4BF0) = 0x240A0000 | QUAD_SIZE; // addiu $t2, $zero, QUAD_SIZE
    *(int*)(0x806F4BF4) = 0x01510019; // multu $t2, $s1
    *(int*)(0x806F4BF8) = 0x00008812; // mflo $s1
    *(int*)(0x806F4BFC) = 0; // NOP
    *(int*)(0x806F4C00) = 0; // NOP
    *(short*)(0x806F4C16) = QUAD_SIZE;
    *(short*)(0x806F4C52) = QUAD_SIZE;

    *(int*)(0x806F502C) = 0x0C000000 | (((int)&getCollisionSquare_New & 0xFFFFFF) >> 2); // Assigning hitbox to data table
    *(int*)(0x806F5134) = 0x0C000000 | (((int)&getCollisionSquare_New & 0xFFFFFF) >> 2); // Assigning hitbox to data table
    *(int*)(0x806F6A0C) = 0x0C000000 | (((int)&checkForValidCollision & 0xFFFFFF) >> 2); // Detecting if object is inside current quadrant
    *(int*)(0x806F6A2C) = 0x0C000000 | (((int)&checkForValidCollision & 0xFFFFFF) >> 2); // Detecting if object is inside current quadrant
}

item_collision* writeItemScale(int id) {
    /**
     * @brief Write item scale to the collision object
     * 
     * @param id Object Model 2 ID
     * 
     * @return collision object
     */
    item_collision* data = dk_malloc(0x20);
    int* m2location = (int*)ObjectModel2Pointer;
    for (int i = 0; i < ObjectModel2Count; i++) {
        ModelTwoData* _object = getObjectArrayAddr(m2location,0x90,i);
        if (_object->object_id == id) {
            for (int j = 0; j < (int)(sizeof(item_scales) / sizeof(item_scale_info)); j++) {
                if (item_scales[j].type == _object->object_type) {
                    if (item_scales[j].scale != 0.0f) {
                        float scale = _object->scale;
                        scale /= item_scales[j].scale;
                        data->scale = scale;
                        return data;
                    }
                }
            }
            data->scale = 1.0f;
            return data;
        }
    }
    data->scale = 1.0f;
    return data;
}

item_collision* writeItemActorScale(void) {
    /**
     * @brief Write item scale to the collision object, for actors
     * 
     * @return collision object
     */
    item_collision* data = dk_malloc(0x20);
    data->scale = 1.0f;
    return data;
}

int isObjectTangible_detailed(int id) {
    /**
     * @brief Override function for object tangibility
     * 
     * @param id Object id
     * 
     * @return Object tangibility, boolean
     */
    if ((CurrentMap == MAP_FUNGIMILLFRONT) && (id == 0xA)) {
        return 0;
    }
    return isObjectTangible(id);
}

int isCollidingWithCylinder(item_collision* item, player_collision_info* player_collision, playerData* player) {
    if ((item->y + 20) < player->floor) {
        return 0; // Provision to ensure items aren't grabbable from above if there's a floor between the player and 10 units above the object
    }
    float height = object_collisions[(int)item->collision_index].hitbox_height * item->scale;
    int top = item->y + height + player_collision->scale;
    int bottom = item->y - player_collision->scale;
    // int bottom = item->y - 14; // Floor collision goes down by 14 units, this should prevent collision from beneath floors
    if ((player_collision->y < top) && (player_collision->y > bottom)) {
        int x_diff = item->x - player_collision->x;
        int z_diff = item->z - player_collision->z;
        int xz_diff_2 = (x_diff * x_diff) + (z_diff * z_diff);
        float item_radius = object_collisions[(int)item->collision_index].hitbox_radius * item->scale;
        int req_diff = player_collision->scale + item_radius;
        if ((req_diff * req_diff) > xz_diff_2) {
            return 1;
        }
    }
    return 0;
}

int isValidKongCollision(item_collision* object, playerData* player) {
    if (object->kong == 0) {
        return 1;
    }
    if (Rando.quality_of_life.rambi_enguarde_pickup) {
        if (object->kong == player->new_kong) {
            return 1;
        }
    }
    return object->kong == player->characterID;
}

void checkModelTwoItemCollision(item_collision* obj_collision, int player_index, player_collision_info* player_collision) {
    if (!obj_collision) {
        return;
    }
    playerData* player = SwapObject[player_index].player;
    while (1) {
        if (!obj_collision->colliding) {
            if (isValidKongCollision(obj_collision, player)) {
                if (isObjectTangible_detailed(obj_collision->id)) {
                    if (getObjectCollectability(obj_collision->id, player_index, obj_collision->obj_type)) {
                        if (isCollidingWithCylinder(obj_collision, player_collision, player)) {
                            obj_collision->colliding = 1;
                            unkCollisionFunc_0(obj_collision->id, 1);
                            if (obj_collision->flag != -1) {
                                writeDynamicFlagItemToFile(obj_collision->flag, 1, getWorld(CurrentMap, 1));
                            }
                            if (player_count == 1) {
                                if (!LatestCollectedObject) {
                                    collected_item_struct* current_object = CollectedObjects;
                                    while (current_object) {
                                        LatestCollectedObject = current_object;
                                        current_object = current_object->next_item;
                                    }
                                }
                                collected_item_struct* new_item = addNewCollectedObject(obj_collision);
                                new_item->next_item = 0;
                                if (CollectedObjects) {
                                    LatestCollectedObject->next_item = new_item;
                                } else {
                                    CollectedObjects = new_item;
                                }
                                LatestCollectedObject = new_item;
                            }
                            int obj_type = obj_collision->obj_type;
                            if ((obj_type == 0x11) || (obj_type == 0x8F)) {
                                standardCrateHandle(player_index, obj_collision->id, player, obj_type);
                            } else if ((obj_type == 0x2B) || ((obj_type >= 0x205) && (obj_type <= 0x208))) {
                                bunchHandle(player_index, obj_collision->id, player);
                            } else if (player_count > 1) {
                                coinCBCollectHandle(player_index, obj_type, obj_collision->unk13);
                            }
                            if (player_count > 1) {
                                getItem(obj_collision->obj_type);
                                deleteModelTwo(obj_collision->id, 1);
                            }
                            if (-1 >= (*(int*)(0x807FBB64) << 15)) {
                                if (obj_collision->obj_type != 0x1D2) {
                                    spawnModelTwoWithDelay(obj_collision->obj_type, obj_collision->x, obj_collision->y, obj_collision->z, 600);
                                }
                            }
                        }
                    }
                }
            }
        }
        obj_collision = (item_collision*)obj_collision->next;
        if (!obj_collision) {
            return;
        }
    }
}