#include "../../include/common.h"

#define TAG_ANYWHERE_KONG_LIMIT 5

static const unsigned char banned_maps[] = {
	1, // Funky's Store
    2, // DK Arcade
    3, // K. Rool Barrel: Lanky's Maze
    5, // Cranky's Lab
    6, // Jungle Japes: Minecart
    8, // Jungle Japes: Army Dillo
    9, // Jetpac
    10, // Kremling Kosh! (very easy)
    14, // Angry Aztec: Beetle Race // Note: Softlock at the end if enabled?
    15, // Snide's H.Q.
    18, // Teetering Turtle Trouble! (very easy)
    25, // Candy's Music Shop
    27, // Frantic Factory: Car Race
    32, // Batty Barrel Bandit! (easy)
    35, // K. Rool Barrel: DK's Target Game
    37, // Jungle Japes: Barrel Blast // Note: The barrels don't work as other kongs so not much point enabling it on this map
    41, // Angry Aztec: Barrel Blast
    50, // K. Rool Barrel: Tiny's Mushroom Game
    54, // Gloomy Galleon: Barrel Blast
    55, // Fungi Forest: Minecart
    76, // DK Rap
    77, // Minecart Mayhem! (easy)
    78, // Busy Barrel Barrage! (easy)
    79, // Busy Barrel Barrage! (normal)
    80, // Main Menu
    82, // Crystal Caves: Beetle Race
    83, // Fungi Forest: Dogadon
    101, // Krazy Kong Klamour! (easy) // Note: Broken with switch kong
    102, // Big Bug Bash! (very easy) // Note: Broken with switch kong
    103, // Searchlight Seek! (very easy) // Note: Broken with switch kong
    104, // Beaver Bother! (easy) // Note: Broken with switch kong
    106, // Creepy Castle: Minecart
    110, // Frantic Factory: Barrel Blast
    111, // Gloomy Galleon: Pufftoss
    115, // Kremling Kosh! (easy)
    116, // Kremling Kosh! (normal)
    117, // Kremling Kosh! (hard)
    118, // Teetering Turtle Trouble! (easy)
    119, // Teetering Turtle Trouble! (normal)
    120, // Teetering Turtle Trouble! (hard)
    121, // Batty Barrel Bandit! (easy)
    122, // Batty Barrel Bandit! (normal)
    123, // Batty Barrel Bandit! (hard)
    131, // Busy Barrel Barrage! (hard)
    136, // Beaver Bother! (normal)
    137, // Beaver Bother! (hard)
    138, // Searchlight Seek! (easy)
    139, // Searchlight Seek! (normal)
    140, // Searchlight Seek! (hard)
    141, // Krazy Kong Klamour! (normal)
    142, // Krazy Kong Klamour! (hard)
    143, // Krazy Kong Klamour! (insane)
    144, // Peril Path Panic! (very easy) // Note: Broken with switch kong
    145, // Peril Path Panic! (easy)
    146, // Peril Path Panic! (normal)
    147, // Peril Path Panic! (hard)
    148, // Big Bug Bash! (easy)
    149, // Big Bug Bash! (normal)
    150, // Big Bug Bash! (hard)
    154, // Frantic Factory: Mad Jack
    165, // K. Rool Barrel: Diddy's Kremling Game
    185, // Enguarde Arena // Note: Handled by character check
    186, // Creepy Castle: Car Race
    187, // Crystal Caves: Barrel Blast
    188, // Creepy Castle: Barrel Blast
    189, // Fungi Forest: Barrel Blast
    190, // Kong Battle: Arena 2 // TODO: Would be really cool to get multiplayer working, currently just voids you out when activated
    191, // Rambi Arena // Note: Handled by character check
    192, // Kong Battle: Arena 3 // TODO: Would be really cool to get multiplayer working, currently just voids you out when activated
    196, // Crystal Caves: Army Dillo
    197, // Angry Aztec: Dogadon
    198, // Training Grounds (End Sequence) // Note: Handled by cutscene check
    199, // Creepy Castle: King Kut Out // Note: Doesn't break the kong order but since this fight is explicitly about tagging we might as well disable
    201, // K. Rool Barrel: Diddy's Rocketbarrel Game
    202, // K. Rool Barrel: Lanky's Shooting Game
    203, // K. Rool Fight: DK Phase // Note: Enabling here breaks the fight and may cause softlocks
    204, // K. Rool Fight: Diddy Phase // Note: Enabling here breaks the fight and may cause softlocks
    205, // K. Rool Fight: Lanky Phase // Note: Enabling here breaks the fight and may cause softlocks
    206, // K. Rool Fight: Tiny Phase // Note: Enabling here breaks the fight and may cause softlocks
    207, // K. Rool Fight: Chunky Phase // Note: Enabling here breaks the fight and may cause softlocks
    208, // Bloopers Ending // Note: Handled by cutscene check
    209, // K. Rool Barrel: Chunky's Hidden Kremling Game
    210, // K. Rool Barrel: Tiny's Pony Tail Twirl Game
    211, // K. Rool Barrel: Chunky's Shooting Game
    212, // K. Rool Barrel: DK's Rambi Game
    213, // K. Lumsy Ending // Note: Handled by cutscene check
    214, // K. Rool's Shoe
    215, // K. Rool's Arena // Note: Handled by cutscene check?
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

void tagAnywhere(int prev_crystals) {
	if (Rando.tag_anywhere) {
		if (Player) {
            if (CurrentMap != 0x2A) {
                char hud_items[] = {0,1,5,8,10,12,13,14};
                tag_countdown = 0;
                if (HUD) {
                    for (int i = 0; i < sizeof(hud_items); i++) {
                        if (HUD->item[(int)hud_items[i]].hud_state) {
                            return;
                        }
                    }
                }
            } else {
                if (tag_countdown > 0) {
                    tag_countdown -= 1;
                }
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
            }
            if (Player->strong_kong_ostand_bitfield & 0x100) {
                // Seasick
                return;
            }
            if (Player->collision_queue_pointer) {
                return;
            }
            int control_state = Player->control_state;
            for (int i = 0; i < sizeof(bad_movement_states); i++) {
                if (bad_movement_states[i] == control_state) {
                    return;
                }
            }
            if ((prev_crystals - 1) == CollectableBase.Crystals) {
                return;
            }
            if (CutsceneActive) {
                return;
            }
            if (CurrentMap == 0x2A) {
                if (MapState & 0x10) {
                    return;
                }
                if (hasTurnedInEnoughCBs()) {
                    if (Player->zPos < 560.0f) {
                        // Too close to boss door
                        return;
                    }
                }
            }
            if (TBVoidByte & 3) {
                return;
            }
            if (tag_countdown != 0) {
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
					for (int i = 0; i < sizeof(banned_maps); i++) {
						if (banned_maps[i] == CurrentMap) {
							return;
						}
					}
                    int next_character = Character + change;
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
								return;
							} else {
								next_character = next_character + change;
                                if (next_character < 0) {
                                    next_character = TAG_ANYWHERE_KONG_LIMIT - 1;
                                } else if (next_character >= TAG_ANYWHERE_KONG_LIMIT) {
                                    next_character = 0;
                                }
							}
						}
                        i++;
                    }
					if ((!reached_limit) && (next_character != Character)) {
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
                        if (CurrentMap == 0x2A) {
                            if (!hasTurnedInEnoughCBs()) {
                                tag_countdown = 3;
                                HUD->item[0].hud_state_timer = 0x100;
                                HUD->item[0].hud_state = 0;
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