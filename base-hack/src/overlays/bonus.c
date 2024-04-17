/**
 * @file bonus.c
 * @author Ballaam
 * @brief Changes within the Bonus Overlay
 * @version 0.1
 * @date 2023-12-16
 * 
 * @copyright Copyright (c) 2023
 * 
 */

#include "../../include/common.h"

static const unsigned char veasy_bonuses[] = {
	MAP_BASH_VEASY,
	MAP_KOSH_VEASY,
	MAP_PPPANIC_VEASY,
	MAP_SNOOP_VEASY,
	MAP_TURTLES_VEASY,
	MAP_SALVAGE_EASY,
	MAP_BATTYBARREL_VEASY,
	MAP_SEARCHLIGHT_VEASY,
};

static const unsigned char easy_bonuses[] = {
	MAP_BASH_EASY,
	MAP_KOSH_EASY,
	MAP_MAUL_EASY,
	MAP_SNOOP_EASY,
	MAP_SNATCH_EASY,
	MAP_SORTIE_EASY,
	MAP_BARRAGE_EASY,
	MAP_BBOTHER_EASY,
	MAP_KLAMOUR_EASY,
	MAP_MMAYHEM_EASY,
	MAP_PPPANIC_EASY,
	MAP_SALVAGE_EASY,
	MAP_TURTLES_EASY,
	MAP_BATTYBARREL_EASY,
	MAP_SEARCHLIGHT_EASY,
};
static const unsigned char med_bonuses[] = {
	MAP_BASH_NORMAL,
	MAP_KOSH_NORMAL,
	MAP_MAUL_NORMAL,
	MAP_SNOOP_NORMAL,
	MAP_SNOOP_NORMAL,
	MAP_SNATCH_NORMAL,
	MAP_SORTIE_NORMAL,
	MAP_BARRAGE_NORMAL,
	MAP_BBOTHER_NORMAL,
	MAP_KLAMOUR_NORMAL,
	MAP_MMAYHEM_NORMAL,
	MAP_PPPANIC_NORMAL,
	MAP_SALVAGE_NORMAL,
	MAP_TURTLES_NORMAL,
	MAP_BATTYBARREL_NORMAL,
	MAP_SEARCHLIGHT_NORMAL,
};

static const unsigned char hard_bonuses[] = {
	MAP_MAUL_HARD,
	MAP_SNATCH_HARD,
	MAP_KOSH_HARD,
	MAP_TURTLES_HARD,
	MAP_BATTYBARREL_HARD,
	MAP_SNOOP_HARD,
	MAP_MMAYHEM_HARD,
	MAP_BARRAGE_HARD,
	MAP_SALVAGE_HARD,
	MAP_SORTIE_HARD,
	MAP_BBOTHER_HARD,
	MAP_SEARCHLIGHT_HARD,
	MAP_KLAMOUR_HARD,
	MAP_PPPANIC_HARD,
	MAP_BASH_HARD,
};

static const unsigned char insane_bonuses[] = {
	MAP_MAUL_INSANE,
	MAP_SNATCH_INSANE,
	MAP_KLAMOUR_INSANE,
};

typedef struct bonus_extra_text {
	/* 0x000 */ char* text;
	/* 0x004 */ const unsigned char* map_array;
	/* 0x008 */ unsigned char count;
	/* 0x009 */ unsigned char rgb[3];
} bonus_extra_text;

static const bonus_extra_text bonus_second_overlays[] = {
	{.text = "(VERY EASY)", .map_array=&veasy_bonuses[0], .count=sizeof(veasy_bonuses), .rgb={0, 255, 0}},
	{.text = "(EASY)", .map_array=&easy_bonuses[0], .count=sizeof(easy_bonuses), .rgb={39, 135, 22}},
	{.text = "(NORMAL)", .map_array=&med_bonuses[0], .count=sizeof(med_bonuses), .rgb={135, 112, 22}},
	{.text = "(HARD)", .map_array=&hard_bonuses[0], .count=sizeof(hard_bonuses), .rgb={148, 6, 6}},
	{.text = "(INSANE)", .map_array=&insane_bonuses[0], .count=sizeof(insane_bonuses), .rgb={255, 0, 255}},
};

void spawnOverlayText(int style, int x, int y, char* str, int unk0, int appearance_length, int in_animation_speed, int out_animation_speed) {
	if (CurrentMap == MAP_SNATCH_HARD) {
		str = "STASH SNOOP";
	}
	spawnTextOverlayWrapper(style, x, y, str, unk0, appearance_length, in_animation_speed, out_animation_speed);
	for (int i = 0; i < 5; i++) {
		int cap = bonus_second_overlays[i].count;
		for (int j = 0; j < cap; j++) {
			if (bonus_second_overlays[i].map_array[j] == CurrentMap) {
				spawnTextOverlayWrapper(0, x, y + 20, bonus_second_overlays[i].text, unk0, appearance_length, in_animation_speed, out_animation_speed);
				for (int k = 0; k < 3; k++) {
					LastSpawnedActor->rgb_mask[k] = bonus_second_overlays[i].rgb[k];
				}
				return;
			}
		}
	}
}

void overlay_mod_bonus(void) {
	if (!isGamemode(GAMEMODE_DKBONUS, 0)) {
		*(int*)(0x8002D628) = 0x016FC022; // sub $t8, $t3, $t7 - Rambi Arena
		*(int*)(0x8002D658) = 0x03224822; // sub $t1, $t9, $v0 - Enguarde Arena
	}

	// Krazy Kong Klamour - Adjsut flicker speeds
	PatchBonusCode();

	if (Rando.music_rando_on) {
		// Lower Crowd SFX Volume
		*(short*)(0x80025192) = CROWD_VOLUME;
		*(short*)(0x80025166) = CROWD_VOLUME;
		*(short*)(0x80025112) = CROWD_VOLUME;
	}
}