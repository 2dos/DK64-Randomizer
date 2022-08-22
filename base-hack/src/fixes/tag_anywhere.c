#include "../../include/common.h"

#define TAG_ANYWHERE_KONG_LIMIT 5

static const unsigned char banned_maps[] = {
    1, // Funky's Store | Reason: Shop
    2, // DK Arcade | Reason: Locked Movement
    5, // Cranky's Lab | Reason: Shop
    6, // Jungle Japes: Minecart | Reason: Locked Movement
    8, // Jungle Japes: Army Dillo | Reason: Boss Map
    9, // Jetpac | Reason: Locked Movement
    10, // Kremling Kosh! (very easy) | Reason: Locked Movement
    14, // Angry Aztec: Beetle Race | Reason: Locked Movement
    15, // Snide's H.Q. | Reason: Shop
    18, // Teetering Turtle Trouble! (very easy) | Reason: Locked Movement
    25, // Candy's Music Shop | Reason: Shop
    27, // Frantic Factory: Car Race | Reason: Locked Movement
    28, // Hideout Helm (Level Intros, Game Over) | Reason: Cutscene Map
    32, // Batty Barrel Bandit! (easy) | Reason: Locked Movement
    37, // Jungle Japes: Barrel Blast | Reason: BBlast Course
    39, // Gloomy Galleon: Seal Race | Reason: Locked Movement
    40, // Nintendo Logo | Reason: Cutscene Map
    41, // Angry Aztec: Barrel Blast | Reason: BBlast Course
    54, // Gloomy Galleon: Barrel Blast | Reason: BBlast Course
    55, // Fungi Forest: Minecart | Reason: Locked Movement
    76, // DK Rap | Reason: Cutscene Map
    77, // Minecart Mayhem! (easy) | Reason: Locked Movement
    78, // Busy Barrel Barrage! (easy) | Reason: Locked Movement
    79, // Busy Barrel Barrage! (normal) | Reason: Locked Movement
    80, // Main Menu | Reason: Locked Movement
    81, // Title Screen (Not For Resale Version) | Reason: Cutscene Map
    82, // Crystal Caves: Beetle Race | Reason: Locked Movement
    83, // Fungi Forest: Dogadon | Reason: Boss Map
    101, // Krazy Kong Klamour! (easy) | Reason: Locked Movement
    102, // Big Bug Bash! (very easy) | Reason: Locked Movement
    103, // Searchlight Seek! (very easy) | Reason: Locked Movement
    104, // Beaver Bother! (easy) | Reason: Locked Movement
    107, // Kong Battle: Battle Arena | Reason: Multiplayer Map
    109, // Kong Battle: Arena 1 | Reason: Multiplayer Map
    110, // Frantic Factory: Barrel Blast | Reason: BBlast Course
    111, // Gloomy Galleon: Pufftoss | Reason: Boss Map
    115, // Kremling Kosh! (easy) | Reason: Locked Movement
    116, // Kremling Kosh! (normal) | Reason: Locked Movement
    117, // Kremling Kosh! (hard) | Reason: Locked Movement
    118, // Teetering Turtle Trouble! (easy) | Reason: Locked Movement
    119, // Teetering Turtle Trouble! (normal) | Reason: Locked Movement
    120, // Teetering Turtle Trouble! (hard) | Reason: Locked Movement
    121, // Batty Barrel Bandit! (easy) | Reason: Locked Movement
    122, // Batty Barrel Bandit! (normal) | Reason: Locked Movement
    123, // Batty Barrel Bandit! (hard) | Reason: Locked Movement
    129, // Minecart Mayhem! (normal) | Reason: Locked Movement
    130, // Minecart Mayhem! (hard) | Reason: Locked Movement
    131, // Busy Barrel Barrage! (hard) | Reason: Locked Movement
    136, // Beaver Bother! (normal) | Reason: Locked Movement
    137, // Beaver Bother! (hard) | Reason: Locked Movement
    138, // Searchlight Seek! (easy) | Reason: Locked Movement
    139, // Searchlight Seek! (normal) | Reason: Locked Movement
    140, // Searchlight Seek! (hard) | Reason: Locked Movement
    141, // Krazy Kong Klamour! (normal) | Reason: Locked Movement
    142, // Krazy Kong Klamour! (hard) | Reason: Locked Movement
    143, // Krazy Kong Klamour! (insane) | Reason: Locked Movement
    144, // Peril Path Panic! (very easy) | Reason: Locked Movement
    145, // Peril Path Panic! (easy) | Reason: Locked Movement
    146, // Peril Path Panic! (normal) | Reason: Locked Movement
    147, // Peril Path Panic! (hard) | Reason: Locked Movement
    148, // Big Bug Bash! (easy) | Reason: Locked Movement
    149, // Big Bug Bash! (normal) | Reason: Locked Movement
    150, // Big Bug Bash! (hard) | Reason: Locked Movement
    152, // Hideout Helm (Intro Story) | Reason: Cutscene Map
    153, // DK Isles (DK Theatre) | Reason: Cutscene Map
    154, // Frantic Factory: Mad Jack | Reason: Boss Map
    172, // Rock (Intro Story) | Reason: Cutscene Map
    184, // Enguarde Arena | Reason: Enguarde-Only Room
    186, // Crystal Caves: Barrel Blast | Reason: BBlast Course
    187, // Creepy Castle: Barrel Blast | Reason: BBlast Course
    188, // Fungi Forest: Barrel Blast | Reason: BBlast Course
    190, // Kong Battle: Arena 2 | Reason: Multiplayer Map
    191, // Rambi Arena | Reason: Rambi-Only Room
    192, // Kong Battle: Arena 3 | Reason: Multiplayer Map
    196, // Crystal Caves: Army Dillo | Reason: Boss Map
    197, // Angry Aztec: Dogadon | Reason: Boss Map
    198, // Training Grounds (End Sequence) | Reason: Cutscene Map
    199, // Creepy Castle: King Kut Out | Reason: Boss Map
    203, // K. Rool Fight: DK Phase | Reason: Boss Map
    204, // K. Rool Fight: Diddy Phase | Reason: Boss Map
    205, // K. Rool Fight: Lanky Phase | Reason: Boss Map
    206, // K. Rool Fight: Tiny Phase | Reason: Boss Map
    207, // K. Rool Fight: Chunky Phase | Reason: Boss Map
    208, // Bloopers Ending | Reason: Cutscene Map
    212, // K. Rool Barrel: DK's Rambi Game | Reason: Rambi-Only Room
    213, // K. Lumsy Ending | Reason: Cutscene Map
    214, // K. Rool's Shoe | Reason: Boss Map
    215, // K. Rool's Arena | Reason: Cutscene Map
};

