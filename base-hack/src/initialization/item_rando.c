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

unsigned short bp_item_table[40] = {
    // Kasplat Rewards
    78, 75, 77, 79, 76,
    78, 75, 77, 79, 76,
    78, 75, 77, 79, 76,
    78, 75, 77, 79, 76,
    78, 75, 77, 79, 76,
    78, 75, 77, 79, 76,
    78, 75, 77, 79, 76,
    78, 75, 77, 79, 76,
};
item_packet medal_item_table[85] = {
    // Medal Rewards
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
    {.item_type = REQITEM_MEDAL},
};
item_packet wrinkly_item_table[35] = {
    // Wrinkly Rewards
    {.item_type = REQITEM_HINT, .level = 0, .kong = KONG_DK},
    {.item_type = REQITEM_HINT, .level = 0, .kong = KONG_DIDDY},
    {.item_type = REQITEM_HINT, .level = 0, .kong = KONG_LANKY},
    {.item_type = REQITEM_HINT, .level = 0, .kong = KONG_TINY},
    {.item_type = REQITEM_HINT, .level = 0, .kong = KONG_CHUNKY},
    {.item_type = REQITEM_HINT, .level = 1, .kong = KONG_DK},
    {.item_type = REQITEM_HINT, .level = 1, .kong = KONG_DIDDY},
    {.item_type = REQITEM_HINT, .level = 1, .kong = KONG_LANKY},
    {.item_type = REQITEM_HINT, .level = 1, .kong = KONG_TINY},
    {.item_type = REQITEM_HINT, .level = 1, .kong = KONG_CHUNKY},
    {.item_type = REQITEM_HINT, .level = 2, .kong = KONG_DK},
    {.item_type = REQITEM_HINT, .level = 2, .kong = KONG_DIDDY},
    {.item_type = REQITEM_HINT, .level = 2, .kong = KONG_LANKY},
    {.item_type = REQITEM_HINT, .level = 2, .kong = KONG_TINY},
    {.item_type = REQITEM_HINT, .level = 2, .kong = KONG_CHUNKY},
    {.item_type = REQITEM_HINT, .level = 3, .kong = KONG_DK},
    {.item_type = REQITEM_HINT, .level = 3, .kong = KONG_DIDDY},
    {.item_type = REQITEM_HINT, .level = 3, .kong = KONG_LANKY},
    {.item_type = REQITEM_HINT, .level = 3, .kong = KONG_TINY},
    {.item_type = REQITEM_HINT, .level = 3, .kong = KONG_CHUNKY},
    {.item_type = REQITEM_HINT, .level = 4, .kong = KONG_DK},
    {.item_type = REQITEM_HINT, .level = 4, .kong = KONG_DIDDY},
    {.item_type = REQITEM_HINT, .level = 4, .kong = KONG_LANKY},
    {.item_type = REQITEM_HINT, .level = 4, .kong = KONG_TINY},
    {.item_type = REQITEM_HINT, .level = 4, .kong = KONG_CHUNKY},
    {.item_type = REQITEM_HINT, .level = 5, .kong = KONG_DK},
    {.item_type = REQITEM_HINT, .level = 5, .kong = KONG_DIDDY},
    {.item_type = REQITEM_HINT, .level = 5, .kong = KONG_LANKY},
    {.item_type = REQITEM_HINT, .level = 5, .kong = KONG_TINY},
    {.item_type = REQITEM_HINT, .level = 5, .kong = KONG_CHUNKY},
    {.item_type = REQITEM_HINT, .level = 6, .kong = KONG_DK},
    {.item_type = REQITEM_HINT, .level = 6, .kong = KONG_DIDDY},
    {.item_type = REQITEM_HINT, .level = 6, .kong = KONG_LANKY},
    {.item_type = REQITEM_HINT, .level = 6, .kong = KONG_TINY},
    {.item_type = REQITEM_HINT, .level = 6, .kong = KONG_CHUNKY},
};
unsigned short crown_item_table[10] = {
    // Crown Rewards
    86, 86, 86, 86,
    86, 86, 86, 86,
    86, 86,
};
unsigned short key_item_table[8] = {
    // Boss Rewards
    72, 72, 72, 72,
    72, 72, 72, 72,
};
model_item_data fairy_item_table[20] = {
    // Fairy Rewards
    {.model = 0x3D, .item = {.item_type = REQITEM_FAIRY}},
    {.model = 0x3D, .item = {.item_type = REQITEM_FAIRY}},
    {.model = 0x3D, .item = {.item_type = REQITEM_FAIRY}},
    {.model = 0x3D, .item = {.item_type = REQITEM_FAIRY}},
    {.model = 0x3D, .item = {.item_type = REQITEM_FAIRY}},
    {.model = 0x3D, .item = {.item_type = REQITEM_FAIRY}},
    {.model = 0x3D, .item = {.item_type = REQITEM_FAIRY}},
    {.model = 0x3D, .item = {.item_type = REQITEM_FAIRY}},
    {.model = 0x3D, .item = {.item_type = REQITEM_FAIRY}},
    {.model = 0x3D, .item = {.item_type = REQITEM_FAIRY}},
    {.model = 0x3D, .item = {.item_type = REQITEM_FAIRY}},
    {.model = 0x3D, .item = {.item_type = REQITEM_FAIRY}},
    {.model = 0x3D, .item = {.item_type = REQITEM_FAIRY}},
    {.model = 0x3D, .item = {.item_type = REQITEM_FAIRY}},
    {.model = 0x3D, .item = {.item_type = REQITEM_FAIRY}},
    {.model = 0x3D, .item = {.item_type = REQITEM_FAIRY}},
    {.model = 0x3D, .item = {.item_type = REQITEM_FAIRY}},
    {.model = 0x3D, .item = {.item_type = REQITEM_FAIRY}},
    {.model = 0x3D, .item = {.item_type = REQITEM_FAIRY}},
    {.model = 0x3D, .item = {.item_type = REQITEM_FAIRY}},
};
unsigned short rcoin_item_table[16] = {
    // Dirt Patch Rewards
    0x8C, 0x8C, 0x8C, 0x8C,
    0x8C, 0x8C, 0x8C, 0x8C,
    0x8C, 0x8C, 0x8C, 0x8C,
    0x8C, 0x8C, 0x8C, 0x8C,
};
unsigned short crate_item_table[16] = {
    // Crate Rewards
    0x2F, 0x2F, 0x2F, 0x2F,
    0x2F, 0x2F, 0x2F, 0x2F,
    0x2F, 0x2F, 0x2F, 0x2F,
    0x2F, 0x2F, 0x2F, 0x2F,
};
patch_db_item patch_flags[16] = {}; // Flag table for dirt patches to differentiate it from balloons
BoulderItemStruct boulder_item_table[16] = {
    // Holdable Object Rewards
    { .map = MAP_ISLES, .spawner_id = 1},
    { .map = MAP_ISLES, .spawner_id = 1},
    { .map = MAP_AZTEC, .spawner_id = 4},
    { .map = MAP_CAVES, .spawner_id = 0},
    { .map = MAP_CAVES, .spawner_id = 1},
    { .map = MAP_CASTLEMUSEUM, .spawner_id = 0},
    { .map = MAP_JAPESLOBBY, .spawner_id = 2},
    { .map = MAP_CASTLELOBBY, .spawner_id = 0},
    { .map = MAP_CAVESLOBBY, .spawner_id = 5},
    { .map = MAP_FUNGIMILLFRONT, .spawner_id = 5},
    { .map = MAP_FUNGIMILLFRONT, .spawner_id = 7},
    { .map = MAP_FUNGIMILLREAR, .spawner_id = 4},
    { .map = MAP_AZTEC, .spawner_id = 3},
    { .map = MAP_AZTEC, .spawner_id = 2},
    { .map = MAP_AZTEC, .spawner_id = 1},
    { .map = MAP_AZTEC, .spawner_id = 0},
};
bonus_barrel_info bonus_data[BONUS_DATA_COUNT] = {}; // Bonus Barrel Rewards
meloncrate_db_item crate_flags[16] = {}; // Melon crate table
model_item_data kong_check_data[4] = {
    // Kong table
    {.model =  1, .item = {.item_type = REQITEM_KONG, .kong = KONG_DIDDY}},
    {.model =  6, .item = {.item_type = REQITEM_KONG, .kong = KONG_LANKY}},
    {.model =  9, .item = {.item_type = REQITEM_KONG, .kong = KONG_TINY}},
    {.model = 12, .item = {.item_type = REQITEM_KONG, .kong = KONG_CHUNKY}},
};
item_packet company_coin_table[2] = {
    {.item_type = REQITEM_COMPANYCOIN, .kong = 0}, // Nintendo Coin
    {.item_type = REQITEM_COMPANYCOIN, .kong = 1}, // Rareware Coin
};

