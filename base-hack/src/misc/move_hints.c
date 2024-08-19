/**
 * @file move_hints.c
 * @author Ballaam
 * @brief Handle in-shop move hints
 * @version 0.1
 * @date 2022-05-13
 * 
 * @copyright Copyright (c) 2022
 * 
 */
#include "../../include/common.h"

int isTBarrelFlag(int flag) {
	/**
	 * @brief Is a flag a training move flag
	 * 
	 * @param flag Flag being queried
	 * 
	 * @return is training flag (bool)
	 */
	return inShortList(flag, &tbarrel_flags[0], 4);
}

int isFairyFlag(int flag) {
	/**
	 * @brief Is a flag a fairy move flag
	 * 
	 * @param flag Flag being queried
	 * 
	 * @return is a fairy move flag (bool)
	 */
	if (flag == FLAG_ABILITY_CAMERA) {
		return 1;
	} else if (flag == FLAG_ABILITY_SHOCKWAVE) {
		return 1;
	}
	return flag == -2;
}

int getHintTextIndex(int shop_owner, shop_paad* shop_data) {
	/**
	 * @brief Get the text index in the text file for a certain hint
	 * 
	 * @param shop_owner Index of the shop owner (0 = Cranky, 1 = Funky, 2 = Candy)
	 * @param shop_data Shop data paad
	 * 
	 * @return text index
	 */
	int purchase_type = shop_data->purchase_type;
	int purchase_value = shop_data->purchase_value;
	int base = 0;
	int kong = shop_data->kong;
	if (shop_data->price > MovesBase[(int)Character].coins) {
		if (purchase_type < 5) {
			moverando_hinttext bases[] = {
				MRT_NOBUY_SPECIALMOVE,
				MRT_NOBUY_SLAM,
				MRT_NOBUY_GUN,
				MRT_NOBUY_AMMOBELT,
				MRT_NOBUY_INSTRUMENT,
			};
			if (purchase_type == PURCHASE_GUN) {
				base = MRT_NOBUY_GUNUPGRADE; // Homing or Sniper
				if (purchase_value == 1) { // Base Gun
					base = MRT_NOBUY_GUN;
				}
			} else {
				base = bases[purchase_type];
			}
		} else {
			int subtype = getMoveProgressiveFlagType(shop_data->flag);
			if (isTBarrelFlag(shop_data->flag)) {
				base = MRT_NOBUY_TRAINING;
			} else if (isFairyFlag(shop_data->flag)) {
				base = MRT_NOBUY_FAIRYMOVE;
			} else if (purchase_type == PURCHASE_GB) {
				base = MRT_NOBUY_BANANA;
			} else if (isFlagInRange(shop_data->flag, FLAG_BP_JAPES_DK_HAS, 40)) {
				base = MRT_NOBUY_BLUEPRINT;
			} else if (isMedalFlag(shop_data->flag)) {
				base = MRT_NOBUY_MEDAL;
			} else if (subtype == 0) {
				base = MRT_NOBUY_SLAM;
			} else if (subtype == 1) {
				base = MRT_NOBUY_AMMOBELT;
			} else if (subtype == 2) {
				base = MRT_NOBUY_INSTRUMENT;
			} else {
				for (int i = 0; i < 5; i++) {
					if (shop_data->flag == kong_flags[i]) {
						base = MRT_NOBUY_KONG;
					}
				}
				if (base == 0) {
					// Generic Item Hint
					base = MRT_NOBUY_ITEM;
				}
			}
		}
	} else {
		if (purchase_type == PURCHASE_MOVES) { // Special Potion Moves
			base = MRT_CANBUY_BBLAST + (kong * 3) + (purchase_value - 1);
		} else if (purchase_type == PURCHASE_SLAM) { // Slams
			base = MRT_CANBUY_SLAM;
		} else if ((purchase_type == PURCHASE_GUN) && (purchase_value == 1)) { // Base Guns
			base = MRT_CANBUY_COCONUT + kong;
		} else if ((purchase_type == PURCHASE_GUN) && (purchase_value != 1)) { // Homing/Sniper
			base = MRT_CANBUY_HOMING + (purchase_value - 2);
		} else if (purchase_type == PURCHASE_AMMOBELT) { // Ammo Belt
			base = MRT_CANBUY_AMMOBELT;
		} else if ((purchase_type == PURCHASE_INSTRUMENT) && (purchase_value == 1)) { // Base Instruments
			base = MRT_CANBUY_BONGOS + kong;
		} else if ((purchase_type == PURCHASE_INSTRUMENT) && (purchase_value != 1)) { // Instrument Upgrades
			base = MRT_CANBUY_INSTRUMENTUPGRADE;
		} else if (purchase_type == PURCHASE_FLAG) {
			int move_flags[] = {FLAG_TBARREL_DIVE, FLAG_TBARREL_ORANGE, FLAG_TBARREL_BARREL, FLAG_TBARREL_VINE, FLAG_ABILITY_CLIMBING, FLAG_ABILITY_CAMERA, FLAG_ABILITY_SHOCKWAVE, -2};
			base = 0;
			int subtype = getMoveProgressiveFlagType(shop_data->flag);
			if (subtype == 0) {
				base = MRT_CANBUY_SLAM;
			} else if (subtype == 1) {
				base = MRT_CANBUY_AMMOBELT;
			} else if (subtype == 2) {
				base = MRT_CANBUY_INSTRUMENTUPGRADE;
			} else {
				for (int i = 0; i < sizeof(move_flags)/4; i++) {
					if (shop_data->flag == move_flags[i]) {
						base = MRT_CANBUY_DIVE + i;
					}
				}
				if (base == 0) {
					int flag = shop_data->flag;
					if (isFlagInRange(flag, FLAG_BP_JAPES_DK_HAS, 40)) {
						base = MRT_CANBUY_BLUEPRINT;
					} else if (isFlagInRange(flag, FLAG_WRINKLYVIEWED, 35)) {
						base = MRT_CANBUY_HINT;
					} else if (isMedalFlag(flag)) {
						base = MRT_CANBUY_MEDAL;
					} else if (flag == FLAG_COLLECTABLE_NINTENDOCOIN) {
						base = MRT_CANBUY_NINTENDO;
					} else if (flag == FLAG_COLLECTABLE_RAREWARECOIN) {
						base = MRT_CANBUY_RAREWARE;
					} else if (isFlagInRange(flag, FLAG_CROWN_JAPES, 10)) {
						base = MRT_CANBUY_CROWN;
					} else if (flag == FLAG_COLLECTABLE_BEAN) {
						base = MRT_CANBUY_BEAN;
					} else if (isFlagInRange(flag, FLAG_PEARL_0_COLLECTED, 5)) {
						base = MRT_CANBUY_PEARL;
					} else if (isFlagInRange(flag, FLAG_FAIRY_1, 20)) {
						base = MRT_CANBUY_FAIRY;
					} else if (isIceTrapFlag(flag) == DYNFLAG_ICETRAP) {
						base = MRT_CANBUY_FAKEITEM;
					} else {
						// Kongs
						for (int i = 0; i < 5; i++) {
							if (flag == kong_flags[i]) {
								base = MRT_CANBUY_KONG;
							}
						}
						// Key
						for (int i = 0; i < 8; i++) {
							if (flag == getKeyFlag(i)) {
								base = MRT_CANBUY_KEY;
							}
						}
					}
				}
			}
		} else if (purchase_type == PURCHASE_GB) {
			base = MRT_CANBUY_BANANA;
		} else if ((purchase_type >= PURCHASE_ICEBUBBLE) && (purchase_type <= PURCHASE_ICESLOW)) {
			base = MRT_CANBUY_FAKEITEM;
		}
	}
	return (base * 3) + shop_owner;
}

int isGoodTextbox(int text_file, int text_index) {
	/**
	 * @brief Checks if a textbox is a hint textbox that should be replaced
	 * 
	 * @param text_file Original text file
	 * @param text_index Original Text index
	 * 
	 * @return Is textbox that can be replaced
	 */
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
	/**
	 * @brief Handler for getting the move hint
	 * 
	 * @param actor Vendor actor
	 * @param text_file Text file that is being used
	 * @param text_index Text index that's being used
	 */
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