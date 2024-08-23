#include "../../include/common.h"

static cc_effects effect_data;

/*
    Effects:
    - 0: Drunky Chunky
        - Makes the kong drunk-walk, has inverted controls
        - Also makes the camera wobble. This can be disabled with "Remove Water Oscillation" on the website
    
    Not Yet implemented effects:
    - Warp to the DK Rap
*/

typedef struct cc_effect_data {
    /* 0x000 */ void* enabler; // Enabling function
    /* 0x004 */ void* disabler; // Disabling function
    /* 0x008 */ void* allower; // Function which checks if the function is allowed to run
    /* 0x00C */ char restart_upon_map_entry; // Restart effect upon map entry (usually happens if the func has a disabler)
    /* 0x00D */ char active; // Run the enabler function whilst active
    /* 0x00E */ char auto_disable; // Disable once enabled (usually for fixed-length events)
} cc_effect_data;

int cc_enable_drunky(void) {
    if (!Player) {
        return 0;
    }
    if (ObjectModel2Timer < 2) {
        return 0;
    }
    Player->strong_kong_ostand_bitfield |= 0x180;
    return 1;
}

int cc_disable_drunky(void) {
    if (!Player) {
        return 0;
    }
    Player->strong_kong_ostand_bitfield &= ~0x180;
    return 1;
}

int cc_allower_generic(void) {
    if (ObjectModel2Timer < 2) {
        return 0;
    }
    if (Gamemode != GAMEMODE_ADVENTURE) {
        return 0;
    }
    if (Mode != GAMEMODE_ADVENTURE) {
        return 0;
    }
    if (TBVoidByte & 3) {
        return 0;
    }
    if (CutsceneActive) {
        return 0;
    }
    if (TransitionSpeed > 0.0f) {
        return 0;
    }
    if (Player) {
        if (!IsAutowalking) {
            return 1;
        }
    }
    return 0;
}

int cc_enabler_icetrap(void) {
    queueIceTrap(ICETRAP_BUBBLE);
    return 1;
}

int cc_allower_icetrap(void) {
    return ice_trap_queued == ICETRAP_OFF;
}

static char in_forced_rap = 0;
static unsigned char previous_rap_map = 0;
static unsigned char previous_rap_exit = 0;
int cc_enabler_warptorap(void) {
    in_forced_rap = 1;
    previous_rap_map = CurrentMap;
    previous_rap_exit = DestExit;
    initiateTransitionFade(MAP_DKRAP, 0, GAMEMODE_RAP);
}

void handleGamemodeWrapper(void) {
    handleGamemodes();
    if ((in_forced_rap) && (Gamemode == GAMEMODE_RAP)) {
        ButtonsEnabledBitfield = 0;
    }
}

int cc_disabler_warptorap(void) {
    if ((in_forced_rap) && (Gamemode == GAMEMODE_RAP)) {
        setNextTransitionType(1);
        initiateTransition(previous_rap_map, previous_rap_exit);
        Mode = GAMEMODE_ADVENTURE;
        in_forced_rap = 0;
    }
}

void skipDKTV(void) {
    if (in_forced_rap) {
        CCEffectData->warp_to_rap = CC_DISABLING;
    } else {
        setNextTransitionType(1);
        initiateTransition(MAP_MAINMENU, 0);
        Mode = GAMEMODE_MAINMENU;
    }
}

typedef struct actor_init_data {
    float unk0;
    float unk4;
    float unk8;
    float unkC;
    float unk10;
    float unk14;
    float unk18;
    float unk1C;
} actor_init_data;

int cc_allower_rockfall(void) {
    return LoadedActorCount < 50; // Not safe to add it
}

int cc_enabler_rockfall(void) {
    if (ObjectModel2Timer % 20) {
        return 0;
    }
    float x_offset = determineXRatioMovement(Player->facing_angle) * Player->hSpeed;
    float z_offset = determineZRatioMovement(Player->facing_angle) * Player->hSpeed;
    float x = Player->xPos + x_offset;
    float y = Player->yPos + 200.0f;
    float z = Player->zPos + z_offset;
    actor_init_data unk; // 0x48 -> 0x67
    return spawnActorSpawnerContainer(0x5C, *(int*)(&x), *(int*)(&y), *(int*)(&z), 0, 0x3F000000, 0, &unk);
}

