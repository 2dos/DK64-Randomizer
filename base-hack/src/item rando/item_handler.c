/**
 * @file item_handler.c
 * @author Ballaam
 * @brief All code pertaining to giving items
 * @version 0.1
 * @date 2025-04-06
 * 
 * @copyright Copyright (c) 2025
 * 
 */

#include "../../include/common.h"

static CountStruct current_item_data;
static const MoveSpecialBijectionStruct move_flag_bijection[] = {
    {.flag = FLAG_TBARREL_DIVE, .move_enum = MOVE_SPECIAL_DIVING},
    {.flag = FLAG_TBARREL_ORANGE, .move_enum = MOVE_SPECIAL_ORANGES},
    {.flag = FLAG_TBARREL_BARREL, .move_enum = MOVE_SPECIAL_BARRELS},
    {.flag = FLAG_TBARREL_VINE, .move_enum = MOVE_SPECIAL_VINES},
    {.flag = FLAG_ABILITY_CAMERA, .move_enum = MOVE_SPECIAL_CAMERA},
    {.flag = FLAG_ABILITY_SHOCKWAVE, .move_enum = MOVE_SPECIAL_SHOCKWAVE},
};

typedef struct pad_refresh_calls {
    unsigned char level;
    unsigned char kong;
    unsigned char signal;
    unsigned char pad;
} pad_refresh_calls;

static const pad_refresh_calls call_checks_pad_refresh[] = {
    {.level = 0,    .kong = KONG_DK,                .signal = ITEMREFRESH_BLAST},
    {.level = 2,    .kong = KONG_DIDDY,             .signal = ITEMREFRESH_SPRING},
    {.level = 1,    .kong = KONG_LANKY,             .signal = ITEMREFRESH_BALLOON},
    {.level = 2,    .kong = KONG_TINY,              .signal = ITEMREFRESH_MONKEYPORT},
    {.level = 2,    .kong = KONG_CHUNKY,            .signal = ITEMREFRESH_GONE},
	{.level = 10,   .kong = MOVE_SPECIAL_VINES,     .signal = ITEMREFRESH_VINE},
};

