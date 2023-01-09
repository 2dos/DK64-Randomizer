#include "../include/common.h"

static const char exittoisles[] = "EXIT TO ISLES";
static const char exittospawn[] = "EXIT TO SPAWN";

typedef struct musicInfo {
	/* 0x000 */ short data[0xB0];
} musicInfo;

void fixMusicRando(void) {
	// Music
	if (Rando.music_rando_on) {
		int size = 0x160;
		musicInfo* write_space = dk_malloc(size);
		int* file_size;
		*(int*)(&file_size) = size;
		copyFromROM(0x1FFF000,write_space,&file_size,0,0,0,0);
		for (int i = 0; i < 0xB0; i++) {
			int subchannel = (write_space->data[i] & 6) >> 1;
			int channel = (write_space->data[i] & 0x78) >> 3;
			songData[i] &= 0xFF81;
			songData[i] |= (subchannel & 3) << 1;
			songData[i] |= (channel & 0xF) << 3;
		}
		complex_free(write_space);
	}
}

void writeEndSequence(void) {
	int size = 0x84;
	int* file_size;
	*(int*)(&file_size) = size;
	copyFromROM(0x1FFF800,(int*)0x807506D0,&file_size,0,0,0,0);
}

typedef struct reward_rom_struct {
	/* 0x000 */ short flag;
	/* 0x002 */ unsigned char actor;
	/* 0x003 */ unsigned char unused;
} reward_rom_struct;

void expandSaveFile(int static_expansion, int actor_count) {
	/*
		File cannot be bigger than 0x200 bytes

		File Structure:
			0x000->0x320 = Flags
			0x320->c+0x320 = Model2
			c+0x320->c+0x645 = Kong Vars
			c+0x645->c+0x6B7 = File Global Vars

		Generalized:
			0 -> f = Flags
			f -> f+c = Model 2
			f+c -> f+c+5k = Kong Vars
			f+c+5k -> f+c+5k+0x72 = File Global Vars
	*/
	// int expansion = static_expansion;
	int expansion = static_expansion + actor_count;
	int flag_block_size = 0x320 + expansion;
	int targ_gb_bits = 5; // Max 127
	int added_bits = (targ_gb_bits - 3) * 8;
	int kong_var_size = 0xA1 + added_bits;
	int file_info_location = flag_block_size + (5 * kong_var_size);
	int file_default_size = file_info_location + 0x72;
	// Flag Block Size
	*(short*)(0x8060E36A) = file_default_size;
	*(short*)(0x8060E31E) = file_default_size;
	*(short*)(0x8060E2C6) = file_default_size;
	*(short*)(0x8060D54A) = file_default_size;
	*(short*)(0x8060D4A2) = file_default_size;
	*(short*)(0x8060D45E) = file_default_size;
	*(short*)(0x8060D3C6) = file_default_size;
	*(short*)(0x8060D32E) = file_default_size;
	*(short*)(0x8060D23E) = file_default_size;
	*(short*)(0x8060CF62) = file_default_size;
	*(short*)(0x8060CC52) = file_default_size;
	*(short*)(0x8060C78A) = file_default_size;
	*(short*)(0x8060C352) = file_default_size;
	*(short*)(0x8060BF96) = file_default_size;
	*(short*)(0x8060BA7A) = file_default_size;
	*(short*)(0x8060BEC6) = file_info_location;
	// Increase GB Storage Size
	*(short*)(0x8060BE12) = targ_gb_bits; // Bit Size
	*(short*)(0x8060BE06) = targ_gb_bits << 3; // Allocation for all levels
	*(short*)(0x8060BE2A) = 0x4021; // SUBU -> ADDU
	*(int*)(0x8060BCC0) = 0x24090000 | kong_var_size; // ADDIU $t1, $r0, kong_var_size
	*(int*)(0x8060BCC4) = 0x01C90019; // MULTU $t1, $t6
	*(int*)(0x8060BCC8) = 0x00004812; // MFLO $t1
	*(int*)(0x8060BCCC) = 0; // NOP
	// Model 2 Start
	*(short*)(0x8060C2F2) = flag_block_size;
	*(short*)(0x8060BCDE) = flag_block_size;
	// Reallocate Balloons + Patches
	*(short*)(0x80688BCE) = 0x320 + static_expansion; // Reallocated to just before model 2 block
}

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

static char boot_speedup_done = 0;

void bootSpeedup(void) {
	if (!boot_speedup_done) {
		boot_speedup_done = 1;
		int balloon_patch_count = 0;
		for (int j = 0; j < 8; j++) {
			coloredBananaCounts[j] = 0;
		}
		int patch_index = 0;
		for (int i = 0; i < 221; i++) {
			balloonPatchCounts[i] = balloon_patch_count;
			int* setup = getMapData(9,i,1,1);
			char* modeltwo_setup = 0;
			char* actor_setup = 0;
			if (setup) {
				int world = getWorld(i,1);
				getModel2AndActorInfo(setup,(int**)&modeltwo_setup,(int**)&actor_setup);
				int model2_count = *(int*)(modeltwo_setup);
				int actor_count = *(int*)(actor_setup);
				char* focused_actor = (char*)(actor_setup + 4);
				char* focused_model2 = (char*)(modeltwo_setup + 4);
				if (actor_count > 0) {
					for (int j = 0; j < actor_count; j++) {
						int actor = *(short*)((int)focused_actor + 0x32) + 0x10;
						balloon_patch_count += isBalloonOrPatch(actor);
						if ((Rando.item_rando) && (actor == 139)) {
							patch_flags[patch_index].map = i;
							patch_flags[patch_index].id = *(short*)((int)focused_actor + 0x34);
							if (isLobby(i)) {
								patch_flags[patch_index].world = 7;
							} else {
								patch_flags[patch_index].world = levelIndexMapping[i];
							}
							patch_index += 1;
						}
						focused_actor += 0x38;
					}
				}
				if (model2_count > 0) {
					for (int j = 0; j < model2_count; j++) {
						coloredBananaCounts[world] += isSingleOrBunch(*(unsigned short*)(focused_model2 + 0x28));
						focused_model2 += 0x30;
					}
				}
				enableComplexFree();
				complexFreeWrapper(setup);
			}
		}
	}
}

