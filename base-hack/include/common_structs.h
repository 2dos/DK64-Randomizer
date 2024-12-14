typedef struct floatPos {
	/* 0x000 */ float xPos;
	/* 0x004 */ float yPos;
	/* 0x008 */ float zPos;
} floatPos;

typedef struct shortPos {
	/* 0x000 */ short xPos;
	/* 0x002 */ short yPos;
	/* 0x004 */ short zPos;
} shortPos;

typedef struct subrender {
	/* 0x000 */ char unk_00[0x4];
	/* 0x004 */ float unk_04;
	/* 0x008 */ char unk_08[0x10-0x8];
	/* 0x010 */ short unk_10;
} subrender;

typedef struct renderingParamsData {
	/* 0x000 */ subrender* sub;
	/* 0x004 */ char unk_04[0x34-0x4];
	/* 0x034 */ float scale_x;
	/* 0x038 */ float scale_y;
	/* 0x03C */ float scale_z;
	/* 0x040 */ char unk_40[0x64-0x40];
	/* 0x064 */ short animation;
} renderingParamsData;

typedef struct actor_subdata {
	/* 0x000 */ int data[4];
} actor_subdata;

typedef struct bone_array {
	/* 0x000 */ char unk_00[0x18];
	/* 0x018 */ short xPos;
	/* 0x01A */ short yPos;
	/* 0x01C */ short zPos;
	/* 0x01E */ char unk_20[0x30-0x1E];
	/* 0x030 */ float fpos_x;
	/* 0x034 */ float fpos_y;
	/* 0x038 */ float fpos_z;
	/* 0x03C */ char unk_3C[0x4];
} bone_array;

typedef struct bonepos {
	/* 0x000 */ int unk_0;
	/* 0x004 */ int unk_4;
	/* 0x008 */ int unk_8;
	/* 0x00C */ int boneX;
	/* 0x010 */ int boneY;
	/* 0x014 */ int boneZ;
	/* 0x018 */ int id;
	/* 0x01C */ void* next_bone;
} bonepos;

typedef struct bone_block_data {
	/* 0x000 */ int unk0;
	/* 0x004 */ bone_array* bone_arrays[2];
	/* 0x00C */ char unk_C[0x14-0xC];
	/* 0x014 */ int timer;
	/* 0x018 */ int timer_0;
	/* 0x01C */ char unk_1C[0x20-0x1C];
	/* 0x020 */ bonepos* bone_positions;
	/* 0x024 */ char unk_24[0x30-0x24];
	/* 0x030 */ float ox;
	/* 0x034 */ float oy;
	/* 0x038 */ float oz;
	/* 0x03C */ char unk_3C[0x40-0x3C];
} bone_block_data;

typedef struct bonedata {
	/* 0x000 */ int unk_0;
	/* 0x004 */ int unk_4;
	/* 0x008 */ int unk_8;
	/* 0x00C */ char unk_0C[0x70 - 0x0C];
	/* 0x070 */ bone_block_data bone_block;
} bonedata;
typedef struct actorData {
	/* 0x000 */ void* model;
	/* 0x004 */ renderingParamsData* render;
	/* 0x008 */ void* current_bone_array;
	/* 0x00C */ float unk_0C;
	/* 0x010 */ char unk_10[0x4C-0x10];
	/* 0x04C */ void* model_file;
	/* 0x050 */ char unk_50[0x58-0x50];
	/* 0x058 */ int actorType;
	/* 0x05C */ unsigned short interaction_bitfield;
	/* 0x05E */ char unk_5E[0x60-0x5E];
	/* 0x060 */ int obj_props_bitfield;
	/* 0x064 */ int unk_64;
	/* 0x068 */ char unk_68[0x6A-0x68];
	/* 0x06A */ short grounded;
	/* 0x06C */ short unk_6C;
	/* 0x06E */ short sound_slot;
	/* 0x070 */ char unk_70[0x7C-0x70];
	/* 0x07C */ float xPos;
	/* 0x080 */ float yPos;
	/* 0x084 */ float zPos;
	/* 0x088 */ char unk_80[0xB8-0x88];
	/* 0x0B8 */ float hSpeed;
	/* 0x0BC */ char unk_BC[0xC0-0xBC];
	/* 0x0C0 */ float yVelocity;
	/* 0x0C4 */ float yAccel;
	/* 0x0C8 */ char unk_C8[0xCC-0xC8];
	/* 0x0CC */ char unk_CC;
	/* 0x0CD */ char unk_CD[0xE4-0xCD];
	/* 0x0E4 */ short rot_x;
	/* 0x0E6 */ short rot_y;
	/* 0x0E8 */ short rot_z;
	/* 0x0EA */ short unk_EA;
	/* 0x0EC */ short unk_EC;
	/* 0x0EE */ short rot_y_copy;
	/* 0x0F0 */ short reward_index;
	/* 0x0F2 */ char unk_F2[0xFD-0xF2];
	/* 0x0FD */ unsigned char unk_FD;
	/* 0x0FE */ char unk_FE[0x11C-0xFE];
	/* 0x11C */ void* parent;
	/* 0x120 */ char unk_120[0x124-0x120];
	/* 0x124 */ actor_subdata* data_pointer;
	/* 0x128 */ short shadow_intensity;
	/* 0x12A */ short draw_distance;
	/* 0x12C */ short chunk;
	/* 0x12E */ char unk_12E[0x132-0x12E];
	/* 0x132 */ short subdata;
	/* 0x134 */ short health;
	/* 0x136 */ char unk_136[0x138-0x136];
	/* 0x138 */ int takes_enemy_damage;
	/* 0x13C */ char unk_13C[0x140-0x13C];
	/* 0x140 */ bonedata* bone_data;
	/* 0x144 */ char noclip_byte;
	/* 0x145 */ char unk_145[0x154-0x145];
	/* 0x154 */ unsigned char control_state;
	/* 0x155 */ char control_state_progress;
	/* 0x156 */ char unk_156[0x15E - 0x156];
	/* 0x15E */ unsigned char height_offset;
	/* 0x15F */ char sub_state;
	/* 0x160 */ char unk_160[0x16A-0x160];
	/* 0x16A */ char rgb_mask[3];
	/* 0x16D */ char unk_16D;
	/* 0x16E */ char unk_16E;
	/* 0x16F */ char unk_16F;
	/* 0x170 */ char unk_170[0x172-0x170];
	/* 0x172 */ short actor_model; // Custom slot. unused I think?? 
	/* 0x174 */ void* paad;
	/* 0x178 */ void* paad2;
	/* 0x17C */ void* paad3;
	/* 0x180 */ void* tied_character_spawner;
} actorData;

typedef struct cameraData {
	/* 0x000 */ char unk_00[0x7C];
	/* 0x07C */ float xPos;
	/* 0x080 */ float yPos;
	/* 0x084 */ float zPos;
	/* 0x088 */ char unk_88[0x12C-0x88];
	/* 0x12C */ short chunk;
	/* 0x12E */ char unk_12E[0x15F-0x12E];
	/* 0x15F */ char facing_angle;
	/* 0x160 */ char unk_160[0x1FC-0x160];
	/* 0x1FC */ float viewportX;
	/* 0x200 */ float viewportY;
	/* 0x204 */ float viewportZ;
	/* 0x208 */ char unk_208[0x22A-0x208];
	/* 0x22A */ short viewportRotation;
	/* 0x22C */ char unk_22C[0x230-0x22C];
	/* 0x230 */ float viewportXRotation;
	/* 0x234 */ char unk_234[0x26B-0x234];
	/* 0x26B */ char camera_state;
} cameraData;

typedef struct tagBarrel {
	/* 0x000 */ char unk_00[0x1A0];
	/* 0x1A0 */ short tag_oscillation_timer;
} tagBarrel;

typedef struct timerActor {
	/* 0x000 */ char unk_00[0x15F];
	/* 0x15F */ char type;
	/* 0x160 */ char unk_160[0x184-0x160];
	/* 0x184 */ int test;
} timerActor;

typedef struct rendering_params {
	/* 0x000 */ char unk_00[0x14];
	/* 0x014 */ bone_array* bone_arrays[2];
	/* 0x01C */ char unk_1C[0x64-0x1C];
	/* 0x064 */ short anim_idx;
	/* 0x066 */ char unk_66[0x68-0x66];
	/* 0x068 */ int anim_ptr;
} rendering_params;

typedef struct playerData {
	/* 0x000 */ char unk_00[0x4];
	/* 0x004 */ rendering_params* rendering_param_pointer;
	/* 0x008 */ char unk_08[0x58 - 0x8];
	/* 0x058 */ int characterID; //02 is dk, 03 is diddy, 04 is lanky, etc
	/* 0x05C */ char unk_5C[0x60-0x5C];
	/* 0x060 */ int obj_props_bitfield;
	/* 0x064 */ char unk_64[0x6A-0x64];
	/* 0x06A */ short grounded_bitfield;
	/* 0x06C */ short unk_bitfield;
	/* 0x06E */ char unk_6E[0x78-0x6E];
	/* 0x078 */ unsigned char sfx_floor;
	/* 0x079 */ char unk_79[0x7C-0x79];
	/* 0x07C */ float xPos;
	/* 0x080 */ float yPos;
	/* 0x084 */ float zPos;
	/* 0x088 */ char unk_88[0xA4-0x88];
	/* 0x0A4 */ float floor;
	/* 0x0A8 */ char unk_A8[0xAC-0xA8];
	/* 0x0AC */ float water_floor;
	/* 0x0B0 */ char unk_B0[0xB8-0xB0];
	/* 0x0B8 */ float hSpeed;
	/* 0x0BC */ char unk_BC[0x4];
	/* 0x0C0 */ float yVelocity;
	/* 0x0C4 */ float yAccel;
	/* 0x0C8 */ char unk_C4[0xE6 - 0xC8];
	/* 0x0E6 */ short facing_angle;
	/* 0x0E8 */ short skew_angle;
	/* 0x0EA */ char unk_EA[0xEE - 0xEA];
	/* 0x0EE */ short next_facing_angle;
	/* 0x0F0 */ char unk_F0[0x10C - 0xF0];
	/* 0x10C */ short standing_on_index;
	/* 0x10E */ unsigned char standing_on_subposition;
	/* 0x10F */ unsigned char standing_on_subposition_0;
	/* 0x110 */ char touching_object;
	/* 0x111 */ char unk_111[0x128 - 0x111];
	/* 0x128 */ short strong_kong_value;
	/* 0x12A */ char unk_12A[2];
	/* 0x12C */ short chunk;
	/* 0x12E */ char unk_12E[0x132 - 0x12E];
	/* 0x132 */ short unk_132;
	/* 0x134 */ char unk_134[0x13C - 0x134];
	/* 0x13C */ int* collision_queue_pointer;
	/* 0x140 */ bonedata* bone_data;
	/* 0x144 */ char noclip;
	/* 0x145 */ char unk_145[0x147 - 0x145];
	/* 0x147 */ char hand_state;
	/* 0x148 */ char unk_148[0x154 - 0x148];
	/* 0x154 */ unsigned char control_state;
	/* 0x155 */ char control_state_progress;
	/* 0x156 */ char unk_156[0x15E - 0x156];
	/* 0x15E */ unsigned char height;
	/* 0x15F */ char unk_15F[0x168 - 0x15F];
	/* 0x168 */ short updraft_target;
	/* 0x16A */ unsigned char rgb_components[3];
	/* 0x16D */ char unk_16D;
	/* 0x16E */ char unk_16E; // shadow width or something
	/* 0x16F */ char unk_16F[0x18A-0x16F];
	/* 0x18A */ short moving_angle;
	/* 0x18C */ char unk_18C[0x1A6-0x18C];
	/* 0x1A6 */ short traction;
	/* 0x1A8 */ char unk_1A8[0x1B0-0x1A8];
	/* 0x1B0 */ float unk_1B0;
	/* 0x1B4 */ char unk_1B4[0x1B8-0x1B4];
	/* 0x1B8 */ float velocity_cap;
	/* 0x1BC */ char unk_1BC[0x1C8-0x1BC];
	/* 0x1C8 */ short turn_speed;
	/* 0x1CA */ char unk_1CA[0x1CC-0x1CA];
	/* 0x1CC */ short old_tag_state;
	/* 0x1CE */ char unk_1CE[0x1D0-0x1CE];
	/* 0x1D0 */ short ostand_value;
	/* 0x1D2 */ char unk_1D2[0x1D4-0x1D2];
	/* 0x1D4 */ float blast_y_velocity;
	/* 0x1D8 */ int unk_1D8;
	/* 0x1DC */ char unk_1DC[0x1E8-0x1DC];
	/* 0x1E8 */ float unk_1E8;
	/* 0x1EC */ char unk_1EC[0x208-0x1EC];
	/* 0x208 */ void* vehicle_actor_pointer;
	/* 0x20C */ char was_gun_out;
	/* 0x20D */ char unk_20D[0x210 - 0x20D];
	/* 0x210 */ unsigned char gun_bone;
	/* 0x211 */ char unk_211[0x23C - 0x211];
	/* 0x23C */ short unk_rocketbarrel_value1;
	/* 0x23E */ short unk_rocketbarrel_value2;
	/* 0x240 */ short balloon_timer;
	/* 0x242 */ char unk_242[0x248 - 0x242];
	/* 0x248 */ short shockwave_timer;
	/* 0x24A */ char unk_24A[0x254 - 0x24A];
	/* 0x254 */ short invulnerability_timer;
	/* 0x256 */ char unk_256[0x284 - 0x256];
	/* 0x284 */ cameraData* camera_pointer;
	/* 0x288 */ float unk_288;
	/* 0x28C */ char unk_28C[0x2BC - 0x28C];
	/* 0x2BC */ floatPos grabPos;
	/* 0x2C8 */ char unk_2C8[0x323 - 0x2C8];
	/* 0x323 */ char unk_rocketbarrel_value3;
	/* 0x324 */ unsigned char player_index;
	/* 0x325 */ char unk_324[0x328 - 0x325];
	/* 0x328 */ actorData* krool_timer_pointer;
	/* 0x32C */ actorData* held_actor;
	/* 0x330 */ char unk_330[0x340 - 0x330];
	/* 0x340 */ float scale[6];
	/* 0x358 */ char unk_358[0x368 - 0x358];
	/* 0x368 */ unsigned int state_bitfield;
	/* 0x36C */ char fairy_state;
	/* 0x36D */ char unk_36D[0x36F - 0x36D];
	/* 0x36F */ char new_kong;
	/* 0x370 */ int strong_kong_ostand_bitfield;
	/* 0x374 */ int unk_fairycam_bitfield;
	/* 0x378 */ char unk_374[0x37D-0x378];
	/* 0x37D */ unsigned char rambi_enabled;
	/* 0x37E */ char unk_37E[0x380 - 0x37E];
	/* 0x380 */ short trap_bubble_timer;
	/* 0x382 */ char unk_382[0x3AC - 0x382];
	/* 0x3AC */ float grab_x;
	/* 0x3B0 */ float grab_y;
	/* 0x3B4 */ float grab_z;
	/* 0x3B8 */ char unk_3B8[0x3BC - 0x3A8];
	/* 0x3BC */ unsigned short try_again_timer;
	/* 0x3BE */ unsigned char detransform_timer;
} playerData; //size 0x630

