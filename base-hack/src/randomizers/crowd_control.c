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
    queueIceTrap(ICETRAP_SUPERBUBBLE);
    return 1;
}

int cc_allower_icetrap(void) {
    if (isBannedTrapMap(CurrentMap, ICETRAP_SUPERBUBBLE)) {
        return 0;
    }
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
    return 1;
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
    return 1;
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

typedef struct timer_paad {
    /* 0x000 */ char unk0[0xc];
    /* 0x00C */ int time;
} timer_paad;

static char getout_killed = 0;
static char getout_init = 0;
Gfx* displayGetOutReticle(Gfx* dl) {
    float x = 0.0f;
    float y = 0.0f;
    calculateScreenPosition(Player->xPos, Player->yPos + Player->height, Player->zPos, &x, &y, 0, 1.0f, 0);
    gDPPipeSync(dl++);
    gDPSetPrimColor(dl++, 0, 0, 0x00, 0xC8, 0x00, 0xFF);
    gDPSetCombineMode(dl++, G_CC_MODULATEIA_PRIM, G_CC_MODULATEIA_PRIM);
    gDPSetRenderMode(dl++, G_RM_XLU_SURF, G_RM_XLU_SURF2);
    gSPDisplayList(dl++, 0x01000118);
    gSPMatrix(dl++, 0x02000080, G_MTX_NOPUSH | G_MTX_LOAD | G_MTX_PROJECTION);
    return displayImage(dl, 0x38, 3, 1, 64, 64, x, y, 0.5f, 0.5f, 0x2D, 0.0f);
}

int cc_enable_getout(void) {
    MapProperties.disable_fairy_camera = 1;
    ButtonsEnabledBitfield &= ~START_BUTTON; // You ain't getting out of this one easily, champ
    spawnActor(0xB0, 0);
    LastSpawnedActor->sub_state = 6;
    Player->krool_timer_pointer = LastSpawnedActor;
    timer_paad* paad = LastSpawnedActor->paad;
    paad->time = 10;
    LastSpawnedActor->xPos = 125;
    LastSpawnedActor->yPos = 0x2A;
    LastSpawnedActor->control_state = 1;
    LastSpawnedActor->shadow_intensity = 0;
    getout_killed = 0;
    getout_init = 1;
    playSFX(0x1A2);
    initTimer(LastSpawnedActor);
}

void fakeGetOut(void) {
    mushroomBounce();
    if (!CCEffectData) {
        return;
    }
    if (CCEffectData->get_out == CC_ENABLED) {
        if (TransitionSpeed > 0.0f) {
            CCEffectData->get_out = CC_DISABLING;
        } else {
            actorData* timer = Player->krool_timer_pointer;
            if (!timer) {
                return;
            }
            if (timer->control_state == 5) {
                if (!getout_killed) {
                    Player->hSpeed = 0.0f;
                    Player->control_state = 0xC;
                    Player->noclip = 0x3C;
                    Player->invulnerability_timer = 0;
                    CollectableBase.StoredDamage = -12;
                    Player->strong_kong_ostand_bitfield &= ~0x10; // Disable Strong Kong
                    playCutscene((void*)0, 6, 5);
                    if (Character == 7) {
                        if (applyDamageMask(0, -1)) {
                            int animation = 0x27;
                            if (Player->grounded_bitfield & 4) {
                                animation = 0x29;
                            }
                            playAnimation(Player, animation);
                            Player->control_state = 0x36;
                            Player->control_state_progress = 0;
                        }
                    } else {
                        adjustProjectileSpawnPosition(Player->xPos, Player->yPos + 1.0f, Player->zPos);
                        spawnProjectile(99, 1, 0.5f, Player->xPos, Player->yPos, Player->zPos, 285.0f, timer);
                    }
                }
                getout_killed = 1;
            } else {
                addDLToOverlay(&displayGetOutReticle, CurrentActorPointer_0, 3);
            }
        }
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
    return spawnActorSpawnerContainer(0x5C, x, y, z, 0, 0x3F000000, 0, &unk);
}

void dummyGuardCode(void) {
    if ((CurrentActorPointer_0->obj_props_bitfield & 0x10) == 0) {
        guardCatchInternal(); // Catch the player
        updateKopStat();
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

int cc_allower_balloon(void) {
    if (Player->grounded_bitfield & 4) {
        return 0;
    }
    if (Character == 7) {
        return 0;
    }
    return 1;
}

int cc_allower_backflip(void) {
    if (!cc_allower_balloon()) {
        return 0;
    }
    return Player->grounded_bitfield & 1;
}

int cc_enabler_balloon(void) {
    if (Player->control_state == 0x6E) {
        Player->balloon_timer += 15;
    } else {
        Player->control_state = 0x6E;
        Player->control_state_progress = 0;
        Player->yVelocity = 0.0f;
        Player->yAccel = 1.8f + (*(double*)(0x8075D308) * 10.0f);
        Player->balloon_timer = 10;
        playActorAnimation(Player, 0x169);
    }
    return 1;
}

int cc_enabler_slip(void) {
    int original_sfx = Player->sfx_floor;
    Player->sfx_floor = 0xC;
    bananaslip();
    Player->sfx_floor = original_sfx;
    return 1;
}

int cc_allower_tag(void) {
    if (!getTAState()) {
        return 0;
    }
    int unlock_count = 0;
    for (int i = 0; i < 5; i++) {
        if (hasAccessToKong(i)) {
            unlock_count += 1;
            if (unlock_count > 1) {
                return 1;
            }
        }
    }
    return 0;
}

int cc_enabler_tag(void) {
    int change_counter = getRNGLower31() & 7;
    for (int j = 0; j < 8; j++) { // Not a while, but a for just in case we get stuck in an inf loop
        for (int i = 0; i < 5; i++) {
            if ((i != Character) && (hasAccessToKong(i))) {
                change_counter--;
                if (change_counter <= 0) {
                    changeKong(i);
                    return 1;
                }
            }
        }
    }
    return 0;
}

int cc_enabler_doabackflip(void) {
    Player->control_state = 0x3E;
    Player->control_state_progress = 0;
    Player->blast_y_velocity = BackflipVelArray[KongIndex];
    Player->ostand_value = 0;
    playAnimation(Player, 0xE);
    return 1;
}

int cc_enabler_ice(void) {
    Player->traction = 1;
    return 1;
}

int cc_disabler_ice(void) {
    Player->traction = 100;
    if (CurrentMap == MAP_CAVESBEETLERACE) {
        Player->traction = 20;
    }
    return 1;
}

int cc_allower_animals(void) {
    if (Character > 4) {
        return 0;
    }
    if (!getTAState()) {
        return 0;
    }
    return 1;
}

int cc_enabler_animals(void) {
    Player->new_kong = Player->characterID;
    if (Player->grounded_bitfield & 4) {
        // Enguarde
        tagKong(9);
        if (Player->water_floor < Player->yPos) {
            Player->control_state = 0x82;
        } else {
            Player->control_state = 0x7F;
        }
        Player->control_state_progress = 0;
        playActorAnimation(Player, 0x317);
        Player->hSpeed = 100.0f;
    } else {
        // Rambi
        tagKong(8);
        Player->control_state = 0xC;
        Player->control_state_progress = 0;
        playAnimation(Player, 9);
        Player->hSpeed = 0.0f;
    }
    Player->ostand_value = 4;
    setAnimalYAccel();
    LevelStateBitfield |= 0x400;
    return 1;
}

int cc_disabler_animals(void) {
    setAction(0x3B, (void*)0, 0);
    Player->rambi_enabled = 0;
    LevelStateBitfield &= ~0x400;
    return 1;
}

int cc_allower_mini(void) {
    if (SwapObject->size != 1) {
        // Already mini, would provide 0 effect
        return 0;
    }
    if (CollectableBase.Crystals == 0) {
        // No crystals, would provide 0 effect
        return 0;
    }
    return 1;
}

int cc_setscale(float value) {
    renderingParamsData* params = (renderingParamsData*)Player->rendering_param_pointer;
    if (!params) {
        return 0;
    }
    params->scale_x = value;
    params->scale_y = value;
    params->scale_z = value;
    return 1;
}

int cc_enabler_mini(void) {
    renderingParamsData* params = (renderingParamsData*)Player->rendering_param_pointer;
    if (!params) {
        return 0;
    }
    if (params->scale_y <= 0.05f) {
        return 1;
    }
    return cc_setscale(0.05f);
}

int cc_disabler_mini(void) {
    return cc_setscale(0.15f);
}

int cc_allower_boulder(void) {
    if ((CurrentMap == MAP_FACTORYJACK) || (CurrentMap == MAP_GALLEONPUFFTOSS)) {
        return 0;
    }
    return LoadedActorCount < 30; // Not safe to add it
}

int cc_enabler_boulder(void) {
    actor_init_data unk;
    return spawnActorSpawnerContainer(61, Player->xPos, Player->yPos, Player->zPos, 0, 0x3F800000, 0, &unk);
}

static const cc_effect_data cc_funcs[] = {
    {.enabler = &cc_enable_drunky, .disabler = &cc_disable_drunky, .restart_upon_map_entry = 1}, // Drunky Kong
    {.restart_upon_map_entry = 0}, // Disable Tag Anywhere
    {.enabler = &cc_enabler_icetrap, .allower=&cc_allower_icetrap, .auto_disable = 1}, // Ice Trap
    {.enabler = &cc_enabler_rockfall, .allower=&cc_allower_rockfall, .active = 1}, // Rockfall
    {.enabler = &cc_enabler_warptorap, .disabler=&cc_disabler_warptorap}, // Warp to Rap
    {.enabler = &cc_enabler_spawnkop, .allower=&cc_allower_spawnkop, .auto_disable = 1}, // Get Kaught
    {.enabler = &cc_enabler_balloon, .allower=&cc_allower_balloon, .auto_disable = 1}, // Baboon Balloon
    {.enabler = &cc_enabler_slip, .auto_disable=1}, // Banana Slip
    {.enabler = &cc_enabler_tag, .allower=&cc_allower_tag}, // Change Kong
    {.enabler = &cc_enabler_doabackflip, .allower=&cc_allower_backflip, .auto_disable = 1}, // Backflip
    {.enabler = &cc_enabler_ice, .disabler = &cc_disabler_ice, .restart_upon_map_entry = 1}, // Ice Floor
    {.enabler = &cc_enable_getout}, // Get out
    {.enabler = &cc_enabler_mini, .allower=&cc_allower_mini, .disabler=&cc_disabler_mini, .active = 1}, // Mini
    {.enabler = &cc_enabler_boulder, .allower=&cc_allower_boulder, .auto_disable=1}, // Spawn Boulder
    {.enabler = &cc_enabler_animals, .allower=&cc_allower_animals, .disabler=&cc_disabler_animals, .restart_upon_map_entry = 1}, // Animal Transform
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