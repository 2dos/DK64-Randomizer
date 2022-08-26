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

static const movement_bitfield banned_movement_btf = {
    .null_state = 0,
    .idle_enemy = 0,
    .first_person_camera = 0,
    .first_person_camera_water = 0,
    .fairy_camera = 1, // Reason: HUD
    .fairy_camera_water = 1, // Reason: HUD
    .locked_bonus_barrel_0x6 = 1, // Reason: Locked Movement
    .minecart_idle = 0,
    .minecart_crouch = 0,
    .minecart_jump = 0,
    .minecart_left = 0,
    .minecart_right = 0,
    .idle = 0,
    .walking = 0,
    .skidding = 0,
    .sliding_beetle_race = 0,
    .sliding_beetle_race_left = 0,
    .sliding_beetle_race_right = 0,
    .sliding_beetle_race_forward = 0,
    .sliding_beetle_race_back = 0,
    .jumping_beetle_race = 0,
    .slipping = 1, // Reason: Visual
    .slipping_helm_slope = 1, // Reason: Visual
    .jumping = 0,
    .baboon_blast_pad = 1, // Reason: Visual
    .bouncing_mushroom = 0,
    .double_jump = 0,
    .simian_spring = 1, // Reason: Visual
    .simian_slam = 0,
    .long_jumping = 0,
    .falling = 0,
    .falling_gun = 0,
    .falling_or_splat = 1, // Reason: Cheese
    .falling_beetle_race = 0,
    .pony_tail_twirl = 0,
    .attacking_enemy = 0,
    .primate_punch = 0,
    .attacking_enemy_0x25 = 0,
    .ground_attack = 0,
    .attacking_enemy_0x27 = 0,
    .ground_attack_final = 0,
    .moving_ground_attack = 0,
    .aerial_attack = 0,
    .rolling = 0,
    .throwing_orange = 0,
    .shockwave = 1, // Reason: Crash
    .chimpy_charge = 1, // Reason: Visual
    .charging_rambi = 0,
    .bouncing = 0,
    .damaged = 1, // Reason: Glitch
    .stunlocked_kasplat = 1, // Reason: Crash
    .damaged_mad_jack = 1, // Reason: Crash
    .unknown_0x34 = 0,
    .damaged_klump_knockback = 1, // Reason: Glitch
    .death = 1, // Reason: Glitch
    .damaged_underwater = 1, // Reason: Glitch
    .damaged_vehicle = 1, // Reason: Glitch
    .shrinking = 1, // Reason: Glitch
    .unknown_0x3a = 0,
    .death_dogadon = 0,
    .crouching = 0,
    .uncrouching = 0,
    .backflip = 0,
    .entering_orangstand = 0,
    .orangstand = 0,
    .jumping_orangstand = 0,
    .barrel_tag_barrel = 1, // Reason: Locked Movement
    .barrel_underwater = 1, // Reason: Locked Movement
    .baboon_blast_shot = 1, // Reason: Locked Movement
    .cannon_shot = 1, // Reason: Locked Movement
    .pushing_object = 0,
    .picking_up_object = 0,
    .idle_carrying_object = 0,
    .walking_carrying_object = 0,
    .dropping_object = 0,
    .throwing_object = 0,
    .jumping_carrying_object = 0,
    .throwing_object_air = 0,
    .surface_swimming = 0,
    .underwater = 0,
    .leaving_water = 0,
    .jumping_water = 0,
    .bananaporter = 1, // Reason: Locked Movement
    .monkeyport = 1, // Reason: Locked Movement
    .bananaport_multiplayer = 1, // Reason: Glitch
    .unknown_0x55 = 0,
    .locked_funky_and_candy = 1, // Reason: Locked Movement
    .swinging_on_vine = 1, // Reason: Crash
    .leaving_vine = 1, // Reason: Crash
    .climbing_tree = 1, // Reason: Crash
    .leaving_tree = 1, // Reason: Crash
    .grabbed_ledge = 1, // Reason: Crash
    .pulling_up_on_ledge = 1, // Reason: Crash
    .idle_gun = 0,
    .walking_gun = 0,
    .putting_away_gun = 0,
    .pulling_out_gun = 0,
    .jumping_gun = 0,
    .aiming_gun = 0,
    .rocketbarrel = 1, // Reason: Glitch
    .taking_photo = 1, // Reason: Glitch
    .taking_photo_underwater = 1, // Reason: Glitch
    .damaged_tnt_barrels = 0,
    .instrument = 1, // Reason: Glitch
    .unknown_0x68 = 0,
    .car_race = 1, // Reason: Locked Movement
    .learning_gun = 1, // Reason: Locked Movement
    .locked_bonus_barrel_0x6b = 1, // Reason: Locked Movement
    .feeding_tns = 1, // Reason: Locked Movement
    .boat = 1, // Reason: Locked Movement
    .baboon_balloon = 1, // Reason: Visual
    .updraft = 1, // Reason: Visual
    .gb_dance = 1, // Reason: Locked Movement
    .key_dance = 1, // Reason: Locked Movement
    .crown_dance = 1, // Reason: Locked Movement
    .loss_dance = 1, // Reason: Locked Movement
    .victory_dance = 1, // Reason: Locked Movement
    .vehicle_castle_car_race = 0,
    .entering_battle_crown = 0,
    .locked_cutscenes = 0,
    .gorilla_grab = 1, // Reason: Locked Movement
    .learning_move = 1, // Reason: Locked Movement
    .locked_car_race_loss = 1, // Reason: Locked Movement
    .locked_beetle_race_loss = 1, // Reason: Locked Movement
    .trapped = 1, // Reason: Locked Movement
    .klaptrap_kong = 1, // Reason: Glitch
    .surface_swimming_enguarde = 0,
    .underwater_enguarde = 0,
    .attacking_enguarde_surface = 0,
    .attacking_enguarde = 0,
    .leaving_water_enguarde = 0,
    .fairy_refill = 1, // Reason: Locked Movement
    .unknown_0x84 = 0,
    .main_menu = 0,
    .entering_main_menu = 0,
    .entering_portal = 1, // Reason: Locked Movement
    .exiting_portal = 1, // Reason: Locked Movement
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
    int offset = CurrentMap >> 3;
    int check = CurrentMap % 8;
    int is_banned = *(unsigned char*)((unsigned char*)(&banned_map_btf) + offset) & (0x80 >> check);
    if (is_banned) {
        return 0;
    }
    int control_state = Player->control_state;
    offset = control_state >> 3;
    check = control_state % 8;
    is_banned = *(unsigned char*)((unsigned char*)(&banned_movement_btf) + offset) & (0x80 >> check);

    if (is_banned) {
        return 0;
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

typedef struct sfx_cache_item {
    /* 0x000 */ unsigned short sfx;
    /* 0x002 */ unsigned char noise_buffer;
    /* 0x003 */ unsigned char sfx_count;
    /* 0x004 */ unsigned int last_played_f;
    /* 0x008 */ unsigned char sfx_delay;
    /* 0x009 */ unsigned char used;
    /* 0x00A */ unsigned short id;
    /* 0x00C */ unsigned char map_initiated;
} sfx_cache_item;

#define SFX_CACHE_SIZE 16
static sfx_cache_item sfx_cache_array[SFX_CACHE_SIZE];

void populateSFXCache(int sfx, int noise_buffer, int sfx_count, int sfx_delay, int id, int init_delay) {
    int has_pushed = 0;
    for (int i = 0; i < SFX_CACHE_SIZE; i++) {
        if (!has_pushed) {
            if (!sfx_cache_array[i].used) {
                sfx_cache_array[i].sfx = sfx;
                sfx_cache_array[i].noise_buffer = noise_buffer;
                sfx_cache_array[i].sfx_count = sfx_count - (init_delay == 0);
                sfx_cache_array[i].sfx_delay = sfx_delay;
                sfx_cache_array[i].last_played_f = ObjectModel2Timer;
                sfx_cache_array[i].map_initiated = CurrentMap;
                sfx_cache_array[i].used = sfx_count > (init_delay == 0);
                has_pushed = 1;
            }
        }
    }
    if (init_delay == 0) {
        playSFXFromObject(0,sfx,-1,127,0,noise_buffer,0.3f);
    }
}

void handleSFXCache(void) {
    for (int i = 0; i < SFX_CACHE_SIZE; i++) {
        if (sfx_cache_array[i].sfx_count == 0) {
            sfx_cache_array[i].used = 0;
        }
        if (sfx_cache_array[i].map_initiated != CurrentMap) {
            sfx_cache_array[i].used = 0;
        }
        if ((sfx_cache_array[i].used) && (ObjectModel2Timer >= (sfx_cache_array[i].last_played_f + sfx_cache_array[i].sfx_delay))) {
            playSFXFromObject(sfx_cache_array[i].id,sfx_cache_array[i].sfx,-1,127,0,sfx_cache_array[i].noise_buffer,0.3f);
            sfx_cache_array[i].sfx_count -= 1;
            sfx_cache_array[i].last_played_f = ObjectModel2Timer;
        }
    }
}

void tagAnywhereAmmo(int player, int obj, int is_homing) {
    coinCBCollectHandle(player, obj, is_homing);
    int id = 0;
    if (LatestCollectedObject) {
        id = LatestCollectedObject->id;
    }
    if (player_count == 1) {
        displayItemOnHUD(2 + is_homing,0,0);
        populateSFXCache(0x331,64,5,4,id,6);
    }
}

void tagAnywhereBunch(int player, int obj, int player_index) {
    coinCBCollectHandle(player, obj, player_index);
    int id = 0;
    if (LatestCollectedObject) {
        id = LatestCollectedObject->id;
    }
    populateSFXCache(Banana,64,5,3,id,0);
}