void giveItem(requirement_item item, int level, int kong, giveItemConfig config) {
    // Gives an item determined by the id. Use level & kong if necessary
    helm_hurry_items hh_item = HHITEM_NOTHING;
    int display_text = 0;
    switch(item) {
        case REQITEM_KONG:
            current_item_data.kong_bitfield |= (1 << kong);
            hh_item = HHITEM_KONG;
            display_text = 1;
            break;
        case REQITEM_GOLDENBANANA:
            giveGB();
            break;
        case REQITEM_BLUEPRINT:
            current_item_data.bp_count[kong]++;
            hh_item = HHITEM_BLUEPRINT;
            break;
        case REQITEM_FAIRY:
            current_item_data.fairies++;
            hh_item = HHITEM_FAIRY;
            break;
        case REQITEM_KEY:
            current_item_data.key_bitfield |= (1 << level);
            hh_item = HHITEM_KEY;
            display_text = 1;
            break;
        case REQITEM_CROWN:
            current_item_data.crowns++;
            hh_item = HHITEM_CROWN;
            break;
        case REQITEM_COMPANYCOIN:
            if (kong == 0) {
                // nintendo coin
                current_item_data.special_items.nintendo_coin = 1;
            } else {
                // rareware coin
                current_item_data.special_items.rareware_coin = 1;
            }
            hh_item = HHITEM_COMPANYCOIN;
            break;
        case REQITEM_MEDAL:
            current_item_data.medals++;
            hh_item = HHITEM_MEDAL;
            break;
        case REQITEM_BEAN:
            current_item_data.special_items.bean = 1;
            hh_item = HHITEM_BEAN;
            display_text = 1;
            break;
        case REQITEM_PEARL:
            current_item_data.pearls++;
            hh_item = HHITEM_PEARL;
            break;
        case REQITEM_RAINBOWCOIN:
            current_item_data.rainbow_coins++;
            hh_item = HHITEM_RAINBOWCOIN;
            if (config.give_coins) {
                for (int i = 0; i < 5; i++) {
                    MovesBase[i].coins += 5;
                }
            }
            break;
        case REQITEM_ICETRAP:
            current_item_data.ice_traps++;
            hh_item = HHITEM_FAKEITEM;
            if (config.apply_ice_trap && kong) {
                queueIceTrap(kong, 1);
            }
            break;
        case REQITEM_JUNK:
            current_item_data.junk_items++;
            break;
        case REQITEM_HINT:
            current_item_data.hint_bitfield[kong] |= (1 << level);
            display_text = 1;
            break;
        case REQITEM_SHOPKEEPER:
            setPermFlag(FLAG_ITEM_CRANKY + kong);
            hh_item = HHITEM_KONG;
            display_text = 1;
            break;
        case REQITEM_RACECOIN:
            current_item_data.race_coins++;
            RaceCoinCount = current_item_data.race_coins;
            break;
        case REQITEM_MOVE:
            if ((level >= 0) && (level < 3)) {
                // Special Moves
                MovesBase[kong].special_moves |= (1 << level);
            } else if (level == 3) {
                // Slam
                giveSlamLevel();
            } else if (level == 4) {
                // Gun
                MovesBase[kong].weapon_bitfield |= 1;
            } else if ((level == 5) || (level == 6)) {
                // Homing/Sniper
                for (int i = 0; i < 5; i++) {
                    MovesBase[i].weapon_bitfield |= (1 << (level - 4));
                }
            } else if (level == 7) {
                // Ammo Belt
                int base = MovesBase[0].ammo_belt;
                for (int i = 0; i < 5; i++) {
                    MovesBase[i].ammo_belt = base + 1;
                }
                CollectableBase.StandardAmmo = 50 << (base + 1);
            } else if (level == 8) {
                // Instrument
                MovesBase[kong].instrument_bitfield |= 1;
                if (CollectableBase.Melons < 2) {
                    CollectableBase.Melons = 2;
                }
            } else if (level == 9) {
                // Progressive instrument
                int ins_level = getInstrumentLevel();
                for (int i = 0; i < 5; i++) {
                    MovesBase[i].instrument_bitfield |= (1 << (ins_level + 1));
                }
                int cap = 2;
                if (MovesBase[0].instrument_bitfield & 4) {
                    cap = 3;
                }
                if (CollectableBase.Melons < cap) {
                    CollectableBase.Melons = cap;
                }
            } else if (level == 10) {
                int base = *(unsigned char*)(&current_item_data.flag_moves);
                *(unsigned char*)(&current_item_data.flag_moves) = base | (0x80 >> kong);
            } else if (level == 11) {
                setPermFlag(FLAG_ABILITY_CLIMBING);
            } else if (level == 12) {
                current_item_data.flag_moves.camera = 1;
                current_item_data.flag_moves.shockwave = 1;
            }
            hh_item = HHITEM_MOVE;
            display_text = 1;
            for (int i = 0; i < 6; i++) {
                if (level == call_checks_pad_refresh[i].level) {
                    if (kong == call_checks_pad_refresh[i].kong) {
                        refreshPads(call_checks_pad_refresh[i].signal);
                    }
                }
            }
            break;
    }
    checkSeedVictory();
    if (config.apply_helm_hurry) {
        addHelmTime(hh_item, 1);
    }
    if ((config.display_item_text && display_text) || (config.force_display_item_text)) {
        spawnItemOverlay(item, level, kong, 0);
    }
}

void giveItemFromPacket(item_packet *packet, int force_text) {
    giveItemConfig cfg = {.display_item_text = 1, .apply_helm_hurry = 1, .give_coins = 1, .apply_ice_trap = 1};
    if (force_text) {
        cfg.force_display_item_text = 1;
    }
    giveItem(packet->item_type, packet->level, packet->kong, cfg);
}

