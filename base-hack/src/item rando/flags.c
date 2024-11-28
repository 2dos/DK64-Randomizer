/**
 * @file flags.c
 * @author Ballaam
 * @brief Item Rando elements associated with flag handling
 * @version 0.1
 * @date 2023-01-17
 * 
 * @copyright Copyright (c) 2023
 * 
 */
#include "../../include/common.h"

/*
    Common terminology:
    - FLUT (Flag LookUp Table): A table in ROM which converts flags from their vanilla flag to a new flag.
        - Eg. If you have the input flag of Rareware GB, and the output flag of DK Japes Medal, picking up rareware GB will set
        the DK Japes Medal flag instead of the normal flag. Check functions also go through this table.
        It's the crux of how item rando works without having to alter a large majority of the game code.
*/

int checkFlagDuplicate(short flag, flagtypes type) {
    /**
     * @brief Duplicate of the check flag function, but instead of going through the FLUT, it checks the vanilla flag
     * 
     * @param flag Flag Index
     * @param type Flag Type (0 = Permanent, 1 = Global, 2 = Temporary)
     * 
     * @return is the flag set (true/false)
     */
    if (flag == -1) {
        return 0;
    }
    unsigned char* fba = 0;
    if ((type == FLAGTYPE_PERMANENT) || (type == FLAGTYPE_GLOBAL)) {
        fba = (unsigned char*)getFlagBlockAddress(type);
    } else {
        fba = (unsigned char*)&TempFlagBlock[0];
    }
    int offset = flag >> 3;
    int shift = flag & 7;
    return (fba[offset] >> shift) & 1;
}

