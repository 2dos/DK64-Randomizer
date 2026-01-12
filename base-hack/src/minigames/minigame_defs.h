#ifndef _COMMON_H_
#define _COMMON_H_

#define F3DEX_GBI_2

#define ENABLE_ORIGIN_WARP_FIX 1
#define ENABLE_SAVE_LOCK_REMOVAL 0 // Crashes on Wii U

#define SONG_COUNT 176
#define ENEMIES_TOTAL 428
#define ENEMY_REWARD_CACHE_SIZE 16
#define ROM_DATA __attribute__((used, section(".data")))
#define ROM_RODATA_NUM __attribute__((used, section(".rodata_num")))
#define ROM_RODATA_PTR __attribute__((used, section(".rodata_ptr")))

#include "../../include/build_os.h"
#include "../../include2/ultra64.h"
#include "../../include/common_enums.h"
#include "../../include/common_structs.h"
#include "../../include/crowd_control.h"
#include "../../include/item_rando_structs.h"
#include "../../include/dynamic_structs.h"
#include "../../include/variable_space_structs.h"
#include "../../include/dk64.h"
#include "../../include/flags.h"
#include "../../include/vars.h"
#include "../../include/music.h"
#include "../../include/macros.h"
#include "../../include/pause.h"
#include "../../include/previews.h"

#endif