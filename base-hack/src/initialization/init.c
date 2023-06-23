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

static char music_storage[MUSIC_SIZE];

typedef struct musicInfo {
	/* 0x000 */ short data[0xB0];
} musicInfo;

typedef enum song_types {
	/* 0x000 */ SONGTYPE_BGM,
	/* 0x001 */ SONGTYPE_EVENT,
	/* 0x002 */ SONGTYPE_MAJORITEM,
	/* 0x003 */ SONGTYPE_MINORITEM,
} song_types;

void fixMusicRando(void) {
	/**
	 * @brief Initialize Music Rando so that the data for each song is correct.
	 * Without this, the game will crash from incorrect properties to what the song is expecting.
	 */
	// Music
	if (Rando.music_rando_on) {
		// Type bitfields
		int size = SONG_COUNT << 1;
		musicInfo* write_space = dk_malloc(size);
		int* file_size;
		*(int*)(&file_size) = size;
		copyFromROM(0x1FFF000,write_space,&file_size,0,0,0,0);
		// Type indexes
		size = SONG_COUNT;
		char* write_space_0 = dk_malloc(size);
		*(int*)(&file_size) = size;
		copyFromROM(0x1FEE200,write_space_0,&file_size,0,0,0,0);
		for (int i = 0; i < SONG_COUNT; i++) {
			// Handle Bitfield
			int subchannel = (write_space->data[i] & 6) >> 1;
			int channel = (write_space->data[i] & 0x78) >> 3;
			songData[i] &= 0xFF81;
			songData[i] |= (subchannel & 3) << 1;
			songData[i] |= (channel & 0xF) << 3;

			// Handle Type Index
			if (write_space_0[i] > -1) {
				song_types type = write_space_0[i];
				int volume = 0;
				if (type == SONGTYPE_BGM) {
					volume = 23000;
				} else if (type == SONGTYPE_MAJORITEM) {
					volume = 27000;
				} else {
					// Event or Minor Item
					volume = 25000;
				}
				songVolumes[i] = volume;
			}
		}
		complex_free(write_space);
		complex_free(write_space_0);

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

float getOscillationDelta(void) {
	return 0.5f;
}

void loadHooks(void) {
	loadSingularHook(0x8063EE08, &InstanceScriptCheck);
	loadSingularHook(0x80731168, &checkFlag_ItemRando);
	loadSingularHook(0x807312F8, &setFlag_ItemRando);
	loadSingularHook(0x8069840C, &VineCode);
	loadSingularHook(0x80698420, &VineShowCode);
	loadSingularHook(0x8063ED7C, &HandleSlamCheck);
	loadSingularHook(0x806FF384, &ModifyCameraColor);
	loadSingularHook(0x8061E684, &SkipCutscenePans);
	loadSingularHook(0x80648364, &ShopImageHandler);
	loadSingularHook(0x806EA70C, &InvertCameraControls);
	loadSingularHook(0x8061CE38, &PlayCutsceneVelocity);
	loadSingularHook(0x80677C14, &FixPufftossInvalidWallCollision);
	loadSingularHook(0x8060DFF4, &SaveToFileFixes);
	loadSingularHook(0x806F6EA0, &BarrelMovesFixes);
	loadSingularHook(0x806E4930, &ChimpyChargeFix);
	loadSingularHook(0x806E48AC, &OStandFix);
	loadSingularHook(0x8067ECB8, &HunkyChunkyFix2);
	loadSingularHook(0x805FC3FC, &EarlyFrameCode);
	loadSingularHook(0x8071417C, &displayListCode);
	loadSingularHook(0x806F8610, &GiveItemPointerToMulti);
	loadSingularHook(0x806F88C8, &CoinHUDReposition);
	loadSingularHook(0x8060005C, &getLobbyExit);
	loadSingularHook(0x806C9A7C, &damageMultiplerCode);
	loadSingularHook(0x8060DEF4, &SaveHelmHurryCheck);
	if (Rando.warp_to_isles_enabled) {
		loadSingularHook(0x806A995C, &PauseExtraSlotCode);
		loadSingularHook(0x806A9818, &PauseExtraHeight);
		loadSingularHook(0x806A87BC, &PauseExtraSlotClamp0);
		loadSingularHook(0x806A8760, &PauseExtraSlotClamp1);
		loadSingularHook(0x806A8804, &PauseExtraSlotCustomCode);
		loadSingularHook(0x806A9898, &PauseCounterCap);
	}
	loadSingularHook(0x806F3E74, &AutowalkFix);
	loadSingularHook(0x80610948, &DynamicCodeFixes);
	if (Rando.perma_lose_kongs) {
		loadSingularHook(0x80682F2C, &permaLossTagCheck);
		loadSingularHook(0x80683620, &permaLossTagSet);
		loadSingularHook(0x806840C4, &permaLossTagDisplayCheck);
	}
	loadSingularHook(0x80689534, &tagPreventCode);
	if (Rando.resolve_bonus) {
		//loadSingularHook(0x80680D10, &destroyAllBarrelsCode);
	}
	loadSingularHook(0x806BD328, &KeyCompressionCode);
	loadSingularHook(0x8067B684, &CannonForceCode);
	loadSingularHook(0x806F9F88, &HUDDisplayCode);
	loadSingularHook(0x806E22B0, &HomingDisable);
	loadSingularHook(0x806EB574, &HomingHUDHandle);
	loadSingularHook(0x806324C4, &DKCollectableFix);
	loadSingularHook(0x806AF70C, &GuardDeathHandle);
	loadSingularHook(0x807132BC, &NinWarpCode);
	if (Rando.quality_of_life.textbox_hold) {
		loadSingularHook(0x8070E83C, &TextHandler);
	}
	loadSingularHook(0x806AE55C, &GuardAutoclear);
	loadSingularHook(0x80637148, &ObjectRotate);
	if (Rando.item_rando) {
		loadSingularHook(0x806A6708, &SpriteFix);
	}
	loadSingularHook(0x806A86FC, &PauseControl_Control);
	loadSingularHook(0x806AA414, &PauseControl_Sprite);
	if (Rando.quality_of_life.brighten_mmm_enemies) {
		loadSingularHook(0x80631380, &brightenMMMEnemies);
	}
	if (Rando.krusha_slot >- 1) {
		loadSingularHook(0x806F97B8, &FixKrushaAmmoHUDColor);
		loadSingularHook(0x806F97E8, &FixKrushaAmmoHUDSize);
	}
}

void initHack(int source) {
	/**
	 * @brief Initialize Hack
	 * 
	 * @param source 0 = CFuncLoop, 1 = ROM Boot
	 * 
	 */
	if (LoadedHooks == 0) {
		if ((source == 1) || (CurrentMap == MAP_NINTENDOLOGO)) {
			DebugInfoOn = 1;
			if (Rando.fast_start_beginning) {
				*(int*)(0x80714540) = 0;
			}
			*(int*)(0x80731F78) = 0; // Debug 1 Column
			*(int*)(0x8060E04C) = 0; // Prevent moves overwrite
			*(short*)(0x8060DDAA) = 0; // Writes readfile data to moves
			*(short*)(0x806C9CDE) = 7; // GiveEverything, write to bitfield. Seems to be unused but might as well
			*(int*)(0x8076BF38) = (int)&music_storage[0]; // Increase music storage
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
			initPathExpansion();
			for (int i = 0; i < 7; i++) {
				SwitchLevel[i] = Rando.slam_level[i];
			}
			if (Rando.quality_of_life.brighten_mmm_enemies) {
				MMMEnemiesBrightened = 1;
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
			initActor(NEWACTOR_JETPACITEMOVERLAY, 1, &getNextMoveText, ACTORMASTER_CONTROLLER, 0, 0, 0x10, 324);
			// Kong Rando
			initKongRando();
			initFiles();
			writeFunction(0x8060CB7C, &fixChimpyCamBug);
            
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
				actor_health_damage[251].init_health = 3; // Spider Boss Health
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
				writeFunction(0x80681158, &completeBonus); // Modify Function Call
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
			loadHooks();
			loadExtraHooks();
			// Moves & Prices
			fixTBarrelsAndBFI(1);
			// Place Move Data
			moveTransplant();
			priceTransplant();

			initStatistics();
			if (Rando.disable_boss_kong_check) {
				*(int*)(0x8064EC00) = 0x24020001;
			}
			actor_functions[70] = &newCounterCode;
			*(short*)(0x8074DC84) = 0x53; // Increase PAAD size
			fixMusicRando();
			*(int*)(0x80748014) = (int)&spawnWrinklyWrapper; // Change function to include setFlag call	
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
			initSmallerQuadChecks();
			writeFunction(0x805FEBC0, &parseCutsceneData); // modifyCutsceneHook
			writeFunction(0x807313A4, &checkVictory_flaghook); // perm flag set hook
			*(int*)(0x80748088) = (int)&CrownDoorCheck; // Update check on Crown Door
			// New Mermaid Checking Code
			writeFunction(0x806C3B5C, &mermaidCheck); // Mermaid Check
			*(short*)(0x806C3B64) = 0x1000; // Force to branch
			*(short*)(0x806C3BD0) = 0x1000; // Force to branch
			*(int*)(0x806C3C20) = 0; // NOP - Cancel control state write
			*(int*)(0x806C3C2C) = 0; // NOP - Cancel control state progress write
			if (Rando.helm_hurry_mode) {
				*(int*)(0x80713CCC) = 0; // Prevent Helm Timer Disable
				*(int*)(0x80713CD8) = 0; // Prevent Shutdown Song Playing
				*(short*)(0x8071256A) = 15; // Init Helm Timer = 15 minutes
				writeFunction(0x807125A4, &initHelmHurry); // Change write
				writeFunction(0x80713DE0, &finishHelmHurry); // Change write
				*(int*)(0x807125CC) = 0; // Prevent Helm Timer Overwrite
				*(short*)(0x807095BE) = 0x2D4; // Change Zipper with K. Rool Laugh
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
				*(short*)(0x806BC582) = 30; // Ice Tomato Timer
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
				writeFunction(0x8069E154, &getWrinklyLevelIndex); // Modify Function Call
			}
			// Mill Lever
			if (Rando.mill_lever_order[0] > 0) {
				int sequence_length = 0;
				int sequence_ended = 0;
				for (int i = 0; i < 5; i++) {
					ReverseMillLeverOrder[i] = 0;
					if (!sequence_ended) {
						if (Rando.mill_lever_order[i] == 0) {
							sequence_ended = 1;
						} else {
							sequence_length += 1;
						}
					}
				}
				*(short*)(0x8064E4CE) = sequence_length;
				for (int i = 0; i < sequence_length; i++) {
					ReverseMillLeverOrder[i] = Rando.mill_lever_order[(sequence_length - 1) - i];
				}
			}
			// Crypt Lever
			if (Rando.crypt_lever_order[0] > 0) {
				for (int i = 0; i < 3; i++) {
					ReverseCryptLeverOrder[i] = Rando.crypt_lever_order[2 - i];
				}
			}
			// Object Instance Scripts
			*(int*)(0x80748064) = (int)&change_object_scripts;
			*(int*)(0x806416BC) = 0; // Prevent parent map check in cross-map object change communications
			// Deathwarp Handle
			writeFunction(0x8071292C, &WarpHandle); // Check if in Helm, in which case, apply transition
			// New Guard Code
			*(short*)(0x806AF75C) = 0x1000;
			// Gold Beaver Code
      		actor_functions[212] = (void*)0x806AD54C; // Set as Blue Beaver Code
			writeFunction(0x806AD750, &beaverExtraHitHandle); // Remove buff until we think of something better
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
				// writeFunction(0x806ADDC0, &handleSpiderTrapCode);
				*(short*)(0x806B12DA) = 0x3A9; // Kasplat Shockwave Chance
				*(short*)(0x806B12FE) = 0x3B3; // Kasplat Shockwave Chance
				actor_health_damage[259].init_health = 9; // Increase Guard Health
			}
			// Fix some silk memes
			*(int*)(0x806ADA6C) = 0;
			writeFunction(0x806ADA70, &HandleSpiderSilkSpawn);
			*(int*)(0x806ADA78) = 0;
			// Fix spider crashes
			int fixed_anim = 0x2F5;
			*(short*)(0x8075F46C) = fixed_anim;
			*(short*)(0x806ADA26) = fixed_anim; // This might fix spawning if set on non-init
			*(short*)(0x806ADA2A) = fixed_anim;
			*(short*)(0x806ADA32) = fixed_anim;
			*(short*)(0x806ADBC6) = fixed_anim;
			*(short*)(0x806ADC66) = fixed_anim;
			*(short*)(0x806ADD3A) = fixed_anim;
			// Oscillation Effects
			if (Rando.remove_oscillation_effects) {
				*(int*)(0x80661B54) = 0; // Remove Ripple Timer 0
				*(int*)(0x80661B64) = 0; // Remove Ripple Timer 1
				*(int*)(0x8068BDF4) = 0; // Disable rocking in Seasick Ship
				*(short*)(0x8068BDFC) = 0x1000; // Disable rocking in Mech Fish
				// *(int*)(0x806609DC) = 0x44802000; // Change ripple oscillation X to 0 (mtc1 $zero, $f4)
				// *(int*)(0x806609EC) = 0x44805000; // Change ripple oscillation Z to 0 (mtc1 $zero, $f10)
				writeFunction(0x80660994, &getOscillationDelta);
				writeFunction(0x806609BC, &getOscillationDelta);
			}
			// Slow Turn Fix
			writeFunction(0x806D2FC0, &fixRBSlowTurn);
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
			writeFunction(0x80712EC4, &postKRoolSaveCheck);
			// Opacity fixes
			writeFunction(0x806380B0, &handleModelTwoOpacity);
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
				writeFunction(0x806F5BE8, &tagAnywhereAmmo);
				// Bunch
				*(short*)(0x806F59A8) = 0x1000;
				writeFunction(0x806F5A08, &tagAnywhereBunch);

				*(int*)(0x806F6CAC) = 0x9204001A; // LBU $a0, 0x1A ($s0)
				*(int*)(0x806F6CB0) = 0x86060002; // LH $a2, 0x2 ($s0)
				writeFunction(0x806F6CB4, &tagAnywhereInit);
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
			SFXVolume = Rando.default_sfx_volume;
			MusicVolume = Rando.default_music_volume;
			ScreenRatio = Rando.default_screen_ratio;
			SoundType = Rando.default_sound_type;
			int sound_subtype = 1;
			if (SoundType == 0) {
				sound_subtype = 2;
			} else if (SoundType == 2) {
				sound_subtype = 4;
			}
			adjustSFXType_Internal(sound_subtype);
			for (int i = 0; i < 4; i++) {
				alterSFXVolume(i, (SFXVolume * 25000) / 40);
			}
			alterMusicVolume(0);
			alterMusicVolume(2);
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
		initiateTransitionFade(MAP_NFRTITLESCREEN, 0, 5);
		CutsceneWillPlay = 0;
		Gamemode = GAMEMODE_MAINMENU;
		Mode = 5;
		StorySkip = 1;
		*(char*)(0x80745D20) = 7;
	}
}

#define PATH_CAP 64
static int balloon_path_pointers[PATH_CAP];

void initPathExpansion(void) {
	*(short*)(0x80722E56) = getHi(&balloon_path_pointers[0]);
	*(short*)(0x80722E7A) = getLo(&balloon_path_pointers[0]);
	*(short*)(0x80722E92) = PATH_CAP;
	*(short*)(0x80722FF6) = getHi(&balloon_path_pointers[0]);
	*(short*)(0x80722FFE) = getLo(&balloon_path_pointers[0]);
	*(short*)(0x80723026) = getHi(&balloon_path_pointers[0]);
	*(short*)(0x8072302E) = getLo(&balloon_path_pointers[0]);
	*(short*)(0x80723CF6) = getHi(&balloon_path_pointers[0]);
	*(short*)(0x80723D06) = getLo(&balloon_path_pointers[0]);
	*(short*)(0x80723FEA) = getHi(&balloon_path_pointers[0]);
	*(short*)(0x80723FEE) = getLo(&balloon_path_pointers[0]);
	*(short*)(0x807241CE) = getHi(&balloon_path_pointers[0]);
	*(short*)(0x807241DE) = getLo(&balloon_path_pointers[0]);
	*(short*)(0x80724312) = getHi(&balloon_path_pointers[0]);
	*(short*)(0x8072431E) = getLo(&balloon_path_pointers[0]);
	*(short*)(0x807245DE) = getHi(&balloon_path_pointers[0]);
	*(short*)(0x807245E6) = getLo(&balloon_path_pointers[0]);
}