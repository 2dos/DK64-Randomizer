#include "../../include/common.h"

#define TAG_ANYWHERE_KONG_LIMIT 5

static const unsigned char banned_maps[] = {
	1, // Funky's Store
    2, // DK Arcade
    3, // K. Rool Barrel: Lanky's Maze
    5, // Cranky's Lab
    6, // Jungle Japes: Minecart
    9, // Jetpac
    10, // Kremling Kosh! (very easy)
    14, // Angry Aztec: Beetle Race // Note: Softlock at the end if enabled?
    15, // Snide's H.Q.
    18, // Teetering Turtle Trouble! (very easy)
    25, // Candy's Music Shop
    27, // Frantic Factory: Car Race
    31, // Gloomy Galleon: K. Rool's Ship // TODO: Test
    32, // Batty Barrel Bandit! (easy)
    35, // K. Rool Barrel: DK's Target Game
    37, // Jungle Japes: Barrel Blast // Note: The barrels don't work as other kongs so not much point enabling it on this map
    41, // Angry Aztec: Barrel Blast
    42, // Troff 'n' Scoff
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
    165, // K. Rool Barrel: Diddy's Kremling Game
    185, // Enguarde Arena // Note: Handled by character check
    186, // Creepy Castle: Car Race
    187, // Crystal Caves: Barrel Blast
    188, // Creepy Castle: Barrel Blast
    189, // Fungi Forest: Barrel Blast
    190, // Kong Battle: Arena 2 // TODO: Would be really cool to get multiplayer working, currently just voids you out when activated
    191, // Rambi Arena // Note: Handled by character check
    192, // Kong Battle: Arena 3 // TODO: Would be really cool to get multiplayer working, currently just voids you out when activated
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
static const short kong_flags[] = {0x181,0x6,0x46,0x42,0x75};

void tagAnywhere(int prev_crystals) {
	if (Rando.tag_anywhere) {
		if (Player) {
            char hud_items[] = {0,1,5,8,10,12,13,14};
            if (HUD) {
                for (int i = 0; i < sizeof(hud_items); i++) {
                    if (HUD->item[(int)hud_items[i]].hud_state) {
                        return;
                    }
                }
            }
            if ((prev_crystals - 1) == CollectableBase.Crystals) {
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
                    int next_character = (Character + TAG_ANYWHERE_KONG_LIMIT + change) % TAG_ANYWHERE_KONG_LIMIT;
					int i = 0;
					int reached_limit = 0;
					do {
                        int pass = 0;
                        if (checkFlag(kong_flags[next_character],0)) {
                            pass = 1;
                            if (Rando.perma_lose_kongs) {
                                if (checkFlag(KONG_LOCKED_START + next_character,0)) {
                                    if (!curseRemoved()) {
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
								next_character = (next_character + TAG_ANYWHERE_KONG_LIMIT + change) % TAG_ANYWHERE_KONG_LIMIT;
							}
						}
					} while (i++ < TAG_ANYWHERE_KONG_LIMIT);
					if ((!reached_limit) && (next_character != Character)) {
						tagKong(next_character + 2);
						clearTagSlide(Player);
						Player->new_kong = next_character + 2;
						int _wb = MovesBase[next_character].weapon_bitfield;
						if (((_wb & 1) == 0) || (Player->was_gun_out == 0)) {
							Player->hand_state = next_character != 1;
							Player->was_gun_out = 0;
						} else {
							Player->hand_state = 2 + (next_character == 1);
							Player->was_gun_out = 1;
						}
					}
				}
			}
		}
	}
}