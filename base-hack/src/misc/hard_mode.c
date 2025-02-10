/**
 * @file hard_mode.c
 * @author Ballaam
 * @brief 
 * @version 0.1
 * @date 2023-08-01
 * 
 * @copyright Copyright (c) 2023
 * 
 */

#include "../../include/common.h"

#define DARK_WORLD_BRIGHTNESS 0.01f
#define LIGHT_BRIGHTNESS 0xFF

/*
    DARK WORLD:
    - Piano Game too hard
    - Japes BBlast not darkened
    - Treasure chests
    - Bblast courses can be a big rough
    - brighten rabbit race (WAY TOO DARK)

    MEMORY CHALLENGE
    - Mermaid is not working properly?
*/

static const map_bitfield is_dark_world_mc = {
    .test_map = 0,
    .funkys_store = 0,
    .dk_arcade = 0,
    .k_rool_barrel_lankys_maze = 0, // Reason: Maze is short enough
    .jungle_japes_mountain = 0,
    .crankys_lab = 1,
    .jungle_japes_minecart = 1,
    .jungle_japes = 0, // Reason: Lag
    .jungle_japes_army_dillo = 1,
    .jetpac = 0,
    .kremling_kosh_very_easy = 1,
    .stealthy_snoop_normal_no_logo = 0,
    .jungle_japes_shell = 1,
    .jungle_japes_lankys_cave = 1,
    .angry_aztec_beetle_race = 1, // Reason: Not a constant stream of coins
    .snides_hq = 0,
    .angry_aztec_tinys_temple = 1, // Reason: No peeking
    .hideout_helm = 1,
    .teetering_turtle_trouble_very_easy = 1,
    .angry_aztec_five_door_temple_dk = 0,
    .angry_aztec_llama_temple = 1,
    .angry_aztec_five_door_temple_diddy = 0,
    .angry_aztec_five_door_temple_tiny = 0,
    .angry_aztec_five_door_temple_lanky = 0,
    .angry_aztec_five_door_temple_chunky = 0,
    .candys_music_shop = 1,
    .frantic_factory = 0, // Reason: Lag
    .frantic_factory_car_race = 1,
    .hideout_helm_level_intros_game_over = 1, // Reason: Consistent with Helm
    .frantic_factory_power_shed = 1,
    .gloomy_galleon = 1,
    .gloomy_galleon_k_rools_ship = 1,
    .batty_barrel_bandit_very_easy = 1,
    .jungle_japes_chunkys_cave = 0, // Reason: Essentially is DW-lite in Vanilla
    .dk_isles_overworld = 1, // Reason: Lobby 6 Entry
    .k_rool_barrel_dks_target_game = 0,
    .frantic_factory_crusher_room = 1, // Reason: No item peek
    .jungle_japes_barrel_blast = 0, // Reason: Cannon Barrels in DW is bad
    .angry_aztec = 1,
    .gloomy_galleon_seal_race = 0,
    .nintendo_logo = 0,
    .angry_aztec_barrel_blast = 0, // Reason: Cannon Barrels in DW is bad
    .troff_n_scoff = 1,
    .gloomy_galleon_shipwreck_diddy_lanky_chunky = 0,
    .gloomy_galleon_treasure_chest = 0,
    .gloomy_galleon_mermaid = 0,
    .gloomy_galleon_shipwreck_dk_tiny = 0,
    .gloomy_galleon_shipwreck_lanky_tiny = 0,
    .fungi_forest = 1,
    .gloomy_galleon_lighthouse = 0,
    .k_rool_barrel_tinys_mushroom_game = 0,
    .gloomy_galleon_mechanical_fish = 0,
    .fungi_forest_ant_hill = 1,
    .battle_arena_beaver_brawl = 0,
    .gloomy_galleon_barrel_blast = 0, // Reason: Cannon Barrels in DW is bad
    .fungi_forest_minecart = 1,
    .fungi_forest_diddys_barn = 0, // Reason: Vanilla is essentially DW, Sky is a bad idea
    .fungi_forest_diddys_attic = 0,
    .fungi_forest_lankys_attic = 0,
    .fungi_forest_dks_barn = 0,
    .fungi_forest_spider = 1,
    .fungi_forest_front_part_of_mill = 1, // Reason: Lever Combo
    .fungi_forest_rear_part_of_mill = 1,
    .fungi_forest_mushroom_puzzle = 0,
    .fungi_forest_giant_mushroom = 1,
    .stealthy_snoop_normal = 1,
    .mad_maze_maul_hard = 1,
    .stash_snatch_normal = 1,
    .mad_maze_maul_easy = 1,
    .mad_maze_maul_normal = 1,
    .fungi_forest_mushroom_leap = 1,
    .fungi_forest_shooting_game = 0,
    .crystal_caves = 1,
    .battle_arena_kritter_karnage = 1,
    .stash_snatch_easy = 1,
    .stash_snatch_hard = 1,
    .dk_rap = 0,
    .minecart_mayhem_easy = 1,
    .busy_barrel_barrage_easy = 1, // Reason: Offers Challenge
    .busy_barrel_barrage_normal = 1, // Reason: Offers Challenge
    .main_menu = 0,
    .title_screen_not_for_resale_version = 0,
    .crystal_caves_beetle_race = 0, // Reason: Light Strobing
    .fungi_forest_dogadon = 1, // Reason: Framebuffer
    .crystal_caves_igloo_tiny = 1,
    .crystal_caves_igloo_lanky = 1,
    .crystal_caves_igloo_dk = 0, // Reason: Maze in DW lol
    .creepy_castle = 1, // Reason: Sky makes climb too hard
    .creepy_castle_ballroom = 1,
    .crystal_caves_rotating_room = 0, // Reason: Has no impact because room is obj
    .crystal_caves_shack_chunky = 1,
    .crystal_caves_shack_dk = 1,
    .crystal_caves_shack_diddy_middle_part = 0,
    .crystal_caves_shack_tiny = 0,
    .crystal_caves_lankys_hut = 0,
    .crystal_caves_igloo_chunky = 1,
    .splish_splash_salvage_normal = 0,
    .k_lumsy = 1,
    .crystal_caves_ice_castle = 1,
    .speedy_swing_sortie_easy = 1,
    .crystal_caves_igloo_diddy = 1,
    .krazy_kong_klamour_easy = 0,
    .big_bug_bash_very_easy = 0,
    .searchlight_seek_very_easy = 0,
    .beaver_bother_easy = 1,
    .creepy_castle_tower = 0,
    .creepy_castle_minecart = 1,
    .kong_battle_battle_arena = 0,
    .creepy_castle_crypt_lanky_tiny = 0,
    .kong_battle_arena_1 = 0,
    .frantic_factory_barrel_blast = 1, // Reason: The only good DW BBlast
    .gloomy_galleon_pufftoss = 0,
    .creepy_castle_crypt_dk_diddy_chunky = 1, // Reason: Lever Combo
    .creepy_castle_museum = 0,
    .creepy_castle_library = 1,
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
    .busy_barrel_barrage_hard = 1, // Reason: Offers Challenge
    .splish_splash_salvage_hard = 0,
    .splish_splash_salvage_easy = 0,
    .speedy_swing_sortie_normal = 1,
    .speedy_swing_sortie_hard = 1,
    .beaver_bother_normal = 1,
    .beaver_bother_hard = 1,
    .searchlight_seek_easy = 0,
    .searchlight_seek_normal = 0,
    .searchlight_seek_hard = 0,
    .krazy_kong_klamour_normal = 0,
    .krazy_kong_klamour_hard = 0,
    .krazy_kong_klamour_insane = 0,
    .peril_path_panic_very_easy = 1,
    .peril_path_panic_easy = 1,
    .peril_path_panic_normal = 1,
    .peril_path_panic_hard = 1,
    .big_bug_bash_easy = 0,
    .big_bug_bash_normal = 0,
    .big_bug_bash_hard = 0,
    .creepy_castle_dungeon = 1, // Reason: Gas makes sky too easy
    .hideout_helm_intro_story = 1,
    .dk_isles_dk_theatre = 1,
    .frantic_factory_mad_jack = 1, // Reason: Better Challenge, FBuffer
    .battle_arena_arena_ambush = 1,
    .battle_arena_more_kritter_karnage = 0,
    .battle_arena_forest_fracas = 1,
    .battle_arena_bish_bash_brawl = 0,
    .battle_arena_kamikaze_kremlings = 1,
    .battle_arena_plinth_panic = 0,
    .battle_arena_pinnacle_palaver = 1,
    .battle_arena_shockwave_showdown = 0,
    .creepy_castle_basement = 1,
    .creepy_castle_tree = 0, // Reason: Sniper Challenge in DW is bad
    .k_rool_barrel_diddys_kremling_game = 1,
    .creepy_castle_chunkys_toolshed = 1,
    .creepy_castle_trash_can = 1,
    .creepy_castle_greenhouse = 1, // Reason: Sky maze lol
    .jungle_japes_lobby = 1,
    .hideout_helm_lobby = 1,
    .dks_house = 1,
    .rock_intro_story = 0,
    .angry_aztec_lobby = 1,
    .gloomy_galleon_lobby = 1,
    .frantic_factory_lobby = 1,
    .training_grounds = 0,
    .dive_barrel = 1,
    .fungi_forest_lobby = 1,
    .gloomy_galleon_submarine = 1,
    .orange_barrel = 1,
    .barrel_barrel = 1,
    .vine_barrel = 1,
    .creepy_castle_crypt = 1,
    .enguarde_arena = 0,
    .creepy_castle_car_race = 1,
    .crystal_caves_barrel_blast = 0, // Reason: Cannon Barrels in DW is bad
    .creepy_castle_barrel_blast = 0, // Reason: Cannon Barrels in DW is bad
    .fungi_forest_barrel_blast = 0, // Reason: Cannon Barrels in DW is bad
    .fairy_island = 1, // Reason: No RW reward peek
    .kong_battle_arena_2 = 0,
    .rambi_arena = 1,
    .kong_battle_arena_3 = 0,
    .creepy_castle_lobby = 0,
    .crystal_caves_lobby = 1,
    .dk_isles_snides_room = 0,
    .crystal_caves_army_dillo = 1,
    .angry_aztec_dogadon = 1, // Reason: Framebuffer
    .training_grounds_end_sequence = 1, // Reason: Framebuffer
    .creepy_castle_king_kut_out = 1,
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
    .k_rool_barrel_chunkys_shooting_game = 0,
    .k_rool_barrel_dks_rambi_game = 1,
    .k_lumsy_ending = 1,
    .k_rools_shoe = 0,
    .k_rools_arena = 0,
};

