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
static unsigned char medal_item_table[40] = {}; // Medal Rewards
static unsigned short crown_item_table[10] = {}; // Crown Rewards
static unsigned short key_item_table[8] = {}; // Boss Rewards
static short fairy_item_table[20] = {}; // Fairy Rewards
static unsigned short rcoin_item_table[16] = {}; // Dirt Patch Rewards
static unsigned short crate_item_table[16] = {}; // Crate Rewards
static patch_db_item patch_flags[16] = {}; // Flag table for dirt patches to differentiate it from balloons
bonus_barrel_info bonus_data[95] = {}; // Bonus Barrel Rewards
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
	int flag_list[] = {26,74,138,168,236,292,317,380};
	for (int i = 0; i < 8; i++) {
		if (old_flag == flag_list[i]) {
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

typedef enum enum_bonus_skin {
    /* 0x000 */ SKIN_GB,
    /* 0x001 */ SKIN_KONG_DK,
    /* 0x002 */ SKIN_KONG_DIDDY,
    /* 0x003 */ SKIN_KONG_LANKY,
    /* 0x004 */ SKIN_KONG_TINY,
    /* 0x005 */ SKIN_KONG_CHUNKY,
    /* 0x006 */ SKIN_BLUEPRINT,
    /* 0x007 */ SKIN_NINTENDO_COIN,
    /* 0x008 */ SKIN_RAREWARE_COIN,
    /* 0x009 */ SKIN_KEY,
    /* 0x00A */ SKIN_CROWN,
    /* 0x00B */ SKIN_MEDAL,
    /* 0x00C */ SKIN_POTION,
    /* 0x00D */ SKIN_BEAN,
    /* 0x00E */ SKIN_PEARL,
    /* 0x00F */ SKIN_FAIRY,
    /* 0x010 */ SKIN_RAINBOW_COIN,
    /* 0x011 */ SKIN_FAKE_ITEM,
    /* 0x012 */ SKIN_JUNK_ITEM,
    /* ----- */ SKIN_TERMINATOR,
} enum_bonus_skin;

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
    {.actor = CUSTOM_ACTORS_START + NEWACTOR_FAKEITEM, .skin=SKIN_FAKE_ITEM},
    {.actor = 0x2F, .skin=SKIN_JUNK_ITEM},
};

enum_bonus_skin getBarrelSkinIndex(int actor) {
    for (int i = 0; i < (sizeof(bonus_skins) / sizeof(barrel_skin_tie)); i++) {
        if (bonus_skins[i].actor == actor) {
            return bonus_skins[i].skin;
        }
    }
    return SKIN_GB;
}

// #define BONUS_CACHE_SIZE SKIN_TERMINATOR * 2
// static void* bonus_texture_data[BONUS_CACHE_SIZE] = {};
// static unsigned char bonus_texture_load[BONUS_CACHE_SIZE] = {};

// void* loadBonusTexture(int texture_offset) {
// 	if (bonus_texture_load[texture_offset] == 0) {
// 		bonus_texture_data[texture_offset] = getMapData(TABLE_TEXTURES, 6026 + texture_offset, 1, 1);
// 	}
// 	bonus_texture_load[texture_offset] = 3;
// 	return bonus_texture_data[texture_offset];
// }

int alterBonusVisuals(int index) {
    if (Rando.location_visuals & 1) {
        if (index < 95) {
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

void initItemRando(void) {
    /**
     * @brief Initialize Item Rando functionality
     */
    // Item Get
    writeFunction(0x806F64C8, &getItem); // Modify Function Call
    writeFunction(0x806F6BA8, &getItem); // Modify Function Call
    writeFunction(0x806F7740, &getItem); // Modify Function Call
    writeFunction(0x806F7764, &getItem); // Modify Function Call
    writeFunction(0x806F7774, &getItem); // Modify Function Call
    writeFunction(0x806F7798, &getItem); // Modify Function Call
    writeFunction(0x806F77B0, &getItem); // Modify Function Call
    writeFunction(0x806F77C4, &getItem); // Modify Function Call
    writeFunction(0x806F7804, &getItem); // Modify Function Call
    writeFunction(0x806F781C, &getItem); // Modify Function Call

    writeFunction(0x806F6350, &getObjectCollectability); // Modify Function Call
    writeFunction(0x8070E1F0, &handleDynamicItemText); // Handle Dynamic Text Item Name
    if (ENABLE_FILENAME) {
        writeFunction(0x8070E1BC, &handleFilename); // Handle Filename
    }

    writeFunction(0x806A7AEC, &BalloonShoot); // Balloon Shoot Hook
    // Rainbow Coins
    writeFunction(0x806A222C, &getPatchFlag); // Get Patch Flags
    writeFunction(0x806A2058, &getPatchFlag); // Get Patch Flags
    *(short*)(0x80688C8E) = 0x30; // Reduce scope of detecting if balloon or patch, so patches don't have dynamic flags
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
    writeFunction(0x80680AE8, &alterBonusVisuals); // Get Bonus Flag Check
    writeFunction(0x80681854, &getBonusFlag); // Get Bonus Flag Check
    writeFunction(0x806C63A8, &getBonusFlag); // Get Bonus Flag Check
    writeFunction(0x806F78B8, &getKongFromBonusFlag); // Reward Table Kong Check
    // Checks Screen
    pausescreenlist screen_count = PAUSESCREEN_TERMINATOR; // 4 screens vanilla + hint screen + check screen + move tracker
    *(short*)(0x806A8672) = screen_count - 1; // Screen decrease cap
    *(short*)(0x806A8646) = screen_count; // Screen increase cap
    *(int*)(0x806A94CC) = 0x2C610003; // SLTIU $at, $v1, 0x3 (Changes render check for <3 rather than == 3)
    *(int*)(0x806A94D0) = 0x10200298; // BEQZ $at, 0x298 (Changes render check for <3 rather than == 3)
    writeFunction(0x806A9F98, &pauseScreen3And4Header); // Header
    writeFunction(0x806AA03C, &pauseScreen3And4Counter); // Counter
    writeFunction(0x806A86BC, &changePauseScreen); // Change screen hook
    writeFunction(0x806A8D20, &changeSelectedLevel); // Change selected level on checks screen
    writeFunction(0x806A84F8, &checkItemDB); // Populate Item Databases
    writeFunction(0x806A9978, &displayHintRegion); // Display hint region
    if (Rando.item_rando) {
        *(short*)(0x806B4E1A) = getActorIndex(Rando.vulture_item);
        *(short*)(0x8069C266) = getActorIndex(Rando.japes_rock_item);
        writeFunction(0x806A78A8, &checkFlagDuplicate); // Balloon: Kong Check
        writeFunction(0x806AAB3C, &checkFlagDuplicate); // Pause: BP Get
        writeFunction(0x806AAB9C, &checkFlagDuplicate); // Pause: BP In
        writeFunction(0x806AAD70, &checkFlagDuplicate); // Pause: Fairies
        writeFunction(0x806AAF70, &checkFlagDuplicate); // Pause: Crowns
        writeFunction(0x806AB064, &checkFlagDuplicate); // Pause: Isle Crown 1
        writeFunction(0x806AB0B4, &checkFlagDuplicate); // Pause: Isle Crown 2
        writeFunction(0x806ABF00, &checkFlagDuplicate); // File Percentage: Keys
        writeFunction(0x806ABF78, &checkFlagDuplicate); // File Percentage: Crowns
        writeFunction(0x806ABFA8, &checkFlagDuplicate); // File Percentage: NCoin
        writeFunction(0x806ABFBC, &checkFlagDuplicate); // File Percentage: RCoin
        writeFunction(0x806AC00C, &checkFlagDuplicate); // File Percentage: Kongs
        writeFunction(0x806BD304, &checkFlagDuplicate); // Key flag check: K. Lumsy
        writeFunction(0x80731A6C, &checkFlagDuplicate); // Count flag-kong array
        writeFunction(0x80731AE8, &checkFlagDuplicate); // Count flag array
        writeFunction(0x806B1E48, &countFlagsForKongFLUT); // Kasplat Check Flag
        *(int*)(0x806F56F8) = 0; // Disable Flag Set for blueprints
        writeFunction(0x806F938C, &banana_medal_acquisition); // Medal Give
        *(int*)(0x806F9394) = 0;
        writeFunction(0x806F5564, &itemGrabHook); // Item Get Hook - Post Flag
        writeFunction(0x806A6CA8, &canItemPersist); // Item Despawn Check
        *(int*)(0x806A741C) = 0; // Prevent Key Twinkly Sound
        writeFunction(0x80688714, &setupHook); // Setup Load Hook
        // Fairy Adjustments
        writeFunction(0x8072728C, &spawnCharSpawnerActor); // Spawn 1
        *(int*)(0x80727290) = 0x36050000; // ORI $a1, $s0, 0x0 -> Change second parameter to the spawner
        writeFunction(0x8072777C, &spawnCharSpawnerActor); // Spawn 2
        *(int*)(0x80727780) = 0x36050000; // ORI $a1, $s0, 0x0 -> Change second parameter to the spawner
        writeFunction(0x807277D0, &spawnCharSpawnerActor); // Spawn 3
        *(int*)(0x807277D4) = 0x36050000; // ORI $a1, $s0, 0x0 -> Change second parameter to the spawner
        writeFunction(0x80727B88, &spawnCharSpawnerActor); // Spawn 4
        *(int*)(0x80727B8C) = 0x36050000; // ORI $a1, $s0, 0x0 -> Change second parameter to the spawner
        writeFunction(0x80727C10, &spawnCharSpawnerActor); // Spawn 4
        *(int*)(0x80727C14) = 0x36050000; // ORI $a1, $s0, 0x0 -> Change second parameter to the spawner
        writeFunction(0x806C5F04, &giveFairyItem); // Fairy Flag Set
        // Rainbow Coins
        writeFunction(0x806A2268, &spawnDirtPatchReward); // Spawn Reward
        // Melon Crate
        *(int*)(0x80747EB0) = (int)&melonCrateItemHandler;
        // Mill GB
        writeFunction(0x806F633C, &isObjectTangible_detailed); // Change object tangibility check function
        
        *(int*)(0x806C5C7C) = 0; // Cancel out fairy draw distance reduction
        *(short*)(0x806C46AA) = 0x4100; // Bring squawks closer to the player for minecarts (X)
        *(short*)(0x806C46E2) = 0x4100; // Bring squawks closer to the player for minecarts (Z)
        *(short*)(0x806C45C2) = 0x0013; // Y Offset squawks reward
    }

    // BP Table
    int bp_size = 0x28;
    unsigned short* bp_write = getFile(bp_size << 1, 0x1FF0E00);
    for (int i = 0; i < bp_size; i++) {
        bp_item_table[i] = bp_write[i];
    }
    // Medal Table
    int medal_size = 0x28;
    unsigned char* medal_write = getFile(medal_size, 0x1FF1080);
    for (int i = 0; i < medal_size; i++) {
        medal_item_table[i] = medal_write[i];
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
            for (int j = 0; j < 95; j++) {
                if (bonus_data[j].flag == reward_write[i].flag) {
                    bonus_data[j].spawn_actor = getActorIndex(reward_write[i].actor);
                }
            }
        }
    }
    writeFunction(0x80681910, &spawnBonusReward); // Spawn Bonus Reward
    writeFunction(0x806C63BC, &spawnRewardAtActor); // Spawn Squawks Reward
    writeFunction(0x806C4654, &spawnMinecartReward); // Spawn Squawks Reward - Minecart
    // Initialize fixed item scales
    writeFunction(0x806F4918, &writeItemScale); // Write scale to collision info
    *(int*)(0x806F491C) = 0x87A40066; // LH $a0, 0x66 ($sp)
    *(short*)(0x806F4C6E) = 0x20; // Change size
    *(short*)(0x806F4C82) = 0x20; // Change size
    writeFunction(0x806F515C, &writeItemActorScale); // Write actor scale to collision info
    // Other init
    initItemDropTable();
    initCollectableCollision();
    initActorDefs();
    initItemDictionary();
}