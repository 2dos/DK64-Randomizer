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

typedef struct actorData {
	/* 0x000 */ void* model;
	/* 0x004 */ renderingParamsData* render;
	/* 0x008 */ char unk_08[0x58-0x8];
	/* 0x058 */ int actorType;
	/* 0x05C */ char unk_5C[0x60-0x5C];
	/* 0x060 */ int obj_props_bitfield;
	/* 0x064 */ char unk_64[0x7C-0x64];
	/* 0x07C */ float xPos;
	/* 0x080 */ float yPos;
	/* 0x084 */ float zPos;
	/* 0x088 */ char unk_80[0xB8-0x88];
	/* 0x0B8 */ float hSpeed;
	/* 0x0BC */ char unk_BC[0xE8-0xBC];
	/* 0x0E8 */ short rot_z;
	/* 0x0EA */ char unk_EA[0x128-0xEA];
	/* 0x128 */ short shadow_intensity;
	/* 0x12A */ char unk_12A[0x144-0x12A];
	/* 0x144 */ char noclip_byte;
	/* 0x145 */ char unk_145[0x154-0x145];
	/* 0x154 */ char control_state;
	/* 0x155 */ char control_state_progress;
	/* 0x156 */ char unk_156[0x16A-0x156];
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

typedef struct bone_array {
	/* 0x000 */ char unk_00[0x58];
	/* 0x058 */ short xPos;
	/* 0x05A */ short yPos;
	/* 0x05C */ short zPos;
} bone_array;

typedef struct rendering_params {
	/* 0x000 */ char unk_00[0x14];
	/* 0x014 */ bone_array* bone_array1;
	/* 0x018 */ bone_array* bone_array2;
	/* 0x01C */ char unk_1C[0x64-0x1C];
	/* 0x064 */ short anim_idx;
	/* 0x066 */ char unk_66[0x68-0x66];
	/* 0x068 */ int anim_ptr;
} rendering_params;

typedef struct bonepos {
	/* 0x000 */ char unk_00[0x0C - 0x00];
	/* 0x00C */ int boneX;
	/* 0x010 */ int boneY;
	/* 0x014 */ int boneZ;
	/* 0x018 */ void* unk_ptr;
	/* 0x01C */ void* next_bone;
} bonepos;

typedef struct bonedata {
	/* 0x000 */ char unk_00[0x84 - 0x00];
	/* 0x084 */ int timer;
	/* 0x088 */ char unk_88[0x90 - 0x88];
	/* 0x090 */ bonepos* bone_positions;
} bonedata;

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
	/* 0x0A8 */ char unk_A8[0xB8-0xA8];
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
	/* 0x10E */ char unk_10E[0x110-0x10E];
	/* 0x110 */ char touching_object;
	/* 0x111 */ char unk_111[0x128 - 0x111];
	/* 0x128 */ short strong_kong_value;
	/* 0x12A */ char unk_12A[2];
	/* 0x12C */ short chunk;
	/* 0x12E */ char unk_12E[0x13C - 0x12E];
	/* 0x13C */ int* collision_queue_pointer;
	/* 0x140 */ bonedata* bone_data;
	/* 0x144 */ char unk_140[0x147 - 0x144];
	/* 0x147 */ char hand_state;
	/* 0x148 */ char unk_148[0x154 - 0x148];
	/* 0x154 */ char control_state;
	/* 0x155 */ char control_state_progress;
	/* 0x156 */ char unk_156[0x16A-0x156];
	/* 0x16A */ unsigned char rgb_components[3];
	/* 0x16D */ char unk_16D[0x18A-0x16D];
	/* 0x18A */ short moving_angle;
	/* 0x18C */ char unk_18C[0x1B8-0x18C];
	/* 0x1B8 */ float velocity_cap;
	/* 0x1BC */ char unk_1BC[0x1D0-0x1BC];
	/* 0x1D0 */ short ostand_value;
	/* 0x1D2 */ char unk_1D2[0x208-0x1D2];
	/* 0x208 */ void* vehicle_actor_pointer;
	/* 0x20C */ char was_gun_out;
	/* 0x20D */ char unk_20D[0x23C - 0x20D];
	/* 0x23C */ short unk_rocketbarrel_value1;
	/* 0x23E */ short unk_rocketbarrel_value2;
	/* 0x240 */ char unk_240[0x284 - 0x240];
	/* 0x284 */ cameraData* camera_pointer;
	/* 0x288 */ char unk_288[0x2BC - 0x288];
	/* 0x2BC */ floatPos grabPos;
	/* 0x2C8 */ char unk_2C8[0x323 - 0x2C8];
	/* 0x323 */ char unk_rocketbarrel_value3;
	/* 0x324 */ char unk_324[0x328 - 0x324];
	/* 0x328 */ actorData* krool_timer_pointer;
	/* 0x32C */ actorData* held_actor;
	/* 0x330 */ char unk_330[0x36C - 0x330];
	/* 0x36C */ char fairy_state;
	/* 0x36D */ char unk_36D[0x36F - 0x36D];
	/* 0x36F */ char new_kong;
	/* 0x370 */ int strong_kong_ostand_bitfield;
	/* 0x374 */ char unk_374[0x37D-0x374];
	/* 0x37D */ unsigned char rambi_enabled;
	/* 0x37E */ char unk_37E[0x3BE - 0x37E];
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
	/* 0x000 */ char unk_00[0x210];
	/* 0x210 */ floatPos cameraPositions[4];
	/* 0x240 */ char unk_21C[0x284-0x240];
	/* 0x284 */ float near;
	/* 0x288 */ char unk_288[0x290-0x288];
	/* 0x290 */ short chunk;
	/* 0x292 */ char unk_292[0x29C-0x292];
	/* 0x29C */ short action_type;
} SwapObjectData;