static const unsigned char bad_movement_states[] = {
	//0x02, // First Person Camera
	//0x03, // First Person Camera (Water)
	0x04, // Fairy Camera
	0x05, // Fairy Camera (Water)
	0x06, // Locked (Bonus Barrel)
	0x15, // Slipping
	0x16, // Slipping
	0x18, // Baboon Blast Pad
	0x1B, // Simian Spring
	//0x1C, // Simian Slam // Note: As far as I know this doesn't break anything, so we'll save the CPU cycles
	0x20, // Falling/Splat, // Note: Prevents quick recovery from fall damage, and I guess maybe switching to avoid fall damage?
	0x2D, // Shockwave
	0x2E, // Chimpy Charge
	0x31, // Damaged
	0x32, // Stunlocked
	0x33, // Damaged
	0x35, // Damaged
	0x36, // Death
	0x37, // Damaged (Underwater)
	0x38, // Damaged
	0x39, // Shrinking
	0x42, // Barrel
	0x43, // Barrel (Underwater)
	0x44, // Baboon Blast Shot
	0x45, // Cannon Shot
	0x52, // Bananaporter
	0x53, // Monkeyport
	0x54, // Bananaporter (Multiplayer)
	0x56, // Locked
	0x57, // Swinging on Vine
	0x58, // Leaving Vine
	0x59, // Climbing Tree
	0x5A, // Leaving Tree
	0x5B, // Grabbed Ledge
	0x5C, // Pulling up on Ledge
	0x63, // Rocketbarrel // Note: Covered by crystal HUD check except for Helm & K. Rool
	0x64, // Taking Photo
	0x65, // Taking Photo
	0x67, // Instrument
	0x69, // Car
	0x6A, // Learning Gun // Note: Handled by map check
	0x6B, // Locked
	0x6C, // Feeding T&S // Note: Handled by map check
	0x6D, // Boat
	0x6E, // Baboon Balloon
	0x6F, // Updraft
	0x70, // GB Dance
	0x71, // Key Dance
	0x72, // Crown Dance
	0x73, // Loss Dance
	0x74, // Victory Dance
	0x78, // Gorilla Grab
	0x79, // Learning Move // Note: Handled by map check
	0x7A, // Locked
	0x7B, // Locked
	0x7C, // Trapped (spider miniBoss)
	0x7D, // Klaptrap Kong (beaver bother) // Note: Handled by map check
	0x83, // Fairy Refill
	0x87, // Entering Portal
	0x88, // Exiting Portal
};

