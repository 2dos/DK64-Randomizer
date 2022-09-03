#include "../../include/common.h"

void blueprintCollect(int flag_index, int destination, int flag_type) {
    if (Rando.helm_hurry_mode) {
        if (Gamemode == 6) { // Only enable BP Checks in Adv Mode
            if (checkFlag(flag_index,flag_type) == 0) { // Only increment timer if blueprint hasn't been collected (prevents cheese with double kasplat spawn)
                HelmStartTime += 120; // Add 120 seconds
            }
        }
    }
    setFlag(flag_index,destination,flag_type);
}

int canSaveHelmHurry(void) {
    if (player_count != 1) {
        return 0;
    }
    if (Rando.helm_hurry_mode) {
        if (checkFlag(FLAG_LOADED_GAME_OVER,0)) {
            return 0;
        }
    }
    return 1;
}