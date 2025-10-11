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
unsigned char HeadSize[MODEL_COUNT];

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
	-1,
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
	-1,
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
		*(short*)(0x806CA97E) = 0x560 | ((songData[0x6B] >> 1) & 3); // Baboon Balloon
	}
}

void writeEndSequence(void) {
	/**
	 * @brief Write our custom end sequence
	 */
	int size = 0x84;
	copyFromROM(0x1FFF800,(int*)0x807506D0,&size,0,0,0,0);
}

float getOscillationDelta(void) {
	if (CurrentMap == MAP_CAVES) {
		return 0.59f;
	}
	return 0.5f;
}

void loadHooks(void) {
	if (MenuDarkness != 0) {
		loadSingularHook(0x807070A0, &RecolorMenuBackground);
	}
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
			bonusAutocomplete = Rando.resolve_bonus;
			TextHoldOn = Rando.quality_of_life.textbox_hold;
			ToggleAmmoOn = Rando.quality_of_life.ammo_swap;
			LobbiesOpen = Rando.lobbies_open_bitfield;
			ShorterBosses = Rando.short_bosses;
			ItemRandoOn = Rando.item_rando;
			KrushaSlot = Rando.krusha_slot;
			RandomSwitches = Rando.random_switches;
			DamageMultiplier = Rando.damage_multiplier; // Keep for Crowd Control. Needs it to know what to set damage mult back to
			initItemRandoPointer();
			initAP();
			RandomizerVersion = 5;
			RandomizerSubVersion = 1;  // Use this for tracker changes
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
			// Kong Rando
            initQoL(); // Also includes initializing spawn point and HUD realignment
            initItemRando();
			initCosmetic();
			initTextChanges();

			replace_zones(1);
			loadHooks();
			loadExtraHooks();
			// Place Move Data
			moveTransplant();
			
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
			
			initPauseMenu(); // Changes to enable more items
			fixCutsceneModels();
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
			if (Rando.colorblind_mode != COLORBLIND_OFF) {
				writeFunction(0x8069E968, &determineShockwaveColor);
			}
			if (Rando.remove_oscillation_effects) {
				writeFunction(0x80660994, &getOscillationDelta);
        		writeFunction(0x806609BC, &getOscillationDelta);
			}
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
	initiateTransitionFade(MAP_NFRTITLESCREEN, 0, GAMEMODE_MAINMENU);
	CutsceneWillPlay = 0;
	Gamemode = GAMEMODE_MAINMENU;
	Mode = GAMEMODE_MAINMENU;
}

int balloon_path_pointers[PATH_CAP];