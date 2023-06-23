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
    FLAG_PEANUTGATE, // Peanut Gate Opened in Galleon
    FLAG_FIRSTJAPESGATE, // First Switch in Japes
    FLAG_FTT_BLOCKER, // B Locker
};

static const short openlevels_flags[] = {
    FLAG_PROGRESSION_SHELLHIVEGATE, // Beehive Gate
    FLAG_PROGRESSION_AZTECTUNNEL, // Aztec Tunnel Door
    FLAG_PROGRESSION_FACTORY_NEUTRALSWITCH, // Factory neutral gate open
    FLAG_COCONUTGATE, // Galleon Coconut Gate Opened
    FLAG_PROGRESSION_FUNGIGREENTUNNEL_FEATHER, // Fungi Green Path Open (Feather)
    FLAG_PROGRESSION_FUNGIGREENTUNNEL_PINEAPPLE, // Fungi Green Path Open (Pineapple)
    FLAG_PROGRESSION_FUNGIGOLDTUNNEL, // Fungi Gold Path Open
};

static const short highreq_flags[] = {
    FLAG_5DT_SPAWNED, // 5DT Switches Spawned
    FLAG_MODIFIER_PRODROOM, // Prod Room On
    FLAG_MODIFIER_GALLEONSHIP, // Galleon Ship Spawned
    FLAG_PROGRESSION_5DIPADS, // Caves 5DI Pads Spawned
};

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
	if ((Rando.quality_of_life.reduce_lag) && (Rando.seasonal_changes != SEASON_CHRISTMAS)) {
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
        if (Rando.open_level_sections) {
            for (int i = 0; i < sizeof(openlevels_flags)/2; i++) {
                setPermFlag(openlevels_flags[i]);
            }
        }
        if (Rando.remove_high_requirements) {
            for (int i = 0; i < sizeof(highreq_flags)/2; i++) {
                setPermFlag(highreq_flags[i]);
            }
        }
    }
}

void fastWarp(void* actor, int player_index) {
    unkMultiplayerWarpFunction(actor,player_index);
    renderScreenTransition(3);
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