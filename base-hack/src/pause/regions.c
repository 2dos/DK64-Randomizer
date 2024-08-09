/**
 * @file regions.c
 * @author Ballaam
 * @brief Region Calculation Functions
 * @version 0.1
 * @date 2023-10-11
 * 
 * @copyright Copyright (c) 2023
 * 
 */
#include "../../include/common.h"

#define REFERENCE_PARENT -3
#define NO_HINT_REGION -2
#define INCONSISTENT_HINT_REGION -1

static char last_safe_parent = -1;
static char hint_region_text[32] = "";

static const char map_hint_regions[] = {
    /*
        Only for situations where an entire map is a singular hint region
        Key:
            -3 = Reference parent
            -2 = No hint region at all
            -1 = Hint region differs depending on context
            >= 0 = Hint region is always a certain enum value
    */
    NO_HINT_REGION, // test_map
    REFERENCE_PARENT, // funkys_store
    REGION_FACTORYSTORAGE, // dk_arcade
    REFERENCE_PARENT, // k_rool_barrel_lankys_maze
    REGION_JAPESCAVERNS, // jungle_japes_mountain
    REFERENCE_PARENT, // crankys_lab
    REGION_JAPESCAVERNS, // jungle_japes_minecart
    INCONSISTENT_HINT_REGION, // jungle_japes
    REGION_OTHERTNS, // jungle_japes_army_dillo
    REGION_JETPAC, // jetpac
    REFERENCE_PARENT, // kremling_kosh_very_easy
    REFERENCE_PARENT, // stealthy_snoop_normal_no_logo
    REGION_JAPESHIVE, // jungle_japes_shell
    REGION_JAPESCAVERNS, // jungle_japes_lankys_cave
    REGION_AZTECOASISTOTEM, // angry_aztec_beetle_race
    REFERENCE_PARENT, // snides_hq
    REGION_AZTECTINY, // angry_aztec_tinys_temple
    REGION_OTHERHELM, // hideout_helm
    REFERENCE_PARENT, // teetering_turtle_trouble_very_easy
    REGION_AZTECGETOUT, // angry_aztec_five_door_temple_dk
    REGION_AZTECLLAMA, // angry_aztec_llama_temple
    REGION_AZTECGETOUT, // angry_aztec_five_door_temple_diddy
    REGION_AZTECGETOUT, // angry_aztec_five_door_temple_tiny
    REGION_AZTECGETOUT, // angry_aztec_five_door_temple_lanky
    REGION_AZTECGETOUT, // angry_aztec_five_door_temple_chunky
    REFERENCE_PARENT, // candys_music_shop
    INCONSISTENT_HINT_REGION, // frantic_factory
    REGION_FACTORYRESEARCH, // frantic_factory_car_race
    NO_HINT_REGION, // hideout_helm_level_intros_game_over
    REGION_FACTORYSTORAGE, // frantic_factory_power_shed
    INCONSISTENT_HINT_REGION, // gloomy_galleon
    REGION_GALLEONLIGHTHOUSE, // gloomy_galleon_k_rools_ship
    REFERENCE_PARENT, // batty_barrel_bandit_very_easy
    REGION_JAPESCAVERNS, // jungle_japes_chunkys_cave
    INCONSISTENT_HINT_REGION, // dk_isles_overworld
    REFERENCE_PARENT, // k_rool_barrel_dks_target_game
    REGION_FACTORYPROD, // frantic_factory_crusher_room
    REGION_JAPESLOW, // jungle_japes_barrel_blast
    INCONSISTENT_HINT_REGION, // angry_aztec
    REGION_GALLEONSHIPYARD, // gloomy_galleon_seal_race
    NO_HINT_REGION, // nintendo_logo
    REGION_AZTECOASISTOTEM, // angry_aztec_barrel_blast
    REGION_OTHERTNS, // troff_n_scoff
    REGION_GALLEONSHIP, // gloomy_galleon_shipwreck_diddy_lanky_chunky
    REGION_GALLEONTREASURE, // gloomy_galleon_treasure_chest
    REGION_GALLEONLIGHTHOUSE, // gloomy_galleon_mermaid
    REGION_GALLEONSHIP, // gloomy_galleon_shipwreck_dk_tiny
    REGION_GALLEONSHIPYARD, // gloomy_galleon_shipwreck_lanky_tiny
    INCONSISTENT_HINT_REGION, // fungi_forest
    REGION_GALLEONLIGHTHOUSE, // gloomy_galleon_lighthouse
    REFERENCE_PARENT, // k_rool_barrel_tinys_mushroom_game
    REGION_GALLEONSHIPYARD, // gloomy_galleon_mechanical_fish
    REGION_FORESTOWL, // fungi_forest_ant_hill
    REFERENCE_PARENT, // battle_arena_beaver_brawl
    REGION_GALLEONLIGHTHOUSE, // gloomy_galleon_barrel_blast
    REGION_FORESTSTART, // fungi_forest_minecart
    REGION_FORESTMILLS, // fungi_forest_diddys_barn
    REGION_FORESTMILLS, // fungi_forest_diddys_attic
    REGION_FORESTMILLS, // fungi_forest_lankys_attic
    REGION_FORESTMILLS, // fungi_forest_dks_barn
    REGION_FORESTMILLS, // fungi_forest_spider
    REGION_FORESTMILLS, // fungi_forest_front_part_of_mill
    REGION_FORESTMILLS, // fungi_forest_rear_part_of_mill
    REGION_FORESTGMINT, // fungi_forest_mushroom_puzzle
    REGION_FORESTGMINT, // fungi_forest_giant_mushroom
    REFERENCE_PARENT, // stealthy_snoop_normal
    REFERENCE_PARENT, // mad_maze_maul_hard
    REFERENCE_PARENT, // stash_snatch_normal
    REFERENCE_PARENT, // mad_maze_maul_easy
    REFERENCE_PARENT, // mad_maze_maul_normal
    REGION_FORESTGMINT, // fungi_forest_mushroom_leap
    REGION_FORESTGMINT, // fungi_forest_shooting_game
    INCONSISTENT_HINT_REGION, // crystal_caves
    REFERENCE_PARENT, // battle_arena_kritter_karnage
    REFERENCE_PARENT, // stash_snatch_easy
    REFERENCE_PARENT, // stash_snatch_hard
    NO_HINT_REGION, // dk_rap
    REFERENCE_PARENT, // minecart_mayhem_easy
    REFERENCE_PARENT, // busy_barrel_barrage_easy
    REFERENCE_PARENT, // busy_barrel_barrage_normal
    NO_HINT_REGION, // main_menu
    NO_HINT_REGION, // title_screen_not_for_resale_version
    REGION_CAVESMAIN, // crystal_caves_beetle_race
    REGION_OTHERTNS, // fungi_forest_dogadon
    REGION_CAVESIGLOO, // crystal_caves_igloo_tiny
    REGION_CAVESIGLOO, // crystal_caves_igloo_lanky
    REGION_CAVESIGLOO, // crystal_caves_igloo_dk
    REGION_CASTLEEXT, // creepy_castle
    REGION_CASTLEROOMS, // creepy_castle_ballroom
    REGION_CAVESCABINS, // crystal_caves_rotating_room
    REGION_CAVESCABINS, // crystal_caves_shack_chunky
    REGION_CAVESCABINS, // crystal_caves_shack_dk
    REGION_CAVESCABINS, // crystal_caves_shack_diddy_middle_part
    REGION_CAVESCABINS, // crystal_caves_shack_tiny
    REGION_CAVESCABINS, // crystal_caves_lankys_hut
    REGION_CAVESIGLOO, // crystal_caves_igloo_chunky
    REFERENCE_PARENT, // splish_splash_salvage_normal
    REGION_ISLESKREM, // k_lumsy
    REGION_CAVESMAIN, // crystal_caves_ice_castle
    REFERENCE_PARENT, // speedy_swing_sortie_easy
    REGION_CAVESIGLOO, // crystal_caves_igloo_diddy
    REFERENCE_PARENT, // krazy_kong_klamour_easy
    REFERENCE_PARENT, // big_bug_bash_very_easy
    REFERENCE_PARENT, // searchlight_seek_very_easy
    REFERENCE_PARENT, // beaver_bother_easy
    REGION_CASTLEROOMS, // creepy_castle_tower
    REGION_CASTLEUNDERGROUND, // creepy_castle_minecart
    NO_HINT_REGION, // kong_battle_battle_arena
    REGION_CASTLEUNDERGROUND, // creepy_castle_crypt_lanky_tiny
    REFERENCE_PARENT, // kong_battle_arena_1
    REGION_FACTORYSTORAGE, // frantic_factory_barrel_blast
    REGION_OTHERTNS, // gloomy_galleon_pufftoss
    REGION_CASTLEUNDERGROUND, // creepy_castle_crypt_dk_diddy_chunky
    REGION_CASTLEROOMS, // creepy_castle_museum
    REGION_CASTLEROOMS, // creepy_castle_library
    REFERENCE_PARENT, // kremling_kosh_easy
    REFERENCE_PARENT, // kremling_kosh_normal
    REFERENCE_PARENT, // kremling_kosh_hard
    REFERENCE_PARENT, // teetering_turtle_trouble_easy
    REFERENCE_PARENT, // teetering_turtle_trouble_normal
    REFERENCE_PARENT, // teetering_turtle_trouble_hard
    REFERENCE_PARENT, // batty_barrel_bandit_easy
    REFERENCE_PARENT, // batty_barrel_bandit_normal
    REFERENCE_PARENT, // batty_barrel_bandit_hard
    REFERENCE_PARENT, // mad_maze_maul_insane
    REFERENCE_PARENT, // stash_snatch_insane
    REFERENCE_PARENT, // stealthy_snoop_very_easy
    REFERENCE_PARENT, // stealthy_snoop_easy
    REFERENCE_PARENT, // stealthy_snoop_hard
    REFERENCE_PARENT, // minecart_mayhem_normal
    REFERENCE_PARENT, // minecart_mayhem_hard
    REFERENCE_PARENT, // busy_barrel_barrage_hard
    REFERENCE_PARENT, // splish_splash_salvage_hard
    REFERENCE_PARENT, // splish_splash_salvage_easy
    REFERENCE_PARENT, // speedy_swing_sortie_normal
    REFERENCE_PARENT, // speedy_swing_sortie_hard
    REFERENCE_PARENT, // beaver_bother_normal
    REFERENCE_PARENT, // beaver_bother_hard
    REFERENCE_PARENT, // searchlight_seek_easy
    REFERENCE_PARENT, // searchlight_seek_normal
    REFERENCE_PARENT, // searchlight_seek_hard
    REFERENCE_PARENT, // krazy_kong_klamour_normal
    REFERENCE_PARENT, // krazy_kong_klamour_hard
    REFERENCE_PARENT, // krazy_kong_klamour_insane
    REFERENCE_PARENT, // peril_path_panic_very_easy
    REFERENCE_PARENT, // peril_path_panic_easy
    REFERENCE_PARENT, // peril_path_panic_normal
    REFERENCE_PARENT, // peril_path_panic_hard
    REFERENCE_PARENT, // big_bug_bash_easy
    REFERENCE_PARENT, // big_bug_bash_normal
    REFERENCE_PARENT, // big_bug_bash_hard
    REGION_CASTLEUNDERGROUND, // creepy_castle_dungeon
    NO_HINT_REGION, // hideout_helm_intro_story
    NO_HINT_REGION, // dk_isles_dk_theatre
    REGION_OTHERTNS, // frantic_factory_mad_jack
    REFERENCE_PARENT, // battle_arena_arena_ambush
    REFERENCE_PARENT, // battle_arena_more_kritter_karnage
    REFERENCE_PARENT, // battle_arena_forest_fracas
    REFERENCE_PARENT, // battle_arena_bish_bash_brawl
    REFERENCE_PARENT, // battle_arena_kamikaze_kremlings
    REFERENCE_PARENT, // battle_arena_plinth_panic
    REFERENCE_PARENT, // battle_arena_pinnacle_palaver
    REFERENCE_PARENT, // battle_arena_shockwave_showdown
    REGION_CASTLEUNDERGROUND, // creepy_castle_basement
    REGION_CASTLEEXT, // creepy_castle_tree
    REFERENCE_PARENT, // k_rool_barrel_diddys_kremling_game
    REGION_CASTLEEXT, // creepy_castle_chunkys_toolshed
    REGION_CASTLEEXT, // creepy_castle_trash_can
    REGION_CASTLEEXT, // creepy_castle_greenhouse
    REGION_ISLESLOBBIES0, // jungle_japes_lobby
    REGION_ISLESLOBBIES1, // hideout_helm_lobby
    REGION_ISLESMAIN, // dks_house
    NO_HINT_REGION, // rock_intro_story
    REGION_ISLESLOBBIES0, // angry_aztec_lobby
    REGION_ISLESLOBBIES0, // gloomy_galleon_lobby
    REGION_ISLESLOBBIES0, // frantic_factory_lobby
    REGION_ISLESMAIN, // training_grounds
    REFERENCE_PARENT, // dive_barrel
    REGION_ISLESLOBBIES0, // fungi_forest_lobby
    REGION_GALLEONSHIPYARD, // gloomy_galleon_submarine
    REFERENCE_PARENT, // orange_barrel
    REFERENCE_PARENT, // barrel_barrel
    REFERENCE_PARENT, // vine_barrel
    REGION_CASTLEUNDERGROUND, // creepy_castle_crypt
    REFERENCE_PARENT, // enguarde_arena
    REGION_CASTLEROOMS, // creepy_castle_car_race
    REGION_CAVESMAIN, // crystal_caves_barrel_blast
    REGION_CASTLEEXT, // creepy_castle_barrel_blast
    REGION_FORESTGMEXT, // fungi_forest_barrel_blast
    INCONSISTENT_HINT_REGION, // fairy_island
    REFERENCE_PARENT, // kong_battle_arena_2
    REFERENCE_PARENT, // rambi_arena
    REFERENCE_PARENT, // kong_battle_arena_3
    REGION_ISLESLOBBIES1, // creepy_castle_lobby
    REGION_ISLESLOBBIES1, // crystal_caves_lobby
    REGION_ISLESKREM, // dk_isles_snides_room
    REGION_OTHERTNS, // crystal_caves_army_dillo
    REGION_OTHERTNS, // angry_aztec_dogadon
    NO_HINT_REGION, // training_grounds_end_sequence
    REGION_OTHERTNS, // creepy_castle_king_kut_out
    REGION_CAVESCABINS, // crystal_caves_shack_diddy_upper_part
    REFERENCE_PARENT, // k_rool_barrel_diddys_rocketbarrel_game
    REFERENCE_PARENT, // k_rool_barrel_lankys_shooting_game
    REGION_ISLESKROOL, // k_rool_fight_dk_phase
    REGION_ISLESKROOL, // k_rool_fight_diddy_phase
    REGION_ISLESKROOL, // k_rool_fight_lanky_phase
    REGION_ISLESKROOL, // k_rool_fight_tiny_phase
    REGION_ISLESKROOL, // k_rool_fight_chunky_phase
    NO_HINT_REGION, // bloopers_ending
    REFERENCE_PARENT, // k_rool_barrel_chunkys_hidden_kremling_game
    REFERENCE_PARENT, // k_rool_barrel_tinys_pony_tail_twirl_game
    REFERENCE_PARENT, // k_rool_barrel_chunkys_shooting_game
    REFERENCE_PARENT, // k_rool_barrel_dks_rambi_game
    NO_HINT_REGION, // k_lumsy_ending
    REGION_ISLESKROOL, // k_rools_shoe
    REGION_ISLESKROOL, // k_rools_arena
};

