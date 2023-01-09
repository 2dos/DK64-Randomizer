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