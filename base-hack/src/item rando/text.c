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
    "GOLDEN BANANA",
    "BLUEPRINT",
    "BOSS KEY",
    "BATTLE CROWN",
    "BANANA FAIRY",
    "RAREWARE COIN",
    "NINTENDO COIN",
    "BANANA MEDAL",
    "POTION",
    "KONG",
    "BEAN",
    "PEARL",
    "RAINBOW COIN",
    "NOTHING",
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
        if (TextItemName >= 14) {
            TextItemName = 0;
        }
        dk_strFormat(location, "%s", text_rewards[(int)TextItemName]);
    } else {
        dk_strFormat(location, format, character);
    }
}