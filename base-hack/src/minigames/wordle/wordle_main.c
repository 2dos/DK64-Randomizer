//avoid
#include "../../../include/common.h"

void entryPoint(void) {
    Gfx *dl;
    renderFrame();
    dlInit(DLPointers[SelectedDLIndex], displayListCount, 3, 1, 0x4D2, 1);
    ObjectModel2Timer++;
    SelectedDLIndex ^= 1;
    CameraDL = &DLArray[SelectedDLIndex];
    handleController();
    if (((MapState & 1) == 0) || (LZFadeoutProgress != 31.0f)) {
        // Render function
        gameLoop(CameraDL, &dl);
    } else {
        dl = DLPointers[SelectedDLIndex];
    }
    dl = unkFadeFunction(dl, 0);
    if (CutsceneActive == 3) { // TODO: This index *should* be dynamic depending on whether it's placed on Jetpac or Arcade
        endDL(dl, SelectedDLIndex, &displayListCount, 1);
    } else {
        DLArr *temp = CameraDL;
        endDL(dl, SelectedDLIndex, &displayListCount, 0);
        unkDLFunction1(&temp->unk0[0xDB0], CameraDL, 0x8076a08c, 1);
    }
}

void gameLoop(DLArr *camera_dl, Gfx **dl_ptr) {

}