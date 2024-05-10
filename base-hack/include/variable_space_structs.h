typedef struct varspace {
	/* 0x000 */ char level_order_rando_on; // 0 = Level Order Rando off, 1 = On
	/* 0x001 */ char level_order[7]; // The level order (Item 1 = Level 1. 0=Japes,1=Aztec,2=Factory,3=Galleon,4=Fungi,5=Caves,6=Castle)
	/* 0x008 */ short troff_scoff_count[7]; // Troff n Scoff requirement for the 7 levels (Item 1 is Japes, Item 2 is Aztec etc.)
	/* 0x016 */ unsigned char blocker_normal_count[8]; // B. Locker count for the 8 lobbies (Item 1 is Japes, Item 2 is Aztec etc.)
	/* 0x01E */ short key_flags[7]; // key given in each level. (Item 1 is Japes etc. flags=[0x1A,0x4A,0x8A,0xA8,0xEC,0x124,0x13D] <- Item 1 of this array is Key 1 etc.)
	/* 0x02C */ char unlock_kongs; // 0 = Kongs not automatically unlocked, 1 = On
	/* 0x02D */ char unlock_moves; // 0 = Moves not granted at the start of a new file. 1 = On
	/* 0x02E */ char fast_start_beginning; // 0 = "Fast Start" setting not applied. 1 = On
	/* 0x02F */ char camera_unlocked; // 0 = Camera not unlocked from the start of a new file. 1 = On
	/* 0x030 */ char tag_anywhere; // 0 = Tag Anywhere buttons not enabled. 1 = Enabled
	/* 0x031 */ char fast_start_helm; // 0 = "Fast Start for Helm" setting not applied. 1 = Applied
	/* 0x032 */ char crown_door_open; // 0 = Crown Door not opened by default. 1 = Opened by default
	/* 0x033 */ char coin_door_open; // 0 = Coin Door not opened by default. 1 = Opened by default. 2 = Only requires RW Coin. 3 = Only requires Nin Coin.
	/* 0x034 */ char item_rando; // 0 = Off, 1 = On
	/* 0x035 */ char price_rando_on; // 0 = Price Randomizer off, 1 = On
	/* 0x036 */ char rareware_gb_fairies; // Fairy requirement to access Rareware GB
	/* 0x037 */ char k_rool_toes[10];
	/* 0x041 */ char randomize_toes;
	/* 0x042 */ char random_drops; // Random enemy item drops
	/* 0x043 */ char colorblind_mode; // 0 = Off, 1 = Prot, 2 = Deut, 3 = Trit
	/* 0x044 */ char dark_mode_textboxes; // 0 = Light Mode, 1 = Dark Mode
	/* 0x045 */ unsigned char slam_prices[2]; // Array of simian slam upgrade prices: [1,2]. First item is super simian slam (blue), 2nd is super duper simian slam (red)
	/* 0x047 */ char call_parent_filter; // Calls filter to remove "unnecessary" links from the parent chain
	/* 0x048 */ char arcade_order[4]; // 01 = 25m, 04 = 50m, 03 = 75m, 02 = 100m
	/* 0x04C */ char crown_door_item;
	/* 0x04D */ unsigned char crown_door_item_count;
	/* 0x04E */ char coin_door_item;
	/* 0x04F */ unsigned char coin_door_item_count;
	/* 0x050 */ unsigned char aztec_beetle_reward;
	/* 0x051 */ unsigned char caves_beetle_reward;
	/* 0x052 */ char disable_wrinkly_kong_requirement; // Disable Kongs being required to access a wrinkly door
	/* 0x053 */ unsigned char ammo_belt_prices[2]; // Array of ammo belt prices: [1,2]. 1 item for each level of ammo belt
	/* 0x055 */ unsigned char instrument_upgrade_prices[3]; // Array of instrument upgrade prices: [1,2,3]. 1st and 3rd items are the Upgrades 1 and 2 respectively. 2nd item is the 3rd melon cost
	/* 0x058 */ char k_rool_order[5]; // Order of K. Rool phases: [0,1,2,3,4] dictates DK->Diddy->Lanky->Tiny->Chunky. If K. Rool is being shortened to less than 5 phases, put the unused phases as -1
	/* 0x05D */ char randomize_more_loading_zones; // 0 = Not randomizing loading zones inside levels. 1 = On
	/* 0x05E */ LZREntrance aztec_beetle_enter; // Map and exit replacing the loading zone which normally bring you to Aztec Beetle Race from Aztec. First byte is map, second byte is exit value. Same logic applies until (and including) "enter_levels[7]"
	/* 0x060 */ LZREntrance aztec_beetle_exit; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
	/* 0x062 */ LZREntrance caves_beetle_exit; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
	/* 0x064 */ LZREntrance seal_race_exit; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
	/* 0x066 */ LZREntrance factory_car_exit; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
	/* 0x068 */ LZREntrance castle_car_exit; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
	/* 0x06A */ LZREntrance seasick_ship_enter; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
	/* 0x06C */ LZREntrance fungi_minecart_enter; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
	/* 0x06E */ LZREntrance fungi_minecart_exit; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
	/* 0x070 */ LZREntrance japes_minecart_exit; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
	/* 0x072 */ LZREntrance castle_minecart_exit; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
	/* 0x074 */ LZREntrance castle_lobby_enter; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
	/* 0x076 */ LZREntrance k_rool_exit; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
	/* 0x078 */ LZREntrance exit_levels[8]; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
	/* 0x088 */ LZREntrance enter_levels[7]; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
	/* 0x096 */ char fps_on; // 0 = FPS display off, 1 = On.
	/* 0x097 */ char boss_kong[7]; // Array of kongs used to fight the boss, in order of vanilla level sequence. If no changes are made, supply the vanilla values
	/* 0x09E */ unsigned char boss_map[7]; // Array of boss maps, in order of vanilla level sequence. If no changes are made, supply the vanilla values
	/* 0x0A5 */ char damage_multiplier; // 1 = Normal. 2 = Double. Any value greater than 11 will be 1 hit KO
	/* 0x0A6 */ char no_health_refill; // 0 = Vanilla. 1 =  No health refill for Tag Barrels, "Voiding", Bonus Barrels, Fairies, K. Rool Health Refills
	/* 0x0A7 */ char move_rando_on; // O = No Move Randomization. 1 = On.
	/* 0x0A8 */ unsigned char tbarrel_prices[4]; // Array of training barrel move prices. First is dive, then orange, then barrel, then vine
	/* 0x0AC */ unsigned char fairy_prices[2]; // Array of fairy move prices. First is camera, second is shockwave. Shockwave/Camera combo price is calculated as the sum of the two
	/* 0x0AE */ char helm_hurry_mode; // 0 = Off, 1 = On: Starting a new file summons the helm timer, each BP adds 2 minutes to the clock, timing out disables saving.
	/* 0x0AF */ char archipelago; // DK64R is being run through Archipelago
	/* 0x0B0 */ quality_options quality_of_life; // Size: 4
	/* 0x0B4 */ char unk_B0[0xC3 - 0xB4];
	/* 0x0C3 */ char outlined_crosshair;
	/* 0x0C4 */ ROMFlags rom_flags;
	/* 0x0C5 */ char enemy_item_rando; // Determines whether to use standard enemy item drop table or a custom table
	/* 0x0C6 */ HardModeSettings hard_mode; // Colloquially known as "Seed of Death"
	/* 0x0C7 */ unsigned char default_sound_type; // 0 = Stereo, 1 = Surround, 2 = Mono
	/* 0x0C8 */ unsigned char default_sfx_volume; // 0 - 40
	/* 0x0C9 */ unsigned char default_music_volume; // 0 - 40
	/* 0x0CA */ unsigned char default_screen_ratio; // 0 = Normal, 1 = Widescreen
	/* 0x0CB */ unsigned char default_camera_type; // 0 = Free, 1 = Follow
	/* 0x0CC */ unsigned char default_camera_mode; // 0 = Inverted, 1 = Non-Inverted
	/* 0x0CD */ unsigned char crypt_lever_order[3]; // 0 = No lever, 1-6 = code
	/* 0x0D0 */ unsigned char mill_lever_order[5]; // 0 = no lever, 1-3 = Code
	/* 0x0D5 */ moves_pregiven_bitfield moves_pregiven; // Bitfield, Size 0x6
	/* 0x0DB */ unsigned char seasonal_changes; // 0 = None, 1 = Halloween, 2 = Christmas
	/* 0x0DC */ unsigned short japes_rock_item; // Actor ID of item that spawns from destroying the rock covering Japes Underground
	/* 0x0DE */ unsigned short vulture_item; // Actor ID of item that the vulture in Tiny Temple has
	/* 0x0E0 */ fairy_activations fairy_triggers_disabled;
	/* 0x0E2 */ unsigned short helm_hurry_start;
	/* 0x0E4 */ short helm_hurry_bonuses[0xE];
	/* 0x100 */ char fairy_rando_on;
	/* 0x101 */ char location_visuals; // Bitfield for visual hints of what is inside a location. 0000 0abc. a = Crowns , b = Boss Doors , c = Bonus Barrels
	/* 0x102 */ char microhints; // 0 = Off, 1 = GGone/Monkeyport, 2 = GGone/MPort, Instruments in Helm
	/* 0x103 */ char random_switches;
	/* 0x104 */ char slam_level[7]; // Level of slam required to slam a switch in a level (if random_switches is on)
	/* 0x10B */ unsigned char remove_rock_bunch; // Remove rock bunch in Jungle Japes
	/* 0x10C */ unsigned char starting_map; // 0 = Isles - from escape
	/* 0x10D */ unsigned char starting_exit;
	/* 0x10E */ unsigned char tns_portal_rando_on;
	/* 0x10F */ unsigned char remove_oscillation_effects; // Removes water oscillation + Seasick Ship interior rocking
	/* 0x110 */ unsigned char arcade_reward; // Reward Index for R2 of Arcade
	/* 0x111 */ unsigned char jetpac_reward; // Reward Index for Jetpac 5000 Pts
	/* 0x112 */ unsigned char medal_cb_req; // 0 = default (75). int (1-100)
	/* 0x113 */ unsigned char any_kong_items; // Bitfield 0000 00ba. a = All items except blueprints disabling kong check. b = Blueprints disable kong check.
	/* 0x114 */ unsigned char increase_tns_boss_lighting; // Increases lighting when awaiting to enter boss to make it easier to see item reward preview
	/* 0x115 */ unsigned char progressive_hint_gb_cap; // 0 = Off, 1 or more = Hints are rewarded for collecting GBs, rather than hint doors, 35th hint is unlocked at x
	/* 0x116 */ char cutscene_skip_setting; // 0 = Off, 1 = On Button Press, 2 = Automatic
	/* 0x117 */ unsigned char enabled_pkmnsnap_enemies[5]; // Bitfield
	/* 0x11C */ char krusha_slot; // -1 = Not replacing a kong. 0-4 = Replaces kong of relevant index. Takes priority over disco chunky
	/* 0x11D */ unsigned char win_condition; // See vars.h for enum
	/* 0x11E */ char tns_indicator;
	/* 0x11F */ char wrinkly_rando_on;
	/* 0x120 */ char kut_out_kong_order[5]; // Value of item: 0 = DK, 1 = Diddy, 2 = Lanky, 3 = Tiny, 4 = Chunky. Kongs can be repeated
	/* 0x125 */ unsigned char remove_blockers; // Bitfield of B. Lockers to remove. 0 = Remove None. 0x7F = remove all except Helm Lobby. 0xFF = Remove all.
	/* 0x126 */ char resolve_bonus; // Bitfield. 0000 0001 = auto-complete bonus barrels. 0000 0010 = auto-complete helm barrels. 0 = Off. 3 = Resolve Helm & Bonus Barrels
	/* 0x127 */ unsigned char keys_preturned; // Bitfield. 0000 0001 = Key 1 turned, 0000 0010 = Key 2 turned etc. Eg. 0x7F = 0111 1111 = All keys except Key 8 turned
	/* 0x128 */ char disable_drops; // 0 = Off. 1 = No Klump/Melon/Ammo Crate Drops
	/* 0x129 */ char hash[5];
	/* 0x12E */ char music_rando_on; // 0 = Off, 1 = Music Rando on, apply extra data shuffle
	/* 0x12F */ char disco_chunky; // 0 = Normal, 1 = Disco. Overriden by Krusha if Krusha replaces Chunky
	/* 0x130 */ LZREntrance ballroom_to_museum; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
	/* 0x132 */ LZREntrance museum_to_ballroom; // Same as "aztec_beetle_enter" but for the loading zone dictated by the nametc
	/* 0x134 */ char shop_indicator_on; // 0 = Off, 1 = Only kong displayed, 2 = Both item and kong
	/* 0x135 */ char warp_to_isles_enabled; // 0 = Off, 1 = Add Warp to Isles option
	/* 0x136 */ unsigned char klaptrap_color_bbother; // 0 = Green, 1 = Purple, 2 = Red
	/* 0x137 */ char open_level_sections; // 0 = Off, 1 = On
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
	/* 0x144 */ unsigned char menusky_rgb_low[3];
	/* 0x147 */ unsigned char menusky_rgb_high[3];
	/* 0x14A */ char patch_kutoutkongs; // 0 = Off, 1 = Forces exit kong to be boss required kong
	/* 0x14B */ char shop_hints; // 0 = Off, 1 = Hints at the beginning of shops
	/* 0x14C */ unsigned char lobbies_open_bitfield; // hccf gfaj
	/* 0x14D */ char perma_lose_kongs; // 0 = Off, 1 = On. AKA "iateyourpie mode"
	/* 0x14E */ char disable_boss_kong_check; // 0 = Enable Check (Vanilla), 1 = Disabled
	/* 0x14F */ char prevent_tag_spawn; // 0 = Off. 1 = Prevents tags from spawning except in T&S
	/* 0x150 */ char jetpac_medal_requirement; // Lowest amount of medals required to access Jetpac. 0 = Don't apply new requirement
	/* 0x151 */ char starting_kong; // Kong you start as upon file init
	/* 0x152 */ char free_target_japes; // Kong you free in Japes
	/* 0x153 */ char free_source_japes; // Kong who frees the kong in Japes
	/* 0x154 */ char free_target_llama; // Kong you free in Llama Temple
	/* 0x155 */ char free_source_llama; // Kong who frees the kong in Llama Temple
	/* 0x156 */ char free_target_ttemple; // Kong you free in Tiny Temple
	/* 0x157 */ char free_source_ttemple; // Kong who frees the kong in Tiny Temple
	/* 0x158 */ char free_target_factory; // Kong you free in Factory
	/* 0x159 */ char free_source_factory; // Kong who frees the kong in Factory
	/* 0x15A */ char version; // 0 = Live, 1 = Dev Site, 2 = Superuser
	/* 0x15B */ char auto_keys; // 0 = Vanilla, 1 = Keys turn in as soon as you get them
	/* 0x15C */ short matching_game_sounds[8]; // Sound effect 0 is treated as "sound not randomized"
	/* 0x16C */ char piano_game_order[7]; // Each item denotes a key, normally CBCDECA (2123420). A = 0, 1 = B, 2 = C, 3 = D, 4 = E, 5 = F
	/* 0x173 */ char dartboard_order[6]; // Each item denotes a picture. 0 = Crystal, 1 = Melon, 2 = Banana, 3 = Orange, 4 = Ammo Crate, 5 = Medal, 6 = Coin, 7 = Film
	/* 0x179 */ char remove_high_requirements; // 0 = Off, 1 = On. Removes high requirements that lock certain areas.
	/* 0x17A */ char fast_gbs; //0 = Off, 1 = On. Makes normally slow Golden Bananas faster.
	/* 0x17B */ char kut_out_phases[3]; // 0 = Phase 1, 1 = Phase 2, 2 = Phase 3, 3 = Phase 4 (Unused)
	/* 0x17E */ char dk_face_puzzle_init[9];
	/* 0x187 */ char chunky_face_puzzle_init[9];
	/* 0x190 */ char helm_order[5]; // Each item is a place in the order. -1 for an empty slot. For each item, 0 = DK, 1 = Chunky, 2 = Tiny, 3 = Lanky, 4 = Diddy. DK has to either be first or not present.
	/* 0x195 */ char disable_rotating_crown; // 0 = Checks flag, 1 = Disabled
	/* 0x196 */ char misc_cosmetic_on;
	/* 0x197 */ rgb skybox_colors[8];
	/* 0x1AF */ char pppanic_klaptrap_color; // 0 = Green, 1 = Purple, 2 = Red
	/* 0x1B0 */ char sseek_klaptrap_color; // 0 = Green, 1 = Purple, 2 = Red
	/* 0x1B1 */ unsigned char wrinkly_rgb[3];
	/* 0x1B4 */ char true_widescreen; // Port of the widescreen hack from gamemasterplc
	/* 0x1B5 */ unsigned char pppanic_fairy_model; // 0 = Vanilla
	/* 0x1B6 */ unsigned char tttrouble_turtle_model; // 0 = Vanilla
	/* 0x1B7 */ DisabledMusicStruct disabled_music;
	/* 0x1B8 */ unsigned short diddy_rnd_codes[3]; // 4 bits assigned for each part of the combination
	/* 0x1BE */ unsigned char jetpac_enemy_order[8]; // Indexes 0-7 to represent enemy difficulty
	/* 0x1C6 */ RandomSwitchesSetting switchsanity; // Size 0x15
	/* 0x1DB */ unsigned char fungi_time_of_day_setting; // See fungi_time enum
	/* 0x1DC */ unsigned char galleon_water_raised;
	/* 0x1DD */ unsigned char krool_requirements; // K Rool bitfield 8765 4321
	/* 0x1DE */ RemovedBarriers removed_barriers; // Size: 2
	/* 0x1E0 */ FasterChecks faster_checks; // Size: 2
	/* 0x1E2 */ BooleanModelSwaps model_swaps; // Size: 1
	/* 0x1E3 */ unsigned char balanced_krool_reqs; // Changes K Rool to require blast for DK Phase and just slam 1 for Chunky Phase
	/* 0x1E4 */ unsigned char pause_hints_colored;
} varspace;