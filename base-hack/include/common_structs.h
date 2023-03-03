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
	/* 0x008 */ char unk_08[0x58-0x8];
	/* 0x058 */ int actorType;
	/* 0x05C */ char unk_5C[0x60-0x5C];
	/* 0x060 */ int obj_props_bitfield;
	/* 0x064 */ int unk_64;
	/* 0x068 */ char unk_68[0x6A-0x68];
	/* 0x06A */ short grounded;
	/* 0x06C */ char unk_6C[0x7C-0x6C];
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
	/* 0x0CD */ char unk_CD[0xE6-0xCD];
	/* 0x0E6 */ short rot_y;
	/* 0x0E8 */ short rot_z;
	/* 0x0EA */ char unk_EA[0x4];
	/* 0x0EE */ short rot_y_copy;
	/* 0x0F0 */ short reward_index;
	/* 0x0F2 */ char unk_F2[0x124-0xF2];
	/* 0x124 */ actor_subdata* data_pointer;
	/* 0x128 */ short shadow_intensity;
	/* 0x12A */ char unk_12A[0x132-0x12A];
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
	/* 0x16D */ char unk_16D[0x174-0x16D];
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
	/* 0x06E */ char unk_6E[0x7C-0x6E];
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
	/* 0x12E */ char unk_12E[0x13C - 0x12E];
	/* 0x13C */ int* collision_queue_pointer;
	/* 0x140 */ bonedata* bone_data;
	/* 0x144 */ char noclip;
	/* 0x145 */ char unk_145[0x147 - 0x145];
	/* 0x147 */ char hand_state;
	/* 0x148 */ char unk_148[0x154 - 0x148];
	/* 0x154 */ unsigned char control_state;
	/* 0x155 */ char control_state_progress;
	/* 0x156 */ char unk_156[0x16A-0x156];
	/* 0x16A */ unsigned char rgb_components[3];
	/* 0x16D */ char unk_16D[0x18A-0x16D];
	/* 0x18A */ short moving_angle;
	/* 0x18C */ char unk_18C[0x1B0-0x18C];
	/* 0x1B0 */ float unk_1B0;
	/* 0x1B4 */ char unk_1B4[0x1B8-0x1B4];
	/* 0x1B8 */ float velocity_cap;
	/* 0x1BC */ char unk_1BC[0x1C8-0x1BC];
	/* 0x1C8 */ short turn_speed;
	/* 0x1CA */ char unk_1CA[0x1CC-0x1CA];
	/* 0x1CC */ short old_tag_state;
	/* 0x1CE */ char unk_1CE[0x1D0-0x1CE];
	/* 0x1D0 */ short ostand_value;
	/* 0x1D2 */ char unk_1D2[0x1E8-0x1D2];
	/* 0x1E8 */ float unk_1E8;
	/* 0x1EC */ char unk_1EC[0x208-0x1EC];
	/* 0x208 */ void* vehicle_actor_pointer;
	/* 0x20C */ char was_gun_out;
	/* 0x20D */ char unk_20D[0x23C - 0x20D];
	/* 0x23C */ short unk_rocketbarrel_value1;
	/* 0x23E */ short unk_rocketbarrel_value2;
	/* 0x240 */ char unk_240[0x248 - 0x240];
	/* 0x248 */ short shockwave_timer;
	/* 0x24A */ char unk_24A[0x254 - 0x24A];
	/* 0x254 */ short invulnerability_timer;
	/* 0x256 */ char unk_256[0x284 - 0x256];
	/* 0x284 */ cameraData* camera_pointer;
	/* 0x288 */ char unk_288[0x2BC - 0x288];
	/* 0x2BC */ floatPos grabPos;
	/* 0x2C8 */ char unk_2C8[0x323 - 0x2C8];
	/* 0x323 */ char unk_rocketbarrel_value3;
	/* 0x324 */ char unk_324[0x328 - 0x324];
	/* 0x328 */ actorData* krool_timer_pointer;
	/* 0x32C */ actorData* held_actor;
	/* 0x330 */ char unk_330[0x340 - 0x330];
	/* 0x340 */ float scale[6];
	/* 0x358 */ char unk_358[0x36C - 0x358];
	/* 0x36C */ char fairy_state;
	/* 0x36D */ char unk_36D[0x36F - 0x36D];
	/* 0x36F */ char new_kong;
	/* 0x370 */ int strong_kong_ostand_bitfield;
	/* 0x374 */ int unk_fairycam_bitfield;
	/* 0x378 */ char unk_374[0x37D-0x378];
	/* 0x37D */ unsigned char rambi_enabled;
	/* 0x37E */ char unk_37E[0x380 - 0x37E];
	/* 0x380 */ short trap_bubble_timer;
	/* 0x382 */ char unk_382[0x3BC - 0x382];
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

