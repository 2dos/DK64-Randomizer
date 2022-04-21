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