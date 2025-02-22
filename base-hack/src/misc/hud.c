/**
 * @file hud.c
 * @author Ballaam
 * @brief Operation of HUD Elements
 * @version 0.1
 * @date 2022-07-17
 * 
 * @copyright Copyright (c) 2022
 * 
 */
#include "../../include/common.h"

#define ICON_SCALE 2.0f
#define DPAD_SCALE 2.5f
#define DPAD_X 1025
#define DPAD_Y_HIGH 100
#define DPAD_Y_LOW 250
#define HUD_CHECK_COUNT 4

#define CAN_USE_DPAD 1
#define CAN_SHOW_DPAD 2

typedef enum dpad_visual_enum {
    /* 0 */ DPADVISIBLE_HIDE,
    /* 1 */ DPADVISIBLE_ALL,
    /* 2 */ DPADVISIBLE_MINIMAL,
} dpad_visual_enum;

static unsigned char race_maps[] = {
    MAP_JAPESMINECART,
    MAP_FUNGIMINECART,
    MAP_CASTLEMINECART,
    MAP_AZTECBEETLE,
    MAP_CAVESBEETLERACE,
    MAP_FACTORYCARRACE,
    MAP_CASTLECARRACE,
    MAP_GALLEONSEALRACE
};

typedef struct hud_element_definition {
    /* 0x000 */ short x;
    /* 0x002 */ short y;
    /* 0x004 */ float unk0;
    /* 0x008 */ float unk1;
    /* 0x00C */ short* counter;
    /* 0x010 */ short cheat;
    /* 0x012 */ char run_allocation;
    /* 0x013 */ unsigned char sprite_index[5]; // One per kong
} hud_element_definition;

static short hud_counts[(ITEMID_TERMINATOR - ITEMID_CHAOSBLOCKER_KONG)] = {};

