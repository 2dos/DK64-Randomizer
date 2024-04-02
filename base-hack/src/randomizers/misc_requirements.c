#include "../../include/common.h"

Gfx* displayComplexJetpacOption(Gfx* dl, actorData* actor) {
	shop_paad* paad = actor->paad2;
	if (paad->state == 1) {
		gSPDisplayList(dl++, 0x01000118);
		gSPMatrix(dl++, 0x020000C0, G_MTX_NOPUSH | G_MTX_LOAD | G_MTX_PROJECTION);
		gDPPipeSync(dl++);
		gDPSetCombineMode(dl++, G_CC_MODULATEIA_PRIM, G_CC_MODULATEIA_PRIM);
		if (paad->unk_0E == 1) {
			actor->sub_state = 0;
			paad->unk_0E = 5;
		} else if (paad->unk_0E != 5) {
			return dl;
		}
		int shift = 0xFF - actor->sub_state;
		if (shift > 8) {
			shift = 8;
		}
		actor->sub_state += shift;
		gDPSetPrimColor(dl++, 0, 0, 0xFF, 0xFF, 0xFF, actor->sub_state);
		int jetpac_requirement = 15;
		if (Rando.jetpac_medal_requirement > 0) {
			jetpac_requirement = Rando.jetpac_medal_requirement;
		}
		int offer_jetpac = (paad->purchase_type >= 0) && (countFlagArray(FLAG_MEDAL_JAPES_DK, 40, 0) >= jetpac_requirement) && (CurrentMap == MAP_CRANKY);
		int start_y = 400;
		if (offer_jetpac) {
			start_y = 350;
		}
		dl = (Gfx*)displayText((int*)dl, 1, 500, start_y, "q YES", 1);
		dl = (Gfx*)displayText((int*)dl, 1, 500, start_y + 100, "b NO", 1);
		if (offer_jetpac) {
			dl = (Gfx*)displayText((int*)dl, 1, 500, start_y + 200, "n JETPAC", 1);
			if (NewlyPressedControllerInput.Buttons.c_up) {
				// Queue Jetpac
				paad->unk_0F = 1;
				paad->purchase_type = -1;
			}
		}
	}
	return dl;
}

void writeJetpacMedalReq(void) {
	*(short*)(0x800268D6) = getHi(&displayComplexJetpacOption);
	*(short*)(0x800268E2) = getLo(&displayComplexJetpacOption);
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
		switch(CurrentMap) {
			case MAP_AZTECBEETLE:
				amt = Rando.coinreq_aztecbeetle;
				break;
			case MAP_JAPESMINECART:
				amt = Rando.coinreq_japescart;
				break;
			case MAP_FUNGIMINECART:
				amt = Rando.coinreq_fungicart;
				break;
			case MAP_CAVESBEETLERACE:
				amt = Rando.coinreq_cavesbeetle;
				break;
			case MAP_FACTORYCARRACE:
				amt = Rando.coinreq_factorycar;
				break;
			case MAP_CASTLECARRACE:
				amt = Rando.coinreq_castlecar;
				break;
			case MAP_GALLEONSEALRACE:
				amt = Rando.coinreq_sealrace;
				break;
			case MAP_CASTLEMINECART:
				amt = Rando.coinreq_castlecart;
				break;
			default:
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

static const unsigned char race_maps[] = {
	MAP_AZTECBEETLE,
	MAP_CAVESBEETLERACE,
	MAP_FACTORYCARRACE,
	MAP_CASTLECARRACE,
	MAP_GALLEONSEALRACE
};

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