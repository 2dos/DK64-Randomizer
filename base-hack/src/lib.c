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
short tbarrel_flags[] = {
	FLAG_TBARREL_BARREL,
	FLAG_TBARREL_DIVE,
	FLAG_TBARREL_ORANGE,
	FLAG_TBARREL_VINE,
};
short bfi_move_flags[] = {
	FLAG_ABILITY_CAMERA,
	FLAG_ABILITY_SHOCKWAVE,
};
const short tnsportal_flags[] = {
	// Troff n Scoff portal clear flags
	FLAG_PORTAL_JAPES,
	FLAG_PORTAL_AZTEC,
	FLAG_PORTAL_FACTORY,
	FLAG_PORTAL_GALLEON,
	FLAG_PORTAL_FUNGI,
	FLAG_PORTAL_CAVES,
	FLAG_PORTAL_CASTLE,
};
const unsigned short slam_flags[] = {FLAG_ITEM_SLAM_0, FLAG_ITEM_SLAM_1, FLAG_ITEM_SLAM_2, FLAG_SHOPMOVE_SLAM_0, FLAG_SHOPMOVE_SLAM_1, FLAG_SHOPMOVE_SLAM_2};
const unsigned short belt_flags[] = {FLAG_ITEM_BELT_0, FLAG_ITEM_BELT_1, FLAG_SHOPMOVE_BELT_0, FLAG_SHOPMOVE_BELT_1};
const unsigned short instrument_flags[] = {FLAG_ITEM_INS_0, FLAG_ITEM_INS_1, FLAG_ITEM_INS_2, FLAG_SHOPMOVE_INS_0, FLAG_SHOPMOVE_INS_1, FLAG_SHOPMOVE_INS_2};
const unsigned char kong_pellets[] = {48,36,42,43,38};
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
static const unsigned char training_maps[] = {
	MAP_TBARREL_VINE,
	MAP_TBARREL_BARREL,
	MAP_TBARREL_DIVE,
	MAP_TBARREL_ORANGE,
};
static short shop_maps[] = {
	MAP_CRANKY,
	MAP_CANDY,
	MAP_FUNKY,
	MAP_SNIDE,
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
static const char overlay_indexes[] = {
	OVERLAY_NONE, // Test Map
	OVERLAY_MENU, // Funky's Store
	OVERLAY_ARCADE, // DK Arcade
	OVERLAY_BONUS, // K. Rool Barrel: Lanky's Maze
	OVERLAY_MINECART, // Jungle Japes: Mountain
	OVERLAY_MENU, // Cranky's Lab
	OVERLAY_MINECART, // Jungle Japes: Minecart
	OVERLAY_CRITTER, // Jungle Japes
	OVERLAY_BOSS, // Jungle Japes: Army Dillo
	OVERLAY_JETPAC, // Jetpac
	OVERLAY_BONUS, // Kremling Kosh! (very easy)
	OVERLAY_BONUS, // Stealthy Snoop! (normal, no logo)
	OVERLAY_NONE, // Jungle Japes: Shell
	OVERLAY_NONE, // Jungle Japes: Lanky's Cave
	OVERLAY_RACE, // Angry Aztec: Beetle Race
	OVERLAY_MENU, // Snide's H.Q.
	OVERLAY_CRITTER, // Angry Aztec: Tiny's Temple
	OVERLAY_NONE, // Hideout Helm
	OVERLAY_BONUS, // Teetering Turtle Trouble! (very easy)
	OVERLAY_NONE, // Angry Aztec: Five Door Temple (DK)
	OVERLAY_NONE, // Angry Aztec: Llama Temple
	OVERLAY_NONE, // Angry Aztec: Five Door Temple (Diddy)
	OVERLAY_NONE, // Angry Aztec: Five Door Temple (Tiny)
	OVERLAY_NONE, // Angry Aztec: Five Door Temple (Lanky)
	OVERLAY_NONE, // Angry Aztec: Five Door Temple (Chunky)
	OVERLAY_MENU, // Candy's Music Shop
	OVERLAY_NONE, // Frantic Factory
	OVERLAY_RACE, // Frantic Factory: Car Race
	OVERLAY_BOSS, // Hideout Helm (Level Intros, Game Over)
	OVERLAY_NONE, // Frantic Factory: Power Shed
	OVERLAY_CRITTER, // Gloomy Galleon
	OVERLAY_NONE, // Gloomy Galleon: K. Rool's Ship
	OVERLAY_BONUS, // Batty Barrel Bandit! (easy)
	OVERLAY_CRITTER, // Jungle Japes: Chunky's Cave
	OVERLAY_CRITTER, // DK Isles Overworld
	OVERLAY_BONUS, // K. Rool Barrel: DK's Target Game
	OVERLAY_NONE, // Frantic Factory: Crusher Room
	OVERLAY_NONE, // Jungle Japes: Barrel Blast
	OVERLAY_NONE, // Angry Aztec
	OVERLAY_RACE, // Gloomy Galleon: Seal Race
	OVERLAY_MENU, // Nintendo Logo
	OVERLAY_NONE, // Angry Aztec: Barrel Blast
	OVERLAY_CRITTER, // Troff 'n' Scoff
	OVERLAY_CRITTER, // Gloomy Galleon: Shipwreck (Diddy, Lanky, Chunky)
	OVERLAY_CRITTER, // Gloomy Galleon: Treasure Chest
	OVERLAY_CRITTER, // Gloomy Galleon: Mermaid
	OVERLAY_CRITTER, // Gloomy Galleon: Shipwreck (DK, Tiny)
	OVERLAY_CRITTER, // Gloomy Galleon: Shipwreck (Lanky, Tiny)
	OVERLAY_NONE, // Fungi Forest
	OVERLAY_NONE, // Gloomy Galleon: Lighthouse
	OVERLAY_BONUS, // K. Rool Barrel: Tiny's Mushroom Game
	OVERLAY_NONE, // Gloomy Galleon: Mechanical Fish
	OVERLAY_NONE, // Fungi Forest: Ant Hill
	OVERLAY_BONUS, // Battle Arena: Beaver Brawl!
	OVERLAY_NONE, // Gloomy Galleon: Barrel Blast
	OVERLAY_MINECART, // Fungi Forest: Minecart
	OVERLAY_CRITTER, // Fungi Forest: Diddy's Barn
	OVERLAY_NONE, // Fungi Forest: Diddy's Attic
	OVERLAY_NONE, // Fungi Forest: Lanky's Attic
	OVERLAY_NONE, // Fungi Forest: DK's Barn
	OVERLAY_BOSS, // Fungi Forest: Spider
	OVERLAY_NONE, // Fungi Forest: Front Part of Mill
	OVERLAY_NONE, // Fungi Forest: Rear Part of Mill
	OVERLAY_NONE, // Fungi Forest: Mushroom Puzzle
	OVERLAY_NONE, // Fungi Forest: Giant Mushroom
	OVERLAY_BONUS, // Stealthy Snoop! (normal)
	OVERLAY_BONUS, // Mad Maze Maul! (hard)
	OVERLAY_BONUS, // Stash Snatch! (normal)
	OVERLAY_BONUS, // Mad Maze Maul! (easy)
	OVERLAY_BONUS, // Mad Maze Maul! (normal)
	OVERLAY_NONE, // Fungi Forest: Mushroom Leap
	OVERLAY_NONE, // Fungi Forest: Shooting Game
	OVERLAY_CRITTER, // Crystal Caves
	OVERLAY_BONUS, // Battle Arena: Kritter Karnage!
	OVERLAY_BONUS, // Stash Snatch! (easy)
	OVERLAY_BONUS, // Stash Snatch! (hard)
	OVERLAY_CRITTER, // DK Rap
	OVERLAY_MINECART, // Minecart Mayhem! (easy)
	OVERLAY_BONUS, // Busy Barrel Barrage! (easy)
	OVERLAY_BONUS, // Busy Barrel Barrage! (normal)
	OVERLAY_MENU, // Main Menu
	OVERLAY_NONE, // Title Screen (Not For Resale Version)
	OVERLAY_RACE, // Crystal Caves: Beetle Race
	OVERLAY_BOSS, // Fungi Forest: Dogadon
	OVERLAY_NONE, // Crystal Caves: Igloo (Tiny)
	OVERLAY_NONE, // Crystal Caves: Igloo (Lanky)
	OVERLAY_NONE, // Crystal Caves: Igloo (DK)
	OVERLAY_NONE, // Creepy Castle
	OVERLAY_NONE, // Creepy Castle: Ballroom
	OVERLAY_NONE, // Crystal Caves: Rotating Room
	OVERLAY_NONE, // Crystal Caves: Shack (Chunky)
	OVERLAY_NONE, // Crystal Caves: Shack (DK)
	OVERLAY_NONE, // Crystal Caves: Shack (Diddy, middle part)
	OVERLAY_NONE, // Crystal Caves: Shack (Tiny)
	OVERLAY_NONE, // Crystal Caves: Lanky's Hut
	OVERLAY_NONE, // Crystal Caves: Igloo (Chunky)
	OVERLAY_BONUS, // Splish-Splash Salvage! (normal)
	OVERLAY_NONE, // K. Lumsy
	OVERLAY_NONE, // Crystal Caves: Ice Castle
	OVERLAY_BONUS, // Speedy Swing Sortie! (easy)
	OVERLAY_NONE, // Crystal Caves: Igloo (Diddy)
	OVERLAY_BONUS, // Krazy Kong Klamour! (easy)
	OVERLAY_BONUS, // Big Bug Bash! (very easy)
	OVERLAY_BONUS, // Searchlight Seek! (very easy)
	OVERLAY_BONUS, // Beaver Bother! (easy)
	OVERLAY_NONE, // Creepy Castle: Tower
	OVERLAY_MINECART, // Creepy Castle: Minecart
	OVERLAY_MULTI, // Kong Battle: Battle Arena
	OVERLAY_NONE, // Creepy Castle: Crypt (Lanky, Tiny)
	OVERLAY_MULTI, // Kong Battle: Arena 1
	OVERLAY_NONE, // Frantic Factory: Barrel Blast
	OVERLAY_BOSS, // Gloomy Galleon: Pufftoss
	OVERLAY_NONE, // Creepy Castle: Crypt (DK, Diddy, Chunky)
	OVERLAY_NONE, // Creepy Castle: Museum
	OVERLAY_NONE, // Creepy Castle: Library
	OVERLAY_BONUS, // Kremling Kosh! (easy)
	OVERLAY_BONUS, // Kremling Kosh! (normal)
	OVERLAY_BONUS, // Kremling Kosh! (hard)
	OVERLAY_BONUS, // Teetering Turtle Trouble! (easy)
	OVERLAY_BONUS, // Teetering Turtle Trouble! (normal)
	OVERLAY_BONUS, // Teetering Turtle Trouble! (hard)
	OVERLAY_BONUS, // Batty Barrel Bandit! (easy)
	OVERLAY_BONUS, // Batty Barrel Bandit! (normal)
	OVERLAY_BONUS, // Batty Barrel Bandit! (hard)
	OVERLAY_BONUS, // Mad Maze Maul! (insane)
	OVERLAY_BONUS, // Stash Snatch! (insane)
	OVERLAY_BONUS, // Stealthy Snoop! (very easy)
	OVERLAY_BONUS, // Stealthy Snoop! (easy)
	OVERLAY_BONUS, // Stealthy Snoop! (hard)
	OVERLAY_MINECART, // Minecart Mayhem! (normal)
	OVERLAY_MINECART, // Minecart Mayhem! (hard)
	OVERLAY_BONUS, // Busy Barrel Barrage! (hard)
	OVERLAY_BONUS, // Splish-Splash Salvage! (hard)
	OVERLAY_BONUS, // Splish-Splash Salvage! (easy)
	OVERLAY_BONUS, // Speedy Swing Sortie! (normal)
	OVERLAY_BONUS, // Speedy Swing Sortie! (hard)
	OVERLAY_BONUS, // Beaver Bother! (normal)
	OVERLAY_BONUS, // Beaver Bother! (hard)
	OVERLAY_BONUS, // Searchlight Seek! (easy)
	OVERLAY_BONUS, // Searchlight Seek! (normal)
	OVERLAY_BONUS, // Searchlight Seek! (hard)
	OVERLAY_BONUS, // Krazy Kong Klamour! (normal)
	OVERLAY_BONUS, // Krazy Kong Klamour! (hard)
	OVERLAY_BONUS, // Krazy Kong Klamour! (insane)
	OVERLAY_BONUS, // Peril Path Panic! (very easy)
	OVERLAY_BONUS, // Peril Path Panic! (easy)
	OVERLAY_BONUS, // Peril Path Panic! (normal)
	OVERLAY_BONUS, // Peril Path Panic! (hard)
	OVERLAY_BONUS, // Big Bug Bash! (easy)
	OVERLAY_BONUS, // Big Bug Bash! (normal)
	OVERLAY_BONUS, // Big Bug Bash! (hard)
	OVERLAY_NONE, // Creepy Castle: Dungeon
	OVERLAY_NONE, // Hideout Helm (Intro Story)
	OVERLAY_NONE, // DK Isles (DK Theatre)
	OVERLAY_BOSS, // Frantic Factory: Mad Jack
	OVERLAY_BONUS, // Battle Arena: Arena Ambush!
	OVERLAY_BONUS, // Battle Arena: More Kritter Karnage!
	OVERLAY_BONUS, // Battle Arena: Forest Fracas!
	OVERLAY_BONUS, // Battle Arena: Bish Bash Brawl!
	OVERLAY_BONUS, // Battle Arena: Kamikaze Kremlings!
	OVERLAY_BONUS, // Battle Arena: Plinth Panic!
	OVERLAY_BONUS, // Battle Arena: Pinnacle Palaver!
	OVERLAY_BONUS, // Battle Arena: Shockwave Showdown!
	OVERLAY_NONE, // Creepy Castle: Basement
	OVERLAY_NONE, // Creepy Castle: Tree
	OVERLAY_BONUS, // K. Rool Barrel: Diddy's Kremling Game
	OVERLAY_NONE, // Creepy Castle: Chunky's Toolshed
	OVERLAY_NONE, // Creepy Castle: Trash Can
	OVERLAY_NONE, // Creepy Castle: Greenhouse
	OVERLAY_CRITTER, // Jungle Japes Lobby
	OVERLAY_CRITTER, // Hideout Helm Lobby
	OVERLAY_NONE, // DK's House
	OVERLAY_NONE, // Rock (Intro Story)
	OVERLAY_CRITTER, // Angry Aztec Lobby
	OVERLAY_CRITTER, // Gloomy Galleon Lobby
	OVERLAY_CRITTER, // Frantic Factory Lobby
	OVERLAY_CRITTER, // Training Grounds
	OVERLAY_CRITTER, // Dive Barrel
	OVERLAY_CRITTER, // Fungi Forest Lobby
	OVERLAY_NONE, // Gloomy Galleon: Submarine
	OVERLAY_CRITTER, // Orange Barrel
	OVERLAY_CRITTER, // Barrel Barrel
	OVERLAY_CRITTER, // Vine Barrel
	OVERLAY_NONE, // Creepy Castle: Crypt
	OVERLAY_BONUS, // Enguarde Arena
	OVERLAY_RACE, // Creepy Castle: Car Race
	OVERLAY_NONE, // Crystal Caves: Barrel Blast
	OVERLAY_NONE, // Creepy Castle: Barrel Blast
	OVERLAY_NONE, // Fungi Forest: Barrel Blast
	OVERLAY_CRITTER, // Fairy Island
	OVERLAY_MULTI, // Kong Battle: Arena 2
	OVERLAY_BONUS, // Rambi Arena
	OVERLAY_MULTI, // Kong Battle: Arena 3
	OVERLAY_CRITTER, // Creepy Castle Lobby
	OVERLAY_CRITTER, // Crystal Caves Lobby
	OVERLAY_CRITTER, // DK Isles: Snide's Room
	OVERLAY_BOSS, // Crystal Caves: Army Dillo
	OVERLAY_BOSS, // Angry Aztec: Dogadon
	OVERLAY_NONE, // Training Grounds (End Sequence)
	OVERLAY_BOSS, // Creepy Castle: King Kut Out
	OVERLAY_NONE, // Crystal Caves: Shack (Diddy, upper part)
	OVERLAY_BONUS, // K. Rool Barrel: Diddy's Rocketbarrel Game
	OVERLAY_BONUS, // K. Rool Barrel: Lanky's Shooting Game
	OVERLAY_BOSS, // K. Rool Fight: DK Phase
	OVERLAY_BOSS, // K. Rool Fight: Diddy Phase
	OVERLAY_BOSS, // K. Rool Fight: Lanky Phase
	OVERLAY_BOSS, // K. Rool Fight: Tiny Phase
	OVERLAY_BOSS, // K. Rool Fight: Chunky Phase
	OVERLAY_NONE, // Bloopers Ending
	OVERLAY_BONUS, // K. Rool Barrel: Chunky's Hidden Kremling Game
	OVERLAY_BONUS, // K. Rool Barrel: Tiny's Pony Tail Twirl Game
	OVERLAY_BONUS, // K. Rool Barrel: Chunky's Shooting Game
	OVERLAY_BONUS, // K. Rool Barrel: DK's Rambi Game
	OVERLAY_NONE, // K. Lumsy Ending
	OVERLAY_BOSS, // K. Rool's Shoe
	OVERLAY_NONE, // K. Rool's Arena
};
const actor_bitfield big_head_actors = {
	// 0
	.unknown_0 = 0,
	.unknown_1 = 0,
	.dk = 1,
	.diddy = 1,
	.lanky = 1,
	.tiny = 1,
	.chunky = 1,
	.krusha = 1,
	.rambi = 1,
	.enguarde = 1,
	// 10
	.unknown_10 = 0,
	.unknown_11 = 0,
	.loading_zone_controller = 0,
	.object_model_2_controller = 0,
	.unknown_14 = 0,
	.unknown_15 = 0,
	.unknown_16 = 0,
	.cannon_barrel = 0,
	.rambi_crate = 0,
	.barrel_diddy_5di = 0,
	// 20
	.camera_focus_point = 0,
	.pushable_box = 0,
	.barrel_spawner = 0,
	.cannon = 0,
	.race_hoop = 0,
	.hunky_chunky_barrel = 0,
	.tnt_barrel = 0,
	.tnt_barrel_spawner = 0,
	.bonus_barrel = 0,
	.minecart = 0,
	// 30
	.fireball = 0,
	.bridge_castle = 0,
	.swinging_light = 0,
	.vine = 0,
	.kremling_kosh_controller = 0,
	.melon_projectile = 0,
	.peanut = 0,
	.rocketbarrel = 0,
	.pineapple = 0,
	.large_brown_bridge = 0,
	// 40
	.mini_monkey_barrel = 0,
	.orange = 0,
	.grape = 0,
	.feather = 0,
	.laser = 0,
	.golden_banana = 0,
	.barrel_gun = 0,
	.watermelon_slice = 0,
	.coconut = 0,
	.rocketbarrel_49 = 0,
	// 50
	.lime = 0,
	.ammo_crate = 0,
	.orange_pickup = 0,
	.banana_coin = 0,
	.dk_coin = 0,
	.small_explosion = 0,
	.orangstand_sprint_barrel = 0,
	.strong_kong_barrel = 0,
	.swinging_light_58 = 0,
	.fireball_59 = 0,
	// 60
	.bananaporter = 0,
	.boulder = 0,
	.minecart_62 = 0,
	.vase_o = 0,
	.vase_colon = 0,
	.vase_triangle = 0,
	.vase_plus = 0,
	.cannon_ball = 0,
	.unknown_68 = 0,
	.vine_69 = 0,
	// 70
	.counter = 0,
	.kremling_red = 1,
	.boss_key = 0,
	.cannon_73 = 0,
	.cannon_ball_74 = 0,
	.blueprint_diddy = 0,
	.blueprint_chunky = 0,
	.blueprint_lanky = 0,
	.blueprint_dk = 0,
	.blueprint_tiny = 0,
	// 80
	.minecart_80 = 0,
	.fire_spawner_dogadon = 0,
	.boulder_debris = 0,
	.spider_web = 0,
	.steel_keg_spawner = 0,
	.steel_keg = 0,
	.crown = 0,
	.minecart_87 = 0,
	.unknown_88 = 0,
	.fire = 0,
	// 90
	.ice_wall = 0,
	.balloon_diddy = 0,
	.stalactite = 0,
	.rock_debris = 0,
	.car = 0,
	.pause_menu = 0,
	.hunky_chunky_barrel_dogadon = 0,
	.tnt_barrel_spawner_dogadon = 0,
	.tag_barrel = 0,
	.fireball_99 = 0,
	// 100
	.pad_1_diddy_5di = 0,
	.pad_2_diddy_5di = 0,
	.pad_3_diddy_5di = 0,
	.pad_4_diddy_5di = 0,
	.pad_5_diddy_5di = 0,
	.pad_6_diddy_5di = 0,
	.kong_reflection = 0,
	.bonus_barrel_hideout_helm = 0,
	.unknown_108 = 0,
	.race_checkpoint = 0,
	// 110
	.cb_bunch = 0,
	.balloon_chunky = 0,
	.balloon_tiny = 0,
	.balloon_lanky = 0,
	.balloon_dk = 0,
	.klumsys_cage = 0,
	.chain = 0,
	.beanstalk = 0,
	.yellow_qmark = 0,
	.cb_single_blue = 0,
	// 120
	.cb_single_yellow = 0,
	.crystal_coconut = 0,
	.dk_coin_122 = 0,
	.kong_mirror = 0,
	.barrel_gun_124 = 0,
	.barrel_gun_125 = 0,
	.fly_swatter = 0,
	.searchlight = 0,
	.headphones = 0,
	.enguarde_crate = 0,
	// 130
	.apple = 0,
	.worm = 0,
	.enguarde_crate_unused = 0,
	.barrel = 0,
	.training_barrel = 0,
	.boombox = 0,
	.tag_barrel_136 = 0,
	.tag_barrel_137 = 0,
	.b_locker = 0,
	.rainbow_coin_patch = 0,
	// 140
	.rainbow_coin = 0,
	.unknown_141 = 0,
	.unknown_142 = 0,
	.unknown_143 = 0,
	.unknown_144 = 0,
	.cannon_seasick_chunky = 0,
	.unknown_146 = 0,
	.balloon_unused_k_rool = 0,
	.rope = 0,
	.banana_barrel = 0,
	// 150
	.banana_barrel_spawner = 0,
	.unknown_151 = 0,
	.unknown_152 = 0,
	.unknown_153 = 0,
	.unknown_154 = 0,
	.unknown_155 = 0,
	.wrinkly = 0,
	.unknown_157 = 0,
	.unknown_158 = 0,
	.unknown_159 = 0,
	// 160
	.unknown_160 = 0,
	.unknown_161 = 0,
	.unknown_162 = 0,
	.banana_fairy_bfi = 1,
	.ice_tomato = 0,
	.tag_barrel_king_kut_out = 0,
	.king_kut_out_part = 0,
	.cannon_167 = 0,
	.unknown_168 = 0,
	.puftup = 0,
	// 170
	.damage_source = 0,
	.orange_171 = 0,
	.unknown_172 = 0,
	.cutscene_controller = 0,
	.unknown_174 = 0,
	.kaboom = 0,
	.timer = 0,
	.timer_controller = 0,
	.beaver = 1,
	.shockwave_mad_jack = 0,
	// 180
	.krash = 1,
	.book = 0,
	.klobber = 0,
	.zinger = 0,
	.snide = 1,
	.army_dillo = 0, // Causes collision issues with the TNT Barrel
	.kremling = 1,
	.klump = 1,
	.camera = 0,
	.cranky = 1,
	// 190
	.funky = 1,
	.candy = 1,
	.beetle = 1,
	.mermaid = 1,
	.vulture = 0,
	.squawks = 0,
	.cutscene_dk = 1,
	.cutscene_diddy = 1,
	.cutscene_lanky = 1,
	.cutscene_tiny = 1,
	// 200
	.cutscene_chunky = 1,
	.llama = 1,
	.fairy_picture = 0,
	.padlock_tns = 0,
	.mad_jack = 0, // Causes him to jump to the ceiling?
	.klaptrap = 1,
	.zinger_206 = 0,
	.vulture_race = 1,
	.klaptrap_purple = 1,
	.klaptrap_red = 1,
	// 210
	.getout_controller = 0,
	.klaptrap_skeleton = 0,
	.beaver_gold = 1,
	.fire_column_spawner = 0,
	.minecart_tnt = 0,
	.minecart_tnt_215 = 0,
	.puftoss = 0, // Inconsequential
	.unknown_217 = 0,
	.handle = 0,
	.slot = 0,
	// 220
	.cannon_seasick_chunky_220 = 0,
	.light_piece = 0,
	.banana_peel = 0,
	.fireball_spawner = 0,
	.mushroom_man = 0,
	.unknown_225 = 0,
	.troff = 1,
	.k_rools_foot = 0,
	.bad_hit_detection_man = 0,
	.k_rools_toe = 0,
	// 230
	.ruler = 0,
	.toy_box = 0,
	.text_overlay = 0,
	.squawks_233 = 0,
	.scoff = 1,
	.robo_kremling = 1,
	.dogadon = 1,
	.unknown_237 = 0,
	.kremling_238 = 1,
	.bongos = 0,
	// 240
	.spotlight_fish = 0,
	.kasplat_dk = 1,
	.kasplat_diddy = 1,
	.kasplat_lanky = 1,
	.kasplat_tiny = 1,
	.kasplat_chunky = 1,
	.mechanical_fish = 0,
	.seal = 1,
	.banana_fairy = 1,
	.squawks_with_spotlight = 0,
	// 250
	.owl = 1,
	.spider_miniboss = 1,
	.rabbit = 1,
	.nintendo_logo = 0,
	.cutscene_object = 1,
	.shockwave = 0,
	.minigame_controller = 0,
	.fire_breath_spawner = 0,
	.shockwave_258 = 0,
	.guard = 0, // Would be funny, but it extends their arm
	// 260
	.text_overlay_260 = 0,
	.robo_zinger = 0,
	.krossbones = 1,
	.fire_shockwave_dogadon = 0,
	.squawks_264 = 0,
	.light_beam = 0,
	.dk_rap_controller = 0,
	.shuri = 0,
	.gimpfish = 0,
	.mr_dice = 0,
	// 270
	.sir_domino = 0,
	.mr_dice_271 = 0,
	.rabbit_272 = 0,
	.fireball_with_glasses = 0,
	.unknown_274 = 0,
	.k_lumsy = 1,
	.spiderling = 1,
	.squawks_277 = 0,
	.projectile = 0,
	.trap_bubble = 0,
	// 280
	.spider_silk_string = 0,
	.k_rool_dk_phase = 1,
	.retexturing_controller = 0,
	.skeleton_head = 0,
	.unknown_284 = 0,
	.bat = 0,
	.giant_clam = 0,
	.unknown_287 = 0,
	.tomato = 0,
	.kritter_in_a_sheet = 0,
	// 290
	.puftup_290 = 0,
	.kosha = 1,
	.k_rool_diddy_phase = 1,
	.k_rool_lanky_phase = 1,
	.k_rool_tiny_phase = 1,
	.k_rool_chunky_phase = 1,
	.unknown_296 = 0,
	.battle_crown_controller = 0,
	.unknown_298 = 0,
	.textbox = 0,
	// 300
	.snake = 1,
	.turtle = 1,
	.toy_car = 0,
	.toy_car_303 = 0,
	.camera_304 = 0,
	.missile = 0,
	.unknown_306 = 0,
	.unknown_307 = 0,
	.seal_308 = 0,
	.kong_logo_instrument = 0,
	// 310
	.spotlight = 0,
	.race_checkpoint_311 = 0,
	.minecart_tnt_312 = 0,
	.idle_particle = 0,
	.rareware_logo = 0,
	.unknown_315 = 0,
	.kong_tag_barrel = 1,
	.locked_kong_tag_barrel = 0,
	.unknown_318 = 0,
	.propeller_boat = 0,
	// 320
	.potion = 0,
	.fairy_refill = 0,
	.car_322 = 0,
	.enemy_car = 0,
	.text_overlay_controller = 0,
	.shockwave_325 = 0,
	.main_menu_controller = 0,
	.kong = 0,
	.klaptrap_328 = 0,
	.fairy = 0,
	// 330
	.bug = 0,
	.klaptrap_331 = 0,
	.big_bug_bash_controller = 0,
	.barrel_main_menu = 0,
	.padlock_k_lumsy = 0,
	.snides_menu = 0,
	.training_barrel_controller = 0,
	.multiplayer_model_main_menu = 0,
	.end_sequence_controller = 0,
	.arena_controller = 0,
	// 340
	.bug_340 = 0,
	.unknown_341 = 0,
	.try_again_dialog = 0,
	.pause_menu_343 = 0,
};


char* levels[] = {
    "ALL",
    "JUNGLE JAPES",
    "ANGRY AZTEC",
    "FRANTIC FACTORY",
    "GLOOMY GALLEON",
    "FUNGI FOREST",
    "CRYSTAL CAVES",
    "CREEPY CASTLE",
    "DK ISLES",
    "HIDEOUT HELM",
};

overlays getOverlayFromMap(maps map) {
	return overlay_indexes[map];
}

int inMinigame(maps map) {
	int offset = map >> 3;
    int check = map % 8;
    return *(unsigned char*)((unsigned char*)(&minigame_maps_btf) + offset) & (0x80 >> check);
}

int inShop(maps map, int include_snide) {
	return inShortList(map, &shop_maps[0], 3 + include_snide);
}

void playSFX(short sfxIndex) {
	playSound(sfxIndex, 0x7FFF, 63.0f, 1.0f, 0, 0);
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
	return normal_key_flags[index];
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

void setCollisionAddress(int actor_index, int is_custom, void* collision_info, int subdata) {
	if (is_custom) {
		actor_index = CUSTOM_ACTORS_START + actor_index;
	}
	actor_collisions[actor_index].collision_info = collision_info;
	actor_collisions[actor_index].unk_4 = subdata;
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

sprite_data_struct feather_gun_sprite = {
	.unk0 = 0xC7,
	.images_per_frame_horizontal = 1,
	.images_per_frame_vertical = 1,
	.codec = 2,
	.unk8 = -1,
	.table = 1,
	.width = 32,
	.height = 32,
	.image_count = 8,
	.images = {
		FEATHER_SPRITE_START + 0,
		FEATHER_SPRITE_START + 1,
		FEATHER_SPRITE_START + 2,
		FEATHER_SPRITE_START + 3,
		FEATHER_SPRITE_START + 4,
		FEATHER_SPRITE_START + 5,
		FEATHER_SPRITE_START + 6,
		FEATHER_SPRITE_START + 7,
	},
};

sprite_data_struct fool_overlay_sprite = {
	.unk0 = 0xC8,
	.images_per_frame_horizontal = 1,
	.images_per_frame_vertical = 1,
	.codec = 1,
	.unk8 = -1,
	.table = 1,
	.width = 40,
	.height = 16,
	.image_count = 1,
	.images = {
		FOOL_SPRITE_START,
	},
};

void giveGB(int kong, int level) {
	changeCollectableCount(8, 0, 1);
	displayItemOnHUD(8, 0, 0);
}

int getTotalCBCount(void) {
	int world = getWorld(CurrentMap,1);
	int count = 0;
	if (world < 7) {
		for (int kong = 0; kong < 5; kong++) {
			count += MovesBase[kong].cb_count[world] + MovesBase[kong].tns_cb_count[world];
		}
	}
	return count;
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
	playSound(0x147, 0x7FFF, 63.0f, 1.0f, 5, 0);
	changeCollectableCount(4, 0, 1);
}

void giveMelon(void) {
	applyDamageMask(0, 1);
}

int inShortList(int target, short* list, int count) {
	for (int i = 0; i < count; i++) {
		if (list[i] == target) {
			return 1;
		}
	}
	return 0;
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
	for (int i = 0; i < 6; i++) {
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

int inTraining(maps map) {
	for (int i = 0; i < sizeof(training_maps); i++) {
		if (map == training_maps[i]) {
			return 1;
		}
	}
	return 0;
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
	return checkFlagDuplicate(normal_key_flags[index], FLAGTYPE_PERMANENT);
}

void* malloc_wipe(int size) {
	void* ptr = dk_malloc(size);
	wipeMemory(ptr, size);
	return ptr;
}

int filterSong(int* song_write) {
	int song = *song_write;
	if ((Rando.disabled_music.events) || (Rando.disabled_music.shops)) {
		if (Rando.disabled_music.events) {
			if (music_types[song] == SONGTYPE_EVENT) {
				*song_write = 0;
				song = 0;
			}
		}
		if (Rando.disabled_music.shops) {
			if (
				((song == SONG_CRANKY) && (CurrentMap == MAP_CRANKY)) || // Cranky
				((song == SONG_FUNKY) && (CurrentMap == MAP_FUNKY)) || // Funky
				((song == SONG_CANDY) && (CurrentMap == MAP_CANDY)) || // Candy
				((song == SONG_SNIDE) && (CurrentMap == MAP_SNIDE)) // Snide
			) {
				*song_write = 0;
				song = 0;
			}
		}
	}
	initSongDisplay(song);
	return getTrackChannel(song);
}

int filterSong_Cancelled(songs song) {
	for (int i = 0; i < 12; i++) {
		if ((MusicTrackChannels[i] != SONG_SILENCE) && (MusicTrackChannels[i] != song)) {
			initSongDisplay(MusicTrackChannels[i]);
			break;
		}
	}
	return getTrackChannel(song);
}

int applyDamageMask(int player_index, int damage) {
	int applied_multiplier = Rando.damage_multiplier;
	if ((damage > 0) || (damage <= -12)) {
		// Health or death-dealing damage
		return applyDamage(player_index, damage);
	}
	if ((CurrentMap == MAP_CASTLEKUTOUT) && (CutsceneActive == 1) && (CutsceneIndex == 4)) {
		// King Kut out death cutscene, force to 0
		applied_multiplier = 0;
	} else if (Rando.hard_mode.lava_water) {
		if (Player->grounded_bitfield & 6) {
			// Underwater
			applied_multiplier = 1;
		}
	}
	return applyDamage(player_index, damage * applied_multiplier);
}

void* replaceWaterTexture(int table, int file, int unk0, int unk1) {
	if (file == 0xCF) {
		return getMapData(7, 0x3BA, unk0, unk1);
	}
	return getMapData(table, file, unk0, unk1);
}

void* replaceWaterTexture_spooky(int table, int file, int unk0, int unk1) {
	if (file == 0xCF) {
		return getMapData(7, 0x3D2, unk0, unk1);
	}
	return getMapData(table, file, unk0, unk1);
}

int isBounceObject(int object) {
	return inShortList(object, (short*)&bounce_objects[0], sizeof(bounce_objects) >> 1);
}

void* getFile(int size, int rom) {
	/**
	 * @brief Get file from ROM
	 */
	void* loc = dk_malloc(size);
	copyFromROM(rom,loc,&size,0,0,0,0);
	return loc;
}

int getMedalCount(void) {
	int regular_medals = countFlagArray(FLAG_MEDAL_JAPES_DK, 40, FLAGTYPE_PERMANENT);
	if (Rando.isles_cb_rando) {
		regular_medals += countFlagArray(FLAG_MEDAL_ISLES_DK, 5, FLAGTYPE_PERMANENT);
	}
	return regular_medals;
}

int isMedalFlag(int flag) {
	if (isFlagInRange(flag, FLAG_MEDAL_JAPES_DK, 40)) {
		return 1;
	}
	return isFlagInRange(flag, FLAG_MEDAL_ISLES_DK, 5);
}

typedef struct flag_counting_struct {
	/* 0x000 */ short flag_start;
	/* 0x002 */ unsigned char item_count;
	/* 0x003 */ unsigned char enabled;
	/* 0x004 */ short* flag_array;
} flag_counting_struct;

static flag_counting_struct flag_counters[] = {
	{.flag_start = 0, .item_count = 0, .enabled=0, .flag_array=(short*)0}, // REQITEM_NONE
	{.flag_start = 0, .item_count = 5, .enabled=2, .flag_array=(short*)&kong_flags}, // REQITEM_KONG
	{.flag_start = 0, .item_count = 0, .enabled=0, .flag_array=(short*)0}, // REQITEM_MOVE
	{.flag_start = 0, .item_count = 0, .enabled=0, .flag_array=(short*)0}, // REQITEM_GOLDENBANANA
	{.flag_start = FLAG_BP_JAPES_DK_HAS, .item_count = 40, .enabled=1, .flag_array=(short*)0}, // REQITEM_BLUEPRINT
	{.flag_start = FLAG_FAIRY_1, .item_count = 20, .enabled=1, .flag_array=(short*)0}, // REQITEM_FAIRY
	{.flag_start = 0, .item_count = 8, .enabled=2, .flag_array=(short*)&normal_key_flags}, // REQITEM_KEY
	{.flag_start = FLAG_CROWN_JAPES, .item_count = 10, .enabled=1, .flag_array=(short*)0}, // REQITEM_CROWN
	{.flag_start = 0, .item_count = 0, .enabled=0, .flag_array=(short*)0}, // REQITEM_COMPANYCOIN
	{.flag_start = 0, .item_count = 0, .enabled=0, .flag_array=(short*)0}, // REQITEM_MEDAL
	{.flag_start = FLAG_COLLECTABLE_BEAN, .item_count = 1, .enabled=1, .flag_array=(short*)0}, // REQITEM_BEAN
	{.flag_start = FLAG_PEARL_0_COLLECTED, .item_count = 5, .enabled=1, .flag_array=(short*)0}, // REQITEM_PEARL
	{.flag_start = FLAG_RAINBOWCOIN_0, .item_count = 16, .enabled=1, .flag_array=(short*)0}, // REQITEM_RAINBOWCOIN
	{.flag_start = FLAG_FAKEITEM, .item_count = 16, .enabled=1, .flag_array=(short*)0}, // REQITEM_ICETRAP
	{.flag_start = 0, .item_count = 0, .enabled=0, .flag_array=(short*)0}, // REQITEM_GAMEPERCENTAGE
	{.flag_start = 0, .item_count = 0, .enabled=0, .flag_array=(short*)0}, // REQITEM_COLOREDBANANA
};

static float percentage_rewards[] = {
	0.4f, // GBs
	0.5f, // Crowns
	0.25f, // Keys
	0.2f, // Medals
	0.5f, // RW Coins
	0.2f, // Fairies
	0.5f, // Nintendo Coins
};

float getPercentageOfItem(int index, float percentage_per_item) {
	float i_f = FileVariables[index];
	return i_f * percentage_per_item;
}

int getGamePercentage(void) {
	// This is a slightly modified version of the vanilla function
	updateFilePercentage();
	float percentage = 0;
	float target = 100.4f;
	if (Rando.isles_cb_rando) {
		percentage_rewards[4] = 0.18f;
		target = 100.5f;
	}
	for (int i = 0; i < 7; i++) {
		percentage += getPercentageOfItem(i, percentage_rewards[i]);
	}
	if (percentage == target) {
		return 101;
	}
	return percentage;
}

int getTotalMoveCount(void) {
	int count = MovesBase[0].simian_slam + MovesBase[0].ammo_belt;
	for (int kong = 0; kong < 5; kong++) {
		for (int i = 0; i < 3; i++) {
			if (MovesBase[kong].special_moves & (1 << i)) {
				count += 1;
			}
		}
		if (MovesBase[kong].weapon_bitfield & 1) {
			count += 1;
		}
		if (MovesBase[kong].instrument_bitfield & 1) {
			count += 1;
		}
	}
	for (int i = 0; i < 4; i++) {
		if (checkFlagDuplicate(tbarrel_flags[i], FLAGTYPE_PERMANENT)) {
			count += 1;
		}
		if (i > 0) {
			if (MovesBase[0].weapon_bitfield & (1 << i)) {
				count += 1;
			}
			if (MovesBase[0].instrument_bitfield & (1 << i)) {
				count += 1;
			}
		}
		if (i < 2) {
			if (checkFlagDuplicate(bfi_move_flags[i], FLAGTYPE_PERMANENT)) {
				count += 1;
			}
		}
	}
	return count;
}

dynamic_flag_icetrap_junk isIceTrapFlag(int flag) {
	if (isFlagInRange(flag, FLAG_FAKEITEM, 0x10)) {
		// Default Allocation
		return DYNFLAG_ICETRAP;
	}
	int junk_invasion = 0;
	int junk_capacity = 100;
	if (Rando.ice_trap_flag_alloc > 16) {
		junk_invasion = Rando.ice_trap_flag_alloc - 16;
		junk_capacity = 116 - Rando.ice_trap_flag_alloc;
	}
	if (isFlagInRange(flag, FLAG_JUNKITEM, junk_invasion)) {
		return DYNFLAG_ICETRAP;
	}
	if (isFlagInRange(flag, FLAG_JUNKITEM + junk_invasion, junk_capacity)) {
		return DYNFLAG_JUNK;
	}
	return DYNFLAG_NEITHER;
}

int getItemCountReq(requirement_item item) {
	int enabled_state = flag_counters[item].enabled;
	int item_count = flag_counters[item].item_count;
	int count = 0;
	if (enabled_state == 1) {
		if (item == REQITEM_ICETRAP) {
			int ice_trap_count = countFlagArray(flag_counters[item].flag_start, item_count, FLAGTYPE_PERMANENT);
			if (Rando.ice_trap_flag_alloc > 16) {
				int extra_count = Rando.ice_trap_flag_alloc - 16;
				ice_trap_count += countFlagArray(FLAG_JUNKITEM, extra_count, FLAGTYPE_PERMANENT);
			}
			return ice_trap_count;
		}
		return countFlagArray(flag_counters[item].flag_start, item_count, FLAGTYPE_PERMANENT);
	} else if (enabled_state == 2) {
		for (int i = 0; i < item_count; i++) {
			if (checkFlagDuplicate(flag_counters[item].flag_array[i], FLAGTYPE_PERMANENT)) {
				count += 1;
			}
		}
		return count;
	}
	switch(item) {
		case REQITEM_MOVE:
			return getTotalMoveCount();
		case REQITEM_GOLDENBANANA:
			return getTotalGBs();
		case REQITEM_COMPANYCOIN:
			if (checkFlagDuplicate(FLAG_COLLECTABLE_NINTENDOCOIN, FLAGTYPE_PERMANENT)) {
				count += 1;
			}
			if (checkFlagDuplicate(FLAG_COLLECTABLE_RAREWARECOIN, FLAGTYPE_PERMANENT)) {
				count += 1;
			}
			return count;
		case REQITEM_MEDAL:
			return getMedalCount();
		case REQITEM_GAMEPERCENTAGE:
			return getGamePercentage();
		case REQITEM_COLOREDBANANA:
			for (int world = 0; world < 7; world++) {
				for (int kong = 0; kong < 5; kong++) {
					count += MovesBase[kong].cb_count[world] + MovesBase[kong].tns_cb_count[world];
				}
			}
			return count;
		default:
			return 0;
	}
	return 0;
}

int isItemRequirementSatisfied(ItemRequirement* req) {
	if (req->item == REQITEM_NONE) {
		return 1;
	}
	return getItemCountReq(req->item) >= req->count;
}

purchase_struct* getShopData(vendors vendor, int kong, int level) {
	if (vendor == SHOP_CRANKY) {
		return &CrankyMoves_New[kong][level];
	}
	if (vendor == SHOP_FUNKY) {
		return &FunkyMoves_New[kong][level];
	}
	if (vendor == SHOP_CANDY) {
		return &CandyMoves_New[kong][level];
	}
	return 0;
}

void exitBoss(void) {
	for (int i = 0; i < 5; i++) {
		if (Rando.k_rool_order[i] == CurrentMap) {
			initiateTransition(MAP_ISLES, 0xC);
			return;
		}
	}
	initiateTransition(MAP_TROFFNSCOFF, 2);
}

int isKrushaAdjacentModel(int kong) {
	custom_kong_models slot_value = Rando.kong_models[kong];
	if (slot_value == KONGMODEL_KRUSHA) {
		return 1;
	}
	if (slot_value == KONGMODEL_KROOL_CUTSCENE) {
		return 1;
	}
	if (slot_value == KONGMODEL_KROOL_FIGHT) {
		return 1;
	}
	return 0;
}