static const hud_element_definition elements[] = {
    {
        // CB (T&S)
        .x = 0x1E, .y=0x26, .unk0 = 15.5f, .unk1=26.0f,
        .cheat=0, .counter=(short*)0, .run_allocation=1,
        .sprite_index={0x40, 0x3D, 0x3F, 0x41, 0x3E},
    },
    {
        // Coins = cheat is normally 2, but disabled
        .x = 0x122, .y=0x26, .unk0 = 16.5f, .unk1=-19.0f,
        .cheat=0, .counter=(short*)0, .run_allocation=1,
        .sprite_index={0x35, 0x32, 0x34, 0x36, 0x33},
    },
    {
        // Ammo - normally , cheat, but swapping with homing
        .x = 0x122, .y=0x78, .unk0 = 8.5f, .unk1=-19.0f,
        .cheat=4, .counter=&CollectableBase.StandardAmmo, .run_allocation=1,
        .sprite_index={68, 36, 45, 77, 42},
    },
    {
        // Homing Ammo
        .x = 0x122, .y=0x78, .unk0 = 8.5f, .unk1=-19.0f,
        .cheat=0, .counter=&CollectableBase.HomingAmmo, .run_allocation=1,
        .sprite_index={68, 36, 45, 77, 42},
    },
    {
        // Oranges
        .x = 0x122, .y=0x8E, .unk0 = 1.5f, .unk1=-19.0f,
        .cheat=8, .counter=&CollectableBase.Oranges, .run_allocation=1,
        .sprite_index={57, 57, 57, 57, 57},
    },
    {
        // Crystals
        .x = 0x122, .y=0xA4, .unk0 = -5.5f, .unk1=-19.0f,
        .cheat=0x20, .counter=&CollectableBase.Crystals, .run_allocation=1,
        .sprite_index={58, 58, 58, 58, 58},
    },
    {
        // Film
        .x = 0x122, .y=0xD0, .unk0 = -19.5f, .unk1=-19.0f,
        .cheat=0x10, .counter=&CollectableBase.Film, .run_allocation=1,
        .sprite_index={56, 56, 56, 56, 56},
    },
    {
        // Instrument
        .x = 0x122, .y=0xBA, .unk0 = -12.5f, .unk1=-19.0f,
        .cheat=0x40, .counter=&CollectableBase.InstrumentEnergy, .run_allocation=1,
        .sprite_index={79, 78, 82, 80, 81},
    },
    {
        // GB Kong
        .x = 0x1E, .y=0x48, .unk0 = 1.5f, .unk1=26.0f,
        .cheat=0, .counter=(short*)0, .run_allocation=1,
        .sprite_index={59, 59, 59, 59, 59},
    },
    {
        // GB Total
        .x = 0x7A, .y=0xD0, .unk0 = 0, .unk1=0,
        .cheat=0, .counter=(short*)0, .run_allocation=0,
        .sprite_index={59, 59, 59, 59, 59},
    },
    {
        // Medal
        .x = 0x52, .y=0xD0, .unk0 = -26.5f, .unk1=26.0f,
        .cheat=0, .counter=(short*)0, .run_allocation=1,
        .sprite_index={0x3C, 0x3C, 0x3C, 0x3C, 0x3C},
    },
    {
        // Race Coin
        .x = 0x122, .y=0x26, .unk0 = 16.5f, .unk1=-19.0f,
        .cheat=0, .counter=(short*)0x80750AC4, .run_allocation=1,
        .sprite_index={73, 73, 73, 73, 73},
    },
    {
        // Blueprint
        .x = 0xC2, .y=0xD0, .unk0 = -26.5f, .unk1=-19.0f,
        .cheat=0, .counter=(short*)0, .run_allocation=1,
        .sprite_index={92, 90, 74, 93, 91},
    },
    {
        // CBs
        .x = 0x122, .y=0x26, .unk0 = -5.5f, .unk1=-26.0f,
        .cheat=0, .counter=(short*)0, .run_allocation=1,
        .sprite_index={0x40, 0x3D, 0x3F, 0x41, 0x3E},
    },
    {
        // Move Cost
        .x = 0x1E, .y=0x26, .unk0 = 15.5f, .unk1=-19.0f,
        .cheat=0, .counter=(short*)0x80750AC8, .run_allocation=1,
        .sprite_index={0x35, 0x32, 0x34, 0x36, 0x33},
    },
    {
        // Multibunch
        .x = 0x122, .y=0x62, .unk0 = 8.5f, .unk1=-19.0f,
        .cheat=0, .counter=(short*)0, .run_allocation=1,
        .sprite_index={168, 168, 168, 168, 168},
    },
    // START OF B LOCKER ITEMS
    {
        // Kong - 0
        .x = 0x7A, .y=0xD0, .unk0 = 0, .unk1=0,
        .cheat=0, .counter=&hud_counts[ITEMID_CHAOSBLOCKER_KONG - ITEMID_CHAOSBLOCKER_KONG], .run_allocation=1,
        .sprite_index={0xA9, 0xAA, 0xAB, 0xAC, 0xAD},
    },
    {
        // Move - 1
        .x = 0x7A, .y=0xD0, .unk0 = 0, .unk1=0,
        .cheat=0, .counter=&hud_counts[ITEMID_CHAOSBLOCKER_MOVE - ITEMID_CHAOSBLOCKER_KONG], .run_allocation=1,
        .sprite_index={0x94, 0x94, 0x94, 0x94, 0x94},
    },
    {
        // GB - 2
        .x = 0x7A, .y=0xD0, .unk0 = 0, .unk1=0,
        .cheat=0, .counter=&hud_counts[ITEMID_CHAOSBLOCKER_GB - ITEMID_CHAOSBLOCKER_KONG], .run_allocation=1,
        .sprite_index={0x3B, 0x3B, 0x3B, 0x3B, 0x3B},
    },
    {
        // BP - 3
        .x = 0x7A, .y=0xD0, .unk0 = 0, .unk1=0,
        .cheat=0, .counter=&hud_counts[ITEMID_CHAOSBLOCKER_BLUEPRINT - ITEMID_CHAOSBLOCKER_KONG], .run_allocation=1,
        .sprite_index={92, 90, 74, 93, 91},
    },
    {
        // Fairy - 4
        .x = 0x7A, .y=0xD0, .unk0 = 0, .unk1=0,
        .cheat=0, .counter=&hud_counts[ITEMID_CHAOSBLOCKER_FAIRY - ITEMID_CHAOSBLOCKER_KONG], .run_allocation=1,
        .sprite_index={0x89, 0x89, 0x89, 0x89, 0x89},
    },
    {
        // Key - 5
        .x = 0x7A, .y=0xD0, .unk0 = 0, .unk1=0,
        .cheat=0, .counter=&hud_counts[ITEMID_CHAOSBLOCKER_KEY - ITEMID_CHAOSBLOCKER_KONG], .run_allocation=1,
        .sprite_index={0x8A, 0x8A, 0x8A, 0x8A, 0x8A},
    },
    {
        // Crown - 6
        .x = 0x7A, .y=0xD0, .unk0 = 0, .unk1=0,
        .cheat=0, .counter=&hud_counts[ITEMID_CHAOSBLOCKER_CROWN - ITEMID_CHAOSBLOCKER_KONG], .run_allocation=1,
        .sprite_index={139, 139, 139, 139, 139},
    },
    {
        // Comapny Coin - 7
        .x = 0x7A, .y=0xD0, .unk0 = 0, .unk1=0,
        .cheat=0, .counter=&hud_counts[ITEMID_CHAOSBLOCKER_COMPANYCOIN - ITEMID_CHAOSBLOCKER_KONG], .run_allocation=1,
        .sprite_index={0x92, 0x92, 0x92, 0x92, 0x92}, // Handled externally
    },
    {
        // Medal - 8
        .x = 0x7A, .y=0xD0, .unk0 = 0, .unk1=0,
        .cheat=0, .counter=&hud_counts[ITEMID_CHAOSBLOCKER_MEDAL - ITEMID_CHAOSBLOCKER_KONG], .run_allocation=1,
        .sprite_index={0x3C, 0x3C, 0x3C, 0x3C, 0x3C},
    },
    {
        // Bean - 9
        .x = 0x7A, .y=0xD0, .unk0 = 0, .unk1=0,
        .cheat=0, .counter=&hud_counts[ITEMID_CHAOSBLOCKER_BEAN - ITEMID_CHAOSBLOCKER_KONG], .run_allocation=1,
        .sprite_index={0x92, 0x92, 0x92, 0x92, 0x92}, // Handled externally
    },
    {
        // Pearl - 10
        .x = 0x7A, .y=0xD0, .unk0 = 0, .unk1=0,
        .cheat=0, .counter=&hud_counts[ITEMID_CHAOSBLOCKER_PEARL - ITEMID_CHAOSBLOCKER_KONG], .run_allocation=1,
        .sprite_index={0x92, 0x92, 0x92, 0x92, 0x92}, // Handled externally
    },
    {
        // Rainbow Coin - 11
        .x = 0x7A, .y=0xD0, .unk0 = 0, .unk1=0,
        .cheat=0, .counter=&hud_counts[ITEMID_CHAOSBLOCKER_RAINBOWCOIN - ITEMID_CHAOSBLOCKER_KONG], .run_allocation=1,
        .sprite_index={0xA0, 0xA0, 0xA0, 0xA0, 0xA0},
    },
    {
        // Ice Trap - 12
        .x = 0x7A, .y=0xD0, .unk0 = 0, .unk1=0,
        .cheat=0, .counter=&hud_counts[ITEMID_CHAOSBLOCKER_ICETRAP - ITEMID_CHAOSBLOCKER_KONG], .run_allocation=1,
        .sprite_index={0x3B, 0x3B, 0x3B, 0x3B, 0x3B}, // TODO: handle sprites for this
    },
    {
        // Game Percentage - 13
        .x = 0x7A, .y=0xD0, .unk0 = 0, .unk1=0,
        .cheat=0, .counter=&hud_counts[ITEMID_CHAOSBLOCKER_GAMEPERCENTAGE - ITEMID_CHAOSBLOCKER_KONG], .run_allocation=1,
        .sprite_index={0x92, 0x92, 0x92, 0x92, 0x92}, // TODO: handle sprites for this
    },
    {
        // Colored Banana - 14
        .x = 0x7A, .y=0xD0, .unk0 = 0, .unk1=0,
        .cheat=0, .counter=&hud_counts[ITEMID_CHAOSBLOCKER_COLOREDBANANA - ITEMID_CHAOSBLOCKER_KONG], .run_allocation=1,
        .sprite_index={128, 126, 127, 129, 125},
    },
    {
        // Terminator
        .x = 0, .y=0, .unk0 = 0.0f, .unk1=0.0f,
        .cheat=0, .counter=(short*)0, .run_allocation=0,
        .sprite_index={0, 0, 0, 0, 0},
    },
    {
        // SCOFF
        .x = 0, .y = 0, .unk0 = 0.0f, .unk1 = 0.0f,
        .cheat = 0, .counter=(short*)0, .run_allocation=0,
        .sprite_index={167, 167, 167, 167, 167},
    },
    {
        // FUNKY
        .x = 0, .y = 0, .unk0 = 0.0f, .unk1 = 0.0f,
        .cheat = 0, .counter=(short*)0, .run_allocation=0,
        .sprite_index={150, 150, 150, 150, 150},
    },
    {
        // CANDY
        .x = 0, .y = 0, .unk0 = 0.0f, .unk1 = 0.0f,
        .cheat = 0, .counter=(short*)0, .run_allocation=0,
        .sprite_index={147, 147, 147, 147, 147},
    },
    {
        // CRANKY
        .x = 0, .y = 0, .unk0 = 0.0f, .unk1 = 0.0f,
        .cheat = 0, .counter=(short*)0, .run_allocation=0,
        .sprite_index={148, 148, 148, 148, 148},
    },
    {
        // DK
        .x = 0, .y = 0, .unk0 = 0.0f, .unk1 = 0.0f,
        .cheat = 0, .counter=(short*)0, .run_allocation=0,
        .sprite_index={169, 169, 169, 169, 169},
    },
    {
        // DIDDY
        .x = 0, .y = 0, .unk0 = 0.0f, .unk1 = 0.0f,
        .cheat = 0, .counter=(short*)0, .run_allocation=0,
        .sprite_index={170, 170, 170, 170, 170},
    },
    {
        // LANKY
        .x = 0, .y = 0, .unk0 = 0.0f, .unk1 = 0.0f,
        .cheat = 0, .counter=(short*)0, .run_allocation=0,
        .sprite_index={171, 171, 171, 171, 171},
    },
    {
        // TINY
        .x = 0, .y = 0, .unk0 = 0.0f, .unk1 = 0.0f,
        .cheat = 0, .counter=(short*)0, .run_allocation=0,
        .sprite_index={172, 172, 172, 172, 172},
    },
    {
        // CHUNKY
        .x = 0, .y = 0, .unk0 = 0.0f, .unk1 = 0.0f,
        .cheat = 0, .counter=(short*)0, .run_allocation=0,
        .sprite_index={173, 173, 173, 173, 173},
    },
};