static const short kong_flags[] = {0x181,0x6,0x46,0x42,0x75};
static unsigned char tag_countdown = 0;
static char can_tag_anywhere = 0;

int canTagAnywhere(int prev_crystals) {
    if (Player->strong_kong_ostand_bitfield & 0x100) {
        // Seasick
        return 0;
    }
    if (Player->collision_queue_pointer) {
        return 0;
    }
    int control_state = Player->control_state;
    for (int i = 0; i < sizeof(bad_movement_states); i++) {
        if (bad_movement_states[i] == control_state) {
            return 0;
        }
    }
    if ((prev_crystals - 1) == CollectableBase.Crystals) {
        return 0;
    }
    if (CutsceneActive) {
        return 0;
    }
    if (ModelTwoTouchCount > 0) {
        return 0;
    }
    if (CurrentMap == 0x2A) {
        if (MapState & 0x10) {
            return 0;
        }
        if (hasTurnedInEnoughCBs()) {
            if (Player->zPos < 560.0f) {
                // Too close to boss door
                return 0;
            }
        }
    }
    for (int i = 0; i < LoadedActorCount; i++) {
        if (LoadedActorArray[i].actor) {
            int tested_type = LoadedActorArray[i].actor->actorType;
            if (tested_type == 48) { // Coconut
                return 0;
            } else if (tested_type == 36) { // Peanut
                return 0;
            } else if (tested_type == 42) { // Grape
                return 0;
            } else if (tested_type == 43) { // Feather
                if (LoadedActorArray[i].actor->control_state == 0) {
                    return 0;
                }
            } else if (tested_type == 38) { // Pineapple
                return 0;
            }
        }
    }
    if (TBVoidByte & 3) {
        return 0;
    }
    if (tag_countdown != 0) {
        return 0;
    }
    for (int i = 0; i < sizeof(banned_maps); i++) {
        if (banned_maps[i] == CurrentMap) {
            return 0;
        }
    }
    return 1;
}

int getTAState(void) {
    return can_tag_anywhere;
}

int getTagAnywhereKong(int direction) {
    int next_character = Character + direction;
    if (next_character < 0) {
        next_character = TAG_ANYWHERE_KONG_LIMIT - 1;
    } else if (next_character >= TAG_ANYWHERE_KONG_LIMIT) {
        next_character = 0;
    }
    int i = 0;
    int reached_limit = 0;
    while (i < TAG_ANYWHERE_KONG_LIMIT) {
        int pass = 0;
        if (checkFlag(kong_flags[next_character],0)) {
            pass = 1;
            if (Rando.perma_lose_kongs) {
                if (checkFlag(KONG_LOCKED_START + next_character,0)) {
                    if ((!curseRemoved()) && (!hasPermaLossGrace())) {
                        pass = 0;
                    }
                }
            }
        }
        if (pass) {
            break;
        } else {
            if ((i + 1) == TAG_ANYWHERE_KONG_LIMIT) {
                reached_limit = 1;
                return Character;
            } else {
                next_character = next_character + direction;
                if (next_character < 0) {
                    next_character = TAG_ANYWHERE_KONG_LIMIT - 1;
                } else if (next_character >= TAG_ANYWHERE_KONG_LIMIT) {
                    next_character = 0;
                }
            }
        }
        i++;
    }
    if (reached_limit) {
        return Character;
    } else {
        return next_character;
    }
}

