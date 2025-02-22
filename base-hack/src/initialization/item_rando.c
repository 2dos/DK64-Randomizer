/**
 * @file item_rando.c
 * @author Ballaam
 * @brief Initializes all item rando elements
 * @version 0.1
 * @date 2023-01-17
 * 
 * @copyright Copyright (c) 2023
 * 
 */
#include "../../include/common.h"

typedef struct reward_rom_struct {
	/* 0x000 */ short flag;
	/* 0x002 */ unsigned short actor;
} reward_rom_struct;

typedef struct patch_db_item {
	/* 0x000 */ short id;
	/* 0x002 */ unsigned char map;
	/* 0x003 */ unsigned char world;
} patch_db_item;

typedef struct meloncrate_db_item {
    /* 0x000 */ short id;
    /* 0x002 */ unsigned char map;
    /* 0x003 */ unsigned char world;
} meloncrate_db_item;

static unsigned short bp_item_table[40] = {}; // Kasplat Rewards
static unsigned char medal_item_table[45] = {}; // Medal Rewards
static unsigned char wrinkly_item_table[35] = {}; // Wrinkly Rewards
static unsigned short crown_item_table[10] = {}; // Crown Rewards
static unsigned short key_item_table[8] = {}; // Boss Rewards
static short fairy_item_table[20] = {}; // Fairy Rewards
static unsigned short rcoin_item_table[16] = {}; // Dirt Patch Rewards
static unsigned short crate_item_table[16] = {}; // Crate Rewards
static patch_db_item patch_flags[16] = {}; // Flag table for dirt patches to differentiate it from balloons
bonus_barrel_info bonus_data[BONUS_DATA_COUNT] = {}; // Bonus Barrel Rewards
static meloncrate_db_item crate_flags[16] = {}; // Melon crate table

int getBPItem(int index) {
    /**
     * @brief Get Blueprint item from kasplat index
     * 
     * @param index Kasplat Index: (5 * level) + kong
     * 
     * @return Actor Index of the reward
     */
	return getActorIndex(bp_item_table[index]);
}

int getMedalItem(int index) {
    /**
     * @brief Get Medal item from medal index
     * 
     * @param index Medal Index: (5 * level) + kong
     * 
     * @return Medal Item Index of the reward
     */
	return medal_item_table[index];
}

int getWrinklyItem(int index) {
    /**
     * @brief Get Wrinkly Door item from medal index
     * 
     * @param index Medal Index: (5 * level) + kong
     * 
     * @return Medal Item Index of the reward
     */
	return wrinkly_item_table[index];
}

int getCrownItem(maps map) {
    /**
     * @brief Get Crown item from map index
     * 
     * @param map Map Index
     * 
     * @return Actor Index of the reward
     */
	for (int i = 0; i < 10; i++) {
		if (map == crown_maps[i]) {
			return getActorIndex(crown_item_table[i]);
		}
	}
	return 0;
}

int getKeyItem(int old_flag) {
    /**
     * @brief Get Boss Reward from the original flag
     * 
     * @param old_flag Original Flag of the reward
     * 
     * @return Actor Index of the reward
     */
	for (int i = 0; i < 8; i++) {
		if (old_flag == normal_key_flags[i]) {
			return getActorIndex(key_item_table[i]);
		}
	}
	return 0;
}

int getFairyModel(int flag) {
    /**
     * @brief Get Fairy Reward from the flag
     * 
     * @param flag Flag Index of the fairy
     * 
     * @return Model Index of the reward
     */
	if ((flag >= 589) && (flag <= 608)) {
		return fairy_item_table[flag - 589];
	}
	return 0x3D;
}

int getRainbowCoinItem(int old_flag) {
	/**
	 * @brief Get Dirt Patch reward from the old flag
     * 
     * @param old_flag Original flag of the dirt patch
	 * 
     * @return Actor Index of the reward
	 */
	return getActorIndex(rcoin_item_table[old_flag - FLAG_RAINBOWCOIN_0]);
}

int getCrateItem(int old_flag) {
	/**
	 * @brief Get Crate reward from the old flag
     * 
     * @param old_flag Original flag of the crate
	 * 
     * @return Actor Index of the reward
	 */
	return getActorIndex(crate_item_table[old_flag - FLAG_MELONCRATE_0]);
}

