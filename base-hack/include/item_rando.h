typedef enum kongcheck_enum {
    /* 0 */ KONGCHECK_JAPES,
    /* 1 */ KONGCHECK_LLAMA,
    /* 2 */ KONGCHECK_ICETEMPLE,
    /* 3 */ KONGCHECK_FACTORY,
} kongcheck_enum;

typedef struct CountSpecialStruct {
    unsigned char nintendo_coin : 1; // 0x80
    unsigned char rareware_coin : 1; // 0x40
    unsigned char bean : 1; // 0x20
    unsigned char unk3 : 1;
    unsigned char unk4 : 1;
    unsigned char unk5 : 1;
    unsigned char unk6 : 1;
    unsigned char unk7 : 1;
} CountSpecialStruct;

typedef enum MoveSpecialEnum {
    MOVE_SPECIAL_DIVING,
    MOVE_SPECIAL_ORANGES,
    MOVE_SPECIAL_BARRELS,
    MOVE_SPECIAL_VINES,
    MOVE_SPECIAL_CAMERA,
    MOVE_SPECIAL_SHOCKWAVE,
} MoveSpecialEnum;

typedef struct MoveSpecialStruct {
    unsigned char diving : 1;
    unsigned char oranges : 1;
    unsigned char barrels : 1;
    unsigned char vines : 1;
    unsigned char camera : 1;
    unsigned char shockwave : 1;
    unsigned char unk6 : 1;
    unsigned char unk7 : 1;
} MoveSpecialStruct;

typedef struct CountStruct {
    /* 0x000 */ unsigned char bp_bitfield[5];
    /* 0x005 */ unsigned char hint_bitfield[5];
    /* 0x00A */ unsigned char key_bitfield;
    /* 0x00B */ unsigned char kong_bitfield;
    /* 0x00C */ unsigned char crowns;
    /* 0x00D */ CountSpecialStruct special_items;
    /* 0x00E */ unsigned char medals;
    /* 0x00F */ unsigned char pearls;
    /* 0x010 */ unsigned char fairies;
    /* 0x011 */ unsigned char rainbow_coins;
    /* 0x012 */ short ice_traps;
    /* 0x014 */ short junk_items;
    /* 0x016 */ MoveSpecialStruct flag_moves;
} CountStruct;

typedef struct MoveSpecialBijectionStruct {
    unsigned short flag;
    unsigned short move_enum;
} MoveSpecialBijectionStruct;

extern void giveItemFromKongData(model_item_data *db_item, int flag);

extern model_item_data kong_check_data[4];