#include "../include/common.h"

const short kong_flags[] = {FLAG_KONG_DK,FLAG_KONG_DIDDY,FLAG_KONG_LANKY,FLAG_KONG_TINY,FLAG_KONG_CHUNKY};
const short normal_key_flags[] = {
	FLAG_KEYHAVE_KEY1,
	FLAG_KEYHAVE_KEY2,
	FLAG_KEYHAVE_KEY3,
	FLAG_KEYHAVE_KEY4,
	FLAG_KEYHAVE_KEY5,
	FLAG_KEYHAVE_KEY6,
	FLAG_KEYHAVE_KEY7,
	FLAG_KEYHAVE_KEY8
};
const unsigned short slam_flags[] = {FLAG_ITEM_SLAM_0, FLAG_ITEM_SLAM_1, FLAG_SHOPMOVE_SLAM_0, FLAG_SHOPMOVE_SLAM_1};
const unsigned short belt_flags[] = {FLAG_ITEM_BELT_0, FLAG_ITEM_BELT_1, FLAG_SHOPMOVE_BELT_0, FLAG_SHOPMOVE_BELT_1};
const unsigned short instrument_flags[] = {FLAG_ITEM_INS_0, FLAG_ITEM_INS_1, FLAG_ITEM_INS_2, FLAG_SHOPMOVE_INS_0, FLAG_SHOPMOVE_INS_1, FLAG_SHOPMOVE_INS_2};
const rgb colorblind_colors[15] = {
    // Protan
    {.red=0x27, .green=0x27, .blue=0x27}, // DK
    {.red=0x00, .green=0x72, .blue=0xFF}, // Diddy
    {.red=0x76, .green=0x6D, .blue=0x5A}, // Lanky
    {.red=0xFF, .green=0xFF, .blue=0xFF}, // Tiny
    {.red=0xFD, .green=0xE4, .blue=0x00}, // Chunky
    // Deutan
    {.red=0x27, .green=0x27, .blue=0x27}, // DK
    {.red=0x31, .green=0x8D, .blue=0xFF}, // Diddy
    {.red=0x7F, .green=0x6D, .blue=0x59}, // Lanky
    {.red=0xFF, .green=0xFF, .blue=0xFF}, // Tiny
    {.red=0xE3, .green=0xA9, .blue=0x00}, // Chunky
    // Tritan
    {.red=0x27, .green=0x27, .blue=0x27}, // DK
    {.red=0xC7, .green=0x20, .blue=0x20}, // Diddy
    {.red=0x13, .green=0xC4, .blue=0xD8}, // Lanky
    {.red=0xFF, .green=0xFF, .blue=0xFF}, // Tiny
    {.red=0xFF, .green=0xA4, .blue=0xA4}, // Chunky
};
const unsigned char crown_maps[] = {
	MAP_BATTLEARENA_BEAVERBRAWL,
	MAP_BATTLEARENA_KRITTERKARNAGE,
	MAP_BATTLEARENA_ARENAAMBUSH,
	MAP_BATTLEARENA_MOREKRITTERKARNAGE,
	MAP_BATTLEARENA_KAMIKAZEKREMLINGS,
	MAP_BATTLEARENA_PLINTHPANIC,
	MAP_BATTLEARENA_PINNACLEPALAVER,
	MAP_BATTLEARENA_FORESTFRACAS,
	MAP_BATTLEARENA_SHOCKWAVESHOWDOWN,
	MAP_BATTLEARENA_BISHBASHBRAWL
};
const unsigned char regular_boss_maps[] = {
	MAP_JAPESDILLO,
    MAP_AZTECDOGADON,
    MAP_FACTORYJACK,
    MAP_GALLEONPUFFTOSS,
    MAP_FUNGIDOGADON,
    MAP_CAVESDILLO,
    MAP_CASTLEKUTOUT
};
static const map_bitfield minigame_maps_btf = {
    // Bitfield on whether a map is a minigame map
	.test_map = 0,
    .funkys_store = 0,
    .dk_arcade = 1,
    .k_rool_barrel_lankys_maze = 1,
    .jungle_japes_mountain = 0,
    .crankys_lab = 0,
    .jungle_japes_minecart = 0,
    .jungle_japes = 0,
    .jungle_japes_army_dillo = 0,
    .jetpac = 1,
    .kremling_kosh_very_easy = 1,
    .stealthy_snoop_normal_no_logo = 1,
    .jungle_japes_shell = 0,
    .jungle_japes_lankys_cave = 0,
    .angry_aztec_beetle_race = 0,
    .snides_hq = 0,
    .angry_aztec_tinys_temple = 0,
    .hideout_helm = 0,
    .teetering_turtle_trouble_very_easy = 1,
    .angry_aztec_five_door_temple_dk = 0,
    .angry_aztec_llama_temple = 0,
    .angry_aztec_five_door_temple_diddy = 0,
    .angry_aztec_five_door_temple_tiny = 0,
    .angry_aztec_five_door_temple_lanky = 0,
    .angry_aztec_five_door_temple_chunky = 0,
    .candys_music_shop = 0,
    .frantic_factory = 0,
    .frantic_factory_car_race = 0,
    .hideout_helm_level_intros_game_over = 0,
    .frantic_factory_power_shed = 0,
    .gloomy_galleon = 0,
    .gloomy_galleon_k_rools_ship = 0,
    .batty_barrel_bandit_very_easy = 1,
    .jungle_japes_chunkys_cave = 0,
    .dk_isles_overworld = 0,
    .k_rool_barrel_dks_target_game = 1,
    .frantic_factory_crusher_room = 0,
    .jungle_japes_barrel_blast = 0,
    .angry_aztec = 0,
    .gloomy_galleon_seal_race = 0,
    .nintendo_logo = 0,
    .angry_aztec_barrel_blast = 0,
    .troff_n_scoff = 0,
    .gloomy_galleon_shipwreck_diddy_lanky_chunky = 0,
    .gloomy_galleon_treasure_chest = 0,
    .gloomy_galleon_mermaid = 0,
    .gloomy_galleon_shipwreck_dk_tiny = 0,
    .gloomy_galleon_shipwreck_lanky_tiny = 0,
    .fungi_forest = 0,
    .gloomy_galleon_lighthouse = 0,
    .k_rool_barrel_tinys_mushroom_game = 1,
    .gloomy_galleon_mechanical_fish = 0,
    .fungi_forest_ant_hill = 0,
    .battle_arena_beaver_brawl = 0,
    .gloomy_galleon_barrel_blast = 0,
    .fungi_forest_minecart = 0,
    .fungi_forest_diddys_barn = 0,
    .fungi_forest_diddys_attic = 0,
    .fungi_forest_lankys_attic = 0,
    .fungi_forest_dks_barn = 0,
    .fungi_forest_spider = 0,
    .fungi_forest_front_part_of_mill = 0,
    .fungi_forest_rear_part_of_mill = 0,
    .fungi_forest_mushroom_puzzle = 0,
    .fungi_forest_giant_mushroom = 0,
    .stealthy_snoop_normal = 1,
    .mad_maze_maul_hard = 1,
    .stash_snatch_normal = 1,
    .mad_maze_maul_easy = 1,
    .mad_maze_maul_normal = 1,
    .fungi_forest_mushroom_leap = 0,
    .fungi_forest_shooting_game = 0,
    .crystal_caves = 0,
    .battle_arena_kritter_karnage = 0,
    .stash_snatch_easy = 1,
    .stash_snatch_hard = 1,
    .dk_rap = 0,
    .minecart_mayhem_easy = 1,
    .busy_barrel_barrage_easy = 1,
    .busy_barrel_barrage_normal = 1,
    .main_menu = 0,
    .title_screen_not_for_resale_version = 0,
    .crystal_caves_beetle_race = 0,
    .fungi_forest_dogadon = 0,
    .crystal_caves_igloo_tiny = 0,
    .crystal_caves_igloo_lanky = 0,
    .crystal_caves_igloo_dk = 0,
    .creepy_castle = 0,
    .creepy_castle_ballroom = 0,
    .crystal_caves_rotating_room = 0,
    .crystal_caves_shack_chunky = 0,
    .crystal_caves_shack_dk = 0,
    .crystal_caves_shack_diddy_middle_part = 0,
    .crystal_caves_shack_tiny = 0,
    .crystal_caves_lankys_hut = 0,
    .crystal_caves_igloo_chunky = 0,
    .splish_splash_salvage_normal = 1,
    .k_lumsy = 0,
    .crystal_caves_ice_castle = 0,
    .speedy_swing_sortie_easy = 1,
    .crystal_caves_igloo_diddy = 0,
    .krazy_kong_klamour_easy = 1,
    .big_bug_bash_very_easy = 1,
    .searchlight_seek_very_easy = 1,
    .beaver_bother_easy = 1,
    .creepy_castle_tower = 0,
    .creepy_castle_minecart = 0,
    .kong_battle_battle_arena = 0,
    .creepy_castle_crypt_lanky_tiny = 0,
    .kong_battle_arena_1 = 0,
    .frantic_factory_barrel_blast = 0,
    .gloomy_galleon_pufftoss = 0,
    .creepy_castle_crypt_dk_diddy_chunky = 0,
    .creepy_castle_museum = 0,
    .creepy_castle_library = 0,
    .kremling_kosh_easy = 1,
    .kremling_kosh_normal = 1,
    .kremling_kosh_hard = 1,
    .teetering_turtle_trouble_easy = 1,
    .teetering_turtle_trouble_normal = 1,
    .teetering_turtle_trouble_hard = 1,
    .batty_barrel_bandit_easy = 1,
    .batty_barrel_bandit_normal = 1,
    .batty_barrel_bandit_hard = 1,
    .mad_maze_maul_insane = 1,
    .stash_snatch_insane = 1,
    .stealthy_snoop_very_easy = 1,
    .stealthy_snoop_easy = 1,
    .stealthy_snoop_hard = 1,
    .minecart_mayhem_normal = 1,
    .minecart_mayhem_hard = 1,
    .busy_barrel_barrage_hard = 1,
    .splish_splash_salvage_hard = 1,
    .splish_splash_salvage_easy = 1,
    .speedy_swing_sortie_normal = 1,
    .speedy_swing_sortie_hard = 1,
    .beaver_bother_normal = 1,
    .beaver_bother_hard = 1,
    .searchlight_seek_easy = 1,
    .searchlight_seek_normal = 1,
    .searchlight_seek_hard = 1,
    .krazy_kong_klamour_normal = 1,
    .krazy_kong_klamour_hard = 1,
    .krazy_kong_klamour_insane = 1,
    .peril_path_panic_very_easy = 1,
    .peril_path_panic_easy = 1,
    .peril_path_panic_normal = 1,
    .peril_path_panic_hard = 1,
    .big_bug_bash_easy = 1,
    .big_bug_bash_normal = 1,
    .big_bug_bash_hard = 1,
    .creepy_castle_dungeon = 0,
    .hideout_helm_intro_story = 0,
    .dk_isles_dk_theatre = 0,
    .frantic_factory_mad_jack = 0,
    .battle_arena_arena_ambush = 0,
    .battle_arena_more_kritter_karnage = 0,
    .battle_arena_forest_fracas = 0,
    .battle_arena_bish_bash_brawl = 0,
    .battle_arena_kamikaze_kremlings = 0,
    .battle_arena_plinth_panic = 0,
    .battle_arena_pinnacle_palaver = 0,
    .battle_arena_shockwave_showdown = 0,
    .creepy_castle_basement = 0,
    .creepy_castle_tree = 0,
    .k_rool_barrel_diddys_kremling_game = 1,
    .creepy_castle_chunkys_toolshed = 0,
    .creepy_castle_trash_can = 0,
    .creepy_castle_greenhouse = 0,
    .jungle_japes_lobby = 0,
    .hideout_helm_lobby = 0,
    .dks_house = 0,
    .rock_intro_story = 0,
    .angry_aztec_lobby = 0,
    .gloomy_galleon_lobby = 0,
    .frantic_factory_lobby = 0,
    .training_grounds = 0,
    .dive_barrel = 0,
    .fungi_forest_lobby = 0,
    .gloomy_galleon_submarine = 0,
    .orange_barrel = 0,
    .barrel_barrel = 0,
    .vine_barrel = 0,
    .creepy_castle_crypt = 0,
    .enguarde_arena = 0,
    .creepy_castle_car_race = 0,
    .crystal_caves_barrel_blast = 0,
    .creepy_castle_barrel_blast = 0,
    .fungi_forest_barrel_blast = 0,
    .fairy_island = 0,
    .kong_battle_arena_2 = 0,
    .rambi_arena = 0,
    .kong_battle_arena_3 = 0,
    .creepy_castle_lobby = 0,
    .crystal_caves_lobby = 0,
    .dk_isles_snides_room = 0,
    .crystal_caves_army_dillo = 0,
    .angry_aztec_dogadon = 0,
    .training_grounds_end_sequence = 0,
    .creepy_castle_king_kut_out = 0,
    .crystal_caves_shack_diddy_upper_part = 0,
    .k_rool_barrel_diddys_rocketbarrel_game = 1,
    .k_rool_barrel_lankys_shooting_game = 1,
    .k_rool_fight_dk_phase = 0,
    .k_rool_fight_diddy_phase = 0,
    .k_rool_fight_lanky_phase = 0,
    .k_rool_fight_tiny_phase = 0,
    .k_rool_fight_chunky_phase = 0,
    .bloopers_ending = 0,
    .k_rool_barrel_chunkys_hidden_kremling_game = 1,
    .k_rool_barrel_tinys_pony_tail_twirl_game = 1,
    .k_rool_barrel_chunkys_shooting_game = 1,
    .k_rool_barrel_dks_rambi_game = 1,
    .k_lumsy_ending = 0,
    .k_rools_shoe = 0,
    .k_rools_arena = 0,
};