typedef struct TextOverlay {
	/* 0x000 */ char unk_00[0x7C];
	/* 0x004 */ //u16
	/* 0x006 */ //u16
	/* 0x008 */ //u8
	/* 0x009 */ //u8
	/* 0x054 */ //layer ID?
	/* 0x07C */ float xPos;
	/* 0x080 */ float yPos;
	/* 0x084 */ float style;
	/* 0x088 */ char unk_88[0x15F-0x88];
	/* 0x15F */ char opacity;
	/* 0x160 */ char unk_160[0x0A];
	/* 0x16A */ unsigned char red;
	/* 0x16B */ unsigned char green;
	/* 0x16C */ unsigned char blue;
	/* 0x16D */ char unk_16D[0x0B];
	/* 0x178 */ char* string;
} TextOverlay;

typedef struct InventoryBase {
	/* 0x000 */ short StandardAmmo;
	/* 0x002 */ short HomingAmmo;
	/* 0x004 */ short Oranges;
	/* 0x006 */ short Crystals;
	/* 0x008 */ short Film;
	/* 0x00A */ char unk0A;
	/* 0x00B */ char Health;
	/* 0x00C */ char Melons;
	/* 0x00D */ char StoredDamage;
	/* 0x00E */ short InstrumentEnergy;
} InventoryBase;

typedef struct AutowalkData {
	/* 0x000 */ char unk_00[0x12];
	/* 0x012 */ short xPos;
	/* 0x014 */ char unk_14[0x2];
	/* 0x016 */ short zPos;
} AutowalkData;

typedef struct KongBase {
	/* 0x000 */ char special_moves;
	/* 0x001 */ char simian_slam;
	/* 0x002 */ char weapon_bitfield;
	/* 0x003 */ char ammo_belt;
	/* 0x004 */ char instrument_bitfield;
	/* 0x005 */ char unk_05[0x2];
	/* 0x007 */ unsigned char coins;
	/* 0x008 */ short instrument_energy;
	/* 0x00A */ short cb_count[0xE];
	/* 0x026 */ short tns_cb_count[0xE];
	/* 0x042 */ short gb_count[0xE];
} KongBase;

typedef struct ISGFadeoutData {
	/* 0x000 */ int FadeoutTime;
	/* 0x004 */ char FadeoutMap;
	/* 0x005 */ char unk_05[0x3];
} ISGFadeoutData;

typedef struct SwapObjectData {
	/* 0x000 */ char unk_00[0x4];
	/* 0x004 */ playerData* player;
	/* 0x008 */ char unk_08[0x210-0x8];
	/* 0x210 */ floatPos cameraPositions[4];
	/* 0x240 */ char unk_21C[0x284-0x240];
	/* 0x284 */ float near;
	/* 0x288 */ char unk_288[0x290-0x288];
	/* 0x290 */ short chunk;
	/* 0x292 */ char unk_292[0x29C-0x292];
	/* 0x29C */ short action_type;
	/* 0x29E */ char unk_29E[0x2C0 - 0x29E];
	/* 0x2C0 */ char size;
	/* 0x2C1 */ char unk_2C1[0x2E2 - 0x2C1];
	/* 0x2E2 */ unsigned short unk_2e2;
} SwapObjectData;

typedef struct ModelTwoData {
	/* 0x000 */ float xPos;
	/* 0x004 */ float yPos;
	/* 0x008 */ float zPos;
	/* 0x00C */ float scale;
	/* 0x010 */ char unk_10[0x20-0x10];
	/* 0x020 */ void* model_pointer;
	/* 0x024 */ void* dl_pointer;
	/* 0x028 */ char unk_28[0x7C-0x28];
	/* 0x07C */ void* behaviour_pointer;
	/* 0x080 */ char unk_80[0x84-0x80];
	/* 0x084 */ short object_type;
	/* 0x086 */ char unk_86[0x2];
	/* 0x088 */ short sub_id;
	/* 0x08A */ short object_id;
	/* 0x08C */ unsigned char collectable_state;
	/* 0x08D */ char unk_8D[0x3];
} ModelTwoData;

typedef struct WarpInfo {
	/* 0x000 */ short xPos;
	/* 0x002 */ short yPos;
	/* 0x004 */ short zPos;
	/* 0x006 */ unsigned char facing_angle; // (val / 255) * 4096
	/* 0x007 */ unsigned char camera_angle; // (player + 0x284)->0x15F
	/* 0x008 */ char will_autowalk;
	/* 0x009 */ char spawn_at_origin;
} WarpInfo;

typedef struct cutsceneInfo {
	/* 0x000 */ char csdata[0xC];
} cutsceneInfo;

typedef struct cutscene_item {
	/* 0x000 */ char unk0;
	/* 0x001 */ unsigned char command;
	/* 0x002 */ char unk2[4];
	/* 0x006 */ short params[3];
	/* 0x00C */ char unkC[0x14-0xC];
} cutscene_item;

typedef struct pan_data {
	/* 0x000 */ short x;
	/* 0x002 */ short y;
	/* 0x004 */ short z;
	/* 0x006 */ short rot_data[3];
	/* 0x00C */ unsigned char zoom;
	/* 0x00D */ unsigned char roll;
} pan_data;

typedef struct cutscene_pan_item {
	/* 0x000 */ char unk0;
	/* 0x001 */ unsigned char command;
	/* 0x002 */ char unk2[2];
	/* 0x004 */ short point_count;
	/* 0x006 */ char unk6[2];
	/* 0x008 */ pan_data* pan_content;
	/* 0x00C */ char unkC[0x14-0xC];
} cutscene_pan_item;

typedef struct cutscene_item_data {
	/* 0x000 */ short num_points;
	/* 0x002 */ short unk_02;
	/* 0x004 */ short* point_array;
	/* 0x008 */ short* length_array;
} cutscene_item_data;

typedef struct queued_cutscene_function {
	/* 0x000 */ void* next;
	/* 0x004 */ void* function;
	/* 0x008 */ int action_timer; // Has 0x8000 0000 or'd onto it for some? reason. Timer is set based on 8076a068
	/* 0x00C */ int unk_C;
	/* 0x010 */ int unk_10;
	/* 0x014 */ int unk_14;
} queued_cutscene_function;

typedef struct cutsceneType {
	/* 0x000 */ char unk_00[0xCC];
	/* 0x0CC */ short cutscene_count;
	/* 0x0CE */ char unk_CE[0xD0-0xCE];
	/* 0x0D0 */ cutscene_item_data* cutscene_databank;
	/* 0x0D4 */ char unk_D4[0xD8-0xD4];
	/* 0x0D8 */ cutscene_item* cutscene_funcbank;
	/* 0x0DC */ int unk_DE;
} cutsceneType;

typedef struct submapInfo {
	/* 0x000 */ char slot_populated;
	/* 0x001 */ char unk_01;
	/* 0x002 */ short transition_properties_bitfield;
	/* 0x004 */ float x;
	/* 0x008 */ float y;
	/* 0x00C */ float z;
	/* 0x010 */ short angle;
	/* 0x012 */ short parent_map;
	/* 0x014 */ char parent_exit;
	/* 0x015 */ char unk_15[0x18-0x15];
	/* 0x018 */ void* setup;
	/* 0x01C */ int uses_extra_setup;
	/* 0x020 */ void* setup2;
	/* 0x024 */ char unk_24[0xC0-0x24];
} submapInfo;

typedef struct SpawnerInfo {
	/* 0x000 */ unsigned char enemy_value;
	/* 0x001 */ char unk_01;
	/* 0x002 */ short yRot;
	/* 0x004 */ short xPos;
	/* 0x006 */ short yPos;
	/* 0x008 */ short zPos;
	/* 0x00A */ char cs_model;
	/* 0x00B */ char unk_0B;
	/* 0x00C */ unsigned char max_idle_speed;
	/* 0x00D */ unsigned char max_aggro_speed;
	/* 0x00E */ char unk_0E;
	/* 0x00F */ char scale;
	/* 0x010 */ char aggro_index;
	/* 0x011 */ char unk_11;
	/* 0x012 */ char init_spawn_state;
	/* 0x013 */ char spawn_trigger;
	/* 0x014 */ char respawnTimerInit;
	/* 0x015 */ char unk_15[0x18-0x15];
	/* 0x018 */ void* tied_actor;
	/* 0x01C */ void* movement_box;
	/* 0x020 */ void* unk_20;
	/* 0x024 */ short respawn_timer;
	/* 0x026 */ char unk_26[0x3C-0x26];
	/* 0x03C */ float unk_3C;
	/* 0x040 */ short chunk;
	/* 0x042 */ char spawn_state;
	/* 0x043 */ char counter;
	/* 0x044 */ unsigned char alt_enemy_value;
	/* 0x045 */ char unk_45;
	/* 0x046 */ short unk_46;
} SpawnerInfo;

typedef struct SpawnerArray {
	/* 0x000 */ SpawnerInfo SpawnerData[120];
} SpawnerArray;

typedef struct SpawnerMasterInfo {
	/* 0x000 */ short count;
	/* 0x002 */ char unk_02[2];
	/* 0x004 */ SpawnerArray* array;
} SpawnerMasterInfo;

typedef struct loadedActorArr {
	/* 0x000 */ actorData* actor;
	/* 0x004 */ int unk_04;
} loadedActorArr;

typedef struct actorNames {
	/* 0x000 */ char actor_name[344][0x10];
} actorNames;

typedef struct actorSpawnerData {
	/* 0x000 */ unsigned short actor_type; // Offset by 0x10
	/* 0x002 */ char unk_02[2];
	/* 0x004 */ floatPos positions;
	/* 0x010 */ char unk_10[0x24-0x10];
	/* 0x024 */ int can_hide_vine;
	/* 0x028 */ char unk_28[0x2C-0x28];
	/* 0x02C */ float flag; // What?????
	/* 0x030 */ char unk_30[0x40-0x30];
	/* 0x040 */ float barrel_resolved;
	/* 0x044 */ void* tied_actor;
	/* 0x048 */ char unk_48[0x54-0x48];
	/* 0x054 */ float spawn_range;
	/* 0x058 */ short model;
	/* 0x05A */ short id;
	/* 0x05C */ char unk_5C[0x64-0x5C];
	/* 0x064 */ void* previous_spawner;
	/* 0x068 */ void* next_spawner;
} actorSpawnerData;

