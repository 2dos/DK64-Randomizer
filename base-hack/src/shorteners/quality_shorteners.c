#include "../../include/common.h"

static const short ftt_flags[] = {
	355, // Bananaporter
    358, // Crown Pad
    360, // Mini Monkey
    361, // Hunky Chunky
    362, // Orangstand Sprint
    363, // Strong Kong
    364, // Rainbow Coin
    365, // Rambi
    366, // Enguarde
    367, // Diddy
    368, // Lanky
    369, // Tiny
    370, // Chunky
    372, // Snide's
    376, // Wrinkly
    775, // Funky
    776, // Snide's
    777, // Cranky
    778, // Candy
    779, // Japes
    780, // Factory
    781, // Galleon
    782, // Fungi
    783, // Caves
    784, // Castle
    786, // Helm
    787, // Aztec
    282, // Caves CS
    194, // Galleon CS
    256, // Daytime
    257, // Fungi CS
    303, // DK 5DI
    349, // Castle CS
    42, // Japes Diddy Help Me Cutscene
    27, // Japes CS
    95, // Aztec CS
    93, // Lanky Help Me
    94, // Tiny Help Me
    140, // Chunky Help Me / Factory CS
    195, // Water Raised
    196, // Water Lowered
    255, // Clock CS
    277, // Rotating Room
    299, // Giant Kosha
    378, // Training Grounds Intro
    0x5C, // Llama CS
};

static const short default_ftt_flags[] = {
    359, // T&S (1)
    392, // T&S (2)
    785, // T&S (3)
    373, // Buy Instruments
    374, // Buy Guns
    0x45, // Tiny Temple Ice Melted
    109, // Hatch opened in Factory
    0xA1, // Peanut Gate Opened in Galleon
    0, // First Switch in Japes
    382, // B Locker
};

void qualityOfLife_shorteners(void) {
	if (Rando.quality_of_life) {
		// No FTTs
		for (int i = 0; i < sizeof(ftt_flags) / 2; i++) {
			setPermFlag(ftt_flags[i]);
		}
		// No Dance
		if (
			(CurrentMap == 14) ||
			(CurrentMap == 27) ||
			(CurrentMap == 39) ||
			(CurrentMap == 82) ||
			(CurrentMap == 185)
		) {
			SkipDance = 0;
		} else {
			SkipDance = 1;
		}
		// Shorter Boss Cutscenes
		TempFlagBlock[0xC] |= 0x80;
		TempFlagBlock[0xD] |= 0x3F;
        if (CurrentMap == 0x57) {
            if (ObjectModel2Timer <= 5) {
                actorData* lzcontroller = (actorData*)findActorWithType(0xC);
                char* lzpaad = (char*)lzcontroller->paad;
                *(char*)(lzpaad) = 0;
            }
        }
	}
    if (ObjectModel2Timer <= 5) {
        for (int i = 0; i < sizeof(default_ftt_flags) / 2; i++) {
            setPermFlag(default_ftt_flags[i]);
        }
    }
}