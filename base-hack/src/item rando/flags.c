#include "../../include/common.h"

int checkFlagDuplicate(short flag, int type) {
    // Duplicate of the check flag function, for the purpose of checking a flag without referencing the lookup table
    if (flag == -1) {
        return 0;
    }
    unsigned char* fba = 0;
    if ((type == 0) || (type == 2)) {
        fba = (unsigned char*)getFlagBlockAddress(type);
    } else {
        fba = (unsigned char*)&TempFlagBlock[0];
    }
    int offset = flag >> 3;
    int shift = flag & 7;
    return (fba[offset] >> shift) & 1;
}

void setFlagDuplicate(short flag, int set, int type) {
    if (flag != -1) {
        unsigned char* fba = 0;
        if ((type == 0) || (type == 2)) {
            fba = (unsigned char*)getFlagBlockAddress(type);
        } else {
            fba = (unsigned char*)&TempFlagBlock[0];
        }
        int offset = flag >> 3;
        int shift = flag & 7;
        if (!set) {
            fba[offset] &= ~(1 << shift);
        } else {
            fba[offset] |= (1 << shift);
        }
        checkVictory_flaghook(flag);
    }
}

int countFlagsForKongFLUT(int startFlag, int start, int cap, int kong) {
    int count = 0;
    if (kong < 5) {
        for (int i = start; i <= cap; i++) {
            int check = getFlagIndex(startFlag, i, kong);
            if (check > -1) {
                count += checkFlag(check, 0);
            }
        }
    }
    return count;
}

int countFlagsDuplicate(int start, int count, int type) {
    int end = start + count;
    int amt = 0;
    for (int i = start; i < end; i++) {
        amt += checkFlagDuplicate(i, type);
    }
    return amt;
}

static short flut_cache[40] = {};
static unsigned char cache_spot = 0;
static int flut_size = -1;

void cacheFlag(int input, int output) {
    int slot = cache_spot;
    flut_cache[(2 * slot)] = input;
    flut_cache[(2 * slot) + 1] = output;
    cache_spot = (cache_spot + 1) % 20;
}

int clampFlag(int flag) {
    /*
        Clamp flag for GBs, Medals, Crowns, BPs, Nin/RW Coin, Boss Key
    */
    if ((flag >= 0x1D5) && (flag <= 0x1FC)) {
        return 1; // Blueprints
    }
    if ((flag >= 0x225) && (flag <= 0x24C)) {
        return 1; // Medal
    }
    if ((flag >= 0x261) && (flag <= 0x26A)) {
        return 1; // Crown
    }
    if ((flag >= 589) && (flag <= 608)) {
        return 1; // Fairy
    }
    if (flag == 0x17B) {
        return 1; // RW Coin
    }
    if ((flag >= 0x1) && (flag <= 0x1F)) {
        return 1; // Japes GBs + Key 1
    }
    if ((flag >= 0x31) && (flag <= 0x4D)) {
        return 1; // Aztec GBs + Key 2
    }
    if ((flag >= 0x70) && (flag <= 0x8B)) {
        return 1; // Factory GBs + Key 3 + Nintendo Coin
    }
    if ((flag >= 0x9A) && (flag <= 0xA8)) {
        return 1; // Galleon GBs (Group 1) + Key 4
    }
    if ((flag >= 0xB6) && (flag <= 0xEC)) {
        return 1; // Galleon GBs (Group 2) + Fungi GBs (Group 1) + Key 5 + Pearls
    }
    if ((flag >= 0xF7) && (flag <= 0x119)) {
        return 1; // Fungi GBs (Group 2) + Caves GBs (Group 1)
    }
    if ((flag >= 0x124) && (flag <= 0x146)) {
        return 1; // Caves GBs (Group 2) + Key 6 + Castle GBs (Group 1) + Key 7 + Rareware GB
    }
    if ((flag >= 0x15E) && (flag <= 0x161)) {
        return 1; // Castle GBs (Group 2)
    }
    if ((flag == 0x17C) || (flag == 0x17D)) {
        return 1; // Key 8 + First GB
    }
    if ((flag >= 0x18E) && (flag <= 0x1AF)) {
        return 1; // Isles GBs
    }
    if ((flag >= FLAG_RAINBOWCOIN_0) && (flag < (FLAG_RAINBOWCOIN_0 + 16))) {
        return 1; // Rainbow Coins
    }
    if (flag == 0x300) {
        return 1; // Fungi Bean
    }
    return 0;
}

