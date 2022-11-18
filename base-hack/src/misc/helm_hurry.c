#include "../../include/common.h"

static unsigned short gb_total = 0;
static unsigned char kong_bitfield = 0;

void blueprintCollect(int flag_index) {
    if (Rando.helm_hurry_mode) {
        if (Gamemode == 6) { // Only enable BP Checks in Adv Mode
            if ((flag_index >= 469) && (flag_index < 509)) {
                HelmStartTime += 120; // Add 120 seconds
            }
        }
    }
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

void checkTotalCache(void) {
    int current_gb_total = 0;
    int current_kong_bitfield = 0;
    for (int kong = 0; kong < 5; kong++) {
        for (int level = 0; level < 8; level++) {
            current_gb_total += MovesBase[kong].gb_count[level];
        }
        if (checkFlag(kong_flags[kong],0)) {
            current_kong_bitfield |= (1 << kong);
        }
    }
    int gb_diff = current_gb_total - gb_total;
    if (gb_diff > 0) {
        HelmStartTime += (30 * gb_diff);
    }
    if (kong_bitfield != current_kong_bitfield) {
        HelmStartTime += 300;
    }
    gb_total = current_gb_total;
    kong_bitfield = current_kong_bitfield;
}