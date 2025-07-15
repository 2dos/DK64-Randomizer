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

char aztec_beetle[0x20] = "GOLDEN BANANA";
char caves_beetle[0x20] = "GOLDEN BANANA";

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
        dk_strFormat(location, "%s", CurrentMap == MAP_AZTECBEETLE ? &aztec_beetle : &caves_beetle);
    } else {
        dk_strFormat(location, format, character);
    }
}