int inMinigame(maps map) {
	int offset = map >> 3;
    int check = map % 8;
    return *(unsigned char*)((unsigned char*)(&minigame_maps_btf) + offset) & (0x80 >> check);
}

void playSFX(short sfxIndex) {
	playSound(sfxIndex,0x7FFF,0x427C0000,0x3F800000,0,0);
}

void setPermFlag(short flagIndex) {
	setFlag(flagIndex,1,FLAGTYPE_PERMANENT);
}

int convertIDToIndex(short obj_index) {
	int _count = ObjectModel2Count;
	int index = -1;
	int* m2location = (int*)ObjectModel2Pointer;
	for (int i = 0; i < _count; i++) {
		ModelTwoData* _object = getObjectArrayAddr(m2location,0x90,i);
		if (_object->object_id == obj_index) {
			index = i;
			return i;
		}
	}
	return index;
}

int convertSubIDToIndex(short obj_index) {
	int _count = ObjectModel2Count;
	int index = -1;
	int* m2location = (int*)ObjectModel2Pointer;
	for (int i = 0; i < _count; i++) {
		ModelTwoData* _object = getObjectArrayAddr(m2location,0x90,i);
		if (_object->sub_id == obj_index) {
			index = i;
			return i;
		}
	}
	return index;
}

