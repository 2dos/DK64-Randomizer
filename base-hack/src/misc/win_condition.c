#include "../../include/common.h"

static unsigned char game_beat_countdown = 0;

void beatGame(void) {
    if (isGamemode(GAMEMODE_ADVENTURE, 1)) {
        setPermFlag(FLAG_GAME_BEATEN);
        if (game_beat_countdown == 0) {
            game_beat_countdown = 6;
        }
    }
}

void finalizeBeatGame(void) {
    // Dumb memes with crashes
    if (game_beat_countdown > 0) {
        if (game_beat_countdown == 1) {
            auto_turn_keys();
            save();
            resetMapContainer();
            loadEndSeq(0);
        }
        game_beat_countdown -= 1;
    }
}

// Pkmn Snap Spreadsheet: https://docs.google.com/spreadsheets/d/1nTZYi36dFaTB1XCgB7dJJffMsaKz-wOFmP5nDo8l3Uo/edit?usp=sharing

static const short poke_snap_actors[] = {
    175, // Kaboom
    178, // Blue Beaver
    181, // Book
    182, // Klobber
    183, // Zinger (Charger)
    187, // Klump
    205, // Klaptrap (Green)
    206, // Zinger (Bomber)
    208, // Klaptrap (Purple)
    209, // Klaptrap (Red)
    212, // Gold Beaver
    224, // Mushroom Man
    230, // Ruler
    235, // Robo-Kremling
    238, // Kremling
    241, // Kasplat (DK)
    242, // Kasplat (Diddy)
    243, // Kasplat (Lanky)
    244, // Kasplat (Tiny)
    245, // Kasplat (Chunky)
    259, // Kop
    261, // Robo-Zinger
    262, // Krossbones
    267, // Shuri
    268, // Gimpfish
    269, // Mr. Dice (Green)
    270, // Sir Domino
    271, // Mr. Dice (Red)
    273, // Fireball w/ Glasses
    276, // Small Spider
    285, // Bat
    288, // Tomato
    289, // Ghost
    290, // Pufftup
    291, // Kosha
    340, // Bug (Trash Can)
    NEWACTOR_ZINGERFLAMETHROWER, // Zinger (Flamethrower)
    NEWACTOR_SCARAB, // Scarab
    163, // BFI Queen
    164, // Ice Tomato
    193, // Mermaid
    201, // Llama
    246, // Mechanical Fish
    247, // Seal
};

typedef struct move_kong_pairs {
    unsigned char move_type;
    unsigned char kong;
    unsigned char level;
} move_kong_pairs;

static const unsigned char required_guns[] = {KONG_DK, KONG_DIDDY, KONG_LANKY, KONG_CHUNKY};
static const move_kong_pairs moves_for_rap[] = {
    {.move_type = 0, .kong = KONG_DK, .level=1},  // Strong Kong
    {.move_type = 2, .kong = KONG_DK, .level=0},  // Coconut
    {.move_type = 0, .kong = KONG_DIDDY, .level=1},  // Rocket
    {.move_type = 2, .kong = KONG_DIDDY, .level=0},  // Peanut
    {.move_type = 4, .kong = KONG_DIDDY, .level=0},  // Guitar
    {.move_type = 0, .kong = KONG_LANKY, .level=0},  // Orangstand
    {.move_type = 0, .kong = KONG_LANKY, .level=1},  // Balloon
    {.move_type = 2, .kong = KONG_LANKY, .level=0},  // Grape
    {.move_type = 4, .kong = KONG_LANKY, .level=0},  // Trombone
    {.move_type = 0, .kong = KONG_TINY, .level=0},  // Mini Monkey
    {.move_type = 0, .kong = KONG_TINY, .level=1},  // Twirl
    {.move_type = 2, .kong = KONG_CHUNKY, .level=0},  // Pineapple
};
static const short rap_flags[] = {FLAG_TBARREL_BARREL, FLAG_TBARREL_ORANGE, FLAG_ABILITY_CLIMBING, FLAG_ITEM_CRANKY};

