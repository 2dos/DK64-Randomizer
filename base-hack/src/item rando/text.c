/**
 * @file text.c
 * @author Ballaam
 * @brief Item Rando text-based changes
 * @version 0.1
 * @date 2023-01-17
 * 
 * @copyright Copyright (c) 2023
 * 
 */
#include "../../include/common.h"

static char* text_rewards[] = {
    "GOLDEN BANANA", // 0
    "BLUEPRINT", // 1
    "BOSS KEY", // 2
    "BATTLE CROWN", // 3
    "BANANA FAIRY", // 4
    "RAREWARE COIN", // 5
    "NINTENDO COIN", // 6
    "BANANA MEDAL", // 7
    "POTION", // 8
    "KONG", // 9
    "BEAN", // 10
    "PEARL", // 11
    "RAINBOW COIN", // 12
    "GLODEN BANANE", // 13
    "NOTHING", // 14
    "SHOPKEEPER", // 15
    "JUNK ITEM", // 16
};

void handleDynamicItemText(char* location, char* format, int character) {
    /**
     * @brief Alter text to convert the | character into the name of an item
     * 
     * @param location Write Location
     * @param format Default formatting of the character
     * @param character Character (ASCII index)
     */
    if (character == 0x7C) {
        // Dynamic Text
        if ((TextItemName == 14) || (TextItemName > 16)) {
            TextItemName = 0;
        }
        dk_strFormat(location, "%s", text_rewards[(int)TextItemName]);
    } else {
        dk_strFormat(location, format, character);
    }
}
char filename[FILENAME_LENGTH + 1] = "";

void handleFilename(char* location, char* format, char* new_name) {
    if (ENABLE_FILENAME) {
        filename[FILENAME_LENGTH] = 0;
        int has_hit_limit = 0;
        for (int i = 0; i < (FILENAME_LENGTH); i++) {
            int val = ReadExtraData(EGD_FILENAME, i);
            if ((val == 0) || (has_hit_limit)) {
                filename[i] = 0;
                has_hit_limit = 1;
            } else {
                filename[i] = val;
            }
        }
        dk_strFormat(location, format, &filename);
    } else {
        dk_strFormat(location, format, new_name);
    }
}