typedef struct spawnerPacket {
	/* 0x000 */ int model;
	/* 0x004 */ char unk_4[0x18-4];
	/* 0x018 */ void* extra_data;
} spawnerPacket;

typedef struct heap {
	/* 0x000 */ void* unk;
	/* 0x004 */ int size;
	/* 0x008 */ void* next;
	/* 0x00C */ void* prev;
} heap;

typedef struct fairyInfo {
	/* 0x000 */ short max_dist_allowed;
	/* 0x002 */ short xPos;
	/* 0x004 */ short yPos;
} fairyInfo;

typedef struct charSpawnerData {
	/* 0x000 */ short actor_type;
	/* 0x002 */ short actor_behaviour;
	/* 0x004 */ char unk_04[0x18-0x4];
} charSpawnerData;

typedef struct uniqueSpawnFunction {
	/* 0x000 */ int actor_type;
	/* 0x004 */ int func;
} uniqueSpawnFunction;

typedef struct actorWrapperParams {
	/* 0x000 */ short actor_type;
	/* 0x002 */ short actor_behaviour;	
} actorWrapperParams;

typedef struct forceSpawnActorData {
	/* 0x000 */ short actor_type;
} forceSpawnActorData;

typedef struct arcadeObject {
	/* 0x000 */ float x;
	/* 0x004 */ float y;
	/* 0x008 */ float x_velocity;
	/* 0x00C */ float y_velocity;
	/* 0x010 */ char unk_10[0x14-0x10];
	/* 0x014 */ void* image_data_pointer;
	/* 0x018 */ char type;
	/* 0x019 */ char movement;
	/* 0x01A */ char unk_1A[0x20-0x1A];
} arcadeObject;

typedef struct arcadeObjectBase {
	/* 0x000 */ arcadeObject object[0x50];
} arcadeObjectBase;

typedef struct arcadeMoveFloor {
	/* 0x000 */ float x;
	/* 0x004 */ float y;
	/* 0x008 */ float y_velocity;
} arcadeMoveFloor;

typedef struct arcadeMoveFloorBase {
	/* 0x000 */ arcadeMoveFloor floor[6];
} arcadeMoveFloorBase;

typedef struct parentMaps {
	/* 0x000 */ char in_submap;
	/* 0x001 */ char unk_01;
	/* 0x002 */ unsigned short transition_properties_bitfield;
	/* 0x004 */ floatPos positions;
	/* 0x010 */ short facing_angle;
	/* 0x012 */ short map;
	/* 0x014 */ unsigned char exit;
	/* 0x015 */ char unk_15[0x18-0x15];
	/* 0x018 */ void* setup_pointer;
	/* 0x01C */ int behaviour_load;
	/* 0x020 */ char unk_1C[0xC0-0x20];
} parentMaps;

typedef struct placementData {
	/* 0x000 */ char unk_00[0x4];
	/* 0x004 */ float x_direction;
	/* 0x008 */ float y_direction;
	/* 0x00C */ int unk_0C;
	/* 0x010 */ short popout_timer;
	/* 0x012 */ char unk_12[0x20-0x12];
} placementData;

typedef struct hud_element {
	/* 0x000 */ short* item_count_pointer;
	/* 0x004 */ short visual_item_count;
	/* 0x006 */ short hud_state_timer;
	/* 0x008 */ int x;
	/* 0x00C */ int y;
	/* 0x010 */ float unk_10[4];
	/* 0x020 */ int hud_state;
	/* 0x024 */ int unk_24;
	/* 0x028 */ placementData* placement_pointer;
	/* 0x02C */ char infinite_setting;
	/* 0x02D */ char unk_2D;
	/* 0x02E */ char unk_2E[0x30-0x2E];
} hud_element;

typedef struct hudData {
	/* 0x000 */ hud_element item[0xE];
} hudData;

typedef struct text_struct {
	/* 0x000 */ unsigned char width;
	/* 0x001 */ unsigned char file_count;
	/* 0x002 */ unsigned char height;
	/* 0x003 */ char kerning_space;
	/* 0x004 */ char kerning_char;
	/* 0x005 */ char kerning_anim;
} text_struct;

typedef struct trigger {
	/* 0x000 */ short x;
	/* 0x002 */ short y;
	/* 0x004 */ short z;
	/* 0x006 */ short radius;
	/* 0x008 */ short height;
	/* 0x00A */ short unk_0A;
	/* 0x00C */ char activation_type;
	/* 0x00D */ char unk_0D[0x10-0xD];
	/* 0x010 */ short type;
	/* 0x012 */ short map;
	/* 0x014 */ short exit;
	/* 0x016 */ short transition;
	/* 0x018 */ char unk_18[0x1A-0x18];
	/* 0x01A */ short cutscene_is_tied;
	/* 0x01C */ short cutscene_activated;
	/* 0x01E */ short shift_cam_to_kong;
	/* 0x020 */ char unk_20[0x38-0x20];
	/* 0x038 */ char not_in_zone;
	/* 0x039 */ char active;
} trigger;

typedef struct cannon {
	/* 0x000 */ char unk_00[0x376];
	/* 0x376 */ short source_map;
	/* 0x378 */ short destination_map;
	/* 0x37A */ short destination_exit;
} cannon;



typedef struct blocker_cheat {
	/* 0x000 */ unsigned char gb_count;
	/* 0x001 */ char kong_index;
} blocker_cheat;

typedef struct main_menu_moves_struct {
	/* 0x000 */ short map;
	/* 0x002 */ short kong;
	/* 0x004 */ char moves;
	/* 0x005 */ char slam_level;
	/* 0x006 */ char instrument;
	/* 0x007 */ char melons;
} main_menu_moves_struct;

typedef struct purchase_struct {
	/* 0x000 */ short purchase_type; // 0 = Moves, 1 = Simian Slam, 2 = Weapon Bitfield, 3 = Ammo Belt, 4 = Instrument Bitfield, -1 = No offer
	/* 0x002 */ short purchase_value;
	/* 0x004 */ unsigned char move_kong; // Kong that the move is normally assigned to. Eg Strong Kong = DK (0), Monkeyport = Tiny (3)
	/* 0x005 */ unsigned char price;
} purchase_struct;

typedef struct race_exit_struct {
	/* 0x000 */ int race_map;
	/* 0x004 */ int container_map;
	/* 0x008 */ int container_exit;
} race_exit_struct;

typedef struct exit_struct {
	/* 0x000 */ short x;
	/* 0x002 */ short y;
	/* 0x004 */ short z;
	/* 0x006 */ char unk_6[4];
} exit_struct;

typedef struct enemy_drop_struct {
	/* 0x000 */ short source_object_type;
	/* 0x002 */ short dropped_object_type;
	/* 0x004 */ unsigned char drop_music;
	/* 0x005 */ unsigned char drop_count;
} enemy_drop_struct;

typedef struct fileExtraStorage {
	/* 0x000 */ unsigned char location_sss_purchased; // 0lll 0pss. l = level (0-7), p = purchased (0-1), s = shop (0-2. Cranky, Funky, Candy)
	/* 0x001 */ unsigned char location_ab1_purchased;
	/* 0x002 */ unsigned char location_ug1_purchased;
	/* 0x003 */ unsigned char location_mln_purchased;
	/* 0x004 */ unsigned int level_igt[9];
} fileExtraStorage;

typedef struct settingsData {
	/* 0x000 */ fileExtraStorage file_extra;
} settingsData;

typedef struct behaviour_data {
	/* 0x000 */ void* extra_data;
	/* 0x004 */ char unk_04[0x10-0x4];
	/* 0x010 */ short unk_10;
	/* 0x012 */ char unk_12[0x14-0x12];
	/* 0x014 */ float unk_14;
	/* 0x018 */ char unk_18[0x38-0x18];
	/* 0x038 */ int unk_38;
	/* 0x03C */ char unk_3C[0x44-0x3C];
	/* 0x044 */ unsigned short timer;
	/* 0x046 */ unsigned short unk_46;
	/* 0x048 */ unsigned char current_state;
	/* 0x049 */ char counter;
	/* 0x04A */ char unk_4A;
	/* 0x04B */ unsigned char next_state;
	/* 0x04C */ char counter_next;
	/* 0x04D */ char unk_4D[0x54-0x4D];
	/* 0x054 */ char pause_state;
	/* 0x055 */ char unk_55[0x58-0x55];
	/* 0x058 */ int distance_cap;
	/* 0x05C */ char switch_pressed;
	/* 0x05D */ char unk_5D;
	/* 0x05E */ unsigned short contact_actor_type;
	/* 0x060 */ char unk_60;
	/* 0x061 */ char unk_61;
	/* 0x062 */ unsigned short unk_62;
	/* 0x064 */ short unk_64;
	/* 0x066 */ unsigned char unk_66;
	/* 0x067 */ char unk_67;
	/* 0x068 */ unsigned short unk_68;
	/* 0x06A */ unsigned short unk_6A;
	/* 0x06C */ unsigned short unk_6C;
	/* 0x06E */ char unk_6E;
	/* 0x06F */ char unk_6F;
	/* 0x070 */ char unk_70;
	/* 0x071 */ char unk_71;
	/* 0x072 */ char unk_72[0x94-0x72];
	/* 0x094 */ void* cutscene_controller_pointer;
	/* 0x098 */ char unk_98[0x9B-0x98];
	/* 0x09B */ unsigned char persistance;
	/* 0x09C */ char unk_9C[0xA0-0x9C];
} behaviour_data;

typedef struct model_struct {
	/* 0x000 */ float x;
	/* 0x004 */ float y;
	/* 0x008 */ float z;
	/* 0x00C */ float scale;
	/* 0x010 */ float rot_x;
	/* 0x014 */ float rot_y;
	/* 0x018 */ float rot_z;
	/* 0x01C */ char unk_1C[0x50-0x1C];
	/* 0x050 */ int unk_50;
	/* 0x054 */ char unk_54[0xB8-0x54];
	/* 0X0B8 */ int unk_B8;
} model_struct;

typedef struct charspawner_flagstruct {
	/* 0x000 */ unsigned char map;
	/* 0x001 */ char unk_01;
	/* 0x002 */ short spawner_id;
	/* 0x004 */ short tied_flag;
	/* 0x006 */ char unk_06[2];
} charspawner_flagstruct;

typedef struct GBDictItem {
	/* 0x000 */ unsigned char map;
	/* 0x001 */ char unk_01;
	/* 0x002 */ short model2_id;
	/* 0x004 */ short flag_index;
	/* 0x006 */ char intended_kong_actor;
	/* 0x007 */ char unk_07;
} GBDictItem;

typedef struct shop_paad {
	/* 0x000 */ char unk_00[2];
	/* 0x002 */ short flag;
	/* 0x004 */ unsigned char kong;
	/* 0x005 */ unsigned char price;
	/* 0x006 */ char unk_06[0xB-0x6];
	/* 0x00B */ char purchase_type;
	/* 0x00C */ char level;
	/* 0x00D */ unsigned char state;
	/* 0x00E */ unsigned char unk_0E;
	/* 0x00F */ char unk_0F;
	/* 0x010 */ unsigned char melons;
	/* 0x011 */ unsigned char purchase_value;
} shop_paad;

typedef struct model2_collision_info {
	/* 0x000 */ unsigned short type;
	/* 0x002 */ char collectable_type;
	/* 0x003 */ unsigned char unk3;
	/* 0x004 */ float unk4;
	/* 0x008 */ float unk8;
	/* 0x00C */ short intended_kong;
	/* 0x00E */ short actor_equivalent;
	/* 0x010 */ short unk10;
	/* 0x012 */ short unk12;
} model2_collision_info;

typedef struct move_rom_item {
	/* 0x000 */ unsigned char move_master_data; // tttl lkkk. t = Type (0 = Moves, 1 = Slam, 2 = Guns, 3 = Ammo Belt, 4 = Instrument, 5 = Flag, 6 = GB, 7 = Vacant), l = move level (reduced by 1), k = kong
	/* 0x001 */ unsigned char price;
	/* 0x002 */ short flag; // -1 = No Flag, -2 = Both Camera & Shockwave (Reserved)
} move_rom_item;
typedef struct move_block {
	/* 0x000 */ move_rom_item cranky_moves[5][8];
	/* 0x0A0 */ move_rom_item funky_moves[5][8];
	/* 0x140 */ move_rom_item candy_moves[5][8];
	/* 0x1E0 */ move_rom_item training_moves[4];
	/* 0x1F0 */ move_rom_item bfi_move;
	/* 0x1F4 */ move_rom_item first_move;
} move_block;



