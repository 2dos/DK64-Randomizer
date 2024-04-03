#include "../../include/common.h"

static const short ftt_flags[] = {
	FLAG_FTT_BANANAPORT, // Bananaporter
    FLAG_FTT_CROWNPAD, // Crown Pad
    FLAG_FTT_MINIMONKEY, // Mini Monkey
    FLAG_FTT_HUNKYCHUNKY, // Hunky Chunky
    FLAG_FTT_ORANGSPRINT, // Orangstand Sprint
    FLAG_FTT_STRONGKONG, // Strong Kong
    FLAG_FTT_RAINBOWCOIN, // Rainbow Coin
    FLAG_FTT_RAMBI, // Rambi
    FLAG_FTT_ENGUARDE, // Enguarde
    FLAG_FTT_DIDDY, // Diddy
    FLAG_FTT_LANKY, // Lanky
    FLAG_FTT_TINY, // Tiny
    FLAG_FTT_CHUNKY, // Chunky
    FLAG_FTT_SNIDE, // Snide's
    FLAG_FTT_WRINKLY, // Wrinkly
    FLAG_FTT_FUNKY, // Funky
    FLAG_FTT_SNIDE0, // Snide's
    FLAG_FTT_CRANKY, // Cranky
    FLAG_FTT_CANDY, // Candy
    FLAG_FTT_JAPES,
    FLAG_FTT_AZTEC,
    FLAG_FTT_FACTORY,
    FLAG_FTT_GALLEON,
    FLAG_FTT_FUNGI,
    FLAG_FTT_CAVES,
    FLAG_FTT_CASTLE,
    FLAG_FTT_HELM,
    FLAG_INTRO_CAVES, // Caves CS
    FLAG_INTRO_GALLEON, // Galleon CS
    FLAG_FTT_TIMESWITCH, // Daytime
    FLAG_INTRO_FUNGI, // Fungi CS
    FLAG_FTT_DK5DI, // DK 5DI
    FLAG_INTRO_CASTLE, // Castle CS
    FLAG_CUTSCENE_DIDDYHELPME, // Japes Diddy Help Me Cutscene
    FLAG_INTRO_JAPES, // Japes CS
    FLAG_INTRO_AZTEC, // Aztec CS
    FLAG_CUTSCENE_LANKYHELPME, // Lanky Help Me
    FLAG_CUTSCENE_TINYHELPME, // Tiny Help Me
    FLAG_INTRO_FACTORY, // Chunky Help Me / Factory CS
    FLAG_CUTSCENE_WATERRAISED, // Water Raised
    FLAG_CUTSCENE_WATERLOWERED, // Water Lowered
    FLAG_CUTSCENE_CLOCK, // Clock CS
    FLAG_CUTSCENE_ROTATING, // Rotating Room
    FLAG_CUTSCENE_KOSHA, // Giant Kosha
    FLAG_WATERFALL, // Training Grounds Intro
    FLAG_CUTSCENE_LLAMA, // Llama CS
};

static const short default_ftt_flags[] = {
    FLAG_TNS_0, // T&S (1)
    FLAG_TNS_1, // T&S (2)
    FLAG_TNS_2, // T&S (3)
    FLAG_BUY_INSTRUMENT, // Buy Instruments
    FLAG_BUY_GUNS, // Buy Guns
    FLAG_ICEMELT, // Tiny Temple Ice Melted
    FLAG_HATCH, // Hatch opened in Factory
    FLAG_FIRSTJAPESGATE, // First Switch in Japes
    FLAG_FTT_BLOCKER, // B Locker
};

typedef struct flag_checker {
    /* 0x000 */ int flag;
    /* 0x004 */ ENUM_RemovedBarriers index;
} flag_checker;