void* checkMove(short* flag, void* fba, int source, int vanilla_flag) {
    if (*flag & 0x8000) {
        // Is Move
        int item_kong = (*flag >> 12) & 7;
        if (item_kong > 4) {
            item_kong = 0;
        }
        int item_type = (*flag >> 8) & 15;
        int item_index = *flag & 0xFF;
        if (item_type == 7) {
            *flag = 0;
            return fba;
        } else {
            char* temp_fba = (char*)&MovesBase[item_kong];
            if (item_index == 0) {
                *flag = 0;
            } else {
                *flag = item_index - 1;
            }
            int init_val = *(char*)(temp_fba + item_type);
            if (((init_val & (1 << *flag)) == 0) && (source == 1)) {
                // Move given
                spawnActor(324,0);
                TextOverlayData.type = item_type;
                TextOverlayData.flag = item_index;
                TextOverlayData.kong = item_kong;
                if (item_type == 4) {
                    if (CollectableBase.Melons < 2) {
                        CollectableBase.Melons = 2;
                        CollectableBase.Health = CollectableBase.Melons << 2;
                    }
                }
            }
            return temp_fba + item_type;
        }
    } else {
        int flag_index = *flag;
        int spawn_overlay = 0;
        int item_type = 0;
        int item_index = 0;
        int item_kong = 0;
        if ((source == 1) && (!checkFlagDuplicate(flag_index, 0)) && (Gamemode == 6)) {
            if ((flag_index == FLAG_ITEM_SLAM_0) || (flag_index == FLAG_ITEM_SLAM_1)) {
                // Slam
                MovesBase[0].simian_slam += 1;
                item_index = MovesBase[0].simian_slam;
                for (int i = 1; i < 5; i++) {
                    MovesBase[i].simian_slam = item_index;
                }
                spawn_overlay = 1;
                item_type = 1;
            } else if ((flag_index == FLAG_ITEM_BELT_0) || (flag_index == FLAG_ITEM_BELT_1)) {
                // Belt
                MovesBase[0].ammo_belt += 1;
                item_index = MovesBase[0].ammo_belt;
                for (int i = 1; i < 5; i++) {
                    MovesBase[i].ammo_belt = item_index;
                }
                spawn_overlay = 1;
                item_type = 3;
            } else if ((flag_index >= FLAG_ITEM_INS_0) && (flag_index <= FLAG_ITEM_INS_2)) {
                // Instrument Upgrade
                item_index = 0;
                for (int i = 1; i < 4; i++) {
                    if (MovesBase[0].instrument_bitfield & (1 << i)) {
                        item_index = i;
                    }
                }
                item_index += 1;
                for (int i = 0; i < 5; i++) {
                    MovesBase[i].instrument_bitfield |= (1 << item_index);
                }
                spawn_overlay = 1;
                item_type = 4;
                if (item_index >= 2) {
                    // 3rd Melon
                    if (CollectableBase.Melons < 3) {
                        CollectableBase.Melons = 3;
                        CollectableBase.Health = CollectableBase.Melons << 2;
                    }
                } else {
                    if (CollectableBase.Melons < 2) {
                        CollectableBase.Melons = 2;
                        CollectableBase.Health = CollectableBase.Melons << 2;
                    }
                }
                item_index += 1;
            } else if ((flag_index >= FLAG_TBARREL_DIVE) && (flag_index <= FLAG_TBARREL_BARREL)) {
                spawn_overlay = 1;
                item_type = 5;
                item_index = flag_index;
            } else if ((flag_index == FLAG_ABILITY_CAMERA) || (flag_index == FLAG_ABILITY_SHOCKWAVE)) {
                spawn_overlay = 1;
                item_type = 5;
                item_index = flag_index;
            } else {
                for (int i = 0; i < 5; i++) {
                    if (flag_index == kong_flags[i]) {
                        spawn_overlay = 1;
                        item_type = 5;
                        item_index = flag_index;
                    }
                }
            }
            // Jetpac/Arcade GB Give
            int give_gb = 0;
            int give_rainbow = 0;
            if ((vanilla_flag == FLAG_COLLECTABLE_NINTENDOCOIN) && (Rando.arcade_reward == 5)) {
                give_gb = 1;
            } else if ((vanilla_flag == FLAG_COLLECTABLE_RAREWARECOIN) && (Rando.jetpac_reward == 5)) {
                give_gb = 1;
            } else if ((vanilla_flag == FLAG_COLLECTABLE_NINTENDOCOIN) && (Rando.arcade_reward == 20)) {
                give_rainbow = 1;
            } else if ((vanilla_flag == FLAG_COLLECTABLE_RAREWARECOIN) && (Rando.jetpac_reward == 11)) {
                give_rainbow = 1;
            }
            if (give_gb) {
                if (!checkFlag(vanilla_flag, 0)) {
                    int world = getWorld(CurrentMap, 1);
                    if (world < 8) {
                        giveGB(Character, world);
                    }
                }
            } else if (give_rainbow) {
                if (!checkFlag(vanilla_flag, 0)) {
                    giveRainbowCoin();
                }
            }
            if (spawn_overlay) {
                spawnActor(324, 0);
                TextOverlayData.type = item_type;
                TextOverlayData.flag = item_index;
                TextOverlayData.kong = item_kong;
            }
        }
    }
    return fba;
}