int isFlagInRange(int test_flag, int start_flag, int count) {
	if (test_flag >= start_flag) {
		return test_flag < (start_flag + count);
	}
	return 0;
}


void* findActorWithType(int search_actor_type) {
	for (int i = 0; i < ActorCount; i++) {
		actorData* _actor_ = (actorData*)ActorArray[i];
		if (_actor_->actorType == search_actor_type) {
			return _actor_;
		}
	}
	return 0;
}

int isRDRAM(void* address) {
	if (((int)address >= 0x80000000) && ((int)address < 0x80800000)) {
		return 1;
	}
	return 0;
}

void setWarpPosition(float x, float y, float z) {
	PositionWarpInfo.xPos = x;
	PositionWarpInfo.yPos = y;
	PositionWarpInfo.zPos = z;
	PositionFloatWarps[0] = x;
	PositionFloatWarps[1] = y;
	PositionFloatWarps[2] = z;
	PositionWarpBitfield = PositionWarpBitfield | 1;
}

void customHideHUD(void) {
	for (int i = 0; i < 0xE; i++) {
		HUD->item[i].hud_state = 0;
	}
}

void createCollisionObjInstance(collision_types subtype, int map, int exit) {
	createCollision(0,Player,subtype,map,exit,collisionPos[0],collisionPos[1],collisionPos[2]);
}

