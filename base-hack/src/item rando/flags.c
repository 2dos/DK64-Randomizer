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

int hasMove(int flag) {
    if (flag == 0) {
        return 1;
    }
    if (flag & 0x8000) {
        int item_kong = (flag >> 12) & 7;
        if (item_kong > 4) {
            item_kong = 0;
        }
        int item_type = (flag >> 8) & 15;
        int item_index = flag & 0xFF;
        if (item_type == 7) {
            return 0;
        } else {
            char* temp_fba = (char*)&MovesBase[item_kong];
            int shift = 0;
            if (item_index != 0) {
                shift = item_index - 1;
            }
            int init_val = *(char*)(temp_fba + item_type);
            return init_val & (1 << shift);
        }
    } else {
        return hasFlagMove(flag);
    }
    return 0;
}

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