#include "../../include/common.h"

static const int krool_write_locations[] = {
	0x8002DBCE, // DK > Diddy
	0x8002E716, // Diddy > Lanky
	0x8002F04E, // Lanky > Tiny
	0x8002FAF2, // Tiny > Chunky
};

static char inside_sound_zone = 0;
static int sound_zone_entry = 0;
static const short sound_effects[] = {560,646,206,179,198};
static char sounds_played[] = {0,0,0,0,0};

#define ISLES_OVERWORLD 0x22

void determine_krool_order(void) {
	int containing = 0;
	int destination = 0;
	int current_phase = 0;
	if (ObjectModel2Timer < 5) {
		if (CurrentMap >= 0xCB) {
			if (CurrentMap <= 0xCF) {
				current_phase = CurrentMap - 0xCB;
				if (Character != current_phase) {
					tagKong(current_phase + 2);
				}
				for (int i = 0; i < 4; i++) {
					containing = Rando.k_rool_order[i];
					destination = Rando.k_rool_order[i + 1];
					if ((containing > -1) && (destination > -1)) {
						*(short*)(*(int*)((int)&krool_write_locations[containing])) = 0xCB + destination;
					}
				}
			}
		}
	}
}

#define SOUND_FREQUENCY 100
#define SOUND_COOLDOWN 1200
void krool_order_indicator(void) {
	float fight_x = 3072.0f;
	float fight_y = 477.0f;
	float fight_z = 675.0f;
	if (CurrentMap == ISLES_OVERWORLD) {
		if (Player) {
			float dx = Player->xPos - fight_x;
			float dy = Player->yPos - fight_y;
			float dz = Player->zPos - fight_z;
			float dist2 = (dx * dx) + (dy * dy) + (dz * dz);
			if (dist2 < 360000) { // In 600 Unit Radius
				if (!inside_sound_zone) {
					sound_zone_entry = FrameReal;
				}
				inside_sound_zone = 1;
				int played_all_sounds = 1;
				for (int i = 0; i < 5; i++) {
					if (Rando.k_rool_order[i] < 0) {
						sounds_played[i] = 1;
					}
					played_all_sounds &= sounds_played[i];
					if ((FrameReal > (sound_zone_entry + (SOUND_FREQUENCY * i))) && (!sounds_played[i])) {
						playSFX(sound_effects[(int)Rando.k_rool_order[i]]);
						sounds_played[i] = 1;
					}
				}
				if (played_all_sounds) {
					sound_zone_entry = FrameReal + SOUND_COOLDOWN;
					for (int i = 0; i < 5; i++) {
						sounds_played[i] = 0;
					}
				}
			} else {
				inside_sound_zone = 0;
				for (int i = 0; i < 5; i++) {
					sounds_played[i] = 0;
				}
			}
		}
	}
}

void disable_krool_health_refills(void) {
	if (ObjectModel2Timer < 5) {
		if (Rando.no_health_refill) {
			if (CurrentMap >= 0xCB) {
				if (CurrentMap <= 0xCF) {
					*(int*)(0x800289B0) = 0; // Between Phases
				}
			}
		}
	}
}