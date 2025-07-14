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

static const unsigned char no_purchase_bases[] = {
	MRT_NOBUY_SPECIALMOVE,
	MRT_NOBUY_SPECIALMOVE,
	MRT_NOBUY_SPECIALMOVE,
	MRT_NOBUY_SLAM,
	MRT_NOBUY_GUN,
	MRT_NOBUY_GUNUPGRADE,
	MRT_NOBUY_GUNUPGRADE,
	MRT_NOBUY_AMMOBELT,
	MRT_NOBUY_INSTRUMENT,
	MRT_NOBUY_INSTRUMENT,
};

purchase_text_hint_struct purchase_hint_text_items[120] = {
	// Cranky
		// DK
		{.enough_coins = MRT_CANBUY_BBLAST, .not_enough_coins = MRT_NOBUY_SPECIALMOVE}, // DK
		{.enough_coins = MRT_CANBUY_SKONG, .not_enough_coins = MRT_NOBUY_SPECIALMOVE}, // DK
		{.enough_coins = MRT_CANBUY_GGRAB, .not_enough_coins = MRT_NOBUY_SPECIALMOVE}, // DK
		{.enough_coins = MRT_CANBUY_GGRAB, .not_enough_coins = MRT_NOBUY_SPECIALMOVE}, // DK
		{.enough_coins = MRT_CANBUY_SLAM, .not_enough_coins = MRT_NOBUY_SLAM}, // DK
		{.enough_coins = 0, .not_enough_coins = 0}, // DK
		{.enough_coins = MRT_CANBUY_SLAM, .not_enough_coins = MRT_NOBUY_SLAM}, // DK
		{.enough_coins = 0, .not_enough_coins = 0}, // DK
		// Diddy
		{.enough_coins = MRT_CANBUY_CCHARGE, .not_enough_coins = MRT_NOBUY_SPECIALMOVE}, // Diddy
		{.enough_coins = MRT_CANBUY_RBARREL, .not_enough_coins = MRT_NOBUY_SPECIALMOVE}, // Diddy
		{.enough_coins = MRT_CANBUY_SSPRING, .not_enough_coins = MRT_NOBUY_SPECIALMOVE}, // Diddy
		{.enough_coins = MRT_CANBUY_SSPRING, .not_enough_coins = MRT_NOBUY_SPECIALMOVE}, // Diddy
		{.enough_coins = MRT_CANBUY_SLAM, .not_enough_coins = MRT_NOBUY_SLAM}, // Diddy
		{.enough_coins = 0, .not_enough_coins = 0}, // Diddy
		{.enough_coins = MRT_CANBUY_SLAM, .not_enough_coins = MRT_NOBUY_SLAM}, // Diddy
		{.enough_coins = 0, .not_enough_coins = 0}, // Diddy
		// Lanky
		{.enough_coins = MRT_CANBUY_OSTAND, .not_enough_coins = MRT_NOBUY_SPECIALMOVE}, // Lanky
		{.enough_coins = MRT_CANBUY_OSTAND, .not_enough_coins = MRT_NOBUY_SPECIALMOVE}, // Lanky
		{.enough_coins = MRT_CANBUY_BBALLOON, .not_enough_coins = MRT_NOBUY_SPECIALMOVE}, // Lanky
		{.enough_coins = MRT_CANBUY_BBALLOON, .not_enough_coins = MRT_NOBUY_SPECIALMOVE}, // Lanky
		{.enough_coins = MRT_CANBUY_SLAM, .not_enough_coins = MRT_NOBUY_SLAM}, // Lanky
		{.enough_coins = MRT_CANBUY_OSPRINT, .not_enough_coins = MRT_NOBUY_SPECIALMOVE}, // Lanky
		{.enough_coins = MRT_CANBUY_SLAM, .not_enough_coins = MRT_NOBUY_SLAM}, // Lanky
		{.enough_coins = 0, .not_enough_coins = 0}, // Lanky
		// Tiny
		{.enough_coins = MRT_CANBUY_MMONKEY, .not_enough_coins = MRT_NOBUY_SPECIALMOVE}, // Tiny
		{.enough_coins = MRT_CANBUY_MMONKEY, .not_enough_coins = MRT_NOBUY_SPECIALMOVE}, // Tiny
		{.enough_coins = MRT_CANBUY_PTT, .not_enough_coins = MRT_NOBUY_SPECIALMOVE}, // Tiny
		{.enough_coins = MRT_CANBUY_PTT, .not_enough_coins = MRT_NOBUY_SPECIALMOVE}, // Tiny
		{.enough_coins = MRT_CANBUY_SLAM, .not_enough_coins = MRT_NOBUY_SLAM}, // Tiny
		{.enough_coins = MRT_CANBUY_MPORT, .not_enough_coins = MRT_NOBUY_SPECIALMOVE}, // Tiny
		{.enough_coins = MRT_CANBUY_SLAM, .not_enough_coins = MRT_NOBUY_SLAM}, // Tiny
		{.enough_coins = 0, .not_enough_coins = 0}, // Tiny
		// Japes
		{.enough_coins = MRT_CANBUY_HCHUNKY, .not_enough_coins = MRT_NOBUY_SPECIALMOVE}, // Chunky
		{.enough_coins = MRT_CANBUY_HCHUNKY, .not_enough_coins = MRT_NOBUY_SPECIALMOVE}, // Chunky
		{.enough_coins = MRT_CANBUY_PPUNCH, .not_enough_coins = MRT_NOBUY_SPECIALMOVE}, // Chunky
		{.enough_coins = MRT_CANBUY_PPUNCH, .not_enough_coins = MRT_NOBUY_SPECIALMOVE}, // Chunky
		{.enough_coins = MRT_CANBUY_SLAM, .not_enough_coins = MRT_NOBUY_SLAM}, // Chunky
		{.enough_coins = MRT_CANBUY_GGONE, .not_enough_coins = MRT_NOBUY_SPECIALMOVE}, // Chunky
		{.enough_coins = MRT_CANBUY_SLAM, .not_enough_coins = MRT_NOBUY_SLAM}, // Chunky
		{.enough_coins = 0, .not_enough_coins = 0}, // Chunky
	// Funky
		// DK
		{.enough_coins = MRT_CANBUY_COCONUT, .not_enough_coins = MRT_NOBUY_GUN}, // DK
		{.enough_coins = MRT_CANBUY_COCONUT, .not_enough_coins = MRT_NOBUY_GUN}, // DK
		{.enough_coins = MRT_CANBUY_AMMOBELT, .not_enough_coins = MRT_NOBUY_AMMOBELT}, // DK
		{.enough_coins = 0, .not_enough_coins = 0}, // DK
		{.enough_coins = MRT_CANBUY_HOMING, .not_enough_coins = MRT_NOBUY_GUNUPGRADE}, // DK
		{.enough_coins = MRT_CANBUY_AMMOBELT, .not_enough_coins = MRT_NOBUY_AMMOBELT}, // DK
		{.enough_coins = MRT_CANBUY_SNIPER, .not_enough_coins = MRT_NOBUY_GUNUPGRADE}, // DK
		{.enough_coins = 0, .not_enough_coins = 0}, // DK
		// Diddy
		{.enough_coins = MRT_CANBUY_PEANUT, .not_enough_coins = MRT_NOBUY_GUN}, // Diddy
		{.enough_coins = MRT_CANBUY_PEANUT, .not_enough_coins = MRT_NOBUY_GUN}, // Diddy
		{.enough_coins = MRT_CANBUY_AMMOBELT, .not_enough_coins = MRT_NOBUY_AMMOBELT}, // Diddy
		{.enough_coins = 0, .not_enough_coins = 0}, // Diddy
		{.enough_coins = MRT_CANBUY_HOMING, .not_enough_coins = MRT_NOBUY_GUNUPGRADE}, // Diddy
		{.enough_coins = MRT_CANBUY_AMMOBELT, .not_enough_coins = MRT_NOBUY_AMMOBELT}, // Diddy
		{.enough_coins = MRT_CANBUY_SNIPER, .not_enough_coins = MRT_NOBUY_GUNUPGRADE}, // Diddy
		{.enough_coins = 0, .not_enough_coins = 0}, // Diddy
		// Lanky
		{.enough_coins = MRT_CANBUY_GRAPE, .not_enough_coins = MRT_NOBUY_GUN}, // Lanky
		{.enough_coins = MRT_CANBUY_GRAPE, .not_enough_coins = MRT_NOBUY_GUN}, // Lanky
		{.enough_coins = MRT_CANBUY_AMMOBELT, .not_enough_coins = MRT_NOBUY_AMMOBELT}, // Lanky
		{.enough_coins = 0, .not_enough_coins = 0}, // Lanky
		{.enough_coins = MRT_CANBUY_HOMING, .not_enough_coins = MRT_NOBUY_GUNUPGRADE}, // Lanky
		{.enough_coins = MRT_CANBUY_AMMOBELT, .not_enough_coins = MRT_NOBUY_AMMOBELT}, // Lanky
		{.enough_coins = MRT_CANBUY_SNIPER, .not_enough_coins = MRT_NOBUY_GUNUPGRADE}, // Lanky
		{.enough_coins = 0, .not_enough_coins = 0}, // Lanky
		// Tiny
		{.enough_coins = MRT_CANBUY_FEATHER, .not_enough_coins = MRT_NOBUY_GUN}, // Tiny
		{.enough_coins = MRT_CANBUY_FEATHER, .not_enough_coins = MRT_NOBUY_GUN}, // Tiny
		{.enough_coins = MRT_CANBUY_AMMOBELT, .not_enough_coins = MRT_NOBUY_AMMOBELT}, // Tiny
		{.enough_coins = 0, .not_enough_coins = 0}, // Tiny
		{.enough_coins = MRT_CANBUY_HOMING, .not_enough_coins = MRT_NOBUY_GUNUPGRADE}, // Tiny
		{.enough_coins = MRT_CANBUY_AMMOBELT, .not_enough_coins = MRT_NOBUY_AMMOBELT}, // Tiny
		{.enough_coins = MRT_CANBUY_SNIPER, .not_enough_coins = MRT_NOBUY_GUNUPGRADE}, // Tiny
		{.enough_coins = 0, .not_enough_coins = 0}, // Tiny
		// Chunky
		{.enough_coins = MRT_CANBUY_PINEAPPLE, .not_enough_coins = MRT_NOBUY_GUN}, // Chunky
		{.enough_coins = MRT_CANBUY_PINEAPPLE, .not_enough_coins = MRT_NOBUY_GUN}, // Chunky
		{.enough_coins = MRT_CANBUY_AMMOBELT, .not_enough_coins = MRT_NOBUY_AMMOBELT}, // Chunky
		{.enough_coins = 0, .not_enough_coins = 0}, // Chunky
		{.enough_coins = MRT_CANBUY_HOMING, .not_enough_coins = MRT_NOBUY_GUNUPGRADE}, // Chunky
		{.enough_coins = MRT_CANBUY_AMMOBELT, .not_enough_coins = MRT_NOBUY_AMMOBELT}, // Chunky
		{.enough_coins = MRT_CANBUY_SNIPER, .not_enough_coins = MRT_NOBUY_GUNUPGRADE}, // Chunky
		{.enough_coins = 0, .not_enough_coins = 0}, // Chunky
	// Candy
		// DK
		{.enough_coins = MRT_CANBUY_BONGOS, .not_enough_coins = MRT_NOBUY_INSTRUMENT}, // DK
		{.enough_coins = MRT_CANBUY_BONGOS, .not_enough_coins = MRT_NOBUY_INSTRUMENT}, // DK
		{.enough_coins = MRT_CANBUY_BONGOS, .not_enough_coins = MRT_NOBUY_INSTRUMENT}, // DK
		{.enough_coins = MRT_CANBUY_INSTRUMENTUPGRADE, .not_enough_coins = MRT_NOBUY_INSTRUMENT}, // DK
		{.enough_coins = 0, .not_enough_coins = 0}, // DK
		{.enough_coins = MRT_CANBUY_INSTRUMENTUPGRADE, .not_enough_coins = MRT_NOBUY_INSTRUMENT}, // DK
		{.enough_coins = MRT_CANBUY_INSTRUMENTUPGRADE, .not_enough_coins = MRT_NOBUY_INSTRUMENT}, // DK
		{.enough_coins = 0, .not_enough_coins = 0}, // DK
		// Diddy
		{.enough_coins = MRT_CANBUY_GUITAR, .not_enough_coins = MRT_NOBUY_INSTRUMENT}, // Diddy
		{.enough_coins = MRT_CANBUY_GUITAR, .not_enough_coins = MRT_NOBUY_INSTRUMENT}, // Diddy
		{.enough_coins = MRT_CANBUY_GUITAR, .not_enough_coins = MRT_NOBUY_INSTRUMENT}, // Diddy
		{.enough_coins = MRT_CANBUY_INSTRUMENTUPGRADE, .not_enough_coins = MRT_NOBUY_INSTRUMENT}, // Diddy
		{.enough_coins = 0, .not_enough_coins = 0}, // Diddy
		{.enough_coins = MRT_CANBUY_INSTRUMENTUPGRADE, .not_enough_coins = MRT_NOBUY_INSTRUMENT}, // Diddy
		{.enough_coins = MRT_CANBUY_INSTRUMENTUPGRADE, .not_enough_coins = MRT_NOBUY_INSTRUMENT}, // Diddy
		{.enough_coins = 0, .not_enough_coins = 0}, // Diddy
		// Lanky
		{.enough_coins = MRT_CANBUY_TROMBONE, .not_enough_coins = MRT_NOBUY_INSTRUMENT}, // Lanky
		{.enough_coins = MRT_CANBUY_TROMBONE, .not_enough_coins = MRT_NOBUY_INSTRUMENT}, // Lanky
		{.enough_coins = MRT_CANBUY_TROMBONE, .not_enough_coins = MRT_NOBUY_INSTRUMENT}, // Lanky
		{.enough_coins = MRT_CANBUY_INSTRUMENTUPGRADE, .not_enough_coins = MRT_NOBUY_INSTRUMENT}, // Lanky
		{.enough_coins = 0, .not_enough_coins = 0}, // Lanky
		{.enough_coins = MRT_CANBUY_INSTRUMENTUPGRADE, .not_enough_coins = MRT_NOBUY_INSTRUMENT}, // Lanky
		{.enough_coins = MRT_CANBUY_INSTRUMENTUPGRADE, .not_enough_coins = MRT_NOBUY_INSTRUMENT}, // Lanky
		{.enough_coins = 0, .not_enough_coins = 0}, // Lanky
		// Tiny
		{.enough_coins = MRT_CANBUY_SAX, .not_enough_coins = MRT_NOBUY_INSTRUMENT}, // Tiny
		{.enough_coins = MRT_CANBUY_SAX, .not_enough_coins = MRT_NOBUY_INSTRUMENT}, // Tiny
		{.enough_coins = MRT_CANBUY_SAX, .not_enough_coins = MRT_NOBUY_INSTRUMENT}, // Tiny
		{.enough_coins = MRT_CANBUY_INSTRUMENTUPGRADE, .not_enough_coins = MRT_NOBUY_INSTRUMENT}, // Tiny
		{.enough_coins = 0, .not_enough_coins = 0}, // Tiny
		{.enough_coins = MRT_CANBUY_INSTRUMENTUPGRADE, .not_enough_coins = MRT_NOBUY_INSTRUMENT}, // Tiny
		{.enough_coins = MRT_CANBUY_INSTRUMENTUPGRADE, .not_enough_coins = MRT_NOBUY_INSTRUMENT}, // Tiny
		{.enough_coins = 0, .not_enough_coins = 0}, // Tiny
		// Chunky
		{.enough_coins = MRT_CANBUY_TRIANGLE, .not_enough_coins = MRT_NOBUY_INSTRUMENT}, // Chunky
		{.enough_coins = MRT_CANBUY_TRIANGLE, .not_enough_coins = MRT_NOBUY_INSTRUMENT}, // Chunky
		{.enough_coins = MRT_CANBUY_TRIANGLE, .not_enough_coins = MRT_NOBUY_INSTRUMENT}, // Chunky
		{.enough_coins = MRT_CANBUY_INSTRUMENTUPGRADE, .not_enough_coins = MRT_NOBUY_INSTRUMENT}, // Chunky
		{.enough_coins = 0, .not_enough_coins = 0}, // Chunky
		{.enough_coins = MRT_CANBUY_INSTRUMENTUPGRADE, .not_enough_coins = MRT_NOBUY_INSTRUMENT}, // Chunky
		{.enough_coins = MRT_CANBUY_INSTRUMENTUPGRADE, .not_enough_coins = MRT_NOBUY_INSTRUMENT}, // Chunky
		{.enough_coins = 0, .not_enough_coins = 0}, // Chunky
};