int setHintRegion(void) {
    int current_region = map_hint_regions[CurrentMap];
    if (current_region >= 0) {
        return current_region;
    } else if (current_region == NO_HINT_REGION) {
        return -1;
    } else if (current_region == REFERENCE_PARENT) {
        if (inShop(CurrentMap, 1)) {
            int level = getWorld(CurrentMap, 1);
            if (level == 7) {
                return REGION_SHOPISLES;
            }
            if (level < 7) {
                return REGION_SHOPJAPES + level;
            }
        } else {
            int parent_map = 0;
            int parent_exit = 0;
            getParentMap(&parent_map, &parent_exit);
            if ((parent_map >= 0) && (parent_map < 216)) {
                current_region = map_hint_regions[parent_map];
                if (current_region >= 0) {
                    return current_region;
                } else if (last_safe_parent >= 0) {
                    return last_safe_parent;
                }
            }
        }
    }
    if (current_region == INCONSISTENT_HINT_REGION) {
        int chunk = Player->chunk;
        int px = Player->xPos;
        int py = Player->yPos;
        int pz = Player->zPos;
        switch (CurrentMap) {
            case MAP_FAIRYISLAND:
                if (chunk == 1) {
                    return REGION_ISLESRAREWARE;
                }
                return REGION_ISLESOUTER;
            case MAP_CAVES:
                if (chunk == 4) {
                    return REGION_CAVESCABINS;
                } else if ((chunk == 8) || (chunk == 13)) {
                    // 8 = Igloos, 13 = GK Room
                    return REGION_CAVESIGLOO;
                }
                return REGION_CAVESMAIN;
            case MAP_FUNGI:
                if ((chunk == 0) || (chunk == 7) || (chunk == 8) || (chunk == 9)) {
                    // 0 = Starting area, 7 = Green Tunnel, 8 = Apple area, 9 = Beanstalk Area
                    return REGION_FORESTSTART;
                } else if ((chunk >= 1) && (chunk <= 6)) {
                    // 1 = Blue Tunnel
                    // 2 = Mills Main
                    // 3 = Snide Area
                    // 4 = Dark Attic Area
                    // 5 = Thornvine Area
                    // 6 = Rear of Thornvine Barn
                    return REGION_FORESTMILLS;
                } else if ((chunk >= 12) && (chunk <= 17)) {
                    // 12 = Yellow Tunnel
                    // 13 = Start of owl tree area
                    // 14 = Owl Tree Area Main
                    // 15 = Rabbit Race Area
                    // 16 = Anthill Area
                    // 17 = Owl Tree Rocketbarrel Area
                    return REGION_FORESTOWL;
                }
                return REGION_FORESTGMEXT;
            case MAP_AZTEC:
                if ((chunk == 4) || (chunk == 12)) {
                    // 4 = Oasis, 12 = Totem
                    return REGION_AZTECOASISTOTEM;
                }
                return REGION_AZTECTUNNELS;
            case MAP_ISLES:
                {
                    if (chunk == 1) {
                        return REGION_ISLESKREM;
                    }
                    // Check fungi island
                    int dx = px - 2594;
                    int dz = pz - 922;
                    if (py > 1450) {
                        if (((dx * dx) + (dz * dz)) < 52900) {
                            return REGION_ISLESOUTER;
                        }
                    }
                    // check outside isles cylinder
                    dx = px - 2880;
                    dz = pz - 1624;
                    if (((dx * dx) + (dz * dz)) > 1270800) {
                        return REGION_ISLESOUTER;
                    }
                    return REGION_ISLESMAIN;
                    
                }
            case MAP_GALLEON:
                if ((chunk >= 9) && (chunk <= 11)) {
                    // 9 = Lighthouse Room
                    // 10 = Behind Ship Door
                    // 11 = Enguarde Room
                    return REGION_GALLEONLIGHTHOUSE;
                } else if ((chunk == 16) || (chunk == 17)) {
                    // 16 = Tunnel to treasure room
                    // 17 = Treasure Room
                    return REGION_GALLEONTREASURE;
                } else if ((chunk >= 0) && (chunk <= 8)) {
                    // 0 = Galleon Start
                    // 1 = Crossroads left
                    // 2 = Crossroads start
                    // 3 = Crossroads right
                    // 4 = Tunnel to Cannon Room
                    // 5 = Cannon Room
                    // 6 = Main Cranky Room
                    // 7 = Main Cranky Room 2
                    // 8 = Chest Room
                    return REGION_GALLEONCAVERNS;
                }
                return REGION_GALLEONSHIPYARD;
            case MAP_FACTORY:
                if (chunk == 12) {
                    // 12 = Tunnel to pole
                    // Chunk has 2 regions, subdivide by x position
                    if (px > 1860) {
                        return REGION_FACTORYTESTING;
                    }
                    return REGION_FACTORYSTART;
                }
                if ((chunk == 8) || (chunk == 9) || (chunk == 11)) {
                    // 8 = Tunnel to left
                    // 9 = Lobby with warps
                    // 11 = Lobby with switch
                    return REGION_FACTORYSTART;
                } else if ((chunk == 10) || ((chunk >= 13) && (chunk <= 19))) {
                    // 10 = Snide Area
                    // 13 = Pink Tunnel
                    // 14 = Number Game
                    // 15 = Pink Tunnel End
                    // 16 = Block Tower
                    // 17 = Number Game Tunnel
                    // 18 = Funky's
                    // 19 = Tunnel to R&D Pole
                    return REGION_FACTORYTESTING;
                } else if ((chunk >= 4) && (chunk <= 6)) {
                    // 4 = Tunnel to Storage
                    // 5 = Production Room
                    // 6 = Tunnel to Hatch
                    return REGION_FACTORYPROD;
                } else if (chunk == 7) {
                    // 7 = Room with the Hatch
                    // Chunk has 2 regions, subdivide by y position
                    if (py < 804) {
                        return REGION_FACTORYPROD;
                    }
                    return REGION_FACTORYSTART;
                } else if ((chunk >= 22) && (chunk <= 30)) {
                    // 22 = Tunnel from Pole to R&D
                    // 23 = Main R&D
                    // 24 = BHDM Room & Tunnel
                    // 25 = Pincode Room & Tunnel
                    // 26 = Piano Room & Tunnel
                    // 27 = Hatch Room & Tunnel
                    // 28 = Car Race Lobby
                    // 29 = Gorilla Grab Room
                    // 30 = Tunnel to Car Race
                    return REGION_FACTORYRESEARCH;
                }
                return REGION_FACTORYSTORAGE;
            case MAP_JAPES:
                if (chunk == 3) {
                    // 3 = Main Area (Both japes hillside and lowlands)
                    // Subdivide based on z position
                    if (pz > 1647) {
                        if (py < 270) {
                            return REGION_JAPESLOW;
                        }
                        if (px > 2258) {
                            if (pz < 1795) {
                                return REGION_JAPESLOW;
                            }
                        }
                        return REGION_JAPESHIGH;
                    }
                    return REGION_JAPESLOW;
                }
                if ((chunk == 0) || (chunk == 1) || (chunk == 2) || (chunk == 18)) {
                    // 0 = Starting Area
                    // 1 = Starting Tunnel
                    // 2 = Diddy Alcove
                    // 18 = Japes Tunnel Exit
                    return REGION_JAPESLOW;
                } else if ((chunk >= 4) && (chunk <= 7)) {
                    // 4 = Hive Tunnel Near
                    // 5 = Hive Tunnel Mid
                    // 6 = Hive Tunnel Far
                    // 7 = Hive area
                    return REGION_JAPESHIVE;
                } else if ((chunk >= 8) && (chunk <= 16)) {
                    // 8 = Tunnel Middle Branch
                    // 9 = Pit
                    // 10 = Tunnel Right Branch
                    // 11 = Tunnel Crossroads
                    // 12 = Near Rambi Door
                    // 13 = Fairy pool
                    // 14 = Storm Area
                    // 15 = Bunch Boulder Area
                    // 16 = Lanky Kasplat Alcove
                    return REGION_JAPESSTORM;
                }
                return REGION_JAPESHIGH;
            default:
                break;

        }
    }
    return -1;
}

