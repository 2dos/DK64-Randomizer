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
        .map = MAP_JAPES,
        .requirement = ITEMREFRESH_BLAST,
        .object_id = 0xD9,
        .target_state = -1,
    },
    {
        .map = MAP_AZTEC,
        .requirement = ITEMREFRESH_BLAST,
        .object_id = 0x2E,
        .target_state = -1,
    },
    {
        .map = MAP_FACTORY,
        .requirement = ITEMREFRESH_BLAST,
        .object_id = 0x4D,
        .target_state = -1,
    },
    {
        .map = MAP_GALLEON,
        .requirement = ITEMREFRESH_BLAST,
        .object_id = 0x34,
        .target_state = -1,
    },
    {
        .map = MAP_FUNGI,
        .requirement = ITEMREFRESH_BLAST,
        .object_id = 0x4C,
        .target_state = -1,
    },
    {
        .map = MAP_CAVES,
        .requirement = ITEMREFRESH_BLAST,
        .object_id = 0x20,
        .target_state = -1,
    },
    {
        .map = MAP_CASTLE,
        .requirement = ITEMREFRESH_BLAST,
        .object_id = 0x1F,
        .target_state = -1,
    },
    // Spring
    {
        .map = MAP_CAVESSHACKDIDDYHIGH,
        .requirement = ITEMREFRESH_SPRING,
        .object_id = 0x3,
        .target_state = -1,
    },
    {
        .map = MAP_ISLES_SNIDEROOM,
        .requirement = ITEMREFRESH_SPRING,
        .object_id = 0x0,
        .target_state = -1,
    },
    {
        .map = MAP_FACTORY,
        .requirement = ITEMREFRESH_SPRING,
        .object_id = 0x26,
        .target_state = -1,
    },
    {
        .map = MAP_FACTORY,
        .requirement = ITEMREFRESH_SPRING,
        .object_id = 0x4F,
        .target_state = -1,
    },
    {
        .map = MAP_FACTORY,
        .requirement = ITEMREFRESH_SPRING,
        .object_id = 0x118,
        .target_state = -1,
    },
    {
        .map = MAP_FACTORY,
        .requirement = ITEMREFRESH_SPRING,
        .object_id = 0x117,
        .target_state = -1,
    },
    {
        .map = MAP_FUNGI,
        .requirement = ITEMREFRESH_SPRING,
        .object_id = 0x13,
        .target_state = -1,
    },
    {
        .map = MAP_FUNGI,
        .requirement = ITEMREFRESH_SPRING,
        .object_id = 0xF,
        .target_state = -1,
    },
    {
        .map = MAP_FUNGI,
        .requirement = ITEMREFRESH_SPRING,
        .object_id = 0x3D,
        .target_state = -1,
    },
    // Balloon (Ignore Dungeon Pads, Castle Tower)
    {
        .map = MAP_CASTLELOBBY,
        .requirement = ITEMREFRESH_BALLOON,
        .object_id = 0x1,
        .target_state = -1,
    },
    {
        .map = MAP_CAVES,
        .requirement = ITEMREFRESH_BALLOON,
        .object_id = 0xB,
        .target_state = -1,
    },
    {
        .map = MAP_CAVES,
        .requirement = ITEMREFRESH_BALLOON,
        .object_id = 0xC,
        .target_state = -1,
    },
    {
        .map = MAP_CAVES,
        .requirement = ITEMREFRESH_BALLOON,
        .object_id = 0x1C,
        .target_state = -1,
    },
    {
        .map = MAP_CAVES,
        .requirement = ITEMREFRESH_BALLOON,
        .object_id = 0xAF,
        .target_state = -1,
    },
    {
        .map = MAP_CAVES5DILANKY,
        .requirement = ITEMREFRESH_BALLOON,
        .object_id = 0x0,
        .target_state = -1,
    },
    {
        .map = MAP_CAVES5DILANKY,
        .requirement = ITEMREFRESH_BALLOON,
        .object_id = 0x1,
        .target_state = -1,
    },
    {
        .map = MAP_CAVES1DC,
        .requirement = ITEMREFRESH_BALLOON,
        .object_id = 0x3,
        .target_state = -1,
    },
    {
        .map = MAP_FACTORY,
        .requirement = ITEMREFRESH_BALLOON,
        .object_id = 0x7B,
        .target_state = -1,
    },
    {
        .map = MAP_FUNGI,
        .requirement = ITEMREFRESH_BALLOON,
        .object_id = 0x14,
        .target_state = -1,
    },
    {
        .map = MAP_GALLEON,
        .requirement = ITEMREFRESH_BALLOON,
        .object_id = 0x10,
        .target_state = -1,
    },
    {
        .map = MAP_GALLEON,
        .requirement = ITEMREFRESH_BALLOON,
        .object_id = 0x3B,
        .target_state = -1,
    },
    {
        .map = MAP_GALLEON,
        .requirement = ITEMREFRESH_BALLOON,
        .object_id = 0x3C,
        .target_state = -1,
    },
    // Monkeyport
    {
        .map = MAP_CASTLEBALLROOM,
        .requirement = ITEMREFRESH_MONKEYPORT,
        .object_id = 0x5,
        .target_state = -1,
    },
    {
        .map = MAP_CASTLEMUSEUM,
        .requirement = ITEMREFRESH_MONKEYPORT,
        .object_id = 0x8,
        .target_state = -1,
    },
    {
        .map = MAP_CASTLEMUSEUM,
        .requirement = ITEMREFRESH_MONKEYPORT,
        .object_id = 0x9,
        .target_state = -1,
    },
    {
        .map = MAP_CASTLEMUSEUM,
        .requirement = ITEMREFRESH_MONKEYPORT,
        .object_id = 0xA,
        .target_state = -1,
    },
    {
        .map = MAP_CAVES,
        .requirement = ITEMREFRESH_MONKEYPORT,
        .object_id = 0x2C,
        .target_state = -1,
    },
    {
        .map = MAP_CAVES,
        .requirement = ITEMREFRESH_MONKEYPORT,
        .object_id = 0x2A,
        .target_state = -1,
    },
    {
        .map = MAP_CAVES,
        .requirement = ITEMREFRESH_MONKEYPORT,
        .object_id = 0xDE,
        .target_state = -1,
    },
    {
        .map = MAP_CAVES,
        .requirement = ITEMREFRESH_MONKEYPORT,
        .object_id = 0x33,
        .target_state = -1,
    },
    {
        .map = MAP_CAVES,
        .requirement = ITEMREFRESH_MONKEYPORT,
        .object_id = 0x2C,
        .target_state = -1,
    },
    {
        .map = MAP_ISLES,
        .requirement = ITEMREFRESH_MONKEYPORT,
        .object_id = 0x37,
        .target_state = -1,
    },
    {
        .map = MAP_ISLES,
        .requirement = ITEMREFRESH_MONKEYPORT,
        .object_id = 0x38,
        .target_state = 0,
    },
    // Gone
    {
        .map = MAP_CASTLESHED,
        .requirement = ITEMREFRESH_GONE,
        .object_id = 0x4,
        .target_state = -1,
    },
    {
        .map = MAP_CAVES,
        .requirement = ITEMREFRESH_GONE,
        .object_id = 0x3D,
        .target_state = -1,
    },
    {
        .map = MAP_CAVES5DCCHUNKY,
        .requirement = ITEMREFRESH_GONE,
        .object_id = 0x6,
        .target_state = -1,
    },
    {
        .map = MAP_FUNGILOBBY,
        .requirement = ITEMREFRESH_GONE,
        .object_id = 0x8,
        .target_state = -1,
    },
    {
        .map = MAP_HELMLOBBY,
        .requirement = ITEMREFRESH_GONE,
        .object_id = 0x3,
        .target_state = 0,
    },
};

