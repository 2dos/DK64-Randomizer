#include "../../include/common.h"

void writeJetpacMedalReq(void) {
	if (Rando.jetpac_medal_requirement) {
		if (Rando.jetpac_medal_requirement < 0) {
			Rando.jetpac_medal_requirement = 0;
		} else if (Rando.jetpac_medal_requirement > 40) {
			Rando.jetpac_medal_requirement = 40;
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
		switch(curr) {
			case 0xE:
				amt = Rando.coinreq_aztecbeetle;
				break;
			case 0x6:
				amt = Rando.coinreq_japescart;
				break;
			case 0x37:
				amt = Rando.coinreq_fungicart;
				break;
			case 0x52:
				amt = Rando.coinreq_cavesbeetle;
				break;
			case 0x1B:
				amt = Rando.coinreq_factorycar;
				break;
			case 0xB9:
				amt = Rando.coinreq_castlecar;
				break;
			case 0x27:
				amt = Rando.coinreq_sealrace;
				break;
			case 0x6A:
				amt = Rando.coinreq_castlecart;
			break;
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

static const unsigned char race_maps[] = {0xE,0x52,0x1B,0xB9,0x27};

void writeCoinRequirements(int source) {
	if (source == 1) {
		// Load Map
		int in_race = 0;
		for (int i = 0; i < sizeof(race_maps); i++) {
			if (CurrentMap == race_maps[i]) {
				in_race = 1;
			}
		}
		if (in_race) {
			*(short*)(0x800247C2) = Rando.coinreq_cavesbeetle;
			*(short*)(0x800247DA) = Rando.coinreq_aztecbeetle;
			
			*(short*)(0x800285A2) = Rando.coinreq_factorycar; // Text
			*(short*)(0x8002888E) = Rando.coinreq_factorycar; // Req
			*(short*)(0x80028A0A) = Rando.coinreq_factorycar; // Req 2
			
			*(short*)(0x8002A232) = Rando.coinreq_sealrace; // Text
			*(short*)(0x8002A08E) = Rando.coinreq_sealrace; // Req

			*(short*)(0x8002BAB6) = Rando.coinreq_castlecar; // Text
			*(short*)(0x8002B6D6) = Rando.coinreq_castlecar; // Req
		}
	} else if (source == 0) {
		// Boot
		*(short*)(0x806C4912) = Rando.coinreq_japescart;
		*(short*)(0x806C4956) = Rando.coinreq_fungicart;
		*(short*)(0x806C499A) = Rando.coinreq_castlecart;
	}
}