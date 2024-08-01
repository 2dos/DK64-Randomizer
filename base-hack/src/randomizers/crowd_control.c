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

typedef enum cc_state {
    CC_READY, // 0
    CC_ENABLING, // 1
    CC_ENABLED, // 2
    CC_DISABLING, // 3
    CC_LOCKED, // 4
} cc_state;

typedef struct cc_effect_data {
    /* 0x000 */ void* enabler; // Enabling function
    /* 0x004 */ void* disabler; // Disabling function
    /* 0x008 */ void* allower; // Function which checks if the function is allowed to run
    /* 0x00C */ char restart_upon_map_entry; // Restart effect upon map entry (usually happens if the func has a disabler)
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

int cc_allower_drunky(void) {
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

static const cc_effect_data cc_funcs[] = {
    {.enabler = &cc_enable_drunky, .disabler=&cc_disable_drunky, .allower=&cc_allower_drunky, .restart_upon_map_entry=1},
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
                        break;
                    }
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