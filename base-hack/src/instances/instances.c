/**
 * @file object_instance_script_changes.c
 * @author Ballaam
 * @author OnlySpaghettiCode
 * @brief Contains various hooks from the object instance script assets into C code
 * @version 0.1
 * @date 2022-01-21
 * 
 * @copyright Copyright (c) 2023
 * 
 */
#include "../../include/common.h"

#define JAPES_DKCAGEGB 0x44
#define JAPES_DKCAGESWITCH 0x40
#define JAPES_MOUNTAINGB 0x52
#define JAPES_MOUNTAINGBSWITCH 0x6
#define FACTORY_DIDDYPRODGB 0x2C
#define FACTORY_DIDDYPRODSWITCH 0x31
#define FACTORY_LANKYPRODGB 0x2A
#define FACTORY_LANKYPRODSWITCH 0x30
#define MILL_CRUSHER 0x8
#define MILL_TRIANGLEPAD 0x0
#define MILLREAR_MINI_BOX 0x3
#define GMUSH_BOARD 0xB
#define CAVES_GBDOME 0x27
#define CAVES_BOULDERDOME 0x2B
#define CAVES_SMALLBOULDERPAD 0x2E
#define CAVES_BIGBOULDERPAD 0x2F
#define JAPES_DIDDYBAMBOOGATE 0x47
#define LLAMA_LAVAGATE 0x18
#define TTEMPLE_BAMBOOGATE 0x15
#define FACTORY_FREESWITCH 0x24

#define ISLES_JAPESBOULDER 0x3
#define ISLES_AZTECDOOR 0x02
#define ISLES_FACTORYPLATFORM 0x05
#define ISLES_FACTORYDOOR 0x06
#define ISLES_GALLEONBARS 0x1A
#define ISLES_FUNGIBOULDER 0x21
#define ISLES_CAVESBOULDER 0x1B
#define ISLES_CASTLEROCK 0x34
#define ISLES_HELMJAW 0x1C

#define MILLREAR_CHUNKYCHECK_RATE 0xF
#define FUNGI_BEAN 0x5
#define FUNGI_BEANCONTROLLER 0x4D

#define FACTORY_LARGEMETALSECTION 0x0
#define ICE_MAZE 0x0

#define HELM_COIN_DOOR 0x3

#define FUNGI_SWITCH_LANKY_MUSHROOM 0XEB

#define JAPES_CAVE_GATE 0x2B
#define JAPES_PEANUT_MOUNTAIN 0x58
#define JAPES_COCONUT_RAMBI 0x123
#define CRYPT_LT_GRAPE 0x0
#define CRYPT_LT_SIMIAN_SWITCH 0x4

#define ITEM_NINTENDO_COIN 0x13E
#define ITEM_RAREWARE_COIN 0x2

#define TNS_NUMBER 0x15
#define TNS_ITEMINDICATOR 0xF

#define CROWN_CONTROLLER 0x0
#define CROWN_INDICATOR 0x4

#define FACTORY_BLOCKELEVATOR_0 0x18
#define FACTORY_BLOCKELEVATOR_1 0x19
#define FACTORY_BLOCKELEVATOR_2 0x1A
#define FACTORY_BLOCKELEVATOR_3 0x1B
#define FACTORY_BLOCKELEVATOR_4 0x1C
#define FACTORY_BLOCKELEVATOR_5 0x27
#define FACTORY_BLOCKELEVATOR_6 0x28

#define JAPES_RAMBI_DOOR 0x115
#define K_ROOL_SHIP 0x35

void spawnWrinklyWrapper(behaviour_data* behaviour, int index, int kong, int unk0) {
	int world = getWorld(CurrentMap, 0);
	int wrinkly_index = kong + (5 * world);
	int flag = FLAG_WRINKLYVIEWED + wrinkly_index;
	if (Rando.hints_are_items) {
		if (!checkFlag(flag, FLAGTYPE_PERMANENT)) {
			item_packet *item_send = &wrinkly_item_table[wrinkly_index];
			displayMedalOverlay(flag, item_send);
		}
	} else {
		setPermFlag(flag);
		giveItem(REQITEM_HINT, world, kong, (giveItemConfig){.apply_helm_hurry = 1});
	}
	if ((CurrentMap != MAP_FUNGILOBBY) || (Rando.quality_of_life.no_wrinkly_puzzles)) {
		// Display hint tick
		displayImageOnObject(index, 1, 2, 0);
		displayImageOnObject(index, 2, 2, 0);
	}
	//
	spawnWrinkly(behaviour, index, kong, unk0);
}

