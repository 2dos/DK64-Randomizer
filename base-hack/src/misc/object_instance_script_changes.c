#include "../../include/common.h"

#define GLOOMY_GALLEON 0x1E
#define ANGRY_AZTEC 0x26
#define FUNGI_FOREST 0x30
#define CASTLE_BALLROOM 0x58
#define CASTLE_MUSEUM 0x71
#define JUNGLE_JAPES 0x7
#define FRANTIC_FACTORY 0x1A
#define CRYSTAL_CAVES 0x48
#define CREEPY_CASTLE 0x57
#define DK_ISLES 0x22
#define LLAMA_TEMPLE 0x14
#define JAPES_MOUNTAIN 0x4
#define MILL_FRONT 0x3D
#define MILL_REAR 0x3E
#define FUNGI_GMUSH 0x40
#define TRAINING_GROUNDS 0xB0
#define TINY_TEMPLE 0x10
#define CAVES_CHUNKY_5DC 0x5A
#define HELM_LOBBY 0xAA
#define GALLEON_FISH 0x33
#define TREASURE_CHEST 0x2C
#define CAVES_DK5DI 0x56
#define HIDEOUT_HELM 0x11
#define CRYPT_LT 0x6C
#define CRYPT_DDC 0x70
#define CASTLE_DUNGEON 0xA3
#define CASTLE_TREE 0xA4

#define FUNGI_MINECART_GRATE 0x22
#define SEASICK_SHIP 0x27
#define AZTEC_BEETLE_GRATE 0x1E
#define BALLROOM_MONKEYPORT 0x5
#define MUSEUM_WARP_MONKEYPORT 0x8
#define JAPES_BBLAST 0xA3
#define FACTORY_BBLAST 0x4D
#define CAVES_BBLAST 0x20
#define CASTLE_BBLAST 0x1F
#define AZTEC_BBLAST 0x2E
#define GALLEON_BBLAST 0x34
#define FUNGI_BBLAST 0x4C
#define AZTEC_SNOOPDOOR 0xA1
#define LLAMA_SNOOPPAD 0x69
#define JAPES_DKCAGEGB 0x44
#define JAPES_DKCAGESWITCH 0x40
#define JAPES_MOUNTAINGB 0x52
#define JAPES_MOUNTAINGBSWITCH 0x6
#define FACTORY_DIDDYPRODGB 0x2C
#define FACTORY_DIDDYPRODSWITCH 0x31
#define MILL_WARNINGLIGHTS 0xC
#define MILL_CRUSHER 0x8
#define MILL_TRIANGLEPAD 0x0
#define GMUSH_BOARD 0xB
#define CAVES_GBDOME 0x27
#define CAVES_BOULDERDOME 0x2B
#define CAVES_SMALLBOULDERPAD 0x2E
#define CAVES_BIGBOULDERPAD 0x2F
#define GALLEON_DKSTAR 0xC
#define AZTEC_LLAMACOCONUT 0xD

#define GALLEON_BONGO_PAD 0x11
#define GALLEON_GUITAR_CACTUS_PAD 0x14
#define GALLEON_SAX_PAD 0x13
#define GALLEON_TROMBONE_PAD 0x12
#define GALLEON_TRIANGLE_PAD 0x1B
#define GALLEON_LANKY_SLAM 0x1D
#define GALLEON_TINY_SLAM 0x1C

#define GALLEON_DK_5DSDOOR 0x19
#define GALLEON_DIDDY_5DSDOOR 0x1A
#define GALLEON_LANKY_5DSDOOR 0x17
#define GALLEON_TINY_5DSDOOR 0x18
#define GALLEON_CHUNKY_5DSDOOR 0x20
#define GALLEON_LANKY_2DSDOOR 0x1F
#define GALLEON_TINY_2DSDOOR 0x1E

#define TGROUNDS_BAMBOOGATE 0x49
#define TGROUNDS_SWITCH 0x39
#define JAPES_DIDDYBAMBOOGATE 0x47
#define JAPES_GATE0 0x2D
#define JAPES_GATE1 0x2E
#define JAPES_GATE2 0x2F
#define JAPES_GUNSWITCH0 0x30
#define JAPES_GUNSWITCH1 0x31
#define JAPES_GUNSWITCH2 0x32
#define JAPES_DIDDYFREEGB 0x48
#define LLAMA_BAMBOOGATE 0x11
#define LLAMA_GUNSWITCH 0x12
#define LLAMA_BONGOPAD 0x16
#define TTEMPLE_SWITCH 0x0
#define TTEMPLE_GUITARPAD 0x4
#define TTEMPLE_KONGLETTER0 0xC
#define TTEMPLE_KONGLETTER1 0xD
#define TTEMPLE_KONGLETTER2 0xE
#define TTEMPLE_KONGLETTER3 0xF
#define TTEMPLE_BAMBOOGATE 0x15
#define TTEMPLE_CHARGESWITCH 0x14
#define FACTORY_FREESWITCH 0x24
#define FACTORY_CAGE 0x21
#define FACTORY_FREEGB 0x78

#define FACTORY_4231_SWITCH 0x3F
#define FACTORY_3124_SWITCH 0x40
#define FACTORY_1342_SWITCH 0x41

#define ISLES_JAPESBOULDER 0x3
#define ISLES_AZTECDOOR 0x02
#define ISLES_FACTORYPLATFORM 0x05
#define ISLES_FACTORYDOOR 0x06
#define ISLES_GALLEONBARS 0x1A
#define ISLES_FUNGIBOULDER 0x21
#define ISLES_CAVESBOULDER 0x1B
#define ISLES_CASTLEROCK 0x34
#define ISLES_HELMJAW 0x1C
#define ISLES_FACTORYDOORCOLLISION 0x100