void setFlagDuplicate(short flag, int set, flagtypes type) {
    /**
     * @brief Duplicate of the set flag function, but instead of going through the FLUT, it sets the vanilla flag
     * 
     * @param flag Flag Index
     * @param set Determines whether to set the flag (1) or clear the flag (0)
     * @param type Flag Type (0 = Permanent, 1 = Global, 2 = Temporary)
     */
    if (flag != -1) {
        unsigned char* fba = 0;
        if ((type == FLAGTYPE_PERMANENT) || (type == FLAGTYPE_GLOBAL)) {
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
    /**
     * @brief Counts a flag array for the amount of flags set within that array.
     * The array is special in that there's items for each kong. This goes via the FLUT though
     * 
     * @param startFlag Starting flag in the array
     * @param start Starting position in the array
     * @param cap Finishing position in the array
     * @param kong Kong which this is being checked for
     * 
     * @return set count
     */
    int count = 0;
    if (kong < 5) {
        for (int i = start; i <= cap; i++) {
            int check = getFlagIndex(startFlag, i, kong);
            if (check > -1) {
                count += checkFlag(check, FLAGTYPE_PERMANENT);
            }
        }
    }
    return count;
}

int countFlagsDuplicate(int start, int count, flagtypes type) {
    /**
     * @brief Counts a flag array for the amount of flags set within that array. Doesn't go via the FLUT
     * 
     * @param start Starting flag in the array
     * @param count Amount of flags to check
     * @param type Flag type (0 = Permanent, 1 = Global, 2 = Temporary)
     * 
     * @return set count
     */
    int end = start + count;
    int amt = 0;
    for (int i = start; i < end; i++) {
        amt += checkFlagDuplicate(i, type);
    }
    return amt;
}

static short flut_cache[40] = {};
static unsigned char cache_spot = 0;
int flut_size = -1;

void cacheFlag(int input, int output) {
    /**
     * @brief Enter flag into the cache table, to reduce the amount of times the game searches the whole FLUT
     * 
     * @param input vanilla flag
     * @param output output flag
     */
    int slot = cache_spot;
    flut_cache[(2 * slot)] = input;
    flut_cache[(2 * slot) + 1] = output;
    cache_spot = (cache_spot + 1) % 20;
}

typedef struct flag_clamping_struct {
    /* 0x000 */ short flag_start;
    /* 0x002 */ short flag_count;
} flag_clamping_struct;

static const flag_clamping_struct clamp_bounds[] = {
    {.flag_start = 0x1D5, .flag_count = 40}, // Blueprints
    {.flag_start = 0x225, .flag_count = 40}, // Regular Medals
    {.flag_start = 0x261, .flag_count = 10}, // Crowns
    {.flag_start = 589, .flag_count = 20}, // Fairies
    {.flag_start = 0x17B, .flag_count = 1}, // RW Coin
    {.flag_start = 1, .flag_count = 0x1F}, // Japes GBs + Key 1
    {.flag_start = 0x31, .flag_count = 0x1D}, // Aztec GBs + Key 2
    {.flag_start = 0x70, .flag_count = 0x1C}, // Factory GBs + Key 3 + Nintendo Coin
    {.flag_start = 0x9A, .flag_count = 0xF}, // Galleon GBs (Group 1) + Key 4
    {.flag_start = 0xB6, .flag_count = 0x37}, // Galleon GBs (Group 2) + Fungi GBs (Group 1) + Key 5 + Pearls
    {.flag_start = 0xF7, .flag_count = 0x23}, // Fungi GBs (Group 2) + Caves GBs (Group 1)
    {.flag_start = 0x124, .flag_count = 0x23}, // Caves GBs (Group 2) + Key 6 + Castle GBs (Group 1) + Key 7 + Rareware GB
    {.flag_start = 0x15E, .flag_count = 0x4}, // Castle GBs (Group 2)
    {.flag_start = 0x17C, .flag_count = 0x2}, // Key 8 + First GB
    {.flag_start = 0x18E, .flag_count = 0x22}, // Isles GBs
    {.flag_start = FLAG_RAINBOWCOIN_0, .flag_count = 16}, // Rainbow Coins
    {.flag_start = FLAG_COLLECTABLE_BEAN, .flag_count = 1}, // Bean
    {.flag_start = FLAG_TBARREL_DIVE, .flag_count = 4}, // TBarrel Moves
    {.flag_start = FLAG_MELONCRATE_0, .flag_count = 16}, // Melon Crates
    {.flag_start = FLAG_ENEMY_KILLED_0, .flag_count = ENEMIES_TOTAL}, // Dropsanity
    {.flag_start = FLAG_MEDAL_ISLES_DK, .flag_count = 5}, // Isles Medals
    {.flag_start = FLAG_WRINKLYVIEWED, .flag_count = 35}, // Hints
    {.flag_start = FLAG_ABILITY_CAMERA, .flag_count = 1}, // Climbing
};

int clampFlag(int flag) {
    /**
     * @brief Clamp flag to filter for flags only present in the FLUT.
     * 
     * @param flag Flag to check
     * 
     * @return is flag in FLUT
     */
    for (int i = 0; i < sizeof(clamp_bounds)/sizeof(flag_clamping_struct); i++) {
        int flag_start = clamp_bounds[i].flag_start;
        int flag_end = flag_start + clamp_bounds[i].flag_count;
        if ((flag >= flag_start) && (flag < flag_end)) {
            return 1;
        }
    }
    return 0;
}

void moveGiveHook(int kong, PURCHASE_TYPES type, int index, int is_jetpac) {
    /**
     * @brief Hook into the move give function, only for non-progressive moves purchased from Cranky, Candy and Funky
     * 
     * @param kong Kong index
     * @param type Move Type
     * @param index Move Index
     */
    if (type == 0) {
        int pad_moves[] = {1, 3, 2, 3, 3};
        if (kong < 5) {
            if (pad_moves[kong] == index) {
                refreshPads((pad_refresh_signals)kong);
            }
        }
    }
    spawnItemOverlay(type, kong, index, is_jetpac);
    if (type == 4) {
        if (CollectableBase.Melons < 2) {
            CollectableBase.Melons = 2;
            CollectableBase.Health = CollectableBase.Melons << 2;
        }
    }
}

void displayKeyText(int flag) {
    for (int i = 0; i < 8; i++) {
        if (getKeyFlag(i) == flag) {
            spawnItemOverlay(PURCHASE_FLAG, 0, getKeyFlag(i), 0);
        }
    }
}

int hasMove(int flag) {
    if (flag == 0) {
        return 1;
    }
    if (flag & 0x8000) {
        int item_kong = (flag >> 12) & 7;
        if (item_kong > 4) {
            item_kong = 0;
        }
        int item_type = (flag >> 8) & 15;
        int item_index = flag & 0xFF;
        if (item_type == 7) {
            return 0;
        } else {
            char* temp_fba = (char*)&MovesBase[item_kong];
            int shift = 0;
            if (item_index != 0) {
                shift = item_index - 1;
            }
            int init_val = *(char*)(temp_fba + item_type);
            return init_val & (1 << shift);
        }
    } else {
        return checkFlagDuplicate(flag, FLAGTYPE_PERMANENT);
    }
    return 0;
}

static unsigned char arcade_hh_bonus[] = {
    HHITEM_COMPANYCOIN, // # 0 - Nintendo Coin / No Item
    HHITEM_BEAN, // "bean",  # 1 - Bean
    HHITEM_BLUEPRINT, // "blueprint",  # 2 - Blueprint
    HHITEM_CROWN, // "crown",  # 3 - Crown
    HHITEM_FAIRY, // "fairy",  # 4 - Fairy
    HHITEM_GB, // "gb",  # 5 - GB
    HHITEM_KEY, // "key",  # 6 - Key
    HHITEM_MEDAL, // "medal",  # 7 - Medal
    HHITEM_PEARL, // "pearl",  # 8 - Pearl
    HHITEM_MOVE, // "potion_dk",  # 9 - Potion (DK)
    HHITEM_MOVE, // "potion_diddy",  # 10 - Potion (Diddy)
    HHITEM_MOVE, // "potion_lanky",  # 11 - Potion (Lanky)
    HHITEM_MOVE, // "potion_tiny",  # 12 - Potion (Tiny)
    HHITEM_MOVE, // "potion_chunky",  # 13 - Potion (Chunky)
    HHITEM_MOVE, // "potion_any",  # 14 - Potion (Any)
    HHITEM_KONG, // "dk",  # 15 - DK
    HHITEM_KONG, // "diddy",  # 16 - Diddy
    HHITEM_KONG, // "lanky",  # 17 - Lanky
    HHITEM_KONG, // "tiny",  # 18 - Tiny
    HHITEM_KONG, // "chunky",  # 19 - Chunky
    HHITEM_RAINBOWCOIN, // "rainbow",  # 20 - Rainbow Coin
    HHITEM_COMPANYCOIN, // "rwcoin",  # 21 - RW Coin
    HHITEM_NOTHING, // "melon",  # 22 - Melon Slice
};

static unsigned char jetpac_hh_bonus[] = {
    HHITEM_COMPANYCOIN, // # 0 - Rareware Coin / No Item
    HHITEM_BEAN, // "bean",  # 1 - Bean
    HHITEM_BLUEPRINT, // "blueprint",  # 2 - Blueprint
    HHITEM_CROWN, // "crown",  # 3 - Crown
    HHITEM_FAIRY, // "fairy",  # 4 - Fairy
    HHITEM_GB, // "gb",  # 5 - GB
    HHITEM_KEY, // "key",  # 6 - Key
    HHITEM_MEDAL, // "medal",  # 7 - Medal
    HHITEM_PEARL, // "pearl",  # 8 - Pearl
    HHITEM_MOVE, // "potion",  # 9 - Potion
    HHITEM_KONG, // "kong",  # 10 - Kong
    HHITEM_RAINBOWCOIN, // "rainbow",  # 11 - Rainbow Coin
    HHITEM_COMPANYCOIN, // "nintendo",  # 12 - Nintendo Coin
    HHITEM_NOTHING, // "melon",  # 13 - Melon
};

static short banned_hh_items[] = {HHITEM_NOTHING, HHITEM_GB};
static short flags_produce_overlay[] = {
    FLAG_ABILITY_CLIMBING,
    FLAG_TBARREL_BARREL,
    FLAG_TBARREL_DIVE,
    FLAG_TBARREL_ORANGE,
    FLAG_TBARREL_VINE,
    FLAG_COLLECTABLE_BEAN,
    FLAG_ABILITY_CAMERA,
    FLAG_ABILITY_SHOCKWAVE,
};

void* checkMove(short* flag, void* fba, int source, int vanilla_flag) {
    /**
     * @brief Check whether a flag is a move, alter the flag block address, and perform any additional functions required.
     * 
     * @param flag Address which contains the flag index
     * @param fba Flag Block Address
     * @param source Whether this function is being called from a set flag call (1) or check flag call (0)
     * @param vanilla_flag The original vanilla flag
     * 
     * @return New flag block address
     */
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
                moveGiveHook(item_kong, item_type, item_index, vanilla_flag == FLAG_COLLECTABLE_RAREWARECOIN);
                
            }
            return temp_fba + item_type;
        }
    } else {
        int flag_index = *flag;
        int spawn_overlay = 0;
        PURCHASE_TYPES item_type = 0;
        int item_index = 0;
        int item_kong = 0;
        if ((source == 1) && (!checkFlagDuplicate(flag_index, FLAGTYPE_PERMANENT)) && (Gamemode == GAMEMODE_ADVENTURE)) {
            if ((flag_index >= FLAG_ITEM_SLAM_0) && (flag_index <= FLAG_ITEM_SLAM_2) ) {
                // Slam
                item_index = giveSlamLevel();
                spawn_overlay = 1;
                item_type = PURCHASE_SLAM;
            } else if ((flag_index == FLAG_ITEM_BELT_0) || (flag_index == FLAG_ITEM_BELT_1)) {
                // Belt
                MovesBase[0].ammo_belt += 1;
                item_index = MovesBase[0].ammo_belt;
                for (int i = 1; i < 5; i++) {
                    MovesBase[i].ammo_belt = item_index;
                }
                CollectableBase.StandardAmmo = 50 * (1 << item_index);
                spawn_overlay = 1;
                item_type = PURCHASE_AMMOBELT;
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
                item_type = PURCHASE_INSTRUMENT;
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
            } else {
                int is_shopkeeper = isFlagInRange(flag_index, FLAG_ITEM_CRANKY, 4);
                int is_hint = isFlagInRange(flag_index, FLAG_WRINKLYVIEWED, 35) && Rando.hints_are_items == 1;
                int is_kong = inShortList(flag_index, (short*)&kong_flags, sizeof(kong_flags) >> 1);
                int is_special_flag = inShortList(flag_index, &flags_produce_overlay, sizeof(flags_produce_overlay) >> 1);
                if ((is_shopkeeper) || (is_hint) || (is_kong) || (is_special_flag)) {
                    spawn_overlay = 1;
                    item_type = PURCHASE_FLAG;
                    item_index = flag_index;
                }
                if (flag_index == FLAG_TBARREL_VINE) {
                    refreshPads(ITEMREFRESH_VINE);
                } else if (flag_index == FLAG_ABILITY_CAMERA) {
                    if (CollectableBase.Film < 10) {
                        CollectableBase.Film = 10;
                    }
                } else if (flag_index == FLAG_ABILITY_SHOCKWAVE) {
                    if (CollectableBase.Crystals < (10*150)) {
                        CollectableBase.Crystals = 10*150;
                    }
                }
            }
            // Jetpac/Arcade GB Give
            int give_gb = 0;
            int give_rainbow = 0;
            int give_health = 0;
            if (vanilla_flag == FLAG_COLLECTABLE_NINTENDOCOIN) {
                if (Rando.arcade_reward < sizeof(arcade_hh_bonus)) {
                    helm_hurry_items hh_bonus = arcade_hh_bonus[(int)Rando.arcade_reward];
                    if (!inShortList(hh_bonus, &banned_hh_items[0], 2)) {
                        addHelmTime(hh_bonus, 1);
                    }
                }
                switch (Rando.arcade_reward) {
                    case 5:
                        give_gb = 1;
                        break;
                    case 6:
                        auto_turn_keys();
                        displayKeyText(flag_index);
                        return fba;
                    case 20:
                        give_rainbow = 1;
                        break;
                    case 22:
                        give_health = 1;
                        break;
                }
            } else if (vanilla_flag == FLAG_COLLECTABLE_RAREWARECOIN) {
                if (Rando.jetpac_reward < sizeof(jetpac_hh_bonus)) {
                    helm_hurry_items hh_bonus = jetpac_hh_bonus[(int)Rando.jetpac_reward];
                    if (!inShortList(hh_bonus, &banned_hh_items[0], 2)) {
                        addHelmTime(hh_bonus, 1);
                    }
                }
                switch (Rando.jetpac_reward) {
                    case 5:
                        give_gb = 1;
                        break;
                    case 6:
                        auto_turn_keys();
                        displayKeyText(flag_index);
                        return fba;
                    case 11:
                        give_rainbow = 1;
                        break;
                    case 13:
                        give_health = 1;
                        break;
                }
            }
            if (!checkFlag(vanilla_flag, FLAGTYPE_PERMANENT)) {
                if (give_gb) {
                    int world = getWorld(CurrentMap, 1);
                    if (world < 9) {
                        giveGB(Character, world);
                    }
                } else if (give_rainbow) {
                    giveRainbowCoin();
                } else if (give_health) {
                    giveMelon();
                }
            }
            if (spawn_overlay) {
                spawnItemOverlay(item_type, item_kong, item_index, vanilla_flag == FLAG_COLLECTABLE_RAREWARECOIN);
            }
        }
    }
    return fba;
}

