/**
 * @file exit_parser.c
 * @author Ballaam
 * @brief Changes related to the new file structure of the exit pointer table
 * @version 0.1
 * @date 2024-12-03
 * 
 * @copyright Copyright (c) 2023
 * 
 */

#include "../../include/common.h"

typedef struct ExitFileStruct {
    /* 0x000 */ SingleExitStruct default_exit; // New exit that's used for voids and level entry=
    /* 0x00A */ short exit_count;
    /* 0x00C */ SingleExitStruct exits[];
} ExitFileStruct;

void loadExits(maps map) {
    ExitFileStruct* file = getMapData(TABLE_MAP_EXITS, map, 1, 1);
    ExitPointer = &file->exits;
    ExitCount = file->exit_count;
    handleRaisedGalleonWater(map);
    DefaultExit = file->default_exit;
}