typedef enum challenge_type {
    /* 0x000 */ CHALLENGE_NONE,
    /* 0x001 */ CHALLENGE_SKY,
    /* 0x002 */ CHALLENGE_DARK_WORLD,
} challenge_type;

static unsigned char banned_challenge_maps[] = {
    MAP_TESTMAP,
    MAP_DKARCADE,
    MAP_JETPAC,
    MAP_SNOOP_NORMALNOLOGO,
    MAP_NINTENDOLOGO,
    MAP_FUNGIDIDDYBARN,
    MAP_DKRAP,
    MAP_CAVESROTATINGROOM,
    MAP_NFRTITLESCREEN,
};

challenge_type getMemoryChallengeType(maps map) {
    if (inU8List(map, &banned_challenge_maps[0], sizeof(banned_challenge_maps))) {
        return CHALLENGE_NONE;
    }
    if (getBitArrayValue(&is_dark_world_mc, map)) {
        return CHALLENGE_DARK_WORLD;
    }
    return CHALLENGE_SKY;
}

static unsigned char blast_maps[] = {
    MAP_JAPESBBLAST,
    MAP_AZTECBBLAST,
    MAP_FACTORYBBLAST,
    MAP_GALLEONBBLAST,
    MAP_FUNGIBBLAST,
    MAP_CAVESBBLAST,
    MAP_CASTLEBBLAST,
};