int hasBeatenDKRapWinCon(void) {
    if (getItemCount_new(REQITEM_KONG, -1, -1) != 5) {
        // Missing at least 1 kong
        return 0;
    }
    for (int i = 0; i < 12; i++) {
        int kong = moves_for_rap[i].kong;
        int head = (int)&MovesBase[kong];
        unsigned char val = *(unsigned char*)(head + moves_for_rap[i].move_type);
        int move_lvl = moves_for_rap[i].level;
        if ((val & (1 << move_lvl)) == 0) {
            return 0;
        }
    }
    for (int i = 0; i < 4; i++) {
        if (!hasFlagMove(rap_flags[i])) {
            return 0;
        }
    }
    return 1;
}

int canAccessKroolsChallenge(void) {
    // Check all 8 Keys
    if (getItemCountReq(REQITEM_KEY) < 8) {
        return 0;
    }
    
    // Check all 40 Blueprints  
    if (getItemCountReq(REQITEM_BLUEPRINT) < 40) {
        return 0;
    }
    
    // Check all 7 Bosses
    if (getItemCountReq(REQITEM_BOSSES) < 7) {
        return 0;
    }
    
    // Check all 43 Bonus Barrels
    if (getItemCountReq(REQITEM_BONUSES_NOHELM) < 43) {
        return 0;
    }
    
    return 1;
}

int canAccessWinCondition(void) {
    // Check if the win condition requirements are met
    switch(Rando.win_condition) {
        case GOAL_KEY8:
            // Key 8 win condition - check for key 8
            return getItemCount_new(REQITEM_KEY, 7, 0);
        
        case GOAL_POKESNAP:
            // Pokemon Snap - check if all required photos are taken
            for (int i = 0; i < (sizeof(poke_snap_actors) / 2); i++) {
                int offset = i >> 3;
                int shift = i & 7;
                if (Rando.enabled_pkmnsnap_enemies[offset] & (1 << shift)) {
                    if (!checkFlag(FLAG_PKMNSNAP_PICTURES + i, FLAGTYPE_PERMANENT)) {
                        return 0;
                    }
                }
            }
            return 1;
        
        case GOAL_DKRAP:
            // DK Rap - check for DK Rap completion
            return hasBeatenDKRapWinCon();
        
        case GOAL_KROOLS_CHALLENGE:
            // Krool's Challenge - check if all required items are collected
            return canAccessKroolsChallenge();
        
        case GOAL_CUSTOMITEM:
            // Custom item requirement - check the specified item count
            return isItemRequirementSatisfied(&Rando.win_condition_extra);
        
        default:
            // For beat K. Rool and other win conditions, return 0 so they use normal key-based spawning
            // Only return 1 if explicitly using krool_ship_spawn_method
            return 0;
    }
}

void checkSeedVictory(void) {
    if (!checkFlag(FLAG_GAME_BEATEN, FLAGTYPE_PERMANENT)) {
        // If krool_ship_spawn_method is enabled, don't trigger victory on win condition items - only when K. Rool is defeated
        if (Rando.krool_ship_spawn_method == 1) {
            return;
        }
        switch(Rando.win_condition) {
            case GOAL_KEY8:
                if (getItemCount_new(REQITEM_KEY, 7, 0)) {
                    beatGame();
                }
                break;
            case GOAL_POKESNAP:
                for (int i = 0; i < (sizeof(poke_snap_actors) / 2); i++) {
                    int offset = i >> 3;
                    int shift = i & 7;
                    if (Rando.enabled_pkmnsnap_enemies[offset] & (1 << shift)) {
                        if (!checkFlag(FLAG_PKMNSNAP_PICTURES + i, FLAGTYPE_PERMANENT)) {
                            return;
                        }
                    }
                }
                beatGame();
                break;
            case GOAL_DKRAP:
                if (hasBeatenDKRapWinCon()) {
                    beatGame();
                }
                break;
            case GOAL_CUSTOMITEM:
                if (isItemRequirementSatisfied(&Rando.win_condition_extra)) {
                    beatGame();
                }
            break;
        }
    }
}

