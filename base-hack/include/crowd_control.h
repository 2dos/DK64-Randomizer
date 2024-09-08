typedef enum cc_state {
    CC_READY, // 0
    CC_ENABLING, // 1
    CC_ENABLED, // 2
    CC_DISABLING, // 3
    CC_LOCKED, // 4
} cc_state;

typedef struct cc_effects {
	/* 0x000 */ unsigned char drunky_chunky;
    /* 0x001 */ unsigned char disable_tag_anywhere;
    /* 0x002 */ unsigned char ice_trap;
    /* 0x003 */ unsigned char rockfall;
    /* 0x004 */ unsigned char warp_to_rap;
    /* 0x005 */ unsigned char get_kaught;
    /* 0x006 */ unsigned char balloon;
    /* 0x007 */ unsigned char slip;
    /* 0x008 */ unsigned char tag;
    /* 0x009 */ unsigned char backflip;
    /* 0x00A */ unsigned char ice_floor;
    /* 0x00B */ unsigned char get_out;
    /* 0x00C */ unsigned char mini;
    /* 0x00D */ unsigned char spawn_boulder;
    /* 0x00E */ unsigned char animal_transform;
} cc_effects;