int isDarkWorld(maps map, int chunk) {
    if (Rando.hard_mode.memory_challenge) {
        return getMemoryChallengeType(map) == CHALLENGE_DARK_WORLD;
    }
    if (map == MAP_JAPES) {
        if (chunk == 3) { // Japes Main
            return 0;
        }
    }
    if (map == MAP_FACTORY) {
        if (chunk == 5) { // Production
            return 0;
        }
        if (chunk == 16) { // Testing
            return 0;
        }
    }
    if (inU8List(CurrentMap, &blast_maps[0], sizeof(blast_maps))) {
        return 0;
    }
    return 1;
}

void alterChunkLighting(int chunk) {
	loadMapChunkLighting(chunk);
	if (chunk == -1) {
		return;
	}
    if (!isDarkWorld(CurrentMap, chunk)) {
        return;
    }
	if (chunk_count > 0) {
		for (int i = 0; i < chunk_count; i++) {
            if (isDarkWorld(CurrentMap, i)) {
                float brightness = DARK_WORLD_BRIGHTNESS;
                if (CurrentMap == MAP_FUNGI) {
                    if ((i >= 13) && (i <= 17)) {
                        brightness = 0.1f;
                    }
                }
                ChunkLighting_Red[i] = brightness;
                ChunkLighting_Green[i] = brightness;
                ChunkLighting_Blue[i] = brightness;
            }
		}
	}
}