typedef struct ModelTwoData {
	/* 0x000 */ float xPos;
	/* 0x004 */ float yPos;
	/* 0x008 */ float zPos;
	/* 0x00C */ char unk_0C[0x20-0xC];
	/* 0x020 */ void* model_pointer;
	/* 0x024 */ void* dl_pointer;
	/* 0x028 */ char unk_28[0x7C-0x28];
	/* 0x07C */ void* behaviour_pointer;
	/* 0x080 */ char unk_80[0x84-0x80];
	/* 0x084 */ short object_type;
	/* 0x086 */ char unk_86[0x2];
	/* 0x088 */ short sub_id;
	/* 0x08A */ short object_id;
	/* 0x08C */ char unk_8C[0x4];
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

typedef struct cutsceneType {
	/* 0x000 */ char unk_00[0xD0];
	/* 0x0D0 */ cutsceneInfo* cutscene_databank;
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
	/* 0x010 */ char unk_10[0x40-0x10];
	/* 0x040 */ float barrel_resolved;
	/* 0x044 */ void* tied_actor;
	/* 0x048 */ char unk_48[0x5A-0x48];
	/* 0x05A */ short id;
	/* 0x05C */ char unk_5C[0x64-0x5C];
	/* 0x064 */ void* previous_spawner;
	/* 0x068 */ void* next_spawner;
} actorSpawnerData;

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

typedef enum console {
    NONE,
    N64,
    WIIU,
    EMULATOR,
} console;

typedef enum data_indexes {
	Music_MIDI,
	Map_Geometry,
	Map_Walls,
	Map_Floors,
	ModelTwo_Geometry,
	Actor_Geometry,
	Unk06,
	Textures_Uncompressed,
	Cutscenes,
	Map_Setups,
	Map_Object_Scripts,
	Animations,
	Text,
	Unk0D,
	Textures,
	Map_Paths,
	Map_Character_Spawners,
	Unk11,
	Map_Loading_Zones,
	Unk13,
	Unk14,
	Map_Autowalks,
	Unk16,
	Map_Exits,
	Map_Race_Checkpoints,
	Textures_2,
	Uncompressed_File_Sizes,
	Unk1B,
	Unk1C,
	Unk1D,
	Unk1E,
	Unk1F,
	Unk20,
} data_indexes;

typedef enum load_modes {
	SAVESTATE,
	MAPWARP,
} load_modes;

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

typedef struct hud_element {
	/* 0x000 */ void* item_count_pointer;
	/* 0x004 */ short visual_item_count;
	/* 0x006 */ short hud_state_timer;
	/* 0x008 */ int x;
	/* 0x00C */ int y;
	/* 0x010 */ float unk_10[4];
	/* 0x020 */ int hud_state;
	/* 0x024 */ char unk_24[0xC];
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

typedef enum codecs {
    IA4,
    IA8,
    RGBA16,
    RGBA32,
} codecs;

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
	/* 0x004 */ short price;
} purchase_struct;

typedef struct race_exit_struct {
	/* 0x000 */ int race_map;
	/* 0x004 */ int container_map;
	/* 0x008 */ int container_exit;
} race_exit_struct;

typedef struct enemy_drop_struct {
	/* 0x000 */ short source_object_type;
	/* 0x002 */ short dropped_object_type;
	/* 0x004 */ unsigned char drop_music;
	/* 0x005 */ unsigned char drop_count;
} enemy_drop_struct;

typedef enum collision_types {
	/* 0x000 */ COLLISION_BBLAST,
	/* 0x001 */ COLLISION_UNKNOWN_1,
	/* 0x002 */ COLLISION_SIMIAN_SPRING,
	/* 0x003 */ COLLISION_MONKEYPORT_WARP,
	/* 0x004 */ COLLISION_GORILLA_GONE,
	/* 0x005 */ COLLISION_BANANAPORT,
	/* 0x006 */ COLLISION_BABOON_BALLOON,
	/* 0x007 */ COLLISION_BATTLE_CROWN,
	/* 0x008 */ COLLISION_UNKNOWN_8,
	/* 0x009 */ COLLISION_MULTI_BANANAPORT,
	/* 0x00A */ COLLISION_MAPWARP,
} collision_types;

typedef struct fileExtraStorage {
	/* 0x000 */ unsigned char location_sss_purchased; // 0lll 0pss. l = level (0-7), p = purchased (0-1), s = shop (0-2. Cranky, Funky, Candy)
	/* 0x001 */ unsigned char location_ab1_purchased;
	/* 0x002 */ unsigned char location_ug1_purchased;
	/* 0x003 */ unsigned char location_mln_purchased;
} fileExtraStorage;

typedef struct settingsData {
	/* 0x000 */ fileExtraStorage file_extra[3];
} settingsData;

typedef struct behaviour_data {
	/* 0x000 */ char unk_00[0x38];
	/* 0x038 */ int unk_38;
	/* 0x03C */ char unk_3C[0x44-0x3C];
	/* 0x044 */ unsigned short timer;
	/* 0x046 */ char unk_46[0x48-0x46];
	/* 0x048 */ unsigned char current_state;
	/* 0x049 */ char counter;
	/* 0x04A */ char unk_4A[0x4B-0x4A];
	/* 0x04B */ unsigned char next_state;
	/* 0x04C */ char unk_4C[0x54-0x4C];
	/* 0x054 */ char pause_state;
	/* 0x055 */ char unk_55[0x58-0x55];
	/* 0x058 */ int distance_cap;
	/* 0x05C */ char switch_pressed;
	/* 0x05D */ char unk_5D;
	/* 0x05E */ unsigned short contact_actor_type;
	/* 0x060 */ char unk_60;
	/* 0x061 */ char unk_61;
	/* 0x062 */ unsigned short unk_62;
	/* 0x064 */ char unk_64[0x66-0x64];
	/* 0x066 */ unsigned char unk_66;
	/* 0x067 */ char unk_67[0x70-0x67];
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
	/* 0x000 */ char unk_00[4];
	/* 0x004 */ short price;
	/* 0x006 */ char unk_06[0xB-0x6];
	/* 0x00B */ char purchase_type;
	/* 0x00C */ char unk_0C;
	/* 0x00D */ unsigned char state;
	/* 0x00E */ char unk_0E[0x10-0x0E];
	/* 0x010 */ unsigned char melons;
	/* 0x011 */ unsigned char purchase_value;
} shop_paad;