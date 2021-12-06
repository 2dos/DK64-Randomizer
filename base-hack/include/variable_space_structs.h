typedef struct varspace {
	/* 0x000 */ char level_order_rando_on;
	/* 0x001 */ char level_order[7];
	/* 0x008 */ short troff_scoff_count[7];
	/* 0x016 */ unsigned char blocker_normal_count[8];
	/* 0x01E */ unsigned char blocker_cheat_count[8];
	/* 0x026 */ short key_flags[8];
	/* 0x036 */ char unlock_kongs;
	/* 0x037 */ char unlock_moves;
	/* 0x038 */ char fast_start_beginning;
	/* 0x039 */ char camera_unlocked;
	/* 0x03A */ char tag_anywhere;
	/* 0x03B */ char fast_start_helm;
	/* 0x03C */ char crown_door_open;
	/* 0x03D */ char coin_door_open;
	/* 0x03E */ char quality_of_life;
} varspace;