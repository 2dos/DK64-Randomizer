/**
 * @file ice_trap.c
 * @author Ballaam
 * @brief All functionality related to the ice trap feature
 * @version 0.1
 * @date 2023-02-01
 * 
 * @copyright Copyright (c) 2023
 * 
 */
#include "../../include/common.h"

ICE_TRAP_TYPES ice_trap_queued = ICETRAP_OFF;

typedef enum ice_trap_map_state {
    ICETRAPREQ_BANNED,
    ICETRAPREQ_SUPER,
    ICETRAPREQ_ALLOW,
} ice_trap_map_state;

static const char banned_trap_maps[] = {
    /*.test_map =*/ ICETRAPREQ_ALLOW,
    /*.funkys_store =*/ ICETRAPREQ_BANNED, // Reason: Shop
    /*.dk_arcade =*/ ICETRAPREQ_BANNED, // Reason: Locked Movement
    /*.k_rool_barrel_lankys_maze =*/ ICETRAPREQ_SUPER, // Reason: Bonus
    /*.jungle_japes_mountain =*/ ICETRAPREQ_ALLOW,
    /*.crankys_lab =*/ ICETRAPREQ_BANNED, // Reason: Shop
    /*.jungle_japes_minecart =*/ ICETRAPREQ_BANNED, // Reason: Locked Movement
    /*.jungle_japes =*/ ICETRAPREQ_ALLOW,
    /*.jungle_japes_army_dillo =*/ ICETRAPREQ_SUPER, // Reason: Boss Map
    /*.jetpac =*/ ICETRAPREQ_BANNED, // Reason: Locked Movement
    /*.kremling_kosh_very_easy =*/ ICETRAPREQ_BANNED, // Reason: Locked Movement
    /*.stealthy_snoop_normal_no_logo =*/ ICETRAPREQ_BANNED, // Reason: Bonus
    /*.jungle_japes_shell =*/ ICETRAPREQ_ALLOW,
    /*.jungle_japes_lankys_cave =*/ ICETRAPREQ_ALLOW,
    /*.angry_aztec_beetle_race =*/ ICETRAPREQ_SUPER, // Reason: Locked Movement
    /*.snides_hq =*/ ICETRAPREQ_BANNED, // Reason: Shop
    /*.angry_aztec_tinys_temple =*/ ICETRAPREQ_ALLOW,
    /*.hideout_helm =*/ ICETRAPREQ_ALLOW,
    /*.teetering_turtle_trouble_very_easy =*/ ICETRAPREQ_BANNED, // Reason: Locked Movement
    /*.angry_aztec_five_door_temple_dk =*/ ICETRAPREQ_ALLOW,
    /*.angry_aztec_llama_temple =*/ ICETRAPREQ_ALLOW,
    /*.angry_aztec_five_door_temple_diddy =*/ ICETRAPREQ_ALLOW,
    /*.angry_aztec_five_door_temple_tiny =*/ ICETRAPREQ_ALLOW,
    /*.angry_aztec_five_door_temple_lanky =*/ ICETRAPREQ_ALLOW,
    /*.angry_aztec_five_door_temple_chunky =*/ ICETRAPREQ_ALLOW,
    /*.candys_music_shop =*/ ICETRAPREQ_BANNED, // Reason: Shop
    /*.frantic_factory =*/ ICETRAPREQ_ALLOW,
    /*.frantic_factory_car_race =*/ ICETRAPREQ_BANNED, // Reason: Locked Movement
    /*.hideout_helm_level_intros_game_over =*/ ICETRAPREQ_BANNED, // Reason: Cutscene Map
    /*.frantic_factory_power_shed =*/ ICETRAPREQ_ALLOW,
    /*.gloomy_galleon =*/ ICETRAPREQ_ALLOW,
    /*.gloomy_galleon_k_rools_ship =*/ ICETRAPREQ_ALLOW,
    /*.batty_barrel_bandit_very_easy =*/ ICETRAPREQ_BANNED, // Reason: Locked Movement
    /*.jungle_japes_chunkys_cave =*/ ICETRAPREQ_ALLOW,
    /*.dk_isles_overworld =*/ ICETRAPREQ_ALLOW,
    /*.k_rool_barrel_dks_target_game =*/ ICETRAPREQ_SUPER, // Reason: Bonus
    /*.frantic_factory_crusher_room =*/ ICETRAPREQ_ALLOW,
    /*.jungle_japes_barrel_blast =*/ ICETRAPREQ_SUPER, // Reason: BBlast Course
    /*.angry_aztec =*/ ICETRAPREQ_ALLOW,
    /*.gloomy_galleon_seal_race =*/ ICETRAPREQ_BANNED, // Reason: Locked Movement
    /*.nintendo_logo =*/ ICETRAPREQ_BANNED, // Reason: Cutscene Map
    /*.angry_aztec_barrel_blast =*/ ICETRAPREQ_SUPER, // Reason: BBlast Course
    /*.troff_n_scoff =*/ ICETRAPREQ_SUPER, // Reason: Bonus
    /*.gloomy_galleon_shipwreck_diddy_lanky_chunky =*/ ICETRAPREQ_ALLOW,
    /*.gloomy_galleon_treasure_chest =*/ ICETRAPREQ_ALLOW,
    /*.gloomy_galleon_mermaid =*/ ICETRAPREQ_ALLOW,
    /*.gloomy_galleon_shipwreck_dk_tiny =*/ ICETRAPREQ_ALLOW,
    /*.gloomy_galleon_shipwreck_lanky_tiny =*/ ICETRAPREQ_ALLOW,
    /*.fungi_forest =*/ ICETRAPREQ_ALLOW,
    /*.gloomy_galleon_lighthouse =*/ ICETRAPREQ_ALLOW,
    /*.k_rool_barrel_tinys_mushroom_game =*/ ICETRAPREQ_SUPER, // Reason: Bonus
    /*.gloomy_galleon_mechanical_fish =*/ ICETRAPREQ_ALLOW,
    /*.fungi_forest_ant_hill =*/ ICETRAPREQ_ALLOW,
    /*.battle_arena_beaver_brawl =*/ ICETRAPREQ_SUPER, // Reason: Bonus
    /*.gloomy_galleon_barrel_blast =*/ ICETRAPREQ_SUPER, // Reason: BBlast Course
    /*.fungi_forest_minecart =*/ ICETRAPREQ_BANNED, // Reason: Locked Movement
    /*.fungi_forest_diddys_barn =*/ ICETRAPREQ_ALLOW,
    /*.fungi_forest_diddys_attic =*/ ICETRAPREQ_ALLOW,
    /*.fungi_forest_lankys_attic =*/ ICETRAPREQ_ALLOW,
    /*.fungi_forest_dks_barn =*/ ICETRAPREQ_ALLOW,
    /*.fungi_forest_spider =*/ ICETRAPREQ_ALLOW,
    /*.fungi_forest_front_part_of_mill =*/ ICETRAPREQ_ALLOW,
    /*.fungi_forest_rear_part_of_mill =*/ ICETRAPREQ_ALLOW,
    /*.fungi_forest_mushroom_puzzle =*/ ICETRAPREQ_ALLOW,
    /*.fungi_forest_giant_mushroom =*/ ICETRAPREQ_ALLOW,
    /*.stealthy_snoop_normal =*/ ICETRAPREQ_SUPER, // Reason: Bonus
    /*.mad_maze_maul_hard =*/ ICETRAPREQ_SUPER, // Reason: Bonus
    /*.stash_snatch_normal =*/ ICETRAPREQ_SUPER, // Reason: Bonus
    /*.mad_maze_maul_easy =*/ ICETRAPREQ_SUPER, // Reason: Bonus
    /*.mad_maze_maul_normal =*/ ICETRAPREQ_SUPER, // Reason: Bonus
    /*.fungi_forest_mushroom_leap =*/ ICETRAPREQ_ALLOW,
    /*.fungi_forest_shooting_game =*/ ICETRAPREQ_ALLOW,
    /*.crystal_caves =*/ ICETRAPREQ_ALLOW,
    /*.battle_arena_kritter_karnage =*/ ICETRAPREQ_SUPER, // Reason: Bonus
    /*.stash_snatch_easy =*/ ICETRAPREQ_SUPER, // Reason: Bonus
    /*.stash_snatch_hard =*/ ICETRAPREQ_SUPER, // Reason: Bonus
    /*.dk_rap =*/ ICETRAPREQ_BANNED, // Reason: Cutscene Map
    /*.minecart_mayhem_easy =*/ ICETRAPREQ_BANNED, // Reason: Locked Movement
    /*.busy_barrel_barrage_easy =*/ ICETRAPREQ_BANNED, // Reason: Locked Movement
    /*.busy_barrel_barrage_normal =*/ ICETRAPREQ_BANNED, // Reason: Locked Movement
    /*.main_menu =*/ ICETRAPREQ_BANNED, // Reason: Locked Movement
    /*.title_screen_not_for_resale_version =*/ ICETRAPREQ_BANNED, // Reason: Cutscene Map
    /*.crystal_caves_beetle_race =*/ ICETRAPREQ_ALLOW,
    /*.fungi_forest_dogadon =*/ ICETRAPREQ_SUPER, // Reason: Boss Map
    /*.crystal_caves_igloo_tiny =*/ ICETRAPREQ_ALLOW,
    /*.crystal_caves_igloo_lanky =*/ ICETRAPREQ_ALLOW,
    /*.crystal_caves_igloo_dk =*/ ICETRAPREQ_ALLOW,
    /*.creepy_castle =*/ ICETRAPREQ_ALLOW,
    /*.creepy_castle_ballroom =*/ ICETRAPREQ_ALLOW,
    /*.crystal_caves_rotating_room =*/ ICETRAPREQ_ALLOW,
    /*.crystal_caves_shack_chunky =*/ ICETRAPREQ_ALLOW,
    /*.crystal_caves_shack_dk =*/ ICETRAPREQ_ALLOW,
    /*.crystal_caves_shack_diddy_middle_part =*/ ICETRAPREQ_ALLOW,
    /*.crystal_caves_shack_tiny =*/ ICETRAPREQ_ALLOW,
    /*.crystal_caves_lankys_hut =*/ ICETRAPREQ_ALLOW,
    /*.crystal_caves_igloo_chunky =*/ ICETRAPREQ_ALLOW,
    /*.splish_splash_salvage_normal =*/ ICETRAPREQ_SUPER, // Reason: Bonus
    /*.k_lumsy =*/ ICETRAPREQ_ALLOW,
    /*.crystal_caves_ice_castle =*/ ICETRAPREQ_ALLOW,
    /*.speedy_swing_sortie_easy =*/ ICETRAPREQ_SUPER, // Reason: Bonus
    /*.crystal_caves_igloo_diddy =*/ ICETRAPREQ_ALLOW,
    /*.krazy_kong_klamour_easy =*/ ICETRAPREQ_BANNED, // Reason: Locked Movement
    /*.big_bug_bash_very_easy =*/ ICETRAPREQ_BANNED, // Reason: Locked Movement
    /*.searchlight_seek_very_easy =*/ ICETRAPREQ_BANNED, // Reason: Locked Movement
    /*.beaver_bother_easy =*/ ICETRAPREQ_BANNED, // Reason: Locked Movement
    /*.creepy_castle_tower =*/ ICETRAPREQ_ALLOW,
    /*.creepy_castle_minecart =*/ ICETRAPREQ_ALLOW,
    /*.kong_battle_battle_arena =*/ ICETRAPREQ_BANNED, // Reason: Multiplayer Map
    /*.creepy_castle_crypt_lanky_tiny =*/ ICETRAPREQ_ALLOW,
    /*.kong_battle_arena_1 =*/ ICETRAPREQ_BANNED, // Reason: Multiplayer Map
    /*.frantic_factory_barrel_blast =*/ ICETRAPREQ_SUPER, // Reason: BBlast Course
    /*.gloomy_galleon_pufftoss =*/ ICETRAPREQ_BANNED, // Reason: Boss Map
    /*.creepy_castle_crypt_dk_diddy_chunky =*/ ICETRAPREQ_ALLOW,
    /*.creepy_castle_museum =*/ ICETRAPREQ_ALLOW,
    /*.creepy_castle_library =*/ ICETRAPREQ_ALLOW,
    /*.kremling_kosh_easy =*/ ICETRAPREQ_BANNED, // Reason: Locked Movement
    /*.kremling_kosh_normal =*/ ICETRAPREQ_BANNED, // Reason: Locked Movement
    /*.kremling_kosh_hard =*/ ICETRAPREQ_BANNED, // Reason: Locked Movement
    /*.teetering_turtle_trouble_easy =*/ ICETRAPREQ_BANNED, // Reason: Locked Movement
    /*.teetering_turtle_trouble_normal =*/ ICETRAPREQ_BANNED, // Reason: Locked Movement
    /*.teetering_turtle_trouble_hard =*/ ICETRAPREQ_BANNED, // Reason: Locked Movement
    /*.batty_barrel_bandit_easy =*/ ICETRAPREQ_BANNED, // Reason: Locked Movement
    /*.batty_barrel_bandit_normal =*/ ICETRAPREQ_BANNED, // Reason: Locked Movement
    /*.batty_barrel_bandit_hard =*/ ICETRAPREQ_BANNED, // Reason: Locked Movement
    /*.mad_maze_maul_insane =*/ ICETRAPREQ_SUPER, // Reason: Bonus
    /*.stash_snatch_insane =*/ ICETRAPREQ_SUPER, // Reason: Bonus
    /*.stealthy_snoop_very_easy =*/ ICETRAPREQ_SUPER, // Reason: Bonus
    /*.stealthy_snoop_easy =*/ ICETRAPREQ_SUPER, // Reason: Bonus
    /*.stealthy_snoop_hard =*/ ICETRAPREQ_SUPER, // Reason: Bonus
    /*.minecart_mayhem_normal =*/ ICETRAPREQ_BANNED, // Reason: Locked Movement
    /*.minecart_mayhem_hard =*/ ICETRAPREQ_BANNED, // Reason: Locked Movement
    /*.busy_barrel_barrage_hard =*/ ICETRAPREQ_BANNED, // Reason: Locked Movement
    /*.splish_splash_salvage_hard =*/ ICETRAPREQ_SUPER, // Reason: Bonus
    /*.splish_splash_salvage_easy =*/ ICETRAPREQ_SUPER, // Reason: Bonus
    /*.speedy_swing_sortie_normal =*/ ICETRAPREQ_SUPER, // Reason: Bonus
    /*.speedy_swing_sortie_hard =*/ ICETRAPREQ_SUPER, // Reason: Bonus
    /*.beaver_bother_normal =*/ ICETRAPREQ_BANNED, // Reason: Locked Movement
    /*.beaver_bother_hard =*/ ICETRAPREQ_BANNED, // Reason: Locked Movement
    /*.searchlight_seek_easy =*/ ICETRAPREQ_BANNED, // Reason: Locked Movement
    /*.searchlight_seek_normal =*/ ICETRAPREQ_BANNED, // Reason: Locked Movement
    /*.searchlight_seek_hard =*/ ICETRAPREQ_BANNED, // Reason: Locked Movement
    /*.krazy_kong_klamour_normal =*/ ICETRAPREQ_BANNED, // Reason: Locked Movement
    /*.krazy_kong_klamour_hard =*/ ICETRAPREQ_BANNED, // Reason: Locked Movement
    /*.krazy_kong_klamour_insane =*/ ICETRAPREQ_BANNED, // Reason: Locked Movement
    /*.peril_path_panic_very_easy =*/ ICETRAPREQ_BANNED, // Reason: Locked Movement
    /*.peril_path_panic_easy =*/ ICETRAPREQ_BANNED, // Reason: Locked Movement
    /*.peril_path_panic_normal =*/ ICETRAPREQ_BANNED, // Reason: Locked Movement
    /*.peril_path_panic_hard =*/ ICETRAPREQ_BANNED, // Reason: Locked Movement
    /*.big_bug_bash_easy =*/ ICETRAPREQ_BANNED, // Reason: Locked Movement
    /*.big_bug_bash_normal =*/ ICETRAPREQ_BANNED, // Reason: Locked Movement
    /*.big_bug_bash_hard =*/ ICETRAPREQ_BANNED, // Reason: Locked Movement
    /*.creepy_castle_dungeon =*/ ICETRAPREQ_ALLOW,
    /*.hideout_helm_intro_story =*/ ICETRAPREQ_BANNED, // Reason: Cutscene Map
    /*.dk_isles_dk_theatre =*/ ICETRAPREQ_BANNED, // Reason: Cutscene Map
    /*.frantic_factory_mad_jack =*/ ICETRAPREQ_SUPER, // Reason: Boss Map
    /*.battle_arena_arena_ambush =*/ ICETRAPREQ_SUPER, // Reason: Bonus
    /*.battle_arena_more_kritter_karnage =*/ ICETRAPREQ_SUPER, // Reason: Bonus
    /*.battle_arena_forest_fracas =*/ ICETRAPREQ_SUPER, // Reason: Bonus
    /*.battle_arena_bish_bash_brawl =*/ ICETRAPREQ_SUPER, // Reason: Bonus
    /*.battle_arena_kamikaze_kremlings =*/ ICETRAPREQ_SUPER, // Reason: Bonus
    /*.battle_arena_plinth_panic =*/ ICETRAPREQ_SUPER, // Reason: Bonus
    /*.battle_arena_pinnacle_palaver =*/ ICETRAPREQ_SUPER, // Reason: Bonus
    /*.battle_arena_shockwave_showdown =*/ ICETRAPREQ_SUPER, // Reason: Bonus
    /*.creepy_castle_basement =*/ ICETRAPREQ_ALLOW,
    /*.creepy_castle_tree =*/ ICETRAPREQ_ALLOW,
    /*.k_rool_barrel_diddys_kremling_game =*/ ICETRAPREQ_SUPER, // Reason: Bonus
    /*.creepy_castle_chunkys_toolshed =*/ ICETRAPREQ_ALLOW,
    /*.creepy_castle_trash_can =*/ ICETRAPREQ_ALLOW,
    /*.creepy_castle_greenhouse =*/ ICETRAPREQ_ALLOW,
    /*.jungle_japes_lobby =*/ ICETRAPREQ_ALLOW,
    /*.hideout_helm_lobby =*/ ICETRAPREQ_ALLOW,
    /*.dks_house =*/ ICETRAPREQ_ALLOW,
    /*.rock_intro_story =*/ ICETRAPREQ_BANNED, // Reason: Cutscene Map
    /*.angry_aztec_lobby =*/ ICETRAPREQ_ALLOW,
    /*.gloomy_galleon_lobby =*/ ICETRAPREQ_ALLOW,
    /*.frantic_factory_lobby =*/ ICETRAPREQ_ALLOW,
    /*.training_grounds =*/ ICETRAPREQ_ALLOW,
    /*.dive_barrel =*/ ICETRAPREQ_SUPER, // Reason: Bonus
    /*.fungi_forest_lobby =*/ ICETRAPREQ_ALLOW,
    /*.gloomy_galleon_submarine =*/ ICETRAPREQ_ALLOW,
    /*.orange_barrel =*/ ICETRAPREQ_SUPER, // Reason: Bonus
    /*.barrel_barrel =*/ ICETRAPREQ_SUPER, // Reason: Bonus
    /*.vine_barrel =*/ ICETRAPREQ_SUPER, // Reason: Bonus
    /*.creepy_castle_crypt =*/ ICETRAPREQ_ALLOW,
    /*.enguarde_arena =*/ ICETRAPREQ_BANNED, // Reason: Enguarde-Only Room
    /*.creepy_castle_car_race =*/ ICETRAPREQ_BANNED, // Reason: Bonus
    /*.crystal_caves_barrel_blast =*/ ICETRAPREQ_SUPER, // Reason: BBlast Course
    /*.creepy_castle_barrel_blast =*/ ICETRAPREQ_SUPER, // Reason: BBlast Course
    /*.fungi_forest_barrel_blast =*/ ICETRAPREQ_SUPER, // Reason: BBlast Course
    /*.fairy_island =*/ ICETRAPREQ_ALLOW,
    /*.kong_battle_arena_2 =*/ ICETRAPREQ_BANNED, // Reason: Multiplayer Map
    /*.rambi_arena =*/ ICETRAPREQ_BANNED, // Reason: Rambi-Only Room
    /*.kong_battle_arena_3 =*/ ICETRAPREQ_BANNED, // Reason: Multiplayer Map
    /*.creepy_castle_lobby =*/ ICETRAPREQ_ALLOW,
    /*.crystal_caves_lobby =*/ ICETRAPREQ_ALLOW,
    /*.dk_isles_snides_room =*/ ICETRAPREQ_ALLOW,
    /*.crystal_caves_army_dillo =*/ ICETRAPREQ_SUPER, // Reason: Boss Map
    /*.angry_aztec_dogadon =*/ ICETRAPREQ_SUPER, // Reason: Boss Map
    /*.training_grounds_end_sequence =*/ ICETRAPREQ_BANNED, // Reason: Cutscene Map
    /*.creepy_castle_king_kut_out =*/ ICETRAPREQ_SUPER, // Reason: Boss Map
    /*.crystal_caves_shack_diddy_upper_part =*/ ICETRAPREQ_ALLOW,
    /*.k_rool_barrel_diddys_rocketbarrel_game =*/ ICETRAPREQ_SUPER, // Reason: Bonus
    /*.k_rool_barrel_lankys_shooting_game =*/ ICETRAPREQ_SUPER, // Reason: Bonus
    /*.k_rool_fight_dk_phase =*/ ICETRAPREQ_SUPER, // Reason: Boss Map
    /*.k_rool_fight_diddy_phase =*/ ICETRAPREQ_SUPER, // Reason: Boss Map
    /*.k_rool_fight_lanky_phase =*/ ICETRAPREQ_SUPER, // Reason: Boss Map
    /*.k_rool_fight_tiny_phase =*/ ICETRAPREQ_SUPER, // Reason: Boss Map
    /*.k_rool_fight_chunky_phase =*/ ICETRAPREQ_SUPER, // Reason: Boss Map
    /*.bloopers_ending =*/ ICETRAPREQ_BANNED, // Reason: Cutscene Map
    /*.k_rool_barrel_chunkys_hidden_kremling_game =*/ ICETRAPREQ_SUPER, // Reason: Bonus
    /*.k_rool_barrel_tinys_pony_tail_twirl_game =*/ ICETRAPREQ_SUPER, // Reason: Bonus
    /*.k_rool_barrel_chunkys_shooting_game =*/ ICETRAPREQ_SUPER, // Reason: Bonus
    /*.k_rool_barrel_dks_rambi_game =*/ ICETRAPREQ_SUPER, // Reason: Rambi-Only Room
    /*.k_lumsy_ending =*/ ICETRAPREQ_BANNED, // Reason: Cutscene Map
    /*.k_rools_shoe =*/ ICETRAPREQ_SUPER, // Reason: Boss Map
    /*.k_rools_arena =*/ ICETRAPREQ_BANNED, // Reason: Cutscene Map
};
static const movement_bitfield banned_trap_movement = {
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
    .simian_spring = 0,
    .simian_slam = 0,
    .long_jumping = 0,
    .falling = 0,
    .falling_gun = 0,
    .falling_or_splat = 0,
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
    .vehicle_castle_car_race = 1, // Reason: Locked Movement
    .entering_battle_crown = 1, // Reason: Glitch
    .locked_cutscenes = 0,
    .gorilla_grab = 1, // Reason: Locked Movement
    .learning_move = 1, // Reason: Locked Movement
    .locked_car_race_loss = 1, // Reason: Locked Movement
    .locked_beetle_race_loss = 1, // Reason: Locked Movement
    .trapped = 1, // Reason: Locked Movement
    .klaptrap_kong = 1, // Reason: Glitch
    .surface_swimming_enguarde = 1, // Reason: Enguarde bone break
    .underwater_enguarde = 1, // Reason: Enguarde bone break
    .attacking_enguarde_surface = 1, // Reason: Enguarde bone break
    .attacking_enguarde = 1, // Reason: Enguarde bone break
    .leaving_water_enguarde = 1, // Reason: Enguarde bone break
    .fairy_refill = 1, // Reason: Locked Movement
    .unknown_0x84 = 0,
    .main_menu = 0,
    .entering_main_menu = 0,
    .entering_portal = 1, // Reason: Locked Movement
    .exiting_portal = 1, // Reason: Locked Movement
};