typedef struct map_bitfield {
	unsigned char test_map : 1;
	unsigned char funkys_store : 1;
	unsigned char dk_arcade : 1;
	unsigned char k_rool_barrel_lankys_maze : 1;
	unsigned char jungle_japes_mountain : 1;
	unsigned char crankys_lab : 1;
	unsigned char jungle_japes_minecart : 1;
	unsigned char jungle_japes : 1;
	unsigned char jungle_japes_army_dillo : 1;
	unsigned char jetpac : 1;
	unsigned char kremling_kosh_very_easy : 1;
	unsigned char stealthy_snoop_normal_no_logo : 1;
	unsigned char jungle_japes_shell : 1;
	unsigned char jungle_japes_lankys_cave : 1;
	unsigned char angry_aztec_beetle_race : 1;
	unsigned char snides_hq : 1;
	unsigned char angry_aztec_tinys_temple : 1;
	unsigned char hideout_helm : 1;
	unsigned char teetering_turtle_trouble_very_easy : 1;
	unsigned char angry_aztec_five_door_temple_dk : 1;
	unsigned char angry_aztec_llama_temple : 1;
	unsigned char angry_aztec_five_door_temple_diddy : 1;
	unsigned char angry_aztec_five_door_temple_tiny : 1;
	unsigned char angry_aztec_five_door_temple_lanky : 1;
	unsigned char angry_aztec_five_door_temple_chunky : 1;
	unsigned char candys_music_shop : 1;
	unsigned char frantic_factory : 1;
	unsigned char frantic_factory_car_race : 1;
	unsigned char hideout_helm_level_intros_game_over : 1;
	unsigned char frantic_factory_power_shed : 1;
	unsigned char gloomy_galleon : 1;
	unsigned char gloomy_galleon_k_rools_ship : 1;
	unsigned char batty_barrel_bandit_very_easy : 1;
	unsigned char jungle_japes_chunkys_cave : 1;
	unsigned char dk_isles_overworld : 1;
	unsigned char k_rool_barrel_dks_target_game : 1;
	unsigned char frantic_factory_crusher_room : 1;
	unsigned char jungle_japes_barrel_blast : 1;
	unsigned char angry_aztec : 1;
	unsigned char gloomy_galleon_seal_race : 1;
	unsigned char nintendo_logo : 1;
	unsigned char angry_aztec_barrel_blast : 1;
	unsigned char troff_n_scoff : 1;
	unsigned char gloomy_galleon_shipwreck_diddy_lanky_chunky : 1;
	unsigned char gloomy_galleon_treasure_chest : 1;
	unsigned char gloomy_galleon_mermaid : 1;
	unsigned char gloomy_galleon_shipwreck_dk_tiny : 1;
	unsigned char gloomy_galleon_shipwreck_lanky_tiny : 1;
	unsigned char fungi_forest : 1;
	unsigned char gloomy_galleon_lighthouse : 1;
	unsigned char k_rool_barrel_tinys_mushroom_game : 1;
	unsigned char gloomy_galleon_mechanical_fish : 1;
	unsigned char fungi_forest_ant_hill : 1;
	unsigned char battle_arena_beaver_brawl : 1;
	unsigned char gloomy_galleon_barrel_blast : 1;
	unsigned char fungi_forest_minecart : 1;
	unsigned char fungi_forest_diddys_barn : 1;
	unsigned char fungi_forest_diddys_attic : 1;
	unsigned char fungi_forest_lankys_attic : 1;
	unsigned char fungi_forest_dks_barn : 1;
	unsigned char fungi_forest_spider : 1;
	unsigned char fungi_forest_front_part_of_mill : 1;
	unsigned char fungi_forest_rear_part_of_mill : 1;
	unsigned char fungi_forest_mushroom_puzzle : 1;
	unsigned char fungi_forest_giant_mushroom : 1;
	unsigned char stealthy_snoop_normal : 1;
	unsigned char mad_maze_maul_hard : 1;
	unsigned char stash_snatch_normal : 1;
	unsigned char mad_maze_maul_easy : 1;
	unsigned char mad_maze_maul_normal : 1;
	unsigned char fungi_forest_mushroom_leap : 1;
	unsigned char fungi_forest_shooting_game : 1;
	unsigned char crystal_caves : 1;
	unsigned char battle_arena_kritter_karnage : 1;
	unsigned char stash_snatch_easy : 1;
	unsigned char stash_snatch_hard : 1;
	unsigned char dk_rap : 1;
	unsigned char minecart_mayhem_easy : 1;
	unsigned char busy_barrel_barrage_easy : 1;
	unsigned char busy_barrel_barrage_normal : 1;
	unsigned char main_menu : 1;
	unsigned char title_screen_not_for_resale_version : 1;
	unsigned char crystal_caves_beetle_race : 1;
	unsigned char fungi_forest_dogadon : 1;
	unsigned char crystal_caves_igloo_tiny : 1;
	unsigned char crystal_caves_igloo_lanky : 1;
	unsigned char crystal_caves_igloo_dk : 1;
	unsigned char creepy_castle : 1;
	unsigned char creepy_castle_ballroom : 1;
	unsigned char crystal_caves_rotating_room : 1;
	unsigned char crystal_caves_shack_chunky : 1;
	unsigned char crystal_caves_shack_dk : 1;
	unsigned char crystal_caves_shack_diddy_middle_part : 1;
	unsigned char crystal_caves_shack_tiny : 1;
	unsigned char crystal_caves_lankys_hut : 1;
	unsigned char crystal_caves_igloo_chunky : 1;
	unsigned char splish_splash_salvage_normal : 1;
	unsigned char k_lumsy : 1;
	unsigned char crystal_caves_ice_castle : 1;
	unsigned char speedy_swing_sortie_easy : 1;
	unsigned char crystal_caves_igloo_diddy : 1;
	unsigned char krazy_kong_klamour_easy : 1;
	unsigned char big_bug_bash_very_easy : 1;
	unsigned char searchlight_seek_very_easy : 1;
	unsigned char beaver_bother_easy : 1;
	unsigned char creepy_castle_tower : 1;
	unsigned char creepy_castle_minecart : 1;
	unsigned char kong_battle_battle_arena : 1;
	unsigned char creepy_castle_crypt_lanky_tiny : 1;
	unsigned char kong_battle_arena_1 : 1;
	unsigned char frantic_factory_barrel_blast : 1;
	unsigned char gloomy_galleon_pufftoss : 1;
	unsigned char creepy_castle_crypt_dk_diddy_chunky : 1;
	unsigned char creepy_castle_museum : 1;
	unsigned char creepy_castle_library : 1;
	unsigned char kremling_kosh_easy : 1;
	unsigned char kremling_kosh_normal : 1;
	unsigned char kremling_kosh_hard : 1;
	unsigned char teetering_turtle_trouble_easy : 1;
	unsigned char teetering_turtle_trouble_normal : 1;
	unsigned char teetering_turtle_trouble_hard : 1;
	unsigned char batty_barrel_bandit_easy : 1;
	unsigned char batty_barrel_bandit_normal : 1;
	unsigned char batty_barrel_bandit_hard : 1;
	unsigned char mad_maze_maul_insane : 1;
	unsigned char stash_snatch_insane : 1;
	unsigned char stealthy_snoop_very_easy : 1;
	unsigned char stealthy_snoop_easy : 1;
	unsigned char stealthy_snoop_hard : 1;
	unsigned char minecart_mayhem_normal : 1;
	unsigned char minecart_mayhem_hard : 1;
	unsigned char busy_barrel_barrage_hard : 1;
	unsigned char splish_splash_salvage_hard : 1;
	unsigned char splish_splash_salvage_easy : 1;
	unsigned char speedy_swing_sortie_normal : 1;
	unsigned char speedy_swing_sortie_hard : 1;
	unsigned char beaver_bother_normal : 1;
	unsigned char beaver_bother_hard : 1;
	unsigned char searchlight_seek_easy : 1;
	unsigned char searchlight_seek_normal : 1;
	unsigned char searchlight_seek_hard : 1;
	unsigned char krazy_kong_klamour_normal : 1;
	unsigned char krazy_kong_klamour_hard : 1;
	unsigned char krazy_kong_klamour_insane : 1;
	unsigned char peril_path_panic_very_easy : 1;
	unsigned char peril_path_panic_easy : 1;
	unsigned char peril_path_panic_normal : 1;
	unsigned char peril_path_panic_hard : 1;
	unsigned char big_bug_bash_easy : 1;
	unsigned char big_bug_bash_normal : 1;
	unsigned char big_bug_bash_hard : 1;
	unsigned char creepy_castle_dungeon : 1;
	unsigned char hideout_helm_intro_story : 1;
	unsigned char dk_isles_dk_theatre : 1;
	unsigned char frantic_factory_mad_jack : 1;
	unsigned char battle_arena_arena_ambush : 1;
	unsigned char battle_arena_more_kritter_karnage : 1;
	unsigned char battle_arena_forest_fracas : 1;
	unsigned char battle_arena_bish_bash_brawl : 1;
	unsigned char battle_arena_kamikaze_kremlings : 1;
	unsigned char battle_arena_plinth_panic : 1;
	unsigned char battle_arena_pinnacle_palaver : 1;
	unsigned char battle_arena_shockwave_showdown : 1;
	unsigned char creepy_castle_basement : 1;
	unsigned char creepy_castle_tree : 1;
	unsigned char k_rool_barrel_diddys_kremling_game : 1;
	unsigned char creepy_castle_chunkys_toolshed : 1;
	unsigned char creepy_castle_trash_can : 1;
	unsigned char creepy_castle_greenhouse : 1;
	unsigned char jungle_japes_lobby : 1;
	unsigned char hideout_helm_lobby : 1;
	unsigned char dks_house : 1;
	unsigned char rock_intro_story : 1;
	unsigned char angry_aztec_lobby : 1;
	unsigned char gloomy_galleon_lobby : 1;
	unsigned char frantic_factory_lobby : 1;
	unsigned char training_grounds : 1;
	unsigned char dive_barrel : 1;
	unsigned char fungi_forest_lobby : 1;
	unsigned char gloomy_galleon_submarine : 1;
	unsigned char orange_barrel : 1;
	unsigned char barrel_barrel : 1;
	unsigned char vine_barrel : 1;
	unsigned char creepy_castle_crypt : 1;
	unsigned char enguarde_arena : 1;
	unsigned char creepy_castle_car_race : 1;
	unsigned char crystal_caves_barrel_blast : 1;
	unsigned char creepy_castle_barrel_blast : 1;
	unsigned char fungi_forest_barrel_blast : 1;
	unsigned char fairy_island : 1;
	unsigned char kong_battle_arena_2 : 1;
	unsigned char rambi_arena : 1;
	unsigned char kong_battle_arena_3 : 1;
	unsigned char creepy_castle_lobby : 1;
	unsigned char crystal_caves_lobby : 1;
	unsigned char dk_isles_snides_room : 1;
	unsigned char crystal_caves_army_dillo : 1;
	unsigned char angry_aztec_dogadon : 1;
	unsigned char training_grounds_end_sequence : 1;
	unsigned char creepy_castle_king_kut_out : 1;
	unsigned char crystal_caves_shack_diddy_upper_part : 1;
	unsigned char k_rool_barrel_diddys_rocketbarrel_game : 1;
	unsigned char k_rool_barrel_lankys_shooting_game : 1;
	unsigned char k_rool_fight_dk_phase : 1;
	unsigned char k_rool_fight_diddy_phase : 1;
	unsigned char k_rool_fight_lanky_phase : 1;
	unsigned char k_rool_fight_tiny_phase : 1;
	unsigned char k_rool_fight_chunky_phase : 1;
	unsigned char bloopers_ending : 1;
	unsigned char k_rool_barrel_chunkys_hidden_kremling_game : 1;
	unsigned char k_rool_barrel_tinys_pony_tail_twirl_game : 1;
	unsigned char k_rool_barrel_chunkys_shooting_game : 1;
	unsigned char k_rool_barrel_dks_rambi_game : 1;
	unsigned char k_lumsy_ending : 1;
	unsigned char k_rools_shoe : 1;
	unsigned char k_rools_arena : 1;
} map_bitfield;

