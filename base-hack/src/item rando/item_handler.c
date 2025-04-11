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

typedef struct CountSpecialStruct {
    unsigned char nintendo_coin : 1; // 0x80
    unsigned char rareware_coin : 1; // 0x40
    unsigned char bean : 1; // 0x20
    unsigned char unk3 : 1;
    unsigned char unk4 : 1;
    unsigned char unk5 : 1;
    unsigned char unk6 : 1;
    unsigned char unk7 : 1;
} CountSpecialStruct;

typedef enum MoveSpecialEnum {
    MOVE_SPECIAL_DIVING,
    MOVE_SPECIAL_ORANGES,
    MOVE_SPECIAL_BARRELS,
    MOVE_SPECIAL_VINES,
    MOVE_SPECIAL_CAMERA,
    MOVE_SPECIAL_SHOCKWAVE,
} MoveSpecialEnum;

typedef struct MoveSpecialStruct {
    unsigned char diving : 1;
    unsigned char oranges : 1;
    unsigned char barrels : 1;
    unsigned char vines : 1;
    unsigned char camera : 1;
    unsigned char shockwave : 1;
    unsigned char unk6 : 1;
    unsigned char unk7 : 1;
} MoveSpecialStruct;

typedef struct CountStruct {
    /* 0x000 */ unsigned char bp_bitfield[5];
    /* 0x005 */ unsigned char hint_bitfield[5];
    /* 0x00A */ unsigned char key_bitfield;
    /* 0x00B */ unsigned char kong_bitfield;
    /* 0x00C */ unsigned char crowns;
    /* 0x00D */ CountSpecialStruct special_items;
    /* 0x00E */ unsigned char medals;
    /* 0x00F */ unsigned char pearls;
    /* 0x010 */ unsigned char fairies;
    /* 0x011 */ unsigned char rainbow_coins;
    /* 0x012 */ short ice_traps;
    /* 0x014 */ short junk_items;
    /* 0x016 */ MoveSpecialStruct flag_moves;
} CountStruct;

typedef struct MoveSpecialBijectionStruct {
    unsigned short flag;
    unsigned short move_enum;
} MoveSpecialBijectionStruct;

static CountStruct current_item_data;
static const MoveSpecialBijectionStruct move_flag_bijection[] = {
    {.flag = FLAG_TBARREL_DIVE, .move_enum = MOVE_SPECIAL_DIVING},
    {.flag = FLAG_TBARREL_ORANGE, .move_enum = MOVE_SPECIAL_ORANGES},
    {.flag = FLAG_TBARREL_BARREL, .move_enum = MOVE_SPECIAL_BARRELS},
    {.flag = FLAG_TBARREL_VINE, .move_enum = MOVE_SPECIAL_VINES},
    {.flag = FLAG_ABILITY_CAMERA, .move_enum = MOVE_SPECIAL_CAMERA},
    {.flag = FLAG_ABILITY_SHOCKWAVE, .move_enum = MOVE_SPECIAL_SHOCKWAVE},
};

void giveItem(requirement_item item, int level, int kong) {
    // Gives an item determined by the id. Use level & kong if necessary
    switch(item) {
        case REQITEM_KONG:
            current_item_data.kong_bitfield |= (1 << kong);
            break;
        case REQITEM_BLUEPRINT:
            current_item_data.bp_bitfield[kong] |= (1 << level);
            break;
        case REQITEM_FAIRY:
            current_item_data.fairies++;
            break;
        case REQITEM_KEY:
            current_item_data.key_bitfield |= (1 << level);
            break;
        case REQITEM_CROWN:
            current_item_data.crowns++;
            break;
        case REQITEM_COMPANYCOIN:
            if (kong == 0) {
                // nintendo coin
                current_item_data.special_items.nintendo_coin = 1;
            } else {
                // rareware coin
                current_item_data.special_items.rareware_coin = 1;
            }
            break;
        case REQITEM_MEDAL:
            current_item_data.medals++;
            break;
        case REQITEM_BEAN:
            current_item_data.special_items.bean = 1;
            break;
        case REQITEM_PEARL:
            current_item_data.pearls++;
            break;
        case REQITEM_RAINBOWCOIN:
            current_item_data.rainbow_coins++;
            break;
        case REQITEM_ICETRAP:
            current_item_data.ice_traps++;
            break;
        case REQITEM_JUNK:
            current_item_data.junk_items++;
            break;
        case REQITEM_HINT:
            current_item_data.hint_bitfield[kong] |= (1 << level);
            break;
        case REQITEM_MOVE:
            // TODO: Move logic here
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
                // Sniper
                for (int i = 0; i < 5; i++) {
                    MovesBase[i].weapon_bitfield |= (1 << (level - 4));
                }
            } else if (level == 7) {
                // Ammo Belt
                int base = MovesBase[0].ammo_belt;
                for (int i = 0; i < 5; i++) {
                    MovesBase[i].ammo_belt = base + 1;
                }
            } else if (level == 8) {
                // Instrument
                MovesBase[kong].instrument_bitfield |= 1;
                if (CollectableBase.Melons < 2) {
                    CollectableBase.Melons = 2;
                }
            } else if (level == 9) {
                // Progressive instrument
                int base = 2;
                int base_btf = MovesBase[0].instrument_bitfield;
                if (base_btf | 2) {
                    base = 4;
                    if (base_btf | 4) {
                        base = 8;
                    }
                }
                for (int i = 0; i < 5; i++) {
                    MovesBase[i].instrument_bitfield |= base;
                }
                if (base >= 4) {
                    if (CollectableBase.Melons < 3) {
                        CollectableBase.Melons = 3;
                    }
                }
            } else if (level == 10) {
                int base = *(unsigned char*)(&current_item_data.flag_moves);
                *(unsigned char*)(&current_item_data.flag_moves) = base | (0x80 >> kong);
            } else if (level == 11) {
                setPermFlag(FLAG_ABILITY_CLIMBING);
            }
            break;
    }
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
                    int has_item = (bitfield_value >> iterator) & 1;
                    if (iterator == i) {
                        return has_item;
                    }
                    if (has_item) {
                        count++;
                    }
                }
            }
            return count;
        case REQITEM_BLUEPRINT:
            bitfield_series = &current_item_data.bp_bitfield;
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