int getItemCount_new(requirement_item item, int level, int kong) {
    /*
        Get the item count, if necessary provide the level and kong
        For bitfield items, set the level and kong to -1 to get the count for that specific parameter
    */
   
    int count = 0;
    unsigned char *bitfield_series = 0;
    int bitfield_value = -1;
    int iterator = 0;
    switch(item) {
        case REQITEM_KONG:
            bitfield_value = current_item_data.kong_bitfield;
            iterator = kong;
        case REQITEM_KEY:
            if (bitfield_value == -1) {
                bitfield_value = current_item_data.key_bitfield;
                iterator = level;
            }
            {
                for (int i = 0; i < 8; i++) {
                    int has_item = (bitfield_value >> i) & 1;
                    if (iterator == i) {
                        return has_item;
                    }
                    if (has_item) {
                        count++;
                    }
                }
            }
            return count;
        case REQITEM_HINT:
            if (!bitfield_series) {
                bitfield_series = &current_item_data.hint_bitfield;
            }
            {
                if ((level >= 0) && (kong >= 0)) {
                    return (bitfield_series[kong] >> level) & 1;
                } else if (level >= 0) {
                    for (int i = 0; i < 5; i++) {
                        if ((bitfield_series[i] >> level) & 1) {
                            count++;
                        }
                    }
                } else if (kong >= 0) {
                    for (int i = 0; i < 8; i++) {
                        if ((bitfield_series[kong] >> i) & 1) {
                            count++;
                        }
                    }
                } else {
                    for (int i = 0; i < 8; i++) {
                        for (int j = 0; j < 5; j++) {
                            if ((bitfield_series[j] >> i) & 1) {
                                count++;
                            }
                        }
                    }
                }
                return count;
            }
            break;
        case REQITEM_BLUEPRINT:
            for (int i = 0; i < 5; i++) {
                if ((kong == i) || (kong == -1)) {
                    count += current_item_data.bp_count[i];
                }
            }
            return count;
        case REQITEM_FAIRY:
            return current_item_data.fairies;
        case REQITEM_CROWN:
            return current_item_data.crowns;
        case REQITEM_COMPANYCOIN:
            if (kong != 1) {
                // Get Nintendo Coin
                if (current_item_data.special_items.nintendo_coin) {
                    count++;
                }
            }
            if (kong != 0) {
                // Get Rareware Coin
                if (current_item_data.special_items.rareware_coin) {
                    count++;
                }
            }
            return count;
        case REQITEM_MEDAL:
            return current_item_data.medals;
        case REQITEM_BEAN:
            if (current_item_data.special_items.bean) {
                return 1;
            }
            return 0;
        case REQITEM_PEARL:
            return current_item_data.pearls;
        case REQITEM_RAINBOWCOIN:
            return current_item_data.rainbow_coins;
        case REQITEM_ICETRAP:
            return current_item_data.ice_traps;
        case REQITEM_JUNK:
            return current_item_data.junk_items;
        case REQITEM_RACECOIN:
            return current_item_data.race_coins;
        case REQITEM_SHOPKEEPER:
            return checkFlag(FLAG_ITEM_CRANKY + kong, FLAGTYPE_PERMANENT);
        case REQITEM_MOVE:
            if ((level >= 0) && (level < 3)) {
                // Special Moves
                return (MovesBase[kong].special_moves >> level) & 1;
            } else if (level == 3) {
                // Slam
                return MovesBase[0].simian_slam;
            } else if (level == 4) {
                // Gun
                return MovesBase[kong].weapon_bitfield & 1;
            } else if ((level == 5) || (level == 6)) {
                // Homing/Sniper
                return (MovesBase[0].weapon_bitfield >> (level - 4)) & 1;
            } else if (level == 7) {
                // Ammo Belt
                return MovesBase[0].ammo_belt;
            } else if (level == 8) {
                // Instrument
                return MovesBase[kong].instrument_bitfield & 1;
            } else if (level == 9) {
                // Progressive instrument
                return getInstrumentLevel();
            } else if (level == 10) {
                int value = *(unsigned char*)(&current_item_data.flag_moves);
                if (value & (0x80 >> kong)) {
                    return 1;
                }
                return 0;
            } else if (level == 11) {
                return checkFlag(FLAG_ABILITY_CLIMBING, FLAGTYPE_PERMANENT);
            } else if (level == 12) {
                return current_item_data.flag_moves.camera && current_item_data.flag_moves.shockwave;
            }
            break;
    }
    return 0;
}

