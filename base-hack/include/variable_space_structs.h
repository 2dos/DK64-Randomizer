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
} varspace;