#include "../../include/common.h"

#define ICON_SCALE 2.0f
#define DPAD_SCALE 2.5f

int* drawDPad(int* dl) {
    if (Gamemode == 6) {
        dl = drawImage(dl, IMAGE_DPAD, RGBA16, 32, 32, 1100, 200, DPAD_SCALE, DPAD_SCALE, 0xC0);
        if ((Rando.tag_anywhere) && (Character < 5)) {
            // Tag Anywhere Faces
            int kong_left = getTagAnywhereKong(-1);
            int kong_right = getTagAnywhereKong(1);
            int can_ta = getTAState();
            int ta_opacity = 0x80;
            if (can_ta) {
                ta_opacity = 0xFF;
            }
            dl = drawImage(dl, IMAGE_KONG_START + kong_left, RGBA16, 32, 32, 1025, 200, ICON_SCALE, ICON_SCALE, ta_opacity);
            dl = drawImage(dl, IMAGE_KONG_START + kong_right, RGBA16, 32, 32, 1165, 200, ICON_SCALE, ICON_SCALE, ta_opacity);
        }
        if (Rando.quality_of_life) {
            // Homing Ammo Toggle
            if (MovesBase[(int)Character].weapon_bitfield & 2) {
                int render_homing = 1 ^ ForceStandardAmmo;
                if (CollectableBase.HomingAmmo == 0) {
                    render_homing = 0;
                }
                dl = drawImage(dl, IMAGE_AMMO_START + render_homing, RGBA16, 32, 32, 1100, 275, ICON_SCALE, ICON_SCALE, 0xFF);

            }
        }
    }
    return dl;
}