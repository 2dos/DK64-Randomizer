/**
 * @file qol.c
 * @author Ballaam
 * @brief Initialize Quality of Life features
 * @version 0.1
 * @date 2023-01-17
 * 
 * @copyright Copyright (c) 2023
 * 
 */
#include "../../include/common.h"

void disableAntiAliasing(void) {
    __osViSwapContext();
    int disable_antialiasing = Rando.quality_of_life.reduce_lag;
    if (Rando.quality_of_life.fast_boot) {
        if (CurrentMap == MAP_NINTENDOLOGO) {
            disable_antialiasing = 1;
        }
    } else if (FrameReal < 230) {
        disable_antialiasing = 1;
    }
    if (disable_antialiasing) {
        *(int*)(0x8001013C) = 0x3216;
        *(int*)(0x8001016C) = 0x3216;
    }
}

void initQoL_Cutscenes(void) {
    /**
     * @brief Initialize any quality of life features which aim to reduce the amount of cutscenes inside DK64
     * Current Elements covered here:
     * - Compressing all key turn in cutscenes in K. Lumsy
     * - Removing the 30s cutscene for freeing the Vulture in Angry Aztec
     * - Adding cutscenes for Item Rando back in if deemed important enough
     */
    int write_size = 4 * sizeof(int);
    int* temp_data = getFile(write_size, 0x1FF3800 + (CurrentMap * 8));
    cs_skip_db[0] = temp_data[0];
    cs_skip_db[1] = temp_data[1];
}

void fixRaceHoopCode(void) {
    unkProjectileCode_3(CurrentActorPointer_0, 0);
}

void renderHoop(void) {
    unkBonusFunction(CurrentActorPointer_0);
    CurrentActorPointer_0->rot_x -= 0x39; // Rotate Hoop
    renderActor(CurrentActorPointer_0, 0);
}

void fixUpdraftBug(int state) {
    controlStateControl(state);
    if (CurrentActorPointer_0->yPos > 600.0f) {
        playerData* player = (playerData*) CurrentActorPointer_0;
        player->updraft_target = 700;
    }
}

void quickWrinklyTextboxes(void) {
    /**
     * @brief Speeds up the wrinkly textboxes by setting the textbox timer to 0x1e upon init if A is pressed
     */
    if (CurrentActorPointer_0->control_state == 0) {
        if (NewlyPressedControllerInput.Buttons.a) {
            short* paad = CurrentActorPointer_0->paad;
            *paad = 0x1E;
        }
    }
    unkTextFunction(CurrentActorPointer_0);
}

static char boot_speedup_done = 0;
void bootSpeedup(void) {
    /**
     * @brief Speed up the boot process by reducing the amount of setups the game is loading
     */
    if (!boot_speedup_done) {
		boot_speedup_done = 1;
		int balloon_patch_count = 0;
		for (int j = 0; j < 8; j++) {
			coloredBananaCounts[j] = 0;
		}
		int patch_index = 0;
        int crate_index = 0;
		for (int i = 0; i < 221; i++) {
			balloonPatchCounts[i] = balloon_patch_count;
			int* setup = getMapData(TABLE_MAP_SETUPS,i,1,1);
			char* modeltwo_setup = 0;
			char* actor_setup = 0;
			if (setup) {
				int world = getWorld(i,1);
				getModel2AndActorInfo(setup,(int**)&modeltwo_setup,(int**)&actor_setup);
				int model2_count = *(int*)(modeltwo_setup);
				int actor_count = *(int*)(actor_setup);
				char* focused_actor = (char*)(actor_setup + 4);
				char* focused_model2 = (char*)(modeltwo_setup + 4);
                int subworld = LEVEL_ISLES;
                if (!isLobby(i)) {
                    subworld = levelIndexMapping[i];
                }
				if (actor_count > 0) {
					for (int j = 0; j < actor_count; j++) {
						int actor = *(short*)((int)focused_actor + 0x32) + 0x10;
						balloon_patch_count += isBalloonOrPatch(actor);
						if (actor == 139) {
                            populatePatchItem(*(short*)((int)focused_actor + 0x34), i, patch_index, subworld);
							patch_index += 1;
						}
						focused_actor += 0x38;
					}
				}
				if (model2_count > 0) {
					for (int j = 0; j < model2_count; j++) {
                        unsigned short m2_obj_type = *(unsigned short*)(focused_model2 + 0x28);
						coloredBananaCounts[world] += isSingleOrBunch(m2_obj_type);
                        if (m2_obj_type == 181) {
                            populateCrateItem(*(short*)((int)focused_model2 + 0x2A), i, crate_index, subworld);
                            crate_index += 1;
                        }
						focused_model2 += 0x30;
					}
				}
				enableComplexFree();
				complexFreeWrapper(setup);
			}
		}
        initItemCheckDenominators();
	}
}

