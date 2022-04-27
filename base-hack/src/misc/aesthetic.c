#include "../../include/common.h"

static short rgb_offsets[3] = {0,0,0};

void colorMenuSky(void) {
	int top_rgb[3] = {0,0,0};
	int magnitude = (ObjectModel2Timer / 10) % 300;
	if (magnitude > 150) {
		magnitude = 300 - magnitude;
	}
	for (int i = 0; i < 3; i++) {
		int previous_rgb = MenuSkyTopRGB[i];
		top_rgb[i] = (magnitude + rgb_offsets[i]) & 0xFF;
		int diff = previous_rgb - top_rgb[i];
		if (((diff < 20) && (diff > -20)) || (ObjectModel2Timer < 3)) {
			MenuSkyTopRGB[i] = top_rgb[i];
		}
		float mag_bottom = magnitude;
		mag_bottom *= 1.5f;
		if (mag_bottom > 255.0f) {
			mag_bottom = 255.0f;
		}
		int magi_bottom = mag_bottom;
		previous_rgb = MenuSkyRGB[i];
		int bottom_i = (magi_bottom + rgb_offsets[i]) & 0xFF;
		diff = previous_rgb - bottom_i;
		if (((diff < 20) && (diff > -20)) || (ObjectModel2Timer < 3)) {
			MenuSkyRGB[i] = bottom_i;
		}
		cycleRNG();
		int dec = RNG & 1;
		if (MenuSkyTopRGB[i] > 0xF0) {
			dec = 1;
		} else if (MenuSkyTopRGB[i] < 0x10) {
			dec = 0;
		}
		int change = (RNG >> 1) & 1;
		if (dec) {
			rgb_offsets[i] -= change;
			if (rgb_offsets[i] < -255) {
				rgb_offsets[i] += 256;
			}
		} else {
			rgb_offsets[i] += change;
			if (rgb_offsets[i] > 255) {
				rgb_offsets[i] -= 255;
			}
		}
	}
}