void changeCharSpawnerFlag(maps map, int spawner_id, int new_flag) {
	for (int i = 0; i < 0x1F; i++) {
		if (charspawnerflags[i].map == map) {
			if (charspawnerflags[i].spawner_id == spawner_id) {
				charspawnerflags[i].tied_flag = new_flag;
			}
		}
	}
}

void resetMapContainer(void) {
	resetMap();
	for (int i = 0; i < 0x12; i++) {
		SubmapData[i].slot_populated = 0;
	}
}

static const unsigned char dk_portal_maps[] = {
	MAP_JAPES,
	MAP_AZTEC,
	MAP_FACTORY,
	MAP_GALLEON,
	MAP_FUNGI,
	MAP_CAVES,
	MAP_CASTLE,
	MAP_JAPESLOBBY,
	MAP_AZTECLOBBY,
	MAP_FACTORYLOBBY,
	MAP_GALLEONLOBBY,
	MAP_FUNGILOBBY,
	MAP_CAVESLOBBY,
	MAP_CASTLELOBBY
};
void correctDKPortal(void) {
	int is_portal_map = 0;
	for (int i = 0; i < sizeof(dk_portal_maps); i++) {
		if (dk_portal_maps[i] == CurrentMap) {
			is_portal_map = 1;
		}
	}
	if (is_portal_map) {
		int portal_exit = isLobby(CurrentMap);
		int exit = DestExit;
		int portal_state = 2;
		if (portal_exit == exit) {
			portal_state = 0;
		}
		if ((CurrentMap == MAP_JAPES) && (exit == 15)) {
			portal_state = 0;
		}
		int _count = ObjectModel2Count;
		int* m2location = (int*)ObjectModel2Pointer;
		for (int i = 0; i < _count; i++) {
			ModelTwoData* _object = getObjectArrayAddr(m2location,0x90,i);
			if (_object->object_type == 0x2AD) {
				behaviour_data* behav = _object->behaviour_pointer;
				if (behav) {
					behav->current_state = portal_state;
					//behav->next_state = portal_state;
				}
			}
		}
	}
}