void initHack(int source) {
	if (LoadedHooks == 0) {
		if ((source == 1) || (CurrentMap == 0x28)) {
			DebugInfoOn = 1;
			// Faster Boot
			*(int*)(0x805FEB00) = 0x0C000000 | (((int)&bootSpeedup & 0xFFFFFF) >> 2); // Modify Function Call
			*(int*)(0x805FEB08) = 0; // Cancel 2nd check
			// Starting map rando
			int starting_map_rando_on = 1;
			if (Rando.starting_map == 0) {
				// Default
				Rando.starting_map = 0x22;
				Rando.starting_exit = 0;
				starting_map_rando_on = 0;
			} else {
				*(short*)(0x8071454A) = Rando.starting_map;
				*(int*)(0x80714550) = 0x24050000 | Rando.starting_exit;
			}
			setPrevSaveMap();
			if (Rando.fast_start_beginning) {
				*(int*)(0x80714540) = 0;
			}
			*(int*)(0x80731F78) = 0; // Debug 1 Column
			*(int*)(0x8060E04C) = 0; // Prevent moves overwrite
			*(short*)(0x8060DDAA) = 0; // Writes readfile data to moves
			*(short*)(0x806C9CDE) = 7; // GiveEverything, write to bitfield. Seems to be unused but might as well
			
			// Prevent GBs being required to view extra screens
			*(int*)(0x806A8624) = 0; // GBs doesn't lock other pause screens
			*(int*)(0x806AB468) = 0; // Show R/Z Icon
			*(int*)(0x806AB318) = 0x24060001; // ADDIU $a2, $r0, 1
			*(int*)(0x806AB31C) = 0xA466C83C; // SH $a2, 0xC83C ($v1) | Overwrite trap func, Replace with overwrite of wheel segments
			*(short*)(0x8075056C) = 201; // Change GB Item cap to 201

			// Strong Kong
			*(int*)(0x8067ECFC) = 0x30810002; // ANDI $at $a0 2
			*(int*)(0x8067ED00) = 0x50200003; // BEQL $at $r0 3
			// Rocketbarrel
			*(int*)(0x80682024) = 0x31810002; // ANDI $at $t4 2
			*(int*)(0x80682028) = 0x50200006; // BEQL $at $r0 0x6
			// OSprint
			*(int*)(0x8067ECE0) = 0x30810004; // ANDI $at $a0 4
			*(int*)(0x8067ECE4) = 0x10200002; // BEQZ $at, 2
			// Mini Monkey
			*(int*)(0x8067EC80) = 0x30830001; // ANDI $v1 $a0 1
			*(int*)(0x8067EC84) = 0x18600002; // BLEZ $v1 2
			// Hunky Chunky (Not Dogadon)
			*(int*)(0x8067ECA0) = 0x30810001; // ANDI $at $a0 1
			*(int*)(0x8067ECA4) = 0x18200002; // BLEZ $at 2
			// PTT
			*(int*)(0x806E20F0) = 0x31010002; // ANDI $at $t0 2
			*(int*)(0x806E20F4) = 0x5020000F; // BEQL $at $r0 0xF
			// PPUnch
			*(int*)(0x806E48F4) = 0x31810002; // ANDI $at $t4 2
			*(int*)(0x806E48F8) = 0x50200074; // BEQL $at $r0 0xF
			if (Rando.krusha_slot == 4) {
				Rando.disco_chunky = 0;
			} else if (Rando.krusha_slot > 4) {
				Rando.krusha_slot = -1;
			}
			DamageMultiplier = Rando.damage_multiplier;
			WarpToIslesEnabled = Rando.warp_to_isles_enabled;
			permaLossMode = Rando.perma_lose_kongs;
			preventTagSpawn = Rando.prevent_tag_spawn;
			bonusAutocomplete = Rando.resolve_bonus;
			TextHoldOn = Rando.quality_of_life.textbox_hold;
			ToggleAmmoOn = Rando.quality_of_life.ammo_swap;
			LobbiesOpen = Rando.lobbies_open_bitfield;
			ShorterBosses = Rando.short_bosses;
			WinCondition = Rando.win_condition;
			ItemRandoOn = Rando.item_rando;
			KrushaSlot = Rando.krusha_slot;
			RandomSwitches = Rando.random_switches;
			for (int i = 0; i < 7; i++) {
				SwitchLevel[i] = Rando.slam_level[i];
			}
			// Kong Rando
			initKongRando();
			// Savefile Expansion		
			int balloon_patch_count = 300; // Normally 121
			expandSaveFile(0x100,balloon_patch_count);
			if (Rando.no_health_refill) {
				*(int*)(0x80683A34) = 0; // Cancel Tag Health Refill
				// *(int*)(0x8060DD10) = 0; // Load File
				// *(int*)(0x806C8010) = 0; // Load into map with < 1 health
				// *(int*)(0x806C94E4) = 0; // ?
				// *(int*)(0x806C9BC0) = 0; // Multiplayer
				*(int*)(0x806CB340) = 0; // Voiding
				*(int*)(0x806DEFE4) = 0; // Fairies
				// *(int*)(0x80708C9C) = 0; // Bonus Barrels (Taking Damge) & Watermelons
				// *(int*)(0x80708CA4) = 0; // Bonus Barrels (Full Health) & Watermelons
				*(int*)(0x806A6EA8) = 0; // Bonus Barrels
			} else {
				*(int*)(0x806A6EA8) = 0x0C1C2519; // Set Bonus Barrel to refill health

			}
			if (Rando.short_bosses) {
				*(short*)(0x8074D474) = 44; // Dogadon Health: 3 + (62 * (2 / 3))
				*(short*)(0x8074D3A8) = 3; // Dillo Health
			}
			if (Rando.resolve_bonus & 1) {
				*(short*)(0x806818DE) = 0x4248; // Make Aztec Lobby GB spawn above the trapdoor)
				*(int*)(0x80681690) = 0; // Make some barrels not play a cutscene
				*(int*)(0x8068188C) = 0; // Prevent disjoint mechanic for Caves/Fungi BBlast Bonus
				*(short*)(0x80681898) = 0x1000;
				*(int*)(0x8068191C) = 0; // Remove Oh Banana
				*(short*)(0x80680986) = 0xFFFE; // Prevent Factory BBBandit Bonus dropping
				*(short*)(0x806809C8) = 0x1000; // Prevent Fungi TTTrouble Bonus dropping
			}
			if (Rando.resolve_bonus) {
				*(int*)(0x80681158) = 0x0C000000 | (((int)&completeBonus & 0xFFFFFF) >> 2); // Modify Function Call
				*(short*)(0x80681962) = 1; // Make bonus noclip	
			}
			if (Rando.tns_portal_rando_on) {
				// Adjust warp code to make camera be behind player, loading portal
				*(int*)(0x806C97D0) = 0xA06E0007; // SB $t6, 0x7 ($v1)
			}
			if (Rando.remove_rock_bunch) {
				*(int*)(0x8069C2FC) = 0;
			}
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
			
			replace_zones(1);
			randomize_bosses();
			loadExtraHooks();
			// Moves & Prices
			fixTBarrelsAndBFI(1);
			// Place Move Data
			moveTransplant();
			priceTransplant();
			if (Rando.disable_boss_kong_check) {
				*(int*)(0x8064EC00) = 0x24020001;
			}
			*(int*)(0x8074C1B8) = (int)&newCounterCode;
			*(short*)(0x8074DC84) = 0x53; // Increase PAAD size
			fixMusicRando();
			// In-Level IGT
			*(int*)(0x8060DF28) = 0x0C000000 | (((int)&updateLevelIGT & 0xFFFFFF) >> 2); // Modify Function Call
			*(int*)(0x806ABB0C) = 0x0C000000 | (((int)&printLevelIGT & 0xFFFFFF) >> 2); // Modify Function Call
			*(short*)(0x806ABB32) = 106; // Adjust kong name height
			// Disable Sniper Scope Overlay
			int asm_code = 0x00801025; // OR $v0, $a0, $r0
			*(int*)(0x806FF80C) = asm_code;
			*(int*)(0x806FF85C) = asm_code;
			*(int*)(0x806FF8AC) = asm_code;
			*(int*)(0x806FF8FC) = asm_code;
			*(int*)(0x806FF940) = asm_code;
			*(int*)(0x806FF988) = asm_code;
			*(int*)(0x806FF9D0) = asm_code;
			*(int*)(0x806FFA18) = asm_code;
			// Change Sniper Crosshair color
			*(short*)(0x806FFA92) = 0xFFD7;
			*(short*)(0x806FFA96) = 0x00FF;
			// *(int*)(0x806FFA90) = 0x3C0D8080;
			// *(int*)(0x806FFA94) = 0x8DADFFFC;
			// Style 6 Mtx
			int base_mtx = 75;
			style6Mtx[0x0] = base_mtx;
			style6Mtx[0x5] = base_mtx;
			style6Mtx[0xF] = 100;
			style6Mtx[0x8] = 0xEA00;
			style6Mtx[0x9] = 0xFD00;
			base_mtx = 12;
			style2Mtx[0x0] = base_mtx;
			style2Mtx[0x5] = base_mtx;
			style2Mtx[0xF] = 10;
			base_mtx = 50;
			style128Mtx[0x0] = base_mtx;
			style128Mtx[0x5] = base_mtx;
			style128Mtx[0xF] = 100;
			writeCoinRequirements(0);
			writeEndSequence();
			*(int*)(0x806F6350) = 0x0C000000 | (((int)&getObjectCollectability & 0xFFFFFF) >> 2); // Modify Function Call
			if (Rando.warp_to_isles_enabled) {
				// Pause Menu Exit To Isles Slot
				*(short*)(0x806A85EE) = 4; // Yes/No Prompt
				*(short*)(0x806A8716) = 4; // Yes/No Prompt
				//*(short*)(0x806A87BE) = 3;
				*(short*)(0x806A880E) = 4; // Yes/No Prompt
				//*(short*)(0x806A8766) = 4;
				*(short*)(0x806A986A) = 4; // Yes/No Prompt
				*(int*)(0x806A9990) = 0x2A210270; // SLTI $at, $s1, 0x2A8
				if (!starting_map_rando_on) {
					PauseSlot3TextPointer = (char*)&exittoisles;
				} else {
					PauseSlot3TextPointer = (char*)&exittospawn;
				}
			}
			if (Rando.quality_of_life.reduce_lag) {
				*(int*)(0x80748010) = 0x8064F2F0; // Cancel Sandstorm
				// No Rain
				*(float*)(0x8075E3E0) = 0.0f; // Set Isles Rain Radius to 0
			}
			if (Rando.quality_of_life.remove_cutscenes) {
				// K. Lumsy
				*(short*)(0x80750680) = 0x22;
				*(short*)(0x80750682) = 0x1;
				*(int*)(0x806BDC24) = 0x0C17FCDE; // Change takeoff warp func
				*(short*)(0x806BDC8C) = 0x1000; // Apply no cutscene to all keys
				*(short*)(0x806BDC3C) = 0x1000; // Apply shorter timer to all keys
				// Fast Vulture
				*(int*)(0x806C50BC) = 0x0C000000 | (((int)&clearVultureCutscene & 0xFFFFFF) >> 2); // Modify Function Call
				// General
				*(int*)(0x80628508) = 0x0C000000 | (((int)&renderScreenTransitionCheck & 0xFFFFFF) >> 2); // Modify Function Call
				// *(int*)(0x8061D920) = 0xA4205CEC; // Set cutscene state change to 0
				// *(int*)(0x8061D91C) = 0x0C000000 | (((int)&checkSkippableCutscene & 0xFFFFFF) >> 2); // Modify Function Call
			} else {
				for (int i = 0; i < 432; i++) {
					cs_skip_db[i] = 0;
				}
			}
			if (Rando.quality_of_life.vanilla_fixes) {
				*(int*)(0x806BE8D8) = 0x0C000000 | (((int)&RabbitRaceInfiniteCode & 0xFFFFFF) >> 2); // Modify Function Call
				*(int*)(0x8067C168) = 0x0C000000 | (((int)&fixDilloTNTPads & 0xFFFFFF) >> 2); // Modify Function Call
			}
			*(int*)(0x806A7564) = 0xC4440080; // Crown default floor will be it's initial Y spawn position. Fixes a crash on N64
			if (Rando.quality_of_life.fast_picture) {
				// Fast Camera Photo
				*(short*)(0x80699454) = 0x5000; // Fast tick/no mega-slowdown on Biz
				int picture_timer = 0x14;
				*(short*)(0x806992B6) = picture_timer; // No wait for camera film development
				*(short*)(0x8069932A) = picture_timer;
			}
			if (Rando.quality_of_life.aztec_lobby_bonus) {
				// Lower Aztec Lobby Bonus
				*(short*)(0x80680D56) = 0x7C; // 0x89 if this needs to be unreachable without PTT
			}
			if (Rando.quality_of_life.fast_boot) {
				// Remove DKTV - Game Over
				*(short*)(0x8071319E) = 0x50;
				*(short*)(0x807131AA) = 5;
				// Remove DKTV - End Seq
				*(short*)(0x8071401E) = 0x50;
				*(short*)(0x8071404E) = 5;
			}
			if (Rando.quality_of_life.fast_transform) {
				// Fast Barrel Animation
				*(short*)(0x8067EAB2) = 1; // OSprint
				*(short*)(0x8067EAC6) = 1; // HC Dogadon 2
				*(short*)(0x8067EACA) = 1; // Others
				*(short*)(0x8067EA92) = 1; // Others 2
			}
			if (Rando.quality_of_life.rambi_enguarde_pickup) {
				// Transformations can pick up other's collectables
				*(int*)(0x806F6330) = 0x96AC036E; // Collection
				// Collection
				*(int*)(0x806F68A0) = 0x95B8036E; // DK Collection
				*(int*)(0x806F68DC) = 0x952C036E; // Diddy Collection
				*(int*)(0x806F6914) = 0x95F9036E; // Tiny Collection
				*(int*)(0x806F694C) = 0x95AE036E; // Lanky Collection
				*(int*)(0x806F6984) = 0x952B036E; // Chunky Collection
				// Opacity
				*(int*)(0x80637998) = 0x95B9036E; // DK Opacity
				*(int*)(0x806379E8) = 0x95CF036E; // Diddy Opacity
				*(int*)(0x80637A28) = 0x9589036E; // Tiny Opacity
				*(int*)(0x80637A68) = 0x954B036E; // Chunky Opacity
				*(int*)(0x80637AA8) = 0x9708036E; // Lanky Opacity
				// CB/Coin rendering
				*(int*)(0x806394FC) = 0x958B036E; // Rendering
				*(int*)(0x80639540) = 0x9728036E; // Rendering
				*(int*)(0x80639584) = 0x95AE036E; // Rendering
				*(int*)(0x80639430) = 0x95CD036E; // Rendering
				*(int*)(0x806393EC) = 0x9519036E; // Rendering
				*(int*)(0x806395C8) = 0x952A036E; // Rendering
				*(int*)(0x8063960C) = 0x95F8036E; // Rendering
				*(int*)(0x80639474) = 0x9549036E; // Rendering
				*(int*)(0x806393A8) = 0x956C036E; // Rendering
				*(int*)(0x806394B8) = 0x970F036E; // Rendering
				*(int*)(0x80639650) = 0x956C036E; // Rendering
				*(int*)(0x80639710) = 0x9549036E; // Rendering
				*(int*)(0x80639750) = 0x970F036E; // Rendering
				*(int*)(0x806396D0) = 0x95CD036E; // Rendering
				*(int*)(0x80639690) = 0x9519036E; // Rendering
			}
			*(int*)(0x806F56E0) = 0x0C000000 | (((int)&getFlagIndex_Corrected & 0xFFFFFF) >> 2); // BP Acquisition - Correct for character
			*(int*)(0x806F9374) = 0x0C000000 | (((int)&getFlagIndex_Corrected & 0xFFFFFF) >> 2); // Medal Acquisition - Correct for character

			*(int*)(0x8070E1F0) = 0x0C000000 | (((int)&handleDynamicItemText & 0xFFFFFF) >> 2); // Handle Dynamic Text Item Name

			*(int*)(0x805FEBC0) = 0x0C000000 | (((int)&parseCutsceneData & 0xFFFFFF) >> 2); // modifyCutsceneHook
			*(int*)(0x807313A4) = 0x0C000000 | (((int)&checkVictory_flaghook & 0xFFFFFF) >> 2); // perm flag set hook

			*(int*)(0x80748088) = (int)&CrownDoorCheck; // Update check on Crown Door
			
			// New Mermaid Checking Code
			*(int*)(0x806C3B5C) = 0x0C000000 | (((int)&mermaidCheck & 0xFFFFFF) >> 2); // Mermaid Check
			*(short*)(0x806C3B64) = 0x1000; // Force to branch
			*(short*)(0x806C3BD0) = 0x1000; // Force to branch
			*(int*)(0x806C3C20) = 0; // NOP - Cancel control state write
			*(int*)(0x806C3C2C) = 0; // NOP - Cancel control state progress write
			if (Rando.helm_hurry_mode) {
				*(int*)(0x80713CCC) = 0; // Prevent Helm Timer Disable
				*(int*)(0x80713CD8) = 0; // Prevent Shutdown Song Playing
				*(short*)(0x8071256A) = 15; // Init Helm Timer = 15 minutes
			}
			if (Rando.always_show_coin_cbs) {
				*(int*)(0x806324D4) = 0x24020001; // ADDIU $v0, $r0, 1 // Disable kong flag check
			}
			if (Rando.fast_warp) {
				// Replace vanilla warp animation (0x52) with monkeyport animation (0x53)
				*(short*)(0x806EE692) = 0x54;
				*(int*)(0x806DC2AC) = 0x0C000000 | (((int)&fastWarp & 0xFFFFFF) >> 2); // Modify Function Call
				*(int*)(0x806DC318) = 0x0C000000 | (((int)&fastWarp_playMusic & 0xFFFFFF) >> 2); // Modify Function Call
			}
			if (Rando.version == 0) {
				// Disable Graphical Debugger
				*(int*)(0x8060EEE0) = 0x240E0000; // ADDIU $t6, $r0, 0
			}
			if (Rando.disco_chunky) {
				// Disco
				*(char*)(0x8075C45B) = 0xE; // General Model
				*(short*)(0x806F123A) = 0xED; // Instrument
				*(int*)(0x806CF37C) = 0; // Fix object holding
				*(short*)(0x8074E82C) = 0xE; // Tag Barrel Model
				*(short*)(0x8075EDAA) = 0xE; // Cutscene Chunky Model
				*(short*)(0x8075571E) = 0xE; // Generic Cutscene Model
				*(short*)(0x80755738) = 0xE; // Generic Cutscene Model
				*(int*)(0x806F1274) = 0; // Prevent model change for GGone
				*(int*)(0x806CBB84) = 0; // Enable opacity filter GGone
				*(short*)(0x8075BF3E) = 0x2F5C; // Make CS Model Behave normally
				*(short*)(0x8075013E) = 0xE; // Low Poly Model
			}
			if (Rando.krusha_slot != -1) {
				// Krusha
				int slot = Rando.krusha_slot;
				KongModelData[slot].model = 0xDB; // General Model
				TagModelData[slot].model = 0xDB; // Tag Barrel Model
				*(int*)(0x80677E94) = 0x0C000000 | (((int)&adjustAnimationTables & 0xFFFFFF) >> 2); // Give Krusha animations to slot
				*(int*)(0x806C32B8) = 0x0C000000 | (((int)&updateCutsceneModels & 0xFFFFFF) >> 2); // Fix cutscene models
				RollingSpeeds[slot] = 175; // Increase Krusha slide speed to 175
				KongTagNames[slot] = 6; // Change kong name in Tag Barrel
				KongTextNames[slot] = KongTextNames[5];
				LedgeHangY[slot] = LedgeHangY[5];
				LedgeHangY_0[slot] = LedgeHangY_0[5];
				*(short*)(0x8074AB5A) = 0x0040; // Enables Krusha's spin attack to knock kasplats down
				PotionAnimations[slot] = PotionAnimations[4];
				switch (slot) {
					case 0:
						// DK
						// *(int*)(0x806F1154) = 0x02002025; // Instrument - Param1
						// *(int*)(0x806F1158) = 0x0C184C65; // Instrument - Func Call
						// *(short*)(0x806F115E) = 0xDB; // Instrument - Param2
						// *(int*)(0x806F1194) = 0; // Instrument - NOP Other stuff
						// *(int*)(0x806F11B0) = 0; // Instrument - NOP Other stuff
						// *(int*)(0x806F11BC) = 0; // Instrument - NOP Other stuff
						// *(int*)(0x806F11D0) = 0; // Instrument - NOP Other stuff
						*(short*)(0x8075ED4A) = 0xDB; // Cutscene DK Model
						*(short*)(0x8075573E) = 0xDB; // Generic Cutscene Model
						*(int*)(0x8074C0A8) = 0x806C9F44; // Replace DK Code w/ Krusha Code
						*(short*)(0x806F0AFE) = 0; // Remove gun from hands in Tag Barrel
						*(int*)(0x806F0AF0) = 0x24050001; // Fix Hand State
						*(int*)(0x806D5EC4) = 0; // Prevent Moving Ground Attack pop up
						*(short*)(0x8064AF5E) = 5; // Reduce slam range for DK Dungeon GB Slam
						break;
					case 1:
						// Diddy
						*(short*)(0x806F11E6) = 0xDB; // Instrument
						*(short*)(0x8075ED62) = 0xDB; // Cutscene Diddy Model
						*(short*)(0x80755736) = 0xDB; // Generic Cutscene Model
						*(int*)(0x8074C0AC) = 0x806C9F44; // Replace Diddy Code w/ Krusha Code
						*(int*)(0x806F0A6C) = 0x0C1A29D9; // Replace hand state call
						*(int*)(0x806F0A78) = 0; // Replace hand state call
						*(int*)(0x806E4938) = 0; // Always run adapt code
						*(int*)(0x806E4940) = 0; // NOP Animation calls
						*(int*)(0x806E4950) = 0; // NOP Animation calls
						*(int*)(0x806E4958) = 0; // NOP Animation calls
						*(int*)(0x806E495C) = 0x0C000000 | (((int)&adaptKrushaZBAnimation_Charge & 0xFFFFFF) >> 2); // Allow Krusha to use slide move if fast enough (Charge)
						*(int*)(0x806E499C) = 0; // NOP Animation calls
						*(int*)(0x806E49C8) = 0; // NOP Animation calls
						*(int*)(0x806E49F0) = 0; // NOP Animation calls
						*(short*)(0x806CF5F0) = 0x5000; // Prevent blink special cases
						*(int*)(0x806CF76C) = 0; // Prevent blink special cases
						*(int*)(0x806832B8) = 0; // Prevent tag blinking
						*(int*)(0x806C1050) = 0; // Prevent Cutscene Kong blinking
						*(unsigned char*)(0x8075D19F) = 0xA0; // Fix Gun Firing
						*(int*)(0x806141B4) = 0x0C000000 | (((int)&DiddySwimFix & 0xFFFFFF) >> 2); // Fix Diddy's Swim Animation
						*(short*)(0x80749764) = 10; // Fix Diddy Swimming (A)
						*(short*)(0x80749758) = 10; // Fix Diddy Swimming (B)
						*(short*)(0x8074974C) = 10; // Fix Diddy Swimming (Z/First Person)
						*(int*)(0x806E903C) = 0x0C000000 | (((int)&MinecartJumpFix & 0xFFFFFF) >> 2); // Fix Diddy Minecart Jump
						*(int*)(0x806D259C) = 0x0C000000 | (((int)&MinecartJumpFix_0 & 0xFFFFFF) >> 2); // Fix Diddy Minecart Jump
						break;
					case 2:
						// Lanky
						/*
							Issues:
								Lanky Phase arm extension has a poly tri not correctly aligned
						*/
						*(short*)(0x806F1202) = 0xDB; // Instrument
						*(short*)(0x8075ED7A) = 0xDB; // Cutscene Lanky Model
						*(short*)(0x8075573A) = 0xDB; // Generic Cutscene Model
						*(int*)(0x8074C0B0) = 0x806C9F44; // Replace Lanky Code w/ Krusha Code
						*(short*)(0x806F0ABE) = 0; // Remove gun from hands in Tag Barrel
						*(int*)(0x806E48BC) = 0x0C000000 | (((int)&adaptKrushaZBAnimation_PunchOStand & 0xFFFFFF) >> 2); // Allow Krusha to use slide move if fast enough (OStand)
						*(int*)(0x806E48B4) = 0; // Always run `adaptKrushaZBAnimation`
						*(int*)(0x806F0AB0) = 0x24050001; // Fix Hand State
						*(short*)(0x80749C74) = 10; // Fix Lanky Swimming (A)
						*(short*)(0x80749C80) = 10; // Fix Lanky Swimming (B)
						*(short*)(0x80749CA4) = 10; // Fix Lanky Swimming (Z/First Person)
						*(int*)(0x806141B4) = 0x0C000000 | (((int)&DiddySwimFix & 0xFFFFFF) >> 2); // Fix Lanky's Swim Animation
						break;
					case 3:
						// Tiny
						*(short*)(0x806F121E) = 0xDB; // Instrument
						*(short*)(0x8075ED92) = 0xDB; // Cutscene Tiny Model
						*(short*)(0x8075573C) = 0xDB; // Generic Cutscene Model
						*(int*)(0x8074C0B4) = 0x806C9F44; // Replace Tiny Code w/ Krusha Code
						*(short*)(0x806F0ADE) = 0; // Remove gun from hands in Tag Barrel
						*(int*)(0x806E47F8) = 0; // Prevent slide bounce
						*(short*)(0x806CF784) = 0x5000; // Prevent blink special cases
						*(short*)(0x806832C0) = 0x5000; // Prevent tag blinking
						*(int*)(0x806C1058) = 0; // Prevent Cutscene Kong blinking
						*(int*)(0x806F0AD0) = 0x24050001; // Fix Hand State
						break;
					case 4:
						// Chunky
						*(short*)(0x806F123A) = 0xDB; // Instrument
						*(int*)(0x806CF37C) = 0; // Fix object holding
						*(short*)(0x8075EDAA) = 0xDB; // Cutscene Chunky Model
						*(short*)(0x8075571E) = 0xDB; // Generic Cutscene Model
						*(short*)(0x80755738) = 0xDB; // Generic Cutscene Model
						*(int*)(0x806F1274) = 0; // Prevent model change for GGone
						*(int*)(0x806CBB84) = 0; // Enable opacity filter GGone
						*(int*)(0x8074C0B8) = 0x806C9F44; // Replace Chunky Code w/ Krusha Code
						*(int*)(0x806E4900) = 0x0C000000 | (((int)&adaptKrushaZBAnimation_PunchOStand & 0xFFFFFF) >> 2); // Allow Krusha to use slide move if fast enough (PPunch)
						*(int*)(0x806E48F8) = 0; // Always run `adaptKrushaZBAnimation`
						*(short*)(0x806F0A9E) = 0; // Remove gun from hands in Tag Barrel
						*(int*)(0x806F0A90) = 0x24050001; // Fix Hand State
					break;
				}
			}
			if (Rando.fast_gbs) {
				*(short*)(0x806BBB22) = 0x0005; // Chunky toy box speedup

				*(short*)(0x806C58D6) = 0x0008; //Owl ring amount
				*(short*)(0x806C5B16) = 0x0008;

				*(int*)(0x806BEDFC) = 0; //Spawn banana coins on beating rabbit 2 (Beating round 2 branches to banana coin spawning label before continuing)
				
				// Arcade R1
				*(unsigned char*)(0x80755B68) = 0x6E; // Modify GB Map
				*(short*)(0x80755B6A) = 0; // Modify GB ID
			}
			// Change Beaver Bother Klaptrap Model
			if (Rando.klaptrap_color_bbother == 0) {
				Rando.klaptrap_color_bbother = 0x21; // Set to default model if no model assigned
			}
			int kko_phase_rando = 0;
			for (int i = 0; i < 3; i++) {
				KKOPhaseOrder[i] = Rando.kut_out_phases[i];
				if (Rando.kut_out_phases[i]) {
					kko_phase_rando = 1;
				}
			}
			KKOPhaseRandoOn = kko_phase_rando;
			*(short*)(0x806F0376) = Rando.klaptrap_color_bbother;
			*(short*)(0x806C8B42) = Rando.klaptrap_color_bbother;
			if (Rando.wrinkly_rando_on) {
				*(int*)(0x8064F170) = 0; // Prevent edge cases for Aztec Chunky/Fungi Wheel
				*(int*)(0x8069E154) = 0x0C000000 | (((int)&getWrinklyLevelIndex & 0xFFFFFF) >> 2); // Modify Function Call
			}
			*(short*)(0x8060D01A) = getHi(&InvertedControls); // Change language store to inverted controls store
			*(short*)(0x8060D01E) = getLo(&InvertedControls); // Change language store to inverted controls store
			*(short*)(0x8060D04C) = 0x1000; // Prevent inverted controls overwrite
			// Expand Display List
			*(short*)(0x805FE56A) = 8000;
			*(short*)(0x805FE592) = 0x4100; // SLL 4 (Doubles display list size)
			// Object Instance Scripts
			*(int*)(0x80748064) = (int)&change_object_scripts;
			*(int*)(0x806416BC) = 0; // Prevent parent map check in cross-map object change communications
			// Sniper Scope Check
			*(int*)(0x806D2988) = 0x93190002; // LBU $t9, 0x2 ($t8)
			*(int*)(0x806D2990) = 0x33210004; // ANDI $at, $t9, 0x4
			*(short*)(0x806D299C) = 0x1020; // BEQ $at, $r0
			// Speedy T&S Turn-Ins
			*(int*)(0x806BE3E0) = 0; // NOP
			// EEPROM Patch
			*(int*)(0x8060D588) = 0; // NOP
			// Cancel Tamper
			*(int*)(0x8060AEFC) = 0; // NOP
			*(int*)(0x80611788) = 0; // NOP
			// Fix HUD if DK not free
			*(int*)(0x806FA324) = 0; // NOP
			*(short*)(0x807505AE) = 385; // Set Flag to DK Flag
			// Fix CB Spawning
			*(short*)(0x806A7882) = 385; // DK Balloon
			// Fix Boss Doors if DK not free
			*(int*)(0x80649358) = 0; // NOP
			// Fix Pause Menu
			*(int*)(0x806ABFF8) = 0; // NOP (Write of first slot to 1)
			*(short*)(0x806AC002) = 0x530;
			*(short*)(0x806AC006) = 0x5B0;
			*(unsigned char*)(0x8075054D) = 0xD7; // Change DK Q Mark to #FFD700
			// Guard Animation Fix
			*(short*)(0x806AF8C6) = 0x2C1;
			// Init New Item Dictionary
			initItemDictionary();
			// Remove flare effect from guards
			*(int*)(0x806AE440) = 0;
			// Boost Diddy/Tiny's Barrel Speed
			*(float*)(0x807533A0) = 240.0f; // Diddy Ground
			*(float*)(0x807533A8) = 240.0f; // Tiny Ground
			*(float*)(0x807533DC) = 260.0f; // Lanky Air
			*(float*)(0x807533E0) = 260.0f; // Tiny Air
			// Bump Model Two Allowance
			int allowance = 550;
			*(short*)(0x80632026) = allowance; // Japes
			*(short*)(0x80632006) = allowance; // Aztec
			*(short*)(0x80631FF6) = allowance; // Factory
			*(short*)(0x80632016) = allowance; // Galleon
			*(short*)(0x80631FE6) = allowance; // Fungi
			*(short*)(0x80632036) = allowance; // Others
			// New Helm Barrel Code
			*(int*)(0x8074C24C) = (int)&HelmBarrelCode;
			// Deathwarp Handle
			*(int*)(0x8071292C) = 0x0C000000 | (((int)&WarpHandle & 0xFFFFFF) >> 2); // Check if in Helm, in which case, apply transition
			// New Guard Code
			*(short*)(0x806AF75C) = 0x1000;
			// Gold Beaver Code
      		*(int*)(0x8074C3F0) = 0x806AD54C; // Set as Blue Beaver Code
			*(int*)(0x806AD750) = 0x0C000000 | (((int)&beaverExtraHitHandle & 0xFFFFFF) >> 2); // Remove buff until we think of something better
			// Move Text Code
			*(int*)(0x8074C5B0) = (int)&getNextMoveText;
			*(int*)(0x8074C5A0) = (int)&getNextMoveText;
			// New Actors
			initActor(151, &ninCoinCode, ACTORMASTER_SPRITE, 0x11);
			initActor(152, &rwCoinCode, ACTORMASTER_SPRITE, 0x11);
			initActor(153, &NothingCode, ACTORMASTER_SPRITE, 0);
			initActor(154, &medalCode, ACTORMASTER_SPRITE, 0x11);
			for (int i = 0; i < 6; i++) {
				initActor(157 + i, &PotionCode, ACTORMASTER_3D, 0x11);
			}
			initActor(141, &KongDropCode, ACTORMASTER_3D, 0x11);
			initActor(142, &KongDropCode, ACTORMASTER_3D, 0x11);
			initActor(143, &KongDropCode, ACTORMASTER_3D, 0x11);
			initActor(144, &KongDropCode, ACTORMASTER_3D, 0x11);
			initActor(155, &KongDropCode, ACTORMASTER_3D, 0x11);
			initActor(172, &beanCode, ACTORMASTER_SPRITE, 0x11);
			initActor(174, &pearlCode, ACTORMASTER_SPRITE, 0x11);
			initActor(88, &fairyDuplicateCode, ACTORMASTER_3D, 0x11);
			initActor(217, &FakeGBCode, ACTORMASTER_3D, 0x11);
			// Any Kong Items
			if (Rando.any_kong_items & 1) {
				// All excl. Blueprints
				*(int*)(0x807319C0) = 0x00001025; // OR $v0, $r0, $r0 - Make all reward spots think no kong
				*(int*)(0x80632E94) = 0x00001025; // OR $v0, $r0, $r0 - Make flag mapping think no kong
			}
			if (Rando.any_kong_items & 2) {
				*(int*)(0x806F56F8) = 0; // Disable Flag Set for blueprints
				*(int*)(0x806A606C) = 0; // Disable translucency for blueprints
			}
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
				// Barrel Aesthetic
				initBarrelChange();
				
				if (Rando.quality_of_life.remove_cutscenes) {
					int cs_unskip[] = {
						0x1A, 2,
						0x1A, 3,
						0x1A, 4,
						0x1A, 5,
						0x26, 14,
						0x40, 1,
						0xA8, 0,
					};
					for (int i = 0; i < (sizeof(cs_unskip) / 8); i++) {
						int cs_offset = 0;
						int cs_val = cs_unskip[(2 * i) + 1];
						int cs_map = cs_unskip[(2 * i)];
						int shift = cs_val % 31;
						if (cs_val > 31) {
							cs_offset = 1;
						}
						int comp = 0xFFFFFFFF - (1 << shift);
						cs_skip_db[(2 * cs_map) + cs_offset] &= comp;
					}
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
			// Rainbow Cion Table
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
			/*
				TODO:
				- Change bonus aesthetic based on reward
			*/

			// Pause Totals/Checks Revamp
			*(int*)(0x806AB3C4) = 0x0C000000 | (((int)&updatePauseScreenWheel & 0xFFFFFF) >> 2); // Change Wheel to scroller
			*(int*)(0x806AB3B4) = 0xAFB00018; // SW $s0, 0x18 ($sp). Change last param to index
			*(int*)(0x806AB3A0) = 0xAFA90014; // SW $t1, 0x14 ($sp). Change 2nd-to-last param to local index
			*(int*)(0x806AB444) = 0; // Prevent joystick sprite rendering
			*(int*)(0x806AB528) = 0x0C000000 | (((int)&handleSpriteCode & 0xFFFFFF) >> 2); // Change sprite control function
			*(int*)(0x806AB52C) = 0x8FA40060; // LW $a0, 0x60 ($sp). Change param
			*(short*)(0x806A8DB2) = 0x0029; // Swap left/right direction
			*(short*)(0x806A8DBA) = 0xFFD8; // Swap left/right direction
			*(short*)(0x806A8DB4) = 0x5420; // BEQL -> BNEL
			*(short*)(0x806A8DF0) = 0x1020; // BNE -> BEQ
			*(int*)(0x806A9F74) = 0x0C000000 | (((int)&pauseScreen3And4ItemName & 0xFFFFFF) >> 2); // Item Name
			// Disable Item Checks
			*(int*)(0x806AB2E8) = 0;
			*(int*)(0x806AB360) = 0;
			*(short*)(0x806ABFCE) = FLAG_BP_JAPES_DK_HAS; // Change BP trigger to being collecting BP rather than turning it in
			initPauseMenu(); // Changes to enable more items
			// Spider Projectile
			if (Rando.hard_enemies) {
				*(int*)(0x806ADDC0) = 0x0C000000 | (((int)&handleSpiderTrapCode & 0xFFFFFF) >> 2);
				*(int*)(0x806CBD78) = 0x18400005; // BLEZ $v0, 0x5 - Decrease in health occurs if trap bubble active
				*(short*)(0x806B12DA) = 0x3A9; // Kasplat Shockwave Chance
				*(short*)(0x806B12FE) = 0x3B3; // Kasplat Shockwave Chance
				*(short*)(0x8074D4D0) = 9; // Increase Guard Health
			}
			// Oscillation Effects
			if (Rando.remove_oscillation_effects) {
				*(int*)(0x80661B54) = 0; // Remove Ripple Timer 0
				*(int*)(0x80661B64) = 0; // Remove Ripple Timer 1
				*(int*)(0x8068BDF4) = 0; // Disable rocking in Seasick Ship
				*(short*)(0x8068BDFC) = 0x1000; // Disable rocking in Mech Fish
			}
			// Slow Turn Fix
			*(int*)(0x806D2FC0) = 0x0C000000 | (((int)&fixRBSlowTurn & 0xFFFFFF) >> 2);
			// Tag Anywhere collectable Fixes
			// CB Bunch
			int non_chunky_bunch_indexes[] = {10,11,13,14};
			for (int i = 0; i < sizeof(non_chunky_bunch_indexes) / 4; i++) {
				int index = non_chunky_bunch_indexes[i];
				ModelTwoCollisionArray[index].actor_equivalent = 0;
			}
			*(int*)(0x806A65B8) = 0x240A0006; // Always ensure chunky bunch sprite
			// Coins
			int non_lanky_coin_indexes[] = {5,7,8,9};
			for (int i = 0; i < sizeof(non_lanky_coin_indexes) / 4; i++) {
				int index = non_lanky_coin_indexes[i];
				ModelTwoCollisionArray[index].actor_equivalent = 0;
			}
			*(int*)(0x806A64B0) = 0x240A0004; // Always ensure lanky coin sprite
			// 1-File Fixes
			*(int*)(0x8060CF34) = 0x240E0001; // Slot 1
			*(int*)(0x8060CF38) = 0x240F0002; // Slot 2
			*(int*)(0x8060CF3C) = 0x24180003; // Slot 3
			*(int*)(0x8060CF40) = 0x240D0000; // Slot 0
			*(int*)(0x8060D3AC) = 0; // Prevent EEPROM Shuffle
			*(int*)(0x8060DCE8) = 0; // Prevent EEPROM Shuffle
			// *(int*)(0x8060C760) = 0x24900000; // Always load file 0
			// *(short*)(0x8060CC22) = 1; // File Loop Cancel 1
			*(short*)(0x8060CD1A) = 1; // File Loop Cancel 2
			*(short*)(0x8060CE7E) = 1; // File Loop Cancel 3
			*(short*)(0x8060CE5A) = 1; // File Loop Cancel 4
			*(short*)(0x8060CF0E) = 1; // File Loop Cancel 5
			*(short*)(0x8060CF26) = 1; // File Loop Cancel 6
			//*(short*)(0x8060D0DE) = 1; // File Loop Cancel 7
			*(short*)(0x8060D106) = 1; // File Loop Cancel 8
			*(short*)(0x8060D43E) = 1; // File Loop Cancel 8
			*(int*)(0x8060CD08) = 0x26670000; // Save to File - File Index
			*(int*)(0x8060CE48) = 0x26670000; // Save to File - File Index
			*(int*)(0x8060CF04) = 0x26270000; // Save to File - File Index
			*(int*)(0x8060BFA4) = 0x252A0000; // Global Block after 1 file entry
			*(int*)(0x8060E378) = 0x258D0000; // Global Block after 1 file entry
			*(int*)(0x8060D33C) = 0x254B0000; // Global Block after 1 file entry
			*(int*)(0x8060D470) = 0x256C0000; // Global Block after 1 file entry
			*(int*)(0x8060D4B0) = 0x252A0000; // Global Block after 1 file entry
			*(int*)(0x8060D558) = 0x258D0000; // Global Block after 1 file entry
			*(int*)(0x8060CF74) = 0x25090000; // Global Block after 1 file entry
			// *(int*)(0x8060CFCC) = 0x25AE0000; // Global Block after 1 file entry
			*(int*)(0x8060D24C) = 0x25AE0000; // Global Block after 1 file entry
			*(int*)(0x8060C84C) = 0xA02067C8; // Force file 0
			*(int*)(0x8060C654) = 0x24040000; // Force file 0 - Save
			*(int*)(0x8060C664) = 0xAFA00034; // Force file 0 - Save
			*(int*)(0x8060C6C4) = 0x24040000; // Force file 0 - Read
			*(int*)(0x8060C6D4) = 0xAFA00034; // Force file 0 - Read
			*(int*)(0x8060D294) = 0; // Cartridge EEPROM Wipe cancel

			// for (int i = 0; i < 10; i++) {
			// 	*(int*)(0x8060D6A0 + (4 * i)) = 0;
			// }
			// *(short*)(0x8060D6C8) = 0x5000;
			// Decouple Camera from Shockwave
			*(short*)(0x806E9812) = FLAG_ABILITY_CAMERA; // Usage
			*(short*)(0x806AB0F6) = FLAG_ABILITY_CAMERA; // Isles Fairies Display
			*(short*)(0x806AAFB6) = FLAG_ABILITY_CAMERA; // Other Fairies Display
			*(short*)(0x806AA762) = FLAG_ABILITY_CAMERA; // Film Display
			*(short*)(0x8060D986) = FLAG_ABILITY_CAMERA; // Film Refill
			*(short*)(0x806F6F76) = FLAG_ABILITY_CAMERA; // Film Refill
			*(short*)(0x806F916A) = FLAG_ABILITY_CAMERA; // Film max
			initItemDropTable();
			initCollectableCollision();
			initActorDefs();
			// LZ Save
			*(int*)(0x80712EC4) = 0x0C000000 | (((int)&postKRoolSaveCheck & 0xFFFFFF) >> 2);
			if (Rando.medal_cb_req > 0) {
				// Change CB Req
				*(short*)(0x806F934E) = Rando.medal_cb_req; // Acquisition
				*(short*)(0x806F935A) = Rando.medal_cb_req; // Acquisition
				*(short*)(0x806AA942) = Rando.medal_cb_req; // Pause Menu Tick
			}
			// Reduce TA Cooldown
			if (Rando.tag_anywhere) {
				// *(int*)(0x806F6D88) = 0; // Makes collectables not produce a flying model which delays collection. Instant change
				*(int*)(0x806F6D94) = 0; // Prevent delayed collection
				// Standard Ammo
				*(short*)(0x806F5B68) = 0x1000;
				*(int*)(0x806F5BE8) = 0x0C000000 | (((int)&tagAnywhereAmmo & 0xFFFFFF) >> 2);
				// Bunch
				*(short*)(0x806F59A8) = 0x1000;
				*(int*)(0x806F5A08) = 0x0C000000 | (((int)&tagAnywhereBunch & 0xFFFFFF) >> 2);

				*(int*)(0x806F6CAC) = 0x9204001A; // LBU $a0, 0x1A ($s0)
				*(int*)(0x806F6CB0) = 0x86060002; // LH $a2, 0x2 ($s0)
				*(int*)(0x806F6CB4) = 0x0C000000 | (((int)&tagAnywhereInit & 0xFFFFFF) >> 2);
				*(int*)(0x806F53AC) = 0; // Prevent LZ case
			}
			// Fix Tag Barrel Background Kong memes
			*(int*)(0x806839F0) = 0x0C000000 | (((int)&tagBarrelBackgroundKong & 0xFFFFFF) >> 2);
			// DK Face Puzzle
			int dk_reg_vals[] = {0x80,0x95,0x83,0x82}; // 0 = r0, 1 = s5, 2 = v1, 3 = v0
			*(unsigned char*)(0x8064AD01) = dk_reg_vals[(int)Rando.dk_face_puzzle_init[2]];
			*(unsigned char*)(0x8064AD05) = dk_reg_vals[(int)Rando.dk_face_puzzle_init[5]];
			*(unsigned char*)(0x8064AD09) = dk_reg_vals[(int)Rando.dk_face_puzzle_init[7]];
			*(unsigned char*)(0x8064AD11) = dk_reg_vals[(int)Rando.dk_face_puzzle_init[0]];
			*(unsigned char*)(0x8064AD15) = dk_reg_vals[(int)Rando.dk_face_puzzle_init[1]];
			*(unsigned char*)(0x8064AD19) = dk_reg_vals[(int)Rando.dk_face_puzzle_init[3]];
			*(unsigned char*)(0x8064AD1D) = dk_reg_vals[(int)Rando.dk_face_puzzle_init[4]];
			*(unsigned char*)(0x8064AD21) = dk_reg_vals[(int)Rando.dk_face_puzzle_init[6]];
			*(unsigned char*)(0x8064AD29) = dk_reg_vals[(int)Rando.dk_face_puzzle_init[8]];
			// Chunky Face Puzzle
			int chunky_reg_vals[] = {0x40,0x54,0x48,0x44}; // 0 = r0, 1 = s4, 2 = t0, 3 = a0
			*(unsigned char*)(0x8064A2D5) = chunky_reg_vals[(int)Rando.chunky_face_puzzle_init[2]];
			*(unsigned char*)(0x8064A2DD) = chunky_reg_vals[(int)Rando.chunky_face_puzzle_init[6]];
			*(unsigned char*)(0x8064A2ED) = chunky_reg_vals[(int)Rando.chunky_face_puzzle_init[0]];
			*(unsigned char*)(0x8064A2F1) = chunky_reg_vals[(int)Rando.chunky_face_puzzle_init[1]];
			*(unsigned char*)(0x8064A2F5) = chunky_reg_vals[(int)Rando.chunky_face_puzzle_init[3]];
			*(unsigned char*)(0x8064A2F9) = chunky_reg_vals[(int)Rando.chunky_face_puzzle_init[4]];
			*(unsigned char*)(0x8064A2FD) = chunky_reg_vals[(int)Rando.chunky_face_puzzle_init[5]];
			*(unsigned char*)(0x8064A301) = chunky_reg_vals[(int)Rando.chunky_face_puzzle_init[7]];
			*(unsigned char*)(0x8064A305) = chunky_reg_vals[(int)Rando.chunky_face_puzzle_init[8]];
			// Realign HUD
			/*
				Item: CB | Coords: 0x1E, 0x26 | X: 0x806F84EE | Y: 0x806F84FE
				Item: Coins | Coords: 0x122, 0x26 | X: 0x806F88CA | Y: 0x806F88CE
				Item: Ammo | Coords: 0x122, 0x48 | X: 0x806F86C6 | Y: 0x806F86CA
				Item: Homing Ammo | Coords: 0x122, 0x48 | X: 0x806F873A | Y: 0x806F873E
				Item: Oranges | Coords: 0x122, 0x6A | X: 0x806F87A6 | Y: 0x806F87AA
				Item: Crystals | Coords: 0x122, 0x8C | X: 0x806F868E | Y: 0x806F8692
				Item: Film | Coords: 0x122, 0xD0 | X: 0x806F8812 | Y: 0x806F8816
				Item: Instrument | Coords: 0x122, 0xAE | X: 0x806F893A | Y: 0x806F893E
				Item: GB Character | Coords: 0x1E, 0x48 | X: 0x806F857E | Y: 0x806F858E
				Item: GB | Coords: 0x7A, 0xD0 | X: 0x806F8642 | Y: 0x806F8646
				Item: Medal (Multi CB) | Coords: 0x52, 0xD0 | X: 0x806F8606 | Y: 0x806F860A
				Item: Race Coin | Coords: 0x122, 0x26 | X: 0x806F8852 | Y: 0x806F8856
				Item: Blueprint | Coords: 0xC2, 0xD0 | X: 0x806F85CA | Y: 0x806F85CE
				Item: CB T&S | Coords: 0x122, 0x26 | X: 0x806F8536 | Y: 0x806F853A
				Item: Unk | Coords: 0x1E, 0x26 | X: 0x806F897A | Y: 0x806F897E
			*/
			int y_spacing = 22;
			int y_bottom = 0xD0;
			*(short*)(0x806F893E) = y_bottom - (1 * y_spacing); // Instrument
			*(short*)(0x806F8692) = y_bottom - (2 * y_spacing); // Crystals
			*(short*)(0x806F87AA) = y_bottom - (3 * y_spacing); // Oranges
			*(short*)(0x806F86CA) = y_bottom - (4 * y_spacing); // Ammo
			*(short*)(0x806F873E) = y_bottom - (4 * y_spacing); // Homing Ammo
			// Multibunch HUD
			if (Rando.quality_of_life.hud_bp_multibunch) {
				*(short*)(0x806F860A) = y_bottom - (5 * y_spacing); // Multi CB
				*(int*)(0x806F97D8) = 0x0C000000 | (((int)&getHUDSprite_HUD & 0xFFFFFF) >> 2); // Change Sprite
				*(int*)(0x806F6BF0) = 0x0C000000 | (((int)&preventMedalHUD & 0xFFFFFF) >> 2); // Prevent Model Two Medals showing HUD
				*(short*)(0x806F8606) = 0x122; // Position X
				*(int*)(0x806F862C) = 0x4600F306; // MOV.S $f12, $f30
				*(int*)(0x806F8634) = 0x4600A386; // MOV.S $f14, $f20
				*(int*)(0x806F98E4) = 0x0C000000 | (((int)&initHUDDirection & 0xFFFFFF) >> 2); // HUD Direction
				*(int*)(0x806F9A00) = 0x0C000000 | (((int)&initHUDDirection & 0xFFFFFF) >> 2); // HUD Direction
				*(int*)(0x806F9A78) = 0x0C000000 | (((int)&initHUDDirection & 0xFFFFFF) >> 2); // HUD Direction
				*(int*)(0x806F9BC0) = 0x0C000000 | (((int)&initHUDDirection & 0xFFFFFF) >> 2); // HUD Direction
				*(int*)(0x806F9D14) = 0x0C000000 | (((int)&initHUDDirection & 0xFFFFFF) >> 2); // HUD Direction
				*(int*)(0x806FA62C) = 0; // NOP: Enable Number Rendering
				*(int*)(0x806FA56C) = 0; // NOP: Prevent opacity check
			}
			if (Rando.quality_of_life.homing_balloons) {
				// Make homing ammo target balloons
				*(short*)(0x80694F6A) = 10; // Coconut
				*(short*)(0x80692B82) = 10; // Peanuts
				*(short*)(0x8069309A) = 10; // Grape
				*(short*)(0x80695406) = 10; // Feather
				*(short*)(0x80694706) = 10; // Pineapple
			}
			// GetOut Timer
			*(unsigned short*)(0x806B7ECA) = 125; // 0x8078 for center-bottom ms timer
			if (Rando.misc_cosmetic_on) {
				for (int i = 0; i < 8; i++) {
					SkyboxBlends[i].top.red = Rando.skybox_colors[i].red;
					SkyboxBlends[i].top.green = Rando.skybox_colors[i].green;
					SkyboxBlends[i].top.blue = Rando.skybox_colors[i].blue;
					float rgb[3] = {0,0,0};
					float rgb_backup[3] = {0,0,0};
					rgb[0] = Rando.skybox_colors[i].red;
					rgb[1] = Rando.skybox_colors[i].green;
					rgb[2] = Rando.skybox_colors[i].blue;
					for (int j = 0; j < 3; j++) {
						rgb_backup[j] = rgb[j];
						rgb[j] *= 1.2f;
					}
					int exceeded = 0;
					for (int j = 0; j < 3; j++) {
						if (rgb[j] > 255.0f) {
							exceeded = 1;
						}
					}
					if (exceeded) {
						for (int j = 0; j < 3; j++) {
							rgb[j] = rgb_backup[j] * 0.8f;
						}
					}
					SkyboxBlends[i].bottom.red = rgb[0];
					SkyboxBlends[i].bottom.green = rgb[1];
					SkyboxBlends[i].bottom.blue = rgb[2];
					for (int j = 0; j < 2; j++) {
						SkyboxBlends[i].unk[j].red = rgb[0];
						SkyboxBlends[i].unk[j].green = rgb[1];
						SkyboxBlends[i].unk[j].blue = rgb[2];
					}
				}
			}
			LoadedHooks = 1;
		}
	}
}

void quickInit(void) {
	initHack(1);
	if (Rando.quality_of_life.fast_boot) {
		initiateTransitionFade(0x51, 0, 5);
		CutsceneWillPlay = 0;
		Gamemode = 5;
		Mode = 5;
		StorySkip = 1;
		*(char*)(0x80745D20) = 7;
	}
}