void initHUDDirection(placementData* hud_data, int item) {
	/**
	 * @brief Modified initialization of HUD Direction function to account for new medal changes.
	 */
	int x_direction = 0;
	int y_direction = 0;
	hud_data->unk_0C = 0;
	switch(item) {
		case ITEMID_CB: // CB
		case ITEMID_CBS_0: // CB T&S
		case ITEMID_MOVECOST: // Move Cost
			x_direction = -1;
			break;
		case ITEMID_GBS: // GBs
		case ITEMID_BPFAIRY: // Blueprint
			y_direction = 1;
			break;
		default:
			x_direction = 1;
		break;
	}
    if ((item >= ITEMID_CHAOSBLOCKER_KONG) && (item < ITEMID_TERMINATOR)) {
        y_direction = 1;
        x_direction = 0;
    }
	hud_data->x_direction = x_direction * 0x30;
	hud_data->y_direction = y_direction * 0x30;
}

void allocateHUD(int reallocate) {
    int cheat_bitfield = 0; // TODO: Hook this up
    int world = getWorld(CurrentMap, 1);
    if (reallocate) {
        HUD = dk_malloc(ITEMID_TERMINATOR * 0x30);
        wipeMallocSpace(HUD);
        *(int*)(0x80754284) = 0; // TODO: Figure out what this does, label it
    }
    int kong = getKong(0);
    KongBase* kong_info = &MovesBase[kong];
    int in_dktv = inDKTV();
    for (int i = 0; i < ITEMID_TERMINATOR; i++) {
        hud_element* element = &HUD->item[i];
        hud_element_definition* element_def = (hud_element_definition*)&elements[i];
        if (reallocate) {
            element->hud_state = 0;
            element->hud_state_timer = 0;
            element->unk_24 = 0;
            element->placement_pointer = (placementData*)0;
            element->infinite_setting = 0;
        }
        if (in_dktv) {
            element->infinite_setting = 1;
        }
        int written_cheat = 0;
        // Write Stuff, normally in switch case
        if (element_def->cheat) {
            if (cheat_bitfield & element_def->cheat) {
                *(element->item_count_pointer) = correctRefillCap(i, 0);
                written_cheat = 1;
            }
        }
        element->item_count_pointer = element_def->counter;
        int item_x = element_def->x;
        int item_y = element_def->y;
        if (i == ITEMID_CB) {
            element->item_count_pointer = &kong_info->cb_count[world];
        } else if (i == ITEMID_COINS) {
            element->item_count_pointer = (short*)&kong_info->unk_05[1];
            if (!inShop(CurrentMap, 0)) {
                item_y = 0x4C;
            }
        } else if (i == ITEMID_INSTRUMENTENERGY) {
            if (!Rando.quality_of_life.global_instrument) {
                element->item_count_pointer = &kong_info->instrument_energy;
            }
        } else if (i == ITEMID_GBKONG) {
            element->item_count_pointer = &kong_info->gb_count[world];
        }
        element->x = item_x;
        element->y = item_y;
        if (element_def->run_allocation) {
            initHUDItem(element_def->unk0, element_def->unk1, &element->unk_10[0], &element->unk_10[1], &element->unk_10[2]);
        }
        // Finalize
        element->unk_2D = written_cheat;
        if (written_cheat) {
            element->infinite_setting = 1;
        }
        if (element->item_count_pointer) {
            element->visual_item_count = *(element->item_count_pointer);
        }
    }
    updateGBCountHUD(0);
    if ((CurrentMap == MAP_HELM) || (CurrentMap == MAP_CAVESBEETLERACE)) {
        setHUDItemAsInfinite(ITEMID_CRYSTALS, 0, 1);
    }
}