int getKongOwnershipFromFlag(int flag) {
    // TODO: I don't like this, I'd like to remove this function if possible
    for (int i = 0; i < 5; i++) {
        if (flag == kong_flags[i]) {
            return getItemCount_new(REQITEM_KONG, 0, i);
        }
    }
    return 0;
}

void giveKongFromFlag(int flag) {
    for (int i = 0; i < 5; i++) {
        if (flag == kong_flags[i]) {
            giveItem(REQITEM_KONG, 0, i, (giveItemConfig){.display_item_text = 0});
        }
    }
}

int hasFlagMove(int flag) {
    for (int i = 0; i < 6; i++) {
        if (move_flag_bijection[i].flag == flag) {
            int shift = 0x80 >> move_flag_bijection[i].move_enum;
            return (*(unsigned char*)(&current_item_data.flag_moves) & shift) != 0;
        }
    }
    return checkFlag(flag, FLAGTYPE_PERMANENT);
}

void setFlagMove(int flag) {
    for (int i = 0; i < 6; i++) {
        if (move_flag_bijection[i].flag == flag) {
            int shift = 0x80 >> move_flag_bijection[i].move_enum;
            *(unsigned char*)(&current_item_data.flag_moves) = *(unsigned char*)(&current_item_data.flag_moves) | shift;
            return;
        }
    }
    setPermFlag(flag);
}

int getShopFlag(vendors vendor, int level, int kong) {
    if (vendor == SHOP_CRANKY) {
        return FLAG_SHOPFLAG + (level * 5) + kong;
    } else if ((vendor == SHOP_FUNKY) && (level < 7)) {
        return FLAG_SHOPFLAG + ((level + 8) * 5) + kong;
    } else if (vendor == SHOP_CANDY) {
        if ((level >= LEVEL_AZTEC) && (level <= LEVEL_GALLEON)) {
            int candy_offset = level - LEVEL_AZTEC;
            return FLAG_SHOPFLAG + ((candy_offset + 15) * 5) + kong;
        } else if ((level >= LEVEL_CAVES) && (level <= LEVEL_CASTLE)) {
            int candy_offset = level - LEVEL_CAVES;
            return FLAG_SHOPFLAG + ((candy_offset + 18) * 5) + kong;
        }
    }
    return 0;
}

static unsigned char FileInfoData[] = {
    2, // Melon Count
    1, // File Populated
    0x16, // IGT
    2, // File Index
    0x18, // Save Count
    8, // DK BP
    8, // Diddy BP
    8, // Lanky BP
    8, // Tiny BP
    8, // Chunky BP
    8, // DK Hints
    8, // Diddy Hints
    8, // Lanky Hints
    8, // Tiny Hints
    8, // Chunky Hints
    8, // Keys
    8, // Kongs
    8, // Crown Count
    8, // Special Items
    8, // Medals
    8, // Pearls
    8, // Fairies
    8, // Rainbow Coins
    16, // Ice Traps
    16, // Junk Items
    16, // Race Coins
    8, // Special Moves
    8, // DK BP Turn-In
    8, // Diddy BP Turn-In
    8, // Lanky BP Turn-In
    8, // Tiny BP Turn-In
    8, // Chunky BP Turn-In
    16, // AP Item Count
    22, // IGT Japes
    22, // IGT Aztec
    22, // IGT Factory
    22, // IGT Galleon
    22, // IGT Fungi
    22, // IGT Caves
    22, // IGT Castle
    22, // IGT Helm
    22, // IGT Isles
    22, // IGT DK
    22, // IGT Diddy
    22, // IGT Lanky
    22, // IGT Tiny
    22, // IGT Chunky
    22, // Hurry IGT
    16, // Tags
    12, // Photos
    16, // Kills
    12, // Kaught
    12, // Deaths
    12, // Trapped
};

short file_info_expansion = FILE_INFO_SIZE;

void GrabFileParameters_FileInfo(int index, int level, short *file_base, unsigned char *bit_size) {
    int offset = *(short*)(0x807ECEA0) + file_info_expansion;
    *file_base += offset;
    *bit_size = 0;
    for (int i = 12; i <= index; i++) {
        *file_base += *bit_size;
        *bit_size = FileInfoData[i - 12];
    }
}