void winRabbitSeed(int song, float volume) {
    playSong(song, volume);
    beatGame();
}

void safeguardRabbitReward(void) {
    if (checkFlag(FLAG_COLLECTABLE_CAVES_CHUNKY_5DI, FLAGTYPE_PERMANENT)) {
        return;
    }
    playCutscene(CurrentActorPointer_0, 3, 1);
}

void checkVictory_flaghook(int flag) {
    checkGlobalProgress(flag);
    checkSeedVictory();
}

static unsigned short extra_kops[] = {
    NEWACTOR_GUARDDISABLEA,
    NEWACTOR_GUARDDISABLEZ,
    NEWACTOR_GUARDGETOUT,
    NEWACTOR_GUARDTAG,
};

int isSnapEnemyInRange(int set) {
    int updated = 0;
    for (int i = 0; i < LoadedActorCount; i++) {
        actorData* actor = LoadedActorArray[i].actor;
        if (actor) {
            int ref_actor = actor->actorType;
            if (inShortList(ref_actor, &extra_kops, 4)) {
                ref_actor = 259;
            }
            int index = inShortList(ref_actor, &poke_snap_actors, sizeof(poke_snap_actors) >> 1);
            if (index) {
                int j = index - 1;
                if (!checkFlag(FLAG_PKMNSNAP_PICTURES + j, FLAGTYPE_PERMANENT)) {
                    int offset = j >> 3;
                    int shift = j & 7;
                    if (Rando.enabled_pkmnsnap_enemies[offset] & (1 << shift)) {
                        float x_store = 0;
                        float y_store = 0;
                        calculateScreenPosition(actor->xPos, actor->yPos + 10.0f, actor->zPos, &x_store, &y_store, 0, 1.0f, 0);
                        int x_int = x_store;
                        int y_int = y_store;
                        if ((x_int >= 0x51) && (x_int <= 0xE9)) { // Normal fairy bounds: 0x8A -> 0xB0
                            if ((y_int >= 0x3B) && (y_int <= 0xAD)) { // Normal fairy bounds: 0x61 -> 0x87
                                if (set) {
                                    updated = 1;
                                    setPermFlag(FLAG_PKMNSNAP_PICTURES + j);
                                } else {
                                    return 1;
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    return updated;
}

static unsigned char pkmn_snap_frames = 0;
static unsigned char pkmn_snap_current = 0;
static unsigned char pkmn_snap_total = 0;

int getPkmnSnapData(int* frames, int* current, int* total) {
    if (pkmn_snap_frames != 0) {
        pkmn_snap_frames += 1;
        if (pkmn_snap_frames > 50) {
            pkmn_snap_frames = 0;
        }
    }
    *frames = pkmn_snap_frames;
    *current = pkmn_snap_current;
    *total = pkmn_snap_total;
    return pkmn_snap_frames != 0;
}

void pokemonSnapMode(void) {
    if (isSnapEnemyInRange(1)) {
        int captured_count = 0;
        int total_count = 0;
        for (int i = 0; i < (sizeof(poke_snap_actors) / 2); i++) {
            captured_count += checkFlag(FLAG_PKMNSNAP_PICTURES + i, FLAGTYPE_PERMANENT);
            int offset = i >> 3;
            int shift = i & 7;
            total_count += ((Rando.enabled_pkmnsnap_enemies[offset] & (1 << shift)) != 0);
        }
        pkmn_snap_frames = 1;
        pkmn_snap_current = captured_count;
        pkmn_snap_total = total_count;
        save();
    }
}