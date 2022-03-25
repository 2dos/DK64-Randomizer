#include "../../include/common.h"

#define FUNKY 1
#define CRANKY 5
#define CANDY 0x19

#define PURCHASE_MOVES 0
#define PURCHASE_SLAM 1
#define PURCHASE_GUN 2
#define PURCHASE_AMMOBELT 3
#define PURCHASE_INSTRUMENT 4
#define PURCHASE_NOTHING -1

int getMoveType(int value) {
	int ret = (value >> 0x4) & 0xF;
	if (ret == 0xF) {
		return -1;
	} else {
		return ret;
	}
}

int getMoveIndex(int value) {
	if (((value >> 4) & 0xF) == 0xF) {
		return 0;
	} else {
		return value & 0xF;
	}
}

static char stored_slam_level = 0;

void replace_moves(void) {
	if (Rando.move_rando_on) {
		if ((CurrentMap == CRANKY) || (CurrentMap == FUNKY) || (CurrentMap == CANDY)) {
			int level = getWorld(CurrentMap,0);
			if (TransitionSpeed < 0) {
				if (level >= 0 && level < 7) {
					for (int i = 0; i < 7; i++) {
						CrankyMoves[0][i].purchase_type = getMoveType(Rando.dk_crankymoves[i]);
						CrankyMoves[0][i].purchase_value = getMoveIndex(Rando.dk_crankymoves[i]);
						CandyMoves[0][i].purchase_type = getMoveType(Rando.dk_candymoves[i]);
						CandyMoves[0][i].purchase_value = getMoveIndex(Rando.dk_candymoves[i]);
						FunkyMoves[0][i].purchase_type = getMoveType(Rando.dk_funkymoves[i]);
						FunkyMoves[0][i].purchase_value = getMoveIndex(Rando.dk_funkymoves[i]);

						CrankyMoves[1][i].purchase_type = getMoveType(Rando.diddy_crankymoves[i]);
						CrankyMoves[1][i].purchase_value = getMoveIndex(Rando.diddy_crankymoves[i]);
						CandyMoves[1][i].purchase_type = getMoveType(Rando.diddy_candymoves[i]);
						CandyMoves[1][i].purchase_value = getMoveIndex(Rando.diddy_candymoves[i]);
						FunkyMoves[1][i].purchase_type = getMoveType(Rando.diddy_funkymoves[i]);
						FunkyMoves[1][i].purchase_value = getMoveIndex(Rando.diddy_funkymoves[i]);

						CrankyMoves[2][i].purchase_type = getMoveType(Rando.lanky_crankymoves[i]);
						CrankyMoves[2][i].purchase_value = getMoveIndex(Rando.lanky_crankymoves[i]);
						CandyMoves[2][i].purchase_type = getMoveType(Rando.lanky_candymoves[i]);
						CandyMoves[2][i].purchase_value = getMoveIndex(Rando.lanky_candymoves[i]);
						FunkyMoves[2][i].purchase_type = getMoveType(Rando.lanky_funkymoves[i]);
						FunkyMoves[2][i].purchase_value = getMoveIndex(Rando.lanky_funkymoves[i]);

						CrankyMoves[3][i].purchase_type = getMoveType(Rando.tiny_crankymoves[i]);
						CrankyMoves[3][i].purchase_value = getMoveIndex(Rando.tiny_crankymoves[i]);
						CandyMoves[3][i].purchase_type = getMoveType(Rando.tiny_candymoves[i]);
						CandyMoves[3][i].purchase_value = getMoveIndex(Rando.tiny_candymoves[i]);
						FunkyMoves[3][i].purchase_type = getMoveType(Rando.tiny_funkymoves[i]);
						FunkyMoves[3][i].purchase_value = getMoveIndex(Rando.tiny_funkymoves[i]);

						CrankyMoves[4][i].purchase_type = getMoveType(Rando.chunky_crankymoves[i]);
						CrankyMoves[4][i].purchase_value = getMoveIndex(Rando.chunky_crankymoves[i]);
						CandyMoves[4][i].purchase_type = getMoveType(Rando.chunky_candymoves[i]);
						CandyMoves[4][i].purchase_value = getMoveIndex(Rando.chunky_candymoves[i]);
						FunkyMoves[4][i].purchase_type = getMoveType(Rando.chunky_funkymoves[i]);
						FunkyMoves[4][i].purchase_value = getMoveIndex(Rando.chunky_funkymoves[i]);
					}
				} else {
					for (int i = 0; i < 7; i++) {
						for (int j = 0; j < 5; j++) {
							CrankyMoves[j][i].purchase_type = -1;
							CrankyMoves[j][i].purchase_value = 0;
							CandyMoves[j][i].purchase_type = -1;
							CandyMoves[j][i].purchase_value = 0;
							FunkyMoves[j][i].purchase_type = -1;
							FunkyMoves[j][i].purchase_value = 0;
						}
					}
				}
			}
			if ((stored_slam_level == 1) && (MovesBase[0].simian_slam == 2)) {
				// Just purchased SSS
				int purchased = 0;
				if (level >= 0 && level < 7) {
					purchased = 1;
				}
				int shop = 0;
				if (CurrentMap == FUNKY) {
					shop = 1;
				} else if (CurrentMap == CANDY) {
					shop = 2;
				}
				StoredSettings.file_extra[(int)FileIndex].location_sss_purchased = (level << 4) | (purchased << 2) | shop;
				SaveToGlobal();
			}
			if (MovesBase[0].simian_slam > 1) {
				int encoded_sss_location = StoredSettings.file_extra[(int)FileIndex].location_sss_purchased;
				int shop = encoded_sss_location & 3;
				int purchased = (encoded_sss_location >> 2) & 1;
				int level = (encoded_sss_location >> 4) & 7;
				for (int i = 0; i < 7; i++) {
					for (int j = 0; j < 5; j++) {
						if (CrankyMoves[j][i].purchase_type == PURCHASE_SLAM) {
							if ((purchased) && (shop == 0) && (level == i)) {
								CrankyMoves[j][i].purchase_type = PURCHASE_NOTHING;
							} else {
								CrankyMoves[j][i].purchase_value = 3;
							}
						}
						if (CandyMoves[j][i].purchase_type == PURCHASE_SLAM) {
							if ((purchased) && (shop == 2) && (level == i)) {
								CrankyMoves[j][i].purchase_type = PURCHASE_NOTHING;
							} else {
								CrankyMoves[j][i].purchase_value = 3;
							}
						}
						if (FunkyMoves[j][i].purchase_type == PURCHASE_SLAM) {
							if ((purchased) && (shop == 1) && (level == i)) {
								CrankyMoves[j][i].purchase_type = PURCHASE_NOTHING;
							} else {
								CrankyMoves[j][i].purchase_value = 3;
							}
						}
					}
				}
			}
			stored_slam_level = MovesBase[0].simian_slam;
		}
	}
}

void cancelMoveSoftlock(void) {
	if (Rando.move_rando_on) {
		if ((CurrentMap == CRANKY) || (CurrentMap == FUNKY) || (CurrentMap == CANDY)) {
			if ((TBVoidByte & 0x30) == 0) {
				if ((CutsceneActive) && (CutsceneIndex == 2) && (CutsceneTimer == 80)) {
					CutsceneStateBitfield &= 0xFFCF;
				}
			}
		}
	}
}