int getPatchFlag(int id) {
    /**
     * @brief Get Patch flag from the ID of the patch
     * 
     * @param id Patch ID inside the map
     * 
     * @return flag index of the patch
     */
	for (int i = 0; i < 16; i++) {
		if (CurrentMap == patch_flags[i].map) {
			if (id == patch_flags[i].id) {
				return FLAG_RAINBOWCOIN_0 + i;
			}
		}
	}
	return 0;
}

int getPatchWorld(int index) {
    /**
     * @brief Gets the world which the patch is in
     * 
     * @param index Patch Index inside the flag table
     * 
     * @return World index of the patch
     */
	return patch_flags[index].world;
}

int getCrateFlag(int id) {
    /**
     * @brief Get Melon Crate flag from the ID of the Melon Crate
     * 
     * @param id Melon Crate ID inside the map
     * 
     * @return flag index of the crate
     */
	for (int i = 0; i < 16; i++) {
		if (CurrentMap == crate_flags[i].map) {
			if (id == crate_flags[i].id) {
				return FLAG_MELONCRATE_0 + i;
			}
		}
	}
	return 0;
}

int getCrateWorld(int index) {
    /**
     * @brief Gets the world which the melon crate is in
     * 
     * @param index Crate Index inside the flag table
     * 
     * @return World index of the crate
     */
	return crate_flags[index].world;
}

void populatePatchItem(int id, int map, int index, int world) {
    /**
     * @brief Populate the patch table with a dirt patch
     * 
     * @param id Patch ID
     * @param map Patch Map
     * @param index Index inside the patch table
     * @param world World where the patch is
     */
    patch_flags[index].id = id;
    patch_flags[index].map = map;
    patch_flags[index].world = world;
}

void populateCrateItem(int id, int map, int index, int world) {
    /**
     * @brief Populate the Crate table with a Melon Crate
     * 
     * @param id Crate ID
     * @param map Crate Map
     * @param index Index inside the Crate table
     * @param world World where the Crate is
     */
    crate_flags[index].id = id;
    crate_flags[index].map = map;
    crate_flags[index].world = world;
}

int getBonusFlag(int index) {
    /**
     * @brief Get bonus barrel flag from barrel index
     * 
     * @param index Barrel Index
     * 
     * @return Flag index
     */
    if (index == 0) {
        return -1;
    }
    return bonus_data[index].flag;
}

typedef struct barrel_skin_tie {
    /* 0x000 */ unsigned short actor;
    /* 0x002 */ unsigned short skin;
} barrel_skin_tie;