typedef struct Controller {
	/* 0x000 */ short Buttons;
	/* 0x002 */ char stickX;
	/* 0x003 */ char stickY;
} Controller;

typedef struct InventoryBase {
	/* 0x000 */ short StandardAmmo;
	/* 0x002 */ short HomingAmmo;
	/* 0x004 */ short Oranges;
	/* 0x006 */ short Crystals;
	/* 0x008 */ short Film;
	/* 0x00A */ char unk0A;
	/* 0x00B */ char Health;
	/* 0x00C */ char Melons;
} InventoryBase;

typedef struct AutowalkData {
	/* 0x000 */ char unk_00[0x12];
	/* 0x012 */ short xPos;
	/* 0x014 */ char unk_14[0x2];
	/* 0x016 */ short zPos;
} AutowalkData;

typedef struct RGB {
	/* 0x000 */ unsigned char red;
	/* 0x001 */ unsigned char green;
	/* 0x002 */ unsigned char blue;
} RGB;

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
	/* 0x010 */ char unk_10[0x2C-0x10];
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
	/* 0x000 */ void* item_count_pointer;
	/* 0x004 */ short visual_item_count;
	/* 0x006 */ short hud_state_timer;
	/* 0x008 */ int x;
	/* 0x00C */ int y;
	/* 0x010 */ float unk_10[4];
	/* 0x020 */ int hud_state;
	/* 0x024 */ char unk_24[0x28-0x24];
	/* 0x028 */ placementData* placement_pointer;
	/* 0x02C */ char unk_2C[0x30-0x2C];
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
	/* 0x004 */ char unk_04[0x14-0x4];
	/* 0x014 */ float unk_14;
	/* 0x018 */ char unk_18[0x38-0x18];
	/* 0x038 */ int unk_38;
	/* 0x03C */ char unk_3C[0x44-0x3C];
	/* 0x044 */ unsigned short timer;
	/* 0x046 */ char unk_46[0x48-0x46];
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
	/* 0x06E */ char unk_6E[0x70-0x6E];
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
	/* 0x010 */ char unk_10[0x50-0x10];
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
	unsigned char remove_cutscenes : 1;
	unsigned char fast_picture : 1;
	unsigned char aztec_lobby_bonus : 1;
	unsigned char dance_skip : 1;
	unsigned char fast_boot : 1;
	unsigned char fast_transform : 1;
	unsigned char ammo_swap : 1;
	unsigned char cb_indicator : 1;
	unsigned char galleon_star : 1;
	unsigned char vanilla_fixes : 1;
	unsigned char textbox_hold : 1;
	unsigned char caves_kosha_dead : 1;
	unsigned char rambi_enguarde_pickup : 1;
	unsigned char hud_bp_multibunch : 1;
	unsigned char homing_balloons : 1;
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
	/* 0x00C */ int unk0;
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
	/* 0x000 */ char unk_0[0x40];
} mtx_item;

typedef struct actor_behaviour_def {
    /* 0x000 */ short actor_type;
    /* 0x002 */ short model;
    /* 0x004 */ char unk4[8];
    /* 0x00C */ void* code;
    /* 0x010 */ void* unk10;
    /* 0x014 */ char str[0x1C];
} actor_behaviour_def;

typedef struct arbitrary_overlay {
	/* 0x000 */ unsigned char type;
	/* 0x001 */ unsigned char kong;
	/* 0x002 */ short flag;
} arbitrary_overlay;

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
	/* 0x000 */ char unk0[0x340];
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