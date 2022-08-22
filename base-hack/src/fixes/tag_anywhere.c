#include "../../include/common.h"

#define TAG_ANYWHERE_KONG_LIMIT 5

static const map_bitfield banned_map_btf = {
    .test_map = 0,
    .funkys_store = 1, // Reason: Shop
    .dk_arcade = 1, // Reason: Locked Movement
    .k_rool_barrel_lankys_maze = 0,
    .jungle_japes_mountain = 0,
    .crankys_lab = 1, // Reason: Shop
    .jungle_japes_minecart = 1, // Reason: Locked Movement
    .jungle_japes = 0,
    .jungle_japes_army_dillo = 1, // Reason: Boss Map
    .jetpac = 1, // Reason: Locked Movement
    .kremling_kosh_very_easy = 1, // Reason: Locked Movement
    .stealthy_snoop_normal_no_logo = 0,
    .jungle_japes_shell = 0,
    .jungle_japes_lankys_cave = 0,
    .angry_aztec_beetle_race = 1, // Reason: Locked Movement
    .snides_hq = 1, // Reason: Shop
    .angry_aztec_tinys_temple = 0,
    .hideout_helm = 0,
    .teetering_turtle_trouble_very_easy = 1, // Reason: Locked Movement
    .angry_aztec_five_door_temple_dk = 0,
    .angry_aztec_llama_temple = 0,
    .angry_aztec_five_door_temple_diddy = 0,
    .angry_aztec_five_door_temple_tiny = 0,
    .angry_aztec_five_door_temple_lanky = 0,
    .angry_aztec_five_door_temple_chunky = 0,
    .candys_music_shop = 1, // Reason: Shop
    .frantic_factory = 0,
    .frantic_factory_car_race = 1, // Reason: Locked Movement
    .hideout_helm_level_intros_game_over = 1, // Reason: Cutscene Map
    .frantic_factory_power_shed = 0,
    .gloomy_galleon = 0,
    .gloomy_galleon_k_rools_ship = 0,
    .batty_barrel_bandit_very_easy = 1, // Reason: Locked Movement
    .jungle_japes_chunkys_cave = 0,
    .dk_isles_overworld = 0,
    .k_rool_barrel_dks_target_game = 0,
    .frantic_factory_crusher_room = 0,
    .jungle_japes_barrel_blast = 1, // Reason: BBlast Course
    .angry_aztec = 0,
    .gloomy_galleon_seal_race = 1, // Reason: Locked Movement
    .nintendo_logo = 1, // Reason: Cutscene Map
    .angry_aztec_barrel_blast = 1, // Reason: BBlast Course
    .troff_n_scoff = 0,
    .gloomy_galleon_shipwreck_diddy_lanky_chunky = 0,
    .gloomy_galleon_treasure_chest = 0,
    .gloomy_galleon_mermaid = 0,
    .gloomy_galleon_shipwreck_dk_tiny = 0,
    .gloomy_galleon_shipwreck_lanky_tiny = 0,
    .fungi_forest = 0,
    .gloomy_galleon_lighthouse = 0,
    .k_rool_barrel_tinys_mushroom_game = 0,
    .gloomy_galleon_mechanical_fish = 0,
    .fungi_forest_ant_hill = 0,
    .battle_arena_beaver_brawl = 0,
    .gloomy_galleon_barrel_blast = 1, // Reason: BBlast Course
    .fungi_forest_minecart = 1, // Reason: Locked Movement
    .fungi_forest_diddys_barn = 0,
    .fungi_forest_diddys_attic = 0,
    .fungi_forest_lankys_attic = 0,
    .fungi_forest_dks_barn = 0,
    .fungi_forest_spider = 0,
    .fungi_forest_front_part_of_mill = 0,
    .fungi_forest_rear_part_of_mill = 0,
    .fungi_forest_mushroom_puzzle = 0,
    .fungi_forest_giant_mushroom = 0,
    .stealthy_snoop_normal = 0,
    .mad_maze_maul_hard = 0,
    .stash_snatch_normal = 0,
    .mad_maze_maul_easy = 0,
    .mad_maze_maul_normal = 0,
    .fungi_forest_mushroom_leap = 0,
    .fungi_forest_shooting_game = 0,
    .crystal_caves = 0,
    .battle_arena_kritter_karnage = 0,
    .stash_snatch_easy = 0,
    .stash_snatch_hard = 0,
    .dk_rap = 1, // Reason: Cutscene Map
    .minecart_mayhem_easy = 1, // Reason: Locked Movement
    .busy_barrel_barrage_easy = 1, // Reason: Locked Movement
    .busy_barrel_barrage_normal = 1, // Reason: Locked Movement
    .main_menu = 1, // Reason: Locked Movement
    .title_screen_not_for_resale_version = 1, // Reason: Cutscene Map
    .crystal_caves_beetle_race = 1, // Reason: Locked Movement
    .fungi_forest_dogadon = 1, // Reason: Boss Map
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
    .splish_splash_salvage_normal = 0,
    .k_lumsy = 0,
    .crystal_caves_ice_castle = 0,
    .speedy_swing_sortie_easy = 0,
    .crystal_caves_igloo_diddy = 0,
    .krazy_kong_klamour_easy = 1, // Reason: Locked Movement
    .big_bug_bash_very_easy = 1, // Reason: Locked Movement
    .searchlight_seek_very_easy = 1, // Reason: Locked Movement
    .beaver_bother_easy = 1, // Reason: Locked Movement
    .creepy_castle_tower = 0,
    .creepy_castle_minecart = 0,
    .kong_battle_battle_arena = 1, // Reason: Multiplayer Map
    .creepy_castle_crypt_lanky_tiny = 0,
    .kong_battle_arena_1 = 1, // Reason: Multiplayer Map
    .frantic_factory_barrel_blast = 1, // Reason: BBlast Course
    .gloomy_galleon_pufftoss = 1, // Reason: Boss Map
    .creepy_castle_crypt_dk_diddy_chunky = 0,
    .creepy_castle_museum = 0,
    .creepy_castle_library = 0,
    .kremling_kosh_easy = 1, // Reason: Locked Movement
    .kremling_kosh_normal = 1, // Reason: Locked Movement
    .kremling_kosh_hard = 1, // Reason: Locked Movement
    .teetering_turtle_trouble_easy = 1, // Reason: Locked Movement
    .teetering_turtle_trouble_normal = 1, // Reason: Locked Movement
    .teetering_turtle_trouble_hard = 1, // Reason: Locked Movement
    .batty_barrel_bandit_easy = 1, // Reason: Locked Movement
    .batty_barrel_bandit_normal = 1, // Reason: Locked Movement
    .batty_barrel_bandit_hard = 1, // Reason: Locked Movement
    .mad_maze_maul_insane = 0,
    .stash_snatch_insane = 0,
    .stealthy_snoop_very_easy = 0,
    .stealthy_snoop_easy = 0,
    .stealthy_snoop_hard = 0,
    .minecart_mayhem_normal = 1, // Reason: Locked Movement
    .minecart_mayhem_hard = 1, // Reason: Locked Movement
    .busy_barrel_barrage_hard = 1, // Reason: Locked Movement
    .splish_splash_salvage_hard = 0,
    .splish_splash_salvage_easy = 0,
    .speedy_swing_sortie_normal = 0,
    .speedy_swing_sortie_hard = 0,
    .beaver_bother_normal = 1, // Reason: Locked Movement
    .beaver_bother_hard = 1, // Reason: Locked Movement
    .searchlight_seek_easy = 1, // Reason: Locked Movement
    .searchlight_seek_normal = 1, // Reason: Locked Movement
    .searchlight_seek_hard = 1, // Reason: Locked Movement
    .krazy_kong_klamour_normal = 1, // Reason: Locked Movement
    .krazy_kong_klamour_hard = 1, // Reason: Locked Movement
    .krazy_kong_klamour_insane = 1, // Reason: Locked Movement
    .peril_path_panic_very_easy = 1, // Reason: Locked Movement
    .peril_path_panic_easy = 1, // Reason: Locked Movement
    .peril_path_panic_normal = 1, // Reason: Locked Movement
    .peril_path_panic_hard = 1, // Reason: Locked Movement
    .big_bug_bash_easy = 1, // Reason: Locked Movement
    .big_bug_bash_normal = 1, // Reason: Locked Movement
    .big_bug_bash_hard = 1, // Reason: Locked Movement
    .creepy_castle_dungeon = 0,
    .hideout_helm_intro_story = 1, // Reason: Cutscene Map
    .dk_isles_dk_theatre = 1, // Reason: Cutscene Map
    .frantic_factory_mad_jack = 1, // Reason: Boss Map
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
    .k_rool_barrel_diddys_kremling_game = 0,
    .creepy_castle_chunkys_toolshed = 0,
    .creepy_castle_trash_can = 0,
    .creepy_castle_greenhouse = 0,
    .jungle_japes_lobby = 0,
    .hideout_helm_lobby = 0,
    .dks_house = 0,
    .rock_intro_story = 1, // Reason: Cutscene Map
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
    .enguarde_arena = 1, // Reason: Enguarde-Only Room
    .creepy_castle_car_race = 0,
    .crystal_caves_barrel_blast = 1, // Reason: BBlast Course
    .creepy_castle_barrel_blast = 1, // Reason: BBlast Course
    .fungi_forest_barrel_blast = 1, // Reason: BBlast Course
    .fairy_island = 0,
    .kong_battle_arena_2 = 1, // Reason: Multiplayer Map
    .rambi_arena = 1, // Reason: Rambi-Only Room
    .kong_battle_arena_3 = 1, // Reason: Multiplayer Map
    .creepy_castle_lobby = 0,
    .crystal_caves_lobby = 0,
    .dk_isles_snides_room = 0,
    .crystal_caves_army_dillo = 1, // Reason: Boss Map
    .angry_aztec_dogadon = 1, // Reason: Boss Map
    .training_grounds_end_sequence = 1, // Reason: Cutscene Map
    .creepy_castle_king_kut_out = 1, // Reason: Boss Map
    .crystal_caves_shack_diddy_upper_part = 0,
    .k_rool_barrel_diddys_rocketbarrel_game = 0,
    .k_rool_barrel_lankys_shooting_game = 0,
    .k_rool_fight_dk_phase = 1, // Reason: Boss Map
    .k_rool_fight_diddy_phase = 1, // Reason: Boss Map
    .k_rool_fight_lanky_phase = 1, // Reason: Boss Map
    .k_rool_fight_tiny_phase = 1, // Reason: Boss Map
    .k_rool_fight_chunky_phase = 1, // Reason: Boss Map
    .bloopers_ending = 1, // Reason: Cutscene Map
    .k_rool_barrel_chunkys_hidden_kremling_game = 0,
    .k_rool_barrel_tinys_pony_tail_twirl_game = 0,
    .k_rool_barrel_chunkys_shooting_game = 0,
    .k_rool_barrel_dks_rambi_game = 1, // Reason: Rambi-Only Room
    .k_lumsy_ending = 1, // Reason: Cutscene Map
    .k_rools_shoe = 1, // Reason: Boss Map
    .k_rools_arena = 1, // Reason: Cutscene Map
};

