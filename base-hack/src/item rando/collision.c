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