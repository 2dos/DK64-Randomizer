typedef enum check_types {
    /* 0x000 */ CHECK_GB,
    /* 0x001 */ CHECK_CROWN,
    /* 0x002 */ CHECK_KEY,
    /* 0x003 */ CHECK_MEDAL,
    /* 0x004 */ CHECK_RWCOIN,
    /* 0x005 */ CHECK_FAIRY,
    /* 0x006 */ CHECK_NINCOIN,
    /* 0x007 */ CHECK_BP,
    /* 0x008 */ CHECK_KONG,
    /* 0x009 */ CHECK_BEAN,
    /* 0x00A */ CHECK_PEARLS,
    /* 0x00B */ CHECK_RAINBOW,
    /* 0x00C */ CHECK_HINTS,
    /* 0x00D */ CHECK_CRATE,
    /* 0x00E */ CHECK_SHOPS,
    /* ----- */ CHECK_TERMINATOR,
} check_types;

/*
    Please don't change the `ROTATION_SPLIT` line. Explanation on why is in `build/adjust_pause_rotation.py`
*/
#define ROTATION_SPLIT 273
#define ROTATION_SPLIT_TOTALS 273
#define ROTATION_TOTALS_REDUCTION 0
#define FEATHER_SPRITE_START 6154
#define BEANSPIN_SPRITE_START 6173
#define POTIONSPIN_SPRITE_START 6205
#define FOOL_SPRITE_START 6162