static const unsigned char bad_movement_states[] = {
	//0x02, // First Person Camera
	//0x03, // First Person Camera (Water)
	0x04, // Fairy Camera
	0x05, // Fairy Camera (Water)
	0x06, // Locked (Bonus Barrel)
	0x15, // Slipping
	0x16, // Slipping
	0x18, // Baboon Blast Pad
	0x1B, // Simian Spring
	//0x1C, // Simian Slam // Note: As far as I know this doesn't break anything, so we'll save the CPU cycles
	0x20, // Falling/Splat, // Note: Prevents quick recovery from fall damage, and I guess maybe switching to avoid fall damage?
	0x2D, // Shockwave
	0x2E, // Chimpy Charge
	0x31, // Damaged
	0x32, // Stunlocked
	0x33, // Damaged
	0x35, // Damaged
	0x36, // Death
	0x37, // Damaged (Underwater)
	0x38, // Damaged
	0x39, // Shrinking
	0x42, // Barrel
	0x43, // Barrel (Underwater)
	0x44, // Baboon Blast Shot
	0x45, // Cannon Shot
	0x52, // Bananaporter
	0x53, // Monkeyport
	0x54, // Bananaporter (Multiplayer)
	0x56, // Locked
	0x57, // Swinging on Vine
	0x58, // Leaving Vine
	0x59, // Climbing Tree
	0x5A, // Leaving Tree
	0x5B, // Grabbed Ledge
	0x5C, // Pulling up on Ledge
	0x63, // Rocketbarrel // Note: Covered by crystal HUD check except for Helm & K. Rool
	0x64, // Taking Photo
	0x65, // Taking Photo
	0x67, // Instrument
	0x69, // Car
	0x6A, // Learning Gun // Note: Handled by map check
	0x6B, // Locked
	0x6C, // Feeding T&S // Note: Handled by map check
	0x6D, // Boat
	0x6E, // Baboon Balloon
	0x6F, // Updraft
	0x70, // GB Dance
	0x71, // Key Dance
	0x72, // Crown Dance
	0x73, // Loss Dance
	0x74, // Victory Dance
	0x78, // Gorilla Grab
	0x79, // Learning Move // Note: Handled by map check
	0x7A, // Locked
	0x7B, // Locked
	0x7C, // Trapped (spider miniBoss)
	0x7D, // Klaptrap Kong (beaver bother) // Note: Handled by map check
	0x83, // Fairy Refill
	0x87, // Entering Portal
	0x88, // Exiting Portal
};