static const barrel_skin_tie bonus_skins[] = {
    {.actor = 78, .skin=SKIN_BLUEPRINT},
    {.actor = 75, .skin=SKIN_BLUEPRINT},
    {.actor = 77, .skin=SKIN_BLUEPRINT},
    {.actor = 79, .skin=SKIN_BLUEPRINT},
    {.actor = 76, .skin=SKIN_BLUEPRINT},
    {.actor = CUSTOM_ACTORS_START + NEWACTOR_NINTENDOCOIN, .skin=SKIN_NINTENDO_COIN},
    {.actor = CUSTOM_ACTORS_START + NEWACTOR_RAREWARECOIN, .skin=SKIN_RAREWARE_COIN},
    {.actor = 72, .skin=SKIN_KEY},
    {.actor = 86, .skin=SKIN_CROWN},
    {.actor = CUSTOM_ACTORS_START + NEWACTOR_MEDAL, .skin=SKIN_MEDAL},
    {.actor = CUSTOM_ACTORS_START + NEWACTOR_POTIONDK, .skin=SKIN_POTION},
    {.actor = CUSTOM_ACTORS_START + NEWACTOR_POTIONDIDDY, .skin=SKIN_POTION},
    {.actor = CUSTOM_ACTORS_START + NEWACTOR_POTIONLANKY, .skin=SKIN_POTION},
    {.actor = CUSTOM_ACTORS_START + NEWACTOR_POTIONTINY, .skin=SKIN_POTION},
    {.actor = CUSTOM_ACTORS_START + NEWACTOR_POTIONCHUNKY, .skin=SKIN_POTION},
    {.actor = CUSTOM_ACTORS_START + NEWACTOR_POTIONANY, .skin=SKIN_POTION},
    {.actor = CUSTOM_ACTORS_START + NEWACTOR_KONGDK, .skin=SKIN_KONG_DK},
    {.actor = CUSTOM_ACTORS_START + NEWACTOR_KONGDIDDY, .skin=SKIN_KONG_DIDDY},
    {.actor = CUSTOM_ACTORS_START + NEWACTOR_KONGLANKY, .skin=SKIN_KONG_LANKY},
    {.actor = CUSTOM_ACTORS_START + NEWACTOR_KONGTINY, .skin=SKIN_KONG_TINY},
    {.actor = CUSTOM_ACTORS_START + NEWACTOR_KONGCHUNKY, .skin=SKIN_KONG_CHUNKY},
    {.actor = CUSTOM_ACTORS_START + NEWACTOR_BEAN, .skin=SKIN_BEAN},
    {.actor = CUSTOM_ACTORS_START + NEWACTOR_PEARL, .skin=SKIN_PEARL},
    {.actor = CUSTOM_ACTORS_START + NEWACTOR_FAIRY, .skin=SKIN_FAIRY},
    {.actor = 140, .skin=SKIN_RAINBOW_COIN},
    {.actor = CUSTOM_ACTORS_START + NEWACTOR_ICETRAPBUBBLE, .skin=SKIN_FAKE_ITEM},
    {.actor = 0x2F, .skin=SKIN_JUNK_ITEM},
    {.actor = CUSTOM_ACTORS_START + NEWACTOR_CRANKYITEM, .skin=SKIN_CRANKY},
    {.actor = CUSTOM_ACTORS_START + NEWACTOR_FUNKYITEM, .skin=SKIN_FUNKY},
    {.actor = CUSTOM_ACTORS_START + NEWACTOR_CANDYITEM, .skin=SKIN_CANDY},
    {.actor = CUSTOM_ACTORS_START + NEWACTOR_SNIDEITEM, .skin=SKIN_SNIDE},
    {.actor = CUSTOM_ACTORS_START + NEWACTOR_ICETRAPREVERSE, .skin=SKIN_FAKE_ITEM},
    {.actor = CUSTOM_ACTORS_START + NEWACTOR_ICETRAPSLOW, .skin=SKIN_FAKE_ITEM},
    {.actor = CUSTOM_ACTORS_START + NEWACTOR_HINTITEMDK, .skin=SKIN_HINT},
    {.actor = CUSTOM_ACTORS_START + NEWACTOR_HINTITEMDIDDY, .skin=SKIN_HINT},
    {.actor = CUSTOM_ACTORS_START + NEWACTOR_HINTITEMLANKY, .skin=SKIN_HINT},
    {.actor = CUSTOM_ACTORS_START + NEWACTOR_HINTITEMTINY, .skin=SKIN_HINT},
    {.actor = CUSTOM_ACTORS_START + NEWACTOR_HINTITEMCHUNKY, .skin=SKIN_HINT},
};

enum_bonus_skin getBarrelSkinIndex(int actor) {
    for (int i = 0; i < (sizeof(bonus_skins) / sizeof(barrel_skin_tie)); i++) {
        if (bonus_skins[i].actor == actor) {
            return bonus_skins[i].skin;
        }
    }
    return SKIN_GB;
}

int alterBonusVisuals(int index) {
    if (Rando.location_visuals.bonus_barrels) {
        if (index < BONUS_DATA_COUNT) {
            int actor = bonus_data[index].spawn_actor;
            enum_bonus_skin skin = getBarrelSkinIndex(actor);
            if (skin != SKIN_GB) {
                for (int i = 0; i < 2; i++) {
                    //retextureZone(CurrentActorPointer_0, i, skin);
                    blink(CurrentActorPointer_0, i, 1);
                    applyImageToActor(CurrentActorPointer_0, i, 0);
                    adjustColorPalette(CurrentActorPointer_0, i, skin, 0.0f);
                    unkPaletteFunc(CurrentActorPointer_0, i, 0);
                }
            }
        }
    }
    return getBonusFlag(index);
}

int getDirtPatchSkin(int flag, flagtypes flag_type) {
    int gone = checkFlag(flag, flag_type);
    if (gone) {
        return 1;
    }
    if (Rando.location_visuals.dirt_patches) {
        int index = flag - FLAG_RAINBOWCOIN_0;
        if (index < 16) {
            int actor = getRainbowCoinItem(flag);
            enum_bonus_skin skin = getBarrelSkinIndex(actor);
            blink(CurrentActorPointer_0, 0, 1);
            applyImageToActor(CurrentActorPointer_0, 0, 0);
            adjustColorPalette(CurrentActorPointer_0, 0, skin + 1, 0.0f);
            unkPaletteFunc(CurrentActorPointer_0, 0, 0);
        }
    }
    return gone;
}