void alterGBKong(maps map, int id, int new_kong) {
	for (int i = 0; i < 113; i++) {
		if (GBDictionary[i].map == map) {
			if (GBDictionary[i].model2_id == id) {
				GBDictionary[i].intended_kong_actor = new_kong + 2;
			}
		}
	}
}

int getCenter(int style, char* str) {
	return (screenCenterX + 100 - (getCenterOffset(style,str))) * 0.5f;
}

int getLo(void* addr) {
    return ((int)addr) & 0xFFFF;
}

int getHi(void* addr) {
    int addr_0 = (int)addr;
    int hi = (addr_0 >> 16) & 0xFFFF;
    int lo = getLo(addr);
    if (lo & 0x8000) {
        hi += 1;
    }
    return hi;
}

void cancelCutscene(int enable_movement) {
	if ((TBVoidByte & 2) == 0) {
		if (CutsceneActive) {
			if (CutsceneTypePointer) {
				if (CutsceneTypePointer->cutscene_databank) {
					int* databank = (int *)(CutsceneTypePointer->cutscene_databank);
					short cam_state = *(short *)(getObjectArrayAddr(databank,0xC,CutsceneIndex));
					// short cam_state = *( short*)(cs_databank + (0xC * CutsceneIndex));
					CurrentCameraState = cam_state;
					PreviousCameraState = cam_state;
					CameraStateChangeTimer = 0;
					if ((Player) && (enable_movement)) {
						Player->control_state = 0xC;
					}
				}
			}
		}
	}
}

void modifyCutscenePoint(int bank, int cutscene, int point, int new_item) {
	if (CutsceneBanks[bank].cutscene_databank) {
		void* databank = CutsceneBanks[bank].cutscene_databank;
		cutscene_item_data* data = (cutscene_item_data*)getObjectArrayAddr(databank,0xC,cutscene);
		short* write_spot = (short*)getObjectArrayAddr(data->point_array,2,point);
		*(short*)write_spot = new_item;
	}
}

void modifyCutsceneItem(int bank, int item, int new_param1, int new_param2, int new_param3) {
	if (CutsceneBanks[bank].cutscene_funcbank) {
		void* funcbank = CutsceneBanks[bank].cutscene_funcbank;
		cutscene_item* data = (cutscene_item*)getObjectArrayAddr(funcbank,0x14,item);
		data->command = 0xD;
		data->params[0] = new_param1;
		data->params[1] = new_param2;
		data->params[2] = new_param3;
	}
}

