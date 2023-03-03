/**
 * @file init.c
 * @author Ballaam
 * @author KillKlli
 * @author OnlySpaghettiCode
 * @brief Initialize ROM
 * @version 0.1
 * @date 2021-12-06
 * 
 * @copyright Copyright (c) 2021
 * 
 */
#include "../../include/common.h"

typedef struct musicInfo {
	/* 0x000 */ short data[0xB0];
} musicInfo;

void fixMusicRando(void) {
	/**
	 * @brief Initialize Music Rando so that the data for each song is correct.
	 * Without this, the game will crash from incorrect properties to what the song is expecting.
	 */
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
	/**
	 * @brief Write our custom end sequence
	 */
	int size = 0x84;
	int* file_size;
	*(int*)(&file_size) = size;
	copyFromROM(0x1FFF800,(int*)0x807506D0,&file_size,0,0,0,0);
}

void initHack(int source) {
	/**
	 * @brief Initialize Hack
	 * 
	 * @param source 0 = CFuncLoop, 1 = ROM Boot
	 * 
	 */
	if (LoadedHooks == 0) {
		if ((source == 1) || (CurrentMap == 0x28)) {
			DebugInfoOn = 1;
			if (Rando.fast_start_beginning) {
				*(int*)(0x80714540) = 0;
			}
			*(int*)(0x80731F78) = 0; // Debug 1 Column
			*(int*)(0x8060E04C) = 0; // Prevent moves overwrite
			*(short*)(0x8060DDAA) = 0; // Writes readfile data to moves
			*(short*)(0x806C9CDE) = 7; // GiveEverything, write to bitfield. Seems to be unused but might as well
			
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
			initActorExpansion();
			for (int i = 0; i < 7; i++) {
				SwitchLevel[i] = Rando.slam_level[i];
			}
			if (Rando.fairy_rando_on) {
				// Fairy Location Table
				int fairy_size = 20<<2;
				fairy_location_item* fairy_write = dk_malloc(fairy_size);
				int* fairy_file_size;
				*(int*)(&fairy_file_size) = fairy_size;
				copyFromROM(0x1FFC000,fairy_write,&fairy_file_size,0,0,0,0);
				for (int i = 0; i < (fairy_size >> 2); i++) {
					for (int j = 0; j < 0x1F; j++) {
						if (charspawnerflags[j].tied_flag == fairy_write[i].flag) {
							charspawnerflags[j].map = fairy_write[i].map;
							charspawnerflags[j].spawner_id = fairy_write[i].id;
						}
					}
				}
			}
			// New Actors
			// 0x11 = 45
			// 0x0 =
			initActor(NEWACTOR_NINTENDOCOIN, 1, &ninCoinCode, ACTORMASTER_SPRITE, 0, 1, 8, 45);
			initActor(NEWACTOR_RAREWARECOIN, 1, &rwCoinCode, ACTORMASTER_SPRITE, 0, 1, 8, 45);
			initActor(NEWACTOR_NULL, 1, &NothingCode, ACTORMASTER_SPRITE, 0, 1, 8, 0);
			initActor(NEWACTOR_MEDAL, 1, &medalCode, ACTORMASTER_SPRITE, 0, 1, 8, 45);
			for (int i = 0; i < 6; i++) {
				initActor(NEWACTOR_POTIONDK + i, 1, &PotionCode, ACTORMASTER_3D, 0, 1, 8, 45);
				if (i < 5) {
					initActor(NEWACTOR_KONGDK + i, 1, &KongDropCode, ACTORMASTER_3D, 0, 1, 8, 45);
				}
			}
			initActor(NEWACTOR_BEAN, 1, &beanCode, ACTORMASTER_SPRITE, 0, 1, 8, 45);
			initActor(NEWACTOR_PEARL, 1, &pearlCode, ACTORMASTER_SPRITE, 0, 1, 8, 45);
			initActor(NEWACTOR_FAIRY, 1, &fairyDuplicateCode, ACTORMASTER_3D, 0, 1, 8, 45);
			initActor(NEWACTOR_FAKEITEM, 1, &FakeGBCode, ACTORMASTER_3D, 0, 1, 8, 45);
			// Kong Rando
			initKongRando();
			initFiles();
            
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
				actor_health_damage[236].init_health = 44; // Dogadon Health: 3 + (62 * (2 / 3))
				actor_health_damage[185].init_health = 3; // Dillo Health
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
            initQoL(); // Also includes initializing spawn point and HUD realignment
            initItemRando();
			initCosmetic();
			initStackTrace();
			initTextChanges();

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
			actor_functions[70] = &newCounterCode;
			*(short*)(0x8074DC84) = 0x53; // Increase PAAD size
			fixMusicRando();			
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
				*(int*)(0x807125A4) = 0x0C000000 | (((int)&initHelmHurry & 0xFFFFFF) >> 2); // Change write
				*(int*)(0x807125CC) = 0; // Prevent Helm Timer Overwrite
			}
			if (Rando.always_show_coin_cbs) {
				*(int*)(0x806324D4) = 0x24020001; // ADDIU $v0, $r0, 1 // Disable kong flag check
			}
			if (Rando.version == 0) {
				// Disable Graphical Debugger
				*(int*)(0x8060EEE0) = 0x240E0000; // ADDIU $t6, $r0, 0
			}
			if (Rando.fast_gbs) {
				*(short*)(0x806BBB22) = 0x0005; // Chunky toy box speedup
				*(short*)(0x806C58D6) = 0x0008; //Owl ring amount
				*(short*)(0x806C5B16) = 0x0008;
				*(int*)(0x806BEDFC) = 0; //Spawn banana coins on beating rabbit 2 (Beating round 2 branches to banana coin spawning label before continuing)
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
			// Object Instance Scripts
			*(int*)(0x80748064) = (int)&change_object_scripts;
			*(int*)(0x806416BC) = 0; // Prevent parent map check in cross-map object change communications
			// Deathwarp Handle
			*(int*)(0x8071292C) = 0x0C000000 | (((int)&WarpHandle & 0xFFFFFF) >> 2); // Check if in Helm, in which case, apply transition
			// New Guard Code
			*(short*)(0x806AF75C) = 0x1000;
			// Gold Beaver Code
      		actor_functions[212] = (void*)0x806AD54C; // Set as Blue Beaver Code
			*(int*)(0x806AD750) = 0x0C000000 | (((int)&beaverExtraHitHandle & 0xFFFFFF) >> 2); // Remove buff until we think of something better
			// Move Text Code
			actor_functions[324] = &getNextMoveText;
			actor_functions[320] = &getNextMoveText;
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
			initPauseMenu(); // Changes to enable more items
			// Spider Projectile
			*(int*)(0x806CBD78) = 0x18400005; // BLEZ $v0, 0x5 - Decrease in health occurs if trap bubble active
			if (Rando.hard_enemies) {
				*(int*)(0x806ADDC0) = 0x0C000000 | (((int)&handleSpiderTrapCode & 0xFFFFFF) >> 2);
				*(short*)(0x806B12DA) = 0x3A9; // Kasplat Shockwave Chance
				*(short*)(0x806B12FE) = 0x3B3; // Kasplat Shockwave Chance
				actor_health_damage[259].init_health = 9; // Increase Guard Health
			}
			// Oscillation Effects
			if (Rando.remove_oscillation_effects) {
				*(int*)(0x80661B54) = 0; // Remove Ripple Timer 0
				*(int*)(0x80661B64) = 0; // Remove Ripple Timer 1
				*(int*)(0x8068BDF4) = 0; // Disable rocking in Seasick Ship
				*(short*)(0x8068BDFC) = 0x1000; // Disable rocking in Mech Fish
				*(int*)(0x806609DC) = 0x44802000; // Change ripple oscillation X to 0 (mtc1 $zero, $f4)
				*(int*)(0x806609EC) = 0x44805000; // Change ripple oscillation Z to 0 (mtc1 $zero, $f10)
			}
			// Slow Turn Fix
			*(int*)(0x806D2FC0) = 0x0C000000 | (((int)&fixRBSlowTurn & 0xFFFFFF) >> 2);
			// CB Bunch
			*(int*)(0x806A65B8) = 0x240A0006; // Always ensure chunky bunch sprite (Rock Bunch)
			// Coins
			*(int*)(0x806A64B0) = 0x240A0004; // Always ensure lanky coin sprite (Rabbit Race 1 Reward)

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
			// LZ Save
			*(int*)(0x80712EC4) = 0x0C000000 | (((int)&postKRoolSaveCheck & 0xFFFFFF) >> 2);
			// Opacity fixes
			*(int*)(0x806380B0) = 0x0C000000 | (((int)&handleModelTwoOpacity & 0xFFFFFF) >> 2);
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

				// initTagAnywhere();
			}
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
			insertROMMessages();
			LoadedHooks = 1;
		}
	}
}

void quickInit(void) {
	/**
	 * @brief Quick Initialization Process. Initializes Hack and, if fast boot is on, transitions to Win95 Screen
	 */
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