void* getHUDSprite_Complex(item_ids item) {
    int kong = getKong(0);
    if (item == ITEMID_CBS_0) {
        kong = *(int*)(0x80745288); // T&S Hover
    }
    if (kong > 4) {
        return (void*)0;
    }
    if (item == ITEMID_CHAOSBLOCKER_BEAN) {
        return &bean_sprite;
    } else if (item == ITEMID_CHAOSBLOCKER_PEARL) {
        return &pearl_sprite;
    } else if (item == ITEMID_CHAOSBLOCKER_COMPANYCOIN) {
        return &company_coin_sprite;
    } else if ((item == ITEMID_STANDARDAMMO) || (item == ITEMID_HOMINGAMMO)) {
        if (isKrushaAdjacentModel(kong)) {
            return (void*)0x80720268; // Orange Ammo
        }
    }
    return sprite_table[elements[item].sprite_index[kong]];
}

void updateBarrierCounts(void) {
    for (int i = 0; i < (ITEMID_TERMINATOR - ITEMID_CHAOSBLOCKER_KONG); i++) {
        int count = getItemCountReq(REQITEM_KONG + i);
        hud_counts[i] = count;
        if (HUD) {
            HUD->item[ITEMID_CHAOSBLOCKER_KONG + i].visual_item_count = count;
        }
    }
}

