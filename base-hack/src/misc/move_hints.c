#include "../../include/common.h"

int isTBarrelFlag(int flag) {
	if (flag == FLAG_TBARREL_BARREL) {
		return 1;
	} else if (flag == FLAG_TBARREL_DIVE) {
		return 1;
	} else if (flag == FLAG_TBARREL_ORANGE) {
		return 1;
	}
	return flag == FLAG_TBARREL_VINE;
}

int isFairyFlag(int flag) {
	if (flag == FLAG_ABILITY_CAMERA) {
		return 1;
	} else if (flag == FLAG_ABILITY_SHOCKWAVE) {
		return 1;
	}
	return flag == -2;
}

int getHintTextIndex(int shop_owner, shop_paad* shop_data) {
	int purchase_type = shop_data->purchase_type;
	int purchase_value = shop_data->purchase_value;
	int base = 0;
	int kong = shop_data->kong;
	if (shop_data->price > MovesBase[(int)Character].coins) {
		if (purchase_type < 5) {
			base = 48 + purchase_type;
		} else {
			int subtype = getMoveProgressiveFlagType(shop_data->flag);
			if (isTBarrelFlag(shop_data->flag)) {
				base = 53;
			} else if (isFairyFlag(shop_data->flag)) {
				base = 54;
			} else if (purchase_type == PURCHASE_GB) {
				base = 56;
			} else if ((shop_data->flag >= FLAG_BP_JAPES_DK_HAS) && (shop_data->flag < (FLAG_BP_JAPES_DK_HAS + 40))) {
				base = 57;
			} else if ((shop_data->flag >= FLAG_MEDAL_JAPES_DK) && (shop_data->flag < (FLAG_MEDAL_JAPES_DK + 40))) {
				base = 58;
			} else if (subtype == 0) {
				base = 49;
			} else if (subtype == 1) {
				base = 51;
			} else if (subtype == 2) {
				base = 52;
			} else {
				for (int i = 0; i < 5; i++) {
					if (shop_data->flag == kong_flags[i]) {
						base = 59;
					}
				}
				if (base == 0) {
					// Generic Item Hint
					base = 55;
				}
			}
		}
	} else {
		if (purchase_type == 0) { // Special Potion Moves
			base = (kong * 3) + (purchase_value - 1);
		} else if (purchase_type == 1) { // Slams
			base = 15;
		} else if ((purchase_type == 2) && (purchase_value == 1)) { // Base Guns
			base = 16 + kong;
		} else if ((purchase_type == 2) && (purchase_value != 1)) { // Homing/Sniper
			base = 21 + (purchase_value - 2);
		} else if (purchase_type == 3) { // Ammo Belt
			base = 23;
		} else if ((purchase_type == 4) && (purchase_value == 1)) { // Base Instruments
			base = 24 + kong;
		} else if ((purchase_type == 4) && (purchase_value != 1)) { // Instrument Upgrades
			base = 29;
		} else if (purchase_type == 5) {
			int move_flags[] = {FLAG_TBARREL_DIVE, FLAG_TBARREL_ORANGE, FLAG_TBARREL_BARREL, FLAG_TBARREL_VINE, FLAG_ABILITY_CAMERA, FLAG_ABILITY_SHOCKWAVE, -2};
			base = 0;
			int subtype = getMoveProgressiveFlagType(shop_data->flag);
			if (subtype == 0) {
				base = 15;
			} else if (subtype == 1) {
				base = 23;
			} else if (subtype == 2) {
				base = 29;
			} else {
				for (int i = 0; i < sizeof(move_flags)/4; i++) {
					if (shop_data->flag == move_flags[i]) {
						base = 30 + i;
					}
				}
				if (base == 0) {
					int flag = shop_data->flag;
					if ((flag >= FLAG_BP_JAPES_DK_HAS) && (flag < (FLAG_BP_JAPES_DK_HAS + 40))) {
						base = 41;
					} else if ((flag >= FLAG_MEDAL_JAPES_DK) && (flag < (FLAG_MEDAL_JAPES_DK + 40))) {
						base = 39;
					} else if (flag == FLAG_COLLECTABLE_NINTENDOCOIN) {
						base = 42;
					} else if (flag == FLAG_COLLECTABLE_RAREWARECOIN) {
						base = 43;
					} else if ((flag >= FLAG_CROWN_JAPES) && (flag < (FLAG_CROWN_JAPES + 10))) {
						base = 38;
					} else if (flag == FLAG_COLLECTABLE_BEAN) {
						base = 44;
					} else if ((flag >= FLAG_PEARL_0_COLLECTED) && (flag < (FLAG_PEARL_0_COLLECTED + 5))) {
						base = 45;
					} else if ((flag >= FLAG_FAIRY_1) && (flag < (FLAG_FAIRY_1 + 20))) {
						base = 47;
					} else {
						// Kongs
						for (int i = 0; i < 5; i++) {
							if (flag == kong_flags[i]) {
								base = 46;
							}
						}
						// Key
						for (int i = 0; i < 8; i++) {
							if (flag == getKeyFlag(i)) {
								base = 40;
							}
						}
					}
				}
			}
		} else if (purchase_type == 6) {
			base = 37;
		}
	}
	return (base * 3) + shop_owner;
}

int isGoodTextbox(int text_file, int text_index) {
	if (text_file == 7) { // Funky
		return ((text_index >= 3) && (text_index <= 8)) || ((text_index >= 11 && (text_index <= 14)));
	} else if (text_file == 8) { // Cranky
		return (text_index == 4) || (text_index == 5) || (text_index == 8) || (text_index == 9);
	} else if (text_file == 9)  { // Candy
		return (text_index == 0) || ((text_index >= 3) && (text_index <= 9)) || ((text_index >= 12) && (text_index <= 15));
	}
	return 1;
}

void getMoveHint(actorData* actor, int text_file, int text_index) {
	int shop = actor->actorType - 189; // 0 = Cranky, 1 = Funky, 2 = Candy
	if ((shop >= 0) && (shop <= 2)) {
		shop_paad* shop_data = (shop_paad*)actor->paad2;
		if (!isGoodTextbox(text_file,text_index)) {
			getTextPointer_0(actor,text_file,text_index);
		} else {
			int hint_text_index = getHintTextIndex(shop,shop_data);
			getTextPointer_0(actor,32,hint_text_index);
		}
	} else {
		getTextPointer_0(actor,text_file,text_index);
	}
}