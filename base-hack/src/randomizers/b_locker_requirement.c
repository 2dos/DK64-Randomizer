#include "../../include/common.h"

void displayBlockerItemOnHUD(void) {
    int world = getWorld(CurrentMap, 0);
    if (world > 7) {
        return;
    }
    if (Rando.b_locker_requirements[world].item == REQITEM_GOLDENBANANA) {
        displayItemOnHUD(9, 1, 0);
    }
}

int getCountOfBlockerRequiredItem(void) {
    int world = getWorld(CurrentMap, 0);
    if (world > 7) {
        return 0;
    }
    return getItemCountReq(Rando.b_locker_requirements[world].item);
}

void initBLocker(void) {
    writeFunction(0x80027570, &displayBlockerItemOnHUD);
    writeFunction(0x800279D0, &getCountOfBlockerRequiredItem);
    writeFunction(0x8002792C, &getCountOfBlockerRequiredItem);
}