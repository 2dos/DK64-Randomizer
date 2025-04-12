typedef enum kongcheck_enum {
    /* 0 */ KONGCHECK_JAPES,
    /* 1 */ KONGCHECK_LLAMA,
    /* 2 */ KONGCHECK_ICETEMPLE,
    /* 3 */ KONGCHECK_FACTORY,
} kongcheck_enum;

extern void giveItemFromKongData(model_item_data *db_item, int flag);

extern model_item_data kong_check_data[4];