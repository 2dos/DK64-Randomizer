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
    CUSTOM_ACTORS_START + NEWACTOR_ZINGERFLAMETHROWER, // Zinger (Flamethrower)
    CUSTOM_ACTORS_START + NEWACTOR_SCARAB, // Scarab
};

typedef struct dk_rap_wincon_data {
    /* 0x000 */ unsigned char move_type; // special, slam, gun, belt, instrument, flag
    /* 0x001 */ unsigned char kong; // if necessary
    /* 0x002 */ unsigned short signifier; // flag index, "bitwise or" if not flag
} dk_rap_wincon_data;

static const dk_rap_wincon_data dk_rap_conditions[] = {
    {.move_type = PURCHASE_FLAG, .signifier=FLAG_KONG_DK}, // DK, "So they're finally here"
    {.move_type = PURCHASE_FLAG, .signifier=FLAG_KONG_DIDDY}, // Diddy, "So they're finally here"
    {.move_type = PURCHASE_FLAG, .signifier=FLAG_KONG_LANKY}, // Lanky, "So they're finally here"
    {.move_type = PURCHASE_FLAG, .signifier=FLAG_KONG_TINY}, // Tiny, "So they're finally here"
    {.move_type = PURCHASE_FLAG, .signifier=FLAG_KONG_CHUNKY}, // Chunky, "So they're finally here"
    {.move_type = PURCHASE_GUN, .kong=KONG_DK, .signifier=1}, // Coconut Gun, "His Coconut Gun can fire in spurts"
    {.move_type = PURCHASE_MOVES, .kong=KONG_DK, .signifier=MOVECHECK_STRONG}, // Strong Kong, "He's bigger, faster and stronger too"
    // {.move_type = PURCHASE_FLAG, .signifier=FLAG_ABILITY_SHOCKWAVE}, // Shockwave, implied through video
    {.move_type = PURCHASE_MOVES, .kong=KONG_TINY, .signifier=MOVECHECK_MINI}, // Mini Monkey, "She can shrink in style to suit her mood"
    {.move_type = PURCHASE_MOVES, .kong=KONG_TINY, .signifier=MOVECHECK_TWIRL}, // Twirl, "She can float through the air"
    {.move_type = PURCHASE_FLAG, .signifier=FLAG_ABILITY_CLIMBING}, // Climbing, "And climb up trees"
    {.move_type = PURCHASE_MOVES, .kong=KONG_LANKY, .signifier=MOVECHECK_OSTAND}, // Orangstand, "He can handstand, when he needs to"
    {.move_type = PURCHASE_MOVES, .kong=KONG_LANKY, .signifier=MOVECHECK_BALLOON}, // Balloon, "Inflate himself, just like a balloon"
    {.move_type = PURCHASE_INSTRUMENT, .kong=KONG_LANKY, .signifier=1}, // Trombone, "This crazy kong just digs this tune"
    // {.move_type = PURCHASE_MOVES, .kong=KONG_DIDDY, .signifier=MOVECHECK_SPRING}, // Spring, implied through video
    {.move_type = PURCHASE_MOVES, .kong=KONG_DIDDY, .signifier=MOVECHECK_ROCKETBARREL}, // Rocket, "He can fly real high with his jetpac on"
    {.move_type = PURCHASE_GUN, .kong=KONG_DIDDY, .signifier=1}, // Popguns, "With his pistols out, he's one tough kong"
    {.move_type = PURCHASE_INSTRUMENT, .kong=KONG_DIDDY, .signifier=1}, // Guitar, "He'll make you smile when he plays his tune"
    // {.move_type = PURCHASE_MOVES, .kong=KONG_CHUNKY, .signifier=MOVECHECK_HUNKY}, // Hunky, Implied through video
    {.move_type = PURCHASE_FLAG, .signifier=FLAG_TBARREL_BARREL}, // Barrels, "Can pick up a boulder with relative ease"
    // {.move_type = PURCHASE_SLAM, .signifier=3}, // SDSS, Implied through video
    {.move_type = PURCHASE_FLAG, .signifier=FLAG_ITEM_CRANKY}, // Cranky, "C'mon Cranky, take it to the fridge"
    {.move_type = PURCHASE_GUN, .kong=KONG_CHUNKY, .signifier=1}, // Pineapple, "Walnuts, Peanuts, Pineapple Smells"
    {.move_type = PURCHASE_GUN, .kong=KONG_LANKY, .signifier=1}, // Grape, "Grapes, Melons, Oranges and Coconut Shells"
    {.move_type = PURCHASE_FLAG, .signifier=FLAG_TBARREL_ORANGE}, // Oranges, "Grapes, Melons, Oranges and Coconut Shells"
};

int hasBeatenDKRapWinCon(void) {
    for (int i = 0; i < sizeof(dk_rap_conditions) / sizeof(dk_rap_wincon_data); i++) {
        PURCHASE_TYPES move_type = dk_rap_conditions[i].move_type;
        int signifier = dk_rap_conditions[i].signifier;
        if ((move_type == PURCHASE_MOVES) || (move_type == PURCHASE_GUN) || (move_type == PURCHASE_INSTRUMENT)) {
            kongs kong = dk_rap_conditions[i].kong;
            int head = (int)&MovesBase[kong];
            unsigned char val = *(unsigned char*)(head + move_type);
            if (!(val & signifier)) {
                return 0;
            }
        } else if ((move_type == PURCHASE_SLAM) || (move_type == PURCHASE_AMMOBELT)) {
            int head = (int)&MovesBase[0];
            unsigned char val = *(unsigned char*)(head + move_type);
            if (val < signifier) {
                return 0;
            }
        } else {
            if (!checkFlagDuplicate(signifier, FLAGTYPE_PERMANENT)) {
                return 0;
            }
        }
    }
    return 1;
}

void checkSeedVictory(void) {
    if (!checkFlag(FLAG_GAME_BEATEN, FLAGTYPE_PERMANENT)) {
        switch(Rando.win_condition) {
            case GOAL_KEY8:
                if (checkFlagDuplicate(FLAG_KEYHAVE_KEY8, FLAGTYPE_PERMANENT)) {
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

void checkVictory_flaghook(int flag) {
    checkGlobalProgress(flag);
    checkSeedVictory();
}

int isSnapEnemyInRange(void) {
    for (int i = 0; i < LoadedActorCount; i++) {
        actorData* actor = LoadedActorArray[i].actor;
        if (actor) {
            int type = actor->actorType;
            for (int j = 0; j < (sizeof(poke_snap_actors) / 2); j++) {
                if (poke_snap_actors[j] == type) {
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
                                    return 1;
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    return 0;
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
    int updated = 0;
    for (int i = 0; i < LoadedActorCount; i++) {
        actorData* actor = LoadedActorArray[i].actor;
        if (actor) {
            int type = actor->actorType;
            for (int j = 0; j < (sizeof(poke_snap_actors) / 2); j++) {
                if (poke_snap_actors[j] == type) {
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
                                    setPermFlag(FLAG_PKMNSNAP_PICTURES + j);
                                    updated = 1;
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    if (updated) {
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