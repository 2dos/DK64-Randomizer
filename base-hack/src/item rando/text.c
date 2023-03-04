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
    "\x04GOLDEN BANANA\x04", // 0
    "\x04BLUEPRINT\x04", // 1
    "\x04BOSS KEY\x04", // 2
    "\x04BATTLE CROWN\x04", // 3
    "\x04BANANA FAIRY\x04", // 4
    "\x04RAREWARE COIN\x04", // 5
    "\x04NINTENDO COIN\x04", // 6
    "\x04BANANA MEDAL\x04", // 7
    "\x04POTION\x04", // 8
    "\x04KONG\x04", // 9
    "\x04BEAN\x04", // 10
    "\x04PEARL\x04", // 11
    "\x04RAINBOW COIN\x04", // 12
    "\x04GLODEN BANANE\x04", // 13
    "\x04NOTHING\x04", // 14
    "\x04JUNK ITEM\x04", // 15
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