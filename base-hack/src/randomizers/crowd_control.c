#include "../../include/common.h"

static cc_effects effect_data;

/*
    Effects:
    - 0: Drunky Chunky
        - Makes the kong drunk-walk, has inverted controls
        - Also makes the camera wobble. This can be disabled with "Remove Water Oscillation" on the website
    
    Not Yet implemented effects:
    - Disable TA
    - Warp to the DK Rap
    - Caves Stalactite Fall (anywhere)
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
    if (!cc_allower_generic()) {
        return 0;
    }
    return ice_trap_queued == ICETRAP_OFF;
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
    if (!cc_allower_generic()) {
        return 0;
    }
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

static const cc_effect_data cc_funcs[] = {
    {.enabler = &cc_enable_drunky, .disabler = &cc_disable_drunky, .allower = &cc_allower_generic, .restart_upon_map_entry = 1}, // Drunky Kong
    {.restart_upon_map_entry = 0}, // Disable Tag Anywhere
    {.enabler = &cc_enabler_icetrap, .allower=&cc_allower_icetrap, .auto_disable = 1}, // Ice Trap
    {.enabler = &cc_enabler_rockfall, .allower=&cc_allower_rockfall, .active = 1}, // Rockfall
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
                if (cc_funcs[i].allower) {
                    if (!callFunc(cc_funcs[i].allower)) {
                        *eff_data = CC_LOCKED;
                        break;
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
                    if (cc_funcs[i].allower) {
                        if (callFunc(cc_funcs[i].allower)) {
                            if (cc_funcs[i].enabler) {
                                callFunc(cc_funcs[i].enabler);
                            }
                        }
                    }
                }
                if (!cc_funcs[i].restart_upon_map_entry) {
                    break;
                }
                if (ObjectModel2Timer >= 2) { // Have this so effects can last through loading zones
                    break;
                }
            case CC_ENABLING:
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
                if (cc_funcs[i].allower) {
                    if (!callFunc(cc_funcs[i].allower)) {
                        *eff_data = CC_LOCKED;
                        break;
                    }
                }
                *eff_data = CC_READY;
                break;
        }
    }
}