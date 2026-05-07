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

void *getTextData(data_indexes table_index, int file_index, int unk0, int unk1) {
    if (file_index & 0x40) {
        table_index = TABLE_UNK06;
        if ((Rando.disable_flavor_text) && (file_index == COMP_TEXT_PREVIEWSFLAVOR)) {
            file_index = 0;
        } else {
            file_index &= 0x3F;
        }
    }
    return getMapData(table_index, file_index, unk0, unk1);
}

int getCharWidthMask(int style, unsigned char *character) {
    if (*character < 0x10) {
        if (style == 6) {
            *character = 132;
            return 0;
        }
    }
    return getCharacterWidth(style, character);
}