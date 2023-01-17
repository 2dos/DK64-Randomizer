#include "../../include/common.h"

static unsigned short gb_total = 0;
static unsigned char kong_bitfield = 0;

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

void addHelmTime(helm_hurry_items item, int multiplier) {
    if (Rando.helm_hurry_mode) {
        if (item != HHITEM_NOTHING) {
            HelmStartTime += (Rando.helm_hurry_bonuses[(int)(item) - 1] * multiplier);
        }
    }
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
        addHelmTime(HHITEM_GB, gb_diff);
    }
    if (kong_bitfield != current_kong_bitfield) {
        addHelmTime(HHITEM_KONG, 1);
    }
    gb_total = current_gb_total;
    kong_bitfield = current_kong_bitfield;
}

int initHelmHurry(void) {
    if (Rando.helm_hurry_start == 0) {
        HelmStartTime = 60;
        return 0;
    }
    HelmStartTime = Rando.helm_hurry_start;
    return 0;
}