typedef struct movement_bitfield {
	unsigned char null_state : 1;
	unsigned char idle_enemy : 1;
	unsigned char first_person_camera : 1;
	unsigned char first_person_camera_water : 1;
	unsigned char fairy_camera : 1;
	unsigned char fairy_camera_water : 1;
	unsigned char locked_bonus_barrel_0x6 : 1;
	unsigned char minecart_idle : 1;
	unsigned char minecart_crouch : 1;
	unsigned char minecart_jump : 1;
	unsigned char minecart_left : 1;
	unsigned char minecart_right : 1;
	unsigned char idle : 1;
	unsigned char walking : 1;
	unsigned char skidding : 1;
	unsigned char sliding_beetle_race : 1;
	unsigned char sliding_beetle_race_left : 1;
	unsigned char sliding_beetle_race_right : 1;
	unsigned char sliding_beetle_race_forward : 1;
	unsigned char sliding_beetle_race_back : 1;
	unsigned char jumping_beetle_race : 1;
	unsigned char slipping : 1;
	unsigned char slipping_helm_slope : 1;
	unsigned char jumping : 1;
	unsigned char baboon_blast_pad : 1;
	unsigned char bouncing_mushroom : 1;
	unsigned char double_jump : 1;
	unsigned char simian_spring : 1;
	unsigned char simian_slam : 1;
	unsigned char long_jumping : 1;
	unsigned char falling : 1;
	unsigned char falling_gun : 1;
	unsigned char falling_or_splat : 1;
	unsigned char falling_beetle_race : 1;
	unsigned char pony_tail_twirl : 1;
	unsigned char attacking_enemy : 1;
	unsigned char primate_punch : 1;
	unsigned char attacking_enemy_0x25 : 1;
	unsigned char ground_attack : 1;
	unsigned char attacking_enemy_0x27 : 1;
	unsigned char ground_attack_final : 1;
	unsigned char moving_ground_attack : 1;
	unsigned char aerial_attack : 1;
	unsigned char rolling : 1;
	unsigned char throwing_orange : 1;
	unsigned char shockwave : 1;
	unsigned char chimpy_charge : 1;
	unsigned char charging_rambi : 1;
	unsigned char bouncing : 1;
	unsigned char damaged : 1;
	unsigned char stunlocked_kasplat : 1;
	unsigned char damaged_mad_jack : 1;
	unsigned char unknown_0x34 : 1;
	unsigned char damaged_klump_knockback : 1;
	unsigned char death : 1;
	unsigned char damaged_underwater : 1;
	unsigned char damaged_vehicle : 1;
	unsigned char shrinking : 1;
	unsigned char unknown_0x3a : 1;
	unsigned char death_dogadon : 1;
	unsigned char crouching : 1;
	unsigned char uncrouching : 1;
	unsigned char backflip : 1;
	unsigned char entering_orangstand : 1;
	unsigned char orangstand : 1;
	unsigned char jumping_orangstand : 1;
	unsigned char barrel_tag_barrel : 1;
	unsigned char barrel_underwater : 1;
	unsigned char baboon_blast_shot : 1;
	unsigned char cannon_shot : 1;
	unsigned char pushing_object : 1;
	unsigned char picking_up_object : 1;
	unsigned char idle_carrying_object : 1;
	unsigned char walking_carrying_object : 1;
	unsigned char dropping_object : 1;
	unsigned char throwing_object : 1;
	unsigned char jumping_carrying_object : 1;
	unsigned char throwing_object_air : 1;
	unsigned char surface_swimming : 1;
	unsigned char underwater : 1;
	unsigned char leaving_water : 1;
	unsigned char jumping_water : 1;
	unsigned char bananaporter : 1;
	unsigned char monkeyport : 1;
	unsigned char bananaport_multiplayer : 1;
	unsigned char unknown_0x55 : 1;
	unsigned char locked_funky_and_candy : 1;
	unsigned char swinging_on_vine : 1;
	unsigned char leaving_vine : 1;
	unsigned char climbing_tree : 1;
	unsigned char leaving_tree : 1;
	unsigned char grabbed_ledge : 1;
	unsigned char pulling_up_on_ledge : 1;
	unsigned char idle_gun : 1;
	unsigned char walking_gun : 1;
	unsigned char putting_away_gun : 1;
	unsigned char pulling_out_gun : 1;
	unsigned char jumping_gun : 1;
	unsigned char aiming_gun : 1;
	unsigned char rocketbarrel : 1;
	unsigned char taking_photo : 1;
	unsigned char taking_photo_underwater : 1;
	unsigned char damaged_tnt_barrels : 1;
	unsigned char instrument : 1;
	unsigned char unknown_0x68 : 1;
	unsigned char car_race : 1;
	unsigned char learning_gun : 1;
	unsigned char locked_bonus_barrel_0x6b : 1;
	unsigned char feeding_tns : 1;
	unsigned char boat : 1;
	unsigned char baboon_balloon : 1;
	unsigned char updraft : 1;
	unsigned char gb_dance : 1;
	unsigned char key_dance : 1;
	unsigned char crown_dance : 1;
	unsigned char loss_dance : 1;
	unsigned char victory_dance : 1;
	unsigned char vehicle_castle_car_race : 1;
	unsigned char entering_battle_crown : 1;
	unsigned char locked_cutscenes : 1;
	unsigned char gorilla_grab : 1;
	unsigned char learning_move : 1;
	unsigned char locked_car_race_loss : 1;
	unsigned char locked_beetle_race_loss : 1;
	unsigned char trapped : 1;
	unsigned char klaptrap_kong : 1;
	unsigned char surface_swimming_enguarde : 1;
	unsigned char underwater_enguarde : 1;
	unsigned char attacking_enguarde_surface : 1;
	unsigned char attacking_enguarde : 1;
	unsigned char leaving_water_enguarde : 1;
	unsigned char fairy_refill : 1;
	unsigned char unknown_0x84 : 1;
	unsigned char main_menu : 1;
	unsigned char entering_main_menu : 1;
	unsigned char entering_portal : 1;
	unsigned char exiting_portal : 1;
} movement_bitfield;

typedef struct collected_item_struct {
	/* 0x000 */ short id;
	/* 0x002 */ short obj_type;
	/* 0x004 */ char unk_04[0x1A - 0x4];
	/* 0x01A */ unsigned char is_homing;
	/* 0x01B */ char unk_1B;
	/* 0x01C */ void* next_item;
} collected_item_struct;

typedef struct quality_options {
	unsigned char reduce_lag : 1;
	unsigned char remove_cutscenes : 1; // 1
	unsigned char mountain_bridge_extended : 1;
	unsigned char unused_3 : 1; // 3
	unsigned char dance_skip : 1;
	unsigned char fast_boot : 1; // 5
	unsigned char no_ship_timers : 1;
	unsigned char ammo_swap : 1; // 7
	unsigned char cb_indicator : 1;
	unsigned char galleon_star : 1; // 9
	unsigned char vanilla_fixes : 1;
	unsigned char textbox_hold : 1; // 11
	unsigned char caves_kosha_dead : 1;
	unsigned char rambi_enguarde_pickup : 1; // 13
	unsigned char hud_bp_multibunch : 1;
	unsigned char homing_balloons : 1; // 15
	unsigned char save_krool_progress : 1;
	unsigned char unused_17 : 1; // 17
	unsigned char blueprint_compression : 1;
	unsigned char fast_hints : 1; // 19
	unsigned char unused_20 : 1;
	unsigned char global_instrument : 1; // 21
	unsigned char fast_pause_transitions : 1;
	unsigned char cannon_game_speed : 1; // 23
	unsigned char remove_enemy_cabin_timer : 1;
} quality_options;

typedef struct image_cache_struct {
	/* 0x000 */ void* image_pointer;
	/* 0x004 */ short image_index;
	/* 0x006 */ unsigned char image_state;
	/* 0x007 */ char unk7;
} image_cache_struct;

typedef struct kong_model_struct {
	/* 0x000 */ int actor;
	/* 0x004 */ int kong_index;
	/* 0x008 */ int model;
	/* 0x00C */ int props_or;
} kong_model_struct;

typedef struct bonus_vanilla_info {
	/* 0x000 */ short flag;
	/* 0x002 */ unsigned char kong_actor;
	/* 0x003 */ unsigned char spawn_actor;
} bonus_vanilla_info;

typedef struct bonus_barrel_info {
	/* 0x000 */ short flag;
	/* 0x002 */ unsigned char kong_actor;
	/* 0x003 */ unsigned char unused;
	/* 0x004 */ unsigned short spawn_actor;
} bonus_barrel_info;

typedef struct bonus_paad {
	/* 0x000 */ float oscillation_y;
	/* 0x004 */ short unk4;
	/* 0x006 */ short unk6;
	/* 0x008 */ short unk8;
	/* 0x00A */ short barrel_index;
	/* 0x00C */ char other_timer;
	/* 0x00D */ char destroy_timer;
	/* 0x00E */ char raise_timer;
} bonus_paad;

typedef struct tag_model_struct {
	/* 0x000 */ short model;
	/* 0x002 */ short actor;
	/* 0x004 */ char unk0;
	/* 0x005 */ char unk1;
} tag_model_struct;

typedef struct mtx_item {
	/* 0x000 */ float mf[4][4];
} mtx_item;

typedef struct actor_behaviour_def {
    /* 0x000 */ short actor_type;
    /* 0x002 */ short model;
    /* 0x004 */ char unk4[8];
    /* 0x00C */ void* code;
    /* 0x010 */ void* unk10;
    /* 0x014 */ char str[0x1C];
} actor_behaviour_def;

typedef struct move_text_overlay_struct {
	/* 0x000 */ unsigned char type;
	/* 0x001 */ unsigned char kong;
	/* 0x002 */ short flag;
	/* 0x004 */ char* string;
	/* 0x008 */ unsigned char used;
	/* 0x009 */ char pad_9[3]; // Used to align with a 4-byte region
} move_text_overlay_struct;

typedef struct rgb {
	/* 0x000 */ unsigned char red;
	/* 0x001 */ unsigned char green;
	/* 0x002 */ unsigned char blue;
} rgb;

typedef struct skybox_blend_struct {
	/* 0x000 */ rgb top;
	/* 0x003 */ rgb bottom;
	/* 0x006 */ rgb unk[2];
} skybox_blend_struct;

typedef struct menu_controller_paad {
	/* 0x000 */ float screen_transition_progress;
	/* 0x004 */ float unk_4;
	/* 0x008 */ char unk_8[0x12-0x8];
	/* 0x012 */ unsigned char current_screen;
	/* 0x013 */ unsigned char next_screen;
	/* 0x014 */ char unk_14[0x16-0x14];
	/* 0x016 */ char prevent_action;
	/* 0x017 */ char selected_action;
} menu_controller_paad;

typedef struct spotlight_hold_paad {
	/* 0x000 */ short unk0;
	/* 0x002 */ char unk2;
} spotlight_hold_paad;

typedef struct pause_paad {
	/* 0x000 */ float unk0;
	/* 0x004 */ char unk4[0xC-0x4];
	/* 0x00C */ short unkC[2];
	/* 0x010 */ unsigned short control;
	/* 0x012 */ char screen;
	/* 0x013 */ char next_screen;
	/* 0x014 */ char unk14;
	/* 0x015 */ char unk15;
} pause_paad;

typedef struct sprite_struct {
	/* 0x000 */ char unk0[0x338];
	/* 0x338 */ void* actor;
	/* 0x33C */ char unk33C[0x340-0x33C];
	/* 0x340 */ float x;
	/* 0x344 */ float y;
	/* 0x348 */ float z;
	/* 0x34C */ char unk34C[0x35C-0x34C];
	/* 0x35C */ void* control;
	/* 0x360 */ float scale_x;
	/* 0x364 */ float scale_z;
	/* 0x368 */ char unk360[0x36A-0x368];
	/* 0x36A */ unsigned char red;
	/* 0x36B */ unsigned char green;
	/* 0x36C */ unsigned char blue;
	/* 0x36D */ unsigned char alpha;
	/* 0x36E */ char unk36E[0x384-0x36E];
	/* 0x384 */ float* unk384;
} sprite_struct;

typedef struct check_struct {
    /* 0x000 */ short flag;
    /* 0x002 */ unsigned char type;
    /* 0x003 */ char associated_level;
} check_struct;

typedef struct sprite_data_struct {
	/* 0x000 */ int unk0;
	/* 0x004 */ char images_per_frame_horizontal;
	/* 0x005 */ char images_per_frame_vertical;
	/* 0x006 */ short codec;
	/* 0x008 */ int unk8;
	/* 0x00C */ char unkC;
	/* 0x00D */ char table;
	/* 0x00E */ short width;
	/* 0x010 */ short height;
	/* 0x012 */ short image_count;
	/* 0x014 */ short images[];
} sprite_data_struct;

