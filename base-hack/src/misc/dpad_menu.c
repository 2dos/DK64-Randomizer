#include "../../include/common.h"

#define ICON_SCALE 2.0f
#define DPAD_SCALE 2.5f
#define DPAD_X 1025
#define DPAD_Y_HIGH 100
#define DPAD_Y_LOW 250

int* drawDPad(int* dl) {
    if (Gamemode == 6) {
        if ((CurrentMap == 0x22) && (CutsceneActive) && (CutsceneIndex == 29)) {
            return dl;
        }
        if ((CurrentMap == 0xCF) && (CutsceneActive)) {
            if (((CutsceneIndex >= 26) && (CutsceneIndex <= 28)) || (CutsceneIndex == 22)) {
                return dl;
            }
        }
        int DPAD_Y = DPAD_Y_HIGH;
        int states[3] = {0,0,0};
        int timers[3] = {0,0,0};
        if (HUD) {
            for (int i = 0; i < 3; i++) {
                int item_index = 0xB;
                if (i == 1) {
                    item_index = 0xD;
                } else if (i == 2) {
                    item_index = 0x1;
                }
                states[i] = HUD->item[item_index].hud_state;
                if (HUD->item[item_index].placement_pointer) {
                    timers[i] = HUD->item[item_index].placement_pointer->popout_timer;
                }
            }
        }
        int low = 0;
        int is_clear = 1;
        int y_position = DPAD_Y_HIGH;
        for (int i = 0; i < 3; i++) {
            if (states[i] == 2) {
                low = 1;
            }
            if (states[i]) {
                is_clear = 0;
            }
            if ((states[i] == 1) || (states[i] == 3)) {
                float ratio = timers[i];
                ratio /= 0x400;
                float diff = ratio * (DPAD_Y_LOW - DPAD_Y_HIGH);
                int calc_y = DPAD_Y_HIGH + diff;
                if (calc_y > y_position) {
                    y_position = calc_y;
                }
            }
        }
        if (low) {
            DPAD_Y = DPAD_Y_LOW;
        } else if (!is_clear) {
            DPAD_Y = y_position;
        }
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
    }
    return dl;
}