void initQoL_FastWarp(void) {
    /**
     * @brief Initialize any quality of life features which speed up bananaporting
     */
    if (Rando.fast_warp) {
        if (!Rando.disabled_music.chunk_songs) {
            writeFunction(0x806DC318, &fastWarp_playMusic); // Modify Function Call
        }
    }
}

static const char exittoisles[] = "EXIT TO ISLES";
static const char exittospawn[] = "EXIT TO SPAWN";

void writeSpawn(int map, int exit) {
    *(short*)(0x8071454A) = map;
    *(int*)(0x80714550) = 0x24050000 | exit;
}

void initSpawn(void) {
    /**
     * @brief Initialize the world spawning procedure
     */
    // Starting map rando
    PauseSlot3TextPointer = (char*)&exittoisles;
    if (Rando.starting_map == 0) {
        // Default
        if ((!Rando.fast_start_beginning) && (Rando.randomize_more_loading_zones == 2)) {
            // No fast start beginning, with LZR
            writeSpawn(MAP_TRAININGGROUNDS, 1);
        }
        Rando.starting_map = MAP_ISLES;
        Rando.starting_exit = 0;
    } else {
        writeSpawn(Rando.starting_map, Rando.starting_exit);
        PauseSlot3TextPointer = (char*)&exittospawn;
    }
    setPrevSaveMap();
}

void QoL_DisplayInstrument(void* handler, int x, int y, int unk0, int unk1, int count, int unk2, int unk3) {
    displayPauseSpriteNumber(handler, x, y, unk0, unk1, CollectableBase.InstrumentEnergy, unk2, unk3);
}

void HeadphonesCodeContainer(void) {
    int has_headphones = 0;
    for (int kong = 0; kong < 5; kong++) {
        if (MovesBase[kong].instrument_bitfield & 1) {
            has_headphones = 1;
        }
    }
    headphonesCode(0, has_headphones);
}

int newInstrumentRefill(int item, int player_index) {
    int refill_count = getRefillCount(item, player_index);
    if (refill_count > 0) {
        CollectableBase.InstrumentEnergy = refill_count >> 1;
    }
    return refill_count;
}

int getInstrumentRefillCount(void) {
    for (int i = 0; i < 5; i++) {
        int btf = MovesBase[i].instrument_bitfield;
        if (btf & 1) {
            int refill_mult = 1;
            while (btf != 0) {
                btf >>= 1;
                refill_mult += 1;
            }
            return refill_mult * 5;
        }
    }
    return 0;
}

int correctRefillCap(int index, int player) {
    if (index == 7) {
        // Instrument
        return getInstrumentRefillCount();
    }
    return getRefillCount(index, player);
}

void initQoL(void) {
    /**
     * @brief Initialize all quality of life functionality
     */
    writeFunction(0x80004EB4, &disableAntiAliasing); // Disable Anti-Aliasing
    initSpawn();
    initQoL_FastWarp();
}