static const short kong_flags[] = {0x181,0x6,0x46,0x42,0x75};
static unsigned char tag_countdown = 0;
static char can_tag_anywhere = 0;

int canTagAnywhere(int prev_crystals) {
    if (Player->strong_kong_ostand_bitfield & 0x100) {
        // Seasick
        return 0;
    }
    if (Player->collision_queue_pointer) {
        return 0;
    }
    
    if ((prev_crystals - 1) == CollectableBase.Crystals) {
        return 0;
    }
    if (CutsceneActive) {
        return 0;
    }
    if (ModelTwoTouchCount > 0) {
        return 0;
    }
    if (CurrentMap == 0x2A) {
        if (MapState & 0x10) {
            return 0;
        }
        if (hasTurnedInEnoughCBs()) {
            if (Player->zPos < 560.0f) {
                // Too close to boss door
                return 0;
            }
        }
    }
    for (int i = 0; i < LoadedActorCount; i++) {
        if (LoadedActorArray[i].actor) {
            int tested_type = LoadedActorArray[i].actor->actorType;
            if (tested_type == 48) { // Coconut
                return 0;
            } else if (tested_type == 36) { // Peanut
                return 0;
            } else if (tested_type == 42) { // Grape
                return 0;
            } else if (tested_type == 43) { // Feather
                if (LoadedActorArray[i].actor->control_state == 0) {
                    return 0;
                }
            } else if (tested_type == 38) { // Pineapple
                return 0;
            }
        }
    }
    if (TBVoidByte & 3) {
        return 0;
    }
    if (tag_countdown != 0) {
        return 0;
    }
    int is_banned = *(unsigned char*)(&banned_map_btf + (CurrentMap >> 3)) & (0x80 >> (CurrentMap % 8));
    if (is_banned) {
        return 0;
    }
    int control_state = Player->control_state;
    for (int i = 0; i < sizeof(bad_movement_states); i++) {
        if (bad_movement_states[i] == control_state) {
            return 0;
        }
    }
    return 1;
}