typedef struct swingable_paad {
    /* 0x000 */ char unk_00[0x28];
    /* 0x028 */ char vine_complete;
} swingable_paad;

void refreshPads(pad_refresh_signals signal) {
    /**
     * @brief Refresh objects to coincide with an item collection
     * 
     * @param signal Pad Refresh Signal
     */
    if (signal == ITEMREFRESH_VINE) {
        int vine_complete = 1;
        for (int i = 0; i < ActorCount; i++) {
            actorData* actor = (actorData*)ActorArray[i];
            int actor_type = actor->actorType;
            if ((actor_type == 33) || (actor_type == 69) || (actor_type == 116)) {
                swingable_paad* paad = actor->paad;
                paad->vine_complete = vine_complete;
                if (vine_complete) {
                    actor->obj_props_bitfield |= 0x04008004;
                    actor->obj_props_bitfield &= 0xFF7FFFFF;
                }
            }
        }
    } else {
        int _count = ObjectModel2Count;
        int *m2location = (int *)ObjectModel2Pointer;
        for (int i = 0; i < (int)(sizeof(pads) / sizeof(pad_refresh_struct)); i++) {
            if ((CurrentMap == pads[i].map) && (signal == pads[i].requirement)) {
                int found_item = 0;
                int j = 0;
                while ((!found_item) && (j < _count)) {
                    ModelTwoData*_object = getObjectArrayAddr(m2location, 0x90, j);
                    if (_object->object_id == pads[i].object_id) {
                        behaviour_data* behavior = _object->behaviour_pointer;
                        if (behavior) {
                            if (pads[i].target_state >= 0) {
                                behavior->current_state = pads[i].target_state;   
                                behavior->next_state = pads[i].target_state;   
                            }
                            behavior->unk_60 = 0; // Remove opacity filter
                            behavior->pause_state = 1; // Set script to run
                        }
                        found_item = 1;
                        break;
                    }
                    j += 1;
                }            
            }
        }
    }
}