typedef struct item_conversion_info {
	/* 0x000 */ short actor;
	/* 0x002 */ short model_two;
	/* 0x004 */ float scale;
} item_conversion_info;

typedef struct item_scale_info {
	/* 0x000 */ int type;
	/* 0x004 */ float scale;
} item_scale_info;

typedef struct charSpawnerActorInfo {
	/* 0x000 */ short actor;
	/* 0x002 */ short model;
	/* 0x004 */ short animation;
	/* 0x006 */ short unk_6;
	/* 0x008 */ int unk_8;
	/* 0x00C */ char unk_C[0x18-0xC];
} charSpawnerActorInfo;

typedef struct player_collision_info {
    /* 0x000 */ float x;
    /* 0x004 */ float y;
    /* 0x008 */ float z;
    /* 0x00C */ float scale;
} player_collision_info;

typedef struct item_collision {
	/* 0x000 */ short id;
	/* 0x002 */ short obj_type;
	/* 0x004 */ short kong;
	/* 0x006 */ short flag;
	/* 0x008 */ short x;
	/* 0x00A */ short y;
	/* 0x00C */ short z;
	/* 0x00E */ char colliding;
	/* 0x00F */ char unkF[0x13-0xF];
	/* 0x013 */ char unk13;
	/* 0x014 */ char collision_index;
	/* 0x015 */ char unk15[0x18-0x15];
	/* 0x018 */ void* next;
	/* 0x01C */ float scale;
} item_collision;

typedef struct hitbox_master_struct {
	/* 0x000 */ item_collision* hitbox[512];
} hitbox_master_struct;

typedef struct fairy_location_item {
	/* 0x000 */ short flag;
	/* 0x002 */ unsigned char map;
	/* 0x003 */ unsigned char id;
} fairy_location_item;

typedef struct fairy_activations {
	unsigned char japes_painting : 1; // 0
	unsigned char factory_funky : 1; // 1
	unsigned char galleon_chest : 1; // 2
	unsigned char fungi_dark_attic : 1; // 3
	unsigned char fungi_thornvine_barn : 1; // 4
	unsigned char caves_igloo : 1; // 5
	unsigned char caves_cabin : 1; // 6
	unsigned char isles_factory_lobby : 1; // 7
	unsigned char isles_fungi_lobby : 1; // 8
} fairy_activations;

typedef struct collision_data_struct {
    /* 0x000 */ void* collision_info;
    /* 0x004 */ char unk_4;
    /* 0x005 */ char unk_5[3];
} collision_data_struct;

typedef struct health_damage_struct {
    /* 0x000 */ short init_health;
    /* 0x002 */ short damage_applied;
} health_damage_struct;

typedef struct collision_info {
    /* 0x000 */ unsigned short type;
    /* 0x002 */ char collectable_type;
    /* 0x003 */ char unk3;
    /* 0x004 */ float unk4;
    /* 0x008 */ float unk8;
    /* 0x00C */ short intended_actor;
    /* 0x00E */ short actor_equivalent;
    /* 0x010 */ short hitbox_y_center;
    /* 0x012 */ short hitbox_radius;
    /* 0x014 */ short hitbox_height;
} collision_info;

typedef struct stack_trace_address_struct {
	/* 0x000 */ void* address;
	/* 0x004 */ int used;
} stack_trace_address_struct;

typedef struct moves_pregiven_bitfield {
	unsigned char blast : 1; // 0 0x80
	unsigned char strong_kong : 1; // 1 0x40
	unsigned char grab : 1; // 2 0x20
	unsigned char charge : 1; // 3 0x10
	unsigned char rocketbarrel : 1; // 4 0x08
	unsigned char spring : 1; // 5 0x04
	unsigned char ostand : 1; // 6 0x02
	unsigned char balloon : 1; // 7 0x01
	unsigned char osprint : 1; // 0 0x80
	unsigned char mini : 1; // 1 0x40
	unsigned char twirl : 1; // 2 0x20
	unsigned char monkeyport : 1; // 3 0x10
	unsigned char hunky : 1; // 4 0x08
	unsigned char punch : 1; // 5 0x04
	unsigned char gone : 1; // 6 0x02
	unsigned char slam_upgrade_0 : 1; // 7 0x01
	unsigned char slam_upgrade_1 : 1; // 0 0x80
	unsigned char slam_upgrade_2 : 1; // 1 0x40
	unsigned char coconut : 1; // 2 0x20
	unsigned char peanut : 1; // 3 0x10
	unsigned char grape : 1; // 4 0x08
	unsigned char feather : 1; // 5 0x04
	unsigned char pineapple : 1; // 6 0x02
	unsigned char bongos : 1; // 7 0x01
	unsigned char guitar : 1; // 0 0x80
	unsigned char trombone : 1; // 1 0x40
	unsigned char sax : 1; // 2 0x20
	unsigned char triangle : 1; // 3 0x10
	unsigned char belt_upgrade_0 : 1; // 4 0x08
	unsigned char belt_upgrade_1 : 1; // 5 0x04
	unsigned char homing : 1; // 6 0x02
	unsigned char sniper : 1; // 7 0x01
	unsigned char ins_upgrade_0 : 1; // 0 0x80
	unsigned char ins_upgrade_1 : 1; // 1 0x40
	unsigned char ins_upgrade_2 : 1; // 2 0x20
	unsigned char dive : 1; // 3 0x10
	unsigned char oranges : 1; // 4 0x08
	unsigned char barrels : 1; // 5 0x04
	unsigned char vines : 1; // 6 0x02
	unsigned char camera : 1; // 7 0x01
	unsigned char shockwave : 1; // 0 0x80
	unsigned char climbing : 1; // 1 0x40
} moves_pregiven_bitfield;

typedef struct weather_struct {
	/* 0x000 */ char frame_count;
	/* 0x001 */ char unk_1[3];
	/* 0x004 */ short* texture_pointer;
	/* 0x008 */ short codec_info;
	/* 0x00A */ unsigned char width;
	/* 0x00B */ unsigned char height;
	/* 0x00C */ void* unkC;
	/* 0x010 */ void* falling_func;
} weather_struct;

typedef struct buttons {
	unsigned char a : 1; // 0x8000
	unsigned char b : 1; // 0x4000
	unsigned char z : 1; // 0x2000
	unsigned char start : 1; // 0x1000
	unsigned char d_up : 1; // 0x0800
	unsigned char d_down : 1; // 0x0400
	unsigned char d_left : 1; // 0x0200
	unsigned char d_right : 1; // 0x0100
	unsigned char unused_0 : 1; // 0x0080
	unsigned char unused_1 : 1; // 0x0040
	unsigned char l : 1; // 0x0020
	unsigned char r : 1; // 0x0010
	unsigned char c_up : 1; // 0x0008
	unsigned char c_down : 1; // 0x0004
	unsigned char c_left : 1; // 0x0002
	unsigned char c_right : 1; // 0x0001
} buttons;

typedef struct Controller {
	/* 0x000 */ buttons Buttons;
	/* 0x002 */ char stickX;
	/* 0x003 */ char stickY;
} Controller;

typedef struct Border {
	/* 0x000 */ char player_count;
	/* 0x001 */ char unk1;
	/* 0x002 */ char unk2;
	/* 0x003 */ char unk3;
	/* 0x004 */ short blackness_left;
	/* 0x006 */ short blackness_top;
	/* 0x008 */ short blackness_right;
	/* 0x00A */ short blackness_bottom;
} Border;

typedef struct DisabledMusicStruct {
	unsigned char wrinkly : 1; // 0x80
	unsigned char shops : 1; // 0x40
	unsigned char events : 1; // 0x20
	unsigned char transform : 1; // 0x10
	unsigned char pause : 1; // 0x08
	unsigned char chunk_songs : 1; // 0x04
	unsigned char unk6 : 1; // 0x02
	unsigned char unk7 : 1; // 0x01
} DisabledMusicStruct;

typedef struct HardModeSettings {
	unsigned char easy_fall : 1; // 0x80
	unsigned char lava_water : 1; // 0x40
	unsigned char bosses : 1; // 0x20
	unsigned char enemies : 1; // 0x10
	unsigned char dark_world : 1; // 0x08
	unsigned char no_geo : 1; // 0x04
	unsigned char memory_challenge : 1; // 0x02
	unsigned char unk7 : 1; // 0x01
} HardModeSettings;

typedef struct SurfaceInfo {
	/* 0x000 */ void* texture_loader;
	/* 0x004 */ void* dl_writer;
	/* 0x008 */ void* ripple_handler;
	/* 0x00C */ void* textures[2];
	/* 0x014 */ unsigned char unk14[4];
} SurfaceInfo;

typedef struct ChunkColorData {
	/* 0x000 */ char unk0[0xC];
	/* 0x00C */ rgb color;
} ChunkColorData;

typedef struct ChunkSub {
	/* 0x000 */ char unk0[0x14];
	/* 0X014 */ ChunkColorData* colors[4];
} ChunkSub;

typedef struct Chunk {
	/* 0x000 */ char unk0[3];
	/* 0x003 */ char reference_dynamic_lighting;
	/* 0x004 */ char unk4[0x4C-0x4];
	/* 0x04C */ ChunkSub* color_pointer;
	/* 0x050 */ char unk50[0x1C8-0x50];
} Chunk;

typedef struct enemy_item_memory_item {
	/* 0x000 */ unsigned short actor;
	/* 0x002 */ unsigned short flag;
} enemy_item_memory_item;

typedef struct enemy_item_rom_item {
	/* 0x000 */ unsigned char map;
	/* 0x001 */ unsigned char char_spawner_id;
	/* 0x002 */ unsigned short actor;
} enemy_item_rom_item;

typedef struct enemy_item_db_item {
	/* 0x000 */ enemy_item_memory_item spawn;
	/* 0x004 */ unsigned short global_index;
} enemy_item_db_item;

typedef struct drop_item {
    /* 0x000 */ short source_object;
    /* 0x002 */ short dropped_object;
    /* 0x004 */ unsigned char drop_music;
    /* 0x005 */ unsigned char drop_count;
} drop_item;

typedef struct sprite_info {
	/* 0x000 */ char unk_00[0x358];
	/* 0x358 */ int timer;
	/* 0x35C */ char unk_35C[0x360-0x35C];
	/* 0x360 */ float scale_x;
	/* 0x364 */ float scale_z;
	/* 0x368 */ char unk_368[0x36A-0x368];
	/* 0x36A */ unsigned char red;
	/* 0x36B */ unsigned char green;
	/* 0x36C */ unsigned char blue;
	/* 0x36D */ unsigned char alpha;
} sprite_info;

typedef struct RandomSwitchesIsles {
	/* 0x000 */ unsigned char monkeyport; // 0 = monkeyport, 1 = blast, 2 = balloon
	/* 0x001 */ unsigned char gone; // 0 = gone, 1-5 = instrument
	/* 0x002 */ unsigned char aztec_lobby_feather;
	/* 0x003 */ unsigned char fungi_lobby_feather;
	/* 0x004 */ unsigned char spawn_rocketbarrel;
} RandomSwitchesIsles;

typedef struct RandomSwitchesJapes {
	/* 0x000 */ unsigned char feather;
	/* 0x001 */ unsigned char rambi;
	/* 0x002 */ unsigned char painting;
	/* 0x003 */ unsigned char diddy_cave;
} RandomSwitchesJapes;

typedef struct RandomSwitchesAztec {
	/* 0x000 */ unsigned char bp_door;
	/* 0x001 */ unsigned char llama_switches[3];
	/* 0x004 */ unsigned char snoop_switch;
	/* 0x005 */ unsigned char guitar;
} RandomSwitchesAztec;

typedef struct RandomSwitchesGalleon {
	/* 0x000 */ unsigned char lighthouse;
	/* 0x001 */ unsigned char shipwreck;
	/* 0x002 */ unsigned char cannongame;
} RandomSwitchesGalleon;

typedef struct RandomSwitchesFungi {
	/* 0x000 */ unsigned char yellow;
	/* 0x001 */ unsigned char green_feather;
	/* 0x002 */ unsigned char green_pineapple;
} RandomSwitchesFungi;

// Any 0s are treated as default
typedef struct RandomSwitchesSetting {
	/* 0x000 */ RandomSwitchesIsles isles;
	/* 0x005 */ RandomSwitchesJapes japes;
	/* 0x009 */ RandomSwitchesAztec aztec;
	/* 0x00F */ RandomSwitchesGalleon galleon;
	/* 0x012 */ RandomSwitchesFungi fungi;
} RandomSwitchesSetting;

