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
char music_types[SONG_COUNT];

typedef struct musicInfo {
	/* 0x000 */ short data[0xB0];
} musicInfo;

void writeFunctionLoop(void) {
	writeFunction(0x805FC164, (int)&cFuncLoop);
}

void fixMusicRando(void) {
	/**
	 * @brief Initialize Music Rando so that the data for each song is correct.
	 * Without this, the game will crash from incorrect properties to what the song is expecting.
	 */
	if (Rando.music_rando_on) {
		// Type bitfields
		int size = SONG_COUNT << 1;
		musicInfo* write_space = getFile(size, 0x1FFF000);
		// Type indexes
		size = SONG_COUNT;
		char* write_space_0 = getFile(size, 0x1FEE200);
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
		*(short*)(0x806CA97E) = 0x560 | ((songData[0x6B] >> 1) & 3); // Baboon Balloon
		*(float*)(0x807565D8) = 1.0f; // Funky and Candy volumes
		*(int*)(0x80604B50) = 0; // Disable galleon outside track isolation
		*(int*)(0x80604A54) = 0; // Disable galleon outside track isolation
		complex_free(write_space);
		complex_free(write_space_0);
	}
	/*
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
			music_types[i] = write_space_0[i];
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
	*/
}

void writeEndSequence(void) {
	/**
	 * @brief Write our custom end sequence
	 */
	int size = 0x84;
	copyFromROM(0x1FFF800,(int*)0x807506D0,&size,0,0,0,0);
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
	loadSingularHook(0x8060DEF4, &SaveHelmHurryCheck);
	if (Rando.warp_to_isles_enabled) {
		loadSingularHook(0x806A995C, &PauseExtraSlotCode);
		loadSingularHook(0x806A9818, &PauseExtraHeight);
		loadSingularHook(0x806A87BC, &PauseExtraSlotClamp0);
		loadSingularHook(0x806A8760, &PauseExtraSlotClamp1);
		loadSingularHook(0x806A8804, &PauseExtraSlotCustomCode);
		loadSingularHook(0x806A9898, &PauseCounterCap);
	} else if (Rando.true_widescreen) {
		*(short*)(0x806A981A) = (SCREEN_HD_FLOAT * 2) - 72;
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
	if (Rando.enemy_item_rando){
		loadSingularHook(0x806680b4, checkBeforeApplyingQuicksand);
		*(int*)(0x806680b8) = 0x8E2C0058; // LW $t4, 0x58 ($s1)
	}
	loadSingularHook(0x806A7474, &disableHelmKeyBounce);
	if (MenuDarkness != 0) {
		loadSingularHook(0x807070A0, &RecolorMenuBackground);
	}
	if (Rando.balanced_krool_reqs) {
		loadSingularHook(0x8067FE28, &makeCannonsRequireBlast);
		loadSingularHook(0x806806B4, &fixCannonBlastNoclip);
	}
	loadSingularHook(0x806FC990, &ApplyTextRecolorHints);
	loadSingularHook(0x80600674, &updateLag);

	// Beaver Bother fix
	loadSingularHook(0x806AD740, &unscareBeaver);
	loadSingularHook(0x806AD728, &scareBeaver);
	*(short*)(0x806B674E) = 0xC; // Increase the scare duration
}

void skipDKTV(void) {
	setNextTransitionType(1);
	initiateTransition(MAP_MAINMENU, 0);
	Mode = GAMEMODE_MAINMENU;
}

void initHack(int source) {
	/**
	 * @brief Initialize Hack
	 * 
	 * @param source 0 = cFuncLoop, 1 = ROM Boot
	 * 
	 */
	if (LoadedHooks == 0) {
		if ((source == 1) || (CurrentMap == MAP_NINTENDOLOGO)) {
			DebugInfoOn = 1;
			if (Rando.fast_start_beginning) {
				*(int*)(0x80714540) = 0;
			}
			*(int*)(0x8076BF38) = (int)&music_storage[0]; // Increase music storage
			WidescreenEnabled = Rando.true_widescreen;
			grab_lock_timer = -1;
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
				fairy_location_item* fairy_write = getFile(fairy_size, 0x1FFC000);
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
			writeFunction(0x8060CB7C, &fixChimpyCamBug);
            
			if (Rando.short_bosses) {
				actor_health_damage[236].init_health = 44; // Dogadon Health: 3 + (62 * (2 / 3))
				actor_health_damage[185].init_health = 3; // Dillo Health
				actor_health_damage[251].init_health = 3; // Spider Boss Health
			}
			if (Rando.resolve_bonus) {
				writeFunction(0x80681158, &completeBonus); // Modify Function Call
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
			
			actor_functions[70] = &newCounterCode;
			
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
			if (Rando.helm_hurry_mode) {
				writeFunction(0x806A8A18, &QuitGame); // Save game on quit
				*(int*)(0x80713CCC) = 0; // Prevent Helm Timer Disable
				*(int*)(0x80713CD8) = 0; // Prevent Shutdown Song Playing
				*(short*)(0x8071256A) = 15; // Init Helm Timer = 15 minutes
				writeFunction(0x807125A4, &initHelmHurry); // Change write
				writeFunction(0x80713DE0, &finishHelmHurry); // Change write
				*(int*)(0x807125CC) = 0; // Prevent Helm Timer Overwrite
				*(short*)(0x807095BE) = 0x2D4; // Change Zipper with K. Rool Laugh
			}
			int kko_phase_rando = 0;
			for (int i = 0; i < 3; i++) {
				KKOPhaseOrder[i] = Rando.kut_out_phases[i];
				if (Rando.kut_out_phases[i]) {
					kko_phase_rando = 1;
				}
			}
			KKOPhaseRandoOn = kko_phase_rando;
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
			// Deathwarp Handle
			writeFunction(0x8071292C, &WarpHandle); // Check if in Helm, in which case, apply transition
			// Gold Beaver Code
      		actor_functions[212] = (void*)0x806AD54C; // Set as Blue Beaver Code
			writeFunction(0x806AD750, &beaverExtraHitHandle); // Remove buff until we think of something better
			// Move Text Code
			actor_functions[324] = &getNextMoveText;
			actor_functions[320] = &getNextMoveText;
			initPauseMenu(); // Changes to enable more items
			// Spider Projectile
			if (Rando.hard_mode.enemies) {
				// writeFunction(0x806ADDC0, &handleSpiderTrapCode);
				actor_health_damage[259].init_health = 9; // Increase Guard Health
			}
			// Fix some silk memes
			writeFunction(0x806ADA70, &HandleSpiderSilkSpawn);
			// Oscillation Effects
			if (Rando.remove_oscillation_effects) {
				writeFunction(0x80660994, &getOscillationDelta);
				writeFunction(0x806609BC, &getOscillationDelta);
			}
			if (DAMAGE_MASKING) {
				// Damage mask
				// writeFunction(0x806A6EA8, &applyDamageMask);
				writeFunction(0x806EE138, &applyDamageMask);
				writeFunction(0x806EE330, &applyDamageMask);
				writeFunction(0x806EE480, &applyDamageMask);
				writeFunction(0x806EEA20, &applyDamageMask);
				writeFunction(0x806EEEA4, &applyDamageMask);
				writeFunction(0x806EF910, &applyDamageMask);
				writeFunction(0x806EF9D0, &applyDamageMask);
				writeFunction(0x806F5860, &applyDamageMask); // Watermelon
			}
			// Slow Turn Fix
			writeFunction(0x806D2FC0, &fixRBSlowTurn);
			// for (int i = 0; i < 10; i++) {
			// 	*(int*)(0x8060D6A0 + (4 * i)) = 0;
			// }
			// *(short*)(0x8060D6C8) = 0x5000;
			// LZ Save
			writeFunction(0x80712EC4, &postKRoolSaveCheck);
			// Opacity fixes
			writeFunction(0x806380B0, &handleModelTwoOpacity);
			// Reduce TA Cooldown
			if (Rando.tag_anywhere) {
				writeFunction(0x806F5BE8, &tagAnywhereAmmo);
				writeFunction(0x806F5A08, &tagAnywhereBunch);
				writeFunction(0x806F6CB4, &tagAnywhereInit);
			}
			if (ENABLE_ORIGIN_WARP_FIX) {
				writeFunction(0x8072F1E8, &handleGrabbingLock);
				writeFunction(0x806CAB68, &handleLedgeLock);
				writeFunction(0x8072F458, &handleActionSet); // Actor grabbables
				writeFunction(0x8072F46C, &handleActionSet); // Model 2 grabbables
				writeFunction(0x806CFC64, &handleActionSet); // Ledge Grabbing
			}
			if (Rando.disabled_music.pause) {
				*(int*)(0x805FC890) = 0; // Pause theme
				*(int*)(0x805FC89C) = 0; // Pause Start theme
			}
			if (Rando.disabled_music.wrinkly) {
				*(int*)(0x8064F180) = 0; // Wrinkly Theme
			}
			if (Rando.disabled_music.transform) {
				*(int*)(0x8067E9E4) = 0; // Transform Theme
				*(int*)(0x8067F7C0) = 0; // Transform Theme
			}
			if ((Rando.disabled_music.events) || (Rando.disabled_music.shops)) {
				*(int*)(0x80602AAC) = 0x27A40018; // addiu $a0, $sp, 0x18
				writeFunction(0x80602AB0, &filterSong);
			}
			if (Rando.disabled_music.chunk_songs) {
				// *(int*)(0x806025BC) = 0; // Disable `playLevelMusic` - Map Load
				*(int*)(0x8061DF74) = 0; // Disable `playLevelMusic`
				*(int*)(0x806DB98C) = 0; // Disable `playLevelMusic`
				*(short*)(0x806034F2) = 0; // Set Japes count to 0
				*(short*)(0x80603556) = 0; // Set Az Beetle count to 0
				*(short*)(0x80603542) = 0; // Set Factory count to 0
				*(short*)(0x8060356A) = 0; // Set Factory Car count to 0
				*(short*)(0x8060351A) = 0; // Set Galleon count to 0
				//*(short*)(0x80603592) = 0; // Set Isles count to 0
				*(short*)(0x80603506) = 0; // Set Aztec count to 0
				*(short*)(0x8060352E) = 0; // Set Galleon Seal count to 0
				*(short*)(0x806035C6) = 0; // Set Fungi count to 0
				*(short*)(0x8060357E) = 0; // Set Fungi Cart count to 0
				*(short*)(0x806035BA) = 0; // Set TGrounds count to 0
			}
			if (Rando.hard_mode.easy_fall) {
				float fall_threshold = 100.0f;
				*(short*)(0x806D3682) = getFloatUpper(fall_threshold); // Change fall too far threshold
				writeFunction(0x806D36B4, &fallDamageWrapper);
				writeFunction(0x8067F540, &transformBarrelImmunity);
				writeFunction(0x8068B178, &factoryShedFallImmunity);
			}
			if (Rando.hard_mode.lava_water) {
				*(int*)(0x806677C4) = 0; // Dynamic Surfaces
				// Static Surfaces
				*(short*)(0x80667ED2) = 0x81;
				*(short*)(0x80667EDA) = 0x81;
				*(short*)(0x80667EEE) = 0x81;
				*(short*)(0x80667EFA) = 0x81;
				writeFunction(0x8062F3F0, &replaceWaterTexture); // Static water textures
				// Dynamic Textures
				SurfaceTypeInformation[0].texture_loader = SurfaceTypeInformation[7].texture_loader;
				SurfaceTypeInformation[0].dl_writer = SurfaceTypeInformation[7].dl_writer;
				SurfaceTypeInformation[3].texture_loader = SurfaceTypeInformation[7].texture_loader;
				SurfaceTypeInformation[3].dl_writer = SurfaceTypeInformation[7].dl_writer;
			} else if (Rando.seasonal_changes == SEASON_HALLOWEEN) {
				writeFunction(0x8062F3F0, &replaceWaterTexture_spooky); // Static water textures
				SurfaceTypeInformation[0].texture_loader = SurfaceTypeInformation[6].texture_loader;
				SurfaceTypeInformation[0].dl_writer = SurfaceTypeInformation[7].dl_writer; // Use lava water renderer instead of acid one to have translucency
				SurfaceTypeInformation[3].texture_loader = SurfaceTypeInformation[6].texture_loader;
				SurfaceTypeInformation[3].dl_writer = SurfaceTypeInformation[7].dl_writer; // Use lava water renderer instead of acid one to have translucency
			}
			if ((Rando.hard_mode.dark_world) || (Rando.hard_mode.memory_challenge)) {
				writeFunction(0x8062F230, &alterChunkLighting);
				writeFunction(0x8065121C, &alterChunkLighting);
				writeFunction(0x8062F2CC, &alterChunkData);
				writeFunction(0x806C9DF8, &shineLight);
				writeFunction(0x806C9E28, &shineLight);
				writeFunction(0x806C9E58, &shineLight);
				writeFunction(0x806C9E88, &shineLight);
				writeFunction(0x806C9EB8, &shineLight);
				writeFunction(0x806C9EE8, &shineLight);
				writeFunction(0x806C9F2C, &shineLight);
				writeFunction(0x806C9F5C, &shineLight);
				// Fungi Time of Day
				*(float*)(0x80748280) = 0.0f;
				*(float*)(0x80748284) = 0.0f;
				*(float*)(0x80748288) = 0.0f;
				*(float*)(0x8074828C) = 0.0f;
				*(float*)(0x80748290) = 0.0f;
				*(float*)(0x80748294) = 0.0f;
				// Troff n Scoff
				*(float*)(0x8075B8B4) = 0.0f;
				*(float*)(0x8075B8B8) = 0.0f;
				// Rain
				*(short*)(0x8068B6AE) = 0;
			}
			if (!Rando.quality_of_life.fast_boot) {
				writeFunction(0x80713258, &skipDKTV);
			}
			if (Rando.any_kong_items & 1) {
				writeFunction(0x80632E94, &getItemRequiredKong);
			}
			writeFunction(0x806F93D4, &gbUpdateHandler);
			if ((Rando.hard_mode.no_geo) || (Rando.hard_mode.memory_challenge)) {
				writeFunction(0x80656538, &displayNoGeoChunk);
				writeFunction(0x806562C0, &displayNoGeoChunk);
				writeFunction(0x80656380, &displayNoGeoChunk);
				writeFunction(0x806565F8, &displayNoGeoChunk);
				// *(int*)(0x80651598) = 0xA1E00002;
			}
			if (Rando.enemy_item_rando) {
				writeFunction(0x80729E54, &indicateCollectionStatus);
				*(unsigned short*)(0x807278CA) = 0xFFF; // Disable enemy switching in Fungi
				writeFunction(0x806B26A0, &fireballEnemyDeath);
				writeFunction(0x806BB310, &rulerEnemyDeath);
			}

			initSwitchsanityChanges();

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
		Mode = GAMEMODE_MAINMENU;
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