void customDamageCode(void) {
    if (Player) {
        if (checkDeathAction(Player)) {
            if (applyDamageMask(0, -1)) {
                int animation = 0x27;
                if (Player->grounded_bitfield & 4) {
                    animation = 0x29;
                }
                playAnimation(Player, animation);
                Player->control_state = 0x36;
                Player->control_state_progress = 0;
            }
            Player->invulnerability_timer = 100;
        }
    }
}

void trapPlayer_New(void) {
    Player->old_tag_state = -1;
    float val = 8.0f;
    float val2 = -30.0f;
    if ((Character >= 1) && (Character <= 3)) {
        val = 10.0f;
    } else if (Character == 6) {
        val = 15.0f;
    }
    if ((Character < 2) || (Character == 4) || (Character == 5)) {
        val2 = -20.0f;
    }
    Player->unk_1B0 = val;
    Player->yAccel = val2;
    if (Player->control_state != 0x7C) {
        Player->shockwave_timer = -1;
        Player->control_state = 0x7C;
        Player->control_state_progress = 0;
        playActorAnimation(Player, 0x13);
        spawnActor(0x117, 0xC5);
        LastSpawnedActor->parent = Player;
        Player->noclip = 0x3C;
    }
}

static const float bone_slow_scales[] = {0.4f, 0.38f, 0.3f};
static const char bone_slow_bones[] = {1, 5, 6};

