#include "../../include/common.h"

static char igt_text[15] = "IGT: 000:00:00";

int* printLevelIGT(int* dl, int x, int y, float scale, char* str) {
    dl = printText(dl, x, y, scale, str);
    int level_index = -1;
    for (int i = 0; i < 12; i++) {
        if ((int)LevelNamesPointer[i] == (int)str) {
            level_index = i;
        }
    }
    int igt_data = 0;
    if (level_index < 9) {
        igt_data = StoredSettings.file_extra.level_igt[level_index];
    }
    int igt_h = igt_data / 3600;
    int igt_m = (igt_data / 60) % 60;
    int igt_s = igt_data % 60;
    dk_strFormat(igt_text, "IGT: %03d:%02d:%02d", igt_h, igt_m, igt_s);
    dl = printText(dl, x, y + 106, 0.5f, (char*)igt_text);
    return dl;
}