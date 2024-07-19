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
            case GOAL_CUSTOMITEM:
                if (!isItemRequirementSatisfied(&Rando.win_condition_extra)) {
                    return;
                }
                beatGame();
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
            if ((type != 0) && (type >= 175) && (type <= 291)) {
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
            if ((type != 0) && (type >= 175) && (type <= 291)) {
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