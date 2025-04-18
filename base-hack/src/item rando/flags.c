/**
 * @file flags.c
 * @author Ballaam
 * @brief Item Rando elements associated with flag handling
 * @version 0.1
 * @date 2023-01-17
 * 
 * @copyright Copyright (c) 2023
 * 
 */
#include "../../include/common.h"

int getKongFromBonusFlag(int flag) {
    /**
     * @brief Get kong index from a bonus table entry
     * 
     * @param flag Flag index associated with the bonus table entry
     * 
     * @return kong index
     */
    if ((Rando.any_kong_items.major_items) == 0) {
        for (int i = 0; i < BONUS_DATA_COUNT; i++) {
            if (bonus_data[i].flag == flag) {
                return bonus_data[i].kong_actor;
            }
        }
    }
    return 0;
}