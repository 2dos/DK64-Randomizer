#include "../../include/common.h"

typedef struct reward_rom_struct {
	/* 0x000 */ short flag;
	/* 0x002 */ unsigned char actor;
	/* 0x003 */ unsigned char unused;
} reward_rom_struct;

typedef struct patch_db_item {
	/* 0x000 */ short id;
	/* 0x002 */ unsigned char map;
	/* 0x003 */ unsigned char world;
} patch_db_item;

static unsigned char bp_item_table[40] = {};
static unsigned char medal_item_table[40] = {};
static unsigned char crown_item_table[10] = {};
static unsigned char key_item_table[8] = {};
static short fairy_item_table[20] = {};
static unsigned char rcoin_item_table[16] = {};
static patch_db_item patch_flags[16] = {};
bonus_barrel_info bonus_data[95] = {};

int getBPItem(int index) {
	return bp_item_table[index];
}

int getMedalItem(int index) {
	return medal_item_table[index];
}

int getCrownItem(int map) {
	int map_list[] = {0x35,0x49,0x9B,0x9C,0x9F,0xA0,0xA1,0x9D,0xA2,0x9E};
	for (int i = 0; i < 10; i++) {
		if (map == map_list[i]) {
			return crown_item_table[i];
		}
	}
	return 0;
}

int getKeyItem(int old_flag) {
	int flag_list[] = {26,74,138,168,236,292,317,380};
	for (int i = 0; i < 8; i++) {
		if (old_flag == flag_list[i]) {
			return key_item_table[i];
		}
	}
	return 0;
}

int getFairyModel(int flag) {
	if ((flag >= 589) && (flag <= 608)) {
		return fairy_item_table[flag - 589];
	}
	return 0x3D;
}

int getRainbowCoinItem(int old_flag) {
	// return TestVariable;
	return rcoin_item_table[old_flag - FLAG_RAINBOWCOIN_0];
}

int getPatchFlag(int id) {
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
	return patch_flags[index].world;
}

void populatePatchItem(int id, int map, int index, int world) {
    patch_flags[index].id = id;
    patch_flags[index].map = map;
    patch_flags[index].world = world;
}