void alterChunkData(void* data) {
	loadChunks(data);
	if (chunk_count > 0) {
		for (int i = 0; i < chunk_count; i++) {
			chunkArray[i].reference_dynamic_lighting = isDarkWorld(CurrentMap, i);    
		}
	}
}

#define SHINE_DISTANCE 30
#define SHINE_RADIUS 40
#define USE_POSITIONAL_SHINE 1

void shineLight(actorData* actor, int kongType) {
    genericKongCode(actor, kongType);
    playerData* player = (playerData*)actor;
    if (!isDarkWorld(CurrentMap, player->chunk)) {
        return;
    }
    if (USE_POSITIONAL_SHINE) {
        float shine_x = determineXRatioMovement(actor->rot_y) * SHINE_DISTANCE;
        float shine_z = determineZRatioMovement(actor->rot_y) * SHINE_DISTANCE;
        shine_x += actor->xPos;
        shine_z += actor->zPos;
        renderLight(shine_x, actor->yPos + 10, shine_z, shine_x, actor->yPos + 20, shine_z, SHINE_RADIUS, 0, LIGHT_BRIGHTNESS, LIGHT_BRIGHTNESS, LIGHT_BRIGHTNESS);
    }
}

int isSkyWorld(maps map) {
    if (Rando.hard_mode.no_geo) {
        return 1;
    }
    if (Rando.hard_mode.memory_challenge) {
        return getMemoryChallengeType(map) == CHALLENGE_SKY;
    }
    return 0;
}

Gfx* displayNoGeoChunk(Gfx* dl, int chunk_index, int shift) {
    if (!isSkyWorld(CurrentMap)) {
        return displayChunk(dl, chunk_index, shift);
    }
    gDPPipeSync(dl++);
    return dl;
}

static unsigned char fall_damage_immunity = 0;

void setFallDamageImmunity(int value) {
    fall_damage_immunity = value;
}