#define CHUNKY5DC_GGONE 0x6
#define CHUNKY5DC_TARGET0 0x3
#define CHUNKY5DC_TARGET1 0x4
#define CHUNKY5DC_TARGET2 0x5
#define HELMLOBBY_GGONE 0x3

#define LLAMA_MATCHING_HEAD_SOUND0_0 0x1E // Sound 173
#define LLAMA_MATCHING_HEAD_SOUND0_1 0x23
#define LLAMA_MATCHING_HEAD_SOUND1_0 0x24 // Sound 171
#define LLAMA_MATCHING_HEAD_SOUND1_1 0x27
#define LLAMA_MATCHING_HEAD_SOUND2_0 0x1B // Sound 169
#define LLAMA_MATCHING_HEAD_SOUND2_1 0x26
#define LLAMA_MATCHING_HEAD_SOUND3_0 0x1D // Sound 174
#define LLAMA_MATCHING_HEAD_SOUND3_1 0x21
#define LLAMA_MATCHING_HEAD_SOUND4_0 0x1A // Sound 172
#define LLAMA_MATCHING_HEAD_SOUND4_1 0x25
#define LLAMA_MATCHING_HEAD_SOUND5_0 0x20 // Sound 175
#define LLAMA_MATCHING_HEAD_SOUND5_1 0x22
#define LLAMA_MATCHING_HEAD_SOUND6_0 0x19 // Sound 168
#define LLAMA_MATCHING_HEAD_SOUND6_1 0x1F
#define LLAMA_MATCHING_HEAD_SOUND7_0 0x1C // Sound 170
#define LLAMA_MATCHING_HEAD_SOUND7_1 0x28

#define FISH_SHIELD1 0x3
#define FISH_SHIELD2 0x4
#define FISH_SHIELD3 0x5

#define CHEST_PEARL_0 0x0
#define MILLREAR_CHUNKYCHECK_RATE 0xF

#define FACTORY_LARGEMETALSECTION 0x0
#define FACTORY_PIANO 0x14
#define FACTORY_DARTBOARD 0x7F
#define ICE_MAZE 0x0

#define HELM_PAD_BONGO 0x2C
#define HELM_PAD_TRIANGLE 0x2D
#define HELM_PAD_SAX 0x2E
#define HELM_PAD_TROMBONE 0x2F
#define HELM_PAD_GUITAR 0x30

#define JAPES_CAVE_GATE 0x2B
#define JAPES_PEANUT_MOUNTAIN 0x58
#define JAPES_COCONUT_RAMBI 0x123
#define LLAMA_GRAPE_SWITCH 0x6B
#define FACTORY_SNATCH_GRATE 0x15
#define FACTORY_PAD_TRIANGLE 0x37
#define FACTORY_PAD_GUITAR 0x38
#define FACTORY_PAD_TROMBONE 0x3B
#define ISLES_SWITCH_GRAPE 0x27
#define ISLES_SWITCH_PINEAPPLE 0x28
#define ISLES_SWITCH_FEATHER 0x29
#define ISLES_SWITCH_PEANUT 0x2A
#define ISLES_SWITCH_COCONUT 0x32
#define AZTEC_CHUNKY_CAGE 0x24
#define CRYPT_LT_GRAPE 0x0
#define CRYPT_DDC_D 0xD
#define CRYPT_DDC_E 0xE
#define CRYPT_DDC_F 0xF
#define DUNGEON_SLAM_DIDDY 0x4
#define DUNGEON_SLAM_DK 0x5
#define DUNGEON_SLAM_LANKY 0x6
#define TREE_DOOR_DK 0x1
#define TREE_DOOR_CHUNKY 0x9

void hideObject(behaviour_data* behaviour_pointer) {
	behaviour_pointer->unk_60 = 1;
	behaviour_pointer->unk_62 = 0;
	behaviour_pointer->unk_66 = 255;
	behaviour_pointer->unk_70 = 0;
	behaviour_pointer->unk_71 = 0;
	setScriptRunState(behaviour_pointer,2,0);
}

int isBonus(int map) {
	int level = levelIndexMapping[map];
	return (level == 9) || (level == 0xD);
}

static const short kong_flags[] = {FLAG_KONG_DK,FLAG_KONG_DIDDY,FLAG_KONG_LANKY,FLAG_KONG_TINY,FLAG_KONG_CHUNKY};
static const unsigned char kong_press_states[] = {0x29,0x2E,0x26,0x29,0x24};
static const unsigned char kong_pellets[] = {48,36,42,43,38};
#define MILL_CRUSHER_PROGRESS 1

int getPressedSwitch(behaviour_data* behaviour_pointer, int bullet_type, int ID) {
	if (behaviour_pointer->switch_pressed == 1) {
		if (behaviour_pointer->contact_actor_type == bullet_type) {
			if (canHitSwitch()) {
				int index = convertSubIDToIndex(ID);
				int* m2location = ObjectModel2Pointer;
				ModelTwoData* _object = getObjectArrayAddr(m2location,0x90,index);
				setSomeTimer(_object->object_type);
				return 1;
			}
		}
	}
	return 0;
}