void getFLUTSize(void) {
    /**
     * @brief Determine amount of flags in the FLUT
     */
    for (int i = 0; i < 0xD00; i++) {
        if (ItemRando_FLUT[2 * i] == -1) {
            flut_size = i;
            return;
        }
    }
}

int binarySearch(int search_item, int low, int high) {
    /**
     * @brief Perform the binary search algorithm on the FLUT
     * 
     * @param search_item The flag being searched for
     * @param low Lower bound of the search
     * @param high Higher bound of the search
     * 
     * @return Index in the FLUT of the flag
     */
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
    /**
     * @brief Search for flag in the FLUT, determining whether to use the FLUT or a binary search algorithm
     * 
     * @param old_flag Flag being searched for
     * @param flag_write Address which contains where the flag is being written to
     * @param source Whether this function is being called from a set flag call (1) or check flag call (0)
     * @param fba Flag Block Address
     * 
     * @return New Flag Block Address
     */
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

void* updateFlag(flagtypes type, short* flag, void* fba, int source) {
    /**
     * @brief Container function for updating the flag from a set/check flag call to reference the FLUT
     * 
     * @param type Flag Type (0 = Permanent, 1 = Global, 2 = Temporary)
     * @param flag Address which contains the flag index
     * @param fba Flag Block Address
     * @param source Whether this function is being called from a set flag call (1) or check flag call (0)
     */
    if ((Rando.item_rando) && (type == FLAGTYPE_PERMANENT) && (*flag != 0)) {
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
    /**
     * @brief Get kong index from a bonus table entry
     * 
     * @param flag Flag index associated with the bonus table entry
     * 
     * @return kong index
     */
    if ((Rando.any_kong_items.major_items) == 0) {
        for (int i = 0; i < BONUS_DATA_COUNT; i++) {
            if (bonus_data[i].flag == flag) {
                return bonus_data[i].kong_actor;
            }
        }
    }
    return 0;
}