void handleFallDamageImmunity(void) {
    if (ObjectModel2Timer == 0) {
        return;
    }
    if (fall_damage_immunity == 0) {
        return;
    }
    if (!Player) {
        fall_damage_immunity -= 1;
        return;
    }
    if (Player->control_state == 0x2A) {
        // Aerial Attack
        return;
    }
    fall_damage_immunity -= 1;
}

void transformBarrelImmunity(void) {
    setFallDamageImmunity(60);
    DisplayExplosionSprite();
}

void factoryShedFallImmunity(short exit) {
    setFallDamageImmunity(30);
    unkLoadingZoneControllerFunction(exit);
}


void fallDamageWrapper(int action, void* actor, int player_index) {
    if (ObjectModel2Timer < 100) {
        return;
    }
    if (fall_damage_immunity > 0) {
        return;
    }
    setAction(action, actor, player_index);
}

static unsigned char stalactite_spawn_bans[] = {
    0x6E, // Baboon Balloon
    0x3E, // Backflip
    0x87, // Entering Portal
    0x88, // Exiting Portal
};

void* spawnStalactite(short actor, float x, float y, float z, int unk0, int unk1, int unk2, void* unk3) {
    if (ObjectModel2Timer < 90) { // Prevent 
        return (void*)0;
    }
    if (Player) {
        if (inU8List(Player->control_state, &stalactite_spawn_bans, sizeof(stalactite_spawn_bans))) {
            return (void*)0;
        }
    }
    return spawnActorSpawnerContainer(actor, x, y, z, unk0, unk1, unk2, unk3);
}

typedef struct balloon_data {
    /* 0x000 */ int path;
    /* 0x004 */ int speed;
} balloon_data;

static float pop_x;
static float pop_z;
static int pop_timer;

void spawnKRoolLankyBalloon(void) {
    balloon_data data = {.path = 1, .speed = 5};
    spawnActorSpawnerContainer(147, 796.0f, 106.0f, 745.0f, 0, 0x3F000000, 0, &data);
}

void popExistingBalloon(void) {
    pop_x = CurrentActorPointer_0->xPos;
    pop_z = CurrentActorPointer_0->zPos;
    pop_timer = 150;
    sendActorSignal(3, 1, 0x2B, 0, 0);
    spawnKRoolLankyBalloon();
}

void handleKRoolDirecting(void) {
    int control_state = CurrentActorPointer_0->control_state;
    if (control_state == 0x2B) {
        float dx = CurrentActorPointer_0->xPos - pop_x;
        float dz = CurrentActorPointer_0->zPos - pop_z;
        float dxz = (dx * dx) + (dz * dz);
        if (pop_timer > 0) {
            pop_timer--;
        }
        if ((dxz < 400) || (pop_timer == 1)) {
            // Within 20 units, or enough time has passed that we need to do an escape
            disappearPeel(0);
            CurrentActorPointer_0->control_state = 0x42;
            CurrentActorPointer_0->control_state_progress = 0;
            resetLankyKR();
        }
    }
    generalActorHandle(0x23, pop_x, pop_z, 0, 0.0f);
}

typedef struct KRoolLanky178 {
    /* 0x000 */ char pad_00[0x14];
    /* 0x014 */ char hits;
} KRoolLanky178;

void incHitCounter(void* actor, int val) {
    setActorSpeed(actor, val);
    KRoolLanky178* aad178 = CurrentActorPointer_0->paad2;
    aad178->hits++; 
}

void parseControllerInput(Controller * cont) {
    getControllerInput(cont);
    if (isGamemode(GAMEMODE_MAINMENU, 1)) {
        return;
    }
    if ((CutsceneActive == 3) || (CutsceneActive == 4)) {
        // In arcade/jetpac
        // TODO: Flip these
        return;
    }
    if (TBVoidByte & 3) {
        // Is pausing/paused
        return;
    }
    if (Player) {
        if (Player->control_state == 0x42) {
            // Tag Barrel
            return;
        }
    }
    cont->stickX = -cont->stickX;
}