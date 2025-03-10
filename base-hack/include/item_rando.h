typedef struct kongcheck_db_item {
    /* 0x000 */ short flag;
    /* 0x002 */ short model;
    /* 0x004 */ unsigned char no_textures;
    /* 0x005 */ char unk5;
} kongcheck_db_item;

typedef enum kongcheck_enum {
    /* 0 */ KONGCHECK_JAPES,
    /* 1 */ KONGCHECK_LLAMA,
    /* 2 */ KONGCHECK_ICETEMPLE,
    /* 3 */ KONGCHECK_FACTORY,
} kongcheck_enum;

extern void giveItemFromKongData(kongcheck_db_item *db_item);

extern kongcheck_db_item kong_check_data[4];