void getFLUTSize(void) {
    for (int i = 0; i < 400; i++) {
        if (ItemRando_FLUT[2 * i] == -1) {
            flut_size = i;
            return;
        }
    }
}

int binarySearch(int search_item, int low, int high) {
    int lim = high - low;
    int old_dist = (high - low) + 1;
    while (low != high) {
        int mid = (low + high) / 2;
        int loc = 2 * mid;
        if (search_item == ItemRando_FLUT[loc]) {
            return mid;
        } else if (search_item > ItemRando_FLUT[loc]) {
            low = mid + 1;
        } else {
            high = mid - 1;
        }
        lim -= 1;
        if (lim == 0) {
            return -1;
        }
        if ((high - low) > old_dist) {
            // diverging
            return -1;
        }
        old_dist = (high - low);
    }
    return -1;
}

void* searchFlag(int old_flag, short* flag_write, int source, void* fba) {
    if (flut_size < 10) {
        // Plain search
        for (int i = 0; i < (flut_size * 2); i++) {
            int lookup = ItemRando_FLUT[(2 * i)];
            if (old_flag == lookup) {
                *flag_write = ItemRando_FLUT[(2 * i) + 1];
                cacheFlag(old_flag, *flag_write);
                return checkMove(flag_write, fba, source, lookup);
            } else if (lookup == -1) {
                cacheFlag(old_flag, -1);
                return fba;
            }
        }
    } else {
        // Search by halves
        int index = binarySearch(old_flag, 0, flut_size - 1);
        if (index >= -1) {
            int lookup = ItemRando_FLUT[(2 * index)];
            if (old_flag == lookup) {
                *flag_write = ItemRando_FLUT[(2 * index) + 1];
                cacheFlag(old_flag, *flag_write);
                return checkMove(flag_write, fba, source, lookup);
            }
        }
    }
    cacheFlag(old_flag, -1);
    return fba;
}

void* updateFlag(int type, short* flag, void* fba, int source) {
    if ((Rando.item_rando) && (type == 0) && (*flag != 0)) {
        if (flut_size == -1) {
            getFLUTSize();
        }
        int vanilla_flag = *flag;
        if (flut_size > 0) {
            if (clampFlag(vanilla_flag)) {
                for (int i = 0; i < 20; i++) {
                    if (flut_cache[(2 * i)] == vanilla_flag) {
                        if (flut_cache[(2 * i) + 1] != -1) {
                            *flag = flut_cache[(2 * i) + 1];
                        }
                        return checkMove(flag, fba, source, vanilla_flag);
                    }
                }
                for (int i = 0; i < flut_size; i++) {
                    int lookup = ItemRando_FLUT[(2 * i)];
                    if (vanilla_flag == lookup) {
                        *flag = ItemRando_FLUT[(2 * i) + 1];
                        cacheFlag(vanilla_flag, *flag);
                        return checkMove(flag, fba, source, vanilla_flag);
                    } else if (lookup == -1) {
                        cacheFlag(vanilla_flag, -1);
                        return fba;
                    }
                }
            }
        }
    }
    return fba;
}

int getKongFromBonusFlag(int flag) {
    if ((Rando.any_kong_items & 1) == 0) {
        for (int i = 0; i < 95; i++) {
            if (bonus_data[i].flag == flag) {
                return bonus_data[i].kong_actor;
            }
        }
    }
    return 0;
}