void displayBarrierHUD(item_ids item, int persist) {
    updateBarrierCounts();
    displayItemOnHUD(item, persist, 0);
}

int canUseDPad(void) {
    /**
     * @brief Determines whether the player will be able to use the DPad Menu.
     * This operates outside of Tag Anywhere as Tag Anywhere has different rules
     * 
     * @return Bitfield of whether the dpad can be shown or used
     */
    if (Gamemode != GAMEMODE_ADVENTURE) {
        return 0; // Not in Adv Mode
    }
    if (player_count > 1) {
        return 0; // In Multiplayer
    }
    if ((CurrentMap == MAP_ISLES) && (CutsceneActive) && (CutsceneIndex == 29)) {
        return 0; // In "K. Rool gets launched" Cutscene
    }
    if (inBossMap(CurrentMap, 0, 1, 1)) {
        return 0; // In 5 main K. Rool Phase Maps or Shoe
    }
    if (TBVoidByte & 2) {
        return 0; // Pausing/Paused
    }
    if (inShop(CurrentMap, 0)) {
        return 0; // In Shop
    }
    if (inU8List(CurrentMap, &race_maps, 8)) {
        return 0; // In Race
    }
    if (inMinigame(CurrentMap)) {
        return CAN_USE_DPAD;
    }
    if (inBattleCrown(CurrentMap)) {
        return CAN_USE_DPAD;
    }
    return CAN_USE_DPAD | CAN_SHOW_DPAD;
}

