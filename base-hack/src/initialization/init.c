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

unsigned char BigHeadMode = 0;

char music_types[SONG_COUNT] = {
	-1,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	-1,
	SONGTYPE_BGM,
	SONGTYPE_EVENT,
	SONGTYPE_EVENT,
	SONGTYPE_EVENT,
	SONGTYPE_EVENT,
	SONGTYPE_EVENT,
	SONGTYPE_BGM,
	SONGTYPE_EVENT,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_MAJORITEM,
	SONGTYPE_BGM,
	SONGTYPE_MAJORITEM,
	SONGTYPE_BGM,
	SONGTYPE_MAJORITEM,
	SONGTYPE_MINORITEM,
	SONGTYPE_EVENT,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_MINORITEM,
	SONGTYPE_MINORITEM,
	SONGTYPE_BGM,
	SONGTYPE_MINORITEM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	-1,
	SONGTYPE_BGM,
	SONGTYPE_EVENT,
	-1,
	SONGTYPE_EVENT,
	-1,
	-1,
	-1,
	SONGTYPE_MINORITEM,
	SONGTYPE_MINORITEM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_EVENT,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_EVENT,
	SONGTYPE_BGM,
	-1,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_MINORITEM,
	-1,
	SONGTYPE_MINORITEM,
	SONGTYPE_BGM,
	SONGTYPE_MAJORITEM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_MAJORITEM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	-1,
	SONGTYPE_EVENT,
	SONGTYPE_EVENT,
	-1,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	-1,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	-1,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_EVENT,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_MAJORITEM,
	SONGTYPE_MAJORITEM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_MAJORITEM,
	SONGTYPE_MAJORITEM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_EVENT,
	SONGTYPE_MAJORITEM,
	SONGTYPE_MAJORITEM,
	SONGTYPE_MINORITEM,
	SONGTYPE_MAJORITEM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_MAJORITEM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	SONGTYPE_BGM,
	-1,
	SONGTYPE_BGM,
	SONGTYPE_EVENT,
	-1,
	SONGTYPE_BGM,
	-1
};

typedef struct musicInfo {
	/* 0x000 */ short data[0xB0];
} musicInfo;

