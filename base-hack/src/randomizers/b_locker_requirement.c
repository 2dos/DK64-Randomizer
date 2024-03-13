#include "../../include/common.h"

int getWorldOffset(void) {
    int world = getWorld(CurrentMap, 0);
    if (world > 7) {
        return 7;
    }
    return world;
}

void setBLockerHead(void) {
    int item = 0;
    int world = getWorldOffset();
    if (world <= 7) {
        item = Rando.b_locker_requirements[world];
    }
    blink(CurrentActorPointer_0, 3, 1);
    applyImageToActor(CurrentActorPointer_0, 3, 0);
    adjustColorPalette(CurrentActorPointer_0, 3, item, 0.0f);
    unkPaletteFunc(CurrentActorPointer_0, 3, 0);
}

void displayBlockerItemOnHUD(void) {
    setBLockerHead();
    int world = getWorldOffset();
    if (world > 7) {
        return;
    }
    int required_item = Rando.b_locker_requirements[world];
    if (required_item == REQITEM_NONE) {
        return;
    }
    int displayed_item = (required_item - REQITEM_KONG) + ITEMID_CHAOSBLOCKER_KONG;
    displayBarrierHUD(displayed_item, 1);
}

int getCountOfBlockerRequiredItem(void) {
    int world = getWorldOffset();
    if (world > 7) {
        return 0;
    }
    return getItemCountReq(Rando.b_locker_requirements[world]);
}

void displayCountOnBLockerTeeth(int count) {
    int world = getWorldOffset();
    if (world > 7) {
        return;
    }
    if (Rando.b_locker_requirements[world] == REQITEM_COLOREDBANANA) {
        count /= 10;
    }
    displayCountOnTeeth(count);
}