int getBPItem(int index) {
    /**
     * @brief Get Blueprint item from kasplat index
     * 
     * @param index Kasplat Index: (5 * level) + kong
     * 
     * @return Actor Index of the reward
     */
	return bp_item_table[index];
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
			return crown_item_table[i];
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
			return key_item_table[i];
		}
	}
	return 0;
}

int getRainbowCoinItem(int old_flag) {
	/**
	 * @brief Get Dirt Patch reward from the old flag
     * 
     * @param old_flag Original flag of the dirt patch
	 * 
     * @return Actor Index of the reward
	 */
	return rcoin_item_table[old_flag - FLAG_RAINBOWCOIN_0];
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

void updateBoulderId(int index, int id) {
    boulder_item_table[index].spawner_id = id;
}

int getBoulderIndex(void) {
    int id = getActorSpawnerIDFromTiedActor(CurrentActorPointer_0);
    for (int i = 0; i < 16; i++) {
        if (boulder_item_table[i].map == CurrentMap) {
            if (boulder_item_table[i].spawner_id == id) {
                return i;
            }
        }
    }
    return -1;
}

int getBoulderItem(void) {
    int index = getBoulderIndex();
    if (index < 0) {
        return 0;
    }
    return boulder_item_table[index].item;
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
    {.actor = NEWACTOR_NINTENDOCOIN, .skin=SKIN_NINTENDO_COIN},
    {.actor = NEWACTOR_RAREWARECOIN, .skin=SKIN_RAREWARE_COIN},
    {.actor = 72, .skin=SKIN_KEY},
    {.actor = 86, .skin=SKIN_CROWN},
    {.actor = NEWACTOR_MEDAL, .skin=SKIN_MEDAL},
    {.actor = NEWACTOR_POTIONDK, .skin=SKIN_POTION},
    {.actor = NEWACTOR_POTIONDIDDY, .skin=SKIN_POTION},
    {.actor = NEWACTOR_POTIONLANKY, .skin=SKIN_POTION},
    {.actor = NEWACTOR_POTIONTINY, .skin=SKIN_POTION},
    {.actor = NEWACTOR_POTIONCHUNKY, .skin=SKIN_POTION},
    {.actor = NEWACTOR_POTIONANY, .skin=SKIN_POTION},
    {.actor = NEWACTOR_KONGDK, .skin=SKIN_KONG_DK},
    {.actor = NEWACTOR_KONGDIDDY, .skin=SKIN_KONG_DIDDY},
    {.actor = NEWACTOR_KONGLANKY, .skin=SKIN_KONG_LANKY},
    {.actor = NEWACTOR_KONGTINY, .skin=SKIN_KONG_TINY},
    {.actor = NEWACTOR_KONGCHUNKY, .skin=SKIN_KONG_CHUNKY},
    {.actor = NEWACTOR_BEAN, .skin=SKIN_BEAN},
    {.actor = NEWACTOR_PEARL, .skin=SKIN_PEARL},
    {.actor = NEWACTOR_FAIRY, .skin=SKIN_FAIRY},
    {.actor = 140, .skin=SKIN_RAINBOW_COIN},
    {.actor = NEWACTOR_ICETRAPBUBBLE, .skin=SKIN_FAKE_ITEM},
    {.actor = 0x2F, .skin=SKIN_JUNK_ITEM},
    {.actor = NEWACTOR_CRANKYITEM, .skin=SKIN_CRANKY},
    {.actor = NEWACTOR_FUNKYITEM, .skin=SKIN_FUNKY},
    {.actor = NEWACTOR_CANDYITEM, .skin=SKIN_CANDY},
    {.actor = NEWACTOR_SNIDEITEM, .skin=SKIN_SNIDE},
    {.actor = NEWACTOR_ICETRAPREVERSE, .skin=SKIN_FAKE_ITEM},
    {.actor = NEWACTOR_ICETRAPSLOW, .skin=SKIN_FAKE_ITEM},
    {.actor = NEWACTOR_HINTITEMDK, .skin=SKIN_HINT},
    {.actor = NEWACTOR_HINTITEMDIDDY, .skin=SKIN_HINT},
    {.actor = NEWACTOR_HINTITEMLANKY, .skin=SKIN_HINT},
    {.actor = NEWACTOR_HINTITEMTINY, .skin=SKIN_HINT},
    {.actor = NEWACTOR_HINTITEMCHUNKY, .skin=SKIN_HINT},
    {.actor = NEWACTOR_ARCHIPELAGOITEM, .skin=SKIN_AP},
    {.actor = 151, .skin=SKIN_FAKE_BEAN},
    {.actor = 152, .skin=SKIN_FAKE_BEAN},
    {.actor = 153, .skin=SKIN_FAKE_BEAN},
    {.actor = 154, .skin=SKIN_FAKE_KEY},
    {.actor = 155, .skin=SKIN_FAKE_KEY},
    {.actor = 157, .skin=SKIN_FAKE_KEY},
    {.actor = NEWACTOR_ICETRAPDISABLEABEAN, .skin=SKIN_FAKE_BEAN},
    {.actor = NEWACTOR_ICETRAPDISABLEBBEAN, .skin=SKIN_FAKE_BEAN},
    {.actor = NEWACTOR_ICETRAPDISABLEZBEAN, .skin=SKIN_FAKE_BEAN},
    {.actor = NEWACTOR_ICETRAPDISABLECUBEAN, .skin=SKIN_FAKE_BEAN},
    {.actor = NEWACTOR_ICETRAPDISABLEAKEY, .skin=SKIN_FAKE_KEY},
    {.actor = NEWACTOR_ICETRAPDISABLEBKEY, .skin=SKIN_FAKE_KEY},
    {.actor = NEWACTOR_ICETRAPDISABLEZKEY, .skin=SKIN_FAKE_KEY},
    {.actor = NEWACTOR_ICETRAPDISABLECUKEY, .skin=SKIN_FAKE_KEY},
    {.actor = NEWACTOR_ICETRAPDISABLEAGB, .skin=SKIN_FAKE_ITEM},
    {.actor = NEWACTOR_ICETRAPDISABLEBGB, .skin=SKIN_FAKE_ITEM},
    {.actor = NEWACTOR_ICETRAPDISABLEZGB, .skin=SKIN_FAKE_ITEM},
    {.actor = NEWACTOR_ICETRAPDISABLECUGB, .skin=SKIN_FAKE_ITEM},
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
    if (checkFlag(flag, flag_type)) {
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
    return 0;
}

void initItemRando(void) {
    /**
     * @brief Initialize Item Rando functionality
     */
    
    // Item Rando
    for (int i = 0; i < 54; i++) {
        bonus_data[i].flag = BonusBarrelData[i].flag;
        bonus_data[i].spawn_actor = 45;
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
        bonus_data[95 + i].spawn_actor = NEWACTOR_POTIONANY;
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
                    bonus_data[j].spawn_actor = reward_write[i].actor;
                }
            }
        }
    }
    // Other init
    initActorDefs();
}