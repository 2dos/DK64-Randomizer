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

typedef struct skipped_cutscene {
    /* 0x000 */ unsigned char map;
    /* 0x001 */ unsigned char cutscene;
} skipped_cutscene;

void initQoL_Cutscenes(void) {
    /**
     * @brief Initialize any quality of life features which aim to reduce the amount of cutscenes inside DK64
     * Current Elements covered here:
     * - Compressing all key turn in cutscenes in K. Lumsy
     * - Removing the 30s cutscene for freeing the Vulture in Angry Aztec
     * - Adding cutscenes for Item Rando back in if deemed important enough
     */
    if (Rando.cutscene_skip_setting == CSSKIP_OFF) {
        // Clear the cutscene skip database
        for (int i = 0; i < 432; i++) {
            cs_skip_db[i] = 0;
        }
    } else {
        if (Rando.item_rando) {
            skipped_cutscene cs_unskip[] = {
                {.map=MAP_FACTORY, .cutscene=2}, // Diddy Prod Spawn
                {.map=MAP_FACTORY, .cutscene=3}, // Tiny Prod Peek
                {.map=MAP_FACTORY, .cutscene=4}, // Lanky Prod Peek
                {.map=MAP_FACTORY, .cutscene=5}, // Chunky Prod Spawn
                {.map=MAP_AZTEC, .cutscene=14}, // Free Llama
                {.map=MAP_FUNGIGIANTMUSHROOM, .cutscene=0}, // Tiny Barrel Spawn
                {.map=MAP_FUNGIGIANTMUSHROOM, .cutscene=1}, // Cannon GB Spawn
                {.map=MAP_CASTLEGREENHOUSE, .cutscene=0}, // Greenhouse Intro
            };
            for (int i = 0; i < (sizeof(cs_unskip) / sizeof(skipped_cutscene)); i++) {
                int cs_offset = 0;
                int cs_val = cs_unskip[i].cutscene;
                int cs_map = cs_unskip[i].map;
                int shift = cs_val % 31;
                if (cs_val > 31) {
                    cs_offset = 1;
                }
                int comp = 0xFFFFFFFF - (1 << shift);
                cs_skip_db[(2 * cs_map) + cs_offset] &= comp;
            }
        }
        writeFunction(0x80628508, &renderScreenTransitionCheck); // Remove transition effects if skipped cutscene
        if (Rando.cutscene_skip_setting == CSSKIP_PRESS) {
            writeFunction(0x8061DD80, &pressSkipHandler); // Handler for press start to skip
        }
    }
    if (Rando.quality_of_life.remove_cutscenes) {
        // K. Lumsy
        *(short*)(0x80750680) = MAP_ISLES;
        *(short*)(0x80750682) = 0x1;
        *(int*)(0x806BDC24) = 0x0C17FCDE; // Change takeoff warp func
        *(short*)(0x806BDC8C) = 0x1000; // Apply no cutscene to all keys
        *(short*)(0x806BDC3C) = 0x1000; // Apply shorter timer to all keys
        // Fast Vulture
        writeFunction(0x806C50BC, &clearVultureCutscene); // Modify Function Call
        // Speedy T&S Turn-Ins
        *(int*)(0x806BE3E0) = 0; // NOP
        // Remove final mermaid text
        *(int*)(0x806C3E10) = 0;
        *(int*)(0x806C3E20) = 0;
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

void initQoL_Fixes(void) {
    /**
     * @brief Initialize any quality of life features which aim to fix unwanted DK64 vanilla bugs
     * Current Elements covered here:
     * - Rabbit Race will give infinite crystals during race 2
     * - Fix the dillo TNT pads to not move when using Tiny
     * - Fix Squawks-with-spotlight's AI to make him follow the Kong more closely in Fungi Forest's Dark Attic
     * Definition of an "unwanted DK64 vanilla bug":
     * - Removing the bug doesn't negatively impact speedrunners/game glitches OR
     * - Leaving the bug in produces a crash or leaves a prominent effect in the game which is undesirable (see Dillo TNT Pads)
     * - Pausing and exiting to another map during Helm Timer will correctly apply the helm timer pause correction
     */
    if (Rando.quality_of_life.vanilla_fixes) {
        writeFunction(0x806BE8D8, &RabbitRaceInfiniteCode); // Modify Function Call
        writeFunction(0x8067C168, &fixDilloTNTPads); // Modify Function Call
        actor_functions[249] = &squawks_with_spotlight_actor_code;

        writeFunction(0x806E5C04, &fixCrownEntrySKong); // Modify Function Call
        *(float*)(0x807482A4) = 0.1f; // Increase Fungi lighting transition rate
    }
    writeFunction(0x806A8844, &helmTime_restart); // Modify Function Call
    writeFunction(0x806A89E8, &helmTime_exitBonus); // Modify Function Call
    writeFunction(0x806A89F8, &helmTime_exitRace); // Modify Function Call
    writeFunction(0x806A89C4, &helmTime_exitLevel); // Modify Function Call
    writeFunction(0x806A89B4, &helmTime_exitBoss); // Modify Function Call
    writeFunction(0x806A8988, &helmTime_exitKRool); // Modify Function Call
}

void initQoL_Misc(void) {
    /**
     * @brief Initialize any quality of life features which have a miscellaneous purpose
     * Current Elements covered here:
     * - Fairy pictures are sped up (This also fixes some INSANE lag on BizHawk)
     * - Lower the Aztec Lobby Bonus barrel to be easier to reach for less skilled players using less laggy platforms
     */
    if (Rando.quality_of_life.fast_hints) {
        writeFunction(0x806A5C30, &quickWrinklyTextboxes);
    }
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
	}
}

void initQoL_Boot(void) {
    /**
     * @brief Initialize any quality of life features which speed up the boot procedure
     * Current Elements covered here:
     * - Removing DKTV when quitting the game or going via end sequence
     * - Speeding up the bootup setup checks
     */
    // Faster Boot
    writeFunction(0x805FEB00, &bootSpeedup); // Modify Function Call
    *(int*)(0x805FEB08) = 0; // Cancel 2nd check
}

void initQoL_FastWarp(void) {
    /**
     * @brief Initialize any quality of life features which speed up bananaporting
     */
    if (Rando.fast_warp) {
        // Replace vanilla warp animation (0x52) with monkeyport animation (0x53)
        *(short*)(0x806EE692) = 0x54;
        writeFunction(0x806DC2AC, &fastWarp); // Modify Function Call
        if (!Rando.disabled_music.chunk_songs) {
            writeFunction(0x806DC318, &fastWarp_playMusic); // Modify Function Call
        }
    }
}

static const char exittoisles[] = "EXIT TO ISLES";
static const char exittospawn[] = "EXIT TO SPAWN";

void initSpawn(void) {
    /**
     * @brief Initialize the world spawning procedure
     */
    // Starting map rando
    int starting_map_rando_on = 1;
    if (Rando.starting_map == 0) {
        // Default
        Rando.starting_map = MAP_ISLES;
        Rando.starting_exit = 0;
        starting_map_rando_on = 0;
    } else {
        *(short*)(0x8071454A) = Rando.starting_map;
        *(int*)(0x80714550) = 0x24050000 | Rando.starting_exit;
    }
    setPrevSaveMap();
    if (Rando.warp_to_isles_enabled) {
        // Pause Menu Exit To Isles Slot
        *(short*)(0x806A85EE) = 4; // Yes/No Prompt
        *(short*)(0x806A8716) = 4; // Yes/No Prompt
        //*(short*)(0x806A87BE) = 3;
        *(short*)(0x806A880E) = 4; // Yes/No Prompt
        //*(short*)(0x806A8766) = 4;
        *(short*)(0x806A986A) = 4; // Yes/No Prompt
        int y_cap = 0x270;
        if (Rando.true_widescreen) {
            y_cap = ((SCREEN_HD_FLOAT * 2) - 72 - 4) + (0x44 * 3);
        }
        *(int*)(0x806A9990) = 0x2A210000 | y_cap; // SLTI $at, $s1, 0x2A8
        if (!starting_map_rando_on) {
            PauseSlot3TextPointer = (char*)&exittoisles;
        } else {
            PauseSlot3TextPointer = (char*)&exittospawn;
        }
    }
}

void initQoL_HUD(void) {
    /**
     * @brief Initialize the HUD
     * 
     */
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
    if (Rando.true_widescreen) {
        y_bottom = SCREEN_HD - 32;
    }
    *(short*)(0x806F893E) = y_bottom - (1 * y_spacing); // Instrument
    *(short*)(0x806F8692) = y_bottom - (2 * y_spacing); // Crystals
    *(short*)(0x806F87AA) = y_bottom - (3 * y_spacing); // Oranges
    *(short*)(0x806F86CA) = y_bottom - (4 * y_spacing); // Ammo
    *(short*)(0x806F873E) = y_bottom - (4 * y_spacing); // Homing Ammo
    // Multibunch HUD
    if (Rando.quality_of_life.hud_bp_multibunch) {
        *(short*)(0x806F860A) = y_bottom - (5 * y_spacing); // Multi CB
        writeFunction(0x806F97D8, &getHUDSprite_HUD); // Change Sprite
        writeFunction(0x806F6BF0, &preventMedalHUD); // Prevent Model Two Medals showing HUD
        int multibunch_hud_x = 0x122;
        if (Rando.true_widescreen) {
            multibunch_hud_x = SCREEN_WD - 30;
        }
        *(short*)(0x806F8606) = multibunch_hud_x; // Position X
        *(int*)(0x806F862C) = 0x4600F306; // MOV.S $f12, $f30
        *(int*)(0x806F8634) = 0x4600A386; // MOV.S $f14, $f20
        writeFunction(0x806F98E4, &initHUDDirection); // HUD Direction
        writeFunction(0x806F9A00, &initHUDDirection); // HUD Direction
        writeFunction(0x806F9A78, &initHUDDirection); // HUD Direction
        writeFunction(0x806F9BC0, &initHUDDirection); // HUD Direction
        writeFunction(0x806F9D14, &initHUDDirection); // HUD Direction
        *(int*)(0x806FA62C) = 0; // NOP: Enable Number Rendering
        *(int*)(0x806FA56C) = 0; // NOP: Prevent opacity check
    }
}

void initNonControllableFixes(void) {
    /**
     * @brief Initialize any changes which we do not want to give the user any control over whether it's removed
     */
    writeFunction(0x806F56E0, &getFlagIndex_Corrected); // BP Acquisition - Correct for character
    writeFunction(0x806F9374, &getFlagIndex_Corrected); // Medal Acquisition - Correct for character
    // Inverted Controls Option
    *(short*)(0x8060D01A) = getHi(&InvertedControls); // Change language store to inverted controls store
    *(short*)(0x8060D01E) = getLo(&InvertedControls); // Change language store to inverted controls store
    *(short*)(0x8060D04C) = 0x1000; // Prevent inverted controls overwrite
    // Disable Sprint Music in Fungi Forest
    writeFunction(0x8067F3DC, &playTransformationSong);
    // New Helm Barrel Code
    actor_functions[107] = &HelmBarrelCode;
    // GetOut Timer
    *(unsigned short*)(0x806B7ECA) = 125; // 0x8078 for center-bottom ms timer
    // Fix Tag Barrel Background Kong memes
    writeFunction(0x806839F0, &tagBarrelBackgroundKong);
    // Better Collision
    writeFunction(0x806F6618, &checkModelTwoItemCollision);
    writeFunction(0x806F662C, &checkModelTwoItemCollision);
    // Dive Check
    writeFunction(0x806E9658, &CanDive_WithCheck);
    // Prevent Japes Dillo Cutscene for the key acquisition
    *(short*)(0x806EFCEC) = 0x1000;
    // Make getting out of spider traps easier on controllers
    *(int*)(0x80752ADC) = (int)&exitTrapBubbleController;
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

void initQoL_InstrumentFix(void) {
    /**
     * @brief Makes instrument energy a global variable used by all kongs, like ammo and oranges
     * 
     */
    if (Rando.quality_of_life.global_instrument) {
        *(int*)(0x8060DC04) = 0; // nop out
        writeFunction(0x8060DB50, &newInstrumentRefill); // New code to set the instrument refill count
        writeFunction(0x806AA728, &QoL_DisplayInstrument); // display number on pause menu
        *(int*)(0x806F891C) = 0x27D502FE; // addiu $s5, $s8, 0x2FE - Infinite Instrument Energy
        *(int*)(0x806F8934) = 0xA7C202FE; // sh $v0, 0x2FE ($fp) - Store item count pointer
        writeFunction(0x806A7DD4, &getInstrumentRefillCount); // Correct refill instruction - Headphones
        writeFunction(0x806F92B8, &correctRefillCap); // Correct refill instruction - changeCollectable

        // Make it so all kongs can refill headphones *if* a kong has music
        actor_functions[128] = &HeadphonesCodeContainer;
        *(int*)(0x806A7C04) = 0x00A0C025; // or $t8, $a1, $zero
    }
}

void initQoL(void) {
    /**
     * @brief Initialize all quality of life functionality
     */
    writeFunction(0x80004EB4, &disableAntiAliasing); // Disable Anti-Aliasing
    initQoL_Cutscenes();
    initQoL_Fixes();
    initQoL_Misc();
    initQoL_Boot();
    initSpawn();
    initQoL_HUD();
    initQoL_FastWarp();
    initQoL_InstrumentFix();
    initNonControllableFixes();
}