void storeHintRegion(void) {
    int current_region = map_hint_regions[CurrentMap];
    if (current_region >= 0) {
        last_safe_parent = current_region;
    } else if (current_region == INCONSISTENT_HINT_REGION) {
        last_safe_parent = setHintRegion();
    } else {
        last_safe_parent = -1;
    }
}

void getHintRegionText(void) {
    int index = setHintRegion();
    if (index < 0) {
        dk_memcpy(hint_region_text, "UNKNOWN", 8);
    } else {
        char* text = hint_region_names[index];
        wipeMemory(hint_region_text, 0x20);
        dk_memcpy(hint_region_text, text, 0x20);
    }
}

Gfx* displayHintRegion(Gfx* dl, int x, int y, float scale, char* text) {
    dl = printText(dl, x, y, scale, text);
    int y_req = 0x198;
    if (Rando.warp_to_isles_enabled) {
        y_req = InitialPauseHeight;
    }
    if (y != y_req) {
        return dl;
    }
    int x_hint = 0x280;
    int y_bottom = 240;
    gDPSetPrimColor(dl++, 0, 0, 0xFF, 0xFF, 0xFF, 0xFF);
    return printText(dl, x_hint, (y_bottom << 2) - 100, 0.45f, (char*)&hint_region_text);
}