void setCrusher(void) {
	if (CurrentMap == MILL_FRONT) {
		if ((ObjectModel2Timer < 10) && (ObjectModel2Timer > 5)) {
			int crusher_index = convertIDToIndex(8);
			int* m2location = ObjectModel2Pointer;
			if (crusher_index > -1) {
				ModelTwoData* _object = getObjectArrayAddr(m2location,0x90,crusher_index);
				if (_object) {
					behaviour_data* behaviour = (behaviour_data*)_object->behaviour_pointer;
					if (behaviour) {
						if (behaviour->counter == 0) {
							behaviour->counter = MILL_CRUSHER_PROGRESS;
						}
					}
				}
			}
		}
	}
}

int checkControlState(int target_control_state) {
	if (Player) {
		if (Player->control_state == target_control_state) {
			if (target_control_state == 0x24) {
				if (Player->control_state_progress == 2) {
					return 1;
				}
			} else {
				if (Player->control_state_progress == 1) {
					return 1;
				}
			}
		}
	}
	return 0;
}

int checkSlamLocation(int kong, int key, int id) {
	if (Character == kong) {
		if (Player) {
			if ((Player->obj_props_bitfield & 0x2000) == 0) {
				if (Player->touching_object == 1) {
					if (id == Player->standing_on_index) {
						if (Player->standing_on_subposition == key) {
							return 1;
						}
					}
				}
			}
		}
	}
	return 0;
}

void playSFXContainer(int id, int vanilla_sfx, int new_sfx) {
	int index = convertIDToIndex(id);
	if (index == -1) {
		index = 0;
	}
	int sfx_played = new_sfx;
	if (new_sfx == 0) {
		sfx_played = vanilla_sfx;
	}
	playSFXFromObject(index,sfx_played,-1,127,0,0,0.3f);
}