void initItemRando(void) {
    /**
     * @brief Initialize Item Rando functionality
     */
    
    // Item Rando
    for (int i = 0; i < 54; i++) {
        BonusBarrelData[i].spawn_actor = 45; // Spawn GB - Have as default
        bonus_data[i].flag = BonusBarrelData[i].flag;
        bonus_data[i].spawn_actor = BonusBarrelData[i].spawn_actor;
        bonus_data[i].kong_actor = BonusBarrelData[i].kong_actor;
    }
    // Add Chunky Minecart GB
    bonus_data[94].flag = 215;
    bonus_data[94].spawn_actor = 45;
    bonus_data[94].kong_actor = 6;
    // Add 4 Training Minigames
    for (int i = 0; i < 4; i++) {
        int tbarrel_flag = 0;
        if (!Rando.fast_start_beginning) {
            tbarrel_flag = FLAG_TBARREL_DIVE + i;
        }
        bonus_data[95 + i].flag = tbarrel_flag;
        bonus_data[95 + i].spawn_actor = CUSTOM_ACTORS_START + NEWACTOR_POTIONANY;
        bonus_data[95 + i].kong_actor = 0;
    }
    
    // Checks Screen
    pausescreenlist screen_count = PAUSESCREEN_TERMINATOR; // 4 screens vanilla + hint screen + check screen + move tracker
    *(short*)(0x806A8672) = screen_count - 1; // Screen decrease cap
    *(short*)(0x806A8646) = screen_count; // Screen increase cap

    // Head Size - It shouldn't be here, but haha funny game crash if placed in base init
    int load_size = 0xED;
    unsigned char* head_write = getFile(load_size, 0x1FEE800);
    for (int i = 0; i < load_size; i++) {
        HeadSize[i] = head_write[i];
    }

    // BP Table
    int bp_size = 0x28;
    unsigned short* bp_write = getFile(bp_size << 1, 0x1FF0E00);
    for (int i = 0; i < bp_size; i++) {
        bp_item_table[i] = bp_write[i];
    }
    // Medal Table
    int medal_size = 45;
    unsigned char* medal_write = getFile(medal_size, 0x1FF1080);
    for (int i = 0; i < medal_size; i++) {
        medal_item_table[i] = medal_write[i];
    }
    // Hint Table
    int wrinkly_size = 35;
    unsigned char* wrinkly_write = getFile(wrinkly_size, 0x1FF0EC0);
    for (int i = 0; i < wrinkly_size; i++) {
        wrinkly_item_table[i] = wrinkly_write[i];
    }
    // Crown Table
    int crown_size = 0xA;
    unsigned short* crown_write = getFile(crown_size << 1, 0x1FF10C0);
    for (int i = 0; i < crown_size; i++) {
        crown_item_table[i] = crown_write[i];
    }
    // Key Table
    int key_size = 0x8;
    unsigned short* key_write = getFile(key_size << 1, 0x1FF1000);
    for (int i = 0; i < key_size; i++) {
        key_item_table[i] = key_write[i];
    }
    // Fairy Table
    int fairy_size = 40;
    unsigned short* fairy_write = getFile(fairy_size, 0x1FF1040);
    for (int i = 0; i < (fairy_size>>1); i++) {
        fairy_item_table[i] = fairy_write[i];
    }
    // Rainbow Coin Table
    int rainbow_size = 0x10;
    unsigned short* rainbow_write = getFile(rainbow_size << 1, 0x1FF10E0);
    for (int i = 0; i < rainbow_size; i++) {
        rcoin_item_table[i] = rainbow_write[i];
    }
    // Melon Crate Table
    int crate_size = 0x10;
    unsigned short* crate_write = getFile(crate_size << 1, 0x1FF0E80);
    for (int i = 0; i < crate_size; i++) {
        crate_item_table[i] = crate_write[i];
    }
    // Reward Table
    for (int i = 0; i < 40; i++) {
        bonus_data[54 + i].flag = 469 + i;
        bonus_data[54 + i].kong_actor = (i % 5) + 2;
        bonus_data[54 + i].spawn_actor = getBPItem(i);
    }
    reward_rom_struct* reward_write = getFile(0x100, 0x1FF1200);
    for (int i = 0; i < 0x40; i++) {
        if (reward_write[i].flag > -1) {
            for (int j = 0; j < BONUS_DATA_COUNT; j++) {
                if (bonus_data[j].flag == reward_write[i].flag) {
                    bonus_data[j].spawn_actor = getActorIndex(reward_write[i].actor);
                }
            }
        }
    }
    // Other init
    initItemDropTable();
    initCollectableCollision();
    initActorDefs();
}