void initItemRando(void) {
    // Item Get
    *(int*)(0x806F64C8) = 0x0C000000 | (((int)&getItem & 0xFFFFFF) >> 2); // Modify Function Call
    *(int*)(0x806F6BA8) = 0x0C000000 | (((int)&getItem & 0xFFFFFF) >> 2); // Modify Function Call
    *(int*)(0x806F7740) = 0x0C000000 | (((int)&getItem & 0xFFFFFF) >> 2); // Modify Function Call
    *(int*)(0x806F7764) = 0x0C000000 | (((int)&getItem & 0xFFFFFF) >> 2); // Modify Function Call
    *(int*)(0x806F7774) = 0x0C000000 | (((int)&getItem & 0xFFFFFF) >> 2); // Modify Function Call
    *(int*)(0x806F7798) = 0x0C000000 | (((int)&getItem & 0xFFFFFF) >> 2); // Modify Function Call
    *(int*)(0x806F77B0) = 0x0C000000 | (((int)&getItem & 0xFFFFFF) >> 2); // Modify Function Call
    *(int*)(0x806F77C4) = 0x0C000000 | (((int)&getItem & 0xFFFFFF) >> 2); // Modify Function Call
    *(int*)(0x806F7804) = 0x0C000000 | (((int)&getItem & 0xFFFFFF) >> 2); // Modify Function Call
    *(int*)(0x806F781C) = 0x0C000000 | (((int)&getItem & 0xFFFFFF) >> 2); // Modify Function Call

    *(int*)(0x806F6350) = 0x0C000000 | (((int)&getObjectCollectability & 0xFFFFFF) >> 2); // Modify Function Call
    *(int*)(0x8070E1F0) = 0x0C000000 | (((int)&handleDynamicItemText & 0xFFFFFF) >> 2); // Handle Dynamic Text Item Name

    // Item Rando
    for (int i = 0; i < 54; i++) {
        BonusBarrelData[i].spawn_actor = 45; // Spawn GB - Have as default
        bonus_data[i].flag = BonusBarrelData[i].flag;
        bonus_data[i].spawn_actor = BonusBarrelData[i].spawn_actor;
        // bonus_data[i].spawn_actor = 88;
        bonus_data[i].kong_actor = BonusBarrelData[i].kong_actor;
    }
    // Add Chunky Minecart GB
    bonus_data[94].flag = 215;
    bonus_data[94].spawn_actor = 45;
    bonus_data[94].kong_actor = 6;
    if (Rando.item_rando) {
        *(short*)(0x806B4E1A) = Rando.vulture_item;
        *(short*)(0x8069C266) = Rando.japes_rock_item;
        *(int*)(0x806A78A8) = 0x0C000000 | (((int)&checkFlagDuplicate & 0xFFFFFF) >> 2); // Balloon: Kong Check
        *(int*)(0x806AAB3C) = 0x0C000000 | (((int)&checkFlagDuplicate & 0xFFFFFF) >> 2); // Pause: BP Get
        *(int*)(0x806AAB9C) = 0x0C000000 | (((int)&checkFlagDuplicate & 0xFFFFFF) >> 2); // Pause: BP In
        *(int*)(0x806AAD70) = 0x0C000000 | (((int)&checkFlagDuplicate & 0xFFFFFF) >> 2); // Pause: Fairies
        *(int*)(0x806AAF70) = 0x0C000000 | (((int)&checkFlagDuplicate & 0xFFFFFF) >> 2); // Pause: Crowns
        *(int*)(0x806AB064) = 0x0C000000 | (((int)&checkFlagDuplicate & 0xFFFFFF) >> 2); // Pause: Isle Crown 1
        *(int*)(0x806AB0B4) = 0x0C000000 | (((int)&checkFlagDuplicate & 0xFFFFFF) >> 2); // Pause: Isle Crown 2
        *(int*)(0x806ABF00) = 0x0C000000 | (((int)&checkFlagDuplicate & 0xFFFFFF) >> 2); // File Percentage: Keys
        *(int*)(0x806ABF78) = 0x0C000000 | (((int)&checkFlagDuplicate & 0xFFFFFF) >> 2); // File Percentage: Crowns
        *(int*)(0x806ABFA8) = 0x0C000000 | (((int)&checkFlagDuplicate & 0xFFFFFF) >> 2); // File Percentage: NCoin
        *(int*)(0x806ABFBC) = 0x0C000000 | (((int)&checkFlagDuplicate & 0xFFFFFF) >> 2); // File Percentage: RCoin
        *(int*)(0x806AC00C) = 0x0C000000 | (((int)&checkFlagDuplicate & 0xFFFFFF) >> 2); // File Percentage: Kongs
        *(int*)(0x806BD304) = 0x0C000000 | (((int)&checkFlagDuplicate & 0xFFFFFF) >> 2); // Key flag check: K. Lumsy
        *(int*)(0x80731A6C) = 0x0C000000 | (((int)&checkFlagDuplicate & 0xFFFFFF) >> 2); // Count flag-kong array
        *(int*)(0x80731AE8) = 0x0C000000 | (((int)&checkFlagDuplicate & 0xFFFFFF) >> 2); // Count flag array
        *(int*)(0x806B1E48) = 0x0C000000 | (((int)&countFlagsForKongFLUT & 0xFFFFFF) >> 2); // Kasplat Check Flag
        *(int*)(0x806F56F8) = 0; // Disable Flag Set for blueprints
        *(int*)(0x806F78B8) = 0x0C000000 | (((int)&getKongFromBonusFlag & 0xFFFFFF) >> 2); // Reward Table Kong Check
        *(int*)(0x806F938C) = 0x0C000000 | (((int)&banana_medal_acquisition & 0xFFFFFF) >> 2); // Medal Give
        *(int*)(0x806F9394) = 0;
        *(int*)(0x806F5564) = 0x0C000000 | (((int)&itemGrabHook & 0xFFFFFF) >> 2); // Item Get Hook - Post Flag
        *(int*)(0x806BD798) = 0x0C000000 | (((int)&KLumsyText & 0xFFFFFF) >> 2); // K. Lumsy code hook
        *(int*)(0x806A6CA8) = 0x0C000000 | (((int)&canItemPersist & 0xFFFFFF) >> 2); // Item Despawn Check
        *(int*)(0x806A741C) = 0; // Prevent Key Twinkly Sound
        *(int*)(0x80688714) = 0x0C000000 | (((int)&setupHook & 0xFFFFFF) >> 2); // Setup Load Hook
        // Fairy Adjustments
        *(int*)(0x8072728C) = 0x0C000000 | (((int)&spawnCharSpawnerActor & 0xFFFFFF) >> 2); // Spawn 1
        *(int*)(0x80727290) = 0x36050000; // ORI $a1, $s0, 0x0 -> Change second parameter to the spawner
        *(int*)(0x8072777C) = 0x0C000000 | (((int)&spawnCharSpawnerActor & 0xFFFFFF) >> 2); // Spawn 2
        *(int*)(0x80727780) = 0x36050000; // ORI $a1, $s0, 0x0 -> Change second parameter to the spawner
        *(int*)(0x807277D0) = 0x0C000000 | (((int)&spawnCharSpawnerActor & 0xFFFFFF) >> 2); // Spawn 3
        *(int*)(0x807277D4) = 0x36050000; // ORI $a1, $s0, 0x0 -> Change second parameter to the spawner
        *(int*)(0x80727B88) = 0x0C000000 | (((int)&spawnCharSpawnerActor & 0xFFFFFF) >> 2); // Spawn 4
        *(int*)(0x80727B8C) = 0x36050000; // ORI $a1, $s0, 0x0 -> Change second parameter to the spawner
        *(int*)(0x80727C10) = 0x0C000000 | (((int)&spawnCharSpawnerActor & 0xFFFFFF) >> 2); // Spawn 4
        *(int*)(0x80727C14) = 0x36050000; // ORI $a1, $s0, 0x0 -> Change second parameter to the spawner
        *(int*)(0x806C5F04) = 0x0C000000 | (((int)&giveFairyItem & 0xFFFFFF) >> 2); // Fairy Flag Set
        // Rainbow Coins
        *(int*)(0x806A2268) = 0x0C000000 | (((int)&spawnDirtPatchReward & 0xFFFFFF) >> 2); // Spawn Reward
        *(int*)(0x806A222C) = 0x0C000000 | (((int)&getPatchFlag & 0xFFFFFF) >> 2); // Get Patch Flags
        *(int*)(0x806A2058) = 0x0C000000 | (((int)&getPatchFlag & 0xFFFFFF) >> 2); // Get Patch Flags
        *(short*)(0x80688C8E) = 0x30; // Reduce scope of detecting if balloon or patch, so patches don't have dynamic flags
        if (Rando.barrel_aesthetic) {
            // Barrel Aesthetic
            initBarrelChange();
        }
        // Checks Screen
        int screen_count = 5;
        *(short*)(0x806A8672) = screen_count; // Screen decrease cap
        *(short*)(0x806A8646) = screen_count + 1; // Screen increase cap
        *(int*)(0x806A94CC) = 0x2C610003; // SLTIU $at, $v1, 0x3 (Changes render check for <3 rather than == 3)
        *(int*)(0x806A94D0) = 0x10200298; // BEQZ $at, 0x298 (Changes render check for <3 rather than == 3)
        *(int*)(0x806A9F98) = 0x0C000000 | (((int)&pauseScreen3And4Header & 0xFFFFFF) >> 2); // Header
        *(int*)(0x806AA03C) = 0x0C000000 | (((int)&pauseScreen3And4Counter & 0xFFFFFF) >> 2); // Counter
        *(int*)(0x806A86BC) = 0x0C000000 | (((int)&changePauseScreen & 0xFFFFFF) >> 2); // Change screen hook
        // *(int*)(0x806A86F8) = 0x2CA10003; // SLTIU $at, $a1, 0x3 (Changes control check for <3 rather than == 3)
        // *(int*)(0x806A86FC) = 0x10200182; // BEQZ $at, 0x182 (Changes control check for <3 rather than == 3)
        // *(int*)(0x806AA410) = 0x2C410003; // SLTIU $at, $v0, 0x3 (Changes sprite check for <3 rather than == 3)
        // *(int*)(0x806AA414) = 0x102003AA; // BEQZ $at, 0x3AA (Changes sprite check for <3 rather than == 3)
        *(int*)(0x806A8D20) = 0x0C000000 | (((int)&changeSelectedLevel & 0xFFFFFF) >> 2); // Change selected level on checks screen
        *(int*)(0x806A84F8) = 0x0C000000 | (((int)&checkItemDB & 0xFFFFFF) >> 2); // Populate Item Databases
    }

    // BP Table
    int bp_size = 0x28;
    unsigned char* bp_write = dk_malloc(bp_size);
    int* bp_file_size;
    *(int*)(&bp_file_size) = bp_size;
    copyFromROM(0x1FF1000,bp_write,&bp_file_size,0,0,0,0);
    for (int i = 0; i < bp_size; i++) {
        bp_item_table[i] = bp_write[i];
    }
    // Medal Table
    int medal_size = 0x28;
    unsigned char* medal_write = dk_malloc(medal_size);
    int* medal_file_size;
    *(int*)(&medal_file_size) = medal_size;
    copyFromROM(0x1FF1080,medal_write,&medal_file_size,0,0,0,0);
    for (int i = 0; i < medal_size; i++) {
        medal_item_table[i] = medal_write[i];
    }
    // Crown Table
    int crown_size = 0xA;
    unsigned char* crown_write = dk_malloc(crown_size);
    int* crown_file_size;
    *(int*)(&crown_file_size) = crown_size;
    copyFromROM(0x1FF10C0,crown_write,&crown_file_size,0,0,0,0);
    for (int i = 0; i < crown_size; i++) {
        crown_item_table[i] = crown_write[i];
    }
    // Key Table
    int key_size = 0x8;
    unsigned char* key_write = dk_malloc(key_size);
    int* key_file_size;
    *(int*)(&key_file_size) = key_size;
    copyFromROM(0x1FF10D0,key_write,&key_file_size,0,0,0,0);
    for (int i = 0; i < key_size; i++) {
        key_item_table[i] = key_write[i];
    }
    // Fairy Table
    int fairy_size = 40;
    unsigned short* fairy_write = dk_malloc(fairy_size);
    int* fairy_file_size;
    *(int*)(&fairy_file_size) = fairy_size;
    copyFromROM(0x1FF1040,fairy_write,&fairy_file_size,0,0,0,0);
    for (int i = 0; i < (fairy_size>>1); i++) {
        fairy_item_table[i] = fairy_write[i];
    }
    // Rainbow Coin Table
    int rainbow_size = 0x10;
    unsigned char* rainbow_write = dk_malloc(rainbow_size);
    int* rainbow_file_size;
    *(int*)(&rainbow_file_size) = rainbow_size;
    copyFromROM(0x1FF10F0,rainbow_write,&rainbow_file_size,0,0,0,0);
    for (int i = 0; i < rainbow_size; i++) {
        rcoin_item_table[i] = rainbow_write[i];
    }
    // Reward Table
    for (int i = 0; i < 40; i++) {
        bonus_data[54 + i].flag = 469 + i;
        bonus_data[54 + i].kong_actor = (i % 5) + 2;
        bonus_data[54 + i].spawn_actor = bp_item_table[i];
    }
    int reward_size = 0x100;
    reward_rom_struct* reward_write = dk_malloc(medal_size);
    int* reward_file_size;
    *(int*)(&reward_file_size) = reward_size;
    copyFromROM(0x1FF1200,reward_write,&reward_file_size,0,0,0,0);
    for (int i = 0; i < 0x40; i++) {
        if (reward_write[i].flag > -1) {
            for (int j = 0; j < 95; j++) {
                if (bonus_data[j].flag == reward_write[i].flag) {
                    bonus_data[j].spawn_actor = reward_write[i].actor;
                }
            }
        }
    }
    *(int*)(0x80681910) = 0x0C000000 | (((int)&spawnBonusReward & 0xFFFFFF) >> 2); // Spawn Bonus Reward
    *(int*)(0x806C63BC) = 0x0C000000 | (((int)&spawnRewardAtActor & 0xFFFFFF) >> 2); // Spawn Squawks Reward
    *(int*)(0x806C4654) = 0x0C000000 | (((int)&spawnMinecartReward & 0xFFFFFF) >> 2); // Spawn Squawks Reward - Minecart
    initItemDropTable();
    initCollectableCollision();
    initActorDefs();
    initItemDictionary();
}