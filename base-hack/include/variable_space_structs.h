typedef struct varspace {
	/* 0x000 */ char level_order_rando_on;
	/* 0x001 */ char level_order[7];
	/* 0x008 */ short troff_scoff_count[7];
	/* 0x016 */ unsigned char blocker_normal_count[8];
	/* 0x01E */ short key_flags[7];
	/* 0x02C */ char unlock_kongs;
	/* 0x02D */ char unlock_moves;
	/* 0x02E */ char fast_start_beginning;
	/* 0x02F */ char camera_unlocked;
	/* 0x030 */ char tag_anywhere;
	/* 0x031 */ char fast_start_helm;
	/* 0x032 */ char crown_door_open;
	/* 0x033 */ char coin_door_open;
	/* 0x034 */ char quality_of_life;
} varspace;