typedef struct LZREntrance {
	/* 0x000 */ unsigned char map;
	/* 0x001 */ char exit;
} LZREntrance;

typedef struct ROMFlags {
	unsigned char plando : 1; // 0x80
	unsigned char spoiler : 1; // 0x40
	unsigned char pass_locked : 1; // 0x20
	unsigned char unk3 : 1; // 0x10
	unsigned char unk4 : 1; // 0x08
	unsigned char unk5 : 1; // 0x04
	unsigned char unk6 : 1; // 0x02
	unsigned char unk7 : 1; // 0x01
} ROMFlags;

typedef struct BooleanModelSwaps {
	unsigned char ice_tomato_is_regular : 1; // 0x80
	unsigned char regular_tomato_is_ice : 1; // 0x40
	unsigned char beetle_is_rabbit : 1; // 0x20
	unsigned char rabbit_is_beetle : 1; // 0x10
	unsigned char unk4 : 1; // 0x08
	unsigned char unk5 : 1; // 0x04
	unsigned char unk6 : 1; // 0x02
	unsigned char unk7 : 1; // 0x01
} BooleanModelSwaps;

typedef struct ItemRequirement {
	/* 0x000 */ unsigned char item;
	/* 0x001 */ unsigned char count;
} ItemRequirement;

typedef struct FreeTradeAgreement {
	unsigned char major_items : 1; // 0x80
	unsigned char blueprints : 1; // 0x40
	unsigned char coins_cbs : 1; // 0x20
	unsigned char balloons : 1; // 0x10
	unsigned char unk4 : 1; // 0x08
	unsigned char unk5 : 1; // 0x04
	unsigned char unk6 : 1; // 0x02
	unsigned char unk7 : 1; // 0x01
} FreeTradeAgreement;

typedef struct LocationVisuals {
	unsigned char crowns : 1; // 0x80
	unsigned char boss_doors : 1; // 0x40
	unsigned char bonus_barrels : 1; // 0x20
	unsigned char dirt_patches : 1; // 0x10
	unsigned char unk4 : 1; // 0x08
	unsigned char unk5 : 1; // 0x04
	unsigned char unk6 : 1; // 0x02
	unsigned char unk7 : 1; // 0x01
} LocationVisuals;

typedef struct path_segment_struct {
	/* 0x000 */ short unk0;
	/* 0x002 */ short x;
	/* 0x004 */ short y;
	/* 0x006 */ short z;
	/* 0x008 */ char speed;
	/* 0x009 */ char unk1;
} path_segment_struct;

typedef struct path_data_struct {
	/* 0x000 */ void* tied_actor;
	/* 0x004 */ path_segment_struct* segments;
	/* 0x008 */ short segment_count;
	/* 0x00A */ char unk_0A[2];
	/* 0x00C */ float segment_position;
	/* 0x010 */ int segment_index;
	/* 0x014 */ char unk14;
	/* 0x015 */ char unk15;
	/* 0x016 */ char unk16;
	/* 0x017 */ char unk17;
	/* 0x018 */ int unk18;
	/* 0x01C */ int path_cycle_count;
	/* 0x020 */ char path_global_speed;
	/* 0x021 */ char unk21;
	/* 0x022 */ char unk_22[0x30-0x22];
} path_data_struct;

typedef struct pen_a_data {
	/* 0x000 */ short x;
	/* 0x002 */ short y;
	/* 0x004 */ short z;
	/* 0x006 */ unsigned char unk6;
	/* 0x007 */ unsigned char unk7;
	/* 0x008 */ unsigned char speed_cap;
	/* 0x009 */ unsigned char unk9;
} pen_a_data;

typedef struct fence_collective_struct {
	/* 0x000 */ char unk_00[0x14];
	/* 0x014 */ pen_a_data* pen_A;
} fence_collective_struct;

typedef struct actor_bitfield {
	// 0
	unsigned char unknown_0 : 1;
	unsigned char unknown_1 : 1;
	unsigned char dk : 1;
	unsigned char diddy : 1;
	unsigned char lanky : 1;
	unsigned char tiny : 1;
	unsigned char chunky : 1;
	unsigned char krusha : 1;
	unsigned char rambi : 1;
	unsigned char enguarde : 1;
	// 10
	unsigned char unknown_10 : 1;
	unsigned char unknown_11 : 1;
	unsigned char loading_zone_controller : 1;
	unsigned char object_model_2_controller : 1;
	unsigned char unknown_14 : 1;
	unsigned char unknown_15 : 1;
	unsigned char unknown_16 : 1;
	unsigned char cannon_barrel : 1;
	unsigned char rambi_crate : 1;
	unsigned char barrel_diddy_5di : 1;
	// 20
	unsigned char camera_focus_point : 1;
	unsigned char pushable_box : 1;
	unsigned char barrel_spawner : 1;
	unsigned char cannon : 1;
	unsigned char race_hoop : 1;
	unsigned char hunky_chunky_barrel : 1;
	unsigned char tnt_barrel : 1;
	unsigned char tnt_barrel_spawner : 1;
	unsigned char bonus_barrel : 1;
	unsigned char minecart : 1;
	// 30
	unsigned char fireball : 1;
	unsigned char bridge_castle : 1;
	unsigned char swinging_light : 1;
	unsigned char vine : 1;
	unsigned char kremling_kosh_controller : 1;
	unsigned char melon_projectile : 1;
	unsigned char peanut : 1;
	unsigned char rocketbarrel : 1;
	unsigned char pineapple : 1;
	unsigned char large_brown_bridge : 1;
	// 40
	unsigned char mini_monkey_barrel : 1;
	unsigned char orange : 1;
	unsigned char grape : 1;
	unsigned char feather : 1;
	unsigned char laser : 1;
	unsigned char golden_banana : 1;
	unsigned char barrel_gun : 1;
	unsigned char watermelon_slice : 1;
	unsigned char coconut : 1;
	unsigned char rocketbarrel_49 : 1;
	// 50
	unsigned char lime : 1;
	unsigned char ammo_crate : 1;
	unsigned char orange_pickup : 1;
	unsigned char banana_coin : 1;
	unsigned char dk_coin : 1;
	unsigned char small_explosion : 1;
	unsigned char orangstand_sprint_barrel : 1;
	unsigned char strong_kong_barrel : 1;
	unsigned char swinging_light_58 : 1;
	unsigned char fireball_59 : 1;
	// 60
	unsigned char bananaporter : 1;
	unsigned char boulder : 1;
	unsigned char minecart_62 : 1;
	unsigned char vase_o : 1;
	unsigned char vase_colon : 1;
	unsigned char vase_triangle : 1;
	unsigned char vase_plus : 1;
	unsigned char cannon_ball : 1;
	unsigned char unknown_68 : 1;
	unsigned char vine_69 : 1;
	// 70
	unsigned char counter : 1;
	unsigned char kremling_red : 1;
	unsigned char boss_key : 1;
	unsigned char cannon_73 : 1;
	unsigned char cannon_ball_74 : 1;
	unsigned char blueprint_diddy : 1;
	unsigned char blueprint_chunky : 1;
	unsigned char blueprint_lanky : 1;
	unsigned char blueprint_dk : 1;
	unsigned char blueprint_tiny : 1;
	// 80
	unsigned char minecart_80 : 1;
	unsigned char fire_spawner_dogadon : 1;
	unsigned char boulder_debris : 1;
	unsigned char spider_web : 1;
	unsigned char steel_keg_spawner : 1;
	unsigned char steel_keg : 1;
	unsigned char crown : 1;
	unsigned char minecart_87 : 1;
	unsigned char unknown_88 : 1;
	unsigned char fire : 1;
	// 90
	unsigned char ice_wall : 1;
	unsigned char balloon_diddy : 1;
	unsigned char stalactite : 1;
	unsigned char rock_debris : 1;
	unsigned char car : 1;
	unsigned char pause_menu : 1;
	unsigned char hunky_chunky_barrel_dogadon : 1;
	unsigned char tnt_barrel_spawner_dogadon : 1;
	unsigned char tag_barrel : 1;
	unsigned char fireball_99 : 1;
	// 100
	unsigned char pad_1_diddy_5di : 1;
	unsigned char pad_2_diddy_5di : 1;
	unsigned char pad_3_diddy_5di : 1;
	unsigned char pad_4_diddy_5di : 1;
	unsigned char pad_5_diddy_5di : 1;
	unsigned char pad_6_diddy_5di : 1;
	unsigned char kong_reflection : 1;
	unsigned char bonus_barrel_hideout_helm : 1;
	unsigned char unknown_108 : 1;
	unsigned char race_checkpoint : 1;
	// 110
	unsigned char cb_bunch : 1;
	unsigned char balloon_chunky : 1;
	unsigned char balloon_tiny : 1;
	unsigned char balloon_lanky : 1;
	unsigned char balloon_dk : 1;
	unsigned char klumsys_cage : 1;
	unsigned char chain : 1;
	unsigned char beanstalk : 1;
	unsigned char yellow_qmark : 1;
	unsigned char cb_single_blue : 1;
	// 120
	unsigned char cb_single_yellow : 1;
	unsigned char crystal_coconut : 1;
	unsigned char dk_coin_122 : 1;
	unsigned char kong_mirror : 1;
	unsigned char barrel_gun_124 : 1;
	unsigned char barrel_gun_125 : 1;
	unsigned char fly_swatter : 1;
	unsigned char searchlight : 1;
	unsigned char headphones : 1;
	unsigned char enguarde_crate : 1;
	// 130
	unsigned char apple : 1;
	unsigned char worm : 1;
	unsigned char enguarde_crate_unused : 1;
	unsigned char barrel : 1;
	unsigned char training_barrel : 1;
	unsigned char boombox : 1;
	unsigned char tag_barrel_136 : 1;
	unsigned char tag_barrel_137 : 1;
	unsigned char b_locker : 1;
	unsigned char rainbow_coin_patch : 1;
	// 140
	unsigned char rainbow_coin : 1;
	unsigned char unknown_141 : 1;
	unsigned char unknown_142 : 1;
	unsigned char unknown_143 : 1;
	unsigned char unknown_144 : 1;
	unsigned char cannon_seasick_chunky : 1;
	unsigned char unknown_146 : 1;
	unsigned char balloon_unused_k_rool : 1;
	unsigned char rope : 1;
	unsigned char banana_barrel : 1;
	// 150
	unsigned char banana_barrel_spawner : 1;
	unsigned char unknown_151 : 1;
	unsigned char unknown_152 : 1;
	unsigned char unknown_153 : 1;
	unsigned char unknown_154 : 1;
	unsigned char unknown_155 : 1;
	unsigned char wrinkly : 1;
	unsigned char unknown_157 : 1;
	unsigned char unknown_158 : 1;
	unsigned char unknown_159 : 1;
	// 160
	unsigned char unknown_160 : 1;
	unsigned char unknown_161 : 1;
	unsigned char unknown_162 : 1;
	unsigned char banana_fairy_bfi : 1;
	unsigned char ice_tomato : 1;
	unsigned char tag_barrel_king_kut_out : 1;
	unsigned char king_kut_out_part : 1;
	unsigned char cannon_167 : 1;
	unsigned char unknown_168 : 1;
	unsigned char puftup : 1;
	// 170
	unsigned char damage_source : 1;
	unsigned char orange_171 : 1;
	unsigned char unknown_172 : 1;
	unsigned char cutscene_controller : 1;
	unsigned char unknown_174 : 1;
	unsigned char kaboom : 1;
	unsigned char timer : 1;
	unsigned char timer_controller : 1;
	unsigned char beaver : 1;
	unsigned char shockwave_mad_jack : 1;
	// 180
	unsigned char krash : 1;
	unsigned char book : 1;
	unsigned char klobber : 1;
	unsigned char zinger : 1;
	unsigned char snide : 1;
	unsigned char army_dillo : 1;
	unsigned char kremling : 1;
	unsigned char klump : 1;
	unsigned char camera : 1;
	unsigned char cranky : 1;
	// 190
	unsigned char funky : 1;
	unsigned char candy : 1;
	unsigned char beetle : 1;
	unsigned char mermaid : 1;
	unsigned char vulture : 1;
	unsigned char squawks : 1;
	unsigned char cutscene_dk : 1;
	unsigned char cutscene_diddy : 1;
	unsigned char cutscene_lanky : 1;
	unsigned char cutscene_tiny : 1;
	// 200
	unsigned char cutscene_chunky : 1;
	unsigned char llama : 1;
	unsigned char fairy_picture : 1;
	unsigned char padlock_tns : 1;
	unsigned char mad_jack : 1;
	unsigned char klaptrap : 1;
	unsigned char zinger_206 : 1;
	unsigned char vulture_race : 1;
	unsigned char klaptrap_purple : 1;
	unsigned char klaptrap_red : 1;
	// 210
	unsigned char getout_controller : 1;
	unsigned char klaptrap_skeleton : 1;
	unsigned char beaver_gold : 1;
	unsigned char fire_column_spawner : 1;
	unsigned char minecart_tnt : 1;
	unsigned char minecart_tnt_215 : 1;
	unsigned char puftoss : 1;
	unsigned char unknown_217 : 1;
	unsigned char handle : 1;
	unsigned char slot : 1;
	// 220
	unsigned char cannon_seasick_chunky_220 : 1;
	unsigned char light_piece : 1;
	unsigned char banana_peel : 1;
	unsigned char fireball_spawner : 1;
	unsigned char mushroom_man : 1;
	unsigned char unknown_225 : 1;
	unsigned char troff : 1;
	unsigned char k_rools_foot : 1;
	unsigned char bad_hit_detection_man : 1;
	unsigned char k_rools_toe : 1;
	// 230
	unsigned char ruler : 1;
	unsigned char toy_box : 1;
	unsigned char text_overlay : 1;
	unsigned char squawks_233 : 1;
	unsigned char scoff : 1;
	unsigned char robo_kremling : 1;
	unsigned char dogadon : 1;
	unsigned char unknown_237 : 1;
	unsigned char kremling_238 : 1;
	unsigned char bongos : 1;
	// 240
	unsigned char spotlight_fish : 1;
	unsigned char kasplat_dk : 1;
	unsigned char kasplat_diddy : 1;
	unsigned char kasplat_lanky : 1;
	unsigned char kasplat_tiny : 1;
	unsigned char kasplat_chunky : 1;
	unsigned char mechanical_fish : 1;
	unsigned char seal : 1;
	unsigned char banana_fairy : 1;
	unsigned char squawks_with_spotlight : 1;
	// 250
	unsigned char owl : 1;
	unsigned char spider_miniboss : 1;
	unsigned char rabbit : 1;
	unsigned char nintendo_logo : 1;
	unsigned char cutscene_object : 1;
	unsigned char shockwave : 1;
	unsigned char minigame_controller : 1;
	unsigned char fire_breath_spawner : 1;
	unsigned char shockwave_258 : 1;
	unsigned char guard : 1;
	// 260
	unsigned char text_overlay_260 : 1;
	unsigned char robo_zinger : 1;
	unsigned char krossbones : 1;
	unsigned char fire_shockwave_dogadon : 1;
	unsigned char squawks_264 : 1;
	unsigned char light_beam : 1;
	unsigned char dk_rap_controller : 1;
	unsigned char shuri : 1;
	unsigned char gimpfish : 1;
	unsigned char mr_dice : 1;
	// 270
	unsigned char sir_domino : 1;
	unsigned char mr_dice_271 : 1;
	unsigned char rabbit_272 : 1;
	unsigned char fireball_with_glasses : 1;
	unsigned char unknown_274 : 1;
	unsigned char k_lumsy : 1;
	unsigned char spiderling : 1;
	unsigned char squawks_277 : 1;
	unsigned char projectile : 1;
	unsigned char trap_bubble : 1;
	// 280
	unsigned char spider_silk_string : 1;
	unsigned char k_rool_dk_phase : 1;
	unsigned char retexturing_controller : 1;
	unsigned char skeleton_head : 1;
	unsigned char unknown_284 : 1;
	unsigned char bat : 1;
	unsigned char giant_clam : 1;
	unsigned char unknown_287 : 1;
	unsigned char tomato : 1;
	unsigned char kritter_in_a_sheet : 1;
	// 290
	unsigned char puftup_290 : 1;
	unsigned char kosha : 1;
	unsigned char k_rool_diddy_phase : 1;
	unsigned char k_rool_lanky_phase : 1;
	unsigned char k_rool_tiny_phase : 1;
	unsigned char k_rool_chunky_phase : 1;
	unsigned char unknown_296 : 1;
	unsigned char battle_crown_controller : 1;
	unsigned char unknown_298 : 1;
	unsigned char textbox : 1;
	// 300
	unsigned char snake : 1;
	unsigned char turtle : 1;
	unsigned char toy_car : 1;
	unsigned char toy_car_303 : 1;
	unsigned char camera_304 : 1;
	unsigned char missile : 1;
	unsigned char unknown_306 : 1;
	unsigned char unknown_307 : 1;
	unsigned char seal_308 : 1;
	unsigned char kong_logo_instrument : 1;
	// 310
	unsigned char spotlight : 1;
	unsigned char race_checkpoint_311 : 1;
	unsigned char minecart_tnt_312 : 1;
	unsigned char idle_particle : 1;
	unsigned char rareware_logo : 1;
	unsigned char unknown_315 : 1;
	unsigned char kong_tag_barrel : 1;
	unsigned char locked_kong_tag_barrel : 1;
	unsigned char unknown_318 : 1;
	unsigned char propeller_boat : 1;
	// 320
	unsigned char potion : 1;
	unsigned char fairy_refill : 1;
	unsigned char car_322 : 1;
	unsigned char enemy_car : 1;
	unsigned char text_overlay_controller : 1;
	unsigned char shockwave_325 : 1;
	unsigned char main_menu_controller : 1;
	unsigned char kong : 1;
	unsigned char klaptrap_328 : 1;
	unsigned char fairy : 1;
	// 330
	unsigned char bug : 1;
	unsigned char klaptrap_331 : 1;
	unsigned char big_bug_bash_controller : 1;
	unsigned char barrel_main_menu : 1;
	unsigned char padlock_k_lumsy : 1;
	unsigned char snides_menu : 1;
	unsigned char training_barrel_controller : 1;
	unsigned char multiplayer_model_main_menu : 1;
	unsigned char end_sequence_controller : 1;
	unsigned char arena_controller : 1;
	// 340
	unsigned char bug_340 : 1;
	unsigned char unknown_341 : 1;
	unsigned char try_again_dialog : 1;
	unsigned char pause_menu_343 : 1;
} actor_bitfield;

