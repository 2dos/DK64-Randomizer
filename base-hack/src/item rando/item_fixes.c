/**
 * @file item_fixes.c
 * @author Ballaam
 * @brief Fixes to item grabbing to make certain items work without a map reload
 * @version 0.1
 * @date 2023-01-28
 * 
 * @copyright Copyright (c) 2023
 * 
 */
#include "../../include/common.h"

typedef struct pad_refresh_struct {
    /* 0x000 */ unsigned char map;
    /* 0x001 */ unsigned char requirement; // 0->4 = kong pads
    /* 0x002 */ unsigned short object_id;
    /* 0x004 */ char target_state;
    /* 0x006 */ unsigned short unk6;
} pad_refresh_struct;

static pad_refresh_struct pads[] = {
    // BBlast Pads
    {
        .map = 7,
        .requirement = PADREFRESH_BLAST,
        .object_id = 0xD9,
        .target_state = -1,
    },
    {
        .map = 0x26,
        .requirement = PADREFRESH_BLAST,
        .object_id = 0x2E,
        .target_state = -1,
    },
    {
        .map = 0x1A,
        .requirement = PADREFRESH_BLAST,
        .object_id = 0x4D,
        .target_state = -1,
    },
    {
        .map = 0x1E,
        .requirement = PADREFRESH_BLAST,
        .object_id = 0x34,
        .target_state = -1,
    },
    {
        .map = 0x30,
        .requirement = PADREFRESH_BLAST,
        .object_id = 0x4C,
        .target_state = -1,
    },
    {
        .map = 0x48,
        .requirement = PADREFRESH_BLAST,
        .object_id = 0x20,
        .target_state = -1,
    },
    {
        .map = 0x57,
        .requirement = PADREFRESH_BLAST,
        .object_id = 0x1F,
        .target_state = -1,
    },
    // Spring
    {
        .map = 0xC8,
        .requirement = PADREFRESH_SPRING,
        .object_id = 0x3,
        .target_state = -1,
    },
    {
        .map = 0xC3,
        .requirement = PADREFRESH_SPRING,
        .object_id = 0x0,
        .target_state = -1,
    },
    {
        .map = 0xC3,
        .requirement = PADREFRESH_SPRING,
        .object_id = 0x0,
        .target_state = -1,
    },
    {
        .map = 0x1A,
        .requirement = PADREFRESH_SPRING,
        .object_id = 0x26,
        .target_state = -1,
    },
    {
        .map = 0x1A,
        .requirement = PADREFRESH_SPRING,
        .object_id = 0x4F,
        .target_state = -1,
    },
    {
        .map = 0x1A,
        .requirement = PADREFRESH_SPRING,
        .object_id = 0x118,
        .target_state = -1,
    },
    {
        .map = 0x1A,
        .requirement = PADREFRESH_SPRING,
        .object_id = 0x117,
        .target_state = -1,
    },
    {
        .map = 0x30,
        .requirement = PADREFRESH_SPRING,
        .object_id = 0x13,
        .target_state = -1,
    },
    {
        .map = 0x30,
        .requirement = PADREFRESH_SPRING,
        .object_id = 0xF,
        .target_state = -1,
    },
    {
        .map = 0x30,
        .requirement = PADREFRESH_SPRING,
        .object_id = 0x3D,
        .target_state = -1,
    },
    // Balloon (Ignore Dungeon Pads, Castle Tower)
    {
        .map = 0xC1,
        .requirement = PADREFRESH_BALLOON,
        .object_id = 0x1,
        .target_state = -1,
    },
    {
        .map = 0x48,
        .requirement = PADREFRESH_BALLOON,
        .object_id = 0xB,
        .target_state = -1,
    },
    {
        .map = 0x48,
        .requirement = PADREFRESH_BALLOON,
        .object_id = 0xC,
        .target_state = -1,
    },
    {
        .map = 0x48,
        .requirement = PADREFRESH_BALLOON,
        .object_id = 0x1C,
        .target_state = -1,
    },
    {
        .map = 0x48,
        .requirement = PADREFRESH_BALLOON,
        .object_id = 0xAF,
        .target_state = -1,
    },
    {
        .map = 0x55,
        .requirement = PADREFRESH_BALLOON,
        .object_id = 0x0,
        .target_state = -1,
    },
    {
        .map = 0x55,
        .requirement = PADREFRESH_BALLOON,
        .object_id = 0x1,
        .target_state = -1,
    },
    {
        .map = 0x5E,
        .requirement = PADREFRESH_BALLOON,
        .object_id = 0x3,
        .target_state = -1,
    },
    {
        .map = 0x1A,
        .requirement = PADREFRESH_BALLOON,
        .object_id = 0x7B,
        .target_state = -1,
    },
    {
        .map = 0x30,
        .requirement = PADREFRESH_BALLOON,
        .object_id = 0x14,
        .target_state = -1,
    },
    {
        .map = 0x1E,
        .requirement = PADREFRESH_BALLOON,
        .object_id = 0x10,
        .target_state = -1,
    },
    {
        .map = 0x1E,
        .requirement = PADREFRESH_BALLOON,
        .object_id = 0x3B,
        .target_state = -1,
    },
    {
        .map = 0x1E,
        .requirement = PADREFRESH_BALLOON,
        .object_id = 0x3C,
        .target_state = -1,
    },
    // Monkeyport
    {
        .map = 0x58,
        .requirement = PADREFRESH_MONKEYPORT,
        .object_id = 0x5,
        .target_state = -1,
    },
    {
        .map = 0x71,
        .requirement = PADREFRESH_MONKEYPORT,
        .object_id = 0x8,
        .target_state = -1,
    },
    {
        .map = 0x71,
        .requirement = PADREFRESH_MONKEYPORT,
        .object_id = 0x9,
        .target_state = -1,
    },
    {
        .map = 0x71,
        .requirement = PADREFRESH_MONKEYPORT,
        .object_id = 0xA,
        .target_state = -1,
    },
    {
        .map = 0x48,
        .requirement = PADREFRESH_MONKEYPORT,
        .object_id = 0x2C,
        .target_state = -1,
    },
    {
        .map = 0x48,
        .requirement = PADREFRESH_MONKEYPORT,
        .object_id = 0x2A,
        .target_state = -1,
    },
    {
        .map = 0x48,
        .requirement = PADREFRESH_MONKEYPORT,
        .object_id = 0xDE,
        .target_state = -1,
    },
    {
        .map = 0x48,
        .requirement = PADREFRESH_MONKEYPORT,
        .object_id = 0x33,
        .target_state = -1,
    },
    {
        .map = 0x48,
        .requirement = PADREFRESH_MONKEYPORT,
        .object_id = 0x2C,
        .target_state = -1,
    },
    {
        .map = 0x22,
        .requirement = PADREFRESH_MONKEYPORT,
        .object_id = 0x37,
        .target_state = -1,
    },
    {
        .map = 0x22,
        .requirement = PADREFRESH_MONKEYPORT,
        .object_id = 0x38,
        .target_state = 0,
    },
    // Gone
    {
        .map = 0xA6,
        .requirement = PADREFRESH_GONE,
        .object_id = 0x4,
        .target_state = -1,
    },
    {
        .map = 0x48,
        .requirement = PADREFRESH_GONE,
        .object_id = 0x3D,
        .target_state = -1,
    },
    {
        .map = 0x5A,
        .requirement = PADREFRESH_GONE,
        .object_id = 0x6,
        .target_state = -1,
    },
    {
        .map = 0xB2,
        .requirement = PADREFRESH_GONE,
        .object_id = 0x8,
        .target_state = -1,
    },
    {
        .map = 0xAA,
        .requirement = PADREFRESH_GONE,
        .object_id = 0x3,
        .target_state = 0,
    },
};

void refreshPads(pad_refresh_signals signal) {
    /**
     * @brief Refresh objects to coincide with an item collection
     * 
     * @param signal Pad Refresh Signal
     */
    int _count = ObjectModel2Count;
    int *m2location = (int *)ObjectModel2Pointer;
    for (int i = 0; i < (int)(sizeof(pads) / sizeof(pad_refresh_struct)); i++) {
        if ((CurrentMap == pads[i].map) && (signal == pads[i].requirement)) {
            for (int i = 0; i < _count; i++) {
                ModelTwoData*_object = getObjectArrayAddr(m2location, 0x90, i);
                if (_object->object_id == pads[i].object_id) {
                    if (pads[i].target_state >= 0) {
                
                    }
                }
            }
            
        }
    }
}