Gfx* drawDPad(Gfx* dl) {
    /**
     * @brief Draws the DPad menu
     * 
     * @param dl Display List Address
     * 
     * @return New Display List Address
     */
    if (Rando.dpad_visual_enabled == DPADVISIBLE_HIDE) {
        return dl;
    }
    if ((canUseDPad() & CAN_SHOW_DPAD) == 0) {
        return dl;
    }
    int DPAD_Y = DPAD_Y_HIGH;
    int dpad_x_pos = DPAD_X;
    if (Rando.dpad_visual_enabled == DPADVISIBLE_ALL) {
        dl = drawImage(dl, IMAGE_DPAD, RGBA16, 32, 32, dpad_x_pos + 75, DPAD_Y + 70, DPAD_SCALE, DPAD_SCALE, 0xC0);
        if ((Rando.tag_anywhere) && (Character < 5)) {
            // Tag Anywhere Faces
            int kong_left = getTagAnywhereKong(-1);
            int kong_right = getTagAnywhereKong(1);
            int can_ta = getTAState();
            int ta_opacity = 0x80;
            if (can_ta) {
                ta_opacity = 0xFF;
            }
            dl = drawImage(dl, IMAGE_KONG_START + kong_left, RGBA16, 32, 32, dpad_x_pos, DPAD_Y + 70, ICON_SCALE, ICON_SCALE, ta_opacity);
            dl = drawImage(dl, IMAGE_KONG_START + kong_right, RGBA16, 32, 32, dpad_x_pos + 140, DPAD_Y + 70, ICON_SCALE, ICON_SCALE, ta_opacity);
        }
        if (Rando.quality_of_life.ammo_swap) {
            // Homing Ammo Toggle
            if (MovesBase[(int)Character].weapon_bitfield & 2) {
                int render_homing = 1 ^ ForceStandardAmmo;
                if (CollectableBase.HomingAmmo == 0) {
                    render_homing = 0;
                }
                dl = drawImage(dl, IMAGE_AMMO_START + render_homing, RGBA16, 32, 32, dpad_x_pos + 75, DPAD_Y + 145, ICON_SCALE, ICON_SCALE, 0xFF);

            }
        }
    }
    if (Rando.quality_of_life.hud_bp_multibunch) {
        // Blueprint Show
        int applied_requirement = 75;
        if (Rando.medal_cb_req > 0) {
            applied_requirement = Rando.medal_cb_req;
        }
        int mdl_opacity = 0x80;
        int world = getWorld(CurrentMap, 1);
        int world_limit = 7;
        if (Rando.isles_cb_rando) {
            world_limit = 8;
        }
        if (world < world_limit) {
            int kong_sum = MovesBase[(int)Character].tns_cb_count[world] + MovesBase[(int)Character].cb_count[world];
            if (kong_sum >= applied_requirement) {
                mdl_opacity = 0xFF;
            }
        }
        dl = drawImage(dl, 116, RGBA16, 32, 32, dpad_x_pos + 75, DPAD_Y, ICON_SCALE, ICON_SCALE, mdl_opacity);
    }
    return dl;
}

void handleDPadFunctionality(void) {
    /**
     * @brief Handle inputs on the DPad and their corresponding functionality
     */
    if (canUseDPad() & CAN_USE_DPAD) {
        if (Rando.quality_of_life.hud_bp_multibunch) {
            updateMultibunchCount();
            if (NewlyPressedControllerInput.Buttons.d_up) {
                displayItemOnHUD(ITEMID_BPFAIRY,0,0);
                int world = getWorld(CurrentMap,1);
                int world_limit = 7;
                if (Rando.isles_cb_rando) {
                    world_limit = 8;
                }
                if ((world < world_limit) && (CurrentMap != MAP_TROFFNSCOFF)) {
                    displayItemOnHUD(ITEMID_MULTIBUNCH,0,0);
                    if (world < 7) {
                        initDingSprite();
                    }
                }
            }
        }
        if (Rando.quality_of_life.ammo_swap) {
            toggleStandardAmmo();
        }
    }
}