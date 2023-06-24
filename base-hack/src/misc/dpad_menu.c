/**
 * @file dpad_menu.c
 * @author Ballaam
 * @brief Operation of the DPad Menu
 * @version 0.1
 * @date 2022-07-17
 * 
 * @copyright Copyright (c) 2022
 * 
 */
#include "../../include/common.h"

#define ICON_SCALE 2.0f
#define DPAD_SCALE 2.5f
#define DPAD_X 1025
#define DPAD_Y_HIGH 100
#define DPAD_Y_LOW 250
#define HUD_CHECK_COUNT 4

#define CAN_USE_DPAD 1
#define CAN_SHOW_DPAD 2

#define DPADVISIBLE_HIDE 0
#define DPADVISIBLE_ALL 1
#define DPADVISIBLE_MINIMAL 2

int canUseDPad(void) {
    /**
     * @brief Determines whether the player will be able to use the DPad Menu.
     * This operates outside of Tag Anywhere as Tag Anywhere has different rules
     * 
     * @return Bitfield of whether the dpad can be shown or used
     */
    if (Gamemode != GAMEMODE_ADVENTURE) {
        return 0; // Not in Adv Mode
    }
    if (player_count > 1) {
        return 0; // In Multiplayer
    }
    if ((CurrentMap == MAP_ISLES) && (CutsceneActive) && (CutsceneIndex == 29)) {
        return 0; // In "K. Rool gets launched" Cutscene
    }
    if (inBossMap(CurrentMap, 0, 1, 1)) {
        return 0; // In 5 main K. Rool Phase Maps or Shoe
    }
    if (TBVoidByte & 2) {
        return 0; // Pausing/Paused
    }
    if ((CurrentMap == MAP_FUNKY) || (CurrentMap == MAP_CRANKY) || (CurrentMap == MAP_CANDY)) {
        return 0; // In Shop
    }
    if (
        (CurrentMap == MAP_JAPESMINECART) || // Japes Minecart
        (CurrentMap == MAP_FUNGIMINECART) || // Fungi Minecart
        (CurrentMap == MAP_CASTLEMINECART) || // Castle Minecart
        (CurrentMap == MAP_AZTECBEETLE) || // Aztec Beetle
        (CurrentMap == MAP_CAVESBEETLERACE) || // Caves Beetle
        (CurrentMap == MAP_FACTORYCARRACE) || // Factory Car Race
        (CurrentMap == MAP_CASTLECARRACE) || // Castle Car Race
        (CurrentMap == MAP_GALLEONSEALRACE) // Seal Race
    ) {
        return 0; // In Race
    }
    if (inMinigame(CurrentMap)) {
        return CAN_USE_DPAD;
    }
    if (inBattleCrown(CurrentMap)) {
        return CAN_USE_DPAD;
    }
    return CAN_USE_DPAD | CAN_SHOW_DPAD;
}

int* drawDPad(int* dl) {
    /**
     * @brief Draws the DPad menu
     * 
     * @param dl Display List Address
     * 
     * @return New Display List Address
     */
    if (Rando.dpad_visual_enabled == DPADVISIBLE_HIDE) {
        return dl;
    }
    if ((canUseDPad() & CAN_SHOW_DPAD) == 0) {
        return dl;
    }
    int DPAD_Y = DPAD_Y_HIGH;
    if (Rando.dpad_visual_enabled == DPADVISIBLE_ALL) {
        dl = drawImage(dl, IMAGE_DPAD, RGBA16, 32, 32, DPAD_X + 75, DPAD_Y + 70, DPAD_SCALE, DPAD_SCALE, 0xC0);
        if ((Rando.tag_anywhere) && (Character < 5)) {
            // Tag Anywhere Faces
            int kong_left = getTagAnywhereKong(-1);
            int kong_right = getTagAnywhereKong(1);
            int can_ta = getTAState();
            int ta_opacity = 0x80;
            if (can_ta) {
                ta_opacity = 0xFF;
            }
            dl = drawImage(dl, IMAGE_KONG_START + kong_left, RGBA16, 32, 32, DPAD_X, DPAD_Y + 70, ICON_SCALE, ICON_SCALE, ta_opacity);
            dl = drawImage(dl, IMAGE_KONG_START + kong_right, RGBA16, 32, 32, DPAD_X + 140, DPAD_Y + 70, ICON_SCALE, ICON_SCALE, ta_opacity);
        }
        if (Rando.quality_of_life.ammo_swap) {
            // Homing Ammo Toggle
            if (MovesBase[(int)Character].weapon_bitfield & 2) {
                int render_homing = 1 ^ ForceStandardAmmo;
                if (CollectableBase.HomingAmmo == 0) {
                    render_homing = 0;
                }
                dl = drawImage(dl, IMAGE_AMMO_START + render_homing, RGBA16, 32, 32, DPAD_X + 75, DPAD_Y + 145, ICON_SCALE, ICON_SCALE, 0xFF);

            }
        }
    }
    if (Rando.quality_of_life.hud_bp_multibunch) {
        // Blueprint Show
        int applied_requirement = 75;
        if (Rando.medal_cb_req > 0) {
            applied_requirement = Rando.medal_cb_req;
        }
        int mdl_opacity = 0x80;
        int world = getWorld(CurrentMap, 0);
        if (world < 7) {
            int kong_sum = MovesBase[(int)Character].tns_cb_count[world] + MovesBase[(int)Character].cb_count[world];
            if (kong_sum >= applied_requirement) {
                mdl_opacity = 0xFF;
            }
        }
        dl = drawImage(dl, 116, RGBA16, 32, 32, DPAD_X + 75, DPAD_Y, ICON_SCALE, ICON_SCALE, mdl_opacity);
    }
    return dl;
}

void handleDPadFunctionality(void) {
    /**
     * @brief Handle inputs on the DPad and their corresponding functionality
     */
    if (canUseDPad() & CAN_USE_DPAD) {
        if (Rando.quality_of_life.hud_bp_multibunch) {
            updateMultibunchCount();
            if (NewlyPressedControllerInput.Buttons.d_up) {
                displayItemOnHUD(0xC,0,0);
                int world = getWorld(CurrentMap,0);
                if ((world < 7) && (CurrentMap != MAP_TROFFNSCOFF)) {
                    displayItemOnHUD(0xA,0,0);
                }
            }
        }
        if (Rando.quality_of_life.ammo_swap) {
            toggleStandardAmmo();
        }
    }
}