static const unsigned char important_huds[] = {0,1};
static unsigned char important_huds_changed[] = {0,0};

void tagAnywhere(int prev_crystals) {
	if (Rando.tag_anywhere) {
		if (Player) {
            if (tag_countdown > 0) {
                tag_countdown -= 1;
            }
            if (CurrentMap == 0x2A) {
                if (tag_countdown == 2) {
                    HUD->item[0].hud_state = 1;
                    if (Player->control_state == 108) {
                        int world = getWorld(CurrentMap,0);
                        if (MovesBase[(int)Character].cb_count[world] > 0) {
                            HUD->item[0].hud_state = 0;
                        }
                    }
                } else if (tag_countdown == 1) {
                    if (Player->control_state == 108) {
                        int world = getWorld(CurrentMap,0);
                        if (MovesBase[(int)Character].cb_count[world] > 0) {
                            HUD->item[0].hud_state = 1;
                        }
                    }
                }
            } else {
                if (tag_countdown == 2) {
                    for (int i = 0; i < sizeof(important_huds); i++) {
                        if (important_huds_changed[i]) {
                            HUD->item[(int)important_huds[i]].hud_state = 0;
                        }
                    }
                } else if (tag_countdown == 1) {
                    for (int i = 0; i < sizeof(important_huds); i++) {
                        if (important_huds_changed[i]) {
                            HUD->item[(int)important_huds[i]].hud_state = 1;
                        }
                    }
                }
            }
            int can_ta = canTagAnywhere(prev_crystals);
            can_tag_anywhere = can_ta;
            if (!can_ta) {
                return;
            }
			if (Character < TAG_ANYWHERE_KONG_LIMIT) {
				int change = 0;
				if (NewlyPressedControllerInput.Buttons & D_Left) {
					change = -1;
				} else if (NewlyPressedControllerInput.Buttons & D_Right) {
					change = 1;
				} else {
					return;
				}
				if (change != 0) {
                    int next_character = getTagAnywhereKong(change);
					if (next_character != Character) {
						if (((MovesBase[next_character].weapon_bitfield & 1) == 0) || (Player->was_gun_out == 0)) {
                            Player->hand_state = 1;
                            Player->was_gun_out = 0;
                            // Without this, tags to and from Diddy mess up
                            if (next_character == 1) {
                                Player->hand_state = 0;
                            }
                        } else {
                            Player->hand_state = 2;
                            Player->was_gun_out = 1;
                            // Without this, tags to and from Diddy mess up
                            if (next_character == 1) {
                                Player->hand_state = 3;
                            }
                        };
                        // Fix HUD memes
                        if (CurrentMap == 0x2A) {
                            if (!hasTurnedInEnoughCBs()) {
                                tag_countdown = 3;
                                HUD->item[0].hud_state_timer = 0x100;
                                HUD->item[0].hud_state = 0;
                            }
                        } else {
                            for (int i = 0; i < sizeof(important_huds); i++) {
                                important_huds_changed[i] = 0;
                                if (HUD) {
                                    int hud_st = HUD->item[(int)important_huds[i]].hud_state;
                                    if ((hud_st == 1) || (hud_st == 2)) {
                                        tag_countdown = 3;
                                        HUD->item[(int)important_huds[i]].hud_state_timer = 0;
                                        HUD->item[(int)important_huds[i]].hud_state = 0;
                                        important_huds_changed[i] = 1;
                                    }
                                }
                            }
                        }
                        tagKong(next_character + 2);
						clearTagSlide(Player);
						Player->new_kong = next_character + 2;
					}
				}
			}
		}
	}
}

void tagAnywhereInit(int is_homing, int model2_id, int obj) {
    assessFlagMapping(CurrentMap, model2_id);
    coinCBCollectHandle(0, obj, is_homing);
}

void tagAnywhereAmmo(int player, int obj, int is_homing) {
    coinCBCollectHandle(player, obj, is_homing);
    if (player_count == 1) {
        displayItemOnHUD(2 + is_homing,0,0);
    }
}

void tagAnywhereBunch(int player, int obj, int is_homing) {
    coinCBCollectHandle(player, obj, is_homing);
    playSFX(Banana);
}