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
    /* 0x016 */ short race_coins;
    /* 0x018 */ MoveSpecialStruct flag_moves;
} CountStruct;

typedef struct StartingItemsKongwiseStruct {
	/* 0x000 */ unsigned char special_moves;
	/* 0x001 */ unsigned char gun;
	/* 0x002 */ unsigned char instrument;
} StartingItemsKongwiseStruct;

typedef struct StartingItemsStruct {
	/* 0x000 */ CountStruct others; // Has an 0x1 pad afterwards
	/* 0x01A */ StartingItemsKongwiseStruct kongs[5];
	/* 0x029 */ unsigned char melons;
	/* 0x02A */ unsigned char slam;
	/* 0x02B */ unsigned char belt;
    /* 0x02C */ unsigned char climbing;
} StartingItemsStruct;

typedef struct MoveSpecialBijectionStruct {
    unsigned short flag;
    unsigned short move_enum;
} MoveSpecialBijectionStruct;

typedef struct reward_rom_struct {
	/* 0x000 */ short flag;
	/* 0x002 */ unsigned short actor;
} reward_rom_struct;

typedef struct patch_db_item {
	/* 0x000 */ short id;
	/* 0x002 */ unsigned char map;
	/* 0x003 */ unsigned char world;
} patch_db_item;

typedef struct meloncrate_db_item {
    /* 0x000 */ short id;
    /* 0x002 */ unsigned char map;
    /* 0x003 */ unsigned char world;
} meloncrate_db_item;

extern void giveItemFromKongData(model_item_data *db_item, int flag);
extern void updateBoulderId(int index, int id);
extern int getBoulderItem(void);
extern int getBoulderIndex(void);

#define BONUS_DATA_COUNT 99
extern unsigned short bp_item_table[40];
extern item_packet medal_item_table[85];
extern item_packet wrinkly_item_table[35];
extern unsigned short crown_item_table[10];
extern unsigned short key_item_table[8];
extern model_item_data fairy_item_table[20];
extern unsigned short rcoin_item_table[16];
extern unsigned short crate_item_table[16];
extern patch_db_item patch_flags[16];
extern BoulderItemStruct boulder_item_table[16];
extern bonus_barrel_info bonus_data[BONUS_DATA_COUNT];
extern meloncrate_db_item crate_flags[16];
extern model_item_data kong_check_data[4];
extern item_packet company_coin_table[2];