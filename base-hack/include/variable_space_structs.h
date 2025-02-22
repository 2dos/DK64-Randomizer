typedef struct varspace {
	/* 0x000 */ char level_order_rando_on; // 0 = Level Order Rando off, 1 = On
	/* 0x001 */ char unk_1[0x2C - 0x1];
	/* 0x02C */ char unlock_kongs; // 0 = Kongs not automatically unlocked, 1 = On
	/* 0x02D */ char required_helm_minigames; // 0 = Disable on instrument play, 1 = One minigame required, 2 = Vanilla
	/* 0x02E */ char fast_start_beginning; // 0 = "Fast Start" setting not applied. 1 = On
	/* 0x02F */ char sprint_barrel_requires_sprint;
	/* 0x030 */ char tag_anywhere; // 0 = Tag Anywhere buttons not enabled. 1 = Enabled
	/* 0x031 */ char fast_start_helm; // 0 = "Fast Start for Helm" setting not applied. 1 = Applied
	/* 0x032 */ LZREntrance mech_fish_exit;
	/* 0x034 */ char item_rando; // 0 = Off, 1 = On
	/* 0x035 */ char crown_timer_reduction;
	/* 0x036 */ char rareware_gb_fairies; // Fairy requirement to access Rareware GB
	/* 0x037 */ char unk_37[12];
	/* 0x043 */ char colorblind_mode; // 0 = Off, 1 = Prot, 2 = Deut, 3 = Trit
	/* 0x044 */ char dark_mode_textboxes; // 0 = Light Mode, 1 = Dark Mode
	/* 0x045 */ unsigned char slam_prices[2]; // Array of simian slam upgrade prices: [1,2]. First item is super simian slam (blue), 2nd is super duper simian slam (red)
	/* 0x047 */ char call_parent_filter; // Calls filter to remove "unnecessary" links from the parent chain
	/* 0x048 */ char unk_48[4];
	/* 0x04C */ ItemRequirement crown_door_requirement;
	/* 0x04E */ ItemRequirement coin_door_requirement;
	/* 0x050 */ unsigned char aztec_beetle_reward;
	/* 0x051 */ unsigned char caves_beetle_reward;
	/* 0x052 */ char disable_wrinkly_kong_requirement; // Disable Kongs being required to access a wrinkly door
	/* 0x053 */ unsigned char ammo_belt_prices[2]; // Array of ammo belt prices: [1,2]. 1 item for each level of ammo belt
	/* 0x055 */ unsigned char instrument_upgrade_prices[3]; // Array of instrument upgrade prices: [1,2,3]. 1st and 3rd items are the Upgrades 1 and 2 respectively. 2nd item is the 3rd melon cost
	/* 0x058 */ unsigned char k_rool_order[5]; // Order of K. Rool phases: [0,1,2,3,4] dictates DK->Diddy->Lanky->Tiny->Chunky. If K. Rool is being shortened to less than 5 phases, put the unused phases as -1
	/* 0x05D */ char randomize_more_loading_zones; // 0 = Not randomizing loading zones inside levels. 1 = On, 2 = Just Castle Cannon
	/* 0x05E */ LZREntrance aztec_beetle_enter; // Map and exit replacing the loading zone which normally bring you to Aztec Beetle Race from Aztec. First byte is map, second byte is exit value. Same logic applies until (and including) "enter_levels[7]"
	/* 0x060 */ char unk_60[10]; 
	/* 0x06A */ LZREntrance seasick_ship_enter; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
	/* 0x06C */ LZREntrance fungi_minecart_enter; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
	/* 0x06E */ char unk_6E[6];
	/* 0x074 */ LZREntrance castle_lobby_enter; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
	/* 0x076 */ char unk_76[2];
	/* 0x078 */ LZREntrance exit_levels[8]; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
	/* 0x088 */ rgb fog[3]; // Order: Aztec, Caves, Castle
	/* 0x091 */ char disable_race_patches;
	/* 0x092 */ char unk_91[0x96 - 0x92];
	/* 0x096 */ char fps_on; // 0 = FPS display off, 1 = On.
	/* 0x097 */ char damage_multiplier; // 1 = Normal. 2 = Double. Any value greater than 11 will be 1 hit KO
	/* 0x098 */ short progressive_bounds[10];
	/* 0x0AC */ char unk_98[0xAE - 0xAC];
	/* 0x0AE */ char helm_hurry_mode; // 0 = Off, 1 = On: Starting a new file summons the helm timer, each BP adds 2 minutes to the clock, timing out disables saving.
	/* 0x0AF */ char archipelago; // DK64R is being run through Archipelago
	/* 0x0B0 */ quality_options quality_of_life; // Size: 4
	/* 0x0B4 */ char unk_B0[0xC0 - 0xB4];
	/* 0x0C0 */ ItemRequirement win_condition_extra; // If requirement is "get x amount of y item"
	/* 0x0C2 */ char hints_are_items; // Hints are collectable as items, wrinkly doors should behave differently
	/* 0x0C3 */ unsigned char prog_hint_item;
	/* 0x0C4 */ ROMFlags rom_flags;
	/* 0x0C5 */ char enemy_item_rando; // Determines whether to use standard enemy item drop table or a custom table
	/* 0x0C6 */ HardModeSettings hard_mode; // Colloquially known as "Seed of Death"
	/* 0x0C7 */ unsigned char default_sound_type; // 0 = Stereo, 1 = Surround, 2 = Mono
	/* 0x0C8 */ unsigned char default_sfx_volume; // 0 - 40
	/* 0x0C9 */ unsigned char default_music_volume; // 0 - 40
	/* 0x0CA */ unsigned char default_screen_ratio; // 0 = Normal, 1 = Widescreen
	/* 0x0CB */ unsigned char default_camera_type; // 0 = Free, 1 = Follow
	/* 0x0CC */ unsigned char default_camera_mode; // 0 = Inverted, 1 = Non-Inverted
	/* 0x0CD */ char unk_cd[8];
	/* 0x0D5 */ moves_pregiven_bitfield moves_pregiven; // Bitfield, Size 0x6
	/* 0x0DB */ unsigned char seasonal_changes; // 0 = None, 1 = Halloween, 2 = Christmas
	/* 0x0DC */ char unk_DC[4];
	/* 0x0E0 */ fairy_activations fairy_triggers_disabled;
	/* 0x0E2 */ unsigned short helm_hurry_start;
	/* 0x0E4 */ short helm_hurry_bonuses[0xE];
	/* 0x100 */ char fairy_rando_on;
	/* 0x101 */ LocationVisuals location_visuals; // Bitfield for visual hints of what is inside a location.
	/* 0x102 */ char microhints; // 0 = Off, 1 = GGone/Monkeyport, 2 = GGone/MPort, Instruments in Helm
	/* 0x103 */ char random_switches;
	/* 0x104 */ char slam_level[7]; // Level of slam required to slam a switch in a level (if random_switches is on)
	/* 0x10B */ char isles_cb_rando; // Gives 5 extra medals and handles appropriately
	/* 0x10C */ unsigned char starting_map; // 0 = Isles - from escape
	/* 0x10D */ unsigned char starting_exit;
	/* 0x10E */ unsigned char tns_portal_rando_on;
	/* 0x10F */ unsigned char remove_oscillation_effects; // Removes water oscillation + Seasick Ship interior rocking
	/* 0x110 */ unsigned char arcade_reward; // Reward Index for R2 of Arcade
	/* 0x111 */ unsigned char jetpac_reward; // Reward Index for Jetpac 5000 Pts
	/* 0x112 */ unsigned char medal_cb_req; // 0 = default (75). int (1-100)
	/* 0x113 */ FreeTradeAgreement any_kong_items;
	/* 0x114 */ char fix_lanky_tiny_prod;
	/* 0x115 */ unsigned char progressive_hint_gb_cap; // 0 = Off, 1 or more = Hints are rewarded for collecting GBs, rather than hint doors, 35th hint is unlocked at x
	/* 0x116 */ char cutscene_skip_setting; // 0 = Off, 1 = On Button Press, 2 = Automatic
	/* 0x117 */ unsigned char enabled_pkmnsnap_enemies[5]; // Bitfield
	/* 0x11C */ char krusha_slot; // -1 = Not replacing a kong. 0-4 = Replaces kong of relevant index. Takes priority over disco chunky
	/* 0x11D */ unsigned char win_condition; // See vars.h for enum
	/* 0x11E */ char tns_indicator;
	/* 0x11F */ char unk_11F[7];
	/* 0x126 */ char resolve_bonus; // Bitfield. 0000 0001 = auto-complete bonus barrels. 0000 0010 = auto-complete helm barrels. 0 = Off. 3 = Resolve Helm & Bonus Barrels
	/* 0x127 */ unsigned char keys_preturned; // Bitfield. 0000 0001 = Key 1 turned, 0000 0010 = Key 2 turned etc. Eg. 0x7F = 0111 1111 = All keys except Key 8 turned
	/* 0x128 */ char disable_drops; // 0 = Off. 1 = No Klump/Melon/Ammo Crate Drops
	/* 0x129 */ unsigned char hash[5];
	/* 0x12E */ char music_rando_on; // 0 = Off, 1 = Music Rando on, apply extra data shuffle
	/* 0x12F */ char disco_chunky; // 0 = Normal, 1 = Disco. Overriden by Krusha if Krusha replaces Chunky
	/* 0x130 */ LZREntrance ballroom_to_museum; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
	/* 0x132 */ LZREntrance museum_to_ballroom; // Same as "aztec_beetle_enter" but for the loading zone dictated by the nametc
	/* 0x134 */ char shop_indicator_on; // 0 = Off, 1 = Only kong displayed, 2 = Both item and kong
	/* 0x135 */ char warp_to_isles_enabled; // 0 = Off, 1 = Add Warp to Isles option
	/* 0x136 */ char unk_136[2];
	/* 0x138 */ char activate_all_bananaports; // 0 = Vanilla, 1 = Most bananaports are activated from the start
	/* 0x139 */ char dpad_visual_enabled; // 0 = Vanilla, 1 = Visual shown
	/* 0x13A */ char fast_warp; // 0 = Vanilla, 1 = Use Multiplayer warp
	/* 0x13B */ char short_bosses; // 0 = Vanilla fights, 1 = Short fights
	/* 0x13C */ unsigned char coinreq_cavesbeetle;
	/* 0x13D */ unsigned char coinreq_aztecbeetle;
	/* 0x13E */ unsigned char coinreq_factorycar;
	/* 0x13F */ unsigned char coinreq_sealrace;
	/* 0x140 */ unsigned char coinreq_castlecar;
	/* 0x141 */ unsigned char coinreq_japescart;
	/* 0x142 */ unsigned char coinreq_fungicart;
	/* 0x143 */ unsigned char coinreq_castlecart;
	/* 0x144 */ char unk_144[8];
	/* 0x14C */ unsigned char lobbies_open_bitfield; // hccf gfaj
	/* 0x14D */ char perma_lose_kongs; // 0 = Off, 1 = On. AKA "iateyourpie mode"
	/* 0x14E */ unsigned char ice_trap_flag_alloc;
	/* 0x14F */ char prevent_tag_spawn; // 0 = Off. 1 = Prevents tags from spawning except in T&S
	/* 0x150 */ char ice_traps_damage;
	/* 0x151 */ char starting_kong; // Kong you start as upon file init
	/* 0x152 */ char free_target_japes; // Kong you free in Japes
	/* 0x153 */ char free_source_japes; // Kong who frees the kong in Japes
	/* 0x154 */ char free_target_llama; // Kong you free in Llama Temple
	/* 0x155 */ char free_source_llama; // Kong who frees the kong in Llama Temple
	/* 0x156 */ char free_target_ttemple; // Kong you free in Tiny Temple
	/* 0x157 */ char free_source_ttemple; // Kong who frees the kong in Tiny Temple
	/* 0x158 */ char free_target_factory; // Kong you free in Factory
	/* 0x159 */ char free_source_factory; // Kong who frees the kong in Factory
	/* 0x15A */ char arcade_reward_idx; // Purely used for the arcade sprite in colorblind mode
	/* 0x15B */ char auto_keys; // 0 = Vanilla, 1 = Keys turn in as soon as you get them
	/* 0x15C */ short matching_game_sounds[8]; // Sound effect 0 is treated as "sound not randomized"
	/* 0x16C */ char piano_game_order[7]; // Each item denotes a key, normally CBCDECA (2123420). A = 0, 1 = B, 2 = C, 3 = D, 4 = E, 5 = F
	/* 0x173 */ char dartboard_order[6]; // Each item denotes a picture. 0 = Crystal, 1 = Melon, 2 = Banana, 3 = Orange, 4 = Ammo Crate, 5 = Medal, 6 = Coin, 7 = Film
	/* 0x179 */ char unk_179[2];
	/* 0x17B */ char kut_out_phases[3]; // 0 = Phase 1, 1 = Phase 2, 2 = Phase 3, 3 = Phase 4 (Unused)
	/* 0x17E */ unsigned char b_locker_requirements[8];
	/* 0x186 */ char unk_186[0x190-0x186];
	/* 0x190 */ char helm_order[5]; // Each item is a place in the order. -1 for an empty slot. For each item, 0 = DK, 1 = Chunky, 2 = Tiny, 3 = Lanky, 4 = Diddy. DK has to either be first or not present.
	/* 0x195 */ char disable_rotating_crown; // 0 = Checks flag, 1 = Disabled
	/* 0x196 */ char misc_cosmetic_on;
	/* 0x197 */ unsigned char unk_197[0x1A2 - 0x197];
	/* 0x1A2 */ LZREntrance blast_entrances[7];
	/* 0x1B0 */ int password;
	/* 0x1B4 */ char unk_1B4;
	/* 0x1B5 */ unsigned char pppanic_fairy_model; // 0 = Vanilla
	/* 0x1B6 */ unsigned char unk_1B6; // 0 = Vanilla
	/* 0x1B7 */ DisabledMusicStruct disabled_music;
	/* 0x1B8 */ unsigned char kong_models[5];
	/* 0x1BD */ char unk_1bd[0x1C6 - 0x1BD];
	/* 0x1C6 */ RandomSwitchesSetting switchsanity; // Size 0x15
	/* 0x1DB */ unsigned char fungi_time_of_day_setting; // See fungi_time enum
	/* 0x1DC */ unsigned char galleon_water_raised;
	/* 0x1DD */ unsigned char krool_requirements; // K Rool bitfield 8765 4321
	/* 0x1DE */ RemovedBarriers removed_barriers; // Size: 2
	/* 0x1E0 */ FasterChecks faster_checks; // Size: 1
	/* 0x1E1 */ char big_head_mode; // 0 = off, 1 = on, 2 = small head
	/* 0x1E2 */ BooleanModelSwaps model_swaps; // Size: 1
	/* 0x1E3 */ unsigned char chunky_phase_krool_slam_req; // Slam level required for Chunky Phase
  	/* 0x1E4 */ unsigned char pause_hints_colored;
	/* 0x1E5 */ char unk_1e5[0x1E7-0x1E5];
	/* 0x1E7 */ char balloon_sound;
	/* 0x1E8 */ unsigned char jetman_rgb[3];
	/* 0x1EB */ unsigned char mermaid_requirement; // Amount of pearls to get the mermaid reward
	/* 0x1EC */ unsigned char check_shop_flags; // Bitfield of pre-given shops: rfcs 0000. r = Cranky, f = Funky, c = Candy, s = Snide
	/* 0x1ED */ unsigned char show_music_name;
	/* 0x1EE */ unsigned char global_coins;
} varspace;