void loadWrinklyTextWrapper(actorData* actor, int file, int index) {
	if (Rando.hints_are_items) {
		index = wrinkly_item_table[index - 1].item_type;
		file = 47;
	}
	getTextPointer_0(actor, file, index);
}

void portalWarpFix(maps map, int exit) {
	if (map == MAP_HELM) {
		exit = getHelmExit();
	}
	initiateTransition(map, exit);
}

int change_object_scripts(behaviour_data* behaviour_pointer, int id, int index, int param2) {
	/**
	 * @brief Perform object script instructions. Can be called either through
	 * COND 6 | 7 index param2
	 * or
	 * EXEC 7 | 125 index param2
	 */
	if (index >= 0) {
		switch(CurrentMap) {
			case MAP_FUNGI:
				if (param2 == FUNGI_BEANCONTROLLER) {
					return getItemCount_new(REQITEM_BEAN, 0, 0);
				} else if (param2 == FUNGI_SWITCH_LANKY_MUSHROOM) {
					if (index == 0) {
						if (Rando.cutscene_skip_setting != CSSKIP_AUTO) {
							PlayCutsceneFromModelTwoScript(behaviour_pointer,12,1,0);
						}
					} else if (index == 1) {
						setPermFlag(FLAG_LANKY_MUSH_OPEN);
					} else if (index == 2) {
						return checkFlag(FLAG_LANKY_MUSH_OPEN, FLAGTYPE_PERMANENT);
					}
				}
				break;
			case MAP_CRANKY:
				if (param2 == ITEM_RAREWARE_COIN) {
					giveItemFromPacket(&company_coin_table[1], 0);
				}
				break;
			case MAP_ISLES:
				if (param2 == ISLES_FACTORYPLATFORM) {
					if (Rando.lobbies_open_bitfield & 4) {
						behaviour_pointer->next_state = 5;
						unkObjFunction0(id,1,0);
						unkObjFunction1(id,1,5);
						unkObjFunction2(id,1,1);
					}
				} else if (param2 == ISLES_HELMJAW) {
					if (Rando.lobbies_open_bitfield & 0x80) {
						behaviour_pointer->current_state = 100;
						behaviour_pointer->next_state = 100;
						unkObjFunction1(id,2,25);
						unkObjFunction2(id,2,1);
						unkObjFunction2(id,3,1);
					}
				} else if (param2 == K_ROOL_SHIP) {
					// Check access requirements based on ship spawn method
					if (Rando.win_condition_spawns_ship) {
						// Win condition-based access
						if (!canAccessWinCondition()) {
							return 0;
						}
					} else {
						// Key-based access
						if (getItemCount_new(REQITEM_KEY, -1, 0) < 8) {
							return 0;
						}
					}
					return 1;
				}
				break;
			case MAP_AZTECLLAMATEMPLE:
				if (param2 == LLAMA_LAVAGATE) {
					if (Rando.cutscene_skip_setting == CSSKIP_AUTO) {
						hideObject(behaviour_pointer);
						behaviour_pointer->pause_state = 1;
					}
				}
				break;
			case MAP_BATTLEARENA_BEAVERBRAWL:
			case MAP_BATTLEARENA_KRITTERKARNAGE:
			case MAP_BATTLEARENA_ARENAAMBUSH:
			case MAP_BATTLEARENA_MOREKRITTERKARNAGE:
			case MAP_BATTLEARENA_FORESTFRACAS:
			case MAP_BATTLEARENA_BISHBASHBRAWL:
			case MAP_BATTLEARENA_KAMIKAZEKREMLINGS:
			case MAP_BATTLEARENA_PLINTHPANIC:
			case MAP_BATTLEARENA_PINNACLEPALAVER:
			case MAP_BATTLEARENA_SHOCKWAVESHOWDOWN:
				if (Rando.location_visuals.crowns) {
					if (param2 == CROWN_CONTROLLER) {
						float x = 730.0f;
						float y = 267.0f;
						float z = 728.0f;
						short crown_index = getCrownIndex(CurrentMap);
						short actor = crown_item_table[crown_index].actor;
						short item = -1;
						float scale = 0.0f;
						if (actor != 0) {
							getModelTwoItemFromActor(actor, &item, &scale);
							if (item >= 0) {
								spawnModelTwo(item, x, y, z, scale, 0x4);
								int i = 0;
								while (i < ObjectModel2Count) {
									ModelTwoData* object = (ModelTwoData*)&ObjectModel2Pointer[i];
									if (object) {
										if (object->object_id == 0x4) {
											model_struct* _model = object->model_pointer;
											if (_model) {
												_model->scale = scale;
											}
											break;
										}
									}
									i++;
								}
							}
						}
					} else if (param2 == CROWN_INDICATOR) {
						behaviour_pointer->unk_70 = 0;
						behaviour_pointer->unk_60 = 1;
						behaviour_pointer->unk_62 = 100;
					}
				}
				break;
			case MAP_TROFFNSCOFF:
				if (Rando.location_visuals.boss_doors) {
					if (param2 == TNS_NUMBER) {
						float x = 600.0f;
						float y = 300.0f;
						float z = 400.0f;
						short item = -1;
						float scale = 0.0f;
						int world = getWorld(CurrentMap, 0);
						if (world < 7) {
							int flag = normal_key_flags[world];
							int key_index = getKeyIndex(flag);
							getModelTwoItemFromActor(key_item_table[key_index].actor, &item, &scale);
							if (item >= 0) {
								spawnModelTwo(item, x, y, z, scale, 0x16);
								int i = 0;
								while (i < ObjectModel2Count) {
									ModelTwoData* object = (ModelTwoData*)&ObjectModel2Pointer[i];
									if (object) {
										if (object->object_id == 0xF) {
											model_struct* _model = object->model_pointer;
											if (_model) {
												_model->scale = 2 * scale;
											}
											break;
										}
									}
									i++;
								}

							}
						}
					} else if (param2 == TNS_ITEMINDICATOR) {
						behaviour_pointer->unk_70 = 0;
						behaviour_pointer->unk_60 = 1;
						behaviour_pointer->unk_62 = 100;
					}
				}
				break;
			case MAP_JAPES:
				if (param2 == JAPES_DKCAGEGB) {
					if (index == 0) {
						if (checkFlag(DKJAPESCAGEGB_OPEN, FLAGTYPE_PERMANENT)) {
							behaviour_pointer->current_state = 5;
							behaviour_pointer->next_state = 5;
						}
					} else if (index == 1) {
						setPermFlag(DKJAPESCAGEGB_OPEN);
					} else if (index == 2) {
						if (checkFlag(DKJAPESCAGEGB_OPEN, FLAGTYPE_PERMANENT)) {
							behaviour_pointer->current_state = 6;
							behaviour_pointer->next_state = 6;
						}
					}
				} else if (param2 == JAPES_DKCAGESWITCH) {
					if(index == 0){
						if (checkFlag(DKJAPESCAGEGB_OPEN, FLAGTYPE_PERMANENT)) {
							behaviour_pointer->current_state = 20;
							behaviour_pointer->next_state = 20;
						}
					} else if(index == 1){
						// Obtain bamboo gate variables
						int bambooGateIndex = convertIDToIndex(64);
						ModelTwoData* gateModelTwoPointer = &ObjectModel2Pointer[bambooGateIndex];
						if (gateModelTwoPointer) {
							// If pointer exists with that id, check behaviour
							behaviour_data* bambooGateBehaviour = gateModelTwoPointer->behaviour_pointer;
							if (bambooGateBehaviour) {
								// If behaviour exists (always should do, but always good to check) initialize the gate
								if(bambooGateIndex != -1 && bambooGateBehaviour->pause_state == RUNSTATE_PAUSED){
									// Bamboo gate is initialized
									return 1;
								}
							}
						}
						// Bamboo gate is presumably not initialized
						return 0;
					}
				} else if (param2 == JAPES_MOUNTAINGB) {
					if (index == 0) {
						if (checkFlag(JAPESMOUNTAINSPAWNED, FLAGTYPE_PERMANENT)) {
							behaviour_pointer->current_state = 20;
							behaviour_pointer->next_state = 20;
						}
					} else if (index == 1) {
						setPermFlag(JAPESMOUNTAINSPAWNED);
					}
				} else if (param2 == JAPES_DIDDYBAMBOOGATE) {
					giveItemFromKongData(&kong_check_data[KONGCHECK_JAPES], FLAG_KONG_DIDDY);
				} else if ((param2 == JAPES_CAVE_GATE) || (param2 == JAPES_PEANUT_MOUNTAIN) || (param2 == JAPES_COCONUT_RAMBI)) {
					if ((param2 == JAPES_PEANUT_MOUNTAIN) && (index == 1)) {
						if (Rando.quality_of_life.mountain_bridge_extended) {
							return 1;
						}
						return 0;
					}
					if (param2 == JAPES_CAVE_GATE) {
						return 0;
					}
					return !Rando.tag_anywhere;
				} else if (param2 == JAPES_RAMBI_DOOR) {
					if (Player) {
						if ((Rando.quality_of_life.vanilla_fixes) && (Player->control_state == 41)) { // B attack
							return 1;
						}
						return Player->control_state == 47; // Z+B Attack
					}
				}
				break;
			case MAP_JAPESMOUNTAIN:
				if (param2 == JAPES_MOUNTAINGBSWITCH) {
					if (checkFlag(JAPESMOUNTAINSPAWNED, FLAGTYPE_PERMANENT)) {
						behaviour_pointer->current_state = 20;
						behaviour_pointer->next_state = 20;
					}
				}
				break;
			case MAP_FUNGIANTHILL:
				if (param2 == FUNGI_BEAN) {
					if (index == 0) {
						return checkFlag(FLAG_COLLECTABLE_BEAN, FLAGTYPE_PERMANENT);
					} else if (index == 1) {
						setPermFlag(FLAG_COLLECTABLE_BEAN);
					}
				}
				break;
			case MAP_FACTORY:
				if (param2 == FACTORY_DIDDYPRODGB) {
					if (index == 0) {
						if (checkFlag(FACTORYDIDDYPRODSPAWNED, FLAGTYPE_PERMANENT)) {
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
				} else if (param2 == FACTORY_LANKYPRODGB) {
					if (index == 0) {
						if (checkFlag(FLAG_LANKYPROD_SPAWNED, FLAGTYPE_PERMANENT) || (!Rando.fix_lanky_tiny_prod)) {
							behaviour_pointer->current_state = 11;
							behaviour_pointer->next_state = 11;
						}
					} else if (index == 1) {
						setPermFlag(FLAG_LANKYPROD_SPAWNED);
					}
				} else if (param2 == FACTORY_LANKYPRODSWITCH) {
					if (checkFlag(FLAG_LANKYPROD_SPAWNED, 0)) {
						behaviour_pointer->current_state = 20;
						behaviour_pointer->next_state = 20;
					}
				} else if (param2 == FACTORY_FREESWITCH) {
					giveItemFromKongData(&kong_check_data[KONGCHECK_FACTORY], FLAG_KONG_CHUNKY);
				} else if (param2 == FACTORY_LARGEMETALSECTION) {
					if (Rando.quality_of_life.vanilla_fixes) {
						behaviour_pointer->current_state = 10;
						for (int i = 1; i < 14; i++) {
							int index = convertIDToIndex(i + 1);
							if (index > -1) {
								behaviour_data* behaviour = ObjectModel2Pointer[index].behaviour_pointer;
								if (behaviour) {
									behaviour->next_state = 10;
								}
							}
						}
					}
				} else if (((param2 >= FACTORY_BLOCKELEVATOR_0) && (param2 <= FACTORY_BLOCKELEVATOR_4)) || (param2 == FACTORY_BLOCKELEVATOR_5) || (param2 == FACTORY_BLOCKELEVATOR_6)) {
					behaviour_pointer->timer = (RNG & 63) + 15;
				} else if (param2 == ITEM_NINTENDO_COIN) {
					giveItemFromPacket(&company_coin_table[0], 0);
				}
				break;
			case MAP_FUNGIMILLFRONT:
				if (param2 == MILL_CRUSHER) {
					if (index == 0) {
						if (checkFlag(FUNGICRUSHERON, FLAGTYPE_PERMANENT)) {
							if (!checkFlag(FLAG_COLLECTABLE_FUNGI_CHUNKY_KEGGB, FLAGTYPE_PERMANENT)) { // If GB not acquired
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
					}
				}
				break;
			case MAP_FUNGIMILLREAR:
				if (param2 == MILL_TRIANGLEPAD) {
					if (checkFlag(FUNGICRUSHERON, FLAGTYPE_PERMANENT)) {
						behaviour_pointer->current_state = 3;
						behaviour_pointer->next_state = 3;
					}
				} else if (param2 == MILLREAR_CHUNKYCHECK_RATE) {
					return Player->characterID == 6 || Rando.quality_of_life.vanilla_fixes;
				} else if (param2 == MILLREAR_MINI_BOX) {
					if (index == 0) {
						if (Rando.cutscene_skip_setting == CSSKIP_AUTO) {
							if (!checkFlag(223, FLAGTYPE_PERMANENT)) {
								setPermFlag(223);
							}
							hideObject(behaviour_pointer);
							behaviour_pointer->unk_70 = 0;
							behaviour_pointer->unk_71 = 0;
							setScriptRunState(behaviour_pointer, RUNSTATE_PAUSED, 0);
						} else {
							PlayCutsceneFromModelTwoScript(behaviour_pointer, 1,1,0);
						}
					}
				}
				break;
			case MAP_FUNGIGIANTMUSHROOM:
				if (param2 == GMUSH_BOARD) {
					int switch_count = 0;
					for (int i = 0; i < 5; i++) {
						if (checkFlag(FLAG_MUSHSWITCH_0 + i, FLAGTYPE_PERMANENT)) {
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
			case MAP_CAVES:
				if (param2 == CAVES_GBDOME) {
					if (index == 0) {
						if (checkFlag(CAVESGBDOME_DESTROYED, FLAGTYPE_PERMANENT)) {
							hideObject(behaviour_pointer);
							behaviour_pointer->current_state = 11;
							behaviour_pointer->next_state = 11;
						}
					} else if (index == 1) {
						setPermFlag(CAVESGBDOME_DESTROYED);
					}
				} else if (param2 == CAVES_SMALLBOULDERPAD) {
					if (checkFlag(CAVESBOULDERDOME_DESTROYED, FLAGTYPE_PERMANENT)) {
						behaviour_pointer->current_state = 20;
						behaviour_pointer->next_state = 20;
					}
				} else if (param2 == CAVES_BOULDERDOME) {
					if (index == 0) {
						if (checkFlag(CAVESBOULDERDOME_DESTROYED, FLAGTYPE_PERMANENT)) {
							hideObject(behaviour_pointer);
							behaviour_pointer->current_state = 11;
							behaviour_pointer->next_state = 11;
						}
					} else if (index == 1) {
						setPermFlag(CAVESBOULDERDOME_DESTROYED);
					}
				} else if (param2 == CAVES_BIGBOULDERPAD) {
					if (checkFlag(CAVESBOULDERDOME_DESTROYED, FLAGTYPE_PERMANENT)) {
						if (checkFlag(CAVESGBDOME_DESTROYED, FLAGTYPE_PERMANENT)) {
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
			case MAP_CAVES5DIDK:
				if (param2 == ICE_MAZE) {
					if (index == 4) {
						return standingOnM2Object(ICE_MAZE);
					} else {
						if (behaviour_pointer->switch_pressed == index) {
							if ((behaviour_pointer->contact_actor_type >= 2) && (behaviour_pointer->contact_actor_type <= 6)) { // isKong
								if (canHitSwitch()) {
									int index = convertSubIDToIndex(id);
									setSomeTimer(ObjectModel2Pointer[index].object_type);
									return 1;
								}
							}
						}
					}
					return 0;
				}
				break;
			case MAP_AZTECTINYTEMPLE:
				if (param2 == TTEMPLE_BAMBOOGATE) {
					giveItemFromKongData(&kong_check_data[KONGCHECK_ICETEMPLE], FLAG_KONG_TINY);
				}
				break;
			case MAP_CASTLECRYPTLANKYTINY:
				if (param2 == CRYPT_LT_GRAPE){
					if (index == 0){
						return !Rando.tag_anywhere;
					} else if (index == 1){
						//obtain gate variables
						int id_needed = 1;
						int gateIndex = convertIDToIndex(id_needed);
						int gateSlot = convertIDToIndex(1);
						ModelTwoData* gateModelTwoPointer = &ObjectModel2Pointer[gateSlot];
						if (gateModelTwoPointer) {
							// If pointer exists with that id, check behaviour
							behaviour_data* gateBehaviour = gateModelTwoPointer->behaviour_pointer;
							if (gateBehaviour) {
								// If behaviour exists (always should do, but always good to check) initialize the gate
								if(gateIndex != -1 && gateBehaviour->pause_state == 0){
									//vanilla initiation code
									unkObjFunction0(id_needed,1,1);
									unkObjFunction1(id_needed,1,3);
									setScriptRunState(gateBehaviour, RUNSTATE_PAUSED, 0);
								}
							}
						}

						//obtain other grape switch's variables
						int grape_switch_id_needed = 17;
						int grapeSlot = convertIDToIndex(17);
						int grapeIndex = convertIDToIndex(grape_switch_id_needed);
						ModelTwoData* grapeSwitchModelTwoPointer = &ObjectModel2Pointer[grapeSlot];
						if (grapeSwitchModelTwoPointer) {
							// If pointer exists with that id, check behaviour
							behaviour_data* grapeSwitchBehaviour = grapeSwitchModelTwoPointer->behaviour_pointer;
							if (grapeSwitchBehaviour) {
								// If behaviour exists (always should do, but always good to check) initialize the other grape switch
								if(grapeIndex != -1 && grapeSwitchBehaviour->pause_state == 0){
									setObjectScriptState(17, 4, 0);
									//vanilla initiation code
									setScriptRunState(grapeSwitchBehaviour, RUNSTATE_PAUSED, 0);
									unkObjFunction0(grape_switch_id_needed,1,1);
									unkObjFunction1(grape_switch_id_needed,1,10);
								}
							}
						}

						//play grape switch cutscene
						if (Rando.cutscene_skip_setting != CSSKIP_AUTO) {
							PlayCutsceneFromModelTwoScript(behaviour_pointer, 0, 1, 0);
							behaviour_pointer->timer = 110;
						}
						
						//move on to state 3
						behaviour_pointer->next_state = 3;
					}
				}
				break;
			case MAP_HELM:
				if (param2 == HELM_COIN_DOOR) {
					if (index == 0) {
						return isItemRequirementSatisfied(&Rando.coin_door_requirement);
					} else if (index == 1) {
						return checkFlag(FLAG_HELM_COINDOOR, FLAGTYPE_PERMANENT) || (Rando.coin_door_requirement.item == REQITEM_NONE);
					} else if (index == 2) {
						// Disable coin door text
						return 1;
					}
				}
				break;
			default:
				break;
		}
	} else if (index == -1) {
		// Bananaport generic code
		if (!WarpData) {
			int size = 90 * 10; // 90 Warps, 10 bytes per warp
			WarpData = getFile(size, 0x1FF0000);
		}
		bananaportGenericCode(behaviour_pointer, id, param2);
	} else if (index == -2) {
		spawnBreakableObject(param2);
	} else if (index == -3) {
		TNSIndicatorGenericCode(behaviour_pointer, id, param2);
	} else if (index == -4) {
		// Helm Lobby - Init
		bonus_shown = 0;
	} else if (index == -5) {
		// Helm Lobby - Can access micro
		return canOpenSpecificBLocker(7);
	} else if (index == -6) {
		// Helm Lobby Show
		activateGonePad();
	} else if (index == -7) {
		return getItemCount_new(REQITEM_KONG, 0, param2) || Rando.disable_wrinkly_kong_requirement;
	} else if (index == -8) {
		return MovesBase[param2].instrument_bitfield & 1;
	} else if (index == -9) {
		if (Rando.win_condition_spawns_ship) {
			// Win condition-based access
			if (!canAccessWinCondition()) {
				return 0;
			}
		} else {
			// Key-based access
			if (getItemCount_new(REQITEM_KEY, -1, 0) < 8) {
				return 0;
			}
		}
		return 1;
	} else if (index == -10) {
		int latest_map = Rando.k_rool_order[0];
		for (int i = 1; i < 5; i++) {
			if (checkFlag(FLAG_KROOL_ENTERED + i, FLAGTYPE_PERMANENT)) {
				if (Rando.k_rool_order[i] != 0xFF) {
					latest_map = Rando.k_rool_order[i];
				}
			}
		}
		initiateTransition(latest_map, 0);
	} else if (index == -11) {
		return canOpenXBlockers(param2);
	} else if (index == -16) {
		PauseText = param2;
	} else if (index == -17) {
		return isTimeOfDay(param2);
	} else if (index == -19) {
		if ((CurrentMap == MAP_FUNGILOBBY) && (!Rando.quality_of_life.no_wrinkly_puzzles)) {
			return 0;
		}
		int world = getWorld(CurrentMap, 0);
		return checkFlag(FLAG_WRINKLYVIEWED + (5 * world) + param2, FLAGTYPE_PERMANENT);
	} else if (index == -20) {
		if (param2 == 0) {
			setScriptRunState(behaviour_pointer, 2, 0);
		}
		int snide_index = getFirstEmptySnideReward(0);
		setPermFlag(FLAG_SNIDE_REWARD + snide_index);
		giveItemFromPacket(&snide_rewards[snide_index].item, 0);
		ItemInventory->turned_in_bp_count[getKong(0)]++;
	}
	return 0;
}