#include "../../include/common.h"

void cancelCutscene(void) {
	if ((TBVoidByte & 2) == 0) {
		if (CutsceneActive) {
			if (CutsceneTypePointer) {
				if (CutsceneTypePointer->cutscene_databank) {
					int* databank = (int *)(CutsceneTypePointer->cutscene_databank);
					short cam_state = *(short *)(getObjectArrayAddr(databank,0xC,CutsceneIndex));
					// short cam_state = *( short*)(cs_databank + (0xC * CutsceneIndex));
					CurrentCameraState = cam_state;
					PreviousCameraState = cam_state;
					CameraStateChangeTimer = 0;
					if (Player) {
						Player->control_state = 0xC;
					}
				}
			}
		}
	}
}

void fixDKFreeSoftlock(void) {
	if (CutsceneActive) {
		if (Rando.free_target_japes == 0) {
			if (CurrentMap == 7) {
				if (CutsceneIndex == 6) {
					cancelCutscene();
				}
			}
		} else if (Rando.free_target_llama == 0) {
			if (CurrentMap == 0x14) {
				if (CutsceneIndex == 3) {
					cancelCutscene();
				}
			}
		} else if (Rando.free_target_ttemple == 0) {
			if (CurrentMap == 0x10) {
				if (CutsceneIndex == 6) {
					cancelCutscene();
				}
			}
		} else if (Rando.free_target_factory == 0) {
			if (CurrentMap == 0x1A) {
				if (CutsceneIndex == 8) {
					cancelCutscene();
				}
			}
		}
	}
}