void modifyCutscenePanPoint(int bank, int item, int point_index, int x, int y, int z, int rot0, int rot1, int rot2, int zoom, int roll) {
	if (CutsceneBanks[bank].cutscene_funcbank) {
		cutscene_pan_item* funcbank = (cutscene_pan_item*)CutsceneBanks[bank].cutscene_funcbank;
		cutscene_pan_item* cs_item = (cutscene_pan_item*)&funcbank[item];
		pan_data* data = (pan_data*)&cs_item->pan_content[point_index];
		data->x = x;
		data->y = y;
		data->z = z;
		data->rot_data[0] = rot0;
		data->rot_data[1] = rot1;
		data->rot_data[2] = rot2;
		data->zoom = zoom;
		data->roll = roll;
	}
}

void modifyCutscenePointTime(int bank, int cutscene, int point, int new_time) {
	cutscene_item_data* databank = CutsceneBanks[bank].cutscene_databank;
	cutscene_item_data* data = (cutscene_item_data*)&databank[cutscene];
	if (data) {
		short* write_spot = (short*)&data->length_array[point];
		if (write_spot) {
			*(short*)write_spot = new_time;
		}
	}
}

void modifyCutscenePointCount(int bank, int cutscene, int point_count) {
	cutscene_item_data* databank = CutsceneBanks[bank].cutscene_databank;
	cutscene_item_data* data = (cutscene_item_data*)&databank[cutscene];
	if (data) {
		data->num_points = point_count;
	}
}

void createCutscene(int bank, int cutscene, int point_count) {
	if (cutscene < CutsceneBanks[bank].cutscene_count) {
		cutscene_item_data* databank = CutsceneBanks[bank].cutscene_databank;
		cutscene_item_data* data = (cutscene_item_data*)&databank[cutscene];
		if (data) {
			data->num_points = point_count;
			data->length_array = dk_malloc(point_count * 2);
			data->point_array = dk_malloc(point_count * 2);
			data->unk_02 = 0;
		}
	}
	// Else - Can't create cutscene
}

int getWrinklyLevelIndex(void) {
	return getWorld(CurrentMap, 0);
}

int getKeyFlag(int index) {
    if ((Rando.level_order_rando_on) && (index < 7)) {
        return Rando.key_flags[index];
    } else {
        return normal_key_flags[index];
    }
}

int getKongFlag(int kong_index) {
	if (kong_index < 0) {
		return 0;
	}
	return kong_flags[kong_index];
}

void initActor(int actor_index, int is_custom, void* func, int master_type, int health, int damage_given, int initial_interactions, int base) {
	if (is_custom) {
		actor_index = CUSTOM_ACTORS_START + actor_index;
	}
	actor_functions[actor_index] = func;
	actor_master_types[actor_index] = master_type;
	actor_health_damage[actor_index].init_health = health;
	actor_health_damage[actor_index].damage_applied = damage_given;
	actor_interactions[actor_index] = initial_interactions;
	actor_extra_data_sizes[actor_index] = actor_extra_data_sizes[base];
	actor_collisions[actor_index].collision_info = actor_collisions[base].collision_info;
	actor_collisions[actor_index].unk_4 = actor_collisions[base].unk_4;
}

sprite_data_struct bean_sprite = {
	.unk0 = 0xC4,
	.images_per_frame_horizontal = 1,
	.images_per_frame_vertical = 1,
	.codec = 2,
	.unk8 = -1,
	.table = 1,
	.width = 64,
	.height = 32,
	.image_count = 1,
	.images = {6020},
};

sprite_data_struct pearl_sprite = {
	.unk0 = 0xC5,
	.images_per_frame_horizontal = 1,
	.images_per_frame_vertical = 1,
	.codec = 2,
	.unk8 = -1,
	.table = 1,
	.width = 32,
	.height = 32,
	.image_count = 1,
	.images = {6021},
};

sprite_data_struct krool_sprite = {
	.unk0 = 0xC6,
	.images_per_frame_horizontal = 2,
	.images_per_frame_vertical = 1,
	.codec = 2,
	.unk8 = -1,
	.table = 1,
	.width = 32,
	.height = 64,
	.image_count = 2,
	.images = {0x383, 0x384},
};

