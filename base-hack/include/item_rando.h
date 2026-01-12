extern void giveItemFromKongData(model_item_data *db_item, int flag);
extern void updateBoulderId(int index, int id);
extern int getBoulderItem(int index);
extern int getBoulderIndex(void);

#define BONUS_DATA_COUNT 99
extern actor_spawn_packet bp_item_table[40];
extern item_packet medal_item_table[85];
extern item_packet wrinkly_item_table[35];
extern actor_spawn_packet crown_item_table[10];
extern actor_spawn_packet key_item_table[8];
extern model_item_data fairy_item_table[20];
extern actor_spawn_packet rcoin_item_table[16];
extern actor_spawn_packet crate_item_table[16];
extern actor_spawn_packet extra_actor_spawns[2];
extern patch_db_item patch_flags[16];
extern BoulderItemStruct boulder_item_table[16];
extern bonus_barrel_info bonus_data[BONUS_DATA_COUNT];
extern meloncrate_db_item crate_flags[16];
extern model_item_data kong_check_data[4];
extern item_packet company_coin_table[2];
extern snide_packet snide_rewards[40];