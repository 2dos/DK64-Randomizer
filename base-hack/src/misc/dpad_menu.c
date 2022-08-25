#include "../../include/common.h"

#define ICON_SCALE 2.0f
#define DPAD_SCALE 2.5f
#define DPAD_X 1025
#define DPAD_Y_HIGH 100
#define DPAD_Y_LOW 250
#define HUD_CHECK_COUNT 4

int canUseDPad(void) {
    if (Gamemode != 6) {
        return 0; // Not in Adv Mode
    }
    if (player_count > 1) {
        return 0; // In Multiplayer
    }
    if ((CurrentMap == 0x22) && (CutsceneActive) && (CutsceneIndex == 29)) {
        return 0; // In "K. Rool gets launched" Cutscene
    }
    if ((CurrentMap >= 0xCB) && (CurrentMap <= 0xCF)) {
        return 0; // In 5 main K. Rool Phase Maps
    }
    if (CurrentMap == 0xD6) {
        return 0; // In Shoe
    }
    if (TBVoidByte & 2) {
        return 0; // Pausing/Paused
    }
    if ((CurrentMap == 1) || (CurrentMap == 5) || (CurrentMap == 0x19)) {
        return 0; // In Shop
    }
    if (
        (CurrentMap == 0x06) || // Japes Minecart
        (CurrentMap == 0x37) || // Fungi Minecart
        (CurrentMap == 0x6A) || // Castle Minecart
        (CurrentMap == 0x0E) || // Aztec Beetle
        (CurrentMap == 0x52) || // Caves Beetle
        (CurrentMap == 0x1B) || // Factory Car Race
        (CurrentMap == 0xB9) || // Castle Car Race
        (CurrentMap == 0x27) // Seal Race
    ) {
        return 0; // In Race
    }
    return 1;
}

int* drawDPad(int* dl) {
    if (!canUseDPad()) {
        return dl;
    }
    int DPAD_Y = DPAD_Y_HIGH;
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
    if (Rando.quality_of_life) {
        // Homing Ammo Toggle
        if (MovesBase[(int)Character].weapon_bitfield & 2) {
            int render_homing = 1 ^ ForceStandardAmmo;
            if (CollectableBase.HomingAmmo == 0) {
                render_homing = 0;
            }
            dl = drawImage(dl, IMAGE_AMMO_START + render_homing, RGBA16, 32, 32, DPAD_X + 75, DPAD_Y + 145, ICON_SCALE, ICON_SCALE, 0xFF);

        }
        // Blueprint Show
        dl = drawImage(dl, 116, RGBA16, 32, 32, DPAD_X + 75, DPAD_Y, ICON_SCALE, ICON_SCALE, 0xFF);
    }
    return dl;
}

void handleDPadFunctionality(void) {
    if (canUseDPad()) {
        updateMultibunchCount();
        if (NewlyPressedControllerInput.Buttons & D_Up) {
            displayItemOnHUD(0xC,0,0);
            int world = getWorld(CurrentMap,1);
            if ((world < 7) && (CurrentMap != 0x2A)) {
                displayItemOnHUD(0xA,0,0);
            }
        }
        toggleStandardAmmo();
    }
}