int getHintTextIndex(int shop_owner, shop_paad* shop_data) {
	/**
	 * @brief Get the text index in the text file for a certain hint
	 * 
	 * @param shop_owner Index of the shop owner (0 = Cranky, 1 = Funky, 2 = Candy)
	 * @param shop_data Shop data paad
	 * 
	 * @return text index
	 */
	int base = 0;
	int level = getWorld(CurrentMap, 1);
	purchase_text_hint_struct *data = &purchase_hint_text_items[(shop_owner * 40) + (Character * 8) + level];
	if (shop_data->price > MovesBase[(int)Character].coins) {
		base = data->not_enough_coins;
	} else {
		base = data->enough_coins;
	}
	return (base * 3) + shop_owner;
	// int purchase_type = shop_data->item_type;
	// int purchase_value = shop_data->item_level;
	// int base = 0;
	// int kong = shop_data->kong;
	// if (shop_data->price > MovesBase[(int)Character].coins) {
	// 	// Not enough money
	// 	base = MRT_NOBUY_ITEM;
	// 	switch (purchase_type) {
	// 		case REQITEM_MOVE:
	// 			if (purchase_value < 10) {
	// 				base = no_purchase_bases[purchase_value];
	// 			} else if (purchase_value == 10) {
	// 				if (kong < 4) {
	// 					base = MRT_NOBUY_TRAINING;
	// 				} else {
	// 					base = MRT_NOBUY_FAIRYMOVE;
	// 				}
	// 			}
	// 			break;
	// 		case REQITEM_GOLDENBANANA:
	// 			base = MRT_NOBUY_BANANA;
	// 			break;
	// 		case REQITEM_BLUEPRINT:
	// 			base = MRT_NOBUY_BLUEPRINT;
	// 			break;
	// 		case REQITEM_MEDAL:
	// 			base = MRT_NOBUY_MEDAL;
	// 			break;
	// 		case REQITEM_KONG:
	// 			base = MRT_NOBUY_KONG;
	// 			break;
	// 	}
	// } else {
	// 	// Enough money
	// 	switch (purchase_type) {
	// 		case REQITEM_MOVE:
	// 			switch (purchase_value) {
	// 				case 0:
	// 				case 1:
	// 				case 2:
	// 					base = MRT_CANBUY_BBLAST + (kong * 3) + purchase_value;
	// 					break;
	// 				case 3:
	// 					base = MRT_CANBUY_SLAM;
	// 					break;
	// 				case 4:
	// 					base = MRT_CANBUY_COCONUT + kong;
	// 					break;
	// 				case 5:
	// 				case 6:
	// 					base = MRT_CANBUY_HOMING + (purchase_value - 5);
	// 					break;
	// 				case 7:
	// 					base = MRT_CANBUY_AMMOBELT;
	// 					break;
	// 				case 8:
	// 					base = MRT_CANBUY_BONGOS + kong;
	// 					break;
	// 				case 9:
	// 					base = MRT_CANBUY_INSTRUMENTUPGRADE + getInstrumentLevel();
	// 					break;
	// 				case 10:
	// 					// kong = subindex
	// 					if (kong < 4) {
	// 						base = MRT_CANBUY_DIVE + kong;
	// 					} else {
	// 						base = MRT_CANBUY_CAMERA + (kong - 4);
	// 					}
	// 					break;
	// 				case 11:
	// 					base = MRT_CANBUY_CLIMB;
	// 					break;
	// 			}
	// 			break;
	// 		case REQITEM_GOLDENBANANA:
	// 			base = MRT_CANBUY_BANANA;
	// 			break;
	// 		case REQITEM_ICETRAP:
	// 			base = MRT_CANBUY_FAKEITEM;
	// 			break;
	// 		case REQITEM_KONG:
	// 			base = MRT_CANBUY_KONG;
	// 			break;
	// 		case REQITEM_KEY:
	// 			base = MRT_CANBUY_KEY;
	// 			break;
	// 		case REQITEM_BLUEPRINT:
	// 			base = MRT_CANBUY_BLUEPRINT;
	// 			break;
	// 		case REQITEM_HINT:
	// 			base = MRT_CANBUY_HINT;
	// 			break;
	// 		case REQITEM_MEDAL:
	// 			base = MRT_CANBUY_MEDAL;
	// 			break;
	// 		case REQITEM_COMPANYCOIN:
	// 			base = MRT_CANBUY_NINTENDO + kong;
	// 			break;
	// 		case REQITEM_CROWN:
	// 			base = MRT_CANBUY_CROWN;
	// 			break;
	// 		case REQITEM_BEAN:
	// 			base = MRT_CANBUY_BEAN;
	// 			break;
	// 		case REQITEM_PEARL:
	// 			base = MRT_CANBUY_PEARL;
	// 			break;
	// 		case REQITEM_FAIRY:
	// 			base = MRT_CANBUY_FAIRY;
	// 			break;
	// 	}
	// }
	// return (base * 3) + shop_owner;
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