int getTAState(void) {
    return can_tag_anywhere;
}

int getTagAnywhereKong(int direction) {
    int next_character = Character + direction;
    if (next_character < 0) {
        next_character = TAG_ANYWHERE_KONG_LIMIT - 1;
    } else if (next_character >= TAG_ANYWHERE_KONG_LIMIT) {
        next_character = 0;
    }
    int i = 0;
    int reached_limit = 0;
    while (i < TAG_ANYWHERE_KONG_LIMIT) {
        int pass = 0;
        if (checkFlag(kong_flags[next_character],0)) {
            pass = 1;
            if (Rando.perma_lose_kongs) {
                if (checkFlag(KONG_LOCKED_START + next_character,0)) {
                    if ((!curseRemoved()) && (!hasPermaLossGrace())) {
                        pass = 0;
                    }
                }
            }
        }
        if (pass) {
            break;
        } else {
            if ((i + 1) == TAG_ANYWHERE_KONG_LIMIT) {
                reached_limit = 1;
                return Character;
            } else {
                next_character = next_character + direction;
                if (next_character < 0) {
                    next_character = TAG_ANYWHERE_KONG_LIMIT - 1;
                } else if (next_character >= TAG_ANYWHERE_KONG_LIMIT) {
                    next_character = 0;
                }
            }
        }
        i++;
    }
    if (reached_limit) {
        return Character;
    } else {
        return next_character;
    }
}