int change_object_scripts(behaviour_data* behaviour_pointer, int id, int index, int param2) {
	switch(CurrentMap) {
		case GLOOMY_GALLEON:
			{
				int gate_index = -1;
				int gate_flag = -1;
				switch (param2) {
					case SEASICK_SHIP:
						if (Rando.randomize_more_loading_zones) {
							initiateTransition_0((Rando.seasick_ship_enter >> 8) & 0xFF, Rando.seasick_ship_enter & 0xFF, 0, 0);
						} else {
							initiateTransition_0(31, 0, 0, 0);
						}
						break;
					case GALLEON_DKSTAR:
						{
							int progress = 1;
							if (Rando.quality_of_life) {
								progress = 3;
							}
							behaviour_pointer->next_state = progress;
						}
						break;
					case GALLEON_BONGO_PAD:
					case GALLEON_GUITAR_CACTUS_PAD:
					case GALLEON_TRIANGLE_PAD:
					case GALLEON_SAX_PAD:
					case GALLEON_TROMBONE_PAD:
					case GALLEON_LANKY_SLAM:
					case GALLEON_TINY_SLAM:
						if (index == 0) { 
							return !Rando.remove_high_requirements;
						}
						else{
							if (Rando.remove_high_requirements) {
								behaviour_pointer->next_state = 6;
							}
							else {
								behaviour_pointer->next_state = 5;
							}
						}
						break;
					case GALLEON_DK_5DSDOOR:
						gate_index = 0;
						gate_flag = GALLEON_5DSOPEN_DK;
					case GALLEON_DIDDY_5DSDOOR:
						if (gate_index < 0) {
							gate_index = 1;
							gate_flag = GALLEON_5DSOPEN_DIDDY;
						}
					case GALLEON_LANKY_5DSDOOR:
						if (gate_index < 0) {
							gate_index = 2;
							gate_flag = GALLEON_5DSOPEN_LANKY;
						}
					case GALLEON_TINY_5DSDOOR:
						if (gate_index < 0) {
							gate_index = 3;
							gate_flag = GALLEON_5DSOPEN_TINY;
						}
					case GALLEON_CHUNKY_5DSDOOR:
						if (gate_index < 0) {
							gate_index = 4;
							gate_flag = GALLEON_5DSOPEN_CHUNKY;
						}
					case GALLEON_LANKY_2DSDOOR:
						if (gate_index < 0) {
							gate_index = 5;
							gate_flag = GALLEON_2DSOPEN_LANKY;
						}
					case GALLEON_TINY_2DSDOOR:
						if (gate_index < 0) {
							gate_index = 6;
							gate_flag = GALLEON_2DSOPEN_TINY;
						}
						if (index == 0) {
							if (Rando.remove_high_requirements) {
								if (checkFlag(gate_flag,0)) {
									behaviour_pointer->current_state = 10;
									behaviour_pointer->next_state = 10;
								}
							}
						} else {
							if (Rando.remove_high_requirements) {
								setPermFlag(gate_flag);
							}
						}
					break;
				}
			}
			break;
		case ANGRY_AZTEC:
			if (param2 == AZTEC_BEETLE_GRATE) {
				if (Rando.randomize_more_loading_zones) {
					initiateTransition_0((Rando.aztec_beetle_enter >> 8) & 0xFF, Rando.aztec_beetle_enter & 0xFF, 0, 0);
				} else {
					initiateTransition_0(14, 0, 0, 0);
				}
			} else if (param2 == AZTEC_SNOOPDOOR) {
				if (index == 0) {
					// Flag Check
					if (checkFlag(SNOOPDOOR_OPEN,0)) {
						behaviour_pointer->next_state = 40;
						behaviour_pointer->current_state = 40;
					}
				} else if (index == 1) {
					// Flag Set
					setPermFlag(SNOOPDOOR_OPEN);
					setNextTransitionType(0);
				}
			} else if (param2 == AZTEC_LLAMACOCONUT) {
				if (!Rando.quality_of_life) {
					PlayCutsceneFromModelTwoScript(behaviour_pointer,23,1,0);
				}
			} else if (param2 == AZTEC_CHUNKY_CAGE) {
				return !Rando.tag_anywhere;
			}
			break;
		case FUNGI_FOREST:
			if (param2 == FUNGI_MINECART_GRATE) {
				if (Rando.randomize_more_loading_zones) {
					initiateTransition_0((Rando.fungi_minecart_enter >> 8) & 0xFF, Rando.fungi_minecart_enter & 0xFF, 0, 0);
				} else {
					initiateTransition_0(55, 0, 0, 0);
				}
			}
			break;
		case CASTLE_BALLROOM:
			if (param2 == BALLROOM_MONKEYPORT) {
				if (Rando.randomize_more_loading_zones) {
					createCollisionObjInstance(COLLISION_MAPWARP,(Rando.ballroom_to_museum >> 8 & 0xFF), Rando.ballroom_to_museum & 0xFF);
				} else {
					createCollisionObjInstance(COLLISION_MAPWARP,113,2);
				}
			}
			break;
		case CASTLE_MUSEUM:
			if (param2 == MUSEUM_WARP_MONKEYPORT) {
				if (Rando.randomize_more_loading_zones) {
					createCollisionObjInstance(COLLISION_MAPWARP,(Rando.museum_to_ballroom >> 8 & 0xFF), Rando.museum_to_ballroom & 0xFF);
				} else {
					createCollisionObjInstance(COLLISION_MAPWARP,88,1);
				}
			}
			break;
		case DK_ISLES:
			if (param2 == ISLES_JAPESBOULDER) {
				if (Rando.lobbies_open_bitfield & 1) {
					hideObject(behaviour_pointer);
				}
			} else if (param2 == ISLES_AZTECDOOR) {
				if (Rando.lobbies_open_bitfield & 2) {
					hideObject(behaviour_pointer);
				}
			} else if (param2 == ISLES_FACTORYPLATFORM) {
				if (Rando.lobbies_open_bitfield & 4) {
					behaviour_pointer->next_state = 5;
					unkObjFunction0(id,1,0);
					unkObjFunction1(id,1,5);
					unkObjFunction2(id,1,1);
				}
			} else if (param2 == ISLES_FACTORYDOOR) {
				if (Rando.lobbies_open_bitfield & 4) {
					hideObject(behaviour_pointer);
				}
			} else if (param2 == ISLES_FACTORYDOORCOLLISION) {
				if ((Rando.lobbies_open_bitfield & 4) || (checkFlag(FLAG_KEYIN_KEY2,0) || ((CutsceneIndex == 7) && (CutsceneActive == 1) && ((CutsceneStateBitfield & 4) == 0)))) {
					hideObject(behaviour_pointer);
					behaviour_pointer->next_state = 1;
				}
			} else if (param2 == ISLES_GALLEONBARS) {
				if (Rando.lobbies_open_bitfield & 8) {
					hideObject(behaviour_pointer);
				}
			} else if (param2 == ISLES_FUNGIBOULDER) {
				if (Rando.lobbies_open_bitfield & 0x10) {
					hideObject(behaviour_pointer);
				}
			} else if (param2 == ISLES_CAVESBOULDER) {
				if (Rando.lobbies_open_bitfield & 0x20) {
					hideObject(behaviour_pointer);
				}
			} else if (param2 == ISLES_CASTLEROCK) {
				if (Rando.lobbies_open_bitfield & 0x40) {
					hideObject(behaviour_pointer);
				}
			} else if (param2 == ISLES_HELMJAW) {
				if (Rando.lobbies_open_bitfield & 0x80) {
					behaviour_pointer->current_state = 100;
					behaviour_pointer->next_state = 100;
					unkObjFunction1(id,2,25);
					unkObjFunction2(id,2,1);
					unkObjFunction2(id,3,1);
				}
			} else if ((param2 == ISLES_SWITCH_COCONUT) || (param2 == ISLES_SWITCH_PEANUT) || (param2 == ISLES_SWITCH_GRAPE) || (param2 == ISLES_SWITCH_FEATHER) || (param2 == ISLES_SWITCH_PINEAPPLE)) {
				return !Rando.tag_anywhere;
			} else {
				// TestVariable = (int)behaviour_pointer;
				// *(int*)(0x807FF700) = id;
			}
			break;
		case LLAMA_TEMPLE:
			if (param2 == LLAMA_SNOOPPAD) {
				if (checkFlag(SNOOPDOOR_OPEN,0)) {
					behaviour_pointer->current_state = 20;
					behaviour_pointer->next_state = 20;
				}
			} else if (param2 == LLAMA_BONGOPAD) {
				return Character == Rando.free_source_llama;
			} else if (param2 == LLAMA_BAMBOOGATE) {
				if (index == 0) {
					return checkFlag(kong_flags[(int)Rando.free_target_llama],0);
				} else if (index == 1) {
					return !checkFlag(kong_flags[(int)Rando.free_target_llama],0);
				}
			} else if (param2 == LLAMA_GUNSWITCH) {
				if (index == 0) {
					return checkFlag(kong_flags[(int)Rando.free_target_llama],0);
				} else if (index == 1) {
					return !checkFlag(kong_flags[(int)Rando.free_target_llama],0);
				} else if (index == 2) {
					setPermFlag(kong_flags[(int)Rando.free_target_llama]);
				} else if ((index >= 3) && (index <= 6)) {
					return getPressedSwitch(behaviour_pointer,kong_pellets[(int)Rando.free_source_llama],id);
				}
			} else if (param2 == LLAMA_GRAPE_SWITCH) {
				return !Rando.tag_anywhere;
			} else {
				int head_ids[] = {
					LLAMA_MATCHING_HEAD_SOUND0_0,
					LLAMA_MATCHING_HEAD_SOUND0_1,
					LLAMA_MATCHING_HEAD_SOUND1_0,
					LLAMA_MATCHING_HEAD_SOUND1_1,
					LLAMA_MATCHING_HEAD_SOUND2_0,
					LLAMA_MATCHING_HEAD_SOUND2_1,
					LLAMA_MATCHING_HEAD_SOUND3_0,
					LLAMA_MATCHING_HEAD_SOUND3_1,
					LLAMA_MATCHING_HEAD_SOUND4_0,
					LLAMA_MATCHING_HEAD_SOUND4_1,
					LLAMA_MATCHING_HEAD_SOUND5_0,
					LLAMA_MATCHING_HEAD_SOUND5_1,
					LLAMA_MATCHING_HEAD_SOUND6_0,
					LLAMA_MATCHING_HEAD_SOUND6_1,
					LLAMA_MATCHING_HEAD_SOUND7_0,
					LLAMA_MATCHING_HEAD_SOUND7_1,
				};
				int head_sounds[] = {173,171,169,174,172,175,168,170};
				int selection = -1;
				for (int k = 0; k < sizeof(head_ids)/4; k++) {
					if (param2 == head_ids[k]) {
						selection = k / 2;
					}
				}
				if (selection > -1) {
					playSFXContainer(param2,head_sounds[selection],Rando.matching_game_sounds[selection]);
				}
				
			}
			break;
		case CAVES_CHUNKY_5DC:
			if ((param2 == CHUNKY5DC_GGONE) || (param2 == CHUNKY5DC_TARGET0) || (param2 == CHUNKY5DC_TARGET1) || (param2 == CHUNKY5DC_TARGET2)) {
				if (index == 0) {
					return isBonus(PreviousMap);
				} else if (index == 1) {
					return !isBonus(PreviousMap);
				}
			}
			break;
		case HELM_LOBBY:
			if (param2 == HELMLOBBY_GGONE) {
				return isBonus(PreviousMap);
			}
			break;
		case JUNGLE_JAPES:
			if (param2 == JAPES_DKCAGEGB) {
				if (index == 0) {
					if (checkFlag(DKJAPESCAGEGB_OPEN,0)) {
						behaviour_pointer->current_state = 5;
						behaviour_pointer->next_state = 5;
					}
				} else if (index == 1) {
					setPermFlag(DKJAPESCAGEGB_OPEN);
				} else if (index == 2) {
					if (checkFlag(DKJAPESCAGEGB_OPEN,0)) {
						behaviour_pointer->current_state = 6;
						behaviour_pointer->next_state = 6;
					}
				}
			} else if (param2 == JAPES_DKCAGESWITCH) {
				if (checkFlag(DKJAPESCAGEGB_OPEN,0)) {
					behaviour_pointer->current_state = 20;
					behaviour_pointer->next_state = 20;
				}
			} else if (param2 == JAPES_MOUNTAINGB) {
				if (index == 0) {
					if (checkFlag(JAPESMOUNTAINSPAWNED,0)) {
						behaviour_pointer->current_state = 20;
						behaviour_pointer->next_state = 20;
					}
				} else if (index == 1) {
					setPermFlag(JAPESMOUNTAINSPAWNED);
				}
			} else if (param2 == JAPES_DIDDYBAMBOOGATE) {
				if (index == 0) {
					return checkFlag(kong_flags[(int)Rando.free_target_japes],0);
				} else if (index == 1) {
					return !checkFlag(kong_flags[(int)Rando.free_target_japes],0);
				} else if (index == 2) {
					setPermFlag(kong_flags[(int)Rando.free_target_japes]);
				}
			} else if ((param2 == JAPES_GUNSWITCH0) || (param2 == JAPES_GUNSWITCH1) || (param2 == JAPES_GUNSWITCH2)) {
				if (index == 0) {
					return checkFlag(kong_flags[(int)Rando.free_target_japes],0);
				} else if (index == 1) {
					return !checkFlag(kong_flags[(int)Rando.free_target_japes],0);
				} else if ((index == 2) || (index == 3)) {
					return getPressedSwitch(behaviour_pointer, kong_pellets[(int)Rando.free_source_japes], id);
				} else if (index == 4) {
					return !Rando.quality_of_life; // TODO: Retry this
				}
			} else if ((param2 == JAPES_GATE0) || (param2 == JAPES_GATE1) || (param2 == JAPES_GATE2)) {
				if (Rando.open_level_sections) {
					behaviour_pointer->current_state = 20;
					behaviour_pointer->next_state = 20;
				}
			} else if (param2 == JAPES_DIDDYFREEGB) {
				if (index == 0) {
					return checkFlag(kong_flags[(int)Rando.free_target_japes],0);
				} else if (index == 1) {
					return !checkFlag(kong_flags[(int)Rando.free_target_japes],0);
				}
			} else if ((param2 == JAPES_CAVE_GATE) || (param2 == JAPES_PEANUT_MOUNTAIN) || (param2 == JAPES_COCONUT_RAMBI)) {
				return !Rando.tag_anywhere;
			}
			break;
		case JAPES_MOUNTAIN:
			if (param2 == JAPES_MOUNTAINGBSWITCH) {
				if (checkFlag(JAPESMOUNTAINSPAWNED,0)) {
					behaviour_pointer->current_state = 20;
					behaviour_pointer->next_state = 20;
				}
			}
			break;
		case FRANTIC_FACTORY:
			if (param2 == FACTORY_DIDDYPRODGB) {
				if (index == 0) {
					if (checkFlag(FACTORYDIDDYPRODSPAWNED,0)) {
						behaviour_pointer->current_state = 11;
						behaviour_pointer->next_state = 11;
					}
				} else if (index == 1) {
					setPermFlag(FACTORYDIDDYPRODSPAWNED);
				}
			} else if (param2 == FACTORY_DIDDYPRODSWITCH) {
				if (checkFlag(FACTORYDIDDYPRODSPAWNED,0)) {
					behaviour_pointer->current_state = 20;
					behaviour_pointer->next_state = 20;
				}
			} else if (param2 == FACTORY_FREESWITCH) {
				if (index == 0) {
					return checkFlag(kong_flags[(int)Rando.free_target_factory],0);
				} else if (index == 1) {
					return !checkFlag(kong_flags[(int)Rando.free_target_factory],0);
				} else if (index == 2) {
					return Character == Rando.free_source_factory;
				} else if (index == 3) {
					setPermFlag(kong_flags[(int)Rando.free_target_factory]);
				}
			} else if (param2 == FACTORY_CAGE) {
				if (index == 0) {
					return checkFlag(kong_flags[(int)Rando.free_target_factory],0);
				} else if (index == 1) {
					return !checkFlag(kong_flags[(int)Rando.free_target_factory],0);
				}
			} else if (param2 == FACTORY_FREEGB) {
				if (index == 0) {
					return checkFlag(kong_flags[(int)Rando.free_target_factory],0);
				} else if (index == 1) {
					return !checkFlag(kong_flags[(int)Rando.free_target_factory],0);
				}
			} else if (param2 == FACTORY_PIANO) {
				if (index < 7) {
					// Kremling appears
					spawnPianoKremling(Rando.piano_game_order[index] + 5,0);
				} else if (index < 14) {
					setAcceptablePianoKey(id, Rando.piano_game_order[index - 7] + 1,2);
				} else if (index < 21) {
					return checkSlamLocation(2, Rando.piano_game_order[index - 14] + 1, id);
				} else if (index < 28) {
					return checkContactSublocation(behaviour_pointer,id,Rando.piano_game_order[index - 21] + 1, 0);
				} else if (index == 28) {
					if (Rando.fast_gbs) {
						behaviour_pointer->next_state = 26;
					} else {
						behaviour_pointer->next_state = 17;
					}
				} else if (index == 29) {
					if (Rando.fast_gbs) {
						behaviour_pointer->next_state = 50;
					} else {
						behaviour_pointer->next_state = 37;
					}
				}
			} else if (param2 == FACTORY_3124_SWITCH || param2 == FACTORY_4231_SWITCH || param2 == FACTORY_1342_SWITCH) {
				if (index == 0) {
					return Rando.fast_gbs;
				} else if (index == 1) {
					// Check if GB is in a state >= 3, this means it was spawned.
					int index = convertIDToIndex(96);
					int* m2location = ObjectModel2Pointer;
					if (index > -1) {
						ModelTwoData* _object = getObjectArrayAddr(m2location,0x90,index);
						behaviour_data* behaviour = (behaviour_data*)_object->behaviour_pointer;
						if (_object && behaviour) {
							if(behaviour->current_state <= 3) {
								behaviour_pointer->current_state = 5;
							}
						}
					}
				} else if (index == 2) {
					if (Rando.fast_gbs) {
						disableDiddyRDDoors();
					}
					else {
						setScriptRunState(behaviour_pointer, 2, 0);
					}
        		}
			} else if (param2 == FACTORY_DARTBOARD) {
				if (index < 6) {
					if (behaviour_pointer->switch_pressed == (Rando.dartboard_order[index] + 1)) {
						if (behaviour_pointer->contact_actor_type == 43) {
							if (canHitSwitch()) {
								int index = convertSubIDToIndex(id);
								int* m2location = ObjectModel2Pointer;
								ModelTwoData* _object = getObjectArrayAddr(m2location,0x90,index);
								setSomeTimer(_object->object_type);
								return 1;
							}
						}
					}
					return 0;
				}
			} else if (param2 == FACTORY_LARGEMETALSECTION) {
				if (Rando.quality_of_life) {
					behaviour_pointer->current_state = 10;
					unsigned char crusher_compontents[] = {1,3,8,9,4,10,11,12,13,2,5,6,7};
					int* m2location = ObjectModel2Pointer;
					for (int component = 0; component < sizeof(crusher_compontents); component++) {
						int index = convertIDToIndex(crusher_compontents[component]);
						if (index > -1) {
							ModelTwoData* _object = getObjectArrayAddr(m2location,0x90,index);
							behaviour_data* behaviour = (behaviour_data*)_object->behaviour_pointer;
							if (behaviour) {
								behaviour->next_state = 10;
							}
						}
					}
				}
			} else if ((param2 == FACTORY_SNATCH_GRATE) || (param2 == FACTORY_PAD_GUITAR) || (param2 == FACTORY_PAD_TRIANGLE) || (param2 == FACTORY_PAD_TROMBONE)) {
				return !Rando.tag_anywhere;
			}
			break;
		case MILL_FRONT:
			if (param2 == MILL_WARNINGLIGHTS) {
				if (checkFlag(FUNGICRUSHERON,0)) {
					behaviour_pointer->current_state = MILL_CRUSHER_PROGRESS * 2;
					behaviour_pointer->next_state = MILL_CRUSHER_PROGRESS * 2;
				}
			} else if (param2 == MILL_CRUSHER) {
				if (index == 0) {
					if (checkFlag(FUNGICRUSHERON,0)) {
						if (!checkFlag(FLAG_COLLECTABLE_FUNGI_CHUNKY_KEGGB,0)) { // If GB not acquired
							if (behaviour_pointer->counter == 0) {
								behaviour_pointer->current_state = 12;
								behaviour_pointer->next_state = 12;
								unkObjFunction1(id,1,8);
								unkObjFunction2(id,1,65535);
							}
						}
					}
				} else if (index == 1) {
					setPermFlag(FUNGICRUSHERON);
					behaviour_pointer->counter = MILL_CRUSHER_PROGRESS;
				}
			}
			break;
		case MILL_REAR:
			if (param2 == MILL_TRIANGLEPAD) {
				if (checkFlag(FUNGICRUSHERON,0)) {
					behaviour_pointer->current_state = 3;
					behaviour_pointer->next_state = 3;
				}
			} else if (param2 == MILLREAR_CHUNKYCHECK_RATE) {
				return Player->characterID == 6 || Rando.quality_of_life;
			}
			break;
		case FUNGI_GMUSH:
			if (param2 == GMUSH_BOARD) {
				int switch_count = 0;
				for (int i = 0; i < 5; i++) {
					if (checkFlag(FLAG_MUSHSWITCH_0 + i,0)) {
						switch_count += 1;
					}
				}
				if (switch_count == 5) {
					behaviour_pointer->current_state = 6;
					behaviour_pointer->next_state = 6;
					behaviour_pointer->timer = 465;
				}
			}
			break;
		case CRYSTAL_CAVES:
			if (param2 == CAVES_GBDOME) {
				if (index == 0) {
					if (checkFlag(CAVESGBDOME_DESTROYED,0)) {
						hideObject(behaviour_pointer);
						behaviour_pointer->current_state = 11;
						behaviour_pointer->next_state = 11;
					}
				} else if (index == 1) {
					setPermFlag(CAVESGBDOME_DESTROYED);
				}
			} else if (param2 == CAVES_SMALLBOULDERPAD) {
				if (checkFlag(CAVESBOULDERDOME_DESTROYED,0)) {
					behaviour_pointer->current_state = 20;
					behaviour_pointer->next_state = 20;
				}
			} else if (param2 == CAVES_BOULDERDOME) {
				if (index == 0) {
					if (checkFlag(CAVESBOULDERDOME_DESTROYED,0)) {
						hideObject(behaviour_pointer);
						behaviour_pointer->current_state = 11;
						behaviour_pointer->next_state = 11;
					}
				} else if (index == 1) {
					setPermFlag(CAVESBOULDERDOME_DESTROYED);
				}
			} else if (param2 == CAVES_BIGBOULDERPAD) {
				if (checkFlag(CAVESBOULDERDOME_DESTROYED,0)) {
					if (checkFlag(CAVESGBDOME_DESTROYED,0)) {
						hideObject(behaviour_pointer);
						behaviour_pointer->current_state = 20;
						behaviour_pointer->next_state = 20;
					} else {
						behaviour_pointer->current_state = 10;
						behaviour_pointer->next_state = 10;
					}
				}
			}
			break;
		case TRAINING_GROUNDS:
			if (param2 == TGROUNDS_SWITCH) {
				if (index == 0) {
					return checkFlag(kong_flags[(int)Rando.starting_kong],0);
				} else if (index == 1) {
					return !checkFlag(kong_flags[(int)Rando.starting_kong],0);
				} else if (index == 2) {
					setPermFlag(kong_flags[(int)Rando.starting_kong]);
				}
			} else if (param2 == TGROUNDS_BAMBOOGATE) {
				if (index == 0) {
					return checkFlag(kong_flags[(int)Rando.starting_kong],0);
				} else if (index == 1) {
					return !checkFlag(kong_flags[(int)Rando.starting_kong],0);
				}
			}
			break;
		case GALLEON_FISH:
			if ((param2 == FISH_SHIELD1) || (param2 == FISH_SHIELD2) || (param2 == FISH_SHIELD3)) {
				int fish_state = 1;
				if (Rando.fast_gbs) {
					fish_state = 5;
				}
				behaviour_pointer->next_state = fish_state;
			}
			break;
		case TREASURE_CHEST:
			if (param2 == CHEST_PEARL_0) {
				if (Rando.fast_gbs) {
					int pearls_collected = 0;
					for (int i = 0; i < 5; i++) {
						pearls_collected += checkFlag(FLAG_PEARL_0_COLLECTED + i,0);
					}
					if (pearls_collected >= 1) {
						for (int i = 0; i < 5; i++) {
							setPermFlag(FLAG_PEARL_0_COLLECTED + i);
						}
						behaviour_pointer->next_state = 2;
					}
				}
			}
			break;
		case CAVES_DK5DI:
			if (param2 == ICE_MAZE) {
				if (behaviour_pointer->switch_pressed == index) {
					if ((behaviour_pointer->contact_actor_type >= 2) && (behaviour_pointer->contact_actor_type <= 6)) { // isKong
						if (canHitSwitch()) {
							int index = convertSubIDToIndex(id);
							int* m2location = ObjectModel2Pointer;
							ModelTwoData* _object = getObjectArrayAddr(m2location,0x90,index);
							setSomeTimer(_object->object_type);
							return 1;
						}
					}
				}
				return 0;
			}
			break;
		case TINY_TEMPLE:
			if (param2 == TTEMPLE_SWITCH) {
				return Character == 1;
			} else if (param2 == TTEMPLE_GUITARPAD) {
				return Character == 1;
			} else if (param2 == TTEMPLE_BAMBOOGATE) {
				if (index == 0) {
					return checkFlag(kong_flags[(int)Rando.free_target_ttemple],0);
				} else if (index == 1) {
					setPermFlag(kong_flags[(int)Rando.free_target_ttemple]);
				}
			} else if (param2 == TTEMPLE_CHARGESWITCH) {
				if (index == 0) {
					return checkFlag(kong_flags[(int)Rando.free_target_ttemple],0);
				} else if (index == 1) {
					return !checkFlag(kong_flags[(int)Rando.free_target_ttemple],0);
				} else if (index == 2) {
					return checkControlState(kong_press_states[(int)Rando.free_source_ttemple]);
				}
			} else if ((param2 == TTEMPLE_KONGLETTER0) || (param2 == TTEMPLE_KONGLETTER1) || (param2 == TTEMPLE_KONGLETTER2) || (param2 == TTEMPLE_KONGLETTER3)) {
				return checkControlState(kong_press_states[(int)Rando.free_source_ttemple]);
			}
			break;
		case CRYPT_LT:
			if (param2 == CRYPT_LT_GRAPE) {
				return !Rando.tag_anywhere;
			}
			break;
		case CRYPT_DDC:
			if ((param2 == CRYPT_DDC_D) || (param2 == CRYPT_DDC_E) || (param2 == CRYPT_DDC_F)) {
				return !Rando.tag_anywhere;
			}
			break;
		case CASTLE_DUNGEON:
			if ((param2 == DUNGEON_SLAM_DK) || (param2 == DUNGEON_SLAM_DIDDY) || (param2 == DUNGEON_SLAM_LANKY)) {
				return !Rando.tag_anywhere;
			}
			break;
		case CASTLE_TREE:
			if ((param2 == TREE_DOOR_DK) || (param2 == TREE_DOOR_CHUNKY)) {
				return !Rando.tag_anywhere;
			}
			break;
		case HIDEOUT_HELM:
			{
				int slot = -1;
				int next_slot = -1;
				int previous_slot = -1;
				int current_slot = -1;
				switch(param2) {
					case HELM_PAD_BONGO:
						slot = 0;
					case HELM_PAD_TRIANGLE:
						if (slot == -1) {
							slot = 1;
						}
					case HELM_PAD_SAX:
						if (slot == -1) {
							slot = 2;
						}
					case HELM_PAD_TROMBONE:
						if (slot == -1) {
							slot = 3;
						}
					case HELM_PAD_GUITAR:
						if (slot == -1) {
							slot = 4;
						}
						if (slot > -1) {
							for (int i = 0; i < 5; i++) {
								if (Rando.helm_order[i] == slot) {
									current_slot = i;
									if (i > 0) {
										previous_slot = Rando.helm_order[i - 1];
									}
									if (i < 4) {
										next_slot = Rando.helm_order[i + 1];
									}
								}
							}
							if (index == 0) {
								// Barrels complete
								if ((next_slot == -1) && (current_slot > -1)) {
									// Helm Complete
									PlayCutsceneFromModelTwoScript(behaviour_pointer, 8, 1, 0);
									setFlag(FLAG_MODIFIER_HELMBOM, 1, 0);
									setFlag(0x50,1,2);
									*(int*)(0x807FF704) = param2;
								} else if (next_slot > -1) {
									// Move to next
									PlayCutsceneFromModelTwoScript(behaviour_pointer, current_slot + 4, 1, 0);
								}
							} else if (index == 1) {
								if (param2 == HELM_PAD_GUITAR) {
									*(int*)(0x807FF700) = previous_slot;
								}
								if (previous_slot == -1) {
									// First or not in sequence
									return 1;
								} else {
									return checkFlag(previous_slot + 0x4B, 2);
								}
							}
						}
					break;
				}
			}
		break;
	}
	InstanceScriptParams[1] = id;
	InstanceScriptParams[2] = index;
	InstanceScriptParams[3] = param2;
	return 0;
}

void spawnCannon(actorData* cannon) {
	cannon->shadow_intensity = 0xFF;
	cannon->obj_props_bitfield |= 0x8000;
	cannon->control_state = 0;
	cannon->noclip_byte = 2;
}

int spawnCannonWrapper(void) {
	if (CurrentMap == DK_ISLES) {
		int spawner_id = getActorSpawnerIDFromTiedActor(CurrentActorPointer);
		if (spawner_id == 8) { // Castle Cannon
			if (Rando.lobbies_open_bitfield & 0x40) {
				return 1;
			}
		} else if (spawner_id == 18) { // Fungi Cannon
			if (Rando.lobbies_open_bitfield & 0x10) {
				return 1;
			}
		} 
	}
	return 0;
}

void disableDiddyRDDoors(void) {
	for(int i = 63; i < 66; ++i) {
		int index = convertIDToIndex(i);
		int* m2location = ObjectModel2Pointer;
		ModelTwoData* _object = getObjectArrayAddr(m2location,0x90,index);
		behaviour_data* behaviour = (behaviour_data*)_object->behaviour_pointer;
		if (behaviour) {
			setScriptRunState(behaviour,2,0);
		}
	}
}