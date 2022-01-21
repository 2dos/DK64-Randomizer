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
	/* 0x033 */ char coin_door_open; // 0 = Coin Door not opened by default. 1 = Opened by default
	/* 0x034 */ char quality_of_life; // 0 = Quality of life features not applied. 1 = Applied
	/* 0x035 */ char price_rando_on; // 0 = Price Randomizer off, 1 = On
	/* 0x036 */ unsigned char special_move_prices[5][3]; // Array of an array of prices [[1,2,3],[1,2,3],[1,2,3],[1,2,3],[1,2,3]]. Each item of the parent array is for a kong, each item of the sub arrays is the price of the moves in order of their vanilla purchase (eg. DK: Baboon Blast > Strong Kong > Gorilla Grab)
	/* 0x045 */ unsigned char slam_prices[2]; // Array of simian slam upgrade prices: [1,2]. First item is super simian slam (blue), 2nd is super duper simian slam (red)
	/* 0x047 */ unsigned char gun_prices[5]; // Array of prices for the base gun for each kong. [1,2,3,4,5]. 1 item for each kong
	/* 0x04C */ unsigned char instrument_prices[5]; // Array of prices for the base instrument for each kong. [1,2,3,4,5]. 1 item for each kong
	/* 0x051 */ unsigned char gun_upgrade_prices[2]; // Array of gun upgrade prices: [1,2]. First item is homing ammo upgrade. 2nd is Sniper Scope (Zoom)
	/* 0x053 */ unsigned char ammo_belt_prices[2]; // Array of ammo belt prices: [1,2]. 1 item for each level of ammo belt
	/* 0x055 */ unsigned char instrument_upgrade_prices[3]; // Array of instrument upgrade prices: [1,2,3]. 1st and 3rd items are the Upgrades 1 and 2 respectively. 2nd item is the 3rd melon cost
	/* 0x058 */ char k_rool_order[5]; // Order of K. Rool phases: [0,1,2,3,4] dictates DK->Diddy->Lanky->Tiny->Chunky. If K. Rool is being shortened to less than 5 phases, put the unused phases as -1
	/* 0x05D */ char randomize_more_loading_zones; // 0 = Not randomizing loading zones inside levels. 1 = On
	/* 0x05E */ unsigned short aztec_beetle_enter; // Map and exit replacing the loading zone which normally bring you to Aztec Beetle Race from Aztec. First byte is map, second byte is exit value. Same logic applies until (and including) "enter_levels[7]"
	/* 0x060 */ unsigned short aztec_beetle_exit; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
	/* 0x062 */ unsigned short caves_beetle_exit; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
	/* 0x064 */ unsigned short seal_race_exit; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
	/* 0x066 */ unsigned short factory_car_exit; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
	/* 0x068 */ unsigned short castle_car_exit; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
	/* 0x06A */ unsigned short seasick_ship_enter; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
	/* 0x06C */ unsigned short fungi_minecart_enter; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
	/* 0x06E */ unsigned short fungi_minecart_exit; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
	/* 0x070 */ unsigned short japes_minecart_exit; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
	/* 0x072 */ unsigned short castle_minecart_exit; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
	/* 0x074 */ unsigned short castle_lobby_enter; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
	/* 0x076 */ unsigned short k_rool_exit; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
	/* 0x078 */ unsigned short exit_levels[8]; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
	/* 0x088 */ unsigned short enter_levels[7]; // Same as "aztec_beetle_enter" but for the loading zone dictated by the name
	/* 0x096 */ char fps_on; // 0 = FPS display off, 1 = On.
	/* 0x097 */ char boss_kong[7]; // Array of kongs used to fight the boss, in order of vanilla level sequence. If no changes are made, supply the vanilla values
	/* 0x09E */ unsigned char boss_map[7]; // Array of boss maps, in order of vanilla level sequence. If no changes are made, supply the vanilla values
	/* 0x0A5 */ char damage_multiplier; // 1 = Normal. 2 = Double. Any value greater than 11 will be 1 hit KO
	/* 0x0A6 */ char no_health_refill; // 0 = Vanilla. 1 =  No health refill for Tag Barrels, "Voiding", Bonus Barrels, Fairies, K. Rool Health Refills
	/* 0x0A7 */ char move_rando_on; // O = No Move Randomization. 1 = On.
	/* 0x0A8 */ unsigned char dk_crankymoves[7]; // First 4 bits indicates the moves type, 0 = Moves, 1 = Slam, 2 = Guns, 3 = Ammo Belt, 4 = Instrument, 0xF = No Upgrade. Last 4 bytes indicate move level (eg. 1 = Baboon Blast, 2 = Strong Kong, 3 = Gorilla Grab). Each item in the array indicates the level it is given (eg. 1st slot is purchased in Japes, 2nd for Aztec etc.)
	/* 0x0AF */ unsigned char diddy_crankymoves[7]; // See "dk_crankymoves"
	/* 0x0B6 */ unsigned char lanky_crankymoves[7]; // See "dk_crankymoves"
	/* 0x0BD */ unsigned char tiny_crankymoves[7]; // See "dk_crankymoves"
	/* 0x0C4 */ unsigned char chunky_crankymoves[7]; // See "dk_crankymoves"
	/* 0x0CB */ unsigned char dk_funkymoves[7]; // See "dk_crankymoves"
	/* 0x0D2 */ unsigned char diddy_funkymoves[7]; // See "dk_crankymoves"
	/* 0x0D9 */ unsigned char lanky_funkymoves[7]; // See "dk_crankymoves"
	/* 0x0E0 */ unsigned char tiny_funkymoves[7]; // See "dk_crankymoves"
	/* 0x0E7 */ unsigned char chunky_funkymoves[7]; // See "dk_crankymoves"
	/* 0x0EE */ unsigned char dk_candymoves[7]; // See "dk_crankymoves"
	/* 0x0F5 */ unsigned char diddy_candymoves[7]; // See "dk_crankymoves"
	/* 0x0FC */ unsigned char lanky_candymoves[7]; // See "dk_crankymoves"
	/* 0x103 */ unsigned char tiny_candymoves[7]; // See "dk_crankymoves"
	/* 0x10A */ unsigned char chunky_candymoves[7]; // See "dk_crankymoves"
	/* 0x111 */ char kut_out_kong_order[5]; // Value of item: 0 = DK, 1 = Diddy, 2 = Lanky, 3 = Tiny, 4 = Chunky. Kongs can be repeated
	/* 0x116 */ unsigned char remove_blockers; // Bitfield of B. Lockers to remove. 0 = Remove None. 0x7F = remove all except Helm Lobby. 0xFF = Remove all.
	/* 0x117 */ char resolve_bonus; // Bitfield. 0000 0001 = auto-complete bonus barrels. 0000 0010 = auto-complete helm barrels. 0 = Off. 3 = Resolve Helm & Bonus Barrels
	/* 0x118 */ unsigned char keys_preturned; // Bitfield. 0000 0001 = Key 1 turned, 0000 0010 = Key 2 turned etc. Eg. 0x7F = 0111 1111 = All keys except Key 8 turned
} varspace;