typedef struct map_properties_bitfield {
	// 807FBB64
	unsigned char disable_first_person : 1; // 8000 0000
	unsigned char menu_overlay : 1; // 4000 0000
	unsigned char unk02 : 1; // 2000 0000
	unsigned char in_training : 1; // 1000 0000 // Assume vines, amongst a couple other things
	unsigned char keep_camera_behind_player : 1; // 0800 0000
	unsigned char multiplayer : 1; // 0400 0000
	unsigned char unk06 : 1; // 0200 0000 // 80634ba0
	unsigned char unk07 : 1; // 0100 0000 // 806568f8 disable something rendering
	
	unsigned char disable_shockwave : 1; // 0080 0000
	unsigned char unk09 : 1; // 0040 0000 // Maze minigames
	unsigned char unk10 : 1; // 0020 0000 // Only in factory bblast
	unsigned char is_crown : 1; // 0010 0000 // Used in bonus overlay calc
	unsigned char minecart_overlay : 1; // 0008 0000
	unsigned char disable_fall_too_far : 1; // 0004 0000
	unsigned char disable_ledge_grabbing : 1; // 0002 0000 // Vanilla disables it in crowns
	unsigned char pickups_respawn : 1; // 0001 0000 // Oranges/Ammo etc
	
	unsigned char unk16 : 1; // 0000 8000 // Enguarde leaving water something
	unsigned char is_bonus : 1; // 0000 4000 // Used in bonus overlay calc
	unsigned char race_overlay : 1; // 0000 2000
	unsigned char water_overlay : 1; // 0000 1000
	unsigned char disable_damage : 1; // 0000 0800
	unsigned char void_to_parent : 1; // 0000 0400 // Void to parent when deathwarping - only set with crowns
	unsigned char disable_guns_and_oranges : 1; // 0000 0200
	unsigned char force_larger_draw_distance : 1; // 0000 0100
	
	unsigned char overhead_camera : 1; // 0000 0080 // Mazes
	unsigned char far_camera : 1; // 0000 0040 // 8061d25c
	unsigned char force_inline_underwater_camera : 1; // 0000 0020 // force camera to be in line with the player's vertical angle when underwater
	unsigned char unk27 : 1; // 0000 0010 // 80622200 Something camera related
	unsigned char unk28 : 1; // 0000 0008 // floor state something? 8061bc0c
	unsigned char unk29 : 1; // 0000 0004 // Enabled during rabbit race. Checked 80621198
	unsigned char disable_fairy_camera : 1; // 0000 0002
	unsigned char boss_overlay : 1; // 0000 0001

	// 807FBB68
	unsigned char unk32 : 8;
	unsigned char unk40 : 8;
	unsigned char unk48 : 7;
	// Start of used stuff
	unsigned char unk55 : 1; // 0000 0100 // Something chunk related
	
	unsigned char unk56 : 1; // 0000 0080 // camera something?
	unsigned char orangstand_slips : 1; // 0000 0040 // Makes orangstand slip
	unsigned char unk58 : 1; // 0000 0020 // camera something?
	unsigned char is_mini_room : 1; // 0000 0010 // Doubles sprite size, doubles scale of spawned actors?
	unsigned char unk60 : 1; // 0000 0008 // Disable water ripple with something?
	unsigned char unk61 : 1; // 0000 0004 // Something renderlight
	unsigned char is_krool : 1; // 0000 0002
	unsigned char disable_instrument : 1; // 0000 0001
} map_properties_bitfield;

typedef struct text_char_info {
	/* 0x000 */ short x_start;
	/* 0x002 */ unsigned char width;
	/* 0x003 */ unsigned char pad3;
} text_char_info;

typedef struct tuple_s {
	/* 0x000 */ short x;
	/* 0x002 */ short y;
	/* 0x004 */ short z;
} tuple_s;

typedef struct rgba {
	/* 0x000 */ unsigned char red;
	/* 0x001 */ unsigned char green;
	/* 0x002 */ unsigned char blue;
	/* 0x003 */ unsigned char alpha;
} rgba;

typedef struct vtx {
	/* 0x000 */ tuple_s position;
	/* 0x006 */ tuple_s u;
	/* 0x00C */ unsigned int color;
} vtx;

typedef struct letter_data {
	/* 0x000 */ vtx vtx_info[4];
} letter_data;

typedef struct char_spawner_paad {
	/* 0x000 */ char unk_00[0xA];
	/* 0x00A */ short x;
	/* 0x00C */ short y;
	/* 0x00E */ short z;
	/* 0x010 */ char unk_10[0x2C-0x10];
	/* 0x02C */ short counter;
} char_spawner_paad;

typedef struct collision_tree_struct {
	/* 0x000 */ short actor_interaction;
	/* 0x002 */ short target_interaction;
	/* 0x004 */ void* function;
	/* 0x008 */ unsigned char collision_type;
	/* 0x009 */ unsigned char unk9;
	/* 0x00A */ unsigned char force_break;
	/* 0x00B */ unsigned char unkB;
} collision_tree_struct;

typedef struct move_overlay_paad {
	/* 0x000 */ void* upper_text;
	/* 0x004 */ void* lower_text;
	/* 0x008 */ unsigned char opacity;
	/* 0x009 */ unsigned char index;
	/* 0x00A */ char unk_0A[0x10-0xA];
	/* 0x010 */ mtx_item matrix_0;
	/* 0x050 */ mtx_item matrix_1;
	/* 0x090 */ int timer;
	/* 0x094 */ actorData* shop_owner;
} move_overlay_paad;

typedef struct SingleExitStruct {
    /* 0x000 */ short x;
    /* 0x002 */ short y;
    /* 0x004 */ short z;
    /* 0x006 */ unsigned char player_angle;
    /* 0x007 */ unsigned char camera_angle;
    /* 0x008 */ unsigned char autowalk;
    /* 0x009 */ unsigned char size;
} SingleExitStruct;

typedef struct FogMapping {
	/* 0x000 */ rgb rgb;
	/* 0x003 */ unsigned char map_index;
	/* 0x004 */ short fog_entry;
	/* 0x006 */ short fog_cap;
} FogMapping;

typedef struct FogData {
	/* 0x000 */ unsigned char enabled;
	/* 0x001 */ rgb rgb;
	/* 0x004 */ unsigned char opacity;
	/* 0x005 */ char pad5;
	/* 0x006 */ short entry_range;
	/* 0x008 */ short cap_range;
} FogData;