static const flag_checker barrier_checks[] = {
    {.flag=FLAG_PROGRESSION_SHELLHIVEGATE, .index=REMOVEDBARRIERS_ENUM_SHELLHIVEGATE}, // Beehive Gate
    {.flag=FLAG_PROGRESSION_AZTECTUNNEL, .index=REMOVEDBARRIERS_ENUM_AZTECTUNNELDOOR}, // Aztec Tunnel Door
    {.flag=FLAG_PROGRESSION_FACTORY_NEUTRALSWITCH, .index=REMOVEDBARRIERS_ENUM_FACTORYTESTINGGATE}, // Factory neutral gate open
    {.flag=FLAG_COCONUTGATE, .index=REMOVEDBARRIERS_ENUM_LIGHTHOUSEGATE}, // Galleon Coconut Gate Opened
    {.flag=FLAG_PROGRESSION_FUNGIGREENTUNNEL_FEATHER, .index=REMOVEDBARRIERS_ENUM_FUNGIGREENTUNNEL}, // Fungi Green Path Open (Feather)
    {.flag=FLAG_PROGRESSION_FUNGIGREENTUNNEL_PINEAPPLE, .index=REMOVEDBARRIERS_ENUM_FUNGIGREENTUNNEL}, // Fungi Green Path Open (Pineapple)
    {.flag=FLAG_PROGRESSION_FUNGIGOLDTUNNEL, .index=REMOVEDBARRIERS_ENUM_FUNGIYELLOWTUNNEL}, // Fungi Gold Path Open
    {.flag=FLAG_5DT_SPAWNED, .index=REMOVEDBARRIERS_ENUM_FIVEDTSWITCHES}, // 5DT Switches Spawned
    {.flag=FLAG_MODIFIER_PRODROOM, .index=REMOVEDBARRIERS_ENUM_PRODUCTIONROOMON}, // Prod Room On
    {.flag=FLAG_MODIFIER_GALLEONSHIP, .index=REMOVEDBARRIERS_ENUM_SEASICKSHIPSPAWNED}, // Galleon Ship Spawned
    {.flag=FLAG_PROGRESSION_5DIPADS, .index=REMOVEDBARRIERS_ENUM_IGLOOPADSSPAWNED}, // Caves 5DI Pads Spawned
    {.flag=FLAG_PEANUTGATE, .index=REMOVEDBARRIERS_ENUM_SHIPWRECKGATE}, // Peanut Gate Opened in Galleon
};

int checkBarrierSetting(ENUM_RemovedBarriers index) {
    int addr = (int)&Rando.removed_barriers;
    int offset = index >> 3;
    addr += offset;
    int mask = 0x80 >> (index & 7);
    int value = *(unsigned char*)(addr);
    value &= mask;
    return value != 0;
}

void qualityOfLife_shorteners(void) {
	if (Rando.quality_of_life.remove_cutscenes) {
		// No FTTs
		for (int i = 0; i < sizeof(ftt_flags) / 2; i++) {
			setPermFlag(ftt_flags[i]);
		}
        // Shorter Boss Cutscenes
		TempFlagBlock[0xC] |= 0x80;
		TempFlagBlock[0xD] |= 0x3F;
    }
	if (Rando.quality_of_life.reduce_lag) {
        if (CurrentMap == MAP_CASTLE) {
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
        for (int i = 0; i < sizeof(barrier_checks)/sizeof(flag_checker); i++) {
            if (checkBarrierSetting(barrier_checks[i].index)) {
                setPermFlag(barrier_checks[i].flag);
            }
        }
    }
}

void fastWarp(void* actor, int player_index) {
    unkMultiplayerWarpFunction(actor,player_index);
    if ((!Rando.true_widescreen) || (!WS_REMOVE_TRANSITIONS)) {
        renderScreenTransition(3);
    }
}

void fastWarp_playMusic(void* actor) {
    clearTagSlide(actor);
    playLevelMusic();
}

void fastWarpShockwaveFix(void) {
    if (Rando.fast_warp) {
        if (Player) {
            if (Player->control_state == 0x54) { // Multiplayer Warp
                if (Player->shockwave_timer != -1) { // Charging Shockwave
                    if (Player->shockwave_timer < 5) {
                        Player->shockwave_timer += 1;
                        if (Player->shockwave_timer < 2) {
                            Player->shockwave_timer += 1; // Prevent ever being a frame where you can shockwave
                        }
                    }
                }
            }
        }
    }
}