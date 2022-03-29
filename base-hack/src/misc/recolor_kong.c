#include "../../include/common.h"

void recolorKong(int red, int green, int blue, int enabled) {
	if (Player) {
		if (enabled) {
			Player->obj_props_bitfield |= 0x00800000;
			Player->rgb_components[0] = red;
			Player->rgb_components[1] = green;
			Player->rgb_components[2] = blue;
		} else {
			Player->obj_props_bitfield &= 0xFF7FFFFF;
		}
	}
}

#define KONG_DK 0
#define KONG_DIDDY 1
#define KONG_LANKY 2
#define KONG_TINY 3
#define KONG_CHUNKY 4
#define KONG_KRUSHA 5
#define KONG_RAMBI 6
#define KONG_ENGUARDE 7

void recolorKongControl(void) {
	if (Rando.kong_rgb_enabled) {
		if (Player) {
			int red = 0;
			int green = 0;
			int blue = 0;
			int enabled = 1;
			switch(Character) {
				case KONG_DK:
					red = Rando.dk_rgb_components[0];
					green = Rando.dk_rgb_components[1];
					blue = Rando.dk_rgb_components[2];
					break;
				case KONG_DIDDY:
					red = Rando.diddy_rgb_components[0];
					green = Rando.diddy_rgb_components[1];
					blue = Rando.diddy_rgb_components[2];
					break;
				case KONG_LANKY:
					red = Rando.lanky_rgb_components[0];
					green = Rando.lanky_rgb_components[1];
					blue = Rando.lanky_rgb_components[2];
					break;
				case KONG_TINY:
					red = Rando.tiny_rgb_components[0];
					green = Rando.tiny_rgb_components[1];
					blue = Rando.tiny_rgb_components[2];
					break;
				case KONG_CHUNKY:
					red = Rando.chunky_rgb_components[0];
					green = Rando.chunky_rgb_components[1];
					blue = Rando.chunky_rgb_components[2];
					break;
				case KONG_KRUSHA:
					enabled = 0;
					break;
				case KONG_RAMBI:
					red = Rando.rambi_rgb_components[0];
					green = Rando.rambi_rgb_components[1];
					blue = Rando.rambi_rgb_components[2];
					break;
				case KONG_ENGUARDE:
					red = Rando.enguarde_rgb_components[0];
					green = Rando.enguarde_rgb_components[1];
					blue = Rando.enguarde_rgb_components[2];
					break;
			}
			recolorKong(red,green,blue,enabled);
		}
	}
}