void fixMusicRando(void) {
	/**
	 * @brief Initialize Music Rando so that the data for each song is correct.
	 * Without this, the game will crash from incorrect properties to what the song is expecting.
	 */
	if (Rando.music_rando_on) {
		// Type indexes
		int size = SONG_COUNT;
		char* write_space_0 = getFile(size, 0x1FEE200);
		for (int i = 0; i < SONG_COUNT; i++) {
			// Handle Type Index
			if (write_space_0[i] > -1) {
				song_types type = write_space_0[i];
				music_types[i] = type;
			}
		}
		*(short*)(0x806CA97E) = 0x560 | ((songData[0x6B] >> 1) & 3); // Baboon Balloon
		*(float*)(0x807565D8) = 1.0f; // Funky and Candy volumes
		*(int*)(0x80604B50) = 0; // Disable galleon outside track isolation
		*(int*)(0x80604A54) = 0; // Disable galleon outside track isolation
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
	for (int i = 0; i < 5; i++) {
		if (Rando.kong_models[i] == KONGMODEL_KRUSHA) {
			loadSingularHook(0x806F97B8, &FixKrushaAmmoHUDColor);
			loadSingularHook(0x806F97E8, &FixKrushaAmmoHUDSize);
			break;
		}
	}
	if (MenuDarkness != 0) {
		loadSingularHook(0x807070A0, &RecolorMenuBackground);
	}
	if (Rando.big_head_mode) {
		loadSingularHook(0x8061A4C8, &AlterHeadSize);
		loadSingularHook(0x806198D4, &AlterHeadSize_0);
	}
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
			*(int*)(0x8076BF38) = (int)&music_storage[0]; // Increase music storage
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
			if (Rando.big_head_mode == 1) {
				BigHeadMode = 0xFF;
			} else if (Rando.big_head_mode == 2) {
				BigHeadMode = 0x2F;
			}
			// HUD Re-allocation fixes
			*(short*)(0x806FB246) = ITEMID_TERMINATOR;
			*(short*)(0x806FABAA) = ITEMID_TERMINATOR;
			*(short*)(0x806F9992) = ITEMID_RESERVED_FUNKY;
			*(short*)(0x806F99AA) = ITEMID_RESERVED_CRANKY;
			*(short*)(0x806F9986) = ITEMID_RESERVED_SCOFF;
			*(short*)(0x806F99C6) = ITEMID_RESERVED_CANDY;
			*(short*)(0x806F99DA) = ITEMID_RESERVED_DK;
			RandomizerVersion = 4;
			initActorExpansion();
			for (int i = 0; i < 7; i++) {
				SwitchLevel[i] = Rando.slam_level[i];
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
			initActor(NEWACTOR_NINTENDOCOIN, 1, &ninCoinCode, ACTORMASTER_3D, 0, 1, 8, 45);
			initActor(NEWACTOR_RAREWARECOIN, 1, &rwCoinCode, ACTORMASTER_3D, 0, 1, 8, 45);
			initActor(NEWACTOR_NULL, 1, &NothingCode, ACTORMASTER_SPRITE, 0, 1, 8, 0);
			initActor(NEWACTOR_MEDAL, 1, &medalCode, ACTORMASTER_3D, 0, 1, 8, 45);
			for (int i = 0; i < 6; i++) {
				initActor(NEWACTOR_POTIONDK + i, 1, &PotionCode, ACTORMASTER_3D, 0, 1, 8, 45);
				if (i < 5) {
					initActor(NEWACTOR_KONGDK + i, 1, &KongDropCode, ACTORMASTER_3D, 0, 1, 8, 45);
					if (i < 4) {
						initActor(NEWACTOR_CRANKYITEM + i, 1, &shopOwnerItemCode, ACTORMASTER_3D, 0, 1, 8, 45);
					}
				}
			}
			initActor(NEWACTOR_BEAN, 1, &beanCode, ACTORMASTER_3D, 0, 1, 8, 45);
			initActor(NEWACTOR_PEARL, 1, &pearlCode, ACTORMASTER_3D, 0, 1, 8, 45);
			initActor(NEWACTOR_FAIRY, 1, &fairyDuplicateCode, ACTORMASTER_3D, 0, 1, 8, 45);
			initActor(NEWACTOR_ICETRAPBUBBLE, 1, &FakeGBCode, ACTORMASTER_3D, 0, 1, 8, 45);
			initActor(NEWACTOR_ICETRAPREVERSE, 1, &FakeGBCode, ACTORMASTER_3D, 0, 1, 8, 45);
			initActor(NEWACTOR_ICETRAPSLOW, 1, &FakeGBCode, ACTORMASTER_3D, 0, 1, 8, 45);
			initActor(NEWACTOR_JETPACITEMOVERLAY, 1, &getNextMoveText, ACTORMASTER_CONTROLLER, 0, 0, 0x10, 324);
			initActor(NEWACTOR_ZINGERFLAMETHROWER, 1, (void*)0x806B4958, ACTORMASTER_3D, 1, 0, 2, 183);
			initActor(NEWACTOR_SCARAB, 1, &kioskBugCode, ACTORMASTER_3D, 1, 0, 2, 183);
			setCollisionAddress(NEWACTOR_SCARAB, 1, (void*)0x8074B240, 1);
			// Kong Rando
			initKongRando();
            initQoL(); // Also includes initializing spawn point and HUD realignment
            initItemRando();
			initCosmetic();
			initTextChanges();

			replace_zones(1);
			loadHooks();
			loadExtraHooks();
			// Place Move Data
			moveTransplant();
			priceTransplant();
			
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
			writeEndSequence();
			
			int kko_phase_rando = 0;
			for (int i = 0; i < 3; i++) {
				KKOPhaseOrder[i] = Rando.kut_out_phases[i];
				if (Rando.kut_out_phases[i]) {
					kko_phase_rando = 1;
				}
			}
			KKOPhaseRandoOn = kko_phase_rando;
			
			initPauseMenu(); // Changes to enable more items
			// Model Stuff
			if (Rando.kong_models[KONG_DK] == KONGMODEL_CRANKY) {
				KongModelData[KONG_DK].props_or = 0;
			}
			if (Rando.kong_models[KONG_TINY] == KONGMODEL_CANDY) {
				KongModelData[KONG_TINY].props_or = 0;
			}
			if (Rando.kong_models[KONG_DIDDY] == KONGMODEL_FUNKY) {
				KongModelData[KONG_DIDDY].props_or = 0;
			}
			fixCutsceneModels();
			// Oscillation Effects
			if (Rando.remove_oscillation_effects) {
				writeFunction(0x80660994, &getOscillationDelta);
				writeFunction(0x806609BC, &getOscillationDelta);
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
			*(int*)(0x80602AAC) = 0x27A40018; // addiu $a0, $sp, 0x18
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
			if (Rando.balloon_sound) {
				writeFunction(0x806A77D8, &playBalloonWhoosh);
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
	}
}

int balloon_path_pointers[PATH_CAP];