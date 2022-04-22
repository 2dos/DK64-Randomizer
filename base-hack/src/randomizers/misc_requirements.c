#include "../../include/common.h"

void writeJetpacMedalReq(void) {
	if (Rando.jetpac_medal_requirement) {
		if (Rando.jetpac_medal_requirement < 4) {
			Rando.jetpac_medal_requirement = 4;
		} else if (Rando.jetpac_medal_requirement > 15) {
			Rando.jetpac_medal_requirement = 15;
		}
		*(unsigned char*)(0x80026513) = Rando.jetpac_medal_requirement; // Actual requirement
		*(unsigned char*)(0x8002644B) = Rando.jetpac_medal_requirement; // Text variable
		*(unsigned char*)(0x80027583) = Rando.jetpac_medal_requirement; // Text Variable
	}
}

int* writeHUDAmount(char* str_location, char* format, int value, int item_index, int* dl) {
	int found = 0;
	int amt = -1;
	if (item_index == 0xB) {
		int curr = CurrentMap;
		if ((curr == 0xE) || (curr == 0x6) || (curr == 0x37) || (curr == 0x52)) {
			amt = 50;
		} else if ((curr == 0x1B) || (curr == 0xB9) || (curr == 0x27)) {
			amt = 10;
		} else if (curr == 0x6A) {
			amt = 25;
		}
		if (amt > -1) {
			found = 1;
		}
	}
	if (found) {
		dk_strFormat(str_location,"%dl%d",value,amt);
		*(unsigned int*)(dl++) = 0xDA380003;
		*(unsigned int*)(dl++) = (int)&style6Mtx[0];
	} else {
		dk_strFormat(str_location,"%d",value);
	}
	return dl;
}