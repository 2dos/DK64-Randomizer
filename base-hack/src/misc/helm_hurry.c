/**
 * @file helm_hurry.c
 * @author Ballaam
 * @brief Helm Hurry gamemode functions
 * @version 0.1
 * @date 2022-09-02
 * 
 * @copyright Copyright (c) 2022
 * 
 */
#include "../../include/common.h"

static unsigned short gb_total = 0;
static unsigned char kong_bitfield = 0;

int canSaveHelmHurry(void) {
    /**
     * @brief Will the game save in Helm Hurry mode
     * 
     * @return Enable Saving
     */
    if (player_count != 1) {
        return 0;
    }
    if (Rando.helm_hurry_mode) {
        if (ReadExtraData(EGD_HELMHURRYDISABLE, 0)) {
            return 0;
        }
    }
    return 1;
}

void addHelmTime(helm_hurry_items item, int multiplier) {
    /**
     * @brief Add Helm time to the Helm Hurry timer
     * 
     * @param item Item Index of the bonus
     * @param multiplier Amount of the item collected
     */
    if (Rando.helm_hurry_mode) {
        if (item != HHITEM_NOTHING) {
            HelmStartTime += (Rando.helm_hurry_bonuses[(int)(item) - 1] * multiplier);
            if (HelmStartTime < 0) {
                HelmStartTime = 0;
            }
        }
    }
}

void checkTotalCache(void) {
    /**
     * @brief Compare variable values to their previously stored values to check for differences
     */
    int current_gb_total = getTotalGBs();
    int current_kong_bitfield = 0;
    for (int kong = 0; kong < 5; kong++) {
        if (checkFlag(kong_flags[kong], FLAGTYPE_PERMANENT)) {
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

void finishHelmHurry(void) {
    save(); // Save all stats
    SaveExtraData(EGD_HELMHURRYDISABLE, 0, 1); // disable saving
    SaveToGlobal();
    LoadGameOver();
}

int initHelmHurry(void) {
    /**
     * @brief Initializes the Helm Hurry timer
     */
    if (getNewSaveTime() > 5) {
        // Old file loaded
        HelmStartTime = ReadExtraData(EGD_HELMHURRYIGT, 0) & 0x7FFFFFFF;
        return 0;
    }
    if (Rando.helm_hurry_start == 0) {
        HelmStartTime = 60;
        return 0;
    }
    HelmStartTime = Rando.helm_hurry_start;
    return 0;
}

void saveHelmHurryTime(void) {
    if ((Rando.helm_hurry_mode) && (isGamemode(GAMEMODE_ADVENTURE, 1) && (HelmTimerShown))) {
        int save_value = HelmCurrentTime;
        if (save_value > 65535) {
            save_value = 65535; // Allows for 18h12m15s of time
        } else if (save_value < 0) {
            save_value = 0;
        }
        SaveExtraData(EGD_HELMHURRYIGT, 0, save_value);
    }
}