void initItemRandoPointer(void) {
    ItemInventory = &current_item_data;
}

void readItemsFromFile(void) {
    wipeTurnedInArray();
    for (int i = 0; i < 5; i++) {
        current_item_data.bp_count[i] = ReadFile(DATA_DKBP + i, 0, 0, FileIndex);
        current_item_data.turned_in_bp_count[i] = ReadFile(DATA_DKBPTURNIN + i, 0, 0, FileIndex);
        current_item_data.hint_bitfield[i] = ReadFile(DATA_DKHINTS + i, 0, 0, FileIndex);
    }
    current_item_data.key_bitfield = ReadFile(DATA_KEYS, 0, 0, FileIndex);
    current_item_data.kong_bitfield = ReadFile(DATA_KONGS, 0, 0, FileIndex);
    current_item_data.crowns = ReadFile(DATA_CROWNS, 0, 0, FileIndex);
    *(unsigned char*)(&current_item_data.special_items) = ReadFile(DATA_SPECIALITEMS, 0, 0, FileIndex);
    current_item_data.medals = ReadFile(DATA_MEDALS, 0, 0, FileIndex);
    current_item_data.pearls = ReadFile(DATA_PEARLS, 0, 0, FileIndex);
    current_item_data.fairies = ReadFile(DATA_FAIRIES, 0, 0, FileIndex);
    current_item_data.rainbow_coins = ReadFile(DATA_RAINBOWCOINS, 0, 0, FileIndex);
    current_item_data.ice_traps = ReadFile(DATA_ICETRAPS, 0, 0, FileIndex);
    current_item_data.junk_items = ReadFile(DATA_JUNKITEMS, 0, 0, FileIndex);
    current_item_data.race_coins = ReadFile(DATA_RACECOINS, 0, 0, FileIndex);
    *(unsigned char*)(&current_item_data.flag_moves) = ReadFile(DATA_SPECIALMOVES, 0, 0, FileIndex);
    for (int i = 0; i < STAT_TERMINATOR; i++) {
        GameStats[i] = ReadFile(DATA_STAT_TAG + i, 0, 0, FileIndex);
    }
}

void saveItemsToFile(void) {
    for (int i = 0; i < 5; i++) {
        SaveToFile(DATA_DKBP + i, 0, 0, FileIndex, current_item_data.bp_count[i]);
        SaveToFile(DATA_DKBPTURNIN + i, 0, 0, FileIndex, current_item_data.turned_in_bp_count[i]);
        SaveToFile(DATA_DKHINTS + i, 0, 0, FileIndex, current_item_data.hint_bitfield[i]);
    }
    SaveToFile(DATA_KEYS, 0, 0, FileIndex, current_item_data.key_bitfield);
    SaveToFile(DATA_KONGS, 0, 0, FileIndex, current_item_data.kong_bitfield);
    SaveToFile(DATA_CROWNS, 0, 0, FileIndex, current_item_data.crowns);
    SaveToFile(DATA_SPECIALITEMS, 0, 0, FileIndex, *(unsigned char*)(&current_item_data.special_items));
    SaveToFile(DATA_MEDALS, 0, 0, FileIndex, current_item_data.medals);
    SaveToFile(DATA_PEARLS, 0, 0, FileIndex, current_item_data.pearls);
    SaveToFile(DATA_FAIRIES, 0, 0, FileIndex, current_item_data.fairies);
    SaveToFile(DATA_RAINBOWCOINS, 0, 0, FileIndex, current_item_data.rainbow_coins);
    SaveToFile(DATA_ICETRAPS, 0, 0, FileIndex, current_item_data.ice_traps);
    SaveToFile(DATA_JUNKITEMS, 0, 0, FileIndex, current_item_data.junk_items);
    SaveToFile(DATA_RACECOINS, 0, 0, FileIndex, current_item_data.race_coins);
    SaveToFile(DATA_SPECIALMOVES, 0, 0, FileIndex, *(unsigned char*)(&current_item_data.flag_moves));
    for (int i = 0; i < STAT_TERMINATOR; i++) {
        SaveToFile(DATA_STAT_TAG + i, 0, 0, FileIndex, GameStats[i]);
    }
}