void giveGB(int kong, int level) {
	changeCollectableCount(8, 0, 1);
	displayItemOnHUD(8, 0, 0);
	// MovesBase[kong].gb_count[level] += 1;
	// if (HUD) {
	// 	short* counter = (short*)&HUD->item[8].item_count_pointer;
	// 	if (counter) {
	// 		*counter = *counter + 1;
	// 	}
	// }
}

void giveRainbowCoin(void) {
	for (int i = 0; i < 5; i++) {
		MovesBase[i].coins += 5;
	}
}

void giveAmmo(void) {
	changeCollectableCount(2, 0, 5);
}

void giveOrange(void) {
	playSound(0x147, 0x7FFF, 0x427C0000, 0x3F800000, 5, 0);
	changeCollectableCount(4, 0, 1);
}

void giveMelon(void) {
	applyDamage(0, 1);
}

void giveCrystal(void) {
	changeCollectableCount(5, 0, 150);
}

int getActorIndex(int actor_input) {
	/**
	 * @brief Changes actor index based on whether the generic bit is set
	 * 
	 * @param actor_input Raw input type
	 * 
	 * @return Final actor index
	 */
	if (actor_input & 0x8000) {
		return CUSTOM_ACTORS_START + (actor_input & 0x7FFF);
	}
	return actor_input;
}

int getCustomActorIndex(new_custom_actors offset) {
	/**
	 * @brief Gets the actor index of a new custom actor based on the offset
	 * 
	 * @param offset Offset index
	 * 
	 * @return Actor index
	 */
	return CUSTOM_ACTORS_START + offset;
}

void spawnItemOverlay(int type, int kong, int index, int force) {
	if (force) {
		spawnActor(getCustomActorIndex(NEWACTOR_JETPACITEMOVERLAY), 0);
	} else {
		spawnActor(324,0);
	}
    TextOverlayData.type = type;
    TextOverlayData.flag = index;
    TextOverlayData.kong = kong;
	TextOverlayData.string = (char*)0;
}

int giveSlamLevel(void) {
	int level = MovesBase[0].simian_slam;
	if (level < 3) {
		for (int i = 0; i < 5; i++) {
			MovesBase[i].simian_slam = level + 1;
		}
		return level + 1;
	}
	return 3;
}

int isSlamFlag(int flag) {
	for (int i = 0; i < 4; i++) {
		if (flag == slam_flags[i]) {
			return 1;
		}
	}
	return 0;
}

int isBeltFlag(int flag) {
	for (int i = 0; i < 4; i++) {
		if (flag == belt_flags[i]) {
			return 1;
		}
	}
	return 0;
}

int isInstrumentUpgradeFlag(int flag) {
	for (int i = 0; i < 6; i++) {
		if (flag == instrument_flags[i]) {
			return 1;
		}
	}
	return 0;
}

int inBattleCrown(maps map) {
	if (map == MAP_BATTLEARENA_BEAVERBRAWL) {
		return 1;
	} else if (map == MAP_BATTLEARENA_KRITTERKARNAGE) {
		return 1;
	}
	return (map >= MAP_BATTLEARENA_ARENAAMBUSH) && (map <= MAP_BATTLEARENA_SHOCKWAVESHOWDOWN);
}

int inBossMap(maps map, int include_regular, int include_krool, int include_shoe) {
	if (include_regular) {
		for (int i = 0; i < 7; i++) {
			if (regular_boss_maps[i] == map) {
				return 1;
			}
		}
	}
	if (include_krool) {
		if ((map >= MAP_KROOLDK) && (map <= MAP_KROOLCHUNKY)) {
			return 1;
		}
	}
	if (include_shoe) {
		return map == MAP_KROOLSHOE;
	}
	return 0;
}

int isGamemode(gamemodes target_mode, int force_both) {
	if (force_both) {
		if ((Gamemode == target_mode) && (Mode == target_mode)) {
			return 1;
		}
		return 0;
	}
	if (Gamemode == target_mode) {
		return 1;
	}
	return Mode == target_mode;
}

int has_key(int index) {
	if (Rando.level_order_rando_on) {
		if (index < 7) {
			return checkFlagDuplicate(Rando.key_flags[index], FLAGTYPE_PERMANENT);
		}
	}
	return checkFlagDuplicate(normal_key_flags[index], FLAGTYPE_PERMANENT);
}