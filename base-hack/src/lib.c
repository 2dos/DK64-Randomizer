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

void playSFX(short sfxIndex) {
	playSound(sfxIndex,0x7FFF,0x427C0000,0x3F800000,0,0);
}

void setPermFlag(short flagIndex) {
	setFlag(flagIndex,1,0);
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

void changeCharSpawnerFlag(int map, int spawner_id, int new_flag) {
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

static const unsigned char dk_portal_maps[] = {0x07,0x26,0x1A,0x1E,0x30,0x48,0x57,0xA9,0xAD,0xAF,0xAE,0xB2,0xC2,0xC1};
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
		if ((CurrentMap == 7) && (exit == 15)) {
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

void alterGBKong(int map, int id, int new_kong) {
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
}