void dummyGuardCode(void) {
    if ((CurrentActorPointer_0->obj_props_bitfield & 0x10) == 0) {
        guardCatchInternal(); // Catch the player
        playActorAnimation(CurrentActorPointer_0, 0x2C0);
    }
    // Render Light
    float x = 0.0f;
    float y = 0.0f;
    float z = 0.0f;
    getBonePosition(CurrentActorPointer_0, 1, &x, &y, &z);
    renderLight(x, y, z, 0.0f, 0.0f, 0.0f, 70.0f, 0, 0xFF, 0xFF, 0xFF);
    // Change kop angle
    CurrentActorPointer_0->rot_y = getAngleBetweenPoints(Player->xPos, Player->zPos, CurrentActorPointer_0->xPos, CurrentActorPointer_0->zPos);
    renderActor(CurrentActorPointer_0, 0);
}

int cc_allower_spawnkop(void) {
    if (isActorLoaded(CUSTOM_ACTORS_START + NEWACTOR_KOPDUMMY)) {
        return 0;
    }
    return 1;
}

int cc_enabler_spawnkop(void) {
    if (!cc_allower_spawnkop()) {
        return 0;
    }
    spawnActor(CUSTOM_ACTORS_START + NEWACTOR_KOPDUMMY, 0x3F);
    float dx = determineXRatioMovement(Player->facing_angle) * 50.0f;
    float dz = determineZRatioMovement(Player->facing_angle) * 50.0f;
    LastSpawnedActor->xPos = Player->xPos + dx;
    LastSpawnedActor->yPos = Player->yPos;
    LastSpawnedActor->zPos = Player->zPos + dz;
    return 1;
}

static const cc_effect_data cc_funcs[] = {
    {.enabler = &cc_enable_drunky, .disabler = &cc_disable_drunky, .restart_upon_map_entry = 1}, // Drunky Kong
    {.restart_upon_map_entry = 0}, // Disable Tag Anywhere
    {.enabler = &cc_enabler_icetrap, .allower=&cc_allower_icetrap, .auto_disable = 1}, // Ice Trap
    {.enabler = &cc_enabler_rockfall, .allower=&cc_allower_rockfall, .active = 1}, // Rockfall
    {.enabler = &cc_enabler_warptorap, .disabler=&cc_disabler_warptorap}, // Warp to Rap
    {.enabler = &cc_enabler_spawnkop, .allower=&cc_allower_spawnkop, .auto_disable = 1}, // Get Kaught
};

void cc_effect_handler(void) {
    CCEffectData = &effect_data;
    int head = (int)&effect_data;
    for (int i = 0; i < sizeof(cc_effects); i++) {
        unsigned char* eff_data = (unsigned char*)head + i;
        cc_state state = *eff_data;
        switch (state) {
            case CC_READY:
            case CC_LOCKED:
                if (cc_allower_generic()) {
                    if (cc_funcs[i].allower) {
                        if (!callFunc(cc_funcs[i].allower)) {
                            *eff_data = CC_LOCKED;
                            break;
                        }
                    }
                }
                if (state == CC_LOCKED) {
                    *eff_data = CC_READY;
                }
                break;
            case CC_ENABLED:
                if (cc_funcs[i].auto_disable) {
                    *eff_data = CC_DISABLING;
                    break;
                }
                if (cc_funcs[i].active) {
                    if (cc_allower_generic()) {
                        if (cc_funcs[i].allower) {
                            if (callFunc(cc_funcs[i].allower)) {
                                if (cc_funcs[i].enabler) {
                                    callFunc(cc_funcs[i].enabler);
                                }
                            }
                        }
                    }
                }
                if (!cc_funcs[i].restart_upon_map_entry) {
                    break;
                }
                if (ObjectModel2Timer > 2) { // Have this so effects can last through loading zones
                    break;
                }
                *eff_data = CC_ENABLING;
                break;
            case CC_ENABLING:
                if (!cc_allower_generic()) {
                    break;
                }
                if (cc_funcs[i].enabler) {
                    if (callFunc(cc_funcs[i].enabler)) {
                        *eff_data = CC_ENABLED;
                    }
                    break;
                }
                *eff_data = CC_ENABLED;
                break;
            case CC_DISABLING:
                if (cc_funcs[i].disabler) {
                    if (!callFunc(cc_funcs[i].disabler)) {
                        return;
                    }
                }
                if (cc_allower_generic()) {
                    if (cc_funcs[i].allower) {
                        if (!callFunc(cc_funcs[i].allower)) {
                            *eff_data = CC_LOCKED;
                            break;
                        }
                    }
                }
                *eff_data = CC_READY;
                break;
        }
    }
}