static const unsigned char important_huds[] = {0,1};
static unsigned char important_huds_changed[] = {0,0};

void tagAnywhere(int prev_crystals) {
	if (Rando.tag_anywhere) {
		if (Player) {
            if (tag_countdown > 0) {
                tag_countdown -= 1;
            }
            if (CurrentMap == 0x2A) {
                if (tag_countdown == 2) {
                    HUD->item[0].hud_state = 1;
                    if (Player->control_state == 108) {
                        int world = getWorld(CurrentMap,0);
                        if (MovesBase[(int)Character].cb_count[world] > 0) {
                            HUD->item[0].hud_state = 0;
                        }
                    }
                } else if (tag_countdown == 1) {
                    if (Player->control_state == 108) {
                        int world = getWorld(CurrentMap,0);
                        if (MovesBase[(int)Character].cb_count[world] > 0) {
                            HUD->item[0].hud_state = 1;
                        }
                    }
                }
            } else {
                if (tag_countdown == 2) {
                    for (int i = 0; i < sizeof(important_huds); i++) {
                        if (important_huds_changed[i]) {
                            HUD->item[(int)important_huds[i]].hud_state = 0;
                        }
                    }
                } else if (tag_countdown == 1) {
                    for (int i = 0; i < sizeof(important_huds); i++) {
                        if (important_huds_changed[i]) {
                            HUD->item[(int)important_huds[i]].hud_state = 1;
                        }
                    }
                }
            }
            int can_ta = canTagAnywhere(prev_crystals);
            can_tag_anywhere = can_ta;
            if (!can_ta) {
                return;
            }
			if (Character < TAG_ANYWHERE_KONG_LIMIT) {
				int change = 0;
				if (NewlyPressedControllerInput.Buttons & D_Left) {
					change = -1;
				} else if (NewlyPressedControllerInput.Buttons & D_Right) {
					change = 1;
				} else {
					return;
				}
				if (change != 0) {
                    int next_character = getTagAnywhereKong(change);
					if (next_character != Character) {
						if (((MovesBase[next_character].weapon_bitfield & 1) == 0) || (Player->was_gun_out == 0)) {
                            Player->hand_state = 1;
                            Player->was_gun_out = 0;
                            // Without this, tags to and from Diddy mess up
                            if (next_character == 1) {
                                Player->hand_state = 0;
                            }
                        } else {
                            Player->hand_state = 2;
                            Player->was_gun_out = 1;
                            // Without this, tags to and from Diddy mess up
                            if (next_character == 1) {
                                Player->hand_state = 3;
                            }
                        };
                        // Fix HUD memes
                        if (CurrentMap == 0x2A) {
                            if (!hasTurnedInEnoughCBs()) {
                                tag_countdown = 3;
                                HUD->item[0].hud_state_timer = 0x100;
                                HUD->item[0].hud_state = 0;
                            }
                        } else {
                            for (int i = 0; i < sizeof(important_huds); i++) {
                                important_huds_changed[i] = 0;
                                if (HUD) {
                                    int hud_st = HUD->item[(int)important_huds[i]].hud_state;
                                    if ((hud_st == 1) || (hud_st == 2)) {
                                        tag_countdown = 3;
                                        HUD->item[(int)important_huds[i]].hud_state_timer = 0;
                                        HUD->item[(int)important_huds[i]].hud_state = 0;
                                        important_huds_changed[i] = 1;
                                    }
                                }
                            }
                        }
                        tagKong(next_character + 2);
						clearTagSlide(Player);
						Player->new_kong = next_character + 2;
					}
				}
			}
		}
	}
}

void tagAnywhereInit(int is_homing, int model2_id, int obj) {
    assessFlagMapping(CurrentMap, model2_id);
    coinCBCollectHandle(0, obj, is_homing);
}

void tagAnywhereAmmo(int player, int obj, int is_homing) {
    coinCBCollectHandle(player, obj, is_homing);
    if (player_count == 1) {
        displayItemOnHUD(2 + is_homing,0,0);
    }
}

void tagAnywhereBunch(int player, int obj, int is_homing) {
    coinCBCollectHandle(player, obj, is_homing);
    playSFX(Banana);
}