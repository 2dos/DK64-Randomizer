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

void initQoL_Lag(void) {
    /**
     * @brief Initialize any quality of life features which aim to reduce lag native to DK64
     * Current Elements covered here:
     * - Turning off the Aztec Sandstorm
     * - Disabling Rain in DK Isles
     */
    writeFunction(0x80004EB4, &disableAntiAliasing); // Disable Anti-Aliasing
    if (Rando.quality_of_life.reduce_lag) {
        *(int*)(0x80748010) = 0x8064F2F0; // Cancel Sandstorm
        // No Rain
        if (Rando.seasonal_changes != SEASON_CHRISTMAS) {
            *(float*)(0x8075E3E0) = 0.0f; // Set Isles Rain Radius to 0
            *(int*)(0x8068AF90) = 0; // Disable weather
        }
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
    if (Rando.quality_of_life.remove_cutscenes) {
        // K. Lumsy
        *(short*)(0x80750680) = MAP_ISLES;
        *(short*)(0x80750682) = 0x1;
        *(int*)(0x806BDC24) = 0x0C17FCDE; // Change takeoff warp func
        *(short*)(0x806BDC8C) = 0x1000; // Apply no cutscene to all keys
        *(short*)(0x806BDC3C) = 0x1000; // Apply shorter timer to all keys
        // Fast Vulture
        writeFunction(0x806C50BC, &clearVultureCutscene); // Modify Function Call
        // General
        writeFunction(0x80628508, &renderScreenTransitionCheck); // Remove transition effects if skipped cutscene
        // Speedy T&S Turn-Ins
        *(int*)(0x806BE3E0) = 0; // NOP
        if (Rando.item_rando) {
            int cs_unskip[] = {
                MAP_FACTORY, 2,
                MAP_FACTORY, 3,
                MAP_FACTORY, 4,
                MAP_FACTORY, 5,
                MAP_AZTEC, 14,
                MAP_FUNGIGIANTMUSHROOM, 0,
                MAP_FUNGIGIANTMUSHROOM, 1,
                MAP_CASTLEGREENHOUSE, 0,
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
    } else {
        // Clear the cutscene skip database
        for (int i = 0; i < 432; i++) {
            cs_skip_db[i] = 0;
        }
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
        writeFunction(0x806A8844, &helmTime_restart); // Modify Function Call
        writeFunction(0x806A89E8, &helmTime_exitBonus); // Modify Function Call
        writeFunction(0x806A89F8, &helmTime_exitRace); // Modify Function Call
        writeFunction(0x806A89C4, &helmTime_exitLevel); // Modify Function Call
        writeFunction(0x806A89B4, &helmTime_exitBoss); // Modify Function Call
        writeFunction(0x806A8988, &helmTime_exitKRool); // Modify Function Call
    }
}

void initQoL_Misc(void) {
    /**
     * @brief Initialize any quality of life features which have a miscellaneous purpose
     * Current Elements covered here:
     * - Fairy pictures are sped up (This also fixes some INSANE lag on BizHawk)
     * - Lower the Aztec Lobby Bonus barrel to be easier to reach for less skilled players using less laggy platforms
     */
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
    if (Rando.quality_of_life.cbs_visible) {
        *(int*)(0x806324D4) = 0x24020001; // ADDIU $v0, $r0, 1 // Disable kong flag check
        *(int*)(0x806A78C4) = 0; // NOP // Disable kong flag check
    }
    if (Rando.quality_of_life.fast_hints) {
        int control_cap = 1;
        *(short*)(0x8069E0F6) = control_cap;
        *(short*)(0x8069E112) = control_cap;
        *(unsigned char*)(0x80758BC9) = 0xAE; // Quadruple Growth Speed (8E -> AE)
        *(unsigned char*)(0x80758BD1) = 0xAE; // Quadruple Shrink Speed (8E -> AE)
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
				if (actor_count > 0) {
					for (int j = 0; j < actor_count; j++) {
						int actor = *(short*)((int)focused_actor + 0x32) + 0x10;
						balloon_patch_count += isBalloonOrPatch(actor);
						if (actor == 139) {
                            int world = 7;
                            if (!isLobby(i)) {
								world = levelIndexMapping[i];
							}
                            populatePatchItem(*(short*)((int)focused_actor + 0x34), i, patch_index, world);
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

void initQoL_Boot(void) {
    /**
     * @brief Initialize any quality of life features which speed up the boot procedure
     * Current Elements covered here:
     * - Removing DKTV when quitting the game or going via end sequence
     * - Speeding up the bootup setup checks
     */
    if (Rando.quality_of_life.fast_boot) {
        // Remove DKTV - Game Over
        *(short*)(0x8071319E) = 0x50;
        *(short*)(0x807131AA) = 5;
        // Remove DKTV - End Seq
        *(short*)(0x8071401E) = 0x50;
        *(short*)(0x8071404E) = 5;
    }
    // Faster Boot
    writeFunction(0x805FEB00, &bootSpeedup); // Modify Function Call
    *(int*)(0x805FEB08) = 0; // Cancel 2nd check
}

void initQoL_Transform(void) {
    /**
     * @brief Initialize any quality of life features which reduce the transformation animation
     */
    if (Rando.quality_of_life.fast_transform) {
        // Fast Barrel Animation
        *(short*)(0x8067EAB2) = 1; // OSprint
        *(short*)(0x8067EAC6) = 1; // HC Dogadon 2
        *(short*)(0x8067EACA) = 1; // Others
        *(short*)(0x8067EA92) = 1; // Others 2
    }
}

void initQoL_AnimalBuddies(void) {
    /**
     * @brief Initialize any quality of life features which change the behaviour of the animal buddies
     * Current Elements covered here:
     * - Making items collectable regardless of whether you're an animal buddy or not
     */
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
}

void initQoL_FastWarp(void) {
    /**
     * @brief Initialize any quality of life features which speed up bananaporting
     */
    if (Rando.fast_warp) {
        // Replace vanilla warp animation (0x52) with monkeyport animation (0x53)
        *(short*)(0x806EE692) = 0x54;
        writeFunction(0x806DC2AC, &fastWarp); // Modify Function Call
        writeFunction(0x806DC318, &fastWarp_playMusic); // Modify Function Call
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
        *(int*)(0x806A9990) = 0x2A210270; // SLTI $at, $s1, 0x2A8
        if (!starting_map_rando_on) {
            PauseSlot3TextPointer = (char*)&exittoisles;
        } else {
            PauseSlot3TextPointer = (char*)&exittospawn;
        }
    }
}

void initQoL_HomingBalloons(void) {
    /**
     * @brief Initialize any quality of life features which make homing ammo home in on balloons
     */
    if (Rando.quality_of_life.homing_balloons) {
        // Make homing ammo target balloons
        *(short*)(0x80694F6A) = 10; // Coconut
        *(short*)(0x80692B82) = 10; // Peanuts
        *(short*)(0x8069309A) = 10; // Grape
        *(short*)(0x80695406) = 10; // Feather
        *(short*)(0x80694706) = 10; // Pineapple
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
        *(short*)(0x806F8606) = 0x122; // Position X
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
    // Move Decoupling
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
    // PPunch
    *(int*)(0x806E48F4) = 0x31810002; // ANDI $at $t4 2
    *(int*)(0x806E48F8) = 0x50200074; // BEQL $at $r0 0xF

    // Disable Sniper Scope Overlay
    // - This isn't covered in the lag section because re-enabling the scope can make Mech Fish harder to beat
    //  - This is a common problem experienced with the vanilla game
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

    *(int*)(0x806A7564) = 0xC4440080; // Crown default floor will be it's initial Y spawn position. Fixes a crash on N64
    writeFunction(0x806F56E0, &getFlagIndex_Corrected); // BP Acquisition - Correct for character
    writeFunction(0x806F9374, &getFlagIndex_Corrected); // Medal Acquisition - Correct for character
    // Inverted Controls Option
    *(short*)(0x8060D01A) = getHi(&InvertedControls); // Change language store to inverted controls store
    *(short*)(0x8060D01E) = getLo(&InvertedControls); // Change language store to inverted controls store
    *(short*)(0x8060D04C) = 0x1000; // Prevent inverted controls overwrite
    // Expand Display List
    *(short*)(0x805FE56A) = 8000;
    *(short*)(0x805FE592) = 0x4100; // SLL 4 (Doubles display list size)
    // Sniper Scope Check
    *(int*)(0x806D2988) = 0x93190002; // LBU $t9, 0x2 ($t8)
    *(int*)(0x806D2990) = 0x33210004; // ANDI $at, $t9, 0x4
    *(short*)(0x806D299C) = 0x1020; // BEQ $at, $r0
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

void initQoL(void) {
    /**
     * @brief Initialize all quality of life functionality
     */
    initQoL_Lag();
    initQoL_Cutscenes();
    initQoL_Fixes();
    initQoL_Misc();
    initQoL_Boot();
    initQoL_Transform();
    initQoL_AnimalBuddies();
    initSpawn();
    initQoL_HomingBalloons();
    initQoL_HUD();
    initQoL_FastWarp();
    initNonControllableFixes();
}