void initIceTrap(void) {
    /**
     * @brief Initialize an ice trap
     */
    if ((ice_trap_queued == ICETRAP_BUBBLE) || (ice_trap_queued == ICETRAP_SUPERBUBBLE)) {
        trapPlayer_New();
        Player->trap_bubble_timer = 200;
    } else if (ice_trap_queued == ICETRAP_REVERSECONTROLS) {
        Player->strong_kong_ostand_bitfield |= 0x80;
        Player->trap_bubble_timer = 240;
    } else if (ice_trap_queued == ICETRAP_SLOWED) {
        for (int i = 0; i < 3; i++) {
            unkSpriteRenderFunc(0xF0);
            unkSpriteRenderFunc_1(1);
            loadSpriteFunction(0x8071F758);
            attachSpriteToBone((void*)0x80720E2C, bone_slow_scales[i], Player, bone_slow_bones[i], 2);
        }
        Player->strong_kong_ostand_bitfield |= 0x08000000;
        Player->trap_bubble_timer = 240;
    }
    playSFX(0x2D4); // K Rool Laugh
    if (Rando.ice_traps_damage) {
        customDamageCode();
    }
    ice_trap_queued = ICETRAP_OFF;
}

void queueIceTrap(ICE_TRAP_TYPES trap_type) {
    /**
     * @brief Call the ice trap queue-ing system
     */
    ice_trap_queued = trap_type;
}

int isBannedTrapMap(maps map, ICE_TRAP_TYPES type) {
    ice_trap_map_state ban_state = banned_trap_maps[map];
    if (ban_state == ICETRAPREQ_ALLOW) {
        return 0;
    }
    if (ban_state == ICETRAPREQ_SUPER) {
        if (type == ICETRAP_SUPERBUBBLE) {
            return 0;
        }
    }
    return 1;
}

void callIceTrap(void) {
    if (ice_trap_queued) {
        if (Player) {
            if (Player->collision_queue_pointer) {
                // Crashes
                return;
            }
            if (ObjectModel2Timer < 5) {
                return;
            }
            if (LZFadeoutProgress > 15.0f) {
                return;
            }
            if (Player->strong_kong_ostand_bitfield & 0x100) {
                // Seasick
                return;
            }
            if (IsAutowalking) {
                return;
            }
            if (Player->shockwave_timer != -1) {
                return;
            }
            // Check Map
            if (isBannedTrapMap(CurrentMap, ice_trap_queued)) {
                return;
            }
            // Check Control State
            if (getBitArrayValue(&banned_trap_movement, Player->control_state)) {
                return;
            }
            initIceTrap();
        }
    }
}